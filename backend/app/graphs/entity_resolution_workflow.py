"""
LangGraph workflow for Entity Resolution - Batch Resume-Job Matching.

This workflow handles matching multiple resumes from an Excel file
against job requirements with scoring and entity resolution.
"""

import logging
from typing import Dict, Any, List, Optional
from langgraph.graph import StateGraph, END
from langchain_core.language_models import BaseChatModel

from .state import BatchRecruitmentState
from ..agents.job_analyzer import job_analyzer_node_sync
from ..agents.matcher import matcher_node_sync
from ..agents.parser import parser_node_sync
from ..graphs.state import create_initial_state

logger = logging.getLogger(__name__)


# ============================================================================
# ENTITY RESOLUTION STATE
# ============================================================================

class EntityResolutionState(Dict[str, Any]):
    """
    Enhanced state for entity resolution with batch processing.

    Fields:
        job_description: Job requirements text or dict
        candidates: List of candidate dictionaries from Excel
        analyzed_job: Structured job requirements
        match_results: List of match results
        ranked_candidates: Sorted candidates by score
        status: Workflow status
        current_index: Current processing index
        errors: List of errors
    """
    pass


# ============================================================================
# WORKFLOW NODES
# ============================================================================

def analyze_job_node(state: EntityResolutionState, llm: BaseChatModel) -> EntityResolutionState:
    """
    Analyze job requirements once for all candidates.

    Args:
        state: Current state
        llm: Language model

    Returns:
        Updated state with analyzed job
    """
    logger.info("EntityResolution: Analyzing job requirements...")

    try:
        job_desc = state.get("job_description", "")

        # If job is already analyzed (dict), skip
        if isinstance(state.get("analyzed_job"), dict):
            logger.info("Job already analyzed, skipping...")
            return state

        # Use recruitment state for job analysis
        temp_state = create_initial_state(
            resume_text="",  # Not needed for job analysis
            job_description=job_desc
        )

        # Analyze job
        analyzed_state = job_analyzer_node_sync(temp_state, llm)

        # Update entity resolution state
        state["analyzed_job"] = analyzed_state.get("analyzed_job")
        state["status"] = "job_analyzed"

        logger.info("Job analysis completed successfully")
        return state

    except Exception as e:
        logger.error(f"Job analysis failed: {e}")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append({
            "stage": "job_analysis",
            "error": str(e)
        })
        state["status"] = "failed"
        return state


def parse_candidates_node(state: EntityResolutionState, llm: BaseChatModel) -> EntityResolutionState:
    """
    Parse all candidate resumes into structured format.

    Args:
        state: Current state
        llm: Language model

    Returns:
        Updated state with parsed candidates
    """
    logger.info("EntityResolution: Parsing candidates...")

    try:
        candidates = state.get("candidates", [])
        parsed_candidates = []

        for idx, candidate in enumerate(candidates):
            logger.info(f"Parsing candidate {idx + 1}/{len(candidates)}: {candidate.get('name', 'Unknown')}")

            # If candidate already has structured data, use it
            if candidate.get("parsed_resume"):
                parsed_candidates.append(candidate)
                continue

            # Convert candidate dict to resume text for parsing
            resume_text = _candidate_dict_to_text(candidate)

            # Create temporary state for parsing
            temp_state = create_initial_state(
                resume_text=resume_text,
                job_description=""
            )

            # Parse resume
            parsed_state = parser_node_sync(temp_state, llm)

            # Add parsed data to candidate
            candidate["parsed_resume"] = parsed_state.get("parsed_resume")
            candidate["resume_text"] = resume_text
            parsed_candidates.append(candidate)

        state["candidates"] = parsed_candidates
        state["status"] = "candidates_parsed"

        logger.info(f"Successfully parsed {len(parsed_candidates)} candidates")
        return state

    except Exception as e:
        logger.error(f"Candidate parsing failed: {e}")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append({
            "stage": "candidate_parsing",
            "error": str(e)
        })
        state["status"] = "failed"
        return state


def match_candidates_node(state: EntityResolutionState, llm: BaseChatModel) -> EntityResolutionState:
    """
    Match all candidates against the job requirements.

    Args:
        state: Current state
        llm: Language model

    Returns:
        Updated state with match results
    """
    logger.info("EntityResolution: Matching candidates to job...")

    try:
        candidates = state.get("candidates", [])
        analyzed_job = state.get("analyzed_job")
        match_results = []

        if not analyzed_job:
            raise ValueError("Job requirements not analyzed")

        for idx, candidate in enumerate(candidates):
            logger.info(f"Matching candidate {idx + 1}/{len(candidates)}: {candidate.get('name', 'Unknown')}")

            # Get parsed resume
            parsed_resume = candidate.get("parsed_resume")
            if not parsed_resume:
                logger.warning(f"Candidate {candidate.get('name')} has no parsed resume, skipping...")
                continue

            # Create temporary state for matching
            temp_state = create_initial_state(
                resume_text=candidate.get("resume_text", ""),
                job_description=state.get("job_description", "")
            )
            temp_state["parsed_resume"] = parsed_resume
            temp_state["analyzed_job"] = analyzed_job

            # Match candidate
            matched_state = matcher_node_sync(temp_state, llm)

            # Store match result
            match_result = {
                "candidate": candidate,
                "match_data": matched_state.get("match_result"),
                "match_score": matched_state.get("match_score", 0),
                "confidence_scores": matched_state.get("confidence_scores", {}),
            }
            match_results.append(match_result)

        state["match_results"] = match_results
        state["status"] = "matching_complete"

        logger.info(f"Successfully matched {len(match_results)} candidates")
        return state

    except Exception as e:
        logger.error(f"Candidate matching failed: {e}")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append({
            "stage": "candidate_matching",
            "error": str(e)
        })
        state["status"] = "failed"
        return state


def rank_candidates_node(state: EntityResolutionState, llm: BaseChatModel) -> EntityResolutionState:
    """
    Rank and sort candidates by match score.

    Args:
        state: Current state
        llm: Language model (not used, but kept for consistency)

    Returns:
        Updated state with ranked candidates
    """
    logger.info("EntityResolution: Ranking candidates...")

    try:
        match_results = state.get("match_results", [])

        # Sort by match score (descending)
        ranked_results = sorted(
            match_results,
            key=lambda x: x.get("match_score", 0),
            reverse=True
        )

        # Add rank to each result
        for idx, result in enumerate(ranked_results):
            result["rank"] = idx + 1

        state["ranked_candidates"] = ranked_results
        state["status"] = "completed"

        logger.info(f"Ranked {len(ranked_results)} candidates")
        return state

    except Exception as e:
        logger.error(f"Candidate ranking failed: {e}")
        if "errors" not in state:
            state["errors"] = []
        state["errors"].append({
            "stage": "candidate_ranking",
            "error": str(e)
        })
        state["status"] = "failed"
        return state


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _candidate_dict_to_text(candidate: Dict[str, Any]) -> str:
    """
    Convert candidate dictionary to resume text for parsing.

    Args:
        candidate: Candidate dictionary from Excel

    Returns:
        Resume text representation
    """
    parts = []

    # Name
    if candidate.get("name"):
        parts.append(f"Name: {candidate['name']}")

    # Contact
    if candidate.get("email"):
        parts.append(f"Email: {candidate['email']}")
    if candidate.get("phone"):
        parts.append(f"Phone: {candidate['phone']}")
    if candidate.get("location"):
        parts.append(f"Location: {candidate['location']}")

    # Experience
    if candidate.get("exp_years"):
        parts.append(f"\nExperience: {candidate['exp_years']} years")

    # Skills
    if candidate.get("skill_set"):
        parts.append(f"\nSkills: {candidate['skill_set']}")

    # Domain
    if candidate.get("domain"):
        parts.append(f"\nDomain: {candidate['domain']}")

    # Previous roles
    if candidate.get("previous_roles"):
        parts.append(f"\nPrevious Roles: {candidate['previous_roles']}")

    # Education
    if candidate.get("education"):
        parts.append(f"\nEducation: {candidate['education']}")

    return "\n".join(parts)


# ============================================================================
# WORKFLOW BUILDER
# ============================================================================

def create_entity_resolution_workflow(llm: BaseChatModel) -> StateGraph:
    """
    Create the entity resolution workflow for batch candidate matching.

    Args:
        llm: Language model instance

    Returns:
        Compiled StateGraph
    """
    logger.info("Building entity resolution workflow...")

    # Create workflow
    workflow = StateGraph(EntityResolutionState)

    # Define nodes with LLM bound
    def analyze_job(state: EntityResolutionState) -> EntityResolutionState:
        return analyze_job_node(state, llm)

    def parse_candidates(state: EntityResolutionState) -> EntityResolutionState:
        return parse_candidates_node(state, llm)

    def match_candidates(state: EntityResolutionState) -> EntityResolutionState:
        return match_candidates_node(state, llm)

    def rank_candidates(state: EntityResolutionState) -> EntityResolutionState:
        return rank_candidates_node(state, llm)

    # Add nodes
    workflow.add_node("analyze_job", analyze_job)
    workflow.add_node("parse_candidates", parse_candidates)
    workflow.add_node("match_candidates", match_candidates)
    workflow.add_node("rank_candidates", rank_candidates)

    # Set entry point
    workflow.set_entry_point("analyze_job")

    # Define edges
    workflow.add_edge("analyze_job", "parse_candidates")
    workflow.add_edge("parse_candidates", "match_candidates")
    workflow.add_edge("match_candidates", "rank_candidates")
    workflow.add_edge("rank_candidates", END)

    logger.info("Entity resolution workflow built successfully")

    return workflow.compile()


# ============================================================================
# WORKFLOW EXECUTOR
# ============================================================================

class EntityResolutionWorkflow:
    """
    Wrapper class for executing entity resolution workflow.
    """

    def __init__(self, llm: BaseChatModel):
        """
        Initialize the workflow.

        Args:
            llm: Language model to use
        """
        self.llm = llm
        self.workflow = create_entity_resolution_workflow(llm)
        logger.info("Entity resolution workflow initialized")

    def run(
        self,
        job_description: str,
        candidates: List[Dict[str, Any]],
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Execute the workflow with job and candidates.

        Args:
            job_description: Job requirements text
            candidates: List of candidate dictionaries from Excel
            progress_callback: Optional callback for progress updates

        Returns:
            Final state with ranked candidates
        """
        logger.info(f"Starting entity resolution: {len(candidates)} candidates")

        # Create initial state
        initial_state: EntityResolutionState = {
            "job_description": job_description,
            "candidates": candidates,
            "analyzed_job": None,
            "match_results": [],
            "ranked_candidates": None,
            "status": "started",
            "current_index": 0,
            "errors": [],
        }

        # Execute workflow
        final_state = self.workflow.invoke(initial_state)

        logger.info(f"Workflow completed with status: {final_state.get('status')}")

        return final_state

    def run_single_match(
        self,
        job_description: str,
        candidate: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute workflow for single candidate.

        Args:
            job_description: Job requirements
            candidate: Single candidate dictionary

        Returns:
            Match result for the candidate
        """
        result = self.run(job_description, [candidate])

        if result.get("ranked_candidates"):
            return result["ranked_candidates"][0]

        return {
            "error": "Matching failed",
            "details": result.get("errors", [])
        }

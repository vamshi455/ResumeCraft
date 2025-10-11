"""
Matcher Agent - Matches candidates to job requirements.
"""

import logging
from typing import Dict, Any
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from ..prompts.base import CAREERCRAFT_SYSTEM_PROMPT
from ..prompts.matching import MATCH_CANDIDATE_TO_JOB_PROMPT
from ..prompts.utils import format_prompt, validate_json_response
from ..graphs.state import (
    RecruitmentState,
    update_state_status,
    add_error_to_state,
    add_confidence_score,
)

logger = logging.getLogger(__name__)


# ============================================================================
# MATCHER NODE
# ============================================================================


async def matcher_node(state: RecruitmentState, llm: BaseChatModel) -> RecruitmentState:
    """
    Matcher node that analyzes candidate-job fit and updates state.

    Args:
        state: Current recruitment state
        llm: Language model instance

    Returns:
        Updated state with match result
    """
    logger.info("Matcher Agent: Starting candidate-job matching...")

    # Update status
    state = update_state_status(state, "matching", "MatcherAgent")

    try:
        # Get parsed data from state
        parsed_resume = state.get("parsed_resume")
        analyzed_job = state.get("analyzed_job")

        if not parsed_resume:
            raise ValueError("No parsed resume available")
        if not analyzed_job:
            raise ValueError("No analyzed job available")

        # Format prompt
        import json
        prompt = format_prompt(
            MATCH_CANDIDATE_TO_JOB_PROMPT,
            candidate_json=json.dumps(parsed_resume, indent=2),
            job_json=json.dumps(analyzed_job, indent=2)
        )

        # Call LLM
        messages = [
            SystemMessage(content=CAREERCRAFT_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        response = await llm.ainvoke(messages)

        # Validate and parse JSON response
        match_data = validate_json_response(response.content)

        # Extract match score for confidence
        match_score = match_data.get("match_summary", {}).get("score", 0)

        # Update state
        state["match_result"] = match_data
        state["match_score"] = match_score
        state = add_confidence_score(state, "matcher", 95.0)  # High confidence in matching

        # Update status
        state = update_state_status(state, "matched", "MatcherAgent")

        logger.info(
            f"Matcher Agent: Successfully matched candidate. "
            f"Score: {match_score}/100, Level: {match_data.get('match_summary', {}).get('level')}"
        )

        return state

    except Exception as e:
        logger.error(f"Matcher Agent: Failed to match candidate: {e}")
        state = add_error_to_state(
            state,
            error=str(e),
            agent="MatcherAgent",
            severity="high",
        )
        state = update_state_status(state, "failed", "MatcherAgent")
        return state


def matcher_node_sync(state: RecruitmentState, llm: BaseChatModel) -> RecruitmentState:
    """
    Synchronous version of matcher node.

    Args:
        state: Current recruitment state
        llm: Language model instance

    Returns:
        Updated state with match result
    """
    logger.info("Matcher Agent: Starting candidate-job matching (sync)...")

    # Update status
    state = update_state_status(state, "matching", "MatcherAgent")

    try:
        # Get parsed data from state
        parsed_resume = state.get("parsed_resume")
        analyzed_job = state.get("analyzed_job")

        if not parsed_resume:
            raise ValueError("No parsed resume available")
        if not analyzed_job:
            raise ValueError("No analyzed job available")

        # Format prompt
        import json
        prompt = format_prompt(
            MATCH_CANDIDATE_TO_JOB_PROMPT,
            candidate_json=json.dumps(parsed_resume, indent=2),
            job_json=json.dumps(analyzed_job, indent=2)
        )

        # Call LLM (sync)
        messages = [
            SystemMessage(content=CAREERCRAFT_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        response = llm.invoke(messages)

        # Validate and parse JSON response
        match_data = validate_json_response(response.content)

        # Extract match score
        match_score = match_data.get("match_summary", {}).get("score", 0)

        # Update state
        state["match_result"] = match_data
        state["match_score"] = match_score
        state = add_confidence_score(state, "matcher", 95.0)

        # Update status
        state = update_state_status(state, "matched", "MatcherAgent")

        logger.info(
            f"Matcher Agent: Successfully matched candidate. "
            f"Score: {match_score}/100"
        )

        return state

    except Exception as e:
        logger.error(f"Matcher Agent: Failed to match candidate: {e}")
        state = add_error_to_state(
            state,
            error=str(e),
            agent="MatcherAgent",
            severity="high",
        )
        state = update_state_status(state, "failed", "MatcherAgent")
        return state


# ============================================================================
# CONDITIONAL EDGE FUNCTIONS
# ============================================================================


def should_enhance_resume(state: RecruitmentState) -> str:
    """
    Determine if resume should be enhanced based on match score.

    Args:
        state: Current state

    Returns:
        Next node name: "enhancer" or "qa_check"
    """
    match_score = state.get("match_score", 0)

    # Enhance if match score is below 90
    if match_score < 90:
        logger.info(f"Match score {match_score} < 90, routing to enhancer")
        return "enhancer"

    logger.info(f"Match score {match_score} >= 90, skipping enhancement")
    return "qa_check"


# ============================================================================
# AGENT CREATION
# ============================================================================


def create_matcher_agent(llm: BaseChatModel):
    """
    Create a matcher agent.

    Args:
        llm: Language model to use

    Returns:
        Matcher agent
    """
    return llm

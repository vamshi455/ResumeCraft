"""
LangGraph workflow for recruitment pipeline.
"""

import logging
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.language_models import BaseChatModel

from .state import RecruitmentState, create_initial_state
from ..agents.parser import parser_node_sync
from ..agents.job_analyzer import job_analyzer_node_sync
from ..agents.matcher import matcher_node_sync, should_enhance_resume
from ..agents.enhancer import enhancer_node_sync, should_retry_enhancement
from ..agents.qa import qa_node_sync, should_request_human_review
from ..agents.supervisor import (
    route_after_parsing,
    route_after_job_analysis,
    route_after_matching,
    route_after_enhancement,
    route_after_qa,
    generate_final_recommendation,
)

logger = logging.getLogger(__name__)


# ============================================================================
# WORKFLOW BUILDER
# ============================================================================


def create_recruitment_workflow(llm: BaseChatModel) -> StateGraph:
    """
    Create the recruitment workflow graph.

    Args:
        llm: Language model instance to use across all agents

    Returns:
        Compiled StateGraph
    """
    logger.info("Building recruitment workflow graph...")

    # Create the workflow
    workflow = StateGraph(RecruitmentState)

    # Define node functions with LLM bound
    def parser(state: RecruitmentState) -> RecruitmentState:
        return parser_node_sync(state, llm)

    def job_analyzer(state: RecruitmentState) -> RecruitmentState:
        return job_analyzer_node_sync(state, llm)

    def matcher(state: RecruitmentState) -> RecruitmentState:
        return matcher_node_sync(state, llm)

    def enhancer(state: RecruitmentState) -> RecruitmentState:
        return enhancer_node_sync(state, llm)

    def qa(state: RecruitmentState) -> RecruitmentState:
        return qa_node_sync(state, llm)

    def human_review_node(state: RecruitmentState) -> RecruitmentState:
        """Placeholder for human review - in production, this would wait for human input"""
        logger.info("Human review required - workflow paused")
        state["status"] = "human_review"
        return state

    def completion_node(state: RecruitmentState) -> RecruitmentState:
        """Final node that generates recommendation"""
        logger.info("Workflow completed, generating final recommendation")
        state["status"] = "completed"
        state["final_recommendation"] = generate_final_recommendation(state)
        return state

    # Add nodes to the workflow
    workflow.add_node("parser", parser)
    workflow.add_node("job_analyzer", job_analyzer)
    workflow.add_node("matcher", matcher)
    workflow.add_node("enhancer", enhancer)
    workflow.add_node("qa", qa)
    workflow.add_node("human_review", human_review_node)
    workflow.add_node("completed", completion_node)

    # Set entry point
    workflow.set_entry_point("parser")

    # Define edges
    # After parsing -> conditional route
    workflow.add_conditional_edges(
        "parser",
        route_after_parsing,
        {
            "job_analyzer": "job_analyzer",
            "human_review": "human_review",
            "end": END,
        }
    )

    # After job analysis -> matcher
    workflow.add_conditional_edges(
        "job_analyzer",
        route_after_job_analysis,
        {
            "matcher": "matcher",
            "end": END,
        }
    )

    # After matching -> conditional route
    workflow.add_conditional_edges(
        "matcher",
        route_after_matching,
        {
            "enhancer": "enhancer",
            "qa_check": "qa",
            "end": END,
        }
    )

    # After enhancement -> conditional retry or QA
    workflow.add_conditional_edges(
        "enhancer",
        route_after_enhancement,
        {
            "enhancer": "enhancer",  # Retry enhancement
            "qa_check": "qa",
        }
    )

    # After QA -> conditional route
    workflow.add_conditional_edges(
        "qa",
        route_after_qa,
        {
            "human_review": "human_review",
            "completed": "completed",
        }
    )

    # After human review -> end
    workflow.add_edge("human_review", END)

    # After completion -> end
    workflow.add_edge("completed", END)

    logger.info("Workflow graph built successfully")

    return workflow.compile()


# ============================================================================
# WORKFLOW EXECUTOR
# ============================================================================


class RecruitmentWorkflow:
    """
    Wrapper class for executing the recruitment workflow.
    """

    def __init__(self, llm: BaseChatModel):
        """
        Initialize the workflow.

        Args:
            llm: Language model to use
        """
        self.llm = llm
        self.workflow = create_recruitment_workflow(llm)
        logger.info("Recruitment workflow initialized")

    def run(
        self,
        resume_text: str,
        job_description: str = None,
    ) -> Dict[str, Any]:
        """
        Execute the workflow with given inputs.

        Args:
            resume_text: Raw resume text
            job_description: Optional job description

        Returns:
            Final state as dictionary
        """
        logger.info("Starting recruitment workflow execution...")

        # Create initial state
        initial_state = create_initial_state(resume_text, job_description)

        # Execute workflow
        final_state = self.workflow.invoke(initial_state)

        logger.info(f"Workflow completed with status: {final_state.get('status')}")

        return final_state

    def run_with_state(self, initial_state: RecruitmentState) -> Dict[str, Any]:
        """
        Execute workflow with custom initial state.

        Args:
            initial_state: Pre-configured state

        Returns:
            Final state as dictionary
        """
        logger.info("Starting recruitment workflow with custom state...")

        final_state = self.workflow.invoke(initial_state)

        logger.info(f"Workflow completed with status: {final_state.get('status')}")

        return final_state


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================


def parse_resume_only(llm: BaseChatModel, resume_text: str) -> Dict[str, Any]:
    """
    Parse a resume without job matching.

    Args:
        llm: Language model
        resume_text: Resume text

    Returns:
        Parsed resume data
    """
    workflow = RecruitmentWorkflow(llm)
    result = workflow.run(resume_text)

    return {
        "parsed_resume": result.get("parsed_resume"),
        "confidence_scores": result.get("confidence_scores"),
        "needs_review": result.get("needs_review"),
        "errors": result.get("errors", []),
    }


def match_candidate_to_job(
    llm: BaseChatModel,
    resume_text: str,
    job_description: str,
) -> Dict[str, Any]:
    """
    Parse resume and match to job without enhancement.

    Args:
        llm: Language model
        resume_text: Resume text
        job_description: Job description

    Returns:
        Match results
    """
    workflow = RecruitmentWorkflow(llm)
    result = workflow.run(resume_text, job_description)

    return {
        "parsed_resume": result.get("parsed_resume"),
        "analyzed_job": result.get("analyzed_job"),
        "match_result": result.get("match_result"),
        "match_score": result.get("match_score"),
        "final_recommendation": result.get("final_recommendation"),
        "errors": result.get("errors", []),
    }


def complete_workflow(
    llm: BaseChatModel,
    resume_text: str,
    job_description: str,
) -> Dict[str, Any]:
    """
    Run complete workflow including enhancement and QA.

    Args:
        llm: Language model
        resume_text: Resume text
        job_description: Job description

    Returns:
        Complete workflow results
    """
    workflow = RecruitmentWorkflow(llm)
    result = workflow.run(resume_text, job_description)

    return result

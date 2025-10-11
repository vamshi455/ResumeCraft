"""
Job Analyzer Agent - Analyzes job descriptions and extracts requirements.
"""

import logging
from typing import Dict, Any
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from ..prompts.base import CAREERCRAFT_SYSTEM_PROMPT, ANALYZE_JOB_DESCRIPTION_PROMPT
from ..prompts.utils import format_prompt, validate_json_response
from ..graphs.state import (
    RecruitmentState,
    update_state_status,
    add_error_to_state,
    add_confidence_score,
)

logger = logging.getLogger(__name__)


# ============================================================================
# JOB ANALYZER NODE
# ============================================================================


async def job_analyzer_node(state: RecruitmentState, llm: BaseChatModel) -> RecruitmentState:
    """
    Job analyzer node that processes job description and updates state.

    Args:
        state: Current recruitment state
        llm: Language model instance

    Returns:
        Updated state with analyzed job
    """
    logger.info("Job Analyzer Agent: Starting job description analysis...")

    # Update status
    state = update_state_status(state, "analyzing_job", "JobAnalyzerAgent")

    try:
        # Get job description from state
        job_description = state.get("job_description", "")

        if not job_description:
            raise ValueError("No job description provided")

        # Format prompt
        prompt = format_prompt(
            ANALYZE_JOB_DESCRIPTION_PROMPT,
            job_description=job_description
        )

        # Call LLM
        messages = [
            SystemMessage(content=CAREERCRAFT_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        response = await llm.ainvoke(messages)

        # Validate and parse JSON response
        analyzed_data = validate_json_response(response.content)

        # Calculate confidence (simple heuristic)
        confidence = 95.0  # High confidence for job analysis (typically accurate)

        # Check if essential fields are present
        if not analyzed_data.get("job_info") or not analyzed_data.get("requirements"):
            confidence = 60.0

        # Update state
        state["analyzed_job"] = analyzed_data
        state = add_confidence_score(state, "job_analyzer", confidence)

        # Update status
        state = update_state_status(state, "job_analyzed", "JobAnalyzerAgent")

        logger.info(
            f"Job Analyzer Agent: Successfully analyzed job. "
            f"Confidence: {confidence}%"
        )

        return state

    except Exception as e:
        logger.error(f"Job Analyzer Agent: Failed to analyze job: {e}")
        state = add_error_to_state(
            state,
            error=str(e),
            agent="JobAnalyzerAgent",
            severity="high",
        )
        state = update_state_status(state, "failed", "JobAnalyzerAgent")
        return state


def job_analyzer_node_sync(state: RecruitmentState, llm: BaseChatModel) -> RecruitmentState:
    """
    Synchronous version of job analyzer node.

    Args:
        state: Current recruitment state
        llm: Language model instance

    Returns:
        Updated state with analyzed job
    """
    logger.info("Job Analyzer Agent: Starting job description analysis (sync)...")

    # Update status
    state = update_state_status(state, "analyzing_job", "JobAnalyzerAgent")

    try:
        # Get job description from state
        job_description = state.get("job_description", "")

        if not job_description:
            raise ValueError("No job description provided")

        # Format prompt
        prompt = format_prompt(
            ANALYZE_JOB_DESCRIPTION_PROMPT,
            job_description=job_description
        )

        # Call LLM (sync)
        messages = [
            SystemMessage(content=CAREERCRAFT_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        response = llm.invoke(messages)

        # Validate and parse JSON response
        analyzed_data = validate_json_response(response.content)

        # Calculate confidence
        confidence = 95.0

        if not analyzed_data.get("job_info") or not analyzed_data.get("requirements"):
            confidence = 60.0

        # Update state
        state["analyzed_job"] = analyzed_data
        state = add_confidence_score(state, "job_analyzer", confidence)

        # Update status
        state = update_state_status(state, "job_analyzed", "JobAnalyzerAgent")

        logger.info(
            f"Job Analyzer Agent: Successfully analyzed job. "
            f"Confidence: {confidence}%"
        )

        return state

    except Exception as e:
        logger.error(f"Job Analyzer Agent: Failed to analyze job: {e}")
        state = add_error_to_state(
            state,
            error=str(e),
            agent="JobAnalyzerAgent",
            severity="high",
        )
        state = update_state_status(state, "failed", "JobAnalyzerAgent")
        return state


# ============================================================================
# AGENT CREATION
# ============================================================================


def create_job_analyzer_agent(llm: BaseChatModel):
    """
    Create a job analyzer agent.

    Args:
        llm: Language model to use

    Returns:
        Job analyzer agent
    """
    return llm

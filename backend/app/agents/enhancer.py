"""
Enhancer Agent - Enhances resumes based on job requirements and gap analysis.
"""

import logging
from typing import Dict, Any
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from ..prompts.base import CAREERCRAFT_SYSTEM_PROMPT
from ..prompts.enhancement import ENHANCE_RESUME_PROMPT
from ..prompts.utils import format_prompt, validate_json_response
from ..graphs.state import (
    RecruitmentState,
    update_state_status,
    add_error_to_state,
    add_confidence_score,
)

logger = logging.getLogger(__name__)


# ============================================================================
# ENHANCER NODE
# ============================================================================


async def enhancer_node(state: RecruitmentState, llm: BaseChatModel) -> RecruitmentState:
    """
    Enhancer node that improves resume and updates state.

    Args:
        state: Current recruitment state
        llm: Language model instance

    Returns:
        Updated state with enhanced resume
    """
    logger.info("Enhancer Agent: Starting resume enhancement...")

    # Update status
    state = update_state_status(state, "enhancing", "EnhancerAgent")

    try:
        # Get data from state
        parsed_resume = state.get("parsed_resume")
        analyzed_job = state.get("analyzed_job")
        match_result = state.get("match_result")

        if not parsed_resume:
            raise ValueError("No parsed resume available")
        if not analyzed_job:
            raise ValueError("No analyzed job available")
        if not match_result:
            raise ValueError("No match result available")

        # Extract gaps from match result
        gaps = match_result.get("gaps", [])

        # Format prompt
        import json
        prompt = format_prompt(
            ENHANCE_RESUME_PROMPT,
            candidate_json=json.dumps(parsed_resume, indent=2),
            job_json=json.dumps(analyzed_job, indent=2),
            gap_analysis=json.dumps(gaps, indent=2)
        )

        # Call LLM with higher temperature for creativity
        messages = [
            SystemMessage(content=CAREERCRAFT_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        response = await llm.ainvoke(messages)

        # Validate and parse JSON response
        enhanced_data = validate_json_response(response.content)

        # Update iteration count
        iterations = state.get("iterations", 0) + 1

        # Update state
        state["enhanced_resume"] = enhanced_data
        state["iterations"] = iterations
        state = add_confidence_score(state, "enhancer", 90.0)

        # Update status
        state = update_state_status(state, "enhanced", "EnhancerAgent")

        logger.info(
            f"Enhancer Agent: Successfully enhanced resume. "
            f"Iteration: {iterations}, "
            f"ATS Score: {enhanced_data.get('ats_score', {}).get('before')} → "
            f"{enhanced_data.get('ats_score', {}).get('after')}"
        )

        return state

    except Exception as e:
        logger.error(f"Enhancer Agent: Failed to enhance resume: {e}")
        state = add_error_to_state(
            state,
            error=str(e),
            agent="EnhancerAgent",
            severity="high",
        )
        state = update_state_status(state, "failed", "EnhancerAgent")
        return state


def enhancer_node_sync(state: RecruitmentState, llm: BaseChatModel) -> RecruitmentState:
    """
    Synchronous version of enhancer node.

    Args:
        state: Current recruitment state
        llm: Language model instance

    Returns:
        Updated state with enhanced resume
    """
    logger.info("Enhancer Agent: Starting resume enhancement (sync)...")

    # Update status
    state = update_state_status(state, "enhancing", "EnhancerAgent")

    try:
        # Get data from state
        parsed_resume = state.get("parsed_resume")
        analyzed_job = state.get("analyzed_job")
        match_result = state.get("match_result")

        if not parsed_resume:
            raise ValueError("No parsed resume available")
        if not analyzed_job:
            raise ValueError("No analyzed job available")
        if not match_result:
            raise ValueError("No match result available")

        # Extract gaps
        gaps = match_result.get("gaps", [])

        # Format prompt
        import json
        prompt = format_prompt(
            ENHANCE_RESUME_PROMPT,
            candidate_json=json.dumps(parsed_resume, indent=2),
            job_json=json.dumps(analyzed_job, indent=2),
            gap_analysis=json.dumps(gaps, indent=2)
        )

        # Call LLM (sync)
        messages = [
            SystemMessage(content=CAREERCRAFT_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        response = llm.invoke(messages)

        # Validate and parse JSON response
        enhanced_data = validate_json_response(response.content)

        # Update iteration count
        iterations = state.get("iterations", 0) + 1

        # Update state
        state["enhanced_resume"] = enhanced_data
        state["iterations"] = iterations
        state = add_confidence_score(state, "enhancer", 90.0)

        # Update status
        state = update_state_status(state, "enhanced", "EnhancerAgent")

        logger.info(
            f"Enhancer Agent: Successfully enhanced resume. Iteration: {iterations}"
        )

        return state

    except Exception as e:
        logger.error(f"Enhancer Agent: Failed to enhance resume: {e}")
        state = add_error_to_state(
            state,
            error=str(e),
            agent="EnhancerAgent",
            severity="high",
        )
        state = update_state_status(state, "failed", "EnhancerAgent")
        return state


# ============================================================================
# CONDITIONAL EDGE FUNCTIONS
# ============================================================================


def should_retry_enhancement(state: RecruitmentState) -> str:
    """
    Determine if enhancement should be retried.

    Args:
        state: Current state

    Returns:
        Next node name: "enhancer" or "qa_check"
    """
    iterations = state.get("iterations", 0)
    max_iterations = 3

    if iterations < max_iterations:
        # Check if enhancement improved ATS score significantly
        enhanced = state.get("enhanced_resume", {})
        ats_before = enhanced.get("ats_score", {}).get("before", 0)
        ats_after = enhanced.get("ats_score", {}).get("after", 0)

        if ats_after < 85 and (ats_after - ats_before) > 5:
            logger.info(f"ATS score {ats_after} < 85, retrying enhancement")
            return "enhancer"

    logger.info(f"Enhancement complete after {iterations} iterations")
    return "qa_check"


# ============================================================================
# AGENT CREATION
# ============================================================================


def create_enhancer_agent(llm: BaseChatModel):
    """
    Create an enhancer agent.

    Args:
        llm: Language model to use

    Returns:
        Enhancer agent
    """
    return llm

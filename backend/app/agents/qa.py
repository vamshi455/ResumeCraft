"""
QA Agent - Quality assurance for enhanced resumes.
"""

import logging
from typing import Dict, Any
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from ..prompts.base import CAREERCRAFT_SYSTEM_PROMPT
from ..prompts.enhancement import QA_ENHANCED_RESUME_PROMPT
from ..prompts.utils import format_prompt, validate_json_response
from ..graphs.state import (
    RecruitmentState,
    update_state_status,
    add_error_to_state,
    add_confidence_score,
)

logger = logging.getLogger(__name__)


# ============================================================================
# QA NODE
# ============================================================================


async def qa_node(state: RecruitmentState, llm: BaseChatModel) -> RecruitmentState:
    """
    QA node that validates enhanced resume and updates state.

    Args:
        state: Current recruitment state
        llm: Language model instance

    Returns:
        Updated state with QA result
    """
    logger.info("QA Agent: Starting quality assurance check...")

    # Update status
    state = update_state_status(state, "qa_check", "QAAgent")

    try:
        # Get data from state
        parsed_resume = state.get("parsed_resume")
        enhanced_resume = state.get("enhanced_resume")

        if not parsed_resume:
            raise ValueError("No parsed resume available")
        if not enhanced_resume:
            # If no enhancement, skip QA
            logger.info("QA Agent: No enhanced resume, skipping QA")
            state = update_state_status(state, "qa_passed", "QAAgent")
            return state

        # Format prompt
        import json
        prompt = format_prompt(
            QA_ENHANCED_RESUME_PROMPT,
            original_json=json.dumps(parsed_resume, indent=2),
            enhanced_json=json.dumps(enhanced_resume, indent=2)
        )

        # Call LLM with low temperature for consistency
        messages = [
            SystemMessage(content=CAREERCRAFT_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        response = await llm.ainvoke(messages)

        # Validate and parse JSON response
        qa_data = validate_json_response(response.content)

        # Extract approval status
        approval = qa_data.get("approval", {})
        status = approval.get("status", "rejected")

        # Update state
        state["qa_result"] = qa_data
        state = add_confidence_score(state, "qa", 95.0)

        # Update status based on approval
        if status == "approved":
            state = update_state_status(state, "qa_passed", "QAAgent")
            logger.info("QA Agent: Enhanced resume approved")
        else:
            state = update_state_status(state, "qa_failed", "QAAgent")
            logger.warning(f"QA Agent: Enhanced resume rejected - {approval.get('reason')}")

        return state

    except Exception as e:
        logger.error(f"QA Agent: Failed quality check: {e}")
        state = add_error_to_state(
            state,
            error=str(e),
            agent="QAAgent",
            severity="medium",
        )
        state = update_state_status(state, "failed", "QAAgent")
        return state


def qa_node_sync(state: RecruitmentState, llm: BaseChatModel) -> RecruitmentState:
    """
    Synchronous version of QA node.

    Args:
        state: Current recruitment state
        llm: Language model instance

    Returns:
        Updated state with QA result
    """
    logger.info("QA Agent: Starting quality assurance check (sync)...")

    # Update status
    state = update_state_status(state, "qa_check", "QAAgent")

    try:
        # Get data from state
        parsed_resume = state.get("parsed_resume")
        enhanced_resume = state.get("enhanced_resume")

        if not parsed_resume:
            raise ValueError("No parsed resume available")
        if not enhanced_resume:
            logger.info("QA Agent: No enhanced resume, skipping QA")
            state = update_state_status(state, "qa_passed", "QAAgent")
            return state

        # Format prompt
        import json
        prompt = format_prompt(
            QA_ENHANCED_RESUME_PROMPT,
            original_json=json.dumps(parsed_resume, indent=2),
            enhanced_json=json.dumps(enhanced_resume, indent=2)
        )

        # Call LLM (sync)
        messages = [
            SystemMessage(content=CAREERCRAFT_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        response = llm.invoke(messages)

        # Validate and parse JSON response
        qa_data = validate_json_response(response.content)

        # Extract approval status
        approval = qa_data.get("approval", {})
        status = approval.get("status", "rejected")

        # Update state
        state["qa_result"] = qa_data
        state = add_confidence_score(state, "qa", 95.0)

        # Update status based on approval
        if status == "approved":
            state = update_state_status(state, "qa_passed", "QAAgent")
            logger.info("QA Agent: Enhanced resume approved")
        else:
            state = update_state_status(state, "qa_failed", "QAAgent")
            logger.warning(f"QA Agent: Enhanced resume rejected")

        return state

    except Exception as e:
        logger.error(f"QA Agent: Failed quality check: {e}")
        state = add_error_to_state(
            state,
            error=str(e),
            agent="QAAgent",
            severity="medium",
        )
        state = update_state_status(state, "failed", "QAAgent")
        return state


# ============================================================================
# CONDITIONAL EDGE FUNCTIONS
# ============================================================================


def should_request_human_review(state: RecruitmentState) -> str:
    """
    Determine if enhanced resume needs human review.

    Args:
        state: Current state

    Returns:
        Next node name: "human_review" or "completed"
    """
    qa_result = state.get("qa_result", {})
    approval = qa_result.get("approval", {})
    status = approval.get("status", "rejected")

    if status == "needs_review":
        logger.info("QA flagged for human review")
        return "human_review"

    if status == "rejected":
        issues = qa_result.get("issues", [])
        critical_issues = [i for i in issues if i.get("severity") == "critical"]
        if critical_issues:
            logger.info(f"QA found {len(critical_issues)} critical issues, requesting review")
            return "human_review"

    logger.info("QA passed, marking as completed")
    return "completed"


# ============================================================================
# AGENT CREATION
# ============================================================================


def create_qa_agent(llm: BaseChatModel):
    """
    Create a QA agent.

    Args:
        llm: Language model to use

    Returns:
        QA agent
    """
    return llm

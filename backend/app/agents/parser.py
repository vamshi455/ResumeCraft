"""
Resume Parser Agent - Extracts structured data from resumes.
"""

import logging
from typing import Dict, Any
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

from ..prompts.base import CAREERCRAFT_SYSTEM_PROMPT, PARSE_RESUME_PROMPT
from ..prompts.utils import format_prompt, validate_json_response
from ..graphs.state import (
    RecruitmentState,
    update_state_status,
    add_error_to_state,
    add_confidence_score,
    flag_for_review,
)

logger = logging.getLogger(__name__)


# ============================================================================
# PARSER TOOL
# ============================================================================


@tool
def parse_resume_tool(resume_text: str) -> Dict[str, Any]:
    """
    Parse resume text and extract structured information.

    Args:
        resume_text: Raw resume text

    Returns:
        Structured resume data
    """
    # This is a placeholder - actual implementation will use LLM
    # The real implementation is in the node function below
    return {"status": "tool_placeholder"}


# ============================================================================
# PARSER AGENT
# ============================================================================


def create_parser_agent(llm: BaseChatModel):
    """
    Create a parser agent that extracts structured data from resumes.

    Args:
        llm: Language model to use

    Returns:
        Parser agent
    """
    # For LangGraph, we'll use the node function directly
    # This function is here for potential future multi-agent setups
    return llm


# ============================================================================
# PARSER NODE
# ============================================================================


async def parser_node(state: RecruitmentState, llm: BaseChatModel) -> RecruitmentState:
    """
    Parser node that processes resume and updates state.

    Args:
        state: Current recruitment state
        llm: Language model instance

    Returns:
        Updated state with parsed resume
    """
    logger.info("Parser Agent: Starting resume parsing...")

    # Update status
    state = update_state_status(state, "parsing", "ParserAgent")

    try:
        # Get resume text from state
        resume_text = state.get("resume_text", "")

        if not resume_text:
            raise ValueError("No resume text provided")

        # Format prompt
        prompt = format_prompt(PARSE_RESUME_PROMPT, resume_text=resume_text)

        # Call LLM
        messages = [
            SystemMessage(content=CAREERCRAFT_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        response = await llm.ainvoke(messages)

        # Validate and parse JSON response
        parsed_data = validate_json_response(response.content)

        # Extract confidence score
        confidence = parsed_data.get("confidence", {}).get("overall", 0)

        # Update state
        state["parsed_resume"] = parsed_data
        state = add_confidence_score(state, "parser", confidence)

        # Flag low confidence fields for review
        needs_review = parsed_data.get("confidence", {}).get("needs_review", [])
        if needs_review and isinstance(needs_review, list):
            for field in needs_review:
                state = flag_for_review(state, field)

        # Update status
        state = update_state_status(state, "parsed", "ParserAgent")

        logger.info(
            f"Parser Agent: Successfully parsed resume. "
            f"Confidence: {confidence}%, Needs review: {needs_review}"
        )

        return state

    except Exception as e:
        logger.error(f"Parser Agent: Failed to parse resume: {e}")
        state = add_error_to_state(
            state,
            error=str(e),
            agent="ParserAgent",
            severity="high",
        )
        state = update_state_status(state, "failed", "ParserAgent")
        return state


def parser_node_sync(state: RecruitmentState, llm: BaseChatModel) -> RecruitmentState:
    """
    Synchronous version of parser node for compatibility.

    Args:
        state: Current recruitment state
        llm: Language model instance

    Returns:
        Updated state with parsed resume
    """
    logger.info("Parser Agent: Starting resume parsing (sync)...")

    # Update status
    state = update_state_status(state, "parsing", "ParserAgent")

    try:
        # Get resume text from state
        resume_text = state.get("resume_text", "")

        if not resume_text:
            raise ValueError("No resume text provided")

        # Format prompt
        prompt = format_prompt(PARSE_RESUME_PROMPT, resume_text=resume_text)

        # Call LLM (sync)
        messages = [
            SystemMessage(content=CAREERCRAFT_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        response = llm.invoke(messages)

        # Validate and parse JSON response
        parsed_data = validate_json_response(response.content)

        # Extract confidence score
        confidence = parsed_data.get("confidence", {}).get("overall", 0)

        # Update state
        state["parsed_resume"] = parsed_data
        state = add_confidence_score(state, "parser", confidence)

        # Flag low confidence fields for review
        needs_review = parsed_data.get("confidence", {}).get("needs_review", [])
        if needs_review and isinstance(needs_review, list):
            for field in needs_review:
                state = flag_for_review(state, field)

        # Update status
        state = update_state_status(state, "parsed", "ParserAgent")

        logger.info(
            f"Parser Agent: Successfully parsed resume. "
            f"Confidence: {confidence}%, Needs review: {needs_review}"
        )

        return state

    except Exception as e:
        logger.error(f"Parser Agent: Failed to parse resume: {e}")
        state = add_error_to_state(
            state,
            error=str(e),
            agent="ParserAgent",
            severity="high",
        )
        state = update_state_status(state, "failed", "ParserAgent")
        return state


# ============================================================================
# CONDITIONAL EDGE FUNCTIONS
# ============================================================================


def should_review_parsing(state: RecruitmentState) -> str:
    """
    Determine if parsed resume needs human review.

    Args:
        state: Current state

    Returns:
        Next node name: "human_review" or "job_analyzer"
    """
    # Check confidence score
    confidence = state.get("confidence_scores", {}).get("parser", 0)

    if confidence < 70:
        logger.info(f"Parser confidence low ({confidence}%), routing to human review")
        return "human_review"

    # Check if any fields flagged for review
    needs_review = state.get("needs_review", [])
    if needs_review:
        logger.info(f"Fields flagged for review: {needs_review}, routing to human review")
        return "human_review"

    logger.info(f"Parser confidence high ({confidence}%), proceeding to job analyzer")
    return "job_analyzer"

"""
Supervisor Agent - Orchestrates the recruitment workflow.
"""

import logging
from typing import Dict, Any, Literal
from langchain_core.language_models import BaseChatModel

from ..graphs.state import (
    RecruitmentState,
    update_state_status,
    get_overall_confidence,
)

logger = logging.getLogger(__name__)


# ============================================================================
# SUPERVISOR AGENT
# ============================================================================


def create_supervisor_agent(llm: BaseChatModel):
    """
    Create a supervisor agent for workflow orchestration.

    Args:
        llm: Language model to use

    Returns:
        Supervisor agent
    """
    return llm


def supervisor_node(state: RecruitmentState) -> RecruitmentState:
    """
    Supervisor node that makes routing decisions.

    Args:
        state: Current recruitment state

    Returns:
        Updated state with routing decision
    """
    logger.info("Supervisor: Evaluating workflow state...")

    current_status = state.get("status", "started")
    overall_confidence = get_overall_confidence(state)

    logger.info(
        f"Supervisor: Current status={current_status}, "
        f"Overall confidence={overall_confidence}%"
    )

    # State is already managed by individual agents
    # Supervisor just logs and monitors
    state["updated_at"] = state.get("updated_at", "")

    return state


# ============================================================================
# ROUTING FUNCTIONS
# ============================================================================


def route_after_parsing(state: RecruitmentState) -> Literal["job_analyzer", "human_review", "end"]:
    """
    Route workflow after resume parsing.

    Args:
        state: Current state

    Returns:
        Next node name
    """
    confidence = state.get("confidence_scores", {}).get("parser", 0)
    needs_review = state.get("needs_review", [])

    # Check if we have a job description to analyze FIRST
    # If we have a job, proceed with matching even if confidence is low
    job_desc = state.get("job_description")
    logger.info(f"Job description: {job_desc[:50] if job_desc else 'None'}...")

    if job_desc and job_desc.strip():
        # We have a job to match against, proceed even if confidence is lower
        if confidence < 50:  # Only stop for very low confidence
            logger.info(f"Very low parsing confidence ({confidence}%), routing to human review")
            return "human_review"

        logger.info(f"Job description provided (confidence: {confidence}%), proceeding to job analysis")
        return "job_analyzer"

    # No job description - apply stricter review criteria
    if confidence < 70:
        logger.info(f"Low parsing confidence ({confidence}%), routing to human review")
        return "human_review"

    if needs_review:
        logger.info(f"Fields flagged for review: {needs_review}, routing to human review")
        return "human_review"

    logger.info("No job description, ending workflow")
    return "end"


def route_after_job_analysis(state: RecruitmentState) -> Literal["matcher", "end"]:
    """
    Route workflow after job analysis.

    Args:
        state: Current state

    Returns:
        Next node name
    """
    analyzed_job = state.get("analyzed_job")

    if not analyzed_job:
        logger.warning("Job analysis failed, ending workflow")
        return "end"

    logger.info("Job analyzed successfully, proceeding to matching")
    return "matcher"


def route_after_matching(state: RecruitmentState) -> Literal["enhancer", "qa_check", "end"]:
    """
    Route workflow after candidate-job matching.

    Args:
        state: Current state

    Returns:
        Next node name
    """
    match_score = state.get("match_score", 0)

    # If match score is excellent, skip enhancement
    if match_score >= 90:
        logger.info(f"Excellent match score ({match_score}), skipping enhancement")
        return "qa_check"

    # If match score is very poor, don't enhance
    if match_score < 40:
        logger.info(f"Poor match score ({match_score}), ending workflow")
        return "end"

    # Otherwise, enhance the resume
    logger.info(f"Match score {match_score}, proceeding to enhancement")
    return "enhancer"


def route_after_enhancement(state: RecruitmentState) -> Literal["enhancer", "qa_check"]:
    """
    Route workflow after resume enhancement.

    Args:
        state: Current state

    Returns:
        Next node name
    """
    iterations = state.get("iterations", 0)
    max_iterations = 3

    # Check if we should retry enhancement
    if iterations < max_iterations:
        enhanced = state.get("enhanced_resume", {})
        ats_before = enhanced.get("ats_score", {}).get("before", 0)
        ats_after = enhanced.get("ats_score", {}).get("after", 0)

        # Retry if improvement is significant but score still low
        if ats_after < 85 and (ats_after - ats_before) > 5:
            logger.info(f"ATS score {ats_after} < 85, retrying enhancement (iteration {iterations})")
            return "enhancer"

    logger.info(f"Enhancement complete after {iterations} iterations, proceeding to QA")
    return "qa_check"


def route_after_qa(state: RecruitmentState) -> Literal["human_review", "completed"]:
    """
    Route workflow after QA check.

    Args:
        state: Current state

    Returns:
        Next node name
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


def route_from_human_review(state: RecruitmentState) -> Literal["enhancer", "completed", "rejected"]:
    """
    Route workflow after human review.

    Args:
        state: Current state

    Returns:
        Next node name
    """
    human_action = state.get("human_action")

    if human_action == "approve":
        logger.info("Human approved, completing workflow")
        return "completed"

    if human_action == "reject":
        logger.info("Human rejected, ending workflow")
        return "rejected"

    if human_action == "revise":
        iterations = state.get("iterations", 0)
        if iterations < 3:
            logger.info("Human requested revision, retrying enhancement")
            return "enhancer"
        else:
            logger.info("Max iterations reached, completing with human feedback")
            return "completed"

    # Default: mark as completed
    logger.info("No human action specified, completing workflow")
    return "completed"


# ============================================================================
# FINAL RECOMMENDATION
# ============================================================================


def generate_final_recommendation(state: RecruitmentState) -> str:
    """
    Generate final hiring recommendation based on workflow results.

    Args:
        state: Final state

    Returns:
        Recommendation text
    """
    match_score = state.get("match_score", 0)
    match_result = state.get("match_result", {})
    overall_confidence = get_overall_confidence(state)

    match_level = match_result.get("match_summary", {}).get("level", "unknown")
    recommendation = match_result.get("match_summary", {}).get("recommendation", "unknown")

    if match_score >= 85 and overall_confidence >= 80:
        return (
            f"STRONG HIRE: Candidate shows {match_level} match ({match_score}%) "
            f"with high confidence ({overall_confidence}%). {recommendation}"
        )
    elif match_score >= 70:
        return (
            f"CONSIDER: Candidate shows {match_level} match ({match_score}%). "
            f"Review gaps and consider for interview. {recommendation}"
        )
    elif match_score >= 50:
        return (
            f"WEAK MATCH: Candidate has moderate fit ({match_score}%). "
            f"Significant gaps exist. Consider only if candidate pool is limited."
        )
    else:
        return (
            f"NOT RECOMMENDED: Poor match ({match_score}%). "
            f"Candidate does not meet key requirements."
        )

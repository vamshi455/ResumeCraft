"""
State management for LangGraph recruitment workflows.
Defines the shared state that flows through all agents.
"""

from typing import TypedDict, Optional, List, Dict, Any, Literal
from datetime import datetime


# ============================================================================
# CORE STATE DEFINITIONS
# ============================================================================


class RecruitmentState(TypedDict, total=False):
    """
    Main state object that flows through the recruitment workflow.

    This state is shared across all agents and persists through checkpoints.
    Each agent reads from and writes to this state.
    """

    # ===== Input Data =====
    resume_text: str
    """Raw resume text input"""

    job_description: str
    """Raw job description text"""

    # ===== Parsed Data =====
    parsed_resume: Optional[Dict[str, Any]]
    """Structured resume data from ParserAgent"""

    analyzed_job: Optional[Dict[str, Any]]
    """Structured job requirements from JobAnalyzerAgent"""

    # ===== Analysis Results =====
    match_result: Optional[Dict[str, Any]]
    """Candidate-job match analysis from MatcherAgent"""

    enhanced_resume: Optional[Dict[str, Any]]
    """Enhanced resume from EnhancerAgent"""

    qa_result: Optional[Dict[str, Any]]
    """Quality assurance results from QAAgent"""

    # ===== Confidence & Metadata =====
    confidence_scores: Dict[str, float]
    """Confidence scores for each step (0-100)"""

    needs_review: List[str]
    """Fields flagged for human review"""

    # ===== Workflow Control =====
    status: Literal[
        "started",
        "parsing",
        "parsed",
        "analyzing_job",
        "job_analyzed",
        "matching",
        "matched",
        "enhancing",
        "enhanced",
        "qa_check",
        "qa_passed",
        "qa_failed",
        "human_review",
        "approved",
        "rejected",
        "completed",
        "failed"
    ]
    """Current workflow status"""

    current_agent: Optional[str]
    """Name of currently executing agent"""

    iterations: int
    """Number of enhancement iterations (max 3)"""

    # ===== Human Feedback =====
    human_feedback: Optional[str]
    """Feedback from human reviewer"""

    human_action: Optional[Literal["approve", "reject", "revise"]]
    """Action taken by human reviewer"""

    # ===== Error Handling =====
    errors: List[Dict[str, Any]]
    """List of errors encountered"""

    retry_count: int
    """Number of retries for current step"""

    # ===== Timestamps =====
    created_at: str
    """Workflow start timestamp"""

    updated_at: str
    """Last update timestamp"""

    # ===== Final Output =====
    final_recommendation: Optional[str]
    """Final hiring recommendation"""

    match_score: Optional[float]
    """Overall match score (0-100)"""


# ============================================================================
# BATCH PROCESSING STATE
# ============================================================================


class BatchRecruitmentState(TypedDict, total=False):
    """
    State for batch processing multiple candidates against one job.
    """

    job_description: str
    """Job description to match against"""

    analyzed_job: Optional[Dict[str, Any]]
    """Analyzed job requirements"""

    resumes: List[str]
    """List of resume texts"""

    candidates: List[Dict[str, Any]]
    """Parsed candidate profiles"""

    match_results: List[Dict[str, Any]]
    """Individual match results"""

    ranked_candidates: Optional[List[Dict[str, Any]]]
    """Candidates ranked by match score"""

    comparative_analysis: Optional[Dict[str, Any]]
    """Comparative analysis across all candidates"""

    status: Literal["started", "processing", "completed", "failed"]
    """Batch processing status"""

    processed_count: int
    """Number of candidates processed"""

    total_count: int
    """Total number of candidates"""


# ============================================================================
# STATE INITIALIZATION HELPERS
# ============================================================================


def create_initial_state(resume_text: str, job_description: Optional[str] = None) -> RecruitmentState:
    """
    Create initial recruitment state.

    Args:
        resume_text: Raw resume text
        job_description: Optional raw job description

    Returns:
        Initialized RecruitmentState
    """
    now = datetime.utcnow().isoformat()

    return RecruitmentState(
        resume_text=resume_text,
        job_description=job_description or "",  # Convert None to empty string
        parsed_resume=None,
        analyzed_job=None,
        match_result=None,
        enhanced_resume=None,
        qa_result=None,
        confidence_scores={},
        needs_review=[],
        status="started",
        current_agent=None,
        iterations=0,
        human_feedback=None,
        human_action=None,
        errors=[],
        retry_count=0,
        created_at=now,
        updated_at=now,
        final_recommendation=None,
        match_score=None,
    )


def create_batch_state(
    job_description: str,
    resumes: List[str]
) -> BatchRecruitmentState:
    """
    Create initial batch processing state.

    Args:
        job_description: Job description to match against
        resumes: List of resume texts

    Returns:
        Initialized BatchRecruitmentState
    """
    return BatchRecruitmentState(
        job_description=job_description,
        analyzed_job=None,
        resumes=resumes,
        candidates=[],
        match_results=[],
        ranked_candidates=None,
        comparative_analysis=None,
        status="started",
        processed_count=0,
        total_count=len(resumes),
    )


# ============================================================================
# STATE UPDATE HELPERS
# ============================================================================


def update_state_status(
    state: RecruitmentState,
    status: str,
    current_agent: Optional[str] = None,
) -> RecruitmentState:
    """
    Update state status and timestamp.

    Args:
        state: Current state
        status: New status
        current_agent: Name of current agent

    Returns:
        Updated state
    """
    state["status"] = status
    state["updated_at"] = datetime.utcnow().isoformat()

    if current_agent:
        state["current_agent"] = current_agent

    return state


def add_error_to_state(
    state: RecruitmentState,
    error: str,
    agent: str,
    severity: Literal["low", "medium", "high", "critical"] = "medium",
) -> RecruitmentState:
    """
    Add error to state.

    Args:
        state: Current state
        error: Error message
        agent: Agent that encountered error
        severity: Error severity

    Returns:
        Updated state
    """
    if "errors" not in state:
        state["errors"] = []

    state["errors"].append({
        "error": error,
        "agent": agent,
        "severity": severity,
        "timestamp": datetime.utcnow().isoformat(),
    })

    state["updated_at"] = datetime.utcnow().isoformat()

    return state


def increment_retry(state: RecruitmentState) -> RecruitmentState:
    """
    Increment retry counter.

    Args:
        state: Current state

    Returns:
        Updated state
    """
    state["retry_count"] = state.get("retry_count", 0) + 1
    state["updated_at"] = datetime.utcnow().isoformat()

    return state


def reset_retry(state: RecruitmentState) -> RecruitmentState:
    """
    Reset retry counter.

    Args:
        state: Current state

    Returns:
        Updated state
    """
    state["retry_count"] = 0
    state["updated_at"] = datetime.utcnow().isoformat()

    return state


def add_confidence_score(
    state: RecruitmentState,
    agent: str,
    score: float,
) -> RecruitmentState:
    """
    Add confidence score for an agent.

    Args:
        state: Current state
        agent: Agent name
        score: Confidence score (0-100)

    Returns:
        Updated state
    """
    if "confidence_scores" not in state:
        state["confidence_scores"] = {}

    state["confidence_scores"][agent] = score
    state["updated_at"] = datetime.utcnow().isoformat()

    return state


def flag_for_review(
    state: RecruitmentState,
    field: str,
) -> RecruitmentState:
    """
    Flag a field for human review.

    Args:
        state: Current state
        field: Field name to flag

    Returns:
        Updated state
    """
    if "needs_review" not in state:
        state["needs_review"] = []

    if field not in state["needs_review"]:
        state["needs_review"].append(field)

    state["updated_at"] = datetime.utcnow().isoformat()

    return state


# ============================================================================
# STATE VALIDATION
# ============================================================================


def validate_state(state: RecruitmentState) -> tuple[bool, List[str]]:
    """
    Validate state has required fields for workflow progression.

    Args:
        state: State to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Check required initial fields
    if not state.get("resume_text"):
        errors.append("Missing resume_text")
    if not state.get("job_description"):
        errors.append("Missing job_description")

    # Check status is valid
    if state.get("status") not in [
        "started", "parsing", "parsed", "analyzing_job", "job_analyzed",
        "matching", "matched", "enhancing", "enhanced", "qa_check",
        "qa_passed", "qa_failed", "human_review", "approved", "rejected",
        "completed", "failed"
    ]:
        errors.append(f"Invalid status: {state.get('status')}")

    return len(errors) == 0, errors


def get_overall_confidence(state: RecruitmentState) -> float:
    """
    Calculate overall confidence score from all agents.

    Args:
        state: Current state

    Returns:
        Average confidence score (0-100)
    """
    scores = state.get("confidence_scores", {})

    if not scores:
        return 0.0

    return sum(scores.values()) / len(scores)

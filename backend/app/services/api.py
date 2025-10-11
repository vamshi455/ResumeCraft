"""
FastAPI service layer for ResumeCraft backend.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime
import os

from langchain_openai import ChatOpenAI

from ..graphs.workflow import RecruitmentWorkflow, parse_resume_only, match_candidate_to_job, complete_workflow
from ..graphs.state import create_initial_state

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ResumeCraft API",
    description="AI-powered resume management and candidate matching",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# PYDANTIC MODELS
# ============================================================================


class ParseResumeRequest(BaseModel):
    """Request model for resume parsing"""
    resume_text: str = Field(..., description="Raw resume text")


class MatchRequest(BaseModel):
    """Request model for candidate-job matching"""
    resume_text: str = Field(..., description="Raw resume text")
    job_description: str = Field(..., description="Job description text")


class EnhanceRequest(BaseModel):
    """Request model for resume enhancement"""
    resume_text: str = Field(..., description="Raw resume text")
    job_description: str = Field(..., description="Job description text")


class WorkflowResponse(BaseModel):
    """Response model for workflow results"""
    status: str
    data: Dict[str, Any]
    errors: List[str] = []
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_llm(temperature: float = 0.1) -> ChatOpenAI:
    """
    Get configured LLM instance.

    Args:
        temperature: Temperature for LLM

    Returns:
        ChatOpenAI instance
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    return ChatOpenAI(
        model="gpt-4-turbo-preview",
        temperature=temperature,
        api_key=api_key,
    )


def extract_text_from_upload(file: UploadFile) -> str:
    """
    Extract text from uploaded file.

    Args:
        file: Uploaded file

    Returns:
        Extracted text

    Raises:
        HTTPException: If file type is unsupported
    """
    # For now, assume text files only
    # TODO: Add PDF/DOCX parsing
    content = file.file.read()

    try:
        text = content.decode("utf-8")
        return text
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Unable to decode file. Please upload a text file."
        )


# ============================================================================
# HEALTH CHECK
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ResumeCraft API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    }


# ============================================================================
# RESUME PARSING
# ============================================================================


@app.post("/api/v1/parse", response_model=WorkflowResponse)
async def parse_resume(request: ParseResumeRequest):
    """
    Parse a resume and extract structured data.

    Args:
        request: Parse request with resume text

    Returns:
        Parsed resume data
    """
    logger.info("Received resume parsing request")

    try:
        llm = get_llm(temperature=0.0)  # Deterministic for parsing

        result = parse_resume_only(llm, request.resume_text)

        return WorkflowResponse(
            status="success",
            data=result,
            errors=result.get("errors", []),
        )

    except Exception as e:
        logger.error(f"Error parsing resume: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse resume: {str(e)}"
        )


@app.post("/api/v1/parse/upload")
async def parse_resume_upload(file: UploadFile = File(...)):
    """
    Parse a resume from uploaded file.

    Args:
        file: Uploaded resume file

    Returns:
        Parsed resume data
    """
    logger.info(f"Received file upload: {file.filename}")

    try:
        # Extract text from file
        resume_text = extract_text_from_upload(file)

        # Parse resume
        llm = get_llm(temperature=0.0)
        result = parse_resume_only(llm, resume_text)

        return WorkflowResponse(
            status="success",
            data=result,
            errors=result.get("errors", []),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing upload: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process upload: {str(e)}"
        )


# ============================================================================
# CANDIDATE-JOB MATCHING
# ============================================================================


@app.post("/api/v1/match", response_model=WorkflowResponse)
async def match_candidate(request: MatchRequest):
    """
    Match a candidate to a job description.

    Args:
        request: Match request with resume and job description

    Returns:
        Match results with score and analysis
    """
    logger.info("Received candidate matching request")

    try:
        llm = get_llm(temperature=0.1)  # Low temperature for consistency

        result = match_candidate_to_job(
            llm,
            request.resume_text,
            request.job_description,
        )

        return WorkflowResponse(
            status="success",
            data=result,
            errors=result.get("errors", []),
        )

    except Exception as e:
        logger.error(f"Error matching candidate: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to match candidate: {str(e)}"
        )


# ============================================================================
# RESUME ENHANCEMENT
# ============================================================================


@app.post("/api/v1/enhance", response_model=WorkflowResponse)
async def enhance_resume(request: EnhanceRequest):
    """
    Enhance a resume for a specific job.

    Args:
        request: Enhancement request with resume and job description

    Returns:
        Enhanced resume with improvements
    """
    logger.info("Received resume enhancement request")

    try:
        llm = get_llm(temperature=0.3)  # Higher temperature for creativity

        result = complete_workflow(
            llm,
            request.resume_text,
            request.job_description,
        )

        return WorkflowResponse(
            status="success",
            data=result,
            errors=result.get("errors", []),
        )

    except Exception as e:
        logger.error(f"Error enhancing resume: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to enhance resume: {str(e)}"
        )


# ============================================================================
# WORKFLOW EXECUTION
# ============================================================================


@app.post("/api/v1/workflow/execute", response_model=WorkflowResponse)
async def execute_workflow(request: EnhanceRequest):
    """
    Execute the complete recruitment workflow.

    Args:
        request: Workflow request with resume and job description

    Returns:
        Complete workflow results
    """
    logger.info("Received workflow execution request")

    try:
        llm = get_llm()

        workflow = RecruitmentWorkflow(llm)
        result = workflow.run(
            request.resume_text,
            request.job_description,
        )

        return WorkflowResponse(
            status="success",
            data=result,
            errors=result.get("errors", []),
        )

    except Exception as e:
        logger.error(f"Error executing workflow: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute workflow: {str(e)}"
        )


# ============================================================================
# ERROR HANDLERS
# ============================================================================


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "timestamp": datetime.utcnow().isoformat(),
        }
    )


# ============================================================================
# STARTUP / SHUTDOWN
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("ResumeCraft API starting up...")
    # Initialize any resources here


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("ResumeCraft API shutting down...")
    # Cleanup resources here


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

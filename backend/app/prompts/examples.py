"""
Example usage and integration patterns for CareerCraft prompts.
Demonstrates how to use the prompts with different LLM providers.
"""

import json
from typing import Dict, Any, List, Optional
import logging

from .base import (
    CAREERCRAFT_SYSTEM_PROMPT,
    PARSE_RESUME_PROMPT,
    ANALYZE_JOB_DESCRIPTION_PROMPT,
    NORMALIZE_SKILLS_PROMPT,
)
from .matching import MATCH_CANDIDATE_TO_JOB_PROMPT, BATCH_MATCH_CANDIDATES_PROMPT
from .enhancement import ENHANCE_RESUME_PROMPT, QA_ENHANCED_RESUME_PROMPT
from .chat import CAREERCRAFT_CHAT_PROMPT
from .config import LLMProvider, get_llm_config, estimate_cost
from .utils import (
    format_prompt,
    format_json_for_prompt,
    validate_json_response,
    safe_llm_call,
)

logger = logging.getLogger(__name__)


# ============================================================================
# OPENAI IMPLEMENTATION EXAMPLES
# ============================================================================


def parse_resume_openai(resume_text: str, api_key: str) -> Dict[str, Any]:
    """
    Parse resume using OpenAI GPT-4.

    Args:
        resume_text: Raw resume text
        api_key: OpenAI API key

    Returns:
        Parsed resume data

    Example:
        >>> resume_text = "John Doe\\nSoftware Engineer\\n..."
        >>> result = parse_resume_openai(resume_text, api_key="sk-...")
        >>> print(result['personal_info']['full_name'])
        'John Doe'
    """
    try:
        import openai

        openai.api_key = api_key
        config = get_llm_config(LLMProvider.OPENAI, task="parsing")

        response = openai.ChatCompletion.create(
            model=config.model,
            messages=[
                {"role": "system", "content": CAREERCRAFT_SYSTEM_PROMPT},
                {"role": "user", "content": format_prompt(PARSE_RESUME_PROMPT, resume_text=resume_text)},
            ],
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            response_format=config.response_format,
        )

        return validate_json_response(response.choices[0].message.content)

    except Exception as e:
        logger.error(f"Resume parsing failed: {e}")
        raise


def match_candidate_openai(
    candidate_json: Dict[str, Any],
    job_json: Dict[str, Any],
    api_key: str,
) -> Dict[str, Any]:
    """
    Match candidate to job using OpenAI.

    Args:
        candidate_json: Parsed candidate profile
        job_json: Analyzed job description
        api_key: OpenAI API key

    Returns:
        Matching analysis with scores

    Example:
        >>> candidate = {"personal_info": {...}, "skills": {...}}
        >>> job = {"job_info": {...}, "requirements": {...}}
        >>> match = match_candidate_openai(candidate, job, api_key="sk-...")
        >>> print(match['match_summary']['score'])
        85
    """
    try:
        import openai

        openai.api_key = api_key
        config = get_llm_config(LLMProvider.OPENAI, task="matching")

        prompt = format_prompt(
            MATCH_CANDIDATE_TO_JOB_PROMPT,
            candidate_json=format_json_for_prompt(candidate_json),
            job_json=format_json_for_prompt(job_json),
        )

        response = openai.ChatCompletion.create(
            model=config.model,
            messages=[
                {"role": "system", "content": CAREERCRAFT_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            response_format=config.response_format,
        )

        return validate_json_response(response.choices[0].message.content)

    except Exception as e:
        logger.error(f"Candidate matching failed: {e}")
        raise


def enhance_resume_openai(
    candidate_json: Dict[str, Any],
    job_json: Dict[str, Any],
    gap_analysis: Dict[str, Any],
    api_key: str,
) -> Dict[str, Any]:
    """
    Enhance resume for job alignment using OpenAI.

    Args:
        candidate_json: Parsed candidate profile
        job_json: Analyzed job description
        gap_analysis: Gap analysis from matching
        api_key: OpenAI API key

    Returns:
        Enhanced resume with change tracking

    Example:
        >>> enhanced = enhance_resume_openai(candidate, job, gaps, api_key="sk-...")
        >>> print(enhanced['ats_score']['after'])
        92
    """
    try:
        import openai

        openai.api_key = api_key
        config = get_llm_config(LLMProvider.OPENAI, task="enhancement")

        prompt = format_prompt(
            ENHANCE_RESUME_PROMPT,
            candidate_json=format_json_for_prompt(candidate_json),
            job_json=format_json_for_prompt(job_json),
            gap_analysis=format_json_for_prompt(gap_analysis),
        )

        response = openai.ChatCompletion.create(
            model=config.model,
            messages=[
                {"role": "system", "content": CAREERCRAFT_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            response_format=config.response_format,
        )

        return validate_json_response(response.choices[0].message.content)

    except Exception as e:
        logger.error(f"Resume enhancement failed: {e}")
        raise


# ============================================================================
# ANTHROPIC IMPLEMENTATION EXAMPLES
# ============================================================================


def parse_resume_anthropic(resume_text: str, api_key: str) -> Dict[str, Any]:
    """
    Parse resume using Anthropic Claude.

    Args:
        resume_text: Raw resume text
        api_key: Anthropic API key

    Returns:
        Parsed resume data
    """
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        config = get_llm_config(LLMProvider.ANTHROPIC, task="parsing")

        message = client.messages.create(
            model=config.model,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            system=CAREERCRAFT_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": format_prompt(PARSE_RESUME_PROMPT, resume_text=resume_text)}
            ],
        )

        return validate_json_response(message.content[0].text)

    except Exception as e:
        logger.error(f"Resume parsing failed (Anthropic): {e}")
        raise


# ============================================================================
# BATCH PROCESSING EXAMPLES
# ============================================================================


def batch_match_candidates(
    candidates: List[Dict[str, Any]],
    job_json: Dict[str, Any],
    api_key: str,
    provider: LLMProvider = LLMProvider.OPENAI,
) -> Dict[str, Any]:
    """
    Match multiple candidates against a job description.

    Args:
        candidates: List of parsed candidate profiles
        job_json: Analyzed job description
        api_key: API key for the provider
        provider: LLM provider to use

    Returns:
        Ranked candidates with comparative analysis

    Example:
        >>> candidates = [candidate1, candidate2, candidate3]
        >>> job = {...}
        >>> results = batch_match_candidates(candidates, job, api_key="sk-...")
        >>> top_candidate = results['ranked_candidates'][0]
        >>> print(f"{top_candidate['name']}: {top_candidate['overall_score']}")
    """
    try:
        if provider == LLMProvider.OPENAI:
            import openai

            openai.api_key = api_key
            config = get_llm_config(provider, task="matching")

            prompt = format_prompt(
                BATCH_MATCH_CANDIDATES_PROMPT,
                job_json=format_json_for_prompt(job_json),
                candidates_json=format_json_for_prompt(candidates),
            )

            response = openai.ChatCompletion.create(
                model=config.model,
                messages=[
                    {"role": "system", "content": CAREERCRAFT_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                response_format=config.response_format,
            )

            return validate_json_response(response.choices[0].message.content)

    except Exception as e:
        logger.error(f"Batch matching failed: {e}")
        raise


# ============================================================================
# COMPLETE WORKFLOW EXAMPLES
# ============================================================================


def complete_candidate_workflow(
    resume_text: str,
    job_description: str,
    api_key: str,
    enhance: bool = False,
) -> Dict[str, Any]:
    """
    Complete workflow: Parse → Analyze → Match → (Optional) Enhance.

    Args:
        resume_text: Raw resume text
        job_description: Raw job description
        api_key: OpenAI API key
        enhance: Whether to enhance the resume

    Returns:
        Complete analysis including parsing, matching, and optional enhancement

    Example:
        >>> result = complete_candidate_workflow(
        ...     resume_text="John Doe...",
        ...     job_description="We're looking for...",
        ...     api_key="sk-...",
        ...     enhance=True
        ... )
        >>> print(f"Match Score: {result['matching']['match_summary']['score']}")
        >>> print(f"ATS Score: {result['enhancement']['ats_score']['after']}")
    """
    workflow_result = {}

    try:
        # Step 1: Parse resume
        logger.info("Parsing resume...")
        candidate_json = parse_resume_openai(resume_text, api_key)
        workflow_result["candidate"] = candidate_json

        # Step 2: Analyze job description
        logger.info("Analyzing job description...")
        import openai

        openai.api_key = api_key
        config = get_llm_config(LLMProvider.OPENAI, task="parsing")

        response = openai.ChatCompletion.create(
            model=config.model,
            messages=[
                {"role": "system", "content": CAREERCRAFT_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": format_prompt(ANALYZE_JOB_DESCRIPTION_PROMPT, job_description=job_description),
                },
            ],
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            response_format=config.response_format,
        )

        job_json = validate_json_response(response.choices[0].message.content)
        workflow_result["job"] = job_json

        # Step 3: Match candidate to job
        logger.info("Matching candidate to job...")
        matching_result = match_candidate_openai(candidate_json, job_json, api_key)
        workflow_result["matching"] = matching_result

        # Step 4: Enhance resume (optional)
        if enhance:
            logger.info("Enhancing resume...")
            gap_analysis = matching_result.get("gaps", {})
            enhancement_result = enhance_resume_openai(candidate_json, job_json, gap_analysis, api_key)
            workflow_result["enhancement"] = enhancement_result

        logger.info("Workflow completed successfully")
        return workflow_result

    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        workflow_result["error"] = str(e)
        return workflow_result


# ============================================================================
# CHAT INTERFACE EXAMPLE
# ============================================================================


def chat_with_careercraft(
    user_message: str,
    conversation_history: List[Dict[str, str]],
    api_key: str,
    resume_count: int = 0,
    job_count: int = 0,
    recent_activity: str = "None",
) -> str:
    """
    Chat with CareerCraft AI assistant.

    Args:
        user_message: User's message
        conversation_history: Previous conversation messages
        api_key: OpenAI API key
        resume_count: Number of resumes in database
        job_count: Number of active jobs
        recent_activity: Recent activity description

    Returns:
        Assistant's response

    Example:
        >>> history = []
        >>> response = chat_with_careercraft(
        ...     "How do I upload a resume?",
        ...     history,
        ...     api_key="sk-..."
        ... )
        >>> print(response)
        >>> history.append({"role": "user", "content": "How do I upload a resume?"})
        >>> history.append({"role": "assistant", "content": response})
    """
    try:
        import openai

        openai.api_key = api_key
        config = get_llm_config(LLMProvider.OPENAI, task="chat")

        # Format conversation history
        history_text = "\n".join(
            [f"{msg['role'].upper()}: {msg['content']}" for msg in conversation_history]
        )

        prompt = format_prompt(
            CAREERCRAFT_CHAT_PROMPT,
            conversation_history=history_text,
            user_message=user_message,
            resume_count=resume_count,
            job_count=job_count,
            recent_activity=recent_activity,
        )

        messages = [{"role": "system", "content": CAREERCRAFT_SYSTEM_PROMPT}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model=config.model,
            messages=messages,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Chat failed: {e}")
        return f"I apologize, but I encountered an error: {str(e)}"


# ============================================================================
# COST ESTIMATION EXAMPLE
# ============================================================================


def estimate_workflow_cost(
    resume_length: int,
    job_description_length: int,
    enhance: bool = False,
    model: str = "gpt-4-turbo-preview",
) -> Dict[str, Any]:
    """
    Estimate the cost of running a complete workflow.

    Args:
        resume_length: Length of resume in characters
        job_description_length: Length of job description in characters
        enhance: Whether enhancement is included
        model: Model to use for estimation

    Returns:
        Cost breakdown

    Example:
        >>> cost = estimate_workflow_cost(
        ...     resume_length=2000,
        ...     job_description_length=1000,
        ...     enhance=True
        ... )
        >>> print(f"Total cost: ${cost['total']:.4f}")
    """
    # Rough token estimation: 1 token ≈ 4 characters
    resume_tokens = resume_length // 4
    job_tokens = job_description_length // 4

    costs = {}

    # Parsing
    parsing_input = len(PARSE_RESUME_PROMPT) // 4 + resume_tokens
    parsing_output = 2000  # Estimated output tokens
    costs["parsing"] = estimate_cost(model, parsing_input, parsing_output)

    # Job analysis
    job_input = len(ANALYZE_JOB_DESCRIPTION_PROMPT) // 4 + job_tokens
    job_output = 1500
    costs["job_analysis"] = estimate_cost(model, job_input, job_output)

    # Matching
    matching_input = len(MATCH_CANDIDATE_TO_JOB_PROMPT) // 4 + resume_tokens + job_tokens
    matching_output = 1500
    costs["matching"] = estimate_cost(model, matching_input, matching_output)

    # Enhancement (optional)
    if enhance:
        enhancement_input = len(ENHANCE_RESUME_PROMPT) // 4 + resume_tokens + job_tokens
        enhancement_output = 3000
        costs["enhancement"] = estimate_cost(model, enhancement_input, enhancement_output)

    costs["total"] = sum(costs.values())

    return costs

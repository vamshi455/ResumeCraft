"""
Utility functions for LLM calls and response processing.
"""

import json
import logging
from typing import Dict, Any, Optional, Callable, List
from functools import wraps
import time

logger = logging.getLogger(__name__)


# ============================================================================
# PROMPT FORMATTING
# ============================================================================


def format_prompt(template: str, **kwargs: Any) -> str:
    """
    Format a prompt template with provided variables.

    Args:
        template: The prompt template string
        **kwargs: Variables to substitute in the template

    Returns:
        Formatted prompt string
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        logger.error(f"Missing template variable: {e}")
        raise ValueError(f"Missing required prompt variable: {e}")


def format_json_for_prompt(data: Dict[str, Any], indent: int = 2) -> str:
    """
    Format dictionary as JSON string for inclusion in prompts.

    Args:
        data: Dictionary to format
        indent: Number of spaces for indentation

    Returns:
        JSON string
    """
    return json.dumps(data, indent=indent, ensure_ascii=False)


# ============================================================================
# RESPONSE VALIDATION
# ============================================================================


def validate_json_response(response: str) -> Dict[str, Any]:
    """
    Validate and parse JSON response from LLM.

    Args:
        response: The response string from LLM

    Returns:
        Parsed JSON dictionary

    Raises:
        ValueError: If response is not valid JSON
    """
    # Remove markdown code blocks if present
    cleaned = response.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response: {e}\nResponse: {response[:500]}")
        raise ValueError(f"LLM returned invalid JSON: {e}")


def validate_schema(data: Dict[str, Any], required_fields: List[str]) -> bool:
    """
    Validate that response contains required fields.

    Args:
        data: The parsed JSON response
        required_fields: List of required field names

    Returns:
        True if valid, False otherwise
    """
    missing = [field for field in required_fields if field not in data]
    if missing:
        logger.warning(f"Missing required fields: {missing}")
        return False
    return True


# ============================================================================
# SAFE LLM CALL WRAPPER
# ============================================================================


def safe_llm_call(
    llm_function: Callable,
    prompt: str,
    system_prompt: Optional[str] = None,
    max_retries: int = 3,
    retry_delay: float = 1.0,
    **llm_kwargs: Any,
) -> Dict[str, Any]:
    """
    Safely execute an LLM call with error handling and retries.

    Args:
        llm_function: The LLM API function to call
        prompt: The user prompt
        system_prompt: Optional system prompt
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
        **llm_kwargs: Additional arguments for the LLM function

    Returns:
        Dictionary with success status and data/error
    """
    for attempt in range(max_retries):
        try:
            # Call the LLM function
            response = llm_function(prompt=prompt, system_prompt=system_prompt, **llm_kwargs)

            # Validate JSON if expected
            if llm_kwargs.get("expect_json", True):
                data = validate_json_response(response)
                return {"success": True, "data": data, "raw_response": response}
            else:
                return {"success": True, "data": response, "raw_response": response}

        except json.JSONDecodeError as e:
            logger.warning(f"JSON decode error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return {
                "success": False,
                "error": "Invalid JSON response",
                "details": str(e),
                "raw_response": response if "response" in locals() else None,
            }

        except Exception as e:
            logger.error(f"LLM call failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                continue
            return {
                "success": False,
                "error": "LLM call failed",
                "details": str(e),
                "attempt": attempt + 1,
            }

    return {"success": False, "error": "Max retries exceeded"}


# ============================================================================
# RESPONSE POST-PROCESSING
# ============================================================================


def extract_confidence_score(response: Dict[str, Any]) -> Optional[int]:
    """
    Extract confidence score from LLM response.

    Args:
        response: Parsed LLM response

    Returns:
        Confidence score (0-100) or None
    """
    # Try common locations for confidence scores
    if "confidence" in response:
        conf = response["confidence"]
        if isinstance(conf, dict) and "overall" in conf:
            return conf["overall"]
        if isinstance(conf, (int, float)):
            return int(conf)

    if "match_summary" in response and "score" in response["match_summary"]:
        return response["match_summary"]["score"]

    return None


def sanitize_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize LLM response by removing null values and empty arrays.

    Args:
        data: The response dictionary

    Returns:
        Sanitized dictionary
    """
    if not isinstance(data, dict):
        return data

    sanitized = {}
    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, list) and len(value) == 0:
            continue
        if isinstance(value, dict):
            sanitized_value = sanitize_response(value)
            if sanitized_value:
                sanitized[key] = sanitized_value
        else:
            sanitized[key] = value

    return sanitized


# ============================================================================
# LOGGING AND MONITORING
# ============================================================================


def log_llm_call(
    task: str,
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    duration: float,
    success: bool,
):
    """
    Log LLM call metrics for monitoring.

    Args:
        task: The task type
        provider: LLM provider name
        model: Model name
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        duration: Call duration in seconds
        success: Whether the call succeeded
    """
    logger.info(
        f"LLM Call - Task: {task}, Provider: {provider}, Model: {model}, "
        f"Tokens: {input_tokens}/{output_tokens}, Duration: {duration:.2f}s, "
        f"Success: {success}"
    )


def monitor_llm_call(task: str, provider: str, model: str):
    """
    Decorator to monitor LLM calls.

    Args:
        task: The task type
        provider: LLM provider name
        model: Model name
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time

                # Extract token counts if available
                input_tokens = kwargs.get("input_tokens", 0)
                output_tokens = kwargs.get("output_tokens", 0)

                log_llm_call(
                    task=task,
                    provider=provider,
                    model=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    duration=duration,
                    success=True,
                )
                return result

            except Exception as e:
                duration = time.time() - start_time
                log_llm_call(
                    task=task,
                    provider=provider,
                    model=model,
                    input_tokens=0,
                    output_tokens=0,
                    duration=duration,
                    success=False,
                )
                raise e

        return wrapper

    return decorator


# ============================================================================
# BATCH PROCESSING UTILITIES
# ============================================================================


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size.

    Args:
        items: List to chunk
        chunk_size: Size of each chunk

    Returns:
        List of chunks
    """
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


def merge_batch_responses(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge multiple batch responses into a single response.

    Args:
        responses: List of response dictionaries

    Returns:
        Merged response dictionary
    """
    if not responses:
        return {}

    merged = {"items": [], "summary": {}}

    for response in responses:
        if "items" in response:
            merged["items"].extend(response["items"])
        if "ranked_candidates" in response:
            if "ranked_candidates" not in merged:
                merged["ranked_candidates"] = []
            merged["ranked_candidates"].extend(response["ranked_candidates"])

    return merged

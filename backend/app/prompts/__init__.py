"""
CareerCraft - LLM Prompt System
Production-ready prompts for AI-powered resume management and candidate matching.
"""

from .base import (
    CAREERCRAFT_SYSTEM_PROMPT,
    PARSE_RESUME_PROMPT,
    ANALYZE_JOB_DESCRIPTION_PROMPT,
    NORMALIZE_SKILLS_PROMPT,
)

from .matching import (
    MATCH_CANDIDATE_TO_JOB_PROMPT,
    BATCH_MATCH_CANDIDATES_PROMPT,
)

from .enhancement import (
    ENHANCE_RESUME_PROMPT,
    QA_ENHANCED_RESUME_PROMPT,
)

from .chat import (
    CAREERCRAFT_CHAT_PROMPT,
)

from .config import (
    LLM_CONFIGS,
    LLMProvider,
    get_llm_config,
)

from .utils import (
    safe_llm_call,
    format_prompt,
    validate_json_response,
)

__all__ = [
    # System prompts
    "CAREERCRAFT_SYSTEM_PROMPT",

    # Parsing prompts
    "PARSE_RESUME_PROMPT",
    "ANALYZE_JOB_DESCRIPTION_PROMPT",
    "NORMALIZE_SKILLS_PROMPT",

    # Matching prompts
    "MATCH_CANDIDATE_TO_JOB_PROMPT",
    "BATCH_MATCH_CANDIDATES_PROMPT",

    # Enhancement prompts
    "ENHANCE_RESUME_PROMPT",
    "QA_ENHANCED_RESUME_PROMPT",

    # Chat prompts
    "CAREERCRAFT_CHAT_PROMPT",

    # Configuration
    "LLM_CONFIGS",
    "LLMProvider",
    "get_llm_config",

    # Utilities
    "safe_llm_call",
    "format_prompt",
    "validate_json_response",
]

__version__ = "1.0.0"

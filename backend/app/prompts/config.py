"""
LLM provider configuration and settings.
Supports OpenAI, Anthropic, and Google providers.
"""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


class LLMConfig(BaseModel):
    """Configuration for a specific LLM provider."""

    model: str
    temperature: float = 0.1
    max_tokens: int = 4000
    response_format: Optional[Dict[str, str]] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None


# ============================================================================
# PROVIDER CONFIGURATIONS
# ============================================================================

LLM_CONFIGS: Dict[str, LLMConfig] = {
    LLMProvider.OPENAI: LLMConfig(
        model="gpt-4-turbo-preview",
        temperature=0.1,
        max_tokens=4000,
        response_format={"type": "json_object"},
    ),
    LLMProvider.ANTHROPIC: LLMConfig(
        model="claude-3-sonnet-20240229",
        temperature=0.1,
        max_tokens=4000,
    ),
    LLMProvider.GOOGLE: LLMConfig(
        model="gemini-pro",
        temperature=0.1,
        max_tokens=4000,
    ),
}


# Task-specific temperature overrides
TASK_TEMPERATURES = {
    "parsing": 0.0,  # Deterministic for data extraction
    "matching": 0.1,  # Low variance for consistent scoring
    "enhancement": 0.3,  # Some creativity for rewriting
    "chat": 0.7,  # More natural conversation
    "qa": 0.0,  # Deterministic quality checks
}


# ============================================================================
# CONFIGURATION HELPERS
# ============================================================================


def get_llm_config(
    provider: LLMProvider = LLMProvider.OPENAI,
    task: Optional[str] = None,
    **overrides: Any,
) -> LLMConfig:
    """
    Get LLM configuration for a specific provider and task.

    Args:
        provider: The LLM provider to use
        task: Optional task name for temperature override
        **overrides: Additional config overrides

    Returns:
        LLMConfig with appropriate settings
    """
    config = LLM_CONFIGS[provider].model_copy()

    # Apply task-specific temperature if provided
    if task and task in TASK_TEMPERATURES:
        config.temperature = TASK_TEMPERATURES[task]

    # Apply any custom overrides
    for key, value in overrides.items():
        if hasattr(config, key):
            setattr(config, key, value)

    return config


def get_config_dict(provider: LLMProvider = LLMProvider.OPENAI, **kwargs: Any) -> Dict[str, Any]:
    """
    Get configuration as dictionary for API calls.

    Args:
        provider: The LLM provider to use
        **kwargs: Additional overrides

    Returns:
        Configuration dictionary
    """
    config = get_llm_config(provider, **kwargs)
    return config.model_dump(exclude_none=True)


# ============================================================================
# MODEL SELECTION BY TASK
# ============================================================================

RECOMMENDED_MODELS = {
    "parsing": {
        LLMProvider.OPENAI: "gpt-4-turbo-preview",
        LLMProvider.ANTHROPIC: "claude-3-sonnet-20240229",
        LLMProvider.GOOGLE: "gemini-pro",
    },
    "matching": {
        LLMProvider.OPENAI: "gpt-4-turbo-preview",
        LLMProvider.ANTHROPIC: "claude-3-sonnet-20240229",
        LLMProvider.GOOGLE: "gemini-pro",
    },
    "enhancement": {
        LLMProvider.OPENAI: "gpt-4-turbo-preview",
        LLMProvider.ANTHROPIC: "claude-3-opus-20240229",  # Better for creative writing
        LLMProvider.GOOGLE: "gemini-pro",
    },
    "chat": {
        LLMProvider.OPENAI: "gpt-4-turbo-preview",
        LLMProvider.ANTHROPIC: "claude-3-sonnet-20240229",
        LLMProvider.GOOGLE: "gemini-pro",
    },
}


def get_recommended_model(task: str, provider: LLMProvider = LLMProvider.OPENAI) -> str:
    """
    Get the recommended model for a specific task and provider.

    Args:
        task: The task type (parsing, matching, enhancement, chat)
        provider: The LLM provider to use

    Returns:
        Model name string
    """
    if task not in RECOMMENDED_MODELS:
        return LLM_CONFIGS[provider].model

    return RECOMMENDED_MODELS[task].get(provider, LLM_CONFIGS[provider].model)


# ============================================================================
# COST TRACKING
# ============================================================================

# Approximate costs per 1K tokens (as of 2024)
PRICING = {
    "gpt-4-turbo-preview": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
    "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
    "gemini-pro": {"input": 0.00025, "output": 0.0005},
}


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Estimate the cost of an LLM call.

    Args:
        model: The model name
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Estimated cost in USD
    """
    if model not in PRICING:
        return 0.0

    pricing = PRICING[model]
    input_cost = (input_tokens / 1000) * pricing["input"]
    output_cost = (output_tokens / 1000) * pricing["output"]

    return input_cost + output_cost

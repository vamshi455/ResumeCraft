"""
LangSmith API Client for deployed LangGraph workflows
"""

import os
import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class LangSmithClient:
    """Client for calling deployed LangGraph workflow on LangSmith Cloud"""

    def __init__(
        self,
        deployment_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 120
    ):
        """
        Initialize LangSmith client.

        Args:
            deployment_url: Full deployment URL or deployment ID
            api_key: LangSmith API key
            timeout: Request timeout in seconds
        """
        # Get from environment if not provided
        self.api_key = api_key or os.getenv("LANGSMITH_API_KEY")
        deployment_input = deployment_url or os.getenv("LANGGRAPH_API_URL")

        if not self.api_key:
            raise ValueError(
                "LANGSMITH_API_KEY not found. Set it in environment or .env file"
            )

        if not deployment_input:
            raise ValueError(
                "LANGGRAPH_API_URL not found. Set it in environment or .env file"
            )

        # Handle both full URL and just deployment ID
        if deployment_input.startswith("http"):
            self.base_url = deployment_input
        else:
            # Just deployment ID provided
            self.base_url = f"https://api.smith.langchain.com/deployments/{deployment_input}"

        self.timeout = timeout
        logger.info(f"LangSmith client initialized with URL: {self.base_url}")

    def invoke(
        self,
        resume_text: str,
        job_description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Invoke the recruitment workflow synchronously.

        Args:
            resume_text: Resume text to process
            job_description: Optional job description for matching
            **kwargs: Additional parameters

        Returns:
            Workflow output as dictionary

        Raises:
            requests.RequestException: If API call fails
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "input": {
                "resume_text": resume_text,
                "job_description": job_description,
                **kwargs
            }
        }

        try:
            logger.info(f"Invoking workflow at {self.base_url}/invoke")

            response = requests.post(
                f"{self.base_url}/invoke",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )

            response.raise_for_status()
            result = response.json()

            logger.info(f"Workflow completed successfully")
            return result

        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {self.timeout}s")
            raise Exception(f"Request timed out after {self.timeout} seconds")

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response: {e.response.text}")
            raise Exception(f"Failed to call LangSmith API: {str(e)}")

    def get_output(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract output from API response.

        Args:
            result: Full API response

        Returns:
            Output dictionary
        """
        return result.get("output", {})


def check_langsmith_config() -> tuple[bool, str]:
    """
    Check if LangSmith is configured.

    Returns:
        Tuple of (is_configured, message)
    """
    api_key = os.getenv("LANGSMITH_API_KEY")
    api_url = os.getenv("LANGGRAPH_API_URL")

    if not api_key:
        return False, "LANGSMITH_API_KEY not set in environment"

    if not api_url:
        return False, "LANGGRAPH_API_URL not set in environment"

    if not api_key.startswith("lsv2_"):
        return False, "LANGSMITH_API_KEY appears invalid (should start with lsv2_)"

    return True, "LangSmith configured successfully"


def get_langsmith_client() -> Optional[LangSmithClient]:
    """
    Get LangSmith client if configured, otherwise None.

    Returns:
        LangSmithClient instance or None
    """
    is_configured, message = check_langsmith_config()

    if not is_configured:
        logger.warning(f"LangSmith not configured: {message}")
        return None

    try:
        return LangSmithClient()
    except Exception as e:
        logger.error(f"Failed to create LangSmith client: {str(e)}")
        return None

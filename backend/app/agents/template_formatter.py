"""
Template Formatter Agent
Analyzes template format and applies it to other resumes
"""

from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class TemplateFormat(BaseModel):
    """Template format structure"""
    sections_order: list[str] = Field(default=[], description="Order of sections in the template")
    section_styles: dict = Field(default_factory=dict, description="Styling for each section (headers, fonts, spacing)")
    contact_info_placement: str = Field(default="top", description="Where contact info appears (top, side, etc)")
    date_format: str = Field(default="MM/YYYY", description="How dates are formatted")
    bullet_style: str = Field(default="standard", description="Style of bullet points")
    spacing: dict = Field(default_factory=dict, description="Spacing between sections and elements")
    font_style: dict = Field(default_factory=dict, description="Font information if detectable")
    layout: str = Field(default="single-column", description="Overall layout style (single-column, two-column, etc)")


class FormattedResume(BaseModel):
    """Formatted resume content"""
    personal_info: dict = Field(default_factory=dict, description="Reformatted personal information")
    sections: list[dict] = Field(default_factory=list, description="Resume sections in template order")
    formatting_notes: list[str] = Field(default_factory=list, description="Notes about formatting changes made")


class TemplateFormatterState(TypedDict):
    """State for template formatter"""
    template_text: str
    template_format: dict
    resume_text: str
    parsed_resume: dict
    formatted_resume: dict
    formatting_confidence: int
    errors: Annotated[list, lambda x, y: x + y]


def analyze_template_format(llm: ChatOpenAI, template_text: str) -> dict:
    """
    Analyze the template resume to extract its format structure.

    Args:
        llm: Language model instance
        template_text: Text extracted from template resume

    Returns:
        Dictionary containing template format structure
    """

    system_prompt = """You are a resume format analyzer. Your job is to analyze a resume template
    and extract its formatting structure, layout, and style patterns.

    Focus on:
    1. Section order and hierarchy
    2. How information is organized
    3. Date formats used
    4. Bullet point styles
    5. Contact information placement
    6. Overall layout structure

    Be detailed and precise in your analysis."""

    user_prompt = f"""Analyze this resume template and extract its format structure:

{template_text}

Provide a detailed analysis of:
1. The order of sections (Summary, Experience, Education, Skills, etc.)
2. How each section is structured
3. Date formatting patterns
4. Bullet point styles
5. Contact information layout
6. Overall visual structure

Return your analysis in a structured format."""

    try:
        structured_llm = llm.with_structured_output(TemplateFormat, method="function_calling")
        result = structured_llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])

        return {
            "template_format": result.model_dump(),
            "formatting_confidence": 85,
            "errors": []
        }
    except Exception as e:
        return {
            "template_format": None,
            "formatting_confidence": 0,
            "errors": [f"Template analysis failed: {str(e)}"]
        }


def apply_template_format(llm: ChatOpenAI, parsed_resume: dict, template_format: dict) -> dict:
    """
    Apply the template format to a parsed resume.

    Args:
        llm: Language model instance
        parsed_resume: Parsed resume data
        template_format: Template format structure

    Returns:
        Dictionary containing formatted resume
    """

    system_prompt = """You are a resume formatter. Your job is to reformat a resume to match
    a specific template format while preserving all the original content.

    Rules:
    1. NEVER add, remove, or fabricate information
    2. Reorganize sections to match template order
    3. Reformat dates to match template style
    4. Apply bullet point style from template
    5. Preserve all achievements, skills, and experiences
    6. Match the layout structure of the template

    Your goal is to make the resume look like it was written using the template."""

    user_prompt = f"""Reformat this resume to match the template format:

PARSED RESUME:
{parsed_resume}

TEMPLATE FORMAT TO MATCH:
{template_format}

Instructions:
1. Reorganize sections to match the template order: {template_format.get('sections_order', [])}
2. Format dates using this pattern: {template_format.get('date_format', 'MM/YYYY')}
3. Use this bullet style: {template_format.get('bullet_style', 'standard')}
4. Place contact info: {template_format.get('contact_info_placement', 'top')}
5. Match the layout: {template_format.get('layout', 'single-column')}

Return the reformatted resume with all sections reorganized and styled according to the template."""

    try:
        structured_llm = llm.with_structured_output(FormattedResume, method="function_calling")
        result = structured_llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])

        return {
            "formatted_resume": result.model_dump(),
            "formatting_confidence": 90,
            "errors": []
        }
    except Exception as e:
        return {
            "formatted_resume": None,
            "formatting_confidence": 0,
            "errors": [f"Formatting failed: {str(e)}"]
        }


def format_resume_with_template(llm: ChatOpenAI, template_text: str, resume_text: str, parsed_resume: dict) -> dict:
    """
    Complete workflow: analyze template and format resume.

    Args:
        llm: Language model instance
        template_text: Text from template resume
        resume_text: Text from resume to format
        parsed_resume: Already parsed resume data

    Returns:
        Dictionary containing formatted resume and metadata
    """

    # Step 1: Analyze template format
    template_result = analyze_template_format(llm, template_text)

    if template_result.get("errors"):
        return {
            "success": False,
            "errors": template_result["errors"],
            "template_format": None,
            "formatted_resume": None
        }

    # Step 2: Apply template format to resume
    format_result = apply_template_format(
        llm,
        parsed_resume,
        template_result["template_format"]
    )

    if format_result.get("errors"):
        return {
            "success": False,
            "errors": format_result["errors"],
            "template_format": template_result["template_format"],
            "formatted_resume": None
        }

    # Step 3: Return complete result
    return {
        "success": True,
        "template_format": template_result["template_format"],
        "formatted_resume": format_result["formatted_resume"],
        "formatting_confidence": format_result["formatting_confidence"],
        "errors": []
    }

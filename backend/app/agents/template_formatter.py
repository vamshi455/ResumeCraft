"""
Template Formatter Agent
Analyzes template format and applies it to other resumes
"""

from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from langchain_core.language_models import BaseChatModel
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


def analyze_template_format(llm: BaseChatModel, template_text: str, custom_instructions: str = None) -> dict:
    """
    Analyze the template resume to extract its format structure.

    Args:
        llm: Language model instance
        template_text: Text extracted from template resume
        custom_instructions: Optional user-provided specific instructions

    Returns:
        Dictionary containing template format structure
    """

    system_prompt = """You are a resume format analyzer. Your job is to analyze a resume template
    and extract its formatting structure, layout, and style patterns with EXTREME PRECISION.

    Focus on:
    1. EXACT section order and hierarchy
    2. SPECIFIC ways information is organized
    3. PRECISE date formats used (with examples)
    4. DETAILED bullet point styles and patterns
    5. EXACT contact information placement and format
    6. COMPLETE layout structure details

    Be extremely detailed and precise in your analysis. Pay attention to:
    - Exact capitalization (ALL CAPS, Title Case, etc.)
    - Punctuation patterns
    - Spacing and separators
    - Formatting conventions
    - Section header styles"""

    user_instructions = ""
    if custom_instructions:
        user_instructions = f"""

CRITICAL USER INSTRUCTIONS - FOLLOW THESE EXACTLY:
{custom_instructions}

These instructions are MANDATORY. The template MUST be analyzed according to these specific requirements."""

    user_prompt = f"""Analyze this resume template and extract its format structure with EXTREME PRECISION:

{template_text}
{user_instructions}

Provide an EXTREMELY detailed analysis of:
1. The EXACT order of sections (include specific names as they appear)
2. How each section is structured (with specific examples from template)
3. Date formatting patterns (show EXACT examples: "Jan 2020", "01/2020", etc.)
4. Bullet point styles (show exact patterns used)
5. Contact information layout (exact format and placement)
6. Overall visual structure (section headers, formatting, etc.)

Be VERY SPECIFIC. For example:
- Don't just say "dates are formatted", say "dates use format 'MMM YYYY - MMM YYYY' like 'Jan 2020 - Dec 2022'"
- Don't just say "sections are ordered", list them: "1. PROFESSIONAL SUMMARY, 2. WORK EXPERIENCE, etc."
- Include actual examples from the template whenever possible

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


def apply_template_format(llm: BaseChatModel, parsed_resume: dict, template_format: dict, custom_instructions: str = None) -> dict:
    """
    Apply the template format to a parsed resume.

    Args:
        llm: Language model instance
        parsed_resume: Parsed resume data
        template_format: Template format structure
        custom_instructions: Optional user-provided specific instructions

    Returns:
        Dictionary containing formatted resume
    """

    system_prompt = """You are a resume formatter. Your job is to reformat a resume to match
    a specific template format while preserving all the original content with PERFECT ACCURACY.

    CRITICAL Rules:
    1. NEVER EVER add, remove, or fabricate ANY information
    2. Reorganize sections to EXACTLY match template order
    3. Reformat dates to PRECISELY match template style
    4. Apply the EXACT bullet point style from template
    5. Preserve ALL achievements, skills, and experiences WORD-FOR-WORD
    6. Match the EXACT layout structure of the template
    7. Use the SAME section headers as they appear in template
    8. Follow ALL capitalization, punctuation, and formatting conventions from template

    Your goal is to make the output look IDENTICAL in structure to the template, while containing
    the candidate's actual information. Think of it as filling a template with new data."""

    user_instructions_text = ""
    if custom_instructions:
        user_instructions_text = f"""

CRITICAL USER-PROVIDED INSTRUCTIONS - THESE ARE MANDATORY:
{custom_instructions}

You MUST follow these instructions EXACTLY. They override any general formatting guidelines."""

    user_prompt = f"""Reformat this resume to EXACTLY match the template format:

PARSED RESUME (candidate's actual information):
{parsed_resume}

TEMPLATE FORMAT TO MATCH PRECISELY:
{template_format}
{user_instructions_text}

MANDATORY Instructions:
1. Reorganize sections in THIS EXACT ORDER: {template_format.get('sections_order', [])}
2. Format dates EXACTLY like this: {template_format.get('date_format', 'MM/YYYY')}
   - Look at the examples in the template format and match them precisely
3. Use EXACTLY this bullet style: {template_format.get('bullet_style', 'standard')}
4. Place contact info EXACTLY: {template_format.get('contact_info_placement', 'top')}
5. Match layout PRECISELY: {template_format.get('layout', 'single-column')}
6. Use section headers EXACTLY as specified in the template
7. Follow ALL specific formatting details from the template format analysis

IMPORTANT: The output should be the candidate's resume content structured EXACTLY like the template.
Think of it as: Template Structure + Candidate Content = Perfect Match

Return the reformatted resume with all sections reorganized and styled according to the template."""

    try:
        # Use JSON mode instead of function_calling for better compatibility
        import json

        response = llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt + "\n\nReturn your response as valid JSON matching the FormattedResume schema."}
        ])

        # Parse the JSON response
        response_text = response.content if hasattr(response, 'content') else str(response)

        # Try to extract JSON from response
        try:
            # Find JSON in the response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response_text[start:end]
                result_dict = json.loads(json_str)
            else:
                result_dict = json.loads(response_text)
        except:
            # If JSON parsing fails, create a structured response
            result_dict = {
                "personal_info": parsed_resume.get("personal_info", {}),
                "sections": [],
                "formatting_notes": ["Template formatting applied based on provided format"]
            }

        # Ensure formatting_notes is a list
        if isinstance(result_dict.get('formatting_notes'), str):
            notes = result_dict['formatting_notes']
            result_dict['formatting_notes'] = [line.strip() for line in notes.split('\n') if line.strip()]
            if not result_dict['formatting_notes']:
                result_dict['formatting_notes'] = [notes]

        # Validate with Pydantic
        validated = FormattedResume(**result_dict)

        return {
            "formatted_resume": validated.model_dump(),
            "formatting_confidence": 90,
            "errors": []
        }
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        return {
            "formatted_resume": None,
            "formatting_confidence": 0,
            "errors": [f"Formatting failed: {str(e)}\n{error_detail}"]
        }


def format_resume_with_template(llm: BaseChatModel, template_text: str, resume_text: str, parsed_resume: dict, custom_instructions: str = None) -> dict:
    """
    Complete workflow: analyze template and format resume.

    Args:
        llm: Language model instance
        template_text: Text from template resume
        resume_text: Text from resume to format
        parsed_resume: Already parsed resume data
        custom_instructions: Optional user-provided instructions for template matching

    Returns:
        Dictionary containing formatted resume and metadata
    """

    # Step 1: Analyze template format
    template_result = analyze_template_format(llm, template_text, custom_instructions)

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
        template_result["template_format"],
        custom_instructions
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

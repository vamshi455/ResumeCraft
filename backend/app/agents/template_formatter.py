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

    IMPORTANT: First determine the template type:
    - SUMMARY/BRIEF: Short cover letter or submission format (e.g., highlights, key skills summary)
    - FULL RESUME: Complete resume with detailed sections

    Focus on:
    1. Template type (summary/brief vs full resume)
    2. EXACT section order and hierarchy
    3. SPECIFIC ways information is organized
    4. PRECISE date formats used (with examples)
    5. DETAILED bullet point styles and patterns
    6. EXACT contact information placement and format
    7. COMPLETE layout structure details

    Be extremely detailed and precise in your analysis. Pay attention to:
    - Exact capitalization (ALL CAPS, Title Case, etc.)
    - Punctuation patterns
    - Spacing and separators
    - Formatting conventions
    - Section header styles

    WARNING: Note any example/placeholder content in template (names, companies, skills)
    - these should NEVER be copied to output, only the structure/format matters"""

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
    a specific template format while using ONLY the candidate's actual information.

    CRITICAL Rules - NEVER BREAK THESE:
    1. NEVER EVER add, remove, fabricate, or hallucinate ANY information not in the original resume
    2. NEVER invent skills, experiences, companies, dates, or achievements
    3. NEVER copy content from the template - only use the candidate's actual data
    4. If the template is a SUMMARY/BRIEF format: Extract only the most relevant highlights from candidate's resume
    5. If the template is a FULL RESUME format: Reorganize all sections to match template order
    6. ONLY use information that exists in the parsed resume data
    7. If information doesn't exist in resume (e.g., no MBA, no specific skill), DO NOT add it
    8. Match the template's structure and style, but fill it with the candidate's real data only

    Template Types:
    - SUMMARY/BRIEF: Short submission letter with highlights (preserve key points only)
    - FULL RESUME: Complete resume with all sections (reorganize everything)

    Your goal: Match template structure, use ONLY candidate's real information, NEVER hallucinate."""

    user_instructions_text = ""
    if custom_instructions:
        user_instructions_text = f"""

CRITICAL USER-PROVIDED INSTRUCTIONS - THESE ARE MANDATORY:
{custom_instructions}

You MUST follow these instructions EXACTLY. They override any general formatting guidelines."""

    user_prompt = f"""Reformat this resume to match the template format using ONLY the candidate's real data:

PARSED RESUME (ONLY source of truth - use ONLY this data):
{parsed_resume}

TEMPLATE FORMAT TO MATCH:
{template_format}
{user_instructions_text}

CRITICAL ANTI-HALLUCINATION RULES:
1. ONLY use information from the PARSED RESUME above
2. If template shows "MBA" but candidate has "BS" - use BS (their actual degree)
3. If template shows "20+ years SAP" but candidate has different skills - use their actual skills
4. NEVER copy example content from template (names, companies, skills, dates)
5. If template is a brief/summary format - extract key highlights from candidate's actual experience
6. If candidate doesn't have something from template - LEAVE IT OUT, don't invent it

FORMATTING Instructions (structure only, not content):
1. Section order: {template_format.get('sections_order', [])}
2. Date format: {template_format.get('date_format', 'MM/YYYY')}
3. Bullet style: {template_format.get('bullet_style', 'standard')}
4. Contact info placement: {template_format.get('contact_info_placement', 'top')}
5. Layout: {template_format.get('layout', 'single-column')}

Formula: Template STRUCTURE (format/order) + Candidate's REAL DATA (from parsed resume only) = Output

VERIFY before returning: Did I use any information NOT in the parsed resume? If yes, remove it!

Return the reformatted resume using ONLY the candidate's actual information."""

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

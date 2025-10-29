"""
Excel Processing Utilities for Entity Resolution.

Handles reading Excel files with candidate data, validating format,
and preparing data for the entity resolution workflow.
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
from io import BytesIO
from datetime import datetime

logger = logging.getLogger(__name__)


# ============================================================================
# EXCEL SCHEMA DEFINITIONS
# ============================================================================

# Required columns for candidate Excel
REQUIRED_CANDIDATE_COLUMNS = [
    "name",
    "skill_set",
    "exp_years",
    "domain"
]

# Optional columns
OPTIONAL_CANDIDATE_COLUMNS = [
    "email",
    "phone",
    "location",
    "previous_roles",
    "education",
    "certifications",
    "linkedin",
    "github",
    "portfolio"
]

# All valid columns
ALL_CANDIDATE_COLUMNS = REQUIRED_CANDIDATE_COLUMNS + OPTIONAL_CANDIDATE_COLUMNS


# ============================================================================
# EXCEL READING & VALIDATION
# ============================================================================

def read_candidate_excel(
    file_path_or_buffer,
    validate: bool = True
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Read candidate Excel file and validate format.

    Args:
        file_path_or_buffer: File path or buffer (from Streamlit upload)
        validate: Whether to validate the format

    Returns:
        Tuple of (DataFrame, list of validation errors)

    Raises:
        ValueError: If file cannot be read
    """
    logger.info("Reading candidate Excel file...")

    try:
        # Read Excel file
        df = pd.read_excel(file_path_or_buffer)
        logger.info(f"Read {len(df)} rows from Excel")

        # Validate if requested
        errors = []
        if validate:
            errors = validate_candidate_dataframe(df)

        return df, errors

    except Exception as e:
        logger.error(f"Failed to read Excel file: {e}")
        raise ValueError(f"Failed to read Excel file: {str(e)}")


def validate_candidate_dataframe(df: pd.DataFrame) -> List[str]:
    """
    Validate candidate DataFrame has required columns and data.

    Args:
        df: Candidate DataFrame

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    # Check if DataFrame is empty
    if df.empty:
        errors.append("Excel file is empty")
        return errors

    # Check required columns
    missing_columns = [col for col in REQUIRED_CANDIDATE_COLUMNS if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")

    # Check for invalid column names
    invalid_columns = [col for col in df.columns if col not in ALL_CANDIDATE_COLUMNS]
    if invalid_columns:
        errors.append(f"Invalid columns found: {', '.join(invalid_columns)}")

    # Check for missing data in required columns
    for col in REQUIRED_CANDIDATE_COLUMNS:
        if col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                errors.append(f"Column '{col}' has {null_count} missing values")

    # Check data types
    if "exp_years" in df.columns:
        try:
            df["exp_years"].astype(float)
        except (ValueError, TypeError):
            errors.append("Column 'exp_years' must contain numeric values")

    return errors


# ============================================================================
# DATA TRANSFORMATION
# ============================================================================

def dataframe_to_candidates(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert DataFrame to list of candidate dictionaries.

    Args:
        df: Candidate DataFrame

    Returns:
        List of candidate dictionaries
    """
    logger.info("Converting DataFrame to candidate list...")

    candidates = []

    for idx, row in df.iterrows():
        candidate = {}

        # Add all available columns
        for col in df.columns:
            value = row[col]

            # Skip NaN values
            if pd.isna(value):
                continue

            # Convert to appropriate type
            if col == "exp_years":
                candidate[col] = float(value)
            else:
                candidate[col] = str(value).strip()

        # Add metadata
        candidate["candidate_id"] = f"candidate_{idx + 1}"
        candidate["source"] = "excel_upload"
        candidate["uploaded_at"] = datetime.now().isoformat()

        candidates.append(candidate)

    logger.info(f"Converted {len(candidates)} candidates")
    return candidates


def candidates_to_dataframe(candidates: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Convert candidate list back to DataFrame.

    Args:
        candidates: List of candidate dictionaries

    Returns:
        DataFrame
    """
    logger.info("Converting candidate list to DataFrame...")

    # Remove metadata fields
    clean_candidates = []
    for candidate in candidates:
        clean_candidate = {k: v for k, v in candidate.items()
                          if k not in ["candidate_id", "source", "uploaded_at", "parsed_resume", "resume_text"]}
        clean_candidates.append(clean_candidate)

    df = pd.DataFrame(clean_candidates)
    logger.info(f"Created DataFrame with {len(df)} rows")

    return df


# ============================================================================
# MATCH RESULTS EXPORT
# ============================================================================

def export_match_results_to_excel(
    match_results: List[Dict[str, Any]],
    include_detailed_analysis: bool = True
) -> BytesIO:
    """
    Export match results to Excel file.

    Args:
        match_results: List of match results from workflow
        include_detailed_analysis: Whether to include detailed analysis sheets

    Returns:
        BytesIO buffer with Excel file
    """
    logger.info(f"Exporting {len(match_results)} match results to Excel...")

    # Create Excel writer
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Summary results
        summary_data = []
        for result in match_results:
            candidate = result.get("candidate", {})
            match_data = result.get("match_data", {})
            match_summary = match_data.get("match_summary", {}) if match_data else {}

            row = {
                "Rank": result.get("rank", 0),
                "Name": candidate.get("name", "N/A"),
                "Match Score": result.get("match_score", 0),
                "Match Level": match_summary.get("level", "N/A"),
                "Recommendation": match_summary.get("recommendation", "N/A"),
                "Skills": candidate.get("skill_set", "N/A"),
                "Experience (Years)": candidate.get("exp_years", 0),
                "Domain": candidate.get("domain", "N/A"),
                "Location": candidate.get("location", "N/A"),
                "Email": candidate.get("email", "N/A"),
                "Phone": candidate.get("phone", "N/A"),
            }
            summary_data.append(row)

        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name="Summary", index=False)

        if include_detailed_analysis:
            # Sheet 2: Detailed scores
            detailed_data = []
            for result in match_results:
                candidate = result.get("candidate", {})
                match_data = result.get("match_data", {})
                detailed_scores = match_data.get("detailed_scores", {}) if match_data else {}

                skills_score = detailed_scores.get("skills", {})
                exp_score = detailed_scores.get("experience", {})

                row = {
                    "Rank": result.get("rank", 0),
                    "Name": candidate.get("name", "N/A"),
                    "Overall Score": result.get("match_score", 0),
                    "Skills Score": skills_score.get("score", 0),
                    "Experience Score": exp_score.get("score", 0),
                    "Education Score": detailed_scores.get("education", {}).get("score", 0),
                    "Soft Skills Score": detailed_scores.get("soft_skills", {}).get("score", 0),
                    "Culture Fit Score": detailed_scores.get("culture_fit", {}).get("score", 0),
                    "Skills Match %": skills_score.get("match_percentage", 0),
                }
                detailed_data.append(row)

            detailed_df = pd.DataFrame(detailed_data)
            detailed_df.to_excel(writer, sheet_name="Detailed Scores", index=False)

            # Sheet 3: Strengths and Gaps
            strengths_gaps_data = []
            for result in match_results:
                candidate = result.get("candidate", {})
                match_data = result.get("match_data", {})

                strengths = match_data.get("strengths", []) if match_data else []
                gaps = match_data.get("gaps", []) if match_data else []

                strengths_text = "; ".join([s.get("strength", s) if isinstance(s, dict) else str(s) for s in strengths])
                gaps_text = "; ".join([g.get("gap", g) if isinstance(g, dict) else str(g) for g in gaps])

                row = {
                    "Rank": result.get("rank", 0),
                    "Name": candidate.get("name", "N/A"),
                    "Match Score": result.get("match_score", 0),
                    "Strengths": strengths_text or "N/A",
                    "Gaps": gaps_text or "No significant gaps",
                }
                strengths_gaps_data.append(row)

            sg_df = pd.DataFrame(strengths_gaps_data)
            sg_df.to_excel(writer, sheet_name="Strengths & Gaps", index=False)

    output.seek(0)
    logger.info("Excel export completed successfully")

    return output


# ============================================================================
# SAMPLE DATA GENERATION
# ============================================================================

def generate_sample_candidate_excel() -> BytesIO:
    """
    Generate a sample candidate Excel file for download.

    Returns:
        BytesIO buffer with sample Excel file
    """
    logger.info("Generating sample candidate Excel...")

    sample_data = [
        {
            "name": "John Doe",
            "skill_set": "Python, Django, REST API, PostgreSQL, Docker, AWS",
            "exp_years": 5.5,
            "domain": "Web Development",
            "previous_roles": "Senior Backend Developer, Software Engineer",
            "education": "B.S. Computer Science",
            "location": "San Francisco, CA",
            "email": "john.doe@example.com",
            "phone": "+1-555-0101"
        },
        {
            "name": "Jane Smith",
            "skill_set": "Java, Spring Boot, Microservices, Kubernetes, Azure",
            "exp_years": 7.0,
            "domain": "Enterprise Software",
            "previous_roles": "Lead Developer, Senior Engineer",
            "education": "M.S. Software Engineering",
            "location": "New York, NY",
            "email": "jane.smith@example.com",
            "phone": "+1-555-0102"
        },
        {
            "name": "Bob Johnson",
            "skill_set": "React, Node.js, TypeScript, MongoDB, GraphQL",
            "exp_years": 3.0,
            "domain": "Full Stack Development",
            "previous_roles": "Full Stack Developer",
            "education": "B.S. Information Technology",
            "location": "Remote",
            "email": "bob.johnson@example.com",
            "phone": "+1-555-0103"
        },
    ]

    df = pd.DataFrame(sample_data)

    output = BytesIO()
    df.to_excel(output, index=False, sheet_name="Candidates")
    output.seek(0)

    logger.info("Sample Excel generated successfully")
    return output


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def get_excel_format_instructions() -> str:
    """
    Get formatted instructions for Excel file structure.

    Returns:
        Markdown-formatted instructions
    """
    return """
### Required Columns:
- **name** - Full name of the candidate
- **skill_set** - Technical skills (comma-separated)
- **exp_years** - Years of experience (numeric)
- **domain** - Domain expertise (e.g., Web Development, Data Science)

### Optional Columns:
- **email** - Email address
- **phone** - Phone number
- **location** - Current location
- **previous_roles** - Previous job titles (comma-separated)
- **education** - Education background
- **certifications** - Professional certifications
- **linkedin** - LinkedIn profile URL
- **github** - GitHub profile URL
- **portfolio** - Portfolio website URL
"""


def get_column_mapping_suggestions(df_columns: List[str]) -> Dict[str, str]:
    """
    Suggest column mappings for non-standard Excel formats.

    Args:
        df_columns: List of column names in the DataFrame

    Returns:
        Dictionary mapping found columns to standard columns
    """
    mappings = {}

    # Common variations
    variations = {
        "name": ["candidate_name", "full_name", "employee_name", "applicant_name"],
        "skill_set": ["skills", "technical_skills", "competencies", "technologies"],
        "exp_years": ["experience", "years_of_experience", "total_experience", "yoe"],
        "domain": ["expertise", "specialization", "field", "area"],
        "email": ["email_address", "contact_email", "e_mail"],
        "phone": ["phone_number", "contact_number", "mobile", "telephone"],
        "location": ["city", "current_location", "residence"],
        "previous_roles": ["past_roles", "job_titles", "positions_held"],
        "education": ["degree", "qualification", "academic_background"],
    }

    # Check each column
    for col in df_columns:
        col_lower = col.lower().strip()

        for standard_col, variations_list in variations.items():
            if col_lower in variations_list or col_lower == standard_col:
                mappings[col] = standard_col
                break

    return mappings

"""
Core system prompts for CareerCraft AI.
Includes system configuration, resume parsing, job analysis, and skill normalization.
"""

# ============================================================================
# SYSTEM CONFIGURATION
# ============================================================================

CAREERCRAFT_SYSTEM_PROMPT = """
You are CareerCraft AI, an intelligent career assistant specializing in resume management,
candidate matching, and resume enhancement. You help recruiters and job seekers by:

1. Parsing and extracting structured data from resumes
2. Matching candidates with job descriptions using semantic analysis
3. Enhancing resumes to align with specific job requirements
4. Providing actionable insights for hiring decisions

CORE PRINCIPLES:
- Always maintain factual accuracy - never fabricate information
- Provide confidence scores for uncertain data
- Flag content that needs human review
- Preserve candidate authenticity while optimizing content
- Follow ethical AI practices in all operations

CAPABILITIES:
- Multi-format resume parsing (PDF, DOCX, TXT)
- Semantic matching using embeddings
- Intelligent resume enhancement
- Gap analysis and recommendations
- ATS optimization

You communicate in a professional, helpful, and clear manner.
"""

# ============================================================================
# RESUME PARSING PROMPT - UNIVERSAL EXTRACTOR
# ============================================================================

PARSE_RESUME_PROMPT = """
Extract structured information from the following resume. Handle any format gracefully.

RESUME TEXT:
```
{resume_text}
```

EXTRACTION RULES:
1. Use YYYY-MM format for all dates (e.g., "2023-06" or "Present")
2. If information is missing or unclear, use null
3. Categorize skills: technical, soft_skills, domain_knowledge, tools, certifications
4. Extract achievements in action-verb format with metrics when available
5. Calculate total years of experience
6. Infer experience level if not explicitly stated
7. Be conservative - accuracy over completeness

OUTPUT SCHEMA (JSON):
{{
  "personal_info": {{
    "full_name": "string",
    "email": "string | null",
    "phone": "string | null",
    "location": "string | null",
    "linkedin_url": "string | null",
    "github_url": "string | null",
    "portfolio_url": "string | null"
  }},

  "summary": {{
    "headline": "professional title/tagline",
    "summary_text": "2-3 sentence professional summary",
    "years_experience": "float | null",
    "experience_level": "entry | mid | senior | lead | executive"
  }},

  "work_experience": [
    {{
      "company": "string",
      "title": "string",
      "location": "string | null",
      "employment_type": "full-time | contract | freelance | internship",
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM | Present",
      "is_current": boolean,
      "description": "brief role overview",
      "achievements": ["achievement 1 with metrics", "achievement 2"],
      "technologies": ["tech1", "tech2"]
    }}
  ],

  "education": [
    {{
      "institution": "string",
      "degree": "string",
      "field": "string",
      "location": "string | null",
      "graduation_date": "YYYY-MM | YYYY",
      "gpa": "float | null",
      "honors": ["honor1"] | null
    }}
  ],

  "skills": {{
    "technical": ["Python", "AWS", "Docker"],
    "soft_skills": ["Leadership", "Communication"],
    "domain_knowledge": ["Machine Learning", "FinTech"],
    "tools": ["Git", "Jira", "VS Code"],
    "languages": [{{"language": "English", "proficiency": "native"}}]
  }},

  "projects": [
    {{
      "name": "string",
      "description": "string",
      "technologies": ["tech1", "tech2"],
      "url": "string | null"
    }}
  ],

  "certifications": [
    {{
      "name": "string",
      "issuer": "string",
      "date": "YYYY-MM",
      "expiry": "YYYY-MM | null",
      "credential_id": "string | null"
    }}
  ],

  "metadata": {{
    "total_years_experience": "float",
    "current_role": "string | null",
    "industries": ["Industry1", "Industry2"],
    "career_level": "entry | mid | senior | lead | executive"
  }},

  "confidence": {{
    "overall": 0-100,
    "personal_info": 0-100,
    "work_experience": 0-100,
    "skills": 0-100,
    "needs_review": ["field1", "field2"] | null
  }}
}}

IMPORTANT: Return ONLY valid JSON without markdown code blocks or explanations.
"""

# ============================================================================
# JOB DESCRIPTION ANALYSIS PROMPT
# ============================================================================

ANALYZE_JOB_DESCRIPTION_PROMPT = """
Analyze the following job description and extract structured requirements for candidate matching.

JOB DESCRIPTION:
```
{job_description}
```

ANALYSIS OBJECTIVES:
1. Distinguish required vs preferred qualifications
2. Extract must-have skills with context
3. Identify deal-breakers
4. Determine experience level
5. Extract company culture indicators
6. Generate matching keywords

OUTPUT SCHEMA (JSON):
{{
  "job_info": {{
    "title": "string",
    "company": "string | null",
    "location": "string",
    "work_type": "remote | hybrid | onsite",
    "employment_type": "full-time | contract | part-time",
    "salary_range": {{
      "min": "integer | null",
      "max": "integer | null",
      "currency": "USD | EUR | etc"
    }}
  }},

  "requirements": {{
    "must_have": {{
      "experience_years": {{
        "min": "integer | null",
        "max": "integer | null"
      }},
      "education": {{
        "level": "bachelors | masters | phd | null",
        "fields": ["Computer Science", "Engineering"] | null
      }},
      "required_skills": [
        {{
          "skill": "Python",
          "proficiency": "expert | advanced | intermediate",
          "years": "integer | null",
          "context": "for backend development"
        }}
      ],
      "certifications": ["AWS Certified"] | null,
      "other": ["US work authorization"] | null
    }},

    "nice_to_have": {{
      "preferred_skills": [
        {{
          "skill": "Go",
          "context": "for microservices"
        }}
      ],
      "bonus_experience": ["FinTech industry", "Open source contributions"]
    }}
  }},

  "responsibilities": [
    "Primary responsibility 1",
    "Primary responsibility 2"
  ],

  "role_details": {{
    "level": "entry | mid | senior | lead | executive",
    "type": "IC | manager | director | executive",
    "team_size": "string | null"
  }},

  "keywords": {{
    "technical": ["Python", "AWS", "Docker"],
    "domain": ["FinTech", "Healthcare"],
    "role": ["Backend", "Full-stack"],
    "soft_skills": ["Leadership", "Communication"]
  }},

  "deal_breakers": [
    "Must have 5+ years Python",
    "Must have US work authorization"
  ],

  "scoring_weights": {{
    "technical_skills": 0.40,
    "experience": 0.30,
    "education": 0.10,
    "soft_skills": 0.10,
    "culture_fit": 0.10
  }}
}}

Return ONLY valid JSON.
"""

# ============================================================================
# SKILL EXTRACTION & NORMALIZATION PROMPT
# ============================================================================

NORMALIZE_SKILLS_PROMPT = """
Extract and normalize skills from text into a standardized taxonomy.

INPUT TEXT:
```
{text}
```

INSTRUCTIONS:
1. Identify all skills (technical, soft, domain, tools)
2. Normalize variations (e.g., "JS" → "JavaScript")
3. Categorize appropriately
4. Remove duplicates
5. Add proficiency context if mentioned

OUTPUT SCHEMA (JSON):
{{
  "technical_skills": [
    {{
      "skill": "Python",
      "normalized_name": "Python",
      "category": "programming_language",
      "proficiency": "expert | advanced | intermediate | beginner | null",
      "years_experience": "float | null",
      "context": "for backend development"
    }}
  ],
  "soft_skills": ["Leadership", "Communication"],
  "domain_knowledge": ["Machine Learning", "FinTech"],
  "tools": ["Git", "Docker", "VS Code"],
  "certifications": ["AWS Certified Solutions Architect"]
}}

Return ONLY valid JSON.
"""

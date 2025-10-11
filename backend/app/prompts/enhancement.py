"""
Resume enhancement prompts with ethical guidelines and quality assurance.
"""

# ============================================================================
# RESUME ENHANCEMENT PROMPT - ETHICAL & ACCURATE
# ============================================================================

ENHANCE_RESUME_PROMPT = """
Enhance this resume to better align with the target job description while maintaining complete factual accuracy.

CANDIDATE PROFILE:
```json
{candidate_json}
```

TARGET JOB:
```json
{job_json}
```

GAP ANALYSIS:
```json
{gap_analysis}
```

ENHANCEMENT RULES:
✅ ALLOWED:
- Reframe existing content with better wording
- Add quantitative context from existing achievements
- Optimize keyword placement
- Improve action verbs
- Reorganize for relevance

❌ FORBIDDEN:
- Fabricate companies, roles, dates, degrees
- Add skills candidate doesn't have
- Invent projects or achievements
- Exaggerate beyond reasonable interpretation
- Create false certifications

QUALITY STANDARDS:
- Every enhancement must be interview-defensible
- Flag all AI-augmented content
- Maintain candidate's authentic voice
- Ensure ATS compatibility

OUTPUT SCHEMA (JSON):
{{
  "strategy": {{
    "target_role": "string",
    "key_focus": ["Emphasize Python/AWS", "Quantify achievements"],
    "keywords_to_add": ["microservices", "distributed systems"],
    "sections_to_emphasize": ["work_experience"]
  }},

  "enhanced_summary": {{
    "original": "string",
    "enhanced": "string",
    "changes": ["Added leadership focus", "Injected keywords"],
    "keywords_added": ["Backend Engineer", "Python", "AWS"]
  }},

  "enhanced_experience": [
    {{
      "company": "TechCorp (unchanged)",
      "title": "Senior Engineer (unchanged)",
      "dates": "2020-01 to Present (unchanged)",

      "achievements": [
        {{
          "enhanced": "Led development of microservices architecture serving 1M+ requests/day, improving system throughput by 40%",
          "original": "Led development of microservices architecture",
          "changes": [
            "Added metric: 1M+ requests/day",
            "Added impact: 40% improvement"
          ],
          "source": "inferred_from_context",
          "confidence": "high",
          "interview_defensible": true
        }}
      ]
    }}
  ],

  "skills_optimization": {{
    "reordered": {{
      "before": ["Python", "JavaScript", "AWS"],
      "after": ["Python", "AWS", "Docker", "JavaScript"],
      "reason": "Prioritized by JD requirements"
    }},
    "contextual_additions": [
      {{
        "skill": "AWS",
        "before": "AWS",
        "after": "AWS (EC2, S3, Lambda, CloudFormation)",
        "justification": "Specified from work experience context"
      }}
    ]
  }},

  "keyword_optimization": {{
    "added_keywords": [
      {{
        "keyword": "distributed systems",
        "occurrences": 3,
        "locations": ["summary", "experience"],
        "natural": true
      }}
    ]
  }},

  "content_additions": [
    {{
      "section": "work_experience",
      "company": "TechCorp",
      "type": "metric",
      "original": "Improved performance",
      "enhanced": "Improved performance by 40% through caching",
      "basis": "inferred_from_responsibility",
      "confidence": "medium",
      "verification_needed": false
    }}
  ],

  "removed_content": [
    {{
      "section": "volunteering",
      "reason": "Not relevant, save space",
      "content": "Library tutoring"
    }}
  ],

  "ats_score": {{
    "before": 65,
    "after": 92,
    "improvements": [
      "Added standard section headers",
      "Optimized keyword density",
      "Removed complex formatting"
    ]
  }},

  "quality_checks": {{
    "factual_accuracy": "passed",
    "authenticity_preserved": true,
    "interview_ready": true,
    "over_optimization": "low_risk",
    "fabrication_check": "clean"
  }},

  "change_summary": [
    "Enhanced summary with backend focus",
    "Added 5 quantitative metrics",
    "Reordered skills by JD priority",
    "Injected 8 target keywords naturally",
    "Removed non-relevant content"
  ],

  "interview_prep": [
    "Be ready to discuss 40% performance improvement details",
    "Prepare examples of distributed systems design",
    "Have metrics ready for all quantified claims"
  ]
}}

Return ONLY valid JSON. Prioritize ethics and accuracy.
"""

# ============================================================================
# QUALITY ASSURANCE PROMPT
# ============================================================================

QA_ENHANCED_RESUME_PROMPT = """
Review this enhanced resume for quality, accuracy, and ethical compliance.

ORIGINAL:
```json
{original_json}
```

ENHANCED:
```json
{enhanced_json}
```

VERIFICATION CHECKLIST:
1. No fabricated information
2. All metrics are reasonable/defensible
3. Skills accurately represented
4. Dates unchanged
5. Companies/titles unchanged
6. No keyword stuffing
7. Natural language flow
8. Interview defensibility

OUTPUT SCHEMA (JSON):
{{
  "approval": {{
    "status": "approved | needs_revision | rejected",
    "confidence": 0-100,
    "ethical_compliance": "pass | fail"
  }},

  "verification": {{
    "no_fabrications": boolean,
    "questionable_claims": [
      {{
        "claim": "Led 8-person team",
        "original": "No team size mentioned",
        "assessment": "acceptable | questionable | fabrication",
        "action": "Verify with candidate"
      }}
    ]
  }},

  "authenticity": {{
    "voice_preserved": boolean,
    "sounds_natural": boolean,
    "maintains_credibility": boolean
  }},

  "ats_check": {{
    "keyword_stuffing": "none | minimal | excessive",
    "readability": "excellent | good | poor",
    "formatting": "clean | needs_work"
  }},

  "issues": [
    {{
      "severity": "critical | high | medium | low",
      "category": "fabrication | optimization | authenticity",
      "issue": "description",
      "location": "section",
      "fix": "recommended action"
    }}
  ],

  "approval_conditions": [
    "Remove team size claim",
    "Soften metric in achievement 3"
  ] | null
}}

Return ONLY valid JSON.
"""

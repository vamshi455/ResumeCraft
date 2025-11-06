"""
Candidate matching prompts for job-candidate alignment analysis.
"""

# ============================================================================
# CANDIDATE MATCHING PROMPT
# ============================================================================

MATCH_CANDIDATE_TO_JOB_PROMPT = """
Analyze how well this candidate matches the job requirements. Provide detailed scoring and insights.

CANDIDATE PROFILE:
```json
{candidate_json}
```

JOB REQUIREMENTS:
```json
{job_json}
```

MATCHING RULES (from config):
{matching_rules}

MATCHING CRITERIA (WEIGHTED):
1. Technical Skills Match (30% weight) - Required vs preferred skills
2. Experience Relevance (25% weight) - Years and role fit
3. Location Compatibility (20% weight) - Remote/Hybrid/Onsite alignment
4. Education Fit (10% weight) - Degree and field of study
5. Soft Skills (8% weight) - Communication, leadership, teamwork
6. Culture Fit (7% weight) - Work style and values alignment

⚠️ CRITICAL: Location Compatibility Rules
- Remote job + Remote candidate = 100/100 (Perfect match)
- Remote job + Onsite candidate = 85/100 (Good - candidate may adjust)
- Onsite job + Remote candidate = 30/100 (Poor - major mismatch)
- Onsite job + Hybrid candidate = 60/100 (Weak - candidate may struggle)
- Hybrid = Mix of both, score accordingly
- Flexible = Can accommodate any preference (100/100)
- If candidate "Willing to Relocate" = Add +20 bonus to location score

OUTPUT SCHEMA (JSON):
{{
  "match_summary": {{
    "score": 0-100,
    "level": "excellent | strong | moderate | weak | poor",
    "recommendation": "highly_recommended | recommended | consider | not_recommended",
    "summary": "One sentence explanation"
  }},

  "detailed_scores": {{
    "skills": {{
      "score": 0-100,
      "weight": 0.30,
      "required_matched": [
        {{
          "skill": "Python",
          "has": true,
          "proficiency": "expert",
          "years": 5,
          "quality": "excellent"
        }}
      ],
      "required_missing": ["Kubernetes"],
      "match_percentage": 85
    }},

    "experience": {{
      "score": 0-100,
      "weight": 0.25,
      "years_match": {{
        "candidate": 5.5,
        "required": 5,
        "meets": true
      }},
      "relevant_roles": [
        {{
          "company": "TechCorp",
          "title": "Backend Engineer",
          "relevance": "high",
          "reason": "Built microservices with Python/AWS"
        }}
      ]
    }},

    "location": {{
      "score": 0-100,
      "weight": 0.20,
      "job_location": "Remote | Hybrid | Onsite | Flexible",
      "candidate_preference": "Remote | Hybrid | Onsite | Flexible",
      "willing_to_relocate": true | false,
      "compatibility": "excellent | good | moderate | poor",
      "reasoning": "Explanation of location score",
      "geographic_match": "same_city | same_state | same_country | international"
    }},

    "education": {{
      "score": 0-100,
      "weight": 0.10,
      "match": "meets | exceeds | below"
    }},

    "soft_skills": {{
      "score": 0-100,
      "weight": 0.08,
      "matched": ["Leadership", "Communication"]
    }},

    "culture_fit": {{
      "score": 0-100,
      "weight": 0.07,
      "indicators": ["Startup experience", "Autonomous work style"]
    }}
  }},

  "strengths": [
    {{
      "category": "technical",
      "strength": "Strong Python/AWS expertise with 5+ years",
      "impact": "high"
    }}
  ],

  "gaps": [
    {{
      "category": "technical",
      "gap": "No Kubernetes experience",
      "severity": "moderate",
      "type": "required",
      "addressable": "yes",
      "suggestion": "Has Docker background, can learn K8s"
    }}
  ],

  "red_flags": [
    "Frequent job hopping"
  ] | null,

  "interview_focus": [
    "Deep dive on distributed systems",
    "Kubernetes knowledge assessment"
  ],

  "enhancement_opportunities": [
    "Add more metrics to achievements",
    "Emphasize payment processing experience"
  ]
}}

Return ONLY valid JSON.
"""

# ============================================================================
# BATCH PROCESSING PROMPT - MULTIPLE CANDIDATES
# ============================================================================

BATCH_MATCH_CANDIDATES_PROMPT = """
Analyze multiple candidates against this job description. Rank and compare.

JOB DESCRIPTION:
```json
{job_json}
```

CANDIDATES:
```json
{candidates_json}
```

INSTRUCTIONS:
1. Score each candidate using the same criteria
2. Rank candidates by match quality
3. Provide comparative analysis
4. Highlight unique strengths of each
5. Recommend top 3 for interview

OUTPUT SCHEMA (JSON):
{{
  "ranked_candidates": [
    {{
      "rank": 1,
      "candidate_id": "uuid",
      "name": "string",
      "overall_score": 0-100,
      "match_level": "excellent | strong | moderate",
      "key_strengths": ["strength1", "strength2"],
      "main_gaps": ["gap1"] | null,
      "recommendation": "Interview immediately"
    }}
  ],

  "comparative_analysis": {{
    "top_skills_across_candidates": [
      "Python (4/5 candidates)",
      "AWS (3/5 candidates)"
    ],
    "common_gaps": ["Kubernetes", "Leadership experience"],
    "diversity_insights": "Mix of senior and mid-level candidates"
  }},

  "interview_recommendations": [
    {{
      "candidate_id": "uuid",
      "priority": "high | medium | low",
      "interview_focus": ["topic1", "topic2"],
      "concerns_to_address": ["concern1"] | null
    }}
  ]
}}

Return ONLY valid JSON.
"""

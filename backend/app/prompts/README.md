# CareerCraft LLM Prompt System

Production-ready prompts for AI-powered resume management, candidate matching, and resume enhancement.

## 📁 Package Structure

```
prompts/
├── __init__.py          # Package exports
├── base.py              # Core system and parsing prompts
├── matching.py          # Candidate-job matching prompts
├── enhancement.py       # Resume enhancement prompts
├── chat.py              # Conversational interface prompts
├── config.py            # LLM provider configurations
├── utils.py             # Utility functions
├── examples.py          # Usage examples and integration patterns
└── README.md            # This file
```

## 🚀 Quick Start

### Installation

```python
from app.prompts import (
    parse_resume_openai,
    match_candidate_openai,
    enhance_resume_openai,
    complete_candidate_workflow,
)
```

### Basic Usage

#### 1. Parse a Resume

```python
from app.prompts.examples import parse_resume_openai

resume_text = """
John Doe
Software Engineer
john.doe@email.com

Experience:
- Senior Backend Engineer at TechCorp (2020-Present)
- Built microservices with Python and AWS
"""

result = parse_resume_openai(resume_text, api_key="sk-...")

print(result['personal_info']['full_name'])  # "John Doe"
print(result['work_experience'][0]['company'])  # "TechCorp"
print(result['skills']['technical'])  # ["Python", "AWS", ...]
```

#### 2. Analyze Job Description

```python
from app.prompts import ANALYZE_JOB_DESCRIPTION_PROMPT, format_prompt
import openai

job_description = """
Backend Engineer - Python/AWS
We're looking for a senior engineer with 5+ years Python experience...
"""

prompt = format_prompt(ANALYZE_JOB_DESCRIPTION_PROMPT, job_description=job_description)

response = openai.ChatCompletion.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": CAREERCRAFT_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ],
    response_format={"type": "json_object"}
)

job_data = json.loads(response.choices[0].message.content)
```

#### 3. Match Candidate to Job

```python
from app.prompts.examples import match_candidate_openai

matching_result = match_candidate_openai(
    candidate_json=parsed_resume,
    job_json=analyzed_job,
    api_key="sk-..."
)

print(matching_result['match_summary']['score'])  # 85
print(matching_result['match_summary']['level'])  # "strong"
print(matching_result['gaps'])  # Missing skills/experience
```

#### 4. Enhance Resume

```python
from app.prompts.examples import enhance_resume_openai

enhanced = enhance_resume_openai(
    candidate_json=parsed_resume,
    job_json=analyzed_job,
    gap_analysis=matching_result['gaps'],
    api_key="sk-..."
)

print(enhanced['ats_score']['before'])  # 65
print(enhanced['ats_score']['after'])  # 92
print(enhanced['change_summary'])  # List of improvements
```

#### 5. Complete Workflow

```python
from app.prompts.examples import complete_candidate_workflow

result = complete_candidate_workflow(
    resume_text=resume_text,
    job_description=job_description,
    api_key="sk-...",
    enhance=True
)

# Returns:
# {
#   "candidate": {...},  # Parsed resume
#   "job": {...},        # Analyzed job
#   "matching": {...},   # Match analysis
#   "enhancement": {...} # Enhanced resume
# }
```

## 🔧 Configuration

### Using Different Providers

```python
from app.prompts.config import LLMProvider, get_llm_config

# OpenAI
config = get_llm_config(LLMProvider.OPENAI, task="parsing")

# Anthropic Claude
config = get_llm_config(LLMProvider.ANTHROPIC, task="enhancement")

# Custom overrides
config = get_llm_config(
    LLMProvider.OPENAI,
    task="matching",
    temperature=0.2,
    max_tokens=5000
)
```

### Task-Specific Temperatures

The system automatically applies optimal temperatures for different tasks:

- **Parsing**: 0.0 (deterministic)
- **Matching**: 0.1 (consistent scoring)
- **Enhancement**: 0.3 (creative rewriting)
- **Chat**: 0.7 (natural conversation)
- **QA**: 0.0 (deterministic checks)

## 📊 Batch Processing

### Match Multiple Candidates

```python
from app.prompts.examples import batch_match_candidates

candidates = [candidate1, candidate2, candidate3]
job = analyzed_job_description

results = batch_match_candidates(
    candidates=candidates,
    job_json=job,
    api_key="sk-..."
)

# Results:
# {
#   "ranked_candidates": [...],  # Sorted by score
#   "comparative_analysis": {...},
#   "interview_recommendations": [...]
# }

top_candidate = results['ranked_candidates'][0]
print(f"{top_candidate['name']}: {top_candidate['overall_score']}/100")
```

## 🛡️ Error Handling

### Safe LLM Calls

```python
from app.prompts.utils import safe_llm_call

result = safe_llm_call(
    llm_function=your_llm_function,
    prompt=formatted_prompt,
    system_prompt=CAREERCRAFT_SYSTEM_PROMPT,
    max_retries=3,
    retry_delay=1.0
)

if result['success']:
    data = result['data']
else:
    print(f"Error: {result['error']}")
    print(f"Details: {result['details']}")
```

### JSON Validation

```python
from app.prompts.utils import validate_json_response, validate_schema

# Parse and validate JSON
data = validate_json_response(llm_response)

# Check required fields
required_fields = ['personal_info', 'work_experience', 'skills']
is_valid = validate_schema(data, required_fields)
```

## 💰 Cost Estimation

```python
from app.prompts.examples import estimate_workflow_cost

cost = estimate_workflow_cost(
    resume_length=2000,  # characters
    job_description_length=1000,
    enhance=True,
    model="gpt-4-turbo-preview"
)

print(f"Parsing: ${cost['parsing']:.4f}")
print(f"Matching: ${cost['matching']:.4f}")
print(f"Enhancement: ${cost['enhancement']:.4f}")
print(f"Total: ${cost['total']:.4f}")
```

## 💬 Chat Interface

```python
from app.prompts.examples import chat_with_careercraft

conversation_history = []

user_message = "How can I improve my resume for a senior engineer role?"

response = chat_with_careercraft(
    user_message=user_message,
    conversation_history=conversation_history,
    api_key="sk-...",
    resume_count=5,
    job_count=3,
    recent_activity="Uploaded 2 resumes today"
)

print(response)

# Update history
conversation_history.append({"role": "user", "content": user_message})
conversation_history.append({"role": "assistant", "content": response})
```

## 🔍 Advanced Features

### Skill Normalization

```python
from app.prompts import NORMALIZE_SKILLS_PROMPT, format_prompt

text = "Experienced with JS, React.js, node, and AWS cloud services"

prompt = format_prompt(NORMALIZE_SKILLS_PROMPT, text=text)
# Returns normalized skills: JavaScript, React, Node.js, AWS
```

### Quality Assurance

```python
from app.prompts import QA_ENHANCED_RESUME_PROMPT

qa_result = qa_enhanced_resume(
    original_json=original_resume,
    enhanced_json=enhanced_resume,
    api_key="sk-..."
)

if qa_result['approval']['status'] == 'approved':
    print("Enhancement approved!")
else:
    print("Issues found:", qa_result['issues'])
```

## 📝 Response Schemas

### Parsed Resume

```json
{
  "personal_info": {
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-234-567-8900",
    "location": "San Francisco, CA",
    "linkedin_url": "linkedin.com/in/johndoe",
    "github_url": "github.com/johndoe"
  },
  "summary": {
    "headline": "Senior Backend Engineer",
    "summary_text": "Experienced engineer with 7+ years...",
    "years_experience": 7.5,
    "experience_level": "senior"
  },
  "work_experience": [...],
  "education": [...],
  "skills": {
    "technical": ["Python", "AWS", "Docker"],
    "soft_skills": ["Leadership", "Communication"],
    "domain_knowledge": ["FinTech", "Microservices"],
    "tools": ["Git", "Jira"]
  },
  "confidence": {
    "overall": 95,
    "personal_info": 100,
    "work_experience": 95,
    "skills": 90
  }
}
```

### Match Result

```json
{
  "match_summary": {
    "score": 85,
    "level": "strong",
    "recommendation": "recommended",
    "summary": "Strong technical fit with minor gaps"
  },
  "detailed_scores": {
    "skills": {"score": 90, "match_percentage": 85},
    "experience": {"score": 85, "years_match": {"meets": true}},
    "education": {"score": 90, "match": "meets"}
  },
  "strengths": [...],
  "gaps": [...],
  "interview_focus": [...]
}
```

## 🔐 Security & Ethics

### Ethical Guidelines

The enhancement prompts follow strict ethical guidelines:

✅ **Allowed:**
- Reframe existing content
- Add quantitative context
- Optimize keywords
- Improve action verbs

❌ **Forbidden:**
- Fabricate information
- Add non-existent skills
- Invent experiences
- False certifications

### Privacy

- Never log or store API keys
- Sanitize sensitive information from logs
- Use secure API connections only
- Follow data retention policies

## 🧪 Testing

```python
# Test resume parsing
def test_parse_resume():
    resume = "John Doe\nSoftware Engineer..."
    result = parse_resume_openai(resume, api_key)
    assert result['personal_info']['full_name'] == "John Doe"
    assert 'work_experience' in result
    assert result['confidence']['overall'] > 80

# Test matching
def test_match_candidate():
    match = match_candidate_openai(candidate, job, api_key)
    assert 0 <= match['match_summary']['score'] <= 100
    assert match['match_summary']['level'] in ['excellent', 'strong', 'moderate', 'weak', 'poor']
```

## 📚 Best Practices

1. **Always validate JSON responses** using `validate_json_response()`
2. **Use task-specific configurations** via `get_llm_config(task=...)`
3. **Implement retry logic** for production systems
4. **Monitor costs** using the estimation utilities
5. **Log all LLM calls** for debugging and auditing
6. **Cache frequently used results** (e.g., job analysis)
7. **Batch similar requests** to reduce API calls
8. **Use quality checks** before accepting enhanced content

## 🐛 Troubleshooting

### Invalid JSON Response

```python
# The utility automatically strips markdown code blocks
response = validate_json_response(llm_response)
# Handles: ```json\n{...}\n``` and ```{...}```
```

### Rate Limiting

```python
from app.prompts.utils import safe_llm_call

# Automatically retries with exponential backoff
result = safe_llm_call(
    llm_function=parse_resume_openai,
    max_retries=5,
    retry_delay=2.0
)
```

### Low Confidence Scores

```python
from app.prompts.utils import extract_confidence_score

confidence = extract_confidence_score(parsed_resume)
if confidence < 70:
    # Flag for human review
    needs_review = parsed_resume['confidence']['needs_review']
    print(f"Low confidence. Review: {needs_review}")
```

## 📖 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic Claude API](https://docs.anthropic.com)
- [CareerCraft API Documentation](../README.md)

## 🤝 Contributing

When adding new prompts:

1. Follow the existing schema patterns
2. Include confidence scores
3. Add validation rules
4. Document expected outputs
5. Add usage examples
6. Test with multiple providers

## 📄 License

See main project LICENSE file.

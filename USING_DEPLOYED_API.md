# Using Your Deployed ResumeCraft API

Congratulations! Your ResumeCraft LangGraph workflow is now deployed on LangSmith Cloud! 🎉

## What You're Seeing

```json
{"detail":"Missing authentication headers"}
```

This is **good news** - it means:
- ✅ Your deployment is live
- ✅ The API is running
- ✅ It's secured and waiting for authenticated requests

## Getting Your API Details

1. **Go to LangSmith Dashboard**: https://smith.langchain.com/deployments
2. **Find your deployment**: "resumecraft" or similar
3. **Get these details**:
   - **Deployment URL**: `https://api.smith.langchain.com/deployments/{deployment-id}`
   - **API Key**: Your LangSmith API key (from Settings → API Keys)

## Option 1: Test with cURL

```bash
# Replace with your actual values
DEPLOYMENT_URL="https://api.smith.langchain.com/deployments/YOUR-DEPLOYMENT-ID"
LANGSMITH_API_KEY="lsv2_pt_your_api_key_here"

# Test the deployment
curl -X POST "$DEPLOYMENT_URL/invoke" \
  -H "Authorization: Bearer $LANGSMITH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "resume_text": "John Doe\nSoftware Engineer with 5 years Python experience\nSkills: Python, Django, PostgreSQL",
      "job_description": "Looking for Senior Python Developer with Django experience"
    }
  }'
```

## Option 2: Test with Python

Create a test script:

```python
# test_deployment.py
import requests
import json
import os

# Your deployment details
DEPLOYMENT_URL = "https://api.smith.langchain.com/deployments/YOUR-DEPLOYMENT-ID"
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")  # or paste your key

def test_workflow(resume_text, job_description):
    """Test the deployed workflow"""

    headers = {
        "Authorization": f"Bearer {LANGSMITH_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": {
            "resume_text": resume_text,
            "job_description": job_description
        }
    }

    response = requests.post(
        f"{DEPLOYMENT_URL}/invoke",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        result = response.json()
        print("✅ Success!")
        print(json.dumps(result, indent=2))
        return result
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

# Test it
if __name__ == "__main__":
    resume = """
    John Doe
    Software Engineer

    Experience:
    - 5 years Python development
    - Django, Flask frameworks
    - PostgreSQL, Redis
    - AWS deployment

    Skills: Python, Django, PostgreSQL, Docker, AWS
    """

    job = """
    Senior Python Developer

    Requirements:
    - 5+ years Python experience
    - Django framework expertise
    - Database design skills
    - Cloud deployment experience
    """

    result = test_workflow(resume, job)
```

Run it:
```bash
export LANGSMITH_API_KEY="lsv2_pt_your_key_here"
python test_deployment.py
```

## Option 3: Use LangGraph SDK

```python
# Using official SDK
from langgraph_sdk import get_client

# Initialize client
client = get_client(
    url="https://api.smith.langchain.com",
    api_key="lsv2_pt_your_key_here"
)

# Create a thread and run workflow
thread = client.threads.create()

result = client.runs.create(
    thread_id=thread["thread_id"],
    assistant_id="YOUR-DEPLOYMENT-ID",
    input={
        "resume_text": "John Doe\nSoftware Engineer...",
        "job_description": "Looking for Senior Python Developer..."
    }
)

print(result)
```

## Option 4: Connect Your Streamlit Apps

Update your Streamlit apps to call the deployed backend:

```python
# In your Streamlit app (e.g., app_entity_resolution.py)
import os
import requests
import streamlit as st

# Configuration
LANGGRAPH_API_URL = os.getenv("LANGGRAPH_API_URL")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

def process_resume(resume_text, job_description):
    """Call deployed LangGraph workflow"""

    headers = {
        "Authorization": f"Bearer {LANGSMITH_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": {
            "resume_text": resume_text,
            "job_description": job_description
        }
    }

    try:
        response = requests.post(
            f"{LANGGRAPH_API_URL}/invoke",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

# Use in your Streamlit app
st.title("Resume Matcher")

resume_text = st.text_area("Resume")
job_description = st.text_area("Job Description")

if st.button("Match"):
    with st.spinner("Processing..."):
        result = process_resume(resume_text, job_description)
        if result:
            st.success("✅ Analysis complete!")
            st.json(result)
```

## API Endpoints

Your deployed workflow exposes these endpoints:

### 1. Invoke (Synchronous)
```
POST /invoke
```
Runs the workflow and waits for completion.

**Request:**
```json
{
  "input": {
    "resume_text": "...",
    "job_description": "..."
  }
}
```

**Response:**
```json
{
  "output": {
    "status": "completed",
    "match_score": 85,
    "parsed_resume": {...},
    "analyzed_job": {...},
    "match_result": {...},
    "final_recommendation": "..."
  }
}
```

### 2. Stream (Async)
```
POST /stream
```
Streams workflow execution in real-time.

### 3. Threads (Stateful)
```
POST /threads
GET /threads/{thread_id}
```
Create and manage stateful conversations.

## Expected Response Format

When you successfully call your deployed API, you'll get:

```json
{
  "output": {
    "status": "completed",
    "resume_text": "...",
    "job_description": "...",
    "parsed_resume": {
      "name": "John Doe",
      "email": "john@example.com",
      "skills": ["Python", "Django", "PostgreSQL"],
      "experience": [...]
    },
    "analyzed_job": {
      "title": "Senior Python Developer",
      "required_skills": ["Python", "Django"],
      "experience_required": "5+ years"
    },
    "match_score": 85,
    "match_result": {
      "matching_skills": ["Python", "Django", "PostgreSQL"],
      "missing_skills": [],
      "score_breakdown": {...}
    },
    "enhanced_resume": {...},
    "qa_result": {...},
    "final_recommendation": "Strong match - Recommend for interview..."
  },
  "metadata": {
    "run_id": "...",
    "thread_id": "..."
  }
}
```

## Monitoring Your Deployment

### View Traces
1. Go to https://smith.langchain.com
2. Select project: "resumecraft-prod" (or your project name)
3. See all workflow executions:
   - Individual agent performance
   - Token usage and costs
   - Error rates
   - Latency metrics

### View Deployment Logs
1. Go to https://smith.langchain.com/deployments
2. Click your deployment
3. View:
   - **Logs**: Runtime logs
   - **Metrics**: Request volume, latency
   - **Revisions**: Deployment history

## Cost Tracking

Monitor your costs in LangSmith:

### LangSmith Cloud Costs
- **Plus Plan**: $99/month
  - 100k traces included
  - $0.001 per additional trace

### Claude API Costs
- **Claude 3 Haiku**:
  - Input: $0.25 / 1M tokens
  - Output: $1.25 / 1M tokens
  - ~$0.42 per resume processing

### Total Monthly Estimate
```
100 resumes/month:
- LangSmith: $99
- Claude: $42
Total: $141/month

1,000 resumes/month:
- LangSmith: $99
- Claude: $420
Total: $519/month
```

## Troubleshooting

### Authentication Error
```json
{"detail":"Missing authentication headers"}
```
**Fix**: Add `Authorization: Bearer YOUR_API_KEY` header

### Not Found Error
```json
{"detail":"Not found"}
```
**Fix**: Check deployment URL is correct

### Timeout Error
```
Request timeout after 60s
```
**Fix**: Increase timeout or optimize slow agents

### Invalid Input
```json
{"detail":"Input validation error"}
```
**Fix**: Ensure `resume_text` and `job_description` are provided

## Next Steps

1. **Test your API** using one of the methods above
2. **Update Streamlit apps** to use deployed backend
3. **Monitor performance** in LangSmith dashboard
4. **Optimize** based on trace data
5. **Scale** - LangSmith auto-scales for you!

## Getting Help

- **Deployment Issues**: https://docs.langchain.com/langsmith/deployments
- **API Reference**: https://docs.smith.langchain.com/api
- **Community**: https://github.com/langchain-ai/langgraph/discussions
- **Support**: support@langchain.com (Plus/Enterprise)

---

**Congratulations on your deployment!** 🚀

Your ResumeCraft workflow is now running in production on LangSmith Cloud with:
- ✅ Auto-scaling
- ✅ Built-in monitoring
- ✅ Production-grade infrastructure
- ✅ Zero maintenance

Start sending requests and watch the traces in your LangSmith dashboard!

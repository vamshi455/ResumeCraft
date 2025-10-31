# Deploy ResumeCraft to LangSmith Cloud

This guide walks you through deploying your ResumeCraft LangGraph workflow to LangSmith Cloud directly from GitHub.

## Prerequisites

Before you begin, ensure you have:

- ✅ GitHub repository (you have this: vamshi455/ResumeCraft)
- ✅ LangSmith Plus or Enterprise account ($99+/month)
- ✅ Anthropic API key
- ✅ All configuration files (created ✅)

## What Gets Deployed

Your ResumeCraft workflow includes:
- **LangGraph Workflow**: Multi-agent recruitment pipeline ([app/graphs/workflow.py](backend/app/graphs/workflow.py))
- **6 Agents**: Parser, Job Analyzer, Matcher, Enhancer, QA, Supervisor
- **State Management**: Full recruitment state tracking
- **Claude Integration**: Anthropic Claude 3 Haiku

**Note**: Streamlit UI apps run separately. LangSmith Cloud hosts the LangGraph backend only.

## Configuration Files Created

✅ **langgraph.json** - LangGraph deployment configuration
```json
{
  "python_version": "3.12",
  "dependencies": ["requirements_streamlit.txt"],
  "graphs": {
    "recruitment": "app.graphs.workflow:create_recruitment_workflow"
  },
  "env": ".env"
}
```

✅ **requirements updates** - Added langsmith packages
✅ **.env.example** - LangSmith environment variables

## Step-by-Step Deployment

### Step 1: Get LangSmith Account (5 minutes)

1. **Sign up for LangSmith**
   - Visit: https://smith.langchain.com
   - Create account or log in
   - Choose plan:
     * **Plus**: $99/month (100k traces, deployments)
     * **Enterprise**: Custom pricing (unlimited, support)

2. **Get API Key**
   - Click profile → **Settings** → **API Keys**
   - Click **Create API Key**
   - Copy key (starts with `lsv2_pt_...`)
   - Save securely

### Step 2: Connect GitHub Repository (5 minutes)

1. **Navigate to Deployments**
   - In LangSmith dashboard
   - Go to **Deployments** → **New Deployment**

2. **Connect GitHub**
   - Click **Connect GitHub**
   - Authorize LangSmith to access your repos
   - Select repository: `vamshi455/ResumeCraft`
   - Select branch: `main`

3. **Configure Build**
   - **Root directory**: `backend`
   - **Config file**: `langgraph.json` (auto-detected)
   - **Python version**: 3.12 (from langgraph.json)

### Step 3: Configure Environment Variables (5 minutes)

In the LangSmith deployment settings, add these environment variables:

#### Required Variables

```bash
# Anthropic API (Required for Claude)
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# LangSmith Configuration (Auto-configured)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=resumecraft-prod
```

#### Optional Variables

```bash
# Workflow Settings
MAX_ENHANCEMENT_ITERATIONS=3
MIN_CONFIDENCE_THRESHOLD=70
MIN_MATCH_SCORE=40

# LLM Settings
DEFAULT_TEMPERATURE=0.1
MAX_TOKENS=4000
```

**Important**: Keep your ANTHROPIC_API_KEY secure. Never commit it to git.

### Step 4: Deploy (2 minutes)

1. **Review Configuration**
   - Check all settings
   - Verify environment variables
   - Confirm build configuration

2. **Click "Deploy"**
   - LangSmith will:
     * Clone your repository
     * Install dependencies
     * Build Docker image
     * Deploy to infrastructure
     * Run health checks

3. **Monitor Deployment**
   - Watch build logs in real-time
   - Typical deployment: 3-5 minutes
   - Wait for status: **Running ✅**

### Step 5: Get Your API Endpoint (1 minute)

Once deployed, you'll receive:

```
Deployment URL: https://api.smith.langchain.com/deployments/{deployment-id}
API Key: (auto-generated or use your LangSmith key)
```

## Using Your Deployed Workflow

### Option A: API Calls (Programmatic)

```python
import requests

url = "https://api.smith.langchain.com/deployments/{deployment-id}/invoke"
headers = {
    "Authorization": f"Bearer {langsmith_api_key}",
    "Content-Type": "application/json"
}

payload = {
    "input": {
        "resume_text": "John Doe\nSoftware Engineer...",
        "job_description": "Senior Python Developer..."
    }
}

response = requests.post(url, json=payload, headers=headers)
result = response.json()

print(f"Match Score: {result['match_score']}")
print(f"Recommendation: {result['final_recommendation']}")
```

### Option B: LangGraph SDK

```python
from langgraph_sdk import get_client

client = get_client(url="https://api.smith.langchain.com")

# Run workflow
result = await client.runs.create(
    assistant_id="{deployment-id}",
    thread_id="thread-123",
    input={
        "resume_text": "...",
        "job_description": "..."
    }
)

print(result)
```

### Option C: Connect Streamlit Apps

Update your Streamlit apps to call the deployed backend:

```python
# In your Streamlit app
import os
import requests

LANGGRAPH_API_URL = os.getenv("LANGGRAPH_API_URL")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

def process_resume(resume_text, job_description):
    """Call deployed LangGraph workflow"""
    response = requests.post(
        f"{LANGGRAPH_API_URL}/invoke",
        headers={"Authorization": f"Bearer {LANGSMITH_API_KEY}"},
        json={
            "input": {
                "resume_text": resume_text,
                "job_description": job_description
            }
        }
    )
    return response.json()
```

## Architecture After Deployment

```
┌─────────────────────────────────────────────┐
│     Streamlit Apps (Separate Hosting)      │
│   - Template Formatter (Streamlit Cloud)   │
│   - Entity Resolution (Streamlit Cloud)    │
└──────────────────┬──────────────────────────┘
                   │ API calls
                   ↓
┌─────────────────────────────────────────────┐
│      LangGraph Backend (LangSmith Cloud)    │
│   - Auto-scaling                            │
│   - Managed infrastructure                  │
│   - Built-in monitoring                     │
└──────────────────┬──────────────────────────┘
                   │ LLM calls
                   ↓
┌─────────────────────────────────────────────┐
│         Anthropic Claude API                │
└─────────────────────────────────────────────┘
```

## Deploy Streamlit Apps Separately

### Option 1: Streamlit Cloud (Recommended for UI)

1. **Connect to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Connect GitHub repo
   - Select app file: `backend/app.py`

2. **Configure Environment**
   ```bash
   LANGGRAPH_API_URL=https://api.smith.langchain.com/deployments/{id}
   LANGSMITH_API_KEY=your-key
   ANTHROPIC_API_KEY=your-key
   ```

3. **Deploy**
   - Click Deploy
   - Access at: https://your-app.streamlit.app

### Option 2: Docker (Self-Hosted UI)

```bash
# Use existing Docker setup for UI only
docker-compose up -d

# Configure to call LangSmith backend
export LANGGRAPH_API_URL=https://api.smith.langchain.com/deployments/{id}
```

## Monitoring & Observability

### Built-in Features

Once deployed to LangSmith Cloud, you automatically get:

1. **Traces**: Every workflow execution traced
2. **Metrics**: Latency, token usage, costs
3. **Logs**: Real-time application logs
4. **Alerts**: Configure for errors, latency
5. **Dashboards**: Pre-built performance dashboards

### Accessing Traces

1. Go to LangSmith dashboard
2. Select project: `resumecraft-prod`
3. View:
   - All runs
   - Success/failure rates
   - Performance metrics
   - Individual traces with full details

### Example Trace View

```
Run ID: abc123
Status: ✅ Success
Duration: 14.2s
Tokens: 28,456 ($0.42)

Execution Flow:
├─ parser (2.3s, 4,123 tokens, $0.06)
├─ job_analyzer (1.8s, 5,234 tokens, $0.08)
├─ matcher (3.1s, 8,234 tokens, $0.12)
├─ enhancer (5.4s, 15,432 tokens, $0.23)
└─ qa (1.2s, 3,123 tokens, $0.05)
```

## Updating Your Deployment

### Automatic Deployments

Configure auto-deploy on git push:

1. **In LangSmith Dashboard**
   - Go to deployment settings
   - Enable **Auto Deploy**
   - Select branch: `main`

2. **Now, whenever you push to main:**
   ```bash
   git add .
   git commit -m "Update workflow"
   git push origin main
   # LangSmith automatically rebuilds and deploys
   ```

### Manual Deployments

1. Push changes to GitHub
2. Go to LangSmith dashboard
3. Click **Redeploy**
4. Select commit/branch
5. Deploy

## Scaling & Performance

### Auto-Scaling (Built-in)

LangSmith Cloud automatically scales based on:
- Request volume
- Response times
- Resource usage

No configuration needed!

### Performance Optimization

Monitor these metrics to optimize:

1. **Agent Latency**
   - Which agents are slowest?
   - Optimize prompts or logic

2. **Token Usage**
   - Which agents use most tokens?
   - Consider smaller models for simple tasks

3. **Error Rates**
   - Where do failures occur?
   - Add validation or error handling

## Cost Estimation

### LangSmith Cloud Costs

```
Plan: Plus ($99/month)
- 100,000 traces/month included
- 1 GB storage
- Auto-scaling infrastructure

Additional:
- Extra traces: $0.001/trace
- Extra storage: $0.10/GB
```

### Claude API Costs

```
Claude 3 Haiku (current model):
- Input: $0.25 / 1M tokens
- Output: $1.25 / 1M tokens

Average per resume processing:
- ~28,000 tokens
- Cost: ~$0.42 per resume
```

### Total Monthly Estimate

```
Low volume (100 resumes/month):
- LangSmith: $99
- Claude API: $42
- Total: $141/month

Medium volume (1,000 resumes/month):
- LangSmith: $99
- Claude API: $420
- Total: $519/month

High volume (10,000 resumes/month):
- LangSmith: $99-199 (extra traces)
- Claude API: $4,200
- Total: $4,299-4,399/month
```

## Troubleshooting

### Deployment Fails

**Check:**
- ✅ langgraph.json is valid JSON
- ✅ requirements_streamlit.txt has no errors
- ✅ Python version matches (3.12)
- ✅ All imports are correct

**View logs:**
- In LangSmith dashboard
- Click deployment → Logs
- Check build and runtime logs

### Runtime Errors

**Common issues:**

1. **Missing API Key**
   ```
   Error: ANTHROPIC_API_KEY not set
   Fix: Add in deployment environment variables
   ```

2. **Import Errors**
   ```
   Error: ModuleNotFoundError: No module named 'X'
   Fix: Add missing package to requirements_streamlit.txt
   ```

3. **Timeout Errors**
   ```
   Error: Request timeout
   Fix: Increase timeout in LangGraph config or optimize slow agents
   ```

### Getting Help

- **Documentation**: https://docs.langchain.com/langsmith/deployments
- **Community**: https://github.com/langchain-ai/langgraph/discussions
- **Support**: support@langchain.com (Plus/Enterprise)
- **Status**: https://status.langchain.com

## Best Practices

### 1. Environment Management

```bash
# Use separate environments
Development: LANGCHAIN_PROJECT=resumecraft-dev
Staging: LANGCHAIN_PROJECT=resumecraft-staging
Production: LANGCHAIN_PROJECT=resumecraft-prod
```

### 2. Version Control

```bash
# Tag releases
git tag -a v1.0.0 -m "Production release v1.0.0"
git push origin v1.0.0

# Deploy specific version in LangSmith
```

### 3. Testing Before Deploy

```bash
# Test locally first
cd backend
langgraph test

# Test with LangSmith (local)
LANGCHAIN_TRACING_V2=true langgraph dev
```

### 4. Monitor Deployments

- Set up alerts for:
  * Error rate > 5%
  * Latency > 30s
  * Token usage spikes
- Review traces weekly
- Optimize based on data

### 5. Cost Management

- Set budget alerts in Anthropic dashboard
- Monitor token usage in LangSmith
- Optimize expensive agents
- Consider caching for repeated queries

## Rollback Strategy

If deployment has issues:

1. **Instant Rollback** (via UI)
   - Go to deployments
   - Click "Rollback to previous version"
   - Select last working deployment

2. **Manual Rollback** (via git)
   ```bash
   git revert HEAD
   git push origin main
   # Auto-deploys previous version
   ```

## Next Steps

1. ✅ **Deploy**: Follow steps above
2. 📊 **Monitor**: Watch traces for 1 week
3. 🔧 **Optimize**: Based on performance data
4. 🎨 **Update UI**: Connect Streamlit to API
5. 📈 **Scale**: Let LangSmith auto-scale as needed

## Resources

- **LangSmith Dashboard**: https://smith.langchain.com
- **Deployment Docs**: https://docs.langchain.com/langsmith/deployments
- **LangGraph Cloud Docs**: https://langchain-ai.github.io/langgraph/cloud/
- **API Reference**: https://api.python.langchain.com
- **Your Repository**: https://github.com/vamshi455/ResumeCraft

---

**Ready to deploy?** Follow Step 1 above and get started! 🚀

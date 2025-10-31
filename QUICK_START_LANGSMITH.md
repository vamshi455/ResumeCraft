# Quick Start: Add LangSmith to ResumeCraft (5 Minutes)

Get observability and monitoring for your ResumeCraft workflow without changing deployment.

## What You'll Get

- 🔍 **Trace every workflow execution**: See each agent's processing steps
- 📊 **Monitor performance**: Track latency, token usage, and costs
- 🐛 **Debug issues**: Inspect inputs/outputs at each node
- 📈 **Analytics**: Success rates, error patterns, bottlenecks

## Prerequisites

- Your existing ResumeCraft setup (already have this ✅)
- LangSmith account (free tier available)

## Step 1: Get LangSmith API Key (2 minutes)

1. Visit https://smith.langchain.com
2. Sign up or log in
3. Click your profile → **Settings** → **API Keys**
4. Click **Create API Key**
5. Copy the key (starts with `lsv2_pt_...`)

## Step 2: Update Configuration (2 minutes)

### Add to requirements

```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft/backend
echo "langsmith>=0.1.0" >> requirements_streamlit.txt
```

### Update environment file

Edit `backend/.env` and add:

```bash
# LangSmith Observability
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_your_api_key_here
LANGCHAIN_PROJECT=resumecraft
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

Replace `lsv2_pt_your_api_key_here` with your actual API key.

## Step 3: Restart Application (1 minute)

### If using Docker:

```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft
docker-compose down
docker-compose build
docker-compose up -d
```

### If running locally:

```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft/backend
./venv/bin/pip install langsmith
./venv/bin/streamlit run app.py
```

## Step 4: Test & View Traces

1. **Process a resume** through your application
2. **Open LangSmith**: https://smith.langchain.com/projects
3. **Select project**: Click on "resumecraft"
4. **View traces**: See your workflow execution!

## What You'll See

### Workflow Trace Example

```
Recruitment Workflow Execution
├─ parser (2.3s)
│  ├─ Input: resume_text
│  └─ Output: parsed_resume
├─ job_analyzer (1.8s)
│  ├─ Input: job_description
│  └─ Output: analyzed_job
├─ matcher (3.1s)
│  ├─ Input: parsed_resume, analyzed_job
│  └─ Output: match_score, match_result
├─ enhancer (5.4s)
│  ├─ Iteration 1 (2.7s)
│  └─ Iteration 2 (2.7s)
└─ qa (1.2s)
   └─ Output: final_recommendation
```

Each node shows:
- Execution time
- Input data
- Output data
- LLM calls made
- Token usage
- Error details (if any)

## Viewing Your Data

### Dashboard Overview
- **Runs**: All workflow executions
- **Traces**: Detailed execution trees
- **Feedback**: Add ratings to traces
- **Datasets**: Create test sets
- **Analytics**: Performance metrics

### Key Metrics to Watch

1. **Latency**
   - Which agent takes longest?
   - Where are bottlenecks?

2. **Token Usage**
   - Cost per execution
   - Most expensive nodes

3. **Success Rate**
   - How often do workflows complete?
   - Common failure points

4. **Quality**
   - Add feedback scores
   - Track over time

## Advanced Features (Optional)

### Add Custom Metadata

Update your workflow to add tags:

```python
from langsmith import trace

@trace(tags=["production", "resume-parsing"])
def parse_resume_only(llm: BaseChatModel, resume_text: str):
    # Your existing code
    pass
```

### Create Evaluation Datasets

1. In LangSmith, go to **Datasets**
2. Click **New Dataset**
3. Add test cases:
   - Input: sample resume + job description
   - Expected output: match score, recommendations

### Set Up Alerts

Configure notifications for:
- High latency (> 10s)
- Error rates (> 5%)
- Token usage spikes

## Troubleshooting

### Not seeing traces?

1. **Check environment variables**
   ```bash
   # In your app, add this to verify:
   import os
   print(f"Tracing enabled: {os.getenv('LANGCHAIN_TRACING_V2')}")
   print(f"Project: {os.getenv('LANGCHAIN_PROJECT')}")
   ```

2. **Verify API key**
   - Should start with `lsv2_pt_`
   - Check it's not commented out in `.env`

3. **Check internet connectivity**
   - LangSmith needs outbound HTTPS access

### Seeing errors?

```bash
# Check logs
docker-compose logs -f resumecraft

# Or if running locally
# Check terminal output
```

Common issues:
- Invalid API key → Double-check the key
- Network blocked → Check firewall rules
- Import error → Reinstall: `pip install -U langsmith`

## Cost & Limits

### Free Tier
- ✅ 5,000 traces/month
- ✅ 14-day retention
- ✅ Basic features

### Plus Plan ($49/month)
- ✅ 100,000 traces/month
- ✅ 90-day retention
- ✅ Advanced features
- ✅ Collaboration tools

### Enterprise (Custom pricing)
- ✅ Unlimited traces
- ✅ Custom retention
- ✅ SSO, RBAC
- ✅ Dedicated support

Start with free tier, upgrade as needed!

## What's Next?

1. **Analyze your workflow**
   - Identify slow agents
   - Find error patterns
   - Optimize prompts

2. **Set up monitoring**
   - Create dashboards
   - Configure alerts
   - Track KPIs

3. **Improve quality**
   - Add evaluation datasets
   - Run experiments
   - A/B test changes

4. **Scale deployment**
   - When ready, see [LANGSMITH_DEPLOYMENT_OPTIONS.md](LANGSMITH_DEPLOYMENT_OPTIONS.md)
   - Choose production deployment

## Examples of Insights You'll Get

### 1. Find Bottlenecks
```
Agent Performance:
- parser: 2.3s avg (fast ✅)
- job_analyzer: 1.8s avg (fast ✅)
- matcher: 3.1s avg (ok ⚠️)
- enhancer: 5.4s avg (slow 🔴)
- qa: 1.2s avg (fast ✅)

→ Optimize enhancer agent!
```

### 2. Track Costs
```
Token Usage:
- enhancer: 15,432 tokens ($0.23)
- matcher: 8,234 tokens ($0.12)
- parser: 4,123 tokens ($0.06)

Total: $0.41 per resume

→ Consider caching or smaller models for parser
```

### 3. Debug Failures
```
Error Pattern Found:
- 12 failures in matcher agent
- Common input: missing job requirements
- Error: "KeyError: 'required_skills'"

→ Add validation in job_analyzer
```

## Resources

- **LangSmith Docs**: https://docs.smith.langchain.com
- **API Reference**: https://api.python.langchain.com/en/latest/langsmith/langsmith.html
- **Examples**: https://github.com/langchain-ai/langsmith-cookbook
- **Community**: https://github.com/langchain-ai/langsmith-sdk/discussions

## Support

- **Documentation Issues**: https://github.com/langchain-ai/langsmith-docs
- **SDK Issues**: https://github.com/langchain-ai/langsmith-sdk
- **Feature Requests**: https://langchain.canny.io/
- **Enterprise Support**: sales@langchain.com

---

**That's it!** You now have observability for your ResumeCraft workflow. No deployment changes, just better visibility. 🎉

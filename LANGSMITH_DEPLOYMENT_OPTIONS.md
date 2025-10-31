# LangSmith Deployment Options for ResumeCraft

## Overview

This guide outlines deployment options for ResumeCraft using LangSmith and LangGraph Platform. Your application uses LangGraph for the recruitment workflow ([workflow.py:33-150](backend/app/graphs/workflow.py#L33-L150)), making it compatible with LangSmith's deployment infrastructure.

## Current Architecture

ResumeCraft is built with:
- **LangGraph workflow**: Multi-agent recruitment pipeline
- **Streamlit UI**: Two apps (main + entity resolution)
- **Anthropic Claude**: LLM provider (Haiku model)
- **Docker support**: Ready for containerization

## Deployment Options

### Option 1: LangSmith Cloud (Recommended for Quick Start)

**Best for**: Teams wanting managed infrastructure with zero maintenance

**Features**:
- Fully managed hosting
- Automatic scaling
- Built-in monitoring via LangSmith
- Easy deployment from git repository
- No infrastructure management

**Setup Steps**:

1. **Sign up for LangSmith**
   ```bash
   # Get API key from https://smith.langchain.com/
   ```

2. **Add LangSmith to your environment**
   ```bash
   # Add to backend/.env
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your-langsmith-api-key
   LANGCHAIN_PROJECT=resumecraft
   ```

3. **Install LangSmith SDK**
   ```bash
   pip install langsmith
   ```

4. **Configure the workflow for LangSmith tracing**
   ```python
   # Already compatible - LangGraph automatically traces to LangSmith
   # when LANGCHAIN_TRACING_V2=true
   ```

5. **Deploy via LangSmith UI**
   - Connect your GitHub repository
   - Configure build settings
   - Push to deploy

**Pricing**: Requires LangSmith Plus or Enterprise plan

**Pros**:
- ✅ Fastest deployment (< 30 minutes)
- ✅ Automatic monitoring and observability
- ✅ Zero infrastructure management
- ✅ Built-in version control

**Cons**:
- ❌ Requires paid LangSmith plan
- ❌ Less control over infrastructure
- ❌ Data stored on LangSmith servers

---

### Option 2: LangGraph Platform - Self-Hosted

**Best for**: Teams needing full control with sensitive data requirements

**Features**:
- Complete infrastructure control
- Data stays in your environment
- Deploy on AWS, GCP, Azure, or on-premises
- Helm charts for Kubernetes deployment
- Available via AWS Marketplace

**Setup Steps**:

1. **Prerequisites**
   - Kubernetes cluster (EKS, GKE, AKS, or self-managed)
   - Helm 3.x installed
   - kubectl configured

2. **Install via Helm (AWS Example)**
   ```bash
   # Add LangChain Helm repository
   helm repo add langchain https://langchain-ai.github.io/helm-charts
   helm repo update

   # Install LangGraph Platform
   helm install langgraph-platform langchain/langgraph-platform \
     --namespace langgraph \
     --create-namespace \
     --set api.anthropicApiKey="$ANTHROPIC_API_KEY"
   ```

3. **Configure ResumeCraft for deployment**
   ```bash
   # Create langgraph.json
   cat > backend/langgraph.json <<EOF
   {
     "dependencies": ["requirements_streamlit.txt"],
     "graphs": {
       "recruitment": "app.graphs.workflow:create_recruitment_workflow"
     },
     "env": ".env"
   }
   EOF
   ```

4. **Build and push Docker image**
   ```bash
   # Use existing Dockerfile or LangGraph CLI
   docker build -t resumecraft:latest .
   docker tag resumecraft:latest your-registry/resumecraft:latest
   docker push your-registry/resumecraft:latest
   ```

5. **Deploy to LangGraph Platform**
   ```bash
   # Using LangGraph CLI
   pip install langgraph-cli
   langgraph deploy --self-hosted
   ```

**Pricing**: Free (self-hosted), AWS Marketplace listing available

**Pros**:
- ✅ Full control over infrastructure
- ✅ Data privacy (stays in your VPC)
- ✅ No vendor lock-in
- ✅ Cost-effective for high volume

**Cons**:
- ❌ Requires DevOps expertise
- ❌ Infrastructure maintenance burden
- ❌ Complex initial setup

---

### Option 3: Hybrid (BYOC - Bring Your Own Cloud)

**Best for**: Teams wanting managed control plane but self-hosted data plane

**Features**:
- SaaS control plane (deployment UI)
- Self-hosted data plane (your infrastructure)
- No data leaves your VPC
- Managed provisioning and scaling

**Setup Steps**:

1. **Sign up for LangSmith Enterprise**
   - Contact LangChain for Enterprise plan
   - Get BYOC provisioning access

2. **Set up VPC infrastructure**
   ```bash
   # Deploy data plane in your AWS VPC
   # LangChain provides Terraform/CloudFormation templates
   ```

3. **Connect to LangSmith control plane**
   ```bash
   # Configure secure connection to LangSmith
   # LangChain provides VPC peering or PrivateLink setup
   ```

4. **Deploy via LangSmith UI**
   - Use LangSmith dashboard
   - Data processing happens in your VPC
   - Control and monitoring via LangSmith

**Pricing**: Enterprise plan only (contact sales)

**Pros**:
- ✅ Managed control plane
- ✅ Data privacy (processing in your VPC)
- ✅ Easy deployment experience
- ✅ Professional support

**Cons**:
- ❌ Most expensive option
- ❌ Requires Enterprise plan
- ❌ Complex networking setup

---

### Option 4: Current Docker Deployment (No LangSmith)

**Best for**: Development, testing, or teams not needing LangSmith features

**Features**:
- Simple Docker Compose setup
- No external dependencies
- Quick local deployment

**Setup Steps** (Already configured):

1. **Configure environment**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

2. **Run with Docker Compose**
   ```bash
   cd /Users/vamshi/MachineLearningProjects/ResumeCraft
   docker-compose up -d
   ```

3. **Access applications**
   - Main app: http://localhost:8501
   - Entity Resolution: http://localhost:8502

**Pros**:
- ✅ Already implemented
- ✅ No additional costs
- ✅ Simple setup
- ✅ Works anywhere Docker runs

**Cons**:
- ❌ No built-in monitoring
- ❌ Manual scaling
- ❌ No tracing/observability
- ❌ Manual deployment management

---

## Recommended Approach

### For Production: **Hybrid Approach**

1. **Phase 1: Add LangSmith Observability** (No deployment changes)
   - Add LangSmith tracing to existing Docker setup
   - Monitor workflow performance
   - Debug issues with trace data
   - **Cost**: Free tier available, then ~$49/month

2. **Phase 2: Deploy to LangGraph Platform** (When ready to scale)
   - Choose Cloud or Self-Hosted based on requirements
   - Migrate using learnings from Phase 1
   - Keep Docker as fallback

### Implementation Steps for Phase 1

```bash
# 1. Add to requirements
echo "langsmith" >> backend/requirements_streamlit.txt

# 2. Update .env
cat >> backend/.env <<EOF

# LangSmith Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key
LANGCHAIN_PROJECT=resumecraft-prod
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
EOF

# 3. Rebuild Docker
docker-compose down
docker-compose build
docker-compose up -d

# 4. Test - your workflow will now trace to LangSmith
```

No code changes needed! LangGraph automatically sends traces when environment variables are set.

---

## Cost Comparison

| Option | Initial Cost | Monthly Cost (est.) | Setup Time |
|--------|-------------|---------------------|------------|
| Docker (current) | $0 | $0 + hosting | 10 min |
| LangSmith observability | $0 | $49-99 | 30 min |
| LangSmith Cloud | $0 | $99-499 | 2-4 hours |
| Self-Hosted | Infrastructure | Infrastructure | 1-2 days |
| Hybrid BYOC | Infrastructure | $499+ | 3-5 days |

*Prices approximate, check https://www.langchain.com/pricing for current rates*

---

## Monitoring & Observability

### With LangSmith (All deployment options)

You get automatic visibility into:
- **Agent execution traces**: See each node in your workflow
- **LLM calls**: Token usage, latency, costs
- **Performance metrics**: Success rates, error rates
- **Debugging**: Inspect inputs/outputs at each step
- **Dataset management**: Test sets for evaluation

### View Your Workflow in LangSmith

Once deployed with LangSmith enabled, you can:
1. Visit https://smith.langchain.com
2. Select your project (resumecraft-prod)
3. View traces of your recruitment workflow:
   - Parser node execution
   - Job analyzer processing
   - Matcher scoring
   - Enhancer iterations
   - QA validation

---

## Next Steps

### Immediate (< 1 hour)
1. Add LangSmith API key to `.env`
2. Install langsmith package
3. Restart Docker containers
4. View traces in LangSmith dashboard

### Short-term (1-2 weeks)
1. Analyze workflow performance in LangSmith
2. Optimize slow nodes
3. Add custom metrics/tags
4. Create evaluation datasets

### Long-term (1-3 months)
1. Decide on production deployment option
2. Plan migration strategy
3. Set up CI/CD pipeline
4. Configure production monitoring

---

## Support Resources

- **LangSmith Docs**: https://docs.smith.langchain.com
- **LangGraph Platform**: https://langchain-ai.github.io/langgraph/cloud/
- **Deployment Guide**: https://docs.langchain.com/langsmith/deployments
- **Community**: https://github.com/langchain-ai/langgraph/discussions
- **Enterprise Support**: Contact sales@langchain.com

---

## Questions?

**Q: Can I use LangSmith without changing deployment?**
A: Yes! Just add environment variables. Your current Docker setup works with LangSmith tracing.

**Q: Do I need to migrate all at once?**
A: No. Start with observability (Phase 1), then deploy when ready.

**Q: What if I'm already using AWS?**
A: Perfect! Self-hosted option works great with EKS. Also available via AWS Marketplace.

**Q: Can I test locally first?**
A: Yes. LangSmith works with local development. Just set env vars and run normally.

**Q: What about costs?**
A: Start with free tier for development. Production needs Plus ($99/mo) or Enterprise (custom).

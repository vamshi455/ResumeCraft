# Deploy Streamlit Apps to Streamlit Cloud

Your Streamlit apps are now updated to connect to your deployed LangSmith workflow!

## What's Changed

✅ **Streamlit apps now use LangSmith API** when configured
✅ **Automatic fallback** to local workflow if LangSmith not available
✅ **Smart detection** - shows which mode is active

## Architecture

```
┌──────────────────────────────────┐
│   Streamlit Cloud (Frontend)     │
│   - app_entity_resolution.py     │
│   - User interface                │
└────────────┬─────────────────────┘
             │
             │ HTTP API calls
             ↓
┌──────────────────────────────────┐
│   LangSmith Cloud (Backend)      │
│   - LangGraph workflow            │
│   - AI processing                 │
│   - ID: 028c1a44-1085-4888...    │
└──────────────────────────────────┘
```

## Option 1: Deploy to Streamlit Cloud (Recommended)

### Step 1: Prepare Your Repository

Your code is already ready! Just make sure changes are pushed:

```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft
git status  # Check everything is committed
git push origin main  # Push if needed
```

### Step 2: Sign Up for Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "Sign up" or "Sign in"
3. Connect your GitHub account

### Step 3: Create New App

1. Click **"New app"**
2. Select your repository: `vamshi455/ResumeCraft`
3. Select branch: `main`
4. Set main file path: `backend/app_entity_resolution.py`
5. Click **"Advanced settings"**

### Step 4: Configure Secrets

In the **Secrets** section, add:

```toml
# Streamlit Cloud Secrets
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"
LANGSMITH_API_KEY = "lsv2_pt_your_langsmith_api_key_here"
LANGGRAPH_API_URL = "https://api.smith.langchain.com/deployments/028c1a44-1085-4888-b504-b5e0dbd1a949"
```

**Important**: Replace with your actual API keys!
- Get Anthropic key from: https://console.anthropic.com/
- Get LangSmith key from: https://smith.langchain.com/settings

### Step 5: Deploy!

1. Click **"Deploy!"**
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://your-app-name.streamlit.app`

---

## Option 2: Run Locally with LangSmith Backend

Test locally before deploying to cloud:

### Step 1: Update Your .env File

```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft/backend
cp .env.example .env
```

Edit `.env` and set:

```bash
# Your API keys
ANTHROPIC_API_KEY=your-anthropic-api-key-here
LANGSMITH_API_KEY=lsv2_pt_your_langsmith_api_key_here

# Your deployed workflow (already filled in!)
LANGGRAPH_API_URL=https://api.smith.langchain.com/deployments/028c1a44-1085-4888-b504-b5e0dbd1a949
```

### Step 2: Run Streamlit

```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft/backend
./venv/bin/streamlit run app_entity_resolution.py
```

### Step 3: Test

1. Browser opens at http://localhost:8501
2. You should see: "🚀 Using deployed LangSmith workflow for matching"
3. Upload resume bank and test matching!

---

## Option 3: Run Locally WITHOUT LangSmith (Local Mode)

If you want to test without the cloud deployment:

### Step 1: Edit .env

```bash
# Comment out or remove these lines:
# LANGSMITH_API_KEY=...
# LANGGRAPH_API_URL=...

# Keep only:
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### Step 2: Run Streamlit

```bash
./venv/bin/streamlit run app_entity_resolution.py
```

You'll see: "💻 Using local AI workflow for matching"

---

## How It Works

The Streamlit apps now **automatically detect** which mode to use:

### LangSmith Mode (Cloud Backend)
```python
# If LANGSMITH_API_KEY and LANGGRAPH_API_URL are set:
✅ Connects to deployed LangSmith workflow
✅ Uses scalable cloud infrastructure
✅ Auto-scaling, monitoring included
✅ Shows: "🚀 Using deployed LangSmith workflow"
```

### Local Mode (Fallback)
```python
# If LangSmith not configured:
✅ Runs workflow locally
✅ Uses your computer's resources
✅ Works without cloud dependency
✅ Shows: "💻 Using local AI workflow"
```

---

## Deployment Checklist

Before deploying to Streamlit Cloud:

- [ ] Code pushed to GitHub
- [ ] LangSmith workflow deployed (✅ Done: 028c1a44-1085-4888-b504-b5e0dbd1a949)
- [ ] Have Anthropic API key
- [ ] Have LangSmith API key
- [ ] Tested locally with LangSmith backend
- [ ] Streamlit Cloud account created
- [ ] Secrets configured in Streamlit Cloud

---

## Troubleshooting

### "LangSmith not configured" warning

**Problem**: App not connecting to LangSmith

**Solution**:
1. Check `.env` file has `LANGSMITH_API_KEY` and `LANGGRAPH_API_URL`
2. On Streamlit Cloud, check Secrets are configured
3. Restart the app

### "API Error" messages

**Problem**: LangSmith API calls failing

**Solution**:
1. Verify API key is correct: https://smith.langchain.com/settings
2. Check deployment is running: https://smith.langchain.com/deployments
3. View traces for error details

### App using local workflow instead of LangSmith

**Problem**: Shows "💻 Using local AI workflow" but you want cloud

**Solution**:
1. Set `LANGSMITH_API_KEY` in environment
2. Set `LANGGRAPH_API_URL` in environment
3. Restart Streamlit app

### Deployment fails on Streamlit Cloud

**Common issues**:
- Missing secrets → Add in Advanced Settings
- Wrong file path → Use `backend/app_entity_resolution.py`
- Python version → Streamlit Cloud uses Python 3.9+ (compatible)

---

## Multiple Streamlit Apps

You have three Streamlit apps in your repo:

### 1. app_entity_resolution.py ✅ UPDATED
- **Status**: Connected to LangSmith
- **Deploy to**: Main production URL
- **Features**: Resume matching with deployed workflow

### 2. app.py (Main navigation)
- **Status**: Navigation hub
- **Deploy to**: Alternative URL or keep local
- **Features**: Links to other apps

### 3. app_template_formatter.py
- **Status**: Standalone, doesn't use LangGraph
- **Deploy to**: Separate URL if needed
- **Features**: Resume template formatting

**Recommendation**: Deploy `app_entity_resolution.py` first since it's the one using LangSmith.

---

## Cost Summary

### Streamlit Cloud
- **Free tier**: 1 public app
- **Paid**: $20/month for private apps + more resources
- **Link**: https://streamlit.io/cloud

### LangSmith Cloud (You already have this)
- **Plus**: $99/month
- **Includes**: 100k traces, auto-scaling, monitoring

### Anthropic Claude API
- **Pay-per-use**: ~$0.42 per resume processed
- **No monthly minimum**

### Total for 100 resumes/month
```
Streamlit Cloud: $0 (free tier)
LangSmith: $99
Claude API: $42
Total: $141/month
```

---

## Next Steps

1. **Test locally first**:
   ```bash
   cd backend
   ./venv/bin/streamlit run app_entity_resolution.py
   ```

2. **If it works, deploy to Streamlit Cloud**:
   - Go to https://share.streamlit.io
   - Follow steps above
   - Add secrets
   - Deploy!

3. **Monitor your deployment**:
   - Streamlit app: Check user traffic
   - LangSmith: View traces at https://smith.langchain.com

---

## Support

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **LangSmith Docs**: https://docs.smith.langchain.com
- **Your Deployment**: https://smith.langchain.com/deployments

**You're all set!** Your Streamlit apps are ready to deploy and will automatically use your LangSmith backend. 🚀

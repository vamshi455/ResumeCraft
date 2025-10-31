# How to Run ResumeCraft - Simple Guide

## What You Have Now

Your ResumeCraft application has **two parts**:

### 1. Backend (LangGraph Workflow) - ✅ DEPLOYED!
- **Where**: Running on LangSmith Cloud
- **What**: Processes resumes, matches with jobs, analyzes candidates
- **URL**: `https://api.smith.langchain.com/deployments/028c1a44-1085-4888-b504-b5e0dbd1a949`
- **Status**: ✅ Live and ready to use

### 2. Frontend (Streamlit Apps) - ❌ NOT DEPLOYED YET
- **Where**: On your computer (not running)
- **What**: User interface for uploading resumes and viewing results
- **Files**:
  - `backend/app.py` - Main app
  - `backend/app_entity_resolution.py` - Entity resolution
  - `backend/app_template_formatter.py` - Template formatter

## Current Situation

```
┌─────────────────────────────────────┐
│   LangSmith Cloud (Backend)         │
│   ✅ DEPLOYED & RUNNING             │
│   - Processes resumes               │
│   - AI matching engine              │
└─────────────────────────────────────┘
          ↑
          │ (needs connection)
          ↓
┌─────────────────────────────────────┐
│   Your Computer (Frontend)          │
│   ❌ NOT RUNNING                    │
│   - Streamlit user interface        │
│   - Upload forms                    │
└─────────────────────────────────────┘
```

## Option A: Test the Backend Only (API)

This tests that your deployed workflow works:

### Step 1: Get Your LangSmith API Key

1. Go to https://smith.langchain.com/settings
2. Click "API Keys"
3. Copy your key (starts with `lsv2_pt_`)

### Step 2: Run the Test Script

```bash
# 1. Go to your project directory
cd /Users/vamshi/MachineLearningProjects/ResumeCraft

# 2. Set your API key (replace with your actual key)
export LANGSMITH_API_KEY="lsv2_pt_your_actual_key_here"

# 3. Run the test
python test_deployment.py
```

**What this does:**
- Sends a test resume to your deployed backend
- Gets back analysis results
- Shows match score, recommendations, etc.

**Expected output:**
```
🚀 Testing deployed ResumeCraft workflow...
⏳ Sending request...
📡 Response status: 200

✅ Success! Workflow executed successfully

🎯 Match Score: 85/100

📄 Parsed Resume:
  Name: John Doe
  Skills: Python, Django, PostgreSQL

📋 Final Recommendation:
  Strong match - Recommend for interview
```

---

## Option B: Run the Full Application (Frontend + Backend)

This gives you the web interface where you can upload resumes.

### Current Problem
Your Streamlit apps (`app.py`, etc.) are configured to run the workflow **locally**, but your workflow is now deployed on **LangSmith Cloud**. You need to connect them.

### Step 1: Update Environment Variables

Edit `backend/.env` and add:

```bash
# Add these lines to backend/.env
LANGGRAPH_API_URL=https://api.smith.langchain.com/deployments/028c1a44-1085-4888-b504-b5e0dbd1a949
LANGSMITH_API_KEY=lsv2_pt_your_actual_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### Step 2: Update Streamlit Apps

Your Streamlit apps need to be modified to call the deployed API instead of running locally.

**Would you like me to:**
1. **Update your Streamlit apps** to connect to the deployed backend?
2. **Or show you how to run everything locally** (not using LangSmith deployment)?

---

## Option C: Run Everything Locally (Easiest for Now)

If you just want to see the application working **without** the cloud deployment:

### Step 1: Configure Environment

```bash
# 1. Go to backend directory
cd /Users/vamshi/MachineLearningProjects/ResumeCraft/backend

# 2. Copy environment file
cp .env.example .env

# 3. Edit .env and add your Anthropic API key
# Open .env in any text editor and change:
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### Step 2: Run Streamlit App

```bash
# Still in backend directory
./venv/bin/streamlit run app.py
```

This will:
- Start the Streamlit web interface
- Run the workflow **locally** on your computer (not using cloud)
- Open browser at http://localhost:8501

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Step 3: Use the Application

1. Browser opens automatically
2. You'll see the ResumeCraft home page
3. Click "Template Formatter" or "Entity Resolution"
4. Upload resumes and test!

---

## Quick Comparison

| Option | What Runs | Pros | Cons |
|--------|-----------|------|------|
| **A: Test Backend API** | Just API | ✅ Tests cloud deployment<br>✅ Very fast | ❌ No user interface<br>❌ Command-line only |
| **B: Full Cloud App** | API (cloud) + UI (local) | ✅ Production setup<br>✅ Scalable | ❌ Needs code updates<br>❌ More complex |
| **C: Run Locally** | Everything on your computer | ✅ Easiest to start<br>✅ No cloud needed | ❌ Not scalable<br>❌ Runs on your machine |

---

## My Recommendation

**Start with Option C (Run Locally)** to see the app working, then we can connect it to the cloud deployment later.

### Quick Start Commands

```bash
# 1. Set up environment
cd /Users/vamshi/MachineLearningProjects/ResumeCraft/backend
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 2. Run the app
./venv/bin/streamlit run app.py

# 3. Open browser to http://localhost:8501
```

---

## Need Help?

Tell me which option you want:

1. **"Test the API only"** → I'll help you run `test_deployment.py`
2. **"Connect Streamlit to cloud"** → I'll update your apps to use the deployed backend
3. **"Run everything locally"** → I'll help you start the Streamlit apps on your computer

Which one would you like to do?

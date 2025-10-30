# 🚀 Running ResumeCraft Locally

Quick guide to run ResumeCraft applications on your local machine.

---

## ✅ Both Apps Are Currently Running!

**Main App:** http://localhost:8501
**Entity Resolution:** http://localhost:8502

---

## 📋 Quick Commands

### Method 1: Auto Start Script (Easiest)

```bash
# From ResumeCraft root directory
./run_apps.sh
```

This automatically starts both apps on ports 8501 and 8502.

### Method 2: Manual Start (Individual Apps)

#### Start Main Unified App (Port 8501)
```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft/backend
./venv/bin/streamlit run app.py --server.port 8501
```

#### Start Entity Resolution (Port 8502)
```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft/backend
./venv/bin/streamlit run app_entity_resolution.py --server.port 8502
```

### Method 3: Using System Streamlit

If you have Streamlit installed globally:

```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft/backend
streamlit run app.py --server.port 8501
```

**Note:** Make sure you're in the `backend/` directory first!

---

## 🛑 Stop Running Apps

### Stop All Apps
```bash
lsof -ti:8501,8502 | xargs kill -9
```

### Stop Individual App
```bash
# Stop Main App (8501)
lsof -ti:8501 | xargs kill -9

# Stop Entity Resolution (8502)
lsof -ti:8502 | xargs kill -9
```

---

## ❌ Common Errors & Fixes

### Error: "File does not exist: app_entity_resolution.py"

**Problem:** You're in the wrong directory

**Fix:**
```bash
# Check current directory
pwd

# Should show: /Users/vamshi/MachineLearningProjects/ResumeCraft/backend
# If not, cd to backend first:
cd /Users/vamshi/MachineLearningProjects/ResumeCraft/backend

# Then run:
streamlit run app_entity_resolution.py --server.port 8502
```

### Error: "Address already in use"

**Problem:** Port is already taken

**Fix:**
```bash
# Kill existing process
lsof -ti:8501 | xargs kill -9

# Then restart
streamlit run app.py --server.port 8501
```

### Error: "streamlit: command not found"

**Problem:** Streamlit not in PATH

**Fix - Use venv:**
```bash
cd backend
./venv/bin/streamlit run app.py --server.port 8501
```

**Fix - Install globally:**
```bash
pip install streamlit
```

---

## 📂 Directory Structure

```
ResumeCraft/
├── run_apps.sh              ← Auto start script (NEW!)
├── backend/
│   ├── app.py              ← Main unified app
│   ├── app_entity_resolution.py  ← Entity Resolution standalone
│   ├── app_template_formatter.py ← Template Formatter (embedded)
│   ├── venv/               ← Virtual environment
│   └── .env                ← API keys (create if missing)
```

---

## 🔑 API Key Setup

Before running, ensure you have your API key configured:

```bash
# Create .env file in backend/
cd backend
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > .env
```

Or copy from example:
```bash
cp .env.example .env
# Then edit .env and add your key
```

---

## 🎯 What Each App Does

### Main App (Port 8501)
**URL:** http://localhost:8501

**Features:**
- Landing page with both features
- Sidebar navigation
- Template Formatter (embedded)
- Entity Resolution launcher
- Unified experience

**Use when:** You want the full platform with navigation

### Entity Resolution Standalone (Port 8502)
**URL:** http://localhost:8502

**Features:**
- Two-panel interface (Jobs | Resume Bank)
- Pre-loaded test jobs
- Excel upload
- AI matching
- Export results

**Use when:** You only need Entity Resolution feature

---

## 🧪 Testing Checklist

After starting apps:

### Test Main App (8501):
- [ ] Visit http://localhost:8501
- [ ] See landing page with both feature cards
- [ ] Click "Launch Template Formatter" - works?
- [ ] Click "Launch Entity Resolution" - works?
- [ ] Sidebar navigation works?
- [ ] Back to Home works?

### Test Entity Resolution (8502):
- [ ] Visit http://localhost:8502
- [ ] See two-panel interface
- [ ] See 3 pre-loaded jobs on left
- [ ] Upload Excel on right - works?
- [ ] Click "Match Candidates" - works?
- [ ] See results and export?

---

## 💡 Pro Tips

### Use Different Browsers/Tabs
- Main App: Chrome
- Entity Resolution: Firefox
- Prevents session state conflicts

### Check Logs in Terminal
- Watch terminal output for errors
- Shows real-time processing logs
- Helpful for debugging

### Port Reference
- **8501** - Main unified app
- **8502** - Entity Resolution standalone
- Both can run simultaneously

### Virtual Environment
Always use the venv for consistent dependencies:
```bash
source backend/venv/bin/activate  # macOS/Linux
backend\venv\Scripts\activate     # Windows
```

---

## 🔄 Restart Apps

If apps behave strangely:

```bash
# Stop all
lsof -ti:8501,8502 | xargs kill -9

# Clear Streamlit cache
rm -rf ~/.streamlit/cache

# Restart
./run_apps.sh
```

---

## 📱 Access URLs

### Local Machine:
- Main: http://localhost:8501
- Entity: http://localhost:8502

### Same Network:
- Main: http://192.168.12.168:8501
- Entity: http://192.168.12.168:8502

### External (if port forwarded):
- Main: http://172.58.49.212:8501
- Entity: http://172.58.49.212:8502

---

## 🆘 Still Having Issues?

### Check Python Version:
```bash
python --version
# Should be 3.12+
```

### Check Dependencies:
```bash
cd backend
./venv/bin/pip list | grep streamlit
# Should show streamlit 1.31.0
```

### Reinstall Dependencies:
```bash
cd backend
./venv/bin/pip install -r requirements_streamlit.txt
```

### Check Ports:
```bash
lsof -ti:8501 -ti:8502
# Shows PIDs if ports are in use
```

---

## 📚 Additional Resources

- [README.md](README.md) - Project overview
- [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md) - Navigation help
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Cloud deployment

---

**Quick Start:**
```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft
./run_apps.sh
```

**Access:**
- Main: http://localhost:8501
- Entity: http://localhost:8502

**Stop:**
```bash
lsof -ti:8501,8502 | xargs kill -9
```

---

**Last Updated:** 2025-10-30
**Current Status:** ✅ Both apps running successfully

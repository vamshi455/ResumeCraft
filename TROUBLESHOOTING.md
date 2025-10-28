# 🔧 Troubleshooting Guide - ResumeCraft

Common issues and their solutions for the ResumeCraft platform.

---

## 🚨 Critical Issues

### Issue: 403 Error When Uploading Excel Files

**Symptoms:**
```
AxiosError: Request failed with status code 403
resume_bank_template.xlsx - 403 error
resume_bank_sample.xlsx - 403 error
```

**Root Cause:**
Conflicting Streamlit configuration between CORS and XSRF protection settings.

**Error Message in Console:**
```
Warning: the config option 'server.enableCORS=false' is not compatible with
'server.enableXsrfProtection=true'.
As a result, 'server.enableCORS' is being overridden to 'true'.
```

**Solution:**

The issue is in `backend/.streamlit/config.toml`. The configuration had:
```toml
[server]
enableCORS = false
enableXsrfProtection = true  # ❌ Conflict!
```

**Fix Applied:**
```toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = false  # ✅ Fixed
maxUploadSize = 200
```

**Steps to Fix:**
1. Edit `backend/.streamlit/config.toml`
2. Set `enableXsrfProtection = false`
3. Add `maxUploadSize = 200` (200 MB limit)
4. Restart Streamlit servers:
   ```bash
   lsof -ti:8501,8502 | xargs kill -9
   streamlit run app.py --server.port 8501 &
   streamlit run app_entity_resolution.py --server.port 8502 &
   ```

**Status:** ✅ **FIXED** (2025-10-28)

---

## 🌐 Network & Port Issues

### Issue: Port Already in Use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Kill all Streamlit processes
lsof -ti:8501,8502 | xargs kill -9

# Restart servers
cd backend
streamlit run app.py --server.port 8501 &
streamlit run app_entity_resolution.py --server.port 8502 &
```

### Issue: Server Not Accessible from Browser

**Symptoms:**
- Server running but localhost:8501 or localhost:8502 not loading
- Connection refused errors

**Solution:**
1. Check if server is actually running:
   ```bash
   lsof -ti:8501
   lsof -ti:8502
   ```

2. Check firewall settings (macOS):
   ```bash
   # Allow Python through firewall
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add $(which python)
   ```

3. Try different browser or clear cache

---

## 📁 File Upload Issues

### Issue: Excel File Upload Fails

**Symptoms:**
- File uploader shows error
- "Invalid file format" message
- File doesn't appear after selection

**Solutions:**

1. **Check File Format:**
   - Must be `.xlsx` or `.xls`
   - Use template: `backend/data/resume_bank_template.xlsx`

2. **Check File Size:**
   - Max size: 200 MB (configurable in config.toml)
   - Reduce rows if file is too large

3. **Check Required Columns:**
   ```
   Required: name, skill_set, exp_years, domain
   Optional: previous_roles, education, location
   ```

4. **Check for File Corruption:**
   ```bash
   # Test opening with pandas
   python -c "import pandas as pd; print(pd.read_excel('file.xlsx').head())"
   ```

### Issue: Temporary Lock Files (~$filename.xlsx)

**Symptoms:**
- Untracked files like `~$resume_bank_template.xlsx`
- Git status shows lock files

**Solution:**
These are Excel temporary lock files. Safe to ignore or delete:
```bash
find . -name "~$*.xlsx" -type f -delete
```

Add to `.gitignore`:
```
~$*.xlsx
~$*.xls
```

---

## 🔐 API & Authentication Issues

### Issue: API Key Missing

**Symptoms:**
```
❌ API Key Missing (in sidebar)
Error: ANTHROPIC_API_KEY not found
```

**Solution:**
1. Create/edit `.env` file in `backend/` directory:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-your-api-key-here
   ```

2. Restart the application

3. Verify in sidebar: Should show "✅ API Key Configured"

### Issue: API Rate Limiting

**Symptoms:**
- Matching process fails midway
- Error: "Rate limit exceeded"

**Solution:**
- Wait a few minutes before retrying
- Reduce batch size (Top N candidates)
- Consider upgrading API plan

---

## 🎨 UI & Display Issues

### Issue: Sidebar Not Showing

**Solution:**
1. Click `>` arrow in top-left corner
2. Check browser window width (responsive design)
3. Clear browser cache
4. Try different browser

### Issue: Colors Not Updating

**Symptoms:**
- Still seeing old purple/pink colors
- New navy/green theme not applied

**Solution:**
1. Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Clear Streamlit cache:
   ```bash
   rm -rf ~/.streamlit/cache
   ```
3. Restart servers

---

## 📊 Matching & AI Issues

### Issue: No Matches Showing

**Symptoms:**
- "Match Candidates" button clicked
- No results appear
- No error message

**Solution:**
1. Ensure resume bank is uploaded (check right panel)
2. Check API key is configured
3. Look for error messages in browser console (F12)
4. Check terminal for Python errors

### Issue: Slow Matching Process

**Symptoms:**
- Matching takes very long
- Progress bar stuck

**Solutions:**
1. **Normal for large datasets:**
   - 20 candidates: ~30 seconds
   - 50 candidates: ~2 minutes
   - 100+ candidates: ~5 minutes

2. **Reduce Top N:**
   - Default: 10
   - Try: 5 for faster results

3. **Check API connectivity:**
   ```bash
   curl -I https://api.anthropic.com
   ```

### Issue: Poor Match Scores

**Symptoms:**
- All candidates getting low scores
- Expected matches not appearing

**Solutions:**
1. **Improve job descriptions:**
   - Be specific with required skills
   - List all technologies
   - Include detailed requirements

2. **Check resume bank data:**
   - Ensure skill_set column is populated
   - Use consistent skill names
   - Include experience years

3. **Review domain alignment:**
   - Match domain field with job requirements

---

## 🧭 Navigation Issues

### Issue: Page Not Loading After Navigation

**Symptoms:**
- Clicked navigation button
- Page blank or shows old content

**Solution:**
1. Wait a moment for Streamlit to rerun
2. Check browser console for errors (F12)
3. Refresh the page manually
4. Clear session state:
   ```python
   # In Streamlit
   st.session_state.clear()
   ```

### Issue: Entity Resolution Button Opens Nothing

**Symptoms:**
- "Open Entity Resolution" button clicked
- No new window/tab opens
- Port 8502 not accessible

**Solution:**
1. Ensure Entity Resolution is running:
   ```bash
   lsof -ti:8502
   ```

2. Start it manually if not running:
   ```bash
   cd backend
   streamlit run app_entity_resolution.py --server.port 8502
   ```

3. Check browser popup blocker

4. Manually navigate to: http://localhost:8502

---

## 📦 Installation & Dependencies

### Issue: Import Error (Module Not Found)

**Symptoms:**
```python
ModuleNotFoundError: No module named 'langchain_anthropic'
ModuleNotFoundError: No module named 'openpyxl'
```

**Solution:**
```bash
cd backend
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Or install individually:
pip install langchain-anthropic openpyxl pandas streamlit
```

### Issue: Python Version Incompatibility

**Symptoms:**
```
SyntaxError: invalid syntax
Type hints not supported
```

**Solution:**
- Requires Python 3.12+
- Check version:
  ```bash
  python --version
  ```
- Upgrade if needed:
  ```bash
  brew install python@3.12  # macOS
  ```

---

## 🐛 General Debugging

### Enable Debug Mode

Add to `backend/.streamlit/config.toml`:
```toml
[runner]
fastReruns = false

[logger]
level = "debug"
```

### View Logs

**Terminal logs:**
```bash
# Check running processes
ps aux | grep streamlit

# View logs in real-time
tail -f ~/.streamlit/logs/streamlit.log
```

**Browser console:**
1. Open DevTools: `F12` or `Cmd+Option+I`
2. Go to Console tab
3. Look for errors (red text)

### Clear All Cache

```bash
# Streamlit cache
rm -rf ~/.streamlit/cache

# Browser cache
# Chrome: Cmd+Shift+Delete
# Firefox: Cmd+Shift+Delete

# Python cache
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -type f -delete
```

---

## 🆘 Still Having Issues?

### Collect Debug Information

Before reporting issues, gather:

1. **Environment:**
   ```bash
   python --version
   pip list | grep -E "streamlit|langchain|pandas"
   ```

2. **Errors:**
   - Terminal error messages
   - Browser console errors (F12)
   - Screenshots

3. **Configuration:**
   ```bash
   cat backend/.streamlit/config.toml
   ```

4. **Logs:**
   ```bash
   tail -50 ~/.streamlit/logs/streamlit.log
   ```

### Check Documentation

- [README.md](README.md) - Project overview
- [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md) - Navigation help
- [ENTITY_RESOLUTION_GUIDE.md](ENTITY_RESOLUTION_GUIDE.md) - Feature guide
- [QUICK_START_ENTITY_RESOLUTION.md](QUICK_START_ENTITY_RESOLUTION.md) - Quick start

### Report Issues

1. Check existing documentation first
2. Gather debug information (above)
3. Create detailed issue report
4. Include steps to reproduce

---

## 📚 Quick Command Reference

```bash
# Start unified app
streamlit run app.py

# Start Entity Resolution
streamlit run app_entity_resolution.py --server.port 8502

# Kill all Streamlit processes
lsof -ti:8501,8502 | xargs kill -9

# Check running processes
lsof -ti:8501 -ti:8502

# Clear cache
rm -rf ~/.streamlit/cache

# View logs
tail -f ~/.streamlit/logs/streamlit.log

# Test API key
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OK' if os.getenv('ANTHROPIC_API_KEY') else 'MISSING')"
```

---

**Last Updated:** 2025-10-28
**Version:** 1.0.0

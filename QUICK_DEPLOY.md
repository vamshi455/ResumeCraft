# 🚀 Quick Deploy - ResumeCraft

**Deploy ResumeCraft to Streamlit Cloud in 5 minutes!**

---

## ⚡ Fastest Way to Deploy

### Option 1: Streamlit Cloud (Recommended - FREE)

**Time:** 5 minutes | **Cost:** Free | **Difficulty:** ⭐ Easy

#### Step 1: Fork or Ensure Repository is Public

Your repository is already public at: `https://github.com/vamshi455/ResumeCraft`

#### Step 2: Deploy Main App

1. **Visit:** https://share.streamlit.io/

2. **Sign in** with GitHub

3. **Click:** "New app"

4. **Fill in:**
   ```
   Repository: vamshi455/ResumeCraft
   Branch: main
   Main file path: backend/app.py
   App URL: resumecraft (or your choice)
   ```

5. **Advanced Settings:**
   - Python version: `3.12`
   - Requirements file: `backend/requirements_streamlit.txt`

6. **Secrets** (Important!):
   Click "Advanced settings" → "Secrets" and paste:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-actual-api-key-here"
   ```

7. **Click:** "Deploy" 🚀

8. **Wait:** 2-3 minutes ⏳

9. **Done!** Your app is live at:
   ```
   https://resumecraft.streamlit.app
   ```
   (or whatever URL you chose)

#### Step 3: Deploy Entity Resolution App

Repeat the same process:

1. **Click:** "New app" again

2. **Fill in:**
   ```
   Repository: vamshi455/ResumeCraft
   Branch: main
   Main file path: backend/app_entity_resolution.py
   App URL: resumecraft-entity (or your choice)
   ```

3. **Same Advanced Settings:**
   - Python version: `3.12`
   - Requirements file: `backend/requirements_streamlit.txt`
   - Secrets: Same `ANTHROPIC_API_KEY`

4. **Click:** "Deploy" 🚀

5. **Done!** Entity Resolution live at:
   ```
   https://resumecraft-entity.streamlit.app
   ```

### ✅ You Now Have:

- **Main App:** https://resumecraft.streamlit.app
- **Entity Resolution:** https://resumecraft-entity.streamlit.app

---

## 🐳 Option 2: Docker (Local or VPS)

**Time:** 10 minutes | **Cost:** Depends on hosting | **Difficulty:** ⭐⭐ Medium

### Prerequisites
- Docker installed
- API key ready

### Deploy

```bash
# Clone repository
git clone https://github.com/vamshi455/ResumeCraft.git
cd ResumeCraft

# Create .env file
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > backend/.env

# Build and run
docker-compose up -d

# Access apps
# Main: http://localhost:8501
# Entity Resolution: http://localhost:8502
```

### Stop

```bash
docker-compose down
```

---

## 🤗 Option 3: Hugging Face Spaces (FREE)

**Time:** 10 minutes | **Cost:** Free | **Difficulty:** ⭐ Easy

### Deploy Main App

1. **Visit:** https://huggingface.co/spaces

2. **Click:** "Create new Space"

3. **Configure:**
   ```
   Name: ResumeCraft
   License: MIT
   SDK: Streamlit
   Hardware: CPU basic (free)
   ```

4. **Click:** "Create Space"

5. **Clone your space:**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/ResumeCraft
   ```

6. **Copy files:**
   ```bash
   cd ResumeCraft
   cp ../ResumeCraft/backend/app.py .
   cp ../ResumeCraft/backend/requirements_streamlit.txt requirements.txt
   cp -r ../ResumeCraft/backend/app ./
   ```

7. **Create README.md:**
   ```bash
   cat > README.md << 'EOF'
   ---
   title: ResumeCraft
   emoji: 📄
   colorFrom: blue
   colorTo: green
   sdk: streamlit
   sdk_version: 1.31.0
   app_file: app.py
   pinned: false
   ---

   # ResumeCraft
   AI-powered resume formatting using Claude AI
   EOF
   ```

8. **Push:**
   ```bash
   git add .
   git commit -m "Deploy to Hugging Face"
   git push
   ```

9. **Add API Key:**
   - Go to Space settings
   - Click "Repository secrets"
   - Add: `ANTHROPIC_API_KEY` = `your-key`

10. **Done!** App is live at:
    ```
    https://huggingface.co/spaces/YOUR_USERNAME/ResumeCraft
    ```

---

## 🎯 Which Option Should You Choose?

| Use Case | Recommended Option | Why? |
|----------|-------------------|------|
| **Demo/Portfolio** | Streamlit Cloud | Free, easy, professional URL |
| **AI/ML Showcase** | Hugging Face Spaces | ML community visibility |
| **Production/Team** | Docker on VPS | Full control, custom domain |
| **Testing Locally** | Docker | Quick setup, no internet needed |

---

## 🔐 Getting Your API Key

If you don't have an Anthropic API key yet:

1. **Visit:** https://console.anthropic.com/
2. **Sign up** or sign in
3. **Go to:** API Keys section
4. **Create** new API key
5. **Copy** the key (starts with `sk-ant-`)
6. **Keep it safe!** Don't share or commit to GitHub

---

## ✅ Post-Deployment Checklist

After deployment, verify:

- [ ] App loads without errors
- [ ] Can upload files (resume, template, Excel)
- [ ] API key is working (check sidebar)
- [ ] All features work (formatting, matching, etc.)
- [ ] No error messages in logs
- [ ] Custom URL is accessible

---

## 🆘 Common Issues

### "Module not found" Error
**Fix:** Ensure `requirements_streamlit.txt` is specified in deployment settings

### "API Key Missing" Error
**Fix:** Add `ANTHROPIC_API_KEY` to secrets/environment variables

### App Won't Start
**Fix:** Check logs, verify Python 3.12 is selected

### Slow Performance
**Fix:** Normal on free tier - upgrade instance or use paid tier

---

## 📚 Need More Options?

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for:
- Railway deployment
- Render deployment
- AWS EC2 setup
- Google Cloud Run
- Heroku deployment
- And more!

---

## 🎉 Success!

Your ResumeCraft is now deployed and accessible to anyone with the URL!

**Share your deployment:**
- Add URL to your GitHub README
- Share on LinkedIn
- Add to your portfolio
- Demo to your team

**Next steps:**
- Monitor usage in Streamlit Cloud dashboard
- Set up custom domain (paid tiers)
- Add analytics
- Collect user feedback

---

**Questions?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Last Updated:** 2025-10-30

# 🚀 ResumeCraft Deployment Guide

## Quick Share Options for Your Team

### ✅ **Option 1: Local Network Sharing (Instant)**

**If your team is on the same WiFi/network:**

1. Keep the app running on your machine
2. Share this URL with your team:
   ```
   http://192.168.87.22:8502
   ```
3. They can access it immediately in their browser!

**Pros:**
- ✅ No setup needed
- ✅ Works immediately
- ✅ Free

**Cons:**
- ⚠️ Requires same network
- ⚠️ Your computer must stay on
- ⚠️ Only works locally

---

### ☁️ **Option 2: Streamlit Cloud (FREE - Recommended)**

**Deploy to the cloud for public access:**

#### Step 1: Push to GitHub
```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft

# Initialize git if not already done
git init
git add .
git commit -m "Add ResumeCraft template formatter"

# Create a GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/ResumeCraft.git
git push -u origin main
```

#### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select:
   - **Repository:** YOUR_USERNAME/ResumeCraft
   - **Branch:** main
   - **Main file path:** backend/app_template_formatter.py
5. Click "Advanced settings" and add:
   - **Secrets:** Add your OpenAI API key
   ```toml
   OPENAI_API_KEY = "sk-your-key-here"
   ```
6. Click "Deploy"
7. Get your public URL: `https://yourapp.streamlit.app`

**Pros:**
- ✅ Free hosting
- ✅ Public URL accessible anywhere
- ✅ Automatic updates when you push to GitHub
- ✅ SSL certificate included

**Cons:**
- ⚠️ Free tier has resource limits
- ⚠️ May sleep after inactivity

---

### 🐳 **Option 3: Docker Deployment (Advanced)**

**For production deployments:**

#### Create Dockerfile:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

WORKDIR /app/backend

EXPOSE 8502

CMD ["streamlit", "run", "app_template_formatter.py", "--server.port=8502", "--server.address=0.0.0.0"]
```

#### Run with Docker:
```bash
# Build
docker build -t resumecraft .

# Run
docker run -p 8502:8502 -e OPENAI_API_KEY=your-key resumecraft
```

**Deploy to:**
- AWS ECS / Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform

---

### 🌍 **Option 4: Ngrok (Quick Demo)**

**For temporary public access:**

```bash
# Install ngrok
brew install ngrok

# Create tunnel
ngrok http 8502
```

You'll get a public URL like: `https://abc123.ngrok.io`

**Pros:**
- ✅ Instant public URL
- ✅ Good for quick demos

**Cons:**
- ⚠️ Temporary (closes when you stop ngrok)
- ⚠️ Free tier has time limits

---

### 📱 **Option 5: Heroku Deployment**

```bash
# Install Heroku CLI
brew install heroku

# Login
heroku login

# Create app
heroku create resumecraft

# Add buildpack
heroku buildpacks:set heroku/python

# Create Procfile
echo "web: streamlit run backend/app_template_formatter.py --server.port=$PORT" > Procfile

# Deploy
git push heroku main
```

---

## 🔐 Security Considerations

### For Public Deployments:

1. **API Key Security:**
   - Never commit `.env` file
   - Use environment variables
   - Use secrets management (Streamlit Cloud secrets, AWS Secrets Manager, etc.)

2. **Add Authentication:**
   ```python
   import streamlit as st

   def check_password():
       if "authenticated" not in st.session_state:
           st.session_state.authenticated = False

       if not st.session_state.authenticated:
           password = st.text_input("Password", type="password")
           if st.button("Login"):
               if password == "your-password":
                   st.session_state.authenticated = True
                   st.rerun()
               else:
                   st.error("Incorrect password")
           st.stop()

   check_password()
   ```

3. **Rate Limiting:**
   - Implement OpenAI API rate limits
   - Add user session limits

---

## 📊 Recommended Setup by Use Case

| Use Case | Best Option | Why |
|----------|-------------|-----|
| Quick demo to team (same office) | Local Network | Instant, no setup |
| Remote team demo | Ngrok | Fast public URL |
| Client presentation | Streamlit Cloud | Professional, stable |
| Production use | Docker + Cloud | Scalable, secure |
| Internal company tool | Docker + VPN | Secure, controlled |

---

## 🆘 Troubleshooting

### App won't start:
```bash
# Check if port is in use
lsof -i :8502

# Kill existing process
pkill -f streamlit

# Restart
streamlit run backend/app_template_formatter.py
```

### Network URL not accessible:
- Check firewall settings
- Ensure both devices on same network
- Try disabling VPN

### Streamlit Cloud deployment fails:
- Check requirements.txt has all dependencies
- Verify secrets are set correctly
- Check logs in Streamlit Cloud dashboard

---

## 📞 Support

For issues or questions:
- Check logs: `streamlit run backend/app_template_formatter.py`
- Streamlit docs: [docs.streamlit.io](https://docs.streamlit.io)
- GitHub issues: Create an issue in your repo

---

## 🎯 Quick Start Command

**To run locally:**
```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft/backend
source venv/bin/activate
streamlit run app_template_formatter.py
```

**Access at:**
- Local: http://localhost:8502
- Network: http://192.168.87.22:8502

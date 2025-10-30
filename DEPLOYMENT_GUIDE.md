# 🚀 ResumeCraft Deployment Guide

Complete guide to publish and deploy ResumeCraft to various cloud platforms.

---

## 📋 Table of Contents

1. [Deployment Options Overview](#deployment-options-overview)
2. [Streamlit Cloud (Recommended)](#1-streamlit-cloud-recommended--free)
3. [Hugging Face Spaces](#2-hugging-face-spaces-free)
4. [Heroku](#3-heroku)
5. [AWS EC2](#4-aws-ec2)
6. [Google Cloud Run](#5-google-cloud-run)
7. [Docker Deployment](#6-docker-deployment)
8. [Railway](#7-railway)
9. [Render](#8-render)

---

## 🎯 Deployment Options Overview

| Platform | Difficulty | Cost | Best For | Setup Time |
|----------|-----------|------|----------|------------|
| **Streamlit Cloud** | ⭐ Easy | Free | Quick demos, testing | 5 min |
| **Hugging Face Spaces** | ⭐ Easy | Free | AI/ML showcases | 10 min |
| **Railway** | ⭐⭐ Medium | Free tier | Small teams | 15 min |
| **Render** | ⭐⭐ Medium | Free tier | Production apps | 15 min |
| **Heroku** | ⭐⭐ Medium | Paid | Established apps | 20 min |
| **Google Cloud Run** | ⭐⭐⭐ Hard | Pay-as-go | Scalable apps | 30 min |
| **AWS EC2** | ⭐⭐⭐⭐ Hard | Variable | Full control | 45 min |
| **Docker** | ⭐⭐⭐ Medium | Depends | Any platform | 30 min |

---

## 1. Streamlit Cloud (Recommended) 🌟 FREE

**Best for:** Quick deployment, demos, personal projects

### Prerequisites
- GitHub account (already have ✓)
- Streamlit Cloud account (free)

### Step-by-Step

#### 1.1 Prepare Repository

Your repository is already set up! Just ensure these files exist:

```bash
# Already have:
✓ backend/app.py
✓ backend/app_entity_resolution.py
✓ backend/requirements.txt (needs updating for Streamlit)
✓ backend/.env.example
```

#### 1.2 Create Streamlit Requirements File

Create `backend/requirements_streamlit.txt`:
```txt
streamlit==1.31.0
langchain-anthropic==0.1.9
langchain==0.1.9
langchain-core==0.1.26
langgraph==0.0.28
pandas==2.2.0
openpyxl==3.1.2
python-docx==1.1.0
PyPDF2==3.0.1
pdfplumber==0.10.3
python-dotenv==1.0.1
loguru==0.7.2
```

#### 1.3 Deploy to Streamlit Cloud

1. **Go to:** https://share.streamlit.io/

2. **Sign in** with GitHub

3. **Click "New app"**

4. **Configure:**
   - Repository: `vamshi455/ResumeCraft`
   - Branch: `main`
   - Main file path: `backend/app.py`
   - App URL: `resumecraft` (or your choice)

5. **Advanced settings:**
   - Python version: `3.12`
   - Requirements file: `backend/requirements_streamlit.txt`

6. **Add secrets** (click "Advanced settings" → "Secrets"):
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-api-key-here"
   ```

7. **Click "Deploy"**

8. **Wait 2-3 minutes** for deployment

9. **Your app is live!** 🎉
   - URL: `https://resumecraft.streamlit.app`

#### 1.4 Deploy Entity Resolution (Second App)

Repeat for Entity Resolution:
- Main file path: `backend/app_entity_resolution.py`
- App URL: `resumecraft-entity-resolution`
- Same secrets

**Result:**
- Main App: `https://resumecraft.streamlit.app`
- Entity Resolution: `https://resumecraft-entity-resolution.streamlit.app`

### Limitations
- Free tier: 1 GB RAM, 800 hours/month
- Apps sleep after inactivity (cold start ~10s)
- No custom domain on free tier

---

## 2. Hugging Face Spaces 🤗 FREE

**Best for:** ML/AI demos, showcase projects

### Step-by-Step

#### 2.1 Create Space

1. Go to: https://huggingface.co/spaces
2. Click "Create new Space"
3. Configure:
   - Name: `ResumeCraft`
   - License: `MIT`
   - SDK: `Streamlit`
   - Hardware: `CPU basic` (free)

#### 2.2 Clone and Push

```bash
# Clone your new space
git clone https://huggingface.co/spaces/YOUR_USERNAME/ResumeCraft

# Copy files
cp -r backend/* ResumeCraft/

# Create app.py in root
cd ResumeCraft
ln -s app.py app.py

# Create README.md
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

# ResumeCraft - AI Resume Formatter
AI-powered resume formatting using Claude AI
EOF

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

#### 2.3 Add Secrets

1. Go to Space settings
2. Click "Repository secrets"
3. Add: `ANTHROPIC_API_KEY` = `your-key`

**Your app is live!** 🎉
- URL: `https://huggingface.co/spaces/YOUR_USERNAME/ResumeCraft`

---

## 3. Heroku

**Best for:** Production apps with custom domains

### Step-by-Step

#### 3.1 Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Login
heroku login
```

#### 3.2 Create Heroku App

```bash
cd /Users/vamshi/MachineLearningProjects/ResumeCraft

# Create app
heroku create resumecraft-app

# Add buildpack
heroku buildpacks:set heroku/python
```

#### 3.3 Create Heroku Files

**Procfile:**
```
web: streamlit run backend/app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt:**
```
python-3.12.0
```

#### 3.4 Deploy

```bash
# Set environment variables
heroku config:set ANTHROPIC_API_KEY="your-key"

# Deploy
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main

# Open app
heroku open
```

**Cost:** ~$7/month for basic dyno

---

## 4. AWS EC2

**Best for:** Full control, scalable production apps

### Step-by-Step

#### 4.1 Launch EC2 Instance

1. Go to AWS Console → EC2
2. Click "Launch Instance"
3. Choose: Ubuntu 22.04 LTS
4. Instance type: t2.medium (2 vCPU, 4 GB RAM)
5. Create key pair (download .pem file)
6. Security Group: Allow ports 22, 8501, 8502

#### 4.2 Connect and Setup

```bash
# SSH to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.12 python3-pip -y

# Clone repository
git clone https://github.com/vamshi455/ResumeCraft.git
cd ResumeCraft/backend

# Install dependencies
pip3 install -r requirements_streamlit.txt

# Setup environment
cp .env.example .env
nano .env  # Add your ANTHROPIC_API_KEY
```

#### 4.3 Setup Systemd Services

**Create service file:**
```bash
sudo nano /etc/systemd/system/resumecraft.service
```

**Content:**
```ini
[Unit]
Description=ResumeCraft Streamlit App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/ResumeCraft/backend
Environment="PATH=/home/ubuntu/.local/bin:/usr/bin"
ExecStart=/home/ubuntu/.local/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0

[Install]
WantedBy=multi-user.target
```

**Start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable resumecraft
sudo systemctl start resumecraft
```

#### 4.4 Setup Nginx (Optional)

```bash
sudo apt install nginx -y

sudo nano /etc/nginx/sites-available/resumecraft
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/resumecraft /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

**Your app is live!** 🎉
- URL: `http://your-ec2-ip:8501`
- Or: `http://your-domain.com` (with Nginx)

**Cost:** ~$15-30/month for t2.medium

---

## 5. Google Cloud Run

**Best for:** Serverless, auto-scaling apps

### Step-by-Step

#### 5.1 Create Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements_streamlit.txt .
RUN pip install --no-cache-dir -r requirements_streamlit.txt

COPY backend/ .

ENV PORT=8080
EXPOSE 8080

CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

#### 5.2 Build and Deploy

```bash
# Install gcloud CLI
# Follow: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/resumecraft

# Deploy to Cloud Run
gcloud run deploy resumecraft \
  --image gcr.io/YOUR_PROJECT_ID/resumecraft \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY="your-key"
```

**Your app is live!** 🎉
- URL provided by Cloud Run

**Cost:** Pay-per-use (~$5-20/month typical)

---

## 6. Docker Deployment

**Best for:** Any platform, local hosting

### Step-by-Step

#### 6.1 Create Docker Files

**Dockerfile:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements_streamlit.txt .
RUN pip install --no-cache-dir -r requirements_streamlit.txt

# Copy application
COPY backend/ .

# Expose ports
EXPOSE 8501 8502

# Create startup script
RUN echo '#!/bin/bash\n\
streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &\n\
streamlit run app_entity_resolution.py --server.port=8502 --server.address=0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  resumecraft:
    build: .
    ports:
      - "8501:8501"
      - "8502:8502"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./backend:/app
    restart: unless-stopped
```

#### 6.2 Build and Run

```bash
# Build image
docker build -t resumecraft .

# Run container
docker run -d \
  -p 8501:8501 \
  -p 8502:8502 \
  -e ANTHROPIC_API_KEY="your-key" \
  --name resumecraft \
  resumecraft

# Or use docker-compose
docker-compose up -d
```

**Access:**
- Main App: http://localhost:8501
- Entity Resolution: http://localhost:8502

---

## 7. Railway 🚂

**Best for:** Simple deployment with free tier

### Step-by-Step

1. **Go to:** https://railway.app/
2. **Sign in** with GitHub
3. **Click "New Project" → "Deploy from GitHub repo"**
4. **Select:** `vamshi455/ResumeCraft`
5. **Configure:**
   - Root directory: `backend`
   - Start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. **Add variables:**
   - `ANTHROPIC_API_KEY` = your key
7. **Deploy**

**Your app is live!** 🎉

**Free tier:** $5 credit/month

---

## 8. Render 🎨

**Best for:** Free tier with custom domains

### Step-by-Step

1. **Go to:** https://render.com/
2. **Sign in** with GitHub
3. **Click "New" → "Web Service"**
4. **Select:** `vamshi455/ResumeCraft`
5. **Configure:**
   - Name: `resumecraft`
   - Environment: `Python 3`
   - Build command: `pip install -r backend/requirements_streamlit.txt`
   - Start command: `streamlit run backend/app.py --server.port=$PORT --server.address=0.0.0.0`
6. **Add environment variables:**
   - `ANTHROPIC_API_KEY` = your key
7. **Create Web Service**

**Your app is live!** 🎉
- URL: `https://resumecraft.onrender.com`

**Free tier:** Available with limitations

---

## 📦 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] `.env` file is in `.gitignore` (already done ✓)
- [ ] API keys are NOT in code (use environment variables)
- [ ] `requirements.txt` or `requirements_streamlit.txt` is up to date
- [ ] Test app locally: `streamlit run app.py`
- [ ] Check all features work
- [ ] README.md has deployment instructions
- [ ] `.env.example` exists for reference
- [ ] Data files are in `.gitignore` if sensitive

---

## 🔐 Security Best Practices

1. **Never commit API keys** to GitHub
2. **Use environment variables** for secrets
3. **Enable HTTPS** on production
4. **Set proper CORS** headers
5. **Rate limit** API calls if needed
6. **Monitor usage** to avoid unexpected costs
7. **Use secrets management** (AWS Secrets Manager, etc.)

---

## 🎯 Recommended Approach

**For Demo/Testing:**
→ Use **Streamlit Cloud** (5 minutes, free, easy)

**For Portfolio/Showcase:**
→ Use **Hugging Face Spaces** (10 minutes, free, ML-focused)

**For Small Team:**
→ Use **Railway** or **Render** (15 minutes, free tier, good UX)

**For Production:**
→ Use **Google Cloud Run** or **AWS EC2** (scalable, reliable)

---

## 📚 Additional Resources

- [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-community-cloud/get-started)
- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
- [Docker Docs](https://docs.docker.com/)

---

## 🆘 Troubleshooting

### App Won't Start
- Check logs: `heroku logs --tail` or platform-specific
- Verify `requirements.txt` has all dependencies
- Check Python version compatibility

### API Key Issues
- Ensure environment variable is set correctly
- Check variable name matches code: `ANTHROPIC_API_KEY`
- Test locally first

### Port Issues
- Use `$PORT` environment variable on cloud platforms
- Don't hardcode port numbers
- Check firewall/security group settings

### Memory Issues
- Upgrade instance type
- Optimize data processing
- Use caching (`@st.cache_resource`)

---

**Need Help?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more issues.

**Last Updated:** 2025-10-30
**Version:** 1.0.0

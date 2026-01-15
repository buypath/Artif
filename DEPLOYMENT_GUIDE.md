# 🚀 Deployment Guide

This guide covers multiple deployment options for the Document Processing System, from easiest to most advanced.

---

## ⭐ Option 1: Streamlit Cloud (Recommended - FREE)

**Best for:** Quick deployment, free hosting, no server management
**Cost:** Free
**Time:** 5-10 minutes

### Step-by-Step Instructions

#### 1. Prepare Your GitHub Repository

Your code is already pushed to GitHub. Make sure it's on a public repository or you have Streamlit Cloud access to private repos.

```bash
# Verify your code is pushed
git status
git push
```

#### 2. Sign Up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign up with GitHub"
3. Authorize Streamlit to access your GitHub account

#### 3. Deploy Your App

1. Click **"New app"** button
2. Fill in the deployment form:
   - **Repository:** `buypath/Artif` (your repo)
   - **Branch:** `claude/document-processing-system-7mrTo`
   - **Main file path:** `app.py`

3. Click **"Advanced settings"**
   - **Python version:** 3.11

4. Click **"Deploy!"**

#### 4. Add Your API Key (Secrets)

1. Once deployed, go to your app settings (⚙️ icon)
2. Click on **"Secrets"**
3. Add your secrets in TOML format:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
```

4. Click **"Save"**
5. Your app will automatically restart

#### 5. Access Your Live App

Your app will be available at:
```
https://[your-app-name].streamlit.app
```

### Streamlit Cloud Features

✅ **Free hosting** for public repos
✅ **Automatic HTTPS**
✅ **Auto-deployment** on git push
✅ **Built-in secrets management**
✅ **Resource management** (1 GB RAM, 1 CPU)
✅ **Custom domains** (paid plans)

### Troubleshooting Streamlit Cloud

**Error: "ModuleNotFoundError"**
- Ensure `requirements.txt` is in the root directory
- Check all dependencies are listed

**Error: "API Key not found"**
- Verify secrets are correctly formatted in TOML
- No quotes around the key name
- Check for typos

**App is slow or timing out**
- Streamlit Cloud free tier has resource limits
- Consider upgrading or optimizing your code

---

## 🐳 Option 2: Docker Deployment

**Best for:** Containerized deployment, reproducible environments
**Cost:** Depends on hosting provider
**Time:** 15-30 minutes

### Create Dockerfile

Create `Dockerfile` in your project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads output

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build the image
docker build -t document-processor .

# Run the container
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY="your-key-here" \
  document-processor
```

### Deploy to Cloud Platforms

**Docker Hub + Any Cloud:**
```bash
# Tag and push to Docker Hub
docker tag document-processor yourusername/document-processor
docker push yourusername/document-processor

# Deploy on any platform that supports Docker
# - AWS ECS
# - Google Cloud Run
# - Azure Container Instances
# - DigitalOcean App Platform
```

---

## 🌐 Option 3: Heroku Deployment

**Best for:** Traditional PaaS deployment
**Cost:** Free tier available (with limitations)
**Time:** 10-20 minutes

### Prerequisites

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login
```

### Create Heroku App

```bash
# Create app
heroku create your-app-name

# Add buildpack
heroku buildpacks:set heroku/python

# Set config vars
heroku config:set ANTHROPIC_API_KEY="your-key-here"
```

### Create Required Files

**`Procfile`:**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**`runtime.txt`:**
```
python-3.11.0
```

### Deploy

```bash
# Commit changes
git add Procfile runtime.txt
git commit -m "Add Heroku deployment files"

# Deploy
git push heroku claude/document-processing-system-7mrTo:main

# Open your app
heroku open
```

---

## ☁️ Option 4: Railway Deployment

**Best for:** Modern, simple deployment
**Cost:** Free tier with $5/month credit
**Time:** 5-10 minutes

### Deploy with Railway

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Railway auto-detects Streamlit and configures

### Add Environment Variables

1. Go to your project settings
2. Click **"Variables"**
3. Add:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```

### Custom Start Command

In Railway settings, set start command:
```
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

---

## 🌩️ Option 5: AWS Deployment

**Best for:** Enterprise-grade hosting, full control
**Cost:** Pay-as-you-go (can be expensive)
**Time:** 30-60 minutes

### Using AWS Elastic Beanstalk

1. **Install EB CLI:**
```bash
pip install awsebcli
```

2. **Initialize EB:**
```bash
eb init -p python-3.11 document-processor
```

3. **Create Environment:**
```bash
eb create document-processor-env
```

4. **Set Environment Variables:**
```bash
eb setenv ANTHROPIC_API_KEY="your-key-here"
```

5. **Deploy:**
```bash
eb deploy
```

6. **Open App:**
```bash
eb open
```

### Using AWS ECS (Docker)

1. Build and push Docker image to ECR
2. Create ECS cluster
3. Define task definition
4. Create service
5. Configure load balancer

*See AWS documentation for detailed steps*

---

## 🔧 Option 6: VPS Deployment (DigitalOcean, Linode, etc.)

**Best for:** Full server control, cost-effective
**Cost:** $5-10/month
**Time:** 30-45 minutes

### Setup on Ubuntu VPS

```bash
# SSH into your server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Python and dependencies
apt install python3.11 python3-pip nginx -y

# Clone your repository
git clone https://github.com/buypath/Artif.git
cd Artif
git checkout claude/document-processing-system-7mrTo

# Install dependencies
pip3 install -r requirements.txt

# Set environment variable
export ANTHROPIC_API_KEY="your-key-here"

# Run with nohup (background)
nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
```

### Configure Nginx Reverse Proxy

Create `/etc/nginx/sites-available/streamlit`:

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
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Setup Systemd Service

Create `/etc/systemd/system/streamlit.service`:

```ini
[Unit]
Description=Streamlit Document Processor
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/root/Artif
Environment="ANTHROPIC_API_KEY=your-key-here"
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
systemctl enable streamlit
systemctl start streamlit
systemctl status streamlit
```

---

## 📊 Comparison Table

| Platform | Cost | Ease | Speed | Control | SSL | Custom Domain |
|----------|------|------|-------|---------|-----|---------------|
| **Streamlit Cloud** | Free | ⭐⭐⭐⭐⭐ | Fast | Low | ✅ | Premium |
| **Railway** | $5/mo | ⭐⭐⭐⭐ | Fast | Medium | ✅ | ✅ |
| **Heroku** | Free tier | ⭐⭐⭐⭐ | Medium | Medium | ✅ | ✅ |
| **Docker** | Varies | ⭐⭐⭐ | Fast | High | Manual | ✅ |
| **AWS** | Pay-as-go | ⭐⭐ | Fast | High | Manual | ✅ |
| **VPS** | $5-10/mo | ⭐⭐ | Medium | Full | Manual | ✅ |

---

## 🔒 Security Best Practices

### 1. Protect Your API Key

**Never commit API keys to Git:**
```bash
# Already in .gitignore
.env
.streamlit/secrets.toml
```

**Use environment variables or secrets management:**
- Streamlit Cloud: Use secrets feature
- Docker: Pass as environment variables
- VPS: Use systemd environment or .env files

### 2. Enable HTTPS

- **Streamlit Cloud:** Automatic HTTPS
- **Other platforms:** Use Let's Encrypt (free SSL)

```bash
# Install certbot
apt install certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

### 3. Restrict Access (Optional)

Add authentication to your Streamlit app:

```python
# In app.py
import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["app_password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    # Your app code here
    pass
```

---

## 🎯 Recommended Deployment Path

### For Most Users (Non-Technical)
**→ Use Streamlit Cloud**
- Easiest setup
- Free hosting
- No server management
- Perfect for demos and personal use

### For Small Teams
**→ Use Railway or Heroku**
- Easy deployment
- Affordable
- Good performance
- Custom domains

### For Production/Enterprise
**→ Use AWS or VPS**
- Full control
- Scalable
- Professional infrastructure
- Custom requirements

---

## 📞 Deployment Support

### Streamlit Cloud Issues
- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)

### General Questions
- Check DEPLOYMENT_SUMMARY.md
- Review WEB_UI_GUIDE.md
- See examples in repository

---

## 🎉 Next Steps After Deployment

1. ✅ Test your deployed app
2. ✅ Share the URL with your team
3. ✅ Monitor usage and performance
4. ✅ Set up custom domain (optional)
5. ✅ Configure backups for output files
6. ✅ Add authentication if needed
7. ✅ Monitor API usage and costs

---

**Your app is ready for the world! 🚀**

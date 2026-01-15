# 🚀 Quick Deploy to Streamlit Cloud (5 Minutes)

The fastest way to get your Document Processing System online!

---

## ✅ Prerequisites

- [x] Code is already on GitHub
- [x] You have your Anthropic API key ready

---

## 📝 Step-by-Step Deployment

### 1️⃣ Go to Streamlit Cloud

Open your browser and go to:
**[share.streamlit.io](https://share.streamlit.io)**

### 2️⃣ Sign In with GitHub

Click **"Continue with GitHub"** and authorize Streamlit Cloud.

### 3️⃣ Create New App

Click the **"New app"** button (big blue button).

### 4️⃣ Configure Your App

Fill in the deployment form:

```
Repository:    buypath/Artif
Branch:        claude/document-processing-system-7mrTo
Main file:     app.py
```

Click **"Advanced settings"** (optional):
- Python version: `3.11`

### 5️⃣ Deploy

Click **"Deploy!"**

Wait 2-3 minutes while Streamlit Cloud:
- ✅ Installs dependencies
- ✅ Configures the environment
- ✅ Starts your app

### 6️⃣ Add Your API Key

**IMPORTANT:** Your app will show an error until you add the API key.

1. Once deployed, click the **"⚙️ Settings"** button (top right)
2. Click **"Secrets"** in the left menu
3. Paste this (replace with your actual key):

```toml
ANTHROPIC_API_KEY = "sk-ant-your-actual-api-key-here"
```

4. Click **"Save"**

Your app will automatically restart with the API key!

### 7️⃣ Access Your Live App

Your app is now live at:
```
https://[random-name].streamlit.app
```

**🎉 That's it! Your app is online!**

---

## 📱 Share Your App

You can now share your app URL with anyone:

```
https://your-app-name.streamlit.app
```

Anyone with the link can:
- Upload Word documents
- Generate semantic analysis
- Create SEO-optimized content
- Download results

---

## ⚙️ App Management

### View Logs

1. Go to your app on Streamlit Cloud
2. Click "Manage app"
3. View logs in real-time

### Update Your App

Your app auto-deploys on git push:

```bash
# Make changes locally
git add .
git commit -m "Update app"
git push

# Streamlit Cloud automatically redeploys!
```

### Change Settings

Access via "⚙️ Settings":
- Update secrets (API keys)
- Change Python version
- View resource usage
- Restart app
- Delete app

---

## 🔒 Security Tips

### Protect Your API Key

✅ **Do:** Add key in Streamlit Cloud secrets
❌ **Don't:** Commit API key to GitHub
❌ **Don't:** Share your secrets publicly

### Control Access (Optional)

Your app is public by default. To restrict access:

1. Add password protection in app.py
2. Use Streamlit Cloud's IP allowlist (paid feature)
3. Deploy on private infrastructure

---

## 💡 Pro Tips

### Custom URL

Free tier gets random URLs like `random-name-123.streamlit.app`

For custom domains like `docs.yourcompany.com`:
- Upgrade to Streamlit Cloud Pro ($20/month)
- Or use alternative deployment (see DEPLOYMENT_GUIDE.md)

### Resource Limits

Free tier includes:
- ✅ 1 GB RAM
- ✅ 1 CPU core
- ✅ Unlimited viewers
- ⚠️ App sleeps after inactivity
- ⚠️ Limited to 3 apps

### Performance

If your app is slow:
1. Check Stage 1/2 token limits in secrets
2. Optimize document sizes
3. Consider upgrading tier
4. Use alternative hosting for heavy workloads

---

## 🆘 Troubleshooting

### "Module not found" Error

**Problem:** Missing dependency
**Solution:** Ensure `requirements.txt` is in root and includes all packages

### "API Key not found" Error

**Problem:** Secret not configured
**Solution:**
1. Go to Settings → Secrets
2. Add: `ANTHROPIC_API_KEY = "your-key"`
3. Save (app restarts automatically)

### App Won't Start

**Problem:** Configuration error
**Solution:**
1. Check logs in Streamlit Cloud
2. Verify `app.py` exists in root
3. Ensure branch name is correct
4. Check Python version compatibility

### File Upload Issues

**Problem:** Files not uploading
**Solution:**
- Max upload: 200MB on Streamlit Cloud
- Only .docx files supported
- Check file isn't corrupted

---

## 📊 Alternative Deployment Options

If Streamlit Cloud doesn't work for you:

| Platform | Best For | Cost |
|----------|----------|------|
| **Railway** | Easy deployment | $5/mo |
| **Heroku** | Traditional PaaS | Free tier |
| **Docker** | Containers | Varies |
| **VPS** | Full control | $5-10/mo |

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## ✅ Checklist

Before sharing your app, verify:

- [ ] App loads without errors
- [ ] Can upload .docx files
- [ ] Stage 1 analysis works
- [ ] Stage 2 rewriting works
- [ ] Can download results
- [ ] API key is secure (in secrets, not code)
- [ ] URL is shareable

---

## 🎉 Success!

Your Document Processing System is now:
- ✅ **Online** and accessible from anywhere
- ✅ **Secure** with encrypted API keys
- ✅ **Auto-updating** on git push
- ✅ **Free** on Streamlit Cloud
- ✅ **Shareable** via simple URL

**Share your app and start processing documents!**

---

**Need help?** Check:
- [WEB_UI_GUIDE.md](WEB_UI_GUIDE.md) - How to use the app
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Other deployment options
- [Streamlit Docs](https://docs.streamlit.io/streamlit-community-cloud)

# 🚀 Quick Deploy Guide - 5 Minutes to Live!

## Deploy to Render (Easiest & Free)

### Step 1: Push to GitHub (2 min)

```bash
cd house-price-prediction

# Initialize git (if not already)
git init
git add .
git commit -m "Ready for deployment"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Deploy on Render (3 min)

1. **Go to [render.com](https://render.com)** → Sign up (free)
2. Click **"New +"** → **"Web Service"**
3. **Connect GitHub** → Select your repository
4. **Configure**:
   - Name: `house-price-prediction`
   - Environment: **Docker**
   - Region: Choose closest
5. **Environment Variables**:
   - `FLASK_ENV=production`
   - (No Google Maps API needed - app uses free OpenStreetMap!)
6. Click **"Create Web Service"**

### Step 3: Wait & Done! ⏱️

- Render builds your Docker image (2-5 minutes)
- Your app goes live automatically
- URL: `https://your-app-name.onrender.com`

### Step 4: Test It! ✅

```bash
# Health check
curl https://your-app-name.onrender.com/health

# Visit in browser
open https://your-app-name.onrender.com
```

---

## 🎯 That's It!

Your app is now live! 🎉

**Note**: Free tier spins down after 15 min inactivity (first request may be slow)

---

## 📝 Next Steps

- **Custom Domain**: Add in Render settings (paid)
- **Persistent Storage**: For model files (if needed)
- **Auto-Deploy**: Enabled by default (deploys on every push)

---

## 🆘 Troubleshooting

**Build fails?**
- Check that `models/` folder has your model files
- Ensure `requirements.txt` is correct

**App crashes?**
- Check logs in Render dashboard
- Verify model files exist

**Need help?** See full guide: `docs/DEPLOYMENT_GUIDE.md`


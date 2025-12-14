# Deployment Guide - House Price Prediction System

This guide covers deploying your Flask ML application to various cloud platforms.

## 🚀 Recommended Platforms

### 1. **Render** (⭐ Best for Free Tier)
- **Free tier available**: Yes (with limitations)
- **Docker support**: Yes
- **Best for**: Quick deployment, free hosting
- **Limitations**: Free tier spins down after 15 min inactivity

### 2. **Railway** (⭐ Best for Docker)
- **Free tier available**: Yes ($5 credit/month)
- **Docker support**: Excellent
- **Best for**: Docker-based deployments, easy setup
- **Limitations**: Credit-based pricing

### 3. **Heroku**
- **Free tier available**: No (discontinued)
- **Docker support**: Yes
- **Best for**: Traditional Flask deployments
- **Limitations**: Paid plans only

### 4. **AWS/GCP/Azure**
- **Free tier available**: Limited (12 months)
- **Docker support**: Yes
- **Best for**: Production, scalability
- **Limitations**: More complex setup

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] Model files are in `models/` directory:
  - `house_price_model.joblib`
  - `preprocessor.joblib`
- [ ] All dependencies are in `requirements.txt`
- [ ] Dockerfile is configured correctly
- [ ] Environment variables are documented
- [ ] `.gitignore` excludes sensitive files

---

## 🎯 Option 1: Deploy to Render (Recommended for Free)

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Ensure model files are committed** (or use Render's persistent disk):
   ```bash
   # If models are large, consider using Git LFS or external storage
   git add models/
   git commit -m "Add trained models"
   ```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Connect your GitHub account

### Step 3: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your repository
3. Configure:
   - **Name**: `house-price-prediction`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty (or `house-price-prediction` if in subfolder)
   - **Environment**: `Docker`
   - **Dockerfile Path**: `Dockerfile`
   - **Docker Context**: `.` (root)

### Step 4: Configure Environment Variables

Add these in Render dashboard → **Environment**:

```
FLASK_ENV=production
PORT=5000
```

**Note**: `GOOGLE_MAPS_API_KEY` is **optional**. The app uses **OpenStreetMap (free)** by default. Only add this if you want to use Google Maps instead.

### Step 5: Update Dockerfile for Render

Render uses port from `$PORT` environment variable. Update your Dockerfile:

```dockerfile
# Change this line in Dockerfile:
EXPOSE 5000

# And update CMD to use PORT env var:
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 4 --timeout 120 src.house_price_prediction.app:app
```

### Step 6: Deploy

1. Click **"Create Web Service"**
2. Render will build and deploy automatically
3. Your app will be available at: `https://your-app-name.onrender.com`

### Step 7: Persistent Storage (for Models)

If models are large, use Render's persistent disk:

1. Go to **Settings** → **Persistent Disk**
2. Add disk (1GB free)
3. Mount at `/app/models`
4. Update Dockerfile to copy models to persistent disk

---

## 🚂 Option 2: Deploy to Railway

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

Or use the web interface.

### Step 2: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**

### Step 3: Configure Deployment

1. Select your repository
2. Railway auto-detects Dockerfile
3. Add environment variables:
   ```
   FLASK_ENV=production
   ```
   **Note**: `GOOGLE_MAPS_API_KEY` is optional - app uses OpenStreetMap by default

### Step 4: Deploy

Railway will automatically:
- Build Docker image
- Deploy your app
- Provide a public URL

### Step 5: Persistent Storage

1. Go to **Settings** → **Volumes**
2. Create volume for `models/` directory
3. Mount at `/app/models`

---

## ☁️ Option 3: Deploy to Heroku

### Step 1: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Or download from heroku.com
```

### Step 2: Login

```bash
heroku login
```

### Step 3: Create Heroku App

```bash
cd house-price-prediction
heroku create your-app-name
```

### Step 4: Configure Buildpacks

```bash
heroku buildpacks:set heroku/python
```

### Step 5: Add Environment Variables

```bash
heroku config:set FLASK_ENV=production
```

**Note**: `GOOGLE_MAPS_API_KEY` is optional - only add if you want Google Maps instead of OpenStreetMap

### Step 6: Deploy

```bash
git push heroku main
```

### Step 7: Scale (if needed)

```bash
heroku ps:scale web=1
```

---

## 🐳 Option 4: Deploy with Docker to Any Platform

### Build Docker Image Locally

```bash
docker build -t house-price-prediction .
```

### Run Locally

```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -v $(pwd)/models:/app/models \
  house-price-prediction
```

### Push to Docker Hub

```bash
# Tag image
docker tag house-price-prediction yourusername/house-price-prediction

# Push to Docker Hub
docker push yourusername/house-price-prediction
```

Then deploy to any platform that supports Docker (AWS ECS, Google Cloud Run, Azure Container Instances, etc.)

---

## 🔧 Platform-Specific Configurations

### Render Configuration

Create `render.yaml` in project root:

```yaml
services:
  - type: web
    name: house-price-prediction
    env: docker
    dockerfilePath: ./Dockerfile
    dockerContext: .
    envVars:
      - key: FLASK_ENV
        value: production
      - key: PORT
        value: 5000
    healthCheckPath: /health
```

### Railway Configuration

Create `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 src.house_price_prediction.app:app",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100
  }
}
```

### Heroku Configuration

Create `Procfile`:

```
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 src.house_price_prediction.app:app
```

---

## 🔍 Post-Deployment Verification

### 1. Health Check

```bash
curl https://your-app-url.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 2. Test Prediction

```bash
curl -X POST https://your-app-url.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "POSTED_BY": "Owner",
    "UNDER_CONSTRUCTION": 0,
    "RERA": 0,
    "BHK_NO.": 3,
    "BHK_OR_RK": "BHK",
    "SQUARE_FT": 1500,
    "READY_TO_MOVE": 1,
    "RESALE": 1,
    "ADDRESS": "Bangalore",
    "LONGITUDE": 12.96991,
    "LATITUDE": 77.59796
  }'
```

### 3. Test Frontend

Visit:
- Landing page: `https://your-app-url.com/`
- Prediction page: `https://your-app-url.com/predict`

---

## 🐛 Troubleshooting

### Issue: Model files not found

**Solution**: Ensure models are:
- Committed to Git (if small)
- Uploaded to persistent storage
- Mounted as volumes in Docker

### Issue: Port binding error

**Solution**: Use `$PORT` environment variable:
```python
port = int(os.environ.get('PORT', 5000))
```

### Issue: Build timeout

**Solution**: 
- Optimize Dockerfile (multi-stage builds)
- Use `.dockerignore` to exclude unnecessary files
- Pre-build and push to Docker Hub

### Issue: Memory limits

**Solution**:
- Reduce Gunicorn workers: `--workers 2`
- Use lighter base image: `python:3.14-slim`
- Optimize model size

---

## 📊 Platform Comparison

| Platform | Free Tier | Docker | Ease | Best For |
|----------|-----------|--------|------|----------|
| **Render** | ✅ Yes | ✅ Yes | ⭐⭐⭐⭐⭐ | Quick deployment |
| **Railway** | ✅ $5 credit | ✅ Yes | ⭐⭐⭐⭐⭐ | Docker apps |
| **Heroku** | ❌ No | ✅ Yes | ⭐⭐⭐⭐ | Traditional |
| **AWS** | ⚠️ Limited | ✅ Yes | ⭐⭐ | Production |
| **GCP** | ⚠️ Limited | ✅ Yes | ⭐⭐ | Production |
| **Vercel** | ✅ Yes | ❌ No | ⭐⭐ | Serverless (not ideal for Flask) |

---

## 🎯 Quick Start: Render (Recommended)

1. **Push to GitHub**
2. **Go to render.com** → Sign up
3. **New Web Service** → Connect repo
4. **Environment**: Docker
5. **Add env vars**: `FLASK_ENV=production`
6. **Deploy** → Done! 🎉

Your app will be live at: `https://your-app.onrender.com`

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

## 💡 Pro Tips

1. **Use environment variables** for all secrets (API keys, etc.)
2. **Enable health checks** for automatic restarts
3. **Set up monitoring** (Render/Railway have built-in monitoring)
4. **Use persistent storage** for model files
5. **Enable auto-deploy** from main branch
6. **Set up custom domain** (available on paid plans)

---

**Need help?** Check the platform-specific documentation or open an issue in your repository.


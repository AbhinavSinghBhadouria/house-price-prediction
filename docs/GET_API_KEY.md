# 🗺️ How to Get Google Maps API Key - Step by Step Guide

## ✅ Quick Answer

**No, I don't have your API key** - You need to get it yourself from Google. It's **FREE** for most uses!

## 📋 Step-by-Step Instructions

### Step 1: Go to Google Cloud Console
1. Visit: https://console.cloud.google.com/
2. Sign in with your Google account (Gmail account works)

### Step 2: Create a Project
1. Click the project dropdown at the top
2. Click **"New Project"**
3. Enter project name: `House Price Prediction` (or any name)
4. Click **"Create"**
5. Wait a few seconds, then select your new project

### Step 3: Enable Required APIs
1. Go to **"APIs & Services"** → **"Library"** (left sidebar)
2. Search for and enable these APIs one by one:
   - **"Maps JavaScript API"** → Click → Enable
   - **"Places API"** → Click → Enable  
   - **"Geocoding API"** → Click → Enable

### Step 4: Create API Key
1. Go to **"APIs & Services"** → **"Credentials"** (left sidebar)
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"API Key"**
4. Your API key will appear! **Copy it immediately**

### Step 5: (Optional) Restrict API Key
For security, restrict the key:
1. Click on your API key to edit it
2. Under **"Application restrictions"** → Select **"HTTP referrers"**
3. Add: `http://localhost:5001/*`
4. Click **"Save"**

### Step 6: Add Key to Your Project

**Option A: Environment Variable (Recommended)**
```bash
export GOOGLE_MAPS_API_KEY="your_api_key_here"
```

**Option B: Direct in Code (Quick Test)**
1. Open: `src/house_price_prediction/templates/predict.html`
2. Find: `key={{ google_maps_key }}`
3. Replace with: `key=YOUR_ACTUAL_API_KEY_HERE`

## 💰 Cost Information

**✅ USUALLY FREE FOR YOUR PROJECT!**

**FREE TIER (Monthly):**
- $200 free credit per month from Google
- Maps JavaScript API: **28,000 free loads/month**
- Places API: **1,000 free requests/day** (30,000/month)
- Geocoding API: **40,000 free requests/month**

**For your house price prediction project:**
- If 100 people use it daily = **$0 cost** ✅
- If 1,000 people use it daily = **Still likely $0** ✅
- Only pay if you have 10,000+ daily users

**See `GOOGLE_MAPS_PRICING.md` for detailed pricing information!**

## 🚀 After Adding the Key

1. Restart your server:
```bash
pkill -f "python.*app"
python -m src.house_price_prediction.app
```

2. Go to: http://localhost:5001/predict
3. You should see the map!

## ❓ Troubleshooting

**"This page can't load Google Maps correctly"**
- Check API key is correct
- Ensure all 3 APIs are enabled
- Check browser console for errors

**Map not showing**
- Verify API key in browser console
- Check that APIs are enabled
- Try a different browser

## 📝 Quick Checklist

- [ ] Created Google Cloud project
- [ ] Enabled Maps JavaScript API
- [ ] Enabled Places API
- [ ] Enabled Geocoding API
- [ ] Created API key
- [ ] Added key to project (env var or code)
- [ ] Restarted server
- [ ] Tested map on prediction page

---

**Need Help?** Check `docs/GOOGLE_MAPS_SETUP.md` for more details!


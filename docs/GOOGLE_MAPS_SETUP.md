# Google Maps API Setup Guide

## 🗺️ Setting Up Google Maps Integration

The prediction page now includes Google Maps integration for easy location selection. Follow these steps to set it up:

## 📋 Step 1: Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Maps JavaScript API**
   - **Places API** (for address autocomplete)
   - **Geocoding API** (for address to coordinates conversion)

4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Copy your API key

## 🔧 Step 2: Add API Key to Project

### Option A: Environment Variable (Recommended for Production)

1. Create a `.env` file in the project root:
```bash
GOOGLE_MAPS_API_KEY=your_api_key_here
```

2. Update `app.py` to pass the key to templates:
```python
import os
from dotenv import load_dotenv

load_dotenv()

@app.route('/predict')
def predict_page():
    api_key = os.getenv('GOOGLE_MAPS_API_KEY', 'YOUR_API_KEY')
    return render_template('predict.html', google_maps_key=api_key)
```

3. Update `predict.html`:
```html
<script src="https://maps.googleapis.com/maps/api/js?key={{ google_maps_key }}&libraries=places&callback=initMap" async defer></script>
```

### Option B: Direct Replacement (Quick Test)

1. Open `src/house_price_prediction/templates/predict.html`
2. Find the line:
```html
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places&callback=initMap" async defer></script>
```
3. Replace `YOUR_API_KEY` with your actual API key

## 🔒 Step 3: Restrict API Key (Security)

1. Go to **Credentials** in Google Cloud Console
2. Click on your API key
3. Under **Application restrictions**, select **HTTP referrers**
4. Add your domain(s):
   - `http://localhost:5001/*` (for development)
   - `https://yourdomain.com/*` (for production)
5. Save changes

## ✅ Step 4: Test the Integration

1. Start your Flask server:
```bash
python -m src.house_price_prediction.app
```

2. Navigate to: `http://localhost:5001/predict`
3. You should see:
   - A map displayed
   - Address search box
   - Clickable map to select location
   - Auto-filled coordinates

## 🎯 Features

### 1. **Map Picker**
- Click anywhere on the map to select location
- Drag the marker to adjust position
- Coordinates automatically update

### 2. **Address Search**
- Type an address in the search box
- Select from autocomplete suggestions
- Map centers on selected location
- Coordinates and marker update automatically

### 3. **Reverse Geocoding**
- When you click on the map, the address is automatically filled
- Shows the formatted address for the selected coordinates

## 💰 Pricing

Google Maps API has a free tier:
- **$200 free credit per month**
- Maps JavaScript API: Free for first 28,000 loads
- Places API: Free for first 1,000 requests/day
- Geocoding API: Free for first 40,000 requests/month

For most personal/small projects, this is sufficient.

## 🐛 Troubleshooting

### Map Not Loading
- Check browser console for errors
- Verify API key is correct
- Ensure required APIs are enabled
- Check API key restrictions

### "This page can't load Google Maps correctly"
- API key might be invalid
- Required APIs not enabled
- API key restrictions too strict

### Autocomplete Not Working
- Ensure Places API is enabled
- Check that `libraries=places` is in the script URL

## 📝 Notes

- The map is styled with a dark theme to match the futuristic UI
- Default center is set to India (lat: 20.5937, lng: 78.9629)
- Map is restricted to India by default (can be changed in `predict.js`)
- Coordinates are automatically formatted to 6 decimal places

---

**Status**: ✅ **GOOGLE MAPS INTEGRATION READY** (Requires API key setup)


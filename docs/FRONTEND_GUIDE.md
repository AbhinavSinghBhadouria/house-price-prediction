# Frontend User Guide

## 🌐 Web Interface

The House Price Prediction System includes a modern, user-friendly web interface that allows anyone to predict house prices without technical knowledge.

## 🚀 Accessing the Frontend

### Start the Server
```bash
python -m src.house_price_prediction.app
```

### Open in Browser
Navigate to: **http://localhost:5000**

## 📝 Using the Frontend

### Step 1: Fill in Property Details

**Required Fields (marked with *):**
- **Property Type**: BHK or RK
- **Number of Bedrooms**: 1-10
- **Area (Square Feet)**: Property area
- **Posted By**: Owner, Dealer, or Builder
- **Location**: Longitude and Latitude coordinates

**Optional Fields:**
- **Address**: Property address
- **Under Construction**: Yes/No
- **RERA Approved**: Yes/No
- **Ready to Move**: Yes/No
- **Resale**: Yes/No

### Step 2: Get Prediction

1. Click **"Predict Price"** button
2. Wait for the AI model to process (usually < 50ms)
3. View the predicted price in Indian currency format (₹Lakhs/Crores)

### Step 3: View Results

The results card displays:
- **Estimated Price**: Formatted in ₹Lakhs or ₹Crores
- **Inference Time**: How fast the prediction was made
- **Model Accuracy**: 90.97% R² Score

## 🎨 Features

### Modern UI
- ✅ Beautiful gradient design
- ✅ Responsive layout (works on mobile/tablet/desktop)
- ✅ Smooth animations
- ✅ Professional appearance

### User Experience
- ✅ Clear form validation
- ✅ Loading states
- ✅ Error handling
- ✅ Success animations
- ✅ Easy-to-use interface

### Technical Features
- ✅ Real-time API communication
- ✅ Indian currency formatting (Lakhs/Crores)
- ✅ Fast inference (< 50ms)
- ✅ Model accuracy display

## 📱 Responsive Design

The frontend is fully responsive and works on:
- 💻 Desktop computers
- 📱 Mobile phones
- 📲 Tablets

## 🔧 Technical Details

### Frontend Stack
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **Vanilla JavaScript**: No framework dependencies
- **Flask Templates**: Server-side rendering

### API Integration
- RESTful API communication
- JSON data format
- Error handling
- Loading states

## 🎯 Example Usage

1. **Property Type**: BHK
2. **Bedrooms**: 3
3. **Area**: 1500 sq ft
4. **Posted By**: Owner
5. **Longitude**: 77.2090
6. **Latitude**: 28.6139
7. **Ready to Move**: Yes

**Result**: Predicted price displayed in ₹Lakhs/Crores

## 🐛 Troubleshooting

### Frontend not loading
- Ensure Flask server is running
- Check browser console for errors
- Verify port 5000 is available

### Prediction fails
- Check all required fields are filled
- Verify model is loaded (check /health endpoint)
- Check browser console for API errors

### Styling issues
- Clear browser cache
- Check static files are being served
- Verify CSS/JS files exist in static/ directory

## 📊 API Endpoints

The frontend uses these endpoints:
- `GET /` - Frontend page
- `POST /predict` - Get price prediction
- `GET /health` - Check API health

## 🎨 Customization

### Changing Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #2563eb;  /* Change this */
    --primary-dark: #1e40af;   /* And this */
}
```

### Modifying Layout
Edit `templates/index.html` for structure changes.

### Adding Features
Edit `static/js/app.js` for new functionality.

---

**Status**: ✅ **FRONTEND READY FOR USE**


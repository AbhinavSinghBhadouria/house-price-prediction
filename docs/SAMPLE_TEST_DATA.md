# 📋 Sample Test Data for House Price Prediction

## ✅ Working Test Data Examples

Use these sample data examples to test your prediction API:

### Example 1: Basic Property (Bangalore)
```json
{
  "POSTED_BY": "Owner",
  "UNDER_CONSTRUCTION": 0,
  "RERA": 0,
  "BHK_NO.": 3,
  "BHK_OR_RK": "BHK",
  "SQUARE_FT": 1500,
  "READY_TO_MOVE": 1,
  "RESALE": 1,
  "ADDRESS": "Ksfc Layout, Bangalore",
  "LONGITUDE": 12.96991,
  "LATITUDE": 77.59796,
  "area": 1500,
  "bedrooms": 3,
  "longitude": 12.96991,
  "latitude": 77.59796,
  "CITY_NAME": "Bangalore"
}
```

### Example 2: Under Construction Property (Mumbai)
```json
{
  "POSTED_BY": "Builder",
  "UNDER_CONSTRUCTION": 1,
  "RERA": 1,
  "BHK_NO.": 2,
  "BHK_OR_RK": "BHK",
  "SQUARE_FT": 1200,
  "READY_TO_MOVE": 0,
  "RESALE": 0,
  "ADDRESS": "Andheri West, Mumbai",
  "LONGITUDE": 19.1364,
  "LATITUDE": 72.8296,
  "area": 1200,
  "bedrooms": 2,
  "longitude": 19.1364,
  "latitude": 72.8296,
  "CITY_NAME": "Mumbai"
}
```

### Example 3: Ready to Move (Delhi)
```json
{
  "POSTED_BY": "Dealer",
  "UNDER_CONSTRUCTION": 0,
  "RERA": 1,
  "BHK_NO.": 4,
  "BHK_OR_RK": "BHK",
  "SQUARE_FT": 2000,
  "READY_TO_MOVE": 1,
  "RESALE": 1,
  "ADDRESS": "Sector 5, Noida",
  "LONGITUDE": 28.5355,
  "LATITUDE": 77.3910,
  "area": 2000,
  "bedrooms": 4,
  "longitude": 28.5355,
  "latitude": 77.3910,
  "CITY_NAME": "Noida"
}
```

## 🧪 Testing via Frontend

### Step 1: Fill in the Form
1. **Property Type**: BHK
2. **Bedrooms**: 3
3. **Area**: 1500 sq ft
4. **Posted By**: Owner
5. **Longitude**: 12.96991
6. **Latitude**: 77.59796
7. **Ready to Move**: Yes
8. **Resale**: Yes

### Step 2: Click "Predict Price"

## 🧪 Testing via API (curl)

```bash
curl -X POST http://localhost:5001/predict \
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
    "LATITUDE": 77.59796,
    "area": 1500,
    "bedrooms": 3,
    "longitude": 12.96991,
    "latitude": 77.59796,
    "CITY_NAME": "Bangalore"
  }'
```

## 📝 Required Fields

**All fields are required:**
- `POSTED_BY`: "Owner", "Dealer", or "Builder"
- `UNDER_CONSTRUCTION`: 0 or 1
- `RERA`: 0 or 1
- `BHK_NO.`: Number (1-10)
- `BHK_OR_RK`: "BHK" or "RK"
- `SQUARE_FT`: Number (area in square feet)
- `READY_TO_MOVE`: 0 or 1
- `RESALE`: 0 or 1
- `ADDRESS`: String (any address)
- `LONGITUDE`: Number (e.g., 12.96991)
- `LATITUDE`: Number (e.g., 77.59796)
- `area`: Same as SQUARE_FT
- `bedrooms`: Same as BHK_NO.
- `longitude`: Same as LONGITUDE
- `latitude`: Same as LATITUDE
- `CITY_NAME`: String (e.g., "Bangalore", "Mumbai")

## ⚠️ Common Issues

### Issue: "No JSON data provided"
**Solution**: Make sure you're sending JSON data with Content-Type header

### Issue: "Model not loaded"
**Solution**: Run `python scripts/train.py` first to train the model

### Issue: Missing columns error
**Solution**: Ensure all required fields are included in your JSON

### Issue: Prediction returns error
**Solution**: Check server logs for detailed error messages

## 🔍 Debugging

Check server logs:
```bash
tail -f server.log
```

Or check the API response for error details.


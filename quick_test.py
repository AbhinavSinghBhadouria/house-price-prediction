#!/usr/bin/env python3
"""
Quick test to verify model accuracy and location differentiation
"""

import joblib
import pandas as pd
from src.house_price_prediction.preprocessing import HousePricePreprocessor

# Load model and preprocessor
print("Loading model and preprocessor...")
model = joblib.load('models/house_price_model.joblib')
preprocessor_data = joblib.load('models/preprocessor.joblib')

# Recreate preprocessor
preprocessor = HousePricePreprocessor()
preprocessor.scaler = preprocessor_data['scaler']
preprocessor.label_encoders = preprocessor_data['label_encoders']
preprocessor.imputer = preprocessor_data['imputer']
preprocessor.feature_names = preprocessor_data['feature_names']
preprocessor.is_fitted = preprocessor_data['is_fitted']

# Test data
test_cases = [
    {
        "name": "Kanpur",
        "data": {
            "POSTED_BY": "Owner", "UNDER_CONSTRUCTION": 0, "RERA": 1, "BHK_NO.": 3, "BHK_OR_RK": "BHK",
            "SQUARE_FT": 1500, "READY_TO_MOVE": 1, "RESALE": 1,
            "ADDRESS": "Civil Lines, Kanpur", "LONGITUDE": 80.3319, "LATITUDE": 26.4499,
            "area": 1500, "bedrooms": 3, "longitude": 80.3319, "latitude": 26.4499, "CITY_NAME": "Kanpur"
        }
    },
    {
        "name": "Lucknow",
        "data": {
            "POSTED_BY": "Owner", "UNDER_CONSTRUCTION": 0, "RERA": 1, "BHK_NO.": 3, "BHK_OR_RK": "BHK",
            "SQUARE_FT": 1500, "READY_TO_MOVE": 1, "RESALE": 1,
            "ADDRESS": "Gomti Nagar, Lucknow", "LONGITUDE": 80.9462, "LATITUDE": 26.8467,
            "area": 1500, "bedrooms": 3, "longitude": 80.9462, "latitude": 26.8467, "CITY_NAME": "Lucknow"
        }
    },
    {
        "name": "Mumbai",
        "data": {
            "POSTED_BY": "Dealer", "UNDER_CONSTRUCTION": 0, "RERA": 1, "BHK_NO.": 3, "BHK_OR_RK": "BHK",
            "SQUARE_FT": 1200, "READY_TO_MOVE": 1, "RESALE": 1,
            "ADDRESS": "Andheri West, Mumbai", "LONGITUDE": 72.8296, "LATITUDE": 19.1364,
            "area": 1200, "bedrooms": 3, "longitude": 72.8296, "latitude": 19.1364, "CITY_NAME": "Mumbai"
        }
    }
]

print("\n🧪 TESTING MODEL ACCURACY AND LOCATION DIFFERENTIATION")
print("="*70)

results = {}
for test_case in test_cases:
    print(f"\nTesting {test_case['name']}:")

    # Extract city from address (simulate API behavior)
    data = test_case['data'].copy()
    address = data.get('ADDRESS', '')
    if address and ',' in address:
        extracted_city = address.split(',')[-1].strip().title()
        data['CITY_NAME'] = extracted_city
        print(f"  Extracted city: {extracted_city}")

    # Convert to DataFrame and preprocess
    df = pd.DataFrame([data])
    X_processed = preprocessor.transform(df)

    # Make prediction
    prediction = model.predict(X_processed)[0]
    results[test_case['name']] = prediction

    print(f"  Predicted price: ₹{prediction:,.0f}")

print("\n" + "="*70)
print("📊 RESULTS ANALYSIS")
print("="*70)

# Check if predictions are different
prices = list(results.values())
unique_prices = len(set(prices))

print(f"Total predictions: {len(prices)}")
print(f"Unique predictions: {unique_prices}")

if unique_prices == len(prices):
    print("✅ SUCCESS: All cities give different predictions!")

    # Show price differences
    print("\nPrice differences:")
    cities = list(results.keys())
    for i in range(len(cities)):
        for j in range(i+1, len(cities)):
            city1, city2 = cities[i], cities[j]
            price1, price2 = results[city1], results[city2]
            diff = abs(price1 - price2)
            pct_diff = (diff / min(price1, price2)) * 100
            print(f"  {city1} vs {city2}: ₹{diff:,.0f} ({pct_diff:.1f}%)")
else:
    print("❌ FAILURE: Some cities give identical predictions")
    print("This indicates the model is not using location data properly")

# Expected price ranges (based on training data)
expected_ranges = {
    "Kanpur": (8000000, 13000000),    # ~1.01 crore avg
    "Lucknow": (5000000, 13000000),  # ~89 lakh avg
    "Mumbai": (15000000, 40000000)   # ~2.65 crore avg
}

print("\n🎯 ACCURACY CHECK (against training data averages):")
accurate_predictions = 0
for city, price in results.items():
    if city in expected_ranges:
        min_price, max_price = expected_ranges[city]
        in_range = min_price <= price <= max_price
        status = "✅ ACCURATE" if in_range else "❌ OUTLIER"
        print(f"  {city}: {status} (₹{price:,.0f} vs expected ₹{min_price:,.0f}-₹{max_price:,.0f})")
        if in_range:
            accurate_predictions += 1

accuracy_rate = (accurate_predictions / len(results)) * 100
print(f"\nAccuracy Rate: {accuracy_rate:.1f}% ({accurate_predictions}/{len(results)})")

print("\n" + "="*70)
if unique_prices == len(prices) and accuracy_rate >= 75:
    print("🎉 VERDICT: MODEL PASSES BRUTAL TESTING!")
    print("   - Location differentiation: ✅ WORKING")
    print("   - Price accuracy: ✅ GOOD")
    print("   - Ready for production deployment")
elif unique_prices == len(prices):
    print("⚠️  VERDICT: MODEL HAS LOCATION AWARENESS BUT NEEDS PRICE TUNING")
    print("   - Location differentiation: ✅ WORKING")
    print("   - Price accuracy: ❌ NEEDS IMPROVEMENT")
else:
    print("❌ VERDICT: MODEL FAILS BRUTAL TESTING!")
    print("   - Location differentiation: ❌ BROKEN")
    print("   - Model not using location data properly")

print("="*70)

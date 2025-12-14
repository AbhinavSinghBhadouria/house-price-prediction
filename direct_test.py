#!/usr/bin/env python3
"""
Direct test of the model without API
"""

import sys
import os
sys.path.insert(0, 'src')

import joblib
import pandas as pd
import numpy as np
from house_price_prediction.preprocessing import HousePricePreprocessor

def test_model_directly():
    print("🧪 TESTING MODEL DIRECTLY")
    print("=" * 50)

    # Load model and preprocessor
    try:
        model = joblib.load('models/house_price_model.joblib')
        preprocessor_data = joblib.load('models/preprocessor.joblib')
        preprocessor = HousePricePreprocessor()
        preprocessor.scaler = preprocessor_data['scaler']
        preprocessor.label_encoders = preprocessor_data['label_encoders']
        preprocessor.imputer = preprocessor_data['imputer']
        preprocessor.feature_names = preprocessor_data['feature_names']
        preprocessor.is_fitted = preprocessor_data['is_fitted']
        print("✅ Model and preprocessor loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return

    # Test different cities
    cities = [
        ('Mumbai', 72.8777, 19.0760),
        ('Delhi', 77.2090, 28.6139),
        ('Bangalore', 77.5946, 12.9716),
        ('Lucknow', 80.9462, 26.8467),
        ('Kanpur', 80.3319, 26.4499),
    ]

    print("\n🏠 Testing predictions for different cities:")
    print("(All: 1500 sqft, 3BHK, Owner, RERA approved)")

    results = []

    for city_name, lng, lat in cities:
        data = {
            'POSTED_BY': 'Owner', 'UNDER_CONSTRUCTION': 0, 'RERA': 1,
            'BHK_NO.': 3, 'BHK_OR_RK': 'BHK', 'SQUARE_FT': 1500,
            'READY_TO_MOVE': 1, 'RESALE': 1,
            'ADDRESS': f'Downtown, {city_name}',
            'LONGITUDE': lng, 'LATITUDE': lat,
            'area': 1500, 'bedrooms': 3,
            'longitude': lng, 'latitude': lat,
            'CITY_NAME': city_name
        }

        try:
            df = pd.DataFrame([data])
            X_processed = preprocessor.transform(df)
            prediction = model.predict(X_processed)[0]
            results.append((city_name, prediction))
            print(f"{city_name:12}: ₹{prediction:,.0f}")
        except Exception as e:
            print(f"{city_name:12}: Error - {e}")

    # Test within Mumbai
    print("\n🏘️  Testing different locations within Mumbai:")

    mumbai_locations = [
        ('Andheri, Mumbai', 72.8697, 19.1197),
        ('Bandra, Mumbai', 72.8402, 19.0596),
        ('Juhu, Mumbai', 72.8295, 19.1075),
        ('Powai, Mumbai', 72.9046, 19.1197),
        ('Thane, Mumbai', 72.9781, 19.2183),
    ]

    mumbai_results = []

    for address, lng, lat in mumbai_locations:
        data = {
            'POSTED_BY': 'Owner', 'UNDER_CONSTRUCTION': 0, 'RERA': 1,
            'BHK_NO.': 3, 'BHK_OR_RK': 'BHK', 'SQUARE_FT': 1500,
            'READY_TO_MOVE': 1, 'RESALE': 1,
            'ADDRESS': address,
            'LONGITUDE': lng, 'LATITUDE': lat,
            'area': 1500, 'bedrooms': 3,
            'longitude': lng, 'latitude': lat,
            'CITY_NAME': 'Mumbai'
        }

        try:
            df = pd.DataFrame([data])
            X_processed = preprocessor.transform(df)
            prediction = model.predict(X_processed)[0]
            mumbai_results.append((address, prediction))
            print(f"{address:20}: ₹{prediction:,.0f}")
        except Exception as e:
            print(f"{address:20}: Error - {e}")

    # Analysis
    print("\n📊 ANALYSIS:")

    if results:
        city_prices = [price for _, price in results]
        unique_city_prices = len(set(city_prices))
        print(f"Cities: {unique_city_prices}/{len(results)} unique prices")
        if unique_city_prices == len(results):
            print("✅ Model differentiates between DIFFERENT cities")
        else:
            print("❌ Model does NOT differentiate between cities")

    if mumbai_results:
        mumbai_prices = [price for _, price in mumbai_results]
        unique_mumbai_prices = len(set(mumbai_prices))
        print(f"Within Mumbai: {unique_mumbai_prices}/{len(mumbai_results)} unique prices")
        if unique_mumbai_prices == len(mumbai_results):
            print("✅ Model differentiates between neighborhoods within Mumbai")
        else:
            print("❌ Model does NOT differentiate between neighborhoods within the same city")

if __name__ == "__main__":
    test_model_directly()
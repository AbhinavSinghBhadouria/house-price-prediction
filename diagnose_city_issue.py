#!/usr/bin/env python3
"""
Diagnostic script to understand why CITY_NAME is not affecting predictions
"""

import sys
import os
sys.path.insert(0, 'src')

import joblib
import pandas as pd
import numpy as np
from house_price_prediction.preprocessing import HousePricePreprocessor

def diagnose_issue():
    print("🔍 DIAGNOSING CITY_NAME ISSUE")
    print("=" * 60)
    
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
        print("✅ Model and preprocessor loaded successfully\n")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return
    
    # Show what features the model expects
    print("📋 MODEL EXPECTED FEATURES:")
    print(f"   Total features: {len(preprocessor.feature_names)}")
    print(f"   Features: {preprocessor.feature_names}\n")
    
    # Check if CITY_NAME is in expected features
    has_city_name = 'CITY_NAME' in preprocessor.feature_names
    print(f"🔍 CITY_NAME in features: {has_city_name}")
    
    if has_city_name:
        print(f"   ✅ CITY_NAME is expected by the model")
        # Check label encoder for CITY_NAME
        if 'CITY_NAME' in preprocessor.label_encoders:
            encoder = preprocessor.label_encoders['CITY_NAME']
            print(f"   Label encoder classes: {list(encoder.classes_)}")
            print(f"   Number of cities in training: {len(encoder.classes_)}")
    else:
        print(f"   ❌ CITY_NAME is NOT in the expected features!")
        print(f"   This means the model was NOT trained with city information.")
        print(f"   The model cannot differentiate between cities.\n")
    
    # Test with different cities
    print("\n" + "=" * 60)
    print("🧪 TESTING WITH DIFFERENT CITIES")
    print("=" * 60)
    
    cities = [
        ('Mumbai', 72.8777, 19.0760),
        ('Delhi', 77.2090, 28.6139),
        ('Bangalore', 77.5946, 12.9716),
    ]
    
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
            print(f"\n📊 Input data for {city_name}:")
            print(f"   CITY_NAME: {data['CITY_NAME']}")
            print(f"   Columns in input: {list(df.columns)}")
            
            # Transform
            X_processed = preprocessor.transform(df)
            print(f"   Processed shape: {X_processed.shape}")
            
            # Check if CITY_NAME column exists after transformation
            if 'CITY_NAME' in X_processed.columns:
                city_value = X_processed['CITY_NAME'].iloc[0]
                print(f"   CITY_NAME value after encoding: {city_value}")
            else:
                print(f"   ⚠️  CITY_NAME column missing after transformation!")
            
            # Show a few feature values
            print(f"   Sample features (first 5):")
            for i, col in enumerate(X_processed.columns[:5]):
                print(f"      {col}: {X_processed[col].iloc[0]}")
            
            # Predict
            prediction = model.predict(X_processed)[0]
            results.append((city_name, prediction))
            print(f"   💰 Predicted price: ₹{prediction:,.0f}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Analysis
    print("\n" + "=" * 60)
    print("📊 ANALYSIS")
    print("=" * 60)
    
    if results:
        prices = [price for _, price in results]
        unique_prices = len(set(prices))
        print(f"Unique prices: {unique_prices}/{len(results)}")
        
        if unique_prices == 1:
            print("\n❌ PROBLEM IDENTIFIED:")
            print("   All cities are producing the SAME price!")
            print("\n💡 LIKELY CAUSES:")
            if not has_city_name:
                print("   1. CITY_NAME is not in the model's expected features")
                print("      → The model was not trained with city information")
                print("      → Solution: Retrain the model with CITY_NAME as a feature")
            else:
                print("   1. CITY_NAME is in features but all cities are being encoded to the same value")
                print("      → Check if cities exist in the label encoder")
                print("      → Check if unseen cities are being mapped to a default value")
            print("   2. Other features (like location coordinates) might not be varying enough")
            print("   3. The model might be too simple or not learning location differences")
        else:
            print("\n✅ Model is producing different prices for different cities")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    diagnose_issue()

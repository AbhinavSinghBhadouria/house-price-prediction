#!/usr/bin/env python3
"""
Quick test to verify if different cities produce different predictions
Tests with Kochi and Chennai (cities in training data)
"""

import sys
sys.path.insert(0, 'src')

import joblib
import pandas as pd
from house_price_prediction.preprocessing import HousePricePreprocessor

def test_city_differences():
    print("🧪 TESTING CITY DIFFERENCES (Kochi vs Chennai)")
    print("=" * 70)
    
    try:
        # Load model and preprocessor
        model = joblib.load('models/house_price_model.joblib')
        preprocessor = HousePricePreprocessor()
        preprocessor.load('models/preprocessor.joblib')
        print("✅ Model and preprocessor loaded\n")
        
        # Check if CITY_NAME is in features
        has_city = 'CITY_NAME' in preprocessor.feature_names
        print(f"📍 CITY_NAME in model features: {has_city}")
        
        if has_city and 'CITY_NAME' in preprocessor.label_encoders:
            cities = list(preprocessor.label_encoders['CITY_NAME'].classes_)
            print(f"   Cities in training: {len(cities)}")
            kochi_in = 'Kochi' in cities or any('kochi' in c.lower() for c in cities)
            chennai_in = 'Chennai' in cities or any('chennai' in c.lower() for c in cities)
            print(f"   Kochi in training: {kochi_in}")
            print(f"   Chennai in training: {chennai_in}\n")
        
        # Test data - same property specs, different cities
        test_cases = [
            {
                'name': 'Kochi',
                'data': {
                    'POSTED_BY': 'Owner', 'UNDER_CONSTRUCTION': 0, 'RERA': 1,
                    'BHK_NO.': 3, 'BHK_OR_RK': 'BHK', 'SQUARE_FT': 1500,
                    'READY_TO_MOVE': 1, 'RESALE': 1,
                    'ADDRESS': 'Downtown, Kochi',
                    'LONGITUDE': 76.2673, 'LATITUDE': 9.9312,
                    'area': 1500, 'bedrooms': 3,
                    'longitude': 76.2673, 'latitude': 9.9312,
                    'CITY_NAME': 'Kochi'
                }
            },
            {
                'name': 'Chennai',
                'data': {
                    'POSTED_BY': 'Owner', 'UNDER_CONSTRUCTION': 0, 'RERA': 1,
                    'BHK_NO.': 3, 'BHK_OR_RK': 'BHK', 'SQUARE_FT': 1500,
                    'READY_TO_MOVE': 1, 'RESALE': 1,
                    'ADDRESS': 'Downtown, Chennai',
                    'LONGITUDE': 80.2707, 'LATITUDE': 13.0827,
                    'area': 1500, 'bedrooms': 3,
                    'longitude': 80.2707, 'latitude': 13.0827,
                    'CITY_NAME': 'Chennai'
                }
            }
        ]
        
        results = []
        print("📊 PREDICTIONS:")
        print("-" * 70)
        
        for test_case in test_cases:
            df = pd.DataFrame([test_case['data']])
            X_processed = preprocessor.transform(df)
            
            # Check CITY_NAME encoding
            if 'CITY_NAME' in X_processed.columns:
                city_encoded = X_processed['CITY_NAME'].iloc[0]
                print(f"{test_case['name']:10} - CITY_NAME encoding: {city_encoded}")
            else:
                print(f"{test_case['name']:10} - ⚠️  CITY_NAME column missing!")
            
            prediction = model.predict(X_processed)[0]
            results.append((test_case['name'], prediction))
            print(f"{'':10}   Predicted price: ₹{prediction:,.0f}\n")
        
        # Analysis
        print("=" * 70)
        print("📊 ANALYSIS:")
        print(f"   Kochi:  ₹{results[0][1]:,.0f}")
        print(f"   Chennai: ₹{results[1][1]:,.0f}")
        print(f"   Difference: ₹{abs(results[0][1] - results[1][1]):,.0f}")
        
        if results[0][1] == results[1][1]:
            print("\n❌ ISSUE: Both cities have IDENTICAL prices!")
            print("\n💡 SOLUTION:")
            print("   1. The model was trained with the bug (categorical features scaled)")
            print("   2. You need to RETRAIN the model with the fixed preprocessing")
            print("   3. After retraining, cities will produce different predictions")
        else:
            diff_pct = (abs(results[0][1] - results[1][1]) / min(results[0][1], results[1][1])) * 100
            print(f"   Difference: {diff_pct:.1f}%")
            if diff_pct > 1:
                print("\n✅ SUCCESS: Cities have different prices!")
            else:
                print("\n⚠️  WARNING: Prices are very similar (might need retraining)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_city_differences()

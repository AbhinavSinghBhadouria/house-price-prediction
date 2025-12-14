#!/usr/bin/env python3
"""
Inspect the saved model to see what features it actually uses
"""

import sys
import os
sys.path.insert(0, 'src')

import joblib
import pandas as pd
import numpy as np

def inspect_model():
    print("🔍 INSPECTING SAVED MODEL AND PREPROCESSOR")
    print("=" * 70)
    
    try:
        # Load preprocessor
        preprocessor_data = joblib.load('models/preprocessor.joblib')
        print("✅ Preprocessor loaded\n")
        
        # Check feature names
        feature_names = preprocessor_data.get('feature_names', [])
        print(f"📋 TOTAL FEATURES: {len(feature_names)}")
        print(f"\n📝 ALL FEATURES:")
        for i, feat in enumerate(feature_names, 1):
            print(f"   {i:3d}. {feat}")
        
        # Check if CITY_NAME is in features
        print(f"\n{'='*70}")
        has_city_name = 'CITY_NAME' in feature_names
        print(f"🏙️  CITY_NAME in features: {has_city_name}")
        
        if has_city_name:
            print("   ✅ CITY_NAME IS being used by the model")
            # Check label encoder
            label_encoders = preprocessor_data.get('label_encoders', {})
            if 'CITY_NAME' in label_encoders:
                encoder = label_encoders['CITY_NAME']
                cities = list(encoder.classes_)
                print(f"   📍 Cities in training data: {len(cities)}")
                print(f"   Cities: {cities[:10]}{'...' if len(cities) > 10 else ''}")
                
                # Check if Kochi and Chennai are in there
                kochi_in = 'Kochi' in cities or 'kochi' in [c.lower() for c in cities]
                chennai_in = 'Chennai' in cities or 'chennai' in [c.lower() for c in cities]
                print(f"\n   Kochi in training: {kochi_in}")
                print(f"   Chennai in training: {chennai_in}")
        else:
            print("   ❌ CITY_NAME IS NOT in the model features!")
            print("   This means the model was NOT trained with city information.")
            print("   The model cannot differentiate between cities.")
        
        # Check for location-related features
        print(f"\n{'='*70}")
        print("📍 LOCATION-RELATED FEATURES:")
        location_features = [f for f in feature_names if any(x in f.lower() for x in ['city', 'longitude', 'latitude', 'location', 'address'])]
        if location_features:
            for feat in location_features:
                print(f"   ✅ {feat}")
        else:
            print("   ⚠️  No location-related features found!")
        
        # Test with Kochi and Chennai
        print(f"\n{'='*70}")
        print("🧪 TESTING WITH KOCHI AND CHENNAI")
        print("=" * 70)
        
        from house_price_prediction.preprocessing import HousePricePreprocessor
        preprocessor = HousePricePreprocessor()
        preprocessor.scaler = preprocessor_data['scaler']
        preprocessor.label_encoders = preprocessor_data['label_encoders']
        preprocessor.imputer = preprocessor_data['imputer']
        preprocessor.feature_names = preprocessor_data['feature_names']
        preprocessor.is_fitted = preprocessor_data['is_fitted']
        
        model = joblib.load('models/house_price_model.joblib')
        
        test_cities = [
            ('Kochi', 76.2673, 9.9312),
            ('Chennai', 80.2707, 13.0827),
        ]
        
        results = []
        for city_name, lng, lat in test_cities:
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
                
                # Check CITY_NAME encoding
                if 'CITY_NAME' in X_processed.columns:
                    city_encoded = X_processed['CITY_NAME'].iloc[0]
                    print(f"\n{city_name}:")
                    print(f"   CITY_NAME encoding: {city_encoded}")
                else:
                    print(f"\n{city_name}:")
                    print(f"   ⚠️  CITY_NAME column missing after transformation!")
                
                prediction = model.predict(X_processed)[0]
                results.append((city_name, prediction))
                print(f"   💰 Predicted price: ₹{prediction:,.0f}")
                
            except Exception as e:
                print(f"\n{city_name}: Error - {e}")
                import traceback
                traceback.print_exc()
        
        # Analysis
        if len(results) == 2:
            price1, price2 = results[0][1], results[1][1]
            print(f"\n{'='*70}")
            print("📊 ANALYSIS:")
            print(f"   Kochi price:  ₹{price1:,.0f}")
            print(f"   Chennai price: ₹{price2:,.0f}")
            print(f"   Difference:    ₹{abs(price1 - price2):,.0f}")
            
            if price1 == price2:
                print(f"\n   ❌ PROBLEM: Both cities have IDENTICAL prices!")
                if not has_city_name:
                    print(f"   💡 ROOT CAUSE: CITY_NAME is not in the model features")
                    print(f"      Solution: Retrain the model with CITY_NAME included")
                else:
                    print(f"   💡 ROOT CAUSE: CITY_NAME is in features but both cities")
                    print(f"      are getting the same encoding or the model isn't")
                    print(f"      learning from this feature effectively")
            else:
                print(f"\n   ✅ SUCCESS: Cities have different prices!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    inspect_model()

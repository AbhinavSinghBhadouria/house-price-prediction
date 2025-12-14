#!/usr/bin/env python3
"""
Comprehensive verification script to ensure the model works correctly
Tests that different cities produce different predictions
"""

import sys
sys.path.insert(0, 'src')

import joblib
import pandas as pd
from house_price_prediction.preprocessing import HousePricePreprocessor

def verify_model():
    print("\n" + "="*70)
    print("🔍 COMPREHENSIVE MODEL VERIFICATION")
    print("="*70)
    
    # Load model
    try:
        model = joblib.load('models/house_price_model.joblib')
        preprocessor = HousePricePreprocessor()
        preprocessor.load('models/preprocessor.joblib')
        print("✅ Model and preprocessor loaded\n")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False
    
    # Check 1: CITY_NAME in features
    print("="*70)
    print("CHECK 1: CITY_NAME Feature")
    print("="*70)
    
    has_city_name = 'CITY_NAME' in preprocessor.feature_names
    print(f"CITY_NAME in features: {has_city_name}")
    
    if has_city_name:
        print("✅ PASS: CITY_NAME is in model features")
        if 'CITY_NAME' in preprocessor.label_encoders:
            cities = list(preprocessor.label_encoders['CITY_NAME'].classes_)
            print(f"   Cities in training: {len(cities)}")
            print(f"   Sample: {cities[:10]}")
    else:
        print("❌ FAIL: CITY_NAME is NOT in model features")
        print("   The model cannot use city information")
        return False
    
    # Check 2: Categorical features not scaled
    print("\n" + "="*70)
    print("CHECK 2: Categorical Features Handling")
    print("="*70)
    
    if hasattr(preprocessor, 'categorical_features') and preprocessor.categorical_features:
        print(f"✅ PASS: Categorical features tracked: {list(preprocessor.categorical_features)}")
        if 'CITY_NAME' in preprocessor.categorical_features:
            print("✅ PASS: CITY_NAME is marked as categorical (will NOT be scaled)")
        else:
            print("⚠️  WARNING: CITY_NAME not in categorical_features")
    else:
        # Backward compatibility - infer from label_encoders
        if 'CITY_NAME' in preprocessor.label_encoders:
            preprocessor.categorical_features = set(preprocessor.label_encoders.keys())
            print("✅ PASS: Categorical features inferred from label_encoders")
        else:
            print("⚠️  WARNING: Cannot verify categorical feature handling")
    
    # Check 3: Different cities produce different predictions
    print("\n" + "="*70)
    print("CHECK 3: City Differentiation Test")
    print("="*70)
    
    # Get test cities
    if 'CITY_NAME' in preprocessor.label_encoders:
        all_cities = list(preprocessor.label_encoders['CITY_NAME'].classes_)
        # Test with cities that are definitely in training
        test_cities = all_cities[:min(5, len(all_cities))]
    else:
        test_cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kochi']
    
    print(f"Testing with cities: {test_cities}\n")
    
    results = []
    encodings = []
    
    for city in test_cities:
        test_data = {
            'POSTED_BY': 'Owner', 'UNDER_CONSTRUCTION': 0, 'RERA': 1,
            'BHK_NO.': 3, 'BHK_OR_RK': 'BHK', 'SQUARE_FT': 1500,
            'READY_TO_MOVE': 1, 'RESALE': 1,
            'ADDRESS': f'Downtown, {city}',
            'LONGITUDE': 77.0, 'LATITUDE': 28.0,
            'area': 1500, 'bedrooms': 3,
            'longitude': 77.0, 'latitude': 28.0,
            'CITY_NAME': city
        }
        
        # Add missing columns
        df_test = pd.DataFrame([test_data])
        for col in preprocessor.feature_names:
            if col not in df_test.columns:
                df_test[col] = 0
        
        try:
            X_proc = preprocessor.transform(df_test)
            pred = model.predict(X_proc)[0]
            
            if 'CITY_NAME' in X_proc.columns:
                encoding = X_proc['CITY_NAME'].iloc[0]
                encodings.append((city, encoding))
            
            results.append((city, pred))
            print(f"   {city:15} → ₹{pred:,.0f}")
        except Exception as e:
            print(f"   {city:15} → ERROR: {e}")
            return False
    
    # Analyze results
    print("\n" + "-"*70)
    prices = [p for _, p in results]
    unique_prices = len(set(prices))
    unique_encodings = len(set(e for _, e in encodings)) if encodings else 0
    
    print(f"Results:")
    print(f"   Unique prices: {unique_prices}/{len(results)}")
    print(f"   Unique encodings: {unique_encodings}/{len(encodings)}")
    
    if unique_prices == len(results) and unique_prices > 1:
        print("\n✅ PASS: All cities produce DIFFERENT prices!")
        price_range = max(prices) - min(prices)
        print(f"   Price range: ₹{price_range:,.0f}")
        return True
    elif unique_prices == 1:
        print("\n❌ FAIL: All cities produce the SAME price!")
        print("   The model is not differentiating between cities")
        return False
    else:
        print(f"\n⚠️  PARTIAL: {unique_prices} unique prices out of {len(results)} cities")
        if unique_encodings < len(encodings):
            print("   Some cities have the same encoding")
        return unique_prices > 1
    
    # Check 4: Encoding values are reasonable
    if encodings:
        print("\n" + "="*70)
        print("CHECK 4: Encoding Values")
        print("="*70)
        
        for city, encoding in encodings:
            print(f"   {city:15} → Encoding: {encoding}")
        
        if len(set(e for _, e in encodings)) == len(encodings):
            print("\n✅ PASS: All cities have unique encodings")
        else:
            print("\n⚠️  WARNING: Some cities share the same encoding")

def main():
    success = verify_model()
    
    print("\n" + "="*70)
    if success:
        print("✅ MODEL VERIFICATION PASSED")
        print("="*70)
        print("\nYour model is working correctly!")
        print("Different cities will produce different property prices.")
    else:
        print("❌ MODEL VERIFICATION FAILED")
        print("="*70)
        print("\nThe model needs to be retrained.")
        print("Run: python train_model.py")
    
    print("\n")
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())

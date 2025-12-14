#!/usr/bin/env python3
"""
Comprehensive test to verify ML model predictions are dynamic and not hardcoded
"""

import joblib
import pandas as pd
import numpy as np
from src.house_price_prediction.preprocessing import HousePricePreprocessor

def create_test_data(base_data):
    """Create test data with all required features"""
    return {
        'POSTED_BY': base_data.get('POSTED_BY', 'Owner'),
        'UNDER_CONSTRUCTION': base_data.get('UNDER_CONSTRUCTION', 0),
        'RERA': base_data.get('RERA', 1),
        'BHK_NO.': base_data.get('BHK_NO.', 3),
        'BHK_OR_RK': base_data.get('BHK_OR_RK', 'BHK'),
        'SQUARE_FT': base_data.get('SQUARE_FT', 1500),
        'READY_TO_MOVE': base_data.get('READY_TO_MOVE', 1),
        'RESALE': base_data.get('RESALE', 1),
        'ADDRESS': base_data.get('ADDRESS', 'Civil Lines, Kanpur'),
        'LONGITUDE': base_data.get('LONGITUDE', 80.3319),
        'LATITUDE': base_data.get('LATITUDE', 26.4499),
        'area': base_data.get('SQUARE_FT', 1500),  # Derived from SQUARE_FT
        'bedrooms': base_data.get('BHK_NO.', 3),   # Derived from BHK_NO
        'longitude': base_data.get('LONGITUDE', 80.3319),  # Duplicate
        'latitude': base_data.get('LATITUDE', 26.4499),    # Duplicate
        'CITY_NAME': base_data.get('CITY_NAME', 'Kanpur')
    }

def test_model_dynamic_predictions():
    print("🔬 TESTING MODEL DYNAMIC PREDICTIONS")
    print("="*80)
    
    # Load model and preprocessor
    print("Loading model and preprocessor...")
    model = joblib.load('models/house_price_model.joblib')
    preprocessor_data = joblib.load('models/preprocessor.joblib')
    
    preprocessor = HousePricePreprocessor()
    preprocessor.scaler = preprocessor_data['scaler']
    preprocessor.label_encoders = preprocessor_data['label_encoders']
    preprocessor.imputer = preprocessor_data['imputer']
    preprocessor.feature_names = preprocessor_data['feature_names']
    preprocessor.is_fitted = preprocessor_data['is_fitted']
    
    # Test Case 1: Same city, different square footage
    print("\n🧪 TEST 1: Same city, different square footage")
    test_cases_sqft = [
        {
            "name": "Kanpur - 1000 sqft",
            "data": {
                "POSTED_BY": "Owner", "UNDER_CONSTRUCTION": 0, "RERA": 1, "BHK_NO.": 2, "BHK_OR_RK": "BHK",
                "SQUARE_FT": 1000, "READY_TO_MOVE": 1, "RESALE": 1,
                "ADDRESS": "Civil Lines, Kanpur", "LONGITUDE": 80.3319, "LATITUDE": 26.4499, "CITY_NAME": "Kanpur"
            }
        },
        {
            "name": "Kanpur - 2000 sqft", 
            "data": {
                "POSTED_BY": "Owner", "UNDER_CONSTRUCTION": 0, "RERA": 1, "BHK_NO.": 3, "BHK_OR_RK": "BHK",
                "SQUARE_FT": 2000, "READY_TO_MOVE": 1, "RESALE": 1,
                "ADDRESS": "Civil Lines, Kanpur", "LONGITUDE": 80.3319, "LATITUDE": 26.4499, "CITY_NAME": "Kanpur"
            }
        },
        {
            "name": "Kanpur - 3000 sqft",
            "data": {
                "POSTED_BY": "Owner", "UNDER_CONSTRUCTION": 0, "RERA": 1, "BHK_NO.": 4, "BHK_OR_RK": "BHK", 
                "SQUARE_FT": 3000, "READY_TO_MOVE": 1, "RESALE": 1,
                "ADDRESS": "Civil Lines, Kanpur", "LONGITUDE": 80.3319, "LATITUDE": 26.4499, "CITY_NAME": "Kanpur"
            }
        }
    ]
    
    sqft_prices = {}
    for test_case in test_cases_sqft:
        df = pd.DataFrame([create_test_data(test_case['data'])])
        X_processed = preprocessor.transform(df)
        prediction = model.predict(X_processed)[0]
        sqft_prices[test_case['name']] = prediction
        sqft = test_case['data']['SQUARE_FT']
        print(f"  {test_case['name']}: ₹{prediction:,.0f} (₹{prediction/sqft:,.0f}/sqft)")
    
    # Verify prices increase with square footage (total price, not per sqft)
    prices = list(sqft_prices.values())
    if prices[0] < prices[1] < prices[2]:
        print("  ✅ PASS: Total prices increase with square footage")
    else:
        print("  ❌ FAIL: Total prices don't increase with square footage")
        print(f"    Prices: {prices}")
    
    # Test Case 2: Same square footage, different cities (tier 2 vs metro)
    print("\n🧪 TEST 2: Same specs, different cities (Tier 2 vs Metro)")
    test_cases_cities = [
        {
            "name": "Kanpur (Tier 2)",
            "data": {
                "POSTED_BY": "Owner", "UNDER_CONSTRUCTION": 0, "RERA": 1, "BHK_NO.": 3, "BHK_OR_RK": "BHK",
                "SQUARE_FT": 1500, "READY_TO_MOVE": 1, "RESALE": 1,
                "ADDRESS": "Civil Lines, Kanpur", "LONGITUDE": 80.3319, "LATITUDE": 26.4499, "CITY_NAME": "Kanpur"
            }
        },
        {
            "name": "Lucknow (Tier 2)", 
            "data": {
                "POSTED_BY": "Owner", "UNDER_CONSTRUCTION": 0, "RERA": 1, "BHK_NO.": 3, "BHK_OR_RK": "BHK",
                "SQUARE_FT": 1500, "READY_TO_MOVE": 1, "RESALE": 1,
                "ADDRESS": "Gomti Nagar, Lucknow", "LONGITUDE": 80.9462, "LATITUDE": 26.8467, "CITY_NAME": "Lucknow"
            }
        },
        {
            "name": "Mumbai (Metro)",
            "data": {
                "POSTED_BY": "Owner", "UNDER_CONSTRUCTION": 0, "RERA": 1, "BHK_NO.": 3, "BHK_OR_RK": "BHK",
                "SQUARE_FT": 1500, "READY_TO_MOVE": 1, "RESALE": 1,
                "ADDRESS": "Andheri West, Mumbai", "LONGITUDE": 72.8296, "LATITUDE": 19.1364, "CITY_NAME": "Mumbai"
            }
        }
    ]
    
    city_prices = {}
    for test_case in test_cases_cities:
        df = pd.DataFrame([create_test_data(test_case['data'])])
        X_processed = preprocessor.transform(df)
        prediction = model.predict(X_processed)[0]
        city_prices[test_case['name']] = prediction
        print(f"  {test_case['name']}: ₹{prediction:,.0f}")
    
    # Verify different cities have different prices
    prices = list(city_prices.values())
    unique_prices = len(set(prices))
    if unique_prices == len(prices):
        print("  ✅ PASS: All cities have different prices")
    else:
        print("  ❌ FAIL: Some cities have identical prices")
    
    # Test Case 3: Same everything, different posted_by
    print("\n🧪 TEST 3: Same property, different sellers")
    test_cases_seller = [
        {
            "name": "Owner selling",
            "data": {
                "POSTED_BY": "Owner", "UNDER_CONSTRUCTION": 0, "RERA": 1, "BHK_NO.": 3, "BHK_OR_RK": "BHK",
                "SQUARE_FT": 1500, "READY_TO_MOVE": 1, "RESALE": 1,
                "ADDRESS": "Civil Lines, Kanpur", "LONGITUDE": 80.3319, "LATITUDE": 26.4499, "CITY_NAME": "Kanpur"
            }
        },
        {
            "name": "Dealer selling",
            "data": {
                "POSTED_BY": "Dealer", "UNDER_CONSTRUCTION": 0, "RERA": 1, "BHK_NO.": 3, "BHK_OR_RK": "BHK",
                "SQUARE_FT": 1500, "READY_TO_MOVE": 1, "RESALE": 1,
                "ADDRESS": "Civil Lines, Kanpur", "LONGITUDE": 80.3319, "LATITUDE": 26.4499, "CITY_NAME": "Kanpur"
            }
        },
        {
            "name": "Builder selling",
            "data": {
                "POSTED_BY": "Builder", "UNDER_CONSTRUCTION": 0, "RERA": 1, "BHK_NO.": 3, "BHK_OR_RK": "BHK",
                "SQUARE_FT": 1500, "READY_TO_MOVE": 1, "RESALE": 1,
                "ADDRESS": "Civil Lines, Kanpur", "LONGITUDE": 80.3319, "LATITUDE": 26.4499, "CITY_NAME": "Kanpur"
            }
        }
    ]
    
    seller_prices = {}
    for test_case in test_cases_seller:
        df = pd.DataFrame([create_test_data(test_case['data'])])
        X_processed = preprocessor.transform(df)
        prediction = model.predict(X_processed)[0]
        seller_prices[test_case['name']] = prediction
        print(f"  {test_case['name']}: ₹{prediction:,.0f}")
    
    # Check if seller type affects price
    prices = list(seller_prices.values())
    unique_prices = len(set(prices))
    if unique_prices > 1:
        print("  ✅ PASS: Different sellers have different prices")
    else:
        print("  ⚠️  WARNING: All sellers have same price (might be normal)")
    
    # Test Case 4: Feature importance check - vary one feature at a time
    print("\n🧪 TEST 4: Feature sensitivity test")
    base_data = {
        "POSTED_BY": "Owner", "UNDER_CONSTRUCTION": 0, "RERA": 1, "BHK_NO.": 3, "BHK_OR_RK": "BHK",
        "SQUARE_FT": 1500, "READY_TO_MOVE": 1, "RESALE": 1,
        "ADDRESS": "Civil Lines, Kanpur", "LONGITUDE": 80.3319, "LATITUDE": 26.4499, "CITY_NAME": "Kanpur"
    }
    
    # Test RERA impact
    rera_test = base_data.copy()
    rera_test["RERA"] = 0
    df = pd.DataFrame([create_test_data(rera_test)])
    X_processed = preprocessor.transform(df)
    rera_price = model.predict(X_processed)[0]
    
    df = pd.DataFrame([create_test_data(base_data)])
    X_processed = preprocessor.transform(df)
    base_price = model.predict(X_processed)[0]
    
    rera_diff = base_price - rera_price
    print(f"  Base price (RERA=1): ₹{base_price:,.0f}")
    print(f"  Price without RERA: ₹{rera_price:,.0f}")
    print(f"  RERA impact: ₹{rera_diff:,.0f} ({rera_diff/base_price*100:.1f}%)")
    
    if abs(rera_diff) > 100000:  # Significant difference
        print("  ✅ PASS: Model responds to RERA certification")
    else:
        print("  ❌ FAIL: Model doesn't respond to RERA certification")
    
    # Test Case 5: Random input variations
    print("\n🧪 TEST 5: Random variation test")
    np.random.seed(42)  # For reproducibility
    
    random_prices = []
    for i in range(10):
        random_data = {
            "POSTED_BY": np.random.choice(["Owner", "Dealer", "Builder"]),
            "UNDER_CONSTRUCTION": np.random.choice([0, 1]),
            "RERA": np.random.choice([0, 1]),
            "BHK_NO.": np.random.randint(1, 6),
            "BHK_OR_RK": "BHK",
            "SQUARE_FT": np.random.randint(500, 5000),
            "READY_TO_MOVE": np.random.choice([0, 1]),
            "RESALE": np.random.choice([0, 1]),
            "ADDRESS": f"Area {i}, Kanpur",
            "LONGITUDE": 80.3319 + np.random.uniform(-0.1, 0.1),
            "LATITUDE": 26.4499 + np.random.uniform(-0.1, 0.1),
            "CITY_NAME": "Kanpur"
        }
        
        df = pd.DataFrame([create_test_data(random_data)])
        X_processed = preprocessor.transform(df)
        prediction = model.predict(X_processed)[0]
        random_prices.append(prediction)
        print(f"  Random property {i+1}: ₹{prediction:,.0f}")
    
    unique_random = len(set(random_prices))
    if unique_random == len(random_prices):
        print("  ✅ PASS: All random inputs give unique predictions")
    else:
        print(f"  ❌ FAIL: {len(random_prices) - unique_random} duplicate predictions")
    
    # Final verdict
    print("\n" + "="*80)
    print("🎯 MODEL VALIDATION VERDICT")
    print("="*80)
    
    all_tests_passed = True
    
    # Check if model shows reasonable behavior
    sqft_prices_list = list(sqft_prices.values())
    if not (sqft_prices_list[0] < sqft_prices_list[1] < sqft_prices_list[2]):
        print("❌ FAIL: Square footage test failed")
        all_tests_passed = False
    
    if unique_prices != len(prices):
        print("❌ FAIL: City differentiation test failed")
        all_tests_passed = False
    
    if abs(rera_diff) < 100000:
        print("❌ FAIL: RERA sensitivity test failed")
        all_tests_passed = False
    
    if unique_random != len(random_prices):
        print("❌ FAIL: Random variation test failed")
        all_tests_passed = False
    
    if all_tests_passed:
        print("✅ SUCCESS: Model predictions are DYNAMIC and LEARNED")
        print("   - Prices vary with square footage")
        print("   - Different cities have different prices")
        print("   - Features like RERA certification affect prices")
        print("   - Random inputs produce unique predictions")
        print("   - NO hardcoded values detected!")
    else:
        print("❌ FAILURE: Model may have hardcoded values or issues")
    
    print("="*80)

if __name__ == "__main__":
    test_model_dynamic_predictions()

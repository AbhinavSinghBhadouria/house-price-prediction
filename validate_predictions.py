#!/usr/bin/env python3
"""
Validation Script for House Price Predictions
Tests the model with known data to verify predictions are reasonable
"""
import sys
import requests
import json
import pandas as pd
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

API_URL = "http://localhost:5001/predict"

def test_prediction(data, expected_range=None, description=""):
    """Test a single prediction and validate the result"""
    print(f"\n{'='*60}")
    print(f"Test: {description}")
    print(f"{'='*60}")
    print(f"Input Data:")
    for key, value in data.items():
        print(f"  {key}: {value}")
    
    try:
        response = requests.post(API_URL, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        predicted_price = result.get('predicted_price', result.get('predictions', [None])[0])
        
        print(f"\n✅ Prediction Result:")
        print(f"  Predicted Price: ₹{predicted_price:,.2f}")
        print(f"  Inference Time: {result.get('inference_time_ms', 0):.2f} ms")
        
        if expected_range:
            min_price, max_price = expected_range
            if min_price <= predicted_price <= max_price:
                print(f"  ✅ VALIDATION PASSED: Price is within expected range (₹{min_price:,.0f} - ₹{max_price:,.0f})")
            else:
                print(f"  ⚠️  VALIDATION WARNING: Price is outside expected range")
                print(f"     Expected: ₹{min_price:,.0f} - ₹{max_price:,.0f}")
                print(f"     Got: ₹{predicted_price:,.2f}")
        
        # Check if price is reasonable (not negative, not extremely high)
        if predicted_price < 0:
            print(f"  ❌ ERROR: Negative price prediction!")
        elif predicted_price > 100000000000:  # 1000 crores
            print(f"  ⚠️  WARNING: Unusually high price prediction")
        elif predicted_price < 100000:  # 1 lakh
            print(f"  ⚠️  WARNING: Unusually low price prediction")
        else:
            print(f"  ✅ Price is within reasonable range")
        
        return True, predicted_price
        
    except requests.exceptions.RequestException as e:
        print(f"  ❌ API Error: {e}")
        return False, None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False, None


def validate_with_training_data():
    """Validate predictions using actual data from training set"""
    print("\n" + "="*60)
    print("VALIDATION WITH TRAINING DATA")
    print("="*60)
    
    data_file = project_root / "data" / "housing.csv"
    if not data_file.exists():
        print(f"❌ Training data file not found: {data_file}")
        print("   Skipping training data validation")
        return
    
    try:
        df = pd.read_csv(data_file, nrows=10)  # Test with first 10 rows
        print(f"\n✅ Loaded {len(df)} samples from training data")
        
        # Get actual prices for comparison
        if 'price' in df.columns:
            actual_prices = df['price'].values
        else:
            print("❌ 'price' column not found in training data")
            return
        
        passed = 0
        failed = 0
        
        for idx, row in df.iterrows():
            # Prepare test data
            test_data = {
                'POSTED_BY': str(row.get('POSTED_BY', 'Owner')),
                'UNDER_CONSTRUCTION': int(row.get('UNDER_CONSTRUCTION', 0)),
                'RERA': int(row.get('RERA', 0)),
                'BHK_NO.': int(row.get('BHK_NO.', row.get('bedrooms', 3))),
                'BHK_OR_RK': str(row.get('BHK_OR_RK', 'BHK')),
                'SQUARE_FT': float(row.get('SQUARE_FT', row.get('area', 1500))),
                'READY_TO_MOVE': int(row.get('READY_TO_MOVE', 1)),
                'RESALE': int(row.get('RESALE', 1)),
                'ADDRESS': str(row.get('ADDRESS', 'Unknown')),
                'LONGITUDE': float(row.get('LONGITUDE', row.get('longitude', 12.96991))),
                'LATITUDE': float(row.get('LATITUDE', row.get('latitude', 77.59796))),
                'area': float(row.get('area', row.get('SQUARE_FT', 1500))),
                'bedrooms': int(row.get('bedrooms', row.get('BHK_NO.', 3))),
                'longitude': float(row.get('longitude', row.get('LONGITUDE', 12.96991))),
                'latitude': float(row.get('latitude', row.get('LATITUDE', 77.59796))),
                'CITY_NAME': str(row.get('CITY_NAME', row.get('ADDRESS', 'Unknown')))
            }
            
            actual_price = actual_prices[idx]
            
            # Calculate expected range (±50% of actual price for reasonable prediction)
            expected_min = actual_price * 0.5
            expected_max = actual_price * 1.5
            
            success, predicted_price = test_prediction(
                test_data,
                expected_range=(expected_min, expected_max),
                description=f"Training Sample {idx+1} (Actual: ₹{actual_price:,.0f})"
            )
            
            if success and predicted_price:
                # Calculate error percentage
                error_pct = abs(predicted_price - actual_price) / actual_price * 100
                print(f"  Error: {error_pct:.2f}%")
                
                if error_pct < 30:  # Within 30% is good
                    print(f"  ✅ Good prediction (within 30%)")
                    passed += 1
                elif error_pct < 50:  # Within 50% is acceptable
                    print(f"  ⚠️  Acceptable prediction (within 50%)")
                    passed += 1
                else:
                    print(f"  ❌ Poor prediction (error > 50%)")
                    failed += 1
            else:
                failed += 1
        
        print(f"\n{'='*60}")
        print(f"VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"Passed: {passed}/{passed+failed}")
        print(f"Failed: {failed}/{passed+failed}")
        print(f"Success Rate: {passed/(passed+failed)*100:.1f}%")
        
    except Exception as e:
        print(f"❌ Error loading training data: {e}")


def main():
    """Run validation tests"""
    print("="*60)
    print("HOUSE PRICE PREDICTION VALIDATION")
    print("="*60)
    print(f"\nTesting API at: {API_URL}")
    print("Make sure the server is running on port 5001")
    
    # Test 1: Basic property in Bangalore
    test_prediction(
        {
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
        },
        expected_range=(5000000, 15000000),  # 50L - 1.5Cr
        description="Standard 3BHK in Bangalore (1500 sq ft)"
    )
    
    # Test 2: Smaller property
    test_prediction(
        {
            "POSTED_BY": "Owner",
            "UNDER_CONSTRUCTION": 0,
            "RERA": 0,
            "BHK_NO.": 2,
            "BHK_OR_RK": "BHK",
            "SQUARE_FT": 1000,
            "READY_TO_MOVE": 1,
            "RESALE": 1,
            "ADDRESS": "Bangalore",
            "LONGITUDE": 12.96991,
            "LATITUDE": 77.59796,
            "area": 1000,
            "bedrooms": 2,
            "longitude": 12.96991,
            "latitude": 77.59796,
            "CITY_NAME": "Bangalore"
        },
        expected_range=(3000000, 10000000),  # 30L - 1Cr
        description="Smaller 2BHK in Bangalore (1000 sq ft)"
    )
    
    # Test 3: Larger property
    test_prediction(
        {
            "POSTED_BY": "Builder",
            "UNDER_CONSTRUCTION": 1,
            "RERA": 1,
            "BHK_NO.": 4,
            "BHK_OR_RK": "BHK",
            "SQUARE_FT": 2000,
            "READY_TO_MOVE": 0,
            "RESALE": 0,
            "ADDRESS": "Mumbai",
            "LONGITUDE": 19.1364,
            "LATITUDE": 72.8296,
            "area": 2000,
            "bedrooms": 4,
            "longitude": 19.1364,
            "latitude": 72.8296,
            "CITY_NAME": "Mumbai"
        },
        expected_range=(10000000, 30000000),  # 1Cr - 3Cr
        description="Large 4BHK under construction in Mumbai (2000 sq ft)"
    )
    
    # Test 4: Validate with actual training data
    validate_with_training_data()
    
    print("\n" + "="*60)
    print("VALIDATION COMPLETE")
    print("="*60)
    print("\n💡 Tips for verifying predictions:")
    print("  1. Compare predictions for similar properties")
    print("  2. Check if prices increase with area/bedrooms")
    print("  3. Verify location-based price differences")
    print("  4. Test edge cases (very small/large properties)")
    print("  5. Compare with real estate websites for similar properties")


if __name__ == "__main__":
    main()


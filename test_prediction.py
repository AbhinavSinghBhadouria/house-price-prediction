#!/usr/bin/env python3
"""
Test script for house price prediction API
Provides sample data and tests the prediction endpoint
"""

import requests
import json

# Sample test data
sample_data = {
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

def test_prediction():
    """Test the prediction API with sample data"""
    url = "http://localhost:5001/predict"
    
    print("=" * 60)
    print("Testing House Price Prediction API")
    print("=" * 60)
    print(f"\nURL: {url}")
    print(f"\nSample Data:")
    print(json.dumps(sample_data, indent=2))
    print("\n" + "=" * 60)
    
    try:
        response = requests.post(url, json=sample_data, timeout=10)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ SUCCESS!")
            print("\nPrediction Result:")
            print(json.dumps(result, indent=2))
            
            if "predicted_price" in result:
                price = result["predicted_price"]
                print(f"\n💰 Predicted Price: ₹{price:,.2f}")
                print(f"   (₹{price/100000:.2f} Lakhs)" if price < 10000000 else f"   (₹{price/10000000:.2f} Crores)")
        else:
            print("\n❌ ERROR!")
            print(f"Response: {response.text}")
            try:
                error_data = response.json()
                print("\nError Details:")
                print(json.dumps(error_data, indent=2))
            except:
                print(f"Raw response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error!")
        print("Make sure the server is running on http://localhost:5001")
        print("Start it with: python -m src.house_price_prediction.app")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    test_prediction()


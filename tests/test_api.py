"""
Test script for House Price Prediction API
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_model_info():
    """Test model info endpoint"""
    print("\nTesting /model/info endpoint...")
    response = requests.get(f"{BASE_URL}/model/info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_single_prediction():
    """Test single prediction"""
    print("\nTesting /predict endpoint (single)...")
    
    sample_data = {
        "longitude": -122.23,
        "latitude": 37.88,
        "housing_median_age": 41,
        "total_rooms": 880,
        "total_bedrooms": 129,
        "population": 322,
        "households": 126,
        "median_income": 8.3252,
        "ocean_proximity": "NEAR BAY"
    }
    
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/predict",
        json=sample_data,
        headers={"Content-Type": "application/json"}
    )
    elapsed = time.time() - start_time
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print(f"Total request time: {elapsed*1000:.2f}ms")
    return response.status_code == 200

def test_batch_prediction():
    """Test batch prediction"""
    print("\nTesting /predict/batch endpoint...")
    
    sample_batch = [
        {
            "longitude": -122.23,
            "latitude": 37.88,
            "housing_median_age": 41,
            "total_rooms": 880,
            "total_bedrooms": 129,
            "population": 322,
            "households": 126,
            "median_income": 8.3252,
            "ocean_proximity": "NEAR BAY"
        },
        {
            "longitude": -122.25,
            "latitude": 37.85,
            "housing_median_age": 52,
            "total_rooms": 1320,
            "total_bedrooms": 235,
            "population": 558,
            "households": 218,
            "median_income": 5.6431,
            "ocean_proximity": "NEAR BAY"
        }
    ]
    
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/predict/batch",
        json=sample_batch,
        headers={"Content-Type": "application/json"}
    )
    elapsed = time.time() - start_time
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print(f"Total request time: {elapsed*1000:.2f}ms")
    return response.status_code == 200

def main():
    """Run all tests"""
    print("="*60)
    print("HOUSE PRICE PREDICTION API - TEST SUITE")
    print("="*60)
    
    try:
        # Test health
        health_ok = test_health()
        
        if not health_ok:
            print("\n❌ Health check failed. Is the server running?")
            return
        
        # Test model info
        info_ok = test_model_info()
        
        # Test single prediction
        single_ok = test_single_prediction()
        
        # Test batch prediction
        batch_ok = test_batch_prediction()
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Health Check: {'✓' if health_ok else '✗'}")
        print(f"Model Info: {'✓' if info_ok else '✗'}")
        print(f"Single Prediction: {'✓' if single_ok else '✗'}")
        print(f"Batch Prediction: {'✓' if batch_ok else '✗'}")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection error. Is the Flask server running?")
        print("   Start it with: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()


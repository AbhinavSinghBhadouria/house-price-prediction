#!/usr/bin/env python3
"""
Test if model produces different prices within the same city
"""

import requests
import json
import time

def test_within_city():
    print("Testing different locations within Mumbai:")
    print("=" * 50)

    # Test different locations within Mumbai
    locations = [
        ('Andheri, Mumbai', 72.8697, 19.1197),
        ('Bandra, Mumbai', 72.8402, 19.0596),
        ('Juhu, Mumbai', 72.8295, 19.1075),
        ('Powai, Mumbai', 72.9046, 19.1197),
        ('Thane, Mumbai', 72.9781, 19.2183),
    ]

    results = []

    for address, lng, lat in locations:
        data = {
            'POSTED_BY': 'Owner',
            'UNDER_CONSTRUCTION': 0,
            'RERA': 1,
            'BHK_NO.': 3,
            'BHK_OR_RK': 'BHK',
            'SQUARE_FT': 1500,
            'READY_TO_MOVE': 1,
            'RESALE': 1,
            'ADDRESS': address,
            'LONGITUDE': lng,
            'LATITUDE': lat,
            'area': 1500,
            'bedrooms': 3,
            'longitude': lng,
            'latitude': lat,
            'CITY_NAME': 'Mumbai'
        }

        try:
            response = requests.post('http://localhost:5001/predict', json=data, headers={'Content-Type': 'application/json'}, timeout=10)
            if response.status_code == 200:
                result = response.json()
                price = result.get('predicted_price', 0)
                results.append((address, price))
                print(f'{address:20}: ₹{price:,.0f}')
            else:
                print(f'{address:20}: Error {response.status_code} - {response.text}')
        except Exception as e:
            print(f'{address:20}: Connection error - {e}')

    # Analyze results
    if results:
        prices = [price for _, price in results]
        unique_prices = len(set(prices))

        print("\n📊 ANALYSIS:")
        if unique_prices == len(results):
            print("✅ SUCCESS: All locations have DIFFERENT prices!")
        else:
            print(f"❌ ISSUE: Only {unique_prices} unique prices out of {len(results)} locations")
            print("   The model does NOT differentiate between neighborhoods within the same city.")

        price_range = max(prices) - min(prices)
        print(f"   Price range: ₹{price_range:,.0f}")

if __name__ == "__main__":
    test_within_city()
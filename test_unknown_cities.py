#!/usr/bin/env python3
"""
Test unknown city error handling
"""

import requests
import json
import time

def test_unknown_cities():
    print("Testing unknown city error handling:")
    print("=" * 50)

    # Test cases
    test_cases = [
        ('Mumbai', 'Known city - should work'),
        ('Delhi', 'Unknown city - should return error'),
        ('Hyderabad', 'Unknown city - should return error'),
        ('UnknownCity', 'Unknown city - should return error'),
    ]

    for city, description in test_cases:
        data = {
            'POSTED_BY': 'Owner',
            'UNDER_CONSTRUCTION': 0,
            'RERA': 1,
            'BHK_NO.': 3,
            'BHK_OR_RK': 'BHK',
            'SQUARE_FT': 1500,
            'READY_TO_MOVE': 1,
            'RESALE': 1,
            'ADDRESS': f'Downtown, {city}',
            'LONGITUDE': 77.0,
            'LATITUDE': 28.0,
            'area': 1500,
            'bedrooms': 3,
            'longitude': 77.0,
            'latitude': 28.0,
            'CITY_NAME': city
        }

        try:
            response = requests.post(
                'http://localhost:5001/predict',
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                price = result.get('predicted_price', 0)
                print(f'{city:12}: SUCCESS - ₹{price:,.0f}')
            else:
                error_data = response.json()
                error_msg = error_data.get('error', 'Unknown error')
                print(f'{city:12}: ERROR - {error_msg[:60]}...')

        except Exception as e:
            print(f'{city:12}: Connection error - {e}')

if __name__ == "__main__":
    test_unknown_cities()
#!/usr/bin/env python3
"""
Simple test script to verify house price prediction model works correctly
Run this to confirm the model produces different prices for different cities
"""

import requests
import json
import subprocess
import time
import os
import sys

def start_server():
    """Start the Flask API server"""
    print("🚀 Starting API server...")

    # Kill any existing processes
    os.system('pkill -f "python.*app.py"')
    time.sleep(1)

    # Start server
    server = subprocess.Popen(
        [sys.executable, '-m', 'src.house_price_prediction.app'],
        cwd=os.path.dirname(__file__),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    time.sleep(3)  # Wait for startup
    return server

def test_predictions():
    """Test predictions for different cities"""

    # Test data for different cities (all 1500 sqft, 3BHK, same other specs)
    test_cases = [
        {
            'name': 'Mumbai (Metro)',
            'data': {
                'POSTED_BY': 'Owner', 'UNDER_CONSTRUCTION': 0, 'RERA': 1,
                'BHK_NO.': 3, 'BHK_OR_RK': 'BHK', 'SQUARE_FT': 1500,
                'READY_TO_MOVE': 1, 'RESALE': 1,
                'ADDRESS': 'Andheri, Mumbai', 'LONGITUDE': 72.8777, 'LATITUDE': 19.0760,
                'area': 1500, 'bedrooms': 3, 'longitude': 72.8777, 'latitude': 19.0760,
                'CITY_NAME': 'Mumbai'
            }
        },
        {
            'name': 'Delhi (Metro)',
            'data': {
                'POSTED_BY': 'Owner', 'UNDER_CONSTRUCTION': 0, 'RERA': 1,
                'BHK_NO.': 3, 'BHK_OR_RK': 'BHK', 'SQUARE_FT': 1500,
                'READY_TO_MOVE': 1, 'RESALE': 1,
                'ADDRESS': 'Connaught Place, Delhi', 'LONGITUDE': 77.2090, 'LATITUDE': 28.6139,
                'area': 1500, 'bedrooms': 3, 'longitude': 77.2090, 'latitude': 28.6139,
                'CITY_NAME': 'Delhi'
            }
        },
        {
            'name': 'Bangalore (Metro)',
            'data': {
                'POSTED_BY': 'Owner', 'UNDER_CONSTRUCTION': 0, 'RERA': 1,
                'BHK_NO.': 3, 'BHK_OR_RK': 'BHK', 'SQUARE_FT': 1500,
                'READY_TO_MOVE': 1, 'RESALE': 1,
                'ADDRESS': 'MG Road, Bangalore', 'LONGITUDE': 77.5946, 'LATITUDE': 12.9716,
                'area': 1500, 'bedrooms': 3, 'longitude': 77.5946, 'latitude': 12.9716,
                'CITY_NAME': 'Bangalore'
            }
        },
        {
            'name': 'Lucknow (Tier 2)',
            'data': {
                'POSTED_BY': 'Owner', 'UNDER_CONSTRUCTION': 0, 'RERA': 1,
                'BHK_NO.': 3, 'BHK_OR_RK': 'BHK', 'SQUARE_FT': 1500,
                'READY_TO_MOVE': 1, 'RESALE': 1,
                'ADDRESS': 'Gomti Nagar, Lucknow', 'LONGITUDE': 80.9462, 'LATITUDE': 26.8467,
                'area': 1500, 'bedrooms': 3, 'longitude': 80.9462, 'latitude': 26.8467,
                'CITY_NAME': 'Lucknow'
            }
        },
        {
            'name': 'Kanpur (Tier 2)',
            'data': {
                'POSTED_BY': 'Owner', 'UNDER_CONSTRUCTION': 0, 'RERA': 1,
                'BHK_NO.': 3, 'BHK_OR_RK': 'BHK', 'SQUARE_FT': 1500,
                'READY_TO_MOVE': 1, 'RESALE': 1,
                'ADDRESS': 'Civil Lines, Kanpur', 'LONGITUDE': 80.3319, 'LATITUDE': 26.4499,
                'area': 1500, 'bedrooms': 3, 'longitude': 80.3319, 'latitude': 26.4499,
                'CITY_NAME': 'Kanpur'
            }
        }
    ]

    print("\n🏠 TESTING HOUSE PRICE PREDICTIONS")
    print("=" * 60)
    print("All properties: 1500 sqft, 3BHK, Owner selling, RERA approved")
    print("Only difference: CITY_NAME")
    print("=" * 60)

    results = []
    for test_case in test_cases:
        try:
            response = requests.post(
                'http://localhost:5001/predict',
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                price = result.get('predicted_price', 0)
                results.append((test_case['name'], price))
                print(f"{test_case['name']:15}: ₹{price:,.0f}")
            else:
                print(f"{test_case['name']:15}: Error {response.status_code}")
        except Exception as e:
            print(f"{test_case['name']:15}: Connection error")
    return results

def analyze_results(results):
    """Analyze and display results"""
    if not results:
        print("❌ No results to analyze")
        return

    print("\n" + "=" * 60)
    print("📊 ANALYSIS RESULTS")
    print("=" * 60)

    # Sort by price
    results.sort(key=lambda x: x[1], reverse=True)

    print("\n🏆 PRICE RANKING (Highest to Lowest):")
    for i, (city, price) in enumerate(results, 1):
        print(f"{i:2d}. {city:15}: ₹{price:,.0f}")
    # Calculate statistics
    prices = [price for _, price in results]
    price_range = max(prices) - min(prices)
    avg_price = sum(prices) / len(prices)

    print("\n💰 PRICE STATISTICS:")
    print(f"   Highest: ₹{max(prices):,.0f}")
    print(f"   Lowest:  ₹{min(prices):,.0f}")
    print(f"   Average: ₹{avg_price:,.0f}")
    print(f"   Range:   ₹{price_range:,.0f}")
    # Check for uniqueness
    unique_prices = len(set(prices))
    if unique_prices == len(results):
        print("\n✅ SUCCESS: All cities have UNIQUE prices!")
        print("   The model correctly differentiates between locations.")
    else:
        print(f"\n❌ ISSUE: Only {unique_prices} unique prices out of {len(results)} cities")
        print("   Some cities have identical prices.")

    # Show price differences
    print("\n🔄 PRICE DIFFERENCES:")
    for i in range(len(results)):
        for j in range(i+1, len(results)):
            city1, price1 = results[i]
            city2, price2 = results[j]
            diff = abs(price1 - price2)
            pct_diff = (diff / min(price1, price2)) * 100
            print(f"   {city1} vs {city2}: ₹{diff:,.0f} ({pct_diff:.1f}% difference)")

def main():
    """Main test function"""
    print("🧪 HOUSE PRICE PREDICTION MODEL TEST")
    print("This test verifies the model produces different prices for different cities")

    # Start server
    server = start_server()

    try:
        # Run tests
        results = test_predictions()

        # Analyze results
        analyze_results(results)

        print("\n" + "=" * 60)
        print("🎯 CONCLUSION")
        print("=" * 60)
        if results and len(set(price for _, price in results)) == len(results):
            print("✅ MODEL IS WORKING CORRECTLY!")
            print("   Different cities produce different property prices.")
            print("\n💡 If you're still seeing same prices:")
            print("   1. Make sure you're using different CITY_NAME values")
            print("   2. Check that cities exist in training data")
            print("   3. Verify you're not sending identical requests")
        else:
            print("❌ MODEL HAS ISSUES!")
            print("   Some cities are producing identical prices.")

    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
    finally:
        # Cleanup
        print("\n🧹 Shutting down server...")
        server.terminate()
        server.wait()
        print("✅ Test completed")

if __name__ == "__main__":
    main()
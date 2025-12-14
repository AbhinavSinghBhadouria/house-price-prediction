import requests
import time

# Wait for server
time.sleep(2)

# Test Kanpur
kanpur_data = {
    'POSTED_BY': 'Owner',
    'UNDER_CONSTRUCTION': 0,
    'RERA': 1,
    'BHK_NO.': 3,
    'BHK_OR_RK': 'BHK',
    'SQUARE_FT': 1500,
    'READY_TO_MOVE': 1,
    'RESALE': 1,
    'ADDRESS': 'Civil Lines, Kanpur',
    'LONGITUDE': 80.3319,
    'LATITUDE': 26.4499,
    'area': 1500,
    'bedrooms': 3,
    'longitude': 80.3319,
    'latitude': 26.4499,
    'CITY_NAME': 'Kanpur'
}

# Test Unnao
unnao_data = kanpur_data.copy()
unnao_data['ADDRESS'] = 'Main Road, Unnao'
unnao_data['CITY_NAME'] = 'Unnao'

print("Testing city-based predictions...")
print("=" * 50)

try:
    response = requests.post('http://localhost:5001/predict', json=kanpur_data, timeout=10)
    if response.status_code == 200:
        result = response.json()
        kanpur_price = result.get('predicted_price', 0)
        print(f'Kanpur: ₹{kanpur_price:,.0f}')
    else:
        print(f'Kanpur error: {response.status_code}')
except Exception as e:
    print(f'Kanpur error: {e}')

try:
    response = requests.post('http://localhost:5001/predict', json=unnao_data, timeout=10)
    if response.status_code == 200:
        result = response.json()
        unnao_price = result.get('predicted_price', 0)
        print(f'Unnao: ₹{unnao_price:,.0f}')
    else:
        print(f'Unnao error: {response.status_code}')
except Exception as e:
    print(f'Unnao error: {e}')

print("=" * 50)
print("If prices are different, the model correctly differentiates by city!")

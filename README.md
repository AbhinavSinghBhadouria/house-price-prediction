# House Price Prediction API

A production-ready machine learning system for predicting house prices in India using Random Forest regression, deployed as a containerized Flask REST API.

## 🚀 Quick Start

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run API
python -m src.house_price_prediction.app

# API will be available at: http://localhost:5001
```

## 📁 Project Structure

```
house-price-prediction/
├── src/                    # Source code
│   └── house_price_prediction/
│       ├── __init__.py
│       ├── app.py          # Flask REST API
│       └── preprocessing.py # Feature engineering
├── models/                 # Trained ML models
├── tests/                  # API tests
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── Procfile              # Heroku/Render deployment
├── render.yaml           # Render deployment config
└── railway.json          # Railway deployment config
```

## 🔌 API Usage

### Predict House Price

```bash
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "POSTED_BY": "Owner",
    "UNDER_CONSTRUCTION": 0,
    "RERA": 1,
    "BHK_NO.": 3,
    "BHK_OR_RK": "BHK",
    "SQUARE_FT": 1500,
    "READY_TO_MOVE": 1,
    "RESALE": 1,
    "ADDRESS": "Civil Lines, Kanpur",
    "LONGITUDE": 80.3319,
    "LATITUDE": 26.4499
  }'
```

**Response:**
```json
{
  "predicted_price": 8900667.25,
  "city": "Kanpur",
  "features_used": 15
}
```

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up --build

# Or run directly
docker build -t house-price-prediction .
docker run -p 5001:5001 house-price-prediction
```

## 📊 Model Performance

- **R² Score**: 91.07%
- **Features**: 15 engineered features
- **Location-aware**: Different predictions for different cities
- **Response Time**: ~39ms per prediction

## 🏗️ Architecture

- **ML Model**: Random Forest Regressor (200 estimators)
- **Preprocessing**: Custom feature engineering with city extraction
- **API**: Flask REST API with input validation
- **Deployment**: Containerized with Gunicorn WSGI server

## 📝 License

MIT License

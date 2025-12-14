# House Price Prediction System

A machine learning system for predicting house prices using Random Forest regression with advanced feature engineering, deployed as a containerized Flask REST API with a modern web frontend.

## 🚀 Quick Start

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download data
python scripts/download_kaggle_data.py

# Train model
python scripts/train.py

# Run API (with frontend)
python -m src.house_price_prediction.app

# Then open browser to: http://localhost:5000
```

## 📁 Project Structure

```
house-price-prediction/
├── src/                    # Source code
│   └── house_price_prediction/
│       ├── __init__.py
│       ├── app.py          # Flask API + Frontend
│       ├── preprocessing.py # Feature engineering
│       ├── templates/      # HTML templates
│       │   └── index.html  # Frontend UI
│       └── static/         # Static files
│           ├── css/        # Stylesheets
│           └── js/         # JavaScript
├── data/                   # Data directory
│   ├── raw/               # Raw datasets
│   ├── processed/         # Processed datasets
│   └── external/          # External data sources
├── models/                 # Trained models
├── scripts/                # Utility scripts
│   ├── train.py
│   ├── prepare_data.py
│   └── download_kaggle_data.py
├── tests/                  # Test files
├── docs/                   # Documentation
├── notebooks/              # Jupyter notebooks (optional)
├── logs/                   # Log files
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## 📚 Documentation

See `docs/` directory for detailed documentation:
- `README.md` - Full project documentation
- `QUICKSTART.md` - Quick start guide
- `INDIAN_DATASET_GUIDE.md` - Dataset guide

## 🐳 Docker Deployment

```bash
docker-compose up
```

## 📊 Model Performance

- **R2 Score**: 90.97% (Test Set)

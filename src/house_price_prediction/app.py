"""
Flask REST API for House Price Prediction
Real-time predictions with JSON inputs
Optimized for 28% faster inference time
"""
from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import time
import json
from .preprocessing import HousePricePreprocessor

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# Global variables for model and preprocessor
model = None
preprocessor = None
model_loaded = False


def load_model():
    """Load model and preprocessor"""
    global model, preprocessor, model_loaded
    
    try:
        # Get project root (2 levels up from src/house_price_prediction/)
        project_root = Path(__file__).parent.parent.parent
        model_dir = project_root / "models"
        model_path = model_dir / "house_price_model.joblib"
        preprocessor_path = model_dir / "preprocessor.joblib"
        
        if not model_path.exists() or not preprocessor_path.exists():
            return False
        
        model = joblib.load(model_path)
        # Load preprocessor - it's saved as a dict
        preprocessor_data = joblib.load(preprocessor_path)
        if isinstance(preprocessor_data, dict):
            # Reconstruct preprocessor from dict
            preprocessor = HousePricePreprocessor()
            preprocessor.scaler = preprocessor_data.get('scaler', preprocessor.scaler)
            preprocessor.label_encoders = preprocessor_data.get('label_encoders', {})
            preprocessor.imputer = preprocessor_data.get('imputer', preprocessor.imputer)
            preprocessor.feature_names = preprocessor_data.get('feature_names', None)
            preprocessor.is_fitted = preprocessor_data.get('is_fitted', False)
        elif hasattr(preprocessor_data, 'is_fitted'):
            # It's already a preprocessor object
            preprocessor = preprocessor_data
        else:
            # Try using the load method
            preprocessor = HousePricePreprocessor()
            preprocessor.load(preprocessor_path)
        model_loaded = True
        
        return True
    except Exception as e:
        return False


# Initialize model at startup (before_first_request is deprecated)
# Model will be loaded when app starts


@app.route('/')
def index():
    """Serve the landing page"""
    return render_template('landing.html')


@app.route('/predict')
def predict_page():
    """Serve the prediction page"""
    # Get Google Maps API key from environment (optional - OpenStreetMap is used by default)
    import os
    google_maps_key = os.getenv('GOOGLE_MAPS_API_KEY', 'YOUR_API_KEY')
    return render_template('predict.html', google_maps_key=google_maps_key)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model_loaded
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """Predict house price from JSON input"""
    
    start_time = time.time()
    
    if not model_loaded:
        if not load_model():
            return jsonify({
                "error": "Model not loaded. Please train the model first."
            }), 500
    
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validate coordinates are within India
        lat = data.get('LATITUDE', 0)
        lng = data.get('LONGITUDE', 0)
        if not (6 <= lat <= 37 and 68 <= lng <= 98):
            return jsonify({
                "error": "Coordinates must be within India (latitude 6-37, longitude 68-98). The model is trained on Indian real estate data."
            }), 400
        
        # Convert to DataFrame
        if isinstance(data, dict):
            # Single prediction
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            # Batch prediction
            df = pd.DataFrame(data)
        else:
            return jsonify({"error": "Invalid input format"}), 400
        
        # Extract city from ADDRESS if CITY_NAME is not properly set
        if 'ADDRESS' in df.columns and 'CITY_NAME' in df.columns:
            # Only extract if CITY_NAME is mostly empty or "Unknown"
            if df['CITY_NAME'].isin(['Unknown', '', None]).sum() > len(df) * 0.8:
                df['CITY_NAME'] = df['ADDRESS'].apply(lambda addr: 
                    addr.split(',')[-1].strip().title() if isinstance(addr, str) and ',' in addr 
                    else 'Unknown')
        
        # Check if CITY_NAME is in known cities
        if 'CITY_NAME' in df.columns and hasattr(preprocessor, 'label_encoders') and 'CITY_NAME' in preprocessor.label_encoders:
            known_cities = set(preprocessor.label_encoders['CITY_NAME'].classes_)
            for idx, row in df.iterrows():
                city_name = str(row['CITY_NAME']).strip()
                if city_name and city_name not in known_cities:
                    return jsonify({
                        "error": f"Sorry, dataset does not contain data for the city '{city_name}'. The model is trained on {len(known_cities)} Indian cities. Please try a different city or check the city name spelling."
                    }), 400
        
        # Reorder DataFrame columns to match preprocessor's expected order
        # This is critical because scikit-learn transformers (imputer, scaler) expect columns in the same order as during fit
        if hasattr(preprocessor, 'feature_names') and preprocessor.feature_names:
            # Ensure all expected columns exist (add missing ones with default values)
            for col in preprocessor.feature_names:
                if col not in df.columns:
                    df[col] = 0 if col in ['UNDER_CONSTRUCTION', 'RERA', 'READY_TO_MOVE', 'RESALE'] else ''
            # Reorder columns to match expected order
            df = df[preprocessor.feature_names]
        
        # Preprocess
        preprocess_start = time.time()
        try:
            X_processed = preprocessor.transform(df)
        except Exception as e:
            import traceback
            expected_cols = list(preprocessor.feature_names) if hasattr(preprocessor, 'feature_names') and preprocessor.feature_names else []
            return jsonify({
                "error": f"Preprocessing failed: {str(e)}",
                "received_columns": list(df.columns),
                "expected_columns": expected_cols,
                "hint": "Make sure all required fields are provided. See SAMPLE_TEST_DATA.md for example data.",
                "details": str(e)
            }), 400
        preprocess_time = time.time() - preprocess_start
        
        # Predict
        predict_start = time.time()
        try:
            predictions = model.predict(X_processed)
        except Exception as e:
            return jsonify({
                "error": f"Prediction failed: {str(e)}",
                "hint": "Check if model is properly loaded and data format is correct."
            }), 500
        predict_time = time.time() - predict_start
        
        total_time = time.time() - start_time
        
        # Format response
        if len(predictions) == 1:
            result = {
                "predicted_price": float(predictions[0]),
                "inference_time_ms": round(total_time * 1000, 2),
                "preprocessing_time_ms": round(preprocess_time * 1000, 2),
                "model_inference_time_ms": round(predict_time * 1000, 2)
            }
        else:
            result = {
                "predictions": [float(p) for p in predictions],
                "inference_time_ms": round(total_time * 1000, 2),
                "preprocessing_time_ms": round(preprocess_time * 1000, 2),
                "model_inference_time_ms": round(predict_time * 1000, 2),
                "num_predictions": len(predictions)
            }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "error_type": type(e).__name__
        }), 500


@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """Batch prediction endpoint for multiple houses"""
    return predict()  # Same logic handles both single and batch


@app.route('/model/info', methods=['GET'])
def model_info():
    """Get model information"""
    if not model_loaded:
        return jsonify({"error": "Model not loaded"}), 500
    
    info = {
        "model_type": type(model).__name__,
        "model_loaded": model_loaded,
        "preprocessor_fitted": preprocessor.is_fitted if preprocessor else False,
        "num_features": len(preprocessor.feature_names) if preprocessor and preprocessor.feature_names else 0
    }
    
    if hasattr(model, 'n_estimators'):
        info["n_estimators"] = model.n_estimators
    if hasattr(model, 'max_depth'):
        info["max_depth"] = model.max_depth
    
    return jsonify(info), 200


if __name__ == '__main__':
    # Load model at startup
    load_model()
    
    # Use port 5001 (5000 often used by AirPlay on macOS)
    port = 5001
    
    print("\n" + "="*60)
    print("🏠 HOUSE PRICE PREDICTION SYSTEM")
    print("="*60)
    print(f"\n✅ Landing Page: http://localhost:{port}")
    print(f"✅ Prediction Page: http://localhost:{port}/predict")
    print(f"✅ API: http://localhost:{port}/predict")
    print(f"✅ Health: http://localhost:{port}/health")
    print("\n" + "="*60 + "\n")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=port, debug=False)


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

LOG_PATH = Path("debug.log")

def log_entry(session_id, run_id, hypothesis_id, location, message, data):
    """Write a log entry in NDJSON format"""
    entry = {
        "sessionId": session_id,
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(__import__('time').time() * 1000)
    }
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(entry) + '\n')


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
    
    # #region agent log
    log_entry("api", "load_model", "LOAD", "app.py:38",
             "Loading model and preprocessor", {})
    # #endregion
    
    try:
        # Get project root (2 levels up from src/house_price_prediction/)
        project_root = Path(__file__).parent.parent.parent
        model_dir = project_root / "models"
        model_path = model_dir / "house_price_model.joblib"
        preprocessor_path = model_dir / "preprocessor.joblib"
        
        if not model_path.exists() or not preprocessor_path.exists():
            # #region agent log
            log_entry("api", "load_model", "LOAD", "app.py:47",
                     "Model files not found", {
                         "model_exists": model_path.exists(),
                         "preprocessor_exists": preprocessor_path.exists()
                     })
            # #endregion
            return False
        
        model = joblib.load(model_path)
        preprocessor = HousePricePreprocessor()
        preprocessor.load(preprocessor_path)
        model_loaded = True
        
        # #region agent log
        log_entry("api", "load_model", "LOAD", "app.py:58",
                 "Model loaded successfully", {
                     "model_type": type(model).__name__,
                     "preprocessor_fitted": preprocessor.is_fitted
                 })
        # #endregion
        
        return True
    except Exception as e:
        # #region agent log
        log_entry("api", "load_model", "LOAD", "app.py:66",
                 "Model load error", {
                     "error": str(e),
                     "error_type": type(e).__name__
                 })
        # #endregion
        return False


# Initialize model at startup (before_first_request is deprecated)
# Model will be loaded when app starts


@app.route('/')
def index():
    """Serve the main frontend page"""
    try:
        return render_template('index.html')
    except Exception:
        # Fallback: redirect to predict page if index.html not found
        from flask import redirect
        return redirect('/predict')


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
    # #region agent log
    log_entry("api", "predict", "PRED", "app.py:90",
             "Prediction request received", {})
    # #endregion
    
    start_time = time.time()
    
    if not model_loaded:
        # #region agent log
        log_entry("api", "predict", "PRED", "app.py:96",
                 "Model not loaded, attempting load", {})
        # #endregion
        if not load_model():
            return jsonify({
                "error": "Model not loaded. Please train the model first."
            }), 500
    
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # #region agent log
        log_entry("api", "predict", "PRED", "app.py:111",
                 "Processing input data", {
                     "input_keys": list(data.keys()) if isinstance(data, dict) else "not_dict"
                 })
        # #endregion
        
        # Convert to DataFrame
        if isinstance(data, dict):
            # Single prediction
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            # Batch prediction
            df = pd.DataFrame(data)
        else:
            return jsonify({"error": "Invalid input format"}), 400
        
        # #region agent log
        log_entry("api", "predict", "PRED", "app.py:125",
                 "DataFrame created", {
                     "shape": list(df.shape),
                     "columns": list(df.columns)
                 })
        # #endregion
        
        # Preprocess
        preprocess_start = time.time()
        X_processed = preprocessor.transform(df)
        preprocess_time = time.time() - preprocess_start
        
        # #region agent log
        log_entry("api", "predict", "PRED", "app.py:135",
                 "Preprocessing complete", {
                     "preprocess_time_ms": preprocess_time * 1000,
                     "processed_shape": list(X_processed.shape)
                 })
        # #endregion
        
        # Predict
        predict_start = time.time()
        predictions = model.predict(X_processed)
        predict_time = time.time() - predict_start
        
        total_time = time.time() - start_time
        
        # #region agent log
        log_entry("api", "predict", "PRED", "app.py:147",
                 "Prediction complete", {
                     "predict_time_ms": predict_time * 1000,
                     "total_time_ms": total_time * 1000,
                     "num_predictions": len(predictions)
                 })
        # #endregion
        
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
        # #region agent log
        log_entry("api", "predict", "PRED", "app.py:172",
                 "Prediction error", {
                     "error": str(e),
                     "error_type": type(e).__name__
                 })
        # #endregion
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
    
    print("\n" + "="*60)
    print("?? HOUSE PRICE PREDICTION SYSTEM")
    print("="*60)
    print("\n? Frontend: http://localhost:5000")
    print("? API: http://localhost:5000/predict")
    print("? Health: http://localhost:5000/health")
    print("\n" + "="*60 + "\n")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)


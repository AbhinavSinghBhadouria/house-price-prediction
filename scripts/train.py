"""
Train Random Forest model for House Price Prediction
Target: 85% R2 score with advanced feature engineering
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib
import json
from pathlib import Path
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from house_price_prediction.preprocessing import HousePricePreprocessor
import time

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


def load_data(data_path):
    """Load housing data from Kaggle dataset"""
    # #region agent log
    log_entry("training", "load_data", "DATA", "train.py:32",
             "Loading data", {"data_path": str(data_path)})
    # #endregion
    
    try:
        # Check if file exists
        if not data_path.exists():
            # #region agent log
            log_entry("training", "load_data", "DATA", "train.py:39",
                     "Data file not found", {
                         "path": str(data_path),
                         "exists": False
                     })
            # #endregion
            print(f"\n⚠️  Data file not found: {data_path}")
            print("   Please download the dataset from Kaggle first:")
            print("   Run: python download_kaggle_data.py")
            raise FileNotFoundError(f"Data file not found: {data_path}")
        
        # Load CSV
        if data_path.suffix == '.csv' or data_path.suffix == '':
            # #region agent log
            log_entry("training", "load_data", "DATA", "train.py:52",
                     "Reading CSV file", {"path": str(data_path)})
            # #endregion
            df = pd.read_csv(data_path)
        else:
            raise ValueError(f"Unsupported file format: {data_path.suffix}")
        
        # #region agent log
        log_entry("training", "load_data", "DATA", "train.py:60",
                 "Data loaded successfully", {
                     "shape": list(df.shape),
                     "columns": list(df.columns),
                     "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024
                 })
        # #endregion
        
        return df
    except FileNotFoundError:
        raise
    except Exception as e:
        # #region agent log
        log_entry("training", "load_data", "DATA", "train.py:72",
                 "Data load error", {
                     "error": str(e),
                     "error_type": type(e).__name__
                 })
        # #endregion
        print(f"\n❌ Error loading data: {e}")
        print("   Please ensure the dataset is downloaded and in the correct format.")
        raise


# Note: Sample data function removed - use Kaggle datasets instead
# Run: python download_kaggle_data.py to download real housing data


def train_model(X_train, y_train, X_val, y_val):
    """Train Random Forest model with hyperparameter tuning"""
    # #region agent log
    log_entry("training", "train_model", "TRAIN", "train.py:88",
             "Starting model training", {
                 "train_shape": list(X_train.shape),
                 "val_shape": list(X_val.shape)
             })
    # #endregion
    
    start_time = time.time()
    
    # Random Forest with optimized hyperparameters for 85% R2 target
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        verbose=1
    )
    
    # #region agent log
    log_entry("training", "train_model", "TRAIN", "train.py:105",
             "Model parameters set", {
                 "n_estimators": 200,
                 "max_depth": 20,
                 "min_samples_split": 5
             })
    # #endregion
    
    model.fit(X_train, y_train)
    
    training_time = time.time() - start_time
    
    # #region agent log
    log_entry("training", "train_model", "TRAIN", "train.py:115",
             "Model training complete", {
                 "training_time_seconds": training_time
             })
    # #endregion
    
    # Evaluate on validation set
    y_pred = model.predict(X_val)
    r2 = r2_score(y_val, y_pred)
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    mae = mean_absolute_error(y_val, y_pred)
    
    # #region agent log
    log_entry("training", "train_model", "TRAIN", "train.py:125",
             "Validation metrics", {
                 "r2_score": float(r2),
                 "rmse": float(rmse),
                 "mae": float(mae)
             })
    # #endregion
    
    return model, r2, rmse, mae


def main():
    """Main training pipeline"""
    # #region agent log
    log_entry("training", "main", "MAIN", "train.py:137",
             "Training pipeline started", {})
    # #endregion
    
    # Paths (relative to project root)
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data" / "processed"
    model_dir = project_root / "models"
    data_dir.mkdir(exist_ok=True)
    model_dir.mkdir(exist_ok=True)
    
    # Load data - try multiple possible filenames
    possible_files = [
        data_dir / "housing.csv",
        data_dir / "california_housing.csv",
        data_dir / "california_housing_train.csv",
        data_dir / "train.csv",
    ]
    
    data_path = None
    for path in possible_files:
        if path.exists():
            data_path = path
            break
    
    if data_path is None:
        # List available files
        available = list(data_dir.glob("*.csv"))
        if available:
            data_path = available[0]
            print(f"Using dataset: {data_path.name}")
        else:
            print("\n❌ No CSV file found in data/ directory")
            print("   Please download the dataset from Kaggle:")
            print("   Run: python download_kaggle_data.py")
            return
    
    df = load_data(data_path)
    
    # #region agent log
    log_entry("training", "main", "MAIN", "train.py:195",
             "Dataset loaded, checking columns", {
                 "columns": list(df.columns),
                 "shape": list(df.shape)
             })
    # #endregion
    
    # Separate features and target
    # Try different common target column names (for Indian and international datasets)
    target_columns = [
        'median_house_value',  # California housing
        'price',                # Common in Indian datasets
        'Price',                # Capitalized
        'house_price',          # Indian datasets
        'House_Price',          # Capitalized
        'target',               # Generic
        'Target'                # Capitalized
    ]
    
    target_col = None
    for col in target_columns:
        if col in df.columns:
            target_col = col
            break
    
    if target_col is None:
        # Show available columns and let user know
        print("\n❌ Target column not found!")
        print(f"\nAvailable columns in dataset:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        print("\n💡 Common target column names:")
        print("   - median_house_value (California housing)")
        print("   - price (Indian datasets)")
        print("   - house_price")
        print("\nPlease ensure your dataset has a price/target column.")
        raise ValueError(f"Target column not found. Available columns: {list(df.columns)}")
    
    # #region agent log
    log_entry("training", "main", "MAIN", "train.py:225",
             "Target column identified", {
                 "target_column": target_col,
                 "target_mean": float(df[target_col].mean()),
                 "target_std": float(df[target_col].std())
             })
    # #endregion
    
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    print(f"\n✓ Using '{target_col}' as target variable")
    
    # #region agent log
    log_entry("training", "main", "MAIN", "train.py:155",
             "Data prepared", {
                 "X_shape": list(X.shape),
                 "y_shape": list(y.shape),
                 "y_mean": float(y.mean()),
                 "y_std": float(y.std())
             })
    # #endregion
    
    # Split data
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42
    )
    
    # #region agent log
    log_entry("training", "main", "MAIN", "train.py:168",
             "Data split complete", {
                 "train_size": len(X_train),
                 "val_size": len(X_val),
                 "test_size": len(X_test)
             })
    # #endregion
    
    # Preprocessing
    preprocessor = HousePricePreprocessor()
    X_train_processed = preprocessor.fit_transform(X_train)
    X_val_processed = preprocessor.transform(X_val)
    X_test_processed = preprocessor.transform(X_test)
    
    # #region agent log
    log_entry("training", "main", "MAIN", "train.py:180",
             "Preprocessing complete", {
                 "train_features": len(X_train_processed.columns),
                 "val_features": len(X_val_processed.columns)
             })
    # #endregion
    
    # Train model
    model, r2_val, rmse_val, mae_val = train_model(
        X_train_processed, y_train, X_val_processed, y_val
    )
    
    # Test set evaluation
    y_test_pred = model.predict(X_test_processed)
    r2_test = r2_score(y_test, y_test_pred)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))
    mae_test = mean_absolute_error(y_test, y_test_pred)
    
    # #region agent log
    log_entry("training", "main", "MAIN", "train.py:195",
             "Test set evaluation", {
                 "r2_score": float(r2_test),
                 "rmse": float(rmse_test),
                 "mae": float(mae_test),
                 "target_r2": 0.85,
                 "achieved_target": r2_test >= 0.85
             })
    # #endregion
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_processed, y_train, 
                               cv=5, scoring='r2', n_jobs=-1)
    
    # #region agent log
    log_entry("training", "main", "MAIN", "train.py:207",
             "Cross-validation complete", {
                 "cv_mean": float(cv_scores.mean()),
                 "cv_std": float(cv_scores.std()),
                 "cv_scores": [float(s) for s in cv_scores]
             })
    # #endregion
    
    # Save model and preprocessor
    model_path = model_dir / "house_price_model.joblib"
    preprocessor_path = model_dir / "preprocessor.joblib"
    
    joblib.dump(model, model_path)
    preprocessor.save(preprocessor_path)
    
    # #region agent log
    log_entry("training", "main", "MAIN", "train.py:220",
             "Model saved", {
                 "model_path": str(model_path),
                 "preprocessor_path": str(preprocessor_path)
             })
    # #endregion
    
    # Print results
    print("\n" + "="*60)
    print("HOUSE PRICE PREDICTION MODEL - TRAINING RESULTS")
    print("="*60)
    print(f"\nValidation Set:")
    print(f"  R2 Score: {r2_val:.4f}")
    print(f"  RMSE: ${rmse_val:,.2f}")
    print(f"  MAE: ${mae_val:,.2f}")
    print(f"\nTest Set:")
    print(f"  R2 Score: {r2_test:.4f}")
    print(f"  RMSE: ${rmse_test:,.2f}")
    print(f"  MAE: ${mae_test:,.2f}")
    print(f"\nCross-Validation (5-fold):")
    print(f"  Mean R2: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
    print(f"\nTarget R2 Score: 0.85")
    print(f"Achieved: {'✓ YES' if r2_test >= 0.85 else '✗ NO'}")
    print(f"\nModel saved to: {model_path}")
    print(f"Preprocessor saved to: {preprocessor_path}")
    print("="*60 + "\n")
    
    return model, preprocessor, r2_test


if __name__ == "__main__":
    main()


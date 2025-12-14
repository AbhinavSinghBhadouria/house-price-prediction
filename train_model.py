#!/usr/bin/env python3
"""
Complete Model Training Script with Fixed Preprocessing
This script will retrain your model with the corrected preprocessing
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import sys
import os

# Add src to path
sys.path.insert(0, 'src')
from house_price_prediction.preprocessing import HousePricePreprocessor

def find_training_data():
    """Find training data file"""
    possible_paths = [
        'data/train.csv',
        'data/training_data.csv',
        'data/dataset.csv',
        'train.csv',
        'training_data.csv',
        'dataset.csv',
        'data.csv',
    ]
    
    for path in possible_paths:
        if Path(path).exists():
            return path
    
    return None

def detect_target_column(df):
    """Detect the target (price) column"""
    possible_names = [
        'price', 'Price', 'PRICE',
        'target', 'Target', 'TARGET',
        'house_price', 'House_Price', 'HOUSE_PRICE',
        'price_in_lakhs', 'Price_in_Lakhs',
        'TARGET(PRICE_IN_LACS)',
    ]
    
    for col in df.columns:
        if col in possible_names or 'price' in col.lower():
            return col
    
    # If not found, assume last column or ask
    return df.columns[-1]

def load_and_prepare_data(data_path):
    """Load and prepare training data"""
    print(f"📂 Loading data from: {data_path}")
    
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'iso-8859-1']
    df = None
    
    for encoding in encodings:
        try:
            if data_path.endswith('.xlsx'):
                df = pd.read_excel(data_path)
            else:
                df = pd.read_csv(data_path, encoding=encoding)
            print(f"✅ Data loaded successfully (encoding: {encoding})")
            break
        except Exception as e:
            continue
    
    if df is None:
        raise ValueError(f"Could not load data from {data_path}")
    
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)[:10]}...")
    
    # Detect target column
    target_col = detect_target_column(df)
    print(f"\n🎯 Target column detected: '{target_col}'")
    
    # Separate features and target
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    # Check for CITY_NAME
    if 'CITY_NAME' not in X.columns:
        print("\n⚠️  WARNING: CITY_NAME not found in data!")
        print("   Checking for alternative city columns...")
        city_cols = [col for col in X.columns if 'city' in col.lower() or 'location' in col.lower()]
        if city_cols:
            print(f"   Found: {city_cols}")
            print(f"   Renaming '{city_cols[0]}' to 'CITY_NAME'...")
            X = X.rename(columns={city_cols[0]: 'CITY_NAME'})
        else:
            print("   ⚠️  No city column found. Model may not differentiate cities properly.")
    
    # Remove rows with missing target
    mask = ~y.isna()
    X = X[mask]
    y = y[mask]
    
    print(f"\n📊 Data summary:")
    print(f"   Features: {X.shape[1]}")
    print(f"   Samples: {X.shape[0]}")
    print(f"   Target range: ₹{y.min():,.0f} - ₹{y.max():,.0f}")
    
    return X, y, target_col

def train_model(X, y, test_size=0.2, random_state=42):
    """Train the model with fixed preprocessing"""
    
    print("\n" + "="*70)
    print("🔄 PREPROCESSING (WITH FIXES)")
    print("="*70)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    print(f"   Training samples: {X_train.shape[0]}")
    print(f"   Test samples: {X_test.shape[0]}")
    
    # Initialize preprocessor (with FIXED code)
    preprocessor = HousePricePreprocessor()
    
    # Fit and transform training data
    print("\n   Fitting preprocessor...")
    X_train_processed = preprocessor.fit_transform(X_train)
    
    print(f"   ✅ Preprocessing complete")
    print(f"   Processed features: {X_train_processed.shape[1]}")
    
    # Check categorical features
    if preprocessor.categorical_features:
        print(f"   Categorical features (NOT scaled): {list(preprocessor.categorical_features)}")
        if 'CITY_NAME' in preprocessor.categorical_features:
            cities = list(preprocessor.label_encoders['CITY_NAME'].classes_)
            print(f"   Cities in training: {len(cities)}")
            print(f"   Sample cities: {cities[:5]}...")
    
    # Transform test data
    X_test_processed = preprocessor.transform(X_test)
    
    print("\n" + "="*70)
    print("🤖 TRAINING MODEL")
    print("="*70)
    
    # Try to load existing model to match type
    model = None
    try:
        old_model = joblib.load('models/house_price_model.joblib')
        model_type = type(old_model).__name__
        print(f"   Detected existing model type: {model_type}")
        
        if model_type == 'RandomForestRegressor':
            model = RandomForestRegressor(
                n_estimators=old_model.n_estimators if hasattr(old_model, 'n_estimators') else 100,
                max_depth=old_model.max_depth if hasattr(old_model, 'max_depth') else None,
                random_state=random_state,
                n_jobs=-1
            )
        elif model_type == 'GradientBoostingRegressor':
            model = GradientBoostingRegressor(
                n_estimators=old_model.n_estimators if hasattr(old_model, 'n_estimators') else 100,
                random_state=random_state
            )
        else:
            # Default to RandomForest
            model = RandomForestRegressor(n_estimators=100, random_state=random_state, n_jobs=-1)
    except:
        # No existing model, use default
        print("   No existing model found, using RandomForestRegressor")
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1
        )
    
    print(f"   Model: {type(model).__name__}")
    print("   Training...")
    
    model.fit(X_train_processed, y_train)
    
    print("   ✅ Training complete!")
    
    # Evaluate
    print("\n" + "="*70)
    print("📊 MODEL EVALUATION")
    print("="*70)
    
    y_train_pred = model.predict(X_train_processed)
    y_test_pred = model.predict(X_test_processed)
    
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)
    
    print(f"\n   Training Set:")
    print(f"      R² Score:  {train_r2:.4f}")
    print(f"      RMSE:      ₹{train_rmse:,.0f}")
    print(f"      MAE:       ₹{train_mae:,.0f}")
    
    print(f"\n   Test Set:")
    print(f"      R² Score:  {test_r2:.4f}")
    print(f"      RMSE:      ₹{test_rmse:,.0f}")
    print(f"      MAE:       ₹{test_mae:,.0f}")
    
    return model, preprocessor, {
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'train_mae': train_mae,
        'test_mae': test_mae
    }

def test_city_differences(model, preprocessor):
    """Test that different cities produce different predictions"""
    print("\n" + "="*70)
    print("🧪 TESTING CITY DIFFERENCES")
    print("="*70)
    
    # Get cities from encoder if available
    cities_to_test = []
    if 'CITY_NAME' in preprocessor.label_encoders:
        all_cities = list(preprocessor.label_encoders['CITY_NAME'].classes_)
        # Test with a few different cities
        cities_to_test = all_cities[:min(5, len(all_cities))]
        print(f"   Testing with cities from training data: {cities_to_test}")
    else:
        # Default test cities
        cities_to_test = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kochi']
        print(f"   Testing with default cities: {cities_to_test}")
    
    results = []
    
    for city in cities_to_test:
        # Create test data with same specs but different city
        test_data = {
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
        
        # Create DataFrame with only columns that model expects
        df_test = pd.DataFrame([test_data])
        
        # Only keep columns that exist in training
        available_cols = [col for col in preprocessor.feature_names if col in df_test.columns]
        missing_cols = [col for col in preprocessor.feature_names if col not in df_test.columns]
        
        if missing_cols:
            # Add missing columns with default values
            for col in missing_cols:
                df_test[col] = 0
        
        try:
            X_test_proc = preprocessor.transform(df_test)
            pred = model.predict(X_test_proc)[0]
            results.append((city, pred))
            
            # Check CITY_NAME encoding
            if 'CITY_NAME' in X_test_proc.columns:
                city_encoded = X_test_proc['CITY_NAME'].iloc[0]
                print(f"   {city:15} → Encoding: {city_encoded:3d} → Price: ₹{pred:,.0f}")
            else:
                print(f"   {city:15} → Price: ₹{pred:,.0f} (⚠️  CITY_NAME not in features)")
        except Exception as e:
            print(f"   {city:15} → Error: {e}")
    
    # Analysis
    if len(results) >= 2:
        prices = [p for _, p in results]
        unique_prices = len(set(prices))
        price_range = max(prices) - min(prices)
        
        print(f"\n   Analysis:")
        print(f"      Unique prices: {unique_prices}/{len(results)}")
        print(f"      Price range: ₹{price_range:,.0f}")
        
        if unique_prices == len(results):
            print(f"\n   ✅ SUCCESS: All cities have DIFFERENT prices!")
            print(f"      The model correctly differentiates between cities.")
        else:
            print(f"\n   ⚠️  WARNING: Some cities have identical prices")
            if 'CITY_NAME' not in preprocessor.feature_names:
                print(f"      CITY_NAME is not in model features - retrain with city data")
            else:
                print(f"      This might be expected if cities are very similar")

def save_model(model, preprocessor, metrics):
    """Save model and preprocessor"""
    print("\n" + "="*70)
    print("💾 SAVING MODEL")
    print("="*70)
    
    # Backup old model
    model_dir = Path('models')
    model_dir.mkdir(exist_ok=True)
    
    old_model_path = model_dir / 'house_price_model.joblib'
    old_preprocessor_path = model_dir / 'preprocessor.joblib'
    
    if old_model_path.exists():
        backup_dir = model_dir / 'backup'
        backup_dir.mkdir(exist_ok=True)
        import shutil
        shutil.copy(old_model_path, backup_dir / 'house_price_model_old.joblib')
        shutil.copy(old_preprocessor_path, backup_dir / 'preprocessor_old.joblib')
        print("   ✅ Old model backed up to models/backup/")
    
    # Save new model
    joblib.dump(model, old_model_path)
    preprocessor.save(old_preprocessor_path)
    
    # Save metrics
    metrics_path = model_dir / 'training_metrics.txt'
    with open(metrics_path, 'w') as f:
        f.write("Model Training Metrics\n")
        f.write("="*50 + "\n\n")
        f.write(f"Training R²: {metrics['train_r2']:.4f}\n")
        f.write(f"Test R²: {metrics['test_r2']:.4f}\n")
        f.write(f"Training RMSE: ₹{metrics['train_rmse']:,.0f}\n")
        f.write(f"Test RMSE: ₹{metrics['test_rmse']:,.0f}\n")
        f.write(f"Training MAE: ₹{metrics['train_mae']:,.0f}\n")
        f.write(f"Test MAE: ₹{metrics['test_mae']:,.0f}\n")
    
    print(f"   ✅ Model saved: {old_model_path}")
    print(f"   ✅ Preprocessor saved: {old_preprocessor_path}")
    print(f"   ✅ Metrics saved: {metrics_path}")

def main():
    """Main training function"""
    print("\n" + "="*70)
    print("🏠 HOUSE PRICE PREDICTION MODEL TRAINING")
    print("="*70)
    print("\nThis script will retrain your model with FIXED preprocessing")
    print("(Categorical features like CITY_NAME will NOT be scaled)\n")
    
    # Find training data
    data_path = find_training_data()
    
    if data_path is None:
        print("❌ ERROR: Training data file not found!")
        print("\nPlease provide the path to your training data:")
        print("   Option 1: Place your CSV file in one of these locations:")
        print("      - data/train.csv")
        print("      - data/training_data.csv")
        print("      - train.csv")
        print("      - training_data.csv")
        print("\n   Option 2: Run this script with the data path:")
        print("      python train_model.py path/to/your/data.csv")
        return
    
    try:
        # Load data
        X, y, target_col = load_and_prepare_data(data_path)
        
        # Train model
        model, preprocessor, metrics = train_model(X, y)
        
        # Test city differences
        test_city_differences(model, preprocessor)
        
        # Save model
        save_model(model, preprocessor, metrics)
        
        print("\n" + "="*70)
        print("✅ TRAINING COMPLETE!")
        print("="*70)
        print("\nYour model has been retrained with the fixed preprocessing.")
        print("Different cities should now produce different predictions.")
        print("\nNext steps:")
        print("   1. Test the model: python test_city_differences.py")
        print("   2. Start the API: python -m src.house_price_prediction.app")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # Custom data path provided
        data_path = sys.argv[1]
        if not Path(data_path).exists():
            print(f"❌ Error: File not found: {data_path}")
            sys.exit(1)
        # Override find_training_data
        import train_model
        train_model.find_training_data = lambda: data_path
    
    sys.exit(main())

"""
Advanced Feature Engineering for House Price Prediction
Includes: rooms per household, population ratios, income bands
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import joblib
import json
from pathlib import Path

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


class HousePricePreprocessor:
    """Advanced feature engineering for house price prediction"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.imputer = SimpleImputer(strategy='median')
        self.feature_names = None
        self.is_fitted = False
        self.categorical_features = set()  # Track which features are categorical (should not be scaled)
        
    def create_advanced_features(self, df):
        """
        Create advanced features:
        - Rooms per household
        - Population ratios
        - Income bands
        """
        
        df = df.copy()
        
        # Rooms per household
        if 'total_rooms' in df.columns and 'households' in df.columns:
            df['rooms_per_household'] = df['total_rooms'] / (df['households'] + 1)
        
        # Bedrooms per household
        if 'total_bedrooms' in df.columns and 'households' in df.columns:
            df['bedrooms_per_household'] = df['total_bedrooms'] / (df['households'] + 1)
        
        # Population ratios
        if 'population' in df.columns and 'households' in df.columns:
            df['population_per_household'] = df['population'] / (df['households'] + 1)
        
        if 'population' in df.columns and 'total_rooms' in df.columns:
            df['population_per_room'] = df['population'] / (df['total_rooms'] + 1)
        
        # Income bands (categorical feature engineering)
        if 'median_income' in df.columns:
            # Create income bands
            income_bands = pd.cut(df['median_income'], 
                                 bins=[0, 2.0, 3.0, 4.0, 5.0, 10.0, np.inf],
                                 labels=['Very Low', 'Low', 'Medium', 'High', 'Very High', 'Extreme'],
                                 include_lowest=True)
            df['income_band'] = income_bands.astype(str)
            
            # Income squared (non-linear feature)
            df['income_squared'] = df['median_income'] ** 2
            
            # Income per room
            if 'total_rooms' in df.columns:
                df['income_per_room'] = df['median_income'] / (df['total_rooms'] + 1)
        
        # Age-based features
        if 'housing_median_age' in df.columns:
            df['age_bins'] = pd.cut(df['housing_median_age'],
                                   bins=[0, 10, 20, 30, 50, np.inf],
                                   labels=['New', 'Recent', 'Mature', 'Old', 'Very Old'],
                                   include_lowest=True)
            df['age_bins'] = df['age_bins'].astype(str)
        
        return df
    
    def fit_transform(self, X, y=None):
        """Fit preprocessor and transform data"""
        
        # Create advanced features
        X_processed = self.create_advanced_features(X)
        
        # Handle missing values
        numeric_cols = X_processed.select_dtypes(include=[np.number]).columns
        categorical_cols = X_processed.select_dtypes(include=['object']).columns
        
        # Impute numeric missing values
        if len(numeric_cols) > 0:
            X_processed[numeric_cols] = self.imputer.fit_transform(X_processed[numeric_cols])
            X_processed[numeric_cols] = pd.DataFrame(X_processed[numeric_cols], 
                                                    columns=numeric_cols,
                                                    index=X_processed.index)
        
        # Encode categorical variables
        for col in categorical_cols:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
            X_processed[col] = self.label_encoders[col].fit_transform(
                X_processed[col].astype(str).fillna('Unknown')
            )
            # Track that this column is categorical (should not be scaled)
            self.categorical_features.add(col)
        
        # Scale numeric features (EXCLUDE encoded categorical features)
        # Categorical features that have been label-encoded should NOT be scaled
        numeric_cols_to_scale = [col for col in numeric_cols if col not in self.categorical_features]
        if len(numeric_cols_to_scale) > 0:
            X_scaled = self.scaler.fit_transform(X_processed[numeric_cols_to_scale])
            X_processed[numeric_cols_to_scale] = pd.DataFrame(X_scaled,
                                                     columns=numeric_cols_to_scale,
                                                     index=X_processed.index)
        
        self.feature_names = list(X_processed.columns)
        self.is_fitted = True
        
        return X_processed
    
    def transform(self, X):
        """Transform new data using fitted preprocessor"""
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform")
        
        # Create advanced features
        X_processed = self.create_advanced_features(X)
        
        # Special handling for CITY_NAME if it exists in input but not in training
        # This helps diagnose issues where city information wasn't used in training
        if 'CITY_NAME' in X_processed.columns and 'CITY_NAME' not in self.feature_names:
            # Log a warning that CITY_NAME is being ignored
            import warnings
            warnings.warn(
                "CITY_NAME is in input data but was not in training features. "
                "The model cannot use city information. Consider retraining with CITY_NAME as a feature.",
                UserWarning
            )
        
        # Handle missing values
        numeric_cols = [col for col in X_processed.select_dtypes(include=[np.number]).columns 
                       if col in self.feature_names]
        categorical_cols = [col for col in X_processed.select_dtypes(include=['object']).columns 
                           if col in self.feature_names]
        
        # Impute numeric missing values
        if len(numeric_cols) > 0:
            X_processed[numeric_cols] = self.imputer.transform(X_processed[numeric_cols])
            X_processed[numeric_cols] = pd.DataFrame(X_processed[numeric_cols],
                                                     columns=numeric_cols,
                                                     index=X_processed.index)
        
        # Encode categorical variables
        for col in categorical_cols:
            if col in self.label_encoders:
                # Handle unseen categories
                known_classes = set(self.label_encoders[col].classes_)
                X_processed[col] = X_processed[col].astype(str).fillna('Unknown')
                
                # Create mapping for known classes
                class_to_int = {cls: idx for idx, cls in enumerate(self.label_encoders[col].classes_)}
                max_known_int = max(class_to_int.values()) if class_to_int else -1
                
                # For unseen categories, use hash-based encoding to give each unique value
                # a different encoding, ensuring different cities get different values
                def encode_value(x):
                    if x in known_classes:
                        return class_to_int[x]
                    else:
                        # Use hash to create a unique encoding for unseen values
                        # Add max_known_int + 1 to ensure it's distinct from known classes
                        # Use modulo to keep it within reasonable range (0 to 2*max_known_int)
                        hash_val = hash(str(x)) % (max_known_int + 1000)
                        return max_known_int + 1 + abs(hash_val)
                
                X_processed[col] = X_processed[col].apply(encode_value)
        
        # Ensure all expected features exist
        for feat in self.feature_names:
            if feat not in X_processed.columns:
                X_processed[feat] = 0
        
        # Reorder columns to match training
        X_processed = X_processed[self.feature_names]
        
        # Scale numeric features (EXCLUDE encoded categorical features)
        # Categorical features that have been label-encoded should NOT be scaled
        numeric_cols_to_scale = [col for col in numeric_cols if col not in self.categorical_features]
        if len(numeric_cols_to_scale) > 0:
            X_scaled = self.scaler.transform(X_processed[numeric_cols_to_scale])
            X_processed[numeric_cols_to_scale] = pd.DataFrame(X_scaled,
                                                     columns=numeric_cols_to_scale,
                                                     index=X_processed.index)
        
        return X_processed
    
    def save(self, filepath):
        """Save preprocessor to disk"""
        preprocessor_data = {
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'imputer': self.imputer,
            'feature_names': self.feature_names,
            'is_fitted': self.is_fitted,
            'categorical_features': self.categorical_features
        }
        joblib.dump(preprocessor_data, filepath)
    
    def load(self, filepath):
        """Load preprocessor from disk"""
        preprocessor_data = joblib.load(filepath)
        self.scaler = preprocessor_data['scaler']
        self.label_encoders = preprocessor_data['label_encoders']
        self.imputer = preprocessor_data['imputer']
        self.feature_names = preprocessor_data['feature_names']
        self.is_fitted = preprocessor_data['is_fitted']
        # Handle backward compatibility: if categorical_features doesn't exist, infer from label_encoders
        if 'categorical_features' in preprocessor_data:
            self.categorical_features = preprocessor_data['categorical_features']
        else:
            # Infer categorical features from label_encoders (backward compatibility)
            self.categorical_features = set(preprocessor_data.get('label_encoders', {}).keys())


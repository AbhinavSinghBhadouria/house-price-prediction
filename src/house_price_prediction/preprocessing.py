"""
Advanced Feature Engineering for House Price Prediction
Includes: rooms per household, population ratios, income bands
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import joblib

class HousePricePreprocessor:
    """Advanced feature engineering for house price prediction"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.imputer = SimpleImputer(strategy='median')
        self.feature_names = None
        self.is_fitted = False
    
    def extract_city_from_address(self, address):
        """Extract city name from address string"""
        if not isinstance(address, str) or not address.strip():
            return 'Unknown'
        
        # Clean the address
        address = address.strip()
        
        # Split by comma and take the last part (usually the city)
        parts = [part.strip() for part in address.split(',')]
        
        # If multiple parts, the last one is likely the city
        if len(parts) > 1:
            city = parts[-1]
        else:
            # If no comma, try to extract from common patterns
            city = address
        
        # Clean up common suffixes and prefixes
        city = city.replace('Road', '').replace('Nagar', '').replace('Colony', '').strip()
        
        # Capitalize properly
        if city:
            city = city.title()
        
        return city if city else 'Unknown'
        
    def create_advanced_features(self, df):
        """
        Create advanced features:
        - Rooms per household
        - Population ratios
        - Income bands
        - Extract city names from addresses
        """
        
        df = df.copy()
        
        # Extract city names from ADDRESS if CITY_NAME is not properly set
        if 'ADDRESS' in df.columns and 'CITY_NAME' in df.columns:
            # Only extract if CITY_NAME is mostly "Unknown" or empty
            if df['CITY_NAME'].isin(['Unknown', '']).sum() > len(df) * 0.8:
                df['CITY_NAME'] = df['ADDRESS'].apply(self.extract_city_from_address)
        
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
        
        # Scale numeric features
        if len(numeric_cols) > 0:
            X_scaled = self.scaler.fit_transform(X_processed[numeric_cols])
            X_processed[numeric_cols] = pd.DataFrame(X_scaled,
                                                     columns=numeric_cols,
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
                
                # Replace unseen categories with a consistent default
                # First, try to use 'Unknown' if it was in training
                if 'Unknown' in known_classes:
                    default_value = 'Unknown'
                else:
                    # Use the alphabetically first known class as default for consistency
                    default_value = sorted(known_classes)[0] if known_classes else 'Unknown'
                
                X_processed[col] = X_processed[col].apply(
                    lambda x: x if x in known_classes else default_value
                )
                
                try:
                    X_processed[col] = self.label_encoders[col].transform(X_processed[col])
                except ValueError:
                    # If still fails, map manually
                    class_to_int = {cls: idx for idx, cls in enumerate(self.label_encoders[col].classes_)}
                    X_processed[col] = X_processed[col].map(lambda x: class_to_int.get(x, class_to_int.get(default_value, 0)))
        
        # Ensure all expected features exist
        for feat in self.feature_names:
            if feat not in X_processed.columns:
                X_processed[feat] = 0
        
        # Reorder columns to match training
        X_processed = X_processed[self.feature_names]
        
        # Scale numeric features
        if len(numeric_cols) > 0:
            X_scaled = self.scaler.transform(X_processed[numeric_cols])
            X_processed[numeric_cols] = pd.DataFrame(X_scaled,
                                                     columns=numeric_cols,
                                                     index=X_processed.index)
        
        return X_processed
    
    def save(self, filepath):
        """Save preprocessor to disk"""
        preprocessor_data = {
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'imputer': self.imputer,
            'feature_names': self.feature_names,
            'is_fitted': self.is_fitted
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


"""
Prepare and merge multiple Kaggle datasets for training
Handles Indian housing datasets with different structures
"""
import pandas as pd
import numpy as np
from pathlib import Path
import json

LOG_PATH = Path("debug.log")

def log_entry(session_id, run_id, hypothesis_id, location, message, data):
    """Write a log entry in NDJSON format"""
    import time
    entry = {
        "sessionId": session_id,
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000)
    }
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(entry) + '\n')


def load_archive_dataset():
    """Load dataset from archive/train.csv"""
    # #region agent log
    log_entry("prepare", "load_archive", "LOAD", "prepare_data.py:32",
             "Loading archive/train.csv", {})
    # #endregion
    
    try:
        project_root = Path(__file__).parent.parent
        archive_path = project_root / "data" / "raw" / "archive" / "train.csv"
        # Also check .temp_files if moved
        temp_archive = project_root / ".temp_files" / "archive" / "train.csv"
        
        if archive_path.exists():
            df = pd.read_csv(archive_path)
        elif temp_archive.exists():
            df = pd.read_csv(temp_archive)
        else:
            raise FileNotFoundError("Archive dataset not found")
        
        # Rename target column to standard name
        if 'TARGET(PRICE_IN_LACS)' in df.columns:
            df = df.rename(columns={'TARGET(PRICE_IN_LACS)': 'price'})
        
        # Convert price from Lacs to actual price (multiply by 100,000)
        if 'price' in df.columns:
            df['price'] = df['price'] * 100000
        
        # #region agent log
        log_entry("prepare", "load_archive", "LOAD", "prepare_data.py:45",
                 "Archive dataset loaded", {
                     "shape": list(df.shape),
                     "columns": list(df.columns),
                     "price_range": [float(df['price'].min()), float(df['price'].max())] if 'price' in df.columns else None
                 })
        # #endregion
        
        return df
    except Exception as e:
        # #region agent log
        log_entry("prepare", "load_archive", "LOAD", "prepare_data.py:53",
                 "Archive load error", {
                     "error": str(e),
                     "error_type": type(e).__name__
                 })
        # #endregion
        return None


def load_city_datasets():
    """Load and combine city-specific datasets from archive-2"""
    # #region agent log
    log_entry("prepare", "load_cities", "LOAD", "prepare_data.py:63",
             "Loading city datasets from archive-2", {})
    # #endregion
    
    project_root = Path(__file__).parent.parent
    city_files = [
        project_root / "data" / "raw" / "archive-2" / "mumbai.csv",
        project_root / "data" / "raw" / "archive-2" / "hyderabad.csv",
        project_root / "data" / "raw" / "archive-2" / "kolkata.csv",
        project_root / "data" / "raw" / "archive-2" / "gurgaon_10k.csv",
        # Also check .temp_files if moved
        project_root / ".temp_files" / "archive-2" / "mumbai.csv",
        project_root / ".temp_files" / "archive-2" / "hyderabad.csv",
        project_root / ".temp_files" / "archive-2" / "kolkata.csv",
        project_root / ".temp_files" / "archive-2" / "gurgaon_10k.csv"
    ]
    
    all_cities = []
    
    for city_file in city_files:
        city_path = Path(city_file) if not isinstance(city_file, Path) else city_file
        if city_path.exists():
            try:
                # #region agent log
                log_entry("prepare", "load_cities", "LOAD", "prepare_data.py:77",
                         f"Loading {city_path.name}", {})
                # #endregion
                
                df = pd.read_csv(city_path)
                
                # Extract city name from filename
                city_name = city_path.stem.replace('_10k', '').title()
                df['CITY_NAME'] = city_name
                
                all_cities.append(df)
                
                # #region agent log
                log_entry("prepare", "load_cities", "LOAD", "prepare_data.py:88",
                         f"Loaded {city_path.name}", {
                             "shape": list(df.shape),
                             "has_price": 'PRICE' in df.columns or 'price' in df.columns
                         })
                # #endregion
            except Exception as e:
                # #region agent log
                log_entry("prepare", "load_cities", "LOAD", "prepare_data.py:96",
                         f"Error loading {city_path.name}", {
                             "error": str(e)
                         })
                # #endregion
                print(f"⚠️  Warning: Could not load {city_file}")
    
    if not all_cities:
        return None
    
    # Combine all city datasets
    combined = pd.concat(all_cities, ignore_index=True)
    
    # #region agent log
    log_entry("prepare", "load_cities", "LOAD", "prepare_data.py:108",
             "City datasets combined", {
                 "total_rows": len(combined),
                 "columns": list(combined.columns)
             })
    # #endregion
    
    return combined


def standardize_columns(df, dataset_type):
    """Standardize column names across different datasets"""
    # #region agent log
    log_entry("prepare", "standardize", "STD", "prepare_data.py:120",
             "Standardizing columns", {
                 "dataset_type": dataset_type,
                 "original_columns": list(df.columns)
             })
    # #endregion
    
    df = df.copy()
    
    # Standardize price column
    price_cols = ['PRICE', 'price', 'TARGET(PRICE_IN_LACS)', 'MIN_PRICE', 'MAX_PRICE']
    for col in price_cols:
        if col in df.columns:
            if col != 'price':
                if 'price' not in df.columns:
                    if col in ['MIN_PRICE', 'MAX_PRICE']:
                        # Use average of min and max if both exist
                        if 'MIN_PRICE' in df.columns and 'MAX_PRICE' in df.columns:
                            df['price'] = (df['MIN_PRICE'].fillna(0) + df['MAX_PRICE'].fillna(0)) / 2
                        elif 'MIN_PRICE' in df.columns:
                            df['price'] = df['MIN_PRICE']
                        elif 'MAX_PRICE' in df.columns:
                            df['price'] = df['MAX_PRICE']
                    else:
                        df['price'] = df[col]
            break
    
    # Standardize area/size column
    area_cols = ['SQUARE_FT', 'square_ft', 'AREA', 'area', 'MIN_AREA_SQFT', 'MAX_AREA_SQFT']
    for col in area_cols:
        if col in df.columns:
            if 'area' not in df.columns:
                if col in ['MIN_AREA_SQFT', 'MAX_AREA_SQFT']:
                    if 'MIN_AREA_SQFT' in df.columns and 'MAX_AREA_SQFT' in df.columns:
                        df['area'] = (df['MIN_AREA_SQFT'].fillna(0) + df['MAX_AREA_SQFT'].fillna(0)) / 2
                    elif 'MIN_AREA_SQFT' in df.columns:
                        df['area'] = df['MIN_AREA_SQFT']
                    elif 'MAX_AREA_SQFT' in df.columns:
                        df['area'] = df['MAX_AREA_SQFT']
                else:
                    df['area'] = df[col]
            break
    
    # Standardize bedroom column
    bedroom_cols = ['BHK_NO.', 'BHK_NO', 'BEDROOM_NUM', 'bedrooms', 'BEDROOMS']
    for col in bedroom_cols:
        if col in df.columns:
            if 'bedrooms' not in df.columns:
                df['bedrooms'] = df[col]
            break
    
    # Standardize location columns
    if 'LONGITUDE' in df.columns and 'longitude' not in df.columns:
        df['longitude'] = df['LONGITUDE']
    if 'LATITUDE' in df.columns and 'latitude' not in df.columns:
        df['latitude'] = df['LATITUDE']
    
    # #region agent log
    log_entry("prepare", "standardize", "STD", "prepare_data.py:170",
             "Columns standardized", {
                 "has_price": 'price' in df.columns,
                 "has_area": 'area' in df.columns,
                 "has_bedrooms": 'bedrooms' in df.columns,
                 "standardized_columns": [c for c in df.columns if c in ['price', 'area', 'bedrooms', 'longitude', 'latitude']]
             })
    # #endregion
    
    return df


def merge_datasets(df1, df2):
    """Merge two datasets, prioritizing archive dataset structure"""
    # #region agent log
    log_entry("prepare", "merge", "MERGE", "prepare_data.py:185",
             "Merging datasets", {
                 "df1_shape": list(df1.shape) if df1 is not None else None,
                 "df2_shape": list(df2.shape) if df2 is not None else None
             })
    # #endregion
    
    if df1 is None and df2 is None:
        return None
    
    if df1 is None:
        return df2
    if df2 is None:
        return df1
    
    # Use archive dataset (df1) as primary since it has better structure
    # Extract useful columns from city dataset (df2) if they exist
    
    # Priority columns to keep
    priority_cols = ['price', 'area', 'bedrooms', 'longitude', 'latitude', 
                     'POSTED_BY', 'UNDER_CONSTRUCTION', 'RERA', 'BHK_OR_RK',
                     'READY_TO_MOVE', 'RESALE', 'ADDRESS', 'CITY_NAME']
    
    # Start with archive dataset (df1) - it has good structure
    merged = df1.copy()
    
    # Add any additional useful columns from city dataset that aren't in archive
    for col in priority_cols:
        if col in df2.columns and col not in merged.columns:
            # Try to add if it makes sense
            if col == 'CITY_NAME':
                # Extract city from address or add as 'Unknown'
                merged[col] = 'Unknown'
    
    # #region agent log
    log_entry("prepare", "merge", "MERGE", "prepare_data.py:220",
             "Datasets merged (using archive as primary)", {
                 "merged_shape": list(merged.shape),
                 "merged_columns": list(merged.columns),
                 "has_location": 'longitude' in merged.columns and 'latitude' in merged.columns
             })
    # #endregion
    
    return merged


def main():
    """Main data preparation function"""
    print("="*60)
    print("DATA PREPARATION - MERGING KAGGLE DATASETS")
    print("="*60)
    
    # #region agent log
    log_entry("prepare", "main", "MAIN", "prepare_data.py:230",
             "Starting data preparation", {})
    # #endregion
    
    # Load datasets
    print("\n📥 Step 1: Loading datasets...")
    
    df_archive = load_archive_dataset()
    if df_archive is not None:
        print(f"   ✓ Loaded archive/train.csv: {df_archive.shape[0]} rows, {df_archive.shape[1]} columns")
    
    df_cities = load_city_datasets()
    if df_cities is not None:
        print(f"   ✓ Loaded city datasets: {df_cities.shape[0]} rows, {df_cities.shape[1]} columns")
    
    # Standardize columns
    print("\n🔧 Step 2: Standardizing column names...")
    
    if df_archive is not None:
        df_archive = standardize_columns(df_archive, "archive")
        print(f"   ✓ Standardized archive dataset")
    
    if df_cities is not None:
        df_cities = standardize_columns(df_cities, "cities")
        print(f"   ✓ Standardized city datasets")
    
    # Merge datasets
    print("\n🔀 Step 3: Merging datasets...")
    
    merged_df = merge_datasets(df_archive, df_cities)
    
    if merged_df is None:
        print("   ❌ No data to merge!")
        return
    
    # Clean and prepare final dataset
    print("\n🧹 Step 4: Cleaning data...")
    
    # Convert price to numeric (handle mixed types)
    if 'price' in merged_df.columns:
        merged_df['price'] = pd.to_numeric(merged_df['price'], errors='coerce')
        print(f"   ✓ Converted price column to numeric")
    
    # Remove rows without price
    initial_rows = len(merged_df)
    merged_df = merged_df.dropna(subset=['price'])
    removed = initial_rows - len(merged_df)
    
    if removed > 0:
        print(f"   ✓ Removed {removed} rows without valid price")
    
    # Remove duplicates
    initial_rows = len(merged_df)
    merged_df = merged_df.drop_duplicates()
    removed = initial_rows - len(merged_df)
    
    if removed > 0:
        print(f"   ✓ Removed {removed} duplicate rows")
    
    # #region agent log
    log_entry("prepare", "main", "MAIN", "prepare_data.py:280",
             "Data preparation complete", {
                 "final_shape": list(merged_df.shape),
                 "final_columns": list(merged_df.columns),
                 "price_stats": {
                     "min": float(merged_df['price'].min()),
                     "max": float(merged_df['price'].max()),
                     "mean": float(merged_df['price'].mean()),
                     "median": float(merged_df['price'].median())
                 } if 'price' in merged_df.columns else None
             })
    # #endregion
    
    # Save merged dataset
    project_root = Path(__file__).parent.parent
    output_path = project_root / "data" / "processed" / "housing.csv"
    merged_df.to_csv(output_path, index=False)
    
    print(f"\n💾 Step 5: Saving merged dataset...")
    print(f"   ✓ Saved to: {output_path}")
    print(f"   ✓ Final dataset: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")
    
    # Summary
    print("\n" + "="*60)
    print("✅ DATA PREPARATION COMPLETE")
    print("="*60)
    print(f"\nDataset saved to: data/housing.csv")
    print(f"Total rows: {len(merged_df):,}")
    print(f"Total columns: {len(merged_df.columns)}")
    
    if 'price' in merged_df.columns:
        try:
            price_min = float(merged_df['price'].min())
            price_max = float(merged_df['price'].max())
            price_mean = float(merged_df['price'].mean())
            price_median = float(merged_df['price'].median())
            
            print(f"\nPrice Statistics:")
            print(f"  Min: ₹{price_min:,.0f}")
            print(f"  Max: ₹{price_max:,.0f}")
            print(f"  Mean: ₹{price_mean:,.0f}")
            print(f"  Median: ₹{price_median:,.0f}")
        except Exception as e:
            print(f"\n⚠️  Could not calculate price statistics: {e}")
    
    print(f"\nKey columns available:")
    key_cols = ['price', 'area', 'bedrooms', 'longitude', 'latitude']
    for col in key_cols:
        if col in merged_df.columns:
            print(f"  ✓ {col}")
        else:
            print(f"  ✗ {col} (missing)")
    
    print("\n🎯 Next step: Run 'python train.py' to train the model")
    print("="*60)


if __name__ == "__main__":
    main()


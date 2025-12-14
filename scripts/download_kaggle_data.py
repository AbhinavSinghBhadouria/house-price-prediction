"""
Download housing dataset from Kaggle
"""
import os
import json
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

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


def setup_kaggle_api():
    """Setup Kaggle API credentials"""
    # #region agent log
    log_entry("kaggle", "setup", "KAGGLE", "download_kaggle_data.py:28",
             "Setting up Kaggle API", {})
    # #endregion
    
    api = KaggleApi()
    
    # Check for credentials
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if kaggle_json.exists():
        # #region agent log
        log_entry("kaggle", "setup", "KAGGLE", "download_kaggle_data.py:38",
                 "Kaggle credentials found", {"path": str(kaggle_json)})
        # #endregion
        api.authenticate()
        return api
    else:
        # #region agent log
        log_entry("kaggle", "setup", "KAGGLE", "download_kaggle_data.py:45",
                 "Kaggle credentials not found", {
                     "expected_path": str(kaggle_json),
                     "kaggle_dir_exists": kaggle_dir.exists()
                 })
        # #endregion
        print("\n⚠️  Kaggle credentials not found!")
        print(f"   Expected location: {kaggle_json}")
        print("\n   To set up Kaggle API:")
        print("   1. Go to https://www.kaggle.com/account")
        print("   2. Scroll to 'API' section")
        print("   3. Click 'Create New API Token'")
        print("   4. Save kaggle.json to ~/.kaggle/kaggle.json")
        print("   5. Set permissions: chmod 600 ~/.kaggle/kaggle.json")
        return None


def download_dataset(dataset_name, data_dir="data", unzip=True):
    """
    Download dataset from Kaggle
    
    Args:
        dataset_name: Kaggle dataset name (e.g., 'camnugent/california-housing-prices')
        data_dir: Directory to save the data
        unzip: Whether to unzip the downloaded files
    """
    # #region agent log
    log_entry("kaggle", "download", "KAGGLE", "download_kaggle_data.py:70",
             "Starting dataset download", {
                 "dataset_name": dataset_name,
                 "data_dir": data_dir
             })
    # #endregion
    
    api = setup_kaggle_api()
    if not api:
        return False
    
    try:
        data_path = Path(data_dir)
        data_path.mkdir(exist_ok=True)
        
        # #region agent log
        log_entry("kaggle", "download", "KAGGLE", "download_kaggle_data.py:82",
                 "Downloading dataset", {"dataset": dataset_name})
        # #endregion
        
        # Download dataset
        api.dataset_download_files(
            dataset_name,
            path=data_path,
            unzip=unzip
        )
        
        # #region agent log
        log_entry("kaggle", "download", "KAGGLE", "download_kaggle_data.py:91",
                 "Dataset downloaded successfully", {
                     "data_dir": str(data_path),
                     "files": list(data_path.glob("*"))
                 })
        # #endregion
        
        print(f"\n✓ Dataset '{dataset_name}' downloaded successfully!")
        print(f"  Saved to: {data_path.absolute()}")
        
        # List downloaded files
        files = list(data_path.glob("*"))
        if files:
            print(f"\n  Downloaded files:")
            for f in files:
                if f.is_file():
                    size_mb = f.stat().st_size / (1024 * 1024)
                    print(f"    - {f.name} ({size_mb:.2f} MB)")
        
        return True
        
    except Exception as e:
        # #region agent log
        log_entry("kaggle", "download", "KAGGLE", "download_kaggle_data.py:110",
                 "Download error", {
                     "error": str(e),
                     "error_type": type(e).__name__
                 })
        # #endregion
        print(f"\n❌ Error downloading dataset: {e}")
        return False


def find_housing_csv(data_dir="data/processed"):
    """Find the housing CSV file in data directory"""
    project_root = Path(__file__).parent.parent
    data_path = project_root / data_dir
    
    # Common housing dataset filenames
    possible_names = [
        "housing.csv",
        "housing.csv.zip",
        "california_housing.csv",
        "california_housing_train.csv",
        "train.csv",
        "data.csv"
    ]
    
    # #region agent log
    log_entry("kaggle", "find_csv", "KAGGLE", "download_kaggle_data.py:135",
             "Searching for CSV file", {
                 "data_dir": str(data_path),
                 "possible_names": possible_names
             })
    # #endregion
    
    # Check for exact matches first
    for name in possible_names:
        file_path = data_path / name
        if file_path.exists():
            # #region agent log
            log_entry("kaggle", "find_csv", "KAGGLE", "download_kaggle_data.py:144",
                     "CSV file found", {"file": str(file_path)})
            # #endregion
            return file_path
    
    # Search for any CSV file
    csv_files = list(data_path.glob("*.csv"))
    if csv_files:
        # #region agent log
        log_entry("kaggle", "find_csv", "KAGGLE", "download_kaggle_data.py:152",
                 "CSV file found (search)", {
                     "file": str(csv_files[0]),
                     "total_csv_files": len(csv_files)
                 })
        # #endregion
        return csv_files[0]
    
    # #region agent log
    log_entry("kaggle", "find_csv", "KAGGLE", "download_kaggle_data.py:160",
             "No CSV file found", {"data_dir": str(data_path)})
    # #endregion
    return None


def main():
    """Main function to download Kaggle dataset"""
    print("="*60)
    print("KAGGLE DATASET DOWNLOADER")
    print("="*60)
    
    # Common housing datasets on Kaggle
    common_datasets = {
        "1": "camnugent/california-housing-prices",
        "2": "quantbruce/real-estate-price-prediction",
        "3": "vedavyasv/usa-housing",
    }
    
    # Indian housing datasets
    indian_datasets = {
        "1": "sukhmandeepsinghbrar/housing-price-dataset",
        "2": "amitabhajoy/bengaluru-house-price-data",
        "3": "ashydv/housing-dataset",
        "4": "suraj520/housing-prices-in-metropolitan-areas-of-india",
        "5": "venkatramakrishnan/indian-house-price-prediction",
    }
    
    print("\n📊 Dataset Categories:")
    print("  A. Popular Housing Datasets (International)")
    print("  B. Indian Housing Price Datasets 🇮🇳")
    print("  C. Enter custom dataset name")
    
    category = input("\nSelect category (A/B/C): ").strip().upper()
    
    if category == "A":
        print("\nPopular Housing Datasets:")
        for key, dataset in common_datasets.items():
            print(f"  {key}. {dataset}")
        choice = input("\nSelect dataset (1-3): ").strip()
        if choice in common_datasets:
            dataset_name = common_datasets[choice]
        else:
            print("Invalid choice. Using default.")
            dataset_name = common_datasets["1"]
    
    elif category == "B":
        print("\n🇮🇳 Indian Housing Price Datasets:")
        print("  1. sukhmandeepsinghbrar/housing-price-dataset")
        print("  2. amitabhajoy/bengaluru-house-price-data (Bangalore)")
        print("  3. ashydv/housing-dataset")
        print("  4. suraj520/housing-prices-in-metropolitan-areas-of-india")
        print("  5. venkatramakrishnan/indian-house-price-prediction")
        print("\n💡 Tip: Search Kaggle for more Indian datasets:")
        print("   - 'india house price'")
        print("   - 'indian real estate'")
        print("   - 'mumbai housing' or 'delhi housing'")
        
        choice = input("\nSelect dataset (1-5): ").strip()
        if choice in indian_datasets:
            dataset_name = indian_datasets[choice]
        else:
            print("Invalid choice. Using default Indian dataset.")
            dataset_name = indian_datasets["1"]
    
    elif category == "C":
        dataset_name = input("Enter Kaggle dataset name (username/dataset): ").strip()
        if not dataset_name:
            print("No dataset name provided. Using default.")
            dataset_name = indian_datasets["1"]
    
    else:
        print("Invalid category. Using Indian dataset by default.")
        dataset_name = indian_datasets["1"]
    
    print(f"\n📥 Downloading: {dataset_name}")
    print("   This may take a few moments...")
    
    success = download_dataset(dataset_name)
    
    if success:
        # Try to find and rename the CSV file
        csv_file = find_housing_csv()
        if csv_file:
            if csv_file.name != "housing.csv":
                target = csv_file.parent / "housing.csv"
                if not target.exists():
                    csv_file.rename(target)
                    print(f"\n✓ Renamed to: housing.csv")
            print(f"\n✓ Dataset ready at: {csv_file.parent / 'housing.csv'}")
        
        print("\n" + "="*60)
        print("✅ SUCCESS! Dataset downloaded.")
        print("="*60)
        print("\nNext steps:")
        print("  1. Check the dataset columns match expected format")
        print("  2. Run: python train.py")
        print("\n💡 Note: If your dataset has different column names,")
        print("   you may need to update train.py to match your data.")
    else:
        print("\n" + "="*60)
        print("❌ DOWNLOAD FAILED")
        print("="*60)
        print("\nPossible issues:")
        print("  1. Kaggle credentials not set up")
        print("     → Run: Setup Kaggle API (see README.md)")
        print("  2. Dataset name incorrect")
        print("     → Verify on https://www.kaggle.com/datasets")
        print("  3. Dataset requires acceptance of terms")
        print("     → Visit dataset page on Kaggle and accept terms")
        print("  4. Internet connection issue")


if __name__ == "__main__":
    main()


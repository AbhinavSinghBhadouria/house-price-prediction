# Purpose of `data/` and `model/` Folders

## 📁 `data/` Folder

### Purpose
The `data/` folder stores your **training datasets** downloaded from Kaggle or other sources.

### What Goes Here
- **CSV files** containing housing data (e.g., `housing.csv`, `california_housing.csv`)
- Raw datasets before preprocessing
- Training data files

### How It's Used

1. **Dataset Download** (`download_kaggle_data.py`):
   ```python
   # Downloads Kaggle datasets to data/ folder
   api.dataset_download_files(dataset_name, path="data", unzip=True)
   ```
   - When you run `python download_kaggle_data.py`, files are saved here
   - Example: `data/housing.csv`

2. **Model Training** (`train.py`):
   ```python
   data_dir = Path("data")
   data_path = data_dir / "housing.csv"  # Looks for CSV files here
   df = load_data(data_path)  # Loads the dataset
   ```
   - Training script automatically searches for CSV files in `data/`
   - Supports multiple filenames: `housing.csv`, `california_housing.csv`, etc.

### Example Structure
```
data/
├── housing.csv              # Main training dataset
└── housing.csv.zip          # (if downloaded as zip)
```

### When to Use
- **Before training**: Download your Kaggle dataset here
- **During training**: Script reads from this folder
- **Never commit**: Add `data/` to `.gitignore` (datasets are large)

---

## 📁 `model/` Folder

### Purpose
The `model/` folder stores your **trained machine learning models** and **preprocessors** after training completes.

### What Goes Here
- **Trained model files** (`.joblib` format)
- **Preprocessor objects** (feature engineering pipeline)
- Saved artifacts needed for predictions

### How It's Used

1. **Model Saving** (`train.py`):
   ```python
   model_dir = Path("model")
   model_path = model_dir / "house_price_model.joblib"
   preprocessor_path = model_dir / "preprocessor.joblib"
   
   # Save after training
   joblib.dump(model, model_path)
   preprocessor.save(preprocessor_path)
   ```
   - After training completes, model and preprocessor are saved here
   - Files: `house_price_model.joblib` and `preprocessor.joblib`

2. **Model Loading** (`app.py`):
   ```python
   model_dir = Path("model")
   model_path = model_dir / "house_price_model.joblib"
   preprocessor_path = model_dir / "preprocessor.joblib"
   
   # Load for API predictions
   model = joblib.load(model_path)
   preprocessor.load(preprocessor_path)
   ```
   - Flask API loads these files when starting
   - Used for real-time predictions

### Example Structure
```
model/
├── house_price_model.joblib    # Trained Random Forest model
└── preprocessor.joblib         # Feature engineering pipeline
```

### When to Use
- **After training**: Files are automatically created here
- **During API**: Flask loads models from here for predictions
- **Version control**: Can commit these (they're smaller than datasets)

---

## 🔄 Complete Workflow

### Step 1: Download Data → `data/` folder
```bash
python download_kaggle_data.py
# Downloads dataset to data/housing.csv
```

### Step 2: Train Model → Creates files in `model/` folder
```bash
python train.py
# Reads from: data/housing.csv
# Saves to: model/house_price_model.joblib
#          model/preprocessor.joblib
```

### Step 3: Run API → Loads from `model/` folder
```bash
python app.py
# Loads: model/house_price_model.joblib
#       model/preprocessor.joblib
# Uses them for predictions
```

---

## 📊 Summary Table

| Folder | Purpose | Contains | Created By | Used By |
|--------|---------|----------|------------|---------|
| `data/` | Store training datasets | CSV files from Kaggle | `download_kaggle_data.py` | `train.py` |
| `model/` | Store trained models | `.joblib` model files | `train.py` | `app.py` |

---

## ⚠️ Important Notes

1. **`data/` folder**:
   - Must exist before training
   - Should contain at least one CSV file
   - Can be empty initially (you'll download data)

2. **`model/` folder**:
   - Created automatically during training
   - Must contain model files before running API
   - If empty, API will show error: "Model not loaded"

3. **File Sizes**:
   - `data/`: Can be large (MB to GB) - don't commit to git
   - `model/`: Usually smaller (MB) - can commit if needed

4. **Docker**:
   - Both folders are mounted as volumes in `docker-compose.yml`
   - This allows persisting data and models across container restarts

---

## 🎯 Quick Reference

**To download data:**
```bash
python download_kaggle_data.py  # → Saves to data/
```

**To train model:**
```bash
python train.py  # → Reads from data/, saves to model/
```

**To run API:**
```bash
python app.py  # → Loads from model/
```


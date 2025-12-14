# Indian Housing Price Dataset Guide

## 🇮🇳 Finding Indian Housing Datasets on Kaggle

### Popular Indian Housing Datasets

1. **sukhmandeepsinghbrar/housing-price-dataset**
   - General Indian housing prices
   - Good starting point

2. **amitabhajoy/bengaluru-house-price-data**
   - Bangalore-specific housing data
   - City-focused dataset

3. **ashydv/housing-dataset**
   - Indian housing dataset
   - Various cities

4. **suraj520/housing-prices-in-metropolitan-areas-of-india**
   - Metropolitan areas focus
   - Multiple cities

5. **venkatramakrishnan/indian-house-price-prediction**
   - Indian house price prediction dataset
   - Pre-processed data

### How to Search for More Datasets

1. **Visit Kaggle Datasets**: https://www.kaggle.com/datasets
2. **Search Terms**:
   - "india house price"
   - "indian real estate"
   - "mumbai housing"
   - "delhi housing"
   - "bangalore house price"
   - "chennai real estate"
   - "hyderabad housing"

3. **Filter by**:
   - File type: CSV
   - Size: Appropriate for your needs
   - License: Check usage rights

## 📥 Downloading Indian Dataset

### Step 1: Run Download Script
```bash
cd house-price-prediction
source venv/bin/activate
python download_kaggle_data.py
```

### Step 2: Select Indian Dataset
```
Select category (A/B/C): B
Select dataset (1-5): [choose your dataset]
```

### Step 3: Verify Dataset
Check that the downloaded CSV has:
- Price/target column
- Feature columns (location, size, etc.)
- Sufficient data points

## 🔧 Adapting Code for Indian Datasets

### Common Column Name Differences

Indian datasets often use different column names:

| Standard Name | Indian Dataset Names |
|---------------|---------------------|
| `median_house_value` | `price`, `Price`, `house_price` |
| `longitude` | `longitude`, `lon`, `Longitude` |
| `latitude` | `latitude`, `lat`, `Latitude` |
| `total_rooms` | `area`, `Area`, `sqft`, `Sqft` |
| `median_income` | `price_per_sqft`, `rate` |

### Automatic Detection

The training script (`train.py`) automatically detects common target column names:
- `median_house_value` (California housing)
- `price` (Indian datasets)
- `Price`
- `house_price`
- `House_Price`

### Manual Column Mapping (if needed)

If your dataset has different column names, you can:

1. **Rename columns in the CSV** before training
2. **Modify `train.py`** to add your column names to the detection list
3. **Create a preprocessing script** to standardize column names

## 📊 Expected Dataset Format

### Minimum Required Columns

Your Indian housing dataset should have:

**Required:**
- Price/target column (any name)
- Location data (latitude/longitude or city/area)
- Size/area information
- Property features

**Optional but helpful:**
- Number of bedrooms
- Number of bathrooms
- Property type (apartment, house, etc.)
- Age of property
- Amenities

### Example Indian Dataset Structure

```csv
area,bedrooms,bathrooms,location,price
1200,2,2,Bangalore,4500000
1500,3,2,Mumbai,8500000
1000,2,1,Delhi,3500000
```

## 🚀 Training with Indian Dataset

### Step 1: Download Dataset
```bash
python download_kaggle_data.py
# Select option B (Indian datasets)
```

### Step 2: Check Dataset
```bash
# Quick check of your data
python -c "import pandas as pd; df = pd.read_csv('data/housing.csv'); print(df.head()); print(df.columns)"
```

### Step 3: Train Model
```bash
python train.py
```

The script will:
- ✅ Automatically detect target column
- ✅ Handle different column names
- ✅ Apply feature engineering
- ✅ Train Random Forest model

## ⚠️ Common Issues & Solutions

### Issue 1: "Target column not found"
**Solution**: Check your dataset column names and ensure a price column exists.

### Issue 2: Different column names
**Solution**: The script auto-detects common names. If yours is different, rename it in the CSV or update `train.py`.

### Issue 3: Missing features
**Solution**: The preprocessing will handle missing values, but ensure you have at least:
- Location data
- Size/area
- Price

### Issue 4: Dataset format issues
**Solution**: 
- Ensure CSV format
- Check for encoding issues (use UTF-8)
- Remove special characters if needed

## 📝 Customizing for Your Dataset

### If Your Dataset Has Different Features

1. **Update `preprocessing.py`**:
   - Modify `create_advanced_features()` to match your columns
   - Add Indian-specific features (e.g., price per sqft ratios)

2. **Update `train.py`**:
   - Add your target column name to the detection list
   - Adjust feature selection if needed

3. **Update `app.py`**:
   - Modify expected input format to match your features

## 🔍 Finding the Right Dataset

### Best Practices

1. **Check dataset size**: At least 1000+ rows for good results
2. **Verify data quality**: Check for missing values, outliers
3. **Location coverage**: Ensure data covers your target area
4. **Recent data**: More recent data = better predictions
5. **Feature richness**: More features = better model performance

### Recommended Search Strategy

1. Start with general "india house price" search
2. Filter by city if you need location-specific data
3. Check dataset descriptions and sample data
4. Verify column names match your needs
5. Download and test with a small sample first

## 📚 Additional Resources

- **Kaggle Datasets**: https://www.kaggle.com/datasets
- **Kaggle Search**: Use filters for "CSV" and "India"
- **Dataset Discussions**: Check comments for usage tips
- **Data.gov.in**: Indian government data portal (alternative source)

## ✅ Quick Checklist

Before training:
- [ ] Dataset downloaded to `data/` folder
- [ ] CSV file readable (check with pandas)
- [ ] Target/price column exists
- [ ] At least 3-5 feature columns present
- [ ] Data size reasonable (1000+ rows recommended)
- [ ] Missing values handled or acceptable

After download:
- [ ] Run `python train.py`
- [ ] Check if target column is detected
- [ ] Verify model training starts successfully


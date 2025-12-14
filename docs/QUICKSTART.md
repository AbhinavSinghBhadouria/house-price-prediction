# Quick Start Guide

## Get Started in 5 Steps

### 1. Activate Virtual Environment
```bash
cd house-price-prediction
source venv/bin/activate
```

### 2. Setup Kaggle API
1. Go to https://www.kaggle.com/account
2. Click "Create New API Token"
3. Save `kaggle.json` to `~/.kaggle/kaggle.json`
4. Set permissions: `chmod 600 ~/.kaggle/kaggle.json`

### 3. Download Dataset
```bash
python download_kaggle_data.py
```
Choose option 1 for California Housing Prices dataset.

### 4. Train Model
```bash
python train.py
```
Wait for training to complete (target: 85% R2 score).

### 5. Start API Server
```bash
python app.py
```

### 6. Test API (in another terminal)
```bash
python test_api.py
```

## That's it! 🎉

Your House Price Prediction API is now running on http://localhost:5000

## Common Issues

**Kaggle credentials not found:**
- Make sure `kaggle.json` is in `~/.kaggle/`
- Check file permissions: `chmod 600 ~/.kaggle/kaggle.json`

**Dataset download fails:**
- Verify your Kaggle API token is valid
- Check internet connection
- Some datasets may require accepting terms on Kaggle website first

**Model not found when starting API:**
- Run `python train.py` first to train and save the model


#!/usr/bin/env python3
"""
Quick check to see if everything is ready for retraining
"""

import sys
from pathlib import Path

def check_ready():
    print("\n" + "="*70)
    print("🔍 CHECKING IF EVERYTHING IS READY")
    print("="*70)
    
    all_ready = True
    
    # Check 1: Training script exists
    print("\n1. Training Script:")
    if Path('train_model.py').exists():
        print("   ✅ train_model.py exists")
    else:
        print("   ❌ train_model.py not found")
        all_ready = False
    
    # Check 2: Preprocessing is fixed
    print("\n2. Preprocessing Fix:")
    try:
        sys.path.insert(0, 'src')
        from house_price_prediction.preprocessing import HousePricePreprocessor
        preprocessor = HousePricePreprocessor()
        if hasattr(preprocessor, 'categorical_features'):
            print("   ✅ Preprocessing has categorical_features tracking")
        else:
            print("   ❌ Preprocessing missing categorical_features")
            all_ready = False
    except Exception as e:
        print(f"   ❌ Error checking preprocessing: {e}")
        all_ready = False
    
    # Check 3: Training data
    print("\n3. Training Data:")
    possible_paths = [
        'data/train.csv',
        'data/training_data.csv',
        'data/dataset.csv',
        'train.csv',
        'training_data.csv',
        'dataset.csv',
        'data.csv',
    ]
    
    found_data = False
    for path in possible_paths:
        if Path(path).exists():
            print(f"   ✅ Found: {path}")
            found_data = True
            break
    
    if not found_data:
        print("   ⚠️  No training data found in common locations")
        print("   You can still provide path when running: python train_model.py path/to/data.csv")
    
    # Check 4: Verification script
    print("\n4. Verification Script:")
    if Path('verify_model_fix.py').exists():
        print("   ✅ verify_model_fix.py exists")
    else:
        print("   ❌ verify_model_fix.py not found")
        all_ready = False
    
    # Check 5: Current model status
    print("\n5. Current Model:")
    if Path('models/house_price_model.joblib').exists():
        print("   ✅ Model file exists (will be backed up before retraining)")
    else:
        print("   ⚠️  No existing model found (will create new one)")
    
    # Summary
    print("\n" + "="*70)
    if all_ready:
        print("✅ EVERYTHING IS READY!")
        print("="*70)
        print("\nYou can now retrain your model:")
        print("   python train_model.py")
        print("\nAfter training, verify it works:")
        print("   python verify_model_fix.py")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("="*70)
        print("\nPlease fix the issues above before retraining.")
    
    print("\n")
    return all_ready

if __name__ == "__main__":
    check_ready()

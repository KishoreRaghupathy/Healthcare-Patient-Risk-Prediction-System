import pickle
import pandas as pd
import os
import sys

def test_model():
    model_path = 'models/readmission_model.pkl'
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        return

    print(f"Loading model from {model_path}...")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully.")

    # Create sample data
    # Columns: age, is_male, systolic_bp, diastolic_bp, heart_rate, spo2, vitals_risk, diagnosis_code, length_of_stay
    sample_data = pd.DataFrame([{
        'age': 65,
        'is_male': 1,
        'systolic_bp': 140,
        'diastolic_bp': 90,
        'heart_rate': 80,
        'spo2': 98,
        'vitals_risk': 1, # Calculated: 140/90 is okish? No, app says >160 or <90. 140 is fine.
                          # But lets just provide a raw value.
                          # Logic in app: 
                          # if sbp > 160 or sbp < 90: vitals_risk += 1
                          # if hr > 100 or hr < 60: vitals_risk += 1
                          # if spo2 < 95: vitals_risk += 1
                          # So for these values vitals_risk should be 0.
        'diagnosis_code': 1, # I10 -> 1
        'length_of_stay': 5
    }])
    
    # Recalculate vitals_risk just to be sure it matches 'concept'
    # sbp=140 (ok), hr=80 (ok), spo2=98 (ok) -> risk=0
    sample_data['vitals_risk'] = 0

    print("\nSample Input Data:")
    print(sample_data)

    print("\nRunning prediction...")
    try:
        # Check if model supports predict_proba
        if hasattr(model, 'predict_proba'):
            prob = model.predict_proba(sample_data)[:, 1]
            print(f"Prediction (Risk Probability): {prob[0]:.4f}")
        else:
            pred = model.predict(sample_data)
            print(f"Prediction (Class): {pred[0]}")
            
    except Exception as e:
        print(f"Prediction failed: {e}")
        # Print expected features if possible
        if hasattr(model, 'feature_names_in_'):
            print(f"Model expects features: {model.feature_names_in_}")

if __name__ == "__main__":
    test_model()

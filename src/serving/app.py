from flask import Flask, request, jsonify
import xgboost as xgb
import pandas as pd
import os
import json
import pickle
from google.cloud import storage

app = Flask(__name__)

# Load model
model_path = 'models/readmission_model.pkl'
model = None

def load_model():
    global model
    display_error = False
    
    # Check if we should download from GCS
    bucket_name = os.environ.get('MODEL_BUCKET')
    if bucket_name and not os.path.exists(model_path):
        print(f"Downloading model from GCS bucket: {bucket_name}")
        try:
            client = storage.Client()
            bucket = client.bucket(bucket_name)
            blob = bucket.blob('models/readmission_model.pkl')
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            blob.download_to_filename(model_path)
            print("Model downloaded successfully.")
        except Exception as e:
            print(f"Failed to download model from GCS: {e}")
            display_error = True

    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load model: {e}")
            display_error = True
    else:
        display_error = True

    if display_error:
        print(f"Warning: Model not found at {model_path}. Predictions will fail.")



@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        # Try loading again (maybe trained after start)
        load_model()
        if not model:
            return jsonify({'error': 'Model not loaded'}), 503

    try:
        data = request.get_json()
        
        # Expected features: age, gender, systolic_bp, diastolic_bp, heart_rate, spo2, diagnosis_code, length_of_stay
        # Needed for prediction: age, is_male, systolic_bp, diastolic_bp, heart_rate, spo2, vitals_risk, diagnosis_code, length_of_stay
        # Note: Model expects specific columns in order or compatible DataFrame.
        # We need to perform same preprocessing as ETL (PreprocessPatient).
        # To avoid code duplication, usually we'd share code. For now, duplicating logic.
        
        age = int(data['age'])
        sbp = int(data['systolic_bp'])
        dbp = int(data['diastolic_bp'])
        hr = int(data['heart_rate'])
        spo2 = int(data['spo2'])
        los = int(data['length_of_stay'])
        diagnosis_str = data['primary_diagnosis']
        
        diagnosis_map = {
            'E11.9': 0, 'I10': 1, 'J44.9': 2, 'I25.10': 3,
            'N18.9': 4, 'F41.9': 5, 'E78.5': 6, 'K21.9': 7
        }
        diagnosis_code = diagnosis_map.get(diagnosis_str, -1)
        
        # Feature Engineering
        vitals_risk = 0
        if sbp > 160 or sbp < 90: vitals_risk += 1
        if hr > 100 or hr < 60: vitals_risk += 1
        if spo2 < 95: vitals_risk += 1
        
        is_male = 1 if data['gender'] == 'Male' else 0
        
        features = pd.DataFrame([{
            'age': age,
            'is_male': is_male,
            'systolic_bp': sbp,
            'diastolic_bp': dbp,
            'heart_rate': hr,
            'spo2': spo2,
            'vitals_risk': vitals_risk,
            'diagnosis_code': diagnosis_code,
            'length_of_stay': los
        }])
        
        # XGBoost prediction
        # If model expects categories, ensure column type is categorical
        # features['diagnosis_code'] = features['diagnosis_code'].astype('category')
        
        prob = model.predict_proba(features)[0][1]
        
        return jsonify({'risk_score':  float(prob)})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    load_model()
    app.run(host='0.0.0.0', port=5000)

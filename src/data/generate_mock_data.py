import pandas as pd
import numpy as np
import random
import os

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_mock_data(num_patients=1000):
    """Generates synthetic patient data for readmission risk prediction."""
    
    data = []
    
    # Diagnosis codes (simplified ICD-10 like codes)
    diagnosis_codes = ['E11.9', 'I10', 'J44.9', 'I25.10', 'N18.9', 'F41.9', 'E78.5', 'K21.9']

    for i in range(num_patients):
        patient_id = f'P{str(i).zfill(5)}'
        
        # Demographics
        age = random.randint(18, 90)
        gender = random.choice(['Male', 'Female'])
        
        # Vitals at discharge (slightly correlated with risk)
        # Higher index = worse health
        health_index = np.random.normal(0, 1) + (age / 100) 
        
        # Systolic BP
        sbp = int(np.random.normal(120, 15) + (10 * health_index))
        # Diastolic BP
        dbp = int(np.random.normal(80, 10) + (5 * health_index))
        # Heart Rate
        hr = int(np.random.normal(75, 12) + (5 * health_index))
        # Oxygen Saturation
        spo2 = int(min(100, np.random.normal(97, 2) - (2 * max(0, health_index))))
        # Temperature
        temp = round(np.random.normal(36.6, 0.4), 1)
        
        # Medical History
        # Randomly assign 1-3 diagnosis codes
        num_diagnoses = random.randint(1, 3)
        diagnoses = random.sample(diagnosis_codes, num_diagnoses)
        primary_diagnosis = diagnoses[0]
        
        # Length of stay
        los = max(1, int(np.random.exponential(4) + health_index))
        
        # Target: Readmission within 30 days
        # Probability increases with age, abn vitals, and specific diagnoses
        prob_readmit = 0.1 
        prob_readmit += (age / 200)
        if sbp > 160 or sbp < 90: prob_readmit += 0.1
        if spo2 < 92: prob_readmit += 0.15
        if 'I25.10' in diagnoses or 'N18.9' in diagnoses: prob_readmit += 0.1
        
        readmitted = 1 if random.random() < min(0.9, prob_readmit) else 0
        
        data.append({
            'patient_id': patient_id,
            'age': age,
            'gender': gender,
            'systolic_bp': sbp,
            'diastolic_bp': dbp,
            'heart_rate': hr,
            'spo2': spo2,
            'temperature': temp,
            'primary_diagnosis': primary_diagnosis,
            'length_of_stay': los,
            'readmitted': readmitted
        })
        
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating mock patient data...")
    df = generate_mock_data(2000)
    
    output_dir = "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "patients.csv")
    
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")
    print(df.head())

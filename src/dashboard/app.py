import streamlit as st
import requests
import json

# Configuration
API_URL = "http://localhost:5000/predict"

st.set_page_config(page_title="Readmission Risk Assessment", layout="wide")

st.title("🏥 Patient Readmission Risk Assessment")
st.markdown("Enter patient vitals and demographics to assess 30-day readmission risk.")

# Input Form
with st.form("patient_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=120, value=65)
        gender = st.selectbox("Gender", ["Male", "Female"])
        length_of_stay = st.number_input("Length of Stay (days)", min_value=1, value=5)
        primary_diagnosis = st.selectbox(
            "Primary Diagnosis Code", 
            ['E11.9', 'I10', 'J44.9', 'I25.10', 'N18.9', 'F41.9', 'E78.5', 'K21.9']
        )
        
    with col2:
        systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=70, max_value=250, value=120)
        diastolic_bp = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=150, value=80)
        heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75)
        spo2 = st.number_input("SpO2 (%)", min_value=50, max_value=100, value=98)
        
    submitted = st.form_submit_button("Assess Risk")

if submitted:
    # Prepare payload
    payload = {
        "age": age,
        "gender": gender,
        "length_of_stay": length_of_stay,
        "primary_diagnosis": primary_diagnosis,
        "systolic_bp": systolic_bp,
        "diastolic_bp": diastolic_bp,
        "heart_rate": heart_rate,
        "spo2": spo2
    }
    
    try:
        with st.spinner("Analyzing risk..."):
            response = requests.post(API_URL, json=payload)
            
        if response.status_code == 200:
            result = response.json()
            risk_score = result.get("risk_score", 0.0)
            
            st.divider()
            st.subheader("Assessment Result")
            
            # Display score
            col_res1, col_res2 = st.columns([1, 2])
            with col_res1:
                st.metric("Readmission Probability", f"{risk_score:.1%}")
            
            with col_res2:
                if risk_score > 0.7:
                    st.error("⚠️ HIGH RISK: Recommend enrolling in post-discharge care program.")
                elif risk_score > 0.3:
                    st.warning("⚠️ MODERATE RISK: Schedule follow-up within 7 days.")
                else:
                    st.success("✅ LOW RISK: Standard discharge protocol.")
                    
        else:
            st.error(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("Error: Could not connect to inference service. Is the backend running?")
    except Exception as e:
        st.error(f"An error occurred: {e}")

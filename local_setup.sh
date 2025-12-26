#!/bin/bash
# Local setup script for Patient Readmission Risk System

# Create directories
mkdir -p data/raw
mkdir -p data/processed
mkdir -p models
mkdir -p src/data
mkdir -p src/etl
mkdir -p src/training
mkdir -p src/serving
mkdir -p src/dashboard

# Create .gitignore
echo "data/" > .gitignore
echo "models/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "venv/" >> .gitignore

# Install dependencies
pip install apache-beam xgboost scikit-learn flask streamlit pandas google-cloud-storage

echo "Setup complete. Directories created and dependencies installed."

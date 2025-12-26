# Local setup script for Patient Readmission Risk System (PowerShell)

# Create directories
New-Item -ItemType Directory -Force -Path "data/raw"
New-Item -ItemType Directory -Force -Path "data/processed"
New-Item -ItemType Directory -Force -Path "models"
New-Item -ItemType Directory -Force -Path "src/data"
New-Item -ItemType Directory -Force -Path "src/etl"
New-Item -ItemType Directory -Force -Path "src/training"
New-Item -ItemType Directory -Force -Path "src/serving"
New-Item -ItemType Directory -Force -Path "src/dashboard"

# Create .gitignore
"data/" | Out-File -FilePath .gitignore -Encoding utf8
"models/" | Out-File -FilePath .gitignore -Append -Encoding utf8
"__pycache__/" | Out-File -FilePath .gitignore -Append -Encoding utf8
"*.pyc" | Out-File -FilePath .gitignore -Append -Encoding utf8
".env" | Out-File -FilePath .gitignore -Append -Encoding utf8
"venv/" | Out-File -FilePath .gitignore -Append -Encoding utf8

# Install dependencies (ignoring errors if pip not found or permission issues, user might need to handle)
try {
    pip install apache-beam xgboost scikit-learn flask streamlit pandas google-cloud-storage
} catch {
    Write-Host "Warning: pip install failed. Please manually install dependencies: apache-beam xgboost scikit-learn flask streamlit pandas google-cloud-storage"
}

Write-Host "Setup complete. Directories created."

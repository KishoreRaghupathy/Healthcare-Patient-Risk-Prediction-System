Write-Host "Starting Patient Readmission Risk System (Local Demo)..."

# Define paths
$VenvPython = "venv\Scripts\python.exe"
$Streamlit = "venv\Scripts\streamlit.exe"

# Check if venv exists
if (-not (Test-Path $VenvPython)) {
    Write-Host "Error: Virtual environment not found. Please run local_setup.ps1 first."
    exit
}

# 1. Generate Data
Write-Host "1. Generating mock data..."
& $VenvPython src/data/generate_mock_data.py

# 2. Run ETL
Write-Host "2. Running ETL pipeline..."
& $VenvPython src/etl/local_pipeline.py

# 3. Train Model
Write-Host "3. Training model..."
& $VenvPython src/training/train_local.py

# 4. Start API (in new window)
Write-Host "4. Starting Prediction API (Flask)..."
$ApiProcess = Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "& '$VenvPython' src/serving/app.py" -PassThru
Write-Host "   API started (PID: $($ApiProcess.Id))."

# Wait a moment for API to initialize
Start-Sleep -Seconds 5

# 5. Start Dashboard (in new window)
Write-Host "5. Starting Dashboard (Streamlit)..."
$DashProcess = Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "& '$Streamlit' run src/dashboard/app.py" -PassThru
Write-Host "   Dashboard started (PID: $($DashProcess.Id))."

Write-Host "---------------------------------------------------"
Write-Host "System is running!"
Write-Host "API: http://localhost:5000"
Write-Host "Dashboard: http://localhost:8501"
Write-Host "Check the new PowerShell windows for logs."
Write-Host "---------------------------------------------------"

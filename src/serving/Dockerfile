FROM python:3.9-slim

WORKDIR /app

# Install system dependencies if any (usually none needed for these python packages on slim, 
# but sometimes build-essential is needed for some xgboost versions if no wheel exists. 
# We'll assume wheels exist for standard linux).

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Run with Gunicorn
# Workers: 1 is often enough for simple serving, but 2-4 is better for concurrency.
# Threads: Using threads can help with I/O bound tasks (like GCS download).
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app

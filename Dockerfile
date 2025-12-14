# Dockerfile for House Price Prediction Flask API
# Optimized for production deployment

FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure templates and static directories are included
COPY src/house_price_prediction/templates/ src/house_price_prediction/templates/
COPY src/house_price_prediction/static/ src/house_price_prediction/static/

# Create directories for data and models
RUN mkdir -p data/raw data/processed data/external models

# Expose port (use PORT env var if available, default to 5000)
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; import os; port = os.environ.get('PORT', '5000'); requests.get(f'http://localhost:{port}/health')"

# Run with Gunicorn for production (use PORT env var for cloud platforms)
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 4 --timeout 120 src.house_price_prediction.app:app


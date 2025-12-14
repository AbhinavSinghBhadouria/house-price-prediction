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

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run with Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "src.house_price_prediction.app:app"]


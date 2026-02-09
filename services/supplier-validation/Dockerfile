# Supplier Validation Workflow [P9] - Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for OCR and image processing
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for file uploads
RUN mkdir -p /tmp/supplier_documents && \
    chmod 755 /tmp/supplier_documents

# Create non-root user
RUN useradd -u 1000 -U -s /bin/bash supplier-validation && \
    chown -R supplier-validation:supplier-validation /app && \
    chown -R supplier-validation:supplier-validation /tmp/supplier_documents

# Switch to non-root user
USER supplier-validation

# Expose port
EXPOSE 8027

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8027/health')" || exit 1

# Run the application
CMD ["python", "main.py"]
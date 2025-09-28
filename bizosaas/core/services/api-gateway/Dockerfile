# BizOSaaS API Gateway - Production Docker Image
# Multi-tier routing with tenant context management

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY services/api-gateway/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared modules first
COPY shared/ ./shared/

# Copy application code
COPY services/api-gateway/ .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' apigateway && \
    chown -R apigateway:apigateway /app

# Switch to non-root user
USER apigateway

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0 \
    PORT=8080

# Run the application
CMD ["python", "main_enhanced.py"]
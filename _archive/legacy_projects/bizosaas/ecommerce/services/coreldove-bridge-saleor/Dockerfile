# CoreLDove Bridge Service for Saleor Integration
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Copy shared modules
COPY ../../shared /app/shared

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8021/health || exit 1

# Expose port
EXPOSE 8021

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8021"]
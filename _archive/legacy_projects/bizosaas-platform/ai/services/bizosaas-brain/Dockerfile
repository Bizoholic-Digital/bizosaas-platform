FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Vault CLI
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    wget \
    unzip \
    && wget https://releases.hashicorp.com/vault/1.15.0/vault_1.15.0_linux_amd64.zip \
    && unzip vault_1.15.0_linux_amd64.zip \
    && mv vault /usr/local/bin/ \
    && rm vault_1.15.0_linux_amd64.zip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements-simple.txt .
RUN pip install --no-cache-dir -r requirements-simple.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash bizosaas \
    && chown -R bizosaas:bizosaas /app
USER bizosaas

# Expose port for the brain (main API)
EXPOSE 8001

# Environment variables for Vault integration
ENV PYTHONPATH=/app
ENV VAULT_ADDR=http://bizosaas-vault:8200
ENV VAULT_TOKEN=bizosaas-dev-root-token
ENV VAULT_MOUNT_PATH=bizosaas
ENV BRAIN_API_URL=http://localhost:8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Run the central brain with Vault integration
CMD ["python", "-m", "uvicorn", "simple_api:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
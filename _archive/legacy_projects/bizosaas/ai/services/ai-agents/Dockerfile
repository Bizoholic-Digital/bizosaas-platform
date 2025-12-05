FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Vault CLI
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    wget \
    unzip \
    && wget https://releases.hashicorp.com/vault/1.15.0/vault_1.15.0_linux_amd64.zip \
    && unzip vault_1.15.0_linux_amd64.zip \
    && mv vault /usr/local/bin/ \
    && rm vault_1.15.0_linux_amd64.zip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY simple_requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt hvac==2.0.0

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1001 aiagents && \
    chown -R aiagents:aiagents /app
USER aiagents

# Environment variables for Vault integration
ENV VAULT_ADDR=http://vault:8200
ENV VAULT_TOKEN=bizosaas-vault-dev-token-2025
ENV BRAIN_API_URL=http://brain-api:8001

# Expose port
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8002/health || exit 1

# Run the application
CMD ["uvicorn", "simple_main:app", "--host", "0.0.0.0", "--port", "8002"]
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
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt hvac==2.0.0

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1001 aiagents && \
  chown -R aiagents:aiagents /app
USER aiagents

# Environment variables for Vault integration
ENV VAULT_ADDR=http://vault:8200
ENV BRAIN_API_URL=http://brain-gateway:8000

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
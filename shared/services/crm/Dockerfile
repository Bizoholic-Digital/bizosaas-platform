FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=crm_project.settings.production

# Set work directory
WORKDIR /app

# Install system dependencies including Vault CLI
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    gettext \
    wget \
    unzip \
    && wget https://releases.hashicorp.com/vault/1.15.0/vault_1.15.0_linux_amd64.zip \
    && unzip vault_1.15.0_linux_amd64.zip \
    && mv vault /usr/local/bin/ \
    && rm vault_1.15.0_linux_amd64.zip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create media, static, and logs directories
RUN mkdir -p /app/media /app/static /app/logs

# Create non-root user for security
RUN useradd -m -u 1001 django && \
    chown -R django:django /app
USER django

# Collect static files (skip for now to avoid database dependency)
# RUN python manage.py collectstatic --noinput --verbosity 0

# Expose port
EXPOSE 8003

# Environment variables for Vault integration
ENV VAULT_ADDR=http://bizosaas-vault:8200
ENV VAULT_TOKEN=bizosaas-dev-root-token
ENV VAULT_MOUNT_PATH=bizosaas
ENV BRAIN_API_URL=http://brain-api:8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8003/health/ || exit 1

# Run application with correct port
CMD ["gunicorn", "--bind", "0.0.0.0:8003", "--workers", "4", "--timeout", "120", "crm_project.wsgi:application"]
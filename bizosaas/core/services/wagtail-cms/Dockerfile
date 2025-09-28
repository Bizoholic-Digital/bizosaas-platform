FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Vault CLI
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    curl \
    wget \
    unzip \
    && wget https://releases.hashicorp.com/vault/1.15.0/vault_1.15.0_linux_amd64.zip \
    && unzip vault_1.15.0_linux_amd64.zip \
    && mv vault /usr/local/bin/ \
    && rm vault_1.15.0_linux_amd64.zip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create static and media directories and log directory
RUN mkdir -p /app/static /app/media /var/log/wagtail

# Create non-root user for security
RUN useradd -m -u 1001 wagtail && \
    chown -R wagtail:wagtail /app
USER wagtail

# Set environment variables
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=wagtail_cms.settings.production
ENV PYTHONUNBUFFERED=1
ENV VAULT_ADDR=http://vault:8200
ENV VAULT_TOKEN=bizosaas-wagtail-cms-token-2025
ENV BRAIN_API_URL=http://brain-api:8001

# Collect static files (skip for now to avoid database dependency)
# RUN python manage.py collectstatic --noinput || true

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:4000/health/ || exit 1

EXPOSE 4000

CMD ["gunicorn", "--bind", "0.0.0.0:4000", "--workers", "3", "--worker-class", "gthread", "wagtail_cms.wsgi:application"]
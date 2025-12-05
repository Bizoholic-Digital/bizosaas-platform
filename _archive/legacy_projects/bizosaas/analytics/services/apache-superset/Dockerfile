# Apache Superset Analytics Dashboard
# Integrated with BizOSaaS Platform for unified analytics

FROM apache/superset:latest

# Switch to root user to install system packages
USER root

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages to the virtual environment site-packages
RUN pip install --target=/app/.venv/lib/python3.10/site-packages --no-cache-dir \
    psycopg2-binary==2.9.10 \
    redis==5.0.8 \
    celery==5.3.4 \
    flask-cors==5.0.0

# Create superset config directory and copy config
RUN mkdir -p /app/pythonpath
COPY superset_config.py /app/pythonpath/superset_config.py

# Set environment variables
ENV SUPERSET_CONFIG_PATH=/app/pythonpath/superset_config.py
ENV PYTHONPATH=/app/pythonpath:/app:$PYTHONPATH

# Create uploads directory
RUN mkdir -p /app/superset_home/uploads && chown -R superset:superset /app/superset_home

# Switch back to superset user
USER superset

# Expose port
EXPOSE 8088

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8088/health || exit 1

# Initialize and run superset
CMD ["/bin/bash", "-c", "\
    echo 'Waiting for database connection...' && \
    while ! pg_isready -h ${POSTGRES_HOST:-postgres} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-postgres}; do sleep 2; done && \
    echo 'Running database migrations...' && \
    superset db upgrade && \
    echo 'Creating default admin user...' && \
    superset fab create-admin --username admin --firstname Admin --lastname User --email admin@bizosaas.com --password ${SUPERSET_ADMIN_PASSWORD:-Bizoholic2024Admin} || echo 'Admin user already exists' && \
    echo 'Initializing Superset...' && \
    superset init && \
    echo 'Starting Superset server...' && \
    superset run -h 0.0.0.0 -p 8088 --with-threads --reload \
"]
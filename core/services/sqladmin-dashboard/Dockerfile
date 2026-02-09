# Multi-stage build for Comprehensive SQLAdmin Dashboard
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILD_DATE
ARG VERSION
ARG VCS_REF

# Add metadata
LABEL maintainer="BizOSaaS Platform Team"
LABEL org.label-schema.build-date=$BUILD_DATE
LABEL org.label-schema.name="BizOSaaS SQLAdmin Dashboard"
LABEL org.label-schema.description="Comprehensive platform management dashboard with full CRUD operations"
LABEL org.label-schema.url="https://bizosaas.com"
LABEL org.label-schema.vcs-ref=$VCS_REF
LABEL org.label-schema.vcs-url="https://github.com/bizosaas/platform"
LABEL org.label-schema.version=$VERSION
LABEL org.label-schema.schema-version="1.0"

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libmagic-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libpq5 \
    libmagic1 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r bizosaas && useradd -r -g bizosaas -s /bin/bash bizosaas

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create necessary directories for the comprehensive admin
RUN mkdir -p /app/logs /app/data /app/static /app/uploads /app/exports /app/reports

# Set ownership and permissions
RUN chown -R bizosaas:bizosaas /app
RUN chmod +x /app/*.py

# Switch to non-root user
USER bizosaas

# Environment variables for production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ADMIN_PORT=8010
ENV ADMIN_HOST=0.0.0.0

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8010/api/system/health || exit 1

# Expose the admin port
EXPOSE 8010

# Default command - run on port 8010
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010", "--workers", "1"]
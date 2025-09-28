# Lightweight BizOSaaS Brain Core - Routing Service Only
FROM python:3.11-slim

WORKDIR /app

# Install minimal dependencies for core router
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy core application
COPY . .

# No external dependencies needed - self-contained core router

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8001/health || exit 1

# Run the lightweight core router
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
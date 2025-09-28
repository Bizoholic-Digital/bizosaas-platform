# AI Agent Service
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8010/health || exit 1

# Run the AI agent service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]
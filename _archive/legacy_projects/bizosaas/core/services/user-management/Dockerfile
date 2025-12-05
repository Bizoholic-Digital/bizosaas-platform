FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ../../requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared modules
COPY ../../shared ./shared

# Copy service code
COPY . .

# Create non-root user
RUN groupadd -r bizosaas && useradd -r -g bizosaas bizosaas
RUN chown -R bizosaas:bizosaas /app
USER bizosaas

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Expose port
EXPOSE 8001

# Start the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
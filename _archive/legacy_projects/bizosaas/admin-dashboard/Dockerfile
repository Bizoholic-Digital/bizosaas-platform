FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt* ./
RUN pip install fastapi uvicorn sqlalchemy psycopg2-binary

# Copy application code
COPY . .

# Expose port
EXPOSE 3003

# Run the application
CMD ["python", "bizosaas_sqladmin.py"]

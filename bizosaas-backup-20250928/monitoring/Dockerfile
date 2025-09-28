FROM python:3.10-slim

WORKDIR /app

# Install monitoring dependencies
RUN pip install fastapi uvicorn psutil redis requests

# Copy monitoring application
COPY monitoring/monitoring_service.py .

# Health check script
COPY monitoring/health_check.py .

# Expose monitoring port
EXPOSE 8090

# Start monitoring service
CMD ["uvicorn", "monitoring_service:app", "--host", "0.0.0.0", "--port", "8090"]
FROM python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default data directory
RUN mkdir -p /data
ENV FILESYSTEM_ROOT=/data

EXPOSE 8000
ENTRYPOINT ["python", "server.py"]

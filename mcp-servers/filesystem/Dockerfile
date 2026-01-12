FROM python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default data directory
RUN mkdir -p /data
ENV FILESYSTEM_ROOT=/data

ENTRYPOINT ["python", "server.py"]

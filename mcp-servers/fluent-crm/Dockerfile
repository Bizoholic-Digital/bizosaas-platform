FROM python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# MCP Servers usually run via stdio, so we don't expose a port
# But we can define the entrypoint
EXPOSE 8000
ENTRYPOINT ["python", "server.py"]

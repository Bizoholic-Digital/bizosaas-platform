# Temporal Workflow Orchestration Service Dockerfile
# Python FastAPI service for managing complex business workflows

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create requirements.txt for Temporal orchestration
COPY <<EOF requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
temporalio==1.5.1
asyncpg==0.29.0
redis==5.0.1
pydantic==2.5.0
python-multipart==0.0.6
aiofiles==23.2.1
httpx==0.25.2
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
EOF

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create main.py for the service
COPY <<EOF main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
import asyncpg
import redis.asyncio as redis
import uvicorn
from datetime import datetime
from typing import Dict, Any, List

app = FastAPI(
    title="BizOSaaS Temporal Orchestration Service",
    description="Workflow orchestration and automation service",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
db_pool = None
redis_client = None

@app.on_event("startup")
async def startup_event():
    global db_pool, redis_client
    # Database connection
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@postgres:5432/bizosaas")
    db_pool = await asyncpg.create_pool(database_url)
    
    # Redis connection
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/5")
    redis_client = redis.from_url(redis_url)
    
    print("✅ Temporal Orchestration Service Started")

@app.on_event("shutdown")
async def shutdown_event():
    global db_pool, redis_client
    if db_pool:
        await db_pool.close()
    if redis_client:
        await redis_client.close()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "temporal-orchestration",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/workflows")
async def list_workflows():
    """List all available workflows"""
    return {
        "workflows": [
            {"name": "crm_workflows", "description": "CRM automation workflows"},
            {"name": "marketing_workflows", "description": "Marketing campaign workflows"},
            {"name": "order_processing", "description": "Order processing workflows"},
            {"name": "lead_management", "description": "Lead nurturing workflows"}
        ]
    }

@app.post("/workflows/{workflow_name}/start")
async def start_workflow(workflow_name: str, payload: Dict[str, Any]):
    """Start a workflow execution"""
    try:
        workflow_id = f"{workflow_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Store workflow execution in database
        async with db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO workflow_executions (workflow_id, workflow_name, status, payload, created_at)
                VALUES ($1, $2, $3, $4, $5)
            """, workflow_id, workflow_name, "started", str(payload), datetime.utcnow())
        
        return {
            "workflow_id": workflow_id,
            "workflow_name": workflow_name,
            "status": "started",
            "message": f"Workflow {workflow_name} started successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/workflows/{workflow_id}/status")
async def get_workflow_status(workflow_id: str):
    """Get workflow execution status"""
    try:
        async with db_pool.acquire() as conn:
            result = await conn.fetchrow("""
                SELECT * FROM workflow_executions WHERE workflow_id = $1
            """, workflow_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        return dict(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8009)
EOF

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8009/health || exit 1

# Expose port
EXPOSE 8009

# Run application
CMD ["python", "main.py"]
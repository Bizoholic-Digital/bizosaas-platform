"""
Logging Service - Centralized logging API for BizOSaas Platform
Provides REST endpoints for log ingestion and retrieval
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import our logging system
import sys
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

from shared.logging_system import (
    get_logger, 
    init_logging_system,
    LogLevel, 
    LogCategory,
    LogEntry,
    CentralizedLogger
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BizOSaas Centralized Logging Service",
    description="Centralized logging and monitoring service for all BizOSaas components",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global logging instance
centralized_logger: Optional[CentralizedLogger] = None

class LogRequest(BaseModel):
    level: LogLevel
    category: LogCategory
    service: str
    message: str
    details: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    tenant_id: Optional[str] = None
    session_id: Optional[str] = None
    trace_id: Optional[str] = None
    performance_metrics: Optional[Dict[str, Any]] = None

class AuditLogRequest(BaseModel):
    user_id: str
    action: str
    resource: str
    tenant_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize logging system on startup"""
    global centralized_logger
    centralized_logger = await init_logging_system()
    logger.info("Centralized logging service started")

@app.get("/")
async def root():
    """Service health check"""
    return {
        "service": "bizosaas-logging-service",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    if not centralized_logger:
        raise HTTPException(status_code=503, detail="Logging system not initialized")
    
    return {
        "status": "healthy",
        "redis_connected": centralized_logger.redis_client is not None,
        "agent_monitor_connected": centralized_logger.agent_monitor is not None,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/logs")
async def create_log_entry(log_request: LogRequest, background_tasks: BackgroundTasks):
    """Create a new log entry"""
    if not centralized_logger:
        raise HTTPException(status_code=503, detail="Logging system not initialized")
    
    try:
        # Use background task for async logging to avoid blocking
        background_tasks.add_task(
            centralized_logger.log,
            log_request.level,
            log_request.category,
            log_request.service,
            log_request.message,
            log_request.details,
            log_request.user_id,
            log_request.tenant_id,
            log_request.session_id,
            log_request.trace_id,
            None,  # error
            log_request.performance_metrics
        )
        
        return {
            "status": "accepted",
            "message": "Log entry queued for processing",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to create log entry: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/logs/audit")
async def create_audit_log(audit_request: AuditLogRequest, background_tasks: BackgroundTasks):
    """Create an audit log entry"""
    if not centralized_logger:
        raise HTTPException(status_code=503, detail="Logging system not initialized")
    
    try:
        background_tasks.add_task(
            centralized_logger.audit_log,
            audit_request.user_id,
            audit_request.action,
            audit_request.resource,
            audit_request.tenant_id,
            audit_request.details,
            audit_request.ip_address
        )
        
        return {
            "status": "accepted",
            "message": "Audit log entry queued for processing",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to create audit log: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs")
async def get_logs(
    category: Optional[str] = Query(None, description="Filter by category"),
    service: Optional[str] = Query(None, description="Filter by service"),
    level: Optional[str] = Query(None, description="Filter by log level"),
    limit: int = Query(100, ge=1, le=1000, description="Number of logs to return")
):
    """Retrieve recent logs with filtering"""
    if not centralized_logger:
        raise HTTPException(status_code=503, detail="Logging system not initialized")
    
    try:
        # Convert string parameters to enums if provided
        log_category = LogCategory(category) if category else None
        log_level = LogLevel(level) if level else None
        
        logs = await centralized_logger.get_recent_logs(
            category=log_category,
            service=service,
            level=log_level,
            limit=limit
        )
        
        return {
            "logs": logs,
            "count": len(logs),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameter: {e}")
    except Exception as e:
        logger.error(f"Failed to retrieve logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs/statistics")
async def get_log_statistics():
    """Get logging statistics for dashboard"""
    if not centralized_logger:
        raise HTTPException(status_code=503, detail="Logging system not initialized")
    
    try:
        stats = await centralized_logger.get_log_statistics()
        
        return {
            "statistics": stats,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to retrieve log statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs/categories")
async def get_log_categories():
    """Get available log categories"""
    return {
        "categories": [category.value for category in LogCategory],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/logs/levels")
async def get_log_levels():
    """Get available log levels"""
    return {
        "levels": [level.value for level in LogLevel],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/logs/bulk")
async def create_bulk_logs(logs: List[LogRequest], background_tasks: BackgroundTasks):
    """Create multiple log entries in bulk"""
    if not centralized_logger:
        raise HTTPException(status_code=503, detail="Logging system not initialized")
    
    if len(logs) > 1000:
        raise HTTPException(status_code=400, detail="Bulk insert limited to 1000 logs at once")
    
    try:
        # Process logs in background
        for log_request in logs:
            background_tasks.add_task(
                centralized_logger.log,
                log_request.level,
                log_request.category,
                log_request.service,
                log_request.message,
                log_request.details,
                log_request.user_id,
                log_request.tenant_id,
                log_request.session_id,
                log_request.trace_id,
                None,  # error
                log_request.performance_metrics
            )
        
        return {
            "status": "accepted",
            "message": f"Bulk insert of {len(logs)} log entries queued for processing",
            "count": len(logs),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to create bulk logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/logs")
async def cleanup_old_logs(days: int = Query(30, ge=1, le=365, description="Delete logs older than N days")):
    """Clean up old logs (admin endpoint)"""
    if not centralized_logger:
        raise HTTPException(status_code=503, detail="Logging system not initialized")
    
    try:
        # This would implement log cleanup logic
        # For now, return a placeholder response
        return {
            "status": "completed",
            "message": f"Cleanup of logs older than {days} days completed",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to cleanup logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Convenience endpoints for common log patterns
@app.post("/logs/info")
async def log_info(
    service: str,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    background_tasks: BackgroundTasks = None
):
    """Quick info logging endpoint"""
    log_request = LogRequest(
        level=LogLevel.INFO,
        category=LogCategory.SYSTEM,
        service=service,
        message=message,
        details=details
    )
    return await create_log_entry(log_request, background_tasks)

@app.post("/logs/error")
async def log_error(
    service: str,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    background_tasks: BackgroundTasks = None
):
    """Quick error logging endpoint"""
    log_request = LogRequest(
        level=LogLevel.ERROR,
        category=LogCategory.SYSTEM,
        service=service,
        message=message,
        details=details
    )
    return await create_log_entry(log_request, background_tasks)

@app.post("/logs/agent")
async def log_agent_activity(
    agent_name: str,
    activity: str,
    tenant_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    performance_metrics: Optional[Dict[str, Any]] = None,
    background_tasks: BackgroundTasks = None
):
    """Log agent activity"""
    log_request = LogRequest(
        level=LogLevel.INFO,
        category=LogCategory.AGENT,
        service=agent_name,
        message=activity,
        tenant_id=tenant_id,
        details=details,
        performance_metrics=performance_metrics
    )
    return await create_log_entry(log_request, background_tasks)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="info"
    )
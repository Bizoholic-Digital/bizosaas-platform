#!/usr/bin/env python3
"""
SQLAdmin Dashboard Service - Port 8005
Provides database administration interface and API endpoints
"""

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from typing import List, Optional, Dict, Any
import uvicorn
import json
from datetime import datetime
import uuid

app = FastAPI(
    title="SQLAdmin Dashboard Service",
    description="Database administration interface with REST API",
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

# Mock database schema and data
MOCK_TABLES = [
    {
        "id": "tbl_001",
        "name": "businesses",
        "schema": "public",
        "columns": [
            {"name": "id", "type": "uuid", "nullable": False, "primary_key": True},
            {"name": "name", "type": "varchar(255)", "nullable": False},
            {"name": "category", "type": "varchar(100)", "nullable": True},
            {"name": "email", "type": "varchar(255)", "nullable": True},
            {"name": "phone", "type": "varchar(50)", "nullable": True},
            {"name": "rating", "type": "decimal(3,2)", "nullable": True},
            {"name": "verified", "type": "boolean", "nullable": False, "default": False},
            {"name": "created_at", "type": "timestamp", "nullable": False},
            {"name": "updated_at", "type": "timestamp", "nullable": False}
        ],
        "row_count": 245,
        "size": "2.3 MB",
        "indexes": ["idx_businesses_name", "idx_businesses_category", "idx_businesses_rating"],
        "foreign_keys": [],
        "description": "Business listings and directory information"
    },
    {
        "id": "tbl_002", 
        "name": "users",
        "schema": "public",
        "columns": [
            {"name": "id", "type": "uuid", "nullable": False, "primary_key": True},
            {"name": "email", "type": "varchar(255)", "nullable": False, "unique": True},
            {"name": "password_hash", "type": "varchar(255)", "nullable": False},
            {"name": "first_name", "type": "varchar(100)", "nullable": True},
            {"name": "last_name", "type": "varchar(100)", "nullable": True},
            {"name": "role", "type": "varchar(50)", "nullable": False, "default": "user"},
            {"name": "is_active", "type": "boolean", "nullable": False, "default": True},
            {"name": "last_login", "type": "timestamp", "nullable": True},
            {"name": "created_at", "type": "timestamp", "nullable": False},
            {"name": "updated_at", "type": "timestamp", "nullable": False}
        ],
        "row_count": 1847,
        "size": "1.8 MB",
        "indexes": ["idx_users_email", "idx_users_role", "idx_users_is_active"],
        "foreign_keys": [],
        "description": "User accounts and authentication data"
    },
    {
        "id": "tbl_003",
        "name": "reviews",
        "schema": "public", 
        "columns": [
            {"name": "id", "type": "uuid", "nullable": False, "primary_key": True},
            {"name": "business_id", "type": "uuid", "nullable": False},
            {"name": "user_id", "type": "uuid", "nullable": False},
            {"name": "rating", "type": "integer", "nullable": False},
            {"name": "title", "type": "varchar(255)", "nullable": True},
            {"name": "content", "type": "text", "nullable": True},
            {"name": "verified", "type": "boolean", "nullable": False, "default": False},
            {"name": "helpful_votes", "type": "integer", "nullable": False, "default": 0},
            {"name": "created_at", "type": "timestamp", "nullable": False},
            {"name": "updated_at", "type": "timestamp", "nullable": False}
        ],
        "row_count": 3456,
        "size": "5.7 MB",
        "indexes": ["idx_reviews_business_id", "idx_reviews_user_id", "idx_reviews_rating"],
        "foreign_keys": [
            {"column": "business_id", "references": "businesses(id)"},
            {"column": "user_id", "references": "users(id)"}
        ],
        "description": "Business reviews and ratings"
    },
    {
        "id": "tbl_004",
        "name": "categories",
        "schema": "public",
        "columns": [
            {"name": "id", "type": "uuid", "nullable": False, "primary_key": True},
            {"name": "name", "type": "varchar(100)", "nullable": False},
            {"name": "slug", "type": "varchar(100)", "nullable": False, "unique": True},
            {"name": "description", "type": "text", "nullable": True},
            {"name": "icon", "type": "varchar(50)", "nullable": True},
            {"name": "parent_id", "type": "uuid", "nullable": True},
            {"name": "business_count", "type": "integer", "nullable": False, "default": 0},
            {"name": "is_active", "type": "boolean", "nullable": False, "default": True},
            {"name": "created_at", "type": "timestamp", "nullable": False},
            {"name": "updated_at", "type": "timestamp", "nullable": False}
        ],
        "row_count": 48,
        "size": "156 KB",
        "indexes": ["idx_categories_slug", "idx_categories_parent_id"],
        "foreign_keys": [
            {"column": "parent_id", "references": "categories(id)"}
        ],
        "description": "Business category taxonomy"
    }
]

MOCK_DATABASE_STATS = {
    "database_name": "bizosaas_db",
    "version": "PostgreSQL 15.4",
    "size": "47.2 MB",
    "tables_count": len(MOCK_TABLES),
    "total_rows": sum(table["row_count"] for table in MOCK_TABLES),
    "connections": {
        "active": 12,
        "idle": 3,
        "max": 100
    },
    "performance": {
        "queries_per_second": 45.7,
        "avg_query_time": "23ms",
        "cache_hit_ratio": "96.3%",
        "buffer_usage": "78%"
    },
    "uptime": "7 days, 14 hours, 32 minutes",
    "last_backup": "2024-09-23T06:00:00Z"
}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "sqladmin-dashboard-service",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "port": 8005
    }

# Database overview endpoint
@app.get("/api/brain/sqladmin/overview")
async def get_database_overview():
    """Get database overview and statistics"""
    try:
        return {
            "database": MOCK_DATABASE_STATS,
            "recent_activity": [
                {
                    "id": "act_001",
                    "type": "query",
                    "query": "SELECT * FROM businesses WHERE rating > 4.5",
                    "duration": "15ms",
                    "rows_affected": 89,
                    "timestamp": "2024-09-23T15:45:32Z",
                    "user": "admin"
                },
                {
                    "id": "act_002", 
                    "type": "insert",
                    "query": "INSERT INTO reviews (business_id, user_id, rating, content) VALUES (...)",
                    "duration": "8ms",
                    "rows_affected": 1,
                    "timestamp": "2024-09-23T15:44:18Z",
                    "user": "api_user"
                },
                {
                    "id": "act_003",
                    "type": "update",
                    "query": "UPDATE businesses SET rating = 4.7 WHERE id = 'biz_001'",
                    "duration": "12ms", 
                    "rows_affected": 1,
                    "timestamp": "2024-09-23T15:43:45Z",
                    "user": "system"
                }
            ],
            "alerts": [
                {
                    "id": "alert_001",
                    "level": "warning",
                    "message": "Connection pool usage at 78% - consider increasing max connections",
                    "timestamp": "2024-09-23T15:30:00Z"
                },
                {
                    "id": "alert_002",
                    "level": "info", 
                    "message": "Automated backup completed successfully",
                    "timestamp": "2024-09-23T06:00:15Z"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get database overview: {str(e)}")

# Tables listing endpoint
@app.get("/api/brain/sqladmin/tables")
async def get_tables(
    schema: Optional[str] = "public",
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100)
):
    """Get database tables with optional filtering"""
    try:
        filtered_tables = MOCK_TABLES.copy()
        
        # Apply search filter
        if search:
            filtered_tables = [
                table for table in filtered_tables
                if search.lower() in table["name"].lower() or 
                   search.lower() in table["description"].lower()
            ]
        
        # Apply schema filter
        if schema != "all":
            filtered_tables = [
                table for table in filtered_tables 
                if table["schema"] == schema
            ]
        
        # Pagination
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        paginated_tables = filtered_tables[start_idx:end_idx]
        
        return {
            "tables": paginated_tables,
            "total": len(filtered_tables),
            "page": page,
            "size": size,
            "total_pages": (len(filtered_tables) + size - 1) // size,
            "schemas": ["public", "analytics", "logs"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tables: {str(e)}")

# Table details endpoint
@app.get("/api/brain/sqladmin/tables/{table_id}")
async def get_table_details(table_id: str):
    """Get detailed information about a specific table"""
    try:
        table = next((t for t in MOCK_TABLES if t["id"] == table_id), None)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")
        
        # Add sample data
        sample_data = []
        if table["name"] == "businesses":
            sample_data = [
                {
                    "id": "biz_001",
                    "name": "Bizoholic Marketing Agency", 
                    "category": "Marketing",
                    "email": "hello@bizoholic.com",
                    "phone": "+1-555-MARKETING",
                    "rating": 4.8,
                    "verified": True,
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-09-20T14:22:00Z"
                },
                {
                    "id": "biz_002",
                    "name": "CorelDove E-commerce",
                    "category": "E-commerce", 
                    "email": "contact@coreldove.com",
                    "phone": "+1-555-ECOMMERCE",
                    "rating": 4.9,
                    "verified": True,
                    "created_at": "2024-02-10T09:15:00Z",
                    "updated_at": "2024-09-21T11:45:00Z"
                }
            ]
        elif table["name"] == "users":
            sample_data = [
                {
                    "id": "usr_001",
                    "email": "admin@bizosaas.com",
                    "first_name": "System",
                    "last_name": "Administrator",
                    "role": "admin",
                    "is_active": True,
                    "last_login": "2024-09-23T15:30:00Z",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-09-23T15:30:00Z"
                }
            ]
        
        return {
            "table": table,
            "sample_data": sample_data,
            "relationships": {
                "incoming": [rel for rel in ["reviews.business_id -> businesses.id"] if table["name"] == "businesses"],
                "outgoing": [rel["column"] + " -> " + rel["references"] for rel in table.get("foreign_keys", [])]
            },
            "performance": {
                "query_count_24h": 1247,
                "avg_query_time": "45ms",
                "slow_queries": 3,
                "index_usage": "92%"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get table details: {str(e)}")

# Query execution endpoint
@app.post("/api/brain/sqladmin/query")
async def execute_query(query_data: dict):
    """Execute SQL query (simulation for demo)"""
    try:
        sql_query = query_data.get("query", "").strip()
        
        if not sql_query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        # Simulate query execution
        if sql_query.lower().startswith("select"):
            # Mock SELECT result
            result = {
                "query": sql_query,
                "execution_time": "23ms",
                "rows_affected": 15,
                "columns": ["id", "name", "category", "rating"],
                "data": [
                    ["biz_001", "Bizoholic Marketing Agency", "Marketing", 4.8],
                    ["biz_002", "CorelDove E-commerce", "E-commerce", 4.9],
                    ["biz_003", "TechStart Innovations", "Technology", 4.6]
                ],
                "status": "success",
                "message": "Query executed successfully"
            }
        elif sql_query.lower().startswith("insert"):
            result = {
                "query": sql_query,
                "execution_time": "8ms",
                "rows_affected": 1,
                "status": "success",
                "message": "1 row inserted successfully"
            }
        elif sql_query.lower().startswith("update"):
            result = {
                "query": sql_query,
                "execution_time": "15ms",
                "rows_affected": 3,
                "status": "success",
                "message": "3 rows updated successfully"
            }
        elif sql_query.lower().startswith("delete"):
            result = {
                "query": sql_query,
                "execution_time": "12ms",
                "rows_affected": 2,
                "status": "success",
                "message": "2 rows deleted successfully"
            }
        else:
            result = {
                "query": sql_query,
                "execution_time": "5ms",
                "rows_affected": 0,
                "status": "success",
                "message": "Query executed successfully"
            }
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")

# Users management endpoint
@app.get("/api/brain/sqladmin/users")
async def get_database_users():
    """Get database users and permissions"""
    try:
        return {
            "users": [
                {
                    "id": "db_user_001",
                    "username": "admin",
                    "role": "superuser",
                    "permissions": ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"],
                    "databases": ["bizosaas_db", "analytics_db"],
                    "active_connections": 3,
                    "last_activity": "2024-09-23T15:45:00Z",
                    "created_at": "2024-01-01T00:00:00Z"
                },
                {
                    "id": "db_user_002", 
                    "username": "api_user",
                    "role": "application",
                    "permissions": ["SELECT", "INSERT", "UPDATE"],
                    "databases": ["bizosaas_db"],
                    "active_connections": 8,
                    "last_activity": "2024-09-23T15:47:00Z",
                    "created_at": "2024-01-15T10:00:00Z"
                },
                {
                    "id": "db_user_003",
                    "username": "readonly_user", 
                    "role": "readonly",
                    "permissions": ["SELECT"],
                    "databases": ["bizosaas_db", "analytics_db"],
                    "active_connections": 1,
                    "last_activity": "2024-09-23T14:30:00Z",
                    "created_at": "2024-02-01T09:00:00Z"
                }
            ],
            "total": 3
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get users: {str(e)}")

# Performance metrics endpoint
@app.get("/api/brain/sqladmin/performance")
async def get_performance_metrics(period: str = "1h"):
    """Get database performance metrics"""
    try:
        # Mock performance data based on period
        if period == "1h":
            metrics = {
                "queries_per_minute": [45, 52, 38, 61, 47, 55, 42, 39, 58, 63],
                "response_times": [23, 18, 31, 15, 28, 22, 19, 35, 17, 24],
                "connections": [8, 12, 15, 9, 11, 14, 13, 10, 16, 12],
                "cpu_usage": [45, 52, 48, 55, 49, 51, 47, 53, 46, 50],
                "memory_usage": [67, 69, 71, 68, 70, 72, 68, 69, 71, 70]
            }
        else:
            metrics = {
                "queries_per_minute": [42, 38, 45, 51, 47, 49, 44, 52, 46, 48],
                "response_times": [25, 22, 27, 20, 26, 23, 24, 21, 28, 25],
                "connections": [10, 11, 13, 9, 12, 14, 11, 10, 15, 12],
                "cpu_usage": [48, 45, 51, 47, 49, 52, 46, 50, 48, 49],
                "memory_usage": [69, 71, 68, 70, 72, 69, 71, 70, 68, 69]
            }
        
        return {
            "period": period,
            "metrics": metrics,
            "summary": {
                "avg_queries_per_minute": sum(metrics["queries_per_minute"]) / len(metrics["queries_per_minute"]),
                "avg_response_time": sum(metrics["response_times"]) / len(metrics["response_times"]),
                "peak_connections": max(metrics["connections"]),
                "avg_cpu_usage": sum(metrics["cpu_usage"]) / len(metrics["cpu_usage"]),
                "avg_memory_usage": sum(metrics["memory_usage"]) / len(metrics["memory_usage"])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get performance metrics: {str(e)}")

# Backup management endpoint
@app.get("/api/brain/sqladmin/backups")
async def get_backups():
    """Get database backup information"""
    try:
        return {
            "backups": [
                {
                    "id": "backup_001",
                    "name": "bizosaas_db_20240923_060000",
                    "type": "full",
                    "size": "234.5 MB",
                    "status": "completed",
                    "created_at": "2024-09-23T06:00:00Z",
                    "duration": "00:03:45",
                    "location": "/backups/full/bizosaas_db_20240923_060000.sql"
                },
                {
                    "id": "backup_002",
                    "name": "bizosaas_db_20240922_060000",
                    "type": "full",
                    "size": "231.2 MB", 
                    "status": "completed",
                    "created_at": "2024-09-22T06:00:00Z",
                    "duration": "00:03:38",
                    "location": "/backups/full/bizosaas_db_20240922_060000.sql"
                },
                {
                    "id": "backup_003",
                    "name": "bizosaas_db_20240921_060000",
                    "type": "full",
                    "size": "228.8 MB",
                    "status": "completed", 
                    "created_at": "2024-09-21T06:00:00Z",
                    "duration": "00:03:42",
                    "location": "/backups/full/bizosaas_db_20240921_060000.sql"
                }
            ],
            "schedule": {
                "full_backup": "daily at 06:00 UTC",
                "incremental_backup": "every 4 hours",
                "retention_policy": "30 days",
                "auto_cleanup": True
            },
            "next_backup": "2024-09-24T06:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get backups: {str(e)}")

# Main entry point
if __name__ == "__main__":
    print("🚀 Starting SQLAdmin Dashboard Service on port 8005...")
    print("🛠️ Service provides database administration interface")
    print("🔗 Integrates with FastAPI Brain Gateway on port 8001")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8005,
        log_level="info"
    )
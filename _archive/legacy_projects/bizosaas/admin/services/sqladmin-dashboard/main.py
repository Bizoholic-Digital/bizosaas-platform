"""
BizOSaaS SQLAlchemy SuperAdmin Dashboard
FastAPI + SQLAlchemy Admin interface for complete database management
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqladmin import Admin, ModelView
from sqlalchemy import create_engine, MetaData, Table, select, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os
import logging
from datetime import datetime
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:securepassword@localhost:5432/bizosaas")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "bizosaas-super-secret-admin-key-2024")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True if ENVIRONMENT == "development" else False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI(
    title="BizOSaaS SuperAdmin Dashboard",
    description="SQLAlchemy-based admin interface for BizOSaaS platform",
    version="1.0.0",
    openapi_url="/api/openapi.json" if ENVIRONMENT == "development" else None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8001", "http://localhost:3009"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# SQLAdmin setup
admin = Admin(app, engine, authentication_backend=None, title="BizOSaaS SuperAdmin")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dynamic model discovery and registration
class DynamicModelView(ModelView):
    """Dynamic model view that adapts to any table structure"""
    
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    
    column_list = "__all__"
    column_searchable_list = []
    column_sortable_list = "__all__"
    
    page_size = 50
    page_size_options = [25, 50, 100, 200]

# Auto-discover and register all tables
def setup_admin_views():
    """Automatically discover database tables and create admin views"""
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        
        # Core tables to prioritize
        priority_tables = [
            'tenants', 'users', 'subscriptions', 'subscription_plans',
            'clients', 'leads', 'campaigns', 'reports', 'ai_insights'
        ]
        
        registered_tables = set()
        
        # Register priority tables first
        for table_name in priority_tables:
            if table_name in metadata.tables and table_name not in registered_tables:
                table = metadata.tables[table_name]
                
                # Create dynamic model class
                model_class = type(
                    f"{table_name.title()}Model",
                    (Base,),
                    {
                        "__table__": table,
                        "__tablename__": table_name
                    }
                )
                
                # Create admin view class
                admin_class = type(
                    f"{table_name.title()}Admin",
                    (DynamicModelView,),
                    {
                        "model": model_class,
                        "name": table_name.replace('_', ' ').title(),
                        "identity": table_name,
                        "icon": "fas fa-table"
                    }
                )
                
                admin.add_view(admin_class)
                registered_tables.add(table_name)
                logger.info(f"Registered admin view for table: {table_name}")
        
        # Register remaining tables
        for table_name, table in metadata.tables.items():
            if table_name not in registered_tables:
                # Create dynamic model class
                model_class = type(
                    f"{table_name.title()}Model",
                    (Base,),
                    {
                        "__table__": table,
                        "__tablename__": table_name
                    }
                )
                
                # Create admin view class
                admin_class = type(
                    f"{table_name.title()}Admin",
                    (DynamicModelView,),
                    {
                        "model": model_class,
                        "name": table_name.replace('_', ' ').title(),
                        "identity": table_name,
                        "icon": "fas fa-database"
                    }
                )
                
                admin.add_view(admin_class)
                registered_tables.add(table_name)
                logger.info(f"Registered admin view for table: {table_name}")
        
        logger.info(f"Successfully registered {len(registered_tables)} admin views")
        
    except Exception as e:
        logger.error(f"Error setting up admin views: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "service": "sqladmin-superadmin-dashboard",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "database_status": "connected",
            "port": 8005
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "sqladmin-superadmin-dashboard",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# Database stats endpoint
@app.get("/api/stats")
async def get_database_stats(db: Session = Depends(get_db)):
    """Get database statistics"""
    try:
        stats = {}
        
        # Get table counts
        metadata = MetaData()
        metadata.reflect(bind=engine)
        
        for table_name, table in metadata.tables.items():
            try:
                count_query = select([text(f"COUNT(*) as count")]).select_from(table)
                result = db.execute(count_query).fetchone()
                stats[table_name] = result[0] if result else 0
            except Exception as e:
                logger.warning(f"Could not get count for table {table_name}: {str(e)}")
                stats[table_name] = 0
        
        return {
            "total_tables": len(metadata.tables),
            "table_counts": stats,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting database stats: {str(e)}")
        return {"error": str(e)}

# Query execution endpoint (be careful with this in production)
@app.post("/api/query")
async def execute_query(query: dict, db: Session = Depends(get_db)):
    """Execute raw SQL query (development only)"""
    if ENVIRONMENT != "development":
        return {"error": "Query execution disabled in production"}
    
    try:
        sql_query = query.get("sql", "")
        if not sql_query.strip():
            return {"error": "Empty query"}
        
        # Basic safety check
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER"]
        if any(keyword in sql_query.upper() for keyword in dangerous_keywords):
            return {"error": "Dangerous query detected"}
        
        result = db.execute(text(sql_query))
        
        if result.returns_rows:
            rows = [dict(row) for row in result.fetchall()]
            return {
                "success": True,
                "rows": rows,
                "count": len(rows)
            }
        else:
            return {
                "success": True,
                "message": "Query executed successfully",
                "rowcount": result.rowcount
            }
            
    except Exception as e:
        logger.error(f"Query execution error: {str(e)}")
        return {"error": str(e)}

# Root redirect
@app.get("/", response_class=RedirectResponse)
async def root():
    """Redirect to admin interface"""
    return RedirectResponse(url="/admin", status_code=302)

# Setup admin views on startup
@app.on_event("startup")
async def startup_event():
    """Initialize admin views on startup"""
    logger.info("Setting up BizOSaaS SuperAdmin Dashboard...")
    setup_admin_views()
    logger.info("BizOSaaS SuperAdmin Dashboard ready!")

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8005))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=ENVIRONMENT == "development",
        log_level="info"
    )
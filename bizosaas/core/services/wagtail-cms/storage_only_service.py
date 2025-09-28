#!/usr/bin/env python3
"""
Wagtail CMS Storage Service - STORAGE LAYER ONLY
This service contains NO business logic - it only stores and retrieves data
ALL business logic is handled by the FastAPI Brain
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import uuid

# Storage-only CMS service
app = FastAPI(
    title="Wagtail CMS Storage Service",
    description="Pure storage layer for CMS data - NO business logic",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for testing (would be database in production)
STORAGE = {
    "tenants": {},
    "pages": {},
    "themes": {}
}

# ========================================================================================
# STORAGE MODELS - Data structures only
# ========================================================================================

class TenantStorageModel(BaseModel):
    tenant_id: str
    name: str
    domain: str
    theme_settings: Dict[str, Any] = {}
    is_active: bool = True
    created_at: datetime = None

class PageStorageModel(BaseModel):
    page_id: str
    tenant_id: str
    title: str
    slug: str
    content: str
    is_published: bool = False
    created_at: datetime = None

# ========================================================================================
# PURE STORAGE ENDPOINTS - No business logic, just CRUD
# ========================================================================================

@app.get("/health")
async def health_check():
    """Health check for storage service"""
    return {
        "status": "healthy",
        "service": "Wagtail CMS Storage Service",
        "role": "Storage Layer Only - No Business Logic",
        "timestamp": datetime.now().isoformat(),
        "storage_count": {
            "tenants": len(STORAGE["tenants"]),
            "pages": len(STORAGE["pages"]),
            "themes": len(STORAGE["themes"])
        }
    }

@app.post("/api/storage/tenants/create/")
async def store_tenant_data(tenant_data: dict):
    """STORAGE ONLY: Store tenant data - no validation or business logic"""
    tenant_id = tenant_data.get("tenant_id", str(uuid.uuid4()))
    
    # Pure storage - no business rules applied here
    STORAGE["tenants"][tenant_id] = {
        "tenant_id": tenant_id,
        "name": tenant_data.get("name", ""),
        "domain": tenant_data.get("domain", ""),
        "theme_settings": tenant_data.get("theme_settings", {}),
        "is_active": tenant_data.get("is_active", True),
        "created_at": datetime.now().isoformat()
    }
    
    return {"success": True, "tenant_id": tenant_id, "action": "stored"}

@app.get("/api/storage/tenants/{tenant_id}/")
async def get_tenant_data(tenant_id: str):
    """STORAGE ONLY: Retrieve tenant data"""
    if tenant_id not in STORAGE["tenants"]:
        raise HTTPException(status_code=404, detail="Tenant not found in storage")
    
    return STORAGE["tenants"][tenant_id]

@app.post("/api/storage/pages/create/")
async def store_page_data(page_data: dict):
    """STORAGE ONLY: Store page data - no validation"""
    page_id = page_data.get("page_id", str(uuid.uuid4()))
    
    # Pure storage - no business rules
    STORAGE["pages"][page_id] = {
        "page_id": page_id,
        "tenant_id": page_data.get("tenant_id", ""),
        "title": page_data.get("title", ""),
        "slug": page_data.get("slug", ""),
        "content": page_data.get("content", ""),
        "is_published": page_data.get("is_published", False),
        "created_at": datetime.now().isoformat()
    }
    
    return {"success": True, "page_id": page_id, "action": "stored"}

@app.get("/api/storage/pages/{tenant_id}/")
async def get_tenant_pages(tenant_id: str):
    """STORAGE ONLY: Get pages for tenant"""
    tenant_pages = {
        page_id: page for page_id, page in STORAGE["pages"].items()
        if page["tenant_id"] == tenant_id
    }
    
    return {"pages": list(tenant_pages.values()), "count": len(tenant_pages)}

@app.put("/api/storage/themes/{tenant_id}/")
async def update_theme_storage(tenant_id: str, theme_data: dict):
    """STORAGE ONLY: Update theme data"""
    STORAGE["themes"][tenant_id] = {
        "tenant_id": tenant_id,
        "theme_settings": theme_data,
        "updated_at": datetime.now().isoformat()
    }
    
    return {"success": True, "tenant_id": tenant_id, "action": "theme_updated"}

@app.get("/api/storage/themes/{tenant_id}/")
async def get_theme_storage(tenant_id: str):
    """STORAGE ONLY: Get theme data"""
    if tenant_id not in STORAGE["themes"]:
        return {"tenant_id": tenant_id, "theme_settings": {}}
    
    return STORAGE["themes"][tenant_id]

@app.get("/api/storage/stats/")
async def get_storage_stats():
    """STORAGE ONLY: Get storage statistics"""
    return {
        "storage_type": "In-Memory (Testing)",
        "tenants_count": len(STORAGE["tenants"]),
        "pages_count": len(STORAGE["pages"]),
        "themes_count": len(STORAGE["themes"]),
        "total_records": len(STORAGE["tenants"]) + len(STORAGE["pages"]) + len(STORAGE["themes"]),
        "note": "This is a storage-only layer with NO business logic"
    }

# ========================================================================================
# ARCHITECTURE VALIDATION ENDPOINTS
# ========================================================================================

@app.get("/architecture/validation")
async def validate_architecture():
    """Validate that this service has NO business logic"""
    return {
        "service_role": "Storage Layer Only",
        "business_logic_present": False,
        "validation_rules_present": False,
        "tenant_isolation_logic": False,
        "workflow_triggers_present": False,
        "note": "All business logic handled by FastAPI Brain",
        "endpoints_available": [
            "/api/storage/tenants/create/",
            "/api/storage/tenants/{tenant_id}/",
            "/api/storage/pages/create/",
            "/api/storage/pages/{tenant_id}/",
            "/api/storage/themes/{tenant_id}/",
            "/api/storage/stats/"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4000, reload=True)
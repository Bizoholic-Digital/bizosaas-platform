#!/usr/bin/env python3

"""
TailAdmin v2 Dashboard - Unified Authentication (TESTING VERSION - No Auth)
"""

import os
import json
import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
STATIC_FILES_PATH = os.getenv("STATIC_FILES_PATH", "/app/html")

app = FastAPI(
    title="TailAdmin v2 Dashboard - Testing Mode",
    description="Secured business operations dashboard (authentication bypassed for testing)",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates and static files
templates = Jinja2Templates(directory=STATIC_FILES_PATH)
app.mount("/static", StaticFiles(directory=f"{STATIC_FILES_PATH}/static"), name="static")

# Pydantic models
class UserSession(BaseModel):
    user_id: str
    email: str
    role: str
    permissions: list
    tenant_id: Optional[str] = None
    accessible_platforms: Optional[list] = []

# Mock user session for testing
def get_mock_user_session() -> UserSession:
    return UserSession(
        user_id="test-admin-123",
        email="admin@bizoholic.com",
        role="super_admin",
        permissions=["*"],
        tenant_id="bizoholic"
    )

# Routes

@app.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """Main TailAdmin v2 dashboard - testing mode (no auth required)"""
    
    # Use mock user session for testing
    user_session = get_mock_user_session()
    
    # Load the TailAdmin v2 dashboard template
    try:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "user": {
                "id": user_session.user_id,
                "email": user_session.email,
                "role": user_session.role,
                "permissions": user_session.permissions,
                "tenant_id": user_session.tenant_id
            }
        })
        
    except Exception as e:
        logger.error(f"Template error: {e}")
        # Fallback HTML response
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>TailAdmin v2 - Testing Mode</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-50">
            <div class="min-h-screen">
                <header class="bg-blue-600 text-white p-4">
                    <h1 class="text-2xl font-bold">TailAdmin v2 Dashboard - Testing Mode</h1>
                    <p class="text-blue-100">Template Error: {e}</p>
                </header>
                <main class="p-6">
                    <div class="bg-white rounded-lg shadow p-6">
                        <h2 class="text-xl font-semibold mb-4">Dashboard Loaded Successfully</h2>
                        <p class="text-gray-600 mb-4">User: {user_session.email} | Role: {user_session.role}</p>
                        <p class="text-sm text-gray-500">Template file not found or corrupted. Using fallback display.</p>
                        
                        <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div class="bg-blue-50 p-4 rounded-lg">
                                <h3 class="font-semibold text-blue-800">Analytics</h3>
                                <p class="text-blue-600 text-sm">Business intelligence</p>
                            </div>
                            <div class="bg-green-50 p-4 rounded-lg">
                                <h3 class="font-semibold text-green-800">AI Agents</h3>
                                <p class="text-green-600 text-sm">28 active agents</p>
                            </div>
                            <div class="bg-purple-50 p-4 rounded-lg">
                                <h3 class="font-semibold text-purple-800">Users</h3>
                                <p class="text-purple-600 text-sm">User management</p>
                            </div>
                        </div>
                    </div>
                </main>
            </div>
        </body>
        </html>
        """)

@app.get("/api/system/health")
async def system_health():
    """System health check"""
    return {
        "status": "healthy",
        "service": "bizosaas-auth-service",
        "version": "2.0.0",
        "mode": "testing",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/user/profile")
async def get_user_profile():
    """Get current user profile"""
    user_session = get_mock_user_session()
    return {
        "user_id": user_session.user_id,
        "email": user_session.email,
        "role": user_session.role,
        "permissions": user_session.permissions,
        "tenant_id": user_session.tenant_id
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
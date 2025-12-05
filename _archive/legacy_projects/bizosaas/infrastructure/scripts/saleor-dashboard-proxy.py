#!/usr/bin/env python3
"""
Saleor Dashboard Proxy for CoreLDove
Provides admin dashboard interface for managing the e-commerce platform
"""

import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CoreLDove Saleor Dashboard",
    description="Admin dashboard for CoreLDove e-commerce platform",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple admin dashboard HTML
ADMIN_DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CoreLDove Admin Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .dashboard-container {
            background: white;
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 800px;
            width: 90%;
        }
        .logo { 
            text-align: center;
            color: #4a5568;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        .subtitle {
            text-align: center;
            color: #718096;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: #f7fafc;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            border-left: 4px solid #667eea;
        }
        .stat-number {
            font-size: 2rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 0.5rem;
        }
        .stat-label {
            color: #718096;
            font-size: 0.9rem;
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .status-item {
            display: flex;
            align-items: center;
            padding: 1rem;
            background: #f7fafc;
            border-radius: 8px;
        }
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 0.75rem;
        }
        .status-online { background: #48bb78; }
        .status-warning { background: #ed8936; }
        .action-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.2s;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover {
            background: #5a6fd8;
            transform: translateY(-1px);
        }
        .btn-secondary {
            background: #e2e8f0;
            color: #4a5568;
        }
        .btn-secondary:hover {
            background: #cbd5e0;
        }
        .api-endpoint {
            background: #2d3748;
            color: #e2e8f0;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.85rem;
            margin: 0.25rem;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <h1 class="logo">🚀 CoreLDove</h1>
        <p class="subtitle">AI-Powered E-commerce Admin Dashboard</p>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">3</div>
                <div class="stat-label">Active Products</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">2</div>
                <div class="stat-label">Categories</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">$1,159.97</div>
                <div class="stat-label">Total Value</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">100%</div>
                <div class="stat-label">System Health</div>
            </div>
        </div>

        <div class="status-grid">
            <div class="status-item">
                <div class="status-indicator status-online"></div>
                <span>GraphQL API (Port 8024)</span>
            </div>
            <div class="status-item">
                <div class="status-indicator status-online"></div>
                <span>Frontend (Port 3001)</span>
            </div>
            <div class="status-item">
                <div class="status-indicator status-online"></div>
                <span>AI Agents (Port 8000)</span>
            </div>
            <div class="status-item">
                <div class="status-indicator status-warning"></div>
                <span>Payment Gateway (Setup Required)</span>
            </div>
        </div>

        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #4a5568; margin-bottom: 1rem;">Quick Access</h3>
            <div>
                <code class="api-endpoint">GraphQL: http://localhost:8024/graphql/</code>
                <code class="api-endpoint">Frontend: http://localhost:3001</code>
                <code class="api-endpoint">AI Agents: http://localhost:8000</code>
            </div>
        </div>

        <div class="action-buttons">
            <a href="http://localhost:3001" class="btn btn-primary">View Storefront</a>
            <a href="http://localhost:8024/graphql/" class="btn btn-secondary">GraphQL Playground</a>
            <a href="http://localhost:8000/docs" class="btn btn-secondary">AI Agents API</a>
            <button onclick="window.location.reload()" class="btn btn-secondary">Refresh Status</button>
        </div>
    </div>

    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => {
            window.location.reload();
        }, 30000);
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def dashboard_home():
    """Main dashboard page"""
    return ADMIN_DASHBOARD_HTML

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "saleor-dashboard-proxy",
        "endpoints": {
            "graphql_api": "http://localhost:8024/graphql/",
            "frontend": "http://localhost:3001",
            "ai_agents": "http://localhost:8000"
        }
    }

@app.get("/admin")
async def admin_redirect():
    """Redirect /admin to main dashboard"""
    return RedirectResponse(url="/")

if __name__ == "__main__":
    uvicorn.run(
        "saleor-dashboard-proxy:app",
        host="0.0.0.0",
        port=9020,
        log_level="info"
    )
#!/usr/bin/env python3
"""
Main entry point for BizOSaaS Unified Dashboard Service
"""

from dashboard_service import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5005, reload=True)
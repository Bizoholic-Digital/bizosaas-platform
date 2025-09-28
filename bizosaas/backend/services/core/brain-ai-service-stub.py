#!/usr/bin/env python3
"""
Simple AI Orchestrator Service - Minimal service for port 8002
"""
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver

class SimpleAIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "ai-orchestrator",
                "version": "1.0.0",
                "timestamp": datetime.now().isoformat(),
                "port": 8002
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            html = """
            <h1>BizOSaaS AI Orchestrator Service</h1>
            <p>Service running on port 8002</p>
            <p>Status: <span style="color: green;">Active</span></p>
            <p><a href="/health">Health Check</a></p>
            """
            self.wfile.write(html.encode())
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    PORT = 8002
    with socketserver.TCPServer(("", PORT), SimpleAIHandler) as httpd:
        print(f"Simple AI Orchestrator Service running on port {PORT}")
        print(f"Health check: http://localhost:{PORT}/health")
        httpd.serve_forever()
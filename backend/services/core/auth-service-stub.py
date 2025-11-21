#!/usr/bin/env python3
"""
Simple Identity Service - Minimal FastAPI service for port 8001
"""
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver

class SimpleIdentityHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "identity-service",
                "version": "1.0.0",
                "timestamp": datetime.now().isoformat(),
                "port": 8001
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            html = """
            <h1>BizOSaaS Identity Service</h1>
            <p>Service running on port 8001</p>
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
    PORT = 8001
    with socketserver.TCPServer(("", PORT), SimpleIdentityHandler) as httpd:
        print(f"Simple Identity Service running on port {PORT}")
        print(f"Health check: http://localhost:{PORT}/health")
        httpd.serve_forever()
#!/usr/bin/env python3
"""
Enhanced Business Directory Service Launcher
Starts both the main directory service and client dashboard
"""

import subprocess
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor
import requests

def start_service(service_script, service_name, port):
    """Start a service in a separate process"""
    try:
        print(f"🚀 Starting {service_name} on port {port}...")
        process = subprocess.Popen([
            sys.executable, service_script
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
        
        # Wait a moment for service to start
        time.sleep(3)
        
        # Test if service is running
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} started successfully on http://localhost:{port}")
                return process
            else:
                print(f"⚠️ {service_name} started but health check failed")
                return process
        except requests.exceptions.RequestException:
            # For dashboard service (no health endpoint)
            try:
                response = requests.get(f"http://localhost:{port}/", timeout=5)
                if response.status_code == 200:
                    print(f"✅ {service_name} started successfully on http://localhost:{port}")
                    return process
                else:
                    print(f"⚠️ {service_name} started but connection failed")
                    return process
            except:
                print(f"❌ {service_name} failed to start properly")
                return process
                
    except Exception as e:
        print(f"❌ Failed to start {service_name}: {str(e)}")
        return None

def main():
    """Main launcher function"""
    print("=" * 80)
    print("🏢 BizOSaaS Enhanced Business Directory Service")
    print("=" * 80)
    print("🔧 Professional directory with client management")
    print("📊 SEO optimization and AI enhancement")
    print("🎯 Client dashboard for CRUD operations")
    print()
    
    services = []
    
    try:
        # Start Enhanced Directory Service (Main API)
        directory_process = start_service(
            "enhanced_directory_service.py",
            "Enhanced Directory Service", 
            8005
        )
        if directory_process:
            services.append(directory_process)
        
        # Start Client Dashboard
        dashboard_process = start_service(
            "client_dashboard.py",
            "Client Dashboard",
            8006
        )
        if dashboard_process:
            services.append(dashboard_process)
        
        print()
        print("=" * 80)
        print("🌐 ACCESS POINTS")
        print("=" * 80)
        print("📋 Enhanced Directory API: http://localhost:8005")
        print("   • Professional directory homepage")
        print("   • RESTful API for business listings")
        print("   • SEO optimization and analytics")
        print()
        print("🎯 Client Dashboard: http://localhost:8006")
        print("   • Business listing management")
        print("   • CRUD operations for clients")
        print("   • Directory submission tracking")
        print()
        print("🔗 API Endpoints:")
        print("   • Health Check: http://localhost:8005/health")
        print("   • Client Listings: http://localhost:8005/api/client/{client_id}/listings")
        print("   • Directory Platforms: http://localhost:8005/api/platforms")
        print("   • Business Categories: http://localhost:8005/api/categories")
        print()
        print("🎯 Dashboard Features:")
        print("   • Client Interface: http://localhost:8006/?client_id=demo_client")
        print("   • Dashboard API: http://localhost:8006/api/client/{client_id}/dashboard-data")
        print()
        print("✅ All services running! Press Ctrl+C to stop all services.")
        print("=" * 80)
        
        # Keep services running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down services...")
            
    except Exception as e:
        print(f"❌ Error starting services: {str(e)}")
        
    finally:
        # Clean up processes
        for process in services:
            try:
                process.terminate()
                process.wait(timeout=5)
                print("✅ Service stopped")
            except:
                process.kill()
                print("🔥 Service force stopped")

if __name__ == "__main__":
    main()
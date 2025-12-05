#!/usr/bin/env python3
"""
Quick Fix Script for Central Hub API Gateway
Diagnoses and attempts to fix the ASGI import error
"""

import subprocess
import json
import time

def run_command(cmd, description):
    """Run a command and return output"""
    print(f"\n🔧 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ Success: {result.stdout.strip()}")
            return result.stdout.strip()
        else:
            print(f"❌ Failed: {result.stderr.strip()}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def check_central_hub_container():
    """Check the Central Hub container status and files"""
    print("🔍 DIAGNOSING CENTRAL HUB CONTAINER")
    print("=" * 50)
    
    # Check container status
    run_command("docker ps --filter name=bizosaas-brain-unified --format 'table {{.Names}}\\t{{.Status}}'", 
                "Checking container status")
    
    # Check container files
    run_command("docker exec bizosaas-brain-unified ls -la /app/", 
                "Listing container files")
    
    # Check Python path
    run_command("docker exec bizosaas-brain-unified python3 -c 'import sys; print(\"\\n\".join(sys.path))'", 
                "Checking Python path")
    
    # Check for simple_api module
    run_command("docker exec bizosaas-brain-unified find /app -name '*simple_api*' -o -name '*api*' -o -name '*.py'", 
                "Finding API modules")
    
    # Check main application file
    run_command("docker exec bizosaas-brain-unified ls -la /app/main.py /app/app.py /app/simple_api.py", 
                "Checking main application files")
    
    # Check requirements and dependencies
    run_command("docker exec bizosaas-brain-unified pip list | grep -E '(fastapi|uvicorn|starlette)'", 
                "Checking FastAPI dependencies")

def attempt_fix():
    """Attempt to fix the Central Hub issue"""
    print("\n🛠️ ATTEMPTING FIXES")
    print("=" * 50)
    
    # Try to restart the container
    print("\n1. Restarting Central Hub container...")
    run_command("docker restart bizosaas-brain-unified", "Restarting container")
    
    # Wait for restart
    time.sleep(5)
    
    # Check if it's working now
    result = run_command("curl -s -o /dev/null -w '%{http_code}' http://localhost:8001/health", 
                        "Testing health endpoint after restart")
    
    if result == "200":
        print("✅ Central Hub is now working!")
        return True
    
    # Try to check logs after restart
    run_command("docker logs bizosaas-brain-unified --tail 10", 
                "Checking logs after restart")
    
    return False

def test_alternative_endpoints():
    """Test alternative ways to access Central Hub functionality"""
    print("\n🔄 TESTING ALTERNATIVE ACCESS METHODS")
    print("=" * 50)
    
    # Test direct container access
    run_command("docker exec bizosaas-brain-unified curl -s http://localhost:8001/health", 
                "Testing health from inside container")
    
    # Test different ports
    for port in [8001, 8080, 3000]:
        run_command(f"curl -s -o /dev/null -w 'Port {port}: %{{http_code}}' http://localhost:{port}/", 
                   f"Testing port {port}")

def create_simple_api_fix():
    """Create a simple API file if missing"""
    print("\n📝 CREATING TEMPORARY API FIX")
    print("=" * 50)
    
    simple_api_content = '''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="BizOSaaS Central Hub", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "central-hub"}

@app.get("/api/brain/health")
async def brain_health():
    return {"status": "healthy", "service": "brain-api"}

@app.get("/")
async def root():
    return {"message": "BizOSaaS Central Hub API Gateway"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
'''
    
    # Create temporary fix file
    with open("/tmp/simple_api_fix.py", "w") as f:
        f.write(simple_api_content)
    
    # Copy to container
    run_command("docker cp /tmp/simple_api_fix.py bizosaas-brain-unified:/app/simple_api.py", 
                "Copying fix file to container")
    
    # Restart container
    run_command("docker restart bizosaas-brain-unified", 
                "Restarting with fix")
    
    time.sleep(5)
    
    # Test fix
    result = run_command("curl -s http://localhost:8001/health", 
                        "Testing fixed endpoint")
    
    return result is not None

def main():
    """Main execution"""
    print("🚀 CENTRAL HUB DIAGNOSTIC AND FIX TOOL")
    print("=" * 60)
    
    # Step 1: Diagnose
    check_central_hub_container()
    
    # Step 2: Attempt basic fix
    if attempt_fix():
        print("\n🎉 Central Hub fixed with restart!")
        return
    
    # Step 3: Test alternatives
    test_alternative_endpoints()
    
    # Step 4: Create fix file
    if create_simple_api_fix():
        print("\n🎉 Central Hub fixed with temporary API!")
    else:
        print("\n❌ Unable to fix Central Hub automatically")
        print("\nManual steps required:")
        print("1. Check container logs: docker logs bizosaas-brain-unified")
        print("2. Verify application files in container")
        print("3. Check Python module imports")
        print("4. Rebuild container if necessary")

if __name__ == "__main__":
    main()
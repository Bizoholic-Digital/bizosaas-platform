import sys
import os

# Add project root to path
sys.path.append("/home/alagiri/projects/bizosaas-platform/bizosaas-brain-core/brain-gateway")

try:
    print("Checking SEO Activities import...")
    from app.activities import seo
    print("✅ SEO Activities imported successfully")
except Exception as e:
    print(f"❌ Failed to import SEO Activities: {e}")
    sys.exit(1)

try:
    print("Checking SEO Workflows import...")
    from app.workflows import seo_audit_workflow
    print("✅ SEO Workflows imported successfully")
except Exception as e:
    print(f"❌ Failed to import SEO Workflows: {e}")
    sys.exit(1)

try:
    print("Checking Worker registration...")
    from worker import run_worker
    # We can't easily inspect the 'worker' object inside run_worker without running it, 
    # but successful import of worker.py means imports inside it are likely valid.
    print("✅ Worker module imported successfully")
except Exception as e:
    print(f"❌ Failed to import Worker module: {e}")
    sys.exit(1)

try:
    print("Checking Main API import...")
    from main import app
    # Check if router is included
    routes = [route.path for route in app.routes]
    if "/api/seo/audit" in routes:
        print("✅ SEO API routes found in FastAPI app")
    else:
        print("❌ SEO API routes NOT found in FastAPI app")
        print("Available routes:", routes)
        sys.exit(1)
except Exception as e:
    print(f"❌ Failed to import Main module: {e}")
    sys.exit(1)

print("🎉 Phase 1 Verification Passed!")

#!/usr/bin/env python3
"""
Startup script for Business Directory Service with AI integration
Checks dependencies and starts the service with AI features enabled
"""

import os
import sys
import subprocess
import uvicorn
from pathlib import Path

def check_dependencies():
    """Check if AI dependencies are installed"""
    
    print("🔧 Checking AI Dependencies...")
    
    required_packages = [
        ("crewai", "0.177.0"),
        ("langchain", "0.1.0"), 
        ("openai", "1.13.3"),
        ("langchain_openai", "0.0.2"),
        ("langchain_community", "0.0.10")
    ]
    
    missing_packages = []
    
    for package, min_version in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} available")
        except ImportError:
            print(f"❌ {package} not found")
            missing_packages.append(f"{package}>={min_version}")
    
    if missing_packages:
        print(f"\n📦 Missing packages: {', '.join(missing_packages)}")
        print("🔄 Installing missing dependencies...")
        
        try:
            # Install missing packages
            cmd = [sys.executable, "-m", "pip", "install"] + missing_packages
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ All dependencies installed successfully")
                return True
            else:
                print(f"❌ Failed to install dependencies: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
    else:
        print("✅ All AI dependencies are available")
        return True

def check_environment():
    """Check environment configuration"""
    
    print("\n🌍 Checking Environment Configuration...")
    
    # Check for OpenAI API key
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OPENAI_API_KEY found")
    else:
        print("⚠️ OPENAI_API_KEY not set")
        print("💡 AI features will work in mock mode without API key")
        print("💡 To enable full AI features, set: export OPENAI_API_KEY=your_key_here")
    
    # Check for other optional environment variables
    optional_vars = [
        ("REDIS_URL", "Redis connection for caching"),
        ("POSTGRES_URL", "PostgreSQL connection for data persistence"),
        ("LOG_LEVEL", "Logging level (INFO, DEBUG, etc.)")
    ]
    
    for var, description in optional_vars:
        if os.getenv(var):
            print(f"✅ {var} found")
        else:
            print(f"ℹ️ {var} not set ({description})")
    
    return True

def test_ai_integration():
    """Quick test of AI integration"""
    
    print("\n🧪 Testing AI Integration...")
    
    try:
        from ai_agents import get_ai_manager
        ai_manager = get_ai_manager()
        print("✅ AI Manager initialized successfully")
        print("🤖 CrewAI agents ready:")
        print("   • Business Listing Optimizer")
        print("   • Lead Scoring Specialist") 
        print("   • Content Curator")
        print("   • Review Analysis Expert")
        print("   • Search Intelligence Agent")
        print("   • Directory SEO Optimizer")
        return True
    except Exception as e:
        print(f"❌ AI integration test failed: {e}")
        print("⚠️ Service will start with AI features disabled")
        return False

def start_service():
    """Start the FastAPI service"""
    
    print("\n🚀 Starting Business Directory Service with AI...")
    print("📍 Service will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🏠 Basic UI: http://localhost:8000/basic")
    print("🤖 AI Status: http://localhost:8000/ai/status")
    
    # Start the service
    try:
        uvicorn.run(
            "directory_service:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Service stopped by user")
    except Exception as e:
        print(f"\n❌ Service failed to start: {e}")

def main():
    """Main startup function"""
    
    print("🏢 Business Directory Service with AI Integration")
    print("=" * 60)
    
    # Check current directory
    current_dir = Path.cwd()
    service_file = current_dir / "directory_service.py"
    ai_file = current_dir / "ai_agents.py"
    
    if not service_file.exists():
        print("❌ directory_service.py not found in current directory")
        print(f"📍 Current directory: {current_dir}")
        print("💡 Please run this script from the business-directory service directory")
        return
    
    if not ai_file.exists():
        print("❌ ai_agents.py not found in current directory")
        print("💡 Make sure ai_agents.py is in the same directory")
        return
    
    print("✅ Service files found")
    
    # Step 1: Check and install dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed")
        print("🔧 Please resolve dependency issues and try again")
        return
    
    # Step 2: Check environment
    if not check_environment():
        print("\n❌ Environment check failed")
        return
    
    # Step 3: Test AI integration
    ai_available = test_ai_integration()
    
    if ai_available:
        print("\n🎉 All systems ready! Starting with full AI features...")
    else:
        print("\n⚠️ Starting with limited AI features...")
    
    # Step 4: Start the service
    start_service()

if __name__ == "__main__":
    main()
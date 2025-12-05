#!/usr/bin/env python3
"""Health check script for monitoring service"""

import requests
import sys
import json

def main():
    try:
        response = requests.get("http://localhost:8090/health", timeout=5)
        if response.status_code == 200:
            print("✅ Monitoring service is healthy")
            sys.exit(0)
        else:
            print(f"❌ Monitoring service returned status {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Monitoring service health check failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
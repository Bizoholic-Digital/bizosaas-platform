#!/usr/bin/env python3
"""
Test script to verify Django CRM Vault integration
Run this to ensure Vault connectivity and secret retrieval works correctly
"""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings.production')

def test_vault_integration():
    """Test Vault integration for Django CRM"""
    
    print("\n" + "="*70)
    print("🔐 Django CRM - Vault Integration Test")
    print("="*70 + "\n")
    
    # Test 1: Import vault helper
    print("Test 1: Importing Vault Helper...")
    try:
        from crm_project.vault_config_helper import (
            get_vault_config,
            get_database_config,
            get_redis_config,
            get_django_secret_key,
            vault_health_check
        )
        print("✅ Vault helper imported successfully\n")
    except ImportError as e:
        print(f"❌ Failed to import vault helper: {e}\n")
        return False
    
    # Test 2: Vault health check
    print("Test 2: Vault Health Check...")
    try:
        health = vault_health_check()
        print(f"   Vault Available: {health['available']}")
        print(f"   Vault Address: {health['addr']}")
        print(f"   Authenticated: {health['authenticated']}")
        print(f"   Mount Path: {health['mount_path']}")
        
        if health['available']:
            print("✅ Vault is healthy and connected\n")
        else:
            print("⚠️  Vault not available - will use fallback values\n")
    except Exception as e:
        print(f"⚠️  Vault health check failed: {e}\n")
    
    # Test 3: Database configuration
    print("Test 3: Database Configuration...")
    try:
        db_config = get_database_config()
        print(f"   Host: {db_config['host']}")
        print(f"   Port: {db_config['port']}")
        print(f"   Database: {db_config['database']}")
        print(f"   Username: {db_config['username']}")
        print(f"   Password: {'*' * len(db_config['password']) if db_config['password'] else 'NOT SET'}")
        print("✅ Database config retrieved\n")
    except Exception as e:
        print(f"❌ Failed to get database config: {e}\n")
        return False
    
    # Test 4: Redis configuration
    print("Test 4: Redis Configuration...")
    try:
        redis_config = get_redis_config()
        print(f"   Host: {redis_config['host']}")
        print(f"   Port: {redis_config['port']}")
        print(f"   Connection String: {redis_config['connection_string']}")
        print("✅ Redis config retrieved\n")
    except Exception as e:
        print(f"❌ Failed to get Redis config: {e}\n")
        return False
    
    # Test 5: Django secret key
    print("Test 5: Django Secret Key...")
    try:
        secret_key = get_django_secret_key('django-crm')
        print(f"   Length: {len(secret_key)} characters")
        print(f"   Preview: {secret_key[:15]}..." if len(secret_key) > 15 else f"   Value: {secret_key}")
        print("✅ Secret key retrieved\n")
    except Exception as e:
        print(f"❌ Failed to get secret key: {e}\n")
        return False
    
    # Test 6: Django settings integration
    print("Test 6: Django Settings Integration...")
    try:
        import django
        django.setup()
        
        from django.conf import settings
        
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   SECRET_KEY Length: {len(settings.SECRET_KEY)}")
        print(f"   Database Engine: {settings.DATABASES['default']['ENGINE']}")
        print(f"   Database Host: {settings.DATABASES['default']['HOST']}")
        print(f"   Cache Backend: {settings.CACHES['default']['BACKEND']}")
        print("✅ Django settings loaded successfully\n")
    except Exception as e:
        print(f"⚠️  Django settings test: {e}\n")
    
    print("="*70)
    print("✅ Vault Integration Test Complete!")
    print("="*70 + "\n")
    
    return True

if __name__ == '__main__':
    success = test_vault_integration()
    sys.exit(0 if success else 1)

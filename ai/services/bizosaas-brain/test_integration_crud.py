#!/usr/bin/env python3
"""
Test script for Integration CRUD endpoints
"""

import json
import requests
import time

BASE_URL = "http://localhost:8001/api"

def test_integration_crud():
    """Test all CRUD operations for integrations"""
    
    print("🧪 Testing Integration CRUD Endpoints")
    print("=" * 50)
    
    # Test CREATE integration
    print("\n1️⃣ Testing CREATE Integration")
    create_data = {
        "name": "Test Custom Integration",
        "category": "custom",
        "description": "A test integration created via API",
        "features": ["Data Sync", "Webhooks", "Analytics"],
        "setupType": "manual",
        "priority": "high",
        "config": {
            "endpoint": "https://api.example.com",
            "timeout": 30
        },
        "automationCapabilities": ["Auto-sync", "Error recovery"],
        "aiFeatures": ["Smart insights", "Predictive analysis"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/integrations", json=create_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            create_result = response.json()
            print(f"✅ Integration created: {create_result['integration']['name']}")
            integration_id = create_result['integration']['id']
        else:
            print(f"❌ Create failed: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Connection refused - Brain API not running on port 8001")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Test READ integration
    print("\n2️⃣ Testing READ Integrations")
    try:
        response = requests.get(f"{BASE_URL}/integrations")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            integrations = response.json()
            print(f"✅ Found {len(integrations)} integrations")
            for integration in integrations[:3]:  # Show first 3
                print(f"  - {integration['name']} ({integration['status']})")
        else:
            print(f"❌ Read failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test UPDATE integration
    print("\n3️⃣ Testing UPDATE Integration")
    update_data = {
        "name": "Updated Test Integration",
        "description": "Updated description via API",
        "priority": "medium",
        "features": ["Data Sync", "Webhooks", "Analytics", "Reporting"]
    }
    
    try:
        response = requests.put(f"{BASE_URL}/integrations/{integration_id}", json=update_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            update_result = response.json()
            print(f"✅ Integration updated: {update_result['integration_id']}")
            print(f"  Updated fields: {list(update_result['updated_fields'].keys())}")
        else:
            print(f"❌ Update failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test DUPLICATE integration
    print("\n4️⃣ Testing DUPLICATE Integration")
    duplicate_data = {
        "name": "Duplicate Test Integration",
        "category": "custom",
        "config": {"endpoint": "https://api.duplicate.com"}
    }
    
    try:
        response = requests.post(f"{BASE_URL}/integrations/{integration_id}/duplicate", json=duplicate_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            duplicate_result = response.json()
            print(f"✅ Integration duplicated: {duplicate_result['new_integration']['name']}")
            duplicate_id = duplicate_result['new_integration']['id']
        else:
            print(f"❌ Duplicate failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test TEMPLATES
    print("\n5️⃣ Testing Integration Templates")
    try:
        response = requests.get(f"{BASE_URL}/integrations/templates")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            templates_result = response.json()
            print(f"✅ Found {templates_result['count']} templates")
            for template in templates_result['templates']:
                print(f"  - {template['name']} ({template['category']})")
        else:
            print(f"❌ Templates failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test CREATE from template
    print("\n6️⃣ Testing CREATE from Template")
    template_data = {
        "name": "Social Media Integration from Template",
        "config": {
            "category": "social",
            "platform": "instagram",
            "features": ["Post Scheduling", "Analytics"]
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/integrations/templates/template-social-media/create", json=template_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            template_result = response.json()
            print(f"✅ Integration created from template: {template_result['integration']['name']}")
            template_integration_id = template_result['integration']['id']
        else:
            print(f"❌ Template creation failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test BATCH operations
    print("\n7️⃣ Testing BATCH Operations")
    batch_data = {
        "operation": "connect",
        "integration_ids": [integration_id, duplicate_id if 'duplicate_id' in locals() else "dummy-id"],
        "params": {"test": True}
    }
    
    try:
        response = requests.post(f"{BASE_URL}/integrations/batch", json=batch_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            batch_result = response.json()
            print(f"✅ Batch operation completed:")
            print(f"  - Total requested: {batch_result['total_requested']}")
            print(f"  - Successful: {batch_result['successful']}")
            print(f"  - Failed: {batch_result['failed']}")
        else:
            print(f"❌ Batch operation failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test DELETE integration (only custom ones)
    print("\n8️⃣ Testing DELETE Integration")
    try:
        response = requests.delete(f"{BASE_URL}/integrations/{integration_id}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            delete_result = response.json()
            print(f"✅ Integration deleted: {delete_result['integration_id']}")
            print(f"  Cleanup performed: {len(delete_result['cleanup_performed'])} tasks")
        else:
            print(f"❌ Delete failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test DELETE system integration (should fail)
    print("\n9️⃣ Testing DELETE System Integration (Should Fail)")
    try:
        response = requests.delete(f"{BASE_URL}/integrations/google-analytics-4")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 400:
            print(f"✅ Correctly prevented deletion of system integration")
        else:
            print(f"❌ Should have prevented system integration deletion")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 50)
    print("🎉 Integration CRUD Testing Complete!")

if __name__ == "__main__":
    test_integration_crud()
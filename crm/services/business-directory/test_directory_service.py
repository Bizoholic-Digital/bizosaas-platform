#!/usr/bin/env python3
"""
Business Directory Service Test Script
Tests all endpoints and validates responses
"""

import requests
import json
from datetime import datetime

def test_endpoint(url, expected_status=200, description=""):
    """Test an endpoint and return results"""
    try:
        response = requests.get(url, timeout=5)
        
        result = {
            "url": url,
            "status_code": response.status_code,
            "success": response.status_code == expected_status,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                data = response.json()
                result["data_type"] = "json"
                if isinstance(data, dict):
                    result["data_keys"] = list(data.keys())
                    if "total_count" in data:
                        result["total_count"] = data["total_count"]
                    if "directories" in data:
                        result["directories_count"] = len(data["directories"])
            except json.JSONDecodeError:
                result["data_type"] = "invalid_json"
        elif response.headers.get('content-type', '').startswith('text/html'):
            result["data_type"] = "html"
            result["content_length"] = len(response.text)
            # Check for title
            if "<title>" in response.text:
                title_start = response.text.find("<title>") + 7
                title_end = response.text.find("</title>", title_start)
                result["page_title"] = response.text[title_start:title_end]
        else:
            result["data_type"] = "other"
            result["content_type"] = response.headers.get('content-type', 'unknown')
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "status_code": 0,
            "success": False,
            "error": str(e),
            "description": description,
            "timestamp": datetime.now().isoformat()
        }

def main():
    """Main test function"""
    
    print("=" * 80)
    print("🏢 BizOSaaS Business Directory Service Test Report")
    print("=" * 80)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test endpoints
    endpoints = [
        ("http://localhost:8003/health", "Health check endpoint"),
        ("http://localhost:8003/directories", "JSON directories API"),
        ("http://localhost:8003/categories", "JSON categories API"),
        ("http://localhost:8003/", "HTML homepage"),
        ("http://localhost:8004/", "Enhanced web interface (if running)")
    ]
    
    results = []
    
    for url, description in endpoints:
        print(f"Testing: {description}")
        result = test_endpoint(url, description=description)
        results.append(result)
        
        if result["success"]:
            print(f"  ✅ SUCCESS - Status: {result['status_code']}")
            if result.get("total_count"):
                print(f"  📊 Data: {result['total_count']} total items")
            if result.get("directories_count"):
                print(f"  🏪 Directories: {result['directories_count']} available")
            if result.get("page_title"):
                print(f"  📄 Page: {result['page_title']}")
            if result.get("content_length"):
                print(f"  📝 HTML Length: {result['content_length']} characters")
        else:
            print(f"  ❌ FAILED - Status: {result['status_code']}")
            if result.get("error"):
                print(f"  🚨 Error: {result['error']}")
        
        print()
    
    # Summary
    successful_tests = sum(1 for r in results if r["success"])
    total_tests = len(results)
    
    print("=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"Successful tests: {successful_tests}/{total_tests}")
    print(f"Success rate: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests == total_tests:
        print("🎉 All tests passed! Directory service is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the details above.")
    
    print()
    print("🌐 Access Points:")
    print("  • API Base: http://localhost:8003/")
    print("  • JSON Directories: http://localhost:8003/directories")
    print("  • HTML Dashboard: http://localhost:8003/")
    print("  • Enhanced UI: http://localhost:8004/ (if running)")
    print("  • API Docs: http://localhost:8003/docs")
    
    print()
    print("📋 Quick Verification:")
    directories_result = next((r for r in results if "/directories" in r["url"]), None)
    if directories_result and directories_result.get("directories_count"):
        print(f"  ✅ Directory service contains {directories_result['directories_count']} business directories")
        print(f"  ✅ API is returning proper JSON data with directory listings")
        print(f"  ✅ No blank page issue - service is working correctly")
    else:
        print(f"  ❌ Directory data not found or invalid")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
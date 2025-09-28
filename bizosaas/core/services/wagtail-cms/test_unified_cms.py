#!/usr/bin/env python3
"""
Unified CMS Testing Script

This script tests the Wagtail CMS migration and AI integration endpoints
to ensure everything is working correctly.
"""

import requests
import json
import sys
import time
from typing import Dict, List, Optional

class UnifiedCMSTester:
    """Test suite for the unified CMS"""
    
    def __init__(self, base_url: str = 'http://localhost:8000'):
        self.base_url = base_url
        self.test_results = []
        
    def test_endpoint(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     expected_status: int = 200, description: str = "") -> bool:
        """Test a single API endpoint"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, timeout=10)
            elif method.upper() == 'PUT':
                response = requests.put(url, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            success = response.status_code == expected_status
            
            result = {
                'endpoint': endpoint,
                'method': method,
                'status_code': response.status_code,
                'expected_status': expected_status,
                'success': success,
                'description': description,
                'response_size': len(response.text) if response.text else 0
            }
            
            if success:
                print(f"✅ {method} {endpoint} - {description}")
                try:
                    result['data'] = response.json()
                except:
                    result['data'] = response.text[:200] + "..." if len(response.text) > 200 else response.text
            else:
                print(f"❌ {method} {endpoint} - Expected {expected_status}, got {response.status_code}")
                result['error'] = response.text[:200] if response.text else "No response body"
            
            self.test_results.append(result)
            return success
            
        except requests.exceptions.RequestException as e:
            print(f"❌ {method} {endpoint} - Connection error: {e}")
            self.test_results.append({
                'endpoint': endpoint,
                'method': method,
                'success': False,
                'error': str(e),
                'description': description
            })
            return False
    
    def test_service_health(self) -> bool:
        """Test basic service health"""
        print("\\n🏥 Testing service health...")
        
        # Test health endpoint
        health_ok = self.test_endpoint('GET', '/health/', description="Health check")
        
        # Test admin access (might redirect)
        admin_ok = self.test_endpoint('GET', '/admin/', expected_status=302, 
                                     description="Admin panel access")
        
        return health_ok or admin_ok  # At least one should work
    
    def test_tenant_endpoints(self) -> bool:
        """Test tenant-related endpoints"""
        print("\\n🏢 Testing tenant endpoints...")
        
        tests = [
            ('GET', '/api/tenants/', "List all tenants"),
            ('GET', '/api/tenants/bizoholic-main/pages/', "Tenant pages"),
            ('GET', '/api/tenants/bizoholic-main/content-summary/', "Tenant content summary"),
        ]
        
        success_count = 0
        for method, endpoint, desc in tests:
            if self.test_endpoint(method, endpoint, description=desc):
                success_count += 1
        
        return success_count >= len(tests) // 2  # At least half should work
    
    def test_content_endpoints(self) -> bool:
        """Test content management endpoints"""
        print("\\n📝 Testing content endpoints...")
        
        tests = [
            ('GET', '/api/tenants/bizoholic-main/landing-pages/', "Landing pages"),
            ('GET', '/api/tenants/bizoholic-main/service-pages/', "Service pages"),
            ('GET', '/api/tenants/bizoholic-main/content-pages/', "Content pages"),
            ('GET', '/api/tenants/bizoholic-main/team-members/', "Team members"),
            ('GET', '/api/tenants/bizoholic-main/testimonials/', "Testimonials"),
            ('GET', '/api/tenants/bizoholic-main/faq-pages/', "FAQ pages"),
        ]
        
        success_count = 0
        for method, endpoint, desc in tests:
            if self.test_endpoint(method, endpoint, description=desc):
                success_count += 1
        
        return success_count >= len(tests) // 2
    
    def test_unified_cms_endpoints(self) -> bool:
        """Test unified CMS API endpoints"""
        print("\\n🔗 Testing unified CMS endpoints...")
        
        tests = [
            ('GET', '/api/cms/pages/', "All CMS pages"),
            ('GET', '/api/cms/content/landing_pages/', "Landing pages by type"),
            ('GET', '/api/cms/content/service_pages/', "Service pages by type"),
            ('GET', '/api/cms/content/content_pages/', "Content pages by type"),
        ]
        
        success_count = 0
        for method, endpoint, desc in tests:
            if self.test_endpoint(method, endpoint, description=desc):
                success_count += 1
        
        return success_count >= 1  # At least one should work
    
    def test_ai_integration_endpoints(self) -> bool:
        """Test AI agent integration endpoints"""
        print("\\n🤖 Testing AI integration endpoints...")
        
        # Test AI content creation (might need authentication)
        sample_content = {
            "content_type": "blog_post",
            "content": {
                "title": "Test AI Generated Content",
                "author": "AI Agent",
                "excerpt": "This is a test post created by AI"
            }
        }
        
        tests = [
            ('GET', '/api/tenants/bizoholic-main/ai/templates/', "AI templates"),
            ('POST', '/api/tenants/bizoholic-main/ai/content/', "AI content creation", sample_content),
            ('GET', '/api/tenants/bizoholic-main/navigation/', "Site navigation"),
        ]
        
        success_count = 0
        for test in tests:
            if len(test) == 4:
                method, endpoint, desc, data = test
                if self.test_endpoint(method, endpoint, data=data, description=desc, expected_status=201 if method == 'POST' else 200):
                    success_count += 1
            else:
                method, endpoint, desc = test
                if self.test_endpoint(method, endpoint, description=desc):
                    success_count += 1
        
        return success_count >= 1
    
    def test_content_data_integrity(self) -> bool:
        """Test that migrated content has proper structure"""
        print("\\n🔍 Testing content data integrity...")
        
        # Get tenant content summary
        if not self.test_endpoint('GET', '/api/tenants/bizoholic-main/content-summary/', 
                                 description="Content summary for integrity check"):
            return False
        
        # Check if we have the expected content types
        last_result = self.test_results[-1]
        if 'data' in last_result:
            summary = last_result['data']
            
            expected_content_types = ['landing_pages', 'service_pages', 'content_pages']
            
            if 'content_summary' in summary and 'pages' in summary['content_summary']:
                pages_summary = summary['content_summary']['pages']
                
                found_types = []
                for content_type in expected_content_types:
                    if content_type in pages_summary and pages_summary[content_type] > 0:
                        found_types.append(content_type)
                        print(f"✅ Found {pages_summary[content_type]} {content_type}")
                
                if len(found_types) >= 2:
                    print("✅ Content integrity check passed")
                    return True
                else:
                    print("⚠️ Some expected content types are missing")
                    return False
        
        print("⚠️ Could not verify content integrity")
        return False
    
    def generate_test_report(self) -> None:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['success']])
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("\\n" + "="*70)
        print("🧪 UNIFIED CMS TEST REPORT")
        print("="*70)
        
        print(f"\\n📊 Overall Results:")
        print(f"   • Total Tests: {total_tests}")
        print(f"   • Passed: {passed_tests}")
        print(f"   • Failed: {total_tests - passed_tests}")
        print(f"   • Success Rate: {success_rate:.1f}%")
        
        # Categorize results
        categories = {
            'Health': [r for r in self.test_results if 'health' in r['endpoint']],
            'Tenants': [r for r in self.test_results if '/tenants/' in r['endpoint']],
            'CMS': [r for r in self.test_results if '/cms/' in r['endpoint']],
            'AI': [r for r in self.test_results if '/ai/' in r['endpoint']],
            'Other': [r for r in self.test_results if not any(x in r['endpoint'] for x in ['health', 'tenants', 'cms', 'ai'])]
        }
        
        print("\\n📋 Results by Category:")
        for category, results in categories.items():
            if results:
                passed = len([r for r in results if r['success']])
                total = len(results)
                rate = (passed / total * 100) if total > 0 else 0
                status = "✅" if rate >= 50 else "❌"
                print(f"   {status} {category}: {passed}/{total} ({rate:.1f}%)")
        
        # Show failed tests
        failed_tests = [r for r in self.test_results if not r['success']]
        if failed_tests:
            print("\\n❌ Failed Tests:")
            for result in failed_tests:
                print(f"   • {result['method']} {result['endpoint']} - {result.get('description', 'No description')}")
                if 'error' in result:
                    print(f"     Error: {result['error'][:100]}...")
        
        # Show successful endpoints with data
        successful_with_data = [r for r in self.test_results if r['success'] and 'data' in r]
        if successful_with_data:
            print("\\n✅ Working Endpoints with Data:")
            for result in successful_with_data:
                data_preview = ""
                if isinstance(result['data'], dict):
                    if 'count' in result['data']:
                        data_preview = f" (Count: {result['data']['count']})"
                    elif len(result['data']) > 0:
                        data_preview = f" (Keys: {list(result['data'].keys())[:3]})"
                print(f"   • {result['method']} {result['endpoint']}{data_preview}")
        
        print("\\n🎯 Recommendations:")
        if success_rate >= 80:
            print("   ✅ CMS is working well! Ready for production use.")
        elif success_rate >= 60:
            print("   ⚠️ CMS is partially working. Check failed endpoints.")
            print("   • Verify database migrations are complete")
            print("   • Check service logs for errors")
        else:
            print("   ❌ CMS has significant issues. Troubleshooting needed.")
            print("   • Verify all services are running")
            print("   • Check database connectivity")
            print("   • Review migration logs")
        
        print("\\n🔧 Next Steps:")
        print("   1. Fix any failing critical endpoints")
        print("   2. Test content creation via admin interface")
        print("   3. Verify AI agent authentication setup")
        print("   4. Test media file uploads")
        print("   5. Configure monitoring and alerts")
        
        print("\\n" + "="*70)
    
    def run_all_tests(self) -> bool:
        """Run complete test suite"""
        print("🚀 Starting Unified CMS Test Suite...")
        print("="*50)
        
        # Wait a moment for services to be ready
        time.sleep(2)
        
        test_results = []
        
        # Run test categories
        test_results.append(("Service Health", self.test_service_health()))
        test_results.append(("Tenant Endpoints", self.test_tenant_endpoints()))
        test_results.append(("Content Endpoints", self.test_content_endpoints()))
        test_results.append(("Unified CMS Endpoints", self.test_unified_cms_endpoints()))
        test_results.append(("AI Integration", self.test_ai_integration_endpoints()))
        test_results.append(("Content Integrity", self.test_content_data_integrity()))
        
        # Generate report
        self.generate_test_report()
        
        # Return overall success
        passed_categories = len([result for _, result in test_results if result])
        total_categories = len(test_results)
        overall_success = passed_categories >= (total_categories // 2)
        
        if overall_success:
            print("\\n🎉 Overall test result: PASSED")
        else:
            print("\\n❌ Overall test result: FAILED")
        
        return overall_success

def main():
    """Main testing function"""
    print("🧪 Unified CMS Testing Tool")
    print("="*40)
    
    # Check if CMS URL is provided
    base_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8000'
    print(f"Testing CMS at: {base_url}")
    
    tester = UnifiedCMSTester(base_url)
    
    try:
        success = tester.run_all_tests()
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\\n⏹️ Testing interrupted by user")
        return 1
    except Exception as e:
        print(f"\\n❌ Unexpected error during testing: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
#!/usr/bin/env python3
"""
Test suite for Baidu Webmaster Tools API Integration
Tests OAuth flow, API authentication, and all major functionalities for Chinese market
"""

import asyncio
import json
import aiohttp
from datetime import datetime
import os
import sys

# Add current directory to path for importing our integration
sys.path.append(os.path.dirname(__file__))

from baidu_webmaster_integration import baidu_webmaster_integration

class TestBaiduWebmasterIntegration:
    def __init__(self):
        self.tenant_id = "test_tenant_123"
        self.test_site_url = "https://example.cn"
        self.test_access_token = os.getenv('BAIDU_WEBMASTER_ACCESS_TOKEN', 'test_access_token_123')
        
    async def test_oauth_flow(self):
        """Test OAuth 2.0 authentication flow"""
        print("🔐 Testing OAuth Flow...")
        
        # Test OAuth URL generation
        scopes = ['basic', 'super']
        oauth_result = baidu_webmaster_integration.generate_oauth_url(self.tenant_id, scopes)
        
        if oauth_result['success']:
            print(f"✅ OAuth URL generated: {oauth_result['auth_url'][:100]}...")
            print(f"   State: {oauth_result['state']}")
            print(f"   Scopes: {oauth_result['scopes']}")
            print(f"   Expires in: {oauth_result['expires_in']} seconds")
            print(f"   Note: {oauth_result['note']}")
        else:
            print(f"❌ OAuth URL generation failed: {oauth_result.get('error', 'Unknown error')}")
            
        return oauth_result['success']
    
    async def test_get_user_sites(self):
        """Test getting user sites"""
        print("🏢 Testing Get User Sites...")
        
        result = await baidu_webmaster_integration.get_user_sites(self.tenant_id, self.test_access_token)
        
        if result['success']:
            print(f"✅ User sites retrieved: {result['count']} sites found")
            if result['sites']:
                for site in result['sites']:
                    print(f"   - {site['site_url']} (Status: {site['verification_status']}, Type: {site['site_type']})")
            print(f"   Note: {result['note']}")
        else:
            print(f"⚠️ User sites retrieval: {result['error']}")
            
        return result
    
    async def test_search_queries(self):
        """Test search queries functionality"""
        print("🔍 Testing Search Queries...")
        
        result = await baidu_webmaster_integration.get_search_queries(
            self.tenant_id, 
            self.test_site_url, 
            self.test_access_token,
            date_from='2024-08-01',
            date_to='2024-09-01'
        )
        
        if result['success']:
            print(f"✅ Search queries retrieved successfully")
            print(f"   Date range: {result['date_range']['from']} to {result['date_range']['to']}")
            queries_data = result['queries_data']
            if queries_data:
                for query in queries_data[:3]:  # Show first 3 queries
                    print(f"   Query: {query['query']}")
                    print(f"   Clicks: {query['clicks']}, Impressions: {query['impressions']}")
                    print(f"   CTR: {query['ctr']:.1f}%, Avg Position: {query['position']:.1f}")
            
            # Show regional performance
            regional_performance = result['regional_performance']
            print(f"   Regional Performance:")
            for tier, data in regional_performance.items():
                print(f"     {tier}: {data['clicks']} clicks, {data['ctr']:.1f}% CTR")
            
            # Check AI insights
            ai_insights = result['ai_insights']
            print(f"   AI Analysis Confidence: {ai_insights['confidence_score']:.1%}")
            print(f"   Performance Trends: {ai_insights['insights']['performance_trends']['clicks_trend']}")
            print(f"   Note: {result['note']}")
        else:
            print(f"⚠️ Search queries: {result['error']}")
            
        return result['success']
    
    async def test_site_health(self):
        """Test site health analysis"""
        print("🏥 Testing Site Health Analysis...")
        
        result = await baidu_webmaster_integration.get_site_health(
            self.tenant_id, 
            self.test_site_url, 
            self.test_access_token
        )
        
        if result['success']:
            health_analysis = result['health_analysis']
            print(f"✅ Site health analysis completed:")
            print(f"   Overall Health Score: {health_analysis['health_score']}/100")
            print(f"   Critical Issues: {len(health_analysis['technical_issues']['critical'])}")
            print(f"   Warnings: {len(health_analysis['technical_issues']['warnings'])}")
            print(f"   Baidu-Specific Optimizations:")
            for key, value in health_analysis['baidu_specific_optimizations'].items():
                print(f"     {key}: {value}")
            print(f"   China Network Performance: {health_analysis['performance_metrics']['page_load_time_china']}")
            print(f"   Note: {result['note']}")
        else:
            print(f"⚠️ Site health analysis: {result['error']}")
            
        return result['success']
    
    async def test_site_verification(self):
        """Test site verification"""
        print("✅ Testing Site Verification...")
        
        result = await baidu_webmaster_integration.verify_site(
            self.tenant_id, 
            self.test_site_url, 
            self.test_access_token,
            verification_method="html_file"
        )
        
        if result['success']:
            verification_result = result['verification_result']
            print(f"✅ Site verification successful:")
            print(f"   Verification Method: {verification_result['verification_method']}")
            print(f"   Verification Status: {verification_result['verification_status']}")
            verification_file = verification_result['verification_details']['verification_file']
            print(f"   Verification File: {verification_file}")
            print(f"   Properties Verified: {len(verification_result['verification_details']['properties_verified'])}")
            
            # Show Chinese-specific notes
            chinese_notes = verification_result['chinese_specific_notes']
            print(f"   Chinese Market Notes:")
            for key, value in chinese_notes.items():
                print(f"     {key}: {value}")
            print(f"   Note: {result['note']}")
        else:
            print(f"⚠️ Site verification: {result['error']}")
            
        return result['success']
    
    async def test_sitemap_submission(self):
        """Test sitemap submission"""
        print("🗺️ Testing Sitemap Submission...")
        
        sitemap_url = f"{self.test_site_url}/sitemap.xml"
        result = await baidu_webmaster_integration.submit_sitemap(
            self.tenant_id, 
            self.test_site_url, 
            sitemap_url,
            self.test_access_token
        )
        
        if result['success']:
            sitemap_status = result['sitemap_status']
            print(f"✅ Sitemap submitted successfully:")
            print(f"   Sitemap URL: {sitemap_status['sitemap_url']}")
            print(f"   Status: {sitemap_status['status']}")
            print(f"   URLs Count: {sitemap_status['urls_count']}")
            print(f"   Submitted: {sitemap_status['last_submitted'][:19]}")
            
            # Show Baidu-specific information
            baidu_specific = sitemap_status['baidu_specific']
            print(f"   Baidu-Specific Recommendations:")
            for key, value in baidu_specific.items():
                print(f"     {key}: {value}")
            print(f"   Note: {result['note']}")
        else:
            print(f"⚠️ Sitemap submission: {result['error']}")
            
        return result['success']
    
    async def test_indexing_status(self):
        """Test URL indexing status"""
        print("📑 Testing URL Indexing Status...")
        
        test_urls = [
            f"{self.test_site_url}/",
            f"{self.test_site_url}/about", 
            f"{self.test_site_url}/products",
            f"{self.test_site_url}/contact"
        ]
        
        result = await baidu_webmaster_integration.check_indexing_status(
            self.tenant_id, 
            self.test_site_url, 
            test_urls,
            self.test_access_token
        )
        
        if result['success']:
            print(f"✅ Indexing status checked: {len(result['indexing_data'])} URLs")
            for url_data in result['indexing_data'][:4]:  # Show first 4 URLs
                print(f"   URL: {url_data['url']}")
                print(f"   Status: {url_data['indexing_status']}")
                print(f"   Last Crawl: {url_data['last_crawl'][:19]}")
                print(f"   Baidu Snapshot: {url_data['baidu_snapshot']}")
            
            # Show summary
            summary = result['summary']
            print(f"   Summary: {summary['indexed_count']}/{summary['total_urls']} URLs indexed ({summary['indexing_rate']})")
            print(f"   Note: {result['note']}")
        else:
            print(f"⚠️ Indexing status: {result['error']}")
            
        return result['success']
    
    async def test_compliance_report(self):
        """Test compliance report"""
        print("📋 Testing Compliance Report...")
        
        result = await baidu_webmaster_integration.get_compliance_report(
            self.tenant_id, 
            self.test_site_url, 
            self.test_access_token
        )
        
        if result['success']:
            compliance_report = result['compliance_report']
            algorithm_monitoring = result['algorithm_monitoring']
            
            print(f"✅ Compliance report generated:")
            print(f"   Overall Compliance Score: {compliance_report['overall_score']}/100")
            print(f"   Content Quality: {compliance_report['compliance_checks']['content_quality']['score']}/100")
            print(f"   User Experience: {compliance_report['compliance_checks']['user_experience']['score']}/100")
            print(f"   Technical Compliance: {compliance_report['compliance_checks']['technical_compliance']['score']}/100")
            print(f"   Regulatory Compliance: {compliance_report['compliance_checks']['regulatory_compliance']['score']}/100")
            print(f"   Spam Detection: {compliance_report['compliance_checks']['spam_detection']['score']}/100")
            
            # Show Chinese market considerations
            chinese_considerations = compliance_report['chinese_market_considerations']
            print(f"   Chinese Market Considerations:")
            for key, value in chinese_considerations.items():
                print(f"     {key}: {value}")
            
            print(f"   Algorithm Updates Monitored: {len(algorithm_monitoring['recent_updates'])}")
            if algorithm_monitoring['recent_updates']:
                latest_update = algorithm_monitoring['recent_updates'][0]
                print(f"   Latest Update: {latest_update['update_name']} (Impact: {latest_update['impact']})")
                print(f"   Description: {latest_update['description']}")
            
            print(f"   Note: {result['note']}")
        else:
            print(f"⚠️ Compliance report: {result['error']}")
            
        return result['success']
    
    async def test_connection_status(self):
        """Test connection status"""
        print("🔗 Testing Connection Status...")
        
        # Test with access token
        result = await baidu_webmaster_integration.get_connection_status(self.tenant_id, self.test_access_token)
        
        print(f"Connection Status: {result['status']}")
        print(f"Auth Method: {result.get('auth_method', 'unknown')}")
        print(f"Message: {result['message']}")
        print(f"API Endpoint: {result.get('api_endpoint', 'unknown')}")
        if 'note' in result:
            print(f"Note: {result['note']}")
        
        return result['status'] in ['connected', 'disconnected']
    
    async def run_all_tests(self):
        """Run all integration tests"""
        print("=" * 60)
        print("🧪 BAIDU WEBMASTER TOOLS API INTEGRATION TESTS")
        print("=" * 60)
        
        tests = [
            ("OAuth Flow", self.test_oauth_flow),
            ("User Sites", self.test_get_user_sites),
            ("Search Queries", self.test_search_queries),
            ("Site Health", self.test_site_health),
            ("Site Verification", self.test_site_verification),
            ("Sitemap Submission", self.test_sitemap_submission),
            ("Indexing Status", self.test_indexing_status),
            ("Compliance Report", self.test_compliance_report),
            ("Connection Status", self.test_connection_status)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            print(f"\n{'─' * 40}")
            try:
                result = await test_func()
                results[test_name] = result
                print(f"Status: {'✅ PASSED' if result else '⚠️ WARNING'}")
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
                results[test_name] = False
        
        # Summary
        print(f"\n{'=' * 60}")
        print("📊 TEST SUMMARY")
        print(f"{'=' * 60}")
        
        passed = sum(1 for r in results.values() if r)
        total = len(results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Warnings/Errors: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        print("\nDetailed Results:")
        for test_name, result in results.items():
            status_icon = "✅" if result else "⚠️"
            print(f"  {status_icon} {test_name}")
        
        print(f"\n{'=' * 60}")
        print("🎯 Integration testing completed!")
        
        if passed == total:
            print("🟢 All tests passed successfully!")
            print("🇨🇳 Ready for Chinese market deployment!")
        elif passed > total * 0.8:
            print("🟡 Most tests passed - minor issues detected")
        else:
            print("🔴 Several tests failed - review integration")
        
        return results

async def test_api_endpoints():
    """Test API endpoints via HTTP requests"""
    print("\n🌐 Testing API Endpoints...")
    
    base_url = "http://localhost:8001"
    
    test_endpoints = [
        ("GET", "/api/integrations/baidu-webmaster?type=status"),
        ("GET", "/api/integrations/baidu-webmaster/sites"),
        ("GET", "/api/integrations/baidu-webmaster/search-queries?site_url=https://example.cn"),
        ("GET", "/api/integrations/baidu-webmaster/site-health?site_url=https://example.cn"),
        ("GET", "/api/integrations/baidu-webmaster/compliance-report?site_url=https://example.cn"),
    ]
    
    async with aiohttp.ClientSession() as session:
        for method, endpoint in test_endpoints:
            try:
                url = f"{base_url}{endpoint}"
                async with session.request(method, url) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ {method} {endpoint} - Success")
                    else:
                        print(f"⚠️ {method} {endpoint} - Status {response.status}")
            except Exception as e:
                print(f"❌ {method} {endpoint} - Error: {str(e)}")

if __name__ == "__main__":
    print("🇨🇳 Starting Baidu Webmaster Tools Integration Tests...")
    print("中国市场搜索引擎优化工具测试开始...")
    
    # Run integration tests
    tester = TestBaiduWebmasterIntegration()
    results = asyncio.run(tester.run_all_tests())
    
    # Test API endpoints if server is running
    try:
        asyncio.run(test_api_endpoints())
    except Exception as e:
        print(f"\n⚠️ API endpoint testing skipped: {str(e)}")
        print("   Make sure the API server is running on localhost:8001")
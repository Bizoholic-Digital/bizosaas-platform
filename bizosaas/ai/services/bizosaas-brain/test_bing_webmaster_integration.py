#!/usr/bin/env python3
"""
Test suite for Bing Webmaster Tools API Integration
Tests OAuth flow, API key authentication, and all major functionalities
"""

import asyncio
import json
import aiohttp
from datetime import datetime
import os
import sys

# Add current directory to path for importing our integration
sys.path.append(os.path.dirname(__file__))

from bing_webmaster_integration import bing_webmaster_integration

class TestBingWebmasterIntegration:
    def __init__(self):
        self.tenant_id = "test_tenant_123"
        self.test_site_url = "https://example.com"
        self.test_api_key = os.getenv('BING_WEBMASTER_API_KEY', 'test_api_key_123')
        
    async def test_oauth_flow(self):
        """Test OAuth 2.0 authentication flow"""
        print("🔐 Testing OAuth Flow...")
        
        # Test OAuth URL generation
        scopes = ['webmaster.read', 'webmaster.manage']
        oauth_result = bing_webmaster_integration.generate_oauth_url(self.tenant_id, scopes)
        
        if oauth_result['success']:
            print(f"✅ OAuth URL generated: {oauth_result['auth_url'][:100]}...")
            print(f"   State: {oauth_result['state']}")
            print(f"   Expires in: {oauth_result['expires_in']} seconds")
        else:
            print(f"❌ OAuth URL generation failed: {oauth_result['error']}")
            
        return oauth_result['success']
    
    async def test_get_user_sites(self):
        """Test getting user sites"""
        print("🏢 Testing Get User Sites...")
        
        # Test with API key
        result = await bing_webmaster_integration.get_user_sites(self.tenant_id, self.test_api_key)
        
        if result['success']:
            print(f"✅ User sites retrieved: {result['count']} sites found")
            if result['sites']:
                for site in result['sites'][:3]:  # Show first 3 sites
                    print(f"   - {site['site_url']} (Status: {site['verification_status']})")
        else:
            print(f"⚠️ User sites retrieval: {result['error']}")
            
        return result
    
    async def test_url_submission(self):
        """Test URL submission functionality"""
        print("📤 Testing URL Submission...")
        
        # Test single URL submission
        single_result = await bing_webmaster_integration.submit_url(
            self.tenant_id, 
            self.test_site_url, 
            f"{self.test_site_url}/test-page",
            self.test_api_key
        )
        
        if single_result['success']:
            print(f"✅ Single URL submitted successfully")
            print(f"   URL: {single_result['submission_result']['url']}")
            print(f"   Status: {single_result['submission_result']['status']}")
        else:
            print(f"⚠️ Single URL submission: {single_result['error']}")
        
        # Test batch URL submission
        test_urls = [
            f"{self.test_site_url}/page1",
            f"{self.test_site_url}/page2",
            f"{self.test_site_url}/page3"
        ]
        
        batch_result = await bing_webmaster_integration.submit_url_batch(
            self.tenant_id, 
            self.test_site_url, 
            test_urls,
            self.test_api_key
        )
        
        if batch_result['success']:
            print(f"✅ Batch URL submission successful: {batch_result['submitted_count']} URLs")
        else:
            print(f"⚠️ Batch URL submission: {batch_result['error']}")
            
        return single_result['success'] and batch_result['success']
    
    async def test_url_submission_quota(self):
        """Test URL submission quota"""
        print("📊 Testing URL Submission Quota...")
        
        result = await bing_webmaster_integration.get_url_submission_quota(
            self.tenant_id, 
            self.test_site_url, 
            self.test_api_key
        )
        
        if result['success']:
            quota = result['quota']
            print(f"✅ Quota information retrieved:")
            print(f"   Daily Quota: {quota['daily_quota']}")
            print(f"   Daily Used: {quota['daily_used']}")
            print(f"   Daily Remaining: {quota['daily_remaining']}")
        else:
            print(f"⚠️ Quota retrieval: {result['error']}")
            
        return result['success']
    
    async def test_search_performance(self):
        """Test search performance analytics"""
        print("📈 Testing Search Performance Analytics...")
        
        search_params = {
            'start_date': '2024-08-01',
            'end_date': '2024-09-01'
        }
        
        result = await bing_webmaster_integration.get_search_performance(
            self.tenant_id, 
            self.test_site_url, 
            search_params,
            self.test_api_key
        )
        
        if result['success']:
            print(f"✅ Search performance data retrieved: {result['count']} queries")
            if result['data']:
                for query_data in result['data'][:3]:  # Show first 3 queries
                    print(f"   Query: {query_data['query']}")
                    print(f"   Clicks: {query_data['clicks']}, Impressions: {query_data['impressions']}")
                    print(f"   CTR: {query_data['ctr']:.2%}, Avg Position: {query_data['avg_position']:.1f}")
        else:
            print(f"⚠️ Search performance: {result['error']}")
            
        return result['success']
    
    async def test_crawl_stats(self):
        """Test crawl statistics"""
        print("🕷️ Testing Crawl Statistics...")
        
        result = await bing_webmaster_integration.get_crawl_stats(
            self.tenant_id, 
            self.test_site_url, 
            self.test_api_key
        )
        
        if result['success']:
            crawl_stats = result['crawl_stats']
            print(f"✅ Crawl statistics retrieved:")
            print(f"   Crawled Pages: {crawl_stats['crawled_pages']}")
            print(f"   Blocked Pages: {crawl_stats['blocked_pages']}")
            print(f"   Crawl Errors: {crawl_stats['crawl_errors']}")
            print(f"   Last Crawl: {crawl_stats['last_crawl_date']}")
        else:
            print(f"⚠️ Crawl statistics: {result['error']}")
            
        return result['success']
    
    async def test_keyword_research(self):
        """Test keyword research functionality"""
        print("🔍 Testing Keyword Research...")
        
        result = await bing_webmaster_integration.get_keyword_research(
            self.tenant_id, 
            "digital marketing", 
            "US", 
            "en-US",
            self.test_api_key
        )
        
        if result['success']:
            keyword_data = result['keyword_data']
            print(f"✅ Keyword research data retrieved:")
            print(f"   Keyword: {keyword_data['keyword']}")
            print(f"   Search Volume: {keyword_data['search_volume']:,}")
            print(f"   Competition: {keyword_data['competition']}")
            print(f"   CPC: ${keyword_data['cpc']:.2f}")
        else:
            print(f"⚠️ Keyword research: {result['error']}")
            
        return result['success']
    
    async def test_page_stats(self):
        """Test page statistics"""
        print("📄 Testing Page Statistics...")
        
        result = await bing_webmaster_integration.get_page_stats(
            self.tenant_id, 
            self.test_site_url, 
            self.test_api_key
        )
        
        if result['success']:
            print(f"✅ Page statistics retrieved: {result['count']} pages")
        else:
            print(f"⚠️ Page statistics: {result['error']}")
            
        return result['success']
    
    async def test_traffic_stats(self):
        """Test traffic and ranking statistics"""
        print("🚦 Testing Traffic and Ranking Statistics...")
        
        result = await bing_webmaster_integration.get_rank_and_traffic_stats(
            self.tenant_id, 
            self.test_site_url, 
            self.test_api_key
        )
        
        if result['success']:
            print(f"✅ Traffic statistics retrieved")
            if 'traffic_stats' in result:
                print(f"   Data available for site: {self.test_site_url}")
        else:
            print(f"⚠️ Traffic statistics: {result['error']}")
            
        return result['success']
    
    async def test_sitemap_submission(self):
        """Test sitemap submission"""
        print("🗺️ Testing Sitemap Submission...")
        
        sitemap_url = f"{self.test_site_url}/sitemap.xml"
        result = await bing_webmaster_integration.submit_sitemap(
            self.tenant_id, 
            self.test_site_url, 
            sitemap_url,
            self.test_api_key
        )
        
        if result['success']:
            sitemap_status = result['sitemap_status']
            print(f"✅ Sitemap submitted successfully:")
            print(f"   Sitemap URL: {sitemap_status['sitemap_url']}")
            print(f"   Status: {sitemap_status['status']}")
            print(f"   Submitted: {sitemap_status['last_submitted']}")
        else:
            print(f"⚠️ Sitemap submission: {result['error']}")
            
        return result['success']
    
    async def test_block_urls(self):
        """Test URL blocking functionality"""
        print("🚫 Testing URL Blocking...")
        
        urls_to_block = [
            f"{self.test_site_url}/private-page",
            f"{self.test_site_url}/admin-area"
        ]
        
        result = await bing_webmaster_integration.block_urls(
            self.tenant_id, 
            self.test_site_url, 
            urls_to_block,
            self.test_api_key
        )
        
        if result['success']:
            print(f"✅ URLs blocked successfully:")
            for url in result['blocked_urls']:
                print(f"   - {url}")
        else:
            print(f"⚠️ URL blocking: {result['error']}")
            
        return result['success']
    
    async def test_connection_status(self):
        """Test connection status"""
        print("🔗 Testing Connection Status...")
        
        # Test with API key
        result = await bing_webmaster_integration.get_connection_status(self.tenant_id, self.test_api_key)
        
        print(f"Connection Status: {result['status']}")
        print(f"Auth Method: {result.get('auth_method', 'unknown')}")
        print(f"Message: {result['message']}")
        
        return result['status'] in ['connected', 'disconnected']
    
    async def run_all_tests(self):
        """Run all integration tests"""
        print("=" * 60)
        print("🧪 BING WEBMASTER TOOLS API INTEGRATION TESTS")
        print("=" * 60)
        
        tests = [
            ("OAuth Flow", self.test_oauth_flow),
            ("User Sites", self.test_get_user_sites),
            ("URL Submission", self.test_url_submission),
            ("URL Quota", self.test_url_submission_quota),
            ("Search Performance", self.test_search_performance),
            ("Crawl Statistics", self.test_crawl_stats),
            ("Keyword Research", self.test_keyword_research),
            ("Page Statistics", self.test_page_stats),
            ("Traffic Statistics", self.test_traffic_stats),
            ("Sitemap Submission", self.test_sitemap_submission),
            ("URL Blocking", self.test_block_urls),
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
        ("GET", "/api/integrations/bing-webmaster?type=status"),
        ("GET", "/api/integrations/bing-webmaster/sites"),
        ("GET", "/api/integrations/bing-webmaster/crawl-stats?site_url=https://example.com"),
        ("GET", "/api/integrations/bing-webmaster/url-submission-quota?site_url=https://example.com"),
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
    # Run integration tests
    tester = TestBingWebmasterIntegration()
    results = asyncio.run(tester.run_all_tests())
    
    # Test API endpoints if server is running
    try:
        asyncio.run(test_api_endpoints())
    except Exception as e:
        print(f"\n⚠️ API endpoint testing skipped: {str(e)}")
        print("   Make sure the API server is running on localhost:8001")
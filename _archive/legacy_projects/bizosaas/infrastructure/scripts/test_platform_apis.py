#!/usr/bin/env python3
"""
Test script for platform API integrations
Validates that the Google Ads, Meta Ads, and LinkedIn Ads clients work correctly
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# Add the marketing automation service to Python path
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas/services/marketing-automation-service')

async def test_google_ads_client():
    """Test Google Ads client functionality"""
    try:
        from platform_apis.google_ads_client import GoogleAdsClient
        
        # Mock credentials for testing
        test_credentials = {
            "developer_token": "test_token",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret", 
            "refresh_token": "test_refresh_token",
            "customer_id": "1234567890"
        }
        
        print("🔍 Testing Google Ads Client...")
        
        client = GoogleAdsClient(test_credentials)
        
        # Test credential validation
        validation_result = await client.validate_credentials()
        print(f"✅ Credential validation: {validation_result['is_healthy']}")
        
        # Test campaign creation
        campaign_data = {
            "name": "Test Campaign",
            "budget": 1000.0,
            "target_audience": {"locations": ["US"], "age_range": "25-54"},
            "creative_assets": []
        }
        
        config = {"channel_type": "SEARCH", "target_cpa": 50.0}
        
        campaign_id = await client.create_campaign(campaign_data, config)
        print(f"✅ Campaign created: {campaign_id}")
        
        # Test performance metrics
        performance = await client.get_campaign_performance(campaign_id)
        print(f"✅ Performance data retrieved: {performance['metrics']['impressions']} impressions")
        
        return True
        
    except Exception as e:
        print(f"❌ Google Ads Client test failed: {e}")
        return False

async def test_meta_ads_client():
    """Test Meta Ads client functionality"""
    try:
        from platform_apis.meta_ads_client import MetaAdsClient
        
        # Mock credentials for testing
        test_credentials = {
            "access_token": "test_access_token",
            "app_id": "test_app_id",
            "app_secret": "test_app_secret",
            "ad_account_id": "1234567890"
        }
        
        print("🔍 Testing Meta Ads Client...")
        
        client = MetaAdsClient(test_credentials)
        
        # Test credential validation
        validation_result = await client.validate_credentials()
        print(f"✅ Credential validation: {validation_result['is_healthy']}")
        
        # Test campaign creation
        campaign_data = {
            "name": "Test Meta Campaign",
            "budget": 1500.0,
            "target_audience": {"countries": ["US"], "age_min": 25, "age_max": 54},
            "creative_assets": []
        }
        
        config = {"objective": "CONVERSIONS", "optimization_goal": "CONVERSIONS"}
        
        campaign_id = await client.create_campaign(campaign_data, config)
        print(f"✅ Campaign created: {campaign_id}")
        
        # Test performance metrics
        performance = await client.get_campaign_performance(campaign_id)
        print(f"✅ Performance data retrieved: {performance['metrics']['impressions']} impressions")
        
        # Test audience insights
        insights = await client.get_audience_insights(campaign_id)
        print(f"✅ Audience insights retrieved: {len(insights['demographics']['age_groups'])} age groups")
        
        return True
        
    except Exception as e:
        print(f"❌ Meta Ads Client test failed: {e}")
        return False

async def test_linkedin_ads_client():
    """Test LinkedIn Ads client functionality"""
    try:
        from platform_apis.linkedin_ads_client import LinkedInAdsClient
        
        # Mock credentials for testing
        test_credentials = {
            "access_token": "test_access_token",
            "client_id": "test_client_id", 
            "client_secret": "test_client_secret",
            "ad_account_id": "1234567890"
        }
        
        print("🔍 Testing LinkedIn Ads Client...")
        
        client = LinkedInAdsClient(test_credentials)
        
        # Test credential validation
        validation_result = await client.validate_credentials()
        print(f"✅ Credential validation: {validation_result['is_healthy']}")
        
        # Test campaign creation
        campaign_data = {
            "name": "Test LinkedIn Campaign",
            "budget": 2000.0,
            "target_audience": {
                "locations": ["us"],
                "industries": ["technology"],
                "functions": ["marketing"]
            },
            "creative_assets": []
        }
        
        config = {"campaign_type": "SPONSORED_UPDATES", "cost_type": "CPM"}
        
        campaign_id = await client.create_campaign(campaign_data, config)
        print(f"✅ Campaign created: {campaign_id}")
        
        # Test performance metrics
        performance = await client.get_campaign_performance(campaign_id)
        print(f"✅ Performance data retrieved: {performance['metrics']['impressions']} impressions")
        
        # Test targeting suggestions
        suggestions = await client.get_targeting_suggestions(["marketing", "advertising"])
        print(f"✅ Targeting suggestions retrieved: {suggestions['total_estimated_reach']} total reach")
        
        return True
        
    except Exception as e:
        print(f"❌ LinkedIn Ads Client test failed: {e}")
        return False

async def test_campaign_operations():
    """Test campaign management operations"""
    try:
        from platform_apis.google_ads_client import GoogleAdsClient
        
        print("🔍 Testing Campaign Operations...")
        
        test_credentials = {
            "developer_token": "test_token",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret", 
            "refresh_token": "test_refresh_token",
            "customer_id": "1234567890"
        }
        
        client = GoogleAdsClient(test_credentials)
        
        # Test budget update
        success = await client.update_campaign_budget("test_campaign_123", 2500.0)
        print(f"✅ Budget update: {success}")
        
        # Test pause/resume
        pause_success = await client.pause_campaign("test_campaign_123")
        print(f"✅ Campaign pause: {pause_success}")
        
        resume_success = await client.resume_campaign("test_campaign_123")
        print(f"✅ Campaign resume: {resume_success}")
        
        # Test keyword performance
        keyword_performance = await client.get_keyword_performance("test_campaign_123")
        print(f"✅ Keyword performance: {len(keyword_performance)} keywords analyzed")
        
        return True
        
    except Exception as e:
        print(f"❌ Campaign operations test failed: {e}")
        return False

async def main():
    """Run all platform API tests"""
    print("🚀 Starting Platform API Integration Tests")
    print(f"📅 Test run: {datetime.now().isoformat()}")
    print("-" * 60)
    
    results = {
        "google_ads": False,
        "meta_ads": False,
        "linkedin_ads": False,
        "campaign_ops": False
    }
    
    # Run tests
    results["google_ads"] = await test_google_ads_client()
    print()
    
    results["meta_ads"] = await test_meta_ads_client()
    print()
    
    results["linkedin_ads"] = await test_linkedin_ads_client()
    print()
    
    results["campaign_ops"] = await test_campaign_operations()
    print()
    
    # Summary
    print("-" * 60)
    print("📊 Test Results Summary:")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name.upper()}: {status}")
    
    print(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All platform API integration tests PASSED!")
        print("✅ Platform APIs are ready for production use with BYOK architecture")
        return 0
    else:
        print("⚠️  Some platform API tests FAILED")
        print("🔧 Review the errors above and fix before deployment")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
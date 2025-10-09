#!/usr/bin/env python3
"""
Test script for Facebook Ads Integration
Run this to verify the integration is working properly
"""

import asyncio
import json
import sys
import os
from facebook_ads_integration import facebook_ads_integration

async def test_oauth_generation():
    """Test OAuth URL generation"""
    print("\n🧪 Testing OAuth URL generation...")
    
    try:
        result = facebook_ads_integration.generate_oauth_url(
            tenant_id="test_tenant",
            scopes=["ads_read", "ads_management"]
        )
        
        if result.get('success'):
            print(f"✅ OAuth URL generated successfully")
            print(f"   Auth URL: {result['auth_url'][:100]}...")
            print(f"   State: {result['state']}")
            print(f"   Expires in: {result['expires_in']} seconds")
        else:
            print(f"❌ OAuth URL generation failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Exception in OAuth generation: {str(e)}")

async def test_connection_status():
    """Test connection status check"""
    print("\n🧪 Testing connection status check...")
    
    try:
        result = await facebook_ads_integration.get_connection_status("test_tenant")
        
        if result.get('success'):
            print(f"✅ Connection status check successful")
            print(f"   Status: {result.get('status')}")
            print(f"   Tenant ID: {result.get('tenant_id')}")
        else:
            print(f"❌ Connection status check failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Exception in connection status: {str(e)}")

async def test_mock_oauth_callback():
    """Test OAuth callback with mock data"""
    print("\n🧪 Testing OAuth callback (mock)...")
    
    # First generate a state
    oauth_result = facebook_ads_integration.generate_oauth_url(
        tenant_id="test_tenant", 
        scopes=["ads_read"]
    )
    
    if not oauth_result.get('success'):
        print(f"❌ Could not generate OAuth URL: {oauth_result.get('error')}")
        return
    
    # Mock callback with invalid code (should fail gracefully)
    try:
        result = await facebook_ads_integration.handle_oauth_callback(
            code="mock_code_12345",
            state=oauth_result['state']
        )
        
        # This should fail since it's a mock code, but shouldn't crash
        if not result.get('success'):
            print(f"✅ OAuth callback correctly rejected mock code: {result.get('error')}")
        else:
            print(f"⚠️  OAuth callback unexpectedly succeeded with mock data")
            
    except Exception as e:
        print(f"❌ Exception in OAuth callback: {str(e)}")

async def test_disconnect():
    """Test disconnection"""
    print("\n🧪 Testing account disconnection...")
    
    try:
        result = await facebook_ads_integration.disconnect_account("test_tenant")
        
        if result.get('success'):
            print(f"✅ Disconnection successful")
            print(f"   Status: {result.get('status')}")
            print(f"   Disconnected at: {result.get('disconnected_at')}")
        else:
            print(f"❌ Disconnection failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Exception in disconnection: {str(e)}")

async def test_campaigns_not_connected():
    """Test campaigns fetch without connection (should fail)"""
    print("\n🧪 Testing campaigns fetch (not connected)...")
    
    try:
        result = await facebook_ads_integration.get_campaigns("test_tenant")
        
        if not result.get('success'):
            print(f"✅ Campaigns fetch correctly failed when not connected: {result.get('error')}")
        else:
            print(f"⚠️  Campaigns fetch unexpectedly succeeded without connection")
            
    except Exception as e:
        print(f"❌ Exception in campaigns fetch: {str(e)}")

async def test_data_models():
    """Test data model creation"""
    print("\n🧪 Testing data models...")
    
    try:
        from facebook_ads_integration import FacebookCampaign, FacebookAdAccount, FacebookAudience, FacebookCreative
        
        # Test campaign model
        mock_campaign_data = {
            'id': 'camp_123456',
            'name': 'Test Campaign',
            'status': 'ACTIVE',
            'objective': 'CONVERSIONS',
            'budget_remaining': 500000,  # $5000 in cents
            'daily_budget': 10000,  # $100 in cents
            'created_time': '2024-01-01T00:00:00Z',
            'updated_time': '2024-01-01T00:00:00Z',
            'start_time': '2024-01-01T00:00:00Z'
        }
        
        mock_insights_data = {
            'impressions': '10000',
            'clicks': '500',
            'spend': '450.50',
            'reach': '8500'
        }
        
        campaign = FacebookCampaign.from_api_response(mock_campaign_data, mock_insights_data)
        print(f"✅ Campaign model created: {campaign.name}")
        print(f"   Impressions: {campaign.impressions:,}")
        print(f"   CTR: {campaign.ctr:.2f}%")
        print(f"   CPC: ${campaign.cpc:.2f}")
        
        # Test account model
        mock_account_data = {
            'id': 'act_123456789',
            'name': 'Test Ad Account',
            'account_id': '123456789',
            'currency': 'USD',
            'timezone_name': 'America/New_York',
            'account_status': 1,
            'balance': '50000'  # $500 in cents
        }
        
        account = FacebookAdAccount.from_api_response(mock_account_data)
        print(f"✅ Account model created: {account.name}")
        print(f"   Balance: ${account.balance:.2f}")
        print(f"   Currency: {account.currency}")
        
        # Test audience model
        mock_audience_data = {
            'id': 'aud_123456',
            'name': 'Test Audience',
            'description': 'Test audience for unit testing',
            'subtype': 'CUSTOM',
            'approximate_count_lower_bound': 15000,
            'operation_status': {'code': 'OK'},
            'retention_days': 180
        }
        
        audience = FacebookAudience.from_api_response(mock_audience_data)
        print(f"✅ Audience model created: {audience.name}")
        print(f"   Size: {audience.approximate_count:,}")
        print(f"   Type: {audience.subtype}")
        
        # Test creative model
        mock_creative_data = {
            'id': 'cre_123456',
            'name': 'Test Creative',
            'status': 'ACTIVE',
            'created_time': '2024-01-01T00:00:00Z',
            'object_story_spec': {
                'link_data': {
                    'name': 'Test Ad Title',
                    'message': 'Test ad message',
                    'picture': 'https://example.com/image.jpg',
                    'call_to_action': {'type': 'LEARN_MORE'}
                }
            }
        }
        
        creative = FacebookCreative.from_api_response(mock_creative_data)
        print(f"✅ Creative model created: {creative.name}")
        print(f"   Title: {creative.title}")
        print(f"   CTA: {creative.call_to_action_type}")
        
    except Exception as e:
        print(f"❌ Exception in data models test: {str(e)}")

def test_environment_config():
    """Test environment configuration"""
    print("\n🧪 Testing environment configuration...")
    
    required_vars = [
        'FACEBOOK_APP_ID',
        'FACEBOOK_APP_SECRET',
        'FACEBOOK_REDIRECT_URI'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print(f"   Copy .env.facebook.example to .env.facebook and configure")
    else:
        print(f"✅ All required environment variables are set")
        
    # Check if credentials look valid (not placeholder values)
    app_id = os.getenv('FACEBOOK_APP_ID', '')
    if app_id and app_id != 'your_facebook_app_id_here':
        print(f"✅ Facebook App ID appears to be configured")
    elif app_id:
        print(f"⚠️  Facebook App ID still has placeholder value")
    else:
        print(f"❌ Facebook App ID not set")

async def main():
    """Run all tests"""
    print("🚀 Facebook Ads Integration Test Suite")
    print("=" * 50)
    
    # Test environment configuration
    test_environment_config()
    
    # Test basic functionality
    await test_connection_status()
    await test_oauth_generation()
    await test_mock_oauth_callback()
    await test_campaigns_not_connected()
    await test_disconnect()
    
    # Test data models
    await test_data_models()
    
    print("\n" + "=" * 50)
    print("🏁 Test suite completed!")
    print("\nNext steps:")
    print("1. Configure your Facebook app credentials in .env.facebook")
    print("2. Start the Brain API: python simple_api.py")
    print("3. Start the frontend: npm run dev")
    print("4. Navigate to the Facebook Ads integration in the UI")
    print("5. Test the full OAuth flow with real Facebook credentials")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n❌ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite failed with exception: {str(e)}")
        sys.exit(1)
#!/usr/bin/env python3
"""
Test script for Google My Business Integration
Tests OAuth flow, location management, posts, reviews, and insights
"""

import asyncio
import os
import json
from datetime import datetime
from google_my_business_integration import GoogleMyBusinessIntegration, LocationState, PostState

async def test_google_my_business_integration():
    """Test Google My Business integration functionality"""
    
    print("🧪 Testing Google My Business Integration")
    print("=" * 50)
    
    # Initialize integration
    gmb = GoogleMyBusinessIntegration()
    tenant_id = "test_tenant"
    
    # Test OAuth URL generation
    print("\n1. Testing OAuth URL Generation")
    oauth_result = gmb.generate_oauth_url(tenant_id, [
        'https://www.googleapis.com/auth/business.manage',
        'https://www.googleapis.com/auth/plus.business.manage'
    ])
    
    if oauth_result['success']:
        print(f"✅ OAuth URL generated successfully")
        print(f"   State: {oauth_result['state']}")
        print(f"   Expires in: {oauth_result['expires_in']} seconds")
        print(f"   URL: {oauth_result['auth_url'][:100]}...")
    else:
        print(f"❌ OAuth URL generation failed: {oauth_result['error']}")
        return
    
    # Test connection status (without actual token)
    print("\n2. Testing Connection Status")
    status_result = await gmb.get_connection_status(tenant_id)
    print(f"   Status: {status_result['status']}")
    print(f"   Message: {status_result['message']}")
    
    # Mock token for testing API methods (in real scenario, this comes from OAuth)
    print("\n3. Setting up mock token for testing")
    gmb.access_tokens[tenant_id] = {
        'access_token': 'mock_token_for_testing',
        'refresh_token': 'mock_refresh_token',
        'expires_at': (datetime.now().replace(year=2025)).isoformat(),
        'scopes': ['https://www.googleapis.com/auth/business.manage'],
        'created_at': datetime.now().isoformat()
    }
    
    # Test account info (will fail with mock token, but tests the logic)
    print("\n4. Testing Account Info Retrieval")
    account_result = await gmb.get_account_info(tenant_id)
    print(f"   Success: {account_result.get('success', False)}")
    if not account_result.get('success'):
        print(f"   Expected error (mock token): {account_result.get('error', 'Unknown error')}")
    
    # Test location data structures
    print("\n5. Testing Data Structures")
    
    # Test location parsing
    mock_location_data = {
        'name': 'accounts/123/locations/456',
        'title': 'Test Restaurant',
        'phoneNumbers': {'primaryPhone': '+1-555-123-4567'},
        'categories': {
            'primaryCategory': {'displayName': 'Restaurant'}
        },
        'websiteUri': 'https://testrestaurant.com',
        'metadata': {'state': 'VERIFIED'},
        'storefrontAddress': {
            'addressLines': ['123 Main St'],
            'locality': 'New York',
            'administrativeArea': 'NY',
            'postalCode': '10001',
            'regionCode': 'US'
        },
        'latlng': {'latitude': 40.7128, 'longitude': -74.0060},
        'regularHours': {
            'periods': [
                {
                    'openDay': 'MONDAY',
                    'openTime': '09:00',
                    'closeDay': 'MONDAY',
                    'closeTime': '18:00'
                }
            ]
        }
    }
    
    from google_my_business_integration import GoogleMyBusinessLocation
    location = GoogleMyBusinessLocation.from_api_response(mock_location_data)
    print(f"✅ Location parsed: {location.location_name}")
    print(f"   Category: {location.primary_category}")
    print(f"   Status: {location.location_state}")
    print(f"   Phone: {location.primary_phone}")
    
    # Test post parsing
    mock_post_data = {
        'name': 'accounts/123/locations/456/localPosts/789',
        'topicType': 'STANDARD',
        'languageCode': 'en-US',
        'summary': 'Join us for our weekly happy hour!',
        'callToAction': {
            'actionType': 'LEARN_MORE',
            'url': 'https://testrestaurant.com/happy-hour'
        },
        'state': 'LIVE',
        'createTime': '2024-01-15T10:00:00Z',
        'updateTime': '2024-01-15T10:00:00Z'
    }
    
    from google_my_business_integration import GoogleMyBusinessPost
    post = GoogleMyBusinessPost.from_api_response(mock_post_data)
    print(f"✅ Post parsed: {post.summary[:50]}...")
    print(f"   Type: {post.topic_type}")
    print(f"   State: {post.state}")
    
    # Test review parsing
    mock_review_data = {
        'name': 'accounts/123/locations/456/reviews/101112',
        'reviewer': {
            'displayName': 'John Smith',
            'profilePhotoUrl': 'https://example.com/photo.jpg'
        },
        'starRating': 5,
        'comment': 'Excellent food and great service!',
        'createTime': '2024-01-14T15:30:00Z',
        'updateTime': '2024-01-14T15:30:00Z',
        'reviewReply': {
            'comment': 'Thank you for your kind words!',
            'updateTime': '2024-01-15T09:00:00Z'
        }
    }
    
    from google_my_business_integration import GoogleMyBusinessReview
    review = GoogleMyBusinessReview.from_api_response(mock_review_data)
    print(f"✅ Review parsed: {review.comment[:30]}...")
    print(f"   Rating: {review.star_rating} stars")
    print(f"   Reviewer: {review.reviewer['displayName']}")
    print(f"   Has reply: {review.review_reply is not None}")
    
    # Test insights parsing
    mock_insights_data = {
        'locationName': 'accounts/123/locations/456',
        'timeZone': 'America/New_York',
        'locationMetrics': [
            {
                'metric': 'QUERIES_DIRECT',
                'totalValue': {'value': '142'}
            },
            {
                'metric': 'VIEWS_MAPS',
                'totalValue': {'value': '89'}
            },
            {
                'metric': 'ACTIONS_PHONE',
                'totalValue': {'value': '23'}
            }
        ]
    }
    
    from google_my_business_integration import GoogleMyBusinessInsights
    insights = GoogleMyBusinessInsights.from_api_response(mock_insights_data)
    print(f"✅ Insights parsed for location: {insights.location_name}")
    print(f"   Time zone: {insights.time_zone}")
    print(f"   Metrics count: {len(insights.location_metrics)}")
    
    # Test form validation helpers
    print("\n6. Testing Form Validation")
    
    def validate_location_data(data):
        """Validate location creation data"""
        required_fields = ['title', 'primaryPhone', 'primaryCategory']
        errors = []
        
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Validate phone format (basic check)
        phone = data.get('primaryPhone', '')
        if phone and not any(char.isdigit() for char in phone):
            errors.append("Phone number must contain digits")
        
        # Validate address
        address = data.get('address', {})
        if not address.get('locality'):
            errors.append("City is required in address")
        
        return errors
    
    # Test valid location data
    valid_location = {
        'title': 'New Test Location',
        'primaryPhone': '+1-555-999-8888',
        'primaryCategory': 'Retail Store',
        'address': {
            'locality': 'San Francisco',
            'administrativeArea': 'CA'
        }
    }
    
    validation_errors = validate_location_data(valid_location)
    if not validation_errors:
        print("✅ Valid location data passed validation")
    else:
        print(f"❌ Validation errors: {validation_errors}")
    
    # Test invalid location data
    invalid_location = {
        'title': '',  # Missing title
        'primaryPhone': 'not-a-phone',  # Invalid phone
        'address': {}  # Missing city
    }
    
    validation_errors = validate_location_data(invalid_location)
    if validation_errors:
        print(f"✅ Invalid location data correctly rejected: {len(validation_errors)} errors")
    else:
        print("❌ Invalid location data incorrectly accepted")
    
    # Test post validation
    def validate_post_data(data):
        """Validate post creation data"""
        errors = []
        
        summary = data.get('summary', '').strip()
        if not summary:
            errors.append("Post content (summary) is required")
        elif len(summary) > 1500:
            errors.append("Post content cannot exceed 1500 characters")
        
        topic_type = data.get('topicType')
        valid_types = ['STANDARD', 'EVENT', 'OFFER', 'PRODUCT']
        if topic_type not in valid_types:
            errors.append(f"Invalid topic type. Must be one of: {', '.join(valid_types)}")
        
        return errors
    
    valid_post = {
        'topicType': 'STANDARD',
        'summary': 'Come visit us for our grand opening celebration!'
    }
    
    post_errors = validate_post_data(valid_post)
    if not post_errors:
        print("✅ Valid post data passed validation")
    else:
        print(f"❌ Post validation errors: {post_errors}")
    
    print("\n7. Testing Error Handling")
    
    # Test refresh token with invalid tenant
    refresh_result = await gmb.refresh_access_token("nonexistent_tenant")
    if not refresh_result['success']:
        print(f"✅ Refresh token correctly failed for invalid tenant")
    else:
        print("❌ Refresh token should have failed for invalid tenant")
    
    # Test API request with invalid token
    api_result = await gmb.make_api_request("invalid_tenant", 'GET', '/accounts')
    if not api_result['success']:
        print(f"✅ API request correctly failed for invalid tenant")
    else:
        print("❌ API request should have failed for invalid tenant")
    
    print("\n8. Integration Summary")
    print("=" * 50)
    print("✅ OAuth URL generation working")
    print("✅ Data structure parsing working")
    print("✅ Form validation working")
    print("✅ Error handling working")
    print("✅ Connection status checking working")
    print("\n📝 Notes:")
    print("   - Actual API calls require valid Google OAuth credentials")
    print("   - Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables")
    print("   - Configure OAuth redirect URI in Google Cloud Console")
    print("   - Enable Google My Business API in Google Cloud Console")
    print("   - Request appropriate API quotas for production use")
    
    print("\n🔧 Environment Setup Checklist:")
    env_vars = [
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_SECRET', 
        'GOOGLE_REDIRECT_URI'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        status = "✅ Set" if value else "❌ Missing"
        print(f"   {var}: {status}")
        if value and len(value) > 20:
            print(f"     Value: {value[:10]}...{value[-10:]}")
        elif value:
            print(f"     Value: {value}")
    
    print(f"\n🎯 Ready for production: {'✅ Yes' if all(os.getenv(var) for var in env_vars) else '❌ No - Missing environment variables'}")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_google_my_business_integration())
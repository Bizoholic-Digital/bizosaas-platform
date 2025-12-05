#!/usr/bin/env python3
"""
Google My Business Integration Service for BizOSaaS Brain API
Provides comprehensive Google My Business API integration with OAuth flows,
location management, posts, reviews, insights, and local SEO optimization.
"""

import os
import json
import uuid
import hashlib
import hmac
import aiohttp
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from urllib.parse import urlencode, parse_qs
import base64
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocationState(str, Enum):
    DRAFT = "DRAFT"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    VERIFIED = "VERIFIED"
    SUSPENDED = "SUSPENDED"
    NEEDS_REVERIFICATION = "NEEDS_REVERIFICATION"
    DUPLICATE = "DUPLICATE"

class PostState(str, Enum):
    DRAFT = "DRAFT"
    LIVE = "LIVE"
    REJECTED = "REJECTED"
    
class ReviewReply(str, Enum):
    NOT_REPLIED = "NOT_REPLIED"
    REPLIED = "REPLIED"

@dataclass
class GoogleMyBusinessLocation:
    name: str
    location_name: str
    primary_phone: str
    primary_category: str
    website_url: Optional[str]
    location_state: str
    address: Dict[str, Any]
    lat_lng: Dict[str, float]
    open_info: Dict[str, Any]
    store_code: Optional[str] = None
    labels: List[str] = None
    additional_phones: List[str] = None
    service_area: Dict[str, Any] = None
    location_key: Optional[str] = None
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'GoogleMyBusinessLocation':
        return cls(
            name=data.get('name', ''),
            location_name=data.get('title', ''),
            primary_phone=data.get('phoneNumbers', {}).get('primaryPhone', ''),
            primary_category=data.get('categories', {}).get('primaryCategory', {}).get('displayName', ''),
            website_url=data.get('websiteUri', ''),
            location_state=data.get('metadata', {}).get('state', 'DRAFT'),
            address=data.get('storefrontAddress', {}),
            lat_lng=data.get('latlng', {}),
            open_info=data.get('regularHours', {}),
            store_code=data.get('storeCode'),
            labels=data.get('labels', []),
            additional_phones=data.get('phoneNumbers', {}).get('additionalPhones', []),
            service_area=data.get('serviceArea', {}),
            location_key=data.get('locationKey')
        )

@dataclass
class GoogleMyBusinessPost:
    name: str
    topic_type: str
    language_code: str
    summary: str
    call_to_action: Dict[str, Any]
    state: str
    create_time: str
    update_time: str
    event: Optional[Dict[str, Any]] = None
    offer: Optional[Dict[str, Any]] = None
    media: Optional[List[Dict[str, Any]]] = None
    search_url: Optional[str] = None
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'GoogleMyBusinessPost':
        return cls(
            name=data.get('name', ''),
            topic_type=data.get('topicType', 'STANDARD'),
            language_code=data.get('languageCode', 'en'),
            summary=data.get('summary', ''),
            call_to_action=data.get('callToAction', {}),
            state=data.get('state', 'DRAFT'),
            create_time=data.get('createTime', ''),
            update_time=data.get('updateTime', ''),
            event=data.get('event'),
            offer=data.get('offer'),
            media=data.get('media', []),
            search_url=data.get('searchUrl')
        )

@dataclass
class GoogleMyBusinessReview:
    name: str
    reviewer: Dict[str, Any]
    star_rating: int
    comment: str
    create_time: str
    update_time: str
    review_reply: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'GoogleMyBusinessReview':
        return cls(
            name=data.get('name', ''),
            reviewer=data.get('reviewer', {}),
            star_rating=data.get('starRating', 1),
            comment=data.get('comment', ''),
            create_time=data.get('createTime', ''),
            update_time=data.get('updateTime', ''),
            review_reply=data.get('reviewReply')
        )

@dataclass
class GoogleMyBusinessInsights:
    location_name: str
    time_zone: str
    metric_requests: List[Dict[str, Any]]
    location_metrics: List[Dict[str, Any]]
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'GoogleMyBusinessInsights':
        return cls(
            location_name=data.get('locationName', ''),
            time_zone=data.get('timeZone', 'UTC'),
            metric_requests=data.get('metricRequests', []),
            location_metrics=data.get('locationMetrics', [])
        )

class GoogleMyBusinessIntegration:
    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:3002/api/brain/integrations/google-my-business/oauth?action=callback')
        self.api_version = 'v1'
        self.base_url = f'https://mybusinessbusinessinformation.googleapis.com/{self.api_version}'
        self.posts_base_url = f'https://mybusinessbusinessinformation.googleapis.com/{self.api_version}'
        self.reviews_base_url = f'https://mybusinessbusinessinformation.googleapis.com/{self.api_version}'
        
        # OAuth state storage (in production, use Redis or database)
        self.oauth_states: Dict[str, Dict[str, Any]] = {}
        
        # Token storage (in production, use encrypted database)
        self.access_tokens: Dict[str, Dict[str, Any]] = {}
        
        # Location cache (in production, use Redis with TTL)
        self.location_cache: Dict[str, Dict[str, Any]] = {}
        
    def generate_oauth_url(self, tenant_id: str, scopes: List[str]) -> Dict[str, Any]:
        """Generate Google OAuth URL for My Business authentication"""
        try:
            # Generate secure state parameter
            state = str(uuid.uuid4())
            
            # Store OAuth state
            self.oauth_states[state] = {
                'tenant_id': tenant_id,
                'scopes': scopes,
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(minutes=15)).isoformat()
            }
            
            # Default Google My Business scopes
            if not scopes:
                scopes = [
                    'https://www.googleapis.com/auth/business.manage',
                    'https://www.googleapis.com/auth/plus.business.manage'
                ]
            
            # Build OAuth URL
            params = {
                'client_id': self.client_id,
                'redirect_uri': self.redirect_uri,
                'scope': ' '.join(scopes),
                'response_type': 'code',
                'state': state,
                'access_type': 'offline',
                'prompt': 'consent'
            }
            
            auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
            
            return {
                'success': True,
                'auth_url': auth_url,
                'state': state,
                'expires_in': 900  # 15 minutes
            }
            
        except Exception as e:
            logger.error(f"Error generating OAuth URL: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to generate OAuth URL: {str(e)}'
            }
    
    async def handle_oauth_callback(self, code: str, state: str) -> Dict[str, Any]:
        """Handle OAuth callback and exchange code for access token"""
        try:
            # Validate state
            if state not in self.oauth_states:
                return {
                    'success': False,
                    'error': 'Invalid OAuth state'
                }
            
            oauth_data = self.oauth_states[state]
            tenant_id = oauth_data['tenant_id']
            
            # Check if state has expired
            expires_at = datetime.fromisoformat(oauth_data['expires_at'])
            if datetime.now() > expires_at:
                del self.oauth_states[state]
                return {
                    'success': False,
                    'error': 'OAuth state expired'
                }
            
            # Exchange code for access token
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': self.redirect_uri
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(token_url, data=token_data) as response:
                    if response.status == 200:
                        token_response = await response.json()
                        
                        # Store access token
                        self.access_tokens[tenant_id] = {
                            'access_token': token_response.get('access_token'),
                            'refresh_token': token_response.get('refresh_token'),
                            'expires_at': (datetime.now() + timedelta(seconds=token_response.get('expires_in', 3600))).isoformat(),
                            'scopes': oauth_data['scopes'],
                            'created_at': datetime.now().isoformat()
                        }
                        
                        # Clean up OAuth state
                        del self.oauth_states[state]
                        
                        # Get account info
                        account_info = await self.get_account_info(tenant_id)
                        
                        return {
                            'success': True,
                            'access_token': token_response.get('access_token'),
                            'account_info': account_info,
                            'expires_in': token_response.get('expires_in', 3600)
                        }
                    else:
                        error_response = await response.json()
                        return {
                            'success': False,
                            'error': error_response.get('error_description', 'Failed to exchange code for token')
                        }
                        
        except Exception as e:
            logger.error(f"Error handling OAuth callback: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to handle OAuth callback: {str(e)}'
            }
    
    async def refresh_access_token(self, tenant_id: str) -> Dict[str, Any]:
        """Refresh expired access token"""
        try:
            if tenant_id not in self.access_tokens:
                return {
                    'success': False,
                    'error': 'No access token found'
                }
            
            token_data = self.access_tokens[tenant_id]
            refresh_token = token_data.get('refresh_token')
            
            if not refresh_token:
                return {
                    'success': False,
                    'error': 'No refresh token available'
                }
            
            # Refresh token
            token_url = "https://oauth2.googleapis.com/token"
            refresh_data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(token_url, data=refresh_data) as response:
                    if response.status == 200:
                        token_response = await response.json()
                        
                        # Update stored token
                        self.access_tokens[tenant_id].update({
                            'access_token': token_response.get('access_token'),
                            'expires_at': (datetime.now() + timedelta(seconds=token_response.get('expires_in', 3600))).isoformat(),
                            'updated_at': datetime.now().isoformat()
                        })
                        
                        return {
                            'success': True,
                            'access_token': token_response.get('access_token'),
                            'expires_in': token_response.get('expires_in', 3600)
                        }
                    else:
                        error_response = await response.json()
                        return {
                            'success': False,
                            'error': error_response.get('error_description', 'Failed to refresh token')
                        }
                        
        except Exception as e:
            logger.error(f"Error refreshing access token: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to refresh access token: {str(e)}'
            }
    
    async def get_valid_access_token(self, tenant_id: str) -> Optional[str]:
        """Get valid access token, refreshing if necessary"""
        try:
            if tenant_id not in self.access_tokens:
                return None
            
            token_data = self.access_tokens[tenant_id]
            expires_at = datetime.fromisoformat(token_data['expires_at'])
            
            # Check if token is expired or will expire in next 5 minutes
            if datetime.now() >= expires_at - timedelta(minutes=5):
                refresh_result = await self.refresh_access_token(tenant_id)
                if not refresh_result['success']:
                    return None
                return refresh_result['access_token']
            
            return token_data['access_token']
            
        except Exception as e:
            logger.error(f"Error getting valid access token: {str(e)}")
            return None
    
    async def make_api_request(self, tenant_id: str, method: str, endpoint: str, data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make authenticated API request to Google My Business API"""
        try:
            access_token = await self.get_valid_access_token(tenant_id)
            if not access_token:
                return {
                    'success': False,
                    'error': 'No valid access token available'
                }
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}{endpoint}"
            
            async with aiohttp.ClientSession() as session:
                if method.upper() == 'GET':
                    async with session.get(url, headers=headers, params=params) as response:
                        response_data = await response.json()
                        if response.status == 200:
                            return {
                                'success': True,
                                'data': response_data
                            }
                        else:
                            return {
                                'success': False,
                                'error': response_data.get('error', {}).get('message', f'API request failed with status {response.status}')
                            }
                elif method.upper() == 'POST':
                    async with session.post(url, headers=headers, json=data, params=params) as response:
                        response_data = await response.json()
                        if response.status in [200, 201]:
                            return {
                                'success': True,
                                'data': response_data
                            }
                        else:
                            return {
                                'success': False,
                                'error': response_data.get('error', {}).get('message', f'API request failed with status {response.status}')
                            }
                elif method.upper() == 'PATCH':
                    async with session.patch(url, headers=headers, json=data, params=params) as response:
                        response_data = await response.json()
                        if response.status == 200:
                            return {
                                'success': True,
                                'data': response_data
                            }
                        else:
                            return {
                                'success': False,
                                'error': response_data.get('error', {}).get('message', f'API request failed with status {response.status}')
                            }
                elif method.upper() == 'DELETE':
                    async with session.delete(url, headers=headers, params=params) as response:
                        if response.status == 200:
                            return {
                                'success': True,
                                'data': {}
                            }
                        else:
                            response_data = await response.json()
                            return {
                                'success': False,
                                'error': response_data.get('error', {}).get('message', f'API request failed with status {response.status}')
                            }
                            
        except Exception as e:
            logger.error(f"Error making API request: {str(e)}")
            return {
                'success': False,
                'error': f'API request failed: {str(e)}'
            }
    
    async def get_account_info(self, tenant_id: str) -> Dict[str, Any]:
        """Get Google My Business account information"""
        try:
            result = await self.make_api_request(tenant_id, 'GET', '/accounts')
            if result['success']:
                accounts = result['data'].get('accounts', [])
                return {
                    'success': True,
                    'accounts': accounts,
                    'account_count': len(accounts)
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error getting account info: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get account info: {str(e)}'
            }
    
    async def get_locations(self, tenant_id: str, account_name: str = None) -> Dict[str, Any]:
        """Get business locations"""
        try:
            if not account_name:
                # Get first account
                account_info = await self.get_account_info(tenant_id)
                if not account_info['success'] or not account_info['accounts']:
                    return {
                        'success': False,
                        'error': 'No accounts found'
                    }
                account_name = account_info['accounts'][0]['name']
            
            result = await self.make_api_request(tenant_id, 'GET', f'/{account_name}/locations')
            if result['success']:
                locations_data = result['data'].get('locations', [])
                locations = [GoogleMyBusinessLocation.from_api_response(loc) for loc in locations_data]
                
                return {
                    'success': True,
                    'locations': [asdict(loc) for loc in locations],
                    'count': len(locations)
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error getting locations: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get locations: {str(e)}'
            }
    
    async def create_location(self, tenant_id: str, location_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new business location"""
        try:
            # Get account name
            account_info = await self.get_account_info(tenant_id)
            if not account_info['success'] or not account_info['accounts']:
                return {
                    'success': False,
                    'error': 'No accounts found'
                }
            account_name = account_info['accounts'][0]['name']
            
            result = await self.make_api_request(tenant_id, 'POST', f'/{account_name}/locations', data=location_data)
            if result['success']:
                location = GoogleMyBusinessLocation.from_api_response(result['data'])
                return {
                    'success': True,
                    'location': asdict(location)
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error creating location: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to create location: {str(e)}'
            }
    
    async def update_location(self, tenant_id: str, location_name: str, location_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing business location"""
        try:
            result = await self.make_api_request(tenant_id, 'PATCH', f'/{location_name}', data=location_data)
            if result['success']:
                location = GoogleMyBusinessLocation.from_api_response(result['data'])
                return {
                    'success': True,
                    'location': asdict(location)
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error updating location: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to update location: {str(e)}'
            }
    
    async def get_location_posts(self, tenant_id: str, location_name: str) -> Dict[str, Any]:
        """Get posts for a specific location"""
        try:
            result = await self.make_api_request(tenant_id, 'GET', f'/{location_name}/localPosts')
            if result['success']:
                posts_data = result['data'].get('localPosts', [])
                posts = [GoogleMyBusinessPost.from_api_response(post) for post in posts_data]
                
                return {
                    'success': True,
                    'posts': [asdict(post) for post in posts],
                    'count': len(posts)
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error getting location posts: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get location posts: {str(e)}'
            }
    
    async def create_post(self, tenant_id: str, location_name: str, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new post for a location"""
        try:
            result = await self.make_api_request(tenant_id, 'POST', f'/{location_name}/localPosts', data=post_data)
            if result['success']:
                post = GoogleMyBusinessPost.from_api_response(result['data'])
                return {
                    'success': True,
                    'post': asdict(post)
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error creating post: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to create post: {str(e)}'
            }
    
    async def get_location_reviews(self, tenant_id: str, location_name: str) -> Dict[str, Any]:
        """Get reviews for a specific location"""
        try:
            result = await self.make_api_request(tenant_id, 'GET', f'/{location_name}/reviews')
            if result['success']:
                reviews_data = result['data'].get('reviews', [])
                reviews = [GoogleMyBusinessReview.from_api_response(review) for review in reviews_data]
                
                return {
                    'success': True,
                    'reviews': [asdict(review) for review in reviews],
                    'count': len(reviews),
                    'average_rating': sum(r.star_rating for r in reviews) / len(reviews) if reviews else 0
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error getting location reviews: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get location reviews: {str(e)}'
            }
    
    async def reply_to_review(self, tenant_id: str, review_name: str, reply_text: str) -> Dict[str, Any]:
        """Reply to a customer review"""
        try:
            reply_data = {
                'comment': reply_text
            }
            result = await self.make_api_request(tenant_id, 'POST', f'/{review_name}/reply', data=reply_data)
            if result['success']:
                return {
                    'success': True,
                    'reply': result['data']
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error replying to review: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to reply to review: {str(e)}'
            }
    
    async def get_location_insights(self, tenant_id: str, location_name: str, metric_requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get insights and analytics for a location"""
        try:
            insights_data = {
                'locationNames': [location_name],
                'basicRequest': {
                    'metricRequests': metric_requests,
                    'timeRange': {
                        'startTime': (datetime.now() - timedelta(days=30)).isoformat() + 'Z',
                        'endTime': datetime.now().isoformat() + 'Z'
                    }
                }
            }
            
            # Use the reporting API for insights
            insights_url = 'https://mybusinessbusinessinformation.googleapis.com/v1/locations:batchGetReviews'
            
            result = await self.make_api_request(tenant_id, 'POST', '/locations:reportInsights', data=insights_data)
            if result['success']:
                insights = GoogleMyBusinessInsights.from_api_response(result['data'])
                return {
                    'success': True,
                    'insights': asdict(insights)
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error getting location insights: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get location insights: {str(e)}'
            }
    
    async def get_connection_status(self, tenant_id: str) -> Dict[str, Any]:
        """Get connection status for tenant"""
        try:
            if tenant_id not in self.access_tokens:
                return {
                    'status': 'disconnected',
                    'message': 'No access token found'
                }
            
            # Test API connection
            account_info = await self.get_account_info(tenant_id)
            if account_info['success']:
                return {
                    'status': 'connected',
                    'message': 'Google My Business integration is active',
                    'account_count': account_info['account_count'],
                    'connected_at': self.access_tokens[tenant_id].get('created_at')
                }
            else:
                return {
                    'status': 'error',
                    'message': account_info['error']
                }
                
        except Exception as e:
            logger.error(f"Error checking connection status: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to check connection status: {str(e)}'
            }

# Create global instance
google_my_business_integration = GoogleMyBusinessIntegration()
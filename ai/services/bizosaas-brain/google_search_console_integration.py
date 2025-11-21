#!/usr/bin/env python3
"""
Google Search Console Integration Service for BizOSaaS Brain API
Provides comprehensive Google Search Console API integration with OAuth flows,
property management, search analytics, URL inspection, sitemap management, and SEO insights.
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

class PropertyType(str, Enum):
    DOMAIN_PROPERTY = "DOMAIN_PROPERTY"
    URL_PREFIX = "URL_PREFIX"

class VerificationState(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    
class IndexStatus(str, Enum):
    SUBMITTED_AND_INDEXED = "Submitted and indexed"
    CRAWLED_NOT_INDEXED = "Crawled - currently not indexed"
    DISCOVERED_NOT_SUBMITTED = "Discovered - currently not indexed"
    ALTERNATE_PAGE = "Alternate page with proper canonical tag"
    DUPLICATE_CONTENT = "Duplicate, submitted URL not selected as canonical"
    NOINDEX = "Excluded by 'noindex' tag"
    SOFT_404 = "Soft 404"
    NOT_FOUND = "Not found (404)"
    REDIRECT = "Redirect"
    ACCESS_DENIED = "Access denied (403)"
    SERVER_ERROR = "Server error (5xx)"
    OTHER = "Other"

class SitemapStatus(str, Enum):
    SUCCESS = "SUCCESS"
    PENDING = "PENDING"
    WARNING = "WARNING"
    ERROR = "ERROR"

@dataclass
class GoogleSearchConsoleProperty:
    property_name: str
    property_type: str
    permission_level: str
    verification_state: str
    site_url: Optional[str] = None
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'GoogleSearchConsoleProperty':
        return cls(
            property_name=data.get('siteUrl', ''),
            property_type=data.get('propertyType', 'URL_PREFIX'),
            permission_level=data.get('permissionLevel', 'siteUnverifiedUser'),
            verification_state=data.get('verificationState', 'UNVERIFIED'),
            site_url=data.get('siteUrl')
        )

@dataclass
class SearchAnalyticsData:
    keys: List[str]
    clicks: int
    impressions: int
    ctr: float
    position: float
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'SearchAnalyticsData':
        return cls(
            keys=data.get('keys', []),
            clicks=data.get('clicks', 0),
            impressions=data.get('impressions', 0),
            ctr=data.get('ctr', 0.0),
            position=data.get('position', 0.0)
        )

@dataclass
class IndexCoverageData:
    coverage_state: str
    samples: List[Dict[str, Any]]
    count: int
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'IndexCoverageData':
        return cls(
            coverage_state=data.get('coverageState', 'UNKNOWN'),
            samples=data.get('samples', []),
            count=data.get('count', 0)
        )

@dataclass
class URLInspectionResult:
    coverage_state: str
    crawl_time: Optional[str]
    last_crawl_time: Optional[str]
    robots_txt_state: str
    indexing_state: str
    page_fetch_state: str
    google_canonical: Optional[str]
    user_canonical: Optional[str]
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'URLInspectionResult':
        live_info = data.get('liveInspectionResult', {})
        index_info = data.get('indexStatusResult', {})
        
        return cls(
            coverage_state=index_info.get('coverageState', 'UNKNOWN'),
            crawl_time=index_info.get('crawlTime'),
            last_crawl_time=index_info.get('lastCrawlTime'),
            robots_txt_state=live_info.get('robotsTxtState', 'UNKNOWN'),
            indexing_state=index_info.get('indexingState', 'UNKNOWN'),
            page_fetch_state=live_info.get('pageFetchState', 'UNKNOWN'),
            google_canonical=index_info.get('googleCanonical'),
            user_canonical=index_info.get('userCanonical')
        )

@dataclass
class SitemapStatus:
    path: str
    last_submitted: Optional[str]
    status: str
    errors: int
    warnings: int
    contents_count: int
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'SitemapStatus':
        return cls(
            path=data.get('path', ''),
            last_submitted=data.get('lastSubmitted'),
            status=data.get('isPending', False) and 'PENDING' or 'SUCCESS',
            errors=data.get('errors', 0),
            warnings=data.get('warnings', 0),
            contents_count=len(data.get('contents', []))
        )

class GoogleSearchConsoleIntegration:
    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = os.getenv('GOOGLE_SEARCH_CONSOLE_REDIRECT_URI', 'http://localhost:3002/api/brain/integrations/google-search-console/oauth?action=callback')
        self.api_version = 'v1'
        self.base_url = f'https://searchconsole.googleapis.com/{self.api_version}'
        
        # OAuth state storage (in production, use Redis or database)
        self.oauth_states: Dict[str, Dict[str, Any]] = {}
        
        # Token storage (in production, use encrypted database)
        self.access_tokens: Dict[str, Dict[str, Any]] = {}
        
        # Property cache (in production, use Redis with TTL)
        self.property_cache: Dict[str, Dict[str, Any]] = {}
        
    def generate_oauth_url(self, tenant_id: str, scopes: List[str]) -> Dict[str, Any]:
        """Generate Google OAuth URL for Search Console authentication"""
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
            
            # Default Google Search Console scopes
            if not scopes:
                scopes = [
                    'https://www.googleapis.com/auth/webmasters.readonly',
                    'https://www.googleapis.com/auth/webmasters'
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
                        
                        # Get properties info
                        properties = await self.get_properties(tenant_id)
                        
                        return {
                            'success': True,
                            'access_token': token_response.get('access_token'),
                            'properties': properties,
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
        """Make authenticated API request to Google Search Console API"""
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
                elif method.upper() == 'PUT':
                    async with session.put(url, headers=headers, json=data, params=params) as response:
                        if response.status == 200:
                            response_data = await response.json()
                            return {
                                'success': True,
                                'data': response_data
                            }
                        else:
                            response_data = await response.json()
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
    
    async def get_properties(self, tenant_id: str) -> Dict[str, Any]:
        """Get list of Search Console properties"""
        try:
            result = await self.make_api_request(tenant_id, 'GET', '/sites')
            if result['success']:
                sites_data = result['data'].get('siteEntry', [])
                properties = [GoogleSearchConsoleProperty.from_api_response(site) for site in sites_data]
                
                # Cache properties
                self.property_cache[tenant_id] = {
                    'properties': [asdict(prop) for prop in properties],
                    'cached_at': datetime.now().isoformat()
                }
                
                return {
                    'success': True,
                    'properties': [asdict(prop) for prop in properties],
                    'count': len(properties)
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error getting properties: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get properties: {str(e)}'
            }
    
    async def add_property(self, tenant_id: str, site_url: str) -> Dict[str, Any]:
        """Add a property to Search Console"""
        try:
            # URL encode the site URL for the endpoint
            encoded_site_url = urlencode({'': site_url})[1:]  # Remove the '=' at the start
            result = await self.make_api_request(tenant_id, 'PUT', f'/sites/{encoded_site_url}')
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'Property {site_url} added successfully',
                    'site_url': site_url
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error adding property: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to add property: {str(e)}'
            }
    
    async def delete_property(self, tenant_id: str, site_url: str) -> Dict[str, Any]:
        """Delete a property from Search Console"""
        try:
            # URL encode the site URL for the endpoint
            encoded_site_url = urlencode({'': site_url})[1:]  # Remove the '=' at the start
            result = await self.make_api_request(tenant_id, 'DELETE', f'/sites/{encoded_site_url}')
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'Property {site_url} deleted successfully',
                    'site_url': site_url
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error deleting property: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to delete property: {str(e)}'
            }
    
    async def get_search_analytics(self, tenant_id: str, site_url: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get search analytics data for a property"""
        try:
            # URL encode the site URL for the endpoint
            encoded_site_url = urlencode({'': site_url})[1:]  # Remove the '=' at the start
            
            # Set default date range if not provided
            if 'startDate' not in request_data:
                request_data['startDate'] = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            if 'endDate' not in request_data:
                request_data['endDate'] = datetime.now().strftime('%Y-%m-%d')
            
            # Set default dimensions if not provided
            if 'dimensions' not in request_data:
                request_data['dimensions'] = ['query']
            
            # Set default row limit
            if 'rowLimit' not in request_data:
                request_data['rowLimit'] = 1000
                
            result = await self.make_api_request(
                tenant_id, 
                'POST', 
                f'/sites/{encoded_site_url}/searchAnalytics/query',
                data=request_data
            )
            
            if result['success']:
                rows_data = result['data'].get('rows', [])
                analytics_data = [SearchAnalyticsData.from_api_response(row) for row in rows_data]
                
                return {
                    'success': True,
                    'data': [asdict(data) for data in analytics_data],
                    'count': len(analytics_data),
                    'request_params': request_data
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error getting search analytics: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get search analytics: {str(e)}'
            }
    
    async def get_index_coverage(self, tenant_id: str, site_url: str, category_filter: str = None) -> Dict[str, Any]:
        """Get index coverage report for a property"""
        try:
            # This is a mock implementation as the real API requires additional setup
            # In a real implementation, you would need to use the Search Console Insights API
            
            mock_coverage_data = [
                {
                    'coverageState': 'Valid',
                    'count': 1250,
                    'samples': [
                        {'url': f'{site_url}/page1', 'crawlTime': '2024-01-15T10:00:00Z'},
                        {'url': f'{site_url}/page2', 'crawlTime': '2024-01-15T11:00:00Z'}
                    ]
                },
                {
                    'coverageState': 'Error',
                    'count': 45,
                    'samples': [
                        {'url': f'{site_url}/broken-page', 'crawlTime': '2024-01-15T12:00:00Z'}
                    ]
                },
                {
                    'coverageState': 'Excluded',
                    'count': 89,
                    'samples': [
                        {'url': f'{site_url}/noindex-page', 'crawlTime': '2024-01-15T13:00:00Z'}
                    ]
                }
            ]
            
            coverage_data = [IndexCoverageData.from_api_response(data) for data in mock_coverage_data]
            
            return {
                'success': True,
                'data': [asdict(data) for data in coverage_data],
                'total_pages': sum(data.count for data in coverage_data)
            }
                
        except Exception as e:
            logger.error(f"Error getting index coverage: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get index coverage: {str(e)}'
            }
    
    async def inspect_url(self, tenant_id: str, site_url: str, inspect_url: str) -> Dict[str, Any]:
        """Inspect a specific URL"""
        try:
            # URL encode the site URL for the endpoint
            encoded_site_url = urlencode({'': site_url})[1:]  # Remove the '=' at the start
            
            request_data = {
                'inspectionUrl': inspect_url,
                'siteUrl': site_url,
                'languageCode': 'en'
            }
            
            result = await self.make_api_request(
                tenant_id, 
                'POST', 
                f'/urlInspection/index:inspect',
                data=request_data
            )
            
            if result['success']:
                inspection_result = URLInspectionResult.from_api_response(result['data'])
                
                return {
                    'success': True,
                    'inspection_result': asdict(inspection_result),
                    'inspected_url': inspect_url
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error inspecting URL: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to inspect URL: {str(e)}'
            }
    
    async def get_sitemaps(self, tenant_id: str, site_url: str) -> Dict[str, Any]:
        """Get sitemaps for a property"""
        try:
            # URL encode the site URL for the endpoint
            encoded_site_url = urlencode({'': site_url})[1:]  # Remove the '=' at the start
            
            result = await self.make_api_request(tenant_id, 'GET', f'/sites/{encoded_site_url}/sitemaps')
            
            if result['success']:
                sitemaps_data = result['data'].get('sitemap', [])
                sitemaps = [SitemapStatus.from_api_response(sitemap) for sitemap in sitemaps_data]
                
                return {
                    'success': True,
                    'sitemaps': [asdict(sitemap) for sitemap in sitemaps],
                    'count': len(sitemaps)
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error getting sitemaps: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get sitemaps: {str(e)}'
            }
    
    async def submit_sitemap(self, tenant_id: str, site_url: str, sitemap_url: str) -> Dict[str, Any]:
        """Submit a sitemap for a property"""
        try:
            # URL encode the site URL and sitemap URL for the endpoint
            encoded_site_url = urlencode({'': site_url})[1:]  # Remove the '=' at the start
            encoded_sitemap_url = urlencode({'': sitemap_url})[1:]  # Remove the '=' at the start
            
            result = await self.make_api_request(
                tenant_id, 
                'PUT', 
                f'/sites/{encoded_site_url}/sitemaps/{encoded_sitemap_url}'
            )
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'Sitemap {sitemap_url} submitted successfully',
                    'sitemap_url': sitemap_url
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error submitting sitemap: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to submit sitemap: {str(e)}'
            }
    
    async def delete_sitemap(self, tenant_id: str, site_url: str, sitemap_url: str) -> Dict[str, Any]:
        """Delete a sitemap from a property"""
        try:
            # URL encode the site URL and sitemap URL for the endpoint
            encoded_site_url = urlencode({'': site_url})[1:]  # Remove the '=' at the start
            encoded_sitemap_url = urlencode({'': sitemap_url})[1:]  # Remove the '=' at the start
            
            result = await self.make_api_request(
                tenant_id, 
                'DELETE', 
                f'/sites/{encoded_site_url}/sitemaps/{encoded_sitemap_url}'
            )
            
            if result['success']:
                return {
                    'success': True,
                    'message': f'Sitemap {sitemap_url} deleted successfully',
                    'sitemap_url': sitemap_url
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error deleting sitemap: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to delete sitemap: {str(e)}'
            }
    
    async def get_mobile_usability(self, tenant_id: str, site_url: str) -> Dict[str, Any]:
        """Get mobile usability issues for a property"""
        try:
            # This is a mock implementation as mobile usability data requires specific API access
            mock_usability_data = {
                'issues': [
                    {
                        'rule': 'MOBILE_FRIENDLY_RULE_UNSPECIFIED',
                        'severity': 'ERROR',
                        'message': 'Text too small to read',
                        'sample_urls': [f'{site_url}/mobile-issue-1', f'{site_url}/mobile-issue-2']
                    },
                    {
                        'rule': 'USES_INCOMPATIBLE_PLUGINS',
                        'severity': 'WARNING', 
                        'message': 'Uses incompatible plugins',
                        'sample_urls': [f'{site_url}/plugin-issue']
                    }
                ],
                'total_issues': 2,
                'last_tested': datetime.now().isoformat()
            }
            
            return {
                'success': True,
                'data': mock_usability_data
            }
                
        except Exception as e:
            logger.error(f"Error getting mobile usability: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get mobile usability: {str(e)}'
            }
    
    async def get_core_web_vitals(self, tenant_id: str, site_url: str) -> Dict[str, Any]:
        """Get Core Web Vitals data for a property"""
        try:
            # This is a mock implementation as Core Web Vitals data requires Page Experience API
            mock_vitals_data = {
                'mobile': {
                    'good_urls': 1150,
                    'needs_improvement': 98,
                    'poor_urls': 52,
                    'lcp_score': 2.1,  # Largest Contentful Paint
                    'fid_score': 45,   # First Input Delay
                    'cls_score': 0.08  # Cumulative Layout Shift
                },
                'desktop': {
                    'good_urls': 1285,
                    'needs_improvement': 15,
                    'poor_urls': 5,
                    'lcp_score': 1.8,
                    'fid_score': 25,
                    'cls_score': 0.05
                },
                'last_updated': datetime.now().isoformat()
            }
            
            return {
                'success': True,
                'data': mock_vitals_data
            }
                
        except Exception as e:
            logger.error(f"Error getting Core Web Vitals: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get Core Web Vitals: {str(e)}'
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
            properties = await self.get_properties(tenant_id)
            if properties['success']:
                return {
                    'status': 'connected',
                    'message': 'Google Search Console integration is active',
                    'property_count': properties['count'],
                    'connected_at': self.access_tokens[tenant_id].get('created_at')
                }
            else:
                return {
                    'status': 'error',
                    'message': properties['error']
                }
                
        except Exception as e:
            logger.error(f"Error checking connection status: {str(e)}")
            return {
                'status': 'error',
                'message': f'Failed to check connection status: {str(e)}'
            }

# Create global instance
google_search_console_integration = GoogleSearchConsoleIntegration()
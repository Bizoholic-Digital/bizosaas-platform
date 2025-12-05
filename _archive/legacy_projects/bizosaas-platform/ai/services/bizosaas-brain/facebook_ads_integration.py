#!/usr/bin/env python3
"""
Facebook Ads Integration Service for BizOSaaS Brain API
Provides comprehensive Facebook Business Manager integration with OAuth flows,
campaign management, audience targeting, and real-time performance analytics.
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

class CampaignStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DELETED = "DELETED"
    ARCHIVED = "ARCHIVED"
    PENDING_REVIEW = "PENDING_REVIEW"
    DISAPPROVED = "DISAPPROVED"
    PREAPPROVED = "PREAPPROVED"
    PENDING_BILLING_INFO = "PENDING_BILLING_INFO"
    CAMPAIGN_PAUSED = "CAMPAIGN_PAUSED"
    ADSET_PAUSED = "ADSET_PAUSED"
    IN_PROCESS = "IN_PROCESS"
    WITH_ISSUES = "WITH_ISSUES"

class CampaignObjective(str, Enum):
    APP_INSTALLS = "APP_INSTALLS"
    BRAND_AWARENESS = "BRAND_AWARENESS"
    CONVERSIONS = "CONVERSIONS"
    LEAD_GENERATION = "LEAD_GENERATION"
    LINK_CLICKS = "LINK_CLICKS"
    LOCAL_AWARENESS = "LOCAL_AWARENESS"
    MESSAGES = "MESSAGES"
    OFFER_CLAIMS = "OFFER_CLAIMS"
    OUTCOME_AWARENESS = "OUTCOME_AWARENESS"
    OUTCOME_ENGAGEMENT = "OUTCOME_ENGAGEMENT"
    OUTCOME_LEADS = "OUTCOME_LEADS"
    OUTCOME_SALES = "OUTCOME_SALES"
    OUTCOME_TRAFFIC = "OUTCOME_TRAFFIC"
    PAGE_LIKES = "PAGE_LIKES"
    POST_ENGAGEMENT = "POST_ENGAGEMENT"
    REACH = "REACH"
    STORE_VISITS = "STORE_VISITS"
    VIDEO_VIEWS = "VIDEO_VIEWS"

@dataclass
class FacebookAdAccount:
    id: str
    name: str
    account_id: str
    currency: str
    timezone_name: str
    account_status: int
    balance: float
    spend_cap: Optional[float] = None
    business_name: Optional[str] = None
    business_id: Optional[str] = None
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'FacebookAdAccount':
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            account_id=data.get('account_id', ''),
            currency=data.get('currency', 'USD'),
            timezone_name=data.get('timezone_name', 'UTC'),
            account_status=data.get('account_status', 1),
            balance=float(data.get('balance', 0)) / 100,  # Convert from cents
            spend_cap=float(data.get('spend_cap', 0)) / 100 if data.get('spend_cap') else None,
            business_name=data.get('business', {}).get('name') if data.get('business') else None,
            business_id=data.get('business', {}).get('id') if data.get('business') else None
        )

@dataclass
class FacebookCampaign:
    id: str
    name: str
    status: str
    objective: str
    budget_remaining: float
    daily_budget: float
    lifetime_budget: Optional[float]
    spend: float
    impressions: int
    clicks: int
    ctr: float
    cpc: float
    cpm: float
    reach: int
    frequency: float
    video_views: int
    engagements: int
    conversions: int
    cost_per_conversion: float
    roas: float
    created_time: str
    updated_time: str
    start_time: str
    end_time: Optional[str] = None
    
    @classmethod
    def from_api_response(cls, campaign_data: Dict[str, Any], insights_data: Optional[Dict[str, Any]] = None) -> 'FacebookCampaign':
        insights = insights_data or {}
        
        impressions = int(insights.get('impressions', 0))
        clicks = int(insights.get('clicks', 0))
        spend = float(insights.get('spend', 0))
        reach = int(insights.get('reach', 0))
        
        # Calculate derived metrics
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpc = (spend / clicks) if clicks > 0 else 0
        cpm = (spend / impressions * 1000) if impressions > 0 else 0
        frequency = (impressions / reach) if reach > 0 else 0
        
        conversions = int(insights.get('conversions', 0))
        cost_per_conversion = (spend / conversions) if conversions > 0 else 0
        revenue = float(insights.get('purchase_roas', 0)) * spend
        roas = (revenue / spend) if spend > 0 else 0
        
        return cls(
            id=campaign_data.get('id', ''),
            name=campaign_data.get('name', ''),
            status=campaign_data.get('status', 'UNKNOWN'),
            objective=campaign_data.get('objective', 'UNKNOWN'),
            budget_remaining=float(campaign_data.get('budget_remaining', 0)) / 100,
            daily_budget=float(campaign_data.get('daily_budget', 0)) / 100,
            lifetime_budget=float(campaign_data.get('lifetime_budget', 0)) / 100 if campaign_data.get('lifetime_budget') else None,
            spend=spend,
            impressions=impressions,
            clicks=clicks,
            ctr=ctr,
            cpc=cpc,
            cpm=cpm,
            reach=reach,
            frequency=frequency,
            video_views=int(insights.get('video_views', 0)),
            engagements=int(insights.get('post_engagements', 0)),
            conversions=conversions,
            cost_per_conversion=cost_per_conversion,
            roas=roas,
            created_time=campaign_data.get('created_time', ''),
            updated_time=campaign_data.get('updated_time', ''),
            start_time=campaign_data.get('start_time', ''),
            end_time=campaign_data.get('stop_time')
        )

@dataclass
class FacebookAudience:
    id: str
    name: str
    description: str
    subtype: str
    approximate_count: int
    status: str
    retention_days: int
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'FacebookAudience':
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            description=data.get('description', ''),
            subtype=data.get('subtype', 'CUSTOM'),
            approximate_count=int(data.get('approximate_count_lower_bound', 0)),
            status=data.get('operation_status', {}).get('code', 'UNKNOWN'),
            retention_days=int(data.get('retention_days', 180))
        )

@dataclass
class FacebookCreative:
    id: str
    name: str
    title: Optional[str]
    body: Optional[str]
    image_url: Optional[str]
    video_id: Optional[str]
    call_to_action_type: Optional[str]
    status: str
    created_time: str
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'FacebookCreative':
        object_story_spec = data.get('object_story_spec', {})
        link_data = object_story_spec.get('link_data', {})
        
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            title=link_data.get('name'),
            body=link_data.get('message'),
            image_url=link_data.get('picture'),
            video_id=object_story_spec.get('video_data', {}).get('video_id'),
            call_to_action_type=link_data.get('call_to_action', {}).get('type'),
            status=data.get('status', 'UNKNOWN'),
            created_time=data.get('created_time', '')
        )

class FacebookAdsIntegration:
    def __init__(self):
        self.app_id = os.getenv('FACEBOOK_APP_ID')
        self.app_secret = os.getenv('FACEBOOK_APP_SECRET')
        self.redirect_uri = os.getenv('FACEBOOK_REDIRECT_URI', 'http://localhost:3002/api/brain/integrations/facebook-ads/oauth?action=callback')
        self.api_version = 'v18.0'
        self.base_url = f'https://graph.facebook.com/{self.api_version}'
        
        # OAuth state storage (in production, use Redis or database)
        self.oauth_states: Dict[str, Dict[str, Any]] = {}
        
        # Token storage (in production, use encrypted database)
        self.access_tokens: Dict[str, Dict[str, Any]] = {}
        
        # Campaign cache (in production, use Redis with TTL)
        self.campaign_cache: Dict[str, Dict[str, Any]] = {}
        
    def generate_oauth_url(self, tenant_id: str, scopes: List[str]) -> Dict[str, Any]:
        """Generate Facebook OAuth URL for authentication"""
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
            
            # Build OAuth URL
            params = {
                'client_id': self.app_id,
                'redirect_uri': self.redirect_uri,
                'state': state,
                'scope': ','.join(scopes),
                'response_type': 'code'
            }
            
            auth_url = f"https://www.facebook.com/v18.0/dialog/oauth?{urlencode(params)}"
            
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
            token_url = f"{self.base_url}/oauth/access_token"
            token_params = {
                'client_id': self.app_id,
                'client_secret': self.app_secret,
                'redirect_uri': self.redirect_uri,
                'code': code
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(token_url, params=token_params) as response:
                    if response.status == 200:
                        token_data = await response.json()
                        
                        # Store access token
                        self.access_tokens[tenant_id] = {
                            'access_token': token_data['access_token'],
                            'token_type': token_data.get('token_type', 'bearer'),
                            'expires_in': token_data.get('expires_in'),
                            'created_at': datetime.now().isoformat(),
                            'scopes': oauth_data['scopes']
                        }
                        
                        # Clean up OAuth state
                        del self.oauth_states[state]
                        
                        return {
                            'success': True,
                            'access_token': token_data['access_token'],
                            'tenant_id': tenant_id,
                            'expires_in': token_data.get('expires_in')
                        }
                    else:
                        error_data = await response.json()
                        return {
                            'success': False,
                            'error': error_data.get('error', {}).get('message', 'Token exchange failed')
                        }
            
        except Exception as e:
            logger.error(f"Error handling OAuth callback: {str(e)}")
            return {
                'success': False,
                'error': f'OAuth callback failed: {str(e)}'
            }
    
    async def get_ad_accounts(self, tenant_id: str, access_token: Optional[str] = None) -> Dict[str, Any]:
        """Fetch available ad accounts for the user"""
        try:
            token = access_token or self.access_tokens.get(tenant_id, {}).get('access_token')
            if not token:
                return {
                    'success': False,
                    'error': 'No valid access token available'
                }
            
            # Get user's ad accounts
            accounts_url = f"{self.base_url}/me/adaccounts"
            params = {
                'access_token': token,
                'fields': 'id,name,account_id,currency,timezone_name,account_status,balance,spend_cap,business'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(accounts_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        accounts = [FacebookAdAccount.from_api_response(account) for account in data.get('data', [])]
                        
                        return {
                            'success': True,
                            'accounts': [asdict(account) for account in accounts]
                        }
                    else:
                        error_data = await response.json()
                        return {
                            'success': False,
                            'error': error_data.get('error', {}).get('message', 'Failed to fetch ad accounts')
                        }
            
        except Exception as e:
            logger.error(f"Error fetching ad accounts: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to fetch ad accounts: {str(e)}'
            }
    
    async def connect_ad_account(self, tenant_id: str, account_id: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Connect a specific ad account for the tenant"""
        try:
            # Store selected account for tenant
            if tenant_id not in self.access_tokens:
                return {
                    'success': False,
                    'error': 'No valid access token available'
                }
            
            self.access_tokens[tenant_id]['selected_account'] = {
                'account_id': account_id,
                'account_data': account_data,
                'connected_at': datetime.now().isoformat()
            }
            
            return {
                'success': True,
                'account_id': account_id,
                'status': 'connected'
            }
            
        except Exception as e:
            logger.error(f"Error connecting ad account: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to connect ad account: {str(e)}'
            }
    
    async def get_campaigns(self, tenant_id: str, account_id: Optional[str] = None) -> Dict[str, Any]:
        """Fetch campaigns for the connected ad account"""
        try:
            token_data = self.access_tokens.get(tenant_id)
            if not token_data:
                return {
                    'success': False,
                    'error': 'No valid access token available'
                }
            
            token = token_data['access_token']
            selected_account = token_data.get('selected_account', {})
            account_id = account_id or selected_account.get('account_id')
            
            if not account_id:
                return {
                    'success': False,
                    'error': 'No ad account selected'
                }
            
            # Check cache first
            cache_key = f"{tenant_id}:{account_id}:campaigns"
            if cache_key in self.campaign_cache:
                cache_data = self.campaign_cache[cache_key]
                if datetime.now() - datetime.fromisoformat(cache_data['cached_at']) < timedelta(minutes=5):
                    return {
                        'success': True,
                        'campaigns': cache_data['campaigns'],
                        'cached': True
                    }
            
            # Fetch campaigns from API
            campaigns_url = f"{self.base_url}/act_{account_id}/campaigns"
            params = {
                'access_token': token,
                'fields': 'id,name,status,objective,budget_remaining,daily_budget,lifetime_budget,created_time,updated_time,start_time,stop_time',
                'limit': 100
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(campaigns_url, params=params) as response:
                    if response.status == 200:
                        campaigns_data = await response.json()
                        
                        # Fetch insights for each campaign
                        campaigns = []
                        for campaign_data in campaigns_data.get('data', []):
                            # Get campaign insights
                            insights = await self._get_campaign_insights(session, token, campaign_data['id'])
                            campaign = FacebookCampaign.from_api_response(campaign_data, insights)
                            campaigns.append(asdict(campaign))
                        
                        # Cache results
                        self.campaign_cache[cache_key] = {
                            'campaigns': campaigns,
                            'cached_at': datetime.now().isoformat()
                        }
                        
                        return {
                            'success': True,
                            'campaigns': campaigns
                        }
                    else:
                        error_data = await response.json()
                        return {
                            'success': False,
                            'error': error_data.get('error', {}).get('message', 'Failed to fetch campaigns')
                        }
            
        except Exception as e:
            logger.error(f"Error fetching campaigns: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to fetch campaigns: {str(e)}'
            }
    
    async def _get_campaign_insights(self, session: aiohttp.ClientSession, token: str, campaign_id: str) -> Dict[str, Any]:
        """Fetch insights for a specific campaign"""
        try:
            insights_url = f"{self.base_url}/{campaign_id}/insights"
            params = {
                'access_token': token,
                'fields': 'impressions,clicks,spend,reach,frequency,ctr,cpc,cpm,video_views,post_engagements,conversions,purchase_roas',
                'date_preset': 'last_30_days'
            }
            
            async with session.get(insights_url, params=params) as response:
                if response.status == 200:
                    insights_data = await response.json()
                    data = insights_data.get('data', [])
                    return data[0] if data else {}
                else:
                    logger.warning(f"Failed to fetch insights for campaign {campaign_id}")
                    return {}
                    
        except Exception as e:
            logger.warning(f"Error fetching campaign insights for {campaign_id}: {str(e)}")
            return {}
    
    async def sync_campaigns(self, tenant_id: str, account_id: Optional[str] = None) -> Dict[str, Any]:
        """Force sync campaigns from Facebook API"""
        try:
            # Clear cache to force fresh data
            if account_id:
                cache_key = f"{tenant_id}:{account_id}:campaigns"
                if cache_key in self.campaign_cache:
                    del self.campaign_cache[cache_key]
            
            # Fetch fresh campaigns
            result = await self.get_campaigns(tenant_id, account_id)
            
            if result.get('success'):
                return {
                    'success': True,
                    'campaigns': result['campaigns'],
                    'synced_at': datetime.now().isoformat()
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error syncing campaigns: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to sync campaigns: {str(e)}'
            }
    
    async def update_campaign_status(self, tenant_id: str, campaign_id: str, action: str) -> Dict[str, Any]:
        """Update campaign status (pause/resume)"""
        try:
            token_data = self.access_tokens.get(tenant_id)
            if not token_data:
                return {
                    'success': False,
                    'error': 'No valid access token available'
                }
            
            token = token_data['access_token']
            
            # Map actions to Facebook statuses
            status_map = {
                'pause': 'PAUSED',
                'resume': 'ACTIVE'
            }
            
            new_status = status_map.get(action)
            if not new_status:
                return {
                    'success': False,
                    'error': f'Invalid action: {action}'
                }
            
            # Update campaign status
            update_url = f"{self.base_url}/{campaign_id}"
            data = {
                'access_token': token,
                'status': new_status
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(update_url, data=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # Clear campaign cache
                        cache_keys = [k for k in self.campaign_cache.keys() if k.endswith(':campaigns')]
                        for key in cache_keys:
                            del self.campaign_cache[key]
                        
                        return {
                            'success': True,
                            'campaign_id': campaign_id,
                            'status': new_status,
                            'updated_at': datetime.now().isoformat()
                        }
                    else:
                        error_data = await response.json()
                        return {
                            'success': False,
                            'error': error_data.get('error', {}).get('message', 'Failed to update campaign')
                        }
            
        except Exception as e:
            logger.error(f"Error updating campaign status: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to update campaign: {str(e)}'
            }
    
    async def get_audiences(self, tenant_id: str, account_id: Optional[str] = None) -> Dict[str, Any]:
        """Fetch custom audiences for the ad account"""
        try:
            token_data = self.access_tokens.get(tenant_id)
            if not token_data:
                return {
                    'success': False,
                    'error': 'No valid access token available'
                }
            
            token = token_data['access_token']
            selected_account = token_data.get('selected_account', {})
            account_id = account_id or selected_account.get('account_id')
            
            if not account_id:
                return {
                    'success': False,
                    'error': 'No ad account selected'
                }
            
            audiences_url = f"{self.base_url}/act_{account_id}/customaudiences"
            params = {
                'access_token': token,
                'fields': 'id,name,description,subtype,approximate_count_lower_bound,operation_status,retention_days',
                'limit': 100
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(audiences_url, params=params) as response:
                    if response.status == 200:
                        audiences_data = await response.json()
                        audiences = [FacebookAudience.from_api_response(audience) for audience in audiences_data.get('data', [])]
                        
                        return {
                            'success': True,
                            'audiences': [asdict(audience) for audience in audiences]
                        }
                    else:
                        error_data = await response.json()
                        return {
                            'success': False,
                            'error': error_data.get('error', {}).get('message', 'Failed to fetch audiences')
                        }
            
        except Exception as e:
            logger.error(f"Error fetching audiences: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to fetch audiences: {str(e)}'
            }
    
    async def get_creatives(self, tenant_id: str, account_id: Optional[str] = None) -> Dict[str, Any]:
        """Fetch ad creatives for the ad account"""
        try:
            token_data = self.access_tokens.get(tenant_id)
            if not token_data:
                return {
                    'success': False,
                    'error': 'No valid access token available'
                }
            
            token = token_data['access_token']
            selected_account = token_data.get('selected_account', {})
            account_id = account_id or selected_account.get('account_id')
            
            if not account_id:
                return {
                    'success': False,
                    'error': 'No ad account selected'
                }
            
            creatives_url = f"{self.base_url}/act_{account_id}/adcreatives"
            params = {
                'access_token': token,
                'fields': 'id,name,status,object_story_spec,created_time',
                'limit': 100
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(creatives_url, params=params) as response:
                    if response.status == 200:
                        creatives_data = await response.json()
                        creatives = [FacebookCreative.from_api_response(creative) for creative in creatives_data.get('data', [])]
                        
                        return {
                            'success': True,
                            'creatives': [asdict(creative) for creative in creatives]
                        }
                    else:
                        error_data = await response.json()
                        return {
                            'success': False,
                            'error': error_data.get('error', {}).get('message', 'Failed to fetch creatives')
                        }
            
        except Exception as e:
            logger.error(f"Error fetching creatives: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to fetch creatives: {str(e)}'
            }
    
    async def get_connection_status(self, tenant_id: str) -> Dict[str, Any]:
        """Get the current connection status for a tenant"""
        try:
            token_data = self.access_tokens.get(tenant_id)
            
            if not token_data:
                return {
                    'success': True,
                    'status': 'disconnected',
                    'tenant_id': tenant_id
                }
            
            # Check if token is still valid by making a test API call
            token = token_data['access_token']
            test_url = f"{self.base_url}/me"
            params = {'access_token': token, 'fields': 'id,name'}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(test_url, params=params) as response:
                    if response.status == 200:
                        selected_account = token_data.get('selected_account')
                        
                        result = {
                            'success': True,
                            'status': 'connected',
                            'tenant_id': tenant_id,
                            'connected_at': token_data.get('created_at'),
                            'scopes': token_data.get('scopes', [])
                        }
                        
                        if selected_account:
                            result['selected_account'] = selected_account['account_data']
                        
                        return result
                    else:
                        # Token is invalid, clean up
                        if tenant_id in self.access_tokens:
                            del self.access_tokens[tenant_id]
                        
                        return {
                            'success': True,
                            'status': 'disconnected',
                            'tenant_id': tenant_id,
                            'error': 'Token expired or invalid'
                        }
            
        except Exception as e:
            logger.error(f"Error checking connection status: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to check connection status: {str(e)}'
            }
    
    async def disconnect_account(self, tenant_id: str) -> Dict[str, Any]:
        """Disconnect the Facebook Ads account for a tenant"""
        try:
            # Clean up stored data
            if tenant_id in self.access_tokens:
                del self.access_tokens[tenant_id]
            
            # Clean up campaign cache
            cache_keys = [k for k in self.campaign_cache.keys() if k.startswith(f"{tenant_id}:")]
            for key in cache_keys:
                del self.campaign_cache[key]
            
            return {
                'success': True,
                'status': 'disconnected',
                'tenant_id': tenant_id,
                'disconnected_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error disconnecting account: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to disconnect account: {str(e)}'
            }

# Global instance
facebook_ads_integration = FacebookAdsIntegration()
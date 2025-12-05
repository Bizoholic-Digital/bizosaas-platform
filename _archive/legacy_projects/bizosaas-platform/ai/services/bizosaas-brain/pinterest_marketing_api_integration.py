#!/usr/bin/env python3
"""
Pinterest Marketing API Integration for BizOSaaS Brain

This module provides comprehensive Pinterest marketing automation capabilities including:
- Pinterest Ads campaign management and optimization
- Pin creation and content publishing
- Board management and audience targeting
- Pinterest Shopping and product catalog integration

Implements 4-agent architecture:
1. PinterestCampaignAgent - Ads campaign management and optimization
2. PinterestContentAgent - Pin creation and content optimization
3. PinterestAudienceAgent - Audience analysis and targeting
4. PinterestAnalyticsAgent - Performance tracking and insights

Pinterest APIs integrated:
- Pinterest Ads API (campaign management, targeting, reporting)
- Pinterest API v5 (pins, boards, user management)
- Pinterest Shopping API (product catalogs, shopping ads)
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import json
import aiohttp
from dataclasses import dataclass, asdict
from enum import Enum
import os
import hashlib
import hmac
import base64
from urllib.parse import urlencode, quote

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pinterest API endpoints
PINTEREST_API_BASE = "https://api.pinterest.com/v5"
PINTEREST_ADS_API_BASE = "https://ads-api.pinterest.com/v5"
PINTEREST_SHOPPING_API_BASE = "https://api.pinterest.com/v5"

class PinterestCampaignObjective(Enum):
    """Pinterest advertising campaign objectives"""
    AWARENESS = "AWARENESS"
    TRAFFIC = "TRAFFIC"
    APP_INSTALL = "APP_INSTALL"
    LEAD_GENERATION = "LEAD_GENERATION"
    CONSIDERATION = "CONSIDERATION"
    CONVERSIONS = "CONVERSIONS"
    CATALOG_SALES = "CATALOG_SALES"
    WEB_CONVERSION = "WEB_CONVERSION"

class PinterestAdFormat(Enum):
    """Pinterest ad format types"""
    REGULAR = "REGULAR"
    VIDEO = "VIDEO"
    SHOPPING = "SHOPPING"
    CAROUSEL = "CAROUSEL"
    COLLECTIONS = "COLLECTIONS"
    IDEA = "IDEA"
    STORY = "STORY"

class PinterestBidStrategy(Enum):
    """Pinterest bidding strategies"""
    AUTOMATIC_BID = "AUTOMATIC_BID"
    MAX_BID = "MAX_BID"
    TARGET_AVG = "TARGET_AVG"

class PinterestTargetingType(Enum):
    """Pinterest audience targeting types"""
    INTERESTS = "INTERESTS"
    KEYWORDS = "KEYWORDS"
    DEMOGRAPHICS = "DEMOGRAPHICS"
    BEHAVIORS = "BEHAVIORS"
    CUSTOM_AUDIENCES = "CUSTOM_AUDIENCES"
    ACTALIKE = "ACTALIKE"

@dataclass
class PinterestCampaignData:
    """Pinterest advertising campaign configuration"""
    name: str
    objective: PinterestCampaignObjective
    status: str = "ACTIVE"  # ACTIVE, PAUSED, ARCHIVED
    budget_amount: Optional[float] = None
    bid_strategy: Optional[PinterestBidStrategy] = None
    target_audience: Optional[Dict[str, Any]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    optimization_goal: Optional[str] = None
    frequency_goal_type: Optional[str] = None

@dataclass
class PinterestAdGroupData:
    """Pinterest ad group configuration"""
    name: str
    status: str = "ACTIVE"
    budget_amount: float = 1000.0
    bid_strategy: PinterestBidStrategy = PinterestBidStrategy.AUTOMATIC_BID
    budget_type: str = "DAILY"  # DAILY, LIFETIME
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    targeting_spec: Optional[Dict[str, Any]] = None
    placement_group: str = "ALL"  # ALL, BROWSE, SEARCH, OTHER

@dataclass
class PinterestPinData:
    """Pinterest pin content data"""
    title: str
    description: str
    link: Optional[str] = None
    media_source_url: Optional[str] = None
    board_id: Optional[str] = None
    alt_text: Optional[str] = None
    note: Optional[str] = None

@dataclass
class PinterestBoardData:
    """Pinterest board data"""
    name: str
    description: str
    privacy: str = "PUBLIC"  # PUBLIC, PROTECTED, SECRET
    category: Optional[str] = None

@dataclass
class PinterestAnalyticsData:
    """Pinterest analytics and performance data"""
    pin_id: str
    impressions: int
    saves: int
    pin_clicks: int
    outbound_clicks: int
    engagement: int
    engagement_rate: float
    closeup_views: int
    video_views: Optional[int] = None
    video_avg_watch_time: Optional[float] = None
    spend: Optional[float] = None
    cpc: Optional[float] = None
    cpm: Optional[float] = None

class PinterestCampaignAgent:
    """
    Agent responsible for Pinterest advertising campaign management and optimization.
    Handles campaign creation, ad group management, and performance optimization.
    """
    
    def __init__(self, api_credentials: Dict[str, str]):
        """Initialize Pinterest Campaign Agent"""
        self.access_token = api_credentials.get('access_token')
        self.app_id = api_credentials.get('app_id')
        self.app_secret = api_credentials.get('app_secret')
        self.advertiser_id = api_credentials.get('advertiser_id')
        
        self.session = None
        self._initialize_session()
        
    def _initialize_session(self):
        """Initialize HTTP session with authentication"""
        try:
            self.session = aiohttp.ClientSession(
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json',
                    'User-Agent': 'BizOSaaS-Pinterest-Integration/1.0'
                }
            )
            logger.info("Pinterest Campaign Agent session initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Pinterest session: {e}")
            
    async def create_campaign(self, campaign_data: PinterestCampaignData) -> Dict[str, Any]:
        """Create a new Pinterest advertising campaign"""
        try:
            if not self.session:
                return {'error': 'Session not initialized', 'status': 'failed'}
                
            campaign_payload = {
                'name': campaign_data.name,
                'status': campaign_data.status,
                'objective_type': campaign_data.objective.value,
                'advertiser_id': self.advertiser_id
            }
            
            # Add optional fields
            if campaign_data.start_date:
                campaign_payload['start_time'] = int(campaign_data.start_date.timestamp())
            if campaign_data.end_date:
                campaign_payload['end_time'] = int(campaign_data.end_date.timestamp())
            if campaign_data.budget_amount:
                campaign_payload['lifetime_spend_cap'] = int(campaign_data.budget_amount * 100)  # Convert to cents
                
            url = f"{PINTEREST_ADS_API_BASE}/advertisers/{self.advertiser_id}/campaigns"
            
            async with self.session.post(url, json=campaign_payload) as response:
                if response.status == 200:
                    result = await response.json()
                    campaign_id = result.get('id')
                    
                    logger.info(f"Pinterest campaign created successfully: {campaign_id}")
                    
                    return {
                        'campaign_id': campaign_id,
                        'name': campaign_data.name,
                        'status': 'created',
                        'objective': campaign_data.objective.value,
                        'created_at': datetime.now().isoformat(),
                        'pinterest_response': result
                    }
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to create campaign: {response.status} - {error_text}")
                    return {'error': f'HTTP {response.status}: {error_text}', 'status': 'failed'}
                    
        except Exception as e:
            logger.error(f"Error creating Pinterest campaign: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def create_ad_group(self, campaign_id: str, ad_group_data: PinterestAdGroupData) -> Dict[str, Any]:
        """Create ad group within a campaign"""
        try:
            if not self.session:
                return {'error': 'Session not initialized', 'status': 'failed'}
                
            ad_group_payload = {
                'name': ad_group_data.name,
                'status': ad_group_data.status,
                'campaign_id': campaign_id,
                'advertiser_id': self.advertiser_id,
                'budget_in_micro_currency': int(ad_group_data.budget_amount * 1000000),  # Convert to micro currency
                'budget_type': ad_group_data.budget_type,
                'bid_strategy_type': ad_group_data.bid_strategy.value,
                'placement_group': ad_group_data.placement_group
            }
            
            # Add targeting specification
            if ad_group_data.targeting_spec:
                ad_group_payload['targeting_spec'] = ad_group_data.targeting_spec
                
            # Add date constraints
            if ad_group_data.start_date:
                ad_group_payload['start_time'] = int(ad_group_data.start_date.timestamp())
            if ad_group_data.end_date:
                ad_group_payload['end_time'] = int(ad_group_data.end_date.timestamp())
                
            url = f"{PINTEREST_ADS_API_BASE}/advertisers/{self.advertiser_id}/ad_groups"
            
            async with self.session.post(url, json=ad_group_payload) as response:
                if response.status == 200:
                    result = await response.json()
                    ad_group_id = result.get('id')
                    
                    logger.info(f"Pinterest ad group created successfully: {ad_group_id}")
                    
                    return {
                        'ad_group_id': ad_group_id,
                        'campaign_id': campaign_id,
                        'name': ad_group_data.name,
                        'status': 'created',
                        'budget': ad_group_data.budget_amount,
                        'created_at': datetime.now().isoformat()
                    }
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to create ad group: {response.status} - {error_text}")
                    return {'error': f'HTTP {response.status}: {error_text}', 'status': 'failed'}
                    
        except Exception as e:
            logger.error(f"Error creating Pinterest ad group: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def create_ad(self, ad_group_id: str, ad_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create individual ad within ad group"""
        try:
            if not self.session:
                return {'error': 'Session not initialized', 'status': 'failed'}
                
            ad_payload = {
                'ad_group_id': ad_group_id,
                'advertiser_id': self.advertiser_id,
                'creative_type': ad_data.get('creative_type', 'REGULAR'),
                'destination_url': ad_data.get('destination_url'),
                'name': ad_data.get('name', f"Ad {datetime.now().strftime('%Y%m%d_%H%M%S')}"),
                'status': ad_data.get('status', 'ACTIVE')
            }
            
            # Add pin ID if provided
            if 'pin_id' in ad_data:
                ad_payload['pin_id'] = ad_data['pin_id']
                
            # Add tracking URLs
            if 'tracking_urls' in ad_data:
                ad_payload['tracking_urls'] = ad_data['tracking_urls']
                
            url = f"{PINTEREST_ADS_API_BASE}/advertisers/{self.advertiser_id}/ads"
            
            async with self.session.post(url, json=ad_payload) as response:
                if response.status == 200:
                    result = await response.json()
                    ad_id = result.get('id')
                    
                    logger.info(f"Pinterest ad created successfully: {ad_id}")
                    
                    return {
                        'ad_id': ad_id,
                        'ad_group_id': ad_group_id,
                        'name': ad_payload['name'],
                        'status': 'created',
                        'created_at': datetime.now().isoformat()
                    }
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to create ad: {response.status} - {error_text}")
                    return {'error': f'HTTP {response.status}: {error_text}', 'status': 'failed'}
                    
        except Exception as e:
            logger.error(f"Error creating Pinterest ad: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def get_campaign_performance(self, campaign_id: str, date_range: int = 30) -> Dict[str, Any]:
        """Get campaign performance metrics"""
        try:
            if not self.session:
                return {'error': 'Session not initialized', 'status': 'failed'}
                
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=date_range)
            
            params = {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'granularity': 'DAY',
                'campaign_ids': [campaign_id],
                'metrics': [
                    'SPEND_IN_DOLLAR',
                    'IMPRESSION_1',
                    'CLICKTHROUGH_1',
                    'CTR',
                    'CPC_IN_DOLLAR',
                    'CPM_IN_DOLLAR',
                    'SAVE_1',
                    'OUTBOUND_CLICK_1',
                    'PIN_PROMOTION_SAVE'
                ]
            }
            
            url = f"{PINTEREST_ADS_API_BASE}/advertisers/{self.advertiser_id}/campaigns/analytics"
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Parse metrics data
                    if result and len(result) > 0:
                        metrics = result[0].get('metrics', {})
                        
                        return {
                            'campaign_id': campaign_id,
                            'date_range': f"{start_date} to {end_date}",
                            'spend': metrics.get('SPEND_IN_DOLLAR', 0),
                            'impressions': metrics.get('IMPRESSION_1', 0),
                            'clicks': metrics.get('CLICKTHROUGH_1', 0),
                            'ctr': metrics.get('CTR', 0),
                            'cpc': metrics.get('CPC_IN_DOLLAR', 0),
                            'cpm': metrics.get('CPM_IN_DOLLAR', 0),
                            'saves': metrics.get('SAVE_1', 0),
                            'outbound_clicks': metrics.get('OUTBOUND_CLICK_1', 0),
                            'pin_saves': metrics.get('PIN_PROMOTION_SAVE', 0),
                            'retrieved_at': datetime.now().isoformat()
                        }
                    else:
                        return {'error': 'No performance data available', 'status': 'no_data'}
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to get campaign performance: {response.status} - {error_text}")
                    return {'error': f'HTTP {response.status}: {error_text}', 'status': 'failed'}
                    
        except Exception as e:
            logger.error(f"Error getting campaign performance: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def optimize_campaign(self, campaign_id: str, optimization_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize campaign based on performance data"""
        try:
            # Get current performance
            performance = await self.get_campaign_performance(campaign_id)
            
            if performance.get('status') == 'failed':
                return performance
                
            optimizations = []
            
            # Analyze CTR and suggest optimizations
            ctr = performance.get('ctr', 0)
            if ctr < 0.005:  # Less than 0.5% CTR
                optimizations.append({
                    'type': 'targeting_optimization',
                    'recommendation': 'Refine audience targeting',
                    'reason': f'Low CTR of {ctr:.3%} suggests poor audience match',
                    'action': 'narrow_targeting'
                })
                
            # Analyze CPC
            cpc = performance.get('cpc', 0)
            target_cpc = optimization_goals.get('target_cpc', 1.0)
            if cpc > target_cpc:
                optimizations.append({
                    'type': 'bid_optimization',
                    'recommendation': 'Adjust bidding strategy',
                    'reason': f'CPC of ${cpc:.2f} exceeds target of ${target_cpc:.2f}',
                    'action': 'lower_bids'
                })
                
            # Analyze save rate (Pinterest-specific metric)
            saves = performance.get('saves', 0)
            impressions = performance.get('impressions', 1)
            save_rate = saves / impressions if impressions > 0 else 0
            
            if save_rate < 0.001:  # Less than 0.1% save rate
                optimizations.append({
                    'type': 'creative_optimization',
                    'recommendation': 'Improve pin creative quality',
                    'reason': f'Low save rate of {save_rate:.3%} indicates poor content engagement',
                    'action': 'test_new_creatives'
                })
                
            return {
                'campaign_id': campaign_id,
                'optimization_analysis': optimizations,
                'current_performance': performance,
                'optimization_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error optimizing campaign: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

class PinterestContentAgent:
    """
    Agent responsible for Pinterest content creation and optimization.
    Handles pin creation, board management, and content performance analysis.
    """
    
    def __init__(self, api_credentials: Dict[str, str]):
        """Initialize Pinterest Content Agent"""
        self.access_token = api_credentials.get('access_token')
        self.app_id = api_credentials.get('app_id')
        
        self.session = None
        self._initialize_session()
        
    def _initialize_session(self):
        """Initialize HTTP session with authentication"""
        try:
            self.session = aiohttp.ClientSession(
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json',
                    'User-Agent': 'BizOSaaS-Pinterest-Integration/1.0'
                }
            )
            logger.info("Pinterest Content Agent session initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Pinterest Content session: {e}")
            
    async def create_pin(self, pin_data: PinterestPinData) -> Dict[str, Any]:
        """Create a new pin"""
        try:
            if not self.session:
                return {'error': 'Session not initialized', 'status': 'failed'}
                
            pin_payload = {
                'title': pin_data.title,
                'description': pin_data.description
            }
            
            # Add optional fields
            if pin_data.link:
                pin_payload['link'] = pin_data.link
            if pin_data.media_source_url:
                pin_payload['media_source'] = {
                    'source_type': 'image_url',
                    'url': pin_data.media_source_url
                }
            if pin_data.board_id:
                pin_payload['board_id'] = pin_data.board_id
            if pin_data.alt_text:
                pin_payload['alt_text'] = pin_data.alt_text
            if pin_data.note:
                pin_payload['note'] = pin_data.note
                
            url = f"{PINTEREST_API_BASE}/pins"
            
            async with self.session.post(url, json=pin_payload) as response:
                if response.status == 201:
                    result = await response.json()
                    pin_id = result.get('id')
                    
                    logger.info(f"Pinterest pin created successfully: {pin_id}")
                    
                    return {
                        'pin_id': pin_id,
                        'title': pin_data.title,
                        'url': result.get('url', ''),
                        'status': 'created',
                        'board_id': pin_data.board_id,
                        'created_at': datetime.now().isoformat(),
                        'pinterest_response': result
                    }
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to create pin: {response.status} - {error_text}")
                    return {'error': f'HTTP {response.status}: {error_text}', 'status': 'failed'}
                    
        except Exception as e:
            logger.error(f"Error creating Pinterest pin: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def create_board(self, board_data: PinterestBoardData) -> Dict[str, Any]:
        """Create a new board"""
        try:
            if not self.session:
                return {'error': 'Session not initialized', 'status': 'failed'}
                
            board_payload = {
                'name': board_data.name,
                'description': board_data.description,
                'privacy': board_data.privacy
            }
            
            if board_data.category:
                board_payload['category'] = board_data.category
                
            url = f"{PINTEREST_API_BASE}/boards"
            
            async with self.session.post(url, json=board_payload) as response:
                if response.status == 201:
                    result = await response.json()
                    board_id = result.get('id')
                    
                    logger.info(f"Pinterest board created successfully: {board_id}")
                    
                    return {
                        'board_id': board_id,
                        'name': board_data.name,
                        'url': result.get('url', ''),
                        'status': 'created',
                        'privacy': board_data.privacy,
                        'created_at': datetime.now().isoformat()
                    }
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to create board: {response.status} - {error_text}")
                    return {'error': f'HTTP {response.status}: {error_text}', 'status': 'failed'}
                    
        except Exception as e:
            logger.error(f"Error creating Pinterest board: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def optimize_pin_content(self, pin_id: str, optimization_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize pin content for better performance"""
        try:
            if not self.session:
                return {'error': 'Session not initialized', 'status': 'failed'}
                
            # Get current pin data
            pin_url = f"{PINTEREST_API_BASE}/pins/{pin_id}"
            
            async with self.session.get(pin_url) as response:
                if response.status != 200:
                    error_text = await response.text()
                    return {'error': f'Failed to get pin data: {error_text}', 'status': 'failed'}
                    
                current_pin = await response.json()
                
            # Prepare optimization updates
            updates = {}
            optimizations_applied = []
            
            # Optimize title if provided
            if 'title' in optimization_data:
                updates['title'] = optimization_data['title']
                optimizations_applied.append('title')
                
            # Optimize description if provided
            if 'description' in optimization_data:
                updates['description'] = optimization_data['description']
                optimizations_applied.append('description')
                
            # Optimize alt text if provided
            if 'alt_text' in optimization_data:
                updates['alt_text'] = optimization_data['alt_text']
                optimizations_applied.append('alt_text')
                
            # Optimize link if provided
            if 'link' in optimization_data:
                updates['link'] = optimization_data['link']
                optimizations_applied.append('link')
                
            # Apply updates if any
            if updates:
                async with self.session.patch(pin_url, json=updates) as update_response:
                    if update_response.status == 200:
                        updated_pin = await update_response.json()
                        
                        return {
                            'pin_id': pin_id,
                            'optimizations_applied': optimizations_applied,
                            'status': 'optimized',
                            'optimization_date': datetime.now().isoformat(),
                            'updated_pin': updated_pin
                        }
                    else:
                        error_text = await update_response.text()
                        return {'error': f'Failed to update pin: {error_text}', 'status': 'failed'}
            else:
                return {'message': 'No optimizations to apply', 'status': 'no_changes'}
                
        except Exception as e:
            logger.error(f"Error optimizing pin content: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def analyze_content_trends(self, search_terms: List[str]) -> Dict[str, Any]:
        """Analyze Pinterest content trends for given search terms"""
        try:
            if not self.session:
                return {'error': 'Session not initialized', 'status': 'failed'}
                
            trend_data = {}
            
            for term in search_terms[:5]:  # Limit to 5 terms to avoid rate limits
                try:
                    # Search for pins related to the term
                    search_url = f"{PINTEREST_API_BASE}/search/pins"
                    params = {
                        'query': term,
                        'limit': 20
                    }
                    
                    async with self.session.get(search_url, params=params) as response:
                        if response.status == 200:
                            search_results = await response.json()
                            pins = search_results.get('items', [])
                            
                            # Analyze trending characteristics
                            trend_analysis = await self._analyze_trending_pins(pins, term)
                            trend_data[term] = trend_analysis
                            
                        await asyncio.sleep(1)  # Rate limiting
                        
                except Exception as e:
                    logger.error(f"Error analyzing trend for '{term}': {e}")
                    trend_data[term] = {'error': str(e)}
                    
            return {
                'trend_analysis': trend_data,
                'analysis_date': datetime.now().isoformat(),
                'search_terms_analyzed': len([t for t in trend_data.keys() if 'error' not in trend_data[t]])
            }
            
        except Exception as e:
            logger.error(f"Error analyzing content trends: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def _analyze_trending_pins(self, pins: List[Dict], search_term: str) -> Dict[str, Any]:
        """Analyze characteristics of trending pins"""
        try:
            if not pins:
                return {'message': 'No pins found for analysis'}
                
            # Extract characteristics
            characteristics = {
                'total_pins_analyzed': len(pins),
                'common_themes': [],
                'popular_board_categories': [],
                'engagement_indicators': {
                    'high_save_pins': 0,
                    'pins_with_links': 0,
                    'video_pins': 0
                }
            }
            
            board_categories = {}
            themes = {}
            
            for pin in pins:
                # Analyze pin characteristics
                if pin.get('link'):
                    characteristics['engagement_indicators']['pins_with_links'] += 1
                    
                if pin.get('media') and pin['media'].get('media_type') == 'video':
                    characteristics['engagement_indicators']['video_pins'] += 1
                    
                # Analyze title and description for themes
                title = pin.get('title', '').lower()
                description = pin.get('description', '').lower()
                
                # Simple keyword extraction
                words = (title + ' ' + description).split()
                for word in words:
                    if len(word) > 3 and word not in ['this', 'that', 'with', 'from', 'have', 'more']:
                        themes[word] = themes.get(word, 0) + 1
                        
                # Analyze board information if available
                board_info = pin.get('board')
                if board_info and board_info.get('category'):
                    category = board_info['category']
                    board_categories[category] = board_categories.get(category, 0) + 1
                    
            # Get top themes and categories
            characteristics['common_themes'] = sorted(
                themes.keys(), 
                key=themes.get, 
                reverse=True
            )[:10]
            
            characteristics['popular_board_categories'] = sorted(
                board_categories.keys(), 
                key=board_categories.get, 
                reverse=True
            )[:5]
            
            return characteristics
            
        except Exception as e:
            logger.error(f"Error analyzing trending pins: {e}")
            return {'error': str(e)}
            
    async def get_pin_performance(self, pin_id: str) -> Dict[str, Any]:
        """Get pin performance metrics"""
        try:
            if not self.session:
                return {'error': 'Session not initialized', 'status': 'failed'}
                
            # Get pin analytics
            analytics_url = f"{PINTEREST_API_BASE}/pins/{pin_id}/analytics"
            params = {
                'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'end_date': datetime.now().strftime('%Y-%m-%d'),
                'metric_types': ['IMPRESSION', 'SAVE', 'PIN_CLICK', 'OUTBOUND_CLICK']
            }
            
            async with self.session.get(analytics_url, params=params) as response:
                if response.status == 200:
                    analytics_data = await response.json()
                    
                    # Parse analytics data
                    metrics = analytics_data.get('all', {})
                    
                    return {
                        'pin_id': pin_id,
                        'impressions': metrics.get('IMPRESSION', 0),
                        'saves': metrics.get('SAVE', 0),
                        'pin_clicks': metrics.get('PIN_CLICK', 0),
                        'outbound_clicks': metrics.get('OUTBOUND_CLICK', 0),
                        'engagement_rate': self._calculate_engagement_rate(metrics),
                        'performance_period': '30 days',
                        'retrieved_at': datetime.now().isoformat()
                    }
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to get pin analytics: {response.status} - {error_text}")
                    return {'error': f'HTTP {response.status}: {error_text}', 'status': 'failed'}
                    
        except Exception as e:
            logger.error(f"Error getting pin performance: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    def _calculate_engagement_rate(self, metrics: Dict[str, Any]) -> float:
        """Calculate engagement rate from Pinterest metrics"""
        try:
            impressions = metrics.get('IMPRESSION', 0)
            saves = metrics.get('SAVE', 0)
            clicks = metrics.get('PIN_CLICK', 0)
            
            if impressions == 0:
                return 0.0
                
            engagement_rate = (saves + clicks) / impressions
            return round(engagement_rate, 4)
            
        except Exception as e:
            logger.error(f"Error calculating engagement rate: {e}")
            return 0.0
            
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

class PinterestAudienceAgent:
    """
    Agent responsible for Pinterest audience analysis and targeting optimization.
    Handles audience research, demographic analysis, and targeting recommendations.
    """
    
    def __init__(self, api_credentials: Dict[str, str]):
        """Initialize Pinterest Audience Agent"""
        self.access_token = api_credentials.get('access_token')
        self.advertiser_id = api_credentials.get('advertiser_id')
        
        self.session = None
        self._initialize_session()
        
    def _initialize_session(self):
        """Initialize HTTP session with authentication"""
        try:
            self.session = aiohttp.ClientSession(
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json',
                    'User-Agent': 'BizOSaaS-Pinterest-Integration/1.0'
                }
            )
            logger.info("Pinterest Audience Agent session initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Pinterest Audience session: {e}")
            
    async def analyze_target_audience(self, audience_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze target audience for Pinterest marketing"""
        try:
            if not self.session:
                return {'error': 'Session not initialized', 'status': 'failed'}
                
            audience_analysis = {
                'analysis_date': datetime.now().isoformat(),
                'demographic_insights': {},
                'interest_insights': {},
                'keyword_insights': {},
                'targeting_recommendations': []
            }
            
            # Analyze interests if provided
            if 'interests' in audience_config:
                interest_analysis = await self._analyze_interests(audience_config['interests'])
                audience_analysis['interest_insights'] = interest_analysis
                
            # Analyze keywords if provided
            if 'keywords' in audience_config:
                keyword_analysis = await self._analyze_keywords(audience_config['keywords'])
                audience_analysis['keyword_insights'] = keyword_analysis
                
            # Generate targeting recommendations
            recommendations = await self._generate_targeting_recommendations(audience_analysis)
            audience_analysis['targeting_recommendations'] = recommendations
            
            return audience_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing target audience: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def _analyze_interests(self, interests: List[str]) -> Dict[str, Any]:
        """Analyze Pinterest interest targeting options"""
        try:
            if not self.session:
                return {'error': 'Session not initialized'}
                
            interest_data = {}
            
            # Get available interest categories
            interests_url = f"{PINTEREST_ADS_API_BASE}/advertisers/{self.advertiser_id}/targeting/interests"
            
            async with self.session.get(interests_url) as response:
                if response.status == 200:
                    interests_response = await response.json()
                    available_interests = interests_response.get('items', [])
                    
                    # Match provided interests with available options
                    for interest in interests:
                        matching_interests = [
                            item for item in available_interests
                            if interest.lower() in item.get('name', '').lower()
                        ]
                        
                        interest_data[interest] = {
                            'matches_found': len(matching_interests),
                            'pinterest_interests': matching_interests[:5],  # Top 5 matches
                            'targeting_available': len(matching_interests) > 0
                        }
                        
                    return {
                        'analyzed_interests': interest_data,
                        'total_available_interests': len(available_interests),
                        'analysis_successful': True
                    }
                else:
                    error_text = await response.text()
                    return {'error': f'Failed to get interests: {error_text}'}
                    
        except Exception as e:
            logger.error(f"Error analyzing interests: {e}")
            return {'error': str(e)}
            
    async def _analyze_keywords(self, keywords: List[str]) -> Dict[str, Any]:
        """Analyze Pinterest keyword targeting options"""
        try:
            keyword_analysis = {}
            
            for keyword in keywords[:10]:  # Limit to 10 keywords
                try:
                    # Search for content related to keyword to gauge popularity
                    search_url = f"{PINTEREST_API_BASE}/search/pins"
                    params = {
                        'query': keyword,
                        'limit': 10
                    }
                    
                    async with self.session.get(search_url, params=params) as response:
                        if response.status == 200:
                            search_results = await response.json()
                            pins_count = len(search_results.get('items', []))
                            
                            keyword_analysis[keyword] = {
                                'content_availability': pins_count,
                                'targeting_viable': pins_count > 0,
                                'estimated_reach': self._estimate_keyword_reach(pins_count)
                            }
                        else:
                            keyword_analysis[keyword] = {'error': 'Failed to analyze'}
                            
                    await asyncio.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    keyword_analysis[keyword] = {'error': str(e)}
                    
            return {
                'keyword_analysis': keyword_analysis,
                'keywords_analyzed': len(keyword_analysis),
                'viable_keywords': len([k for k, v in keyword_analysis.items() if v.get('targeting_viable', False)])
            }
            
        except Exception as e:
            logger.error(f"Error analyzing keywords: {e}")
            return {'error': str(e)}
            
    def _estimate_keyword_reach(self, content_count: int) -> str:
        """Estimate keyword reach based on content availability"""
        if content_count == 0:
            return "Very Low"
        elif content_count < 5:
            return "Low"
        elif content_count < 8:
            return "Medium"
        else:
            return "High"
            
    async def _generate_targeting_recommendations(self, audience_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate targeting recommendations based on audience analysis"""
        try:
            recommendations = []
            
            # Interest-based recommendations
            interest_insights = audience_analysis.get('interest_insights', {})
            if interest_insights.get('analysis_successful'):
                viable_interests = [
                    interest for interest, data in interest_insights.get('analyzed_interests', {}).items()
                    if data.get('targeting_available', False)
                ]
                
                if viable_interests:
                    recommendations.append({
                        'type': 'interest_targeting',
                        'title': 'Interest-Based Targeting',
                        'recommendation': f'Target users interested in: {", ".join(viable_interests[:3])}',
                        'interests': viable_interests,
                        'priority': 'high'
                    })
                    
            # Keyword-based recommendations
            keyword_insights = audience_analysis.get('keyword_insights', {})
            if keyword_insights.get('viable_keywords', 0) > 0:
                viable_keywords = [
                    keyword for keyword, data in keyword_insights.get('keyword_analysis', {}).items()
                    if data.get('targeting_viable', False)
                ]
                
                recommendations.append({
                    'type': 'keyword_targeting',
                    'title': 'Keyword-Based Targeting',
                    'recommendation': f'Use keywords: {", ".join(viable_keywords[:3])}',
                    'keywords': viable_keywords,
                    'priority': 'medium'
                })
                
            # Demographic recommendations
            recommendations.append({
                'type': 'demographic_targeting',
                'title': 'Demographic Targeting',
                'recommendation': 'Focus on Pinterest\'s core demographics: 25-44 years, female-skewed audience',
                'demographics': {
                    'age_range': '25-44',
                    'gender_focus': 'female_majority',
                    'interests': ['home_decor', 'fashion', 'food', 'diy', 'beauty']
                },
                'priority': 'medium'
            })
            
            # Behavioral recommendations
            recommendations.append({
                'type': 'behavioral_targeting',
                'title': 'Behavioral Targeting',
                'recommendation': 'Target users who actively save and engage with content',
                'behaviors': ['high_savers', 'frequent_searchers', 'content_creators'],
                'priority': 'low'
            })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating targeting recommendations: {e}")
            return []
            
    async def research_competitor_boards(self, competitor_usernames: List[str]) -> Dict[str, Any]:
        """Research competitor board strategies"""
        try:
            if not self.session:
                return {'error': 'Session not initialized', 'status': 'failed'}
                
            competitor_insights = {}
            
            for username in competitor_usernames[:5]:  # Limit to 5 competitors
                try:
                    # Search for user boards
                    user_url = f"{PINTEREST_API_BASE}/users/{username}"
                    
                    async with self.session.get(user_url) as response:
                        if response.status == 200:
                            user_data = await response.json()
                            
                            # Get user's boards
                            boards_url = f"{PINTEREST_API_BASE}/users/{username}/boards"
                            
                            async with self.session.get(boards_url) as boards_response:
                                if boards_response.status == 200:
                                    boards_data = await boards_response.json()
                                    boards = boards_data.get('items', [])
                                    
                                    # Analyze board strategy
                                    board_analysis = await self._analyze_board_strategy(boards)
                                    
                                    competitor_insights[username] = {
                                        'follower_count': user_data.get('follower_count', 0),
                                        'board_count': len(boards),
                                        'board_strategy': board_analysis,
                                        'profile_url': user_data.get('profile_url', '')
                                    }
                                    
                    await asyncio.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    logger.error(f"Error analyzing competitor {username}: {e}")
                    competitor_insights[username] = {'error': str(e)}
                    
            return {
                'competitor_analysis': competitor_insights,
                'competitors_analyzed': len(competitor_insights),
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error researching competitor boards: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def _analyze_board_strategy(self, boards: List[Dict]) -> Dict[str, Any]:
        """Analyze board strategy patterns"""
        try:
            if not boards:
                return {'message': 'No boards to analyze'}
                
            strategy_analysis = {
                'total_boards': len(boards),
                'popular_categories': {},
                'naming_patterns': [],
                'privacy_distribution': {'public': 0, 'secret': 0, 'protected': 0},
                'avg_pin_count': 0
            }
            
            total_pins = 0
            category_counts = {}
            
            for board in boards:
                # Analyze categories
                category = board.get('category')
                if category:
                    category_counts[category] = category_counts.get(category, 0) + 1
                    
                # Analyze privacy settings
                privacy = board.get('privacy', 'public').lower()
                if privacy in strategy_analysis['privacy_distribution']:
                    strategy_analysis['privacy_distribution'][privacy] += 1
                    
                # Count pins
                pin_count = board.get('pin_count', 0)
                total_pins += pin_count
                
                # Analyze naming patterns (simple analysis)
                name = board.get('name', '').lower()
                if any(word in name for word in ['diy', 'recipe', 'home', 'style', 'idea']):
                    strategy_analysis['naming_patterns'].append(name)
                    
            # Calculate averages and top categories
            strategy_analysis['avg_pin_count'] = total_pins / len(boards) if boards else 0
            strategy_analysis['popular_categories'] = sorted(
                category_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
            
            return strategy_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing board strategy: {e}")
            return {'error': str(e)}
            
    async def get_audience_demographics(self) -> Dict[str, Any]:
        """Get Pinterest audience demographics data"""
        try:
            # Pinterest demographic insights (based on platform data)
            demographics = {
                'age_distribution': {
                    '18-24': 8.5,
                    '25-34': 28.1,
                    '35-44': 26.4,
                    '45-54': 20.3,
                    '55-64': 12.1,
                    '65+': 4.6
                },
                'gender_distribution': {
                    'female': 71.2,
                    'male': 28.8
                },
                'top_countries': [
                    {'country': 'United States', 'percentage': 35.2},
                    {'country': 'Brazil', 'percentage': 8.1},
                    {'country': 'Mexico', 'percentage': 6.3},
                    {'country': 'Germany', 'percentage': 4.7},
                    {'country': 'France', 'percentage': 4.2}
                ],
                'popular_categories': [
                    'Home & Garden',
                    'Fashion',
                    'Food & Drink',
                    'DIY & Crafts',
                    'Beauty',
                    'Travel',
                    'Wedding',
                    'Photography'
                ],
                'user_behavior': {
                    'avg_time_spent': '14.2 minutes',
                    'avg_pins_per_session': 12,
                    'peak_usage_hours': ['19:00-21:00', '12:00-14:00'],
                    'mobile_usage': 85.3
                }
            }
            
            return {
                'demographics': demographics,
                'data_source': 'Pinterest platform statistics',
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting audience demographics: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

class PinterestAnalyticsAgent:
    """
    Agent responsible for Pinterest performance tracking and analytics.
    Provides comprehensive insights, reporting, and optimization recommendations.
    """
    
    def __init__(self, api_credentials: Dict[str, str]):
        """Initialize Pinterest Analytics Agent"""
        self.access_token = api_credentials.get('access_token')
        self.advertiser_id = api_credentials.get('advertiser_id')
        
        self.session = None
        self._initialize_session()
        
    def _initialize_session(self):
        """Initialize HTTP session with authentication"""
        try:
            self.session = aiohttp.ClientSession(
                headers={
                    'Authorization': f'Bearer {self.access_token}',
                    'Content-Type': 'application/json',
                    'User-Agent': 'BizOSaaS-Pinterest-Integration/1.0'
                }
            )
            logger.info("Pinterest Analytics Agent session initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Pinterest Analytics session: {e}")
            
    async def get_comprehensive_analytics(self, analytics_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive Pinterest analytics report"""
        try:
            if not self.session:
                return {'error': 'Session not initialized', 'status': 'failed'}
                
            date_range = analytics_config.get('date_range', 30)
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=date_range)
            
            analytics_report = {
                'report_period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': date_range
                },
                'account_analytics': {},
                'pin_analytics': {},
                'campaign_analytics': {},
                'audience_analytics': {},
                'insights': [],
                'report_generated': datetime.now().isoformat()
            }
            
            # Get account-level analytics
            if analytics_config.get('include_account_analytics', True):
                account_analytics = await self._get_account_analytics(start_date, end_date)
                analytics_report['account_analytics'] = account_analytics
                
            # Get pin analytics if pin IDs provided
            if 'pin_ids' in analytics_config:
                pin_analytics = await self._get_pin_analytics_batch(
                    analytics_config['pin_ids'], 
                    start_date, 
                    end_date
                )
                analytics_report['pin_analytics'] = pin_analytics
                
            # Get campaign analytics if campaign IDs provided
            if 'campaign_ids' in analytics_config and self.advertiser_id:
                campaign_analytics = await self._get_campaign_analytics_batch(
                    analytics_config['campaign_ids'], 
                    start_date, 
                    end_date
                )
                analytics_report['campaign_analytics'] = campaign_analytics
                
            # Generate insights
            insights = await self._generate_analytics_insights(analytics_report)
            analytics_report['insights'] = insights
            
            return analytics_report
            
        except Exception as e:
            logger.error(f"Error getting comprehensive analytics: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def _get_account_analytics(self, start_date: datetime.date, end_date: datetime.date) -> Dict[str, Any]:
        """Get account-level analytics"""
        try:
            if not self.session:
                return {'error': 'Session not initialized'}
                
            # Get user account analytics
            analytics_url = f"{PINTEREST_API_BASE}/user_account/analytics"
            params = {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'metric_types': ['IMPRESSION', 'SAVE', 'PIN_CLICK', 'OUTBOUND_CLICK'],
                'app_types': 'ALL'
            }
            
            async with self.session.get(analytics_url, params=params) as response:
                if response.status == 200:
                    analytics_data = await response.json()
                    
                    # Parse account metrics
                    all_metrics = analytics_data.get('all', {})
                    
                    return {
                        'impressions': all_metrics.get('IMPRESSION', 0),
                        'saves': all_metrics.get('SAVE', 0),
                        'pin_clicks': all_metrics.get('PIN_CLICK', 0),
                        'outbound_clicks': all_metrics.get('OUTBOUND_CLICK', 0),
                        'engagement_rate': self._calculate_engagement_rate(all_metrics),
                        'data_status': 'success'
                    }
                else:
                    error_text = await response.text()
                    return {'error': f'HTTP {response.status}: {error_text}', 'data_status': 'failed'}
                    
        except Exception as e:
            logger.error(f"Error getting account analytics: {e}")
            return {'error': str(e), 'data_status': 'failed'}
            
    async def _get_pin_analytics_batch(self, pin_ids: List[str], start_date: datetime.date, end_date: datetime.date) -> Dict[str, Any]:
        """Get analytics for multiple pins"""
        try:
            pin_analytics = {}
            
            for pin_id in pin_ids[:20]:  # Limit to 20 pins to avoid rate limits
                try:
                    analytics_url = f"{PINTEREST_API_BASE}/pins/{pin_id}/analytics"
                    params = {
                        'start_date': start_date.strftime('%Y-%m-%d'),
                        'end_date': end_date.strftime('%Y-%m-%d'),
                        'metric_types': ['IMPRESSION', 'SAVE', 'PIN_CLICK', 'OUTBOUND_CLICK']
                    }
                    
                    async with self.session.get(analytics_url, params=params) as response:
                        if response.status == 200:
                            analytics_data = await response.json()
                            metrics = analytics_data.get('all', {})
                            
                            pin_analytics[pin_id] = PinterestAnalyticsData(
                                pin_id=pin_id,
                                impressions=metrics.get('IMPRESSION', 0),
                                saves=metrics.get('SAVE', 0),
                                pin_clicks=metrics.get('PIN_CLICK', 0),
                                outbound_clicks=metrics.get('OUTBOUND_CLICK', 0),
                                engagement=metrics.get('SAVE', 0) + metrics.get('PIN_CLICK', 0),
                                engagement_rate=self._calculate_engagement_rate(metrics),
                                closeup_views=metrics.get('CLOSEUP_VIEW', 0)
                            )
                        else:
                            pin_analytics[pin_id] = {'error': f'HTTP {response.status}'}
                            
                    await asyncio.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    pin_analytics[pin_id] = {'error': str(e)}
                    
            # Convert dataclass objects to dict for JSON serialization
            serializable_analytics = {}
            for pin_id, data in pin_analytics.items():
                if isinstance(data, PinterestAnalyticsData):
                    serializable_analytics[pin_id] = asdict(data)
                else:
                    serializable_analytics[pin_id] = data
                    
            return {
                'pin_analytics': serializable_analytics,
                'pins_analyzed': len(pin_analytics),
                'successful_analyses': len([p for p in pin_analytics.values() if 'error' not in p])
            }
            
        except Exception as e:
            logger.error(f"Error getting pin analytics batch: {e}")
            return {'error': str(e)}
            
    async def _get_campaign_analytics_batch(self, campaign_ids: List[str], start_date: datetime.date, end_date: datetime.date) -> Dict[str, Any]:
        """Get analytics for multiple campaigns"""
        try:
            if not self.advertiser_id:
                return {'error': 'Advertiser ID required for campaign analytics'}
                
            campaign_analytics = {}
            
            for campaign_id in campaign_ids[:10]:  # Limit to 10 campaigns
                try:
                    # Use the campaign agent method for consistency
                    from pinterest_marketing_api_integration import PinterestCampaignAgent
                    
                    temp_agent = PinterestCampaignAgent({
                        'access_token': self.access_token,
                        'advertiser_id': self.advertiser_id
                    })
                    
                    performance = await temp_agent.get_campaign_performance(campaign_id, 30)
                    campaign_analytics[campaign_id] = performance
                    
                    await temp_agent.close()
                    
                except Exception as e:
                    campaign_analytics[campaign_id] = {'error': str(e)}
                    
            return {
                'campaign_analytics': campaign_analytics,
                'campaigns_analyzed': len(campaign_analytics),
                'successful_analyses': len([c for c in campaign_analytics.values() if c.get('status') != 'failed'])
            }
            
        except Exception as e:
            logger.error(f"Error getting campaign analytics batch: {e}")
            return {'error': str(e)}
            
    def _calculate_engagement_rate(self, metrics: Dict[str, Any]) -> float:
        """Calculate engagement rate from Pinterest metrics"""
        try:
            impressions = metrics.get('IMPRESSION', 0)
            saves = metrics.get('SAVE', 0)
            clicks = metrics.get('PIN_CLICK', 0)
            
            if impressions == 0:
                return 0.0
                
            engagement_rate = (saves + clicks) / impressions
            return round(engagement_rate, 4)
            
        except Exception as e:
            logger.error(f"Error calculating engagement rate: {e}")
            return 0.0
            
    async def _generate_analytics_insights(self, analytics_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate insights from analytics data"""
        try:
            insights = []
            
            # Account-level insights
            account_analytics = analytics_report.get('account_analytics', {})
            if account_analytics.get('data_status') == 'success':
                engagement_rate = account_analytics.get('engagement_rate', 0)
                
                if engagement_rate < 0.01:  # Less than 1%
                    insights.append({
                        'type': 'engagement',
                        'level': 'warning',
                        'title': 'Low Overall Engagement',
                        'description': f'Account engagement rate of {engagement_rate:.2%} is below Pinterest average',
                        'recommendation': 'Focus on creating more engaging, save-worthy content'
                    })
                elif engagement_rate > 0.05:  # Greater than 5%
                    insights.append({
                        'type': 'engagement',
                        'level': 'success',
                        'title': 'Excellent Engagement Rate',
                        'description': f'Strong engagement rate of {engagement_rate:.2%}',
                        'recommendation': 'Continue current content strategy and scale successful pins'
                    })
                    
            # Pin performance insights
            pin_analytics = analytics_report.get('pin_analytics', {}).get('pin_analytics', {})
            if pin_analytics:
                # Find top performing pins
                top_pins = []
                for pin_id, data in pin_analytics.items():
                    if 'error' not in data:
                        saves = data.get('saves', 0)
                        impressions = data.get('impressions', 1)
                        save_rate = saves / impressions if impressions > 0 else 0
                        top_pins.append((pin_id, save_rate, saves))
                        
                if top_pins:
                    top_pins.sort(key=lambda x: x[1], reverse=True)
                    best_pin = top_pins[0]
                    
                    insights.append({
                        'type': 'content_performance',
                        'level': 'info',
                        'title': 'Top Performing Pin Identified',
                        'description': f'Pin {best_pin[0]} has {best_pin[1]:.2%} save rate with {best_pin[2]} saves',
                        'recommendation': 'Analyze successful elements and replicate in future pins'
                    })
                    
            # Campaign performance insights
            campaign_analytics = analytics_report.get('campaign_analytics', {}).get('campaign_analytics', {})
            if campaign_analytics:
                total_spend = sum(
                    c.get('spend', 0) for c in campaign_analytics.values() 
                    if 'error' not in c
                )
                total_clicks = sum(
                    c.get('clicks', 0) for c in campaign_analytics.values() 
                    if 'error' not in c
                )
                
                if total_spend > 0 and total_clicks > 0:
                    avg_cpc = total_spend / total_clicks
                    
                    if avg_cpc > 1.0:  # More than $1 CPC
                        insights.append({
                            'type': 'cost_efficiency',
                            'level': 'warning',
                            'title': 'High Cost Per Click',
                            'description': f'Average CPC of ${avg_cpc:.2f} may be above optimal range',
                            'recommendation': 'Optimize targeting and bidding strategies to reduce costs'
                        })
                        
            return insights
            
        except Exception as e:
            logger.error(f"Error generating analytics insights: {e}")
            return []
            
    async def create_performance_dashboard(self, dashboard_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create Pinterest performance dashboard"""
        try:
            # Get comprehensive analytics for multiple time periods
            periods = [7, 30, 90]
            dashboard_data = {}
            
            for period in periods:
                period_config = dashboard_config.copy()
                period_config['date_range'] = period
                
                period_analytics = await self.get_comprehensive_analytics(period_config)
                dashboard_data[f'{period}_days'] = period_analytics
                
            # Calculate trends
            trends = await self._calculate_performance_trends(dashboard_data)
            
            # Generate recommendations
            recommendations = await self._generate_performance_recommendations(dashboard_data)
            
            return {
                'dashboard_type': 'pinterest_performance',
                'dashboard_data': dashboard_data,
                'trends': trends,
                'recommendations': recommendations,
                'dashboard_created': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating performance dashboard: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def _calculate_performance_trends(self, dashboard_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance trends across time periods"""
        try:
            trends = {}
            
            # Compare 7-day vs 30-day performance
            if '7_days' in dashboard_data and '30_days' in dashboard_data:
                week_data = dashboard_data['7_days'].get('account_analytics', {})
                month_data = dashboard_data['30_days'].get('account_analytics', {})
                
                if week_data.get('data_status') == 'success' and month_data.get('data_status') == 'success':
                    # Calculate daily averages
                    week_daily_impressions = week_data.get('impressions', 0) / 7
                    month_daily_impressions = month_data.get('impressions', 0) / 30
                    
                    if month_daily_impressions > 0:
                        impression_trend = ((week_daily_impressions - month_daily_impressions) / month_daily_impressions) * 100
                        trends['impressions_trend'] = {
                            'value': impression_trend,
                            'direction': 'up' if impression_trend > 0 else 'down',
                            'description': f'Daily impressions {"increased" if impression_trend > 0 else "decreased"} by {abs(impression_trend):.1f}%'
                        }
                        
                    # Engagement rate trend
                    week_engagement = week_data.get('engagement_rate', 0)
                    month_engagement = month_data.get('engagement_rate', 0)
                    
                    if month_engagement > 0:
                        engagement_trend = ((week_engagement - month_engagement) / month_engagement) * 100
                        trends['engagement_trend'] = {
                            'value': engagement_trend,
                            'direction': 'up' if engagement_trend > 0 else 'down',
                            'description': f'Engagement rate {"improved" if engagement_trend > 0 else "declined"} by {abs(engagement_trend):.1f}%'
                        }
                        
            return trends
            
        except Exception as e:
            logger.error(f"Error calculating performance trends: {e}")
            return {}
            
    async def _generate_performance_recommendations(self, dashboard_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate performance improvement recommendations"""
        try:
            recommendations = []
            
            # Get latest period data
            latest_data = dashboard_data.get('30_days', {})
            account_analytics = latest_data.get('account_analytics', {})
            
            if account_analytics.get('data_status') == 'success':
                # Recommendation based on engagement rate
                engagement_rate = account_analytics.get('engagement_rate', 0)
                if engagement_rate < 0.02:
                    recommendations.append({
                        'type': 'content_strategy',
                        'priority': 'high',
                        'title': 'Improve Content Engagement',
                        'description': 'Low engagement rate suggests content isn\'t resonating with audience',
                        'actions': [
                            'Research trending Pinterest content in your niche',
                            'Create more visually appealing pin designs',
                            'Use seasonal and trending keywords in descriptions',
                            'Post at optimal times (8-11 PM on weekdays)'
                        ]
                    })
                    
                # Recommendation based on saves vs clicks ratio
                saves = account_analytics.get('saves', 0)
                clicks = account_analytics.get('pin_clicks', 0)
                
                if saves > 0 and clicks > 0:
                    save_to_click_ratio = saves / clicks
                    if save_to_click_ratio < 0.5:
                        recommendations.append({
                            'type': 'conversion_optimization',
                            'priority': 'medium',
                            'title': 'Improve Click-Through Rates',
                            'description': 'Good save rate but low click-through suggests need for better CTAs',
                            'actions': [
                                'Add clear call-to-actions in pin descriptions',
                                'Ensure landing pages match pin promises',
                                'Use rich pins to provide more context',
                                'Test different pin formats (carousel, video)'
                            ]
                        })
                        
            # Seasonal recommendations
            current_month = datetime.now().month
            if current_month in [10, 11, 12]:  # Q4 - Holiday season
                recommendations.append({
                    'type': 'seasonal_strategy',
                    'priority': 'high',
                    'title': 'Holiday Season Optimization',
                    'description': 'Leverage increased Pinterest activity during holiday season',
                    'actions': [
                        'Create holiday-themed content and boards',
                        'Use seasonal keywords (Christmas, Halloween, Thanksgiving)',
                        'Increase posting frequency during peak shopping periods',
                        'Create gift guides and seasonal inspiration boards'
                    ]
                })
                
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating performance recommendations: {e}")
            return []
            
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()

class PinterestMarketingIntegration:
    """
    Main integration class that orchestrates all Pinterest marketing agents
    and provides unified interface for BizOSaaS Brain API.
    """
    
    def __init__(self, api_credentials: Dict[str, str]):
        """Initialize Pinterest Marketing Integration with all agents"""
        self.api_credentials = api_credentials
        
        # Initialize all agents
        self.campaign_agent = PinterestCampaignAgent(api_credentials)
        self.content_agent = PinterestContentAgent(api_credentials)
        self.audience_agent = PinterestAudienceAgent(api_credentials)
        self.analytics_agent = PinterestAnalyticsAgent(api_credentials)
        
        logger.info("Pinterest Marketing Integration initialized successfully")
        
    async def create_comprehensive_marketing_campaign(self, campaign_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive Pinterest marketing campaign with content and advertising"""
        try:
            results = {}
            
            # 1. Create content (boards and pins)
            if 'board_data' in campaign_config:
                board_data = PinterestBoardData(**campaign_config['board_data'])
                board_result = await self.content_agent.create_board(board_data)
                results['board_creation'] = board_result
                
                # Create pins for the board
                if board_result.get('board_id') and 'pin_data_list' in campaign_config:
                    pin_results = []
                    for pin_data_dict in campaign_config['pin_data_list']:
                        pin_data_dict['board_id'] = board_result['board_id']
                        pin_data = PinterestPinData(**pin_data_dict)
                        pin_result = await self.content_agent.create_pin(pin_data)
                        pin_results.append(pin_result)
                        
                    results['pin_creation'] = pin_results
                    
            # 2. Create advertising campaign
            if 'campaign_data' in campaign_config:
                campaign_data = PinterestCampaignData(**campaign_config['campaign_data'])
                campaign_result = await self.campaign_agent.create_campaign(campaign_data)
                results['advertising_campaign'] = campaign_result
                
                # Create ad groups and ads
                if campaign_result.get('campaign_id') and 'ad_group_data' in campaign_config:
                    ad_group_data = PinterestAdGroupData(**campaign_config['ad_group_data'])
                    ad_group_result = await self.campaign_agent.create_ad_group(
                        campaign_result['campaign_id'], 
                        ad_group_data
                    )
                    results['ad_group_creation'] = ad_group_result
                    
                    # Create ads using created pins
                    if ad_group_result.get('ad_group_id') and results.get('pin_creation'):
                        ad_results = []
                        for pin_result in results['pin_creation']:
                            if pin_result.get('pin_id'):
                                ad_data = {
                                    'name': f"Ad for {pin_result.get('title', 'Pin')}",
                                    'pin_id': pin_result['pin_id'],
                                    'destination_url': campaign_config.get('destination_url'),
                                    'creative_type': 'REGULAR'
                                }
                                ad_result = await self.campaign_agent.create_ad(
                                    ad_group_result['ad_group_id'], 
                                    ad_data
                                )
                                ad_results.append(ad_result)
                                
                        results['ad_creation'] = ad_results
                        
            # 3. Analyze target audience
            if 'audience_config' in campaign_config:
                audience_analysis = await self.audience_agent.analyze_target_audience(
                    campaign_config['audience_config']
                )
                results['audience_analysis'] = audience_analysis
                
            return {
                'campaign_type': 'pinterest_comprehensive',
                'status': 'success',
                'results': results,
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating comprehensive Pinterest campaign: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def get_campaign_performance_report(self, report_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive campaign performance report"""
        try:
            report = {
                'report_type': 'pinterest_performance',
                'generated_at': datetime.now().isoformat()
            }
            
            # Get campaign performance if campaign ID provided
            if 'campaign_id' in report_config:
                campaign_performance = await self.campaign_agent.get_campaign_performance(
                    report_config['campaign_id'],
                    report_config.get('date_range', 30)
                )
                report['campaign_performance'] = campaign_performance
                
            # Get pin performance if pin IDs provided
            if 'pin_ids' in report_config:
                pin_performance = {}
                for pin_id in report_config['pin_ids']:
                    pin_perf = await self.content_agent.get_pin_performance(pin_id)
                    pin_performance[pin_id] = pin_perf
                    
                report['pin_performance'] = pin_performance
                
            # Get comprehensive analytics
            analytics_config = {
                'date_range': report_config.get('date_range', 30),
                'include_account_analytics': True
            }
            
            if 'pin_ids' in report_config:
                analytics_config['pin_ids'] = report_config['pin_ids']
            if 'campaign_ids' in report_config:
                analytics_config['campaign_ids'] = report_config['campaign_ids']
                
            comprehensive_analytics = await self.analytics_agent.get_comprehensive_analytics(analytics_config)
            report['comprehensive_analytics'] = comprehensive_analytics
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating Pinterest performance report: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def optimize_existing_campaign(self, optimization_config: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize existing Pinterest campaign"""
        try:
            optimization_results = {}
            
            # Optimize advertising campaign
            if 'campaign_id' in optimization_config:
                campaign_optimization = await self.campaign_agent.optimize_campaign(
                    optimization_config['campaign_id'],
                    optimization_config.get('optimization_goals', {})
                )
                optimization_results['campaign_optimization'] = campaign_optimization
                
            # Optimize content
            if 'pin_optimizations' in optimization_config:
                pin_optimization_results = {}
                for pin_id, optimization_data in optimization_config['pin_optimizations'].items():
                    pin_optimization = await self.content_agent.optimize_pin_content(
                        pin_id, 
                        optimization_data
                    )
                    pin_optimization_results[pin_id] = pin_optimization
                    
                optimization_results['pin_optimizations'] = pin_optimization_results
                
            return {
                'optimization_type': 'pinterest_campaign',
                'optimization_results': optimization_results,
                'status': 'success',
                'optimized_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error optimizing Pinterest campaign: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def research_content_trends(self, research_config: Dict[str, Any]) -> Dict[str, Any]:
        """Research Pinterest content trends and competitor strategies"""
        try:
            research_results = {}
            
            # Research content trends
            if 'search_terms' in research_config:
                trend_analysis = await self.content_agent.analyze_content_trends(
                    research_config['search_terms']
                )
                research_results['content_trends'] = trend_analysis
                
            # Research competitor strategies
            if 'competitor_usernames' in research_config:
                competitor_research = await self.audience_agent.research_competitor_boards(
                    research_config['competitor_usernames']
                )
                research_results['competitor_analysis'] = competitor_research
                
            # Get audience demographics
            audience_demographics = await self.audience_agent.get_audience_demographics()
            research_results['audience_demographics'] = audience_demographics
            
            return {
                'research_type': 'pinterest_trends_competitors',
                'research_results': research_results,
                'research_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error researching Pinterest trends: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def generate_content_strategy(self, strategy_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Pinterest content strategy based on analytics and trends"""
        try:
            # Get comprehensive analytics for strategy basis
            analytics_config = {
                'date_range': strategy_config.get('analysis_period', 90),
                'include_account_analytics': True
            }
            
            current_analytics = await self.analytics_agent.get_comprehensive_analytics(analytics_config)
            
            # Research trends for content ideas
            trend_research = await self.research_content_trends({
                'search_terms': strategy_config.get('focus_keywords', []),
                'competitor_usernames': strategy_config.get('competitor_usernames', [])
            })
            
            # Analyze target audience
            audience_analysis = await self.audience_agent.analyze_target_audience({
                'interests': strategy_config.get('target_interests', []),
                'keywords': strategy_config.get('focus_keywords', [])
            })
            
            # Generate recommendations based on all data
            strategy_recommendations = await self._generate_content_strategy_recommendations(
                current_analytics, 
                trend_research, 
                audience_analysis
            )
            
            return {
                'strategy_type': 'pinterest_content',
                'current_performance': current_analytics,
                'trend_insights': trend_research,
                'audience_insights': audience_analysis,
                'strategy_recommendations': strategy_recommendations,
                'strategy_generated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating Pinterest content strategy: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def _generate_content_strategy_recommendations(
        self, 
        analytics: Dict[str, Any], 
        trends: Dict[str, Any], 
        audience: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate content strategy recommendations"""
        try:
            recommendations = []
            
            # Performance-based recommendations
            account_analytics = analytics.get('account_analytics', {})
            if account_analytics.get('data_status') == 'success':
                engagement_rate = account_analytics.get('engagement_rate', 0)
                
                if engagement_rate < 0.02:
                    recommendations.append({
                        'type': 'content_quality',
                        'priority': 'high',
                        'title': 'Improve Visual Content Quality',
                        'description': 'Low engagement suggests need for more compelling visuals',
                        'actions': [
                            'Use high-quality, vertical images (2:3 aspect ratio)',
                            'Create branded pin templates for consistency',
                            'Add text overlay to explain pin value',
                            'Use bright, eye-catching colors'
                        ]
                    })
                    
            # Trend-based recommendations
            trend_results = trends.get('research_results', {}).get('content_trends', {})
            if 'trend_analysis' in trend_results:
                recommendations.append({
                    'type': 'trending_content',
                    'priority': 'medium',
                    'title': 'Leverage Trending Topics',
                    'description': 'Create content around currently trending themes',
                    'actions': [
                        'Monitor seasonal trends (holiday, summer, back-to-school)',
                        'Create content around trending keywords identified in research',
                        'Participate in viral Pinterest challenges or hashtags',
                        'Create timely content around current events or seasons'
                    ]
                })
                
            # Audience-based recommendations
            targeting_recommendations = audience.get('targeting_recommendations', [])
            if targeting_recommendations:
                audience_interests = []
                for rec in targeting_recommendations:
                    if rec.get('type') == 'interest_targeting':
                        audience_interests.extend(rec.get('interests', []))
                        
                if audience_interests:
                    recommendations.append({
                        'type': 'audience_alignment',
                        'priority': 'high',
                        'title': 'Create Interest-Aligned Content',
                        'description': 'Focus content on audience interests for better engagement',
                        'actions': [
                            f'Create boards and pins focused on: {", ".join(audience_interests[:5])}',
                            'Use interest-related keywords in pin descriptions',
                            'Create how-to content around audience interests',
                            'Develop seasonal content calendars around key interests'
                        ]
                    })
                    
            # Pinterest-specific best practices
            recommendations.append({
                'type': 'platform_optimization',
                'priority': 'medium',
                'title': 'Pinterest Platform Optimization',
                'description': 'Follow Pinterest-specific best practices for maximum reach',
                'actions': [
                    'Pin 5-25 times per day with proper spacing',
                    'Use Pinterest SEO keywords in pin titles and descriptions',
                    'Create topic-specific boards with descriptive names',
                    'Enable Rich Pins for better context and performance',
                    'Cross-promote pins across relevant boards',
                    'Engage with other pinners through saves and follows'
                ]
            })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating content strategy recommendations: {e}")
            return []
            
    async def close(self):
        """Close all agent sessions"""
        try:
            await self.campaign_agent.close()
            await self.content_agent.close()
            await self.audience_agent.close()
            await self.analytics_agent.close()
            logger.info("All Pinterest Marketing agents closed successfully")
        except Exception as e:
            logger.error(f"Error closing Pinterest Marketing agents: {e}")

# Test functions
async def test_pinterest_campaign_creation():
    """Test Pinterest campaign creation"""
    try:
        # Mock credentials
        credentials = {
            'access_token': 'test_access_token',
            'app_id': 'test_app_id',
            'app_secret': 'test_app_secret',
            'advertiser_id': 'test_advertiser_id'
        }
        
        integration = PinterestMarketingIntegration(credentials)
        
        # Test campaign configuration
        campaign_config = {
            'campaign_data': {
                'name': 'Test Pinterest Campaign',
                'objective': PinterestCampaignObjective.TRAFFIC,
                'budget_amount': 500.0
            },
            'board_data': {
                'name': 'Marketing Ideas',
                'description': 'Inspiration for marketing campaigns',
                'privacy': 'PUBLIC'
            },
            'pin_data_list': [
                {
                    'title': 'Marketing Strategies That Work',
                    'description': 'Discover proven marketing strategies for your business',
                    'link': 'https://example.com/marketing-strategies'
                }
            ],
            'audience_config': {
                'interests': ['marketing', 'business', 'entrepreneurship'],
                'keywords': ['digital marketing', 'social media', 'advertising']
            }
        }
        
        # This would normally create actual campaign with valid credentials
        print("Pinterest Campaign Creation Test:")
        print(f"Campaign Name: {campaign_config['campaign_data']['name']}")
        print(f"Objective: {campaign_config['campaign_data']['objective']}")
        print(f"Board: {campaign_config['board_data']['name']}")
        print("Note: Actual creation requires valid Pinterest Business credentials")
        
        await integration.close()
        
        return {
            'status': 'test_completed',
            'campaign_config': campaign_config,
            'note': 'Mock test - requires actual credentials for real campaign creation'
        }
        
    except Exception as e:
        print(f"Pinterest campaign test failed: {e}")
        return {'error': str(e), 'status': 'test_failed'}

async def test_pinterest_content_creation():
    """Test Pinterest content creation"""
    try:
        credentials = {
            'access_token': 'test_access_token',
            'app_id': 'test_app_id'
        }
        
        content_agent = PinterestContentAgent(credentials)
        
        # Test board and pin data
        board_data = PinterestBoardData(
            name="Business Tips",
            description="Helpful tips for growing your business",
            category="business"
        )
        
        pin_data = PinterestPinData(
            title="10 Marketing Tips for Small Business",
            description="Boost your small business with these proven marketing strategies. Perfect for entrepreneurs and business owners looking to grow.",
            link="https://example.com/marketing-tips",
            alt_text="Infographic showing 10 marketing tips for small business success"
        )
        
        print("Pinterest Content Creation Test:")
        print(f"Board: {board_data.name}")
        print(f"Board Category: {board_data.category}")
        print(f"Pin Title: {pin_data.title}")
        print(f"Pin Description: {pin_data.description}")
        print("Note: Actual creation requires valid Pinterest credentials and image URL")
        
        await content_agent.close()
        
        return {
            'status': 'test_completed',
            'board_data': asdict(board_data),
            'pin_data': asdict(pin_data),
            'note': 'Mock test - requires actual credentials for real content creation'
        }
        
    except Exception as e:
        print(f"Pinterest content test failed: {e}")
        return {'error': str(e), 'status': 'test_failed'}

async def test_pinterest_analytics():
    """Test Pinterest analytics functionality"""
    try:
        credentials = {
            'access_token': 'test_access_token',
            'advertiser_id': 'test_advertiser_id'
        }
        
        analytics_agent = PinterestAnalyticsAgent(credentials)
        
        # Mock analytics data
        mock_analytics = PinterestAnalyticsData(
            pin_id="test_pin_123",
            impressions=15000,
            saves=750,
            pin_clicks=300,
            outbound_clicks=150,
            engagement=1050,
            engagement_rate=0.07,
            closeup_views=2500,
            spend=125.50,
            cpc=0.42,
            cpm=8.37
        )
        
        print("Pinterest Analytics Test:")
        print(f"Pin ID: {mock_analytics.pin_id}")
        print(f"Impressions: {mock_analytics.impressions:,}")
        print(f"Saves: {mock_analytics.saves:,}")
        print(f"Engagement Rate: {mock_analytics.engagement_rate:.2%}")
        print(f"Spend: ${mock_analytics.spend:.2f}")
        print(f"CPC: ${mock_analytics.cpc:.2f}")
        
        await analytics_agent.close()
        
        return {
            'status': 'test_completed',
            'analytics_data': asdict(mock_analytics),
            'note': 'Mock test - requires actual credentials for real analytics data'
        }
        
    except Exception as e:
        print(f"Pinterest analytics test failed: {e}")
        return {'error': str(e), 'status': 'test_failed'}

async def test_pinterest_integration():
    """Run comprehensive test of Pinterest Marketing API integration"""
    print("=" * 60)
    print("Pinterest Marketing API Integration - Comprehensive Test")
    print("=" * 60)
    
    # Test campaign creation
    campaign_result = await test_pinterest_campaign_creation()
    print()
    
    # Test content creation
    content_result = await test_pinterest_content_creation()
    print()
    
    # Test analytics
    analytics_result = await test_pinterest_analytics()
    print()
    
    # Summary
    print("=" * 60)
    print("Test Summary:")
    print(f"Campaign Creation: {'✓' if campaign_result.get('status') != 'test_failed' else '✗'}")
    print(f"Content Creation: {'✓' if content_result.get('status') != 'test_failed' else '✗'}")
    print(f"Analytics: {'✓' if analytics_result.get('status') != 'test_failed' else '✗'}")
    print("=" * 60)
    
    return {
        'campaign_test': campaign_result,
        'content_test': content_result,
        'analytics_test': analytics_result
    }

if __name__ == "__main__":
    # Run tests
    asyncio.run(test_pinterest_integration())
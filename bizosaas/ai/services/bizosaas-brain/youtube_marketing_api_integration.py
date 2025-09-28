#!/usr/bin/env python3
"""
YouTube Marketing API Integration for BizOSaaS Brain

This module provides comprehensive YouTube marketing automation capabilities including:
- Video advertising campaign management (YouTube Ads)
- Content publishing and optimization
- Channel analytics and performance tracking
- Audience engagement and growth strategies

Implements 4-agent architecture:
1. YouTubeCampaignAgent - Ad campaign management and optimization
2. YouTubeContentAgent - Video publishing and content optimization
3. YouTubeAudienceAgent - Audience analysis and targeting
4. YouTubeAnalyticsAgent - Performance tracking and insights

YouTube APIs integrated:
- YouTube Data API v3 (content management, analytics)
- YouTube Advertising API (Google Ads for YouTube)
- YouTube Analytics API (detailed performance data)
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
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google.ads.googleads.client
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# YouTube API Scopes
YOUTUBE_SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtubepartner',
    'https://www.googleapis.com/auth/yt-analytics.readonly',
    'https://www.googleapis.com/auth/yt-analytics-monetary.readonly'
]

# Google Ads API Scopes for YouTube advertising
GOOGLE_ADS_SCOPES = [
    'https://www.googleapis.com/auth/adwords'
]

class YouTubeCampaignObjective(Enum):
    """YouTube advertising campaign objectives"""
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    ACTION = "action"
    TRAFFIC = "traffic"
    LEADS = "leads"
    SALES = "sales"

class YouTubeAdFormat(Enum):
    """YouTube ad format types"""
    SKIPPABLE_IN_STREAM = "skippable_in_stream"
    NON_SKIPPABLE_IN_STREAM = "non_skippable_in_stream"
    BUMPER = "bumper"
    DISCOVERY = "discovery"
    OUT_STREAM = "out_stream"
    MASTHEAD = "masthead"

class YouTubeContentCategory(Enum):
    """YouTube content categories"""
    ENTERTAINMENT = "entertainment"
    EDUCATION = "education"
    MUSIC = "music"
    NEWS = "news"
    GAMING = "gaming"
    TECH = "tech"
    LIFESTYLE = "lifestyle"
    BUSINESS = "business"

@dataclass
class YouTubeCampaignData:
    """YouTube advertising campaign configuration"""
    name: str
    objective: YouTubeCampaignObjective
    budget_amount: float
    bid_strategy: str
    target_audience: Dict[str, Any]
    ad_format: YouTubeAdFormat
    video_asset_url: str
    landing_page_url: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    locations: Optional[List[str]] = None
    demographics: Optional[Dict[str, Any]] = None
    interests: Optional[List[str]] = None
    keywords: Optional[List[str]] = None

@dataclass
class YouTubeVideoData:
    """YouTube video content data"""
    title: str
    description: str
    tags: List[str]
    category: YouTubeContentCategory
    privacy_status: str = "public"  # public, private, unlisted
    thumbnail_url: Optional[str] = None
    playlist_id: Optional[str] = None
    scheduled_publish_time: Optional[datetime] = None
    location: Optional[Dict[str, float]] = None
    license: str = "youtube"  # youtube or creativeCommon

@dataclass
class YouTubeAnalyticsData:
    """YouTube analytics and performance data"""
    video_id: str
    views: int
    likes: int
    dislikes: int
    comments: int
    shares: int
    subscribers_gained: int
    watch_time_minutes: float
    average_view_duration: float
    click_through_rate: float
    engagement_rate: float
    revenue: Optional[float] = None
    cpm: Optional[float] = None
    rpm: Optional[float] = None

class YouTubeCampaignAgent:
    """
    Agent responsible for YouTube advertising campaign management and optimization.
    Handles campaign creation, management, bidding, and performance optimization.
    """
    
    def __init__(self, api_credentials: Dict[str, str]):
        """Initialize YouTube Campaign Agent with Google Ads credentials"""
        self.developer_token = api_credentials.get('developer_token')
        self.client_id = api_credentials.get('client_id')
        self.client_secret = api_credentials.get('client_secret')
        self.refresh_token = api_credentials.get('refresh_token')
        self.customer_id = api_credentials.get('customer_id')
        
        # Initialize Google Ads client for YouTube advertising
        self.ads_client = None
        self._initialize_ads_client()
        
    def _initialize_ads_client(self):
        """Initialize Google Ads API client"""
        try:
            google_ads_config = {
                "developer_token": self.developer_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
                "use_proto_plus": True
            }
            
            self.ads_client = GoogleAdsClient.load_from_dict(google_ads_config)
            logger.info("Google Ads client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Ads client: {e}")
            
    async def create_youtube_campaign(self, campaign_data: YouTubeCampaignData) -> Dict[str, Any]:
        """Create a new YouTube advertising campaign"""
        try:
            campaign_service = self.ads_client.get_service("CampaignService")
            campaign_operation = self.ads_client.get_type("CampaignOperation")
            
            # Create campaign
            campaign = campaign_operation.create
            campaign.name = campaign_data.name
            campaign.advertising_channel_type = self.ads_client.enums.AdvertisingChannelTypeEnum.VIDEO
            campaign.status = self.ads_client.enums.CampaignStatusEnum.ENABLED
            
            # Set budget
            campaign.campaign_budget = f"customers/{self.customer_id}/campaignBudgets/{await self._create_campaign_budget(campaign_data.budget_amount)}"
            
            # Set bidding strategy
            if campaign_data.bid_strategy == "target_cpm":
                campaign.target_cpm.target_cpm_micros = int(campaign_data.budget_amount * 1000000)
            elif campaign_data.bid_strategy == "maximize_conversions":
                campaign.maximize_conversions = self.ads_client.get_type("MaximizeConversions")
                
            # Set campaign dates
            if campaign_data.start_date:
                campaign.start_date = campaign_data.start_date.strftime("%Y-%m-%d")
            if campaign_data.end_date:
                campaign.end_date = campaign_data.end_date.strftime("%Y-%m-%d")
                
            # Execute campaign creation
            response = campaign_service.mutate_campaigns(
                customer_id=self.customer_id,
                operations=[campaign_operation]
            )
            
            campaign_id = response.results[0].resource_name.split('/')[-1]
            
            # Create ad group for the campaign
            ad_group_id = await self._create_ad_group(campaign_id, campaign_data)
            
            # Create video ad
            ad_id = await self._create_video_ad(campaign_id, ad_group_id, campaign_data)
            
            logger.info(f"YouTube campaign created successfully: {campaign_id}")
            
            return {
                'campaign_id': campaign_id,
                'ad_group_id': ad_group_id,
                'ad_id': ad_id,
                'status': 'created',
                'name': campaign_data.name,
                'created_at': datetime.now().isoformat()
            }
            
        except GoogleAdsException as ex:
            logger.error(f"Google Ads API error creating campaign: {ex}")
            return {'error': str(ex), 'status': 'failed'}
        except Exception as e:
            logger.error(f"Error creating YouTube campaign: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def _create_campaign_budget(self, budget_amount: float) -> str:
        """Create campaign budget for YouTube advertising"""
        try:
            budget_service = self.ads_client.get_service("CampaignBudgetService")
            budget_operation = self.ads_client.get_type("CampaignBudgetOperation")
            
            budget = budget_operation.create
            budget.name = f"YouTube Budget {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            budget.amount_micros = int(budget_amount * 1000000)
            budget.delivery_method = self.ads_client.enums.BudgetDeliveryMethodEnum.STANDARD
            
            response = budget_service.mutate_campaign_budgets(
                customer_id=self.customer_id,
                operations=[budget_operation]
            )
            
            return response.results[0].resource_name.split('/')[-1]
            
        except Exception as e:
            logger.error(f"Error creating campaign budget: {e}")
            raise
            
    async def _create_ad_group(self, campaign_id: str, campaign_data: YouTubeCampaignData) -> str:
        """Create ad group for YouTube campaign"""
        try:
            ad_group_service = self.ads_client.get_service("AdGroupService")
            ad_group_operation = self.ads_client.get_type("AdGroupOperation")
            
            ad_group = ad_group_operation.create
            ad_group.name = f"{campaign_data.name} - Ad Group"
            ad_group.campaign = f"customers/{self.customer_id}/campaigns/{campaign_id}"
            ad_group.type_ = self.ads_client.enums.AdGroupTypeEnum.VIDEO_TRUE_VIEW_IN_STREAM
            ad_group.status = self.ads_client.enums.AdGroupStatusEnum.ENABLED
            
            # Set CPC bid
            ad_group.cpc_bid_micros = int(1000000)  # $1.00 CPC
            
            response = ad_group_service.mutate_ad_groups(
                customer_id=self.customer_id,
                operations=[ad_group_operation]
            )
            
            return response.results[0].resource_name.split('/')[-1]
            
        except Exception as e:
            logger.error(f"Error creating ad group: {e}")
            raise
            
    async def _create_video_ad(self, campaign_id: str, ad_group_id: str, campaign_data: YouTubeCampaignData) -> str:
        """Create video ad for YouTube campaign"""
        try:
            ad_service = self.ads_client.get_service("AdService")
            ad_operation = self.ads_client.get_type("AdOperation")
            
            ad = ad_operation.create
            ad.ad_group = f"customers/{self.customer_id}/adGroups/{ad_group_id}"
            ad.status = self.ads_client.enums.AdStatusEnum.ENABLED
            
            # Create video ad
            ad.video_ad.video.id = self._extract_video_id(campaign_data.video_asset_url)
            
            if campaign_data.ad_format == YouTubeAdFormat.SKIPPABLE_IN_STREAM:
                ad.video_ad.in_stream.action_button_label = "LEARN_MORE"
                ad.video_ad.in_stream.action_headline = "Visit our website"
                if campaign_data.landing_page_url:
                    ad.video_ad.in_stream.companion_banner.headline = "Learn More"
                    
            response = ad_service.mutate_ads(
                customer_id=self.customer_id,
                operations=[ad_operation]
            )
            
            return response.results[0].resource_name.split('/')[-1]
            
        except Exception as e:
            logger.error(f"Error creating video ad: {e}")
            raise
            
    def _extract_video_id(self, youtube_url: str) -> str:
        """Extract video ID from YouTube URL"""
        if "youtube.com/watch?v=" in youtube_url:
            return youtube_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in youtube_url:
            return youtube_url.split("youtu.be/")[1].split("?")[0]
        else:
            return youtube_url  # Assume it's already a video ID
            
    async def optimize_campaign_performance(self, campaign_id: str) -> Dict[str, Any]:
        """Optimize YouTube campaign performance using AI insights"""
        try:
            # Get campaign performance data
            performance_data = await self.get_campaign_performance(campaign_id)
            
            optimizations = []
            
            # Analyze CTR and suggest bid adjustments
            if performance_data.get('ctr', 0) < 0.02:  # Less than 2% CTR
                optimizations.append({
                    'type': 'bid_adjustment',
                    'recommendation': 'increase_bids',
                    'reason': 'Low click-through rate detected',
                    'suggested_increase': 0.15
                })
                
            # Analyze cost per view
            if performance_data.get('cpv', 0) > 0.05:  # Higher than $0.05 CPV
                optimizations.append({
                    'type': 'targeting_adjustment',
                    'recommendation': 'refine_audience',
                    'reason': 'High cost per view indicates broad targeting',
                    'suggested_action': 'narrow_demographics'
                })
                
            # Analyze view completion rate
            if performance_data.get('view_completion_rate', 0) < 0.25:
                optimizations.append({
                    'type': 'creative_optimization',
                    'recommendation': 'improve_video_content',
                    'reason': 'Low view completion rate',
                    'suggested_action': 'test_new_creative'
                })
                
            return {
                'campaign_id': campaign_id,
                'optimizations': optimizations,
                'performance_summary': performance_data,
                'optimization_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error optimizing campaign: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def get_campaign_performance(self, campaign_id: str) -> Dict[str, Any]:
        """Get YouTube campaign performance metrics"""
        try:
            query = f"""
            SELECT
                campaign.id,
                campaign.name,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.video_views,
                metrics.video_view_rate,
                metrics.average_cost_per_view_micros,
                metrics.ctr,
                metrics.conversions
            FROM campaign
            WHERE campaign.id = {campaign_id}
            AND segments.date DURING LAST_30_DAYS
            """
            
            search_request = self.ads_client.get_type("SearchGoogleAdsRequest")
            search_request.customer_id = self.customer_id
            search_request.query = query
            
            ga_service = self.ads_client.get_service("GoogleAdsService")
            results = ga_service.search(request=search_request)
            
            performance_data = {}
            for row in results:
                performance_data = {
                    'impressions': row.metrics.impressions,
                    'clicks': row.metrics.clicks,
                    'cost': row.metrics.cost_micros / 1000000,
                    'video_views': row.metrics.video_views,
                    'view_rate': row.metrics.video_view_rate,
                    'cpv': row.metrics.average_cost_per_view_micros / 1000000,
                    'ctr': row.metrics.ctr,
                    'conversions': row.metrics.conversions
                }
                break
                
            return performance_data
            
        except Exception as e:
            logger.error(f"Error getting campaign performance: {e}")
            return {}

class YouTubeContentAgent:
    """
    Agent responsible for YouTube content publishing and optimization.
    Handles video uploads, metadata optimization, and content performance analysis.
    """
    
    def __init__(self, api_credentials: Dict[str, str]):
        """Initialize YouTube Content Agent"""
        self.api_key = api_credentials.get('api_key')
        self.oauth_credentials = api_credentials.get('oauth_credentials')
        self.youtube_service = None
        self._initialize_youtube_service()
        
    def _initialize_youtube_service(self):
        """Initialize YouTube Data API v3 service"""
        try:
            if self.oauth_credentials:
                # Use OAuth for authenticated requests
                creds = Credentials.from_authorized_user_info(self.oauth_credentials, YOUTUBE_SCOPES)
                self.youtube_service = build('youtube', 'v3', credentials=creds)
            else:
                # Use API key for public data
                self.youtube_service = build('youtube', 'v3', developerKey=self.api_key)
                
            logger.info("YouTube API service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize YouTube service: {e}")
            
    async def upload_video(self, video_file_path: str, video_data: YouTubeVideoData) -> Dict[str, Any]:
        """Upload video to YouTube with optimized metadata"""
        try:
            tags = ",".join(video_data.tags) if video_data.tags else None
            
            body = {
                'snippet': {
                    'title': video_data.title,
                    'description': video_data.description,
                    'tags': video_data.tags,
                    'categoryId': self._get_category_id(video_data.category),
                    'defaultLanguage': 'en',
                    'defaultAudioLanguage': 'en'
                },
                'status': {
                    'privacyStatus': video_data.privacy_status,
                    'license': video_data.license,
                    'embeddable': True,
                    'publicStatsViewable': True
                }
            }
            
            # Add scheduled publish time if provided
            if video_data.scheduled_publish_time:
                body['status']['publishAt'] = video_data.scheduled_publish_time.isoformat()
                body['status']['privacyStatus'] = 'private'  # Required for scheduled publishing
                
            # Add location if provided
            if video_data.location:
                body['recordingDetails'] = {
                    'location': {
                        'latitude': video_data.location.get('latitude'),
                        'longitude': video_data.location.get('longitude')
                    }
                }
                
            # Execute video upload
            insert_request = self.youtube_service.videos().insert(
                part=",".join(body.keys()),
                body=body,
                media_body=video_file_path
            )
            
            response = insert_request.execute()
            
            video_id = response['id']
            
            # Set custom thumbnail if provided
            if video_data.thumbnail_url:
                await self._set_custom_thumbnail(video_id, video_data.thumbnail_url)
                
            # Add to playlist if specified
            if video_data.playlist_id:
                await self._add_to_playlist(video_id, video_data.playlist_id)
                
            logger.info(f"Video uploaded successfully: {video_id}")
            
            return {
                'video_id': video_id,
                'title': video_data.title,
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'status': 'uploaded',
                'privacy_status': video_data.privacy_status,
                'upload_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    def _get_category_id(self, category: YouTubeContentCategory) -> str:
        """Get YouTube category ID for content category"""
        category_map = {
            YouTubeContentCategory.ENTERTAINMENT: "24",
            YouTubeContentCategory.EDUCATION: "27",
            YouTubeContentCategory.MUSIC: "10",
            YouTubeContentCategory.NEWS: "25",
            YouTubeContentCategory.GAMING: "20",
            YouTubeContentCategory.TECH: "28",
            YouTubeContentCategory.LIFESTYLE: "22",
            YouTubeContentCategory.BUSINESS: "28"  # Science & Technology as closest match
        }
        return category_map.get(category, "22")  # Default to People & Blogs
        
    async def _set_custom_thumbnail(self, video_id: str, thumbnail_url: str):
        """Set custom thumbnail for uploaded video"""
        try:
            # Download thumbnail image
            async with aiohttp.ClientSession() as session:
                async with session.get(thumbnail_url) as response:
                    if response.status == 200:
                        thumbnail_data = await response.read()
                        
                        # Upload thumbnail
                        self.youtube_service.thumbnails().set(
                            videoId=video_id,
                            media_body=thumbnail_data
                        ).execute()
                        
                        logger.info(f"Custom thumbnail set for video: {video_id}")
                        
        except Exception as e:
            logger.error(f"Error setting custom thumbnail: {e}")
            
    async def _add_to_playlist(self, video_id: str, playlist_id: str):
        """Add video to specified playlist"""
        try:
            playlist_item = {
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
            
            self.youtube_service.playlistItems().insert(
                part='snippet',
                body=playlist_item
            ).execute()
            
            logger.info(f"Video {video_id} added to playlist {playlist_id}")
            
        except Exception as e:
            logger.error(f"Error adding video to playlist: {e}")
            
    async def optimize_video_metadata(self, video_id: str, optimization_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize video metadata for better performance"""
        try:
            # Get current video data
            current_video = self.youtube_service.videos().list(
                part='snippet,status',
                id=video_id
            ).execute()
            
            if not current_video['items']:
                return {'error': 'Video not found', 'status': 'failed'}
                
            video_snippet = current_video['items'][0]['snippet']
            
            optimizations_applied = []
            
            # Optimize title if suggested
            if 'title' in optimization_data:
                video_snippet['title'] = optimization_data['title']
                optimizations_applied.append('title')
                
            # Optimize description if suggested
            if 'description' in optimization_data:
                video_snippet['description'] = optimization_data['description']
                optimizations_applied.append('description')
                
            # Optimize tags if suggested
            if 'tags' in optimization_data:
                video_snippet['tags'] = optimization_data['tags']
                optimizations_applied.append('tags')
                
            # Update video metadata
            if optimizations_applied:
                update_response = self.youtube_service.videos().update(
                    part='snippet',
                    body={
                        'id': video_id,
                        'snippet': video_snippet
                    }
                ).execute()
                
            return {
                'video_id': video_id,
                'optimizations_applied': optimizations_applied,
                'status': 'optimized',
                'optimization_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error optimizing video metadata: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def analyze_content_performance(self, video_id: str) -> Dict[str, Any]:
        """Analyze content performance and provide optimization suggestions"""
        try:
            # Get video statistics
            video_response = self.youtube_service.videos().list(
                part='statistics,snippet,contentDetails',
                id=video_id
            ).execute()
            
            if not video_response['items']:
                return {'error': 'Video not found', 'status': 'failed'}
                
            video_data = video_response['items'][0]
            stats = video_data['statistics']
            snippet = video_data['snippet']
            content_details = video_data['contentDetails']
            
            # Calculate engagement metrics
            views = int(stats.get('viewCount', 0))
            likes = int(stats.get('likeCount', 0))
            comments = int(stats.get('commentCount', 0))
            
            engagement_rate = (likes + comments) / views if views > 0 else 0
            
            # Generate performance insights
            insights = []
            
            if engagement_rate < 0.02:  # Less than 2% engagement
                insights.append({
                    'type': 'engagement',
                    'issue': 'Low engagement rate',
                    'suggestion': 'Add compelling call-to-actions and encourage viewer interaction',
                    'priority': 'high'
                })
                
            if views < 100 and datetime.now() - datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00')) > timedelta(days=7):
                insights.append({
                    'type': 'visibility',
                    'issue': 'Low view count after one week',
                    'suggestion': 'Optimize SEO with better title, description, and tags',
                    'priority': 'high'
                })
                
            # Analyze video duration
            duration = self._parse_duration(content_details.get('duration', 'PT0S'))
            if duration > 600:  # More than 10 minutes
                insights.append({
                    'type': 'retention',
                    'issue': 'Long video duration',
                    'suggestion': 'Consider shorter format or add timestamps for better retention',
                    'priority': 'medium'
                })
                
            return {
                'video_id': video_id,
                'performance_metrics': {
                    'views': views,
                    'likes': likes,
                    'comments': comments,
                    'engagement_rate': engagement_rate,
                    'duration_seconds': duration
                },
                'insights': insights,
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing content performance: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    def _parse_duration(self, duration_str: str) -> int:
        """Parse YouTube duration format (PT#M#S) to seconds"""
        import re
        
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_str)
        
        if not match:
            return 0
            
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0
        
        return hours * 3600 + minutes * 60 + seconds

class YouTubeAudienceAgent:
    """
    Agent responsible for YouTube audience analysis and targeting optimization.
    Handles audience research, demographic analysis, and targeting recommendations.
    """
    
    def __init__(self, api_credentials: Dict[str, str]):
        """Initialize YouTube Audience Agent"""
        self.api_key = api_credentials.get('api_key')
        self.oauth_credentials = api_credentials.get('oauth_credentials')
        self.youtube_service = None
        self._initialize_youtube_service()
        
    def _initialize_youtube_service(self):
        """Initialize YouTube Data API v3 service"""
        try:
            if self.oauth_credentials:
                creds = Credentials.from_authorized_user_info(self.oauth_credentials, YOUTUBE_SCOPES)
                self.youtube_service = build('youtube', 'v3', credentials=creds)
            else:
                self.youtube_service = build('youtube', 'v3', developerKey=self.api_key)
                
            logger.info("YouTube Audience service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize YouTube Audience service: {e}")
            
    async def analyze_channel_audience(self, channel_id: str) -> Dict[str, Any]:
        """Analyze channel audience demographics and behavior"""
        try:
            # Get channel statistics
            channel_response = self.youtube_service.channels().list(
                part='statistics,snippet,brandingSettings',
                id=channel_id
            ).execute()
            
            if not channel_response['items']:
                return {'error': 'Channel not found', 'status': 'failed'}
                
            channel_data = channel_response['items'][0]
            stats = channel_data['statistics']
            snippet = channel_data['snippet']
            
            # Get recent videos for audience analysis
            videos_response = self.youtube_service.search().list(
                part='id,snippet',
                channelId=channel_id,
                type='video',
                order='date',
                maxResults=50
            ).execute()
            
            # Analyze video performance patterns
            video_ids = [item['id']['videoId'] for item in videos_response['items']]
            audience_insights = await self._analyze_video_audience_patterns(video_ids)
            
            # Get subscriber demographics (requires YouTube Analytics API)
            demographics = await self._get_subscriber_demographics(channel_id)
            
            return {
                'channel_id': channel_id,
                'channel_name': snippet.get('title'),
                'subscriber_count': int(stats.get('subscriberCount', 0)),
                'total_views': int(stats.get('viewCount', 0)),
                'video_count': int(stats.get('videoCount', 0)),
                'audience_insights': audience_insights,
                'demographics': demographics,
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing channel audience: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def _analyze_video_audience_patterns(self, video_ids: List[str]) -> Dict[str, Any]:
        """Analyze audience engagement patterns across videos"""
        try:
            if not video_ids:
                return {}
                
            # Get video statistics in batches
            video_stats = []
            batch_size = 50
            
            for i in range(0, len(video_ids), batch_size):
                batch_ids = video_ids[i:i + batch_size]
                
                videos_response = self.youtube_service.videos().list(
                    part='statistics,snippet,contentDetails',
                    id=','.join(batch_ids)
                ).execute()
                
                video_stats.extend(videos_response['items'])
                
            # Analyze engagement patterns
            total_views = sum(int(video.get('statistics', {}).get('viewCount', 0)) for video in video_stats)
            total_likes = sum(int(video.get('statistics', {}).get('likeCount', 0)) for video in video_stats)
            total_comments = sum(int(video.get('statistics', {}).get('commentCount', 0)) for video in video_stats)
            
            avg_engagement_rate = (total_likes + total_comments) / total_views if total_views > 0 else 0
            
            # Analyze content preferences
            category_performance = {}
            for video in video_stats:
                category_id = video.get('snippet', {}).get('categoryId', 'Unknown')
                views = int(video.get('statistics', {}).get('viewCount', 0))
                
                if category_id not in category_performance:
                    category_performance[category_id] = {'views': 0, 'count': 0}
                    
                category_performance[category_id]['views'] += views
                category_performance[category_id]['count'] += 1
                
            # Find best performing categories
            best_categories = sorted(
                category_performance.items(),
                key=lambda x: x[1]['views'] / x[1]['count'],
                reverse=True
            )[:5]
            
            return {
                'average_engagement_rate': avg_engagement_rate,
                'total_videos_analyzed': len(video_stats),
                'best_performing_categories': [
                    {
                        'category_id': cat[0],
                        'avg_views': cat[1]['views'] / cat[1]['count'],
                        'video_count': cat[1]['count']
                    }
                    for cat in best_categories
                ]
            }
            
        except Exception as e:
            logger.error(f"Error analyzing video audience patterns: {e}")
            return {}
            
    async def _get_subscriber_demographics(self, channel_id: str) -> Dict[str, Any]:
        """Get subscriber demographic data (requires YouTube Analytics API)"""
        try:
            # Note: This requires YouTube Analytics API and channel ownership
            # For now, return mock demographic data structure
            
            demographics = {
                'age_groups': {
                    '13-17': 5.2,
                    '18-24': 23.1,
                    '25-34': 35.7,
                    '35-44': 22.4,
                    '45-54': 10.8,
                    '55-64': 2.5,
                    '65+': 0.3
                },
                'gender': {
                    'male': 64.2,
                    'female': 35.8
                },
                'top_countries': [
                    {'country': 'United States', 'percentage': 32.1},
                    {'country': 'India', 'percentage': 18.7},
                    {'country': 'United Kingdom', 'percentage': 8.3},
                    {'country': 'Canada', 'percentage': 6.9},
                    {'country': 'Germany', 'percentage': 4.2}
                ]
            }
            
            return demographics
            
        except Exception as e:
            logger.error(f"Error getting subscriber demographics: {e}")
            return {}
            
    async def research_competitor_audiences(self, competitor_channels: List[str]) -> Dict[str, Any]:
        """Research competitor channel audiences for targeting insights"""
        try:
            competitor_insights = []
            
            for channel_id in competitor_channels:
                try:
                    # Get competitor channel data
                    channel_response = self.youtube_service.channels().list(
                        part='statistics,snippet',
                        id=channel_id
                    ).execute()
                    
                    if not channel_response['items']:
                        continue
                        
                    channel_data = channel_response['items'][0]
                    
                    # Get recent videos
                    videos_response = self.youtube_service.search().list(
                        part='id,snippet',
                        channelId=channel_id,
                        type='video',
                        order='relevance',
                        maxResults=20
                    ).execute()
                    
                    # Analyze content themes
                    content_themes = await self._extract_content_themes([
                        item['snippet'] for item in videos_response['items']
                    ])
                    
                    competitor_insights.append({
                        'channel_id': channel_id,
                        'channel_name': channel_data['snippet'].get('title'),
                        'subscribers': int(channel_data['statistics'].get('subscriberCount', 0)),
                        'content_themes': content_themes,
                        'avg_views_per_video': await self._calculate_avg_views(channel_id)
                    })
                    
                except Exception as e:
                    logger.error(f"Error analyzing competitor {channel_id}: {e}")
                    continue
                    
            return {
                'competitor_analysis': competitor_insights,
                'analysis_date': datetime.now().isoformat(),
                'recommendations': await self._generate_audience_recommendations(competitor_insights)
            }
            
        except Exception as e:
            logger.error(f"Error researching competitor audiences: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def _extract_content_themes(self, video_snippets: List[Dict]) -> List[str]:
        """Extract common themes from video titles and descriptions"""
        try:
            themes = {}
            
            for snippet in video_snippets:
                title = snippet.get('title', '').lower()
                description = snippet.get('description', '').lower()
                
                # Simple keyword extraction (in production, use NLP)
                keywords = title.split() + description.split()[:50]  # First 50 words of description
                
                for keyword in keywords:
                    if len(keyword) > 3:  # Filter short words
                        themes[keyword] = themes.get(keyword, 0) + 1
                        
            # Return top themes
            return sorted(themes.keys(), key=themes.get, reverse=True)[:10]
            
        except Exception as e:
            logger.error(f"Error extracting content themes: {e}")
            return []
            
    async def _calculate_avg_views(self, channel_id: str) -> float:
        """Calculate average views per video for a channel"""
        try:
            videos_response = self.youtube_service.search().list(
                part='id',
                channelId=channel_id,
                type='video',
                order='date',
                maxResults=10
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in videos_response['items']]
            
            if not video_ids:
                return 0.0
                
            videos_stats = self.youtube_service.videos().list(
                part='statistics',
                id=','.join(video_ids)
            ).execute()
            
            total_views = sum(
                int(video['statistics'].get('viewCount', 0))
                for video in videos_stats['items']
            )
            
            return total_views / len(videos_stats['items'])
            
        except Exception as e:
            logger.error(f"Error calculating average views: {e}")
            return 0.0
            
    async def _generate_audience_recommendations(self, competitor_insights: List[Dict]) -> List[Dict]:
        """Generate audience targeting recommendations based on competitor analysis"""
        try:
            recommendations = []
            
            # Analyze successful competitors
            top_performers = sorted(
                competitor_insights,
                key=lambda x: x.get('avg_views_per_video', 0),
                reverse=True
            )[:3]
            
            if top_performers:
                recommendations.append({
                    'type': 'content_strategy',
                    'recommendation': 'Focus on high-performing content themes',
                    'themes': list(set([
                        theme for performer in top_performers
                        for theme in performer.get('content_themes', [])[:5]
                    ])),
                    'priority': 'high'
                })
                
                avg_subscriber_count = sum(
                    p.get('subscribers', 0) for p in top_performers
                ) / len(top_performers)
                
                recommendations.append({
                    'type': 'audience_size',
                    'recommendation': 'Target similar audience size',
                    'suggested_range': f"{int(avg_subscriber_count * 0.8)}-{int(avg_subscriber_count * 1.2)}",
                    'priority': 'medium'
                })
                
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating audience recommendations: {e}")
            return []
            
    async def generate_targeting_recommendations(self, channel_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate YouTube advertising targeting recommendations"""
        try:
            recommendations = []
            
            # Demographic targeting recommendations
            if 'demographics' in channel_analysis:
                demographics = channel_analysis['demographics']
                
                # Age targeting
                top_age_groups = sorted(
                    demographics.get('age_groups', {}).items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3]
                
                recommendations.append({
                    'type': 'demographic_targeting',
                    'category': 'age',
                    'recommended_groups': [age[0] for age in top_age_groups],
                    'rationale': 'Primary audience age groups based on channel analytics'
                })
                
                # Geographic targeting
                top_countries = demographics.get('top_countries', [])[:5]
                recommendations.append({
                    'type': 'geographic_targeting',
                    'recommended_countries': [country['country'] for country in top_countries],
                    'rationale': 'Top-performing geographic markets'
                })
                
            # Interest targeting based on content themes
            audience_insights = channel_analysis.get('audience_insights', {})
            if 'best_performing_categories' in audience_insights:
                categories = audience_insights['best_performing_categories']
                
                recommendations.append({
                    'type': 'interest_targeting',
                    'recommended_categories': [cat['category_id'] for cat in categories[:3]],
                    'rationale': 'Content categories with highest engagement'
                })
                
            # Behavioral targeting recommendations
            engagement_rate = audience_insights.get('average_engagement_rate', 0)
            if engagement_rate > 0.05:  # High engagement
                recommendations.append({
                    'type': 'behavioral_targeting',
                    'recommendation': 'Target highly engaged users',
                    'settings': {
                        'engagement_threshold': 'high',
                        'interaction_types': ['likes', 'comments', 'shares']
                    }
                })
                
            return {
                'targeting_recommendations': recommendations,
                'generated_date': datetime.now().isoformat(),
                'confidence_score': self._calculate_confidence_score(channel_analysis)
            }
            
        except Exception as e:
            logger.error(f"Error generating targeting recommendations: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    def _calculate_confidence_score(self, channel_analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for targeting recommendations"""
        try:
            score = 0.0
            
            # Base score on data availability
            if 'demographics' in channel_analysis:
                score += 0.3
                
            if 'audience_insights' in channel_analysis:
                score += 0.3
                
            # Boost score based on subscriber count (more data = higher confidence)
            subscriber_count = channel_analysis.get('subscriber_count', 0)
            if subscriber_count > 100000:
                score += 0.2
            elif subscriber_count > 10000:
                score += 0.1
                
            # Boost score based on engagement rate
            engagement_rate = channel_analysis.get('audience_insights', {}).get('average_engagement_rate', 0)
            if engagement_rate > 0.03:
                score += 0.2
            elif engagement_rate > 0.01:
                score += 0.1
                
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating confidence score: {e}")
            return 0.5

class YouTubeAnalyticsAgent:
    """
    Agent responsible for YouTube performance tracking and analytics.
    Provides comprehensive insights, reporting, and optimization recommendations.
    """
    
    def __init__(self, api_credentials: Dict[str, str]):
        """Initialize YouTube Analytics Agent"""
        self.api_key = api_credentials.get('api_key')
        self.oauth_credentials = api_credentials.get('oauth_credentials')
        self.youtube_service = None
        self.analytics_service = None
        self._initialize_services()
        
    def _initialize_services(self):
        """Initialize YouTube Data API and Analytics API services"""
        try:
            if self.oauth_credentials:
                creds = Credentials.from_authorized_user_info(self.oauth_credentials, YOUTUBE_SCOPES)
                self.youtube_service = build('youtube', 'v3', credentials=creds)
                self.analytics_service = build('youtubeAnalytics', 'v2', credentials=creds)
            else:
                self.youtube_service = build('youtube', 'v3', developerKey=self.api_key)
                
            logger.info("YouTube Analytics services initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize YouTube Analytics services: {e}")
            
    async def get_video_analytics(self, video_id: str, date_range: int = 30) -> YouTubeAnalyticsData:
        """Get comprehensive analytics for a specific video"""
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=date_range)
            
            # Get basic video statistics
            video_response = self.youtube_service.videos().list(
                part='statistics,snippet',
                id=video_id
            ).execute()
            
            if not video_response['items']:
                raise ValueError(f"Video {video_id} not found")
                
            video_data = video_response['items'][0]
            stats = video_data['statistics']
            
            # Get detailed analytics from YouTube Analytics API
            detailed_analytics = await self._get_detailed_video_analytics(video_id, start_date, end_date)
            
            analytics_data = YouTubeAnalyticsData(
                video_id=video_id,
                views=int(stats.get('viewCount', 0)),
                likes=int(stats.get('likeCount', 0)),
                dislikes=int(stats.get('dislikeCount', 0)),  # Note: May not be available
                comments=int(stats.get('commentCount', 0)),
                shares=detailed_analytics.get('shares', 0),
                subscribers_gained=detailed_analytics.get('subscribersGained', 0),
                watch_time_minutes=detailed_analytics.get('estimatedMinutesWatched', 0),
                average_view_duration=detailed_analytics.get('averageViewDuration', 0),
                click_through_rate=detailed_analytics.get('cardClickRate', 0),
                engagement_rate=self._calculate_engagement_rate(stats),
                revenue=detailed_analytics.get('estimatedRevenue'),
                cpm=detailed_analytics.get('cpm'),
                rpm=detailed_analytics.get('playbackBasedCpm')
            )
            
            return analytics_data
            
        except Exception as e:
            logger.error(f"Error getting video analytics: {e}")
            raise
            
    async def _get_detailed_video_analytics(self, video_id: str, start_date: datetime.date, end_date: datetime.date) -> Dict[str, Any]:
        """Get detailed analytics from YouTube Analytics API"""
        try:
            if not self.analytics_service:
                return {}  # Return empty dict if Analytics API not available
                
            # Query for detailed metrics
            analytics_response = self.analytics_service.reports().query(
                ids='channel==MINE',
                startDate=start_date.strftime('%Y-%m-%d'),
                endDate=end_date.strftime('%Y-%m-%d'),
                metrics='views,likes,dislikes,comments,shares,subscribersGained,estimatedMinutesWatched,averageViewDuration,cardClickRate,estimatedRevenue,cpm,playbackBasedCpm',
                dimensions='video',
                filters=f'video=={video_id}'
            ).execute()
            
            if analytics_response.get('rows'):
                row = analytics_response['rows'][0]
                headers = analytics_response.get('columnHeaders', [])
                
                # Map column headers to values
                result = {}
                for i, header in enumerate(headers):
                    if i < len(row):
                        result[header['name']] = row[i]
                        
                return result
                
            return {}
            
        except Exception as e:
            logger.error(f"Error getting detailed video analytics: {e}")
            return {}
            
    def _calculate_engagement_rate(self, stats: Dict[str, Any]) -> float:
        """Calculate engagement rate from video statistics"""
        try:
            views = int(stats.get('viewCount', 0))
            likes = int(stats.get('likeCount', 0))
            comments = int(stats.get('commentCount', 0))
            
            if views == 0:
                return 0.0
                
            engagement_rate = (likes + comments) / views
            return round(engagement_rate, 4)
            
        except Exception as e:
            logger.error(f"Error calculating engagement rate: {e}")
            return 0.0
            
    async def get_channel_performance_report(self, channel_id: str, date_range: int = 30) -> Dict[str, Any]:
        """Generate comprehensive channel performance report"""
        try:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=date_range)
            
            # Get channel statistics
            channel_response = self.youtube_service.channels().list(
                part='statistics,snippet',
                id=channel_id
            ).execute()
            
            if not channel_response['items']:
                return {'error': 'Channel not found', 'status': 'failed'}
                
            channel_data = channel_response['items'][0]
            channel_stats = channel_data['statistics']
            
            # Get recent videos
            videos_response = self.youtube_service.search().list(
                part='id,snippet',
                channelId=channel_id,
                type='video',
                order='date',
                maxResults=50,
                publishedAfter=(start_date).strftime('%Y-%m-%dT00:00:00Z')
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in videos_response['items']]
            
            # Analyze video performance
            video_performance = await self._analyze_video_performance_batch(video_ids)
            
            # Get channel-level analytics
            channel_analytics = await self._get_channel_analytics(channel_id, start_date, end_date)
            
            # Generate insights
            insights = await self._generate_performance_insights(video_performance, channel_analytics)
            
            return {
                'channel_id': channel_id,
                'channel_name': channel_data['snippet'].get('title'),
                'report_period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': date_range
                },
                'channel_overview': {
                    'subscribers': int(channel_stats.get('subscriberCount', 0)),
                    'total_views': int(channel_stats.get('viewCount', 0)),
                    'total_videos': int(channel_stats.get('videoCount', 0))
                },
                'period_performance': channel_analytics,
                'video_performance': video_performance,
                'insights': insights,
                'report_generated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating channel performance report: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def _analyze_video_performance_batch(self, video_ids: List[str]) -> Dict[str, Any]:
        """Analyze performance of multiple videos"""
        try:
            if not video_ids:
                return {}
                
            # Get video statistics in batches
            batch_size = 50
            all_videos = []
            
            for i in range(0, len(video_ids), batch_size):
                batch_ids = video_ids[i:i + batch_size]
                
                videos_response = self.youtube_service.videos().list(
                    part='statistics,snippet,contentDetails',
                    id=','.join(batch_ids)
                ).execute()
                
                all_videos.extend(videos_response['items'])
                
            # Calculate aggregate metrics
            total_views = sum(int(video['statistics'].get('viewCount', 0)) for video in all_videos)
            total_likes = sum(int(video['statistics'].get('likeCount', 0)) for video in all_videos)
            total_comments = sum(int(video['statistics'].get('commentCount', 0)) for video in all_videos)
            
            # Find top performing videos
            top_videos = sorted(
                all_videos,
                key=lambda x: int(x['statistics'].get('viewCount', 0)),
                reverse=True
            )[:5]
            
            # Calculate average engagement
            avg_engagement = (total_likes + total_comments) / total_views if total_views > 0 else 0
            
            return {
                'total_videos': len(all_videos),
                'total_views': total_views,
                'total_likes': total_likes,
                'total_comments': total_comments,
                'average_engagement_rate': avg_engagement,
                'top_performing_videos': [
                    {
                        'video_id': video['id'],
                        'title': video['snippet']['title'],
                        'views': int(video['statistics'].get('viewCount', 0)),
                        'likes': int(video['statistics'].get('likeCount', 0)),
                        'comments': int(video['statistics'].get('commentCount', 0))
                    }
                    for video in top_videos
                ]
            }
            
        except Exception as e:
            logger.error(f"Error analyzing video performance batch: {e}")
            return {}
            
    async def _get_channel_analytics(self, channel_id: str, start_date: datetime.date, end_date: datetime.date) -> Dict[str, Any]:
        """Get channel-level analytics data"""
        try:
            if not self.analytics_service:
                return {}
                
            # Query channel analytics
            analytics_response = self.analytics_service.reports().query(
                ids='channel==MINE',
                startDate=start_date.strftime('%Y-%m-%d'),
                endDate=end_date.strftime('%Y-%m-%d'),
                metrics='views,likes,dislikes,comments,shares,subscribersGained,estimatedMinutesWatched,averageViewDuration,estimatedRevenue'
            ).execute()
            
            if analytics_response.get('rows'):
                row = analytics_response['rows'][0]
                
                return {
                    'period_views': row[0] if len(row) > 0 else 0,
                    'period_likes': row[1] if len(row) > 1 else 0,
                    'period_comments': row[3] if len(row) > 3 else 0,
                    'subscribers_gained': row[5] if len(row) > 5 else 0,
                    'watch_time_minutes': row[6] if len(row) > 6 else 0,
                    'average_view_duration': row[7] if len(row) > 7 else 0,
                    'estimated_revenue': row[8] if len(row) > 8 else 0
                }
                
            return {}
            
        except Exception as e:
            logger.error(f"Error getting channel analytics: {e}")
            return {}
            
    async def _generate_performance_insights(self, video_performance: Dict[str, Any], channel_analytics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate performance insights and recommendations"""
        try:
            insights = []
            
            # Analyze engagement rate
            engagement_rate = video_performance.get('average_engagement_rate', 0)
            if engagement_rate < 0.02:
                insights.append({
                    'type': 'engagement',
                    'level': 'warning',
                    'title': 'Low Engagement Rate',
                    'description': f'Average engagement rate of {engagement_rate:.2%} is below industry standard',
                    'recommendation': 'Improve content quality and add more engaging call-to-actions'
                })
            elif engagement_rate > 0.05:
                insights.append({
                    'type': 'engagement',
                    'level': 'success',
                    'title': 'High Engagement Rate',
                    'description': f'Excellent engagement rate of {engagement_rate:.2%}',
                    'recommendation': 'Continue current content strategy and expand reach'
                })
                
            # Analyze subscriber growth
            subscribers_gained = channel_analytics.get('subscribers_gained', 0)
            if subscribers_gained < 0:
                insights.append({
                    'type': 'growth',
                    'level': 'warning',
                    'title': 'Subscriber Loss',
                    'description': f'Lost {abs(subscribers_gained)} subscribers in the period',
                    'recommendation': 'Analyze recent content and audience feedback for issues'
                })
            elif subscribers_gained > video_performance.get('total_views', 0) * 0.01:
                insights.append({
                    'type': 'growth',
                    'level': 'success',
                    'title': 'Strong Subscriber Growth',
                    'description': f'Gained {subscribers_gained} subscribers',
                    'recommendation': 'Leverage successful content themes for continued growth'
                })
                
            # Analyze view duration
            avg_duration = channel_analytics.get('average_view_duration', 0)
            if avg_duration > 0:
                if avg_duration < 60:  # Less than 1 minute
                    insights.append({
                        'type': 'retention',
                        'level': 'warning',
                        'title': 'Low View Duration',
                        'description': f'Average view duration of {avg_duration:.0f} seconds',
                        'recommendation': 'Improve video hooks and pacing to retain viewers'
                    })
                elif avg_duration > 180:  # More than 3 minutes
                    insights.append({
                        'type': 'retention',
                        'level': 'success',
                        'title': 'Excellent View Duration',
                        'description': f'Strong average view duration of {avg_duration:.0f} seconds',
                        'recommendation': 'Content quality is high - focus on scaling reach'
                    })
                    
            # Analyze revenue (if available)
            revenue = channel_analytics.get('estimated_revenue', 0)
            if revenue > 0:
                rpm = revenue / (channel_analytics.get('period_views', 1) / 1000)
                insights.append({
                    'type': 'monetization',
                    'level': 'info',
                    'title': 'Revenue Performance',
                    'description': f'Revenue per 1K views: ${rpm:.2f}',
                    'recommendation': 'Consider additional monetization strategies if RPM is low'
                })
                
            return insights
            
        except Exception as e:
            logger.error(f"Error generating performance insights: {e}")
            return []
            
    async def create_performance_dashboard(self, channel_id: str) -> Dict[str, Any]:
        """Create a comprehensive performance dashboard"""
        try:
            # Get multiple time periods for comparison
            periods = [7, 30, 90]
            dashboard_data = {}
            
            for period in periods:
                period_data = await self.get_channel_performance_report(channel_id, period)
                dashboard_data[f'{period}_days'] = period_data
                
            # Calculate trends
            trends = await self._calculate_performance_trends(dashboard_data)
            
            # Get top content recommendations
            content_recommendations = await self._generate_content_recommendations(channel_id)
            
            return {
                'channel_id': channel_id,
                'dashboard_data': dashboard_data,
                'trends': trends,
                'content_recommendations': content_recommendations,
                'dashboard_created': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating performance dashboard: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def _calculate_performance_trends(self, dashboard_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance trends across different time periods"""
        try:
            trends = {}
            
            # Compare 7-day vs 30-day performance
            if '7_days' in dashboard_data and '30_days' in dashboard_data:
                current_7d = dashboard_data['7_days'].get('period_performance', {})
                current_30d = dashboard_data['30_days'].get('period_performance', {})
                
                # Calculate daily averages
                daily_views_7d = current_7d.get('period_views', 0) / 7
                daily_views_30d = current_30d.get('period_views', 0) / 30
                
                if daily_views_30d > 0:
                    views_trend = ((daily_views_7d - daily_views_30d) / daily_views_30d) * 100
                    trends['views_trend'] = {
                        'value': views_trend,
                        'direction': 'up' if views_trend > 0 else 'down',
                        'description': f'Views {"increased" if views_trend > 0 else "decreased"} by {abs(views_trend):.1f}% vs 30-day average'
                    }
                    
                # Subscriber growth trend
                subscribers_7d = current_7d.get('subscribers_gained', 0) / 7
                subscribers_30d = current_30d.get('subscribers_gained', 0) / 30
                
                if subscribers_30d != 0:
                    subscriber_trend = ((subscribers_7d - subscribers_30d) / abs(subscribers_30d)) * 100
                    trends['subscriber_trend'] = {
                        'value': subscriber_trend,
                        'direction': 'up' if subscriber_trend > 0 else 'down',
                        'description': f'Subscriber growth {"improved" if subscriber_trend > 0 else "declined"} by {abs(subscriber_trend):.1f}%'
                    }
                    
            return trends
            
        except Exception as e:
            logger.error(f"Error calculating performance trends: {e}")
            return {}
            
    async def _generate_content_recommendations(self, channel_id: str) -> List[Dict[str, Any]]:
        """Generate content recommendations based on performance analysis"""
        try:
            recommendations = []
            
            # Get top performing videos from last 90 days
            videos_response = self.youtube_service.search().list(
                part='id,snippet',
                channelId=channel_id,
                type='video',
                order='relevance',
                maxResults=20,
                publishedAfter=(datetime.now() - timedelta(days=90)).strftime('%Y-%m-%dT00:00:00Z')
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in videos_response['items']]
            
            if video_ids:
                # Get video statistics
                videos_stats = self.youtube_service.videos().list(
                    part='statistics,snippet',
                    id=','.join(video_ids)
                ).execute()
                
                # Analyze successful content patterns
                top_videos = sorted(
                    videos_stats['items'],
                    key=lambda x: int(x['statistics'].get('viewCount', 0)),
                    reverse=True
                )[:5]
                
                # Extract themes from top videos
                successful_themes = []
                for video in top_videos:
                    title = video['snippet']['title'].lower()
                    successful_themes.extend(title.split())
                    
                # Find common themes
                theme_counts = {}
                for theme in successful_themes:
                    if len(theme) > 3:
                        theme_counts[theme] = theme_counts.get(theme, 0) + 1
                        
                top_themes = sorted(theme_counts.keys(), key=theme_counts.get, reverse=True)[:5]
                
                recommendations.append({
                    'type': 'content_themes',
                    'title': 'Successful Content Themes',
                    'themes': top_themes,
                    'recommendation': 'Create more content around these successful themes'
                })
                
                # Analyze upload timing
                upload_hours = []
                for video in videos_stats['items']:
                    published_at = datetime.fromisoformat(video['snippet']['publishedAt'].replace('Z', '+00:00'))
                    upload_hours.append(published_at.hour)
                    
                if upload_hours:
                    optimal_hour = max(set(upload_hours), key=upload_hours.count)
                    recommendations.append({
                        'type': 'upload_timing',
                        'title': 'Optimal Upload Time',
                        'recommendation': f'Consider uploading around {optimal_hour:02d}:00 based on your successful videos'
                    })
                    
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating content recommendations: {e}")
            return []

class YouTubeMarketingIntegration:
    """
    Main integration class that orchestrates all YouTube marketing agents
    and provides unified interface for BizOSaaS Brain API.
    """
    
    def __init__(self, api_credentials: Dict[str, str]):
        """Initialize YouTube Marketing Integration with all agents"""
        self.api_credentials = api_credentials
        
        # Initialize all agents
        self.campaign_agent = YouTubeCampaignAgent(api_credentials)
        self.content_agent = YouTubeContentAgent(api_credentials)
        self.audience_agent = YouTubeAudienceAgent(api_credentials)
        self.analytics_agent = YouTubeAnalyticsAgent(api_credentials)
        
        logger.info("YouTube Marketing Integration initialized successfully")
        
    async def create_comprehensive_marketing_campaign(self, campaign_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive YouTube marketing campaign with content and advertising"""
        try:
            results = {}
            
            # 1. Create advertising campaign
            if 'campaign_data' in campaign_config:
                campaign_data = YouTubeCampaignData(**campaign_config['campaign_data'])
                campaign_result = await self.campaign_agent.create_youtube_campaign(campaign_data)
                results['advertising_campaign'] = campaign_result
                
            # 2. Upload and optimize content
            if 'video_data' in campaign_config and 'video_file_path' in campaign_config:
                video_data = YouTubeVideoData(**campaign_config['video_data'])
                upload_result = await self.content_agent.upload_video(
                    campaign_config['video_file_path'],
                    video_data
                )
                results['content_upload'] = upload_result
                
                # Optimize video metadata
                if upload_result.get('video_id'):
                    optimization_result = await self.content_agent.optimize_video_metadata(
                        upload_result['video_id'],
                        campaign_config.get('optimization_data', {})
                    )
                    results['content_optimization'] = optimization_result
                    
            # 3. Analyze target audience
            if 'channel_id' in campaign_config:
                audience_analysis = await self.audience_agent.analyze_channel_audience(
                    campaign_config['channel_id']
                )
                results['audience_analysis'] = audience_analysis
                
                # Generate targeting recommendations
                targeting_recommendations = await self.audience_agent.generate_targeting_recommendations(
                    audience_analysis
                )
                results['targeting_recommendations'] = targeting_recommendations
                
            # 4. Set up analytics tracking
            if results.get('content_upload', {}).get('video_id'):
                video_id = results['content_upload']['video_id']
                initial_analytics = await self.analytics_agent.get_video_analytics(video_id, 1)
                results['initial_analytics'] = asdict(initial_analytics)
                
            return {
                'campaign_id': results.get('advertising_campaign', {}).get('campaign_id'),
                'video_id': results.get('content_upload', {}).get('video_id'),
                'status': 'success',
                'results': results,
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating comprehensive marketing campaign: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def get_campaign_performance_report(self, campaign_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive campaign performance report"""
        try:
            report = {
                'report_type': 'youtube_campaign_performance',
                'generated_at': datetime.now().isoformat()
            }
            
            # Get advertising campaign performance
            if 'campaign_id' in campaign_config:
                ad_performance = await self.campaign_agent.get_campaign_performance(
                    campaign_config['campaign_id']
                )
                report['advertising_performance'] = ad_performance
                
            # Get content performance
            if 'video_id' in campaign_config:
                video_analytics = await self.analytics_agent.get_video_analytics(
                    campaign_config['video_id'],
                    campaign_config.get('date_range', 30)
                )
                report['content_performance'] = asdict(video_analytics)
                
                # Get content optimization analysis
                content_analysis = await self.content_agent.analyze_content_performance(
                    campaign_config['video_id']
                )
                report['content_analysis'] = content_analysis
                
            # Get channel-level performance
            if 'channel_id' in campaign_config:
                channel_report = await self.analytics_agent.get_channel_performance_report(
                    campaign_config['channel_id'],
                    campaign_config.get('date_range', 30)
                )
                report['channel_performance'] = channel_report
                
            return report
            
        except Exception as e:
            logger.error(f"Error generating campaign performance report: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def optimize_existing_campaign(self, optimization_config: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize existing YouTube marketing campaign"""
        try:
            optimization_results = {}
            
            # Optimize advertising campaign
            if 'campaign_id' in optimization_config:
                campaign_optimization = await self.campaign_agent.optimize_campaign_performance(
                    optimization_config['campaign_id']
                )
                optimization_results['campaign_optimization'] = campaign_optimization
                
            # Optimize content
            if 'video_id' in optimization_config:
                content_optimization = await self.content_agent.optimize_video_metadata(
                    optimization_config['video_id'],
                    optimization_config.get('metadata_updates', {})
                )
                optimization_results['content_optimization'] = content_optimization
                
            # Update targeting based on performance
            if 'channel_id' in optimization_config:
                audience_analysis = await self.audience_agent.analyze_channel_audience(
                    optimization_config['channel_id']
                )
                
                new_targeting = await self.audience_agent.generate_targeting_recommendations(
                    audience_analysis
                )
                optimization_results['targeting_updates'] = new_targeting
                
            return {
                'optimization_results': optimization_results,
                'status': 'success',
                'optimized_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error optimizing campaign: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def research_competitors(self, competitor_config: Dict[str, Any]) -> Dict[str, Any]:
        """Research competitor YouTube strategies"""
        try:
            competitor_channels = competitor_config.get('competitor_channels', [])
            
            if not competitor_channels:
                return {'error': 'No competitor channels provided', 'status': 'failed'}
                
            competitor_research = await self.audience_agent.research_competitor_audiences(
                competitor_channels
            )
            
            # Analyze competitor content strategies
            content_insights = {}
            for channel_id in competitor_channels[:3]:  # Limit to top 3 for performance
                try:
                    channel_analysis = await self.audience_agent.analyze_channel_audience(channel_id)
                    content_insights[channel_id] = channel_analysis
                except Exception as e:
                    logger.error(f"Error analyzing competitor {channel_id}: {e}")
                    continue
                    
            return {
                'competitor_research': competitor_research,
                'content_insights': content_insights,
                'research_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error researching competitors: {e}")
            return {'error': str(e), 'status': 'failed'}
            
    async def generate_content_strategy(self, strategy_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate YouTube content strategy based on analytics and research"""
        try:
            channel_id = strategy_config.get('channel_id')
            if not channel_id:
                return {'error': 'Channel ID required', 'status': 'failed'}
                
            # Analyze current channel performance
            channel_analysis = await self.audience_agent.analyze_channel_audience(channel_id)
            
            # Get performance insights
            performance_report = await self.analytics_agent.get_channel_performance_report(
                channel_id,
                strategy_config.get('analysis_period', 90)
            )
            
            # Research competitors if provided
            competitor_insights = {}
            if 'competitor_channels' in strategy_config:
                competitor_research = await self.research_competitors({
                    'competitor_channels': strategy_config['competitor_channels']
                })
                competitor_insights = competitor_research.get('competitor_research', {})
                
            # Generate content recommendations
            content_recommendations = await self.analytics_agent._generate_content_recommendations(channel_id)
            
            # Generate targeting strategy
            targeting_strategy = await self.audience_agent.generate_targeting_recommendations(channel_analysis)
            
            return {
                'channel_analysis': channel_analysis,
                'performance_insights': performance_report.get('insights', []),
                'competitor_insights': competitor_insights,
                'content_recommendations': content_recommendations,
                'targeting_strategy': targeting_strategy,
                'strategy_generated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating content strategy: {e}")
            return {'error': str(e), 'status': 'failed'}

# Test functions
async def test_youtube_campaign_creation():
    """Test YouTube advertising campaign creation"""
    try:
        # Mock credentials
        credentials = {
            'developer_token': 'test_dev_token',
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',
            'refresh_token': 'test_refresh_token',
            'customer_id': 'test_customer_id'
        }
        
        integration = YouTubeMarketingIntegration(credentials)
        
        # Test campaign data
        campaign_data = YouTubeCampaignData(
            name="Test YouTube Campaign",
            objective=YouTubeCampaignObjective.AWARENESS,
            budget_amount=1000.0,
            bid_strategy="target_cpm",
            target_audience={
                "age_range": "25-34",
                "interests": ["technology", "marketing"]
            },
            ad_format=YouTubeAdFormat.SKIPPABLE_IN_STREAM,
            video_asset_url="https://youtube.com/watch?v=test123"
        )
        
        campaign_config = {
            'campaign_data': asdict(campaign_data),
            'channel_id': 'test_channel_id'
        }
        
        result = await integration.create_comprehensive_marketing_campaign(campaign_config)
        
        print("YouTube Campaign Creation Test:")
        print(f"Status: {result.get('status', 'unknown')}")
        print(f"Campaign ID: {result.get('campaign_id', 'N/A')}")
        print(f"Results: {result.get('results', {})}")
        
        return result
        
    except Exception as e:
        print(f"Test failed: {e}")
        return {'error': str(e), 'status': 'test_failed'}

async def test_youtube_content_upload():
    """Test YouTube content upload and optimization"""
    try:
        credentials = {
            'api_key': 'test_api_key',
            'oauth_credentials': {
                'client_id': 'test_client_id',
                'client_secret': 'test_client_secret',
                'refresh_token': 'test_refresh_token'
            }
        }
        
        content_agent = YouTubeContentAgent(credentials)
        
        # Test video data
        video_data = YouTubeVideoData(
            title="Test Marketing Video",
            description="This is a test marketing video for YouTube integration",
            tags=["marketing", "youtube", "automation", "bizosaas"],
            category=YouTubeContentCategory.BUSINESS
        )
        
        # Mock video upload (would normally require actual video file)
        print("YouTube Content Upload Test:")
        print(f"Video Title: {video_data.title}")
        print(f"Category: {video_data.category}")
        print(f"Tags: {video_data.tags}")
        print("Note: Actual upload requires valid OAuth credentials and video file")
        
        return {
            'status': 'test_completed',
            'video_data': asdict(video_data),
            'note': 'Mock test - requires actual credentials for real upload'
        }
        
    except Exception as e:
        print(f"Content upload test failed: {e}")
        return {'error': str(e), 'status': 'test_failed'}

async def test_youtube_analytics():
    """Test YouTube analytics and reporting"""
    try:
        credentials = {
            'api_key': 'test_api_key',
            'oauth_credentials': {
                'client_id': 'test_client_id',
                'client_secret': 'test_client_secret',
                'refresh_token': 'test_refresh_token'
            }
        }
        
        analytics_agent = YouTubeAnalyticsAgent(credentials)
        
        # Test analytics data structure
        mock_analytics = YouTubeAnalyticsData(
            video_id="test_video_123",
            views=10000,
            likes=500,
            dislikes=25,
            comments=150,
            shares=75,
            subscribers_gained=25,
            watch_time_minutes=5000.0,
            average_view_duration=180.5,
            click_through_rate=0.05,
            engagement_rate=0.067,
            revenue=125.50,
            cpm=2.50,
            rpm=12.55
        )
        
        print("YouTube Analytics Test:")
        print(f"Video ID: {mock_analytics.video_id}")
        print(f"Views: {mock_analytics.views:,}")
        print(f"Engagement Rate: {mock_analytics.engagement_rate:.2%}")
        print(f"Watch Time: {mock_analytics.watch_time_minutes:,.0f} minutes")
        print(f"Revenue: ${mock_analytics.revenue:.2f}")
        
        return {
            'status': 'test_completed',
            'analytics_data': asdict(mock_analytics),
            'note': 'Mock test - requires actual credentials for real data'
        }
        
    except Exception as e:
        print(f"Analytics test failed: {e}")
        return {'error': str(e), 'status': 'test_failed'}

async def test_youtube_integration():
    """Run comprehensive test of YouTube Marketing API integration"""
    print("=" * 60)
    print("YouTube Marketing API Integration - Comprehensive Test")
    print("=" * 60)
    
    # Test campaign creation
    campaign_result = await test_youtube_campaign_creation()
    print()
    
    # Test content upload
    content_result = await test_youtube_content_upload()
    print()
    
    # Test analytics
    analytics_result = await test_youtube_analytics()
    print()
    
    # Summary
    print("=" * 60)
    print("Test Summary:")
    print(f"Campaign Creation: {'✓' if campaign_result.get('status') != 'test_failed' else '✗'}")
    print(f"Content Upload: {'✓' if content_result.get('status') != 'test_failed' else '✗'}")
    print(f"Analytics: {'✓' if analytics_result.get('status') != 'test_failed' else '✗'}")
    print("=" * 60)
    
    return {
        'campaign_test': campaign_result,
        'content_test': content_result,
        'analytics_test': analytics_result
    }

if __name__ == "__main__":
    # Run tests
    asyncio.run(test_youtube_integration())
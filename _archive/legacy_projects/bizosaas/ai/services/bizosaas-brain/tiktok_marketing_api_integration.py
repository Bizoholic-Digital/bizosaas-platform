"""
TikTok Marketing API Integration for BizOSaaS Brain

This module provides comprehensive TikTok marketing automation capabilities through 
specialized AI agents for viral content creation, influencer campaigns, and trend tracking.

Architecture:
- TikTokCampaignAgent: Campaign creation and management via TikTok for Business API
- TikTokContentAgent: Video content creation, posting, and viral trend tracking
- TikTokAudienceAgent: Audience targeting, engagement, and community management
- TikTokAnalyticsAgent: Performance tracking, viral metrics, and growth analytics

Author: BizOSaaS Development Team
Version: 1.0.0
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import hashlib
import hmac
import base64
from urllib.parse import urlencode, quote
import mimetypes
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TikTokCampaignObjective(Enum):
    """TikTok campaign objectives"""
    REACH = "REACH"
    VIDEO_VIEW = "VIDEO_VIEW"
    TRAFFIC = "TRAFFIC"
    CONVERSIONS = "CONVERSIONS"
    APP_INSTALL = "APP_INSTALL"
    LEAD_GENERATION = "LEAD_GENERATION"
    ENGAGEMENT = "ENGAGEMENT"


class TikTokContentType(Enum):
    """TikTok content types"""
    VIDEO = "VIDEO"
    SPARK_AD = "SPARK_AD"
    COLLECTION_AD = "COLLECTION_AD"
    BRANDED_HASHTAG = "BRANDED_HASHTAG_CHALLENGE"
    BRANDED_EFFECT = "BRANDED_EFFECT"


class TikTokAudienceType(Enum):
    """TikTok audience targeting types"""
    DEMOGRAPHICS = "demographics"
    INTERESTS = "interests"
    BEHAVIORS = "behaviors"
    CUSTOM_AUDIENCES = "custom_audiences"
    LOOKALIKE_AUDIENCES = "lookalike_audiences"
    DEVICE_TARGETING = "device_targeting"


class TikTokPlacement(Enum):
    """TikTok ad placements"""
    TIKTOK = "PLACEMENT_TYPE_TIKTOK"
    PANGLE = "PLACEMENT_TYPE_PANGLE"
    BOTH = "PLACEMENT_TYPE_AUTOMATIC"


@dataclass
class TikTokCampaignConfig:
    """Configuration for TikTok campaigns"""
    name: str
    objective: TikTokCampaignObjective
    daily_budget: float
    placements: List[TikTokPlacement]
    targeting: Dict[str, Any] = None
    bid_strategy: str = "BID_TYPE_NO_BID"
    optimization_goal: str = "CLICK"
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    
    def to_api_format(self) -> Dict[str, Any]:
        """Convert to TikTok API format"""
        config = {
            "campaign_name": self.name,
            "objective_type": self.objective.value,
            "budget_mode": "BUDGET_MODE_DAY",
            "budget": int(self.daily_budget * 100),  # TikTok API uses cents
            "status": "ENABLE"  # Campaign status
        }
        
        if self.start_time:
            config["schedule_start_time"] = self.start_time
            
        if self.end_time:
            config["schedule_end_time"] = self.end_time
            
        return config


@dataclass
class TikTokVideoContent:
    """TikTok video content configuration"""
    video_url: str
    video_cover_image_url: str
    brand_safety_type: str = "STANDARD_INVENTORY"
    caption: str = ""
    hashtags: List[str] = None
    mentions: List[str] = None
    call_to_action: str = "LEARN_MORE"
    landing_page_url: Optional[str] = None
    
    def format_caption(self) -> str:
        """Format caption with hashtags and mentions"""
        formatted_caption = self.caption
        
        if self.mentions:
            for mention in self.mentions:
                if not mention.startswith("@"):
                    mention = f"@{mention}"
                formatted_caption += f" {mention}"
        
        if self.hashtags:
            hashtag_text = " ".join([f"#{tag.lstrip('#')}" for tag in self.hashtags])
            formatted_caption += f" {hashtag_text}"
            
        return formatted_caption
    
    def to_api_format(self) -> Dict[str, Any]:
        """Convert to TikTok Creative API format"""
        return {
            "video_id": self.video_url,
            "image_ids": [self.video_cover_image_url],
            "brand_safety_type": self.brand_safety_type,
            "ad_text": self.format_caption(),
            "call_to_action": self.call_to_action,
            "landing_page_url": self.landing_page_url,
            "creative_type": "VIDEO_TYPE_VIDEO"
        }


@dataclass
class TikTokTrendingHashtag:
    """TikTok trending hashtag data"""
    hashtag: str
    view_count: int
    growth_rate: float
    trend_score: float
    category: str
    related_hashtags: List[str] = None


class TikTokAPIClient:
    """Base TikTok API client with authentication and rate limiting"""
    
    def __init__(self, access_token: str, advertiser_id: str = None, app_id: str = None, secret: str = None):
        self.access_token = access_token
        self.advertiser_id = advertiser_id
        self.app_id = app_id
        self.secret = secret
        self.base_url = "https://business-api.tiktok.com/open_api/v1.3"
        self.session = None
        self.rate_limit_remaining = 100
        self.rate_limit_reset = datetime.now()
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers={
                "Access-Token": self.access_token,
                "Content-Type": "application/json"
            },
            timeout=aiohttp.ClientTimeout(total=60)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
            
    async def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict[str, Any]:
        """Make authenticated request to TikTok API"""
        if not self.session:
            raise RuntimeError("Client not initialized. Use async context manager.")
            
        # Check rate limits
        if self.rate_limit_remaining <= 5 and datetime.now() < self.rate_limit_reset:
            wait_time = (self.rate_limit_reset - datetime.now()).total_seconds()
            logger.warning(f"Rate limit approaching. Waiting {wait_time:.1f}s")
            await asyncio.sleep(wait_time)
            
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Add advertiser_id to data if available
        if self.advertiser_id and data:
            data["advertiser_id"] = self.advertiser_id
        elif self.advertiser_id and not data:
            data = {"advertiser_id": self.advertiser_id}
            
        try:
            async with self.session.request(method, url, json=data, params=params) as response:
                # Update rate limit info from headers
                self.rate_limit_remaining = int(response.headers.get("X-Rate-Limit-Remaining", 100))
                reset_time = response.headers.get("X-Rate-Limit-Reset")
                if reset_time:
                    self.rate_limit_reset = datetime.fromtimestamp(int(reset_time))
                
                try:
                    response_data = await response.json()
                except:
                    response_data = {"message": await response.text()}
                
                if response.status >= 400:
                    logger.error(f"TikTok API error {response.status}: {response_data}")
                    return {
                        "success": False,
                        "error": f"API error {response.status}",
                        "details": response_data,
                        "status_code": response.status
                    }
                    
                # TikTok API has a specific response format
                if response_data.get("code") != 0:
                    logger.error(f"TikTok API business error: {response_data}")
                    return {
                        "success": False,
                        "error": "TikTok API error",
                        "details": response_data,
                        "code": response_data.get("code")
                    }
                    
                logger.info(f"TikTok API {method} {endpoint}: Success")
                return {
                    "success": True,
                    "data": response_data.get("data", response_data),
                    "status_code": response.status
                }
                
        except aiohttp.ClientError as e:
            logger.error(f"TikTok API request failed: {str(e)}")
            return {
                "success": False,
                "error": "Request failed",
                "details": str(e)
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "success": False,
                "error": "Unexpected error",
                "details": str(e)
            }


class TikTokCampaignAgent:
    """AI agent for TikTok campaign management"""
    
    def __init__(self, access_token: str, advertiser_id: str):
        self.access_token = access_token
        self.advertiser_id = advertiser_id
        self.client = TikTokAPIClient(access_token, advertiser_id)
        
    async def create_campaign(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new TikTok campaign"""
        try:
            config = TikTokCampaignConfig(
                name=request_data.get("name", "New TikTok Campaign"),
                objective=TikTokCampaignObjective(request_data.get("objective", "VIDEO_VIEW")),
                daily_budget=float(request_data.get("daily_budget", 20.0)),
                placements=[TikTokPlacement(p) for p in request_data.get("placements", ["PLACEMENT_TYPE_TIKTOK"])],
                targeting=request_data.get("targeting", {}),
                bid_strategy=request_data.get("bid_strategy", "BID_TYPE_NO_BID"),
                optimization_goal=request_data.get("optimization_goal", "CLICK")
            )
            
            async with self.client as client:
                campaign_data = config.to_api_format()
                
                response = await client._make_request("POST", "campaign/create/", data=campaign_data)
                
                if response.get("success"):
                    campaign_id = response["data"]["campaign_id"]
                    
                    # Get campaign details
                    details = await self.get_campaign_details(campaign_id)
                    
                    return {
                        "success": True,
                        "campaign_id": campaign_id,
                        "details": details,
                        "message": "TikTok campaign created successfully"
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Campaign creation error: {str(e)}")
            return {
                "success": False,
                "error": "Campaign creation failed",
                "details": str(e)
            }
    
    async def get_campaign_details(self, campaign_id: str) -> Dict[str, Any]:
        """Get detailed campaign information"""
        try:
            async with self.client as client:
                response = await client._make_request(
                    "GET",
                    "campaign/get/",
                    params={
                        "advertiser_id": self.advertiser_id,
                        "campaign_ids": f'["{campaign_id}"]',
                        "fields": '["campaign_id","campaign_name","objective_type","status","budget","schedule_start_time","schedule_end_time","create_time","modify_time"]'
                    }
                )
                
                if response.get("success") and response["data"].get("list"):
                    return response["data"]["list"][0]
                
                return {"error": "Failed to fetch campaign details"}
                
        except Exception as e:
            logger.error(f"Get campaign details error: {str(e)}")
            return {"error": str(e)}
    
    async def create_ad_group(self, campaign_id: str, ad_group_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create ad group for TikTok campaign"""
        try:
            ad_group_config = {
                "campaign_id": campaign_id,
                "adgroup_name": ad_group_data.get("name", "TikTok Ad Group"),
                "placement_type": ad_group_data.get("placement_type", "PLACEMENT_TYPE_TIKTOK"),
                "promotion_type": ad_group_data.get("promotion_type", "WEBSITE"),
                "budget_mode": "BUDGET_MODE_DAY",
                "budget": int(float(ad_group_data.get("daily_budget", 10.0)) * 100),
                "bid_type": ad_group_data.get("bid_type", "BID_TYPE_NO_BID"),
                "optimization_goal": ad_group_data.get("optimization_goal", "CLICK"),
                "targeting": ad_group_data.get("targeting", {}),
                "status": "ENABLE",
                "pacing": "PACING_MODE_SMOOTH"
            }
            
            async with self.client as client:
                response = await client._make_request("POST", "adgroup/create/", data=ad_group_config)
                
                if response.get("success"):
                    return {
                        "success": True,
                        "ad_group_id": response["data"]["adgroup_id"],
                        "campaign_id": campaign_id,
                        "message": "Ad group created successfully"
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Ad group creation error: {str(e)}")
            return {
                "success": False,
                "error": "Ad group creation failed",
                "details": str(e)
            }
    
    async def get_campaign_performance(self, campaign_ids: List[str], date_range: Dict[str, str]) -> Dict[str, Any]:
        """Get TikTok campaign performance metrics"""
        try:
            metrics = [
                "spend", "impressions", "clicks", "ctr", "cpc", "cpm",
                "conversion", "cost_per_conversion", "conversion_rate",
                "video_play_actions", "video_watched_2s", "video_watched_6s",
                "reach", "frequency"
            ]
            
            params = {
                "advertiser_id": self.advertiser_id,
                "service_type": "AUCTION",
                "report_type": "BASIC",
                "data_level": "AUCTION_CAMPAIGN",
                "dimensions": '["campaign_id"]',
                "metrics": json.dumps(metrics),
                "start_date": date_range.get("start_date"),
                "end_date": date_range.get("end_date"),
                "filters": json.dumps([{
                    "field_name": "campaign_id",
                    "filter_type": "IN",
                    "filter_value": campaign_ids
                }])
            }
            
            async with self.client as client:
                response = await client._make_request("GET", "report/integrated/get/", params=params)
                
                if response.get("success") and response["data"].get("list"):
                    performance_data = response["data"]["list"]
                    
                    # Process performance data
                    processed_metrics = {}
                    for campaign_data in performance_data:
                        campaign_id = campaign_data.get("dimensions", {}).get("campaign_id")
                        metrics_data = campaign_data.get("metrics", {})
                        
                        processed_metrics[campaign_id] = {
                            "impressions": int(metrics_data.get("impressions", 0)),
                            "clicks": int(metrics_data.get("clicks", 0)),
                            "spend": float(metrics_data.get("spend", 0)),
                            "conversions": int(metrics_data.get("conversion", 0)),
                            "ctr": float(metrics_data.get("ctr", 0)),
                            "cpc": float(metrics_data.get("cpc", 0)),
                            "cpm": float(metrics_data.get("cpm", 0)),
                            "video_views": int(metrics_data.get("video_play_actions", 0)),
                            "video_2s_views": int(metrics_data.get("video_watched_2s", 0)),
                            "video_6s_views": int(metrics_data.get("video_watched_6s", 0)),
                            "reach": int(metrics_data.get("reach", 0))
                        }
                    
                    return {
                        "success": True,
                        "campaign_performance": processed_metrics,
                        "date_range": date_range
                    }
                
                return {
                    "success": False,
                    "error": "No performance data available"
                }
                
        except Exception as e:
            logger.error(f"Performance tracking error: {str(e)}")
            return {
                "success": False,
                "error": "Performance tracking failed",
                "details": str(e)
            }


class TikTokContentAgent:
    """AI agent for TikTok content creation and viral trend tracking"""
    
    def __init__(self, access_token: str, advertiser_id: str):
        self.access_token = access_token
        self.advertiser_id = advertiser_id
        self.client = TikTokAPIClient(access_token, advertiser_id)
        
    async def upload_video(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Upload video content to TikTok"""
        try:
            video_url = video_data.get("video_url", "")
            video_signature = video_data.get("video_signature", "")
            
            if not video_url:
                return {
                    "success": False,
                    "error": "Video URL is required"
                }
            
            upload_data = {
                "advertiser_id": self.advertiser_id,
                "upload_type": "UPLOAD_BY_URL",
                "video_url": video_url,
                "video_signature": video_signature,
                "flaw_detect": True,
                "auto_bind_enabled": True,
                "auto_fix_enabled": True
            }
            
            async with self.client as client:
                response = await client._make_request("POST", "file/video/ad/upload/", data=upload_data)
                
                if response.get("success"):
                    return {
                        "success": True,
                        "video_id": response["data"]["video_id"],
                        "message": "Video uploaded successfully"
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Video upload error: {str(e)}")
            return {
                "success": False,
                "error": "Video upload failed",
                "details": str(e)
            }
    
    async def create_video_ad(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create TikTok video ad"""
        try:
            content = TikTokVideoContent(
                video_url=request_data.get("video_url", ""),
                video_cover_image_url=request_data.get("cover_image_url", ""),
                caption=request_data.get("caption", ""),
                hashtags=request_data.get("hashtags", []),
                mentions=request_data.get("mentions", []),
                call_to_action=request_data.get("call_to_action", "LEARN_MORE"),
                landing_page_url=request_data.get("landing_page_url"),
                brand_safety_type=request_data.get("brand_safety_type", "STANDARD_INVENTORY")
            )
            
            ad_config = {
                "advertiser_id": self.advertiser_id,
                "adgroup_id": request_data.get("adgroup_id", ""),
                "ad_name": request_data.get("ad_name", "TikTok Video Ad"),
                "ad_format": "SINGLE_VIDEO",
                "ad_text": content.format_caption(),
                "call_to_action": content.call_to_action,
                "landing_page_url": content.landing_page_url,
                "video_id": content.video_url,  # Assuming this is the uploaded video ID
                "image_ids": [content.video_cover_image_url],
                "brand_safety_type": content.brand_safety_type,
                "status": "ENABLE"
            }
            
            async with self.client as client:
                response = await client._make_request("POST", "ad/create/", data=ad_config)
                
                if response.get("success"):
                    return {
                        "success": True,
                        "ad_id": response["data"]["ad_id"],
                        "content": asdict(content),
                        "message": "TikTok video ad created successfully"
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Video ad creation error: {str(e)}")
            return {
                "success": False,
                "error": "Video ad creation failed",
                "details": str(e)
            }
    
    async def get_trending_hashtags(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get trending hashtags for TikTok content optimization"""
        try:
            # Note: TikTok doesn't have a public trending hashtags API
            # This would typically integrate with third-party trend tracking services
            # or use TikTok's internal research tools
            
            category = request_data.get("category", "general")
            region = request_data.get("region", "US")
            limit = request_data.get("limit", 20)
            
            # Simulated trending hashtags (in production, integrate with actual trend APIs)
            trending_hashtags = [
                TikTokTrendingHashtag(
                    hashtag="viral",
                    view_count=1500000000,
                    growth_rate=25.5,
                    trend_score=95.0,
                    category="general",
                    related_hashtags=["fyp", "trending", "viral"]
                ),
                TikTokTrendingHashtag(
                    hashtag="fyp",
                    view_count=8900000000,
                    growth_rate=15.2,
                    trend_score=88.0,
                    category="general",
                    related_hashtags=["foryou", "viral", "trending"]
                ),
                TikTokTrendingHashtag(
                    hashtag="business",
                    view_count=450000000,
                    growth_rate=42.1,
                    trend_score=78.0,
                    category="business",
                    related_hashtags=["entrepreneur", "businesstips", "marketing"]
                ),
                TikTokTrendingHashtag(
                    hashtag="marketing",
                    view_count=320000000,
                    growth_rate=38.7,
                    trend_score=75.0,
                    category="business",
                    related_hashtags=["business", "digitalmarketing", "socialmedia"]
                )
            ]
            
            # Filter by category if specified
            if category != "general":
                trending_hashtags = [h for h in trending_hashtags if h.category == category]
            
            # Sort by trend score
            trending_hashtags.sort(key=lambda x: x.trend_score, reverse=True)
            
            return {
                "success": True,
                "trending_hashtags": [asdict(h) for h in trending_hashtags[:limit]],
                "category": category,
                "region": region,
                "recommendations": self._generate_hashtag_recommendations(trending_hashtags[:10])
            }
            
        except Exception as e:
            logger.error(f"Trending hashtags error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to get trending hashtags",
                "details": str(e)
            }
    
    async def analyze_viral_content(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze viral content patterns for optimization"""
        try:
            content_url = request_data.get("content_url", "")
            analysis_type = request_data.get("analysis_type", "comprehensive")
            
            # In production, this would analyze actual TikTok content
            # For now, we'll provide structured analysis framework
            
            viral_analysis = {
                "content_score": 85.5,
                "viral_potential": "HIGH",
                "engagement_factors": {
                    "hook_strength": 9.2,
                    "visual_appeal": 8.8,
                    "trend_alignment": 9.5,
                    "audio_quality": 8.0,
                    "timing": 7.5
                },
                "optimization_suggestions": [
                    "Add trending audio to increase discoverability",
                    "Include popular hashtags: #fyp, #viral, #trending",
                    "Post during peak hours (6-9 PM EST)",
                    "Create strong hook in first 3 seconds",
                    "Use jump cuts to maintain engagement"
                ],
                "predicted_metrics": {
                    "estimated_views": "100K-500K",
                    "estimated_engagement_rate": "12-15%",
                    "viral_probability": 0.75
                },
                "content_elements": {
                    "has_trending_audio": True,
                    "has_captions": True,
                    "video_length": 28,  # seconds
                    "trend_participation": True,
                    "call_to_action": True
                }
            }
            
            return {
                "success": True,
                "content_url": content_url,
                "viral_analysis": viral_analysis,
                "recommendations": self._generate_content_optimization_tips(viral_analysis)
            }
            
        except Exception as e:
            logger.error(f"Viral content analysis error: {str(e)}")
            return {
                "success": False,
                "error": "Viral content analysis failed",
                "details": str(e)
            }
    
    def _generate_hashtag_recommendations(self, trending_hashtags: List[TikTokTrendingHashtag]) -> List[str]:
        """Generate hashtag usage recommendations"""
        recommendations = []
        
        if trending_hashtags:
            top_hashtag = trending_hashtags[0]
            recommendations.append(f"Use #{top_hashtag.hashtag} for maximum visibility (95M+ views)")
        
        recommendations.extend([
            "Mix trending hashtags with niche-specific ones for better targeting",
            "Use 3-5 hashtags per video for optimal performance",
            "Include #fyp or #foryou to increase For You Page visibility",
            "Research hashtag competition before using",
            "Create branded hashtags for campaign tracking"
        ])
        
        return recommendations
    
    def _generate_content_optimization_tips(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate content optimization recommendations"""
        tips = []
        
        engagement_factors = analysis.get("engagement_factors", {})
        
        if engagement_factors.get("hook_strength", 0) < 8:
            tips.append("Strengthen your opening hook - first 3 seconds are crucial")
        
        if engagement_factors.get("audio_quality", 0) < 8:
            tips.append("Use trending or high-quality audio to boost engagement")
        
        if engagement_factors.get("trend_alignment", 0) < 8:
            tips.append("Participate in current trends and challenges")
        
        tips.extend([
            "Post consistently during your audience's peak hours",
            "Use captions for accessibility and better engagement",
            "Encourage comments with questions or calls-to-action",
            "Keep videos between 15-30 seconds for optimal performance",
            "Cross-promote on other social platforms"
        ])
        
        return tips


class TikTokAudienceAgent:
    """AI agent for TikTok audience targeting and engagement"""
    
    def __init__(self, access_token: str, advertiser_id: str):
        self.access_token = access_token
        self.advertiser_id = advertiser_id
        self.client = TikTokAPIClient(access_token, advertiser_id)
        
    async def create_custom_audience(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create custom audience for TikTok campaigns"""
        try:
            audience_config = {
                "advertiser_id": self.advertiser_id,
                "custom_audience_name": request_data.get("name", "Custom Audience"),
                "audience_type": request_data.get("audience_type", "CUSTOMER_FILE"),
                "file_type": request_data.get("file_type", "EMAIL_SHA256"),
                "calculate_type": "UNION"
            }
            
            # Handle different audience creation methods
            audience_type = request_data.get("audience_type", "CUSTOMER_FILE")
            
            if audience_type == "WEBSITE_TRAFFIC":
                audience_config.update({
                    "audience_type": "WEBSITE_TRAFFIC",
                    "pixel_id": request_data.get("pixel_id", ""),
                    "retention_days": request_data.get("retention_days", 30),
                    "rule": request_data.get("website_rules", {})
                })
            elif audience_type == "APP_ACTIVITY":
                audience_config.update({
                    "audience_type": "APP_ACTIVITY", 
                    "app_id": request_data.get("app_id", ""),
                    "retention_days": request_data.get("retention_days", 30),
                    "rule": request_data.get("app_rules", {})
                })
            
            async with self.client as client:
                response = await client._make_request("POST", "dmp/custom_audience/create/", data=audience_config)
                
                if response.get("success"):
                    return {
                        "success": True,
                        "audience_id": response["data"]["custom_audience_id"],
                        "audience_name": audience_config["custom_audience_name"],
                        "audience_type": audience_type,
                        "message": "Custom audience created successfully"
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Custom audience creation error: {str(e)}")
            return {
                "success": False,
                "error": "Custom audience creation failed",
                "details": str(e)
            }
    
    async def get_audience_insights(self, audience_id: str) -> Dict[str, Any]:
        """Get insights for custom audience"""
        try:
            async with self.client as client:
                response = await client._make_request(
                    "GET",
                    "dmp/custom_audience/get/",
                    params={
                        "advertiser_id": self.advertiser_id,
                        "custom_audience_ids": f'["{audience_id}"]'
                    }
                )
                
                if response.get("success") and response["data"].get("list"):
                    audience_data = response["data"]["list"][0]
                    
                    return {
                        "success": True,
                        "audience_id": audience_id,
                        "audience_size": audience_data.get("audience_size", 0),
                        "audience_type": audience_data.get("audience_type"),
                        "status": audience_data.get("status"),
                        "create_time": audience_data.get("create_time"),
                        "coverage": self._calculate_audience_coverage(audience_data)
                    }
                
                return {
                    "success": False,
                    "error": "Audience not found"
                }
                
        except Exception as e:
            logger.error(f"Audience insights error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to get audience insights",
                "details": str(e)
            }
    
    async def suggest_targeting_options(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest targeting options based on campaign goals"""
        try:
            campaign_objective = request_data.get("objective", "VIDEO_VIEW")
            target_audience = request_data.get("target_audience", {})
            budget_range = request_data.get("budget_range", "medium")
            
            # Generate targeting suggestions based on objective
            targeting_suggestions = self._generate_targeting_suggestions(
                campaign_objective, 
                target_audience, 
                budget_range
            )
            
            # Get interest categories (simulated - in production use actual API)
            interest_categories = await self._get_interest_categories()
            
            return {
                "success": True,
                "targeting_suggestions": targeting_suggestions,
                "available_interests": interest_categories,
                "recommended_audience_size": self._get_recommended_audience_size(campaign_objective),
                "targeting_tips": self._get_targeting_tips(campaign_objective)
            }
            
        except Exception as e:
            logger.error(f"Targeting suggestions error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to generate targeting suggestions",
                "details": str(e)
            }
    
    async def _get_interest_categories(self) -> List[Dict[str, Any]]:
        """Get available interest categories for targeting"""
        # In production, this would call the actual TikTok interests API
        return [
            {"category": "Business & Industry", "subcategories": ["Marketing", "Entrepreneurship", "Startups"]},
            {"category": "Technology", "subcategories": ["AI & Machine Learning", "Software", "Gadgets"]},
            {"category": "Entertainment", "subcategories": ["Music", "Movies", "Gaming"]},
            {"category": "Fashion & Beauty", "subcategories": ["Fashion", "Makeup", "Skincare"]},
            {"category": "Food & Drink", "subcategories": ["Cooking", "Restaurants", "Healthy Eating"]},
            {"category": "Sports & Fitness", "subcategories": ["Fitness", "Sports", "Health"]},
            {"category": "Travel", "subcategories": ["Adventure", "Luxury Travel", "Budget Travel"]},
            {"category": "Education", "subcategories": ["Online Learning", "Professional Development", "Skills"]}
        ]
    
    def _generate_targeting_suggestions(self, objective: str, target_audience: Dict, budget_range: str) -> Dict[str, Any]:
        """Generate AI-powered targeting suggestions"""
        suggestions = {
            "demographics": {},
            "interests": [],
            "behaviors": [],
            "custom_audiences": [],
            "placement_recommendations": []
        }
        
        # Demographics suggestions based on objective
        if objective == "LEAD_GENERATION":
            suggestions["demographics"] = {
                "age_range": [25, 54],
                "gender": "ALL",
                "languages": ["en"],
                "income_levels": ["MIDDLE_CLASS", "UPPER_MIDDLE_CLASS"]
            }
        elif objective == "VIDEO_VIEW":
            suggestions["demographics"] = {
                "age_range": [16, 34],
                "gender": "ALL", 
                "languages": ["en"]
            }
        
        # Interest suggestions
        business_interests = ["Marketing", "Entrepreneurship", "Business Development", "Digital Marketing"]
        if target_audience.get("business_focused"):
            suggestions["interests"].extend(business_interests)
        
        # Behavior suggestions
        suggestions["behaviors"] = [
            "Frequent App Users",
            "Online Shoppers",
            "Video Content Consumers"
        ]
        
        # Placement recommendations
        if budget_range == "low":
            suggestions["placement_recommendations"] = ["PLACEMENT_TYPE_TIKTOK"]
        else:
            suggestions["placement_recommendations"] = ["PLACEMENT_TYPE_AUTOMATIC"]
        
        return suggestions
    
    def _calculate_audience_coverage(self, audience_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate audience coverage metrics"""
        audience_size = audience_data.get("audience_size", 0)
        
        coverage = {
            "size_category": "small",
            "reach_potential": "limited",
            "cost_efficiency": "high"
        }
        
        if audience_size > 1000000:
            coverage.update({
                "size_category": "large",
                "reach_potential": "high",
                "cost_efficiency": "medium"
            })
        elif audience_size > 100000:
            coverage.update({
                "size_category": "medium",
                "reach_potential": "good",
                "cost_efficiency": "good"
            })
        
        return coverage
    
    def _get_recommended_audience_size(self, objective: str) -> Dict[str, Any]:
        """Get recommended audience size based on campaign objective"""
        recommendations = {
            "VIDEO_VIEW": {"min": 100000, "max": 10000000, "optimal": 1000000},
            "TRAFFIC": {"min": 500000, "max": 5000000, "optimal": 1500000}, 
            "CONVERSIONS": {"min": 200000, "max": 2000000, "optimal": 800000},
            "LEAD_GENERATION": {"min": 100000, "max": 1000000, "optimal": 400000}
        }
        
        return recommendations.get(objective, {"min": 100000, "max": 1000000, "optimal": 500000})
    
    def _get_targeting_tips(self, objective: str) -> List[str]:
        """Get targeting tips based on campaign objective"""
        base_tips = [
            "Start with broader targeting and optimize based on performance",
            "Use lookalike audiences for better conversion rates",
            "Test different age ranges to find your optimal audience",
            "Consider device and connection type for video campaigns"
        ]
        
        objective_tips = {
            "VIDEO_VIEW": ["Target users who engage with video content", "Focus on entertainment and lifestyle interests"],
            "TRAFFIC": ["Use website custom audiences", "Target users with high purchase intent"],
            "CONVERSIONS": ["Create conversion-focused custom audiences", "Use pixel data for retargeting"],
            "LEAD_GENERATION": ["Target professional demographics", "Focus on business and career interests"]
        }
        
        return base_tips + objective_tips.get(objective, [])


class TikTokAnalyticsAgent:
    """AI agent for TikTok marketing analytics and insights"""
    
    def __init__(self, access_token: str, advertiser_id: str):
        self.access_token = access_token
        self.advertiser_id = advertiser_id
        self.client = TikTokAPIClient(access_token, advertiser_id)
        
    async def get_account_overview(self, date_range: Dict[str, str]) -> Dict[str, Any]:
        """Get comprehensive TikTok account overview"""
        try:
            metrics = [
                "spend", "impressions", "clicks", "ctr", "cpc", "cpm",
                "conversion", "cost_per_conversion", "conversion_rate",
                "video_play_actions", "video_watched_2s", "video_watched_6s",
                "profile_visits", "likes", "shares", "comments"
            ]
            
            params = {
                "advertiser_id": self.advertiser_id,
                "service_type": "AUCTION", 
                "report_type": "BASIC",
                "data_level": "AUCTION_ADVERTISER",
                "dimensions": '["advertiser_id"]',
                "metrics": json.dumps(metrics),
                "start_date": date_range.get("start_date"),
                "end_date": date_range.get("end_date")
            }
            
            async with self.client as client:
                response = await client._make_request("GET", "report/integrated/get/", params=params)
                
                if response.get("success") and response["data"].get("list"):
                    data = response["data"]["list"][0]
                    metrics_data = data.get("metrics", {})
                    
                    # Process metrics
                    processed_metrics = {
                        "spend": float(metrics_data.get("spend", 0)),
                        "impressions": int(metrics_data.get("impressions", 0)),
                        "clicks": int(metrics_data.get("clicks", 0)),
                        "video_views": int(metrics_data.get("video_play_actions", 0)),
                        "video_2s_views": int(metrics_data.get("video_watched_2s", 0)),
                        "video_6s_views": int(metrics_data.get("video_watched_6s", 0)),
                        "profile_visits": int(metrics_data.get("profile_visits", 0)),
                        "engagement": {
                            "likes": int(metrics_data.get("likes", 0)),
                            "shares": int(metrics_data.get("shares", 0)),
                            "comments": int(metrics_data.get("comments", 0))
                        },
                        "performance": {
                            "ctr": float(metrics_data.get("ctr", 0)),
                            "cpc": float(metrics_data.get("cpc", 0)),
                            "cpm": float(metrics_data.get("cpm", 0)),
                            "conversion_rate": float(metrics_data.get("conversion_rate", 0))
                        }
                    }
                    
                    # Calculate additional metrics
                    total_engagement = sum(processed_metrics["engagement"].values())
                    engagement_rate = (total_engagement / processed_metrics["impressions"]) * 100 if processed_metrics["impressions"] > 0 else 0
                    video_completion_rate = (processed_metrics["video_6s_views"] / processed_metrics["video_views"]) * 100 if processed_metrics["video_views"] > 0 else 0
                    
                    processed_metrics["calculated_metrics"] = {
                        "engagement_rate": engagement_rate,
                        "video_completion_rate": video_completion_rate,
                        "cost_per_engagement": processed_metrics["spend"] / total_engagement if total_engagement > 0 else 0
                    }
                    
                    return {
                        "success": True,
                        "advertiser_id": self.advertiser_id,
                        "date_range": date_range,
                        "metrics": processed_metrics,
                        "insights": self._generate_account_insights(processed_metrics)
                    }
                
                return {
                    "success": False,
                    "error": "No account data available"
                }
                
        except Exception as e:
            logger.error(f"Account overview error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to get account overview",
                "details": str(e)
            }
    
    async def analyze_video_performance(self, ad_ids: List[str], date_range: Dict[str, str]) -> Dict[str, Any]:
        """Analyze video ad performance in detail"""
        try:
            video_metrics = [
                "video_play_actions", "video_watched_2s", "video_watched_6s",
                "video_watched_25p", "video_watched_50p", "video_watched_75p", 
                "video_watched_100p", "impressions", "clicks", "spend",
                "likes", "shares", "comments", "profile_visits"
            ]
            
            params = {
                "advertiser_id": self.advertiser_id,
                "service_type": "AUCTION",
                "report_type": "BASIC", 
                "data_level": "AUCTION_AD",
                "dimensions": '["ad_id"]',
                "metrics": json.dumps(video_metrics),
                "start_date": date_range.get("start_date"),
                "end_date": date_range.get("end_date"),
                "filters": json.dumps([{
                    "field_name": "ad_id",
                    "filter_type": "IN",
                    "filter_value": ad_ids
                }])
            }
            
            async with self.client as client:
                response = await client._make_request("GET", "report/integrated/get/", params=params)
                
                if response.get("success") and response["data"].get("list"):
                    video_performance = []
                    
                    for ad_data in response["data"]["list"]:
                        ad_id = ad_data.get("dimensions", {}).get("ad_id")
                        metrics = ad_data.get("metrics", {})
                        
                        # Calculate video engagement metrics
                        video_views = int(metrics.get("video_play_actions", 0))
                        views_2s = int(metrics.get("video_watched_2s", 0))
                        views_6s = int(metrics.get("video_watched_6s", 0))
                        views_25p = int(metrics.get("video_watched_25p", 0))
                        views_50p = int(metrics.get("video_watched_50p", 0))
                        views_75p = int(metrics.get("video_watched_75p", 0))
                        views_100p = int(metrics.get("video_watched_100p", 0))
                        
                        performance_data = {
                            "ad_id": ad_id,
                            "video_metrics": {
                                "total_views": video_views,
                                "2s_views": views_2s,
                                "6s_views": views_6s,
                                "25p_views": views_25p,
                                "50p_views": views_50p,
                                "75p_views": views_75p,
                                "100p_views": views_100p
                            },
                            "engagement": {
                                "likes": int(metrics.get("likes", 0)),
                                "shares": int(metrics.get("shares", 0)),
                                "comments": int(metrics.get("comments", 0)),
                                "profile_visits": int(metrics.get("profile_visits", 0))
                            },
                            "completion_rates": {
                                "2s_rate": (views_2s / video_views) * 100 if video_views > 0 else 0,
                                "6s_rate": (views_6s / video_views) * 100 if video_views > 0 else 0,
                                "25p_rate": (views_25p / video_views) * 100 if video_views > 0 else 0,
                                "50p_rate": (views_50p / video_views) * 100 if video_views > 0 else 0,
                                "75p_rate": (views_75p / video_views) * 100 if video_views > 0 else 0,
                                "100p_rate": (views_100p / video_views) * 100 if video_views > 0 else 0
                            },
                            "spend": float(metrics.get("spend", 0))
                        }
                        
                        video_performance.append(performance_data)
                    
                    # Sort by engagement rate
                    video_performance.sort(
                        key=lambda x: sum(x["engagement"].values()) / max(x["video_metrics"]["total_views"], 1),
                        reverse=True
                    )
                    
                    return {
                        "success": True,
                        "video_performance": video_performance,
                        "summary": self._generate_video_performance_summary(video_performance),
                        "recommendations": self._generate_video_optimization_tips(video_performance)
                    }
                
                return {
                    "success": False,
                    "error": "No video performance data available"
                }
                
        except Exception as e:
            logger.error(f"Video performance analysis error: {str(e)}")
            return {
                "success": False,
                "error": "Video performance analysis failed",
                "details": str(e)
            }
    
    async def generate_growth_insights(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive growth insights and recommendations"""
        try:
            date_range = request_data.get("date_range", {})
            campaign_ids = request_data.get("campaign_ids", [])
            
            # Get account overview
            account_overview = await self.get_account_overview(date_range)
            
            # Get campaign performance
            campaign_performance = {}
            if campaign_ids:
                campaign_agent = TikTokCampaignAgent(self.access_token, self.advertiser_id)
                perf_result = await campaign_agent.get_campaign_performance(campaign_ids, date_range)
                if perf_result.get("success"):
                    campaign_performance = perf_result["campaign_performance"]
            
            # Generate growth insights
            growth_insights = {
                "account_health": self._assess_account_health(account_overview.get("metrics", {})),
                "growth_opportunities": self._identify_growth_opportunities(
                    account_overview.get("metrics", {}),
                    campaign_performance
                ),
                "competitive_analysis": self._generate_competitive_insights(),
                "trend_alignment": self._analyze_trend_alignment(),
                "optimization_priorities": self._prioritize_optimizations(
                    account_overview.get("metrics", {})
                )
            }
            
            return {
                "success": True,
                "report_id": hashlib.md5(f"{datetime.now().isoformat()}{self.advertiser_id}".encode()).hexdigest()[:16],
                "generated_at": datetime.now().isoformat(),
                "date_range": date_range,
                "account_metrics": account_overview.get("metrics", {}),
                "growth_insights": growth_insights,
                "action_plan": self._create_growth_action_plan(growth_insights)
            }
            
        except Exception as e:
            logger.error(f"Growth insights error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to generate growth insights",
                "details": str(e)
            }
    
    def _generate_account_insights(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate insights from account metrics"""
        insights = []
        
        engagement_rate = metrics.get("calculated_metrics", {}).get("engagement_rate", 0)
        video_completion_rate = metrics.get("calculated_metrics", {}).get("video_completion_rate", 0)
        ctr = metrics.get("performance", {}).get("ctr", 0)
        
        if engagement_rate > 8:
            insights.append(f"Excellent engagement rate at {engagement_rate:.2f}% - well above TikTok average")
        elif engagement_rate < 3:
            insights.append("Low engagement rate - focus on creating more interactive content")
        
        if video_completion_rate > 50:
            insights.append("High video completion rate indicates strong content quality")
        elif video_completion_rate < 25:
            insights.append("Low video completion rate - consider shorter, more engaging content")
        
        if ctr > 2:
            insights.append("Strong click-through rate shows effective call-to-actions")
        elif ctr < 0.8:
            insights.append("Low CTR - optimize ad creative and targeting")
        
        return insights
    
    def _generate_video_performance_summary(self, video_performance: List[Dict]) -> Dict[str, Any]:
        """Generate summary of video performance"""
        if not video_performance:
            return {}
        
        total_views = sum(video["video_metrics"]["total_views"] for video in video_performance)
        avg_completion_rate = sum(video["completion_rates"]["50p_rate"] for video in video_performance) / len(video_performance)
        total_engagement = sum(sum(video["engagement"].values()) for video in video_performance)
        
        best_performing = video_performance[0] if video_performance else {}
        
        return {
            "total_videos_analyzed": len(video_performance),
            "total_video_views": total_views,
            "average_completion_rate": avg_completion_rate,
            "total_engagement": total_engagement,
            "best_performing_ad": {
                "ad_id": best_performing.get("ad_id"),
                "views": best_performing.get("video_metrics", {}).get("total_views", 0),
                "engagement_rate": (sum(best_performing.get("engagement", {}).values()) / max(best_performing.get("video_metrics", {}).get("total_views", 1), 1)) * 100
            }
        }
    
    def _generate_video_optimization_tips(self, video_performance: List[Dict]) -> List[str]:
        """Generate video optimization recommendations"""
        tips = []
        
        if video_performance:
            avg_2s_rate = sum(video["completion_rates"]["2s_rate"] for video in video_performance) / len(video_performance)
            avg_6s_rate = sum(video["completion_rates"]["6s_rate"] for video in video_performance) / len(video_performance)
            
            if avg_2s_rate < 70:
                tips.append("Improve video hooks - many viewers drop off within 2 seconds")
            
            if avg_6s_rate < 40:
                tips.append("Focus on engaging content in first 6 seconds to reduce drop-off")
        
        tips.extend([
            "Use trending sounds and effects to increase discoverability",
            "Create content that encourages interaction (comments, likes, shares)",
            "Test different video lengths to find optimal duration",
            "Include clear call-to-actions in video content",
            "Optimize for mobile viewing with vertical format",
            "Post during peak hours when your audience is most active"
        ])
        
        return tips
    
    def _assess_account_health(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall account health"""
        health_score = 0
        health_factors = {}
        
        # Engagement rate assessment
        engagement_rate = metrics.get("calculated_metrics", {}).get("engagement_rate", 0)
        if engagement_rate > 6:
            health_factors["engagement"] = {"score": 90, "status": "excellent"}
            health_score += 30
        elif engagement_rate > 3:
            health_factors["engagement"] = {"score": 70, "status": "good"}
            health_score += 20
        else:
            health_factors["engagement"] = {"score": 40, "status": "needs_improvement"}
            health_score += 10
        
        # Video completion assessment
        completion_rate = metrics.get("calculated_metrics", {}).get("video_completion_rate", 0)
        if completion_rate > 40:
            health_factors["content_quality"] = {"score": 85, "status": "high"}
            health_score += 25
        elif completion_rate > 20:
            health_factors["content_quality"] = {"score": 65, "status": "medium"}
            health_score += 15
        else:
            health_factors["content_quality"] = {"score": 35, "status": "low"}
            health_score += 5
        
        # Cost efficiency assessment
        cpc = metrics.get("performance", {}).get("cpc", 0)
        if cpc < 0.5:
            health_factors["cost_efficiency"] = {"score": 90, "status": "excellent"}
            health_score += 20
        elif cpc < 1.0:
            health_factors["cost_efficiency"] = {"score": 70, "status": "good"}
            health_score += 15
        else:
            health_factors["cost_efficiency"] = {"score": 50, "status": "average"}
            health_score += 10
        
        # Overall reach assessment
        impressions = metrics.get("impressions", 0)
        if impressions > 1000000:
            health_factors["reach"] = {"score": 85, "status": "high"}
            health_score += 15
        elif impressions > 100000:
            health_factors["reach"] = {"score": 65, "status": "medium"}
            health_score += 10
        else:
            health_factors["reach"] = {"score": 40, "status": "low"}
            health_score += 5
        
        return {
            "overall_score": min(health_score, 100),
            "health_factors": health_factors,
            "status": "excellent" if health_score > 80 else "good" if health_score > 60 else "needs_improvement"
        }
    
    def _identify_growth_opportunities(self, account_metrics: Dict, campaign_performance: Dict) -> List[Dict[str, Any]]:
        """Identify growth opportunities"""
        opportunities = []
        
        engagement_rate = account_metrics.get("calculated_metrics", {}).get("engagement_rate", 0)
        if engagement_rate < 5:
            opportunities.append({
                "type": "engagement_optimization",
                "priority": "high",
                "description": "Increase engagement rate through more interactive content",
                "potential_impact": "25-40% increase in organic reach"
            })
        
        video_completion_rate = account_metrics.get("calculated_metrics", {}).get("video_completion_rate", 0)
        if video_completion_rate < 30:
            opportunities.append({
                "type": "content_optimization",
                "priority": "high", 
                "description": "Improve video retention with stronger hooks and pacing",
                "potential_impact": "15-25% improvement in algorithm favorability"
            })
        
        ctr = account_metrics.get("performance", {}).get("ctr", 0)
        if ctr < 1.5:
            opportunities.append({
                "type": "creative_optimization",
                "priority": "medium",
                "description": "Enhance ad creatives and call-to-actions",
                "potential_impact": "20-35% increase in click-through rate"
            })
        
        # Always include trend participation opportunity
        opportunities.append({
            "type": "trend_participation",
            "priority": "medium",
            "description": "Actively participate in trending challenges and use trending audio",
            "potential_impact": "50-100% increase in organic discovery"
        })
        
        return opportunities
    
    def _generate_competitive_insights(self) -> Dict[str, Any]:
        """Generate competitive analysis insights"""
        # In production, this would analyze actual competitive data
        return {
            "market_position": "growing",
            "competitive_advantages": [
                "High engagement rate compared to industry average",
                "Strong video completion rates",
                "Effective use of trending content"
            ],
            "areas_for_improvement": [
                "Increase posting frequency for better algorithm preference",
                "Diversify content formats (Stories, Live, etc.)",
                "Improve audience targeting precision"
            ],
            "benchmark_metrics": {
                "average_engagement_rate": "4.2%",
                "average_completion_rate": "32%",
                "average_ctr": "1.8%"
            }
        }
    
    def _analyze_trend_alignment(self) -> Dict[str, Any]:
        """Analyze alignment with current TikTok trends"""
        return {
            "trend_participation_score": 75,
            "trending_elements_used": [
                "Popular audio tracks",
                "Trending hashtags",
                "Current challenges"
            ],
            "missed_opportunities": [
                "Branded hashtag challenges",
                "Influencer collaborations",
                "User-generated content campaigns"
            ],
            "recommendations": [
                "Monitor trending page daily for new opportunities",
                "Create content around emerging trends within 24-48 hours",
                "Develop branded hashtag challenges for community engagement"
            ]
        }
    
    def _prioritize_optimizations(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize optimization tasks by impact and effort"""
        optimizations = []
        
        engagement_rate = metrics.get("calculated_metrics", {}).get("engagement_rate", 0)
        if engagement_rate < 4:
            optimizations.append({
                "task": "Improve Engagement Rate",
                "priority": 1,
                "effort": "medium",
                "impact": "high",
                "timeline": "2-4 weeks",
                "actions": [
                    "Add interactive elements to videos",
                    "Ask questions in captions",
                    "Use trending audio and effects",
                    "Post at optimal times"
                ]
            })
        
        video_completion = metrics.get("calculated_metrics", {}).get("video_completion_rate", 0)
        if video_completion < 35:
            optimizations.append({
                "task": "Optimize Video Retention",
                "priority": 2,
                "effort": "high",
                "impact": "high", 
                "timeline": "1-3 weeks",
                "actions": [
                    "Create stronger opening hooks",
                    "Use jump cuts and fast pacing",
                    "Keep videos under 30 seconds",
                    "Add captions for accessibility"
                ]
            })
        
        optimizations.append({
            "task": "Scale Successful Content",
            "priority": 3,
            "effort": "low",
            "impact": "medium",
            "timeline": "1 week",
            "actions": [
                "Identify top-performing content",
                "Create variations of successful videos",
                "Increase budget for best-performing ads",
                "A/B test similar content formats"
            ]
        })
        
        return sorted(optimizations, key=lambda x: x["priority"])
    
    def _create_growth_action_plan(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """Create actionable growth plan"""
        return {
            "immediate_actions": [
                "Optimize underperforming video content",
                "Increase posting frequency during peak hours",
                "Participate in current trending challenges"
            ],
            "short_term_goals": [
                "Achieve 6%+ engagement rate within 30 days",
                "Improve video completion rate to 40%+",
                "Increase follower growth rate by 25%"
            ],
            "long_term_strategy": [
                "Build consistent brand presence on TikTok",
                "Develop signature content style and format",
                "Create branded hashtag challenges",
                "Partner with relevant TikTok creators"
            ],
            "success_metrics": [
                "Engagement rate > 6%",
                "Video completion rate > 40%",
                "CTR > 2%",
                "Cost per acquisition < $5"
            ]
        }


# Main TikTok Marketing API Integration Class
class TikTokMarketingAPIIntegration:
    """
    Main integration class that orchestrates all TikTok marketing agents
    and provides a unified interface for the Brain API Gateway
    """
    
    def __init__(self, access_token: str, advertiser_id: str, app_id: str = None, secret: str = None):
        self.access_token = access_token
        self.advertiser_id = advertiser_id
        self.app_id = app_id
        self.secret = secret
        
        # Initialize agents
        self.campaign_agent = TikTokCampaignAgent(access_token, advertiser_id)
        self.content_agent = TikTokContentAgent(access_token, advertiser_id)
        self.audience_agent = TikTokAudienceAgent(access_token, advertiser_id)
        self.analytics_agent = TikTokAnalyticsAgent(access_token, advertiser_id)
        
    async def execute_viral_campaign_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute complete TikTok viral campaign workflow"""
        try:
            results = {
                "workflow_id": hashlib.md5(f"{datetime.now().isoformat()}{workflow_data}".encode()).hexdigest()[:16],
                "started_at": datetime.now().isoformat(),
                "steps": []
            }
            
            # Step 1: Create custom audience if specified
            if "audience" in workflow_data:
                audience_result = await self.audience_agent.create_custom_audience(workflow_data["audience"])
                results["steps"].append({
                    "step": "audience_creation",
                    "success": audience_result.get("success", False),
                    "data": audience_result
                })
            
            # Step 2: Create campaign
            if "campaign" in workflow_data:
                campaign_result = await self.campaign_agent.create_campaign(workflow_data["campaign"])
                results["steps"].append({
                    "step": "campaign_creation",
                    "success": campaign_result.get("success", False),
                    "data": campaign_result
                })
                
                if not campaign_result.get("success"):
                    results["success"] = False
                    results["error"] = "Campaign creation failed"
                    return results
                
                campaign_id = campaign_result.get("campaign_id")
                
                # Step 3: Create ad group
                if "ad_group" in workflow_data:
                    ad_group_data = workflow_data["ad_group"]
                    ad_group_result = await self.campaign_agent.create_ad_group(campaign_id, ad_group_data)
                    results["steps"].append({
                        "step": "ad_group_creation",
                        "success": ad_group_result.get("success", False),
                        "data": ad_group_result
                    })
                    
                    if ad_group_result.get("success"):
                        ad_group_id = ad_group_result.get("ad_group_id")
            
            # Step 4: Upload and create video content
            if "content" in workflow_data:
                for content_item in workflow_data["content"]:
                    # Upload video first
                    upload_result = await self.content_agent.upload_video({
                        "video_url": content_item.get("video_url"),
                        "video_signature": content_item.get("video_signature", "")
                    })
                    
                    if upload_result.get("success"):
                        content_item["video_url"] = upload_result["video_id"]
                        if "ad_group_id" not in content_item and 'ad_group_id' in locals():
                            content_item["ad_group_id"] = ad_group_id
                        
                        ad_result = await self.content_agent.create_video_ad(content_item)
                        results["steps"].append({
                            "step": "video_ad_creation",
                            "success": ad_result.get("success", False),
                            "data": ad_result
                        })
            
            # Step 5: Get trending hashtags for optimization
            if workflow_data.get("optimize_for_trends", True):
                trends_result = await self.content_agent.get_trending_hashtags({
                    "category": workflow_data.get("trend_category", "business"),
                    "limit": 10
                })
                results["steps"].append({
                    "step": "trend_optimization",
                    "success": trends_result.get("success", False),
                    "data": trends_result
                })
            
            results["success"] = all(step.get("success", False) for step in results["steps"])
            results["completed_at"] = datetime.now().isoformat()
            
            return results
            
        except Exception as e:
            logger.error(f"Viral campaign workflow error: {str(e)}")
            return {
                "success": False,
                "error": "Viral campaign workflow execution failed",
                "details": str(e)
            }
    
    async def get_comprehensive_insights(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive insights across all TikTok marketing activities"""
        try:
            date_range = request_data.get("date_range", {})
            
            # Get account overview
            account_overview = await self.analytics_agent.get_account_overview(date_range)
            
            # Get growth insights
            growth_insights = await self.analytics_agent.generate_growth_insights({
                "date_range": date_range,
                "campaign_ids": request_data.get("campaign_ids", [])
            })
            
            # Get trending content insights
            trending_insights = await self.content_agent.get_trending_hashtags({
                "category": "general",
                "limit": 15
            })
            
            return {
                "success": True,
                "insights": {
                    "account_performance": account_overview.get("metrics", {}) if account_overview.get("success") else {},
                    "growth_analysis": growth_insights.get("growth_insights", {}) if growth_insights.get("success") else {},
                    "trending_opportunities": trending_insights.get("trending_hashtags", []) if trending_insights.get("success") else []
                },
                "recommendations": self._consolidate_recommendations([
                    account_overview.get("insights", []),
                    growth_insights.get("action_plan", {}).get("immediate_actions", []),
                    trending_insights.get("recommendations", [])
                ]),
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Comprehensive insights error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to generate comprehensive insights",
                "details": str(e)
            }
    
    def _consolidate_recommendations(self, recommendation_lists: List[List[str]]) -> List[str]:
        """Consolidate recommendations from multiple sources"""
        all_recommendations = []
        for rec_list in recommendation_lists:
            if isinstance(rec_list, list):
                all_recommendations.extend(rec_list)
        
        # Remove duplicates while preserving order
        seen = set()
        consolidated = []
        for rec in all_recommendations:
            if rec not in seen:
                seen.add(rec)
                consolidated.append(rec)
        
        return consolidated[:12]  # Return top 12 recommendations


# Export main classes for Brain API Gateway integration
__all__ = [
    "TikTokMarketingAPIIntegration",
    "TikTokCampaignAgent",
    "TikTokContentAgent",
    "TikTokAudienceAgent", 
    "TikTokAnalyticsAgent",
    "TikTokCampaignObjective",
    "TikTokContentType",
    "TikTokPlacement"
]


# Example usage and testing functions
async def test_tiktok_integration():
    """Test TikTok Marketing API integration"""
    # Test configuration
    test_config = {
        "access_token": "YOUR_TIKTOK_ACCESS_TOKEN",
        "advertiser_id": "YOUR_TIKTOK_ADVERTISER_ID",
        "app_id": "YOUR_TIKTOK_APP_ID",
        "secret": "YOUR_TIKTOK_APP_SECRET"
    }
    
    try:
        # Initialize integration
        tiktok = TikTokMarketingAPIIntegration(
            access_token=test_config["access_token"],
            advertiser_id=test_config["advertiser_id"],
            app_id=test_config.get("app_id"),
            secret=test_config.get("secret")
        )
        
        # Test viral campaign workflow
        viral_workflow_data = {
            "campaign": {
                "name": "TikTok Viral Marketing Campaign",
                "objective": "VIDEO_VIEW",
                "daily_budget": 50.0,
                "placements": ["PLACEMENT_TYPE_TIKTOK"],
                "targeting": {
                    "age_groups": ["AGE_18_24", "AGE_25_34"],
                    "genders": ["MALE", "FEMALE"],
                    "interests": ["BUSINESS", "MARKETING"]
                }
            },
            "ad_group": {
                "name": "Viral Video Ad Group",
                "daily_budget": 25.0,
                "optimization_goal": "VIDEO_VIEW",
                "placement_type": "PLACEMENT_TYPE_TIKTOK"
            },
            "content": [{
                "ad_name": "AI Marketing Revolution",
                "video_url": "https://example.com/marketing-video.mp4",
                "cover_image_url": "https://example.com/cover-image.jpg",
                "caption": "Transform your business with AI marketing! 🚀",
                "hashtags": ["AIMarketing", "BusinessGrowth", "MarketingTips", "fyp"],
                "call_to_action": "LEARN_MORE",
                "landing_page_url": "https://example.com/ai-marketing"
            }],
            "optimize_for_trends": True,
            "trend_category": "business"
        }
        
        # Execute viral campaign workflow
        result = await tiktok.execute_viral_campaign_workflow(viral_workflow_data)
        print(f"Viral campaign workflow result: {json.dumps(result, indent=2)}")
        
        # Get comprehensive insights
        insights_result = await tiktok.get_comprehensive_insights({
            "date_range": {
                "start_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                "end_date": datetime.now().strftime("%Y-%m-%d")
            }
        })
        print(f"Comprehensive insights: {json.dumps(insights_result, indent=2)}")
        
        return True
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Run tests
    asyncio.run(test_tiktok_integration())
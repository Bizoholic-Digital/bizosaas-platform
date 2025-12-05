"""
Instagram Marketing API Integration for BizOSaaS Brain

This module provides comprehensive Instagram marketing automation capabilities through 
specialized AI agents for visual content marketing, influencer campaigns, and engagement tracking.

Architecture:
- InstagramCampaignAgent: Campaign creation and management via Facebook Marketing API
- InstagramContentAgent: Visual content creation, posting, and Stories management
- InstagramEngagementAgent: Audience engagement, comments, and community management
- InstagramAnalyticsAgent: Performance tracking, insights, and growth analytics

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


class InstagramCampaignObjective(Enum):
    """Instagram campaign objectives"""
    BRAND_AWARENESS = "BRAND_AWARENESS"
    REACH = "REACH"
    TRAFFIC = "LINK_CLICKS"
    ENGAGEMENT = "ENGAGEMENT"
    APP_INSTALLS = "APP_INSTALLS"
    VIDEO_VIEWS = "VIDEO_VIEWS"
    LEAD_GENERATION = "LEAD_GENERATION"
    CONVERSIONS = "CONVERSIONS"


class InstagramContentType(Enum):
    """Instagram content types"""
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    CAROUSEL = "CAROUSEL_ALBUM_AD"
    STORY = "STORY"
    REELS = "REELS"


class InstagramAudienceType(Enum):
    """Instagram audience targeting types"""
    DEMOGRAPHICS = "demographics"
    INTERESTS = "interests"
    BEHAVIORS = "behaviors"
    CUSTOM_AUDIENCES = "custom_audiences"
    LOOKALIKE_AUDIENCES = "lookalike_audiences"


class InstagramPlacement(Enum):
    """Instagram ad placements"""
    FEED = "instagram_feed"
    STORIES = "instagram_stories"
    REELS = "instagram_reels"
    EXPLORE = "instagram_explore"


@dataclass
class InstagramCampaignConfig:
    """Configuration for Instagram campaigns"""
    name: str
    objective: InstagramCampaignObjective
    daily_budget: float
    placements: List[InstagramPlacement]
    targeting: Dict[str, Any] = None
    bid_strategy: str = "LOWEST_COST_WITHOUT_CAP"
    optimization_goal: str = "LINK_CLICKS"
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    
    def to_api_format(self) -> Dict[str, Any]:
        """Convert to Instagram/Facebook API format"""
        config = {
            "name": self.name,
            "objective": self.objective.value,
            "status": "PAUSED",  # Always create paused for review
            "daily_budget": int(self.daily_budget * 100),  # Facebook API uses cents
            "bid_strategy": self.bid_strategy,
            "optimization_goal": self.optimization_goal,
            "publisher_platforms": ["instagram"],
            "instagram_positions": [p.value for p in self.placements]
        }
        
        if self.targeting:
            config["targeting"] = self.targeting
            
        if self.start_time:
            config["start_time"] = self.start_time
            
        if self.end_time:
            config["end_time"] = self.end_time
            
        return config


@dataclass
class InstagramContent:
    """Instagram content configuration"""
    caption: str
    media_type: InstagramContentType
    media_url: str
    hashtags: List[str] = None
    mentions: List[str] = None
    location: Dict[str, Any] = None
    call_to_action: str = "Learn More"
    link_url: Optional[str] = None
    
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
            formatted_caption += f"\n\n{hashtag_text}"
            
        return formatted_caption
    
    def to_api_format(self) -> Dict[str, Any]:
        """Convert to Instagram Graph API format"""
        return {
            "caption": self.format_caption(),
            "media_type": self.media_type.value,
            "media_url": self.media_url,
            "location": self.location,
            "call_to_action": self.call_to_action,
            "link": self.link_url
        }


@dataclass
class InstagramInsight:
    """Instagram analytics insight data"""
    metric_name: str
    metric_value: Union[int, float]
    period: str
    date_range: Dict[str, str]
    breakdown: Optional[Dict[str, Any]] = None


class InstagramAPIClient:
    """Base Instagram API client with authentication and rate limiting"""
    
    def __init__(self, access_token: str, instagram_account_id: str = None, facebook_page_id: str = None):
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id
        self.facebook_page_id = facebook_page_id
        self.base_url = "https://graph.facebook.com/v19.0"
        self.session = None
        self.rate_limit_remaining = 200
        self.rate_limit_reset = datetime.now()
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            },
            timeout=aiohttp.ClientTimeout(total=60)  # Longer timeout for media uploads
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
            
    async def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None, files: Dict = None) -> Dict[str, Any]:
        """Make authenticated request to Instagram/Facebook API"""
        if not self.session:
            raise RuntimeError("Client not initialized. Use async context manager.")
            
        # Check rate limits
        if self.rate_limit_remaining <= 10 and datetime.now() < self.rate_limit_reset:
            wait_time = (self.rate_limit_reset - datetime.now()).total_seconds()
            logger.warning(f"Rate limit approaching. Waiting {wait_time:.1f}s")
            await asyncio.sleep(wait_time)
            
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Add access token to params
        if not params:
            params = {}
        params["access_token"] = self.access_token
        
        try:
            # Handle file uploads differently
            if files:
                # For file uploads, we need FormData
                form_data = aiohttp.FormData()
                if data:
                    for key, value in data.items():
                        form_data.add_field(key, str(value))
                for key, file_info in files.items():
                    form_data.add_field(key, file_info["content"], filename=file_info["filename"], content_type=file_info["content_type"])
                
                async with self.session.request(method, url, data=form_data, params=params) as response:
                    response_data = await self._process_response(response)
            else:
                # Regular JSON requests
                async with self.session.request(method, url, json=data, params=params) as response:
                    response_data = await self._process_response(response)
            
            return response_data
            
        except aiohttp.ClientError as e:
            logger.error(f"Instagram API request failed: {str(e)}")
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
    
    async def _process_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Process API response"""
        # Update rate limit info from headers
        self.rate_limit_remaining = int(response.headers.get("X-Business-Use-Case-Usage", "200"))
        
        try:
            response_data = await response.json()
        except:
            response_data = await response.text()
        
        if response.status >= 400:
            logger.error(f"Instagram API error {response.status}: {response_data}")
            return {
                "success": False,
                "error": f"API error {response.status}",
                "details": response_data,
                "status_code": response.status
            }
            
        logger.info(f"Instagram API {response.status}: Success")
        return {
            "success": True,
            "data": response_data,
            "status_code": response.status
        }


class InstagramCampaignAgent:
    """AI agent for Instagram campaign management via Facebook Marketing API"""
    
    def __init__(self, access_token: str, ad_account_id: str, instagram_account_id: str):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.instagram_account_id = instagram_account_id
        self.client = InstagramAPIClient(access_token, instagram_account_id)
        
    async def create_campaign(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Instagram campaign"""
        try:
            config = InstagramCampaignConfig(
                name=request_data.get("name", "New Instagram Campaign"),
                objective=InstagramCampaignObjective(request_data.get("objective", "TRAFFIC")),
                daily_budget=float(request_data.get("daily_budget", 20.0)),
                placements=[InstagramPlacement(p) for p in request_data.get("placements", ["instagram_feed"])],
                targeting=request_data.get("targeting", {}),
                bid_strategy=request_data.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP"),
                optimization_goal=request_data.get("optimization_goal", "LINK_CLICKS")
            )
            
            async with self.client as client:
                # Create campaign
                campaign_data = config.to_api_format()
                
                response = await client._make_request(
                    "POST", 
                    f"act_{self.ad_account_id}/campaigns",
                    data=campaign_data
                )
                
                if response.get("success"):
                    campaign_id = response["data"]["id"]
                    
                    # Get campaign details
                    details = await self.get_campaign_details(campaign_id)
                    
                    return {
                        "success": True,
                        "campaign_id": campaign_id,
                        "details": details,
                        "message": "Instagram campaign created successfully"
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
        async with self.client as client:
            response = await client._make_request(
                "GET", 
                campaign_id,
                params={"fields": "id,name,objective,status,daily_budget,created_time,updated_time"}
            )
            
            if response.get("success"):
                return response["data"]
            
            return {"error": "Failed to fetch campaign details"}
    
    async def create_ad_set(self, campaign_id: str, ad_set_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create ad set for Instagram campaign"""
        try:
            ad_set_config = {
                "name": ad_set_data.get("name", "Instagram Ad Set"),
                "campaign_id": campaign_id,
                "daily_budget": int(float(ad_set_data.get("daily_budget", 10.0)) * 100),
                "bid_strategy": ad_set_data.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP"),
                "optimization_goal": ad_set_data.get("optimization_goal", "LINK_CLICKS"),
                "billing_event": ad_set_data.get("billing_event", "IMPRESSIONS"),
                "status": "PAUSED",
                "targeting": ad_set_data.get("targeting", {}),
                "promoted_object": {
                    "page_id": self.instagram_account_id
                },
                "instagram_actor_id": self.instagram_account_id
            }
            
            async with self.client as client:
                response = await client._make_request(
                    "POST",
                    f"act_{self.ad_account_id}/adsets", 
                    data=ad_set_config
                )
                
                if response.get("success"):
                    return {
                        "success": True,
                        "ad_set_id": response["data"]["id"],
                        "campaign_id": campaign_id,
                        "message": "Ad set created successfully"
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Ad set creation error: {str(e)}")
            return {
                "success": False,
                "error": "Ad set creation failed",
                "details": str(e)
            }
    
    async def get_campaign_performance(self, campaign_id: str, date_range: Dict[str, str]) -> Dict[str, Any]:
        """Get Instagram campaign performance metrics"""
        try:
            params = {
                "fields": "campaign_id,impressions,clicks,spend,actions,cpc,cpm,ctr,reach,frequency",
                "time_range": {
                    "since": date_range.get("start_date"),
                    "until": date_range.get("end_date")
                },
                "level": "campaign"
            }
            
            async with self.client as client:
                response = await client._make_request(
                    "GET",
                    f"{campaign_id}/insights",
                    params=params
                )
                
                if response.get("success") and response["data"].get("data"):
                    insights = response["data"]["data"][0]
                    
                    # Parse actions for conversions
                    conversions = 0
                    if "actions" in insights:
                        for action in insights["actions"]:
                            if action.get("action_type") in ["purchase", "lead", "complete_registration"]:
                                conversions += int(action.get("value", 0))
                    
                    return {
                        "success": True,
                        "campaign_id": campaign_id,
                        "metrics": {
                            "impressions": int(insights.get("impressions", 0)),
                            "clicks": int(insights.get("clicks", 0)),
                            "spend": float(insights.get("spend", 0)),
                            "reach": int(insights.get("reach", 0)),
                            "frequency": float(insights.get("frequency", 0)),
                            "cpc": float(insights.get("cpc", 0)),
                            "cpm": float(insights.get("cpm", 0)),
                            "ctr": float(insights.get("ctr", 0)),
                            "conversions": conversions
                        },
                        "date_range": date_range
                    }
                
                return {
                    "success": False,
                    "error": "No insights data available",
                    "campaign_id": campaign_id
                }
                
        except Exception as e:
            logger.error(f"Performance tracking error: {str(e)}")
            return {
                "success": False,
                "error": "Performance tracking failed",
                "details": str(e)
            }


class InstagramContentAgent:
    """AI agent for Instagram content creation and publishing"""
    
    def __init__(self, access_token: str, instagram_account_id: str, facebook_page_id: str = None):
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id
        self.facebook_page_id = facebook_page_id
        self.client = InstagramAPIClient(access_token, instagram_account_id, facebook_page_id)
        
    async def create_media_post(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Instagram media post (image or video)"""
        try:
            content = InstagramContent(
                caption=request_data.get("caption", ""),
                media_type=InstagramContentType(request_data.get("media_type", "IMAGE")),
                media_url=request_data.get("media_url", ""),
                hashtags=request_data.get("hashtags", []),
                mentions=request_data.get("mentions", []),
                location=request_data.get("location"),
                call_to_action=request_data.get("call_to_action", "Learn More"),
                link_url=request_data.get("link_url")
            )
            
            async with self.client as client:
                # Step 1: Create media object
                media_data = {
                    "image_url" if content.media_type == InstagramContentType.IMAGE else "video_url": content.media_url,
                    "caption": content.format_caption(),
                    "media_type": content.media_type.value
                }
                
                if content.location:
                    media_data["location_id"] = content.location.get("id")
                
                create_response = await client._make_request(
                    "POST",
                    f"{self.instagram_account_id}/media",
                    data=media_data
                )
                
                if not create_response.get("success"):
                    return create_response
                
                media_id = create_response["data"]["id"]
                
                # Step 2: Publish media
                publish_response = await client._make_request(
                    "POST",
                    f"{self.instagram_account_id}/media_publish",
                    data={"creation_id": media_id}
                )
                
                if publish_response.get("success"):
                    post_id = publish_response["data"]["id"]
                    
                    return {
                        "success": True,
                        "post_id": post_id,
                        "media_id": media_id,
                        "content": asdict(content),
                        "message": "Instagram post published successfully"
                    }
                
                return publish_response
                
        except Exception as e:
            logger.error(f"Content creation error: {str(e)}")
            return {
                "success": False,
                "error": "Content creation failed",
                "details": str(e)
            }
    
    async def create_carousel_post(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Instagram carousel post with multiple media items"""
        try:
            media_items = request_data.get("media_items", [])
            caption = request_data.get("caption", "")
            hashtags = request_data.get("hashtags", [])
            
            if len(media_items) < 2:
                return {
                    "success": False,
                    "error": "Carousel requires at least 2 media items"
                }
            
            async with self.client as client:
                # Step 1: Create media objects for each item
                media_ids = []
                for item in media_items:
                    media_data = {
                        "image_url" if item.get("type", "image") == "image" else "video_url": item.get("url"),
                        "media_type": "IMAGE" if item.get("type", "image") == "image" else "VIDEO",
                        "is_carousel_item": True
                    }
                    
                    media_response = await client._make_request(
                        "POST",
                        f"{self.instagram_account_id}/media",
                        data=media_data
                    )
                    
                    if media_response.get("success"):
                        media_ids.append(media_response["data"]["id"])
                    else:
                        return {
                            "success": False,
                            "error": f"Failed to create media item: {media_response.get('error')}"
                        }
                
                # Step 2: Create carousel container
                formatted_caption = caption
                if hashtags:
                    hashtag_text = " ".join([f"#{tag.lstrip('#')}" for tag in hashtags])
                    formatted_caption += f"\n\n{hashtag_text}"
                
                carousel_data = {
                    "media_type": "CAROUSEL",
                    "children": ",".join(media_ids),
                    "caption": formatted_caption
                }
                
                carousel_response = await client._make_request(
                    "POST",
                    f"{self.instagram_account_id}/media",
                    data=carousel_data
                )
                
                if not carousel_response.get("success"):
                    return carousel_response
                
                carousel_id = carousel_response["data"]["id"]
                
                # Step 3: Publish carousel
                publish_response = await client._make_request(
                    "POST",
                    f"{self.instagram_account_id}/media_publish",
                    data={"creation_id": carousel_id}
                )
                
                if publish_response.get("success"):
                    return {
                        "success": True,
                        "post_id": publish_response["data"]["id"],
                        "carousel_id": carousel_id,
                        "media_count": len(media_ids),
                        "message": "Instagram carousel published successfully"
                    }
                
                return publish_response
                
        except Exception as e:
            logger.error(f"Carousel creation error: {str(e)}")
            return {
                "success": False,
                "error": "Carousel creation failed",
                "details": str(e)
            }
    
    async def create_story(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Instagram Story"""
        try:
            media_url = request_data.get("media_url", "")
            media_type = request_data.get("media_type", "IMAGE")
            
            if not media_url:
                return {
                    "success": False,
                    "error": "Media URL is required for Stories"
                }
            
            async with self.client as client:
                story_data = {
                    "image_url" if media_type == "IMAGE" else "video_url": media_url,
                    "media_type": media_type
                }
                
                response = await client._make_request(
                    "POST",
                    f"{self.instagram_account_id}/media",
                    data=story_data
                )
                
                if response.get("success"):
                    story_id = response["data"]["id"]
                    
                    # Publish story
                    publish_response = await client._make_request(
                        "POST",
                        f"{self.instagram_account_id}/media_publish",
                        data={"creation_id": story_id}
                    )
                    
                    if publish_response.get("success"):
                        return {
                            "success": True,
                            "story_id": publish_response["data"]["id"],
                            "media_type": media_type,
                            "message": "Instagram Story published successfully"
                        }
                    
                    return publish_response
                
                return response
                
        except Exception as e:
            logger.error(f"Story creation error: {str(e)}")
            return {
                "success": False,
                "error": "Story creation failed",
                "details": str(e)
            }
    
    async def get_media_insights(self, media_id: str) -> Dict[str, Any]:
        """Get insights for specific media post"""
        try:
            async with self.client as client:
                response = await client._make_request(
                    "GET",
                    f"{media_id}/insights",
                    params={
                        "metric": "impressions,reach,likes,comments,shares,saves,profile_visits,website_clicks"
                    }
                )
                
                if response.get("success"):
                    insights_data = response["data"]["data"]
                    
                    # Convert to more readable format
                    metrics = {}
                    for insight in insights_data:
                        metrics[insight["name"]] = insight["values"][0]["value"]
                    
                    return {
                        "success": True,
                        "media_id": media_id,
                        "metrics": metrics,
                        "engagement_rate": self._calculate_engagement_rate(metrics)
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Media insights error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to get media insights",
                "details": str(e)
            }
    
    def _calculate_engagement_rate(self, metrics: Dict[str, Any]) -> float:
        """Calculate engagement rate for a post"""
        impressions = metrics.get("impressions", 1)
        likes = metrics.get("likes", 0)
        comments = metrics.get("comments", 0)
        shares = metrics.get("shares", 0)
        saves = metrics.get("saves", 0)
        
        total_engagement = likes + comments + shares + saves
        return (total_engagement / impressions) * 100 if impressions > 0 else 0


class InstagramEngagementAgent:
    """AI agent for Instagram audience engagement and community management"""
    
    def __init__(self, access_token: str, instagram_account_id: str):
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id
        self.client = InstagramAPIClient(access_token, instagram_account_id)
        
    async def get_comments(self, media_id: str) -> Dict[str, Any]:
        """Get comments for a specific media post"""
        try:
            async with self.client as client:
                response = await client._make_request(
                    "GET",
                    f"{media_id}/comments",
                    params={
                        "fields": "id,text,username,timestamp,like_count,replies"
                    }
                )
                
                if response.get("success"):
                    comments = response["data"]["data"]
                    
                    return {
                        "success": True,
                        "media_id": media_id,
                        "comment_count": len(comments),
                        "comments": comments,
                        "top_comments": sorted(comments, key=lambda x: x.get("like_count", 0), reverse=True)[:5]
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Comments retrieval error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to get comments",
                "details": str(e)
            }
    
    async def reply_to_comment(self, comment_id: str, reply_text: str) -> Dict[str, Any]:
        """Reply to a comment"""
        try:
            async with self.client as client:
                response = await client._make_request(
                    "POST",
                    f"{comment_id}/replies",
                    data={"message": reply_text}
                )
                
                if response.get("success"):
                    return {
                        "success": True,
                        "reply_id": response["data"]["id"],
                        "comment_id": comment_id,
                        "reply_text": reply_text,
                        "message": "Reply posted successfully"
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Comment reply error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to reply to comment",
                "details": str(e)
            }
    
    async def moderate_comments(self, media_id: str, moderation_rules: Dict[str, Any]) -> Dict[str, Any]:
        """Moderate comments based on rules"""
        try:
            # Get comments first
            comments_result = await self.get_comments(media_id)
            
            if not comments_result.get("success"):
                return comments_result
            
            comments = comments_result["comments"]
            moderation_actions = []
            
            # Define spam/inappropriate keywords
            spam_keywords = moderation_rules.get("spam_keywords", [
                "buy now", "click here", "follow for follow", "f4f", "l4l"
            ])
            inappropriate_keywords = moderation_rules.get("inappropriate_keywords", [])
            
            for comment in comments:
                comment_text = comment.get("text", "").lower()
                action_needed = False
                action_type = None
                
                # Check for spam
                if any(keyword.lower() in comment_text for keyword in spam_keywords):
                    action_needed = True
                    action_type = "spam"
                
                # Check for inappropriate content
                if any(keyword.lower() in comment_text for keyword in inappropriate_keywords):
                    action_needed = True
                    action_type = "inappropriate"
                
                if action_needed:
                    moderation_actions.append({
                        "comment_id": comment["id"],
                        "username": comment.get("username"),
                        "text": comment.get("text"),
                        "action_type": action_type,
                        "recommended_action": "hide" if moderation_rules.get("auto_moderate") else "review"
                    })
            
            return {
                "success": True,
                "media_id": media_id,
                "total_comments": len(comments),
                "flagged_comments": len(moderation_actions),
                "moderation_actions": moderation_actions,
                "message": f"Comment moderation completed. {len(moderation_actions)} comments flagged."
            }
            
        except Exception as e:
            logger.error(f"Comment moderation error: {str(e)}")
            return {
                "success": False,
                "error": "Comment moderation failed",
                "details": str(e)
            }
    
    async def analyze_audience_engagement(self, date_range: Dict[str, str]) -> Dict[str, Any]:
        """Analyze audience engagement patterns"""
        try:
            async with self.client as client:
                # Get recent media posts
                media_response = await client._make_request(
                    "GET",
                    f"{self.instagram_account_id}/media",
                    params={
                        "fields": "id,media_type,timestamp,caption,like_count,comments_count",
                        "since": date_range.get("start_date"),
                        "until": date_range.get("end_date"),
                        "limit": 50
                    }
                )
                
                if not media_response.get("success"):
                    return media_response
                
                media_posts = media_response["data"]["data"]
                
                # Analyze engagement patterns
                engagement_analysis = {
                    "total_posts": len(media_posts),
                    "total_likes": sum(post.get("like_count", 0) for post in media_posts),
                    "total_comments": sum(post.get("comments_count", 0) for post in media_posts),
                    "average_likes": 0,
                    "average_comments": 0,
                    "best_performing_post": None,
                    "engagement_by_type": {},
                    "posting_patterns": {}
                }
                
                if len(media_posts) > 0:
                    engagement_analysis["average_likes"] = engagement_analysis["total_likes"] / len(media_posts)
                    engagement_analysis["average_comments"] = engagement_analysis["total_comments"] / len(media_posts)
                    
                    # Find best performing post
                    best_post = max(media_posts, key=lambda x: x.get("like_count", 0) + x.get("comments_count", 0))
                    engagement_analysis["best_performing_post"] = {
                        "id": best_post.get("id"),
                        "likes": best_post.get("like_count", 0),
                        "comments": best_post.get("comments_count", 0),
                        "media_type": best_post.get("media_type"),
                        "caption_preview": best_post.get("caption", "")[:100] + "..." if best_post.get("caption") else ""
                    }
                    
                    # Analyze by media type
                    type_stats = {}
                    for post in media_posts:
                        media_type = post.get("media_type", "UNKNOWN")
                        if media_type not in type_stats:
                            type_stats[media_type] = {"count": 0, "total_likes": 0, "total_comments": 0}
                        
                        type_stats[media_type]["count"] += 1
                        type_stats[media_type]["total_likes"] += post.get("like_count", 0)
                        type_stats[media_type]["total_comments"] += post.get("comments_count", 0)
                    
                    # Calculate averages by type
                    for media_type, stats in type_stats.items():
                        engagement_analysis["engagement_by_type"][media_type] = {
                            "post_count": stats["count"],
                            "avg_likes": stats["total_likes"] / stats["count"],
                            "avg_comments": stats["total_comments"] / stats["count"],
                            "total_engagement": stats["total_likes"] + stats["total_comments"]
                        }
                
                return {
                    "success": True,
                    "date_range": date_range,
                    "engagement_analysis": engagement_analysis,
                    "recommendations": self._generate_engagement_recommendations(engagement_analysis)
                }
                
        except Exception as e:
            logger.error(f"Engagement analysis error: {str(e)}")
            return {
                "success": False,
                "error": "Engagement analysis failed",
                "details": str(e)
            }
    
    def _generate_engagement_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on engagement analysis"""
        recommendations = []
        
        avg_likes = analysis.get("average_likes", 0)
        avg_comments = analysis.get("average_comments", 0)
        
        if avg_likes < 100:
            recommendations.append("Focus on creating more engaging visual content to increase likes")
        
        if avg_comments < 10:
            recommendations.append("Add more call-to-action questions in captions to encourage comments")
        
        # Analyze performance by content type
        engagement_by_type = analysis.get("engagement_by_type", {})
        if engagement_by_type:
            best_type = max(engagement_by_type.items(), key=lambda x: x[1]["total_engagement"])
            recommendations.append(f"Focus more on {best_type[0]} content - it performs best with your audience")
        
        recommendations.extend([
            "Post consistently during peak engagement hours (typically 6-9 PM)",
            "Use relevant hashtags to increase discoverability",
            "Engage with your community by responding to comments promptly",
            "Consider Instagram Stories and Reels for higher reach",
            "Collaborate with micro-influencers in your niche"
        ])
        
        return recommendations


class InstagramAnalyticsAgent:
    """AI agent for Instagram marketing analytics and insights"""
    
    def __init__(self, access_token: str, instagram_account_id: str):
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id
        self.client = InstagramAPIClient(access_token, instagram_account_id)
        
    async def get_account_insights(self, date_range: Dict[str, str]) -> Dict[str, Any]:
        """Get comprehensive Instagram account insights"""
        try:
            metrics = [
                "impressions", "reach", "profile_views", "website_clicks",
                "follower_count", "email_contacts", "phone_call_clicks",
                "text_message_clicks", "get_directions_clicks"
            ]
            
            params = {
                "metric": ",".join(metrics),
                "period": "day",
                "since": date_range.get("start_date"),
                "until": date_range.get("end_date")
            }
            
            async with self.client as client:
                response = await client._make_request(
                    "GET",
                    f"{self.instagram_account_id}/insights",
                    params=params
                )
                
                if response.get("success"):
                    insights_data = response["data"]["data"]
                    
                    # Process insights into readable format
                    processed_insights = {}
                    for insight in insights_data:
                        metric_name = insight["name"]
                        values = insight["values"]
                        
                        # Sum up values for the period
                        total_value = sum(value.get("value", 0) for value in values)
                        processed_insights[metric_name] = total_value
                    
                    # Calculate additional metrics
                    impressions = processed_insights.get("impressions", 0)
                    reach = processed_insights.get("reach", 0)
                    profile_views = processed_insights.get("profile_views", 0)
                    
                    calculated_metrics = {
                        "engagement_rate": (profile_views / impressions) * 100 if impressions > 0 else 0,
                        "reach_rate": (reach / impressions) * 100 if impressions > 0 else 0,
                        "profile_conversion_rate": (profile_views / reach) * 100 if reach > 0 else 0
                    }
                    
                    return {
                        "success": True,
                        "account_id": self.instagram_account_id,
                        "date_range": date_range,
                        "metrics": processed_insights,
                        "calculated_metrics": calculated_metrics,
                        "insights": self._generate_account_insights(processed_insights, calculated_metrics)
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Account insights error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to get account insights",
                "details": str(e)
            }
    
    async def get_audience_demographics(self) -> Dict[str, Any]:
        """Get audience demographic insights"""
        try:
            demographic_metrics = [
                "audience_gender_age", "audience_locale", "audience_country",
                "audience_city", "online_followers"
            ]
            
            async with self.client as client:
                response = await client._make_request(
                    "GET",
                    f"{self.instagram_account_id}/insights",
                    params={
                        "metric": ",".join(demographic_metrics),
                        "period": "lifetime"
                    }
                )
                
                if response.get("success"):
                    insights_data = response["data"]["data"]
                    
                    demographics = {}
                    for insight in insights_data:
                        metric_name = insight["name"]
                        values = insight["values"][0]["value"] if insight["values"] else {}
                        demographics[metric_name] = values
                    
                    return {
                        "success": True,
                        "account_id": self.instagram_account_id,
                        "demographics": demographics,
                        "audience_summary": self._summarize_audience_demographics(demographics)
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Demographics analysis error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to get audience demographics",
                "details": str(e)
            }
    
    async def generate_content_performance_report(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive content performance report"""
        try:
            date_range = request_data.get("date_range", {})
            limit = request_data.get("limit", 25)
            
            async with self.client as client:
                # Get media posts
                media_response = await client._make_request(
                    "GET",
                    f"{self.instagram_account_id}/media",
                    params={
                        "fields": "id,media_type,media_url,permalink,timestamp,caption,like_count,comments_count",
                        "since": date_range.get("start_date"),
                        "until": date_range.get("end_date"),
                        "limit": limit
                    }
                )
                
                if not media_response.get("success"):
                    return media_response
                
                media_posts = media_response["data"]["data"]
                
                # Get insights for each post
                content_performance = []
                for post in media_posts:
                    post_insights = await self._get_post_insights(post["id"])
                    
                    performance_data = {
                        "post_id": post["id"],
                        "media_type": post.get("media_type"),
                        "timestamp": post.get("timestamp"),
                        "permalink": post.get("permalink"),
                        "caption_preview": post.get("caption", "")[:100] + "..." if post.get("caption") else "",
                        "likes": post.get("like_count", 0),
                        "comments": post.get("comments_count", 0),
                        "insights": post_insights
                    }
                    
                    content_performance.append(performance_data)
                
                # Sort by total engagement
                content_performance.sort(
                    key=lambda x: x["likes"] + x["comments"] + x["insights"].get("reach", 0),
                    reverse=True
                )
                
                # Generate report summary
                report_summary = self._generate_content_report_summary(content_performance)
                
                return {
                    "success": True,
                    "report_id": hashlib.md5(f"{datetime.now().isoformat()}{self.instagram_account_id}".encode()).hexdigest()[:16],
                    "generated_at": datetime.now().isoformat(),
                    "date_range": date_range,
                    "total_posts": len(content_performance),
                    "content_performance": content_performance,
                    "summary": report_summary,
                    "recommendations": self._generate_content_recommendations(content_performance, report_summary)
                }
                
        except Exception as e:
            logger.error(f"Content report generation error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to generate content performance report",
                "details": str(e)
            }
    
    async def _get_post_insights(self, post_id: str) -> Dict[str, Any]:
        """Get insights for a specific post"""
        try:
            async with self.client as client:
                response = await client._make_request(
                    "GET",
                    f"{post_id}/insights",
                    params={
                        "metric": "impressions,reach,engagement,saved,video_views,profile_visits"
                    }
                )
                
                if response.get("success"):
                    insights_data = response["data"]["data"]
                    
                    insights = {}
                    for insight in insights_data:
                        insights[insight["name"]] = insight["values"][0]["value"]
                    
                    return insights
                
                return {}
                
        except Exception as e:
            logger.error(f"Post insights error for {post_id}: {str(e)}")
            return {}
    
    def _generate_account_insights(self, metrics: Dict[str, Any], calculated_metrics: Dict[str, Any]) -> List[str]:
        """Generate insights from account metrics"""
        insights = []
        
        impressions = metrics.get("impressions", 0)
        reach = metrics.get("reach", 0)
        profile_views = metrics.get("profile_views", 0)
        
        if reach / impressions > 0.3 if impressions > 0 else False:
            insights.append("Excellent reach rate! Your content is being seen by a wide audience.")
        elif reach / impressions < 0.1 if impressions > 0 else False:
            insights.append("Low reach rate. Consider using more relevant hashtags and posting at optimal times.")
        
        if calculated_metrics.get("profile_conversion_rate", 0) > 5:
            insights.append("High profile conversion rate indicates strong content quality.")
        elif calculated_metrics.get("profile_conversion_rate", 0) < 2:
            insights.append("Consider optimizing your profile bio and highlight stories to increase profile engagement.")
        
        website_clicks = metrics.get("website_clicks", 0)
        if website_clicks > 0:
            insights.append(f"Generated {website_clicks} website clicks - good conversion to external traffic.")
        else:
            insights.append("No website clicks recorded. Consider adding clear call-to-actions in your content.")
        
        return insights
    
    def _summarize_audience_demographics(self, demographics: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize audience demographic data"""
        summary = {}
        
        # Gender and age breakdown
        gender_age = demographics.get("audience_gender_age", {})
        if gender_age:
            summary["primary_demographic"] = max(gender_age.items(), key=lambda x: x[1])[0] if gender_age else "Unknown"
        
        # Top locations
        countries = demographics.get("audience_country", {})
        if countries:
            summary["top_country"] = max(countries.items(), key=lambda x: x[1])[0] if countries else "Unknown"
        
        cities = demographics.get("audience_city", {})
        if cities:
            summary["top_city"] = max(cities.items(), key=lambda x: x[1])[0] if cities else "Unknown"
        
        return summary
    
    def _generate_content_report_summary(self, content_performance: List[Dict]) -> Dict[str, Any]:
        """Generate summary from content performance data"""
        if not content_performance:
            return {}
        
        total_likes = sum(post["likes"] for post in content_performance)
        total_comments = sum(post["comments"] for post in content_performance)
        total_posts = len(content_performance)
        
        # Best performing content
        best_post = content_performance[0] if content_performance else {}
        
        # Content type analysis
        type_performance = {}
        for post in content_performance:
            media_type = post.get("media_type", "UNKNOWN")
            if media_type not in type_performance:
                type_performance[media_type] = {"count": 0, "total_engagement": 0}
            
            type_performance[media_type]["count"] += 1
            type_performance[media_type]["total_engagement"] += post["likes"] + post["comments"]
        
        return {
            "total_engagement": total_likes + total_comments,
            "average_likes_per_post": total_likes / total_posts if total_posts > 0 else 0,
            "average_comments_per_post": total_comments / total_posts if total_posts > 0 else 0,
            "best_performing_post": {
                "post_id": best_post.get("post_id"),
                "total_engagement": best_post.get("likes", 0) + best_post.get("comments", 0),
                "media_type": best_post.get("media_type")
            },
            "content_type_performance": type_performance
        }
    
    def _generate_content_recommendations(self, content_performance: List[Dict], summary: Dict[str, Any]) -> List[str]:
        """Generate content strategy recommendations"""
        recommendations = []
        
        # Analyze best performing content type
        type_performance = summary.get("content_type_performance", {})
        if type_performance:
            best_type = max(type_performance.items(), key=lambda x: x[1]["total_engagement"] / x[1]["count"])
            recommendations.append(f"Focus more on {best_type[0]} content - it generates highest engagement per post")
        
        avg_comments = summary.get("average_comments_per_post", 0)
        if avg_comments < 5:
            recommendations.append("Increase community engagement by asking questions in your captions")
        
        # Analyze top performing posts for patterns
        top_posts = content_performance[:5]
        if top_posts:
            recommendations.append("Analyze your top 5 performing posts to identify successful content patterns")
        
        recommendations.extend([
            "Maintain consistent posting schedule for better algorithm performance",
            "Use Instagram Stories and Reels to increase reach and engagement",
            "Collaborate with relevant accounts in your niche",
            "Optimize posting times based on when your audience is most active",
            "Create content pillars to maintain variety while staying on-brand"
        ])
        
        return recommendations


# Main Instagram Marketing API Integration Class
class InstagramMarketingAPIIntegration:
    """
    Main integration class that orchestrates all Instagram marketing agents
    and provides a unified interface for the Brain API Gateway
    """
    
    def __init__(self, access_token: str, instagram_account_id: str, ad_account_id: str = None, facebook_page_id: str = None):
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id
        self.ad_account_id = ad_account_id
        self.facebook_page_id = facebook_page_id
        
        # Initialize agents
        self.campaign_agent = InstagramCampaignAgent(access_token, ad_account_id, instagram_account_id) if ad_account_id else None
        self.content_agent = InstagramContentAgent(access_token, instagram_account_id, facebook_page_id)
        self.engagement_agent = InstagramEngagementAgent(access_token, instagram_account_id)
        self.analytics_agent = InstagramAnalyticsAgent(access_token, instagram_account_id)
        
    async def execute_content_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute complete Instagram content workflow"""
        try:
            results = {
                "workflow_id": hashlib.md5(f"{datetime.now().isoformat()}{workflow_data}".encode()).hexdigest()[:16],
                "started_at": datetime.now().isoformat(),
                "steps": []
            }
            
            # Step 1: Create content posts
            if "posts" in workflow_data:
                for post_data in workflow_data["posts"]:
                    if post_data.get("type") == "carousel":
                        post_result = await self.content_agent.create_carousel_post(post_data)
                    elif post_data.get("type") == "story":
                        post_result = await self.content_agent.create_story(post_data)
                    else:
                        post_result = await self.content_agent.create_media_post(post_data)
                    
                    results["steps"].append({
                        "step": "content_creation",
                        "post_type": post_data.get("type", "media"),
                        "success": post_result.get("success", False),
                        "data": post_result
                    })
            
            # Step 2: Schedule engagement monitoring
            if workflow_data.get("enable_engagement_tracking", True):
                engagement_result = await self.engagement_agent.analyze_audience_engagement({
                    "start_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
                    "end_date": datetime.now().strftime("%Y-%m-%d")
                })
                
                results["steps"].append({
                    "step": "engagement_analysis",
                    "success": engagement_result.get("success", False),
                    "data": engagement_result
                })
            
            # Step 3: Generate insights if requested
            if workflow_data.get("generate_insights", True):
                insights_result = await self.get_comprehensive_insights({
                    "date_range": {
                        "start_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                        "end_date": datetime.now().strftime("%Y-%m-%d")
                    }
                })
                
                results["steps"].append({
                    "step": "insights_generation", 
                    "success": insights_result.get("success", False),
                    "data": insights_result
                })
            
            results["success"] = all(step.get("success", False) for step in results["steps"])
            results["completed_at"] = datetime.now().isoformat()
            
            return results
            
        except Exception as e:
            logger.error(f"Content workflow error: {str(e)}")
            return {
                "success": False,
                "error": "Content workflow execution failed",
                "details": str(e)
            }
    
    async def get_comprehensive_insights(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive insights across all Instagram marketing activities"""
        try:
            date_range = request_data.get("date_range", {})
            
            # Get account insights
            account_insights = await self.analytics_agent.get_account_insights(date_range)
            
            # Get audience demographics
            demographics = await self.analytics_agent.get_audience_demographics()
            
            # Get content performance report
            content_report = await self.analytics_agent.generate_content_performance_report({
                "date_range": date_range,
                "limit": 25
            })
            
            # Get engagement analysis
            engagement_analysis = await self.engagement_agent.analyze_audience_engagement(date_range)
            
            return {
                "success": True,
                "insights": {
                    "account_performance": account_insights.get("metrics", {}) if account_insights.get("success") else {},
                    "audience_demographics": demographics.get("demographics", {}) if demographics.get("success") else {},
                    "content_performance": content_report.get("summary", {}) if content_report.get("success") else {},
                    "engagement_analysis": engagement_analysis.get("engagement_analysis", {}) if engagement_analysis.get("success") else {}
                },
                "recommendations": self._consolidate_recommendations([
                    account_insights.get("insights", []),
                    content_report.get("recommendations", []),
                    engagement_analysis.get("recommendations", [])
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
        
        return consolidated[:10]  # Return top 10 recommendations


# Export main classes for Brain API Gateway integration
__all__ = [
    "InstagramMarketingAPIIntegration",
    "InstagramCampaignAgent",
    "InstagramContentAgent", 
    "InstagramEngagementAgent",
    "InstagramAnalyticsAgent",
    "InstagramCampaignObjective",
    "InstagramContentType",
    "InstagramPlacement"
]


# Example usage and testing functions
async def test_instagram_integration():
    """Test Instagram Marketing API integration"""
    # Test configuration
    test_config = {
        "access_token": "YOUR_INSTAGRAM_ACCESS_TOKEN",
        "instagram_account_id": "YOUR_INSTAGRAM_BUSINESS_ACCOUNT_ID",
        "ad_account_id": "YOUR_FACEBOOK_AD_ACCOUNT_ID",  # Optional for campaigns
        "facebook_page_id": "YOUR_FACEBOOK_PAGE_ID"  # Optional
    }
    
    try:
        # Initialize integration
        instagram = InstagramMarketingAPIIntegration(
            access_token=test_config["access_token"],
            instagram_account_id=test_config["instagram_account_id"],
            ad_account_id=test_config.get("ad_account_id"),
            facebook_page_id=test_config.get("facebook_page_id")
        )
        
        # Test content workflow
        content_workflow_data = {
            "posts": [
                {
                    "caption": "Transform your business with AI-powered marketing! 🚀 #AIMarketing #BusinessGrowth #Innovation",
                    "media_type": "IMAGE",
                    "media_url": "https://example.com/marketing-image.jpg",
                    "hashtags": ["AIMarketing", "BusinessGrowth", "Innovation", "MarketingTips"],
                    "call_to_action": "Learn More",
                    "link_url": "https://example.com/ai-marketing"
                }
            ],
            "enable_engagement_tracking": True,
            "generate_insights": True
        }
        
        # Execute content workflow
        result = await instagram.execute_content_workflow(content_workflow_data)
        print(f"Content workflow result: {json.dumps(result, indent=2)}")
        
        # Get comprehensive insights
        insights_result = await instagram.get_comprehensive_insights({
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
    asyncio.run(test_instagram_integration())
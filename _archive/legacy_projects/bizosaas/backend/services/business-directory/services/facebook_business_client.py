"""
Facebook Graph API Business Client
Handles business page sync with Facebook using Graph API
"""

import asyncio
import json
import logging
import time
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from circuitbreaker import circuit

from ..models.base import PlatformIntegration
from ..core.config import settings
from ..core.database import get_async_session

logger = logging.getLogger(__name__)

@dataclass
class FacebookAPIResponse:
    """Structured Facebook API response"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    rate_limit_remaining: Optional[int] = None

class FacebookRateLimiter:
    """Rate limiter for Facebook Graph API calls"""
    
    def __init__(self, calls_per_hour: int = 200):
        self.calls_per_hour = calls_per_hour
        self.calls = []
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquire rate limit permission"""
        async with self.lock:
            now = time.time()
            # Remove calls older than 1 hour
            self.calls = [call for call in self.calls if now - call < 3600.0]
            
            if len(self.calls) >= self.calls_per_hour:
                sleep_time = 3600.0 - (now - self.calls[0])
                if sleep_time > 0:
                    await asyncio.sleep(min(sleep_time, 60))  # Max 1 minute wait
                    return await self.acquire()
            
            self.calls.append(now)

class FacebookBusinessClient:
    """Facebook Graph API client for business page management"""
    
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v18.0"
        self.rate_limiter = FacebookRateLimiter()
        self.session = None
        
    async def get_session(self) -> httpx.AsyncClient:
        """Get HTTP session"""
        if not self.session:
            self.session = httpx.AsyncClient(
                timeout=30.0,
                limits=httpx.Limits(max_connections=10, max_keepalive_connections=5)
            )
        return self.session
    
    @circuit(failure_threshold=5, recovery_timeout=60)
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError))
    )
    async def _make_request(self, method: str, endpoint: str, access_token: str, **kwargs) -> FacebookAPIResponse:
        """Make API request with retry and circuit breaker"""
        await self.rate_limiter.acquire()
        
        session = await self.get_session()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Add access token to params
        params = kwargs.get("params", {})
        params["access_token"] = access_token
        kwargs["params"] = params
        
        try:
            response = await session.request(method, url, **kwargs)
            
            # Check rate limiting headers
            rate_limit_remaining = response.headers.get("X-App-Usage")
            
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 3600))
                logger.warning(f"Facebook API rate limit exceeded. Retry after {retry_after} seconds")
                await asyncio.sleep(min(retry_after, 300))  # Max 5 minutes wait
                return await self._make_request(method, endpoint, access_token, **kwargs)
            
            response.raise_for_status()
            
            return FacebookAPIResponse(
                success=True,
                data=response.json() if response.content else {},
                status_code=response.status_code,
                rate_limit_remaining=rate_limit_remaining
            )
            
        except httpx.HTTPStatusError as e:
            error_msg = f"Facebook API HTTP error: {e.response.status_code}"
            if e.response.content:
                try:
                    error_data = e.response.json()
                    error_msg += f" - {error_data.get('error', {}).get('message', '')}"
                except:
                    pass
                    
            logger.error(error_msg)
            return FacebookAPIResponse(
                success=False,
                error=error_msg,
                status_code=e.response.status_code
            )
            
        except Exception as e:
            logger.error(f"Facebook API request failed: {str(e)}")
            return FacebookAPIResponse(success=False, error=str(e))
    
    async def get_page_info(self, page_id: str, access_token: str, fields: str = None) -> FacebookAPIResponse:
        """Get Facebook page information"""
        default_fields = [
            "id", "name", "about", "description", "category", "phone", "website",
            "emails", "location", "hours", "rating_count", "overall_star_rating",
            "cover", "picture", "is_verified", "is_published", "fan_count",
            "checkins", "talking_about_count", "category_list", "link"
        ]
        
        if not fields:
            fields = ",".join(default_fields)
        
        params = {"fields": fields}
        return await self._make_request("GET", page_id, access_token, params=params)
    
    async def get_page_posts(self, page_id: str, access_token: str, limit: int = 25,
                            since: datetime = None, until: datetime = None) -> FacebookAPIResponse:
        """Get page posts"""
        fields = "id,message,story,created_time,type,status_type,link,picture,full_picture,source,description,caption,name,object_id,application,likes.summary(true),comments.summary(true),shares"
        
        params = {
            "fields": fields,
            "limit": min(limit, 100)
        }
        
        if since:
            params["since"] = int(since.timestamp())
        if until:
            params["until"] = int(until.timestamp())
        
        return await self._make_request("GET", f"{page_id}/posts", access_token, params=params)
    
    async def get_page_reviews(self, page_id: str, access_token: str, limit: int = 25) -> FacebookAPIResponse:
        """Get page reviews/ratings"""
        fields = "created_time,reviewer,rating,review_text,open_graph_story"
        params = {
            "fields": fields,
            "limit": min(limit, 100)
        }
        
        return await self._make_request("GET", f"{page_id}/ratings", access_token, params=params)
    
    async def get_page_insights(self, page_id: str, access_token: str, metrics: List[str] = None,
                               period: str = "day", since: datetime = None, until: datetime = None) -> FacebookAPIResponse:
        """Get page insights/analytics"""
        default_metrics = [
            "page_impressions", "page_impressions_unique", "page_engaged_users",
            "page_fan_adds", "page_fan_removes", "page_views_total",
            "page_actions_post_reactions_total"
        ]
        
        if not metrics:
            metrics = default_metrics
        
        params = {
            "metric": ",".join(metrics),
            "period": period
        }
        
        if since:
            params["since"] = since.strftime("%Y-%m-%d")
        if until:
            params["until"] = until.strftime("%Y-%m-%d")
        
        return await self._make_request("GET", f"{page_id}/insights", access_token, params=params)
    
    async def search_pages(self, query: str, access_token: str, location: str = None,
                          limit: int = 25) -> FacebookAPIResponse:
        """Search for Facebook pages"""
        params = {
            "q": query,
            "type": "page",
            "limit": min(limit, 100),
            "fields": "id,name,category,location,link,picture,cover,fan_count,checkins"
        }
        
        if location:
            params["center"] = location
        
        return await self._make_request("GET", "search", access_token, params=params)
    
    async def get_user_pages(self, access_token: str) -> FacebookAPIResponse:
        """Get pages managed by the user"""
        fields = "id,name,category,access_token,perms,tasks,category_list,picture,cover,link"
        params = {"fields": fields}
        
        return await self._make_request("GET", "me/accounts", access_token, params=params)
    
    async def update_page_info(self, page_id: str, access_token: str, **updates) -> FacebookAPIResponse:
        """Update page information"""
        return await self._make_request("POST", page_id, access_token, data=updates)
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.aclose()
            self.session = None

# Platform-specific data mappers
class FacebookDataMapper:
    """Maps Facebook API responses to our unified business data format"""
    
    @staticmethod
    def map_page_info(facebook_page: Dict[str, Any]) -> Dict[str, Any]:
        """Map Facebook page to unified business format"""
        location = facebook_page.get("location", {})
        picture = facebook_page.get("picture", {}).get("data", {})
        cover = facebook_page.get("cover", {})
        
        return {
            "platform": "facebook",
            "platform_id": facebook_page.get("id"),
            "name": facebook_page.get("name"),
            "description": facebook_page.get("about") or facebook_page.get("description"),
            "phone": facebook_page.get("phone"),
            "website_url": facebook_page.get("website"),
            "social_url": facebook_page.get("link"),
            "emails": facebook_page.get("emails", []),
            "image_url": picture.get("url"),
            "cover_photo_url": cover.get("source"),
            "rating": facebook_page.get("overall_star_rating"),
            "review_count": facebook_page.get("rating_count"),
            "followers_count": facebook_page.get("fan_count"),
            "checkins_count": facebook_page.get("checkins"),
            "category": facebook_page.get("category"),
            "categories": [cat.get("name") for cat in facebook_page.get("category_list", [])],
            "is_verified": facebook_page.get("is_verified"),
            "is_published": facebook_page.get("is_published"),
            "location": {
                "address": location.get("street"),
                "city": location.get("city"),
                "state": location.get("state"),
                "postal_code": location.get("zip"),
                "country": location.get("country"),
                "formatted_address": ", ".join(filter(None, [
                    location.get("street"),
                    location.get("city"),
                    location.get("state"),
                    location.get("zip")
                ]))
            },
            "coordinates": {
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude")
            },
            "hours": FacebookDataMapper._map_hours(facebook_page.get("hours", {})),
            "platform_data": {
                "talking_about_count": facebook_page.get("talking_about_count"),
                "page_id": facebook_page.get("id"),
                "username": facebook_page.get("username")
            }
        }
    
    @staticmethod
    def _map_hours(hours_data: Dict[str, Any]) -> Dict[str, Any]:
        """Map Facebook hours format to unified format"""
        if not hours_data:
            return {}
        
        # Facebook uses day_hour format (e.g., "mon_1_open": "09:00")
        periods = []
        days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        
        for i, day in enumerate(days):
            for period in ["1", "2"]:  # Facebook supports up to 2 periods per day
                open_key = f"{day}_{period}_open"
                close_key = f"{day}_{period}_close"
                
                if open_key in hours_data and close_key in hours_data:
                    periods.append({
                        "day": i,  # 0 = Monday
                        "start": hours_data[open_key],
                        "end": hours_data[close_key]
                    })
        
        return {"periods": periods}
    
    @staticmethod
    def map_posts(facebook_posts: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Map Facebook posts to unified format"""
        posts = []
        for post in facebook_posts.get("data", []):
            likes = post.get("likes", {}).get("summary", {})
            comments = post.get("comments", {}).get("summary", {})
            shares = post.get("shares", {})
            
            posts.append({
                "platform": "facebook",
                "post_id": post.get("id"),
                "message": post.get("message") or post.get("story"),
                "type": post.get("type"),
                "status_type": post.get("status_type"),
                "created_time": post.get("created_time"),
                "link": post.get("link"),
                "picture": post.get("picture") or post.get("full_picture"),
                "likes_count": likes.get("total_count", 0),
                "comments_count": comments.get("total_count", 0),
                "shares_count": shares.get("count", 0),
                "platform_data": {
                    "object_id": post.get("object_id"),
                    "application": post.get("application"),
                    "caption": post.get("caption"),
                    "description": post.get("description"),
                    "name": post.get("name"),
                    "source": post.get("source")
                }
            })
        return posts
    
    @staticmethod
    def map_reviews(facebook_reviews: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Map Facebook reviews to unified format"""
        reviews = []
        for review in facebook_reviews.get("data", []):
            reviewer = review.get("reviewer", {})
            reviews.append({
                "platform": "facebook",
                "review_id": review.get("id"),
                "author_name": reviewer.get("name"),
                "author_id": reviewer.get("id"),
                "rating": review.get("rating"),
                "text": review.get("review_text"),
                "time_created": review.get("created_time"),
                "platform_data": {
                    "open_graph_story": review.get("open_graph_story")
                }
            })
        return reviews
    
    @staticmethod
    def map_insights(facebook_insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Map Facebook insights to unified analytics format"""
        insights = []
        for insight in facebook_insights.get("data", []):
            values = insight.get("values", [])
            for value in values:
                insights.append({
                    "platform": "facebook",
                    "metric_name": insight.get("name"),
                    "metric_title": insight.get("title"),
                    "period": insight.get("period"),
                    "date": value.get("end_time"),
                    "value": value.get("value"),
                    "platform_data": {
                        "description": insight.get("description")
                    }
                })
        return insights

# Global instance
facebook_client = FacebookBusinessClient()
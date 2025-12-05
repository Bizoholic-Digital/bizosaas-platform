"""
LinkedIn Marketing API Integration for BizOSaaS Brain

This module provides comprehensive LinkedIn marketing automation capabilities through 
specialized AI agents for professional networking, B2B campaigns, and lead generation.

Architecture:
- LinkedInCampaignAgent: Campaign creation and management
- LinkedInAudienceAgent: Professional audience targeting and segmentation  
- LinkedInContentAgent: Content creation and publishing
- LinkedInAnalyticsAgent: Performance tracking and insights

Author: BizOSaaS Development Team
Version: 1.0.0
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import hashlib
import hmac
import base64
from urllib.parse import urlencode, quote

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LinkedInCampaignObjective(Enum):
    """LinkedIn campaign objectives"""
    BRAND_AWARENESS = "BRAND_AWARENESS"
    WEBSITE_VISITS = "WEBSITE_VISITS"
    ENGAGEMENT = "ENGAGEMENT"
    VIDEO_VIEWS = "VIDEO_VIEWS"
    LEAD_GENERATION = "LEAD_GENERATION"
    WEBSITE_CONVERSIONS = "WEBSITE_CONVERSIONS"
    JOB_APPLICANTS = "JOB_APPLICANTS"


class LinkedInAudienceType(Enum):
    """LinkedIn audience targeting types"""
    LOCATION = "location"
    COMPANY = "company"
    JOB_TITLE = "jobTitle"
    JOB_FUNCTION = "jobFunction"
    INDUSTRY = "industry"
    SENIORITY = "seniority"
    SKILLS = "skills"
    INTERESTS = "interests"
    EDUCATION = "education"


class LinkedInContentFormat(Enum):
    """LinkedIn content formats"""
    SINGLE_IMAGE = "SINGLE_IMAGE"
    VIDEO = "VIDEO"
    CAROUSEL = "CAROUSEL"
    TEXT_ONLY = "TEXT_ONLY"
    DOCUMENT = "DOCUMENT"
    EVENT = "EVENT"
    ARTICLE = "ARTICLE"


@dataclass
class LinkedInCampaignConfig:
    """Configuration for LinkedIn campaigns"""
    name: str
    objective: LinkedInCampaignObjective
    daily_budget: float
    start_date: str
    end_date: Optional[str] = None
    targeting: Dict[str, Any] = None
    bid_type: str = "AUTOMATED_BID"
    optimization_target: str = "CLICK_THROUGH_RATE"
    
    def to_api_format(self) -> Dict[str, Any]:
        """Convert to LinkedIn API format"""
        config = {
            "name": self.name,
            "type": "SPONSORED_CONTENT",
            "status": "PAUSED",
            "changeAuditStamps": {
                "created": {
                    "time": int(datetime.now().timestamp() * 1000)
                }
            },
            "costType": "CPM",
            "dailyBudget": {
                "currencyCode": "USD",
                "amount": str(int(self.daily_budget * 1000000))  # LinkedIn uses micro-currency
            }
        }
        
        if self.start_date:
            config["runSchedule"] = {
                "start": int(datetime.fromisoformat(self.start_date).timestamp() * 1000)
            }
            
        if self.end_date:
            config["runSchedule"]["end"] = int(datetime.fromisoformat(self.end_date).timestamp() * 1000)
            
        if self.targeting:
            config["targeting"] = self.targeting
            
        return config


@dataclass
class LinkedInAudienceSegment:
    """LinkedIn audience segment configuration"""
    name: str
    targeting_criteria: Dict[str, Any]
    estimated_size: Optional[int] = None
    
    def to_api_format(self) -> Dict[str, Any]:
        """Convert to LinkedIn targeting API format"""
        return {
            "includedTargetingFacets": self.targeting_criteria,
            "excludedTargetingFacets": {}
        }


@dataclass
class LinkedInContent:
    """LinkedIn content configuration"""
    title: str
    description: str
    format_type: LinkedInContentFormat
    call_to_action: str
    landing_page_url: str
    media_urls: List[str] = None
    
    def to_api_format(self) -> Dict[str, Any]:
        """Convert to LinkedIn Creative API format"""
        creative = {
            "variables": {
                "clickUri": self.landing_page_url,
                "data": {
                    "com.linkedin.ads.SponsoredContentCreativeVariables": {
                        "activity": f"urn:li:activity:{self.generate_activity_id()}",
                        "directSponsoredContent": True,
                        "shareCommentary": {
                            "text": self.description
                        }
                    }
                }
            }
        }
        
        return creative
    
    def generate_activity_id(self) -> str:
        """Generate a unique activity ID"""
        content_hash = hashlib.md5(f"{self.title}{self.description}".encode()).hexdigest()
        return content_hash[:16]


class LinkedInAPIClient:
    """Base LinkedIn API client with authentication and rate limiting"""
    
    def __init__(self, access_token: str, client_id: str = None, client_secret: str = None):
        self.access_token = access_token
        self.client_id = client_id  
        self.client_secret = client_secret
        self.base_url = "https://api.linkedin.com/rest"
        self.session = None
        self.rate_limit_remaining = 1000
        self.rate_limit_reset = datetime.now()
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "LinkedIn-Version": "202306",
                "X-Restli-Protocol-Version": "2.0.0",
                "Content-Type": "application/json"
            },
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
            
    async def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict[str, Any]:
        """Make authenticated request to LinkedIn API"""
        if not self.session:
            raise RuntimeError("Client not initialized. Use async context manager.")
            
        # Check rate limits
        if self.rate_limit_remaining <= 10 and datetime.now() < self.rate_limit_reset:
            wait_time = (self.rate_limit_reset - datetime.now()).total_seconds()
            logger.warning(f"Rate limit approaching. Waiting {wait_time:.1f}s")
            await asyncio.sleep(wait_time)
            
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            async with self.session.request(method, url, json=data, params=params) as response:
                # Update rate limit info
                self.rate_limit_remaining = int(response.headers.get("X-RateLimit-Remaining", 1000))
                reset_time = response.headers.get("X-RateLimit-Reset")
                if reset_time:
                    self.rate_limit_reset = datetime.fromtimestamp(int(reset_time))
                
                response_data = await response.json() if response.content_type == 'application/json' else await response.text()
                
                if response.status >= 400:
                    logger.error(f"LinkedIn API error {response.status}: {response_data}")
                    return {
                        "success": False,
                        "error": f"API error {response.status}",
                        "details": response_data,
                        "status_code": response.status
                    }
                    
                logger.info(f"LinkedIn API {method} {endpoint}: {response.status}")
                return {
                    "success": True,
                    "data": response_data,
                    "status_code": response.status
                }
                
        except aiohttp.ClientError as e:
            logger.error(f"LinkedIn API request failed: {str(e)}")
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


class LinkedInCampaignAgent:
    """AI agent for LinkedIn campaign management and optimization"""
    
    def __init__(self, access_token: str, account_id: str):
        self.access_token = access_token
        self.account_id = account_id
        self.client = LinkedInAPIClient(access_token)
        
    async def create_campaign(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new LinkedIn campaign"""
        try:
            config = LinkedInCampaignConfig(
                name=request_data.get("name", "New LinkedIn Campaign"),
                objective=LinkedInCampaignObjective(request_data.get("objective", "WEBSITE_VISITS")),
                daily_budget=float(request_data.get("daily_budget", 50.0)),
                start_date=request_data.get("start_date", datetime.now().isoformat()),
                end_date=request_data.get("end_date"),
                targeting=request_data.get("targeting", {}),
                bid_type=request_data.get("bid_type", "AUTOMATED_BID"),
                optimization_target=request_data.get("optimization_target", "CLICK_THROUGH_RATE")
            )
            
            async with self.client as client:
                # Create campaign group first
                campaign_group_data = {
                    "account": f"urn:li:sponsoredAccount:{self.account_id}",
                    "name": f"{config.name} - Group",
                    "status": "ACTIVE",
                    "totalBudget": {
                        "currencyCode": "USD", 
                        "amount": str(int(config.daily_budget * 30 * 1000000))
                    }
                }
                
                group_response = await client._make_request("POST", "campaignGroups", campaign_group_data)
                
                if not group_response.get("success"):
                    return group_response
                    
                campaign_group_id = group_response["data"]["id"]
                
                # Create campaign
                campaign_data = config.to_api_format()
                campaign_data["campaignGroup"] = f"urn:li:sponsoredCampaignGroup:{campaign_group_id}"
                campaign_data["account"] = f"urn:li:sponsoredAccount:{self.account_id}"
                
                campaign_response = await client._make_request("POST", "campaigns", campaign_data)
                
                if campaign_response.get("success"):
                    campaign_id = campaign_response["data"]["id"]
                    
                    # Get campaign details
                    details = await self.get_campaign_details(campaign_id)
                    
                    return {
                        "success": True,
                        "campaign_id": campaign_id,
                        "campaign_group_id": campaign_group_id,
                        "details": details,
                        "message": "LinkedIn campaign created successfully"
                    }
                
                return campaign_response
                
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
            response = await client._make_request("GET", f"campaigns/{campaign_id}")
            
            if response.get("success"):
                return response["data"]
            
            return {"error": "Failed to fetch campaign details"}
    
    async def update_campaign_budget(self, campaign_id: str, new_budget: float) -> Dict[str, Any]:
        """Update campaign daily budget"""
        try:
            update_data = {
                "dailyBudget": {
                    "currencyCode": "USD",
                    "amount": str(int(new_budget * 1000000))
                }
            }
            
            async with self.client as client:
                response = await client._make_request("POST", f"campaigns/{campaign_id}", update_data)
                
                if response.get("success"):
                    return {
                        "success": True,
                        "campaign_id": campaign_id,
                        "new_budget": new_budget,
                        "message": "Budget updated successfully"
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Budget update error: {str(e)}")
            return {
                "success": False,
                "error": "Budget update failed",
                "details": str(e)
            }
    
    async def pause_resume_campaign(self, campaign_id: str, action: str) -> Dict[str, Any]:
        """Pause or resume a campaign"""
        try:
            status = "PAUSED" if action.lower() == "pause" else "ACTIVE"
            update_data = {"status": status}
            
            async with self.client as client:
                response = await client._make_request("POST", f"campaigns/{campaign_id}", update_data)
                
                if response.get("success"):
                    return {
                        "success": True,
                        "campaign_id": campaign_id,
                        "status": status,
                        "message": f"Campaign {action.lower()}d successfully"
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Campaign status update error: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to {action.lower()} campaign",
                "details": str(e)
            }
    
    async def get_campaign_performance(self, campaign_id: str, date_range: Dict[str, str]) -> Dict[str, Any]:
        """Get campaign performance metrics"""
        try:
            params = {
                "q": "analytics",
                "pivot": "CAMPAIGN", 
                "dateRange.start.day": date_range.get("start_day"),
                "dateRange.start.month": date_range.get("start_month"),
                "dateRange.start.year": date_range.get("start_year"),
                "dateRange.end.day": date_range.get("end_day"),
                "dateRange.end.month": date_range.get("end_month"),
                "dateRange.end.year": date_range.get("end_year"),
                "campaigns[0]": f"urn:li:sponsoredCampaign:{campaign_id}",
                "fields": "dateRange,impressions,clicks,costInUsd,externalWebsiteConversions"
            }
            
            async with self.client as client:
                response = await client._make_request("GET", "adAnalyticsV2", params=params)
                
                if response.get("success"):
                    analytics = response["data"]["elements"][0] if response["data"]["elements"] else {}
                    
                    return {
                        "success": True,
                        "campaign_id": campaign_id,
                        "metrics": {
                            "impressions": analytics.get("impressions", 0),
                            "clicks": analytics.get("clicks", 0),
                            "spend": analytics.get("costInUsd", 0),
                            "conversions": analytics.get("externalWebsiteConversions", 0),
                            "ctr": (analytics.get("clicks", 0) / analytics.get("impressions", 1)) * 100,
                            "cpc": analytics.get("costInUsd", 0) / analytics.get("clicks", 1) if analytics.get("clicks", 0) > 0 else 0
                        },
                        "date_range": date_range
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Performance tracking error: {str(e)}")
            return {
                "success": False,
                "error": "Performance tracking failed",
                "details": str(e)
            }


class LinkedInAudienceAgent:
    """AI agent for LinkedIn audience targeting and segmentation"""
    
    def __init__(self, access_token: str, account_id: str):
        self.access_token = access_token
        self.account_id = account_id
        self.client = LinkedInAPIClient(access_token)
        
    async def create_audience_segment(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create targeted audience segment"""
        try:
            segment = LinkedInAudienceSegment(
                name=request_data.get("name", "New Audience Segment"),
                targeting_criteria=request_data.get("targeting", {}),
                estimated_size=request_data.get("estimated_size")
            )
            
            # Get audience size estimate
            size_estimate = await self.estimate_audience_size(segment.targeting_criteria)
            segment.estimated_size = size_estimate.get("estimated_size", 0)
            
            return {
                "success": True,
                "segment": asdict(segment),
                "api_format": segment.to_api_format(),
                "estimated_reach": size_estimate,
                "message": "Audience segment created successfully"
            }
            
        except Exception as e:
            logger.error(f"Audience segment creation error: {str(e)}")
            return {
                "success": False,
                "error": "Audience segment creation failed",
                "details": str(e)
            }
    
    async def estimate_audience_size(self, targeting_criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate audience size for targeting criteria"""
        try:
            params = {
                "account": f"urn:li:sponsoredAccount:{self.account_id}",
                "targetingCriteria": targeting_criteria
            }
            
            async with self.client as client:
                response = await client._make_request("GET", "audienceCountsV2", params=params)
                
                if response.get("success"):
                    count_data = response["data"]
                    
                    return {
                        "success": True,
                        "estimated_size": count_data.get("total", 0),
                        "details": {
                            "total_reached": count_data.get("total", 0),
                            "active_members": count_data.get("activeMembers", 0),
                            "targeting_expansion": count_data.get("targetingExpansionEnabled", False)
                        }
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Audience estimation error: {str(e)}")
            return {
                "success": False,
                "error": "Audience estimation failed",
                "details": str(e),
                "estimated_size": 0
            }
    
    async def get_targeting_suggestions(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get LinkedIn targeting suggestions"""
        try:
            query_type = request_data.get("type", "company")
            search_term = request_data.get("query", "")
            
            if query_type == "company":
                endpoint = "companiesV2"
                params = {"q": "universalName", "universalName": search_term}
            elif query_type == "job_title":
                endpoint = "jobTitles"  
                params = {"q": "title", "title": search_term}
            elif query_type == "skills":
                endpoint = "skills"
                params = {"q": "name", "name": search_term}
            else:
                return {
                    "success": False,
                    "error": "Invalid targeting type",
                    "supported_types": ["company", "job_title", "skills"]
                }
                
            async with self.client as client:
                response = await client._make_request("GET", endpoint, params=params)
                
                if response.get("success"):
                    suggestions = []
                    elements = response["data"].get("elements", [])
                    
                    for element in elements[:10]:  # Limit to top 10
                        suggestion = {
                            "id": element.get("id"),
                            "name": element.get("localizedName", element.get("name", "")),
                            "type": query_type
                        }
                        suggestions.append(suggestion)
                    
                    return {
                        "success": True,
                        "suggestions": suggestions,
                        "query": search_term,
                        "type": query_type
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Targeting suggestions error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to get targeting suggestions",
                "details": str(e)
            }
    
    async def analyze_competitor_audience(self, competitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitor audience for targeting insights"""
        try:
            competitor_name = competitor_data.get("company_name", "")
            
            # Search for competitor company
            company_search = await self.get_targeting_suggestions({
                "type": "company",
                "query": competitor_name
            })
            
            if not company_search.get("success") or not company_search.get("suggestions"):
                return {
                    "success": False,
                    "error": "Competitor company not found",
                    "query": competitor_name
                }
            
            competitor_id = company_search["suggestions"][0]["id"]
            
            # Analyze audience that works at competitor
            targeting_criteria = {
                "companies": [competitor_id],
                "jobExperience": ["CURRENT"]
            }
            
            audience_estimate = await self.estimate_audience_size(targeting_criteria)
            
            return {
                "success": True,
                "competitor": {
                    "name": competitor_name,
                    "linkedin_id": competitor_id,
                    "employee_count": audience_estimate.get("estimated_size", 0)
                },
                "targeting_recommendations": {
                    "exclude_current_employees": True,
                    "target_past_employees": True,
                    "target_similar_companies": True,
                    "suggested_job_functions": [
                        "Marketing", "Sales", "Business Development",
                        "Product Management", "Engineering"
                    ]
                },
                "audience_insights": audience_estimate
            }
            
        except Exception as e:
            logger.error(f"Competitor analysis error: {str(e)}")
            return {
                "success": False,
                "error": "Competitor analysis failed",
                "details": str(e)
            }


class LinkedInContentAgent:
    """AI agent for LinkedIn content creation and publishing"""
    
    def __init__(self, access_token: str, person_id: str = None, company_id: str = None):
        self.access_token = access_token
        self.person_id = person_id
        self.company_id = company_id  
        self.client = LinkedInAPIClient(access_token)
        
    async def create_sponsored_content(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create sponsored content for campaigns"""
        try:
            content = LinkedInContent(
                title=request_data.get("title", ""),
                description=request_data.get("description", ""),
                format_type=LinkedInContentFormat(request_data.get("format", "SINGLE_IMAGE")),
                call_to_action=request_data.get("cta", "Learn More"),
                landing_page_url=request_data.get("landing_url", ""),
                media_urls=request_data.get("media_urls", [])
            )
            
            async with self.client as client:
                # Create creative
                creative_data = content.to_api_format()
                creative_data["campaign"] = request_data.get("campaign_id", "")
                
                response = await client._make_request("POST", "creatives", creative_data)
                
                if response.get("success"):
                    creative_id = response["data"]["id"]
                    
                    return {
                        "success": True,
                        "creative_id": creative_id,
                        "content": asdict(content),
                        "message": "Sponsored content created successfully"
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Content creation error: {str(e)}")
            return {
                "success": False,
                "error": "Content creation failed",
                "details": str(e)
            }
    
    async def upload_media(self, media_data: Dict[str, Any]) -> Dict[str, Any]:
        """Upload media assets for content"""
        try:
            media_type = media_data.get("type", "image")
            media_url = media_data.get("url", "")
            
            if not media_url:
                return {
                    "success": False,
                    "error": "Media URL is required"
                }
            
            # Register upload
            register_data = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": f"urn:li:person:{self.person_id}" if self.person_id else f"urn:li:organization:{self.company_id}",
                    "serviceRelationships": [{
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }]
                }
            }
            
            async with self.client as client:
                register_response = await client._make_request("POST", "assets?action=registerUpload", register_data)
                
                if not register_response.get("success"):
                    return register_response
                
                upload_info = register_response["data"]["value"]
                asset_id = upload_info["asset"]
                upload_url = upload_info["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
                
                # Download and upload media
                async with aiohttp.ClientSession() as session:
                    # Download media
                    async with session.get(media_url) as media_response:
                        if media_response.status != 200:
                            return {
                                "success": False,
                                "error": "Failed to download media"
                            }
                        
                        media_content = await media_response.read()
                    
                    # Upload to LinkedIn
                    headers = {"Authorization": f"Bearer {self.access_token}"}
                    async with session.put(upload_url, data=media_content, headers=headers) as upload_response:
                        if upload_response.status not in [200, 201]:
                            return {
                                "success": False,
                                "error": "Failed to upload media to LinkedIn"
                            }
                
                return {
                    "success": True,
                    "asset_id": asset_id,
                    "media_type": media_type,
                    "message": "Media uploaded successfully"
                }
                
        except Exception as e:
            logger.error(f"Media upload error: {str(e)}")
            return {
                "success": False,
                "error": "Media upload failed",
                "details": str(e)
            }
    
    async def create_article_content(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create LinkedIn article content"""
        try:
            author_id = self.person_id or self.company_id
            if not author_id:
                return {
                    "success": False,
                    "error": "Author ID (person or company) is required"
                }
            
            article_payload = {
                "author": f"urn:li:person:{author_id}" if self.person_id else f"urn:li:organization:{author_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": article_data.get("description", "")
                        },
                        "shareMediaCategory": "ARTICLE",
                        "media": [{
                            "status": "READY",
                            "description": {
                                "text": article_data.get("title", "")
                            },
                            "originalUrl": article_data.get("article_url", ""),
                            "title": {
                                "text": article_data.get("title", "")
                            }
                        }]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            async with self.client as client:
                response = await client._make_request("POST", "ugcPosts", article_payload)
                
                if response.get("success"):
                    post_id = response["data"]["id"]
                    
                    return {
                        "success": True,
                        "post_id": post_id,
                        "article_url": article_data.get("article_url"),
                        "message": "Article shared successfully"
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Article creation error: {str(e)}")
            return {
                "success": False,
                "error": "Article creation failed",
                "details": str(e)
            }
    
    async def get_content_performance(self, content_id: str) -> Dict[str, Any]:
        """Get performance metrics for content"""
        try:
            params = {
                "q": "authors",
                "authors": f"urn:li:person:{self.person_id}" if self.person_id else f"urn:li:organization:{self.company_id}",
                "sortBy": "LAST_MODIFIED"
            }
            
            async with self.client as client:
                response = await client._make_request("GET", "shares", params=params)
                
                if response.get("success"):
                    shares = response["data"]["elements"]
                    
                    # Find specific content
                    content_share = None
                    for share in shares:
                        if content_id in share.get("id", ""):
                            content_share = share
                            break
                    
                    if not content_share:
                        return {
                            "success": False,
                            "error": "Content not found"
                        }
                    
                    # Get social actions (likes, comments, shares)
                    social_detail = content_share.get("socialDetail", {})
                    
                    return {
                        "success": True,
                        "content_id": content_id,
                        "performance": {
                            "likes": social_detail.get("totalSocialActivityCounts", {}).get("numLikes", 0),
                            "comments": social_detail.get("totalSocialActivityCounts", {}).get("numComments", 0),
                            "shares": social_detail.get("totalSocialActivityCounts", {}).get("numShares", 0),
                            "views": social_detail.get("totalSocialActivityCounts", {}).get("numViews", 0)
                        },
                        "engagement_rate": self._calculate_engagement_rate(social_detail)
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Content performance error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to get content performance",
                "details": str(e)
            }
    
    def _calculate_engagement_rate(self, social_detail: Dict[str, Any]) -> float:
        """Calculate engagement rate for content"""
        counts = social_detail.get("totalSocialActivityCounts", {})
        likes = counts.get("numLikes", 0)
        comments = counts.get("numComments", 0)
        shares = counts.get("numShares", 0)
        views = counts.get("numViews", 1)  # Avoid division by zero
        
        total_engagement = likes + comments + shares
        return (total_engagement / views) * 100 if views > 0 else 0


class LinkedInAnalyticsAgent:
    """AI agent for LinkedIn marketing analytics and insights"""
    
    def __init__(self, access_token: str, account_id: str):
        self.access_token = access_token
        self.account_id = account_id
        self.client = LinkedInAPIClient(access_token)
        
    async def get_account_insights(self, date_range: Dict[str, str]) -> Dict[str, Any]:
        """Get comprehensive account performance insights"""
        try:
            params = {
                "q": "analytics",
                "pivot": "ACCOUNT",
                "dateRange.start.day": date_range.get("start_day"),
                "dateRange.start.month": date_range.get("start_month"),
                "dateRange.start.year": date_range.get("start_year"),
                "dateRange.end.day": date_range.get("end_day"),
                "dateRange.end.month": date_range.get("end_month"),
                "dateRange.end.year": date_range.get("end_year"),
                "accounts[0]": f"urn:li:sponsoredAccount:{self.account_id}",
                "fields": "dateRange,impressions,clicks,costInUsd,externalWebsiteConversions,likes,comments,shares,follows,totalEngagements"
            }
            
            async with self.client as client:
                response = await client._make_request("GET", "adAnalyticsV2", params=params)
                
                if response.get("success"):
                    analytics = response["data"]["elements"][0] if response["data"]["elements"] else {}
                    
                    # Calculate key metrics
                    impressions = analytics.get("impressions", 0)
                    clicks = analytics.get("clicks", 0)
                    spend = analytics.get("costInUsd", 0)
                    conversions = analytics.get("externalWebsiteConversions", 0)
                    
                    metrics = {
                        "overview": {
                            "impressions": impressions,
                            "clicks": clicks,
                            "spend": spend,
                            "conversions": conversions
                        },
                        "performance": {
                            "ctr": (clicks / impressions) * 100 if impressions > 0 else 0,
                            "cpc": spend / clicks if clicks > 0 else 0,
                            "cpm": (spend / impressions) * 1000 if impressions > 0 else 0,
                            "conversion_rate": (conversions / clicks) * 100 if clicks > 0 else 0,
                            "cost_per_conversion": spend / conversions if conversions > 0 else 0
                        },
                        "engagement": {
                            "likes": analytics.get("likes", 0),
                            "comments": analytics.get("comments", 0),
                            "shares": analytics.get("shares", 0),
                            "follows": analytics.get("follows", 0),
                            "total_engagements": analytics.get("totalEngagements", 0)
                        }
                    }
                    
                    return {
                        "success": True,
                        "account_id": self.account_id,
                        "date_range": date_range,
                        "metrics": metrics,
                        "insights": self._generate_insights(metrics)
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Account insights error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to get account insights",
                "details": str(e)
            }
    
    async def get_audience_demographics(self, campaign_id: str = None) -> Dict[str, Any]:
        """Get audience demographic insights"""
        try:
            params = {
                "q": "analytics",
                "pivot": "MEMBER_COMPANY_SIZE,MEMBER_INDUSTRY,MEMBER_SENIORITY,MEMBER_JOB_FUNCTION",
                "dateRange.start.day": 1,
                "dateRange.start.month": (datetime.now() - timedelta(days=30)).month,
                "dateRange.start.year": (datetime.now() - timedelta(days=30)).year,
                "dateRange.end.day": datetime.now().day,
                "dateRange.end.month": datetime.now().month,
                "dateRange.end.year": datetime.now().year,
                "accounts[0]": f"urn:li:sponsoredAccount:{self.account_id}",
                "fields": "pivot,pivotValues,impressions,clicks,costInUsd"
            }
            
            if campaign_id:
                params["campaigns[0]"] = f"urn:li:sponsoredCampaign:{campaign_id}"
            
            async with self.client as client:
                response = await client._make_request("GET", "adAnalyticsV2", params=params)
                
                if response.get("success"):
                    elements = response["data"]["elements"]
                    demographics = {
                        "company_size": [],
                        "industry": [],
                        "seniority": [],
                        "job_function": []
                    }
                    
                    for element in elements:
                        pivot = element.get("pivot", "")
                        pivot_values = element.get("pivotValues", [])
                        
                        for pivot_value in pivot_values:
                            demo_data = {
                                "segment": pivot_value,
                                "impressions": element.get("impressions", 0),
                                "clicks": element.get("clicks", 0),
                                "spend": element.get("costInUsd", 0)
                            }
                            
                            if "COMPANY_SIZE" in pivot:
                                demographics["company_size"].append(demo_data)
                            elif "INDUSTRY" in pivot:
                                demographics["industry"].append(demo_data)
                            elif "SENIORITY" in pivot:
                                demographics["seniority"].append(demo_data)
                            elif "JOB_FUNCTION" in pivot:
                                demographics["job_function"].append(demo_data)
                    
                    return {
                        "success": True,
                        "campaign_id": campaign_id,
                        "demographics": demographics,
                        "top_segments": self._get_top_segments(demographics)
                    }
                
                return response
                
        except Exception as e:
            logger.error(f"Demographics analysis error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to get audience demographics",
                "details": str(e)
            }
    
    async def generate_performance_report(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        try:
            date_range = request_data.get("date_range", {})
            campaign_ids = request_data.get("campaign_ids", [])
            include_demographics = request_data.get("include_demographics", True)
            
            # Get account insights
            account_insights = await self.get_account_insights(date_range)
            
            # Get campaign performance for each campaign
            campaign_performance = []
            for campaign_id in campaign_ids:
                from . import LinkedInCampaignAgent  # Avoid circular import
                campaign_agent = LinkedInCampaignAgent(self.access_token, self.account_id)
                perf = await campaign_agent.get_campaign_performance(campaign_id, date_range)
                if perf.get("success"):
                    campaign_performance.append(perf)
            
            # Get demographics if requested
            demographics = None
            if include_demographics:
                demo_result = await self.get_audience_demographics()
                if demo_result.get("success"):
                    demographics = demo_result["demographics"]
            
            report = {
                "success": True,
                "report_id": hashlib.md5(f"{datetime.now().isoformat()}{self.account_id}".encode()).hexdigest()[:16],
                "generated_at": datetime.now().isoformat(),
                "date_range": date_range,
                "account_insights": account_insights.get("metrics") if account_insights.get("success") else {},
                "campaign_performance": campaign_performance,
                "audience_demographics": demographics,
                "recommendations": self._generate_recommendations(
                    account_insights.get("metrics", {}),
                    campaign_performance,
                    demographics
                ),
                "executive_summary": self._create_executive_summary(
                    account_insights.get("metrics", {}),
                    campaign_performance
                )
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Report generation error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to generate performance report",
                "details": str(e)
            }
    
    def _generate_insights(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate actionable insights from metrics"""
        insights = []
        performance = metrics.get("performance", {})
        
        # CTR insights
        ctr = performance.get("ctr", 0)
        if ctr < 0.5:
            insights.append("CTR is below LinkedIn average (0.5%). Consider improving ad creative or targeting.")
        elif ctr > 1.0:
            insights.append("Excellent CTR performance! Consider scaling successful campaigns.")
        
        # CPC insights
        cpc = performance.get("cpc", 0)
        if cpc > 10:
            insights.append("CPC is high. Consider optimizing targeting or improving relevance score.")
        
        # Conversion rate insights
        conv_rate = performance.get("conversion_rate", 0)
        if conv_rate < 2:
            insights.append("Conversion rate could be improved. Review landing page experience.")
        elif conv_rate > 5:
            insights.append("Strong conversion performance! Consider increasing budget allocation.")
        
        return insights
    
    def _get_top_segments(self, demographics: Dict[str, Any]) -> Dict[str, Any]:
        """Get top performing demographic segments"""
        top_segments = {}
        
        for category, segments in demographics.items():
            if segments:
                # Sort by clicks and take top 3
                sorted_segments = sorted(segments, key=lambda x: x.get("clicks", 0), reverse=True)
                top_segments[category] = sorted_segments[:3]
        
        return top_segments
    
    def _generate_recommendations(self, account_metrics: Dict, campaign_performance: List, demographics: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Performance-based recommendations
        if account_metrics.get("performance", {}).get("ctr", 0) < 0.5:
            recommendations.append("Test new creative formats - try video or carousel ads for better engagement")
        
        if account_metrics.get("performance", {}).get("conversion_rate", 0) < 2:
            recommendations.append("Optimize landing pages for mobile experience and faster load times")
        
        # Budget allocation recommendations
        if len(campaign_performance) > 1:
            best_performing = max(campaign_performance, key=lambda x: x.get("metrics", {}).get("ctr", 0), default={})
            if best_performing:
                recommendations.append(f"Increase budget for top-performing campaign (ID: {best_performing.get('campaign_id', 'N/A')})")
        
        # Targeting recommendations
        if demographics:
            top_industry = max(demographics.get("industry", []), key=lambda x: x.get("clicks", 0), default={})
            if top_industry:
                recommendations.append(f"Focus more budget on {top_industry.get('segment', 'top industry')} segment")
        
        recommendations.append("Consider A/B testing different call-to-action buttons")
        recommendations.append("Implement LinkedIn Insight Tag for better conversion tracking")
        
        return recommendations
    
    def _create_executive_summary(self, account_metrics: Dict, campaign_performance: List) -> Dict[str, Any]:
        """Create executive summary of performance"""
        overview = account_metrics.get("overview", {})
        performance = account_metrics.get("performance", {})
        
        total_campaigns = len(campaign_performance)
        active_campaigns = len([c for c in campaign_performance if c.get("metrics", {}).get("impressions", 0) > 0])
        
        return {
            "total_spend": overview.get("spend", 0),
            "total_impressions": overview.get("impressions", 0),
            "total_clicks": overview.get("clicks", 0),
            "total_conversions": overview.get("conversions", 0),
            "average_ctr": performance.get("ctr", 0),
            "average_cpc": performance.get("cpc", 0),
            "campaign_count": {
                "total": total_campaigns,
                "active": active_campaigns
            },
            "key_highlight": self._get_key_highlight(performance, overview)
        }
    
    def _get_key_highlight(self, performance: Dict, overview: Dict) -> str:
        """Get the most important highlight from performance data"""
        ctr = performance.get("ctr", 0)
        conversions = overview.get("conversions", 0)
        
        if ctr > 1.0:
            return f"Exceptional CTR of {ctr:.2f}% - significantly above LinkedIn average"
        elif conversions > 100:
            return f"Strong conversion performance with {conversions} total conversions"
        elif performance.get("conversion_rate", 0) > 5:
            return f"High conversion rate of {performance.get('conversion_rate', 0):.2f}%"
        else:
            return "Performance metrics within expected ranges - opportunities for optimization identified"


# Main LinkedIn Marketing API Integration Class
class LinkedInMarketingAPIIntegration:
    """
    Main integration class that orchestrates all LinkedIn marketing agents
    and provides a unified interface for the Brain API Gateway
    """
    
    def __init__(self, access_token: str, account_id: str, person_id: str = None, company_id: str = None):
        self.access_token = access_token
        self.account_id = account_id
        self.person_id = person_id
        self.company_id = company_id
        
        # Initialize agents
        self.campaign_agent = LinkedInCampaignAgent(access_token, account_id)
        self.audience_agent = LinkedInAudienceAgent(access_token, account_id)
        self.content_agent = LinkedInContentAgent(access_token, person_id, company_id)
        self.analytics_agent = LinkedInAnalyticsAgent(access_token, account_id)
        
    async def execute_campaign_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute complete LinkedIn campaign workflow"""
        try:
            results = {
                "workflow_id": hashlib.md5(f"{datetime.now().isoformat()}{workflow_data}".encode()).hexdigest()[:16],
                "started_at": datetime.now().isoformat(),
                "steps": []
            }
            
            # Step 1: Create audience segment
            if "audience" in workflow_data:
                audience_result = await self.audience_agent.create_audience_segment(workflow_data["audience"])
                results["steps"].append({
                    "step": "audience_creation",
                    "success": audience_result.get("success", False),
                    "data": audience_result
                })
                
                # Add targeting to campaign data
                if audience_result.get("success"):
                    workflow_data["campaign"]["targeting"] = audience_result["api_format"]["includedTargetingFacets"]
            
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
            
            # Step 3: Create content/creatives
            if "content" in workflow_data and campaign_id:
                for content_item in workflow_data["content"]:
                    content_item["campaign_id"] = f"urn:li:sponsoredCampaign:{campaign_id}"
                    content_result = await self.content_agent.create_sponsored_content(content_item)
                    results["steps"].append({
                        "step": "content_creation",
                        "success": content_result.get("success", False),
                        "data": content_result
                    })
            
            # Step 4: Activate campaign if requested
            if workflow_data.get("auto_activate", False) and campaign_id:
                activation_result = await self.campaign_agent.pause_resume_campaign(campaign_id, "resume")
                results["steps"].append({
                    "step": "campaign_activation",
                    "success": activation_result.get("success", False),
                    "data": activation_result
                })
            
            results["success"] = all(step.get("success", False) for step in results["steps"])
            results["completed_at"] = datetime.now().isoformat()
            
            return results
            
        except Exception as e:
            logger.error(f"Workflow execution error: {str(e)}")
            return {
                "success": False,
                "error": "Workflow execution failed",
                "details": str(e)
            }
    
    async def get_comprehensive_insights(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive insights across all LinkedIn marketing activities"""
        try:
            date_range = request_data.get("date_range", {})
            
            # Get account insights
            account_insights = await self.analytics_agent.get_account_insights(date_range)
            
            # Get audience demographics
            demographics = await self.analytics_agent.get_audience_demographics()
            
            # Generate performance report
            report = await self.analytics_agent.generate_performance_report({
                "date_range": date_range,
                "campaign_ids": request_data.get("campaign_ids", []),
                "include_demographics": True
            })
            
            return {
                "success": True,
                "insights": {
                    "account_performance": account_insights.get("metrics") if account_insights.get("success") else {},
                    "audience_demographics": demographics.get("demographics") if demographics.get("success") else {},
                    "performance_report": report if report.get("success") else {}
                },
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Comprehensive insights error: {str(e)}")
            return {
                "success": False,
                "error": "Failed to generate comprehensive insights",
                "details": str(e)
            }


# Export main classes for Brain API Gateway integration
__all__ = [
    "LinkedInMarketingAPIIntegration",
    "LinkedInCampaignAgent", 
    "LinkedInAudienceAgent",
    "LinkedInContentAgent",
    "LinkedInAnalyticsAgent",
    "LinkedInCampaignObjective",
    "LinkedInAudienceType", 
    "LinkedInContentFormat"
]


# Example usage and testing functions
async def test_linkedin_integration():
    """Test LinkedIn Marketing API integration"""
    # Test configuration
    test_config = {
        "access_token": "YOUR_LINKEDIN_ACCESS_TOKEN",
        "account_id": "YOUR_LINKEDIN_ACCOUNT_ID",
        "person_id": "YOUR_PERSON_ID",  # Optional
        "company_id": "YOUR_COMPANY_ID"  # Optional
    }
    
    try:
        # Initialize integration
        linkedin = LinkedInMarketingAPIIntegration(
            access_token=test_config["access_token"],
            account_id=test_config["account_id"],
            person_id=test_config.get("person_id"),
            company_id=test_config.get("company_id")
        )
        
        # Test workflow execution
        workflow_data = {
            "audience": {
                "name": "Tech Professionals",
                "targeting": {
                    "industries": ["SOFTWARE"],
                    "jobFunctions": ["ENGINEERING", "PRODUCT_MANAGEMENT"],
                    "seniorityLevels": ["MANAGER", "SENIOR", "DIRECTOR"]
                }
            },
            "campaign": {
                "name": "LinkedIn Test Campaign",
                "objective": "WEBSITE_VISITS",
                "daily_budget": 50.0,
                "start_date": datetime.now().isoformat(),
                "bid_type": "AUTOMATED_BID"
            },
            "content": [{
                "title": "Transform Your Business with AI",
                "description": "Discover how AI can revolutionize your marketing strategy. Click to learn more!",
                "format": "SINGLE_IMAGE",
                "cta": "Learn More",
                "landing_url": "https://example.com/ai-marketing"
            }],
            "auto_activate": False  # Keep paused for testing
        }
        
        # Execute workflow
        result = await linkedin.execute_campaign_workflow(workflow_data)
        print(f"Workflow execution result: {json.dumps(result, indent=2)}")
        
        # Get insights
        insights_result = await linkedin.get_comprehensive_insights({
            "date_range": {
                "start_day": "1",
                "start_month": str((datetime.now() - timedelta(days=30)).month),
                "start_year": str((datetime.now() - timedelta(days=30)).year),
                "end_day": str(datetime.now().day),
                "end_month": str(datetime.now().month),
                "end_year": str(datetime.now().year)
            }
        })
        print(f"Comprehensive insights: {json.dumps(insights_result, indent=2)}")
        
        return True
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Run tests
    asyncio.run(test_linkedin_integration())
#!/usr/bin/env python3

"""
BizOSaaS Data Synchronization - API Integration Module
Cross-platform API integration and data exchange
"""

import asyncio
import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from enum import Enum

import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class APIEndpointType(str, Enum):
    USERS = "users"
    LEADS = "leads"
    ORDERS = "orders"
    PRODUCTS = "products"
    CAMPAIGNS = "campaigns"
    ANALYTICS = "analytics"

class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

@dataclass
class APIEndpoint:
    platform: str
    endpoint_type: APIEndpointType
    method: HTTPMethod
    url: str
    headers: Dict[str, str]
    auth_required: bool = True
    rate_limit: Optional[int] = None
    timeout: int = 30

@dataclass
class APIResponse:
    success: bool
    status_code: int
    data: Dict[str, Any]
    headers: Dict[str, str]
    response_time_ms: int
    error_message: Optional[str] = None

class PlatformAPIClient:
    """Generic API client for platform integrations"""
    
    def __init__(self, platform: str, base_url: str, auth_token: str = ""):
        self.platform = platform
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.session = None
        self.endpoints = self._load_endpoints()
        
    def _load_endpoints(self) -> Dict[APIEndpointType, APIEndpoint]:
        """Load platform-specific API endpoints"""
        
        if self.platform == "bizoholic":
            return {
                APIEndpointType.USERS: APIEndpoint(
                    platform="bizoholic",
                    endpoint_type=APIEndpointType.USERS,
                    method=HTTPMethod.GET,
                    url=f"{self.base_url}/api/users",
                    headers={"Content-Type": "application/json"},
                    rate_limit=100
                ),
                APIEndpointType.LEADS: APIEndpoint(
                    platform="bizoholic",
                    endpoint_type=APIEndpointType.LEADS,
                    method=HTTPMethod.GET,
                    url=f"{self.base_url}/api/leads",
                    headers={"Content-Type": "application/json"},
                    rate_limit=100
                ),
                APIEndpointType.CAMPAIGNS: APIEndpoint(
                    platform="bizoholic",
                    endpoint_type=APIEndpointType.CAMPAIGNS,
                    method=HTTPMethod.GET,
                    url=f"{self.base_url}/api/campaigns",
                    headers={"Content-Type": "application/json"},
                    rate_limit=50
                ),
                APIEndpointType.ANALYTICS: APIEndpoint(
                    platform="bizoholic",
                    endpoint_type=APIEndpointType.ANALYTICS,
                    method=HTTPMethod.GET,
                    url=f"{self.base_url}/api/analytics",
                    headers={"Content-Type": "application/json"},
                    rate_limit=20
                )
            }
        
        elif self.platform == "coreldove":
            return {
                APIEndpointType.USERS: APIEndpoint(
                    platform="coreldove",
                    endpoint_type=APIEndpointType.USERS,
                    method=HTTPMethod.POST,
                    url=f"{self.base_url}/graphql",
                    headers={"Content-Type": "application/json"},
                    rate_limit=100
                ),
                APIEndpointType.PRODUCTS: APIEndpoint(
                    platform="coreldove",
                    endpoint_type=APIEndpointType.PRODUCTS,
                    method=HTTPMethod.POST,
                    url=f"{self.base_url}/graphql",
                    headers={"Content-Type": "application/json"},
                    rate_limit=100
                ),
                APIEndpointType.ORDERS: APIEndpoint(
                    platform="coreldove",
                    endpoint_type=APIEndpointType.ORDERS,
                    method=HTTPMethod.POST,
                    url=f"{self.base_url}/graphql",
                    headers={"Content-Type": "application/json"},
                    rate_limit=50
                ),
                APIEndpointType.ANALYTICS: APIEndpoint(
                    platform="coreldove",
                    endpoint_type=APIEndpointType.ANALYTICS,
                    method=HTTPMethod.POST,
                    url=f"{self.base_url}/graphql",
                    headers={"Content-Type": "application/json"},
                    rate_limit=20
                )
            }
        
        elif self.platform == "bizosaas":
            return {
                APIEndpointType.USERS: APIEndpoint(
                    platform="bizosaas",
                    endpoint_type=APIEndpointType.USERS,
                    method=HTTPMethod.GET,
                    url=f"{self.base_url}/api/brain/django-crm/contacts",
                    headers={"Content-Type": "application/json"},
                    rate_limit=200
                ),
                APIEndpointType.LEADS: APIEndpoint(
                    platform="bizosaas",
                    endpoint_type=APIEndpointType.LEADS,
                    method=HTTPMethod.GET,
                    url=f"{self.base_url}/api/brain/django-crm/leads",
                    headers={"Content-Type": "application/json"},
                    rate_limit=200
                ),
                APIEndpointType.ANALYTICS: APIEndpoint(
                    platform="bizosaas",
                    endpoint_type=APIEndpointType.ANALYTICS,
                    method=HTTPMethod.GET,
                    url=f"{self.base_url}/api/brain/superset/dashboards",
                    headers={"Content-Type": "application/json"},
                    rate_limit=50
                )
            }
        
        return {}
    
    async def initialize(self):
        """Initialize HTTP session"""
        self.session = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
        )
        logger.info(f"✅ Initialized API client for {self.platform}")
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.aclose()
        logger.info(f"🔄 Closed API client for {self.platform}")
    
    async def make_request(self, 
                          endpoint_type: APIEndpointType,
                          method: Optional[HTTPMethod] = None,
                          data: Optional[Dict[str, Any]] = None,
                          params: Optional[Dict[str, Any]] = None,
                          custom_headers: Optional[Dict[str, str]] = None) -> APIResponse:
        """Make API request to platform endpoint"""
        
        if not self.session:
            await self.initialize()
        
        endpoint = self.endpoints.get(endpoint_type)
        if not endpoint:
            return APIResponse(
                success=False,
                status_code=404,
                data={},
                headers={},
                response_time_ms=0,
                error_message=f"Endpoint {endpoint_type} not configured for {self.platform}"
            )
        
        # Prepare request
        url = endpoint.url
        headers = endpoint.headers.copy()
        
        # Add authentication
        if endpoint.auth_required and self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        # Add custom headers
        if custom_headers:
            headers.update(custom_headers)
        
        # Use endpoint method or override
        request_method = method.value if method else endpoint.method.value
        
        start_time = datetime.now()
        
        try:
            # Handle GraphQL requests (CoreLDove)
            if self.platform == "coreldove" and endpoint_type in [
                APIEndpointType.USERS, APIEndpointType.PRODUCTS, APIEndpointType.ORDERS
            ]:
                query_data = self._build_graphql_query(endpoint_type, data, params)
                response = await self.session.post(url, json=query_data, headers=headers)
            else:
                # Handle REST requests
                if request_method == "GET":
                    response = await self.session.get(url, params=params, headers=headers)
                elif request_method == "POST":
                    response = await self.session.post(url, json=data, params=params, headers=headers)
                elif request_method == "PUT":
                    response = await self.session.put(url, json=data, params=params, headers=headers)
                elif request_method == "PATCH":
                    response = await self.session.patch(url, json=data, params=params, headers=headers)
                elif request_method == "DELETE":
                    response = await self.session.delete(url, params=params, headers=headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {request_method}")
            
            response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            
            # Parse response
            try:
                response_data = response.json()
            except:
                response_data = {"text": response.text}
            
            return APIResponse(
                success=response.is_success,
                status_code=response.status_code,
                data=response_data,
                headers=dict(response.headers),
                response_time_ms=response_time_ms,
                error_message=None if response.is_success else f"HTTP {response.status_code}: {response.text}"
            )
            
        except Exception as e:
            response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            
            return APIResponse(
                success=False,
                status_code=0,
                data={},
                headers={},
                response_time_ms=response_time_ms,
                error_message=str(e)
            )
    
    def _build_graphql_query(self, 
                           endpoint_type: APIEndpointType,
                           data: Optional[Dict[str, Any]] = None,
                           params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build GraphQL query for CoreLDove platform"""
        
        if endpoint_type == APIEndpointType.USERS:
            if data:  # Create/Update user
                return {
                    "query": """
                        mutation createUser($input: UserInput!) {
                            userCreate(input: $input) {
                                user {
                                    id
                                    email
                                    firstName
                                    lastName
                                    isActive
                                }
                                errors {
                                    field
                                    message
                                }
                            }
                        }
                    """,
                    "variables": {"input": data}
                }
            else:  # Query users
                return {
                    "query": """
                        query getUsers($first: Int, $filter: UserFilterInput) {
                            users(first: $first, filter: $filter) {
                                edges {
                                    node {
                                        id
                                        email
                                        firstName
                                        lastName
                                        isActive
                                        dateJoined
                                    }
                                }
                                pageInfo {
                                    hasNextPage
                                    hasPreviousPage
                                }
                            }
                        }
                    """,
                    "variables": params or {"first": 50}
                }
        
        elif endpoint_type == APIEndpointType.PRODUCTS:
            if data:  # Create/Update product
                return {
                    "query": """
                        mutation createProduct($input: ProductInput!) {
                            productCreate(input: $input) {
                                product {
                                    id
                                    name
                                    slug
                                    description
                                    isPublished
                                }
                                errors {
                                    field
                                    message
                                }
                            }
                        }
                    """,
                    "variables": {"input": data}
                }
            else:  # Query products
                return {
                    "query": """
                        query getProducts($first: Int, $filter: ProductFilterInput) {
                            products(first: $first, filter: $filter) {
                                edges {
                                    node {
                                        id
                                        name
                                        slug
                                        description
                                        isPublished
                                        defaultVariant {
                                            id
                                            pricing {
                                                price {
                                                    amount
                                                    currency
                                                }
                                            }
                                        }
                                    }
                                }
                                pageInfo {
                                    hasNextPage
                                    hasPreviousPage
                                }
                            }
                        }
                    """,
                    "variables": params or {"first": 50}
                }
        
        elif endpoint_type == APIEndpointType.ORDERS:
            if data:  # Create order
                return {
                    "query": """
                        mutation createOrder($input: OrderCreateInput!) {
                            orderCreate(input: $input) {
                                order {
                                    id
                                    number
                                    status
                                    total {
                                        amount
                                        currency
                                    }
                                }
                                errors {
                                    field
                                    message
                                }
                            }
                        }
                    """,
                    "variables": {"input": data}
                }
            else:  # Query orders
                return {
                    "query": """
                        query getOrders($first: Int, $filter: OrderFilterInput) {
                            orders(first: $first, filter: $filter) {
                                edges {
                                    node {
                                        id
                                        number
                                        status
                                        created
                                        total {
                                            amount
                                            currency
                                        }
                                        user {
                                            id
                                            email
                                        }
                                    }
                                }
                                pageInfo {
                                    hasNextPage
                                    hasPreviousPage
                                }
                            }
                        }
                    """,
                    "variables": params or {"first": 50}
                }
        
        return {"query": "", "variables": {}}

class CrossPlatformAPIManager:
    """Manages API integrations across all platforms"""
    
    def __init__(self, db_pool, redis_client):
        self.db_pool = db_pool
        self.redis_client = redis_client
        self.clients = {}
        self.rate_limiters = {}
        
    async def initialize(self, platform_configs: Dict[str, Dict[str, str]]):
        """Initialize API clients for all platforms"""
        
        for platform, config in platform_configs.items():
            client = PlatformAPIClient(
                platform=platform,
                base_url=config["base_url"],
                auth_token=config.get("auth_token", "")
            )
            
            await client.initialize()
            self.clients[platform] = client
            
            # Initialize rate limiter for platform
            self.rate_limiters[platform] = RateLimiter(
                platform=platform,
                redis_client=self.redis_client
            )
        
        logger.info(f"✅ Initialized API clients for {len(self.clients)} platforms")
    
    async def close_all(self):
        """Close all API clients"""
        for client in self.clients.values():
            await client.close()
        logger.info("🔄 Closed all API clients")
    
    async def sync_data(self, 
                       source_platform: str,
                       target_platforms: List[str],
                       endpoint_type: APIEndpointType,
                       data: Dict[str, Any],
                       sync_mode: str = "create") -> Dict[str, APIResponse]:
        """Sync data across platforms"""
        
        results = {}
        
        for target_platform in target_platforms:
            if target_platform == source_platform:
                continue
            
            if target_platform not in self.clients:
                logger.warning(f"No API client for {target_platform}")
                continue
            
            # Check rate limits
            if not await self.rate_limiters[target_platform].can_make_request(endpoint_type):
                logger.warning(f"Rate limit exceeded for {target_platform} {endpoint_type}")
                results[target_platform] = APIResponse(
                    success=False,
                    status_code=429,
                    data={},
                    headers={},
                    response_time_ms=0,
                    error_message="Rate limit exceeded"
                )
                continue
            
            # Transform data for target platform
            transformed_data = await self._transform_data_for_platform(
                data, source_platform, target_platform, endpoint_type
            )
            
            # Determine HTTP method based on sync mode
            method = self._get_sync_method(sync_mode)
            
            # Make API request
            client = self.clients[target_platform]
            response = await client.make_request(
                endpoint_type=endpoint_type,
                method=method,
                data=transformed_data
            )
            
            results[target_platform] = response
            
            # Update rate limiter
            await self.rate_limiters[target_platform].record_request(endpoint_type)
            
            # Log result
            if response.success:
                logger.info(f"✅ Synced {endpoint_type} to {target_platform}")
            else:
                logger.error(f"❌ Failed to sync {endpoint_type} to {target_platform}: {response.error_message}")
        
        return results
    
    async def fetch_data(self, 
                        platform: str,
                        endpoint_type: APIEndpointType,
                        params: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Fetch data from specific platform"""
        
        if platform not in self.clients:
            return APIResponse(
                success=False,
                status_code=404,
                data={},
                headers={},
                response_time_ms=0,
                error_message=f"No API client for {platform}"
            )
        
        # Check rate limits
        if not await self.rate_limiters[platform].can_make_request(endpoint_type):
            return APIResponse(
                success=False,
                status_code=429,
                data={},
                headers={},
                response_time_ms=0,
                error_message="Rate limit exceeded"
            )
        
        client = self.clients[platform]
        response = await client.make_request(
            endpoint_type=endpoint_type,
            method=HTTPMethod.GET,
            params=params
        )
        
        # Update rate limiter
        await self.rate_limiters[platform].record_request(endpoint_type)
        
        return response
    
    async def bulk_sync(self, 
                       source_platform: str,
                       target_platforms: List[str],
                       endpoint_type: APIEndpointType,
                       data_list: List[Dict[str, Any]],
                       batch_size: int = 10) -> Dict[str, List[APIResponse]]:
        """Perform bulk synchronization with batching"""
        
        results = {platform: [] for platform in target_platforms}
        
        # Process in batches
        for i in range(0, len(data_list), batch_size):
            batch = data_list[i:i + batch_size]
            
            # Sync batch concurrently
            tasks = []
            for data in batch:
                task = self.sync_data(
                    source_platform=source_platform,
                    target_platforms=target_platforms,
                    endpoint_type=endpoint_type,
                    data=data
                )
                tasks.append(task)
            
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Collect results
            for data_results in batch_results:
                if isinstance(data_results, dict):
                    for platform, response in data_results.items():
                        results[platform].append(response)
            
            # Add delay between batches to respect rate limits
            await asyncio.sleep(1)
        
        return results
    
    async def _transform_data_for_platform(self,
                                         data: Dict[str, Any],
                                         source_platform: str,
                                         target_platform: str,
                                         endpoint_type: APIEndpointType) -> Dict[str, Any]:
        """Transform data for target platform API format"""
        
        # Platform-specific transformations
        if target_platform == "coreldove":
            # Transform for GraphQL format
            if endpoint_type == APIEndpointType.USERS:
                return {
                    "email": data.get("email"),
                    "firstName": data.get("name", "").split()[0] if data.get("name") else "",
                    "lastName": " ".join(data.get("name", "").split()[1:]) if data.get("name") else "",
                    "isActive": data.get("status") == "active"
                }
            elif endpoint_type == APIEndpointType.PRODUCTS:
                return {
                    "name": data.get("name"),
                    "description": data.get("description", ""),
                    "slug": data.get("slug", data.get("name", "").lower().replace(" ", "-")),
                    "isPublished": data.get("status") == "published"
                }
        
        elif target_platform == "bizoholic":
            # Transform for marketing platform
            if endpoint_type == APIEndpointType.LEADS:
                return {
                    "name": data.get("name"),
                    "email": data.get("email"),
                    "phone": data.get("phone"),
                    "source": "cross_platform_sync",
                    "score": data.get("score", 0),
                    "status": data.get("status", "new")
                }
            elif endpoint_type == APIEndpointType.CAMPAIGNS:
                return {
                    "name": data.get("name"),
                    "budget": data.get("budget"),
                    "status": data.get("status"),
                    "platform": source_platform
                }
        
        elif target_platform == "bizosaas":
            # Transform for unified platform
            return {
                **data,
                "_sync_metadata": {
                    "source_platform": source_platform,
                    "synced_at": datetime.now(timezone.utc).isoformat()
                }
            }
        
        return data
    
    def _get_sync_method(self, sync_mode: str) -> HTTPMethod:
        """Get HTTP method for sync mode"""
        method_mapping = {
            "create": HTTPMethod.POST,
            "update": HTTPMethod.PUT,
            "patch": HTTPMethod.PATCH,
            "delete": HTTPMethod.DELETE
        }
        return method_mapping.get(sync_mode, HTTPMethod.POST)

class RateLimiter:
    """Rate limiter for API requests"""
    
    def __init__(self, platform: str, redis_client):
        self.platform = platform
        self.redis_client = redis_client
        self.limits = self._get_rate_limits()
    
    def _get_rate_limits(self) -> Dict[APIEndpointType, Dict[str, int]]:
        """Get rate limits for platform endpoints"""
        
        # Default limits (requests per minute)
        default_limits = {
            APIEndpointType.USERS: {"requests": 100, "window": 60},
            APIEndpointType.LEADS: {"requests": 100, "window": 60},
            APIEndpointType.PRODUCTS: {"requests": 100, "window": 60},
            APIEndpointType.ORDERS: {"requests": 50, "window": 60},
            APIEndpointType.CAMPAIGNS: {"requests": 50, "window": 60},
            APIEndpointType.ANALYTICS: {"requests": 20, "window": 60}
        }
        
        # Platform-specific overrides
        if self.platform == "coreldove":
            # GraphQL might have different limits
            default_limits[APIEndpointType.PRODUCTS]["requests"] = 200
        elif self.platform == "bizosaas":
            # Internal API can handle more requests
            for endpoint_type in default_limits:
                default_limits[endpoint_type]["requests"] *= 2
        
        return default_limits
    
    async def can_make_request(self, endpoint_type: APIEndpointType) -> bool:
        """Check if request can be made within rate limits"""
        
        if endpoint_type not in self.limits:
            return True
        
        limit_config = self.limits[endpoint_type]
        key = f"rate_limit:{self.platform}:{endpoint_type.value}"
        
        try:
            current_count = await self.redis_client.get(key)
            current_count = int(current_count) if current_count else 0
            
            return current_count < limit_config["requests"]
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True  # Allow request if rate limiter fails
    
    async def record_request(self, endpoint_type: APIEndpointType):
        """Record a request for rate limiting"""
        
        if endpoint_type not in self.limits:
            return
        
        limit_config = self.limits[endpoint_type]
        key = f"rate_limit:{self.platform}:{endpoint_type.value}"
        
        try:
            # Increment counter with expiration
            await self.redis_client.incr(key)
            await self.redis_client.expire(key, limit_config["window"])
            
        except Exception as e:
            logger.error(f"Error recording request: {e}")

# Utility functions for API testing
async def test_platform_connectivity(api_manager: CrossPlatformAPIManager) -> Dict[str, bool]:
    """Test connectivity to all platforms"""
    
    results = {}
    
    for platform, client in api_manager.clients.items():
        try:
            # Make a simple health check request
            response = await client.make_request(
                endpoint_type=APIEndpointType.USERS,
                method=HTTPMethod.GET,
                params={"limit": 1}
            )
            
            results[platform] = response.success and response.status_code in [200, 201]
            
        except Exception as e:
            logger.error(f"Connectivity test failed for {platform}: {e}")
            results[platform] = False
    
    return results

async def benchmark_api_performance(api_manager: CrossPlatformAPIManager,
                                  platform: str,
                                  endpoint_type: APIEndpointType,
                                  num_requests: int = 10) -> Dict[str, float]:
    """Benchmark API performance"""
    
    if platform not in api_manager.clients:
        return {"error": "Platform not available"}
    
    response_times = []
    success_count = 0
    
    for _ in range(num_requests):
        response = await api_manager.fetch_data(platform, endpoint_type, {"limit": 1})
        response_times.append(response.response_time_ms)
        
        if response.success:
            success_count += 1
        
        # Small delay between requests
        await asyncio.sleep(0.1)
    
    return {
        "avg_response_time_ms": sum(response_times) / len(response_times),
        "min_response_time_ms": min(response_times),
        "max_response_time_ms": max(response_times),
        "success_rate": success_count / num_requests,
        "total_requests": num_requests
    }
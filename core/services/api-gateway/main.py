"""
API Gateway Service - BizoholicSaaS
Central routing, authentication, and load balancing for all microservices
Port: 8080
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from typing import Dict, Any, Optional
import logging
import time
from datetime import datetime
import asyncio
import json

# Shared imports
import sys
import os
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

# Import auth endpoints
from auth_endpoints import router as auth_router

# Try to import shared modules, but don't fail if they don't exist
try:
    from shared.auth.jwt_auth import get_current_user, UserContext, ServiceAuthToken
    from shared.database.connection import get_redis_client, init_database
except ImportError as e:
    logger.warning(f"Could not import shared modules: {e}")
    get_current_user = None
    UserContext = None
    ServiceAuthToken = None
    get_redis_client = None
    init_database = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Gateway - BizoholicSaaS",
    description="Central API Gateway for microservices routing and authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include authentication router
app.include_router(auth_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
redis_client = None
http_client = None

# Service configuration
SERVICES_CONFIG = {
    "ai-agents": {
        "base_url": "http://localhost:8002",
        "health_endpoint": "/health",
        "routes": ["/agents", "/onboarding", "/workflows"],
        "public_routes": [],
        "timeout": 120  # AI tasks can take longer
    },
    "business-directory": {
        "base_url": "http://localhost:8003",
        "health_endpoint": "/health", 
        "routes": ["/directory", "/listings", "/search"],
        "public_routes": [],
        "timeout": 45
    },
    "payment-service": {
        "base_url": "http://localhost:8004",
        "health_endpoint": "/health",
        "routes": ["/payments", "/subscriptions", "/billing"],
        "public_routes": [],
        "timeout": 30
    },
    "wagtail-cms": {
        "base_url": "http://localhost:8005",
        "health_endpoint": "/health",
        "routes": ["/api", "/admin", "/cms"],
        "public_routes": [],
        "timeout": 30
    },
    "marketing-apis": {
        "base_url": "http://localhost:8008",
        "health_endpoint": "/health",
        "routes": ["/campaigns", "/analytics", "/leads"],
        "public_routes": [],
        "timeout": 60
    },
    "amazon-integration": {
        "base_url": "http://localhost:8009",
        "health_endpoint": "/health",
        "routes": ["/products", "/orders", "/inventory"],
        "public_routes": [],
        "timeout": 45
    }
}

# Rate limiting configuration
RATE_LIMITS = {
    "default": {"requests": 100, "window": 60},  # 100 requests per minute
    "auth": {"requests": 10, "window": 60},      # 10 auth requests per minute  
    "ai-agents": {"requests": 20, "window": 60}, # 20 AI requests per minute
    "webhooks": {"requests": 1000, "window": 60} # Higher limit for webhooks
}

# Circuit breaker configuration
CIRCUIT_BREAKER_CONFIG = {
    "failure_threshold": 5,  # Number of failures before opening circuit
    "recovery_timeout": 30,  # Seconds before trying to close circuit
    "success_threshold": 3   # Successful requests needed to close circuit
}

class CircuitBreakerState:
    """Circuit breaker state management"""
    
    def __init__(self):
        self.states = {}  # service_name -> {state, failures, last_failure, successes}
    
    def get_state(self, service_name: str) -> str:
        """Get current circuit breaker state for service"""
        if service_name not in self.states:
            self.states[service_name] = {
                "state": "closed",
                "failures": 0,
                "last_failure": None,
                "successes": 0
            }
        
        state_info = self.states[service_name]
        
        # Check if we should move from open to half-open
        if (state_info["state"] == "open" and 
            state_info["last_failure"] and
            time.time() - state_info["last_failure"] > CIRCUIT_BREAKER_CONFIG["recovery_timeout"]):
            state_info["state"] = "half-open"
            state_info["successes"] = 0
        
        return state_info["state"]
    
    def record_success(self, service_name: str):
        """Record successful request"""
        if service_name not in self.states:
            return
        
        state_info = self.states[service_name]
        state_info["failures"] = 0
        
        if state_info["state"] == "half-open":
            state_info["successes"] += 1
            if state_info["successes"] >= CIRCUIT_BREAKER_CONFIG["success_threshold"]:
                state_info["state"] = "closed"
                state_info["successes"] = 0
    
    def record_failure(self, service_name: str):
        """Record failed request"""
        if service_name not in self.states:
            self.states[service_name] = {
                "state": "closed",
                "failures": 0,
                "last_failure": None,
                "successes": 0
            }
        
        state_info = self.states[service_name]
        state_info["failures"] += 1
        state_info["last_failure"] = time.time()
        
        if state_info["failures"] >= CIRCUIT_BREAKER_CONFIG["failure_threshold"]:
            state_info["state"] = "open"

circuit_breaker = CircuitBreakerState()

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize connections and services"""
    global redis_client, http_client
    
    try:
        # Initialize HTTP client for service requests (always needed)
        http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(60.0),
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
        )
        
        # Try to initialize database connections (optional for basic functionality)
        try:
            await init_database()
            redis_client = await get_redis_client()
            logger.info("Database connections initialized successfully")
        except Exception as db_error:
            logger.warning(f"Database initialization failed, continuing without it: {db_error}")
            redis_client = None
        
        logger.info("API Gateway initialized successfully")
        
        # Start health check background task
        asyncio.create_task(health_check_services())
        
    except Exception as e:
        logger.error(f"API Gateway startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown"""
    global http_client
    
    if http_client:
        await http_client.aclose()
    
    logger.info("API Gateway shutdown complete")

# Health check endpoints
@app.get("/health")
async def health_check():
    """API Gateway health check"""
    return {
        "status": "healthy",
        "service": "api-gateway",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health/services")
async def services_health_check():
    """Check health of all downstream services"""
    
    health_status = {}
    
    for service_name, config in SERVICES_CONFIG.items():
        try:
            circuit_state = circuit_breaker.get_state(service_name)
            
            if circuit_state == "open":
                health_status[service_name] = {
                    "status": "circuit_open",
                    "available": False,
                    "circuit_state": circuit_state
                }
                continue
            
            # Check service health
            health_url = f"{config['base_url']}{config['health_endpoint']}"
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(health_url)
                
                if response.status_code == 200:
                    health_status[service_name] = {
                        "status": "healthy",
                        "available": True,
                        "circuit_state": circuit_state,
                        "response_time": response.elapsed.total_seconds()
                    }
                    circuit_breaker.record_success(service_name)
                else:
                    health_status[service_name] = {
                        "status": "unhealthy",
                        "available": False,
                        "circuit_state": circuit_state,
                        "status_code": response.status_code
                    }
                    circuit_breaker.record_failure(service_name)
                    
        except Exception as e:
            health_status[service_name] = {
                "status": "error",
                "available": False,
                "circuit_state": circuit_breaker.get_state(service_name),
                "error": str(e)
            }
            circuit_breaker.record_failure(service_name)
    
    # Overall health
    all_healthy = all(service["available"] for service in health_status.values())
    
    return {
        "overall_status": "healthy" if all_healthy else "degraded",
        "services": health_status,
        "timestamp": datetime.utcnow().isoformat()
    }

# Rate limiting middleware
async def check_rate_limit(request: Request, service_name: str = "default") -> bool:
    """Check if request is within rate limits"""
    
    # If Redis is not available, allow all requests
    if not redis_client:
        return True
    
    try:
        # Get client identifier (IP or user ID)
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "unknown")
        client_id = f"{client_ip}:{hash(user_agent) % 1000}"
        
        # Determine rate limit based on service and endpoint
        rate_limit_key = service_name
        if "auth" in str(request.url.path):
            rate_limit_key = "auth"
        elif "webhooks" in str(request.url.path):
            rate_limit_key = "webhooks"
        
        limits = RATE_LIMITS.get(rate_limit_key, RATE_LIMITS["default"])
        
        # Check rate limit in Redis
        redis_key = f"rate_limit:{rate_limit_key}:{client_id}"
        
        # Use Redis sliding window
        current_time = int(time.time())
        window_start = current_time - limits["window"]
        
        # Remove old entries
        await redis_client.zremrangebyscore(redis_key, 0, window_start)
        
        # Count current requests
        current_requests = await redis_client.zcard(redis_key)
        
        if current_requests >= limits["requests"]:
            return False
        
        # Add current request
        await redis_client.zadd(redis_key, {str(current_time): current_time})
        await redis_client.expire(redis_key, limits["window"])
        
        return True
        
    except Exception as e:
        logger.error(f"Rate limit check error: {e}")
        return True  # Allow request if rate limiting fails

# Authentication middleware
async def authenticate_request(request: Request) -> Optional[UserContext]:
    """Authenticate request and return user context"""
    
    try:
        # Check if route is public
        path = str(request.url.path)
        
        for service_name, config in SERVICES_CONFIG.items():
            for public_route in config.get("public_routes", []):
                if path.startswith(public_route):
                    return None  # Public route, no auth needed
        
        # Get authorization header
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        # Extract and validate token
        token = auth_header.replace("Bearer ", "")
        
        # Use shared JWT validation
        from shared.auth.jwt_auth import jwt_manager
        token_data = jwt_manager.verify_token(token)
        
        return UserContext(
            user_id=token_data.user_id,
            tenant_id=token_data.tenant_id,
            email=token_data.email,
            role=token_data.role,
            permissions=token_data.permissions
        )
        
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return None

# Service routing
async def route_request(request: Request, service_name: str, path: str) -> Response:
    """Route request to appropriate microservice"""
    
    try:
        # Check circuit breaker
        circuit_state = circuit_breaker.get_state(service_name)
        if circuit_state == "open":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Service {service_name} is temporarily unavailable"
            )
        
        config = SERVICES_CONFIG[service_name]
        target_url = f"{config['base_url']}{path}"
        
        # Get request body
        body = await request.body()
        
        # Prepare headers (remove hop-by-hop headers)
        headers = dict(request.headers)
        headers.pop("host", None)
        headers.pop("content-length", None)
        
        # Add service-to-service authentication
        service_token = ServiceAuthToken.create_service_token(
            service_name="api-gateway",
            target_service=service_name
        )
        headers["x-service-auth"] = service_token
        
        # Make request to service
        start_time = time.time()
        
        async with httpx.AsyncClient(timeout=config.get("timeout", 30)) as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=dict(request.query_params)
            )
        
        # Record metrics
        duration = time.time() - start_time
        await record_request_metrics(service_name, response.status_code, duration)
        
        # Update circuit breaker
        if response.status_code < 500:
            circuit_breaker.record_success(service_name)
        else:
            circuit_breaker.record_failure(service_name)
        
        # Return response
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type")
        )
        
    except httpx.TimeoutException:
        circuit_breaker.record_failure(service_name)
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Request to {service_name} timed out"
        )
    except httpx.ConnectError:
        circuit_breaker.record_failure(service_name)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not connect to {service_name}"
        )
    except Exception as e:
        circuit_breaker.record_failure(service_name)
        logger.error(f"Routing error for {service_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error routing request to {service_name}"
        )

async def record_request_metrics(service_name: str, status_code: int, duration: float):
    """Record request metrics in Redis"""
    
    # Skip metrics if Redis is not available
    if not redis_client:
        return
    
    try:
        current_time = int(time.time())
        
        # Record request count
        await redis_client.hincrby("gateway:metrics:requests", service_name, 1)
        
        # Record response time
        await redis_client.hset("gateway:metrics:response_times", service_name, duration)
        
        # Record status code
        status_key = f"{service_name}:{status_code}"
        await redis_client.hincrby("gateway:metrics:status_codes", status_key, 1)
        
        # Record in time series (for monitoring)
        ts_key = f"gateway:timeseries:{service_name}:{current_time // 60}"  # Per minute
        await redis_client.zadd(ts_key, {str(current_time): duration})
        await redis_client.expire(ts_key, 3600)  # Keep for 1 hour
        
    except Exception as e:
        logger.error(f"Record metrics error: {e}")

# Dynamic routing based on path (excluding gateway management endpoints)
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def dynamic_router(request: Request, path: str):
    """Dynamic router for all service requests"""
    
    try:
        # Add leading slash if not present
        if not path.startswith("/"):
            path = "/" + path
        
        # Gateway management routes are handled by dedicated endpoints
        
        # Determine target service based on path
        service_name = None
        for svc_name, config in SERVICES_CONFIG.items():
            for route in config["routes"]:
                if path.startswith(route):
                    service_name = svc_name
                    break
            if service_name:
                break
        
        if not service_name:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found for this path"
            )
        
        # Check rate limits
        rate_limit_ok = await check_rate_limit(request, service_name)
        if not rate_limit_ok:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
        
        # Authenticate request if needed
        user_context = await authenticate_request(request)
        
        # Check if authentication is required
        is_public = False
        for public_route in SERVICES_CONFIG[service_name].get("public_routes", []):
            if path.startswith(public_route):
                is_public = True
                break
        
        if not is_public and not user_context:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        # Route request to service
        response = await route_request(request, service_name, path)
        
        # Add headers
        response.headers["x-gateway-service"] = service_name
        response.headers["x-gateway-timestamp"] = str(int(time.time()))
        
        if user_context:
            response.headers["x-user-id"] = user_context.user_id
            response.headers["x-tenant-id"] = user_context.tenant_id
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dynamic router error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal gateway error"
        )

# Metrics and monitoring endpoints
@app.get("/gateway/metrics")
async def get_gateway_metrics():
    """Get API Gateway metrics"""
    
    try:
        if not redis_client:
            return {
                "total_requests": 0,
                "requests_by_service": {},
                "average_response_time": 0,
                "response_times_by_service": {},
                "status_codes": {},
                "circuit_breaker_states": {
                    service: circuit_breaker.get_state(service) 
                    for service in SERVICES_CONFIG.keys()
                },
                "redis_available": False,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get request counts
        request_counts = await redis_client.hgetall("gateway:metrics:requests")
        
        # Get response times
        response_times = await redis_client.hgetall("gateway:metrics:response_times")
        
        # Get status codes
        status_codes = await redis_client.hgetall("gateway:metrics:status_codes")
        
        # Calculate derived metrics
        total_requests = sum(int(count) for count in request_counts.values())
        avg_response_time = sum(float(time) for time in response_times.values()) / len(response_times) if response_times else 0
        
        return {
            "total_requests": total_requests,
            "requests_by_service": {k: int(v) for k, v in request_counts.items()},
            "average_response_time": round(avg_response_time, 3),
            "response_times_by_service": {k: float(v) for k, v in response_times.items()},
            "status_codes": {k: int(v) for k, v in status_codes.items()},
            "circuit_breaker_states": {
                service: circuit_breaker.get_state(service) 
                for service in SERVICES_CONFIG.keys()
            },
            "redis_available": True,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Get gateway metrics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get metrics"
        )

@app.get("/gateway/config")
async def get_gateway_config():
    """Get current gateway configuration"""
    
    return {
        "services": {
            service: {
                "base_url": config["base_url"],
                "routes": config["routes"],
                "public_routes": config.get("public_routes", []),
                "timeout": config.get("timeout", 30)
            }
            for service, config in SERVICES_CONFIG.items()
        },
        "rate_limits": RATE_LIMITS,
        "circuit_breaker": CIRCUIT_BREAKER_CONFIG,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/gateway/circuit-breaker/{service_name}/reset")
async def reset_circuit_breaker(service_name: str):
    """Reset circuit breaker for a service"""
    
    if service_name not in SERVICES_CONFIG:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Reset circuit breaker state
    if service_name in circuit_breaker.states:
        circuit_breaker.states[service_name] = {
            "state": "closed",
            "failures": 0,
            "last_failure": None,
            "successes": 0
        }
    
    return {
        "message": f"Circuit breaker reset for {service_name}",
        "service": service_name,
        "new_state": "closed"
    }

# Load balancing (for future use with multiple service instances)
class LoadBalancer:
    """Simple round-robin load balancer"""
    
    def __init__(self):
        self.service_instances = {}  # service_name -> [list of instances]
        self.current_instance = {}   # service_name -> current_index
    
    def add_instance(self, service_name: str, instance_url: str):
        """Add service instance"""
        if service_name not in self.service_instances:
            self.service_instances[service_name] = []
            self.current_instance[service_name] = 0
        
        if instance_url not in self.service_instances[service_name]:
            self.service_instances[service_name].append(instance_url)
    
    def get_instance(self, service_name: str) -> str:
        """Get next instance using round-robin"""
        if service_name not in self.service_instances:
            return SERVICES_CONFIG[service_name]["base_url"]
        
        instances = self.service_instances[service_name]
        if not instances:
            return SERVICES_CONFIG[service_name]["base_url"]
        
        current = self.current_instance[service_name]
        instance = instances[current]
        
        # Move to next instance
        self.current_instance[service_name] = (current + 1) % len(instances)
        
        return instance

load_balancer = LoadBalancer()

# Background health check task
async def health_check_services():
    """Background task to continuously check service health"""
    
    while True:
        try:
            await asyncio.sleep(30)  # Check every 30 seconds
            
            for service_name, config in SERVICES_CONFIG.items():
                try:
                    health_url = f"{config['base_url']}{config['health_endpoint']}"
                    
                    async with httpx.AsyncClient(timeout=5.0) as client:
                        response = await client.get(health_url)
                        
                        if response.status_code == 200:
                            circuit_breaker.record_success(service_name)
                            
                            # Cache health status if Redis is available
                            if redis_client:
                                await redis_client.hset(
                                    "gateway:service_health",
                                    service_name,
                                    json.dumps({
                                        "status": "healthy",
                                        "last_check": datetime.utcnow().isoformat(),
                                        "response_time": response.elapsed.total_seconds()
                                    })
                                )
                        else:
                            circuit_breaker.record_failure(service_name)
                            
                            if redis_client:
                                await redis_client.hset(
                                    "gateway:service_health", 
                                    service_name,
                                    json.dumps({
                                        "status": "unhealthy",
                                        "last_check": datetime.utcnow().isoformat(),
                                        "status_code": response.status_code
                                    })
                                )
                            
                except Exception as e:
                    circuit_breaker.record_failure(service_name)
                    
                    if redis_client:
                        await redis_client.hset(
                            "gateway:service_health",
                            service_name, 
                            json.dumps({
                                "status": "error",
                                "last_check": datetime.utcnow().isoformat(),
                                "error": str(e)
                            })
                        )
                    
        except Exception as e:
            logger.error(f"Health check background task error: {e}")

# Request/Response logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and responses"""
    
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        
        # Log response
        duration = time.time() - start_time
        logger.info(f"Response: {response.status_code} ({duration:.3f}s)")
        
        # Add performance headers
        response.headers["x-response-time"] = f"{duration:.3f}s"
        
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"Request failed: {request.method} {request.url.path} - {str(e)} ({duration:.3f}s)")
        raise

# WebSocket proxy (for real-time features)
@app.websocket("/ws/{path:path}")
async def websocket_proxy(websocket, path: str):
    """Proxy WebSocket connections to appropriate services"""
    
    # Determine target service
    service_name = None
    for svc_name, config in SERVICES_CONFIG.items():
        for route in config["routes"]:
            if f"/{path}".startswith(route):
                service_name = svc_name
                break
        if service_name:
            break
    
    if not service_name:
        await websocket.close(code=1000, reason="Service not found")
        return
    
    # For now, just accept and close - full WebSocket proxy would require more complex implementation
    await websocket.accept()
    await websocket.send_text(json.dumps({
        "message": "WebSocket proxy not fully implemented",
        "service": service_name,
        "path": path
    }))
    await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
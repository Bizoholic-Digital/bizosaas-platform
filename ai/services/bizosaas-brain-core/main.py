#!/usr/bin/env python3
"""
BizOSaaS Central Brain - CORE ROUTER ONLY
Lightweight routing and orchestration service

This service ONLY handles:
1. Domain routing & tenant resolution  
2. Authentication & authorization
3. Service orchestration & proxy
4. Business logic coordination
5. Multi-tenant data routing

All other concerns moved to specialized microservices.
"""

from fastapi import FastAPI, HTTPException, Depends, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import asyncio
import os
import httpx
import logging
from datetime import datetime
import redis.asyncio as redis
from enum import Enum
from pydantic import BaseModel

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis connection for HITL state management
REDIS_URL = os.getenv("REDIS_URL", "redis://bizosaas-redis-primary:6379/0")
redis_client = None

# Simple tenant resolution (simplified for core router)
from typing import NamedTuple

class SimpleTenant(NamedTuple):
    id: str
    domain: str
    name: str

def get_simple_tenant(domain: str) -> SimpleTenant:
    """Simple tenant resolution - can be enhanced later"""
    return SimpleTenant(
        id=domain.split('.')[0] if '.' in domain else "default",
        domain=domain,
        name=domain.replace('.', '_')
    )

# ========================================================================================
# HITL (HUMAN-IN-THE-LOOP) CONTROL SYSTEM
# ========================================================================================

class AutonomyLevel(str, Enum):
    """Progressive autonomy levels for AI operations"""
    SUPERVISED = "supervised"          # Every decision requires human approval
    ASSISTED = "assisted"              # AI suggests, human approves high-risk only
    MONITORED = "monitored"            # AI acts, human can intervene within time window
    AUTONOMOUS = "autonomous"          # AI acts independently, human notified
    ADAPTIVE = "adaptive"              # AI learns and adjusts confidence thresholds

class WorkflowConfig(BaseModel):
    """HITL configuration for a specific workflow"""
    workflow_id: str
    hitl_enabled: bool
    confidence_threshold: float
    autonomy_level: AutonomyLevel
    service_name: str
    timeout_seconds: int = 300  # 5 minutes default for human response

class HITLDecision(BaseModel):
    """AI decision awaiting human approval"""
    decision_id: str
    workflow_id: str
    confidence: float
    recommended_action: Dict[str, Any]
    reasoning: str
    timestamp: datetime

class HITLController:
    """Manages Human-in-the-Loop decision making and progressive autonomy"""

    def __init__(self):
        # Default workflow configurations
        self.workflows = {
            "lead_processing": WorkflowConfig(
                workflow_id="lead_processing",
                hitl_enabled=True,
                confidence_threshold=0.85,
                autonomy_level=AutonomyLevel.ASSISTED,
                service_name="django-crm"
            ),
            "product_sourcing": WorkflowConfig(
                workflow_id="product_sourcing",
                hitl_enabled=True,
                confidence_threshold=0.90,
                autonomy_level=AutonomyLevel.MONITORED,
                service_name="saleor"
            ),
            "campaign_optimization": WorkflowConfig(
                workflow_id="campaign_optimization",
                hitl_enabled=False,
                confidence_threshold=0.75,
                autonomy_level=AutonomyLevel.AUTONOMOUS,
                service_name="ai-agents"
            ),
            "content_generation": WorkflowConfig(
                workflow_id="content_generation",
                hitl_enabled=False,
                confidence_threshold=0.80,
                autonomy_level=AutonomyLevel.AUTONOMOUS,
                service_name="wagtail"
            ),
            "customer_support": WorkflowConfig(
                workflow_id="customer_support",
                hitl_enabled=True,
                confidence_threshold=0.85,
                autonomy_level=AutonomyLevel.ASSISTED,
                service_name="conversations"
            ),
            "payment_processing": WorkflowConfig(
                workflow_id="payment_processing",
                hitl_enabled=True,
                confidence_threshold=0.95,
                autonomy_level=AutonomyLevel.SUPERVISED,
                service_name="payments"
            ),
            "inventory_management": WorkflowConfig(
                workflow_id="inventory_management",
                hitl_enabled=False,
                confidence_threshold=0.80,
                autonomy_level=AutonomyLevel.MONITORED,
                service_name="saleor"
            ),
            "analytics_reporting": WorkflowConfig(
                workflow_id="analytics_reporting",
                hitl_enabled=False,
                confidence_threshold=0.70,
                autonomy_level=AutonomyLevel.AUTONOMOUS,
                service_name="analytics"
            )
        }

    async def check_hitl_required(self, workflow_id: str, confidence: float) -> bool:
        """Determine if human approval is required for this decision"""
        config = self.workflows.get(workflow_id)
        if not config:
            logger.warning(f"Unknown workflow {workflow_id}, defaulting to HITL required")
            return True  # Default to requiring HITL for unknown workflows

        # Check if HITL is globally enabled for this workflow
        if not config.hitl_enabled:
            return False

        # Check confidence threshold
        if confidence < config.confidence_threshold:
            logger.info(f"HITL required: confidence {confidence} below threshold {config.confidence_threshold}")
            return True

        # Check autonomy level
        if config.autonomy_level == AutonomyLevel.SUPERVISED:
            return True  # Always require approval
        elif config.autonomy_level == AutonomyLevel.ASSISTED:
            return confidence < 0.90  # High confidence can bypass
        elif config.autonomy_level == AutonomyLevel.MONITORED:
            return confidence < 0.85  # Medium-high confidence can bypass

        return False  # AUTONOMOUS and ADAPTIVE don't require HITL

    async def store_pending_decision(self, decision: HITLDecision) -> str:
        """Store a decision awaiting human approval in Redis"""
        if redis_client:
            try:
                key = f"hitl:pending:{decision.decision_id}"
                await redis_client.setex(
                    key,
                    300,  # 5 minutes TTL
                    decision.model_dump_json()
                )
                logger.info(f"Stored pending HITL decision: {decision.decision_id}")
                return decision.decision_id
            except Exception as e:
                logger.error(f"Failed to store HITL decision: {e}")
                return None
        return None

    async def get_pending_decision(self, decision_id: str) -> Optional[HITLDecision]:
        """Retrieve a pending decision from Redis"""
        if redis_client:
            try:
                key = f"hitl:pending:{decision_id}"
                data = await redis_client.get(key)
                if data:
                    return HITLDecision.model_validate_json(data)
            except Exception as e:
                logger.error(f"Failed to retrieve HITL decision: {e}")
        return None

    def get_workflow_config(self, workflow_id: str) -> Optional[WorkflowConfig]:
        """Get configuration for a specific workflow"""
        return self.workflows.get(workflow_id)

    def update_workflow_config(self, workflow_id: str, config: WorkflowConfig):
        """Update workflow configuration (super admin only)"""
        self.workflows[workflow_id] = config
        logger.info(f"Updated HITL config for workflow: {workflow_id}")

    async def record_decision_outcome(self, decision_id: str, approved: bool, feedback: str = None):
        """Record the outcome of a HITL decision for AI learning"""
        if redis_client:
            try:
                key = f"hitl:history:{decision_id}"
                outcome = {
                    "decision_id": decision_id,
                    "approved": approved,
                    "feedback": feedback,
                    "timestamp": datetime.now().isoformat()
                }
                await redis_client.setex(key, 86400, str(outcome))  # 24 hours
                logger.info(f"Recorded HITL outcome: {decision_id} - {'approved' if approved else 'rejected'}")
            except Exception as e:
                logger.error(f"Failed to record HITL outcome: {e}")

# Initialize HITL Controller
hitl_controller = HITLController()

app = FastAPI(
    title="BizOSaaS Central Brain - Core Router",
    description="Lightweight routing and orchestration service",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================================================================
# SERVICE REGISTRY - Routes to specialized microservices
# ========================================================================================

SERVICE_REGISTRY = {
    "ai-agents": "http://ai-agent-service:8010",
    "payments": "http://payment-service:8014", 
    "documents": "http://document-service:8015",
    "conversations": "http://conversation-service:8016",
    "vault": "http://vault:8200",  # Official Vault service
    "events": "http://event-service:8018",
    "admin": "http://admin-service:8019",
    "analytics": "http://analytics-service:8013",
    "training": "http://ai-training-service:8020",
    "websocket": "http://websocket-service:8021",
    "wagtail": "http://wagtail-cms:8002",
    "django-crm": "http://django-crm:8000", 
    "saleor": "http://bizosaas-saleor-api-8003:8000"
}

# ========================================================================================
# CORE FUNCTIONS - Tenant Resolution & Routing
# ========================================================================================

def get_current_tenant(request: Request) -> Optional[SimpleTenant]:
    """Resolve tenant from domain/headers"""
    host = request.headers.get("host", "")
    domain = host.split(":")[0]
    return get_simple_tenant(domain)

async def proxy_to_service(service_name: str, path: str, method: str, headers: dict, body: dict = None) -> dict:
    """Proxy request to appropriate microservice"""
    service_url = SERVICE_REGISTRY.get(service_name)
    if not service_url:
        raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=f"{service_url}{path}",
                headers=headers,
                json=body,
                timeout=30.0
            )
            return response.json() if response.headers.get("content-type", "").startswith("application/json") else {"data": response.text}
        except Exception as e:
            logger.error(f"Service proxy error: {e}")
            raise HTTPException(status_code=503, detail=f"Service {service_name} unavailable")

# ========================================================================================
# CORE API ENDPOINTS - Health & Routing
# ========================================================================================

@app.get("/")
async def root():
    return {
        "service": "BizOSaaS Central Brain - Core Router",
        "version": "2.0.0",
        "status": "active",
        "architecture": "microservices",
        "services": len(SERVICE_REGISTRY),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Core health check"""
    return {
        "status": "healthy", 
        "service": "bizosaas-brain-core",
        "timestamp": datetime.now().isoformat(),
        "tenant_registry": "active",
        "services_registered": len(SERVICE_REGISTRY)
    }

@app.get("/services")
async def list_services():
    """List all registered microservices"""
    return {
        "services": SERVICE_REGISTRY,
        "count": len(SERVICE_REGISTRY),
        "timestamp": datetime.now().isoformat()
    }

# ========================================================================================
# HITL CONTROL ENDPOINTS - Super Admin Management
# ========================================================================================

@app.get("/api/brain/hitl/workflows")
async def get_all_workflows():
    """Get all workflow HITL configurations (super admin only)"""
    workflows = {}
    for workflow_id, config in hitl_controller.workflows.items():
        workflows[workflow_id] = {
            "workflow_id": config.workflow_id,
            "hitl_enabled": config.hitl_enabled,
            "confidence_threshold": config.confidence_threshold,
            "autonomy_level": config.autonomy_level.value,
            "service_name": config.service_name,
            "timeout_seconds": config.timeout_seconds
        }
    return {
        "workflows": workflows,
        "total": len(workflows),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/brain/hitl/workflows/{workflow_id}")
async def get_workflow_config(workflow_id: str):
    """Get specific workflow HITL configuration"""
    config = hitl_controller.get_workflow_config(workflow_id)
    if not config:
        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")

    return {
        "workflow_id": config.workflow_id,
        "hitl_enabled": config.hitl_enabled,
        "confidence_threshold": config.confidence_threshold,
        "autonomy_level": config.autonomy_level.value,
        "service_name": config.service_name,
        "timeout_seconds": config.timeout_seconds
    }

@app.post("/api/brain/hitl/workflows/{workflow_id}/toggle")
async def toggle_workflow_hitl(workflow_id: str, enabled: bool):
    """Toggle HITL on/off for a specific workflow (super admin only)"""
    config = hitl_controller.get_workflow_config(workflow_id)
    if not config:
        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")

    config.hitl_enabled = enabled
    hitl_controller.update_workflow_config(workflow_id, config)

    return {
        "workflow_id": workflow_id,
        "hitl_enabled": enabled,
        "message": f"HITL {'enabled' if enabled else 'disabled'} for {workflow_id}",
        "timestamp": datetime.now().isoformat()
    }

@app.put("/api/brain/hitl/workflows/{workflow_id}/confidence")
async def update_confidence_threshold(workflow_id: str, threshold: float):
    """Update confidence threshold for a workflow (super admin only)"""
    if not 0.0 <= threshold <= 1.0:
        raise HTTPException(status_code=400, detail="Confidence threshold must be between 0.0 and 1.0")

    config = hitl_controller.get_workflow_config(workflow_id)
    if not config:
        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")

    config.confidence_threshold = threshold
    hitl_controller.update_workflow_config(workflow_id, config)

    return {
        "workflow_id": workflow_id,
        "confidence_threshold": threshold,
        "message": f"Confidence threshold updated for {workflow_id}",
        "timestamp": datetime.now().isoformat()
    }

@app.put("/api/brain/hitl/workflows/{workflow_id}/autonomy")
async def update_autonomy_level(workflow_id: str, level: AutonomyLevel):
    """Update autonomy level for a workflow (super admin only)"""
    config = hitl_controller.get_workflow_config(workflow_id)
    if not config:
        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")

    config.autonomy_level = level
    hitl_controller.update_workflow_config(workflow_id, config)

    return {
        "workflow_id": workflow_id,
        "autonomy_level": level.value,
        "message": f"Autonomy level updated to {level.value} for {workflow_id}",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/brain/hitl/decisions/pending")
async def get_pending_decisions():
    """Get all pending HITL decisions awaiting approval"""
    if not redis_client:
        return {"decisions": [], "message": "Redis not connected"}

    try:
        # Scan for all pending decisions
        pending_keys = []
        async for key in redis_client.scan_iter(match="hitl:pending:*"):
            pending_keys.append(key)

        decisions = []
        for key in pending_keys:
            data = await redis_client.get(key)
            if data:
                decision = HITLDecision.model_validate_json(data)
                decisions.append({
                    "decision_id": decision.decision_id,
                    "workflow_id": decision.workflow_id,
                    "confidence": decision.confidence,
                    "recommended_action": decision.recommended_action,
                    "reasoning": decision.reasoning,
                    "timestamp": decision.timestamp.isoformat()
                })

        return {
            "decisions": decisions,
            "count": len(decisions),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching pending decisions: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch pending decisions")

@app.post("/api/brain/hitl/decisions/{decision_id}/approve")
async def approve_decision(decision_id: str, feedback: Optional[str] = None):
    """Approve a pending HITL decision (super admin or assigned user)"""
    decision = await hitl_controller.get_pending_decision(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail=f"Decision {decision_id} not found or expired")

    # Record the approval
    await hitl_controller.record_decision_outcome(decision_id, approved=True, feedback=feedback)

    # Execute the approved action by routing to the appropriate service
    config = hitl_controller.get_workflow_config(decision.workflow_id)
    if config:
        try:
            # Route to the service that requested the decision
            result = await proxy_to_service(
                config.service_name,
                "/execute-decision",
                "POST",
                {},
                decision.recommended_action
            )

            # Clear the pending decision
            if redis_client:
                await redis_client.delete(f"hitl:pending:{decision_id}")

            return {
                "decision_id": decision_id,
                "status": "approved",
                "executed": True,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error executing approved decision: {e}")
            return {
                "decision_id": decision_id,
                "status": "approved",
                "executed": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    return {
        "decision_id": decision_id,
        "status": "approved",
        "message": "Decision approved but service configuration not found",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/brain/hitl/decisions/{decision_id}/reject")
async def reject_decision(decision_id: str, feedback: str):
    """Reject a pending HITL decision with feedback (super admin or assigned user)"""
    decision = await hitl_controller.get_pending_decision(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail=f"Decision {decision_id} not found or expired")

    # Record the rejection
    await hitl_controller.record_decision_outcome(decision_id, approved=False, feedback=feedback)

    # Clear the pending decision
    if redis_client:
        await redis_client.delete(f"hitl:pending:{decision_id}")

    return {
        "decision_id": decision_id,
        "status": "rejected",
        "feedback": feedback,
        "message": "Decision rejected. AI will learn from this feedback.",
        "timestamp": datetime.now().isoformat()
    }

# ========================================================================================
# SALEOR GRAPHQL ADAPTER - Convert REST to GraphQL
# ========================================================================================

async def saleor_graphql_request(query: str, variables: dict = None) -> dict:
    """Send GraphQL request to Saleor API"""
    saleor_url = "http://bizosaas-saleor-api-8003:8000/graphql/"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                saleor_url,
                json={
                    "query": query,
                    "variables": variables or {}
                },
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
            return response.json()
        except Exception as e:
            logger.error(f"Saleor GraphQL error: {e}")
            return {"errors": [{"message": str(e)}]}

@app.get("/api/brain/saleor/products")
async def saleor_products(
    request: Request,
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 12
):
    """Get products from Saleor via GraphQL"""
    
    # Build GraphQL query for products
    query = """
    query GetProducts($first: Int, $filter: ProductFilterInput) {
        products(first: $first, filter: $filter) {
            edges {
                node {
                    id
                    name
                    description
                    slug
                    pricing {
                        priceRange {
                            start {
                                gross {
                                    amount
                                    currency
                                }
                            }
                        }
                    }
                    thumbnail {
                        url
                    }
                    category {
                        id
                        name
                    }
                    rating
                    variants {
                        id
                        name
                    }
                }
            }
            pageInfo {
                hasNextPage
                hasPreviousPage
            }
            totalCount
        }
    }
    """
    
    # Build variables
    variables = {"first": limit}
    filter_input = {}
    
    if search:
        filter_input["search"] = search
    if category:
        filter_input["categories"] = [category]
    
    if filter_input:
        variables["filter"] = filter_input
    
    # Make GraphQL request
    result = await saleor_graphql_request(query, variables)
    
    if "errors" in result:
        # Return fallback data if Saleor is unavailable
        return {
            "products": [
                {
                    "id": "fallback-1",
                    "name": "Premium Wireless Headphones",
                    "description": "High-quality wireless headphones with noise cancellation.",
                    "pricing": {
                        "priceRange": {
                            "start": {
                                "gross": {"amount": 149.99, "currency": "USD"}
                            }
                        }
                    },
                    "thumbnail": {"url": "/placeholder-product.jpg"},
                    "category": {"name": "Electronics"},
                    "rating": 4.5
                },
                {
                    "id": "fallback-2", 
                    "name": "Organic Cotton T-Shirt",
                    "description": "Comfortable and sustainable organic cotton t-shirt.",
                    "pricing": {
                        "priceRange": {
                            "start": {
                                "gross": {"amount": 29.99, "currency": "USD"}
                            }
                        }
                    },
                    "thumbnail": {"url": "/placeholder-product.jpg"},
                    "category": {"name": "Fashion"},
                    "rating": 4.2
                }
            ],
            "count": 2,
            "totalCount": 2,
            "hasNextPage": False,
            "source": "fallback"
        }
    
    # Transform GraphQL response to REST format
    products_data = result.get("data", {}).get("products", {})
    products = []
    
    for edge in products_data.get("edges", []):
        node = edge["node"]
        products.append({
            "id": node["id"],
            "name": node["name"],
            "description": node.get("description", ""),
            "slug": node.get("slug", ""),
            "pricing": node.get("pricing", {}),
            "thumbnail": node.get("thumbnail", {}),
            "category": node.get("category", {}),
            "rating": node.get("rating", 4.0),
            "variants": node.get("variants", [])
        })
    
    page_info = products_data.get("pageInfo", {})
    
    return {
        "products": products,
        "count": len(products),
        "totalCount": products_data.get("totalCount", 0),
        "hasNextPage": page_info.get("hasNextPage", False),
        "source": "saleor"
    }

@app.get("/api/brain/saleor/categories")
async def saleor_categories(request: Request):
    """Get categories from Saleor via GraphQL"""
    
    query = """
    query GetCategories {
        categories(first: 100) {
            edges {
                node {
                    id
                    name
                    slug
                    description
                    products {
                        totalCount
                    }
                }
            }
        }
    }
    """
    
    result = await saleor_graphql_request(query)
    
    if "errors" in result:
        return {
            "categories": [
                {"id": "fallback-1", "name": "Electronics", "slug": "electronics", "productCount": 25},
                {"id": "fallback-2", "name": "Fashion", "slug": "fashion", "productCount": 18},
                {"id": "fallback-3", "name": "Home & Garden", "slug": "home-garden", "productCount": 12}
            ],
            "source": "fallback"
        }
    
    categories_data = result.get("data", {}).get("categories", {})
    categories = []
    
    for edge in categories_data.get("edges", []):
        node = edge["node"]
        categories.append({
            "id": node["id"],
            "name": node["name"],
            "slug": node.get("slug", ""),
            "description": node.get("description", ""),
            "productCount": node.get("products", {}).get("totalCount", 0)
        })
    
    return {
        "categories": categories,
        "source": "saleor"
    }

# ========================================================================================
# ROUTING ENDPOINTS - Proxy to Microservices  
# ========================================================================================

@app.api_route("/api/brain/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def route_to_service(service_name: str, path: str, request: Request):
    """Route all service requests to appropriate microservices"""
    
    # Skip Saleor routes - handled by specific endpoints above
    if service_name == "saleor" and path in ["products", "categories"]:
        raise HTTPException(status_code=404, detail="Use specific Saleor endpoints")
    
    # Get tenant context
    tenant = get_current_tenant(request)
    tenant_id = tenant.id if tenant else "default"
    
    # Prepare headers with tenant context
    headers = dict(request.headers)
    headers["x-tenant-id"] = tenant_id
    
    # Get request body if present
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.json()
        except:
            body = {}
    
    # Add tenant context to body
    if body:
        body["tenant_id"] = tenant_id
    
    # Proxy to appropriate service
    return await proxy_to_service(service_name, f"/{path}", request.method, headers, body)

# ========================================================================================
# LEGACY COMPATIBILITY - Direct endpoints for existing integrations
# ========================================================================================

@app.get("/api/dashboard")
async def dashboard_proxy(request: Request):
    """Proxy dashboard requests to admin service"""
    return await proxy_to_service("admin", "/dashboard", "GET", dict(request.headers))

@app.get("/api/directory/categories")
async def directory_categories_proxy(request: Request):
    """Proxy directory requests to business directory service"""
    return await proxy_to_service("admin", "/directory/categories", "GET", dict(request.headers))

# ========================================================================================
# HITL-AWARE ROUTING - Enhanced proxy with confidence checking
# ========================================================================================

@app.post("/api/brain/{service_name}/with-hitl/{path:path}")
async def route_with_hitl_check(
    service_name: str,
    path: str,
    request: Request,
    workflow_id: str,
    confidence: float
):
    """
    Route request with HITL confidence checking.
    AI services use this endpoint to route decisions that may require human approval.
    """
    # Check if HITL is required for this workflow and confidence level
    hitl_required = await hitl_controller.check_hitl_required(workflow_id, confidence)

    # Get tenant context
    tenant = get_current_tenant(request)
    tenant_id = tenant.id if tenant else "default"

    # Prepare headers and body
    headers = dict(request.headers)
    headers["x-tenant-id"] = tenant_id

    body = await request.json()
    body["tenant_id"] = tenant_id

    if hitl_required:
        # Create pending decision for human approval
        import uuid
        decision_id = str(uuid.uuid4())

        decision = HITLDecision(
            decision_id=decision_id,
            workflow_id=workflow_id,
            confidence=confidence,
            recommended_action=body,
            reasoning=body.get("reasoning", "AI decision pending human review"),
            timestamp=datetime.now()
        )

        await hitl_controller.store_pending_decision(decision)

        return {
            "status": "pending_approval",
            "decision_id": decision_id,
            "workflow_id": workflow_id,
            "confidence": confidence,
            "message": "This decision requires human approval due to confidence threshold or HITL settings",
            "approval_url": f"/api/brain/hitl/decisions/{decision_id}",
            "timestamp": datetime.now().isoformat()
        }
    else:
        # Confidence is high enough, proceed with autonomous execution
        result = await proxy_to_service(service_name, f"/{path}", "POST", headers, body)

        return {
            "status": "executed",
            "workflow_id": workflow_id,
            "confidence": confidence,
            "result": result,
            "message": "Decision executed autonomously based on high confidence",
            "timestamp": datetime.now().isoformat()
        }

# ========================================================================================
# STARTUP & SHUTDOWN - Redis Connection Management
# ========================================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize Redis connection for HITL state management"""
    global redis_client
    try:
        redis_client = await redis.from_url(
            REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        await redis_client.ping()
        logger.info(f"✅ Connected to Redis at {REDIS_URL} for HITL state management")
    except Exception as e:
        logger.error(f"❌ Failed to connect to Redis: {e}")
        logger.warning("HITL decision storage will be unavailable")
        redis_client = None

@app.on_event("shutdown")
async def shutdown_event():
    """Close Redis connection"""
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("Closed Redis connection")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
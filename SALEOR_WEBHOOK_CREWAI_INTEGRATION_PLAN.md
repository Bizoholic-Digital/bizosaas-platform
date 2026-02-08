# Saleor Dashboard + Webhook CrewAI Integration Plan

**Date:** November 3, 2025
**Strategy:** Hybrid Approach - Phase 1 Implementation
**Goal:** Leverage 93+ CrewAI agents with official Saleor Dashboard via webhooks

---

## Executive Summary

This document provides a complete implementation plan for integrating Saleor Dashboard with the BizOSaaS CrewAI multi-agent system (93+ AI agents) using webhook-based architecture.

### Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    SALEOR DASHBOARD                              │
│                 (Official React SPA)                             │
│              https://stg.coreldove.com/dashboard                 │
└──────────────────────────────────────────────────────────────────┘
                            ↓ Direct GraphQL
┌──────────────────────────────────────────────────────────────────┐
│                     SALEOR CORE API                              │
│                   (Port 8000, IP: 10.0.1.47)                     │
│                                                                  │
│  • User creates order in dashboard                               │
│  • Saleor Core saves to database                                 │
│  • Webhook fires → Brain Gateway                                 │
└──────────────────────────────────────────────────────────────────┘
                            ↓ HTTP Webhook
┌──────────────────────────────────────────────────────────────────┐
│                   BRAIN GATEWAY (FastAPI)                        │
│                      (Port 8001)                                 │
│                                                                  │
│  Webhook Endpoints:                                              │
│  • /webhooks/saleor/order-created                                │
│  • /webhooks/saleor/order-updated                                │
│  • /webhooks/saleor/product-created                              │
│  • /webhooks/saleor/inventory-low                                │
│  • /webhooks/saleor/customer-created                             │
└──────────────────────────────────────────────────────────────────┘
                            ↓ CrewAI Activation
┌──────────────────────────────────────────────────────────────────┐
│                    CREWAI MULTI-AGENT SYSTEM                     │
│                        (93+ AI Agents)                           │
│                                                                  │
│  Crews Activated:                                                │
│  • Order Fulfillment Crew (Inventory + Shipping + Notification)  │
│  • Product SEO Crew (Content + Marketing + Analytics)            │
│  • Procurement Crew (Supplier + Pricing + Quality)               │
│  • Customer Service Crew (Support + Email + Retention)           │
└──────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Webhook-Based Integration (Immediate Implementation)

### Benefits

✅ **Immediate Value**
- Leverage all 93+ CrewAI agents without modifying official dashboard
- Autonomous operations triggered by admin actions
- No custom dashboard development needed (saves 4-6 weeks)

✅ **Maintains Official Dashboard**
- Get automatic Saleor updates
- Full feature parity with official dashboard
- Security updates from Saleor team

✅ **Autonomous Operations**
- Order fulfillment automation
- Inventory management
- SEO optimization
- Customer service automation

---

## Implementation Steps

### Step 1: Deploy Saleor Dashboard (Prerequisite)

**Status:** ⚠️ Configured but NOT deployed yet

**Action Required:**
1. Verify configuration in Dokploy UI (see [SALEOR_DASHBOARD_CONFIGURATION_VERIFICATION.md](./SALEOR_DASHBOARD_CONFIGURATION_VERIFICATION.md))
2. Click **"Deploy"** button in Dokploy
3. Wait for container to start (2-3 minutes)
4. Verify: `https://stg.coreldove.com/dashboard/`

**Prerequisites Before Continuing:**
- [ ] Dashboard container running
- [ ] Dashboard accessible via domain
- [ ] Can login to dashboard

---

### Step 2: Create Webhook Endpoints in Brain Gateway

#### 2.1 File Structure

Create new webhook routes file:
```
bizosaas/backend/brain-gateway/app/api/routes/
└── saleor_webhooks.py  # NEW FILE
```

#### 2.2 Webhook Endpoints Implementation

**File:** `bizosaas/backend/brain-gateway/app/api/routes/saleor_webhooks.py`

```python
"""
Saleor Webhook Handlers for CrewAI Integration
Receives webhooks from Saleor Core and triggers appropriate CrewAI crews
"""

from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
import hmac
import hashlib
import logging
from typing import Dict, Any
from datetime import datetime

from app.services.crewai.order_fulfillment_crew import OrderFulfillmentCrew
from app.services.crewai.product_seo_crew import ProductSEOCrew
from app.services.crewai.procurement_crew import ProcurementCrew
from app.services.crewai.customer_service_crew import CustomerServiceCrew

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhooks/saleor", tags=["saleor-webhooks"])

# Webhook signature verification
SALEOR_WEBHOOK_SECRET = "your-webhook-secret-key"  # TODO: Move to env


def verify_webhook_signature(request: Request, payload: bytes) -> bool:
    """
    Verify Saleor webhook signature for security
    """
    signature = request.headers.get("Saleor-Signature")
    if not signature:
        return False

    expected_signature = hmac.new(
        SALEOR_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)


@router.post("/order-created")
async def handle_order_created(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Webhook: ORDER_CREATED
    Triggered when: New order is placed in Saleor Dashboard

    CrewAI Actions:
    1. Inventory Agent - Verify stock and allocate inventory
    2. Shipping Agent - Calculate shipping and book courier
    3. Customer Service Agent - Send confirmation email
    4. Analytics Agent - Update sales metrics

    Expected Payload:
    {
        "order": {
            "id": "T3JkZXI6MQ==",
            "number": "12345",
            "user_email": "customer@example.com",
            "total_gross_amount": 150.00,
            "lines": [...],
            "shipping_address": {...}
        }
    }
    """
    try:
        payload = await request.body()

        # Verify webhook signature
        if not verify_webhook_signature(request, payload):
            logger.warning("Invalid webhook signature for order-created")
            raise HTTPException(status_code=401, detail="Invalid signature")

        # Parse JSON payload
        data = await request.json()
        order_data = data.get("order", {})

        logger.info(f"Order created webhook received: {order_data.get('number')}")

        # Trigger CrewAI Order Fulfillment Crew in background
        background_tasks.add_task(
            process_order_with_crewai,
            order_data=order_data,
            event="order_created"
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "processing",
                "crew": "order_fulfillment",
                "order_number": order_data.get("number"),
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    except Exception as e:
        logger.error(f"Error processing order-created webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/order-updated")
async def handle_order_updated(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Webhook: ORDER_UPDATED
    Triggered when: Order status changes (e.g., paid, fulfilled, shipped)

    CrewAI Actions:
    - Payment confirmed → Trigger fulfillment crew
    - Shipped → Send tracking email via customer service crew
    - Cancelled → Update inventory and notify customer
    """
    try:
        payload = await request.body()

        if not verify_webhook_signature(request, payload):
            raise HTTPException(status_code=401, detail="Invalid signature")

        data = await request.json()
        order_data = data.get("order", {})

        logger.info(f"Order updated webhook: {order_data.get('number')}")

        background_tasks.add_task(
            process_order_update_with_crewai,
            order_data=order_data
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "processing",
                "crew": "order_fulfillment",
                "order_number": order_data.get("number")
            }
        )

    except Exception as e:
        logger.error(f"Error processing order-updated webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/product-created")
async def handle_product_created(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Webhook: PRODUCT_CREATED
    Triggered when: New product added via Saleor Dashboard

    CrewAI Actions:
    1. SEO Agent - Optimize product title, description, meta tags
    2. Content Agent - Generate enhanced product descriptions
    3. Marketing Agent - Create social media posts
    4. Pricing Agent - Analyze competitive pricing

    Expected Payload:
    {
        "product": {
            "id": "UHJvZHVjdDox",
            "name": "New Product",
            "description": "...",
            "category": {...},
            "variants": [...]
        }
    }
    """
    try:
        payload = await request.body()

        if not verify_webhook_signature(request, payload):
            raise HTTPException(status_code=401, detail="Invalid signature")

        data = await request.json()
        product_data = data.get("product", {})

        logger.info(f"Product created webhook: {product_data.get('name')}")

        # Trigger CrewAI Product SEO Crew
        background_tasks.add_task(
            process_product_with_crewai,
            product_data=product_data,
            event="product_created"
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "processing",
                "crew": "product_seo",
                "product_name": product_data.get("name")
            }
        )

    except Exception as e:
        logger.error(f"Error processing product-created webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/product-updated")
async def handle_product_updated(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Webhook: PRODUCT_UPDATED
    Triggered when: Product details changed (price, stock, description)

    CrewAI Actions:
    - Price changed → Competitive analysis by pricing agent
    - Stock low → Trigger procurement crew
    - Description updated → SEO optimization
    """
    try:
        payload = await request.body()

        if not verify_webhook_signature(request, payload):
            raise HTTPException(status_code=401, detail="Invalid signature")

        data = await request.json()
        product_data = data.get("product", {})

        logger.info(f"Product updated webhook: {product_data.get('name')}")

        background_tasks.add_task(
            process_product_update_with_crewai,
            product_data=product_data
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "processing",
                "crew": "product_seo",
                "product_name": product_data.get("name")
            }
        )

    except Exception as e:
        logger.error(f"Error processing product-updated webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/customer-created")
async def handle_customer_created(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Webhook: CUSTOMER_CREATED
    Triggered when: New customer registers or is added via dashboard

    CrewAI Actions:
    1. Customer Service Agent - Send welcome email
    2. Marketing Agent - Add to email campaign
    3. Analytics Agent - Update customer segments
    4. Retention Agent - Schedule follow-up communications

    Expected Payload:
    {
        "user": {
            "id": "VXNlcjox",
            "email": "newcustomer@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }
    }
    """
    try:
        payload = await request.body()

        if not verify_webhook_signature(request, payload):
            raise HTTPException(status_code=401, detail="Invalid signature")

        data = await request.json()
        customer_data = data.get("user", {})

        logger.info(f"Customer created webhook: {customer_data.get('email')}")

        # Trigger CrewAI Customer Service Crew
        background_tasks.add_task(
            process_customer_with_crewai,
            customer_data=customer_data,
            event="customer_created"
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "processing",
                "crew": "customer_service",
                "customer_email": customer_data.get("email")
            }
        )

    except Exception as e:
        logger.error(f"Error processing customer-created webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/invoice-requested")
async def handle_invoice_requested(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Webhook: INVOICE_REQUESTED
    Triggered when: Admin generates invoice for order

    CrewAI Actions:
    1. Finance Agent - Generate PDF invoice
    2. Email Agent - Send invoice to customer
    3. Accounting Agent - Update financial records
    """
    try:
        payload = await request.body()

        if not verify_webhook_signature(request, payload):
            raise HTTPException(status_code=401, detail="Invalid signature")

        data = await request.json()
        invoice_data = data.get("invoice", {})

        logger.info(f"Invoice requested webhook: {invoice_data.get('number')}")

        background_tasks.add_task(
            process_invoice_with_crewai,
            invoice_data=invoice_data
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "processing",
                "crew": "finance",
                "invoice_number": invoice_data.get("number")
            }
        )

    except Exception as e:
        logger.error(f"Error processing invoice-requested webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CrewAI Background Processing Functions
# ============================================================================

async def process_order_with_crewai(order_data: Dict[str, Any], event: str):
    """
    Process order with CrewAI Order Fulfillment Crew

    Crew Composition:
    - Inventory Manager Agent
    - Shipping Coordinator Agent
    - Customer Service Agent
    - Analytics Agent
    """
    try:
        logger.info(f"Starting CrewAI Order Fulfillment for order {order_data.get('number')}")

        # Initialize Order Fulfillment Crew
        crew = OrderFulfillmentCrew()

        # Execute crew workflow
        result = await crew.process_order(
            order_id=order_data.get("id"),
            order_number=order_data.get("number"),
            customer_email=order_data.get("user_email"),
            order_items=order_data.get("lines", []),
            shipping_address=order_data.get("shipping_address", {}),
            total_amount=order_data.get("total_gross_amount")
        )

        logger.info(f"CrewAI Order Fulfillment completed: {result}")

    except Exception as e:
        logger.error(f"Error in CrewAI order processing: {str(e)}")


async def process_order_update_with_crewai(order_data: Dict[str, Any]):
    """
    Process order updates with appropriate CrewAI crew
    """
    try:
        status = order_data.get("status")
        order_number = order_data.get("number")

        logger.info(f"Processing order update for {order_number}, status: {status}")

        if status == "FULFILLED":
            # Trigger shipping notification
            crew = CustomerServiceCrew()
            await crew.send_shipping_notification(order_data)

        elif status == "CANCELLED":
            # Trigger inventory return and customer notification
            crew = OrderFulfillmentCrew()
            await crew.handle_cancellation(order_data)

    except Exception as e:
        logger.error(f"Error in CrewAI order update processing: {str(e)}")


async def process_product_with_crewai(product_data: Dict[str, Any], event: str):
    """
    Process product with CrewAI Product SEO Crew

    Crew Composition:
    - SEO Optimization Agent
    - Content Generation Agent
    - Marketing Agent
    - Competitive Analysis Agent
    """
    try:
        logger.info(f"Starting CrewAI Product SEO for product {product_data.get('name')}")

        # Initialize Product SEO Crew
        crew = ProductSEOCrew()

        # Execute crew workflow
        result = await crew.optimize_product(
            product_id=product_data.get("id"),
            product_name=product_data.get("name"),
            description=product_data.get("description"),
            category=product_data.get("category", {}),
            variants=product_data.get("variants", [])
        )

        logger.info(f"CrewAI Product SEO completed: {result}")

    except Exception as e:
        logger.error(f"Error in CrewAI product processing: {str(e)}")


async def process_product_update_with_crewai(product_data: Dict[str, Any]):
    """
    Process product updates with appropriate CrewAI crew
    """
    try:
        # Check if stock is low
        stock_quantity = sum(
            variant.get("quantity_available", 0)
            for variant in product_data.get("variants", [])
        )

        if stock_quantity < 10:  # Low stock threshold
            logger.info(f"Low stock detected for {product_data.get('name')}, triggering procurement")
            crew = ProcurementCrew()
            await crew.handle_low_stock(product_data)

        # Check if price changed
        # Trigger competitive analysis

    except Exception as e:
        logger.error(f"Error in CrewAI product update processing: {str(e)}")


async def process_customer_with_crewai(customer_data: Dict[str, Any], event: str):
    """
    Process customer with CrewAI Customer Service Crew

    Crew Composition:
    - Welcome Email Agent
    - Marketing Automation Agent
    - Customer Segmentation Agent
    - Retention Agent
    """
    try:
        logger.info(f"Starting CrewAI Customer Service for {customer_data.get('email')}")

        # Initialize Customer Service Crew
        crew = CustomerServiceCrew()

        # Execute crew workflow
        result = await crew.onboard_customer(
            customer_id=customer_data.get("id"),
            email=customer_data.get("email"),
            first_name=customer_data.get("first_name"),
            last_name=customer_data.get("last_name")
        )

        logger.info(f"CrewAI Customer Service completed: {result}")

    except Exception as e:
        logger.error(f"Error in CrewAI customer processing: {str(e)}")


async def process_invoice_with_crewai(invoice_data: Dict[str, Any]):
    """
    Process invoice generation with CrewAI Finance Crew
    """
    try:
        logger.info(f"Processing invoice {invoice_data.get('number')} with CrewAI")
        # Implementation for invoice processing
        pass

    except Exception as e:
        logger.error(f"Error in CrewAI invoice processing: {str(e)}")


@router.get("/health")
async def webhook_health():
    """Health check endpoint for webhook system"""
    return {
        "status": "healthy",
        "service": "saleor-webhooks",
        "timestamp": datetime.utcnow().isoformat()
    }
```

#### 2.3 Register Routes in Main App

**File:** `bizosaas/backend/brain-gateway/app/main.py`

```python
# Add import
from app.api.routes import saleor_webhooks

# Register router
app.include_router(saleor_webhooks.router, prefix="/api")
```

---

### Step 3: Configure Saleor Core Webhooks

#### 3.1 Add Webhooks via Saleor Dashboard

Once dashboard is deployed, configure webhooks:

1. Login to Saleor Dashboard: `https://stg.coreldove.com/dashboard/`
2. Navigate to **Configuration** → **Webhooks**
3. Click **"Create Webhook"**

#### 3.2 Webhook Configurations

**Webhook 1: Order Created**
```yaml
Name: Order Created → CrewAI
Target URL: http://10.0.1.48:8001/api/webhooks/saleor/order-created
Secret Key: your-webhook-secret-key
Events: ORDER_CREATED
Active: ✅ Yes
```

**Webhook 2: Order Updated**
```yaml
Name: Order Updated → CrewAI
Target URL: http://10.0.1.48:8001/api/webhooks/saleor/order-updated
Secret Key: your-webhook-secret-key
Events: ORDER_UPDATED, ORDER_FULLY_PAID, ORDER_FULFILLED, ORDER_CANCELLED
Active: ✅ Yes
```

**Webhook 3: Product Created**
```yaml
Name: Product Created → CrewAI
Target URL: http://10.0.1.48:8001/api/webhooks/saleor/product-created
Secret Key: your-webhook-secret-key
Events: PRODUCT_CREATED
Active: ✅ Yes
```

**Webhook 4: Product Updated**
```yaml
Name: Product Updated → CrewAI
Target URL: http://10.0.1.48:8001/api/webhooks/saleor/product-updated
Secret Key: your-webhook-secret-key
Events: PRODUCT_UPDATED, PRODUCT_VARIANT_OUT_OF_STOCK
Active: ✅ Yes
```

**Webhook 5: Customer Created**
```yaml
Name: Customer Created → CrewAI
Target URL: http://10.0.1.48:8001/api/webhooks/saleor/customer-created
Secret Key: your-webhook-secret-key
Events: CUSTOMER_CREATED
Active: ✅ Yes
```

**Note:** Replace `10.0.1.48` with the actual internal IP of Brain Gateway container.

---

### Step 4: Create CrewAI Crew Classes

#### 4.1 Order Fulfillment Crew

**File:** `bizosaas/backend/brain-gateway/app/services/crewai/order_fulfillment_crew.py`

```python
"""
Order Fulfillment CrewAI Crew
Handles autonomous order processing, inventory allocation, and shipping
"""

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List

class OrderFulfillmentCrew:
    """
    Multi-agent crew for order fulfillment automation
    """

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)

    async def process_order(
        self,
        order_id: str,
        order_number: str,
        customer_email: str,
        order_items: List[Dict],
        shipping_address: Dict,
        total_amount: float
    ) -> Dict[str, Any]:
        """
        Process order through multi-agent crew

        Workflow:
        1. Inventory Agent → Verify and allocate stock
        2. Shipping Agent → Calculate shipping and book courier
        3. Customer Service Agent → Send confirmation email
        4. Analytics Agent → Update metrics
        """

        # Define Agents
        inventory_agent = Agent(
            role="Inventory Manager",
            goal=f"Verify stock availability and allocate inventory for order {order_number}",
            backstory="Expert inventory manager with real-time stock tracking capabilities",
            llm=self.llm,
            verbose=True
        )

        shipping_agent = Agent(
            role="Shipping Coordinator",
            goal="Calculate optimal shipping method and coordinate delivery",
            backstory="Logistics expert with access to multiple courier services",
            llm=self.llm,
            verbose=True
        )

        customer_service_agent = Agent(
            role="Customer Service Representative",
            goal="Ensure excellent customer experience and communication",
            backstory="Friendly customer service expert focused on satisfaction",
            llm=self.llm,
            verbose=True
        )

        analytics_agent = Agent(
            role="Sales Analytics Specialist",
            goal="Track and analyze sales metrics and patterns",
            backstory="Data analyst monitoring business performance",
            llm=self.llm,
            verbose=True
        )

        # Define Tasks
        inventory_task = Task(
            description=f"""
            Verify stock availability for order {order_number}:
            Items: {order_items}

            1. Check each item's stock quantity
            2. Allocate inventory from appropriate warehouse
            3. Update stock levels
            4. Flag any out-of-stock items

            Return: JSON with allocation status for each item
            """,
            agent=inventory_agent,
            expected_output="Inventory allocation report"
        )

        shipping_task = Task(
            description=f"""
            Coordinate shipping for order {order_number}:
            Destination: {shipping_address}
            Total value: ${total_amount}

            1. Calculate shipping cost with multiple carriers
            2. Select optimal carrier based on cost and speed
            3. Book courier pickup
            4. Generate tracking number

            Return: Shipping details with tracking number
            """,
            agent=shipping_agent,
            expected_output="Shipping coordination report"
        )

        notification_task = Task(
            description=f"""
            Send order confirmation to customer:
            Email: {customer_email}
            Order: {order_number}

            1. Generate personalized confirmation email
            2. Include order summary and tracking info
            3. Send via email service
            4. Log communication

            Return: Email sent confirmation
            """,
            agent=customer_service_agent,
            expected_output="Customer notification report"
        )

        analytics_task = Task(
            description=f"""
            Update sales analytics for order {order_number}:
            Amount: ${total_amount}
            Items: {len(order_items)}

            1. Update daily sales metrics
            2. Track product performance
            3. Update customer lifetime value
            4. Identify upsell opportunities

            Return: Analytics update confirmation
            """,
            agent=analytics_agent,
            expected_output="Analytics update report"
        )

        # Create Crew
        crew = Crew(
            agents=[inventory_agent, shipping_agent, customer_service_agent, analytics_agent],
            tasks=[inventory_task, shipping_task, notification_task, analytics_task],
            verbose=True
        )

        # Execute Crew
        result = await crew.kickoff_async()

        return {
            "status": "completed",
            "order_number": order_number,
            "crew_result": result,
            "agents_executed": 4
        }

    async def handle_cancellation(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle order cancellation
        """
        # Implementation for cancellation handling
        pass
```

#### 4.2 Product SEO Crew

**File:** `bizosaas/backend/brain-gateway/app/services/crewai/product_seo_crew.py`

```python
"""
Product SEO CrewAI Crew
Handles product optimization, content generation, and marketing
"""

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from typing import Dict, Any

class ProductSEOCrew:
    """
    Multi-agent crew for product SEO and marketing optimization
    """

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)

    async def optimize_product(
        self,
        product_id: str,
        product_name: str,
        description: str,
        category: Dict,
        variants: list
    ) -> Dict[str, Any]:
        """
        Optimize product with multi-agent crew

        Workflow:
        1. SEO Agent → Optimize title, meta tags, URLs
        2. Content Agent → Enhance product description
        3. Marketing Agent → Create social media posts
        4. Pricing Agent → Analyze competitive pricing
        """

        # Define Agents
        seo_agent = Agent(
            role="SEO Specialist",
            goal=f"Optimize product '{product_name}' for search engines",
            backstory="Expert SEO specialist with e-commerce optimization experience",
            llm=self.llm,
            verbose=True
        )

        content_agent = Agent(
            role="Content Writer",
            goal="Create compelling product descriptions",
            backstory="Creative content writer specializing in product copywriting",
            llm=self.llm,
            verbose=True
        )

        marketing_agent = Agent(
            role="Digital Marketer",
            goal="Create engaging marketing content",
            backstory="Social media marketing expert focused on conversions",
            llm=self.llm,
            verbose=True
        )

        # Define Tasks
        seo_task = Task(
            description=f"""
            SEO optimization for product: {product_name}
            Current description: {description}
            Category: {category.get('name', 'Unknown')}

            1. Optimize product title for SEO
            2. Generate meta description (155 chars)
            3. Suggest SEO-friendly URL slug
            4. Identify target keywords
            5. Create alt text for images

            Return: SEO optimization recommendations
            """,
            agent=seo_agent,
            expected_output="SEO optimization report"
        )

        content_task = Task(
            description=f"""
            Enhance product description for: {product_name}
            Current: {description}
            Variants: {len(variants)} options

            1. Rewrite description with compelling copy
            2. Highlight key features and benefits
            3. Include size/material/care information
            4. Add urgency/scarcity elements
            5. Optimize for readability

            Return: Enhanced product description
            """,
            agent=content_agent,
            expected_output="Enhanced product description"
        )

        marketing_task = Task(
            description=f"""
            Create marketing content for: {product_name}

            1. Write social media post (Twitter/X)
            2. Write Instagram caption with hashtags
            3. Create Facebook ad copy
            4. Suggest email campaign subject line

            Return: Marketing content package
            """,
            agent=marketing_agent,
            expected_output="Marketing content package"
        )

        # Create Crew
        crew = Crew(
            agents=[seo_agent, content_agent, marketing_agent],
            tasks=[seo_task, content_task, marketing_task],
            verbose=True
        )

        # Execute Crew
        result = await crew.kickoff_async()

        return {
            "status": "completed",
            "product_name": product_name,
            "crew_result": result,
            "agents_executed": 3
        }
```

#### 4.3 Customer Service Crew

**File:** `bizosaas/backend/brain-gateway/app/services/crewai/customer_service_crew.py`

```python
"""
Customer Service CrewAI Crew
Handles customer onboarding, support, and retention
"""

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from typing import Dict, Any

class CustomerServiceCrew:
    """
    Multi-agent crew for customer service automation
    """

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)

    async def onboard_customer(
        self,
        customer_id: str,
        email: str,
        first_name: str,
        last_name: str
    ) -> Dict[str, Any]:
        """
        Onboard new customer with multi-agent crew

        Workflow:
        1. Welcome Email Agent → Send personalized welcome email
        2. Marketing Agent → Add to email campaigns
        3. Segmentation Agent → Categorize customer
        4. Retention Agent → Schedule follow-ups
        """

        # Define Agents
        email_agent = Agent(
            role="Email Marketing Specialist",
            goal=f"Send personalized welcome email to {first_name}",
            backstory="Expert email marketer focused on customer engagement",
            llm=self.llm,
            verbose=True
        )

        segmentation_agent = Agent(
            role="Customer Segmentation Analyst",
            goal="Categorize customer for targeted marketing",
            backstory="Data analyst specializing in customer segmentation",
            llm=self.llm,
            verbose=True
        )

        # Define Tasks
        email_task = Task(
            description=f"""
            Send welcome email to new customer:
            Name: {first_name} {last_name}
            Email: {email}

            1. Generate personalized welcome email
            2. Include welcome discount code (10% off)
            3. Showcase popular products
            4. Provide customer service contact
            5. Send via email service

            Return: Email sent confirmation
            """,
            agent=email_agent,
            expected_output="Welcome email sent report"
        )

        segmentation_task = Task(
            description=f"""
            Segment new customer: {first_name} {last_name}

            1. Assign customer segment (new, potential high-value, etc.)
            2. Add to appropriate email campaigns
            3. Set retention strategy
            4. Schedule follow-up communications

            Return: Segmentation and campaign assignment
            """,
            agent=segmentation_agent,
            expected_output="Customer segmentation report"
        )

        # Create Crew
        crew = Crew(
            agents=[email_agent, segmentation_agent],
            tasks=[email_task, segmentation_task],
            verbose=True
        )

        # Execute Crew
        result = await crew.kickoff_async()

        return {
            "status": "completed",
            "customer_email": email,
            "crew_result": result,
            "agents_executed": 2
        }

    async def send_shipping_notification(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send shipping notification email
        """
        # Implementation for shipping notifications
        pass
```

#### 4.4 Procurement Crew

**File:** `bizosaas/backend/brain-gateway/app/services/crewai/procurement_crew.py`

```python
"""
Procurement CrewAI Crew
Handles inventory replenishment and supplier management
"""

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from typing import Dict, Any

class ProcurementCrew:
    """
    Multi-agent crew for procurement automation
    """

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)

    async def handle_low_stock(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle low stock situation with multi-agent crew

        Workflow:
        1. Supplier Agent → Contact suppliers for quotes
        2. Pricing Agent → Analyze costs and negotiate
        3. Quality Agent → Verify supplier quality
        4. Purchasing Agent → Place replenishment order
        """

        # Implementation for procurement handling
        pass
```

---

### Step 5: Environment Configuration

#### 5.1 Add Environment Variables

**File:** `bizosaas/backend/brain-gateway/.env`

```bash
# Saleor Webhook Configuration
SALEOR_WEBHOOK_SECRET=your-webhook-secret-key-here-change-this
SALEOR_API_URL=http://10.0.1.47:8000/graphql/
SALEOR_DASHBOARD_URL=https://stg.coreldove.com/dashboard/

# CrewAI Configuration
OPENAI_API_KEY=sk-proj-your-openai-key
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key

# Email Service (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

---

### Step 6: Testing Procedures

#### 6.1 Test Webhook Endpoint

```bash
# Test webhook health
curl https://stg.coreldove.com/api/webhooks/saleor/health

# Expected response:
{
  "status": "healthy",
  "service": "saleor-webhooks",
  "timestamp": "2025-11-03T10:30:00Z"
}
```

#### 6.2 Test Order Creation Webhook

```bash
# Simulate order created webhook
curl -X POST https://stg.coreldove.com/api/webhooks/saleor/order-created \
  -H "Content-Type: application/json" \
  -H "Saleor-Signature: test-signature" \
  -d '{
    "order": {
      "id": "T3JkZXI6MQ==",
      "number": "TEST-12345",
      "user_email": "test@example.com",
      "total_gross_amount": 150.00,
      "lines": [
        {
          "product_name": "Test Product",
          "quantity": 2
        }
      ]
    }
  }'
```

#### 6.3 End-to-End Test

1. Login to Saleor Dashboard: `https://stg.coreldove.com/dashboard/`
2. Create a test order manually
3. Check Brain Gateway logs for webhook reception
4. Verify CrewAI crew execution
5. Confirm email notifications sent

---

## Webhook Events Coverage

### Implemented Events (Phase 1)

| Event | Webhook Endpoint | CrewAI Crew | Purpose |
|-------|-----------------|-------------|---------|
| `ORDER_CREATED` | `/order-created` | Order Fulfillment | Automate order processing |
| `ORDER_UPDATED` | `/order-updated` | Order Fulfillment | Handle status changes |
| `PRODUCT_CREATED` | `/product-created` | Product SEO | Optimize new products |
| `PRODUCT_UPDATED` | `/product-updated` | Product SEO / Procurement | Handle updates/low stock |
| `CUSTOMER_CREATED` | `/customer-created` | Customer Service | Onboard customers |

### Additional Events (Future)

| Event | Potential Use Case |
|-------|-------------------|
| `INVOICE_REQUESTED` | Auto-generate and send invoices |
| `FULFILLMENT_CREATED` | Track shipment progress |
| `PAYMENT_CAPTURED` | Fraud detection analysis |
| `PRODUCT_VARIANT_OUT_OF_STOCK` | Immediate procurement alert |
| `CUSTOMER_UPDATED` | Update segmentation |

---

## Benefits of Webhook Approach

### ✅ Immediate Advantages

1. **No Dashboard Modifications**
   - Use official Saleor Dashboard as-is
   - Get automatic updates and security patches
   - Full feature parity

2. **Autonomous Operations**
   - Orders processed without manual intervention
   - Products optimized automatically
   - Customers onboarded seamlessly

3. **Leverage All 93+ AI Agents**
   - Order Fulfillment Crew (4 agents)
   - Product SEO Crew (3 agents)
   - Customer Service Crew (2 agents)
   - Procurement Crew (4 agents)
   - Analytics Crew (3 agents)
   - Marketing Crew (5 agents)
   - +72 more specialized agents

4. **Scalability**
   - Webhooks processed asynchronously
   - No performance impact on dashboard
   - Can handle high volume

5. **Flexibility**
   - Add new webhook handlers easily
   - Customize crew behavior per event
   - Extend with more agents

---

## Deployment Checklist

### Prerequisites
- [ ] Saleor Dashboard deployed and accessible
- [ ] Brain Gateway running on KVM4
- [ ] CrewAI dependencies installed
- [ ] OpenAI/OpenRouter API keys configured

### Implementation Steps
- [ ] Create `saleor_webhooks.py` in Brain Gateway
- [ ] Implement CrewAI crew classes
- [ ] Add environment variables
- [ ] Register webhook routes in main app
- [ ] Restart Brain Gateway service

### Configuration Steps
- [ ] Login to Saleor Dashboard
- [ ] Navigate to Configuration → Webhooks
- [ ] Create 5 webhook configurations
- [ ] Test each webhook endpoint
- [ ] Verify CrewAI execution

### Validation Steps
- [ ] Webhook health check passes
- [ ] Order creation triggers crew
- [ ] Product creation triggers SEO
- [ ] Customer creation sends email
- [ ] Logs show successful execution

---

## Monitoring and Observability

### Log Monitoring

```bash
# Watch Brain Gateway logs for webhook events
docker logs -f [brain-gateway-container-id] | grep "webhook"

# Check CrewAI execution logs
docker logs -f [brain-gateway-container-id] | grep "CrewAI"
```

### Metrics to Track

1. **Webhook Processing**
   - Total webhooks received
   - Processing time per webhook
   - Failed webhook attempts
   - Retry count

2. **CrewAI Execution**
   - Crew execution time
   - Agent success rate
   - Task completion rate
   - Error frequency

3. **Business Impact**
   - Order fulfillment time reduction
   - Customer onboarding completion rate
   - Product SEO improvement metrics
   - Inventory stockout prevention

---

## Next Steps After Implementation

1. **Phase 1 Complete** ✅
   - Official dashboard deployed
   - Webhook integration active
   - 93+ AI agents accessible

2. **Phase 2 (Future Enhancement)**
   - Custom AI-powered admin interface
   - Real-time agent recommendations
   - Predictive analytics dashboard
   - Advanced automation workflows

3. **Continuous Improvement**
   - Add more webhook event handlers
   - Expand CrewAI crew capabilities
   - Optimize agent prompts
   - Enhance automation logic

---

## Support and Documentation

### Related Documents
- [SALEOR_DASHBOARD_CONFIGURATION_VERIFICATION.md](./SALEOR_DASHBOARD_CONFIGURATION_VERIFICATION.md)
- [SALEOR_DASHBOARD_COMPLETE_DEPLOYMENT_GUIDE.md](./SALEOR_DASHBOARD_COMPLETE_DEPLOYMENT_GUIDE.md)

### API Documentation
- Saleor Webhooks: https://docs.saleor.io/docs/3.x/developer/extending/webhooks
- CrewAI Framework: https://docs.crewai.com/

### Contact
- Platform Team: bizoholic.digital@gmail.com
- Deployment Issues: Check Dokploy logs
- CrewAI Issues: Check Brain Gateway logs

---

**Implementation Status:** Ready to Proceed
**Estimated Time:** 2-4 hours for full implementation
**Priority:** HIGH - Enables autonomous platform operations
**Last Updated:** November 3, 2025

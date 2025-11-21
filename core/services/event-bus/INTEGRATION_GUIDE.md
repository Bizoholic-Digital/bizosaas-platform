# Event Bus Integration Guide

This guide shows how to integrate existing BizOSaaS services with the Event Bus for autonomous AI agent coordination.

## 🎯 Integration Overview

The Event Bus enables:
- **AI Agents** to coordinate tasks autonomously
- **CRM Service** to trigger AI analysis when leads are created
- **Campaign Service** to receive optimization suggestions from AI
- **Cross-service communication** through domain events

## 🔧 Integration Examples

### 1. AI Agents Service Integration

**File**: `/home/alagiri/projects/bizoholic/bizosaas/services/ai-agents/event_integration.py`

```python
import asyncio
import httpx
from uuid import uuid4

class AIAgentsEventIntegration:
    def __init__(self, event_bus_url="http://localhost:8009"):
        self.event_bus_url = event_bus_url
        self.client = httpx.AsyncClient()
    
    async def initialize_subscriptions(self):
        """Subscribe to events that require AI processing"""
        
        # Subscribe to lead creation for automatic scoring
        await self.client.post(f"{self.event_bus_url}/events/subscribe", json={
            "event_type": "lead.created",
            "service_name": "ai-agents",
            "webhook_url": f"http://localhost:8001/events/lead-created"
        })
        
        # Subscribe to analysis requests
        await self.client.post(f"{self.event_bus_url}/events/subscribe", json={
            "event_type": "ai.analysis_requested", 
            "service_name": "ai-agents",
            "webhook_url": f"http://localhost:8001/events/analysis-requested"
        })
    
    async def handle_new_lead(self, event_data):
        """Handle new lead events for automatic analysis"""
        lead_id = event_data["data"]["lead_id"]
        tenant_id = event_data["tenant_id"]
        
        # Trigger lead scoring analysis
        await self.publish_analysis_request(
            tenant_id=tenant_id,
            analysis_type="lead_scoring",
            target_id=lead_id,
            parameters={"auto_triggered": True}
        )
    
    async def publish_analysis_results(self, tenant_id, analysis_id, results):
        """Publish AI analysis completion"""
        await self.client.post(f"{self.event_bus_url}/events/publish", json={
            "event_type": "ai.analysis_completed",
            "tenant_id": tenant_id,
            "source_service": "ai-agents",
            "data": {
                "analysis_id": analysis_id,
                "results": results,
                "confidence_score": results.get("confidence", 85)
            },
            "priority": "high"
        })
    
    async def publish_analysis_request(self, tenant_id, analysis_type, target_id, parameters):
        """Request AI analysis"""
        await self.client.post(f"{self.event_bus_url}/events/publish", json={
            "event_type": "ai.analysis_requested",
            "tenant_id": tenant_id,
            "source_service": "ai-agents",
            "data": {
                "analysis_type": analysis_type,
                "target_id": target_id,
                "parameters": parameters
            }
        })

# Add to your AI Agents service main.py
ai_integration = AIAgentsEventIntegration()

@app.on_event("startup")
async def setup_event_integration():
    await ai_integration.initialize_subscriptions()

# Webhook endpoints to receive events
@app.post("/events/lead-created")
async def handle_lead_created(event_data: dict):
    await ai_integration.handle_new_lead(event_data)
    return {"status": "processed"}

@app.post("/events/analysis-requested")
async def handle_analysis_requested(event_data: dict):
    # Process analysis request
    analysis_type = event_data["data"]["analysis_type"]
    target_id = event_data["data"]["target_id"]
    
    # Perform analysis (your existing logic)
    results = await perform_analysis(analysis_type, target_id)
    
    # Publish results
    await ai_integration.publish_analysis_results(
        tenant_id=event_data["tenant_id"],
        analysis_id=str(uuid4()),
        results=results
    )
    return {"status": "analyzed"}
```

### 2. Django CRM Integration

**File**: `/home/alagiri/projects/bizoholic/bizosaas/services/django-crm/event_integration.py`

```python
import asyncio
import httpx
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lead

class CRMEventIntegration:
    def __init__(self, event_bus_url="http://localhost:8009"):
        self.event_bus_url = event_bus_url
        self.client = httpx.AsyncClient()
    
    async def publish_lead_created(self, lead):
        """Publish lead creation event"""
        try:
            response = await self.client.post(f"{self.event_bus_url}/events/publish", json={
                "event_type": "lead.created",
                "tenant_id": str(lead.tenant_id),
                "source_service": "django-crm",
                "data": {
                    "lead_id": str(lead.id),
                    "contact_info": {
                        "email": lead.email,
                        "company": lead.company,
                        "phone": lead.phone
                    },
                    "source": lead.source,
                    "created_at": lead.created_at.isoformat()
                },
                "priority": "high",
                "target_services": ["ai-agents", "marketing-automation"]
            })
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to publish lead event: {e}")
            return False

# Django signal integration
crm_integration = CRMEventIntegration()

@receiver(post_save, sender=Lead)
def lead_created_handler(sender, instance, created, **kwargs):
    """Handle lead creation signals"""
    if created:  # Only for new leads
        # Run async operation in thread
        import threading
        
        def publish_event():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(crm_integration.publish_lead_created(instance))
            loop.close()
        
        thread = threading.Thread(target=publish_event)
        thread.start()

# Add webhook endpoint for receiving AI analysis results
# In your Django views.py:

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def ai_analysis_webhook(request):
    """Receive AI analysis results"""
    if request.method == 'POST':
        try:
            event_data = json.loads(request.body)
            analysis_type = event_data["data"]["analysis_type"]
            
            if analysis_type == "lead_scoring":
                target_id = event_data["data"]["target_id"]
                results = event_data["data"]["results"]
                score = results.get("score", 0)
                
                # Update lead with AI score
                try:
                    lead = Lead.objects.get(id=target_id)
                    lead.ai_score = score
                    lead.ai_analysis_results = results
                    lead.save()
                    
                    # If high score, mark as hot lead
                    if score > 80:
                        lead.status = "hot"
                        lead.save()
                        
                except Lead.DoesNotExist:
                    pass
            
            return JsonResponse({"status": "processed"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)
```

### 3. Campaign Management Integration

**File**: `/home/alagiri/projects/bizoholic/bizosaas/services/campaign-management/event_integration.py`

```python
import asyncio
import httpx
from uuid import uuid4

class CampaignEventIntegration:
    def __init__(self, event_bus_url="http://localhost:8009"):
        self.event_bus_url = event_bus_url
        self.client = httpx.AsyncClient()
    
    async def initialize_subscriptions(self):
        """Subscribe to AI optimization events"""
        await self.client.post(f"{self.event_bus_url}/events/subscribe", json={
            "event_type": "ai.analysis_completed",
            "service_name": "campaign-management",
            "filters": {"analysis_type": "campaign_optimization"},
            "webhook_url": "http://localhost:8005/events/optimization-results"
        })
    
    async def publish_campaign_launched(self, campaign_id, tenant_id, campaign_data):
        """Publish campaign launch event"""
        await self.client.post(f"{self.event_bus_url}/events/publish", json={
            "event_type": "campaign.launched",
            "tenant_id": tenant_id,
            "source_service": "campaign-management",
            "data": {
                "campaign_id": campaign_id,
                "campaign_type": campaign_data.get("type"),
                "budget": campaign_data.get("budget"),
                "target_audience": campaign_data.get("audience")
            },
            "target_services": ["ai-agents", "analytics-service"]
        })
    
    async def handle_optimization_results(self, event_data):
        """Handle AI optimization suggestions"""
        campaign_id = event_data["data"]["target_id"]
        suggestions = event_data["data"]["results"].get("optimization_suggestions", [])
        
        # Apply high-impact suggestions automatically
        for suggestion in suggestions:
            if suggestion.get("impact") == "high":
                await self.apply_optimization(campaign_id, suggestion)
    
    async def apply_optimization(self, campaign_id, suggestion):
        """Apply optimization suggestion"""
        # Your campaign optimization logic here
        print(f"Applying optimization to {campaign_id}: {suggestion}")
        
        # Publish optimization applied event
        await self.client.post(f"{self.event_bus_url}/events/publish", json={
            "event_type": "campaign.optimized",
            "tenant_id": "your-tenant-id",
            "source_service": "campaign-management",
            "data": {
                "campaign_id": campaign_id,
                "optimization_applied": suggestion,
                "applied_automatically": True
            }
        })
```

## 🔗 Service Webhook Endpoints

Each service should implement webhook endpoints to receive events:

### Standard Webhook Pattern

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class EventWebhook(BaseModel):
    event_id: str
    event_type: str
    tenant_id: str
    source_service: str
    data: dict
    timestamp: str

@app.post("/events/{event_type}")
async def handle_event(event_type: str, webhook_data: EventWebhook):
    """Generic event handler"""
    try:
        # Route to specific handler based on event type
        handler_map = {
            "lead.created": handle_lead_created,
            "ai.analysis_completed": handle_analysis_completed,
            "campaign.launched": handle_campaign_launched
        }
        
        handler = handler_map.get(event_type.replace(".", "_"))
        if handler:
            await handler(webhook_data)
            return {"status": "processed"}
        else:
            return {"status": "ignored", "reason": "no handler"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## 🚀 Quick Integration Steps

### 1. Add Event Bus Client

```bash
# In your service directory
pip install httpx asyncio
```

### 2. Initialize Event Integration

```python
# In your service's main.py or __init__.py
from .event_integration import YourServiceEventIntegration

event_integration = YourServiceEventIntegration()

@app.on_event("startup")
async def setup_events():
    await event_integration.initialize_subscriptions()
```

### 3. Add Webhook Endpoints

```python
# Add webhook routes for receiving events
@app.post("/events/lead-created")
async def webhook_lead_created(event_data: dict):
    await event_integration.handle_lead_created(event_data)
    return {"status": "processed"}
```

### 4. Publish Events

```python
# When important events occur in your service
await event_integration.publish_event(
    event_type="your.event_type",
    tenant_id=tenant_id,
    data=event_data
)
```

## 📊 Testing Integration

### 1. Start Event Bus
```bash
cd /home/alagiri/projects/bizoholic/bizosaas/services/event-bus
python3 standalone_main.py
```

### 2. Test Event Publishing
```bash
curl -X POST "http://localhost:8009/demo/create-lead?tenant_id=550e8400-e29b-41d4-a716-446655440000"
```

### 3. Check Metrics
```bash
curl -s "http://localhost:8009/metrics" | jq
```

### 4. View Event History
```bash
curl -X POST "http://localhost:8009/events/history" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "550e8400-e29b-41d4-a716-446655440000",
    "limit": 10
  }'
```

## 🤖 AI Agent Coordination Workflow

Here's how the complete AI agent coordination works:

```
1. Lead Created (CRM) 
   ↓
2. Event: lead.created → Event Bus
   ↓  
3. AI Agents receive event → Auto-trigger lead scoring
   ↓
4. Event: ai.analysis_requested → Event Bus
   ↓
5. AI Agent processes → Lead scoring analysis
   ↓
6. Event: ai.analysis_completed → Event Bus
   ↓
7. CRM receives results → Updates lead score
   ↓
8. If high score → Event: lead.qualified → Event Bus
   ↓
9. Campaign Service → Adjusts targeting for similar leads
   ↓
10. Analytics Service → Updates conversion predictions
```

## 🔄 Event-Driven Patterns

### Pattern 1: Trigger and Response
```python
# Service A publishes trigger event
await publish_event("analysis.requested", data)

# Service B processes and responds  
await publish_event("analysis.completed", results)
```

### Pattern 2: Broadcast Notification
```python
# Notify all interested services
await publish_event("campaign.launched", {
    "target_services": ["ai-agents", "analytics", "crm"]
})
```

### Pattern 3: Chain of Responsibility
```python
# Each service in chain processes and forwards
await publish_event("lead.processing_step_completed", {
    "next_step": "qualification",
    "processor": "ai-agents"
})
```

## 📈 Monitoring and Debugging

### Event Bus Dashboard
- **Metrics**: http://localhost:8009/metrics
- **Health**: http://localhost:8009/health  
- **API Docs**: http://localhost:8009/docs

### Key Metrics to Monitor
- `events_published` - Total events published
- `active_subscriptions` - Number of active subscriptions
- `event_store_size` - Number of events in memory store

### Debugging Tips
1. **Check Event History**: Use `/events/history` to see what events were published
2. **Verify Subscriptions**: Use `/subscriptions` to see active subscriptions  
3. **Test Webhooks**: Use `/demo/*` endpoints to test event flow
4. **Monitor Logs**: Check service logs for webhook delivery status

This integration enables autonomous AI agent coordination across your BizOSaaS platform, creating intelligent workflows that automatically optimize campaigns, score leads, and coordinate cross-service tasks.
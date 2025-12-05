"""
Integration Examples for BizOSaaS Event Bus

Demonstrates how different services can integrate with the event bus
for autonomous AI agent coordination and cross-service communication.
"""

import asyncio
from datetime import datetime
from uuid import UUID, uuid4

from client_sdk import EventBusClient, EventBusClientConfig, create_event_bus_client
from domain_events import (
    LeadCreated, CampaignLaunched, AIAnalysisCompleted, 
    AgentTaskAssigned, EventPriority
)


# Example 1: AI Agents Service Integration

class AIAgentsEventIntegration:
    """
    Shows how AI Agents service integrates with the event bus
    for coordinating autonomous agent tasks
    """
    
    def __init__(self, event_bus_client: EventBusClient):
        self.client = event_bus_client
        self.active_tasks = {}
    
    async def initialize(self):
        """Set up event subscriptions for AI agents"""
        
        # Subscribe to analysis requests
        await self.client.subscribe_to_events(
            event_type="ai.analysis_requested",
            handler=self.handle_analysis_request
        )
        
        # Subscribe to lead creation for automatic processing
        await self.client.subscribe_to_events(
            event_type="lead.created",
            handler=self.handle_new_lead
        )
        
        # Subscribe to campaign launches for optimization
        await self.client.subscribe_to_events(
            event_type="campaign.launched",
            handler=self.handle_campaign_launch
        )
    
    async def handle_analysis_request(self, event):
        """Handle incoming analysis requests"""
        analysis_type = event.data.get("analysis_type")
        target_id = event.data.get("target_id")
        parameters = event.data.get("parameters", {})
        
        print(f"🤖 AI Agent received analysis request: {analysis_type} for {target_id}")
        
        # Assign task to appropriate agent
        agent_id = self.select_best_agent(analysis_type)
        task_id = str(uuid4())
        
        # Publish agent task assignment
        await self.client.publish_event(
            event_type="agent.task_assigned",
            tenant_id=event.tenant_id,
            data={
                "task_id": task_id,
                "agent_id": agent_id,
                "task_type": analysis_type,
                "target_id": target_id,
                "parameters": parameters
            },
            correlation_id=event.event_id
        )
        
        # Simulate task processing
        await self.process_analysis_task(task_id, analysis_type, target_id, event.tenant_id, event.event_id)
    
    async def handle_new_lead(self, event):
        """Automatically analyze new leads"""
        lead_id = event.data.get("lead_id")
        contact_info = event.data.get("contact_info", {})
        
        print(f"🔍 Auto-analyzing new lead: {lead_id}")
        
        # Request lead scoring analysis
        await self.client.publish_event(
            event_type="ai.analysis_requested",
            tenant_id=event.tenant_id,
            data={
                "analysis_type": "lead_scoring",
                "target_id": lead_id,
                "parameters": {
                    "contact_info": contact_info,
                    "auto_triggered": True
                }
            },
            priority=EventPriority.HIGH,
            correlation_id=event.event_id
        )
    
    async def handle_campaign_launch(self, event):
        """Automatically set up campaign monitoring"""
        campaign_id = event.data.get("campaign_id")
        
        print(f"📊 Setting up campaign monitoring: {campaign_id}")
        
        # Request campaign analysis setup
        await self.client.publish_event(
            event_type="ai.analysis_requested",
            tenant_id=event.tenant_id,
            data={
                "analysis_type": "campaign_monitoring",
                "target_id": campaign_id,
                "parameters": {
                    "monitoring_interval": 3600,  # 1 hour
                    "auto_optimization": True
                }
            },
            correlation_id=event.event_id
        )
    
    def select_best_agent(self, analysis_type: str) -> str:
        """Select the best AI agent for a task"""
        agent_mapping = {
            "lead_scoring": "lead-qualification-agent",
            "campaign_optimization": "campaign-optimizer-agent",
            "campaign_monitoring": "performance-monitor-agent",
            "competitor_analysis": "market-research-agent",
            "content_generation": "content-creator-agent"
        }
        
        return agent_mapping.get(analysis_type, "general-analysis-agent")
    
    async def process_analysis_task(self, task_id: str, analysis_type: str, target_id: str, tenant_id: UUID, correlation_id: UUID):
        """Simulate processing an analysis task"""
        
        # Simulate processing time
        await asyncio.sleep(2)
        
        # Generate mock results based on analysis type
        results = self.generate_mock_results(analysis_type)
        
        # Publish task completion
        await self.client.publish_event(
            event_type="agent.task_completed",
            tenant_id=tenant_id,
            data={
                "task_id": task_id,
                "agent_id": self.select_best_agent(analysis_type),
                "task_type": analysis_type,
                "target_id": target_id,
                "success": True,
                "results": results
            },
            correlation_id=correlation_id
        )
        
        # Publish analysis completed
        await self.client.publish_event(
            event_type="ai.analysis_completed",
            tenant_id=tenant_id,
            data={
                "analysis_id": task_id,
                "analysis_type": analysis_type,
                "target_id": target_id,
                "results": results,
                "confidence_score": results.get("confidence", 85)
            },
            priority=EventPriority.HIGH,
            correlation_id=correlation_id
        )
    
    def generate_mock_results(self, analysis_type: str) -> dict:
        """Generate mock analysis results"""
        if analysis_type == "lead_scoring":
            return {
                "score": 87,
                "confidence": 92,
                "factors": [
                    {"factor": "company_size", "weight": 0.3, "score": 90},
                    {"factor": "industry_match", "weight": 0.25, "score": 85},
                    {"factor": "engagement_level", "weight": 0.2, "score": 88},
                    {"factor": "budget_indicator", "weight": 0.25, "score": 85}
                ],
                "recommendations": [
                    "High-quality lead - prioritize for immediate follow-up",
                    "Strong budget indicators detected",
                    "Industry expertise aligns well with our services"
                ]
            }
        
        elif analysis_type == "campaign_optimization":
            return {
                "current_performance": {
                    "ctr": 2.3,
                    "conversion_rate": 4.1,
                    "cost_per_lead": 45.67
                },
                "optimization_suggestions": [
                    {
                        "area": "keywords",
                        "impact": "high",
                        "suggestion": "Add 5 long-tail keywords with lower competition"
                    },
                    {
                        "area": "bid_strategy",
                        "impact": "medium", 
                        "suggestion": "Increase bids for high-converting keywords by 15%"
                    }
                ],
                "projected_improvement": {
                    "ctr_increase": "+12%",
                    "cost_reduction": "-8%"
                }
            }
        
        else:
            return {
                "status": "completed",
                "insights": ["Analysis completed successfully"],
                "confidence": 75
            }


# Example 2: CRM Service Integration

class CRMEventIntegration:
    """
    Shows how CRM service integrates with event bus
    for lead management and customer lifecycle events
    """
    
    def __init__(self, event_bus_client: EventBusClient):
        self.client = event_bus_client
    
    async def initialize(self):
        """Set up CRM event subscriptions"""
        
        # Subscribe to AI analysis results
        await self.client.subscribe_to_events(
            event_type="ai.analysis_completed",
            handler=self.handle_analysis_results
        )
        
        # Subscribe to agent task completions
        await self.client.subscribe_to_events(
            event_type="agent.task_completed", 
            handler=self.handle_agent_task_completion
        )
    
    async def create_new_lead(self, tenant_id: UUID, contact_info: dict, source: str):
        """Create a new lead and trigger events"""
        lead_id = uuid4()
        
        # Store lead in CRM database (simulated)
        print(f"📝 CRM: Creating new lead {lead_id} from {source}")
        
        # Publish lead created event
        await self.client.publish_event(
            event_type="lead.created",
            tenant_id=tenant_id,
            data={
                "lead_id": str(lead_id),
                "source": source,
                "contact_info": contact_info,
                "created_at": datetime.utcnow().isoformat(),
                "status": "new"
            },
            priority=EventPriority.HIGH,
            target_services=["ai-agents", "marketing-automation"]
        )
        
        return lead_id
    
    async def handle_analysis_results(self, event):
        """Handle AI analysis results"""
        analysis_type = event.data.get("analysis_type")
        target_id = event.data.get("target_id")
        results = event.data.get("results", {})
        
        if analysis_type == "lead_scoring":
            score = results.get("score", 0)
            print(f"📊 CRM: Updating lead {target_id} with AI score: {score}")
            
            # Update lead in database (simulated)
            if score > 80:
                # High-quality lead - create opportunity
                await self.create_opportunity_from_lead(target_id, score, event.tenant_id)
            elif score > 60:
                # Medium quality - add to nurture campaign
                await self.add_to_nurture_campaign(target_id, event.tenant_id)
        
        elif analysis_type == "campaign_optimization":
            print(f"📈 CRM: Received campaign optimization for {target_id}")
            suggestions = results.get("optimization_suggestions", [])
            
            # Log optimization suggestions (in real implementation, notify campaign manager)
            for suggestion in suggestions:
                print(f"   💡 {suggestion['area']}: {suggestion['suggestion']}")
    
    async def handle_agent_task_completion(self, event):
        """Handle agent task completions"""
        task_type = event.data.get("task_type")
        success = event.data.get("success")
        agent_id = event.data.get("agent_id")
        
        print(f"✅ CRM: Agent {agent_id} completed {task_type} - Success: {success}")
        
        # Log agent activity for performance tracking
        if not success:
            print(f"⚠️  Task failed: {event.data.get('error', 'Unknown error')}")
    
    async def create_opportunity_from_lead(self, lead_id: str, score: int, tenant_id: UUID):
        """Create opportunity from high-scoring lead"""
        opportunity_id = uuid4()
        
        print(f"🎯 CRM: Creating opportunity {opportunity_id} from lead {lead_id}")
        
        # Publish opportunity created event
        await self.client.publish_event(
            event_type="opportunity.created",
            tenant_id=tenant_id,
            data={
                "opportunity_id": str(opportunity_id),
                "lead_id": lead_id,
                "score": score,
                "stage": "qualification",
                "created_by": "ai_lead_scoring"
            },
            target_services=["sales-automation", "analytics-service"]
        )
    
    async def add_to_nurture_campaign(self, lead_id: str, tenant_id: UUID):
        """Add lead to nurture campaign"""
        print(f"🌱 CRM: Adding lead {lead_id} to nurture campaign")
        
        # Publish nurture event
        await self.client.publish_event(
            event_type="lead.added_to_nurture",
            tenant_id=tenant_id,
            data={
                "lead_id": lead_id,
                "campaign_type": "nurture",
                "sequence": "standard_b2b_nurture"
            },
            target_services=["marketing-automation"]
        )


# Example 3: Campaign Management Integration

class CampaignManagementEventIntegration:
    """
    Shows how Campaign Management service integrates with event bus
    """
    
    def __init__(self, event_bus_client: EventBusClient):
        self.client = event_bus_client
    
    async def initialize(self):
        """Set up campaign management subscriptions"""
        
        # Subscribe to optimization suggestions
        await self.client.subscribe_to_events(
            event_type="ai.analysis_completed",
            handler=self.handle_optimization_results,
            filters={"analysis_type": "campaign_optimization"}
        )
        
        # Subscribe to lead qualification for budget allocation
        await self.client.subscribe_to_events(
            event_type="lead.qualified",
            handler=self.handle_qualified_lead
        )
    
    async def launch_campaign(self, tenant_id: UUID, campaign_data: dict):
        """Launch a new campaign"""
        campaign_id = uuid4()
        
        print(f"🚀 Campaign: Launching campaign {campaign_id}")
        
        # Publish campaign launched event
        await self.client.publish_event(
            event_type="campaign.launched",
            tenant_id=tenant_id,
            data={
                "campaign_id": str(campaign_id),
                "campaign_type": campaign_data.get("type", "ppc"),
                "budget": campaign_data.get("budget", 1000),
                "target_audience": campaign_data.get("audience", {}),
                "objectives": campaign_data.get("objectives", [])
            },
            priority=EventPriority.HIGH,
            target_services=["ai-agents", "analytics-service"]
        )
        
        return campaign_id
    
    async def handle_optimization_results(self, event):
        """Handle campaign optimization suggestions"""
        target_id = event.data.get("target_id")
        results = event.data.get("results", {})
        
        suggestions = results.get("optimization_suggestions", [])
        projected_improvement = results.get("projected_improvement", {})
        
        print(f"🎯 Campaign: Received optimization for campaign {target_id}")
        
        # Apply high-impact suggestions automatically
        for suggestion in suggestions:
            if suggestion.get("impact") == "high":
                await self.apply_optimization_suggestion(target_id, suggestion, event.tenant_id)
        
        # Log projected improvements
        if projected_improvement:
            print(f"   📈 Projected CTR increase: {projected_improvement.get('ctr_increase', 'N/A')}")
            print(f"   💰 Projected cost reduction: {projected_improvement.get('cost_reduction', 'N/A')}")
    
    async def apply_optimization_suggestion(self, campaign_id: str, suggestion: dict, tenant_id: UUID):
        """Apply an optimization suggestion"""
        area = suggestion.get("area")
        suggestion_text = suggestion.get("suggestion")
        
        print(f"⚡ Campaign: Auto-applying optimization to {campaign_id}: {area}")
        
        # Publish optimization applied event
        await self.client.publish_event(
            event_type="campaign.optimized",
            tenant_id=tenant_id,
            data={
                "campaign_id": campaign_id,
                "optimization_area": area,
                "optimization_applied": suggestion_text,
                "applied_by": "ai_auto_optimizer"
            },
            target_services=["analytics-service"]
        )
    
    async def handle_qualified_lead(self, event):
        """Adjust campaign budgets based on lead quality"""
        lead_source = event.data.get("source")
        qualification_score = event.data.get("qualification_score", 0)
        
        print(f"💡 Campaign: Lead qualified from {lead_source} with score {qualification_score}")
        
        # If high-quality lead, potentially increase budget for that source
        if qualification_score > 85:
            print(f"   📊 Considering budget increase for {lead_source} campaigns")


# Demo/Testing Function

async def run_integration_demo():
    """
    Run a comprehensive demo of event bus integrations
    showing autonomous AI agent coordination
    """
    
    print("🚀 Starting BizOSaaS Event Bus Integration Demo")
    print("=" * 60)
    
    # Create event bus clients for different services
    ai_client = await create_event_bus_client("ai-agents")
    crm_client = await create_event_bus_client("crm-service") 
    campaign_client = await create_event_bus_client("campaign-service")
    
    # Initialize service integrations
    ai_integration = AIAgentsEventIntegration(ai_client)
    crm_integration = CRMEventIntegration(crm_client)
    campaign_integration = CampaignManagementEventIntegration(campaign_client)
    
    # Set up event subscriptions
    await ai_integration.initialize()
    await crm_integration.initialize()
    await campaign_integration.initialize()
    
    print("✅ All services initialized and subscribed to events")
    print()
    
    # Simulate a complete workflow
    tenant_id = uuid4()
    
    # Step 1: New lead comes in
    print("📝 STEP 1: New lead creation")
    lead_id = await crm_integration.create_new_lead(
        tenant_id=tenant_id,
        contact_info={
            "email": "john.doe@techcorp.com",
            "company": "TechCorp Inc",
            "phone": "+1-555-0123",
            "industry": "Technology"
        },
        source="website_form"
    )
    
    # Wait for AI processing
    await asyncio.sleep(3)
    print()
    
    # Step 2: Launch a campaign
    print("🚀 STEP 2: Campaign launch")
    campaign_id = await campaign_integration.launch_campaign(
        tenant_id=tenant_id,
        campaign_data={
            "type": "google_ads",
            "budget": 5000,
            "audience": {"industry": "technology", "company_size": "medium"},
            "objectives": ["lead_generation", "brand_awareness"]
        }
    )
    
    # Wait for AI analysis
    await asyncio.sleep(3)
    print()
    
    # Step 3: Simulate lead qualification
    print("🎯 STEP 3: Lead qualification")
    await crm_client.publish_event(
        event_type="lead.qualified",
        tenant_id=tenant_id,
        data={
            "lead_id": str(lead_id),
            "qualification_score": 89,
            "qualified_by": "ai_scoring_agent",
            "source": "website_form"
        }
    )
    
    # Wait for processing
    await asyncio.sleep(2)
    print()
    
    # Step 4: Request campaign optimization
    print("📊 STEP 4: Campaign optimization request")
    await ai_client.publish_event(
        event_type="ai.analysis_requested",
        tenant_id=tenant_id,
        data={
            "analysis_type": "campaign_optimization",
            "target_id": str(campaign_id),
            "parameters": {
                "current_performance": {
                    "ctr": 1.8,
                    "conversion_rate": 3.2,
                    "cost_per_lead": 67.50
                }
            }
        }
    )
    
    # Wait for optimization
    await asyncio.sleep(3)
    print()
    
    print("🎉 Demo completed! Event-driven workflow executed successfully.")
    print("💡 This demonstrates autonomous AI agent coordination through events.")
    
    # Cleanup
    await ai_client.disconnect()
    await crm_client.disconnect()
    await campaign_client.disconnect()


if __name__ == "__main__":
    asyncio.run(run_integration_demo())
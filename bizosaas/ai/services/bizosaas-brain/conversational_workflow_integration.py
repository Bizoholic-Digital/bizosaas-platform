#!/usr/bin/env python3
"""
Conversational Workflow Integration
Bridges natural language commands with Temporal workflow orchestration
Makes workflow creation through conversational AI the primary method
"""

import asyncio
import json
import logging
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import uuid
import httpx

# Import existing Temporal integration
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'temporal-integration'))
from temporal_client import (
    TemporalClient,
    WorkflowRequest,
    WorkflowResponse,
    WorkflowType,
    WorkflowStatus,
    AIAgentWorkflowOrchestrator
)

logger = logging.getLogger(__name__)

class ConversationalIntent(str, Enum):
    """Natural language intents for workflow operations"""
    CREATE_WORKFLOW = "create_workflow"
    START_WORKFLOW = "start_workflow"
    CHECK_STATUS = "check_status"
    CANCEL_WORKFLOW = "cancel_workflow"
    LIST_WORKFLOWS = "list_workflows"
    SCHEDULE_WORKFLOW = "schedule_workflow"
    OPTIMIZE_WORKFLOW = "optimize_workflow"
    GET_SUGGESTIONS = "get_suggestions"

class WorkflowComplexity(str, Enum):
    """Workflow complexity levels for conversational creation"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"

@dataclass
class ConversationalWorkflowRequest:
    """Natural language workflow request"""
    user_intent: str
    workflow_description: str
    tenant_id: str
    user_id: str
    context: Dict[str, Any]
    constraints: Optional[Dict[str, Any]] = None
    priority: str = "normal"  # low, normal, high, urgent

@dataclass
class WorkflowTemplate:
    """Pre-configured workflow templates"""
    template_id: str
    name: str
    description: str
    workflow_type: WorkflowType
    complexity: WorkflowComplexity
    required_inputs: List[str]
    optional_inputs: List[str]
    estimated_duration: int  # minutes
    agent_types: List[str]
    keywords: List[str]
    example_triggers: List[str]

class ConversationalWorkflowProcessor:
    """Processes natural language workflow requests"""
    
    def __init__(self, temporal_client: TemporalClient):
        self.temporal_client = temporal_client
        self.orchestrator = AIAgentWorkflowOrchestrator(temporal_client)
        self.templates = self._initialize_templates()
        self.active_conversations = {}
    
    def _initialize_templates(self) -> Dict[str, WorkflowTemplate]:
        """Initialize workflow templates with conversational triggers"""
        templates = {
            "customer_onboarding": WorkflowTemplate(
                template_id="customer_onboarding",
                name="AI Customer Onboarding",
                description="Automate new customer onboarding with AI-powered welcome sequences",
                workflow_type=WorkflowType.AI_CUSTOMER_ONBOARDING,
                complexity=WorkflowComplexity.MODERATE,
                required_inputs=["customer_email", "customer_name"],
                optional_inputs=["company_name", "industry", "preferences"],
                estimated_duration=30,
                agent_types=["email_agent", "crm_agent", "communication_agent"],
                keywords=["onboard", "welcome", "new customer", "setup", "introduction"],
                example_triggers=[
                    "onboard new customers automatically",
                    "create welcome sequence for new users",
                    "set up customer introduction workflow"
                ]
            ),
            "lead_qualification": WorkflowTemplate(
                template_id="lead_qualification",
                name="AI Lead Qualification",
                description="Automatically qualify and score leads using AI analysis",
                workflow_type=WorkflowType.AI_LEAD_QUALIFICATION,
                complexity=WorkflowComplexity.MODERATE,
                required_inputs=["lead_data"],
                optional_inputs=["scoring_criteria", "qualification_rules"],
                estimated_duration=15,
                agent_types=["analytics_agent", "crm_agent", "scoring_agent"],
                keywords=["qualify", "score", "leads", "prospects", "assessment"],
                example_triggers=[
                    "qualify incoming leads",
                    "score prospects automatically",
                    "assess lead quality with AI"
                ]
            ),
            "content_generation": WorkflowTemplate(
                template_id="content_generation",
                name="AI Content Generation",
                description="Generate marketing content across multiple channels",
                workflow_type=WorkflowType.AI_CONTENT_GENERATION,
                complexity=WorkflowComplexity.SIMPLE,
                required_inputs=["content_topic", "target_audience"],
                optional_inputs=["content_type", "tone", "channels"],
                estimated_duration=20,
                agent_types=["content_agent", "seo_agent", "social_media_agent"],
                keywords=["content", "generate", "create", "write", "blog", "social"],
                example_triggers=[
                    "create blog content about our product",
                    "generate social media posts",
                    "write marketing copy for campaign"
                ]
            ),
            "campaign_optimization": WorkflowTemplate(
                template_id="campaign_optimization",
                name="Campaign Optimization",
                description="Optimize marketing campaigns using AI insights",
                workflow_type=WorkflowType.CAMPAIGN_OPTIMIZATION,
                complexity=WorkflowComplexity.COMPLEX,
                required_inputs=["campaign_id"],
                optional_inputs=["optimization_goals", "constraints", "budget"],
                estimated_duration=45,
                agent_types=["analytics_agent", "optimization_agent", "reporting_agent"],
                keywords=["optimize", "improve", "campaign", "performance", "analysis"],
                example_triggers=[
                    "optimize my Google Ads campaign",
                    "improve email campaign performance",
                    "analyze and enhance marketing ROI"
                ]
            ),
            "product_sourcing": WorkflowTemplate(
                template_id="product_sourcing",
                name="E-commerce Product Sourcing",
                description="Find and analyze products for e-commerce using AI",
                workflow_type=WorkflowType.AMAZON_SPAPI_SOURCING,
                complexity=WorkflowComplexity.COMPLEX,
                required_inputs=["product_category"],
                optional_inputs=["price_range", "margin_targets", "competition_level"],
                estimated_duration=60,
                agent_types=["sourcing_agent", "analytics_agent", "market_research_agent"],
                keywords=["source", "find", "products", "amazon", "e-commerce", "research"],
                example_triggers=[
                    "find profitable products to sell",
                    "research trending items on Amazon",
                    "source products for my store"
                ]
            ),
            "customer_support": WorkflowTemplate(
                template_id="customer_support",
                name="AI Customer Support",
                description="Automated customer support with AI-powered responses",
                workflow_type=WorkflowType.AI_CUSTOMER_SUPPORT,
                complexity=WorkflowComplexity.MODERATE,
                required_inputs=["support_channel"],
                optional_inputs=["escalation_rules", "knowledge_base", "response_tone"],
                estimated_duration=25,
                agent_types=["support_agent", "knowledge_agent", "escalation_agent"],
                keywords=["support", "help", "customer service", "tickets", "inquiries"],
                example_triggers=[
                    "automate customer support responses",
                    "handle support tickets with AI",
                    "create intelligent help system"
                ]
            )
        }
        
        return templates
    
    async def process_natural_language_request(self, request: ConversationalWorkflowRequest) -> Dict[str, Any]:
        """Process natural language workflow request"""
        try:
            # Parse the user intent and extract workflow requirements
            parsed_intent = await self._parse_user_intent(request.user_intent)
            
            if parsed_intent["intent"] == ConversationalIntent.CREATE_WORKFLOW:
                return await self._handle_create_workflow(request, parsed_intent)
            elif parsed_intent["intent"] == ConversationalIntent.START_WORKFLOW:
                return await self._handle_start_workflow(request, parsed_intent)
            elif parsed_intent["intent"] == ConversationalIntent.CHECK_STATUS:
                return await self._handle_check_status(request, parsed_intent)
            elif parsed_intent["intent"] == ConversationalIntent.LIST_WORKFLOWS:
                return await self._handle_list_workflows(request)
            elif parsed_intent["intent"] == ConversationalIntent.GET_SUGGESTIONS:
                return await self._handle_get_suggestions(request)
            else:
                return {
                    "success": False,
                    "message": "I didn't understand what workflow action you want to perform. Try 'create workflow for...' or 'start workflow to...'",
                    "suggestions": [
                        "Create a workflow to onboard new customers",
                        "Start lead qualification workflow",
                        "Show me my running workflows",
                        "Generate content for social media"
                    ]
                }
                
        except Exception as e:
            logger.error(f"Error processing workflow request: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Sorry, I encountered an error processing your workflow request."
            }
    
    async def _parse_user_intent(self, user_input: str) -> Dict[str, Any]:
        """Parse user input to determine intent and extract parameters"""
        user_input_lower = user_input.lower().strip()
        
        # Intent detection patterns
        intent_patterns = {
            ConversationalIntent.CREATE_WORKFLOW: [
                r"create.*workflow", r"build.*workflow", r"set up.*automation",
                r"automate.*process", r"make.*workflow", r"design.*flow"
            ],
            ConversationalIntent.START_WORKFLOW: [
                r"start.*workflow", r"run.*workflow", r"execute.*workflow",
                r"launch.*automation", r"begin.*process"
            ],
            ConversationalIntent.CHECK_STATUS: [
                r"status.*workflow", r"check.*workflow", r"how.*workflow",
                r"workflow.*running", r"progress.*workflow"
            ],
            ConversationalIntent.LIST_WORKFLOWS: [
                r"list.*workflows", r"show.*workflows", r"my.*workflows",
                r"active.*workflows", r"running.*workflows"
            ],
            ConversationalIntent.CANCEL_WORKFLOW: [
                r"cancel.*workflow", r"stop.*workflow", r"terminate.*workflow"
            ],
            ConversationalIntent.GET_SUGGESTIONS: [
                r"suggest.*workflow", r"recommend.*workflow", r"what.*workflow",
                r"help.*workflow", r"ideas.*workflow"
            ]
        }
        
        # Detect intent
        detected_intent = ConversationalIntent.GET_SUGGESTIONS  # default
        for intent, patterns in intent_patterns.items():
            if any(re.search(pattern, user_input_lower) for pattern in patterns):
                detected_intent = intent
                break
        
        # Extract entities based on templates
        extracted_entities = self._extract_workflow_entities(user_input_lower)
        
        return {
            "intent": detected_intent,
            "entities": extracted_entities,
            "original_input": user_input,
            "confidence": 0.8  # Mock confidence score
        }
    
    def _extract_workflow_entities(self, user_input: str) -> Dict[str, Any]:
        """Extract workflow-related entities from user input"""
        entities = {
            "workflow_type": None,
            "template_match": None,
            "parameters": {},
            "time_constraints": None,
            "priority": "normal"
        }
        
        # Match against template keywords
        for template_id, template in self.templates.items():
            keyword_matches = sum(1 for keyword in template.keywords if keyword in user_input)
            if keyword_matches > 0:
                entities["template_match"] = template_id
                entities["workflow_type"] = template.workflow_type
                break
        
        # Extract common parameters
        if "email" in user_input:
            entities["parameters"]["involves_email"] = True
        if "social media" in user_input or "social" in user_input:
            entities["parameters"]["involves_social"] = True
        if "urgent" in user_input or "asap" in user_input:
            entities["priority"] = "urgent"
        elif "high priority" in user_input:
            entities["priority"] = "high"
        
        return entities
    
    async def _handle_create_workflow(self, request: ConversationalWorkflowRequest, parsed_intent: Dict[str, Any]) -> Dict[str, Any]:
        """Handle workflow creation request"""
        entities = parsed_intent["entities"]
        
        if entities["template_match"]:
            template = self.templates[entities["template_match"]]
            
            # Check if we have required parameters
            missing_params = []
            for required in template.required_inputs:
                if required not in entities["parameters"]:
                    missing_params.append(required)
            
            if missing_params:
                return {
                    "success": False,
                    "message": f"To create this workflow, I need more information:",
                    "required_parameters": missing_params,
                    "template": {
                        "name": template.name,
                        "description": template.description,
                        "estimated_duration": f"{template.estimated_duration} minutes"
                    },
                    "action": "collect_parameters"
                }
            
            # Create workflow request
            workflow_request = WorkflowRequest(
                workflow_type=template.workflow_type,
                tenant_id=request.tenant_id,
                user_id=request.user_id,
                input_data={
                    "template_id": template.template_id,
                    "user_parameters": entities["parameters"],
                    "context": request.context,
                    "priority": entities.get("priority", "normal"),
                    "created_via": "conversational_ai"
                }
            )
            
            # Start workflow
            result = await self.temporal_client.start_workflow(workflow_request)
            
            if result.status != WorkflowStatus.FAILED:
                return {
                    "success": True,
                    "message": f"✅ Created {template.name} workflow successfully!",
                    "workflow": {
                        "id": result.workflow_id,
                        "name": template.name,
                        "type": template.workflow_type,
                        "status": result.status,
                        "estimated_duration": f"{template.estimated_duration} minutes"
                    },
                    "next_steps": [
                        f"Your workflow '{template.name}' is now running",
                        "I'll notify you when it completes",
                        "You can check status by asking 'How is my workflow doing?'"
                    ]
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to create workflow: {result.error}",
                    "error": result.error
                }
        
        else:
            # No template match - provide suggestions
            return {
                "success": False,
                "message": "I couldn't determine what type of workflow you want to create.",
                "suggestions": [
                    "Create a workflow to onboard new customers",
                    "Build automation for lead qualification", 
                    "Set up content generation workflow",
                    "Automate campaign optimization"
                ],
                "available_templates": [
                    {
                        "name": template.name,
                        "description": template.description,
                        "example": template.example_triggers[0]
                    }
                    for template in self.templates.values()
                ]
            }
    
    async def _handle_start_workflow(self, request: ConversationalWorkflowRequest, parsed_intent: Dict[str, Any]) -> Dict[str, Any]:
        """Handle workflow start request"""
        # This is similar to create_workflow but for pre-existing workflow definitions
        return await self._handle_create_workflow(request, parsed_intent)
    
    async def _handle_check_status(self, request: ConversationalWorkflowRequest, parsed_intent: Dict[str, Any]) -> Dict[str, Any]:
        """Handle workflow status check request"""
        try:
            # For now, we'll return mock status data
            # In a real implementation, this would query active workflows for the user
            active_workflows = [
                {
                    "id": "workflow_123",
                    "name": "Customer Onboarding",
                    "status": "running",
                    "progress": "60%",
                    "started": "10 minutes ago",
                    "estimated_completion": "5 minutes"
                },
                {
                    "id": "workflow_456", 
                    "name": "Lead Qualification",
                    "status": "completed",
                    "progress": "100%",
                    "started": "30 minutes ago",
                    "completed": "5 minutes ago"
                }
            ]
            
            if active_workflows:
                status_message = "Here's the status of your workflows:\n\n"
                for workflow in active_workflows:
                    status_icon = "🟢" if workflow["status"] == "running" else "✅" if workflow["status"] == "completed" else "🔴"
                    status_message += f"{status_icon} **{workflow['name']}**\n"
                    status_message += f"   Status: {workflow['status'].title()}\n"
                    status_message += f"   Progress: {workflow['progress']}\n"
                    if workflow["status"] == "running":
                        status_message += f"   ETA: {workflow['estimated_completion']}\n"
                    status_message += "\n"
                
                return {
                    "success": True,
                    "message": status_message,
                    "workflows": active_workflows
                }
            else:
                return {
                    "success": True,
                    "message": "You don't have any active workflows right now.",
                    "suggestions": [
                        "Create a new workflow to get started",
                        "Ask me 'What workflows can you help me with?'"
                    ]
                }
        
        except Exception as e:
            logger.error(f"Error checking workflow status: {e}")
            return {
                "success": False,
                "message": "Sorry, I couldn't retrieve your workflow status right now."
            }
    
    async def _handle_list_workflows(self, request: ConversationalWorkflowRequest) -> Dict[str, Any]:
        """Handle list workflows request"""
        return {
            "success": True,
            "message": "Here are the workflows I can help you create:",
            "templates": [
                {
                    "name": template.name,
                    "description": template.description,
                    "complexity": template.complexity,
                    "duration": f"{template.estimated_duration} minutes",
                    "example": template.example_triggers[0]
                }
                for template in self.templates.values()
            ],
            "actions": [
                "Just tell me what you want to automate, and I'll suggest the best workflow",
                "Try saying: 'Create a workflow to onboard new customers'"
            ]
        }
    
    async def _handle_get_suggestions(self, request: ConversationalWorkflowRequest) -> Dict[str, Any]:
        """Handle workflow suggestions request"""
        # Get suggestions based on user context and tenant
        context_suggestions = []
        
        # Analyze user's context to provide relevant suggestions
        if "marketing" in request.context.get("current_focus", ""):
            context_suggestions.extend([
                "Create content generation workflow for social media",
                "Set up lead qualification automation",
                "Automate email marketing campaigns"
            ])
        
        if "ecommerce" in request.context.get("current_focus", ""):
            context_suggestions.extend([
                "Find profitable products to source",
                "Automate order processing workflow",
                "Set up customer support automation"
            ])
        
        return {
            "success": True,
            "message": "Here are some workflow ideas based on your needs:",
            "suggestions": context_suggestions if context_suggestions else [
                "Automate customer onboarding for new users",
                "Create AI-powered lead qualification",
                "Generate marketing content automatically",
                "Optimize your advertising campaigns",
                "Set up customer support automation"
            ],
            "popular_workflows": [
                {
                    "name": "AI Customer Onboarding",
                    "description": "Welcome new customers with personalized sequences",
                    "example": "Create a workflow to welcome new customers"
                },
                {
                    "name": "Content Generation",
                    "description": "Generate blog posts and social media content",
                    "example": "Generate content for my social media"
                },
                {
                    "name": "Lead Qualification",
                    "description": "Automatically score and qualify leads",
                    "example": "Qualify my leads using AI"
                }
            ]
        }

# Global workflow processor instance
workflow_processor = None

async def get_workflow_processor() -> ConversationalWorkflowProcessor:
    """Get workflow processor instance"""
    global workflow_processor
    if not workflow_processor:
        temporal_client = TemporalClient()
        await temporal_client.initialize()
        workflow_processor = ConversationalWorkflowProcessor(temporal_client)
    return workflow_processor

async def process_workflow_command(
    user_input: str,
    tenant_id: str,
    user_id: str,
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """Process a natural language workflow command"""
    processor = await get_workflow_processor()
    
    request = ConversationalWorkflowRequest(
        user_intent=user_input,
        workflow_description=user_input,
        tenant_id=tenant_id,
        user_id=user_id,
        context=context
    )
    
    return await processor.process_natural_language_request(request)

# Workflow suggestion functions for the AI command processor
def is_workflow_command(user_input: str) -> bool:
    """Detect if user input is workflow-related"""
    workflow_keywords = [
        "workflow", "automate", "automation", "process", "create", "build",
        "schedule", "run", "execute", "start", "launch", "set up"
    ]
    
    user_lower = user_input.lower()
    return any(keyword in user_lower for keyword in workflow_keywords)

def extract_workflow_context(user_input: str) -> Dict[str, Any]:
    """Extract workflow context from user input"""
    context = {
        "workflow_related": True,
        "urgency": "normal",
        "automation_type": "general"
    }
    
    user_lower = user_input.lower()
    
    if any(word in user_lower for word in ["urgent", "asap", "immediately"]):
        context["urgency"] = "high"
    
    if any(word in user_lower for word in ["marketing", "campaign", "content"]):
        context["automation_type"] = "marketing"
    elif any(word in user_lower for word in ["customer", "support", "onboard"]):
        context["automation_type"] = "customer"
    elif any(word in user_lower for word in ["product", "sourcing", "ecommerce"]):
        context["automation_type"] = "ecommerce"
    
    return context
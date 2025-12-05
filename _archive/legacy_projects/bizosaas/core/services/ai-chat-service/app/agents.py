"""
AI Agent integration and management for role-based chat
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

import httpx
from .models import (
    UserRole, AgentRequest, AgentResponse, AgentCapability, 
    AIAssistant, ConversationContext
)

logger = logging.getLogger(__name__)

class CrewAIIntegration:
    """Integration with CrewAI backend service"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.timeout = 30.0
        self.retry_attempts = 3
        self.agent_endpoints = {
            # Infrastructure Management (Super Admin)
            "system_monitor": "/agents/system-monitor",
            "security_analyzer": "/agents/security-analysis",
            "performance_optimizer": "/agents/performance-optimizer",
            "infrastructure_manager": "/agents/infrastructure-manager",
            
            # Business Operations (Tenant Admin)
            "analytics_specialist": "/agents/analytics-insights",
            "customer_insights": "/agents/customer-insights", 
            "revenue_optimizer": "/agents/revenue-optimizer",
            "integration_manager": "/agents/integration-manager",
            
            # Marketing & Sales (Users)
            "campaign_optimizer": "/agents/campaign-optimizer",
            "lead_analyzer": "/agents/lead-analysis",
            "content_generator": "/agents/content-generator",
            "social_media_specialist": "/agents/social-media-specialist",
            
            # General Support (All roles)
            "support_assistant": "/agents/support-assistant",
            "information_retriever": "/agents/information-retriever"
        }
    
    async def query_agent(self, request: AgentRequest) -> AgentResponse:
        """Query a specific CrewAI agent"""
        start_time = datetime.now()
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload = {
                    "query": request.query,
                    "context": request.context.dict(),
                    "message_history": request.message_history,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "user_role": request.context.user_role,
                    "tenant_id": request.context.tenant_id
                }
                
                # Add optional parameters
                if request.max_tokens:
                    payload["max_tokens"] = request.max_tokens
                if request.temperature:
                    payload["temperature"] = request.temperature
                
                endpoint = self.agent_endpoints.get(
                    request.agent_name, 
                    "/agents/general-query"
                )
                
                # Retry logic for resilience
                last_exception = None
                for attempt in range(self.retry_attempts):
                    try:
                        response = await client.post(
                            f"{self.base_url}{endpoint}",
                            json=payload,
                            headers={
                                "Content-Type": "application/json",
                                "X-Request-ID": str(request.context.tenant_id),
                                "X-User-Role": request.context.user_role
                            }
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            processing_time = (datetime.now() - start_time).total_seconds()
                            
                            return AgentResponse(
                                agent_name=request.agent_name,
                                response=data.get("response", "No response available"),
                                confidence=data.get("confidence", 0.8),
                                suggested_actions=data.get("suggested_actions", []),
                                metadata=data.get("metadata", {}),
                                processing_time=processing_time,
                                tokens_used=data.get("tokens_used")
                            )
                        elif response.status_code == 503:
                            # Service temporarily unavailable, retry
                            await asyncio.sleep(1 * (attempt + 1))
                            continue
                        else:
                            break
                            
                    except httpx.TimeoutException as e:
                        last_exception = e
                        await asyncio.sleep(1 * (attempt + 1))
                        continue
                    except Exception as e:
                        last_exception = e
                        break
                
                # All retries failed
                processing_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"CrewAI agent query failed after {self.retry_attempts} attempts: {last_exception}")
                
                return AgentResponse(
                    agent_name=request.agent_name,
                    response=self._get_fallback_response(request.agent_name, request.query),
                    confidence=0.1,
                    metadata={
                        "error": "service_unavailable",
                        "last_exception": str(last_exception),
                        "attempts": self.retry_attempts
                    },
                    processing_time=processing_time
                )
                
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Unexpected error in CrewAI integration: {e}")
            
            return AgentResponse(
                agent_name=request.agent_name,
                response="I'm experiencing technical difficulties. Please try again later.",
                confidence=0.0,
                metadata={"error": str(e)},
                processing_time=processing_time
            )
    
    def _get_fallback_response(self, agent_name: str, query: str) -> str:
        """Generate fallback response when agent is unavailable"""
        fallback_responses = {
            "system_monitor": "System monitoring agent is currently unavailable. Please check the monitoring dashboard directly or contact IT support.",
            "security_analyzer": "Security analysis agent is offline. Please refer to the security dashboard or contact the security team immediately if this is urgent.",
            "performance_optimizer": "Performance optimization agent is unavailable. Please check system metrics manually or try again later.",
            "analytics_specialist": "Analytics agent is temporarily down. Please use the reports dashboard for current data.",
            "campaign_optimizer": "Campaign optimization agent is offline. Please review campaigns manually or contact marketing support.",
            "lead_analyzer": "Lead analysis agent is unavailable. Please check the CRM directly for lead information.",
            "content_generator": "Content generation agent is offline. Please create content manually or try again later.",
            "support_assistant": "Support agent is temporarily unavailable. Please contact support directly or check the help documentation."
        }
        
        return fallback_responses.get(
            agent_name,
            "I'm temporarily unable to process your request. Please try again in a few moments or contact support if the issue persists."
        )
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of CrewAI service"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/health")
                
                if response.status_code == 200:
                    return {
                        "status": "healthy",
                        "response_time": response.elapsed.total_seconds(),
                        "data": response.json()
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "status_code": response.status_code,
                        "error": "Service returned non-200 status"
                    }
        except Exception as e:
            return {
                "status": "unavailable",
                "error": str(e)
            }

class AgentSelector:
    """Intelligent agent selection based on query content and user context"""
    
    def __init__(self):
        self.agent_capabilities = self._define_agent_capabilities()
    
    def _define_agent_capabilities(self) -> Dict[str, AgentCapability]:
        """Define capabilities for each agent"""
        return {
            "system_monitor": AgentCapability(
                name="System Monitor",
                description="Monitors system health, uptime, and infrastructure metrics",
                keywords=["system", "health", "uptime", "server", "infrastructure", "monitor", "status", "performance"],
                confidence_threshold=0.8,
                requires_data_access=True
            ),
            "security_analyzer": AgentCapability(
                name="Security Analyzer", 
                description="Analyzes security threats, vulnerabilities, and compliance",
                keywords=["security", "threat", "vulnerability", "breach", "attack", "compliance", "audit", "firewall"],
                confidence_threshold=0.9,
                requires_data_access=True
            ),
            "performance_optimizer": AgentCapability(
                name="Performance Optimizer",
                description="Optimizes system and application performance",
                keywords=["performance", "optimize", "slow", "speed", "latency", "throughput", "bottleneck", "cache"],
                confidence_threshold=0.7
            ),
            "analytics_specialist": AgentCapability(
                name="Analytics Specialist",
                description="Provides business analytics and data insights",
                keywords=["analytics", "data", "insights", "report", "metrics", "kpi", "dashboard", "trends"],
                confidence_threshold=0.7,
                requires_data_access=True
            ),
            "campaign_optimizer": AgentCapability(
                name="Campaign Optimizer",
                description="Optimizes marketing campaigns and advertising",
                keywords=["campaign", "marketing", "ads", "advertising", "conversion", "ctr", "roi", "optimize"],
                confidence_threshold=0.8
            ),
            "lead_analyzer": AgentCapability(
                name="Lead Analyzer",
                description="Analyzes leads, prospects, and sales pipeline",
                keywords=["lead", "prospect", "sales", "pipeline", "customer", "conversion", "funnel", "crm"],
                confidence_threshold=0.8,
                requires_data_access=True
            ),
            "content_generator": AgentCapability(
                name="Content Generator",
                description="Generates marketing content and copy",
                keywords=["content", "write", "create", "copy", "blog", "social", "email", "generate"],
                confidence_threshold=0.6
            ),
            "support_assistant": AgentCapability(
                name="Support Assistant",
                description="Provides general support and help",
                keywords=["help", "support", "question", "how", "what", "why", "guide", "documentation"],
                confidence_threshold=0.5
            )
        }
    
    def select_best_agent(self, query: str, available_agents: List[str], user_role: UserRole) -> str:
        """Select the best agent for a query based on content analysis"""
        query_lower = query.lower()
        
        # Calculate confidence scores for each available agent
        agent_scores = {}
        
        for agent_name in available_agents:
            capability = self.agent_capabilities.get(agent_name)
            if not capability:
                continue
            
            # Calculate keyword match score
            keyword_matches = sum(1 for keyword in capability.keywords if keyword in query_lower)
            keyword_score = keyword_matches / len(capability.keywords) if capability.keywords else 0
            
            # Apply role-based weighting
            role_weight = self._get_role_weight(agent_name, user_role)
            
            # Calculate final score
            final_score = keyword_score * role_weight
            
            if final_score >= capability.confidence_threshold:
                agent_scores[agent_name] = final_score
        
        # Return highest scoring agent, or default to first available
        if agent_scores:
            return max(agent_scores.items(), key=lambda x: x[1])[0]
        else:
            return available_agents[0] if available_agents else "support_assistant"
    
    def _get_role_weight(self, agent_name: str, user_role: UserRole) -> float:
        """Get role-based weighting for agent selection"""
        role_weights = {
            UserRole.SUPER_ADMIN: {
                "system_monitor": 1.0,
                "security_analyzer": 1.0, 
                "performance_optimizer": 1.0,
                "infrastructure_manager": 1.0,
                "analytics_specialist": 0.8,
                "support_assistant": 0.6
            },
            UserRole.TENANT_ADMIN: {
                "analytics_specialist": 1.0,
                "customer_insights": 1.0,
                "revenue_optimizer": 1.0,
                "integration_manager": 1.0,
                "campaign_optimizer": 0.8,
                "lead_analyzer": 0.8,
                "support_assistant": 0.7
            },
            UserRole.USER: {
                "campaign_optimizer": 1.0,
                "lead_analyzer": 1.0,
                "content_generator": 1.0,
                "social_media_specialist": 1.0,
                "analytics_specialist": 0.6,
                "support_assistant": 0.8
            },
            UserRole.READONLY: {
                "support_assistant": 1.0,
                "information_retriever": 1.0,
                "analytics_specialist": 0.5
            }
        }
        
        return role_weights.get(user_role, {}).get(agent_name, 0.5)

# AI Assistant configurations for each role
def get_role_assistants() -> Dict[UserRole, AIAssistant]:
    """Get AI assistant configurations for each user role"""
    return {
        UserRole.SUPER_ADMIN: AIAssistant(
            name="InfraBot",
            description="Your infrastructure management and system monitoring assistant",
            role=UserRole.SUPER_ADMIN,
            avatar="🔧",
            capabilities=[
                AgentCapability(
                    name="System Health Monitoring",
                    description="Monitor system health, uptime, and performance metrics",
                    keywords=["health", "monitor", "uptime", "system"],
                    confidence_threshold=0.8
                ),
                AgentCapability(
                    name="Security Analysis",
                    description="Analyze security threats and vulnerabilities",
                    keywords=["security", "threat", "vulnerability"],
                    confidence_threshold=0.9
                ),
                AgentCapability(
                    name="Performance Optimization",
                    description="Optimize system and application performance",
                    keywords=["performance", "optimize", "speed"],
                    confidence_threshold=0.7
                )
            ],
            available_agents=[
                "system_monitor", "security_analyzer", "performance_optimizer", "infrastructure_manager"
            ],
            default_agent="system_monitor",
            greeting_message="Hello! I'm InfraBot, your infrastructure assistant. I can help you monitor systems, analyze security, and optimize performance. What would you like to check today?",
            context_limits={"max_history": 20, "max_tokens": 4000}
        ),
        
        UserRole.TENANT_ADMIN: AIAssistant(
            name="BizBot", 
            description="Your business operations and analytics assistant",
            role=UserRole.TENANT_ADMIN,
            avatar="📊",
            capabilities=[
                AgentCapability(
                    name="Business Analytics",
                    description="Provide insights from business data and metrics",
                    keywords=["analytics", "insights", "data", "metrics"],
                    confidence_threshold=0.7
                ),
                AgentCapability(
                    name="Customer Management",
                    description="Analyze customer data and behavior",
                    keywords=["customer", "user", "behavior", "retention"],
                    confidence_threshold=0.8
                ),
                AgentCapability(
                    name="Revenue Optimization",
                    description="Optimize revenue streams and pricing",
                    keywords=["revenue", "pricing", "subscription", "billing"],
                    confidence_threshold=0.8
                )
            ],
            available_agents=[
                "analytics_specialist", "customer_insights", "revenue_optimizer", "integration_manager"
            ],
            default_agent="analytics_specialist",
            greeting_message="Hi! I'm BizBot, your business operations assistant. I can help you analyze business metrics, understand customers, and optimize revenue. What business insights do you need?",
            context_limits={"max_history": 15, "max_tokens": 3000}
        ),
        
        UserRole.USER: AIAssistant(
            name="MarketBot",
            description="Your marketing campaigns and lead management assistant", 
            role=UserRole.USER,
            avatar="🎯",
            capabilities=[
                AgentCapability(
                    name="Campaign Optimization",
                    description="Optimize marketing campaigns and advertising",
                    keywords=["campaign", "marketing", "ads", "optimization"],
                    confidence_threshold=0.8
                ),
                AgentCapability(
                    name="Lead Analysis",
                    description="Analyze leads and sales pipeline",
                    keywords=["lead", "prospect", "sales", "conversion"],
                    confidence_threshold=0.8
                ),
                AgentCapability(
                    name="Content Creation",
                    description="Generate marketing content and copy",
                    keywords=["content", "write", "create", "copy"],
                    confidence_threshold=0.6
                )
            ],
            available_agents=[
                "campaign_optimizer", "lead_analyzer", "content_generator", "social_media_specialist"
            ],
            default_agent="campaign_optimizer",
            greeting_message="Hello! I'm MarketBot, your marketing assistant. I can help optimize campaigns, analyze leads, and create content. What marketing challenge can I help you with?",
            context_limits={"max_history": 12, "max_tokens": 2500}
        ),
        
        UserRole.READONLY: AIAssistant(
            name="InfoBot",
            description="Your general business queries and support assistant",
            role=UserRole.READONLY,
            avatar="ℹ️",
            capabilities=[
                AgentCapability(
                    name="Information Retrieval",
                    description="Find information and answer general questions",
                    keywords=["what", "how", "when", "where", "why"],
                    confidence_threshold=0.5
                ),
                AgentCapability(
                    name="Support Assistance",
                    description="Provide support and guidance",
                    keywords=["help", "support", "guide", "tutorial"],
                    confidence_threshold=0.6
                )
            ],
            available_agents=["support_assistant", "information_retriever"],
            default_agent="support_assistant",
            greeting_message="Hi! I'm InfoBot, your information assistant. I can help answer questions, provide guidance, and offer support. What would you like to know?",
            context_limits={"max_history": 10, "max_tokens": 2000}
        )
    }

# Global instances
crew_ai_integration = CrewAIIntegration()
agent_selector = AgentSelector()
role_assistants = get_role_assistants()
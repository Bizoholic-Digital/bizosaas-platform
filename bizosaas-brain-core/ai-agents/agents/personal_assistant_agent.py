import asyncio
import os
import httpx
from typing import Dict, Any, List, Optional
from enum import Enum

from .base_agent import BaseAgent, AgentRole, AgentTaskRequest, AgentTaskResponse, TaskStatus
from .orchestration import HierarchicalCrewOrchestrator, OrchestrationMode

class PersonalAssistantAgent(BaseAgent):
    """
    The master orchestrator agent that provides a conversational interface 
    and coordinates 93+ specialized agents, now with RAG capabilities.
    """
    
    def __init__(self):
        super().__init__(
            agent_name="personal_assistant",
            agent_role=AgentRole.OPERATIONS,
            description="Your personal BizOSaas assistant that coordinates all specialized agents and retrieves business knowledge.",
            version="1.1.0"
        )
        self.orchestrator = HierarchicalCrewOrchestrator()
        self.brain_gateway_url = os.getenv("BRAIN_GATEWAY_URL", "http://brain-gateway:8000")
        
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """
        Handle conversational requests. If the request is specialized, 
        delegate to the appropriate agent or workflow. Use RAG for knowledge.
        """
        message = task_request.input_data.get("message", "").lower()
        
        # Specialized Routing
        if any(word in message for word in ["seo", "keyword", "search"]):
            return await self._delegate_to_workflow("seo_specialist", task_request)
        elif any(word in message for word in ["marketing", "campaign", "strategy"]):
            return await self._delegate_to_workflow("marketing_strategist", task_request)
        elif any(word in message for word in ["audit", "digital presence", "presence"]):
            return await self._delegate_to_workflow("comprehensive_digital_audit", task_request)
        elif any(word in message for word in ["ecommerce", "store", "sales"]):
            return await self._delegate_to_workflow("ecommerce_specialist", task_request)
        
        # Knowledge Retrieval via RAG
        rag_context = await self._get_rag_context(message)
        
        if rag_context:
            # In a real implementation, we would pass this context to an LLM
            # For now, we synthesize a response with the retrieved knowledge
            retrieved_info = "\n".join(rag_context[:2])
            return {
                "response": f"Based on my knowledge base: {retrieved_info}\n\nHow else can I assist you with your business today?",
                "suggestions": ["Run a Digital Audit", "Optimize my SEO", "I have more questions"],
                "agent_name": "personal_assistant",
                "metadata": {"rag_applied": True}
            }
        
        # Default conversational response
        return {
            "response": "Hello! I'm your BizOSaas Personal Assistant. I can help you with SEO, Marketing, E-commerce, or run a full Digital Audit for your business. What would you like to focus on today?",
            "suggestions": ["Run a Digital Audit", "Optimize my SEO", "Create a Marketing Plan"],
            "agent_name": "personal_assistant"
        }

    async def _get_rag_context(self, query: str) -> List[str]:
        """Call Brain Gateway RAG API to get context"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.brain_gateway_url}/api/brain/rag/retrieve",
                    json={"query": query, "limit": 3},
                    timeout=5.0
                )
                if response.status_code == 200:
                    return response.json().get("context", [])
                return []
        except Exception as e:
            self.logger.error(f"RAG retrieval failed: {e}")
            return []

    async def _delegate_to_workflow(self, workflow_id: str, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Delegate the task to the Workflow Engine / Orchestrator"""
        self.logger.info(f"Delegating specialized task to workflow: {workflow_id}")
        
        try:
            # If it's a known workflow definition
            if workflow_id in self.orchestrator.workflow_definitions:
                execution = await self.orchestrator.execute_workflow(
                    workflow_id=workflow_id,
                    input_data=task_request.input_data,
                    tenant_id=task_request.tenant_id,
                    user_id=task_request.user_id
                )
                return {
                    "response": f"I've started the {workflow_id} workflow for you. I'll notify you once the specialized agents have completed the analysis.",
                    "execution_id": execution.execution_id,
                    "status": execution.status,
                    "agent_name": "personal_assistant"
                }
            
            # If it's a direct agent call (as a fallback)
            agent = self.orchestrator.agent_registry.get(workflow_id)
            if agent:
                response = await agent.execute_task(task_request)
                return {
                    "response": response.result.get("response", f"The {workflow_id} agent has completed your request."),
                    "details": response.result,
                    "agent_name": workflow_id
                }
                
            return {"response": f"I recognized you want help with {workflow_id}, but the specialized system is currently warming up. Can I help with something else?"}
            
        except Exception as e:
            self.logger.error(f"Delegation failed: {e}")
            return {"response": f"I tried to coordinate with my specialized team for {workflow_id}, but encountered an error. Let's try something simpler!"}

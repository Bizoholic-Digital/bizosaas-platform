import asyncio
import os
import httpx
from typing import Dict, Any, List, Optional
from enum import Enum

from .base_agent import BaseAgent, AgentRole, AgentTaskRequest, AgentTaskResponse, TaskStatus
from .orchestration import HierarchicalCrewOrchestrator, OrchestrationMode
from .intelligent_routing import IntelligentRouter
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

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
        
        # Initialize Intelligent Router
        llm = self._get_llm_for_task({"temperature": 0.0})
        self.router = IntelligentRouter(self.orchestrator, llm)
        self.memory = MemorySaver()
        
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """
        Handle conversational requests. If the request is specialized, 
        delegate to the appropriate agent or workflow. Use RAG for knowledge.
        Supports 'CSM' (Client Success Manager) mode for proactive guidance.
        """
        message = task_request.input_data.get("message", "").lower()
        persona = task_request.input_data.get("persona", "general_assistant")
        
        # CSM Specific Logic
        if persona == "csm":
            if any(word in message for word in ["status", "how is it going", "progress", "impact"]):
                return await self._delegate_to_workflow("impact_analysis", task_request)
            
            # Proactive CSM Guidance
            if not message: # Initial encounter
                return {
                    "response": "Hello! I'm your Client Success Manager. I've finished auditing your connected accounts and I'm ready to help you launch your first campaign. Shall we review the recommended strategy?",
                    "suggestions": ["Review Strategy", "Check Discovery Results", "I have a question"],
                    "agent_name": "csm"
                }

        # Advanced Intent Classification via LangGraph
        try:
            config = {"configurable": {"thread_id": task_request.user_id or "default"}}
            state_input = {"messages": [HumanMessage(content=message)]}
            
            # Run the router
            graph_result = await self.router.ainvoke(state_input, config)
            
            # Check for HITL (Approval required)
            if graph_result.get("is_sensitive") and not graph_result.get("approved"):
                return {
                    "response": f"I've identified that you want to start the '{graph_result.get('candidate_workflow')}' workflow. Since this is a sensitive action, I need your confirmation to proceed.",
                    "suggestions": ["Confirm and Proceed", "Cancel"],
                    "agent_name": "personal_assistant",
                    "metadata": {"requires_approval": True, "workflow_id": graph_result.get("candidate_workflow")}
                }

            routing_result = graph_result.get("routing_result")
            if routing_result and routing_result.get("status") == "initiated":
                 return await self._delegate_to_workflow(routing_result["workflow_id"], task_request)
                 
        except Exception as e:
            self.logger.error(f"Intelligent routing failed, falling back: {e}")

        # Knowledge Retrieval via RAG
        rag_context = await self._get_rag_context(message)
        
        if rag_context:
            retrieved_info = "\n".join(rag_context[:2])
            return {
                "response": f"Based on my knowledge base: {retrieved_info}\n\nHow else can I assist you with your business today?",
                "suggestions": ["Run a Digital Audit", "Optimize my SEO", "I have more questions"],
                "agent_name": "personal_assistant",
                "metadata": {"rag_applied": True}
            }
        
        # Default conversational response
        default_response = await self._get_prompt("general_assistant_prompt", {"input": message or "How can you help me?"})
        return {
            "response": default_response,
            "suggestions": ["Run a Digital Audit", "Optimize my SEO", "Create a Marketing Plan", "Launch a Campaign"],
            "agent_name": "personal_assistant"
        }

    async def _classify_intent(self, message: str) -> Optional[str]:
        """Classify user intent into a specific workflow ID using LLM"""
        try:
            from langchain.prompts import PromptTemplate
            from langchain.schema import HumanMessage, SystemMessage
            
            # Get available workflows
            workflows = list(self.orchestrator.workflow_definitions.keys())
            # Add standalone agents if needed (usually covered by workflows or specialized agents)
            # For now, focus on workflows as they are the primary "skills"
            
            prompt = f"""
            You are the Routing System for the BizOSaas Personal Assistant.
            Your job is to map the user's message to the most appropriate Workflow ID.
            
            Available Workflows:
            {", ".join(workflows)}
            
            Additional Options:
            - general_chat (if the message is greeting, small talk, or vague)
            - unknown (if you are unsure)
            
            User Message: "{message}"
            
            Return ONLY the Workflow ID (or general_chat/unknown). Do not add any explanation.
            """
            
            # Use the agent's configured LLM (fast model preferred)
            llm = self._get_llm_for_task(config={"temperature": 0.0, "model_provider": "groq"}) # Fast model
            
            response = await llm.ainvoke([HumanMessage(content=prompt)])
            intent = response.content.strip().lower()
            
            # Validate intent
            if intent in workflows:
                return intent
            if intent == "general_chat":
                return "general_chat"
                
            return None
            
        except ImportError:
            self.logger.warning("LangChain not available for intent classification")
            return None
        except Exception as e:
            self.logger.error(f"Intent classification error: {e}")
            return None

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

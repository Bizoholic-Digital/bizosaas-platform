import operator
from typing import Annotated, Dict, List, Any, Optional, Union
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from agents.base_agent import BaseAgent
import structlog

logger = structlog.get_logger(__name__)

class AgentState(TypedDict):
    """The state of the agent graph."""
    messages: Annotated[List[BaseMessage], operator.add]
    candidate_workflow: Optional[str]
    is_sensitive: bool
    approved: Optional[bool]
    routing_result: Optional[Dict[str, Any]]

class IntelligentRouter:
    def __init__(self, orchestrator: Any, llm_provider: Any):
        self.orchestrator = orchestrator
        self.llm = llm_provider  # This should be a LangChain Chat Model
        self.workflow_definitions = orchestrator.workflow_definitions
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        # Define nodes
        workflow.add_node("classify_intent", self._classify_intent)
        workflow.add_node("check_sensitivity", self._check_sensitivity)
        workflow.add_node("request_approval", self._request_approval)
        workflow.add_node("execute_workflow", self._execute_workflow)

        # Define edges
        workflow.set_entry_point("classify_intent")
        workflow.add_edge("classify_intent", "check_sensitivity")
        
        workflow.add_conditional_edges(
            "check_sensitivity",
            self._should_request_approval,
            {
                "request": "request_approval",
                "skip": "execute_workflow"
            }
        )

        workflow.add_edge("request_approval", END) # The graph pauses here for interrupt
        workflow.add_edge("execute_workflow", END)

        return workflow.compile(interrupt_before=["request_approval"])

    async def _classify_intent(self, state: AgentState) -> Dict[str, Any]:
        """Classify user intent into a workflow."""
        last_message = state["messages"][-1].content
        
        # Build prompt from registered workflows
        workflow_list = "\n".join([f"- {fid}: {w.description}" for fid, w in self.workflow_definitions.items()])
        
        prompt = ChatPromptTemplate.from_template("""
        You are the Brain OS Dispatcher. Your job is to classify the user's request into one of the available workflows.
        
        Available Workflows:
        {workflows}
        
        If the request does not match any workflow, return 'none'.
        
        User Request: {input}
        
        Return ONLY the workflow ID or 'none'.
        """)
        
        chain = prompt | self.llm
        result = await chain.ainvoke({"workflows": workflow_list, "input": last_message})
        workflow_id = result.content.strip().lower()
        
        if workflow_id not in self.workflow_definitions:
            workflow_id = None
            
        logger.info("Classified intent", workflow_id=workflow_id)
        return {"candidate_workflow": workflow_id}

    def _check_sensitivity(self, state: AgentState) -> Dict[str, Any]:
        """Check if the selected workflow is sensitive and needs HITL."""
        workflow_id = state.get("candidate_workflow")
        sensitive_workflows = ["campaign_launch", "delete_data", "update_billing"] # Examples
        
        is_sensitive = workflow_id in sensitive_workflows
        logger.info("Checked sensitivity", workflow_id=workflow_id, is_sensitive=is_sensitive)
        return {"is_sensitive": is_sensitive}

    def _should_request_approval(self, state: AgentState) -> str:
        """Route based on sensitivity and existing approval."""
        if state.get("is_sensitive") and not state.get("approved"):
            return "request"
        return "skip"

    async def _request_approval(self, state: AgentState) -> Dict[str, Any]:
        """Node that waits for human approval. The graph will stop here."""
        # This node is actually just a placeholder for the interrupt
        return {}

    async def _execute_workflow(self, state: AgentState) -> Dict[str, Any]:
        """Actually execute the selected workflow."""
        workflow_id = state.get("candidate_workflow")
        if not workflow_id:
            return {"routing_result": {"status": "error", "message": "No matching workflow found."}}
        
        # We delegate the actual execution to the orchestrator
        # In a real scenario, this might be an async call or a Temporal trigger
        result = {"status": "initiated", "workflow_id": workflow_id, "message": f"Successfully routed to {workflow_id}"}
        return {"routing_result": result}

    async def ainvoke(self, input_data: Dict[str, Any], config: Dict[str, Any] = None):
        """Invoke the graph with the given input."""
        return await self.graph.ainvoke(input_data, config)

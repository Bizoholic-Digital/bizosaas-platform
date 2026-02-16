import asyncio
import os
import json
import sys
from datetime import datetime, timezone

# Add parent dir to path to import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock missing dependencies to allow importing BaseAgent in isolation
import sys
sys.modules['crewai'] = type('Mock', (), {'Agent': object, 'Task': object, 'Crew': object, 'Process': object})
sys.modules['crewai_tools'] = type('Mock', (), {'SerperDevTool': object, 'ScrapeWebsiteTool': object})

from agents.base_agent import BaseAgent, AgentRole, AgentTaskRequest, AgentTaskResponse, TaskStatus
import structlog

# Mock Agent for testing
class TestBridgeAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="BridgeTestAgent",
            agent_role=AgentRole.OPERATIONS,
            description="Agent to test RAG and Persona bridge"
        )
    
    async def _execute_agent_logic(self, task_request):
        # Verify persona was injected
        persona = task_request.input_data.get("brand_persona")
        if persona:
            print(f"✅ Persona injected: {json.dumps(persona)[:50]}...")
        else:
            print("❌ Persona NOT injected")
            
        # Verify RAG context was added
        if task_request.context:
            print(f"✅ RAG context added: {len(task_request.context)} chunks")
        else:
            print("❌ RAG context NOT added")
            
        return {"status": "test_complete", "received_persona": bool(persona), "received_context": bool(task_request.context)}

    async def _validate_tenant_access(self, tenant_id, user_id):
        return True

    async def _update_task_status(self, task_id, status):
        return True

async def run_test():
    # Set mock gateway URL
    os.environ["BRAIN_GATEWAY_URL"] = "http://localhost:8000" 
    
    agent = TestBridgeAgent()
    await agent.initialize()
    
    task = AgentTaskRequest(
        tenant_id="test-tenant-123",
        agent_name="BridgeTestAgent",
        task_type="test",
        task_description="Explain our SEO strategy for next quarter.",
        input_data={},
        config={"use_rag": True, "use_persona": True, "store_memory": True}
    )
    
    print("Running bridge test task...")
    try:
        response = await agent.execute_task(task)
        print(f"Task completed with status: {response.status}")
        print(f"Result: {json.dumps(response.result, indent=2)}")
    except Exception as e:
        print(f"Caught expected error (if gateway down): {e}")

if __name__ == "__main__":
    asyncio.run(run_test())

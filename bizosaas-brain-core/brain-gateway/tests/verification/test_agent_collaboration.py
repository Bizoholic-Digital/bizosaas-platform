
import asyncio
import logging
import json
from unittest.mock import AsyncMock, patch
from app.services.agent_orchestrator import agent_orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mock User
class MockUser:
    id = "user_123"
    tenant_id = "test_tenant"

async def test_orchestrator():
    print("\n--- Testing AgentOrchestrator ---\n")
    
    user = MockUser()
    request_text = "Analyze the competitive landscape for 'Eco-friendly Coffee Cups' and then suggest a marketing strategy."
    
    # Mock Plan JSON
    mock_plan = {
        "thought_process": "I need to research competitors first, then create a strategy.",
        "delegation_plan": [
            {
                "step_id": 1,
                "agent_id": "market_research",
                "task": "Find top 3 competitors for eco-friendly coffee cups.",
                "context": "Focus on US market."
            },
            {
                "step_id": 2,
                "agent_id": "marketing_strategist",
                "task": "Create a marketing strategy based on competitor research.",
                "dependencies": [1]
            }
        ]
    }
    
    # Mock Responses
    async def mock_call_ai_agent_with_rag(*args, **kwargs):
        agent_type = kwargs.get("agent_type")
        task = kwargs.get("task_description")
        
        print(f"Mock Call -> Agent: {agent_type}")
        
        if agent_type == "master_orchestrator":
            if "delegation plan" in task:
                return {"response": json.dumps(mock_plan)}
            else:
                return {"response": "Final Consolidated Answer: Based on research, here is the strategy..."}
        
        elif agent_type == "market_research":
             return {"response": "Competitor 1: GreenCup, Competitor 2: EcoBrew..."}
             
        elif agent_type == "marketing_strategist":
             return {"response": "Strategy: Emphasize sustainability and durability."}
             
        return {"response": "Unknown agent response"}

    # Patch the external call
    with patch("app.services.agent_orchestrator.call_ai_agent_with_rag", side_effect=mock_call_ai_agent_with_rag):
        
        result = await agent_orchestrator.process_request(request_text, user)
        
        # Verify
        print("\n--- Result Verification ---")
        trace = result.get("orchestration_trace", {})
        results = trace.get("results", {})
        
        assert len(results) == 2, f"Failed: Expected 2 steps executed, got {len(results)}"
        assert results[1]["response"] == "Competitor 1: GreenCup, Competitor 2: EcoBrew...", "Failed: Step 1 result mismatch"
        assert results[2]["response"] == "Strategy: Emphasize sustainability and durability.", "Failed: Step 2 result mismatch"
        
        print("✅ Orchestrator Plan Execution Verified")
        print(f"Final Response: {result['response']}")

    print("\n🎉 AgentOrchestrator Verification Passed!")

if __name__ == "__main__":
    asyncio.run(test_orchestrator())

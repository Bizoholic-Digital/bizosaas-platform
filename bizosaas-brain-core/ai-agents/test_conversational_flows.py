import asyncio
import os
import logging
from unittest.mock import MagicMock, patch

# Configure Environment
os.environ["OPENAI_API_KEY"] = "sk-mock-key"
os.environ["GROQ_API_KEY"] = "gsk-mock-key"

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ConversationalTest")

# Imports
from agents.personal_assistant_agent import PersonalAssistantAgent
from agents.base_agent import AgentTaskRequest
from agents.orchestration import HierarchicalCrewOrchestrator
from langchain_core.messages import HumanMessage

async def test_langgraph_routing():
    logger.info("\n=== Testing LangGraph Intelligent Routing ===")
    
    agent = PersonalAssistantAgent()
    
    # Mock the router invocation
    with patch.object(agent.router, 'ainvoke', new_callable=MagicMock) as mock_ainvoke:
        # Test Case 1: Sensitive Action (Campaign Launch) - Should return HITL response
        mock_ainvoke.return_value = asyncio.Future()
        mock_ainvoke.return_value.set_result({
            "candidate_workflow": "campaign_launch",
            "is_sensitive": True,
            "approved": False,
            "messages": [HumanMessage(content="launch campaign")]
        })
        
        request = AgentTaskRequest(
            tenant_id="test-tenant",
            user_id="test-user",
            agent_name="personal_assistant",
            task_type="chat",
            input_data={"message": "launch campaign"}
        )
        
        result = await agent._execute_agent_logic(request)
        logger.info(f"Sensitive Action Result: {result}")
        
        if result.get("metadata", {}).get("requires_approval") == True:
            logger.info("✅ PASS: Correctly triggered HITL for sensitive action")
        else:
            logger.error(f"❌ FAIL: Expected HITL, got {result}")

        # Test Case 2: Non-sensitive routing
        mock_ainvoke.return_value = asyncio.Future()
        mock_ainvoke.return_value.set_result({
            "candidate_workflow": "comprehensive_digital_audit",
            "is_sensitive": False,
            "approved": False,
            "routing_result": {"status": "initiated", "workflow_id": "comprehensive_digital_audit"}
        })
        
        agent._delegate_to_workflow = MagicMock(return_value=asyncio.Future())
        agent._delegate_to_workflow.return_value.set_result({"status": "delegated", "workflow": "comprehensive_digital_audit"})
        
        result = await agent._execute_agent_logic(request)
        logger.info(f"Standard Routing Result: {result.get('workflow')}")
        
        if result.get("workflow") == "comprehensive_digital_audit":
            logger.info("✅ PASS: Correctly routed non-sensitive action")
        else:
            logger.error(f"❌ FAIL: Expected 'comprehensive_digital_audit', got {result}")

async def test_campaign_launch_crew_init():
    logger.info("\n=== Testing Campaign Launch Crew Initialization ===")
    from agents.workflow_crews import CampaignLaunchCrew
    
    try:
        crew = CampaignLaunchCrew()
        logger.info("✅ PASS: CampaignLaunchCrew initialized successfully")
        logger.info(f"  - Strategist: {crew.strategist}")
        logger.info(f"  - Content Creator: {crew.content_creator}")
        logger.info(f"  - SEO Specialist: {crew.seo_specialist}")
        return True
    except Exception as e:
        logger.error(f"❌ FAIL: Initialization failed: {e}")
        return False

async def main():
    await test_langgraph_routing()
    await test_campaign_launch_crew_init()

if __name__ == "__main__":
    asyncio.run(main())

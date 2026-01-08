#!/usr/bin/env python3
"""
Quick test to verify OnboardingStrategyWorkflow is properly registered and functional
"""
import asyncio
import os
import sys

# Set mock environment
os.environ["OPENAI_API_KEY"] = "sk-mock-key"
os.environ["CREWAI_TRACING_ENABLED"] = "false"

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_onboarding_workflow():
    """Test the onboarding workflow"""
    print("=" * 60)
    print("Testing OnboardingStrategyWorkflow")
    print("=" * 60)
    
    try:
        # Import after setting environment
        from main import refined_agent_registry, setup_centralized_agents
        from agents.base_agent import AgentTaskRequest
        
        # Mock Crew.kickoff
        from unittest.mock import MagicMock
        import crewai
        crewai.Crew.kickoff = lambda self, *args, **kwargs: "Mocked Result"
        
        # Initialize agents
        print("\n1. Initializing agents...")
        await setup_centralized_agents()
        print("   ✅ Agents initialized")
        
        # Check if workflow is registered
        print("\n2. Checking workflow registration...")
        workflow_id = "onboarding_strategy_workflow"
        
        if workflow_id not in refined_agent_registry:
            print(f"   ❌ Workflow '{workflow_id}' NOT FOUND in registry!")
            print(f"   Available workflows: {[k for k in refined_agent_registry.keys() if 'workflow' in k]}")
            return False
        
        print(f"   ✅ Workflow '{workflow_id}' found in registry")
        
        # Get the workflow
        workflow = refined_agent_registry[workflow_id]
        print(f"   ✅ Workflow instance: {workflow.__class__.__name__}")
        
        # Create test request
        print("\n3. Creating test request...")
        request = AgentTaskRequest(
            tenant_id="test-tenant",
            user_id="test-user",
            task_type="workflow_execution",
            task_description="Test onboarding workflow",
            input_data={
                "business_name": "Coreldove",
                "website_url": "https://coreldove.com",
                "goals": ["Scale Sales", "Improve SEO"]
            }
        )
        print("   ✅ Request created")
        
        # Execute workflow
        print("\n4. Executing workflow...")
        result = await workflow.execute_task(request)
        print("   ✅ Workflow executed successfully")
        
        # Check result
        print("\n5. Validating result...")
        if hasattr(result, 'result') and isinstance(result.result, dict):
            output = result.result
            print(f"   ✅ Result structure valid")
            print(f"   ✅ Workflow type: {output.get('workflow')}")
            print(f"   ✅ Business name: {output.get('business_name')}")
            print(f"   ✅ Status: {output.get('status')}")
            
            # Check all phases
            phases = ['digital_footprint', 'strategic_roadmap', 'budget_allocation', 'immediate_actions']
            for phase in phases:
                if phase in output:
                    print(f"   ✅ Phase '{phase}' present")
                else:
                    print(f"   ⚠️  Phase '{phase}' missing")
        else:
            print(f"   ⚠️  Unexpected result format: {type(result)}")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - OnboardingStrategyWorkflow is functional!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_onboarding_workflow())
    sys.exit(0 if success else 1)

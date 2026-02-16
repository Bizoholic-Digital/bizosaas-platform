import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from agents.documentation_agent import DocumentationAgent, DocumentationTaskType
from agents.base_agent import AgentTaskRequest

@pytest.fixture
def doc_agent():
    with patch('agents.base_agent.prompt_registry', new_callable=AsyncMock), \
         patch('agents.documentation_agent.Agent'), \
         patch('agents.base_agent.BaseAgent._get_llm_for_task', return_value=None):
        return DocumentationAgent()




@pytest.mark.asyncio
async def test_api_doc_generation(doc_agent):
    # Mock file reading and crew execution
    mock_request = AgentTaskRequest(
        tenant_id="test_tenant",
        user_id="test_user",
        agent_name="documentation_agent",
        task_type=DocumentationTaskType.API_DOC_GENERATION,
        input_data={
            "target_path": "agents/base_agent.py",
            "output_file": "docs/test_api_doc.md"
        }
    )
    
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', MagicMock()), \
         patch('agents.documentation_agent.Crew') as mock_crew_class:
        
        mock_crew = mock_crew_class.return_value
        mock_crew.kickoff.return_value = "## Sample API Documentation"
        
        # We need to mock _get_prompt too since it's an async method in BaseAgent
        with patch.object(DocumentationAgent, '_get_prompt', return_value="Mocked Prompt"):
            result = await doc_agent.execute_task(mock_request)
            
            assert result.status == "completed"
            assert "Sample API Documentation" in result.result['documentation']
            assert "docs/test_api_doc.md" in result.result['file_saved']

@pytest.mark.asyncio
async def test_invalid_task_type(doc_agent):
    mock_request = AgentTaskRequest(
        tenant_id="test_tenant",
        user_id="test_user",
        agent_name="documentation_agent",
        task_type="invalid_task",
        input_data={}
    )

    
    result = await doc_agent.execute_task(mock_request)
    assert result.status == "failed"
    assert "Unsupported task type" in result.error_message


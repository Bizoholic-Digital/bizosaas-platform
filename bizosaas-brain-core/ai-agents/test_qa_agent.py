
import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import json
import asyncio

# --- MOCKING DEPENDENCIES START ---
def module_exists(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def mock_package(name):
    # Only create if not exists
    if name in sys.modules:
        return sys.modules[name]
        
    m = MagicMock()
    # Fix for importlib inspection in Python 3.12+
    m.__spec__ = MagicMock()
    m.__loader__ = MagicMock()
    m.__package__ = name
    m.__path__ = [] # Mark as package
    m.__file__ = "mocked"
    sys.modules[name] = m
    return m

# List of all potential heavy/external dependencies to mock
dependencies_to_mock = [
    "crewai", "crewai.tools", "crewai.process", "crewai.agent", "crewai.task", "crewai.crew", "crewai_tools",
    "langchain", "langchain.tools", "langchain_core", "langchain_core.prompts", "langchain_core.tools", 
    "langchain_openai", "langchain_community",
    "pydantic",
    "requests",
    "structlog",
    "litellm",
    "tiktoken",
    "chromadb",
    "opentelemetry",
    "opentelemetry.api",
    "redis",
    "psycopg2",
    "fastapi",
    "uvicorn",
    "numpy",
    "pandas",
    "sklearn"
]

# Create mocks
for dep in dependencies_to_mock:
    mock_package(dep)

# Link submodules to parents
for dep in dependencies_to_mock:
    parts = dep.split('.')
    if len(parts) > 1:
        parent_name = ".".join(parts[:-1])
        child_name = parts[-1]
        if parent_name in sys.modules:
            setattr(sys.modules[parent_name], child_name, sys.modules[dep])

# Special Pydantic handling
if 'pydantic' in sys.modules:
    pm = sys.modules['pydantic']
    # Define a real minimalist BaseModel so inheritance works if needed
    class MockBaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    pm.BaseModel = MockBaseModel
    pm.Field = MagicMock(return_value=None)

# --- MOCKING DEPENDENCIES END ---

# Adjust path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import
from agents.base_agent import AgentTaskRequest, TaskPriority

class AgentType:
    QUALITY_ASSURANCE = "quality_assurance"
from agents.quality_assurance_agent import RefinedQualityAssuranceAgent

# Mock environment variables
os.environ["OPENAI_API_KEY"] = "sk-mock-key"
os.environ["OPENROUTER_API_KEY"] = "sk-mock-router"

class TestRefinedQualityAssuranceAgent(unittest.TestCase):
    
    def setUp(self):
        # Patch Agent at class level where it is imported
        with patch("agents.quality_assurance_agent.Agent") as MockAgent:
            # We also need to patch the BaseAgent's __init__ because it might try to do things
            with patch("agents.base_agent.BaseAgent.__init__", return_value=None) as MockBaseInit:
                self.agent = RefinedQualityAssuranceAgent()
                # Manually set attributes usually set by BaseAgent
                self.agent.agent_name = "quality_assurance_auditor"
                self.agent.logger = MagicMock()
                self.agent.crewai_agent = MagicMock()
                self.agent.crewai_agent.role = "Quality Assurance Auditor"

        self.task_request = AgentTaskRequest(
            agent_type=AgentType.QUALITY_ASSURANCE,
            task_description="Test Audit",
            input_data={
                "content_to_review": "This is a sample generated blog post that is too short.",
                "context": "Write a 500 word blog post about AI.",
                "criteria": ["Length", "Accuracy"]
            },
            priority=TaskPriority.NORMAL
        )

    def test_initialization(self):
        print("\nTesting Initialization...")
        self.assertEqual(self.agent.agent_name, "quality_assurance_auditor")
        print("Initialization Passed.")

    @patch("agents.quality_assurance_agent.Crew")
    @patch("agents.quality_assurance_agent.Task")
    def test_audit_execution_success(self, MockTask, MockCrew):
        print("\nTesting Audit Execution Success...")
        # Setup Mock Crew output
        mock_crew_instance = MagicMock()
        MockCrew.return_value = mock_crew_instance
        
        # Simulate LLM returning valid JSON
        mock_response = """
        {
            "overall_score": 8.5,
            "relevance_score": 9,
            "clarity_score": 8,
            "feedback_summary": "Good start but needs more depth.",
            "improvement_suggestions": ["Add more examples", "Explain technical terms"],
            "is_approved": true
        }
        """
        mock_crew_instance.kickoff.return_value = mock_response

        # Execute async method synchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.agent._execute_agent_logic(self.task_request))
        finally:
            loop.close()

        # Verify
        self.assertIn("qa_report", result)
        qa_report = result["qa_report"]
        self.assertEqual(qa_report["overall_score"], 8.5)
        self.assertTrue(qa_report["is_approved"])
        self.assertEqual(len(qa_report["improvement_suggestions"]), 2)
        print("Audit Execution Success Passed.")

    @patch("agents.quality_assurance_agent.Crew")
    @patch("agents.quality_assurance_agent.Task")
    def test_audit_execution_failure_parsing(self, MockTask, MockCrew):
        print("\nTesting Audit Execution Parsing Failure...")
        # Setup Mock Crew output with invalid JSON
        mock_crew_instance = MagicMock()
        MockCrew.return_value = mock_crew_instance
        
        mock_response = "This is not JSON."
        mock_crew_instance.kickoff.return_value = mock_response

        # Execute
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.agent._execute_agent_logic(self.task_request))
        finally:
            loop.close()

        # Verify fallback behavior
        self.assertIn("qa_report", result)
        qa_report = result["qa_report"]
        self.assertEqual(qa_report["overall_score"], 0)
        self.assertFalse(qa_report["is_approved"])
        print("Audit Execution Parsing Failure Passed.")

if __name__ == "__main__":
    unittest.main()

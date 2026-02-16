import asyncio
import unittest
import sys
from unittest.mock import MagicMock, patch

# Mock dependencies before importing agents
sys.modules['crewai'] = MagicMock()
sys.modules['crewai.tools'] = MagicMock()
sys.modules['crewai_tools'] = MagicMock()
sys.modules['tools.connector_tools'] = MagicMock()
sys.modules['langgraph'] = MagicMock()
sys.modules['langgraph.checkpoint.memory'] = MagicMock()

from agents.prompt_registry import PromptRegistry

class TestPromptRegistry(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.registry = PromptRegistry()

    @patch("langchainhub.Client.pull")
    @patch.dict("os.environ", {"LANGCHAIN_API_KEY": "test-key"})
    async def test_get_prompt_hub_success(self, mock_pull):
        # Mock hub.pull return
        mock_prompt = MagicMock()
        mock_prompt.template = "Hub template for {name}"
        mock_pull.return_value = mock_prompt
        
        result = await self.registry.get_prompt("test_prompt", {"name": "BizOSaas"})
        self.assertEqual(result, "Hub template for BizOSaas")
        mock_pull.assert_called_once_with("bizosaas/test-prompt")

    @patch("langchainhub.Client.pull")
    async def test_get_prompt_fallback(self, mock_pull):
        # Ensure no API key for fallback
        with patch.dict("os.environ", {}, clear=True):
            result = await self.registry.get_prompt("marketing_strategist_backstory")
            self.assertIn("expert marketing strategist", result)
            mock_pull.assert_not_called()

    async def test_get_prompt_with_variables(self):
        result = await self.registry.get_prompt("marketing_strategist_goal", {"tenant_id": "T123"})
        self.assertIn("T123", result)

    async def test_get_prompt_missing_variables(self):
        # Should return unformatted template or handle gracefully
        result = await self.registry.get_prompt("marketing_strategist_goal")
        self.assertIn("{tenant_id}", result)

if __name__ == "__main__":
    unittest.main()

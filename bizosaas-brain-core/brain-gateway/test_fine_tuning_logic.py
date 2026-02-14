import asyncio
import json
import os
import unittest
from unittest.mock import MagicMock, patch
from dataclasses import dataclass

# Mock the imports before importing the pipeline
import sys
sys.modules['app.core.vault'] = MagicMock()
sys.modules['app.core.rag'] = MagicMock()
sys.modules['app.connectors.registry'] = MagicMock()

from app.core.fine_tuning_pipeline import FineTuningPipeline

@dataclass
class MockRow:
    content: str
    metadata: dict
    agent_id: str
    tenant_id: str

class TestFineTuningPipeline(unittest.TestCase):
    def setUp(self):
        # Patch get_config_val to return a valid dummy DB URL
        with patch('app.core.fine_tuning_pipeline.get_config_val') as mock_get:
            mock_get.return_value = "postgresql://user:pass@localhost/db"
            with patch('sqlalchemy.create_engine'):
                with patch('sqlalchemy.orm.sessionmaker'):
                    self.pipeline = FineTuningPipeline()
                    # Mock the Session
                    self.pipeline.Session = MagicMock()


    def test_export_logic(self):
        # Mocking the query results
        mock_results = [
            MockRow(
                content="High quality result",
                metadata={"source": "agent_result", "task": "Task 1", "effectiveness_score": 0.9},
                agent_id="strategist",
                tenant_id="tenant1"
            ),
            MockRow(
                content="Another good one",
                metadata={"source": "agent_result", "task": "Task 2", "effectiveness_score": 0.85},
                agent_id="writer",
                tenant_id="tenant2"
            )
        ]
        
        mock_session = self.pipeline.Session.return_value.__enter__.return_value
        mock_session.execute.return_value = mock_results
        
        output_file = "test_training.jsonl"
        if os.path.exists(output_file):
            os.remove(output_file)
            
        loop = asyncio.get_event_loop()
        path = loop.run_until_complete(self.pipeline.export_training_corpus(output_file=output_file))
        
        self.assertTrue(os.path.exists(output_file))
        
        with open(output_file, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)
            
            first_entry = json.loads(lines[0])
            self.assertEqual(first_entry['messages'][0]['content'], "You are a helpful AI assistant specialized as a strategist.")
            self.assertEqual(first_entry['messages'][1]['content'], "Task 1")
            self.assertEqual(first_entry['messages'][2]['content'], "High quality result")

        os.remove(output_file)

if __name__ == "__main__":
    unittest.main()

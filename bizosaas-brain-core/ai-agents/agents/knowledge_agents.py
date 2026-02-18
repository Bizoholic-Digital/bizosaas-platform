from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentRole, AgentTaskRequest
import json
import logging

logger = logging.getLogger(__name__)

class RelationExtractionAgent(BaseAgent):
    """
    Agent specialized in extracting entities and their relationships from unstructured text.
    Used to populate the Knowledge Graph (KAG).
    """
    
    def __init__(self):
        super().__init__(
            agent_name="relation_extraction",
            agent_role=AgentRole.TECHNICAL,
            description="Extracts entities and relationships from text for Knowledge Graph population",
            version="1.0.0"
        )

    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """
        Extracts triples (subject, relation, object) from the provided text.
        """
        content = task_request.input_data.get("content", "")
        if not content:
            return {"entities": [], "relationships": []}

        # Select LLM
        llm = self._get_llm_for_task(task_request.config)
        
        prompt = f"""
        Extract entities and their relationships from the following text as a JSON object.
        Entities should have an 'id', 'label', and 'type'.
        Relationships should have a 'source_id', 'target_id', 'type', and 'weight'.
        
        Text: {content}
        
        Output format:
        {{
            "entities": [{{ "id": "1", "label": "Bizoholic", "type": "Company" }}],
            "relationships": [{{ "source_id": "1", "target_id": "2", "type": "PARTNER_OF", "weight": 0.9 }}]
        }}
        """
        
        try:
            response = await llm.ainvoke(prompt)
            # Basic parsing (improve with structured output if possible)
            result_text = response.content
            # Strip markdown if present
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            return json.loads(result_text)
        except Exception as e:
            self.logger.error(f"Relation extraction failed: {e}")
            return {"error": str(e), "entities": [], "relationships": []}

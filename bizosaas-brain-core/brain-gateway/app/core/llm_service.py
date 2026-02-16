"""
LLM Service for Brain Gateway
Provides a simplified interface for content generation, wrapping the robust intelligence module.
Used primarily by Temporal workflows.
"""

from typing import List, Optional, Dict, Any
import logging
from app.core import intelligence

logger = logging.getLogger(__name__)

async def generate_content(prompt: str, context: List[str] = [], agent_type: str = "content_creator") -> str:
    """
    Generates content using the intelligence service.
    
    Args:
        prompt: The main user prompt or instruction.
        context: Optional list of context strings to append.
        agent_type: The type of agent to use (default: content_creator).
        
    Returns:
        Generated text content.
    """
    try:
        # Construct a comprehensive task description
        task_description = prompt
        if context:
            task_description += "\n\nAdditional Context:\n" + "\n".join(context)

        logger.info(f"Generating content via LLM Service (Agent: {agent_type})")

        # Call the intelligence layer
        # payload is empty as we are passing everything in task_description for now
        result = await intelligence.call_ai_agent_with_rag(
            agent_type=agent_type,
            task_description=task_description,
            payload={},
            priority="normal",
            use_rag=True
        )
        
        # Extract content from various possible response formats
        content = ""
        if isinstance(result, dict):
            content = result.get("content") or \
                      result.get("generated_content") or \
                      result.get("response") or \
                      result.get("text") or \
                      str(result)
        else:
            content = str(result)
            
        return content

    except Exception as e:
        logger.error(f"LLM Service generation failed: {str(e)}")
        # Fallback or re-raise depending on requirements. 
        # For now, creating a safe error message to prevent workflow crash
        return f"Error generating content: {str(e)}"

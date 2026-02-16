"""
Prompt Registry for BizOSaas AI Agents
Manages dynamic prompt templates from LangChain Hub with local fallbacks.
"""

import os
import logging
import json
from typing import Dict, Any, Optional
import langchainhub as hub
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
import structlog

logger = structlog.get_logger(__name__)

class PromptRegistry:
    """
    Centralized registry for managing agent prompts.
    Provides local fallbacks when LangChain Hub is unavailable.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PromptRegistry, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
            
        self.prompts: Dict[str, Any] = {}
        self.fallbacks: Dict[str, str] = {
            "marketing_strategist_backstory": """You are an expert marketing strategist with 15+ years of experience 
            across digital marketing, brand strategy, and campaign optimization. You understand 
            market dynamics, consumer behavior, and emerging trends. Your strategic recommendations 
            are data-driven and focused on measurable outcomes.""",
            
            "marketing_strategist_goal": "Develop comprehensive marketing strategies that maximize ROI and brand impact for {tenant_id}",
            
            "personal_assistant_intent": "Classify the following user message into one of these intents: {intents}. Message: {message}",
            
            "general_assistant_prompt": "You are a helpful BizOSaas assistant. Help the user with their request: {input}",
            
            "documentation_agent_backstory": """You are a highly skilled Technical Documentation Specialist AI. 
            You excel at parsing complex codebases, understanding system architectures, and 
            translating technical details into clear, concise, and structured documentation 
            for both developers and end-users.""",
            
            "documentation_agent_goal": "Generate and maintain high-quality technical documentation for the BizOSaas platform.",
            
            "api_doc_generator_prompt": """Analyze the following Python code and generate a technical markdown documentation for its API routes. 
            Include route paths, methods, request parameters, response models, and a brief description of each endpoint.
            Code: {code}""",
            
            "user_guide_generator_prompt": """Generate a user-friendly guide for the following feature based on the provided technical details. 
            Focus on clarity, step-by-step instructions, and use cases.
            Feature Details: {details}""",
            
            "changelog_generator_prompt": """Summarize the following git commit messages into a user-friendly changelog. 
            Group changes by 'Added', 'Changed', 'Fixed', and 'Deprecated'.
            Commits: {commits}"""
        }
        self.initialized = True
        logger.info("PromptRegistry initialized")

    async def get_prompt(self, name: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """
        Get a prompt by name, pulling from Hub if possible, else using fallback.
        """
        template = await self._pull_from_hub(name)
        if not template:
            template = self.fallbacks.get(name, "Default prompt template")
            logger.debug("Using fallback for prompt", name=name)
        
        if variables:
            try:
                return template.format(**variables)
            except KeyError as e:
                logger.warning("Missing variables for prompt formatting", name=name, error=str(e))
                return template
        return template

    async def _pull_from_hub(self, name: str) -> Optional[str]:
        """
        Pull a prompt template from LangChain Hub.
        """
        api_key = os.getenv("LANGCHAIN_API_KEY")
        if not api_key:
            return None
            
        try:
            # Mapping internal names to hub handles (e.g., 'marketing_strategist' -> 'bizosaas/marketing-strategist')
            hub_handle = f"bizosaas/{name.replace('_', '-')}"
            client = hub.Client()
            prompt = client.pull(hub_handle)
            
            if hasattr(prompt, "template"):
                return prompt.template
            elif hasattr(prompt, "messages"):
                # Handle ChatPromptTemplates
                return json.dumps([m.content for m in prompt.messages])
            return str(prompt)
        except Exception as e:
            logger.debug("Failed to pull prompt from hub", name=name, error=str(e))
            return None

# Global instance
prompt_registry = PromptRegistry()

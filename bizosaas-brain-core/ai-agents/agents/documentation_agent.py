"""
Documentation Agent for BizOSaas Core
Automates technical documentation generation, API summaries, and user guides.
"""

import asyncio
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum

from crewai import Agent, Task, Crew, Process
from .base_agent import BaseAgent, AgentRole, AgentTaskRequest
import structlog

logger = structlog.get_logger(__name__)

class DocumentationTaskType(str, Enum):
    API_DOC_GENERATION = "api_doc_generation"
    USER_GUIDE_GENERATION = "user_guide_generation"
    CHANGELOG_GENERATION = "changelog_generation"
    SYSTEM_OVERVIEW = "system_overview"

class DocumentationAgent(BaseAgent):
    """AI agent specialized in generating and maintaining technical documentation"""
    
    def __init__(self):
        super().__init__(
            agent_name="documentation_agent",
            agent_role=AgentRole.TECHNICAL,
            description="AI Technical Documentation Specialist specialized in parsing codebases and generating structured documentation",
            version="1.0.0"
        )
        
        self.crewai_agent = Agent(
            role='Technical Documentation Specialist',
            goal='Generate and maintain high-quality technical documentation for the BizOSaas platform',
            backstory="""You are an expert technical writer and software architect. You excel at 
            analyzing complex systems, parsing source code, and creating clear, accessible 
            documentation for developers and users. You translate technical logic into 
            user-friendly value propositions while maintaining technical accuracy.""",
            verbose=True,
            allow_delegation=False
        )
    
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute documentation tasks based on request type"""
        task_type = task_request.task_type
        input_data = task_request.input_data
        
        # Apply LLM override if provided in config
        llm = self._get_llm_for_task(task_request.config)
        if llm:
            self.crewai_agent.llm = llm
            self.logger.info("Applied LLM override to DocumentationAgent", 
                             provider=task_request.config.get("model_provider"))

        # Pull managed prompts
        self.crewai_agent.backstory = await self._get_prompt("documentation_agent_backstory")
        self.crewai_agent.goal = await self._get_prompt("documentation_agent_goal")
        
        if task_type == DocumentationTaskType.API_DOC_GENERATION:
            return await self._generate_api_docs(input_data)
        elif task_type == DocumentationTaskType.USER_GUIDE_GENERATION:
            return await self._generate_user_guide(input_data)
        elif task_type == DocumentationTaskType.CHANGELOG_GENERATION:
            return await self._generate_changelog(input_data)
        else:
            raise ValueError(f"Unsupported task type: {task_type}")

    async def _generate_api_docs(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Scan code and generate API documentation"""
        target_path = input_data.get("target_path")
        if not target_path:
            return {"status": "error", "message": "No target_path provided"}
            
        # Ensure path is absolute if it doesn't exist relative to CWD
        if not os.path.isabs(target_path):
            target_path = os.path.join(os.getcwd(), target_path)

        if not os.path.exists(target_path):
            return {"status": "error", "message": f"Target path {target_path} not found"}
        
        # Read the file content
        try:
            with open(target_path, 'r') as f:
                content = f.read()
            self.logger.info(f"Read {len(content)} bytes from {target_path}")
        except Exception as e:
            return {"status": "error", "message": f"Error reading file: {str(e)}"}
            
        # Get the prompt for API doc generation
        prompt_vars = {"code": content[:8000]} # Limit content size for LLM to avoid token overflow
        prompt = await self._get_prompt("api_doc_generator_prompt", prompt_vars)
        
        # Define the task
        task = Task(
            description=f"Generate technical markdown documentation for the API routes in {os.path.basename(target_path)}. Input: {prompt}",
            expected_output="A structured markdown document detailing the API endpoints, methods, parameters, and response models.",
            agent=self.crewai_agent
        )
        
        # Execute via Crew
        crew = Crew(agents=[self.crewai_agent], tasks=[task], process=Process.sequential)
        result = await asyncio.to_thread(crew.kickoff)
        
        # Save to docs if requested
        output_file = input_data.get("output_file")
        if output_file:
            if not os.path.isabs(output_file):
                output_file = os.path.join(os.getcwd(), output_file)
            
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(str(result))
            self.logger.info(f"Saved documentation to {output_file}")
                
        return {
            "status": "success",
            "documentation": str(result),
            "file_saved": output_file if output_file else None
        }

    async def _generate_user_guide(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate user-friendly feature guide"""
        feature_details = input_data.get("feature_details", "No details provided")
        prompt = await self._get_prompt("user_guide_generator_prompt", {"details": feature_details})
        
        task = Task(
            description=f"Generate a user-friendly guide for a platform feature. Prompt: {prompt}",
            expected_output="A clear, step-by-step markdown user guide with use cases.",
            agent=self.crewai_agent
        )
        
        crew = Crew(agents=[self.crewai_agent], tasks=[task])
        result = await asyncio.to_thread(crew.kickoff)
        
        return {"status": "success", "guide": str(result)}

    async def _generate_changelog(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate changelog from commit messages"""
        commits = input_data.get("commits", "No commits provided")
        prompt = await self._get_prompt("changelog_generator_prompt", {"commits": commits})
        
        task = Task(
            description=f"Generate a markdown changelog from the provided commit history. Prompt: {prompt}",
            expected_output="A formatted markdown changelog grouped by standard categories (Added, Fixed, etc.).",
            agent=self.crewai_agent
        )
        
        crew = Crew(agents=[self.crewai_agent], tasks=[task])
        result = await asyncio.to_thread(crew.kickoff)
        
        return {"status": "success", "changelog": str(result)}

"""
Refined Development & Technical Agents
Category 4 of the 20 Core Agent Architecture
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum

from crewai import Agent, Task, Crew, Process
from .base_agent import BaseAgent, AgentRole, AgentTaskRequest

class CodeGenerationAgent(BaseAgent):
    """
    4.1 Code Generation Agent
    Purpose: Feature development, bug fixing, code review
    """
    
    def __init__(self):
        super().__init__(
            agent_name="code_generation_agent",
            agent_role=AgentRole.OPERATIONS,
            description="Agent for automated code generation, refactoring, and review",
            version="2.0.0"
        )
        
        self.crew_agent = Agent(
            role='Senior Full-Stack Engineer',
            goal='Generate clean, efficient, and well-tested code following best practices',
            backstory="""You are an elite software engineer with mastery over multiple programming 
            languages and frameworks. You follow SOLID principles, write comprehensive tests, 
            and excel at architectural design. You prioritize maintainability and performance.""",
            verbose=True,
            allow_delegation=False
        )

    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute code generation"""
        input_data = task_request.input_data
        mode = input_data.get('mode', 'feature_dev')
        
        mode_tasks = {
            'feature_dev': "implementing new features based on technical specifications",
            'bug_fixing': "diagnosing and resolving reported bugs or logic errors",
            'code_review': "performing a critical review of existing code for quality and security",
            'refactoring': "improving code structure and quality without changing external behavior"
        }
        
        code_task = Task(
            description=f"""
            Perform {mode_tasks.get(mode, mode)} for:
            {json.dumps(input_data.get('requirements', {}))}
            
            Tech Stack: {json.dumps(input_data.get('tech_stack', ['Python', 'React', 'Node.js']))}
            Existing Context: {input_data.get('code_context', 'New module')}
            Testing Requirement: {input_data.get('testing_level', 'Unit tests required')}
            
            Deliverables:
            1. Implementation Code (ready for PR)
            2. Test Suite (Unit/Integration)
            3. Detailed Documentation of changes
            4. Performance Analysis
            5. Security Considerations
            """,
            agent=self.crew_agent,
            expected_output=f"A high-quality code implementation for {mode}."
        )
        
        crew = Crew(
            agents=[self.crew_agent],
            tasks=[code_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent": self.agent_name,
            "code_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": str(result)
        }

class DevOpsAutomationAgent(BaseAgent):
    """
    4.2 DevOps Automation Agent
    Purpose: CI/CD, Infrastructure as Code, Monitoring setup
    """
    
    def __init__(self):
        super().__init__(
            agent_name="devops_automation_agent",
            agent_role=AgentRole.OPERATIONS,
            description="Agent for infrastructure automation and CI/CD orchestration",
            version="2.0.0"
        )
        
        self.crew_agent = Agent(
            role='Cloud Solutions Architect',
            goal='Automate infrastructure and deployment pipelines for maximum availability and security',
            backstory="""You are a DevOps expert specializing in cloud-native architectures. 
            You excel at Infrastructure as Code, automated CI/CD, and site reliability engineering. 
            You understand Docker, Kubernetes, Terraform, and advanced monitoring stacks.""",
            verbose=True,
            allow_delegation=True
        )

    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute DevOps automation tasks"""
        input_data = task_request.input_data
        mode = input_data.get('mode', 'deployment_pipeline')
        
        mode_focus = {
            'deployment_pipeline': "creating and optimizing CI/CD workflows",
            'infrastructure_setup': "generating IaC templates (Terraform/CloudFormation)",
            'monitoring_config': "setting up observability (Grafana/Loki/Prometheus)",
            'security_hardening': "implementing security scans and hardening scripts"
        }
        
        devops_task = Task(
            description=f"""
            Execute {mode_focus.get(mode, mode)} for:
            {json.dumps(input_data.get('infra_requirements', {}))}
            
            Environment: {input_data.get('environment', 'staging')}
            Cloud Provider: {input_data.get('provider', 'Hostinger KVM2/Docker')}
            
            Deliverables:
            1. Automation Scripts/Templates
            2. Configuration Files
            3. Deployment Steps
            4. Security Audit of the configuration
            5. Failure Recovery Plan
            """,
            agent=self.crew_agent,
            expected_output=f"A complete DevOps automation package for {mode}."
        )
        
        crew = Crew(
            agents=[self.crew_agent],
            tasks=[devops_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent": self.agent_name,
            "devops_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": str(result)
        }

class TechnicalDocumentationAgent(BaseAgent):
    """
    4.3 Technical Documentation Agent
    Purpose: API docs, System architecture docs, User manuals
    """
    
    def __init__(self):
        super().__init__(
            agent_name="tech_documentation_agent",
            agent_role=AgentRole.OPERATIONS,
            description="Agent for comprehensive technical and system documentation",
            version="2.0.0"
        )
        
        self.crew_agent = Agent(
            role='Lead Technical Writer',
            goal='Create clear, comprehensive, and accurate documentation for developers and users',
            backstory="""You are an expert technical documentarian who can bridge the gap 
            between complex code and human understanding. You excel at creating API references, 
            architecture diagrams, and step-by-step guides.""",
            verbose=True,
            allow_delegation=False
        )

    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute technical documentation tasks"""
        input_data = task_request.input_data
        mode = input_data.get('mode', 'api_documentation')
        
        mode_tasks = {
            'api_documentation': "generating Swagger/OpenAPI style documentation for endpoints",
            'system_architecture': "documenting system components, data flow, and infrastructure",
            'user_guides': "creating step-by-step instructions for end-users",
            'codebus_documentation': "documenting internal modules and logic"
        }
        
        doc_task = Task(
            description=f"""
            Perform {mode_tasks.get(mode, mode)} for:
            {json.dumps(input_data.get('context', {}))}
            
            Source Material: {input_data.get('source_type', 'codebase/PRD')}
            Target Audience: {input_data.get('audience', 'developers')}
            Format: {input_data.get('format', 'Markdown')}
            
            Deliverables:
            1. Comprehensive Documentation File
            2. Diagrams (Mermaid.js format where applicable)
            3. Code Examples/Snippets
            4. Change Log / Versioning notes
            """,
            agent=self.crew_agent,
            expected_output=f"High-quality technical documentation for {mode}."
        )
        
        crew = Crew(
            agents=[self.crew_agent],
            tasks=[doc_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent": self.agent_name,
            "doc_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": str(result)
        }

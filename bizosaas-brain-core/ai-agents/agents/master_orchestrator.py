"""
Refined Master Orchestrator Agent
Category 8 of the 20 Core Agent Architecture - Final Piece
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum

from crewai import Agent, Task, Crew, Process
from .base_agent import BaseAgent, AgentRole, AgentTaskRequest

class MasterOrchestratorAgent(BaseAgent):
    """
    8.1 Master Orchestrator Agent
    Purpose: Cross-agent coordination, Workflow selection, Global state management
    """
    
    def __init__(self):
        super().__init__(
            agent_name="master_orchestrator_agent",
            agent_role=AgentRole.OPERATIONS,
            description="The central intelligence for orchestrating all BizOSaas AI agents and workflows",
            version="2.0.0"
        )
        
        self.crew_agent = Agent(
            role='Principal AI Orchestrator',
            goal='Ensure optimal execution of complex business objectives by coordinating specialized AI agents',
            backstory="""You are the ultimate coordinator. You understand the capabilities 
            of every agent in the BizOSaas ecosystem. You can translate high-level business 
            goals into sequenced agent tasks and workflows. You manage dependencies, 
            resolve conflicts between agents, and ensure coherent global outputs.""",
            verbose=True,
            allow_delegation=True
        )

    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute master orchestration"""
        input_data = task_request.input_data
        global_objective = input_data.get('objective', 'Automate business growth')
        
        orchestration_task = Task(
            description=f"""
            Orchestrate the following global objective:
            {global_objective}
            
            Available Agent Categories:
            1. Business Intelligence
            2. Content & Creative
            3. Marketing & Growth
            4. Development & Technical
            5. Customer & CRM
            6. Finance & Trading
            7. Gaming & Community
            
            Context: {json.dumps(input_data.get('global_context', {}))}
            
            Deliverables:
            1. Master Execution Plan (Sequenced steps)
            2. Selected Agents & Modules for each step
            3. Data Handoff Definitions (Inputs/Outputs between agents)
            4. Success Verification Protocol
            5. Resource/API Optimization Strategy
            """,
            agent=self.crew_agent,
            expected_output="A master strategic execution plan involving multiple specialized agents."
        )
        
        crew = Crew(
            agents=[self.crew_agent],
            tasks=[orchestration_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent": self.agent_name,
            "orchestration_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": str(result),
            "execution_meta": {
                "objective_depth": input_data.get('depth', 'strategic'),
                "priority": input_data.get('priority', 'high')
            }
        }

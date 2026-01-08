"""
Refined Customer & CRM Agents
Category 5 of the 20 Core Agent Architecture
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum

from crewai import Agent, Task, Crew, Process
from .base_agent import BaseAgent, AgentRole, AgentTaskRequest

class CustomerEngagementAgent(BaseAgent):
    """
    5.1 Customer Engagement Agent
    Purpose: Lead nurturing, support automation, customer onboarding
    """
    
    def __init__(self):
        super().__init__(
            agent_name="customer_engagement_agent",
            agent_role=AgentRole.OPERATIONS,
            description="Agent for personalized customer engagement and success",
            version="2.0.0"
        )
        
        self.crew_agent = Agent(
            role='Customer Success Director',
            goal='Ensure every customer and lead receives personalized, high-value interaction',
            backstory="""You are an expert in customer relationships and behavioral psychology. 
            You excel at nurturing leads through the funnel, managing complex onboardings, 
            and ensuring long-term customer satisfaction. You are empathetic yet data-driven.""",
            verbose=True,
            allow_delegation=True
        )

    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute customer engagement tasks"""
        input_data = task_request.input_data
        mode = input_data.get('mode', 'lead_nurturing')
        
        engagement_task = Task(
            description=f"""
            Develop an engagement strategy for {mode.replace('_', ' ')}:
            {json.dumps(input_data.get('customer_context', {}))}
            
            Customer Segment: {input_data.get('segment', 'General')}
            Current Lifetime Value: {input_data.get('ltv', 'Unknown')}
            
            Requirements:
            1. Personalized Communication Plan (Email/DM/In-app)
            2. Onboarding Workflow (Step-by-step)
            3. Friction Point Identification & Resolution
            4. Retention Strategy
            5. Suggested Loyalty/Engagement Rewards
            """,
            agent=self.crew_agent,
            expected_output=f"A personalized engagement strategy for {mode}."
        )
        
        crew = Crew(
            agents=[self.crew_agent],
            tasks=[engagement_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent": self.agent_name,
            "engagement_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": str(result)
        }

class SalesIntelligenceAgent(BaseAgent):
    """
    5.2 Sales Intelligence Agent
    Purpose: Lead qualification, Opportunity scoring, Sales forecasting
    """
    
    def __init__(self):
        super().__init__(
            agent_name="sales_intelligence_agent",
            agent_role=AgentRole.OPERATIONS,
            description="Agent for advanced sales intelligence and lead qualification",
            version="2.0.0"
        )
        
        self.crew_agent = Agent(
            role='Senior Sales Operations Analyst',
            goal='Identify high-propensity opportunities and optimize sales performance',
            backstory="""You are a sales strategy expert. You use data to identify which leads 
            are most likely to close, when to reach out, and what the optimal deal size should be. 
            You excel at clean pipeline management and accurate revenue forecasting.""",
            verbose=True,
            allow_delegation=False
        )

    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute sales intelligence tasks"""
        input_data = task_request.input_data
        mode = input_data.get('mode', 'lead_qualification')
        
        sales_task = Task(
            description=f"""
            Perform {mode.replace('_', ' ')} analysis for:
            {json.dumps(input_data.get('sales_context', {}))}
            
            Current Pipeline Value: {input_data.get('pipeline_value', 'Unknown')}
            Growth Targets: {input_data.get('growth_target', 'Not specified')}
            
            Deliverables:
            1. Lead/Opportunity Scoring Matrix
            2. High-Value Prospect Identification
            3. Sales Pipeline Health Report
            4. Revenue Forecast (Quarterly/Yearly)
            5. Deal Velocity Optimization Recommendations
            """,
            agent=self.crew_agent,
            expected_output=f"A detailed sales intelligence report for {mode}."
        )
        
        crew = Crew(
            agents=[self.crew_agent],
            tasks=[sales_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent": self.agent_name,
            "sales_intel_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": str(result)
        }

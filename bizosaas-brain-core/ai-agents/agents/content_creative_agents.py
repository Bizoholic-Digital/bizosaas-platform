"""
Refined Content & Creative Agents
Category 2 of the 20 Core Agent Architecture
"""

import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from enum import Enum

from crewai import Agent, Task, Crew, Process
from .base_agent import BaseAgent, AgentRole, AgentTaskRequest

class ContentGenerationAgent(BaseAgent):
    """
    2.1 Content Generation Agent
    Purpose: Multi-format content creation (Blogs, Social, Ads, Email)
    """
    
    def __init__(self):
        super().__init__(
            agent_name="content_generation_agent",
            agent_role=AgentRole.MARKETING,
            description="Agent for high-quality multi-format content creation",
            version="2.0.0"
        )
        
        self.crew_agent = Agent(
            role='Creative Content Strategist',
            goal='Generate engaging, high-converting content tailored to specific channels',
            backstory="""You are a world-class copywriter and content strategist. You excel at 
            understanding brand voice, audience psychology, and channel-specific best practices. 
            You can write everything from long-form thought leadership to punchy social copy.""",
            verbose=True,
            allow_delegation=False
        )

    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute content generation based on format and tone"""
        input_data = task_request.input_data
        format_type = input_data.get('format', 'blog_post')
        tone = input_data.get('tone', 'professional')
        params = input_data.get('params', {})
        
        format_prompts = {
            'blog_post': "engaging long-form article with SEO headers",
            'social_media': "punchy, platform-specific posts with hashtags",
            'ad_copy': "high-converting headlines and descriptions with clear CTAs",
            'email_marketing': "personalized subject lines and persuasive body copy",
            'whitepaper': "authoritative, data-driven long-form technical content"
        }
        
        context = input_data.get('context', {})
        target_audience = context.get('target_audience', 'general')
        
        content_task = Task(
            description=f"""
            Generate {format_prompts.get(format_type, format_type)} based on this context:
            {json.dumps(context)}
            
            Tone: {tone}
            Target Audience: {target_audience}
            Language: {params.get('language', 'English')}
            Key Constraints: {params.get('constraints', 'No jargon, stay concise')}
            
            Deliverables:
            1. Title/Subject Line
            2. Main Content Body
            3. Meta Description (if applicable)
            4. Suggested Visual/Image Prompts
            """,
            agent=self.crew_agent,
            expected_output=f"A high-quality {format_type} in a {tone} tone."
        )
        
        crew = Crew(
            agents=[self.crew_agent],
            tasks=[content_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent": self.agent_name,
            "format": format_type,
            "content_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": str(result),
            "content_meta": {
                "tone": tone,
                "audience": target_audience,
                "word_count_est": params.get('target_length', 'variable')
            }
        }

class CreativeDesignAgent(BaseAgent):
    """
    2.2 Creative Design Agent
    Purpose: Visual concept generation, Ad creative ideation, UI/UX prompt engineering
    """
    
    def __init__(self):
        super().__init__(
            agent_name="creative_design_agent",
            agent_role=AgentRole.MARKETING,
            description="Agent for visual ideation and design prompt engineering",
            version="2.0.0"
        )
        
        self.crew_agent = Agent(
            role='Visual Brand Visionary',
            goal='Translate brand concepts into stunning visual directions and prompts',
            backstory="""You are an expert design director and prompt engineer for visual AI. 
            You understand color theory, composition, and visual storytelling. You excel at 
            creating detailed prompts for Midjourney, DALL-E, and Stable Diffusion.""",
            verbose=True,
            allow_delegation=True
        )

    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute creative design ideation"""
        input_data = task_request.input_data
        mode = input_data.get('mode', 'ad_creative')
        
        mode_configs = {
            'ad_creative': "visual concepts for digital advertising campaigns",
            'brand_identity': "logo concepts, color palettes, and typography directions",
            'ui_ux_concepts': "app/web interface layouts and user flow visualizations",
            'social_visuals': "Instagram/Pinterest style visual trends and templates"
        }
        
        design_task = Task(
            description=f"""
            Develop creative directions for {mode_configs.get(mode, mode)}:
            {json.dumps(input_data.get('context', {}))}
            
            Requirements:
            1. 3 Distinct Visual Concepts
            2. Detailed AI Image Generation Prompts (Midjourney/DALL-E style)
            3. Color Palette Recommendations (HEX codes)
            4. Typography selections
            5. Emotional design rationale
            """,
            agent=self.crew_agent,
            expected_output="A comprehensive visual design brief with specific prompts."
        )
        
        crew = Crew(
            agents=[self.crew_agent],
            tasks=[design_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent": self.agent_name,
            "mode": mode,
            "design_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": str(result)
        }

class SEOOptimizationAgent(BaseAgent):
    """
    2.3 SEO Optimization Agent
    Purpose: Keyword research, On-page optimization, Content SEO audit
    """
    
    def __init__(self):
        super().__init__(
            agent_name="seo_optimization_agent",
            agent_role=AgentRole.MARKETING,
            description="Agent for comprehensive SEO strategy and content optimization",
            version="2.0.0"
        )
        
        self.crew_agent = Agent(
            role='Senior SEO Strategist',
            goal='Maximize organic visibility through data-driven architectural and content SEO',
            backstory="""You are a veteran SEO specialist who understands search engine algorithms 
            inside out. You focus on semantic search, technical SEO, and high-value keyword 
            acquisition that drives real business results.""",
            verbose=True,
            allow_delegation=False
        )

    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute SEO tasks"""
        input_data = task_request.input_data
        mode = input_data.get('mode', 'keyword_research')
        
        mode_tasks = {
            'keyword_research': "identifying high-volume, low-competition semantic keywords",
            'on_page_optimization': "optimizing existing pages for specific target keywords",
            'seo_audit': "technical and content-based health check for a URL",
            'internal_linking': "developing a strategy to improve site authority distribution"
        }
        
        seo_task = Task(
            description=f"""
            Perform {mode_tasks.get(mode, mode)} for:
            {json.dumps(input_data.get('context', {}))}
            
            Focus on: {input_data.get('target_niche', 'general')}
            Competitors: {json.dumps(input_data.get('competitors', []))}
            
            Deliverables:
            1. Identified High-Potential Keywords (Volume vs Difficulty)
            2. Structural SEO Recommendations
            3. Content Gap Analysis
            4. 90-day SEO Growth Plan
            """,
            agent=self.crew_agent,
            expected_output=f"A targeted SEO {mode} report."
        )
        
        crew = Crew(
            agents=[self.crew_agent],
            tasks=[seo_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent": self.agent_name,
            "mode": mode,
            "seo_task_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": str(result)
        }

class VideoMarketingAgent(BaseAgent):
    """
    2.4 Video Marketing Agent
    Purpose: Video scriptwriting, storyboarding, production planning, and video SEO
    """
    
    def __init__(self):
        super().__init__(
            agent_name="video_marketing_agent",
            agent_role=AgentRole.MARKETING,
            description="Agent for video content strategy, scripting, and production planning",
            version="2.0.0"
        )
        
        self.crew_agent = Agent(
            role='Video Content Director',
            goal='Create compelling video scripts and production strategies that drive viewer retention',
            backstory="""You are a veteran of YouTube, TikTok, and TV commercial production. 
            You understand visual storytelling, pacing, and how to hook viewers in the first 3 seconds. 
            You excel at turning complex business ideas into viral video concepts.""",
            verbose=True,
            allow_delegation=True
        )

    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute video marketing tasks"""
        input_data = task_request.input_data
        mode = input_data.get('mode', 'video_script')
        
        mode_tasks = {
            'video_script': "writing a high-retention script for YouTube/Social",
            'storyboarding': "developing a visual storyboard and shot list",
            'video_seo': "optimizing video titles, tags, and AI-generated transcripts",
            'production_planning': "detailed production budget and equipment planning"
        }
        
        video_task = Task(
            description=f"""
            Perform {mode_tasks.get(mode, mode)} for:
            {json.dumps(input_data.get('context', {}))}
            
            Format: {input_data.get('platform', 'YouTube')}
            Tone: {input_data.get('tone', 'dynamic')}
            
            Deliverables:
            1. Master Video Concept
            2. Full Script/Storyboard (with timecodes)
            3. Hook & CTA Strategy
            4. AI Video Generation Prompts (Sora/Runway style)
            5. Thumbnail Ideation
            """,
            agent=self.crew_agent,
            expected_output=f"A professional video {mode} brief."
        )
        
        crew = Crew(
            agents=[self.crew_agent],
            tasks=[video_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent": self.agent_name,
            "mode": mode,
            "video_task_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "results": str(result)
        }

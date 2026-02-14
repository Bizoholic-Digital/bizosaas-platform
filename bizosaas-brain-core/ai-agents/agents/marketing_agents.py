"""
Centralized Marketing Agents for BizOSaas Core
Migrated from scattered CrewAI agents into unified business logic layer
"""

import asyncio
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from enum import Enum

import requests
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool

from .base_agent import BaseAgent, AgentRole, AgentTaskRequest
from tools.connector_tools import ConnectorTools

class MarketingTaskType(str, Enum):
    STRATEGY_DEVELOPMENT = "strategy_development"
    CONTENT_CREATION = "content_creation"
    SEO_OPTIMIZATION = "seo_optimization"
    SOCIAL_MEDIA_MANAGEMENT = "social_media_management"
    BRAND_POSITIONING = "brand_positioning"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    MARKET_RESEARCH = "market_research"
    GEO_OPTIMIZATION = "geo_optimization"
    INFLUENCER_MARKETING = "influencer_marketing"

class MarketingStrategistAgent(BaseAgent):
    """Central marketing strategy coordination agent"""
    
    def __init__(self):
        super().__init__(
            agent_name="marketing_strategist",
            agent_role=AgentRole.MARKETING,
            description="AI Marketing Strategist specializing in comprehensive campaign planning and strategy development",
            version="2.0.0"
        )
        
        # Initialize connector tools
        connector_tools = ConnectorTools()
        
        self.crewai_agent = Agent(
            role='Marketing Strategist',
            goal='Develop comprehensive marketing strategies that maximize ROI and brand impact',
            backstory="""You are an expert marketing strategist with 15+ years of experience 
            across digital marketing, brand strategy, and campaign optimization. You understand 
            market dynamics, consumer behavior, and emerging trends. Your strategic recommendations 
            are data-driven and focused on measurable outcomes.
            
            You have access to the client's connected platforms (WordPress, CRM, etc.) via the 
            Connector Tools. ALWAYS check for connected data before making assumptions.""",
            verbose=True,
            allow_delegation=True,
            # tools=[connector_tools.fetch_data, connector_tools.perform_action] # DISABLED_FOR_TEST
        )
    
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute marketing strategy development with cross-client learning insights"""
        input_data = task_request.input_data
        task_type = task_request.task_type
        
        # Apply LLM override if provided in config
        llm = self._get_llm_for_task(task_request.config)
        if llm:
            self.crewai_agent.llm = llm
            self.logger.info("Applied LLM override to MarketingStrategistAgent", 
                             provider=task_request.config.get("model_provider"))

        # Get cross-client insights before executing the task

        insights = await self.get_cross_client_insights(task_request)
        
        # Enrich input data with insights
        enriched_input = input_data.copy()
        if insights:
            enriched_input['cross_client_insights'] = insights
            self.logger.info(f"Applied {len(insights)} cross-client insights to task", 
                           task_id=task_request.task_id)
        
        if task_type == MarketingTaskType.STRATEGY_DEVELOPMENT:
            result = await self._develop_marketing_strategy(enriched_input)
        elif task_type == MarketingTaskType.COMPETITIVE_ANALYSIS:
            result = await self._perform_competitive_analysis(enriched_input)
        else:
            raise ValueError(f"Unsupported task type: {task_type}")
        
        # Add insights metadata to the result
        if insights:
            result['applied_insights'] = {
                'insight_count': len(insights),
                'insight_types': [insight['type'] for insight in insights],
                'average_effectiveness': sum(insight.get('effectiveness_score', 0) 
                                           for insight in insights) / len(insights) if insights else 0
            }
        
        # Add confidence score based on insights
        result['confidence_score'] = self._calculate_confidence_with_insights(result, insights)
        
        return result
    
    async def _develop_marketing_strategy(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive marketing strategy enhanced with cross-client insights"""
        company_info = input_data.get('company_info', {})
        goals = input_data.get('goals', {})
        budget = input_data.get('budget', 0)
        timeline = input_data.get('timeline', '3 months')
        insights = input_data.get('cross_client_insights', [])
        
        # Prepare insights context for the AI agent
        insights_context = ""
        if insights:
            insights_context = f"""
            
            CROSS-CLIENT INSIGHTS (Based on similar successful campaigns):
            {self._format_insights_for_strategy(insights)}
            
            Consider these proven patterns when developing the strategy.
            """
        
        # Create CrewAI task for strategy development with insights
        strategy_task = Task(
            description=f"""
            Develop a comprehensive marketing strategy for {company_info.get('name', 'the company')}.
            
            Company Information:
            - Industry: {company_info.get('industry', 'Not specified')}
            - Size: {company_info.get('size', 'Not specified')}
            - Target Market: {company_info.get('target_market', 'Not specified')}
            
            Goals: {goals}
            Budget: ${budget:,}
            Timeline: {timeline}
            {insights_context}
            
            Provide:
            1. Market Analysis (enhanced with cross-client trends)
            2. Target Audience Segmentation (informed by successful patterns)
            3. Recommended Channels and Tactics (prioritized by proven effectiveness)
            4. Budget Allocation (optimized using cross-client data)
            5. Timeline and Milestones (based on successful campaign patterns)
            6. Success Metrics and KPIs (benchmarked against similar campaigns)
            
            IMPORTANT: 
            1. Use the 'Fetch Data from Connector' tool to gather real data from connected platforms (e.g., WordPress content, CRM leads) if available.
            2. Incorporate the cross-client insights to improve strategy effectiveness while maintaining relevance to this specific company.
            """,
            agent=self.crewai_agent,
            expected_output="Comprehensive marketing strategy document with actionable recommendations enhanced by cross-client learning"
        )
        
        # Execute strategy development
        crew = Crew(
            agents=[self.crewai_agent],
            tasks=[strategy_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "strategy": str(result),
            "company_info": company_info,
            "budget_allocation": self._calculate_budget_allocation(budget),
            "timeline_milestones": self._generate_timeline_milestones(timeline),
            "success_metrics": self._define_success_metrics(goals),
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    
    async def _perform_competitive_analysis(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform competitive landscape analysis"""
        competitors = input_data.get('competitors', [])
        industry = input_data.get('industry', '')
        
        analysis_results = []
        
        for competitor in competitors:
            competitor_analysis = {
                "competitor": competitor,
                "strengths": [],
                "weaknesses": [],
                "opportunities": [],
                "marketing_channels": [],
                "estimated_budget": None,
                "key_messages": []
            }
            
            # Perform analysis (would integrate with external tools in production)
            # For now, return structured analysis framework
            analysis_results.append(competitor_analysis)
        
        return {
            "competitive_analysis": analysis_results,
            "market_gaps": [],
            "positioning_opportunities": [],
            "recommended_differentiation": {},
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    
    def _calculate_budget_allocation(self, total_budget: float) -> Dict[str, float]:
        """Calculate recommended budget allocation across channels"""
        return {
            "paid_advertising": total_budget * 0.35,
            "content_marketing": total_budget * 0.25,
            "seo_optimization": total_budget * 0.15,
            "social_media": total_budget * 0.15,
            "email_marketing": total_budget * 0.10
        }
    
    def _generate_timeline_milestones(self, timeline: str) -> List[Dict[str, Any]]:
        """Generate timeline milestones"""
        # Parse timeline and create milestones
        return [
            {"phase": "Strategy & Planning", "duration": "Week 1-2", "deliverables": ["Strategy Document", "Campaign Plans"]},
            {"phase": "Implementation", "duration": "Week 3-8", "deliverables": ["Campaign Launch", "Content Creation"]},
            {"phase": "Optimization", "duration": "Week 9-12", "deliverables": ["Performance Analysis", "Strategy Refinement"]}
        ]
    
    def _define_success_metrics(self, goals: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Define success metrics based on goals"""
        return [
            {"metric": "Lead Generation", "target": "25% increase", "timeframe": "3 months"},
            {"metric": "Brand Awareness", "target": "40% increase", "timeframe": "6 months"},
            {"metric": "ROI", "target": "300%+", "timeframe": "3 months"}
        ]
    
    def _calculate_confidence_with_insights(
        self, 
        result: Dict[str, Any], 
        insights: List[Dict[str, Any]]
    ) -> float:
        """Calculate confidence score based on cross-client insights"""
        base_confidence = 0.7  # Base confidence without insights
        
        if not insights:
            return base_confidence
        
        # Boost confidence based on insights quality and relevance
        insight_boost = 0.0
        for insight in insights:
            effectiveness = insight.get('effectiveness_score', 0.5)
            relevance = insight.get('relevance_score', 0.5)
            validation_count = insight.get('validation_count', 1)
            
            # More validated insights carry more weight
            validation_weight = min(validation_count / 10.0, 1.0)
            insight_contribution = (effectiveness * relevance * validation_weight) * 0.05
            insight_boost += insight_contribution
        
        # Cap the maximum confidence at 0.95
        return min(base_confidence + insight_boost, 0.95)
    
    def _format_insights_for_strategy(self, insights: List[Dict[str, Any]]) -> str:
        """Format cross-client insights for strategy development context"""
        if not insights:
            return "No relevant insights available."
        
        formatted_insights = []
        
        for idx, insight in enumerate(insights, 1):
            insight_type = insight.get('type', 'general')
            effectiveness = insight.get('effectiveness_score', 0)
            recommendations = insight.get('recommendations', [])
            industry = insight.get('industry_vertical', 'general')
            
            insight_text = f"""
            Insight #{idx} ({insight_type.replace('_', ' ').title()}):
            - Industry Context: {industry}
            - Effectiveness Score: {effectiveness:.2f}/1.0
            - Proven Strategies: {', '.join(recommendations[:3]) if recommendations else 'General best practices'}
            """
            
            formatted_insights.append(insight_text.strip())
        
        return '\n\n'.join(formatted_insights)

class ContentCreatorAgent(BaseAgent):
    """AI-powered content creation and strategy agent"""
    
    def __init__(self):
        super().__init__(
            agent_name="content_creator",
            agent_role=AgentRole.MARKETING,
            description="AI Content Creator specializing in multi-format content development and optimization",
            version="2.0.0"
        )
        
        self.crewai_agent = Agent(
            role='Content Creator',
            goal='Create compelling, engaging content that drives conversions and builds brand authority',
            backstory="""You are a creative content strategist and writer with expertise in 
            copywriting, storytelling, and content optimization across all digital platforms. 
            You understand audience psychology and create content that resonates and converts.""",
            verbose=True,
            allow_delegation=False
        )
    
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute content creation tasks"""
        input_data = task_request.input_data
        content_type = input_data.get('content_type', 'blog_post')
        
        if content_type == 'blog_post':
            return await self._create_blog_content(input_data)
        elif content_type == 'social_media':
            return await self._create_social_media_content(input_data)
        elif content_type == 'email':
            return await self._create_email_content(input_data)
        elif content_type == 'ad_copy':
            return await self._create_ad_copy(input_data)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
    
    async def _create_blog_content(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create blog post content"""
        topic = input_data.get('topic', '')
        target_audience = input_data.get('target_audience', '')
        keywords = input_data.get('keywords', [])
        word_count = input_data.get('word_count', 1000)
        
        content_task = Task(
            description=f"""
            Create a comprehensive blog post about: {topic}
            
            Requirements:
            - Target Audience: {target_audience}
            - Target Keywords: {', '.join(keywords)}
            - Word Count: {word_count} words
            - Include SEO optimization
            - Add compelling headlines and subheadings
            - Include call-to-action
            
            Structure:
            1. Engaging headline
            2. Introduction hook
            3. Main content with subheadings
            4. Actionable takeaways
            5. Compelling CTA
            """,
            agent=self.crewai_agent,
            expected_output="Complete blog post with SEO optimization and compelling copy"
        )
        
        crew = Crew(
            agents=[self.crewai_agent],
            tasks=[content_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "content": str(result),
            "content_type": "blog_post",
            "topic": topic,
            "seo_keywords": keywords,
            "word_count": len(str(result).split()),
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    
    async def _create_social_media_content(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create social media content"""
        platform = input_data.get('platform', 'linkedin')
        campaign_goal = input_data.get('campaign_goal', 'engagement')
        brand_voice = input_data.get('brand_voice', 'professional')
        
        return {
            "content": "Sample social media content",
            "platform": platform,
            "campaign_goal": campaign_goal,
            "hashtags": ["#marketing", "#business"],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    
    async def _create_email_content(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create email marketing content"""
        email_type = input_data.get('email_type', 'newsletter')
        subject_line = input_data.get('subject_line', '')
        
        return {
            "subject_line": subject_line,
            "email_content": "Sample email content",
            "email_type": email_type,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    
    async def _create_ad_copy(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create advertising copy"""
        ad_platform = input_data.get('ad_platform', 'google_ads')
        product_service = input_data.get('product_service', '')
        
        return {
            "headline": "Sample ad headline",
            "description": "Sample ad description",
            "ad_platform": ad_platform,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }

class SEOSpecialistAgent(BaseAgent):
    """SEO optimization and search strategy agent"""
    
    def __init__(self):
        super().__init__(
            agent_name="seo_specialist",
            agent_role=AgentRole.MARKETING,
            description="AI SEO Specialist for technical SEO, keyword research, and search optimization",
            version="2.0.0"
        )
        
        self.crewai_agent = Agent(
            role='SEO Specialist',
            goal='Optimize websites and content for maximum search engine visibility and organic traffic',
            backstory="""You are an expert SEO specialist with deep knowledge of search engine 
            algorithms, technical SEO, content optimization, and link building strategies. You stay 
            current with Google updates and best practices.""",
            verbose=True,
            allow_delegation=False
        )
    
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute SEO optimization tasks"""
        input_data = task_request.input_data
        seo_task_type = input_data.get('seo_task_type', 'keyword_research')
        
        if seo_task_type == 'keyword_research':
            return await self._perform_keyword_research(input_data)
        elif seo_task_type == 'content_optimization':
            return await self._optimize_content_for_seo(input_data)
        elif seo_task_type == 'technical_audit':
            return await self._perform_technical_seo_audit(input_data)
        else:
            raise ValueError(f"Unsupported SEO task type: {seo_task_type}")
    
    async def _perform_keyword_research(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive keyword research"""
        seed_keywords = input_data.get('seed_keywords', [])
        industry = input_data.get('industry', '')
        location = input_data.get('location', '')
        
        # Mock keyword research results (would integrate with actual tools)
        keyword_results = [
            {
                "keyword": keyword,
                "search_volume": 1000,
                "difficulty": "medium",
                "cpc": 2.50,
                "intent": "commercial"
            }
            for keyword in seed_keywords
        ]
        
        return {
            "primary_keywords": keyword_results,
            "long_tail_keywords": [],
            "competitor_keywords": [],
            "content_opportunities": [],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    
    async def _optimize_content_for_seo(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize content for SEO"""
        content = input_data.get('content', '')
        target_keywords = input_data.get('target_keywords', [])
        
        return {
            "optimized_content": content,
            "seo_score": 85,
            "recommendations": [
                "Add more keyword variations",
                "Improve internal linking",
                "Optimize meta descriptions"
            ],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    
    async def _perform_technical_seo_audit(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform technical SEO audit"""
        website_url = input_data.get('website_url', '')
        
        return {
            "audit_results": {
                "page_speed_score": 85,
                "mobile_friendly": True,
                "ssl_enabled": True,
                "meta_tags_present": True,
                "structured_data": False
            },
            "recommendations": [
                "Add structured data markup",
                "Optimize image sizes",
                "Improve Core Web Vitals"
            ],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }

class SocialMediaAgent(BaseAgent):
    """Social media management and optimization agent"""
    
    def __init__(self):
        super().__init__(
            agent_name="social_media_specialist",
            agent_role=AgentRole.MARKETING,
            description="AI Social Media Specialist for multi-platform social strategy and management",
            version="2.0.0"
        )
    
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute social media tasks"""
        return {
            "social_strategy": "Sample social media strategy",
            "content_calendar": [],
            "engagement_tactics": [],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }

class BrandPositioningAgent(BaseAgent):
    """Brand strategy and positioning specialist"""
    
    def __init__(self):
        super().__init__(
            agent_name="brand_positioning_specialist",
            agent_role=AgentRole.MARKETING,
            description="AI Brand Positioning Specialist for strategic brand development",
            version="2.0.0"
        )
    
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute brand positioning tasks"""
        return {
            "brand_strategy": "Sample brand positioning strategy",
            "value_proposition": "Sample value proposition",
            "brand_guidelines": {},
            "generated_at": datetime.now(timezone.utc).isoformat()
        }

class CompetitiveAnalysisAgent(BaseAgent):
    """Competitive intelligence and analysis specialist"""
    
    def __init__(self):
        super().__init__(
            agent_name="competitive_analysis_specialist",
            agent_role=AgentRole.MARKETING,
            description="AI Competitive Analysis Specialist for market intelligence",
            version="2.0.0"
        )
    
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute competitive analysis tasks"""
        return {
            "competitor_profiles": [],
            "market_gaps": [],
            "opportunities": [],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }

class LegacyMarketResearchAgent(BaseAgent):
    """Market research and analysis specialist"""
    
    def __init__(self):
        super().__init__(
            agent_name="market_research_specialist",
            agent_role=AgentRole.MARKETING,
            description="AI Market Research Specialist for comprehensive market analysis",
            version="2.0.0"
        )
    
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute market research tasks"""
        return {
            "market_analysis": {},
            "target_audience_insights": {},
            "trends": [],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }

class GEOAgent(BaseAgent):
    """Generative Engine Optimization specialist"""
    
    def __init__(self):
        super().__init__(
            agent_name="geo_specialist",
            agent_role=AgentRole.MARKETING,
            description="AI GEO Specialist for Generative Engine Optimization",
            version="2.0.0"
        )
    
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute GEO optimization tasks"""
        return {
            "geo_strategy": "Sample GEO optimization strategy",
            "content_recommendations": [],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }

class InfluencerMarketingAgent(BaseAgent):
    """Influencer marketing strategy and management specialist"""
    
    def __init__(self):
        super().__init__(
            agent_name="influencer_marketing_specialist",
            agent_role=AgentRole.MARKETING,
            description="AI Influencer Marketing Specialist for partnership strategy",
            version="2.0.0"
        )
    
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        """Execute influencer marketing tasks"""
        return {
            "influencer_strategy": "Sample influencer marketing strategy",
            "recommended_influencers": [],
            "campaign_ideas": [],
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
# Aliases and Dummies for backward compatibility or orchestration requirements
class SocialMediaSpecialistAgent(SocialMediaAgent):
    """Alias for SocialMediaAgent to satisfy legacy imports"""
    pass

class EmailMarketingAgent(BaseAgent):
    """Email marketing specialist"""
    def __init__(self):
        super().__init__(
            agent_name="email_marketing_specialist",
            agent_role=AgentRole.MARKETING,
            description="AI Email Marketing Specialist",
            version="2.0.0"
        )
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        return {"email_campaign": {}, "generated_at": datetime.now(timezone.utc).isoformat()}

class PaidAdvertisingAgent(BaseAgent):
    """Paid advertising specialist"""
    def __init__(self):
        super().__init__(
            agent_name="paid_advertising_specialist",
            agent_role=AgentRole.MARKETING,
            description="AI Paid Advertising Specialist",
            version="2.0.0"
        )
    async def _execute_agent_logic(self, task_request: AgentTaskRequest) -> Dict[str, Any]:
        return {"ad_campaign": {}, "generated_at": datetime.now(timezone.utc).isoformat()}

# Aliases and Dummies
class SocialMediaSpecialistAgent(SocialMediaAgent):
    """Alias for SocialMediaAgent"""
    pass

class EmailMarketingAgent(BaseAgent):
    """Email marketing specialist"""
    def __init__(self):
        super().__init__(
            agent_name="email_marketing_specialist",
            agent_role=AgentRole.MARKETING,
            description="AI Email Marketing Specialist",
            version="2.0.0"
        )

class PaidAdvertisingAgent(BaseAgent):
    """Paid advertising specialist"""
    def __init__(self):
        super().__init__(
            agent_name="paid_advertising_specialist",
            agent_role=AgentRole.MARKETING,
            description="AI Paid Advertising Specialist",
            version="2.0.0"
        )

class MarketingAutomationAgent(BaseAgent):
    """Marketing automation specialist"""
    def __init__(self):
        super().__init__(
            agent_name="marketing_automation_specialist", 
            agent_role=AgentRole.MARKETING,
            description="AI Marketing Automation Specialist",
            version="2.0.0"
        )

class BrandingSpecialistAgent(BrandPositioningAgent):
    """Alias for BrandPositioningAgent"""
    pass

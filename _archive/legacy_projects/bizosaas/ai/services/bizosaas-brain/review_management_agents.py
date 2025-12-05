"""
CrewAI Agents for Review Management & Response Automation

Provides specialized AI agents for comprehensive review management including:
- Review analysis and sentiment detection
- Intelligent response generation
- Reputation management strategy
- Competitor review benchmarking
- Review workflow optimization
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field
import structlog

# CrewAI imports
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool

# Import review workflow models
from review_management_workflows import (
    ReviewData, ReviewResponse, ReviewPlatform, ReviewSentiment,
    ResponseStatus, RepuationAlert
)

# Import unified tenant system
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from unified_tenant_middleware import UnifiedTenant

logger = structlog.get_logger(__name__)


class ReviewAnalysisTool(BaseTool):
    """Tool for comprehensive review analysis"""
    name = "review_analyzer"
    description = "Analyzes customer reviews for sentiment, themes, and actionable insights"
    
    def _run(self, review_content: str, rating: float, platform: str) -> str:
        """Analyze review content and extract insights"""
        try:
            # Comprehensive analysis logic
            analysis = {
                "sentiment_indicators": self._extract_sentiment_indicators(review_content),
                "key_themes": self._extract_themes(review_content),
                "emotion_indicators": self._extract_emotions(review_content),
                "service_aspects": self._analyze_service_aspects(review_content),
                "urgency_factors": self._assess_urgency(review_content, rating),
                "response_recommendations": self._generate_response_strategy(review_content, rating)
            }
            
            return json.dumps(analysis, indent=2)
            
        except Exception as e:
            logger.error(f"Review analysis failed: {e}")
            return json.dumps({"error": str(e)})
    
    def _extract_sentiment_indicators(self, content: str) -> Dict[str, Any]:
        """Extract sentiment indicators from review text"""
        positive_words = [
            "excellent", "amazing", "outstanding", "fantastic", "wonderful",
            "great", "good", "helpful", "friendly", "professional", "quick",
            "efficient", "clean", "fresh", "delicious", "recommend"
        ]
        
        negative_words = [
            "terrible", "awful", "horrible", "worst", "bad", "poor",
            "slow", "rude", "unprofessional", "dirty", "expired",
            "disappointed", "frustrated", "angry", "waste", "never"
        ]
        
        content_lower = content.lower()
        
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        return {
            "positive_indicators": positive_count,
            "negative_indicators": negative_count,
            "sentiment_balance": positive_count - negative_count,
            "detected_positive_words": [word for word in positive_words if word in content_lower],
            "detected_negative_words": [word for word in negative_words if word in content_lower]
        }
    
    def _extract_themes(self, content: str) -> List[str]:
        """Extract key themes from review content"""
        theme_keywords = {
            "service_quality": ["service", "staff", "employee", "help", "assistance"],
            "product_quality": ["product", "item", "goods", "quality", "fresh"],
            "pricing": ["price", "cost", "expensive", "cheap", "value", "money"],
            "cleanliness": ["clean", "dirty", "hygiene", "sanitary", "mess"],
            "speed": ["fast", "slow", "quick", "wait", "time", "delayed"],
            "location": ["location", "parking", "access", "convenient", "far"],
            "atmosphere": ["atmosphere", "ambiance", "environment", "comfortable"]
        }
        
        detected_themes = []
        content_lower = content.lower()
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                detected_themes.append(theme)
        
        return detected_themes
    
    def _extract_emotions(self, content: str) -> List[str]:
        """Extract emotional indicators from review"""
        emotion_keywords = {
            "joy": ["happy", "pleased", "satisfied", "delighted", "thrilled"],
            "anger": ["angry", "furious", "mad", "frustrated", "annoyed"],
            "disappointment": ["disappointed", "let down", "expected better"],
            "surprise": ["surprised", "unexpected", "wow", "amazing"],
            "trust": ["trust", "reliable", "dependable", "consistent"],
            "disgust": ["disgusting", "gross", "awful", "terrible"]
        }
        
        detected_emotions = []
        content_lower = content.lower()
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                detected_emotions.append(emotion)
        
        return detected_emotions
    
    def _analyze_service_aspects(self, content: str) -> Dict[str, str]:
        """Analyze specific service aspects mentioned"""
        aspects = {
            "staff_behavior": "",
            "product_quality": "",
            "facility_condition": "",
            "wait_time": "",
            "value_for_money": ""
        }
        
        content_lower = content.lower()
        
        # Staff behavior analysis
        if any(word in content_lower for word in ["staff", "employee", "worker", "cashier"]):
            if any(word in content_lower for word in ["rude", "unprofessional", "unhelpful"]):
                aspects["staff_behavior"] = "negative"
            elif any(word in content_lower for word in ["friendly", "helpful", "professional"]):
                aspects["staff_behavior"] = "positive"
            else:
                aspects["staff_behavior"] = "mentioned"
        
        # Similar analysis for other aspects...
        
        return aspects
    
    def _assess_urgency(self, content: str, rating: float) -> int:
        """Assess urgency level for response (1-5)"""
        urgency_factors = 0
        content_lower = content.lower()
        
        # Rating-based urgency
        if rating <= 2:
            urgency_factors += 3
        elif rating <= 3:
            urgency_factors += 1
        
        # Content-based urgency indicators
        high_urgency_phrases = [
            "never again", "worst experience", "health concern", "food poisoning",
            "discrimination", "harassment", "illegal", "lawsuit", "report",
            "health department", "better business bureau"
        ]
        
        if any(phrase in content_lower for phrase in high_urgency_phrases):
            urgency_factors += 2
        
        return min(5, max(1, urgency_factors))
    
    def _generate_response_strategy(self, content: str, rating: float) -> Dict[str, Any]:
        """Generate response strategy recommendations"""
        strategy = {
            "response_tone": "professional",
            "key_points_to_address": [],
            "response_length": "medium",
            "personalization_level": "standard",
            "follow_up_required": False
        }
        
        if rating <= 2:
            strategy["response_tone"] = "empathetic_apologetic"
            strategy["response_length"] = "detailed"
            strategy["follow_up_required"] = True
            strategy["key_points_to_address"].append("sincere_apology")
            strategy["key_points_to_address"].append("specific_resolution")
            strategy["key_points_to_address"].append("offline_conversation")
        elif rating >= 4:
            strategy["response_tone"] = "grateful_enthusiastic"
            strategy["key_points_to_address"].append("express_gratitude")
            strategy["key_points_to_address"].append("highlight_positives")
            strategy["key_points_to_address"].append("encourage_return")
        
        return strategy


class CompetitorReviewTool(BaseTool):
    """Tool for competitor review analysis and benchmarking"""
    name = "competitor_analyzer"
    description = "Analyzes competitor reviews for benchmarking and strategy insights"
    
    def _run(self, competitor_name: str, industry: str, location: str) -> str:
        """Analyze competitor reviews and provide insights"""
        try:
            analysis = {
                "competitor": competitor_name,
                "analysis_date": datetime.now().isoformat(),
                "review_summary": self._get_competitor_review_summary(competitor_name),
                "strength_analysis": self._analyze_competitor_strengths(competitor_name),
                "weakness_analysis": self._analyze_competitor_weaknesses(competitor_name),
                "opportunity_gaps": self._identify_opportunity_gaps(competitor_name),
                "response_strategy_analysis": self._analyze_response_strategies(competitor_name),
                "benchmarking_metrics": self._generate_benchmarking_metrics(competitor_name)
            }
            
            return json.dumps(analysis, indent=2)
            
        except Exception as e:
            logger.error(f"Competitor analysis failed: {e}")
            return json.dumps({"error": str(e)})
    
    def _get_competitor_review_summary(self, competitor: str) -> Dict[str, Any]:
        """Get summary of competitor's reviews"""
        # This would integrate with review platform APIs
        return {
            "total_reviews": 150,
            "average_rating": 4.2,
            "recent_review_count": 25,
            "response_rate": 0.65,
            "platform_breakdown": {
                "google": 80,
                "yelp": 45,
                "facebook": 25
            }
        }
    
    def _analyze_competitor_strengths(self, competitor: str) -> List[str]:
        """Analyze competitor's review-based strengths"""
        return [
            "Consistently praised for customer service",
            "High ratings for product quality",
            "Quick response times to reviews",
            "Professional tone in responses"
        ]
    
    def _analyze_competitor_weaknesses(self, competitor: str) -> List[str]:
        """Analyze competitor's review-based weaknesses"""
        return [
            "Slow to respond to negative reviews",
            "Generic response templates",
            "Pricing concerns mentioned frequently",
            "Limited presence on some platforms"
        ]
    
    def _identify_opportunity_gaps(self, competitor: str) -> List[str]:
        """Identify opportunities based on competitor weaknesses"""
        return [
            "Faster negative review response times",
            "More personalized review responses",
            "Better value proposition messaging",
            "Expanded platform presence"
        ]
    
    def _analyze_response_strategies(self, competitor: str) -> Dict[str, Any]:
        """Analyze competitor's response strategies"""
        return {
            "response_templates": "uses generic templates",
            "personalization_level": "low",
            "escalation_handling": "basic",
            "follow_up_strategy": "minimal"
        }
    
    def _generate_benchmarking_metrics(self, competitor: str) -> Dict[str, float]:
        """Generate benchmarking metrics"""
        return {
            "response_rate": 0.65,
            "average_response_time_hours": 48,
            "sentiment_score": 0.72,
            "engagement_rate": 0.23
        }


class ResponseOptimizationTool(BaseTool):
    """Tool for optimizing review responses"""
    name = "response_optimizer"
    description = "Optimizes review responses for better engagement and sentiment"
    
    def _run(self, response_draft: str, review_context: str, business_context: str) -> str:
        """Optimize a review response draft"""
        try:
            optimization = {
                "original_response": response_draft,
                "optimization_suggestions": self._generate_optimization_suggestions(response_draft),
                "tone_analysis": self._analyze_response_tone(response_draft),
                "length_analysis": self._analyze_response_length(response_draft),
                "personalization_score": self._score_personalization(response_draft, review_context),
                "improved_response": self._generate_improved_response(response_draft, review_context, business_context),
                "effectiveness_score": self._calculate_effectiveness_score(response_draft)
            }
            
            return json.dumps(optimization, indent=2)
            
        except Exception as e:
            logger.error(f"Response optimization failed: {e}")
            return json.dumps({"error": str(e)})
    
    def _generate_optimization_suggestions(self, response: str) -> List[str]:
        """Generate specific optimization suggestions"""
        suggestions = []
        
        if len(response) < 50:
            suggestions.append("Response is too brief - consider adding more detail")
        elif len(response) > 300:
            suggestions.append("Response is too long - consider being more concise")
        
        if not any(word in response.lower() for word in ["thank", "appreciate", "grateful"]):
            suggestions.append("Add gratitude expression")
        
        if "we" not in response.lower():
            suggestions.append("Consider using inclusive language ('we', 'our team')")
        
        return suggestions
    
    def _analyze_response_tone(self, response: str) -> Dict[str, Any]:
        """Analyze the tone of the response"""
        tone_indicators = {
            "professional": ["thank you", "appreciate", "team", "business"],
            "empathetic": ["understand", "sorry", "concern", "care"],
            "solution_oriented": ["improve", "address", "resolve", "fix"],
            "friendly": ["glad", "happy", "pleased", "welcome"]
        }
        
        detected_tones = []
        response_lower = response.lower()
        
        for tone, keywords in tone_indicators.items():
            if any(keyword in response_lower for keyword in keywords):
                detected_tones.append(tone)
        
        return {
            "detected_tones": detected_tones,
            "primary_tone": detected_tones[0] if detected_tones else "neutral",
            "tone_consistency": len(detected_tones) > 0
        }
    
    def _analyze_response_length(self, response: str) -> Dict[str, Any]:
        """Analyze response length appropriateness"""
        word_count = len(response.split())
        
        return {
            "word_count": word_count,
            "character_count": len(response),
            "optimal_range": word_count >= 20 and word_count <= 100,
            "recommendation": self._get_length_recommendation(word_count)
        }
    
    def _get_length_recommendation(self, word_count: int) -> str:
        """Get length recommendation based on word count"""
        if word_count < 20:
            return "Consider adding more detail and personalization"
        elif word_count > 100:
            return "Consider making response more concise"
        else:
            return "Length is appropriate"
    
    def _score_personalization(self, response: str, review_context: str) -> float:
        """Score the personalization level of the response"""
        score = 0.0
        
        # Check for specific mentions from the review
        if "your" in response.lower():
            score += 0.2
        
        # Check for specific issue addressing
        if any(word in response.lower() for word in ["specifically", "particular", "mentioned"]):
            score += 0.3
        
        # Check for business-specific details
        if any(word in response.lower() for word in ["location", "store", "restaurant", "service"]):
            score += 0.2
        
        # Check for follow-up invitation
        if any(phrase in response.lower() for phrase in ["contact us", "reach out", "discuss"]):
            score += 0.3
        
        return min(1.0, score)
    
    def _generate_improved_response(self, original: str, review_context: str, business_context: str) -> str:
        """Generate an improved version of the response"""
        # This would use advanced NLP and the business context to improve the response
        # For now, return a template improved response
        return f"""Thank you for taking the time to share your feedback. 
        We truly appreciate your business and the opportunity to serve you. 
        
        {original.strip()}
        
        We're committed to providing the best experience possible, and your 
        feedback helps us continue to improve. Please don't hesitate to reach 
        out to us directly if you have any additional concerns.
        
        Thank you again for choosing us!"""
    
    def _calculate_effectiveness_score(self, response: str) -> float:
        """Calculate overall effectiveness score for the response"""
        factors = {
            "has_gratitude": any(word in response.lower() for word in ["thank", "appreciate"]),
            "addresses_concern": "concern" in response.lower() or "issue" in response.lower(),
            "offers_solution": any(word in response.lower() for word in ["improve", "resolve", "address"]),
            "invites_contact": any(phrase in response.lower() for phrase in ["contact", "reach out", "call"]),
            "professional_tone": not any(word in response.lower() for word in ["whatever", "fine", "deal"])
        }
        
        score = sum(factors.values()) / len(factors)
        return round(score, 2)


class ReviewAnalystAgent:
    """Specialized agent for review sentiment analysis and categorization"""
    
    def __init__(self):
        self.agent = Agent(
            role='Senior Review Analyst',
            goal='Analyze customer reviews to extract sentiment, themes, and actionable insights for reputation management',
            backstory="""You are a senior customer experience analyst with 10+ years 
            of experience in analyzing customer feedback across multiple industries. 
            You excel at identifying sentiment patterns, extracting key themes, and 
            providing actionable insights for business improvement.""",
            verbose=True,
            allow_delegation=False,
            tools=[ReviewAnalysisTool()],
            memory=True
        )
    
    def create_analysis_task(self, reviews: List[ReviewData]) -> Task:
        """Create a comprehensive review analysis task"""
        reviews_data = []
        for review in reviews:
            reviews_data.append({
                "platform": review.platform.value,
                "rating": review.rating,
                "content": review.content,
                "reviewer": review.reviewer_name,
                "date": review.platform_created_at.isoformat()
            })
        
        return Task(
            description=f"""Analyze the following {len(reviews)} customer reviews:
            
            {json.dumps(reviews_data, indent=2)}
            
            Provide a comprehensive analysis including:
            1. Overall sentiment distribution and trends
            2. Key themes and categories mentioned
            3. Specific service aspects praised or criticized
            4. Emotional indicators and urgency levels
            5. Actionable insights for business improvement
            6. Response priority recommendations
            7. Competitive positioning opportunities
            
            Focus on extracting insights that can drive business decisions and 
            improve customer satisfaction.""",
            agent=self.agent,
            expected_output="Comprehensive JSON report with sentiment analysis and business insights"
        )


class ResponseWriterAgent:
    """Specialized agent for generating professional review responses"""
    
    def __init__(self):
        self.agent = Agent(
            role='Professional Response Writer',
            goal='Create empathetic, professional, and brand-appropriate responses to customer reviews',
            backstory="""You are a master of customer communication with extensive 
            experience in crafting responses that turn negative experiences into 
            positive outcomes and reinforce positive experiences. You understand 
            brand voice, crisis communication, and customer psychology.""",
            verbose=True,
            allow_delegation=False,
            tools=[ResponseOptimizationTool()],
            memory=True
        )
    
    def create_response_task(self, review: ReviewData, business_context: Dict[str, Any]) -> Task:
        """Create a review response generation task"""
        return Task(
            description=f"""Generate a professional response to this customer review:
            
            Platform: {review.platform.value}
            Rating: {review.rating}/5
            Reviewer: {review.reviewer_name}
            Review Title: {review.title or 'N/A'}
            Review Content: {review.content}
            Sentiment: {review.sentiment.value if review.sentiment else 'Unknown'}
            Date: {review.platform_created_at.isoformat()}
            
            Business Context:
            {json.dumps(business_context, indent=2)}
            
            Response Requirements:
            1. Professional and empathetic tone
            2. Address specific points mentioned in the review
            3. Thank the customer for their feedback
            4. Provide specific resolution or next steps if needed
            5. Maintain brand voice and values
            6. Keep response concise but comprehensive
            7. Personalize without being overly familiar
            
            For negative reviews (rating ≤ 3):
            - Acknowledge concerns genuinely and specifically
            - Apologize appropriately without admitting fault unnecessarily
            - Offer concrete resolution steps
            - Invite offline conversation for complex issues
            - Show commitment to improvement
            
            For positive reviews (rating ≥ 4):
            - Express genuine gratitude
            - Highlight specific positives mentioned
            - Reinforce brand values
            - Encourage future engagement
            - Build community feeling
            
            Ensure the response demonstrates active listening and genuine care 
            for the customer experience.""",
            agent=self.agent,
            expected_output="Professional, empathetic review response (100-200 words)"
        )


class ReputationManagerAgent:
    """Specialized agent for reputation management strategy and monitoring"""
    
    def __init__(self):
        self.agent = Agent(
            role='Reputation Management Strategist',
            goal='Develop comprehensive reputation management strategies and monitor online presence',
            backstory="""You are a digital reputation management expert with deep 
            understanding of online review ecosystems, crisis management, and 
            brand positioning. You excel at turning reputation challenges into 
            competitive advantages.""",
            verbose=True,
            allow_delegation=True,
            tools=[CompetitorReviewTool()],
            memory=True
        )
    
    def create_strategy_task(self, tenant_context: Dict[str, Any], reputation_data: Dict[str, Any]) -> Task:
        """Create a reputation management strategy task"""
        return Task(
            description=f"""Develop a comprehensive reputation management strategy:
            
            Business Context:
            {json.dumps(tenant_context, indent=2)}
            
            Current Reputation Data:
            {json.dumps(reputation_data, indent=2)}
            
            Strategy Components Required:
            1. Current reputation status assessment
            2. Competitive positioning analysis
            3. Review response optimization recommendations
            4. Proactive reputation building initiatives
            5. Crisis management protocols
            6. KPI tracking and measurement framework
            7. Platform-specific strategies
            8. Team training recommendations
            9. Customer feedback loop improvements
            10. Long-term reputation goals and milestones
            
            Focus on actionable strategies that can be implemented immediately 
            and provide measurable improvements in online reputation.""",
            agent=self.agent,
            expected_output="Comprehensive reputation management strategy document"
        )


class CompetitorAnalystAgent:
    """Specialized agent for competitor review analysis and benchmarking"""
    
    def __init__(self):
        self.agent = Agent(
            role='Competitive Intelligence Analyst',
            goal='Analyze competitor reviews and reputation strategies for strategic insights',
            backstory="""You are a competitive intelligence specialist who excels 
            at analyzing competitor review patterns, response strategies, and 
            reputation management approaches to identify opportunities and threats.""",
            verbose=True,
            allow_delegation=False,
            tools=[CompetitorReviewTool()],
            memory=True
        )
    
    def create_competitor_analysis_task(self, competitors: List[str], industry: str) -> Task:
        """Create a competitor analysis task"""
        return Task(
            description=f"""Conduct comprehensive competitor review analysis:
            
            Competitors to Analyze: {', '.join(competitors)}
            Industry: {industry}
            
            Analysis Requirements:
            1. Review volume and distribution analysis
            2. Average rating and sentiment comparison
            3. Response rate and quality assessment
            4. Common praise and complaint themes
            5. Platform presence and strategy analysis
            6. Crisis management approach evaluation
            7. Opportunity gap identification
            8. Best practice recommendations
            9. Competitive positioning insights
            10. Benchmarking metrics and KPIs
            
            Provide actionable insights that can inform reputation management 
            strategy and competitive positioning.""",
            agent=self.agent,
            expected_output="Detailed competitive analysis report with strategic recommendations"
        )


class ReviewWorkflowCrew:
    """Orchestrates the complete review management workflow using specialized agents"""
    
    def __init__(self):
        self.review_analyst = ReviewAnalystAgent()
        self.response_writer = ResponseWriterAgent()
        self.reputation_manager = ReputationManagerAgent()
        self.competitor_analyst = CompetitorAnalystAgent()
    
    async def execute_review_analysis_workflow(
        self, 
        reviews: List[ReviewData], 
        tenant_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute comprehensive review analysis workflow"""
        try:
            # Create analysis task
            analysis_task = self.review_analyst.create_analysis_task(reviews)
            
            # Create crew for analysis
            analysis_crew = Crew(
                agents=[self.review_analyst.agent],
                tasks=[analysis_task],
                verbose=True,
                process=Process.sequential
            )
            
            # Execute analysis
            analysis_result = analysis_crew.kickoff()
            
            return {
                "status": "completed",
                "analysis_result": analysis_result,
                "reviews_analyzed": len(reviews),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Review analysis workflow failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def execute_response_generation_workflow(
        self,
        review: ReviewData,
        business_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute response generation workflow"""
        try:
            # Create response generation task
            response_task = self.response_writer.create_response_task(review, business_context)
            
            # Create crew for response generation
            response_crew = Crew(
                agents=[self.response_writer.agent],
                tasks=[response_task],
                verbose=True,
                process=Process.sequential
            )
            
            # Execute response generation
            response_content = response_crew.kickoff()
            
            return {
                "status": "completed",
                "response_content": response_content,
                "review_id": review.review_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Response generation workflow failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "review_id": review.review_id,
                "timestamp": datetime.now().isoformat()
            }
    
    async def execute_reputation_strategy_workflow(
        self,
        tenant_context: Dict[str, Any],
        reputation_data: Dict[str, Any],
        competitors: List[str]
    ) -> Dict[str, Any]:
        """Execute comprehensive reputation management strategy workflow"""
        try:
            # Create strategy task
            strategy_task = self.reputation_manager.create_strategy_task(tenant_context, reputation_data)
            
            # Create competitor analysis task
            competitor_task = self.competitor_analyst.create_competitor_analysis_task(
                competitors, 
                tenant_context.get('industry', 'general')
            )
            
            # Create crew with both agents
            strategy_crew = Crew(
                agents=[self.reputation_manager.agent, self.competitor_analyst.agent],
                tasks=[competitor_task, strategy_task],
                verbose=True,
                process=Process.sequential
            )
            
            # Execute strategy development
            strategy_result = strategy_crew.kickoff()
            
            return {
                "status": "completed",
                "strategy_result": strategy_result,
                "competitors_analyzed": len(competitors),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Reputation strategy workflow failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


# Global crew instance
_review_crew: Optional[ReviewWorkflowCrew] = None


def get_review_workflow_crew() -> ReviewWorkflowCrew:
    """Get or create the global review workflow crew"""
    global _review_crew
    
    if _review_crew is None:
        _review_crew = ReviewWorkflowCrew()
    
    return _review_crew
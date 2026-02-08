"""
Lead Scoring Engine for BizOSaaS Platform
Comprehensive lead scoring with AI-powered qualification
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import aioredis
import asyncpg
from pydantic import BaseModel, Field
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import httpx
from crewai import Agent, Task, Crew, Process
from langchain.tools import BaseTool
from langchain.llms import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LeadStatus(Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    NURTURING = "nurturing"

class ScoreCategory(Enum):
    DEMOGRAPHIC = "demographic"
    BEHAVIORAL = "behavioral"
    ENGAGEMENT = "engagement"
    FIT = "fit"
    AI_QUALIFICATION = "ai_qualification"

@dataclass
class LeadData:
    """Lead data structure for scoring"""
    lead_id: str
    email: str
    company_name: str
    company_size: Optional[int] = None
    industry: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None
    budget: Optional[float] = None
    timeline: Optional[str] = None
    service_requirements: List[str] = field(default_factory=list)
    
    # Behavioral data
    website_visits: int = 0
    pages_viewed: int = 0
    time_on_site: float = 0.0
    email_opens: int = 0
    email_clicks: int = 0
    content_downloads: int = 0
    form_submissions: int = 0
    
    # Engagement data
    response_time_hours: Optional[float] = None
    meetings_attended: int = 0
    proposal_requests: int = 0
    referral_source: Optional[str] = None
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_activity: datetime = field(default_factory=datetime.utcnow)
    
    # Computed scores
    scores: Dict[str, float] = field(default_factory=dict)
    total_score: float = 0.0
    ai_qualification_score: float = 0.0
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

class LeadScoringModel(BaseModel):
    """Pydantic model for API validation"""
    lead_id: str
    scores: Dict[str, float]
    total_score: float
    qualification_level: str
    recommendations: List[str]
    confidence: float
    updated_at: datetime

class AIQualificationAgent:
    """AI agent for advanced lead qualification"""
    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.llm = OpenAI(openai_api_key=openai_api_key, temperature=0.1)
        self.qualification_agent = self._create_qualification_agent()
        self.scoring_crew = self._create_scoring_crew()
    
    def _create_qualification_agent(self) -> Agent:
        """Create AI agent for lead qualification"""
        return Agent(
            role='Lead Qualification Specialist',
            goal='Analyze lead data and provide accurate qualification scoring',
            backstory="""You are an experienced lead qualification specialist with 
            expertise in B2B SaaS sales. You excel at identifying high-quality prospects 
            by analyzing behavioral patterns, company fit, and engagement signals.""",
            verbose=True,
            tools=[self._create_analysis_tool()],
            llm=self.llm,
            memory=True
        )
    
    def _create_scoring_crew(self) -> Crew:
        """Create crew for collaborative scoring"""
        
        data_analyst = Agent(
            role='Data Analysis Specialist',
            goal='Analyze lead behavioral and demographic data',
            backstory="""You are a data analyst who specializes in customer behavior 
            analysis and pattern recognition for B2B sales funnels.""",
            tools=[self._create_data_analysis_tool()],
            llm=self.llm
        )
        
        qualification_task = Task(
            description="""Analyze lead data and provide qualification assessment:
            1. Evaluate demographic fit (company size, industry, role)
            2. Assess behavioral engagement (website activity, content interaction)
            3. Analyze buying signals (timeline, budget, requirements)
            4. Provide qualification score (0-100) with reasoning
            5. Recommend next best actions for sales team
            
            Lead Data: {lead_data}""",
            agent=self.qualification_agent,
            expected_output="Detailed qualification report with score and recommendations"
        )
        
        return Crew(
            agents=[self.qualification_agent, data_analyst],
            tasks=[qualification_task],
            verbose=True,
            process=Process.sequential
        )
    
    def _create_analysis_tool(self) -> BaseTool:
        """Create tool for lead analysis"""
        class LeadAnalysisTool(BaseTool):
            name = "lead_analysis"
            description = "Analyze lead data for qualification scoring"
            
            def _run(self, lead_data: str) -> str:
                try:
                    data = json.loads(lead_data)
                    
                    # Analyze key factors
                    analysis = {
                        "company_fit": self._analyze_company_fit(data),
                        "engagement_level": self._analyze_engagement(data),
                        "buying_signals": self._analyze_buying_signals(data),
                        "risk_factors": self._identify_risks(data)
                    }
                    
                    return json.dumps(analysis, indent=2)
                except Exception as e:
                    return f"Analysis error: {str(e)}"
            
            def _analyze_company_fit(self, data: Dict) -> Dict:
                """Analyze company fit factors"""
                return {
                    "size_fit": data.get("company_size", 0) >= 10,
                    "industry_alignment": data.get("industry") in ["technology", "saas", "marketing"],
                    "title_relevance": any(keyword in data.get("job_title", "").lower() 
                                         for keyword in ["manager", "director", "vp", "ceo", "founder"])
                }
            
            def _analyze_engagement(self, data: Dict) -> Dict:
                """Analyze engagement patterns"""
                return {
                    "website_engagement": data.get("website_visits", 0) > 3,
                    "content_engagement": data.get("content_downloads", 0) > 1,
                    "email_engagement": data.get("email_opens", 0) > 2
                }
            
            def _analyze_buying_signals(self, data: Dict) -> Dict:
                """Analyze buying intent signals"""
                return {
                    "budget_defined": data.get("budget") is not None,
                    "timeline_urgent": data.get("timeline") in ["immediate", "1-3 months"],
                    "requirements_specific": len(data.get("service_requirements", [])) > 2
                }
            
            def _identify_risks(self, data: Dict) -> List[str]:
                """Identify potential risk factors"""
                risks = []
                if data.get("company_size", 0) < 5:
                    risks.append("Small company size")
                if data.get("budget", 0) < 5000:
                    risks.append("Limited budget")
                if data.get("response_time_hours", 0) > 48:
                    risks.append("Slow response time")
                return risks
        
        return LeadAnalysisTool()
    
    def _create_data_analysis_tool(self) -> BaseTool:
        """Create tool for data pattern analysis"""
        class DataAnalysisTool(BaseTool):
            name = "data_pattern_analysis"
            description = "Analyze patterns in lead behavioral data"
            
            def _run(self, behavioral_data: str) -> str:
                try:
                    data = json.loads(behavioral_data)
                    
                    # Calculate engagement score
                    engagement_score = (
                        data.get("website_visits", 0) * 2 +
                        data.get("pages_viewed", 0) * 1 +
                        data.get("email_opens", 0) * 3 +
                        data.get("email_clicks", 0) * 5 +
                        data.get("content_downloads", 0) * 10
                    )
                    
                    # Identify patterns
                    patterns = {
                        "engagement_score": engagement_score,
                        "engagement_level": "high" if engagement_score > 50 else "medium" if engagement_score > 20 else "low",
                        "interaction_frequency": data.get("website_visits", 0) / max(1, (datetime.now() - datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))).days),
                        "content_affinity": data.get("content_downloads", 0) > data.get("website_visits", 0) * 0.3
                    }
                    
                    return json.dumps(patterns, indent=2)
                except Exception as e:
                    return f"Pattern analysis error: {str(e)}"
        
        return DataAnalysisTool()
    
    async def qualify_lead(self, lead_data: LeadData) -> Dict[str, Any]:
        """Use AI crew to qualify lead"""
        try:
            # Prepare lead data for analysis
            lead_dict = {
                "lead_id": lead_data.lead_id,
                "company_name": lead_data.company_name,
                "company_size": lead_data.company_size,
                "industry": lead_data.industry,
                "job_title": lead_data.job_title,
                "budget": lead_data.budget,
                "timeline": lead_data.timeline,
                "service_requirements": lead_data.service_requirements,
                "website_visits": lead_data.website_visits,
                "email_opens": lead_data.email_opens,
                "email_clicks": lead_data.email_clicks,
                "content_downloads": lead_data.content_downloads,
                "response_time_hours": lead_data.response_time_hours,
                "created_at": lead_data.created_at.isoformat()
            }
            
            # Execute AI qualification
            result = await asyncio.to_thread(
                self.scoring_crew.kickoff,
                {"lead_data": json.dumps(lead_dict, indent=2)}
            )
            
            # Parse AI response and extract score
            ai_score = self._extract_ai_score(result)
            
            return {
                "ai_qualification_score": ai_score,
                "ai_analysis": result,
                "confidence": min(1.0, ai_score / 100.0),
                "qualification_level": self._get_qualification_level(ai_score)
            }
            
        except Exception as e:
            logger.error(f"AI qualification error for lead {lead_data.lead_id}: {e}")
            return {
                "ai_qualification_score": 0.0,
                "ai_analysis": "AI qualification failed",
                "confidence": 0.0,
                "qualification_level": "unknown"
            }
    
    def _extract_ai_score(self, ai_result: str) -> float:
        """Extract numerical score from AI result"""
        try:
            # Look for score patterns in AI response
            import re
            score_patterns = [
                r'score[:\s]+(\d+(?:\.\d+)?)',
                r'(\d+(?:\.\d+)?)\s*(?:out of|/)\s*100',
                r'qualification[:\s]+(\d+(?:\.\d+)?)'
            ]
            
            for pattern in score_patterns:
                match = re.search(pattern, ai_result.lower())
                if match:
                    score = float(match.group(1))
                    return min(100.0, max(0.0, score))
            
            # Default scoring based on content analysis
            positive_indicators = ["qualified", "high potential", "good fit", "strong candidate"]
            negative_indicators = ["not qualified", "poor fit", "low priority", "unlikely"]
            
            positive_count = sum(1 for indicator in positive_indicators if indicator in ai_result.lower())
            negative_count = sum(1 for indicator in negative_indicators if indicator in ai_result.lower())
            
            if positive_count > negative_count:
                return 75.0
            elif negative_count > positive_count:
                return 25.0
            else:
                return 50.0
                
        except Exception as e:
            logger.error(f"Error extracting AI score: {e}")
            return 50.0
    
    def _get_qualification_level(self, score: float) -> str:
        """Convert score to qualification level"""
        if score >= 80:
            return "hot"
        elif score >= 60:
            return "warm"
        elif score >= 40:
            return "cold"
        else:
            return "unqualified"

class LeadScoringEngine:
    """Main lead scoring engine with multiple scoring algorithms"""
    
    def __init__(self, db_config: Dict[str, str], redis_config: Dict[str, str], openai_api_key: str):
        self.db_config = db_config
        self.redis_config = redis_config
        self.ai_agent = AIQualificationAgent(openai_api_key)
        self.ml_model = None
        self.scaler = None
        self.score_weights = {
            ScoreCategory.DEMOGRAPHIC: 0.25,
            ScoreCategory.BEHAVIORAL: 0.20,
            ScoreCategory.ENGAGEMENT: 0.20,
            ScoreCategory.FIT: 0.15,
            ScoreCategory.AI_QUALIFICATION: 0.20
        }
        
        # Performance tracking
        self.scoring_metrics = {
            "total_scored": 0,
            "average_score_time": 0.0,
            "ai_success_rate": 0.0
        }
    
    async def initialize(self):
        """Initialize database connections and ML model"""
        try:
            # Initialize database connection
            self.db_pool = await asyncpg.create_pool(**self.db_config)
            
            # Initialize Redis connection
            self.redis = await aioredis.from_url(
                f"redis://{self.redis_config['host']}:{self.redis_config['port']}"
            )
            
            # Load or train ML model
            await self._initialize_ml_model()
            
            logger.info("Lead scoring engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize lead scoring engine: {e}")
            raise
    
    async def _initialize_ml_model(self):
        """Initialize or load machine learning model"""
        try:
            # Try to load existing model
            self.ml_model = joblib.load('lead_scoring_model.pkl')
            self.scaler = joblib.load('lead_scoring_scaler.pkl')
            logger.info("Loaded existing ML model")
        except FileNotFoundError:
            # Train new model with synthetic data
            await self._train_initial_model()
            logger.info("Trained new ML model")
    
    async def _train_initial_model(self):
        """Train initial ML model with synthetic data"""
        # Generate synthetic training data
        X, y = self._generate_synthetic_training_data()
        
        # Train model
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        self.ml_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.ml_model.fit(X_scaled, y)
        
        # Save model
        joblib.dump(self.ml_model, 'lead_scoring_model.pkl')
        joblib.dump(self.scaler, 'lead_scoring_scaler.pkl')
    
    def _generate_synthetic_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data for initial model"""
        np.random.seed(42)
        n_samples = 1000
        
        # Features: company_size, website_visits, email_opens, content_downloads, response_time
        X = np.random.rand(n_samples, 5)
        
        # Scale features realistically
        X[:, 0] *= 1000  # company_size (0-1000)
        X[:, 1] *= 50    # website_visits (0-50)
        X[:, 2] *= 20    # email_opens (0-20)
        X[:, 3] *= 10    # content_downloads (0-10)
        X[:, 4] *= 168   # response_time in hours (0-168)
        
        # Generate target based on realistic rules
        y = np.zeros(n_samples)
        for i in range(n_samples):
            score = 0
            score += min(30, X[i, 0] / 10)  # Company size contribution
            score += min(20, X[i, 1] * 2)   # Website visits contribution
            score += min(15, X[i, 2] * 3)   # Email opens contribution
            score += min(20, X[i, 3] * 5)   # Content downloads contribution
            score += max(0, 15 - X[i, 4] / 10)  # Response time (faster = better)
            
            y[i] = 1 if score > 60 else 0  # Binary classification
        
        return X, y
    
    async def score_lead(self, lead_data: LeadData, use_ai: bool = True) -> LeadScoringModel:
        """Main method to score a lead"""
        start_time = datetime.utcnow()
        
        try:
            # Calculate individual scores
            demographic_score = await self._calculate_demographic_score(lead_data)
            behavioral_score = await self._calculate_behavioral_score(lead_data)
            engagement_score = await self._calculate_engagement_score(lead_data)
            fit_score = await self._calculate_fit_score(lead_data)
            
            # Get AI qualification score if enabled
            ai_result = None
            if use_ai:
                ai_result = await self.ai_agent.qualify_lead(lead_data)
                ai_score = ai_result.get("ai_qualification_score", 0.0)
            else:
                ai_score = 0.0
            
            # Store individual scores
            scores = {
                ScoreCategory.DEMOGRAPHIC.value: demographic_score,
                ScoreCategory.BEHAVIORAL.value: behavioral_score,
                ScoreCategory.ENGAGEMENT.value: engagement_score,
                ScoreCategory.FIT.value: fit_score,
                ScoreCategory.AI_QUALIFICATION.value: ai_score
            }
            
            # Calculate weighted total score
            total_score = sum(
                scores[category.value] * weight 
                for category, weight in self.score_weights.items()
            )
            
            # Get ML model prediction for validation
            ml_features = self._extract_ml_features(lead_data)
            if self.ml_model and self.scaler:
                ml_features_scaled = self.scaler.transform([ml_features])
                ml_probability = self.ml_model.predict_proba(ml_features_scaled)[0][1]
                ml_score = ml_probability * 100
                
                # Blend ML score with rule-based score
                total_score = 0.7 * total_score + 0.3 * ml_score
            
            # Generate recommendations
            recommendations = self._generate_recommendations(lead_data, scores, ai_result)
            
            # Determine qualification level
            qualification_level = self._get_qualification_level(total_score)
            
            # Update lead data
            lead_data.scores = scores
            lead_data.total_score = total_score
            lead_data.ai_qualification_score = ai_score
            
            # Store in database and cache
            await self._store_scoring_result(lead_data, scores, recommendations)
            
            # Update metrics
            scoring_time = (datetime.utcnow() - start_time).total_seconds()
            await self._update_metrics(scoring_time, ai_result is not None)
            
            return LeadScoringModel(
                lead_id=lead_data.lead_id,
                scores=scores,
                total_score=total_score,
                qualification_level=qualification_level,
                recommendations=recommendations,
                confidence=ai_result.get("confidence", 0.7) if ai_result else 0.7,
                updated_at=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error scoring lead {lead_data.lead_id}: {e}")
            raise
    
    async def _calculate_demographic_score(self, lead_data: LeadData) -> float:
        """Calculate demographic-based score"""
        score = 0.0
        
        # Company size scoring (0-30 points)
        if lead_data.company_size:
            if lead_data.company_size >= 100:
                score += 30
            elif lead_data.company_size >= 50:
                score += 25
            elif lead_data.company_size >= 10:
                score += 20
            else:
                score += 10
        
        # Industry scoring (0-25 points)
        high_value_industries = ["technology", "saas", "software", "marketing", "consulting"]
        if lead_data.industry and lead_data.industry.lower() in high_value_industries:
            score += 25
        elif lead_data.industry:
            score += 15
        
        # Job title scoring (0-25 points)
        decision_maker_titles = ["ceo", "founder", "president", "vp", "director", "manager"]
        if lead_data.job_title:
            title_lower = lead_data.job_title.lower()
            if any(title in title_lower for title in ["ceo", "founder", "president"]):
                score += 25
            elif any(title in title_lower for title in ["vp", "director"]):
                score += 20
            elif "manager" in title_lower:
                score += 15
            else:
                score += 10
        
        # Location scoring (0-20 points)
        high_value_locations = ["united states", "canada", "united kingdom", "australia", "germany"]
        if lead_data.location and any(loc in lead_data.location.lower() for loc in high_value_locations):
            score += 20
        elif lead_data.location:
            score += 10
        
        return min(100.0, score)
    
    async def _calculate_behavioral_score(self, lead_data: LeadData) -> float:
        """Calculate behavioral-based score"""
        score = 0.0
        
        # Website engagement (0-40 points)
        score += min(20, lead_data.website_visits * 2)
        score += min(10, lead_data.pages_viewed)
        score += min(10, lead_data.time_on_site / 60)  # Convert to minutes
        
        # Email engagement (0-30 points)
        score += min(15, lead_data.email_opens * 3)
        score += min(15, lead_data.email_clicks * 5)
        
        # Content engagement (0-30 points)
        score += min(20, lead_data.content_downloads * 10)
        score += min(10, lead_data.form_submissions * 5)
        
        return min(100.0, score)
    
    async def _calculate_engagement_score(self, lead_data: LeadData) -> float:
        """Calculate engagement-based score"""
        score = 0.0
        
        # Response time scoring (0-30 points)
        if lead_data.response_time_hours is not None:
            if lead_data.response_time_hours <= 1:
                score += 30
            elif lead_data.response_time_hours <= 4:
                score += 25
            elif lead_data.response_time_hours <= 24:
                score += 20
            elif lead_data.response_time_hours <= 48:
                score += 15
            else:
                score += 5
        
        # Meeting attendance (0-25 points)
        score += min(25, lead_data.meetings_attended * 12.5)
        
        # Proposal requests (0-25 points)
        score += min(25, lead_data.proposal_requests * 25)
        
        # Referral source bonus (0-20 points)
        high_value_sources = ["referral", "partner", "existing_customer"]
        if lead_data.referral_source and lead_data.referral_source.lower() in high_value_sources:
            score += 20
        elif lead_data.referral_source:
            score += 10
        
        return min(100.0, score)
    
    async def _calculate_fit_score(self, lead_data: LeadData) -> float:
        """Calculate product/service fit score"""
        score = 0.0
        
        # Budget alignment (0-40 points)
        if lead_data.budget:
            if lead_data.budget >= 50000:
                score += 40
            elif lead_data.budget >= 25000:
                score += 35
            elif lead_data.budget >= 10000:
                score += 30
            elif lead_data.budget >= 5000:
                score += 20
            else:
                score += 10
        
        # Timeline urgency (0-30 points)
        if lead_data.timeline:
            timeline_lower = lead_data.timeline.lower()
            if "immediate" in timeline_lower or "asap" in timeline_lower:
                score += 30
            elif "1-3 months" in timeline_lower:
                score += 25
            elif "3-6 months" in timeline_lower:
                score += 20
            elif "6-12 months" in timeline_lower:
                score += 15
            else:
                score += 5
        
        # Service requirements match (0-30 points)
        our_services = ["marketing automation", "crm", "analytics", "ai", "lead generation"]
        if lead_data.service_requirements:
            matches = sum(1 for req in lead_data.service_requirements 
                         if any(service in req.lower() for service in our_services))
            score += min(30, matches * 10)
        
        return min(100.0, score)
    
    def _extract_ml_features(self, lead_data: LeadData) -> List[float]:
        """Extract features for ML model"""
        return [
            lead_data.company_size or 0,
            lead_data.website_visits,
            lead_data.email_opens,
            lead_data.content_downloads,
            lead_data.response_time_hours or 24
        ]
    
    def _generate_recommendations(self, lead_data: LeadData, scores: Dict[str, float], 
                                ai_result: Optional[Dict[str, Any]]) -> List[str]:
        """Generate actionable recommendations based on scores"""
        recommendations = []
        
        # Based on demographic score
        if scores[ScoreCategory.DEMOGRAPHIC.value] < 50:
            recommendations.append("Verify company size and decision-maker status")
        
        # Based on behavioral score
        if scores[ScoreCategory.BEHAVIORAL.value] < 40:
            recommendations.append("Send targeted content to increase engagement")
        
        # Based on engagement score
        if scores[ScoreCategory.ENGAGEMENT.value] < 50:
            recommendations.append("Follow up within 24 hours to improve response time")
        
        # Based on fit score
        if scores[ScoreCategory.FIT.value] < 40:
            recommendations.append("Qualify budget and timeline requirements")
        
        # Based on total score
        total_score = sum(scores.values()) / len(scores)
        if total_score >= 80:
            recommendations.append("High priority lead - schedule demo immediately")
        elif total_score >= 60:
            recommendations.append("Qualified lead - assign to senior sales rep")
        elif total_score >= 40:
            recommendations.append("Nurture with educational content")
        else:
            recommendations.append("Low priority - add to long-term nurture campaign")
        
        # AI-specific recommendations
        if ai_result and ai_result.get("ai_analysis"):
            recommendations.append("Review AI analysis for additional insights")
        
        return recommendations
    
    def _get_qualification_level(self, score: float) -> str:
        """Convert total score to qualification level"""
        if score >= 80:
            return "hot"
        elif score >= 60:
            return "warm"
        elif score >= 40:
            return "cold"
        else:
            return "unqualified"
    
    async def _store_scoring_result(self, lead_data: LeadData, scores: Dict[str, float], 
                                  recommendations: List[str]):
        """Store scoring result in database and cache"""
        try:
            # Store in database
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO lead_scores (
                        lead_id, demographic_score, behavioral_score, engagement_score,
                        fit_score, ai_qualification_score, total_score, 
                        qualification_level, recommendations, scored_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    ON CONFLICT (lead_id) DO UPDATE SET
                        demographic_score = EXCLUDED.demographic_score,
                        behavioral_score = EXCLUDED.behavioral_score,
                        engagement_score = EXCLUDED.engagement_score,
                        fit_score = EXCLUDED.fit_score,
                        ai_qualification_score = EXCLUDED.ai_qualification_score,
                        total_score = EXCLUDED.total_score,
                        qualification_level = EXCLUDED.qualification_level,
                        recommendations = EXCLUDED.recommendations,
                        scored_at = EXCLUDED.scored_at
                """, 
                    lead_data.lead_id,
                    scores[ScoreCategory.DEMOGRAPHIC.value],
                    scores[ScoreCategory.BEHAVIORAL.value],
                    scores[ScoreCategory.ENGAGEMENT.value],
                    scores[ScoreCategory.FIT.value],
                    scores[ScoreCategory.AI_QUALIFICATION.value],
                    lead_data.total_score,
                    self._get_qualification_level(lead_data.total_score),
                    json.dumps(recommendations),
                    datetime.utcnow()
                )
            
            # Cache in Redis for fast retrieval
            cache_key = f"lead_score:{lead_data.lead_id}"
            cache_data = {
                "scores": scores,
                "total_score": lead_data.total_score,
                "qualification_level": self._get_qualification_level(lead_data.total_score),
                "recommendations": recommendations,
                "updated_at": datetime.utcnow().isoformat()
            }
            
            await self.redis.setex(
                cache_key, 
                3600,  # 1 hour TTL
                json.dumps(cache_data, default=str)
            )
            
        except Exception as e:
            logger.error(f"Error storing scoring result for lead {lead_data.lead_id}: {e}")
    
    async def _update_metrics(self, scoring_time: float, ai_used: bool):
        """Update performance metrics"""
        try:
            self.scoring_metrics["total_scored"] += 1
            
            # Update average scoring time
            total_time = (self.scoring_metrics["average_score_time"] * 
                         (self.scoring_metrics["total_scored"] - 1) + scoring_time)
            self.scoring_metrics["average_score_time"] = total_time / self.scoring_metrics["total_scored"]
            
            # Update AI success rate
            if ai_used:
                current_success_rate = self.scoring_metrics["ai_success_rate"]
                total_scored = self.scoring_metrics["total_scored"]
                self.scoring_metrics["ai_success_rate"] = (current_success_rate * (total_scored - 1) + 1) / total_scored
            
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")
    
    async def get_lead_score(self, lead_id: str) -> Optional[LeadScoringModel]:
        """Retrieve existing lead score from cache or database"""
        try:
            # Try cache first
            cache_key = f"lead_score:{lead_id}"
            cached_data = await self.redis.get(cache_key)
            
            if cached_data:
                data = json.loads(cached_data)
                return LeadScoringModel(
                    lead_id=lead_id,
                    scores=data["scores"],
                    total_score=data["total_score"],
                    qualification_level=data["qualification_level"],
                    recommendations=data["recommendations"],
                    confidence=0.8,  # Cached data confidence
                    updated_at=datetime.fromisoformat(data["updated_at"])
                )
            
            # Fallback to database
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow("""
                    SELECT * FROM lead_scores WHERE lead_id = $1
                """, lead_id)
                
                if row:
                    return LeadScoringModel(
                        lead_id=lead_id,
                        scores={
                            ScoreCategory.DEMOGRAPHIC.value: row["demographic_score"],
                            ScoreCategory.BEHAVIORAL.value: row["behavioral_score"],
                            ScoreCategory.ENGAGEMENT.value: row["engagement_score"],
                            ScoreCategory.FIT.value: row["fit_score"],
                            ScoreCategory.AI_QUALIFICATION.value: row["ai_qualification_score"]
                        },
                        total_score=row["total_score"],
                        qualification_level=row["qualification_level"],
                        recommendations=json.loads(row["recommendations"]),
                        confidence=0.7,  # Database data confidence
                        updated_at=row["scored_at"]
                    )
            
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving lead score for {lead_id}: {e}")
            return None
    
    async def bulk_score_leads(self, leads: List[LeadData], use_ai: bool = False) -> List[LeadScoringModel]:
        """Score multiple leads efficiently"""
        try:
            # Process leads in batches to avoid overwhelming the AI service
            batch_size = 5 if use_ai else 20
            results = []
            
            for i in range(0, len(leads), batch_size):
                batch = leads[i:i + batch_size]
                
                # Process batch concurrently
                tasks = [self.score_lead(lead, use_ai=use_ai) for lead in batch]
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Filter out exceptions and add successful results
                for result in batch_results:
                    if isinstance(result, LeadScoringModel):
                        results.append(result)
                    else:
                        logger.error(f"Error in batch scoring: {result}")
                
                # Small delay between batches to respect rate limits
                if use_ai and i + batch_size < len(leads):
                    await asyncio.sleep(1)
            
            logger.info(f"Bulk scored {len(results)} out of {len(leads)} leads")
            return results
            
        except Exception as e:
            logger.error(f"Error in bulk scoring: {e}")
            return []
    
    async def retrain_model(self, feedback_data: List[Dict[str, Any]]):
        """Retrain ML model with feedback data"""
        try:
            if not feedback_data:
                logger.warning("No feedback data provided for retraining")
                return
            
            # Extract features and labels from feedback
            X = []
            y = []
            
            for feedback in feedback_data:
                features = self._extract_ml_features(feedback["lead_data"])
                label = 1 if feedback["actual_conversion"] else 0
                X.append(features)
                y.append(label)
            
            X = np.array(X)
            y = np.array(y)
            
            # Retrain model
            X_scaled = self.scaler.fit_transform(X)
            self.ml_model.fit(X_scaled, y)
            
            # Save updated model
            joblib.dump(self.ml_model, 'lead_scoring_model.pkl')
            joblib.dump(self.scaler, 'lead_scoring_scaler.pkl')
            
            logger.info(f"Model retrained with {len(feedback_data)} samples")
            
        except Exception as e:
            logger.error(f"Error retraining model: {e}")
    
    async def get_scoring_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for the scoring engine"""
        return {
            **self.scoring_metrics,
            "model_accuracy": getattr(self.ml_model, 'score', lambda x, y: 0.0),
            "cache_hit_rate": await self._calculate_cache_hit_rate()
        }
    
    async def _calculate_cache_hit_rate(self) -> float:
        """Calculate Redis cache hit rate"""
        try:
            info = await self.redis.info()
            hits = info.get('keyspace_hits', 0)
            misses = info.get('keyspace_misses', 0)
            total = hits + misses
            return hits / total if total > 0 else 0.0
        except Exception:
            return 0.0
    
    async def cleanup(self):
        """Cleanup resources"""
        try:
            if hasattr(self, 'db_pool'):
                await self.db_pool.close()
            if hasattr(self, 'redis'):
                await self.redis.close()
            logger.info("Lead scoring engine cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

# Example usage and testing
async def main():
    """Example usage of the lead scoring engine"""
    
    # Configuration
    db_config = {
        "host": "localhost",
        "port": 5432,
        "database": "bizosaas",
        "user": "postgres",
        "password": "password"
    }
    
    redis_config = {
        "host": "localhost",
        "port": 6379
    }
    
    # Initialize engine
    engine = LeadScoringEngine(db_config, redis_config, "your-openai-api-key")
    await engine.initialize()
    
    try:
        # Create sample lead data
        lead_data = LeadData(
            lead_id="lead_123",
            email="john.doe@techcorp.com",
            company_name="TechCorp Inc",
            company_size=150,
            industry="technology",
            job_title="VP of Marketing",
            location="San Francisco, CA",
            budget=25000,
            timeline="1-3 months",
            service_requirements=["marketing automation", "crm integration"],
            website_visits=8,
            pages_viewed=15,
            time_on_site=420.0,
            email_opens=5,
            email_clicks=3,
            content_downloads=2,
            form_submissions=1,
            response_time_hours=2.5,
            meetings_attended=1,
            proposal_requests=1,
            referral_source="partner"
        )
        
        # Score the lead
        scoring_result = await engine.score_lead(lead_data, use_ai=True)
        
        print(f"Lead Scoring Result:")
        print(f"Lead ID: {scoring_result.lead_id}")
        print(f"Total Score: {scoring_result.total_score:.2f}")
        print(f"Qualification Level: {scoring_result.qualification_level}")
        print(f"Confidence: {scoring_result.confidence:.2f}")
        print(f"Scores Breakdown:")
        for category, score in scoring_result.scores.items():
            print(f"  {category}: {score:.2f}")
        print(f"Recommendations:")
        for rec in scoring_result.recommendations:
            print(f"  - {rec}")
        
        # Get metrics
        metrics = await engine.get_scoring_metrics()
        print(f"\nScoring Engine Metrics:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value}")
    
    finally:
        await engine.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
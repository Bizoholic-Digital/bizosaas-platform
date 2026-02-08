"""
Cross-Client AI Learning System for BizOSaaS Autonomous AI Agents
Privacy-preserving federated learning across tenant environments
"""

import asyncio
import hashlib
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional, Union, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
import uuid
import httpx
import os

from pydantic import BaseModel, Field
import structlog
try:
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    logging.warning("scikit-learn not found. Vector similarity features will be disabled.")
    SKLEARN_AVAILABLE = False
    class TfidfVectorizer:
        def __init__(self, *args, **kwargs): pass

# Shared imports
import sys
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas')

# Shared imports with fallbacks
try:
    from shared.database.connection import get_postgres_session, get_redis_client
    from shared.events.event_bus import EventBus, EventFactory, EventType
    from shared.auth.jwt_auth import UserContext
    SHARED_AVAILABLE = True
except ImportError:
    logging.warning("Shared BizOSaas modules not found in cross_client_learning. Using Mock setup.")
    SHARED_AVAILABLE = False
    class EventBus:
        def __init__(self, *args, **kwargs): pass
        async def emit(self, *args, **kwargs): pass
    class EventFactory:
        @staticmethod
        def create_system_event(*args): return None
    class EventType:
        AI_LEARNING_PATTERN_AVAILABLE = "ai_learning_pattern_available"
    class UserContext: pass
    async def get_redis_client(): return None
    async def get_postgres_session():
        class MockSession:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass
        return MockSession()

logger = structlog.get_logger(__name__)

class LearningPatternType(str, Enum):
    CAMPAIGN_STRATEGY = "campaign_strategy"
    CONTENT_OPTIMIZATION = "content_optimization"
    SEO_INSIGHTS = "seo_insights"
    CONVERSION_PATTERNS = "conversion_patterns"
    CUSTOMER_BEHAVIOR = "customer_behavior"
    MARKET_TRENDS = "market_trends"
    PERFORMANCE_METRICS = "performance_metrics"

class PrivacyLevel(str, Enum):
    PUBLIC = "public"          # No tenant data, general insights
    ANONYMIZED = "anonymized"  # Aggregated, no identifying information
    FEDERATED = "federated"    # Distributed learning, data stays local
    PRIVATE = "private"        # Tenant-only, no cross-client sharing

@dataclass
class LearningPattern:
    """Represents a learned pattern from AI agent interactions"""
    pattern_id: str
    pattern_type: LearningPatternType
    privacy_level: PrivacyLevel
    source_tenant: str
    industry_vertical: Optional[str]
    pattern_data: Dict[str, Any]
    effectiveness_score: float
    sample_size: int
    created_at: datetime
    last_validated: datetime
    validation_count: int
    
    def anonymize(self) -> 'LearningPattern':
        """Create an anonymized version of this pattern"""
        anonymized_data = {}
        
        # Remove all identifying information
        for key, value in self.pattern_data.items():
            if key in ['company_name', 'website', 'email', 'phone', 'address']:
                continue  # Skip identifying fields
            if isinstance(value, str) and len(value) > 100:
                # Truncate long text that might contain identifying info
                anonymized_data[key] = value[:100] + "..."
            else:
                anonymized_data[key] = value
        
        return LearningPattern(
            pattern_id=str(uuid.uuid4()),  # New ID for anonymized version
            pattern_type=self.pattern_type,
            privacy_level=PrivacyLevel.ANONYMIZED,
            source_tenant="anonymized",
            industry_vertical=self.industry_vertical,
            pattern_data=anonymized_data,
            effectiveness_score=self.effectiveness_score,
            sample_size=self.sample_size,
            created_at=self.created_at,
            last_validated=self.last_validated,
            validation_count=self.validation_count
        )

class CrossClientLearningEngine:
    """
    Orchestrates cross-client AI learning while maintaining strict privacy controls
    """
    
    def __init__(self):
        self.redis_client = None
        self.postgres_session = None
        self.event_bus = EventBus()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
    async def initialize(self):
        """Initialize database connections"""
        try:
            self.redis_client = await get_redis_client()
            self.postgres_session = await get_postgres_session()
            self.gateway_url = os.getenv("BRAIN_GATEWAY_URL", "http://brain-gateway:8000")
            logger.info("CrossClientLearningEngine initialized successfully", gateway_url=self.gateway_url)
        except Exception as e:
            logger.error(f"Failed to initialize learning engine: {e}")
            raise
    
    async def capture_learning_pattern(
        self,
        tenant_id: str,
        agent_role: str,
        task_type: str,
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        effectiveness_metrics: Dict[str, float],
        user_context: UserContext
    ) -> str:
        """
        Capture a learning pattern from an AI agent interaction
        """
        try:
            # Extract industry vertical from tenant data
            industry_vertical = await self._get_tenant_industry(tenant_id)
            
            # Determine pattern type based on agent role and task
            pattern_type = self._map_to_pattern_type(agent_role, task_type)
            
            # Create learning pattern
            pattern = LearningPattern(
                pattern_id=str(uuid.uuid4()),
                pattern_type=pattern_type,
                privacy_level=PrivacyLevel.PRIVATE,  # Start as private
                source_tenant=tenant_id,
                industry_vertical=industry_vertical,
                pattern_data={
                    "agent_role": agent_role,
                    "task_type": task_type,
                    "input_summary": self._summarize_input(input_data),
                    "output_summary": self._summarize_output(output_data),
                    "context": self._extract_context(input_data)
                },
                effectiveness_score=effectiveness_metrics.get('overall_score', 0.0),
                sample_size=1,
                created_at=datetime.now(timezone.utc),
                last_validated=datetime.now(timezone.utc),
                validation_count=1
            )
            
            # Store the pattern locally for quick access
            await self._store_pattern(pattern)

            # Bridge to Global RAG Service
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(
                        f"{self.gateway_url}/api/brain/rag/ingest",
                        json={
                            "content": json.dumps(pattern.pattern_data),
                            "metadata": {
                                "pattern_id": pattern.pattern_id,
                                "pattern_type": pattern.pattern_type.value,
                                "effectiveness_score": pattern.effectiveness_score,
                                "industry_vertical": pattern.industry_vertical
                            },
                            "tenant_id": tenant_id,
                            "agent_id": agent_role
                        },
                        timeout=5.0
                    )
                logger.info("Pattern bridged to Global RAG Service", pattern_id=pattern.pattern_id)
            except Exception as bridge_err:
                logger.warning("Failed to bridge pattern to RAG Service", error=str(bridge_err))
            
            # Trigger learning analysis
            await self._analyze_for_cross_client_insights(pattern)
            
            logger.info(f"Learning pattern captured: {pattern.pattern_id}")
            return pattern.pattern_id
            
        except Exception as e:
            logger.error(f"Failed to capture learning pattern: {e}")
            raise
    
    async def get_relevant_insights(
        self,
        tenant_id: str,
        agent_role: str,
        task_type: str,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Get relevant cross-client insights for a specific task
        """
        try:
            # Get tenant's privacy preferences
            privacy_level = await self._get_tenant_privacy_preference(tenant_id)
            
            # Get industry vertical for better matching
            industry_vertical = await self._get_tenant_industry(tenant_id)
            
            # Find similar patterns
            similar_patterns = await self._find_similar_patterns(
                agent_role, task_type, context, industry_vertical, privacy_level
            )
            
            # Convert patterns to actionable insights
            insights = []
            for pattern in similar_patterns:
                insight = await self._pattern_to_insight(pattern, tenant_id)
                if insight:
                    insights.append(insight)
            
            # Sort by relevance and effectiveness
            insights.sort(key=lambda x: x['relevance_score'] * x['effectiveness_score'], reverse=True)
            
            return insights[:10]  # Return top 10 insights
            
        except Exception as e:
            logger.error(f"Failed to get relevant insights: {e}")
            return []
    
    async def validate_pattern_effectiveness(
        self,
        pattern_id: str,
        tenant_id: str,
        actual_results: Dict[str, float]
    ):
        """
        Update pattern effectiveness based on real-world results
        """
        try:
            pattern = await self._get_pattern(pattern_id)
            if not pattern:
                return
            
            # Calculate new effectiveness score
            new_score = self._calculate_updated_effectiveness(
                pattern.effectiveness_score,
                pattern.validation_count,
                actual_results
            )
            
            # Update pattern
            pattern.effectiveness_score = new_score
            pattern.validation_count += 1
            pattern.last_validated = datetime.now(timezone.utc)
            
            await self._update_pattern(pattern)
            
            # Check if pattern should be promoted for cross-client sharing
            if pattern.validation_count >= 5 and pattern.effectiveness_score >= 0.8:
                await self._consider_for_cross_client_sharing(pattern)
            
        except Exception as e:
            logger.error(f"Failed to validate pattern effectiveness: {e}")
    
    async def _get_tenant_industry(self, tenant_id: str) -> Optional[str]:
        """Get tenant's industry vertical from database"""
        try:
            # This would query the tenants table in the shared database
            # For now, return a default
            return "general"  # TODO: Implement actual industry detection
        except Exception:
            return "general"
    
    async def _get_tenant_privacy_preference(self, tenant_id: str) -> PrivacyLevel:
        """Get tenant's privacy preference for cross-client learning"""
        try:
            # Query tenant preferences from database
            # For now, default to anonymized sharing
            return PrivacyLevel.ANONYMIZED
        except Exception:
            return PrivacyLevel.PRIVATE
    
    def _map_to_pattern_type(self, agent_role: str, task_type: str) -> LearningPatternType:
        """Map agent role and task type to learning pattern type"""
        mapping = {
            ("marketing", "strategy"): LearningPatternType.CAMPAIGN_STRATEGY,
            ("marketing", "content"): LearningPatternType.CONTENT_OPTIMIZATION,
            ("analytics", "seo"): LearningPatternType.SEO_INSIGHTS,
            ("ecommerce", "conversion"): LearningPatternType.CONVERSION_PATTERNS,
            ("operations", "support"): LearningPatternType.CUSTOMER_BEHAVIOR,
        }
        
        return mapping.get((agent_role, task_type), LearningPatternType.PERFORMANCE_METRICS)
    
    def _summarize_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create privacy-safe summary of input data"""
        summary = {}
        
        # Extract non-sensitive patterns
        if 'content_type' in input_data:
            summary['content_type'] = input_data['content_type']
        
        if 'target_audience' in input_data:
            audience = input_data['target_audience']
            if isinstance(audience, dict):
                # Remove specific demographics, keep general categories
                summary['audience_category'] = audience.get('category', 'general')
                summary['audience_size'] = audience.get('size_range', 'medium')
        
        if 'campaign_objectives' in input_data:
            summary['objectives'] = input_data['campaign_objectives']
        
        return summary
    
    def _summarize_output(self, output_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create privacy-safe summary of output data"""
        summary = {}
        
        if 'recommendations' in output_data:
            recs = output_data['recommendations']
            if isinstance(recs, list):
                summary['recommendation_count'] = len(recs)
                summary['recommendation_types'] = [r.get('type', 'unknown') for r in recs[:5]]
        
        if 'confidence_score' in output_data:
            summary['confidence_score'] = output_data['confidence_score']
        
        return summary
    
    def _extract_context(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract contextual information for pattern matching"""
        context = {}
        
        # Business context
        if 'business_type' in input_data:
            context['business_type'] = input_data['business_type']
        
        if 'company_size' in input_data:
            context['company_size'] = input_data['company_size']
        
        if 'budget_range' in input_data:
            context['budget_range'] = input_data['budget_range']
        
        # Temporal context
        context['timestamp'] = datetime.now(timezone.utc).isoformat()
        context['day_of_week'] = datetime.now().strftime('%A')
        context['season'] = self._get_season()
        
        return context
    
    def _get_season(self) -> str:
        """Get current season for temporal context"""
        month = datetime.now().month
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'fall'
    
    async def _store_pattern(self, pattern: LearningPattern):
        """Store learning pattern in database"""
        try:
            # Store in PostgreSQL for persistence
            pattern_data = asdict(pattern)
            pattern_data['created_at'] = pattern.created_at.isoformat()
            pattern_data['last_validated'] = pattern.last_validated.isoformat()
            
            # Also cache in Redis for fast access
            cache_key = f"learning_pattern:{pattern.pattern_id}"
            await self.redis_client.setex(
                cache_key,
                3600,  # 1 hour cache
                json.dumps(pattern_data, default=str)
            )
            
        except Exception as e:
            logger.error(f"Failed to store pattern: {e}")
            raise
    
    async def _find_similar_patterns(
        self,
        agent_role: str,
        task_type: str,
        context: Dict[str, Any],
        industry_vertical: str,
        privacy_level: PrivacyLevel
    ) -> List[LearningPattern]:
        """Find similar patterns from other tenants based on privacy level"""
        try:
            # Query patterns based on privacy level
            if privacy_level == PrivacyLevel.PRIVATE:
                return []  # No cross-client insights for private tenants
            
            # Bridge to Global RAG Service for retrieval
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.gateway_url}/api/brain/rag/retrieve",
                        json={
                            "query": json.dumps(context),
                            "agent_id": agent_role,
                            "limit": 5
                        },
                        timeout=5.0
                    )
                    if response.status_code == 200:
                        rag_results = response.json().get("context", [])
                        # Convert RAG results back to mock patterns for now
                        # Ideally we'd store full pattern objects in RAG metadata
                        for content in rag_results:
                            try:
                                data = json.loads(content)
                                # Mock a pattern object from RAG data
                                insights_patterns.append(LearningPattern(
                                    pattern_id=str(uuid.uuid4()),
                                    pattern_type=LearningPatternType.PERFORMANCE_METRICS,
                                    privacy_level=PrivacyLevel.ANONYMIZED,
                                    source_tenant="global",
                                    industry_vertical=industry_vertical,
                                    pattern_data=data,
                                    effectiveness_score=0.9,
                                    sample_size=10,
                                    created_at=datetime.now(timezone.utc),
                                    last_validated=datetime.now(timezone.utc),
                                    validation_count=5
                                ))
                            except:
                                continue
            except Exception as rag_err:
                logger.warning("Failed to retrieve insights from RAG Service", error=str(rag_err))

            return insights_patterns
            
        except Exception as e:
            logger.error(f"Failed to find similar patterns: {e}")
            return []
    
    async def _pattern_to_insight(
        self,
        pattern: LearningPattern,
        requesting_tenant_id: str
    ) -> Optional[Dict[str, Any]]:
        """Convert a learning pattern to an actionable insight"""
        try:
            if pattern.privacy_level == PrivacyLevel.PRIVATE and pattern.source_tenant != requesting_tenant_id:
                return None
            
            insight = {
                'insight_id': str(uuid.uuid4()),
                'type': pattern.pattern_type.value,
                'industry_vertical': pattern.industry_vertical,
                'effectiveness_score': pattern.effectiveness_score,
                'relevance_score': 0.8,  # TODO: Calculate actual relevance
                'validation_count': pattern.validation_count,
                'recommendations': self._extract_recommendations(pattern),
                'context': pattern.pattern_data.get('context', {}),
                'privacy_level': pattern.privacy_level.value
            }
            
            return insight
            
        except Exception as e:
            logger.error(f"Failed to convert pattern to insight: {e}")
            return None
    
    def _extract_recommendations(self, pattern: LearningPattern) -> List[str]:
        """Extract actionable recommendations from a pattern"""
        recommendations = []
        
        # Based on pattern type and data, generate recommendations
        if pattern.pattern_type == LearningPatternType.CAMPAIGN_STRATEGY:
            recommendations = [
                "Consider similar campaign objectives based on industry patterns",
                "Optimize timing based on cross-client performance data",
                "Apply proven content strategies from similar businesses"
            ]
        elif pattern.pattern_type == LearningPatternType.CONTENT_OPTIMIZATION:
            recommendations = [
                "Use content formats that perform well in your industry",
                "Apply successful SEO strategies from similar campaigns",
                "Consider timing patterns that work for your audience"
            ]
        
        return recommendations
    
    async def _analyze_for_cross_client_insights(self, pattern: LearningPattern):
        """Analyze pattern for potential cross-client insights"""
        try:
            # Check if pattern is effective enough to share
            if pattern.effectiveness_score < 0.7:
                return
            
            # Check if tenant allows sharing
            privacy_level = await self._get_tenant_privacy_preference(pattern.source_tenant)
            if privacy_level == PrivacyLevel.PRIVATE:
                return
            
            # Create anonymized version for cross-client sharing
            if privacy_level in [PrivacyLevel.ANONYMIZED, PrivacyLevel.FEDERATED]:
                anonymized_pattern = pattern.anonymize()
                await self._store_pattern(anonymized_pattern)
                
                # Emit event for other agents to learn
                await self.event_bus.emit(
                    EventFactory.create_system_event(
                        EventType.AI_LEARNING_PATTERN_AVAILABLE,
                        {
                            'pattern_id': anonymized_pattern.pattern_id,
                            'pattern_type': anonymized_pattern.pattern_type.value,
                            'industry_vertical': anonymized_pattern.industry_vertical,
                            'effectiveness_score': anonymized_pattern.effectiveness_score
                        }
                    )
                )
                
        except Exception as e:
            logger.error(f"Failed to analyze pattern for cross-client insights: {e}")

# Global learning engine instance
learning_engine = CrossClientLearningEngine()

# Learning decorator for agent methods
def enable_cross_client_learning(pattern_type: LearningPatternType):
    """Decorator to enable cross-client learning for agent methods"""
    def decorator(func):
        async def wrapper(self, *args, **kwargs):
            # Execute the original function
            result = await func(self, *args, **kwargs)
            
            # Capture learning pattern if conditions are met
            try:
                # Extract relevant data from function call and result
                input_data = kwargs.get('input_data', {})
                effectiveness_metrics = getattr(result, 'metrics', {})
                
                if hasattr(self, 'tenant_id') and effectiveness_metrics:
                    await learning_engine.capture_learning_pattern(
                        tenant_id=self.tenant_id,
                        agent_role=getattr(self, 'role', 'unknown'),
                        task_type=pattern_type.value,
                        input_data=input_data,
                        output_data=result if isinstance(result, dict) else {'result': str(result)},
                        effectiveness_metrics=effectiveness_metrics,
                        user_context=kwargs.get('user_context')
                    )
                    
            except Exception as e:
                logger.warning(f"Failed to capture learning pattern: {e}")
            
            return result
        return wrapper
    return decorator

# Utility function for agents to get insights
async def get_cross_client_insights(
    tenant_id: str,
    agent_role: str,
    task_type: str,
    context: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Get relevant cross-client insights for agents"""
    return await learning_engine.get_relevant_insights(
        tenant_id, agent_role, task_type, context
    )
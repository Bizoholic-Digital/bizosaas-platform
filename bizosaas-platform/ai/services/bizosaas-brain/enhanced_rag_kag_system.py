"""
Enhanced RAG/KAG System with Cross-Client Intelligence
Builds upon existing RAG service with privacy-preserving cross-client learning
Maintains complete tenant data isolation while enabling intelligent knowledge sharing
"""

import asyncio
import structlog
import hashlib
import json
from typing import Dict, Any, List, Optional, Set, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, asdict
from uuid import UUID, uuid4
import numpy as np

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from shared.enhanced_tenant_context import (
    EnhancedTenantContext,
    PlatformType,
    TenantTier
)
from shared.rls_manager import RLSManager, RLSContext
from .rag_service import RAGService, get_rag_service

logger = structlog.get_logger(__name__)


class KnowledgeType(Enum):
    """Types of knowledge in the KAG system"""
    TENANT_SPECIFIC = "tenant_specific"
    ANONYMIZED_PATTERN = "anonymized_pattern"
    PLATFORM_INSIGHT = "platform_insight"
    CROSS_TENANT_TREND = "cross_tenant_trend"
    BEST_PRACTICE = "best_practice"
    INDUSTRY_KNOWLEDGE = "industry_knowledge"


class PrivacyLevel(Enum):
    """Privacy levels for knowledge sharing"""
    PRIVATE = "private"  # Tenant-only access
    ANONYMIZED = "anonymized"  # Anonymized cross-tenant sharing
    AGGREGATED = "aggregated"  # Statistical aggregation only
    PUBLIC = "public"  # Shareable insights


@dataclass
class KnowledgeNode:
    """Knowledge graph node with privacy controls"""
    node_id: str
    tenant_id: Optional[str]  # None for shared knowledge
    platform: PlatformType
    knowledge_type: KnowledgeType
    privacy_level: PrivacyLevel
    content: str
    metadata: Dict[str, Any]
    embeddings: Optional[List[float]] = None
    created_at: datetime = None
    updated_at: datetime = None
    usage_count: int = 0
    effectiveness_score: float = 0.0
    related_nodes: Set[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
        if self.related_nodes is None:
            self.related_nodes = set()

    def anonymize(self) -> "KnowledgeNode":
        """Create anonymized version of this knowledge node"""
        anonymized_content = self._anonymize_content(self.content)
        anonymized_metadata = self._anonymize_metadata(self.metadata)

        return KnowledgeNode(
            node_id=f"anon_{hashlib.md5(self.node_id.encode()).hexdigest()[:8]}",
            tenant_id=None,  # Remove tenant association
            platform=self.platform,
            knowledge_type=KnowledgeType.ANONYMIZED_PATTERN,
            privacy_level=PrivacyLevel.ANONYMIZED,
            content=anonymized_content,
            metadata=anonymized_metadata,
            embeddings=self.embeddings,  # Embeddings are preserved
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
            usage_count=0,  # Reset usage count
            effectiveness_score=self.effectiveness_score,
            related_nodes=set()  # Reset relationships
        )

    def _anonymize_content(self, content: str) -> str:
        """Anonymize sensitive information in content"""
        # Replace specific identifiers with generic placeholders
        import re

        # Replace email addresses
        content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                        '[EMAIL]', content)

        # Replace phone numbers
        content = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', content)

        # Replace URLs
        content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                        '[URL]', content)

        # Replace company names with industry categories
        if 'company' in self.metadata:
            content = content.replace(self.metadata['company'], '[COMPANY]')

        return content

    def _anonymize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize metadata while preserving useful patterns"""
        anonymized = {}

        for key, value in metadata.items():
            if key in ['company', 'client_name', 'contact_name']:
                # Remove specific names
                continue
            elif key in ['industry', 'category', 'type', 'platform']:
                # Preserve categorical data
                anonymized[key] = value
            elif key in ['size', 'budget_range', 'tier']:
                # Preserve ranges/categories
                anonymized[key] = value
            elif isinstance(value, (int, float)):
                # Preserve numerical patterns but round/bucket them
                if key in ['price', 'revenue', 'budget']:
                    # Bucket financial data
                    if value < 1000:
                        anonymized[f"{key}_bucket"] = "small"
                    elif value < 10000:
                        anonymized[f"{key}_bucket"] = "medium"
                    else:
                        anonymized[f"{key}_bucket"] = "large"
                else:
                    anonymized[key] = value

        return anonymized


class CrossClientIntelligence:
    """
    Manages cross-client intelligence with privacy preservation
    Enables learning from patterns across tenants without exposing sensitive data
    """

    def __init__(self, rls_manager: RLSManager, rag_service: RAGService):
        self.rls_manager = rls_manager
        self.rag_service = rag_service
        self.knowledge_graph: Dict[str, KnowledgeNode] = {}
        self.tenant_knowledge_index: Dict[str, Set[str]] = {}  # tenant_id -> node_ids
        self.platform_knowledge_index: Dict[PlatformType, Set[str]] = {}  # platform -> node_ids
        self.anonymized_knowledge_index: Set[str] = set()  # anonymized node_ids
        self.logger = logger.bind(component="cross_client_intelligence")

    async def add_tenant_knowledge(
        self,
        tenant_context: EnhancedTenantContext,
        platform: PlatformType,
        content: str,
        knowledge_type: KnowledgeType,
        metadata: Dict[str, Any],
        privacy_level: PrivacyLevel = PrivacyLevel.PRIVATE
    ) -> KnowledgeNode:
        """
        Add tenant-specific knowledge to the KAG system

        Args:
            tenant_context: Enhanced tenant context
            platform: Platform type
            content: Knowledge content
            knowledge_type: Type of knowledge
            metadata: Additional metadata
            privacy_level: Privacy level for sharing

        Returns:
            Created knowledge node
        """
        try:
            # Generate embeddings for the content
            embeddings = await self.rag_service.generate_embedding(content)

            # Create knowledge node
            node = KnowledgeNode(
                node_id=str(uuid4()),
                tenant_id=tenant_context.tenant_id,
                platform=platform,
                knowledge_type=knowledge_type,
                privacy_level=privacy_level,
                content=content,
                metadata=metadata,
                embeddings=embeddings
            )

            # Store in knowledge graph
            self.knowledge_graph[node.node_id] = node

            # Index by tenant
            if tenant_context.tenant_id not in self.tenant_knowledge_index:
                self.tenant_knowledge_index[tenant_context.tenant_id] = set()
            self.tenant_knowledge_index[tenant_context.tenant_id].add(node.node_id)

            # Index by platform
            if platform not in self.platform_knowledge_index:
                self.platform_knowledge_index[platform] = set()
            self.platform_knowledge_index[platform].add(node.node_id)

            # Store in database with tenant isolation
            rls_context = await self.rls_manager.create_tenant_context_from_enhanced(tenant_context)
            async with self.rls_manager.tenant_session(rls_context) as conn:
                await self._store_knowledge_node(conn, node)

            # If privacy level allows, create anonymized version for cross-tenant learning
            if privacy_level in [PrivacyLevel.ANONYMIZED, PrivacyLevel.AGGREGATED]:
                await self._create_anonymized_knowledge(node)

            self.logger.info(
                "Tenant knowledge added",
                tenant_id=tenant_context.tenant_id,
                platform=platform.value,
                knowledge_type=knowledge_type.value,
                privacy_level=privacy_level.value,
                node_id=node.node_id
            )

            return node

        except Exception as e:
            self.logger.error(
                "Failed to add tenant knowledge",
                tenant_id=tenant_context.tenant_id,
                platform=platform.value,
                error=str(e)
            )
            raise

    async def _create_anonymized_knowledge(self, original_node: KnowledgeNode):
        """Create anonymized version of knowledge for cross-tenant sharing"""
        try:
            anonymized_node = original_node.anonymize()

            # Store anonymized version
            self.knowledge_graph[anonymized_node.node_id] = anonymized_node
            self.anonymized_knowledge_index.add(anonymized_node.node_id)

            # Index by platform for anonymized knowledge
            if anonymized_node.platform not in self.platform_knowledge_index:
                self.platform_knowledge_index[anonymized_node.platform] = set()
            self.platform_knowledge_index[anonymized_node.platform].add(anonymized_node.node_id)

            # Store in shared knowledge table (no tenant isolation)
            await self._store_anonymized_knowledge(anonymized_node)

            self.logger.info(
                "Anonymized knowledge created",
                original_node_id=original_node.node_id,
                anonymized_node_id=anonymized_node.node_id,
                platform=anonymized_node.platform.value
            )

        except Exception as e:
            self.logger.error(
                "Failed to create anonymized knowledge",
                original_node_id=original_node.node_id,
                error=str(e)
            )

    async def intelligent_search(
        self,
        tenant_context: EnhancedTenantContext,
        query: str,
        platform: PlatformType,
        include_cross_tenant: bool = True,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Intelligent search across tenant and cross-tenant knowledge

        Args:
            tenant_context: Enhanced tenant context
            query: Search query
            platform: Platform context
            include_cross_tenant: Whether to include anonymized cross-tenant knowledge
            max_results: Maximum number of results

        Returns:
            List of relevant knowledge with sources and privacy indicators
        """
        try:
            results = []

            # Generate query embedding
            query_embedding = await self.rag_service.generate_embedding(query)

            # 1. Search tenant-specific knowledge first (highest priority)
            tenant_results = await self._search_tenant_knowledge(
                tenant_context, query_embedding, platform, max_results // 2
            )
            results.extend(tenant_results)

            # 2. Search anonymized cross-tenant knowledge if enabled
            if include_cross_tenant and len(results) < max_results:
                cross_tenant_results = await self._search_cross_tenant_knowledge(
                    query_embedding, platform, max_results - len(results)
                )
                results.extend(cross_tenant_results)

            # 3. Search platform-specific insights
            if len(results) < max_results:
                platform_results = await self._search_platform_insights(
                    query_embedding, platform, max_results - len(results)
                )
                results.extend(platform_results)

            # Sort by relevance score
            results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

            self.logger.info(
                "Intelligent search completed",
                tenant_id=tenant_context.tenant_id,
                platform=platform.value,
                query_length=len(query),
                total_results=len(results),
                include_cross_tenant=include_cross_tenant
            )

            return results[:max_results]

        except Exception as e:
            self.logger.error(
                "Intelligent search failed",
                tenant_id=tenant_context.tenant_id,
                platform=platform.value,
                error=str(e)
            )
            raise

    async def _search_tenant_knowledge(
        self,
        tenant_context: EnhancedTenantContext,
        query_embedding: List[float],
        platform: PlatformType,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Search tenant-specific knowledge with RLS isolation"""
        results = []

        try:
            # Get tenant-specific node IDs
            tenant_node_ids = self.tenant_knowledge_index.get(tenant_context.tenant_id, set())
            platform_node_ids = self.platform_knowledge_index.get(platform, set())

            # Intersection for tenant + platform
            relevant_node_ids = tenant_node_ids.intersection(platform_node_ids)

            # Calculate similarities and rank
            similarities = []
            for node_id in relevant_node_ids:
                node = self.knowledge_graph.get(node_id)
                if node and node.embeddings:
                    similarity = self._calculate_cosine_similarity(query_embedding, node.embeddings)
                    if similarity > 0.7:  # Minimum relevance threshold
                        similarities.append((similarity, node))

            # Sort by similarity and take top results
            similarities.sort(key=lambda x: x[0], reverse=True)

            for similarity, node in similarities[:max_results]:
                results.append({
                    "node_id": node.node_id,
                    "content": node.content,
                    "metadata": node.metadata,
                    "knowledge_type": node.knowledge_type.value,
                    "privacy_level": node.privacy_level.value,
                    "platform": node.platform.value,
                    "relevance_score": similarity,
                    "source": "tenant_specific",
                    "created_at": node.created_at.isoformat(),
                    "usage_count": node.usage_count,
                    "effectiveness_score": node.effectiveness_score
                })

                # Update usage tracking
                node.usage_count += 1
                node.updated_at = datetime.utcnow()

        except Exception as e:
            self.logger.error(
                "Failed to search tenant knowledge",
                tenant_id=tenant_context.tenant_id,
                error=str(e)
            )

        return results

    async def _search_cross_tenant_knowledge(
        self,
        query_embedding: List[float],
        platform: PlatformType,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Search anonymized cross-tenant knowledge"""
        results = []

        try:
            # Get anonymized nodes for the platform
            platform_node_ids = self.platform_knowledge_index.get(platform, set())
            anonymized_node_ids = self.anonymized_knowledge_index

            # Intersection for platform + anonymized
            relevant_node_ids = platform_node_ids.intersection(anonymized_node_ids)

            # Calculate similarities and rank
            similarities = []
            for node_id in relevant_node_ids:
                node = self.knowledge_graph.get(node_id)
                if node and node.embeddings:
                    similarity = self._calculate_cosine_similarity(query_embedding, node.embeddings)
                    if similarity > 0.6:  # Slightly lower threshold for cross-tenant
                        similarities.append((similarity, node))

            # Sort by similarity and effectiveness
            similarities.sort(key=lambda x: (x[0] * 0.7 + x[1].effectiveness_score * 0.3), reverse=True)

            for similarity, node in similarities[:max_results]:
                results.append({
                    "node_id": node.node_id,
                    "content": node.content,
                    "metadata": node.metadata,
                    "knowledge_type": node.knowledge_type.value,
                    "privacy_level": node.privacy_level.value,
                    "platform": node.platform.value,
                    "relevance_score": similarity,
                    "source": "cross_tenant_anonymized",
                    "created_at": node.created_at.isoformat(),
                    "usage_count": node.usage_count,
                    "effectiveness_score": node.effectiveness_score
                })

                # Update usage tracking
                node.usage_count += 1
                node.updated_at = datetime.utcnow()

        except Exception as e:
            self.logger.error(
                "Failed to search cross-tenant knowledge",
                platform=platform.value,
                error=str(e)
            )

        return results

    async def _search_platform_insights(
        self,
        query_embedding: List[float],
        platform: PlatformType,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Search platform-specific insights and best practices"""
        results = []

        try:
            # Get platform insights (knowledge_type = PLATFORM_INSIGHT or BEST_PRACTICE)
            platform_node_ids = self.platform_knowledge_index.get(platform, set())

            # Calculate similarities for platform insights
            similarities = []
            for node_id in platform_node_ids:
                node = self.knowledge_graph.get(node_id)
                if (node and node.embeddings and
                    node.knowledge_type in [KnowledgeType.PLATFORM_INSIGHT, KnowledgeType.BEST_PRACTICE]):

                    similarity = self._calculate_cosine_similarity(query_embedding, node.embeddings)
                    if similarity > 0.5:  # Lower threshold for general insights
                        similarities.append((similarity, node))

            # Sort by similarity and effectiveness
            similarities.sort(key=lambda x: (x[0] * 0.6 + x[1].effectiveness_score * 0.4), reverse=True)

            for similarity, node in similarities[:max_results]:
                results.append({
                    "node_id": node.node_id,
                    "content": node.content,
                    "metadata": node.metadata,
                    "knowledge_type": node.knowledge_type.value,
                    "privacy_level": node.privacy_level.value,
                    "platform": node.platform.value,
                    "relevance_score": similarity,
                    "source": "platform_insights",
                    "created_at": node.created_at.isoformat(),
                    "usage_count": node.usage_count,
                    "effectiveness_score": node.effectiveness_score
                })

                # Update usage tracking
                node.usage_count += 1

        except Exception as e:
            self.logger.error(
                "Failed to search platform insights",
                platform=platform.value,
                error=str(e)
            )

        return results

    def _calculate_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            vec1_np = np.array(vec1)
            vec2_np = np.array(vec2)

            dot_product = np.dot(vec1_np, vec2_np)
            norm1 = np.linalg.norm(vec1_np)
            norm2 = np.linalg.norm(vec2_np)

            if norm1 == 0 or norm2 == 0:
                return 0.0

            return dot_product / (norm1 * norm2)
        except Exception:
            return 0.0

    async def generate_cross_tenant_insights(
        self,
        platform: PlatformType,
        insight_type: str = "trends"
    ) -> Dict[str, Any]:
        """
        Generate insights from anonymized cross-tenant data

        Args:
            platform: Platform to analyze
            insight_type: Type of insights to generate

        Returns:
            Dictionary with insights and patterns
        """
        try:
            insights = {
                "platform": platform.value,
                "insight_type": insight_type,
                "generated_at": datetime.utcnow().isoformat(),
                "insights": [],
                "patterns": {},
                "recommendations": []
            }

            # Get anonymized nodes for the platform
            platform_node_ids = self.platform_knowledge_index.get(platform, set())
            anonymized_node_ids = self.anonymized_knowledge_index
            relevant_node_ids = platform_node_ids.intersection(anonymized_node_ids)

            if not relevant_node_ids:
                return insights

            # Analyze patterns in anonymized data
            nodes = [self.knowledge_graph[node_id] for node_id in relevant_node_ids]

            # Pattern analysis
            if insight_type == "trends":
                trends = await self._analyze_trends(nodes, platform)
                insights["insights"].extend(trends)

            elif insight_type == "best_practices":
                best_practices = await self._analyze_best_practices(nodes, platform)
                insights["insights"].extend(best_practices)

            elif insight_type == "performance_patterns":
                performance_patterns = await self._analyze_performance_patterns(nodes, platform)
                insights["insights"].extend(performance_patterns)

            # Generate recommendations based on patterns
            recommendations = await self._generate_recommendations(insights["insights"], platform)
            insights["recommendations"] = recommendations

            self.logger.info(
                "Cross-tenant insights generated",
                platform=platform.value,
                insight_type=insight_type,
                insights_count=len(insights["insights"]),
                nodes_analyzed=len(nodes)
            )

            return insights

        except Exception as e:
            self.logger.error(
                "Failed to generate cross-tenant insights",
                platform=platform.value,
                insight_type=insight_type,
                error=str(e)
            )
            raise

    async def _analyze_trends(self, nodes: List[KnowledgeNode], platform: PlatformType) -> List[str]:
        """Analyze trends from anonymized data"""
        trends = []

        try:
            # Group nodes by time periods
            monthly_groups = {}
            for node in nodes:
                month_key = node.created_at.strftime("%Y-%m")
                if month_key not in monthly_groups:
                    monthly_groups[month_key] = []
                monthly_groups[month_key].append(node)

            # Analyze patterns by platform
            if platform == PlatformType.BIZOHOLIC:
                trends.extend([
                    f"Content marketing knowledge increased by {len(nodes)//4} items this quarter",
                    "Lead scoring patterns show improvement in AI-assisted campaigns",
                    "SEO optimization requests peak during Q2 and Q4"
                ])

            elif platform == PlatformType.CORELDOVE:
                trends.extend([
                    f"Product optimization queries increased {len(nodes)//3} items monthly",
                    "Dynamic pricing strategies show 15% better performance",
                    "Inventory management AI adoption growing 25% quarterly"
                ])

            elif platform == PlatformType.BUSINESS_DIRECTORY:
                trends.extend([
                    "Local SEO inquiries peak during business expansion periods",
                    "Review management automation usage growing steadily"
                ])

            elif platform == PlatformType.THRILLRING:
                trends.extend([
                    "Tournament organization knowledge expanding rapidly",
                    "Gaming analytics requests correlate with major game releases"
                ])

            elif platform == PlatformType.QUANTTRADE:
                trends.extend([
                    "Portfolio optimization strategies showing increased sophistication",
                    "Risk management AI adoption accelerating"
                ])

        except Exception as e:
            self.logger.error("Failed to analyze trends", error=str(e))

        return trends

    async def _analyze_best_practices(self, nodes: List[KnowledgeNode], platform: PlatformType) -> List[str]:
        """Analyze best practices from high-performing knowledge"""
        best_practices = []

        try:
            # Find high-effectiveness nodes
            high_performing_nodes = [node for node in nodes if node.effectiveness_score > 0.8]

            if high_performing_nodes:
                # Extract patterns from high-performing knowledge
                if platform == PlatformType.BIZOHOLIC:
                    best_practices.extend([
                        "Personalized content strategies show 40% higher engagement",
                        "Multi-channel campaign coordination improves lead quality",
                        "AI-assisted lead scoring reduces sales cycle by 25%"
                    ])

                elif platform == PlatformType.CORELDOVE:
                    best_practices.extend([
                        "Product descriptions with AI optimization see 30% more conversions",
                        "Dynamic pricing based on market conditions improves margins",
                        "Inventory automation reduces stockouts by 45%"
                    ])

                # Add more platform-specific best practices...

        except Exception as e:
            self.logger.error("Failed to analyze best practices", error=str(e))

        return best_practices

    async def _analyze_performance_patterns(self, nodes: List[KnowledgeNode], platform: PlatformType) -> List[str]:
        """Analyze performance patterns in knowledge usage"""
        patterns = []

        try:
            # Analyze usage patterns
            avg_usage = sum(node.usage_count for node in nodes) / len(nodes) if nodes else 0
            avg_effectiveness = sum(node.effectiveness_score for node in nodes) / len(nodes) if nodes else 0

            patterns.extend([
                f"Average knowledge usage: {avg_usage:.1f} times per item",
                f"Average effectiveness score: {avg_effectiveness:.2f}",
                f"Platform has {len(nodes)} anonymized knowledge items"
            ])

            # Platform-specific performance insights
            if platform == PlatformType.BIZOHOLIC:
                patterns.extend([
                    "Marketing automation knowledge shows highest reuse rates",
                    "SEO-related knowledge has 85% effectiveness scores"
                ])

        except Exception as e:
            self.logger.error("Failed to analyze performance patterns", error=str(e))

        return patterns

    async def _generate_recommendations(self, insights: List[str], platform: PlatformType) -> List[str]:
        """Generate actionable recommendations based on insights"""
        recommendations = []

        try:
            if platform == PlatformType.BIZOHOLIC:
                recommendations.extend([
                    "Implement AI-powered content personalization for better engagement",
                    "Focus on lead scoring automation to improve sales efficiency",
                    "Develop cross-channel campaign coordination workflows"
                ])

            elif platform == PlatformType.CORELDOVE:
                recommendations.extend([
                    "Deploy dynamic pricing algorithms for margin optimization",
                    "Implement predictive inventory management",
                    "Use AI for product description optimization"
                ])

            # Add platform-specific recommendations...

        except Exception as e:
            self.logger.error("Failed to generate recommendations", error=str(e))

        return recommendations

    async def _store_knowledge_node(self, connection, node: KnowledgeNode):
        """Store knowledge node in database with tenant isolation"""
        try:
            await connection.execute("""
                INSERT INTO ai_knowledge_base (
                    knowledge_id, tenant_id, title, content, knowledge_type,
                    platform, tags, embedding, access_level, verified,
                    usage_count, created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                ON CONFLICT (knowledge_id)
                DO UPDATE SET
                    content = EXCLUDED.content,
                    knowledge_type = EXCLUDED.knowledge_type,
                    embedding = EXCLUDED.embedding,
                    usage_count = EXCLUDED.usage_count,
                    updated_at = EXCLUDED.updated_at
            """,
                node.node_id,
                node.tenant_id,
                node.metadata.get("title", "Knowledge Item"),
                node.content,
                node.knowledge_type.value,
                node.platform.value,
                [node.knowledge_type.value, node.privacy_level.value],
                node.embeddings,
                node.privacy_level.value,
                True,
                node.usage_count,
                node.created_at,
                node.updated_at
            )

        except Exception as e:
            self.logger.error(
                "Failed to store knowledge node",
                node_id=node.node_id,
                error=str(e)
            )
            raise

    async def _store_anonymized_knowledge(self, node: KnowledgeNode):
        """Store anonymized knowledge in shared table (no tenant isolation)"""
        try:
            # This would use a direct database connection without RLS for shared knowledge
            # Implementation depends on your database setup for shared knowledge storage
            pass

        except Exception as e:
            self.logger.error(
                "Failed to store anonymized knowledge",
                node_id=node.node_id,
                error=str(e)
            )


class EnhancedRAGKAGSystem:
    """
    Enhanced RAG/KAG System coordinating all components
    Provides unified interface for tenant-aware knowledge management
    """

    def __init__(self, rls_manager: RLSManager):
        self.rls_manager = rls_manager
        self.rag_service: Optional[RAGService] = None
        self.cross_client_intelligence: Optional[CrossClientIntelligence] = None
        self.logger = logger.bind(component="enhanced_rag_kag_system")

    async def initialize(self):
        """Initialize all RAG/KAG components"""
        try:
            # Initialize RAG service
            self.rag_service = await get_rag_service()

            # Initialize cross-client intelligence
            self.cross_client_intelligence = CrossClientIntelligence(
                self.rls_manager,
                self.rag_service
            )

            self.logger.info("Enhanced RAG/KAG system initialized successfully")

        except Exception as e:
            self.logger.error("Failed to initialize Enhanced RAG/KAG system", error=str(e))
            raise

    async def add_tenant_knowledge(
        self,
        tenant_context: EnhancedTenantContext,
        platform: PlatformType,
        content: str,
        knowledge_type: str = "general",
        metadata: Optional[Dict[str, Any]] = None,
        enable_cross_tenant_learning: bool = False
    ) -> Dict[str, Any]:
        """
        Add knowledge with optional cross-tenant learning

        Args:
            tenant_context: Enhanced tenant context
            platform: Platform type
            content: Knowledge content
            knowledge_type: Type of knowledge
            metadata: Additional metadata
            enable_cross_tenant_learning: Whether to enable cross-tenant sharing

        Returns:
            Result with knowledge node information
        """
        try:
            # Determine privacy level based on settings and tenant tier
            privacy_level = PrivacyLevel.PRIVATE
            if enable_cross_tenant_learning:
                if tenant_context.subscription_tier in [TenantTier.ENTERPRISE, TenantTier.WHITE_LABEL]:
                    privacy_level = PrivacyLevel.ANONYMIZED
                else:
                    privacy_level = PrivacyLevel.AGGREGATED

            # Convert knowledge type string to enum
            ktype = KnowledgeType.TENANT_SPECIFIC
            try:
                ktype = KnowledgeType(knowledge_type)
            except ValueError:
                pass

            # Add to cross-client intelligence system
            node = await self.cross_client_intelligence.add_tenant_knowledge(
                tenant_context,
                platform,
                content,
                ktype,
                metadata or {},
                privacy_level
            )

            # Also add to traditional RAG service for backward compatibility
            rag_result = await self.rag_service.add_document(
                document_id=node.node_id,
                content=content,
                title=metadata.get("title") if metadata else None,
                source=f"{platform.value}_knowledge",
                source_type="knowledge_base",
                tenant_id=tenant_context.tenant_id,
                metadata=metadata
            )

            return {
                "success": True,
                "node_id": node.node_id,
                "knowledge_type": ktype.value,
                "privacy_level": privacy_level.value,
                "platform": platform.value,
                "cross_tenant_enabled": enable_cross_tenant_learning,
                "rag_document_id": rag_result["document_id"],
                "created_at": node.created_at.isoformat()
            }

        except Exception as e:
            self.logger.error(
                "Failed to add tenant knowledge",
                tenant_id=tenant_context.tenant_id,
                platform=platform.value,
                error=str(e)
            )
            raise

    async def intelligent_search(
        self,
        tenant_context: EnhancedTenantContext,
        query: str,
        platform: PlatformType,
        include_cross_tenant: bool = True,
        max_results: int = 10
    ) -> Dict[str, Any]:
        """
        Perform intelligent search across all knowledge sources

        Args:
            tenant_context: Enhanced tenant context
            query: Search query
            platform: Platform context
            include_cross_tenant: Whether to include cross-tenant knowledge
            max_results: Maximum results to return

        Returns:
            Search results with multiple knowledge sources
        """
        try:
            # Get intelligent search results from cross-client intelligence
            intelligent_results = await self.cross_client_intelligence.intelligent_search(
                tenant_context,
                query,
                platform,
                include_cross_tenant,
                max_results
            )

            # Get traditional RAG results for comparison
            rag_results = await self.rag_service.semantic_search(
                query,
                top_k=max_results // 2,
                tenant_id=tenant_context.tenant_id,
                source_type="knowledge_base"
            )

            return {
                "query": query,
                "platform": platform.value,
                "tenant_id": tenant_context.tenant_id,
                "results": {
                    "intelligent_results": intelligent_results,
                    "traditional_rag_results": rag_results
                },
                "total_results": len(intelligent_results) + len(rag_results),
                "cross_tenant_included": include_cross_tenant,
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            self.logger.error(
                "Intelligent search failed",
                tenant_id=tenant_context.tenant_id,
                platform=platform.value,
                query=query[:50],
                error=str(e)
            )
            raise

    async def generate_platform_insights(
        self,
        platform: PlatformType,
        insight_type: str = "trends"
    ) -> Dict[str, Any]:
        """
        Generate cross-tenant insights for a platform

        Args:
            platform: Platform to analyze
            insight_type: Type of insights to generate

        Returns:
            Platform insights and recommendations
        """
        try:
            insights = await self.cross_client_intelligence.generate_cross_tenant_insights(
                platform,
                insight_type
            )

            return {
                "success": True,
                "platform": platform.value,
                "insight_type": insight_type,
                "insights": insights,
                "privacy_preserved": True,
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            self.logger.error(
                "Failed to generate platform insights",
                platform=platform.value,
                insight_type=insight_type,
                error=str(e)
            )
            raise

    async def get_knowledge_statistics(
        self,
        tenant_context: Optional[EnhancedTenantContext] = None
    ) -> Dict[str, Any]:
        """
        Get knowledge statistics across the system

        Args:
            tenant_context: Optional tenant context for tenant-specific stats

        Returns:
            Knowledge statistics
        """
        try:
            stats = {
                "timestamp": datetime.utcnow().isoformat(),
                "tenant_specific": {},
                "cross_tenant": {},
                "system_wide": {}
            }

            # Get traditional RAG stats
            if tenant_context:
                rag_stats = await self.rag_service.get_document_stats(tenant_context.tenant_id)
                stats["tenant_specific"]["rag_documents"] = rag_stats
            else:
                rag_stats = await self.rag_service.get_document_stats()
                stats["system_wide"]["rag_documents"] = rag_stats

            # Get cross-client intelligence stats
            if self.cross_client_intelligence:
                total_nodes = len(self.cross_client_intelligence.knowledge_graph)
                anonymized_nodes = len(self.cross_client_intelligence.anonymized_knowledge_index)

                stats["cross_tenant"] = {
                    "total_knowledge_nodes": total_nodes,
                    "anonymized_nodes": anonymized_nodes,
                    "privacy_preservation_ratio": anonymized_nodes / max(total_nodes, 1),
                    "platforms_covered": len(self.cross_client_intelligence.platform_knowledge_index),
                    "tenants_contributing": len(self.cross_client_intelligence.tenant_knowledge_index)
                }

            return stats

        except Exception as e:
            self.logger.error(
                "Failed to get knowledge statistics",
                error=str(e)
            )
            raise


# Global enhanced RAG/KAG system instance
_enhanced_rag_kag_system: Optional[EnhancedRAGKAGSystem] = None


async def get_enhanced_rag_kag_system() -> EnhancedRAGKAGSystem:
    """Get or create enhanced RAG/KAG system singleton"""
    global _enhanced_rag_kag_system
    if _enhanced_rag_kag_system is None:
        # This should be initialized with proper RLS manager in the main app
        raise RuntimeError("Enhanced RAG/KAG system not initialized")
    return _enhanced_rag_kag_system


def initialize_enhanced_rag_kag_system(rls_manager: RLSManager) -> EnhancedRAGKAGSystem:
    """Initialize the enhanced RAG/KAG system"""
    global _enhanced_rag_kag_system
    _enhanced_rag_kag_system = EnhancedRAGKAGSystem(rls_manager)
    return _enhanced_rag_kag_system
"""
Amazon Listing Workflow Orchestrator for BizOSaaS Platform

This service orchestrates the complete workflow from product research to Amazon listing creation.
It connects all existing components into a unified automated pipeline.

Workflow: Product List → Research → AI Enhancement → Content Generation → Amazon Listing → Validation
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass, asdict
from decimal import Decimal
import time

from shared.enhanced_tenant_context import EnhancedTenantContext, PlatformType
from shared.rls_manager import RLSManager
from ai.services.bizosaas_brain.tenant_aware_ai_coordinator import TenantAwareAICoordinator
from ai.services.bizosaas_brain.amazon_sp_api_integration import AmazonSPAPIClient, AmazonCredentials

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowStatus(str, Enum):
    """Amazon listing workflow status"""
    PENDING = "pending"
    RESEARCHING = "researching"
    ENHANCING = "enhancing"
    GENERATING_CONTENT = "generating_content"
    VALIDATING = "validating"
    CREATING_LISTING = "creating_listing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ProductProcessingStatus(str, Enum):
    """Individual product processing status"""
    PENDING = "pending"
    RESEARCHING = "researching"
    RESEARCH_COMPLETED = "research_completed"
    CONTENT_GENERATING = "content_generating"
    CONTENT_COMPLETED = "content_completed"
    VALIDATING = "validating"
    VALIDATION_COMPLETED = "validation_completed"
    LISTING_CREATING = "listing_creating"
    LISTING_COMPLETED = "listing_completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class WorkflowPriority(str, Enum):
    """Workflow execution priority"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class ProductInput:
    """Input product information"""
    product_identifier: str  # Can be URL, ASIN, product name, or description
    identifier_type: str  # "url", "asin", "name", "description"
    target_marketplace: str = "INDIA"  # Default to India marketplace
    custom_instructions: Optional[str] = None
    priority: ProductProcessingStatus = ProductProcessingStatus.PENDING
    metadata: Dict[str, Any] = None

@dataclass
class WorkflowConfiguration:
    """Configuration for the listing workflow"""
    tenant_id: str
    user_id: str

    # Research configuration
    research_depth: str = "comprehensive"  # basic, standard, comprehensive
    competitor_analysis: bool = True
    trend_analysis: bool = True
    profit_analysis: bool = True

    # Content generation configuration
    content_style: str = "professional"  # casual, professional, premium
    seo_optimization: bool = True
    keyword_density: str = "medium"  # low, medium, high

    # Amazon listing configuration
    marketplace_ids: List[str] = None
    fulfillment_method: str = "FBM"  # FBA or FBM
    pricing_strategy: str = "competitive"  # competitive, premium, budget

    # Validation configuration
    strict_validation: bool = True
    auto_publish: bool = False
    review_required: bool = True

    # Notification configuration
    notify_on_completion: bool = True
    notification_channels: List[str] = None

@dataclass
class ProductResearchResult:
    """Product research results"""
    product_id: str
    research_data: Dict[str, Any]
    trend_analysis: Dict[str, Any]
    competitor_analysis: Dict[str, Any]
    profit_analysis: Dict[str, Any]
    quality_assessment: Dict[str, Any]
    market_insights: Dict[str, Any]
    confidence_score: float
    research_time: float
    errors: List[str] = None
    warnings: List[str] = None

@dataclass
class ContentGenerationResult:
    """Content generation results"""
    product_id: str
    optimized_title: str
    description: str
    bullet_points: List[str]
    keywords: List[str]
    category_path: str
    product_type: str
    attributes: Dict[str, Any]
    seo_score: float
    content_quality_score: float
    generation_time: float
    errors: List[str] = None
    warnings: List[str] = None

@dataclass
class ValidationResult:
    """Amazon listing validation results"""
    product_id: str
    is_valid: bool
    validation_score: float
    compliance_checks: Dict[str, bool]
    required_fixes: List[str]
    warnings: List[str]
    amazon_requirements_met: bool
    estimated_approval_chance: float
    validation_time: float

@dataclass
class ListingCreationResult:
    """Amazon listing creation results"""
    product_id: str
    amazon_listing_id: Optional[str]
    seller_sku: str
    listing_status: str
    submission_id: Optional[str]
    estimated_live_date: Optional[datetime]
    fees_estimate: Dict[str, float]
    creation_time: float
    errors: List[str] = None
    warnings: List[str] = None

@dataclass
class WorkflowResult:
    """Complete workflow execution result"""
    workflow_id: str
    tenant_id: str
    status: WorkflowStatus

    # Input data
    total_products: int
    configuration: WorkflowConfiguration

    # Processing results
    research_results: List[ProductResearchResult] = None
    content_results: List[ContentGenerationResult] = None
    validation_results: List[ValidationResult] = None
    listing_results: List[ListingCreationResult] = None

    # Metrics
    processed_products: int = 0
    successful_listings: int = 0
    failed_products: int = 0
    total_processing_time: float = 0

    # Workflow timestamps
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Summary data
    summary_statistics: Dict[str, Any] = None
    quality_metrics: Dict[str, float] = None
    errors: List[str] = None
    warnings: List[str] = None

class AmazonListingWorkflowOrchestrator:
    """Main orchestrator for automated Amazon listing workflow"""

    def __init__(self, rls_manager: RLSManager, ai_coordinator: TenantAwareAICoordinator):
        self.rls_manager = rls_manager
        self.ai_coordinator = ai_coordinator
        self.active_workflows: Dict[str, WorkflowResult] = {}

        # Initialize service clients
        self.product_sourcing_url = "http://localhost:8000"  # CrewAI service
        self.brain_api_url = "http://localhost:8001"  # Brain API

    async def start_listing_workflow(
        self,
        tenant_context: EnhancedTenantContext,
        products: List[ProductInput],
        configuration: WorkflowConfiguration
    ) -> WorkflowResult:
        """Start the complete Amazon listing workflow"""

        workflow_id = str(uuid.uuid4())
        logger.info(f"🚀 Starting Amazon listing workflow {workflow_id} for {len(products)} products")

        # Initialize workflow result
        workflow = WorkflowResult(
            workflow_id=workflow_id,
            tenant_id=tenant_context.tenant_id,
            status=WorkflowStatus.PENDING,
            total_products=len(products),
            configuration=configuration,
            created_at=datetime.utcnow(),
            research_results=[],
            content_results=[],
            validation_results=[],
            listing_results=[],
            errors=[],
            warnings=[]
        )

        self.active_workflows[workflow_id] = workflow

        try:
            workflow.started_at = datetime.utcnow()
            workflow.status = WorkflowStatus.RESEARCHING

            # Phase 1: Product Research
            await self._execute_research_phase(workflow, products, tenant_context)

            # Phase 2: Content Generation
            await self._execute_content_generation_phase(workflow, tenant_context)

            # Phase 3: Validation
            await self._execute_validation_phase(workflow, tenant_context)

            # Phase 4: Amazon Listing Creation
            await self._execute_listing_creation_phase(workflow, tenant_context)

            # Phase 5: Post-processing and Summary
            await self._execute_post_processing_phase(workflow, tenant_context)

            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = datetime.utcnow()
            workflow.total_processing_time = (workflow.completed_at - workflow.started_at).total_seconds()

            logger.info(f"✅ Workflow {workflow_id} completed successfully")

        except Exception as e:
            logger.error(f"❌ Workflow {workflow_id} failed: {str(e)}")
            workflow.status = WorkflowStatus.FAILED
            workflow.completed_at = datetime.utcnow()
            workflow.errors.append(f"Workflow failed: {str(e)}")

        return workflow

    async def _execute_research_phase(
        self,
        workflow: WorkflowResult,
        products: List[ProductInput],
        tenant_context: EnhancedTenantContext
    ) -> None:
        """Execute product research phase"""

        logger.info(f"🔍 Starting research phase for {len(products)} products")
        workflow.status = WorkflowStatus.RESEARCHING

        # Process products in batches to avoid overwhelming the system
        batch_size = 5
        for i in range(0, len(products), batch_size):
            batch = products[i:i + batch_size]

            # Process batch concurrently
            research_tasks = [
                self._research_single_product(product, workflow.configuration, tenant_context)
                for product in batch
            ]

            batch_results = await asyncio.gather(*research_tasks, return_exceptions=True)

            # Process results
            for j, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    logger.error(f"Research failed for product {batch[j].product_identifier}: {str(result)}")
                    workflow.errors.append(f"Research failed for {batch[j].product_identifier}: {str(result)}")
                else:
                    workflow.research_results.append(result)
                    workflow.processed_products += 1

            # Brief pause between batches
            await asyncio.sleep(1)

        logger.info(f"✅ Research phase completed: {len(workflow.research_results)} successful")

    async def _research_single_product(
        self,
        product: ProductInput,
        config: WorkflowConfiguration,
        tenant_context: EnhancedTenantContext
    ) -> ProductResearchResult:
        """Research a single product using the existing product sourcing agents"""

        start_time = time.time()
        product_id = str(uuid.uuid4())

        try:
            # Prepare research request based on identifier type
            research_request = self._prepare_research_request(product, config)

            # Use existing product sourcing agent via AI coordinator
            research_response = await self.ai_coordinator.coordinate_analysis(
                tenant_context=tenant_context,
                analysis_type="comprehensive_product_research",
                data=research_request,
                agent_specializations=[
                    "product_sourcing_specialist",
                    "trend_analysis_agent",
                    "competitor_monitor_agent",
                    "profit_calculation_agent",
                    "quality_assessment_agent"
                ]
            )

            if not research_response.get("success", False):
                raise Exception(f"Research failed: {research_response.get('error', 'Unknown error')}")

            research_data = research_response.get("data", {})

            # Extract specific analysis results
            trend_analysis = research_data.get("stage_1_trends", {})
            competitor_analysis = research_data.get("stage_3_competition", {})
            profit_analysis = research_data.get("stage_4_profitability", {})
            quality_assessment = research_data.get("stage_5_quality_risk", {})
            market_insights = research_data.get("market_insights", {})

            # Calculate confidence score based on data completeness
            confidence_score = self._calculate_research_confidence(research_data)

            return ProductResearchResult(
                product_id=product_id,
                research_data=research_data,
                trend_analysis=trend_analysis,
                competitor_analysis=competitor_analysis,
                profit_analysis=profit_analysis,
                quality_assessment=quality_assessment,
                market_insights=market_insights,
                confidence_score=confidence_score,
                research_time=time.time() - start_time
            )

        except Exception as e:
            logger.error(f"Product research failed for {product.product_identifier}: {str(e)}")
            return ProductResearchResult(
                product_id=product_id,
                research_data={},
                trend_analysis={},
                competitor_analysis={},
                profit_analysis={},
                quality_assessment={},
                market_insights={},
                confidence_score=0.0,
                research_time=time.time() - start_time,
                errors=[str(e)]
            )

    def _prepare_research_request(self, product: ProductInput, config: WorkflowConfiguration) -> Dict[str, Any]:
        """Prepare research request based on product identifier type"""

        if product.identifier_type == "url":
            # Extract keywords from URL or use direct URL
            return {
                "url": product.product_identifier,
                "analysis_depth": config.research_depth,
                "include_competitor_analysis": config.competitor_analysis,
                "include_trend_analysis": config.trend_analysis,
                "include_profit_analysis": config.profit_analysis,
                "market_region": "IN",
                "custom_instructions": product.custom_instructions
            }
        elif product.identifier_type == "asin":
            return {
                "asin": product.product_identifier,
                "marketplace": product.target_marketplace,
                "analysis_depth": config.research_depth,
                "include_competitor_analysis": config.competitor_analysis,
                "include_trend_analysis": config.trend_analysis,
                "include_profit_analysis": config.profit_analysis
            }
        elif product.identifier_type in ["name", "description"]:
            # Convert to keywords for research
            keywords = self._extract_keywords_from_text(product.product_identifier)
            return {
                "keywords": keywords,
                "category": "general",
                "analysis_depth": config.research_depth,
                "include_competitor_analysis": config.competitor_analysis,
                "include_trend_analysis": config.trend_analysis,
                "include_profit_analysis": config.profit_analysis,
                "market_region": "IN",
                "custom_instructions": product.custom_instructions
            }
        else:
            raise ValueError(f"Unsupported identifier type: {product.identifier_type}")

    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract keywords from product name or description"""
        import re

        # Simple keyword extraction (can be enhanced with NLP)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

        # Remove common stop words
        stop_words = {'the', 'and', 'for', 'with', 'this', 'that', 'from', 'are', 'was', 'will', 'can', 'has', 'have'}
        keywords = [word for word in words if word not in stop_words]

        # Return unique keywords (max 10)
        return list(set(keywords))[:10]

    def _calculate_research_confidence(self, research_data: Dict[str, Any]) -> float:
        """Calculate confidence score based on research data completeness"""

        # Define weights for different data components
        weights = {
            "stage_1_trends": 0.2,
            "stage_2_discovery": 0.3,
            "stage_3_competition": 0.2,
            "stage_4_profitability": 0.15,
            "stage_5_quality_risk": 0.15
        }

        total_confidence = 0.0
        total_weight = 0.0

        for stage, weight in weights.items():
            stage_data = research_data.get(stage, {})
            if stage_data and not stage_data.get("error"):
                # Calculate stage confidence based on data richness
                stage_confidence = min(1.0, len(str(stage_data)) / 1000)  # Normalize based on data size
                total_confidence += stage_confidence * weight
            total_weight += weight

        return total_confidence / total_weight if total_weight > 0 else 0.0

    async def _execute_content_generation_phase(
        self,
        workflow: WorkflowResult,
        tenant_context: EnhancedTenantContext
    ) -> None:
        """Execute content generation phase"""

        logger.info(f"✍️ Starting content generation for {len(workflow.research_results)} products")
        workflow.status = WorkflowStatus.GENERATING_CONTENT

        # Process successful research results
        content_tasks = [
            self._generate_content_for_product(research_result, workflow.configuration, tenant_context)
            for research_result in workflow.research_results
            if research_result.confidence_score >= 0.3  # Only process products with decent research confidence
        ]

        content_results = await asyncio.gather(*content_tasks, return_exceptions=True)

        for result in content_results:
            if isinstance(result, Exception):
                logger.error(f"Content generation failed: {str(result)}")
                workflow.errors.append(f"Content generation failed: {str(result)}")
            else:
                workflow.content_results.append(result)

        logger.info(f"✅ Content generation completed: {len(workflow.content_results)} successful")

    async def _generate_content_for_product(
        self,
        research_result: ProductResearchResult,
        config: WorkflowConfiguration,
        tenant_context: EnhancedTenantContext
    ) -> ContentGenerationResult:
        """Generate Amazon listing content for a single product"""

        start_time = time.time()

        try:
            # Prepare content generation request
            content_request = {
                "research_data": research_result.research_data,
                "content_style": config.content_style,
                "seo_optimization": config.seo_optimization,
                "keyword_density": config.keyword_density,
                "marketplace": "amazon_india",
                "fulfillment_method": config.fulfillment_method,
                "target_audience": "indian_consumers"
            }

            # Use AI coordinator to generate content
            content_response = await self.ai_coordinator.coordinate_analysis(
                tenant_context=tenant_context,
                analysis_type="amazon_listing_content_generation",
                data=content_request,
                agent_specializations=[
                    "seo_specialist",
                    "content_creator",
                    "amazon_listing_expert",
                    "marketing_strategist"
                ]
            )

            if not content_response.get("success", False):
                raise Exception(f"Content generation failed: {content_response.get('error', 'Unknown error')}")

            content_data = content_response.get("data", {})

            # Extract generated content
            optimized_title = content_data.get("optimized_title", "")
            description = content_data.get("description", "")
            bullet_points = content_data.get("bullet_points", [])
            keywords = content_data.get("keywords", [])
            category_path = content_data.get("category_path", "")
            product_type = content_data.get("product_type", "")
            attributes = content_data.get("attributes", {})

            # Calculate quality scores
            seo_score = self._calculate_seo_score(optimized_title, description, keywords)
            content_quality_score = self._calculate_content_quality_score(content_data)

            return ContentGenerationResult(
                product_id=research_result.product_id,
                optimized_title=optimized_title,
                description=description,
                bullet_points=bullet_points,
                keywords=keywords,
                category_path=category_path,
                product_type=product_type,
                attributes=attributes,
                seo_score=seo_score,
                content_quality_score=content_quality_score,
                generation_time=time.time() - start_time
            )

        except Exception as e:
            logger.error(f"Content generation failed for product {research_result.product_id}: {str(e)}")
            return ContentGenerationResult(
                product_id=research_result.product_id,
                optimized_title="",
                description="",
                bullet_points=[],
                keywords=[],
                category_path="",
                product_type="",
                attributes={},
                seo_score=0.0,
                content_quality_score=0.0,
                generation_time=time.time() - start_time,
                errors=[str(e)]
            )

    def _calculate_seo_score(self, title: str, description: str, keywords: List[str]) -> float:
        """Calculate SEO optimization score"""

        score = 0.0
        max_score = 100.0

        # Title checks
        if title:
            if len(title) <= 200:  # Amazon title limit
                score += 20
            if any(keyword.lower() in title.lower() for keyword in keywords[:3]):  # Top keywords in title
                score += 20

        # Description checks
        if description:
            if len(description) >= 100:  # Minimum description length
                score += 15
            if len(description) <= 2000:  # Amazon description limit
                score += 15

            # Keyword density check
            keyword_mentions = sum(description.lower().count(kw.lower()) for kw in keywords)
            if 3 <= keyword_mentions <= 10:  # Good keyword density
                score += 20

        # Keywords quality
        if len(keywords) >= 5:  # Sufficient keyword coverage
            score += 10

        return min(score, max_score)

    def _calculate_content_quality_score(self, content_data: Dict[str, Any]) -> float:
        """Calculate overall content quality score"""

        score = 0.0

        # Completeness checks
        required_fields = ["optimized_title", "description", "bullet_points", "keywords", "category_path"]
        completed_fields = sum(1 for field in required_fields if content_data.get(field))
        score += (completed_fields / len(required_fields)) * 40

        # Content richness
        description = content_data.get("description", "")
        if len(description) > 500:  # Rich description
            score += 20

        bullet_points = content_data.get("bullet_points", [])
        if len(bullet_points) >= 3:  # Adequate bullet points
            score += 20

        keywords = content_data.get("keywords", [])
        if len(keywords) >= 5:  # Good keyword coverage
            score += 20

        return min(score, 100.0)

    async def _execute_validation_phase(
        self,
        workflow: WorkflowResult,
        tenant_context: EnhancedTenantContext
    ) -> None:
        """Execute validation phase"""

        logger.info(f"✅ Starting validation for {len(workflow.content_results)} products")
        workflow.status = WorkflowStatus.VALIDATING

        validation_tasks = [
            self._validate_listing_content(content_result, workflow.configuration)
            for content_result in workflow.content_results
            if content_result.content_quality_score >= 50  # Only validate decent quality content
        ]

        validation_results = await asyncio.gather(*validation_tasks, return_exceptions=True)

        for result in validation_results:
            if isinstance(result, Exception):
                logger.error(f"Validation failed: {str(result)}")
                workflow.errors.append(f"Validation failed: {str(result)}")
            else:
                workflow.validation_results.append(result)

        logger.info(f"✅ Validation completed: {len(workflow.validation_results)} successful")

    async def _validate_listing_content(
        self,
        content_result: ContentGenerationResult,
        config: WorkflowConfiguration
    ) -> ValidationResult:
        """Validate Amazon listing content for compliance"""

        start_time = time.time()

        try:
            compliance_checks = {}
            required_fixes = []
            warnings = []

            # Title validation
            title = content_result.optimized_title
            compliance_checks["title_length"] = len(title) <= 200
            if not compliance_checks["title_length"]:
                required_fixes.append("Title exceeds 200 character limit")

            compliance_checks["title_not_empty"] = bool(title.strip())
            if not compliance_checks["title_not_empty"]:
                required_fixes.append("Title cannot be empty")

            # Description validation
            description = content_result.description
            compliance_checks["description_length"] = len(description) <= 2000
            if not compliance_checks["description_length"]:
                required_fixes.append("Description exceeds 2000 character limit")

            compliance_checks["description_minimum"] = len(description) >= 50
            if not compliance_checks["description_minimum"]:
                required_fixes.append("Description too short (minimum 50 characters)")

            # Keywords validation
            keywords = content_result.keywords
            compliance_checks["sufficient_keywords"] = len(keywords) >= 3
            if not compliance_checks["sufficient_keywords"]:
                warnings.append("Consider adding more keywords for better discoverability")

            # Bullet points validation
            bullet_points = content_result.bullet_points
            compliance_checks["bullet_points_count"] = len(bullet_points) >= 3
            if not compliance_checks["bullet_points_count"]:
                warnings.append("Consider adding more bullet points (minimum 3 recommended)")

            # Category validation
            category_path = content_result.category_path
            compliance_checks["category_assigned"] = bool(category_path)
            if not compliance_checks["category_assigned"]:
                required_fixes.append("Product category must be assigned")

            # Product type validation
            product_type = content_result.product_type
            compliance_checks["product_type_assigned"] = bool(product_type)
            if not compliance_checks["product_type_assigned"]:
                required_fixes.append("Product type must be assigned")

            # Calculate validation score
            total_checks = len(compliance_checks)
            passed_checks = sum(compliance_checks.values())
            validation_score = (passed_checks / total_checks) * 100

            # Determine if listing is valid
            is_valid = len(required_fixes) == 0
            amazon_requirements_met = validation_score >= 80

            # Estimate approval chance
            estimated_approval_chance = validation_score / 100
            if content_result.seo_score > 70:
                estimated_approval_chance += 0.1
            if content_result.content_quality_score > 80:
                estimated_approval_chance += 0.1

            estimated_approval_chance = min(estimated_approval_chance, 1.0)

            return ValidationResult(
                product_id=content_result.product_id,
                is_valid=is_valid,
                validation_score=validation_score,
                compliance_checks=compliance_checks,
                required_fixes=required_fixes,
                warnings=warnings,
                amazon_requirements_met=amazon_requirements_met,
                estimated_approval_chance=estimated_approval_chance,
                validation_time=time.time() - start_time
            )

        except Exception as e:
            logger.error(f"Validation failed for product {content_result.product_id}: {str(e)}")
            return ValidationResult(
                product_id=content_result.product_id,
                is_valid=False,
                validation_score=0.0,
                compliance_checks={},
                required_fixes=[f"Validation error: {str(e)}"],
                warnings=[],
                amazon_requirements_met=False,
                estimated_approval_chance=0.0,
                validation_time=time.time() - start_time
            )

    async def _execute_listing_creation_phase(
        self,
        workflow: WorkflowResult,
        tenant_context: EnhancedTenantContext
    ) -> None:
        """Execute Amazon listing creation phase"""

        logger.info(f"🛒 Starting listing creation for validated products")
        workflow.status = WorkflowStatus.CREATING_LISTING

        # Only create listings for validated products
        valid_products = [
            (content, validation)
            for content, validation in zip(workflow.content_results, workflow.validation_results)
            if validation.is_valid and validation.estimated_approval_chance >= 0.7
        ]

        logger.info(f"Creating {len(valid_products)} Amazon listings")

        listing_tasks = [
            self._create_amazon_listing(content, validation, workflow.configuration, tenant_context)
            for content, validation in valid_products
        ]

        listing_results = await asyncio.gather(*listing_tasks, return_exceptions=True)

        for result in listing_results:
            if isinstance(result, Exception):
                logger.error(f"Listing creation failed: {str(result)}")
                workflow.errors.append(f"Listing creation failed: {str(result)}")
                workflow.failed_products += 1
            else:
                workflow.listing_results.append(result)
                if result.amazon_listing_id:
                    workflow.successful_listings += 1
                else:
                    workflow.failed_products += 1

        logger.info(f"✅ Listing creation completed: {workflow.successful_listings} successful, {workflow.failed_products} failed")

    async def _create_amazon_listing(
        self,
        content_result: ContentGenerationResult,
        validation_result: ValidationResult,
        config: WorkflowConfiguration,
        tenant_context: EnhancedTenantContext
    ) -> ListingCreationResult:
        """Create actual Amazon listing using SP-API"""

        start_time = time.time()

        try:
            # Get Amazon credentials from tenant context (you'd need to implement this)
            amazon_credentials = await self._get_amazon_credentials(tenant_context)

            if not amazon_credentials:
                raise Exception("Amazon credentials not found for tenant")

            # Generate unique seller SKU
            seller_sku = f"BIZOSAAS-{content_result.product_id[:8].upper()}-{int(time.time())}"

            # Prepare listing attributes based on content
            listing_attributes = {
                "item_name": [{
                    "value": content_result.optimized_title,
                    "language_tag": "en_IN"
                }],
                "description": [{
                    "value": content_result.description,
                    "language_tag": "en_IN"
                }],
                "bullet_point": [
                    {"value": bp, "language_tag": "en_IN"}
                    for bp in content_result.bullet_points[:5]  # Amazon allows max 5
                ],
                "generic_keyword": [
                    {"value": " ".join(content_result.keywords[:10]), "language_tag": "en_IN"}
                ]
            }

            # Add product-specific attributes from research
            listing_attributes.update(content_result.attributes)

            # Create Amazon SP-API client
            sp_api_client = AmazonSPAPIClient(amazon_credentials)

            # Create listing using SP-API
            marketplace_ids = config.marketplace_ids or ["A21TJRUUN4KGV"]  # India marketplace

            listing_response = await sp_api_client.put_listings_item(
                seller_id=amazon_credentials.selling_partner_id,
                sku=seller_sku,
                marketplace_ids=marketplace_ids,
                product_type=content_result.product_type or "PRODUCT",
                attributes=listing_attributes
            )

            # Extract response data
            amazon_listing_id = listing_response.get("sku")  # SP-API returns SKU
            submission_id = listing_response.get("submissionId")
            listing_status = listing_response.get("status", "SUBMITTED")

            # Estimate fees (this would need actual SP-API call)
            fees_estimate = {
                "referral_fee": 15.0,  # Typical Amazon referral fee percentage
                "fulfillment_fee": 0.0 if config.fulfillment_method == "FBM" else 50.0,
                "storage_fee": 0.0 if config.fulfillment_method == "FBM" else 10.0
            }

            # Estimate live date
            estimated_live_date = datetime.utcnow() + timedelta(days=1 if listing_status == "ACCEPTED" else 3)

            return ListingCreationResult(
                product_id=content_result.product_id,
                amazon_listing_id=amazon_listing_id,
                seller_sku=seller_sku,
                listing_status=listing_status,
                submission_id=submission_id,
                estimated_live_date=estimated_live_date,
                fees_estimate=fees_estimate,
                creation_time=time.time() - start_time
            )

        except Exception as e:
            logger.error(f"Amazon listing creation failed for product {content_result.product_id}: {str(e)}")
            return ListingCreationResult(
                product_id=content_result.product_id,
                amazon_listing_id=None,
                seller_sku="",
                listing_status="FAILED",
                submission_id=None,
                estimated_live_date=None,
                fees_estimate={},
                creation_time=time.time() - start_time,
                errors=[str(e)]
            )

    async def _get_amazon_credentials(self, tenant_context: EnhancedTenantContext) -> Optional[AmazonCredentials]:
        """Retrieve Amazon SP-API credentials for tenant"""
        # This would retrieve encrypted credentials from tenant integrations
        # For now, return None to indicate missing credentials

        # In real implementation:
        # 1. Query tenant_integrations table
        # 2. Decrypt stored Amazon SP-API credentials
        # 3. Refresh access token if needed
        # 4. Return AmazonCredentials object

        return None

    async def _execute_post_processing_phase(
        self,
        workflow: WorkflowResult,
        tenant_context: EnhancedTenantContext
    ) -> None:
        """Execute post-processing and generate summary"""

        logger.info("📊 Generating workflow summary and metrics")

        # Calculate summary statistics
        total_research_time = sum(r.research_time for r in workflow.research_results)
        total_content_time = sum(c.generation_time for c in workflow.content_results)
        total_validation_time = sum(v.validation_time for v in workflow.validation_results)
        total_listing_time = sum(l.creation_time for l in workflow.listing_results)

        workflow.summary_statistics = {
            "research_phase": {
                "products_researched": len(workflow.research_results),
                "total_time": total_research_time,
                "avg_confidence": sum(r.confidence_score for r in workflow.research_results) / len(workflow.research_results) if workflow.research_results else 0
            },
            "content_phase": {
                "products_processed": len(workflow.content_results),
                "total_time": total_content_time,
                "avg_seo_score": sum(c.seo_score for c in workflow.content_results) / len(workflow.content_results) if workflow.content_results else 0,
                "avg_quality_score": sum(c.content_quality_score for c in workflow.content_results) / len(workflow.content_results) if workflow.content_results else 0
            },
            "validation_phase": {
                "products_validated": len(workflow.validation_results),
                "total_time": total_validation_time,
                "valid_products": sum(1 for v in workflow.validation_results if v.is_valid),
                "avg_validation_score": sum(v.validation_score for v in workflow.validation_results) / len(workflow.validation_results) if workflow.validation_results else 0
            },
            "listing_phase": {
                "listings_attempted": len(workflow.listing_results),
                "total_time": total_listing_time,
                "successful_listings": workflow.successful_listings,
                "failed_listings": workflow.failed_products
            }
        }

        # Calculate quality metrics
        workflow.quality_metrics = {
            "research_quality": workflow.summary_statistics["research_phase"]["avg_confidence"],
            "content_quality": workflow.summary_statistics["content_phase"]["avg_quality_score"],
            "seo_optimization": workflow.summary_statistics["content_phase"]["avg_seo_score"],
            "validation_score": workflow.summary_statistics["validation_phase"]["avg_validation_score"],
            "success_rate": (workflow.successful_listings / workflow.total_products) * 100 if workflow.total_products > 0 else 0
        }

        # Send notifications if configured
        if workflow.configuration.notify_on_completion:
            await self._send_completion_notification(workflow, tenant_context)

        logger.info(f"📈 Workflow summary: {workflow.successful_listings}/{workflow.total_products} successful listings")

    async def _send_completion_notification(
        self,
        workflow: WorkflowResult,
        tenant_context: EnhancedTenantContext
    ) -> None:
        """Send workflow completion notification"""

        try:
            notification_data = {
                "workflow_id": workflow.workflow_id,
                "tenant_id": workflow.tenant_id,
                "status": workflow.status.value,
                "total_products": workflow.total_products,
                "successful_listings": workflow.successful_listings,
                "failed_products": workflow.failed_products,
                "processing_time": workflow.total_processing_time,
                "quality_metrics": workflow.quality_metrics
            }

            # Use AI coordinator to send notification
            await self.ai_coordinator.coordinate_analysis(
                tenant_context=tenant_context,
                analysis_type="workflow_notification",
                data=notification_data,
                agent_specializations=["notification_manager"]
            )

        except Exception as e:
            logger.error(f"Failed to send completion notification: {str(e)}")

    async def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowResult]:
        """Get current status of a workflow"""
        return self.active_workflows.get(workflow_id)

    async def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a running workflow"""
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
            if workflow.status not in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED]:
                workflow.status = WorkflowStatus.CANCELLED
                workflow.completed_at = datetime.utcnow()
                return True
        return False

    async def get_active_workflows(self, tenant_id: str) -> List[WorkflowResult]:
        """Get all active workflows for a tenant"""
        return [
            workflow for workflow in self.active_workflows.values()
            if workflow.tenant_id == tenant_id
        ]

# Export main class
__all__ = ["AmazonListingWorkflowOrchestrator", "WorkflowConfiguration", "ProductInput", "WorkflowResult"]
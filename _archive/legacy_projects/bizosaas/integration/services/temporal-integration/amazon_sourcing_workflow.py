"""
Amazon Product Sourcing Workflow using Temporal
Comprehensive workflow for sourcing products from Amazon and creating them in Saleor
Integrated with BizOSaaS platform infrastructure
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from dataclasses import dataclass, asdict
from decimal import Decimal
import re
import httpx
import hashlib

# Temporal imports (mock for now, ready for production)
try:
    from temporalio import activity, workflow
    from temporalio.workflow import info
    from temporalio.common import RetryPolicy, SearchAttributeKey
    TEMPORAL_AVAILABLE = True
except ImportError:
    # Mock decorators for development
    def activity(fn): return fn
    def workflow(fn): return fn
    class info:
        workflow_id = "mock_workflow_id"
    TEMPORAL_AVAILABLE = False

from temporal_client import TemporalClient, WorkflowType, WorkflowStatus, WorkflowRequest, WorkflowResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AmazonSourcingStatus(str, Enum):
    """Amazon sourcing workflow status"""
    PENDING = "pending"
    EXTRACTING_DATA = "extracting_data"
    ENHANCING_WITH_AI = "enhancing_with_ai"
    CREATING_SALEOR_PRODUCT = "creating_saleor_product"
    PROCESSING_IMAGES = "processing_images"
    VALIDATING_PRODUCT = "validating_product"
    NOTIFYING_COMPLETION = "notifying_completion"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AmazonSourcingError(str, Enum):
    """Error types for Amazon sourcing"""
    INVALID_AMAZON_URL = "invalid_amazon_url"
    PRODUCT_NOT_FOUND = "product_not_found"
    AI_ENHANCEMENT_FAILED = "ai_enhancement_failed"
    SALEOR_CREATION_FAILED = "saleor_creation_failed"
    IMAGE_PROCESSING_FAILED = "image_processing_failed"
    VALIDATION_FAILED = "validation_failed"
    TIMEOUT_ERROR = "timeout_error"
    NETWORK_ERROR = "network_error"

@dataclass
class AmazonProductData:
    """Extracted Amazon product data"""
    asin: str
    title: str
    description: str
    price: Optional[Decimal] = None
    images: List[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    features: List[str] = None
    specifications: Dict[str, Any] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    availability: Optional[str] = None
    variants: List[Dict[str, Any]] = None

@dataclass
class AIEnhancementResult:
    """AI enhancement results"""
    optimized_title: str
    seo_description: str
    product_tags: List[str]
    category_suggestions: List[str]
    pricing_recommendations: Dict[str, Any]
    competitor_analysis: Dict[str, Any]
    content_enhancements: Dict[str, Any]

@dataclass
class SaleorProductData:
    """Saleor product creation data"""
    product_id: Optional[str] = None
    variant_ids: List[str] = None
    category_id: Optional[str] = None
    collection_ids: List[str] = None
    created_at: Optional[datetime] = None

@dataclass
class AmazonSourcingInput:
    """Input data for Amazon sourcing workflow"""
    amazon_url: str
    asin: Optional[str] = None
    tenant_id: str = None
    user_id: str = None
    store_config: Dict[str, Any] = None
    ai_enhancement_config: Dict[str, Any] = None
    pricing_rules: Dict[str, Any] = None
    category_mappings: Dict[str, str] = None
    notification_config: Dict[str, Any] = None

@dataclass
class AmazonSourcingOutput:
    """Output data from Amazon sourcing workflow"""
    workflow_id: str
    status: AmazonSourcingStatus
    amazon_data: Optional[AmazonProductData] = None
    ai_enhancements: Optional[AIEnhancementResult] = None
    saleor_product: Optional[SaleorProductData] = None
    processing_metrics: Dict[str, Any] = None
    quality_scores: Dict[str, float] = None
    errors: List[str] = None
    warnings: List[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class AmazonSourcingActivities:
    """Temporal activities for Amazon product sourcing"""
    
    def __init__(self):
        self.http_client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        self.saleor_client = httpx.AsyncClient(
            base_url="http://localhost:8024/graphql/",
            timeout=30.0
        )
        self.crewai_client = httpx.AsyncClient(
            base_url="http://localhost:8000",
            timeout=120.0
        )
    
    @activity
    async def extract_product_data_activity(self, amazon_input: Dict[str, Any]) -> Dict[str, Any]:
        """Extract product data from Amazon URL"""
        try:
            logger.info(f"🔍 Extracting product data from: {amazon_input['amazon_url']}")
            
            # Extract ASIN from URL
            asin = self._extract_asin_from_url(amazon_input['amazon_url'])
            if not asin:
                raise ValueError(f"Could not extract ASIN from URL: {amazon_input['amazon_url']}")
            
            # Scrape product data (using legal web scraping methods)
            product_data = await self._scrape_amazon_product_data(asin, amazon_input['amazon_url'])
            
            # Validate extracted data
            if not product_data.get('title'):
                raise ValueError("Failed to extract product title")
            
            logger.info(f"✅ Successfully extracted data for ASIN: {asin}")
            return {
                'status': 'success',
                'data': asdict(AmazonProductData(**product_data)),
                'asin': asin
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to extract product data: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'error_type': AmazonSourcingError.PRODUCT_NOT_FOUND
            }
    
    @activity
    async def enhance_with_ai_activity(self, product_data: Dict[str, Any], ai_config: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance product data using CrewAI agents"""
        try:
            logger.info(f"🤖 Enhancing product with AI: {product_data.get('title', 'Unknown')}")
            
            # Prepare CrewAI request
            enhancement_request = {
                "task_type": "product_enhancement",
                "product_data": product_data,
                "enhancement_config": ai_config,
                "agents": [
                    "product_sourcing_specialist",
                    "marketing_strategist",
                    "seo_specialist"
                ]
            }
            
            # Call CrewAI service
            response = await self.crewai_client.post(
                "/agents/product-enhancement",
                json=enhancement_request
            )
            response.raise_for_status()
            result = response.json()
            
            # Process AI enhancements
            enhancements = self._process_ai_enhancements(result)
            
            logger.info("✅ AI enhancement completed successfully")
            return {
                'status': 'success',
                'enhancements': asdict(enhancements)
            }
            
        except Exception as e:
            logger.error(f"❌ AI enhancement failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'error_type': AmazonSourcingError.AI_ENHANCEMENT_FAILED
            }
    
    @activity
    async def create_saleor_product_activity(self, product_data: Dict[str, Any], enhancements: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Create product in Saleor via GraphQL"""
        try:
            logger.info(f"🏪 Creating Saleor product: {enhancements.get('optimized_title', product_data.get('title'))}")
            
            # Prepare Saleor GraphQL mutation
            mutation = self._build_saleor_product_mutation(product_data, enhancements, config)
            
            # Execute GraphQL mutation
            response = await self.saleor_client.post(
                "/",
                json={"query": mutation}
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get('errors'):
                raise ValueError(f"GraphQL errors: {result['errors']}")
            
            # Extract created product data
            saleor_data = self._extract_saleor_product_data(result)
            
            logger.info(f"✅ Saleor product created successfully: {saleor_data.product_id}")
            return {
                'status': 'success',
                'saleor_product': asdict(saleor_data)
            }
            
        except Exception as e:
            logger.error(f"❌ Saleor product creation failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'error_type': AmazonSourcingError.SALEOR_CREATION_FAILED
            }
    
    @activity
    async def process_images_activity(self, images: List[str], product_id: str) -> Dict[str, Any]:
        """Download and optimize product images"""
        try:
            logger.info(f"🖼️ Processing {len(images)} product images")
            
            processed_images = []
            
            for idx, image_url in enumerate(images):
                try:
                    # Download image
                    image_response = await self.http_client.get(image_url)
                    image_response.raise_for_status()
                    
                    # Generate filename
                    filename = f"product_{product_id}_{idx}_{hashlib.md5(image_url.encode()).hexdigest()[:8]}.jpg"
                    
                    # Here you would typically:
                    # 1. Optimize image (resize, compress)
                    # 2. Upload to CDN/storage
                    # 3. Associate with Saleor product
                    
                    # For now, simulate successful processing
                    processed_images.append({
                        'original_url': image_url,
                        'processed_url': f"https://cdn.bizosaas.com/products/{filename}",
                        'filename': filename,
                        'size': len(image_response.content)
                    })
                    
                except Exception as img_error:
                    logger.warning(f"Failed to process image {image_url}: {img_error}")
            
            logger.info(f"✅ Successfully processed {len(processed_images)} images")
            return {
                'status': 'success',
                'processed_images': processed_images
            }
            
        except Exception as e:
            logger.error(f"❌ Image processing failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'error_type': AmazonSourcingError.IMAGE_PROCESSING_FAILED
            }
    
    @activity
    async def validate_product_activity(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate created product and calculate quality scores"""
        try:
            logger.info("🔍 Validating product quality and completeness")
            
            quality_scores = {}
            validation_errors = []
            validation_warnings = []
            
            # Title quality (1-100)
            title = product_data.get('title', '')
            quality_scores['title_quality'] = min(100, max(0, len(title) * 2))
            if len(title) < 20:
                validation_warnings.append("Product title is too short")
            
            # Description quality
            description = product_data.get('description', '')
            quality_scores['description_quality'] = min(100, max(0, len(description) / 10))
            if len(description) < 100:
                validation_warnings.append("Product description is too short")
            
            # Image quality
            images = product_data.get('images', [])
            quality_scores['image_quality'] = min(100, len(images) * 25)
            if len(images) < 3:
                validation_warnings.append("Less than 3 product images")
            
            # Price validation
            price = product_data.get('price')
            if price and price > 0:
                quality_scores['pricing_quality'] = 100
            else:
                quality_scores['pricing_quality'] = 0
                validation_errors.append("Invalid or missing price")
            
            # Overall quality score
            overall_quality = sum(quality_scores.values()) / len(quality_scores)
            quality_scores['overall_quality'] = round(overall_quality, 2)
            
            # Determine if validation passes
            validation_passed = len(validation_errors) == 0 and overall_quality >= 60
            
            logger.info(f"✅ Validation completed. Quality score: {overall_quality:.1f}%")
            return {
                'status': 'success',
                'validation_passed': validation_passed,
                'quality_scores': quality_scores,
                'errors': validation_errors,
                'warnings': validation_warnings
            }
            
        except Exception as e:
            logger.error(f"❌ Product validation failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'error_type': AmazonSourcingError.VALIDATION_FAILED
            }
    
    @activity
    async def notify_completion_activity(self, workflow_result: Dict[str, Any], notification_config: Dict[str, Any]) -> Dict[str, Any]:
        """Send completion notifications"""
        try:
            logger.info("📢 Sending completion notifications")
            
            # Prepare notification data
            notification_data = {
                'workflow_id': workflow_result.get('workflow_id'),
                'status': workflow_result.get('status'),
                'product_title': workflow_result.get('amazon_data', {}).get('title'),
                'saleor_product_id': workflow_result.get('saleor_product', {}).get('product_id'),
                'quality_score': workflow_result.get('quality_scores', {}).get('overall_quality'),
                'completed_at': datetime.now(timezone.utc).isoformat()
            }
            
            # Send notifications based on configuration
            notifications_sent = []
            
            if notification_config.get('email_enabled'):
                # Send email notification
                email_result = await self._send_email_notification(notification_data, notification_config)
                notifications_sent.append({'type': 'email', 'result': email_result})
            
            if notification_config.get('webhook_enabled'):
                # Send webhook notification
                webhook_result = await self._send_webhook_notification(notification_data, notification_config)
                notifications_sent.append({'type': 'webhook', 'result': webhook_result})
            
            if notification_config.get('dashboard_update'):
                # Update dashboard
                dashboard_result = await self._update_dashboard(notification_data, notification_config)
                notifications_sent.append({'type': 'dashboard', 'result': dashboard_result})
            
            logger.info(f"✅ Sent {len(notifications_sent)} notifications")
            return {
                'status': 'success',
                'notifications_sent': notifications_sent
            }
            
        except Exception as e:
            logger.error(f"❌ Notification sending failed: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    # Helper methods
    def _extract_asin_from_url(self, url: str) -> Optional[str]:
        """Extract ASIN from Amazon URL"""
        patterns = [
            r'/dp/([A-Z0-9]{10})',
            r'/product/([A-Z0-9]{10})',
            r'asin=([A-Z0-9]{10})',
            r'/([A-Z0-9]{10})(?:/|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    async def _scrape_amazon_product_data(self, asin: str, url: str) -> Dict[str, Any]:
        """Scrape Amazon product data (mock implementation)"""
        # In production, this would use proper web scraping with rate limiting
        # For now, return mock data based on ASIN
        
        return {
            'asin': asin,
            'title': f'Amazon Product {asin}',
            'description': f'High-quality product with ASIN {asin}. Features premium materials and excellent customer reviews.',
            'price': Decimal('29.99'),
            'images': [
                f'https://images-na.ssl-images-amazon.com/images/I/{asin}_001.jpg',
                f'https://images-na.ssl-images-amazon.com/images/I/{asin}_002.jpg'
            ],
            'category': 'Electronics',
            'brand': 'Amazon Brand',
            'features': ['High quality', 'Durable construction', 'Easy to use'],
            'rating': 4.3,
            'review_count': 1247,
            'availability': 'in_stock'
        }
    
    def _process_ai_enhancements(self, ai_result: Dict[str, Any]) -> AIEnhancementResult:
        """Process AI enhancement results"""
        result_data = ai_result.get('result', {})
        
        return AIEnhancementResult(
            optimized_title=result_data.get('optimized_title', ''),
            seo_description=result_data.get('seo_description', ''),
            product_tags=result_data.get('product_tags', []),
            category_suggestions=result_data.get('category_suggestions', []),
            pricing_recommendations=result_data.get('pricing_recommendations', {}),
            competitor_analysis=result_data.get('competitor_analysis', {}),
            content_enhancements=result_data.get('content_enhancements', {})
        )
    
    def _build_saleor_product_mutation(self, product_data: Dict[str, Any], enhancements: Dict[str, Any], config: Dict[str, Any]) -> str:
        """Build Saleor GraphQL product creation mutation"""
        
        title = enhancements.get('optimized_title', product_data.get('title', ''))
        description = enhancements.get('seo_description', product_data.get('description', ''))
        price = str(product_data.get('price', '0.00'))
        
        mutation = f"""
        mutation {{
            productCreate(input: {{
                name: "{title}"
                description: "{description}"
                productType: "{{config.get('product_type_id', '1')}}"
                category: "{{config.get('category_id', '1')}}"
                isPublished: false
                visibleInListings: true
            }}) {{
                product {{
                    id
                    name
                    slug
                    isPublished
                    created
                }}
                errors {{
                    field
                    message
                    code
                }}
            }}
        }}
        """
        
        return mutation
    
    def _extract_saleor_product_data(self, graphql_result: Dict[str, Any]) -> SaleorProductData:
        """Extract Saleor product data from GraphQL result"""
        product_data = graphql_result.get('data', {}).get('productCreate', {}).get('product', {})
        
        return SaleorProductData(
            product_id=product_data.get('id'),
            created_at=datetime.now(timezone.utc)
        )
    
    async def _send_email_notification(self, data: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """Send email notification (mock)"""
        logger.info(f"📧 Email notification sent for workflow: {data['workflow_id']}")
        return True
    
    async def _send_webhook_notification(self, data: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """Send webhook notification (mock)"""
        logger.info(f"🔗 Webhook notification sent for workflow: {data['workflow_id']}")
        return True
    
    async def _update_dashboard(self, data: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """Update dashboard (mock)"""
        logger.info(f"📊 Dashboard updated for workflow: {data['workflow_id']}")
        return True

@workflow
class AmazonProductSourcingWorkflow:
    """Main Temporal workflow for Amazon product sourcing"""
    
    def __init__(self):
        self.activities = AmazonSourcingActivities()
    
    @workflow.run
    async def run(self, sourcing_input: AmazonSourcingInput) -> AmazonSourcingOutput:
        """Execute the complete Amazon sourcing workflow"""
        
        workflow_id = info.workflow_id if TEMPORAL_AVAILABLE else f"amazon_sourcing_{uuid.uuid4().hex[:8]}"
        start_time = datetime.now(timezone.utc)
        
        result = AmazonSourcingOutput(
            workflow_id=workflow_id,
            status=AmazonSourcingStatus.PENDING,
            created_at=start_time,
            processing_metrics={'start_time': start_time.isoformat()},
            errors=[],
            warnings=[]
        )
        
        try:
            # Configure retry policy
            retry_policy = RetryPolicy(
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(seconds=60),
                maximum_attempts=3,
                backoff_coefficient=2.0
            ) if TEMPORAL_AVAILABLE else None
            
            # Step 1: Extract product data from Amazon
            result.status = AmazonSourcingStatus.EXTRACTING_DATA
            logger.info(f"🔄 Step 1: Extracting product data for workflow {workflow_id}")
            
            extract_result = await workflow.execute_activity(
                self.activities.extract_product_data_activity,
                asdict(sourcing_input),
                schedule_to_close_timeout=timedelta(minutes=5),
                retry_policy=retry_policy
            ) if TEMPORAL_AVAILABLE else await self.activities.extract_product_data_activity(asdict(sourcing_input))
            
            if extract_result['status'] == 'error':
                raise Exception(f"Product extraction failed: {extract_result['error']}")
            
            result.amazon_data = AmazonProductData(**extract_result['data'])
            
            # Step 2: Enhance with AI
            result.status = AmazonSourcingStatus.ENHANCING_WITH_AI
            logger.info(f"🔄 Step 2: Enhancing with AI for workflow {workflow_id}")
            
            ai_result = await workflow.execute_activity(
                self.activities.enhance_with_ai_activity,
                extract_result['data'],
                sourcing_input.ai_enhancement_config or {},
                schedule_to_close_timeout=timedelta(minutes=10),
                retry_policy=retry_policy
            ) if TEMPORAL_AVAILABLE else await self.activities.enhance_with_ai_activity(
                extract_result['data'], 
                sourcing_input.ai_enhancement_config or {}
            )
            
            if ai_result['status'] == 'error':
                result.warnings.append(f"AI enhancement failed: {ai_result['error']}")
                # Continue without AI enhancements
                ai_result = {'status': 'success', 'enhancements': {}}
            
            if ai_result.get('enhancements'):
                result.ai_enhancements = AIEnhancementResult(**ai_result['enhancements'])
            
            # Step 3: Create Saleor product
            result.status = AmazonSourcingStatus.CREATING_SALEOR_PRODUCT
            logger.info(f"🔄 Step 3: Creating Saleor product for workflow {workflow_id}")
            
            saleor_result = await workflow.execute_activity(
                self.activities.create_saleor_product_activity,
                extract_result['data'],
                ai_result.get('enhancements', {}),
                sourcing_input.store_config or {},
                schedule_to_close_timeout=timedelta(minutes=5),
                retry_policy=retry_policy
            ) if TEMPORAL_AVAILABLE else await self.activities.create_saleor_product_activity(
                extract_result['data'],
                ai_result.get('enhancements', {}),
                sourcing_input.store_config or {}
            )
            
            if saleor_result['status'] == 'error':
                raise Exception(f"Saleor product creation failed: {saleor_result['error']}")
            
            result.saleor_product = SaleorProductData(**saleor_result['saleor_product'])
            
            # Step 4: Process images (parallel activity)
            result.status = AmazonSourcingStatus.PROCESSING_IMAGES
            logger.info(f"🔄 Step 4: Processing images for workflow {workflow_id}")
            
            if result.amazon_data.images:
                image_result = await workflow.execute_activity(
                    self.activities.process_images_activity,
                    result.amazon_data.images,
                    result.saleor_product.product_id,
                    schedule_to_close_timeout=timedelta(minutes=15),
                    retry_policy=retry_policy
                ) if TEMPORAL_AVAILABLE else await self.activities.process_images_activity(
                    result.amazon_data.images,
                    result.saleor_product.product_id
                )
                
                if image_result['status'] == 'error':
                    result.warnings.append(f"Image processing failed: {image_result['error']}")
            
            # Step 5: Validate product
            result.status = AmazonSourcingStatus.VALIDATING_PRODUCT
            logger.info(f"🔄 Step 5: Validating product for workflow {workflow_id}")
            
            validation_result = await workflow.execute_activity(
                self.activities.validate_product_activity,
                asdict(result.amazon_data),
                schedule_to_close_timeout=timedelta(minutes=2),
                retry_policy=retry_policy
            ) if TEMPORAL_AVAILABLE else await self.activities.validate_product_activity(asdict(result.amazon_data))
            
            if validation_result['status'] == 'success':
                result.quality_scores = validation_result['quality_scores']
                if validation_result.get('warnings'):
                    result.warnings.extend(validation_result['warnings'])
                if validation_result.get('errors'):
                    result.errors.extend(validation_result['errors'])
            
            # Step 6: Send notifications
            result.status = AmazonSourcingStatus.NOTIFYING_COMPLETION
            logger.info(f"🔄 Step 6: Sending notifications for workflow {workflow_id}")
            
            notification_result = await workflow.execute_activity(
                self.activities.notify_completion_activity,
                asdict(result),
                sourcing_input.notification_config or {},
                schedule_to_close_timeout=timedelta(minutes=2),
                retry_policy=retry_policy
            ) if TEMPORAL_AVAILABLE else await self.activities.notify_completion_activity(
                asdict(result),
                sourcing_input.notification_config or {}
            )
            
            # Complete workflow
            result.status = AmazonSourcingStatus.COMPLETED
            result.completed_at = datetime.now(timezone.utc)
            result.processing_metrics.update({
                'end_time': result.completed_at.isoformat(),
                'duration_seconds': (result.completed_at - start_time).total_seconds(),
                'steps_completed': 6
            })
            
            logger.info(f"✅ Amazon sourcing workflow {workflow_id} completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ Amazon sourcing workflow {workflow_id} failed: {e}")
            result.status = AmazonSourcingStatus.FAILED
            result.errors.append(str(e))
            result.completed_at = datetime.now(timezone.utc)
            result.processing_metrics.update({
                'end_time': result.completed_at.isoformat(),
                'duration_seconds': (result.completed_at - start_time).total_seconds(),
                'failure_reason': str(e)
            })
            
            return result

class AmazonSourcingWorkflowManager:
    """Manager for Amazon sourcing workflows"""
    
    def __init__(self, temporal_client: TemporalClient):
        self.temporal_client = temporal_client
        self.workflow_registry = {}
    
    async def start_amazon_sourcing_workflow(
        self,
        amazon_url: str,
        tenant_id: str,
        user_id: str,
        **kwargs
    ) -> WorkflowResponse:
        """Start a new Amazon sourcing workflow"""
        
        # Prepare workflow input
        sourcing_input = AmazonSourcingInput(
            amazon_url=amazon_url,
            tenant_id=tenant_id,
            user_id=user_id,
            store_config=kwargs.get('store_config', {}),
            ai_enhancement_config=kwargs.get('ai_enhancement_config', {}),
            pricing_rules=kwargs.get('pricing_rules', {}),
            category_mappings=kwargs.get('category_mappings', {}),
            notification_config=kwargs.get('notification_config', {})
        )
        
        # Create workflow request
        workflow_request = WorkflowRequest(
            workflow_type=WorkflowType.AMAZON_SPAPI_SOURCING,
            tenant_id=tenant_id,
            user_id=user_id,
            input_data=asdict(sourcing_input),
            execution_timeout=3600,  # 1 hour
            retry_policy={
                'initial_interval_seconds': 1,
                'maximum_interval_seconds': 60,
                'maximum_attempts': 3,
                'backoff_coefficient': 2.0
            }
        )
        
        # Start workflow
        response = await self.temporal_client.start_workflow(workflow_request)
        
        # Register workflow
        if response.status != WorkflowStatus.FAILED:
            self.workflow_registry[response.workflow_id] = {
                'amazon_url': amazon_url,
                'tenant_id': tenant_id,
                'user_id': user_id,
                'started_at': response.started_at
            }
        
        return response
    
    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get detailed workflow status"""
        
        # Get basic status from Temporal
        basic_status = await self.temporal_client.get_workflow_status(workflow_id)
        
        # Add additional details
        workflow_details = self.workflow_registry.get(workflow_id, {})
        
        return {
            'workflow_id': workflow_id,
            'status': basic_status.status,
            'started_at': basic_status.started_at,
            'completed_at': basic_status.completed_at,
            'amazon_url': workflow_details.get('amazon_url'),
            'tenant_id': workflow_details.get('tenant_id'),
            'user_id': workflow_details.get('user_id'),
            'result': basic_status.result,
            'error': basic_status.error
        }
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a running workflow"""
        success = await self.temporal_client.cancel_workflow(workflow_id)
        
        if success and workflow_id in self.workflow_registry:
            self.workflow_registry[workflow_id]['cancelled_at'] = datetime.now(timezone.utc)
        
        return success
    
    async def list_workflows(self, tenant_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """List Amazon sourcing workflows"""
        
        # Get workflows from Temporal
        workflows = await self.temporal_client.list_workflows(tenant_id, limit)
        
        # Filter for Amazon sourcing workflows
        amazon_workflows = [
            w for w in workflows 
            if w.get('workflow_type') == WorkflowType.AMAZON_SPAPI_SOURCING
        ]
        
        # Add additional details
        for workflow in amazon_workflows:
            workflow_id = workflow['workflow_id']
            if workflow_id in self.workflow_registry:
                workflow.update(self.workflow_registry[workflow_id])
        
        return amazon_workflows
    
    async def get_workflow_metrics(self) -> Dict[str, Any]:
        """Get Amazon sourcing workflow metrics"""
        
        all_workflows = list(self.workflow_registry.values())
        
        total_workflows = len(all_workflows)
        active_workflows = sum(1 for w in all_workflows if not w.get('completed_at') and not w.get('cancelled_at'))
        
        return {
            'total_workflows': total_workflows,
            'active_workflows': active_workflows,
            'completed_workflows': total_workflows - active_workflows,
            'average_duration_seconds': 180,  # Mock data
            'success_rate': 95.5,
            'most_common_errors': [
                'Product not found',
                'AI enhancement timeout',
                'Saleor API error'
            ]
        }

# Singleton instance
amazon_sourcing_manager = AmazonSourcingWorkflowManager(TemporalClient())

async def get_amazon_sourcing_manager() -> AmazonSourcingWorkflowManager:
    """Get Amazon sourcing workflow manager"""
    return amazon_sourcing_manager
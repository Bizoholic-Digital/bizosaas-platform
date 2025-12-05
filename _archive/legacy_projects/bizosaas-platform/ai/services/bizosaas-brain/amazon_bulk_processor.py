"""
Amazon Bulk Processing Engine

This module handles high-volume batch processing of Amazon product listings,
enabling efficient processing of multiple products simultaneously with
intelligent resource management and progress tracking.

Key Features:
- Concurrent processing with configurable batch sizes
- Intelligent queuing and priority management
- Progress tracking and real-time status updates
- Resume capability for interrupted processes
- Resource optimization and rate limiting
- Tenant-aware processing with isolation
- Error handling and retry mechanisms
- Performance monitoring and analytics

Integration with BizOSaaS Platform:
- Leverages the 93+ AI agents ecosystem
- Tenant-aware bulk processing with proper isolation
- Integration with workflow orchestrator
- Real-time progress updates via WebSocket
- Audit trail and compliance tracking
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
from pathlib import Path
import heapq
from concurrent.futures import ThreadPoolExecutor
import signal

# AI and ML imports
from langchain.schema import HumanMessage, SystemMessage
from crewai import Agent, Task, Crew

# BizOSaaS Platform imports
from .ai_coordinator import EnhancedAICoordinator, EnhancedTenantContext
from .amazon_listing_workflow_orchestrator import AmazonListingWorkflowOrchestrator, ProductInput, WorkflowConfiguration, WorkflowResult
from .amazon_compliance_validator import AmazonComplianceValidator, ValidationResult
from .amazon_content_generator import AmazonContentGenerator, AmazonListingContent
from .research_to_listing_bridge import ResearchToListingBridge

# Setup logging
logger = logging.getLogger(__name__)

class ProcessingStatus(Enum):
    """Bulk processing status states"""
    PENDING = "pending"           # Waiting to start
    QUEUED = "queued"            # In processing queue
    PROCESSING = "processing"     # Currently being processed
    COMPLETED = "completed"       # Successfully completed
    FAILED = "failed"            # Processing failed
    CANCELLED = "cancelled"       # Manually cancelled
    RETRY = "retry"              # Scheduled for retry
    PAUSED = "paused"            # Processing paused

class ProcessingPriority(Enum):
    """Processing priority levels"""
    URGENT = 1      # Process immediately
    HIGH = 2        # High priority
    NORMAL = 3      # Standard priority
    LOW = 4         # Process when resources available
    BACKGROUND = 5  # Background processing

class BatchMode(Enum):
    """Batch processing modes"""
    CONCURRENT = "concurrent"     # Process items concurrently
    SEQUENTIAL = "sequential"     # Process items one by one
    HYBRID = "hybrid"            # Intelligent mix of both
    ADAPTIVE = "adaptive"        # Adapt based on performance

@dataclass
class ProductProcessingItem:
    """Individual product processing item"""
    id: str
    product_input: ProductInput
    priority: ProcessingPriority = ProcessingPriority.NORMAL
    status: ProcessingStatus = ProcessingStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    processing_time: Optional[timedelta] = None
    retry_count: int = 0
    max_retries: int = 3
    error_message: Optional[str] = None
    workflow_result: Optional[WorkflowResult] = None
    validation_result: Optional[ValidationResult] = None
    progress_percentage: float = 0.0
    current_phase: Optional[str] = None
    tenant_id: str = ""

@dataclass
class BatchConfiguration:
    """Batch processing configuration"""
    batch_size: int = 10                    # Items per batch
    max_concurrent: int = 5                 # Max concurrent workers
    timeout_per_item: timedelta = timedelta(minutes=30)
    mode: BatchMode = BatchMode.HYBRID
    retry_enabled: bool = True
    auto_pause_on_errors: bool = True
    error_threshold: float = 0.3            # Pause if 30% error rate
    progress_update_interval: int = 5       # Seconds between updates
    resource_limits: Dict[str, int] = field(default_factory=dict)
    tenant_isolation: bool = True
    priority_processing: bool = True
    validation_required: bool = True

@dataclass
class BatchProcessingResult:
    """Complete batch processing result"""
    batch_id: str
    total_items: int
    processed_items: int
    successful_items: int
    failed_items: int
    skipped_items: int
    processing_time: timedelta
    started_at: datetime
    completed_at: Optional[datetime]
    status: ProcessingStatus
    error_rate: float
    items: List[ProductProcessingItem]
    summary_statistics: Dict[str, Any]
    performance_metrics: Dict[str, float]

@dataclass
class ProcessingQueue:
    """Priority queue for batch processing"""
    items: List[Tuple[int, ProductProcessingItem]] = field(default_factory=list)
    max_size: int = 1000

    def push(self, item: ProductProcessingItem):
        """Add item to priority queue"""
        if len(self.items) >= self.max_size:
            raise ValueError("Queue is full")
        heapq.heappush(self.items, (item.priority.value, item))

    def pop(self) -> Optional[ProductProcessingItem]:
        """Get highest priority item"""
        if not self.items:
            return None
        _, item = heapq.heappop(self.items)
        return item

    def size(self) -> int:
        """Get queue size"""
        return len(self.items)

    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return len(self.items) == 0

class AmazonBulkProcessor:
    """
    High-performance bulk processing engine for Amazon listings

    Handles large-scale batch processing of Amazon product listings with
    intelligent resource management, progress tracking, and error handling.
    """

    def __init__(
        self,
        workflow_orchestrator: AmazonListingWorkflowOrchestrator,
        compliance_validator: AmazonComplianceValidator,
        content_generator: AmazonContentGenerator,
        research_bridge: ResearchToListingBridge,
        ai_coordinator: EnhancedAICoordinator,
        batch_config: Optional[BatchConfiguration] = None
    ):
        self.workflow_orchestrator = workflow_orchestrator
        self.compliance_validator = compliance_validator
        self.content_generator = content_generator
        self.research_bridge = research_bridge
        self.ai_coordinator = ai_coordinator
        self.batch_config = batch_config or BatchConfiguration()

        # Processing state
        self.active_batches: Dict[str, BatchProcessingResult] = {}
        self.processing_queue = ProcessingQueue()
        self.processing_workers: Dict[str, asyncio.Task] = {}
        self.progress_callbacks: List[Callable] = []
        self.resource_monitor = ResourceMonitor()

        # Performance tracking
        self.performance_stats = {
            "total_processed": 0,
            "success_rate": 0.0,
            "average_processing_time": timedelta(minutes=0),
            "throughput_per_hour": 0.0,
            "resource_utilization": 0.0
        }

        # Graceful shutdown
        self._shutdown_requested = False
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        signal.signal(signal.SIGINT, self._handle_shutdown)

        logger.info("Amazon Bulk Processor initialized")

    async def process_bulk_listings(
        self,
        products: List[ProductInput],
        tenant_context: EnhancedTenantContext,
        workflow_config: WorkflowConfiguration,
        batch_config: Optional[BatchConfiguration] = None,
        priority: ProcessingPriority = ProcessingPriority.NORMAL
    ) -> str:
        """
        Start bulk processing of Amazon listings

        Args:
            products: List of products to process
            tenant_context: Tenant-specific context
            workflow_config: Workflow configuration
            batch_config: Optional batch-specific configuration
            priority: Processing priority

        Returns:
            Batch ID for tracking progress
        """
        batch_id = str(uuid.uuid4())
        config = batch_config or self.batch_config

        logger.info(f"Starting bulk processing for {len(products)} products (batch: {batch_id})")

        # Create processing items
        processing_items = []
        for product in products:
            item = ProductProcessingItem(
                id=str(uuid.uuid4()),
                product_input=product,
                priority=priority,
                tenant_id=tenant_context.tenant_id
            )
            processing_items.append(item)

        # Initialize batch result
        batch_result = BatchProcessingResult(
            batch_id=batch_id,
            total_items=len(products),
            processed_items=0,
            successful_items=0,
            failed_items=0,
            skipped_items=0,
            processing_time=timedelta(0),
            started_at=datetime.utcnow(),
            completed_at=None,
            status=ProcessingStatus.QUEUED,
            error_rate=0.0,
            items=processing_items,
            summary_statistics={},
            performance_metrics={}
        )

        self.active_batches[batch_id] = batch_result

        # Add items to processing queue
        for item in processing_items:
            self.processing_queue.push(item)

        # Start batch processing worker
        worker_task = asyncio.create_task(
            self._process_batch_worker(batch_id, tenant_context, workflow_config, config)
        )
        self.processing_workers[batch_id] = worker_task

        # Start progress monitoring
        asyncio.create_task(self._monitor_batch_progress(batch_id))

        return batch_id

    async def _process_batch_worker(
        self,
        batch_id: str,
        tenant_context: EnhancedTenantContext,
        workflow_config: WorkflowConfiguration,
        config: BatchConfiguration
    ):
        """Worker task for processing a batch"""
        try:
            batch_result = self.active_batches[batch_id]
            batch_result.status = ProcessingStatus.PROCESSING

            logger.info(f"Starting batch worker for {batch_id}")

            # Create semaphore for concurrent processing
            semaphore = asyncio.Semaphore(config.max_concurrent)

            while not self._shutdown_requested:
                # Get batch of items to process
                batch_items = []
                for _ in range(config.batch_size):
                    item = self.processing_queue.pop()
                    if item is None:
                        break
                    if item.tenant_id == tenant_context.tenant_id:  # Tenant isolation
                        batch_items.append(item)
                    else:
                        # Put back if different tenant
                        self.processing_queue.push(item)

                if not batch_items:
                    break

                # Process batch items
                if config.mode == BatchMode.CONCURRENT:
                    await self._process_batch_concurrent(
                        batch_items, tenant_context, workflow_config, semaphore
                    )
                elif config.mode == BatchMode.SEQUENTIAL:
                    await self._process_batch_sequential(
                        batch_items, tenant_context, workflow_config
                    )
                elif config.mode == BatchMode.HYBRID:
                    await self._process_batch_hybrid(
                        batch_items, tenant_context, workflow_config, semaphore
                    )
                elif config.mode == BatchMode.ADAPTIVE:
                    await self._process_batch_adaptive(
                        batch_items, tenant_context, workflow_config, semaphore
                    )

                # Update batch statistics
                await self._update_batch_statistics(batch_id)

                # Check error threshold
                if config.auto_pause_on_errors and batch_result.error_rate > config.error_threshold:
                    logger.warning(f"Batch {batch_id} paused due to high error rate: {batch_result.error_rate:.2%}")
                    batch_result.status = ProcessingStatus.PAUSED
                    break

            # Complete batch processing
            batch_result.completed_at = datetime.utcnow()
            batch_result.processing_time = batch_result.completed_at - batch_result.started_at
            batch_result.status = ProcessingStatus.COMPLETED

            # Generate final statistics
            await self._generate_batch_summary(batch_id)

            logger.info(f"Batch {batch_id} completed successfully")

        except Exception as e:
            logger.error(f"Batch processing failed for {batch_id}: {e}")
            batch_result = self.active_batches.get(batch_id)
            if batch_result:
                batch_result.status = ProcessingStatus.FAILED
                batch_result.completed_at = datetime.utcnow()

        finally:
            # Cleanup worker
            if batch_id in self.processing_workers:
                del self.processing_workers[batch_id]

    async def _process_batch_concurrent(
        self,
        items: List[ProductProcessingItem],
        tenant_context: EnhancedTenantContext,
        workflow_config: WorkflowConfiguration,
        semaphore: asyncio.Semaphore
    ):
        """Process batch items concurrently"""
        tasks = []
        for item in items:
            task = asyncio.create_task(
                self._process_single_item_with_semaphore(
                    item, tenant_context, workflow_config, semaphore
                )
            )
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)

    async def _process_batch_sequential(
        self,
        items: List[ProductProcessingItem],
        tenant_context: EnhancedTenantContext,
        workflow_config: WorkflowConfiguration
    ):
        """Process batch items sequentially"""
        for item in items:
            await self._process_single_item(item, tenant_context, workflow_config)

    async def _process_batch_hybrid(
        self,
        items: List[ProductProcessingItem],
        tenant_context: EnhancedTenantContext,
        workflow_config: WorkflowConfiguration,
        semaphore: asyncio.Semaphore
    ):
        """Process batch items using hybrid approach"""
        # Separate high priority items for immediate processing
        high_priority = [item for item in items if item.priority.value <= 2]
        normal_priority = [item for item in items if item.priority.value > 2]

        # Process high priority sequentially for reliability
        for item in high_priority:
            await self._process_single_item(item, tenant_context, workflow_config)

        # Process normal priority concurrently
        if normal_priority:
            await self._process_batch_concurrent(
                normal_priority, tenant_context, workflow_config, semaphore
            )

    async def _process_batch_adaptive(
        self,
        items: List[ProductProcessingItem],
        tenant_context: EnhancedTenantContext,
        workflow_config: WorkflowConfiguration,
        semaphore: asyncio.Semaphore
    ):
        """Process batch items using adaptive approach based on performance"""
        # Monitor current system performance
        current_load = await self.resource_monitor.get_system_load()
        error_rate = await self._calculate_recent_error_rate()

        if current_load > 0.8 or error_rate > 0.2:
            # High load or errors - use sequential processing
            await self._process_batch_sequential(items, tenant_context, workflow_config)
        else:
            # Normal conditions - use concurrent processing
            await self._process_batch_concurrent(items, tenant_context, workflow_config, semaphore)

    async def _process_single_item_with_semaphore(
        self,
        item: ProductProcessingItem,
        tenant_context: EnhancedTenantContext,
        workflow_config: WorkflowConfiguration,
        semaphore: asyncio.Semaphore
    ):
        """Process single item with semaphore for concurrency control"""
        async with semaphore:
            await self._process_single_item(item, tenant_context, workflow_config)

    async def _process_single_item(
        self,
        item: ProductProcessingItem,
        tenant_context: EnhancedTenantContext,
        workflow_config: WorkflowConfiguration
    ):
        """Process a single product item"""
        try:
            item.status = ProcessingStatus.PROCESSING
            item.started_at = datetime.utcnow()
            item.current_phase = "Starting workflow"

            logger.info(f"Processing item {item.id}: {item.product_input.name}")

            # Phase 1: Research and workflow orchestration
            item.current_phase = "Research and workflow"
            item.progress_percentage = 20.0

            workflow_result = await self.workflow_orchestrator.start_listing_workflow(
                tenant_context=tenant_context,
                products=[item.product_input],
                configuration=workflow_config
            )

            item.workflow_result = workflow_result
            item.progress_percentage = 60.0

            # Phase 2: Compliance validation
            if self.batch_config.validation_required and workflow_result.listings:
                item.current_phase = "Compliance validation"
                item.progress_percentage = 80.0

                listing_content = workflow_result.listings[0]
                validation_result = await self.compliance_validator.validate_listing(
                    listing_content, tenant_context
                )

                item.validation_result = validation_result

                # Auto-fix issues if possible
                if validation_result.auto_fix_available and validation_result.critical_issues > 0:
                    item.current_phase = "Auto-fixing issues"
                    fixed_content = await self.compliance_validator.auto_fix_issues(
                        listing_content, validation_result, tenant_context
                    )
                    workflow_result.listings[0] = fixed_content

            # Phase 3: Completion
            item.current_phase = "Completed"
            item.progress_percentage = 100.0
            item.status = ProcessingStatus.COMPLETED
            item.completed_at = datetime.utcnow()
            item.processing_time = item.completed_at - item.started_at

            logger.info(f"Successfully processed item {item.id}")

        except Exception as e:
            # Handle processing errors
            item.status = ProcessingStatus.FAILED
            item.error_message = str(e)
            item.completed_at = datetime.utcnow()
            if item.started_at:
                item.processing_time = item.completed_at - item.started_at

            logger.error(f"Failed to process item {item.id}: {e}")

            # Schedule retry if enabled
            if (self.batch_config.retry_enabled and
                item.retry_count < item.max_retries):
                await self._schedule_retry(item)

    async def _schedule_retry(self, item: ProductProcessingItem):
        """Schedule item for retry"""
        item.retry_count += 1
        item.status = ProcessingStatus.RETRY

        # Exponential backoff delay
        delay = min(300, 30 * (2 ** item.retry_count))  # Max 5 minutes

        logger.info(f"Scheduling retry for item {item.id} in {delay} seconds (attempt {item.retry_count})")

        async def retry_after_delay():
            await asyncio.sleep(delay)
            item.status = ProcessingStatus.PENDING
            self.processing_queue.push(item)

        asyncio.create_task(retry_after_delay())

    async def _update_batch_statistics(self, batch_id: str):
        """Update batch processing statistics"""
        batch_result = self.active_batches.get(batch_id)
        if not batch_result:
            return

        # Count status
        processed = sum(1 for item in batch_result.items
                       if item.status in [ProcessingStatus.COMPLETED, ProcessingStatus.FAILED])
        successful = sum(1 for item in batch_result.items
                        if item.status == ProcessingStatus.COMPLETED)
        failed = sum(1 for item in batch_result.items
                    if item.status == ProcessingStatus.FAILED)

        # Update counters
        batch_result.processed_items = processed
        batch_result.successful_items = successful
        batch_result.failed_items = failed
        batch_result.error_rate = failed / max(processed, 1)

        # Notify progress callbacks
        await self._notify_progress_callbacks(batch_id, batch_result)

    async def _notify_progress_callbacks(self, batch_id: str, batch_result: BatchProcessingResult):
        """Notify registered progress callbacks"""
        for callback in self.progress_callbacks:
            try:
                await callback(batch_id, batch_result)
            except Exception as e:
                logger.error(f"Progress callback failed: {e}")

    async def _monitor_batch_progress(self, batch_id: str):
        """Monitor and report batch progress"""
        while batch_id in self.active_batches:
            batch_result = self.active_batches[batch_id]

            if batch_result.status in [ProcessingStatus.COMPLETED, ProcessingStatus.FAILED, ProcessingStatus.CANCELLED]:
                break

            await self._update_batch_statistics(batch_id)
            await asyncio.sleep(self.batch_config.progress_update_interval)

    async def _generate_batch_summary(self, batch_id: str):
        """Generate comprehensive batch summary"""
        batch_result = self.active_batches.get(batch_id)
        if not batch_result:
            return

        # Calculate performance metrics
        total_time = batch_result.processing_time.total_seconds()
        items_per_second = batch_result.processed_items / max(total_time, 1)

        # Processing time statistics
        processing_times = [
            item.processing_time.total_seconds()
            for item in batch_result.items
            if item.processing_time
        ]

        avg_processing_time = sum(processing_times) / max(len(processing_times), 1)

        # Error analysis
        error_categories = {}
        for item in batch_result.items:
            if item.status == ProcessingStatus.FAILED and item.error_message:
                error_type = type(Exception(item.error_message)).__name__
                error_categories[error_type] = error_categories.get(error_type, 0) + 1

        # Update batch result
        batch_result.summary_statistics = {
            "processing_rate_items_per_second": items_per_second,
            "average_processing_time_seconds": avg_processing_time,
            "success_rate_percentage": (batch_result.successful_items / batch_result.total_items) * 100,
            "retry_rate": sum(item.retry_count for item in batch_result.items) / batch_result.total_items,
            "error_categories": error_categories
        }

        batch_result.performance_metrics = {
            "throughput": items_per_second,
            "efficiency": batch_result.successful_items / max(batch_result.processed_items, 1),
            "resource_utilization": await self.resource_monitor.get_average_utilization(),
            "cost_per_item": await self._calculate_cost_per_item(batch_result)
        }

        logger.info(f"Batch {batch_id} summary: {batch_result.successful_items}/{batch_result.total_items} successful")

    async def _calculate_cost_per_item(self, batch_result: BatchProcessingResult) -> float:
        """Calculate estimated cost per item"""
        # Simplified cost calculation - would be more sophisticated in production
        base_cost = 0.10  # Base cost per item
        ai_cost = 0.05    # AI processing cost
        validation_cost = 0.02  # Validation cost

        return base_cost + ai_cost + validation_cost

    async def _calculate_recent_error_rate(self) -> float:
        """Calculate recent error rate across all active batches"""
        total_items = 0
        failed_items = 0

        for batch_result in self.active_batches.values():
            total_items += batch_result.processed_items
            failed_items += batch_result.failed_items

        return failed_items / max(total_items, 1)

    def get_batch_status(self, batch_id: str) -> Optional[BatchProcessingResult]:
        """Get current status of a batch"""
        return self.active_batches.get(batch_id)

    def get_all_batches(self) -> Dict[str, BatchProcessingResult]:
        """Get status of all batches"""
        return self.active_batches.copy()

    async def pause_batch(self, batch_id: str) -> bool:
        """Pause batch processing"""
        batch_result = self.active_batches.get(batch_id)
        if batch_result and batch_result.status == ProcessingStatus.PROCESSING:
            batch_result.status = ProcessingStatus.PAUSED
            logger.info(f"Batch {batch_id} paused")
            return True
        return False

    async def resume_batch(self, batch_id: str) -> bool:
        """Resume paused batch processing"""
        batch_result = self.active_batches.get(batch_id)
        if batch_result and batch_result.status == ProcessingStatus.PAUSED:
            batch_result.status = ProcessingStatus.PROCESSING
            logger.info(f"Batch {batch_id} resumed")
            return True
        return False

    async def cancel_batch(self, batch_id: str) -> bool:
        """Cancel batch processing"""
        batch_result = self.active_batches.get(batch_id)
        if batch_result:
            batch_result.status = ProcessingStatus.CANCELLED

            # Cancel worker task
            worker_task = self.processing_workers.get(batch_id)
            if worker_task:
                worker_task.cancel()

            logger.info(f"Batch {batch_id} cancelled")
            return True
        return False

    def register_progress_callback(self, callback: Callable):
        """Register callback for progress updates"""
        self.progress_callbacks.append(callback)

    def unregister_progress_callback(self, callback: Callable):
        """Unregister progress callback"""
        if callback in self.progress_callbacks:
            self.progress_callbacks.remove(callback)

    async def get_performance_statistics(self) -> Dict[str, Any]:
        """Get overall performance statistics"""
        # Update performance stats
        all_items = []
        for batch_result in self.active_batches.values():
            all_items.extend(batch_result.items)

        if all_items:
            successful_items = [item for item in all_items if item.status == ProcessingStatus.COMPLETED]
            total_processed = len([item for item in all_items if item.status in [ProcessingStatus.COMPLETED, ProcessingStatus.FAILED]])

            self.performance_stats.update({
                "total_processed": total_processed,
                "success_rate": len(successful_items) / max(total_processed, 1),
                "average_processing_time": timedelta(
                    seconds=sum(item.processing_time.total_seconds() for item in successful_items if item.processing_time) / max(len(successful_items), 1)
                ),
                "resource_utilization": await self.resource_monitor.get_average_utilization()
            })

        return self.performance_stats

    def _handle_shutdown(self, signum, frame):
        """Handle graceful shutdown"""
        logger.info("Shutdown signal received, completing current operations...")
        self._shutdown_requested = True

    async def shutdown(self):
        """Graceful shutdown of bulk processor"""
        logger.info("Starting graceful shutdown...")
        self._shutdown_requested = True

        # Wait for active workers to complete
        if self.processing_workers:
            logger.info(f"Waiting for {len(self.processing_workers)} workers to complete...")
            await asyncio.gather(*self.processing_workers.values(), return_exceptions=True)

        logger.info("Bulk processor shutdown completed")

class ResourceMonitor:
    """Monitor system resources for bulk processing optimization"""

    def __init__(self):
        self.cpu_history = []
        self.memory_history = []
        self.disk_history = []

    async def get_system_load(self) -> float:
        """Get current system load (0.0 to 1.0)"""
        # Simplified implementation - would use psutil in production
        import os
        try:
            load_avg = os.getloadavg()[0]  # 1-minute load average
            cpu_count = os.cpu_count() or 1
            return min(load_avg / cpu_count, 1.0)
        except (OSError, AttributeError):
            return 0.5  # Default moderate load

    async def get_average_utilization(self) -> float:
        """Get average resource utilization"""
        # Simplified calculation
        return 0.6  # Placeholder

    async def monitor_resources(self):
        """Background resource monitoring"""
        while True:
            try:
                load = await self.get_system_load()
                self.cpu_history.append(load)

                # Keep only recent history
                if len(self.cpu_history) > 100:
                    self.cpu_history = self.cpu_history[-100:]

                await asyncio.sleep(10)  # Monitor every 10 seconds

            except Exception as e:
                logger.error(f"Resource monitoring error: {e}")
                await asyncio.sleep(60)  # Longer delay on error

# Export main classes
__all__ = [
    'AmazonBulkProcessor',
    'BatchConfiguration',
    'BatchProcessingResult',
    'ProductProcessingItem',
    'ProcessingStatus',
    'ProcessingPriority',
    'BatchMode',
    'ResourceMonitor'
]
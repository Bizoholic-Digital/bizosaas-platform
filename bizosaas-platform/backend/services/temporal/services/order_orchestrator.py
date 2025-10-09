"""
Order Processing Orchestrator
Main coordinator for the complete order processing workflow
"""

import asyncio
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Any, Tuple
from uuid import uuid4

from ..models.order_models import (
    OrderStatus, PaymentStatus, FulfillmentStatus, OrderResponse,
    OrderItem, Address, PaymentDetails, PricingSummary, Fulfillment,
    FraudAssessment, FraudRiskLevel, ProcessingError
)

logger = logging.getLogger(__name__)


class OrderProcessingOrchestrator:
    """
    Main orchestrator for order processing workflow
    Coordinates inventory, payments, fulfillment, and notifications
    """
    
    def __init__(
        self,
        inventory_manager,
        payment_processor,
        fulfillment_manager,
        notification_service,
        saleor_integration,
        ai_crew_integration,
        performance_monitor,
        metrics_collector
    ):
        self.inventory_manager = inventory_manager
        self.payment_processor = payment_processor
        self.fulfillment_manager = fulfillment_manager
        self.notification_service = notification_service
        self.saleor_integration = saleor_integration
        self.ai_crew_integration = ai_crew_integration
        self.performance_monitor = performance_monitor
        self.metrics_collector = metrics_collector
        
        # Order processing configuration
        self.config = {
            "high_value_threshold": Decimal("1000.00"),  # Requires manual review
            "fraud_score_threshold": 75.0,  # Requires fraud review
            "inventory_reservation_timeout": 1800,  # 30 minutes
            "payment_auth_timeout": 900,  # 15 minutes
            "processing_timeout": 3600,  # 1 hour
            "max_retry_attempts": 3,
            "auto_capture_payments": True,
            "enable_ai_optimization": True
        }
        
        # In-memory storage for demo (replace with database in production)
        self.orders = {}
        self.processing_locks = {}
        
    async def initialize(self):
        """Initialize the orchestrator and all dependencies"""
        logger.info("Initializing Order Processing Orchestrator...")
        
        try:
            # Initialize all services
            await self.inventory_manager.initialize()
            await self.payment_processor.initialize()
            await self.fulfillment_manager.initialize()
            await self.notification_service.initialize()
            await self.saleor_integration.initialize()
            await self.ai_crew_integration.initialize()
            
            logger.info("Order Processing Orchestrator initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Order Processing Orchestrator: {e}")
            raise
    
    async def shutdown(self):
        """Cleanup orchestrator and all dependencies"""
        logger.info("Shutting down Order Processing Orchestrator...")
        
        try:
            # Cleanup all services
            await self.inventory_manager.shutdown()
            await self.payment_processor.shutdown()
            await self.fulfillment_manager.shutdown()
            await self.notification_service.shutdown()
            await self.saleor_integration.shutdown()
            await self.ai_crew_integration.shutdown()
            
            logger.info("Order Processing Orchestrator shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during orchestrator shutdown: {e}")
    
    async def process_order(self, order_data: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a new order through the complete workflow
        
        Args:
            order_data: Order creation data
            user_context: User context for authorization
            
        Returns:
            Dict containing order processing result
        """
        order_id = str(uuid4())
        start_time = datetime.utcnow()
        
        logger.info(f"Starting order processing for order {order_id}")
        
        try:
            # Acquire processing lock
            async with self._get_processing_lock(order_id):
                
                # Track processing start
                await self.performance_monitor.start_order_processing(order_id)
                
                # Step 1: Validate and create order
                order = await self._create_order(order_id, order_data, user_context)
                
                # Step 2: Fraud detection and risk assessment
                fraud_assessment = await self._assess_fraud_risk(order)
                order["fraud_assessment"] = fraud_assessment
                
                # Step 3: Check for HITL requirements
                if await self._requires_human_review(order, fraud_assessment):
                    order["status"] = OrderStatus.ON_HOLD
                    await self._request_human_review(order, "high_value_or_fraud_risk")
                    return order
                
                # Step 4: Inventory validation and reservation
                inventory_result = await self._process_inventory(order)
                if not inventory_result["success"]:
                    order["status"] = OrderStatus.FAILED
                    raise Exception(f"Inventory processing failed: {inventory_result['error']}")
                
                order["status"] = OrderStatus.INVENTORY_RESERVED
                
                # Step 5: Payment authorization
                payment_result = await self._process_payment_authorization(order)
                if not payment_result["success"]:
                    # Release inventory reservation
                    await self._release_inventory_reservation(order)
                    order["status"] = OrderStatus.FAILED
                    raise Exception(f"Payment authorization failed: {payment_result['error']}")
                
                order["payment_details"] = payment_result["payment_details"]
                order["status"] = OrderStatus.PAYMENT_AUTHORIZED
                
                # Step 6: Calculate taxes and final pricing
                pricing_result = await self._calculate_final_pricing(order)
                order["pricing"] = pricing_result
                
                # Step 7: AI optimization (if enabled)
                if self.config["enable_ai_optimization"]:
                    optimization_result = await self._ai_optimize_order(order)
                    order.update(optimization_result)
                
                # Step 8: Move to processing
                order["status"] = OrderStatus.PROCESSING
                
                # Step 9: Schedule fulfillment
                await self._schedule_fulfillment(order)
                
                # Step 10: Save order
                self.orders[order_id] = order
                
                # Track processing completion
                processing_time = (datetime.utcnow() - start_time).total_seconds()
                await self.performance_monitor.complete_order_processing(
                    order_id, processing_time, success=True
                )
                
                # Log metrics
                await self.metrics_collector.record_order_metric(
                    order_id=order_id,
                    metric_type="processing_time",
                    value=processing_time
                )
                
                logger.info(f"Order {order_id} processed successfully in {processing_time:.2f}s")
                
                return order
                
        except Exception as e:
            logger.error(f"Order processing failed for {order_id}: {e}")
            
            # Track processing failure
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            await self.performance_monitor.complete_order_processing(
                order_id, processing_time, success=False
            )
            
            # Cleanup on failure
            await self._cleanup_failed_order(order_id)
            
            raise Exception(f"Order processing failed: {str(e)}")
    
    async def update_order_status(
        self, 
        order_id: str, 
        new_status: OrderStatus, 
        update_data: Dict[str, Any],
        user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update order status with workflow triggers"""
        
        logger.info(f"Updating order {order_id} status to {new_status}")
        
        if order_id not in self.orders:
            raise Exception(f"Order {order_id} not found")
        
        order = self.orders[order_id]
        old_status = order["status"]
        
        # Validate status transition
        if not await self._validate_status_transition(old_status, new_status):
            raise Exception(f"Invalid status transition from {old_status} to {new_status}")
        
        # Update order
        order["status"] = new_status
        order["updated_at"] = datetime.utcnow()
        
        # Apply additional updates
        for key, value in update_data.items():
            if key not in ["id", "order_number", "created_at"]:
                order[key] = value
        
        # Trigger status-specific workflows
        await self._handle_status_change(order, old_status, new_status)
        
        return order
    
    async def process_fulfillment(
        self, 
        order_id: str, 
        fulfillment_data: Dict[str, Any],
        user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process order fulfillment"""
        
        logger.info(f"Processing fulfillment for order {order_id}")
        
        if order_id not in self.orders:
            raise Exception(f"Order {order_id} not found")
        
        order = self.orders[order_id]
        
        # Validate order can be fulfilled
        if order["status"] not in [OrderStatus.PROCESSING, OrderStatus.READY_TO_SHIP]:
            raise Exception(f"Order {order_id} cannot be fulfilled in status {order['status']}")
        
        try:
            # Process fulfillment through fulfillment manager
            fulfillment_result = await self.fulfillment_manager.process_fulfillment(
                order_id=order_id,
                order_items=order["items"],
                fulfillment_data=fulfillment_data
            )
            
            # Update order with fulfillment details
            if "fulfillments" not in order:
                order["fulfillments"] = []
            
            order["fulfillments"].append(fulfillment_result)
            
            # Update status based on fulfillment
            if fulfillment_result["status"] == FulfillmentStatus.SHIPPED:
                order["status"] = OrderStatus.SHIPPED
                
                # Capture payment if auto-capture is enabled
                if self.config["auto_capture_payments"]:
                    await self._capture_payment(order)
            
            order["updated_at"] = datetime.utcnow()
            
            return order
            
        except Exception as e:
            logger.error(f"Fulfillment processing failed for order {order_id}: {e}")
            raise Exception(f"Fulfillment processing failed: {str(e)}")
    
    async def process_refund(
        self, 
        order_id: str, 
        refund_data: Dict[str, Any],
        user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process order refund"""
        
        logger.info(f"Processing refund for order {order_id}")
        
        if order_id not in self.orders:
            raise Exception(f"Order {order_id} not found")
        
        order = self.orders[order_id]
        
        # Validate order can be refunded
        if order["status"] not in [OrderStatus.DELIVERED, OrderStatus.SHIPPED, OrderStatus.PAYMENT_CAPTURED]:
            raise Exception(f"Order {order_id} cannot be refunded in status {order['status']}")
        
        try:
            # Process refund through payment processor
            refund_result = await self.payment_processor.process_refund(
                order_id=order_id,
                payment_details=order["payment_details"],
                refund_data=refund_data
            )
            
            # Update inventory if items are being restocked
            if refund_data.get("restock_items", True):
                await self._restock_items(order, refund_data.get("items"))
            
            # Update order status
            if refund_result["refund_type"] == "full":
                order["status"] = OrderStatus.REFUNDED
            else:
                order["status"] = OrderStatus.PARTIALLY_REFUNDED
            
            # Update payment details
            order["payment_details"].update(refund_result["payment_update"])
            order["updated_at"] = datetime.utcnow()
            
            return order
            
        except Exception as e:
            logger.error(f"Refund processing failed for order {order_id}: {e}")
            raise Exception(f"Refund processing failed: {str(e)}")
    
    async def get_order_tracking(self, order_id: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get order tracking information"""
        
        if order_id not in self.orders:
            raise Exception(f"Order {order_id} not found")
        
        order = self.orders[order_id]
        
        # Get tracking info from fulfillment manager
        tracking_info = await self.fulfillment_manager.get_tracking_info(order_id)
        
        return {
            "order_id": order_id,
            "status": order["status"],
            "tracking_number": tracking_info.get("tracking_number"),
            "carrier": tracking_info.get("carrier"),
            "estimated_delivery": tracking_info.get("estimated_delivery"),
            "events": tracking_info.get("events", []),
            "last_updated": tracking_info.get("last_updated", datetime.utcnow())
        }
    
    async def get_order(self, order_id: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Get complete order information"""
        
        if order_id not in self.orders:
            raise Exception(f"Order {order_id} not found")
        
        return self.orders[order_id]
    
    async def list_orders(
        self, 
        user_context: Dict[str, Any],
        status_filter: Optional[OrderStatus] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """List orders with filtering and pagination"""
        
        orders = list(self.orders.values())
        
        # Apply status filter
        if status_filter:
            orders = [order for order in orders if order["status"] == status_filter]
        
        # Apply pagination
        total = len(orders)
        orders = orders[offset:offset + limit]
        
        return orders
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get health status of all services"""
        
        health_status = {}
        
        try:
            health_status["inventory_manager"] = await self.inventory_manager.get_health()
            health_status["payment_processor"] = await self.payment_processor.get_health()
            health_status["fulfillment_manager"] = await self.fulfillment_manager.get_health()
            health_status["notification_service"] = await self.notification_service.get_health()
            health_status["saleor_integration"] = await self.saleor_integration.get_health()
            health_status["ai_crew_integration"] = await self.ai_crew_integration.get_health()
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            health_status["error"] = str(e)
        
        return health_status
    
    async def get_inventory_analytics(self) -> Dict[str, Any]:
        """Get inventory analytics and insights"""
        
        return await self.inventory_manager.get_analytics()
    
    async def send_order_notifications(self, order_result: Dict[str, Any]):
        """Send order confirmation notifications"""
        
        await self.notification_service.send_order_confirmation(order_result)
    
    async def send_fulfillment_notifications(self, fulfillment_result: Dict[str, Any]):
        """Send fulfillment notifications"""
        
        await self.notification_service.send_shipping_notification(fulfillment_result)
    
    async def send_refund_notifications(self, refund_result: Dict[str, Any]):
        """Send refund notifications"""
        
        await self.notification_service.send_refund_confirmation(refund_result)
    
    # Private helper methods
    
    async def _create_order(self, order_id: str, order_data: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Create initial order object"""
        
        # Generate order number
        order_number = f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{order_id[:8].upper()}"
        
        # Calculate subtotal
        subtotal = sum(
            Decimal(str(item["unit_price"])) * item["quantity"] 
            for item in order_data["items"]
        )
        
        order = {
            "id": order_id,
            "order_number": order_number,
            "customer_id": order_data["customer_id"],
            "status": OrderStatus.PENDING,
            "items": order_data["items"],
            "billing_address": order_data["billing_address"],
            "shipping_address": order_data["shipping_address"],
            "pricing": {
                "subtotal": subtotal,
                "tax_total": Decimal("0"),
                "shipping_total": Decimal("0"),
                "discount_total": Decimal("0"),
                "total": subtotal,
                "currency": order_data["currency"],
                "tax_lines": []
            },
            "payment_method": order_data["payment_method"],
            "shipping_method": order_data["shipping_method"],
            "notes": order_data.get("notes"),
            "metadata": order_data.get("metadata", {}),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "created_by": user_context.get("user_id")
        }
        
        return order
    
    async def _assess_fraud_risk(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Assess fraud risk for the order"""
        
        # Simple fraud assessment (enhance with ML models)
        risk_score = 0.0
        factors = []
        
        # Check order value
        total_amount = order["pricing"]["total"]
        if total_amount > Decimal("500"):
            risk_score += 15.0
            factors.append("High order value")
        
        # Check billing vs shipping address
        billing = order["billing_address"]
        shipping = order["shipping_address"]
        if billing["country"] != shipping["country"]:
            risk_score += 25.0
            factors.append("Different billing and shipping countries")
        
        # Determine risk level
        if risk_score < 25:
            risk_level = FraudRiskLevel.LOW
        elif risk_score < 50:
            risk_level = FraudRiskLevel.MEDIUM
        elif risk_score < 75:
            risk_level = FraudRiskLevel.HIGH
        else:
            risk_level = FraudRiskLevel.CRITICAL
        
        requires_review = risk_score >= self.config["fraud_score_threshold"]
        
        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "factors": factors,
            "recommendations": [],
            "requires_review": requires_review,
            "assessed_at": datetime.utcnow(),
            "assessed_by": "automated"
        }
    
    async def _requires_human_review(self, order: Dict[str, Any], fraud_assessment: Dict[str, Any]) -> bool:
        """Check if order requires human review"""
        
        # High value orders
        if order["pricing"]["total"] > self.config["high_value_threshold"]:
            return True
        
        # High fraud risk
        if fraud_assessment["requires_review"]:
            return True
        
        return False
    
    async def _request_human_review(self, order: Dict[str, Any], review_type: str):
        """Request human review for the order"""
        
        logger.info(f"Requesting human review for order {order['id']}: {review_type}")
        
        # In production, this would create a review task for human operators
        # For now, we'll just log the request
        
    async def _process_inventory(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Process inventory validation and reservation"""
        
        return await self.inventory_manager.reserve_inventory(
            order_id=order["id"],
            items=order["items"]
        )
    
    async def _process_payment_authorization(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Process payment authorization"""
        
        return await self.payment_processor.authorize_payment(
            order_id=order["id"],
            amount=order["pricing"]["total"],
            payment_method=order["payment_method"],
            billing_address=order["billing_address"]
        )
    
    async def _calculate_final_pricing(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate final pricing including taxes and shipping"""
        
        # Calculate taxes (simplified)
        subtotal = order["pricing"]["subtotal"]
        tax_rate = Decimal("0.08")  # 8% tax rate
        tax_total = subtotal * tax_rate
        
        # Calculate shipping (simplified)
        shipping_total = Decimal("9.99")  # Flat rate shipping
        
        # Calculate total
        total = subtotal + tax_total + shipping_total
        
        return {
            "subtotal": subtotal,
            "tax_total": tax_total,
            "shipping_total": shipping_total,
            "discount_total": Decimal("0"),
            "total": total,
            "currency": order["pricing"]["currency"],
            "tax_lines": [
                {
                    "name": "Sales Tax",
                    "rate": tax_rate,
                    "amount": tax_total,
                    "jurisdiction": "US",
                    "tax_type": "sales"
                }
            ]
        }
    
    async def _ai_optimize_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI crew to optimize order processing"""
        
        try:
            optimization_result = await self.ai_crew_integration.optimize_order(order)
            return optimization_result
        except Exception as e:
            logger.warning(f"AI optimization failed: {e}")
            return {}
    
    async def _schedule_fulfillment(self, order: Dict[str, Any]):
        """Schedule order for fulfillment"""
        
        await self.fulfillment_manager.schedule_fulfillment(order)
    
    async def _cleanup_failed_order(self, order_id: str):
        """Cleanup resources for failed order"""
        
        try:
            # Release inventory reservation
            await self.inventory_manager.release_reservation(order_id)
            
            # Cancel payment authorization
            await self.payment_processor.cancel_authorization(order_id)
            
        except Exception as e:
            logger.error(f"Cleanup failed for order {order_id}: {e}")
    
    async def _validate_status_transition(self, old_status: OrderStatus, new_status: OrderStatus) -> bool:
        """Validate if status transition is allowed"""
        
        # Define allowed transitions (simplified)
        allowed_transitions = {
            OrderStatus.PENDING: [OrderStatus.PROCESSING, OrderStatus.CANCELLED, OrderStatus.ON_HOLD],
            OrderStatus.PROCESSING: [OrderStatus.READY_TO_SHIP, OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.READY_TO_SHIP: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.SHIPPED: [OrderStatus.IN_TRANSIT, OrderStatus.DELIVERED],
            OrderStatus.IN_TRANSIT: [OrderStatus.DELIVERED, OrderStatus.RETURNED],
            OrderStatus.DELIVERED: [OrderStatus.RETURNED, OrderStatus.REFUNDED]
        }
        
        return new_status in allowed_transitions.get(old_status, [])
    
    async def _handle_status_change(self, order: Dict[str, Any], old_status: OrderStatus, new_status: OrderStatus):
        """Handle order status change triggers"""
        
        if new_status == OrderStatus.SHIPPED:
            # Send shipping notification
            await self.notification_service.send_shipping_notification(order)
        
        elif new_status == OrderStatus.DELIVERED:
            # Send delivery confirmation
            await self.notification_service.send_delivery_confirmation(order)
        
        elif new_status == OrderStatus.CANCELLED:
            # Release inventory and refund payment
            await self._handle_cancellation(order)
    
    async def _capture_payment(self, order: Dict[str, Any]):
        """Capture authorized payment"""
        
        await self.payment_processor.capture_payment(
            order_id=order["id"],
            payment_details=order["payment_details"]
        )
        
        order["payment_details"]["status"] = PaymentStatus.CAPTURED
        order["status"] = OrderStatus.PAYMENT_CAPTURED
    
    async def _release_inventory_reservation(self, order: Dict[str, Any]):
        """Release inventory reservation"""
        
        await self.inventory_manager.release_reservation(order["id"])
    
    async def _restock_items(self, order: Dict[str, Any], item_ids: Optional[List[str]] = None):
        """Restock returned items"""
        
        items_to_restock = order["items"]
        if item_ids:
            items_to_restock = [item for item in order["items"] if item["id"] in item_ids]
        
        await self.inventory_manager.restock_items(
            order_id=order["id"],
            items=items_to_restock
        )
    
    async def _handle_cancellation(self, order: Dict[str, Any]):
        """Handle order cancellation"""
        
        # Release inventory
        await self._release_inventory_reservation(order)
        
        # Refund payment if captured
        if order.get("payment_details", {}).get("status") == PaymentStatus.CAPTURED:
            await self.payment_processor.process_refund(
                order_id=order["id"],
                payment_details=order["payment_details"],
                refund_data={"reason": "Order cancelled", "amount": order["pricing"]["total"]}
            )
    
    async def _get_processing_lock(self, order_id: str):
        """Get processing lock for order"""
        
        if order_id not in self.processing_locks:
            self.processing_locks[order_id] = asyncio.Lock()
        
        return self.processing_locks[order_id]
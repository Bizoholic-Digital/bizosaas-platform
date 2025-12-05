"""
Unified Webhook Management Service
Handles webhooks from all payment gateways with signature verification,
processing, retry logic, and failure handling for high-volume processing
"""

import asyncio
import logging
import json
import hmac
import hashlib
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Union, Any
from uuid import UUID, uuid4
import httpx

from sqlalchemy import text, select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from core.error_handler import ErrorHandler
from services.multi_payment_gateway_service import (
    multi_payment_service, PaymentGateway, PaymentStatus
)
from services.subscription_management_service import subscription_service
from services.indian_tax_compliance_service import indian_tax_service


class WebhookEventType(Enum):
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    PAYMENT_PENDING = "payment_pending"
    PAYMENT_REFUNDED = "payment_refunded"
    SUBSCRIPTION_CREATED = "subscription_created"
    SUBSCRIPTION_UPDATED = "subscription_updated"
    SUBSCRIPTION_CANCELLED = "subscription_cancelled"
    INVOICE_PAID = "invoice_paid"
    INVOICE_FAILED = "invoice_failed"
    DISPUTE_CREATED = "dispute_created"
    UNKNOWN = "unknown"


class WebhookStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"
    IGNORED = "ignored"
    RETRY = "retry"


class WebhookPriority(Enum):
    HIGH = "high"  # Payment success/failure
    MEDIUM = "medium"  # Subscription events
    LOW = "low"  # Analytics events


class WebhookManagementService:
    """Main service for managing webhooks from all payment gateways"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_handler = ErrorHandler()
        
        # Webhook processing configuration
        self.max_retries = 3
        self.retry_intervals = [60, 300, 900]  # 1 min, 5 min, 15 min
        self.processing_timeout = 30  # seconds
        
        # Gateway-specific webhook configurations
        self.gateway_configs = {
            PaymentGateway.RAZORPAY: {
                "signature_header": "X-Razorpay-Signature",
                "event_field": "event",
                "entity_field": "payload",
                "important_events": [
                    "payment.captured", "payment.failed", "subscription.charged",
                    "subscription.cancelled", "refund.created"
                ]
            },
            PaymentGateway.PAYU: {
                "signature_header": "X-PayU-Signature",
                "event_field": "status",
                "entity_field": "data",
                "important_events": [
                    "success", "failure", "pending", "cancelled"
                ]
            },
            PaymentGateway.PAYPAL: {
                "signature_header": "PAYPAL-TRANSMISSION-SIG",
                "event_field": "event_type",
                "entity_field": "resource",
                "important_events": [
                    "CHECKOUT.ORDER.COMPLETED", "CHECKOUT.ORDER.CANCELLED",
                    "BILLING.SUBSCRIPTION.CREATED", "BILLING.SUBSCRIPTION.CANCELLED"
                ]
            },
            PaymentGateway.STRIPE: {
                "signature_header": "Stripe-Signature",
                "event_field": "type",
                "entity_field": "data",
                "important_events": [
                    "payment_intent.succeeded", "payment_intent.payment_failed",
                    "invoice.payment_succeeded", "customer.subscription.deleted"
                ]
            }
        }
    
    async def receive_webhook(
        self,
        gateway: PaymentGateway,
        headers: Dict[str, str],
        payload: str,
        request_id: str = None
    ) -> Dict:
        """Receive and queue webhook for processing"""
        
        try:
            # Generate request ID if not provided
            if not request_id:
                request_id = f"wh_{uuid4().hex[:12]}"
            
            # Get signature from headers
            gateway_config = self.gateway_configs.get(gateway)
            if not gateway_config:
                return {
                    "success": False,
                    "error": f"Unsupported gateway: {gateway.value}",
                    "request_id": request_id
                }
            
            signature_header = gateway_config["signature_header"]
            signature = headers.get(signature_header)
            
            if not signature:
                return {
                    "success": False,
                    "error": f"Missing signature header: {signature_header}",
                    "request_id": request_id
                }
            
            # Parse payload to determine event type and priority
            try:
                payload_data = json.loads(payload)
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": "Invalid JSON payload",
                    "request_id": request_id
                }
            
            event_type = self._determine_event_type(gateway, payload_data)
            priority = self._determine_priority(event_type)
            
            # Store webhook event
            webhook_id = await self._store_webhook_event(
                gateway=gateway,
                event_type=event_type,
                payload=payload,
                signature=signature,
                priority=priority,
                request_id=request_id
            )
            
            # Queue for immediate processing if high priority
            if priority == WebhookPriority.HIGH:
                asyncio.create_task(self._process_webhook_async(webhook_id))
            
            return {
                "success": True,
                "webhook_id": str(webhook_id),
                "event_type": event_type.value,
                "priority": priority.value,
                "request_id": request_id
            }
            
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "webhook_management",
                "action": "receive_webhook",
                "gateway": gateway.value,
                "request_id": request_id
            })
            return {
                "success": False,
                "error": str(e),
                "request_id": request_id
            }
    
    async def process_webhook_batch(
        self,
        batch_size: int = 50,
        max_processing_time: int = 300
    ) -> Dict:
        """Process a batch of pending webhooks"""
        
        try:
            start_time = datetime.now()
            processed_count = 0
            failed_count = 0
            
            while (datetime.now() - start_time).seconds < max_processing_time:
                # Get next batch of webhooks to process
                webhooks = await self._get_pending_webhooks(batch_size)
                
                if not webhooks:
                    break
                
                # Process webhooks concurrently
                tasks = []
                for webhook in webhooks:
                    task = asyncio.create_task(
                        self._process_webhook_async(webhook["id"])
                    )
                    tasks.append(task)
                
                # Wait for batch completion
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Count results
                for result in results:
                    if isinstance(result, Exception):
                        failed_count += 1
                    elif result and result.get("success"):
                        processed_count += 1
                    else:
                        failed_count += 1
            
            return {
                "success": True,
                "processed_count": processed_count,
                "failed_count": failed_count,
                "processing_time_seconds": (datetime.now() - start_time).seconds
            }
            
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "webhook_management",
                "action": "process_webhook_batch"
            })
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _process_webhook_async(self, webhook_id: UUID) -> Dict:
        """Process a single webhook asynchronously"""
        
        try:
            # Get webhook details
            webhook = await self._get_webhook_details(webhook_id)
            if not webhook:
                return {
                    "success": False,
                    "error": "Webhook not found"
                }
            
            # Update status to processing
            await self._update_webhook_status(webhook_id, WebhookStatus.PROCESSING)
            
            # Verify webhook signature
            verification_result = await self._verify_webhook_signature(webhook)
            if not verification_result.get("verified"):
                await self._update_webhook_status(
                    webhook_id, 
                    WebhookStatus.FAILED,
                    error="Signature verification failed"
                )
                return {
                    "success": False,
                    "error": "Signature verification failed"
                }
            
            # Process webhook based on event type
            processing_result = await self._process_webhook_event(webhook)
            
            if processing_result.get("success"):
                await self._update_webhook_status(
                    webhook_id,
                    WebhookStatus.PROCESSED,
                    processing_result=processing_result
                )
                
                self.logger.info(f"Webhook processed successfully: {webhook_id}")
                return processing_result
            else:
                # Check if retry is needed
                if webhook["processing_attempts"] < self.max_retries:
                    retry_delay = self.retry_intervals[min(
                        webhook["processing_attempts"],
                        len(self.retry_intervals) - 1
                    )]
                    
                    await self._schedule_webhook_retry(webhook_id, retry_delay)
                    return {
                        "success": False,
                        "error": processing_result.get("error"),
                        "retry_scheduled": True
                    }
                else:
                    await self._update_webhook_status(
                        webhook_id,
                        WebhookStatus.FAILED,
                        error=processing_result.get("error")
                    )
                    return {
                        "success": False,
                        "error": processing_result.get("error"),
                        "max_retries_exceeded": True
                    }
            
        except Exception as e:
            await self._update_webhook_status(
                webhook_id,
                WebhookStatus.FAILED,
                error=str(e)
            )
            
            self.logger.error(f"Webhook processing failed: {webhook_id} - {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _process_webhook_event(self, webhook: Dict) -> Dict:
        """Process webhook event based on type"""
        
        try:
            event_type = WebhookEventType(webhook["event_type"])
            gateway = PaymentGateway(webhook["gateway"])
            payload_data = json.loads(webhook["payload"])
            
            # Extract relevant data from payload
            event_data = await self._extract_event_data(gateway, payload_data, event_type)
            
            if event_type == WebhookEventType.PAYMENT_SUCCESS:
                return await self._handle_payment_success(event_data, gateway)
            
            elif event_type == WebhookEventType.PAYMENT_FAILED:
                return await self._handle_payment_failed(event_data, gateway)
            
            elif event_type == WebhookEventType.PAYMENT_REFUNDED:
                return await self._handle_payment_refunded(event_data, gateway)
            
            elif event_type == WebhookEventType.SUBSCRIPTION_CREATED:
                return await self._handle_subscription_created(event_data, gateway)
            
            elif event_type == WebhookEventType.SUBSCRIPTION_CANCELLED:
                return await self._handle_subscription_cancelled(event_data, gateway)
            
            elif event_type == WebhookEventType.INVOICE_PAID:
                return await self._handle_invoice_paid(event_data, gateway)
            
            elif event_type == WebhookEventType.DISPUTE_CREATED:
                return await self._handle_dispute_created(event_data, gateway)
            
            else:
                # Log unknown events for monitoring
                self.logger.info(f"Unknown webhook event type: {event_type.value} from {gateway.value}")
                return {
                    "success": True,
                    "action": "ignored",
                    "reason": "Unknown event type"
                }
            
        except Exception as e:
            self.logger.error(f"Webhook event processing failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _handle_payment_success(self, event_data: Dict, gateway: PaymentGateway) -> Dict:
        """Handle successful payment webhook"""
        
        try:
            payment_id = event_data.get("payment_id")
            amount = Decimal(str(event_data.get("amount", 0)))
            
            if not payment_id:
                return {
                    "success": False,
                    "error": "Missing payment ID in event data"
                }
            
            # Update payment status in database
            async with get_db() as db:
                update_query = text("""
                    UPDATE payment_transactions SET
                        status = 'success',
                        captured_amount = :amount,
                        completed_at = NOW(),
                        updated_at = NOW(),
                        webhook_data = :webhook_data::JSONB
                    WHERE gateway_payment_id = :payment_id
                    AND gateway = :gateway
                    RETURNING internal_payment_id, tenant_id, transaction_type, metadata
                """)
                
                result = await db.execute(update_query, {
                    "payment_id": payment_id,
                    "amount": float(amount),
                    "gateway": gateway.value,
                    "webhook_data": json.dumps(event_data)
                })
                
                payment_record = result.first()
                if not payment_record:
                    return {
                        "success": False,
                        "error": "Payment record not found"
                    }
                
                await db.commit()
            
            # Trigger post-payment actions
            await self._trigger_payment_success_actions(
                payment_id=payment_record.internal_payment_id,
                tenant_id=UUID(payment_record.tenant_id),
                transaction_type=payment_record.transaction_type,
                amount=amount,
                metadata=payment_record.metadata or {}
            )
            
            return {
                "success": True,
                "action": "payment_updated",
                "payment_id": payment_id,
                "amount": float(amount),
                "status": "success"
            }
            
        except Exception as e:
            self.logger.error(f"Payment success handling failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _handle_payment_failed(self, event_data: Dict, gateway: PaymentGateway) -> Dict:
        """Handle failed payment webhook"""
        
        try:
            payment_id = event_data.get("payment_id")
            error_reason = event_data.get("error_reason", "Payment failed")
            
            if not payment_id:
                return {
                    "success": False,
                    "error": "Missing payment ID in event data"
                }
            
            # Update payment status in database
            async with get_db() as db:
                update_query = text("""
                    UPDATE payment_transactions SET
                        status = 'failed',
                        failed_at = NOW(),
                        updated_at = NOW(),
                        webhook_data = :webhook_data::JSONB
                    WHERE gateway_payment_id = :payment_id
                    AND gateway = :gateway
                    RETURNING internal_payment_id, tenant_id, user_id, transaction_type
                """)
                
                result = await db.execute(update_query, {
                    "payment_id": payment_id,
                    "gateway": gateway.value,
                    "webhook_data": json.dumps(event_data)
                })
                
                payment_record = result.first()
                if not payment_record:
                    return {
                        "success": False,
                        "error": "Payment record not found"
                    }
                
                await db.commit()
            
            # Trigger failure handling actions
            await self._trigger_payment_failure_actions(
                payment_id=payment_record.internal_payment_id,
                tenant_id=UUID(payment_record.tenant_id),
                user_id=UUID(payment_record.user_id) if payment_record.user_id else None,
                transaction_type=payment_record.transaction_type,
                error_reason=error_reason
            )
            
            return {
                "success": True,
                "action": "payment_failed",
                "payment_id": payment_id,
                "error_reason": error_reason
            }
            
        except Exception as e:
            self.logger.error(f"Payment failure handling failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _handle_payment_refunded(self, event_data: Dict, gateway: PaymentGateway) -> Dict:
        """Handle payment refund webhook"""
        
        try:
            payment_id = event_data.get("payment_id")
            refund_amount = Decimal(str(event_data.get("refund_amount", 0)))
            refund_id = event_data.get("refund_id")
            
            # Update payment and create refund record
            async with get_db() as db:
                # Update payment transaction
                update_payment_query = text("""
                    UPDATE payment_transactions SET
                        refunded_amount = refunded_amount + :refund_amount,
                        status = CASE 
                            WHEN (refunded_amount + :refund_amount) >= captured_amount THEN 'refunded'
                            ELSE 'partial_refunded'
                        END,
                        refunded_at = NOW(),
                        updated_at = NOW()
                    WHERE gateway_payment_id = :payment_id
                    AND gateway = :gateway
                    RETURNING internal_payment_id, tenant_id
                """)
                
                payment_result = await db.execute(update_payment_query, {
                    "payment_id": payment_id,
                    "refund_amount": float(refund_amount),
                    "gateway": gateway.value
                })
                
                payment_record = payment_result.first()
                if not payment_record:
                    return {
                        "success": False,
                        "error": "Payment record not found"
                    }
                
                # Create refund record if not exists
                refund_query = text("""
                    INSERT INTO payment_refunds (
                        payment_id, tenant_id, gateway, gateway_refund_id, 
                        refund_amount, status, gateway_response, completed_at
                    ) VALUES (
                        :payment_id, :tenant_id, :gateway, :gateway_refund_id,
                        :refund_amount, 'completed', :gateway_response::JSONB, NOW()
                    ) ON CONFLICT (gateway, gateway_refund_id) DO UPDATE SET
                        status = 'completed',
                        completed_at = NOW()
                    RETURNING id
                """)
                
                await db.execute(refund_query, {
                    "payment_id": payment_record.internal_payment_id,
                    "tenant_id": payment_record.tenant_id,
                    "gateway": gateway.value,
                    "gateway_refund_id": refund_id,
                    "refund_amount": float(refund_amount),
                    "gateway_response": json.dumps(event_data)
                })
                
                await db.commit()
            
            return {
                "success": True,
                "action": "refund_processed",
                "payment_id": payment_id,
                "refund_amount": float(refund_amount),
                "refund_id": refund_id
            }
            
        except Exception as e:
            self.logger.error(f"Refund handling failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _handle_subscription_created(self, event_data: Dict, gateway: PaymentGateway) -> Dict:
        """Handle subscription created webhook"""
        
        try:
            subscription_id = event_data.get("subscription_id")
            customer_id = event_data.get("customer_id")
            
            # Update subscription status
            async with get_db() as db:
                update_query = text("""
                    UPDATE enhanced_subscriptions SET
                        status = 'active',
                        gateway_customer_id = :customer_id,
                        activated_at = NOW(),
                        updated_at = NOW()
                    WHERE gateway_subscription_id = :subscription_id
                    AND payment_gateway = :gateway
                    RETURNING id, tenant_id
                """)
                
                result = await db.execute(update_query, {
                    "subscription_id": subscription_id,
                    "customer_id": customer_id,
                    "gateway": gateway.value
                })
                
                subscription_record = result.first()
                if subscription_record:
                    await db.commit()
                    return {
                        "success": True,
                        "action": "subscription_activated",
                        "subscription_id": subscription_id
                    }
                
            return {
                "success": False,
                "error": "Subscription not found"
            }
            
        except Exception as e:
            self.logger.error(f"Subscription creation handling failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _handle_subscription_cancelled(self, event_data: Dict, gateway: PaymentGateway) -> Dict:
        """Handle subscription cancelled webhook"""
        
        try:
            subscription_id = event_data.get("subscription_id")
            cancellation_reason = event_data.get("reason", "Gateway cancellation")
            
            # Update subscription status
            async with get_db() as db:
                update_query = text("""
                    UPDATE enhanced_subscriptions SET
                        status = 'cancelled',
                        cancelled_at = NOW(),
                        cancelled_reason = :reason,
                        updated_at = NOW()
                    WHERE gateway_subscription_id = :subscription_id
                    AND payment_gateway = :gateway
                    RETURNING id, tenant_id, user_id
                """)
                
                result = await db.execute(update_query, {
                    "subscription_id": subscription_id,
                    "reason": cancellation_reason,
                    "gateway": gateway.value
                })
                
                subscription_record = result.first()
                if subscription_record:
                    await db.commit()
                    
                    # Trigger subscription cancellation actions
                    await self._trigger_subscription_cancelled_actions(
                        subscription_id=UUID(subscription_record.id),
                        tenant_id=UUID(subscription_record.tenant_id),
                        user_id=UUID(subscription_record.user_id) if subscription_record.user_id else None,
                        reason=cancellation_reason
                    )
                    
                    return {
                        "success": True,
                        "action": "subscription_cancelled",
                        "subscription_id": subscription_id,
                        "reason": cancellation_reason
                    }
                
            return {
                "success": False,
                "error": "Subscription not found"
            }
            
        except Exception as e:
            self.logger.error(f"Subscription cancellation handling failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _handle_invoice_paid(self, event_data: Dict, gateway: PaymentGateway) -> Dict:
        """Handle invoice paid webhook"""
        
        try:
            invoice_id = event_data.get("invoice_id")
            amount_paid = Decimal(str(event_data.get("amount_paid", 0)))
            
            # Update invoice status
            async with get_db() as db:
                update_query = text("""
                    UPDATE invoices SET
                        status = 'paid',
                        paid_at = NOW(),
                        updated_at = NOW()
                    WHERE id = :invoice_id
                    RETURNING id, tenant_id
                """)
                
                result = await db.execute(update_query, {
                    "invoice_id": invoice_id
                })
                
                invoice_record = result.first()
                if invoice_record:
                    await db.commit()
                    return {
                        "success": True,
                        "action": "invoice_paid",
                        "invoice_id": invoice_id,
                        "amount_paid": float(amount_paid)
                    }
                
            return {
                "success": False,
                "error": "Invoice not found"
            }
            
        except Exception as e:
            self.logger.error(f"Invoice paid handling failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _handle_dispute_created(self, event_data: Dict, gateway: PaymentGateway) -> Dict:
        """Handle dispute/chargeback webhook"""
        
        try:
            payment_id = event_data.get("payment_id")
            dispute_id = event_data.get("dispute_id")
            amount = Decimal(str(event_data.get("amount", 0)))
            reason = event_data.get("reason", "Dispute created")
            
            # Create dispute record
            async with get_db() as db:
                # Get payment details
                payment_query = text("""
                    SELECT internal_payment_id, tenant_id 
                    FROM payment_transactions 
                    WHERE gateway_payment_id = :payment_id AND gateway = :gateway
                """)
                
                payment_result = await db.execute(payment_query, {
                    "payment_id": payment_id,
                    "gateway": gateway.value
                })
                
                payment_record = payment_result.first()
                if not payment_record:
                    return {
                        "success": False,
                        "error": "Payment not found for dispute"
                    }
                
                # Create dispute record (table would need to be created)
                dispute_query = text("""
                    INSERT INTO payment_disputes (
                        payment_id, tenant_id, gateway, gateway_dispute_id,
                        amount, reason, status, created_at
                    ) VALUES (
                        :payment_id, :tenant_id, :gateway, :dispute_id,
                        :amount, :reason, 'open', NOW()
                    ) ON CONFLICT (gateway, gateway_dispute_id) DO NOTHING
                    RETURNING id
                """)
                
                await db.execute(dispute_query, {
                    "payment_id": payment_record.internal_payment_id,
                    "tenant_id": payment_record.tenant_id,
                    "gateway": gateway.value,
                    "dispute_id": dispute_id,
                    "amount": float(amount),
                    "reason": reason
                })
                
                await db.commit()
            
            # Trigger dispute notification
            await self._trigger_dispute_notifications(
                payment_id=payment_record.internal_payment_id,
                tenant_id=UUID(payment_record.tenant_id),
                dispute_id=dispute_id,
                amount=amount,
                reason=reason
            )
            
            return {
                "success": True,
                "action": "dispute_created",
                "dispute_id": dispute_id,
                "payment_id": payment_id,
                "amount": float(amount)
            }
            
        except Exception as e:
            self.logger.error(f"Dispute handling failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _determine_event_type(self, gateway: PaymentGateway, payload_data: Dict) -> WebhookEventType:
        """Determine webhook event type from payload"""
        
        gateway_config = self.gateway_configs.get(gateway)
        if not gateway_config:
            return WebhookEventType.UNKNOWN
        
        event_field = gateway_config["event_field"]
        event_value = payload_data.get(event_field, "").lower()
        
        # Gateway-specific event mapping
        if gateway == PaymentGateway.RAZORPAY:
            if event_value == "payment.captured":
                return WebhookEventType.PAYMENT_SUCCESS
            elif event_value == "payment.failed":
                return WebhookEventType.PAYMENT_FAILED
            elif event_value == "refund.created":
                return WebhookEventType.PAYMENT_REFUNDED
            elif event_value == "subscription.charged":
                return WebhookEventType.PAYMENT_SUCCESS
            elif event_value == "subscription.cancelled":
                return WebhookEventType.SUBSCRIPTION_CANCELLED
        
        elif gateway == PaymentGateway.PAYU:
            if event_value == "success":
                return WebhookEventType.PAYMENT_SUCCESS
            elif event_value in ["failure", "cancelled"]:
                return WebhookEventType.PAYMENT_FAILED
            elif event_value == "pending":
                return WebhookEventType.PAYMENT_PENDING
        
        elif gateway == PaymentGateway.PAYPAL:
            if event_value == "checkout.order.completed":
                return WebhookEventType.PAYMENT_SUCCESS
            elif event_value == "checkout.order.cancelled":
                return WebhookEventType.PAYMENT_FAILED
            elif event_value == "billing.subscription.created":
                return WebhookEventType.SUBSCRIPTION_CREATED
            elif event_value == "billing.subscription.cancelled":
                return WebhookEventType.SUBSCRIPTION_CANCELLED
        
        elif gateway == PaymentGateway.STRIPE:
            if event_value == "payment_intent.succeeded":
                return WebhookEventType.PAYMENT_SUCCESS
            elif event_value == "payment_intent.payment_failed":
                return WebhookEventType.PAYMENT_FAILED
            elif event_value == "invoice.payment_succeeded":
                return WebhookEventType.INVOICE_PAID
            elif event_value == "customer.subscription.deleted":
                return WebhookEventType.SUBSCRIPTION_CANCELLED
        
        return WebhookEventType.UNKNOWN
    
    def _determine_priority(self, event_type: WebhookEventType) -> WebhookPriority:
        """Determine webhook processing priority"""
        
        high_priority_events = [
            WebhookEventType.PAYMENT_SUCCESS,
            WebhookEventType.PAYMENT_FAILED,
            WebhookEventType.PAYMENT_REFUNDED,
            WebhookEventType.DISPUTE_CREATED
        ]
        
        medium_priority_events = [
            WebhookEventType.SUBSCRIPTION_CREATED,
            WebhookEventType.SUBSCRIPTION_CANCELLED,
            WebhookEventType.INVOICE_PAID
        ]
        
        if event_type in high_priority_events:
            return WebhookPriority.HIGH
        elif event_type in medium_priority_events:
            return WebhookPriority.MEDIUM
        else:
            return WebhookPriority.LOW
    
    async def _store_webhook_event(
        self,
        gateway: PaymentGateway,
        event_type: WebhookEventType,
        payload: str,
        signature: str,
        priority: WebhookPriority,
        request_id: str
    ) -> UUID:
        """Store webhook event in database"""
        
        try:
            async with get_db() as db:
                insert_query = text("""
                    INSERT INTO payment_webhook_events (
                        gateway, event_type, payload, signature, processing_status,
                        processing_attempts, priority, request_id, received_at
                    ) VALUES (
                        :gateway, :event_type, :payload::JSONB, :signature, 'pending',
                        0, :priority, :request_id, NOW()
                    ) RETURNING id
                """)
                
                result = await db.execute(insert_query, {
                    "gateway": gateway.value,
                    "event_type": event_type.value,
                    "payload": payload,
                    "signature": signature,
                    "priority": priority.value,
                    "request_id": request_id
                })
                
                webhook_id = result.scalar()
                await db.commit()
                
                return UUID(webhook_id)
                
        except Exception as e:
            self.logger.error(f"Failed to store webhook event: {e}")
            raise
    
    async def _get_pending_webhooks(self, limit: int = 50) -> List[Dict]:
        """Get pending webhooks for processing"""
        
        try:
            async with get_db() as db:
                query = text("""
                    SELECT id, gateway, event_type, payload, signature, processing_attempts, priority
                    FROM payment_webhook_events
                    WHERE processing_status = 'pending'
                    OR (processing_status = 'retry' AND next_retry_at <= NOW())
                    ORDER BY priority DESC, received_at ASC
                    LIMIT :limit
                """)
                
                result = await db.execute(query, {"limit": limit})
                
                webhooks = []
                for row in result:
                    webhooks.append({
                        "id": UUID(row.id),
                        "gateway": row.gateway,
                        "event_type": row.event_type,
                        "payload": row.payload,
                        "signature": row.signature,
                        "processing_attempts": row.processing_attempts,
                        "priority": row.priority
                    })
                
                return webhooks
                
        except Exception as e:
            self.logger.error(f"Failed to get pending webhooks: {e}")
            return []
    
    async def _get_webhook_details(self, webhook_id: UUID) -> Optional[Dict]:
        """Get webhook details by ID"""
        
        try:
            async with get_db() as db:
                query = text("""
                    SELECT * FROM payment_webhook_events 
                    WHERE id = :webhook_id
                """)
                
                result = await db.execute(query, {"webhook_id": str(webhook_id)})
                row = result.first()
                
                if row:
                    return {
                        "id": UUID(row.id),
                        "gateway": row.gateway,
                        "event_type": row.event_type,
                        "payload": row.payload,
                        "signature": row.signature,
                        "processing_attempts": row.processing_attempts,
                        "processing_status": row.processing_status,
                        "verification_status": row.verification_status,
                        "received_at": row.received_at
                    }
                
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to get webhook details: {e}")
            return None
    
    async def _verify_webhook_signature(self, webhook: Dict) -> Dict:
        """Verify webhook signature"""
        
        try:
            gateway = PaymentGateway(webhook["gateway"])
            payload = webhook["payload"]
            signature = webhook["signature"]
            
            # Use the multi-payment service to verify signature
            verification_result = await multi_payment_service.process_webhook(
                gateway=gateway,
                payload=payload,
                signature=signature
            )
            
            # Update verification status
            await self._update_webhook_verification_status(
                webhook["id"],
                "verified" if verification_result.get("success") else "failed"
            )
            
            return {
                "verified": verification_result.get("success", False),
                "error": verification_result.get("error") if not verification_result.get("success") else None
            }
            
        except Exception as e:
            self.logger.error(f"Webhook signature verification failed: {e}")
            return {
                "verified": False,
                "error": str(e)
            }
    
    async def _extract_event_data(
        self,
        gateway: PaymentGateway,
        payload_data: Dict,
        event_type: WebhookEventType
    ) -> Dict:
        """Extract relevant data from webhook payload"""
        
        try:
            gateway_config = self.gateway_configs.get(gateway)
            entity_field = gateway_config["entity_field"]
            entity_data = payload_data.get(entity_field, {})
            
            # Common data extraction
            extracted_data = {
                "raw_payload": payload_data,
                "timestamp": datetime.now().isoformat()
            }
            
            # Gateway-specific data extraction
            if gateway == PaymentGateway.RAZORPAY:
                if event_type in [WebhookEventType.PAYMENT_SUCCESS, WebhookEventType.PAYMENT_FAILED]:
                    payment_entity = entity_data.get("payment", {}).get("entity", {})
                    extracted_data.update({
                        "payment_id": payment_entity.get("id"),
                        "order_id": payment_entity.get("order_id"),
                        "amount": payment_entity.get("amount", 0) / 100,  # Convert from paise
                        "currency": payment_entity.get("currency"),
                        "method": payment_entity.get("method"),
                        "status": payment_entity.get("status"),
                        "error_reason": payment_entity.get("error_description")
                    })
                
                elif event_type == WebhookEventType.PAYMENT_REFUNDED:
                    refund_entity = entity_data.get("refund", {}).get("entity", {})
                    extracted_data.update({
                        "refund_id": refund_entity.get("id"),
                        "payment_id": refund_entity.get("payment_id"),
                        "refund_amount": refund_entity.get("amount", 0) / 100,
                        "currency": refund_entity.get("currency")
                    })
            
            elif gateway == PaymentGateway.PAYU:
                extracted_data.update({
                    "payment_id": payload_data.get("txnid"),
                    "amount": float(payload_data.get("amount", 0)),
                    "currency": "INR",
                    "status": payload_data.get("status"),
                    "method": payload_data.get("mode"),
                    "error_reason": payload_data.get("error_Message")
                })
            
            elif gateway == PaymentGateway.PAYPAL:
                if event_type == WebhookEventType.PAYMENT_SUCCESS:
                    extracted_data.update({
                        "payment_id": entity_data.get("id"),
                        "amount": float(entity_data.get("purchase_units", [{}])[0].get("amount", {}).get("value", 0)),
                        "currency": entity_data.get("purchase_units", [{}])[0].get("amount", {}).get("currency_code"),
                        "status": entity_data.get("status")
                    })
                
                elif event_type in [WebhookEventType.SUBSCRIPTION_CREATED, WebhookEventType.SUBSCRIPTION_CANCELLED]:
                    extracted_data.update({
                        "subscription_id": entity_data.get("id"),
                        "status": entity_data.get("status"),
                        "customer_id": entity_data.get("subscriber", {}).get("payer_id")
                    })
            
            elif gateway == PaymentGateway.STRIPE:
                if event_type in [WebhookEventType.PAYMENT_SUCCESS, WebhookEventType.PAYMENT_FAILED]:
                    payment_intent = entity_data.get("object", {})
                    extracted_data.update({
                        "payment_id": payment_intent.get("id"),
                        "amount": payment_intent.get("amount", 0) / 100,  # Convert from cents
                        "currency": payment_intent.get("currency"),
                        "status": payment_intent.get("status"),
                        "error_reason": payment_intent.get("last_payment_error", {}).get("message")
                    })
            
            return extracted_data
            
        except Exception as e:
            self.logger.error(f"Event data extraction failed: {e}")
            return {
                "raw_payload": payload_data,
                "extraction_error": str(e)
            }
    
    async def _update_webhook_status(
        self,
        webhook_id: UUID,
        status: WebhookStatus,
        error: str = None,
        processing_result: Dict = None
    ):
        """Update webhook processing status"""
        
        try:
            async with get_db() as db:
                update_fields = [
                    "processing_status = :status",
                    "processing_attempts = processing_attempts + 1",
                    "updated_at = NOW()"
                ]
                params = {
                    "webhook_id": str(webhook_id),
                    "status": status.value
                }
                
                if status == WebhookStatus.PROCESSED:
                    update_fields.append("processed_at = NOW()")
                
                if error:
                    update_fields.append("processing_error = :error")
                    params["error"] = error
                
                if processing_result:
                    update_fields.append("processing_result = :result::JSONB")
                    params["result"] = json.dumps(processing_result)
                
                query = text(f"""
                    UPDATE payment_webhook_events 
                    SET {', '.join(update_fields)}
                    WHERE id = :webhook_id
                """)
                
                await db.execute(query, params)
                await db.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to update webhook status: {e}")
    
    async def _update_webhook_verification_status(self, webhook_id: UUID, status: str):
        """Update webhook verification status"""
        
        try:
            async with get_db() as db:
                query = text("""
                    UPDATE payment_webhook_events 
                    SET verification_status = :status
                    WHERE id = :webhook_id
                """)
                
                await db.execute(query, {
                    "webhook_id": str(webhook_id),
                    "status": status
                })
                await db.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to update verification status: {e}")
    
    async def _schedule_webhook_retry(self, webhook_id: UUID, delay_seconds: int):
        """Schedule webhook retry"""
        
        try:
            retry_time = datetime.now() + timedelta(seconds=delay_seconds)
            
            async with get_db() as db:
                query = text("""
                    UPDATE payment_webhook_events 
                    SET processing_status = 'retry',
                        next_retry_at = :retry_time
                    WHERE id = :webhook_id
                """)
                
                await db.execute(query, {
                    "webhook_id": str(webhook_id),
                    "retry_time": retry_time
                })
                await db.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to schedule webhook retry: {e}")
    
    async def _trigger_payment_success_actions(
        self,
        payment_id: UUID,
        tenant_id: UUID,
        transaction_type: str,
        amount: Decimal,
        metadata: Dict
    ):
        """Trigger actions after successful payment"""
        
        try:
            # Update subscription if this was a subscription payment
            if transaction_type == "subscription":
                subscription_id = metadata.get("subscription_id")
                if subscription_id:
                    await subscription_service.process_subscription_billing(
                        subscription_id=UUID(subscription_id)
                    )
            
            # Generate invoice for Indian customers
            if transaction_type in ["subscription", "usage_billing"]:
                # This would trigger invoice generation
                pass
            
            # Update revenue metrics (refresh materialized views)
            # This could be done asynchronously
            pass
            
        except Exception as e:
            self.logger.error(f"Payment success actions failed: {e}")
    
    async def _trigger_payment_failure_actions(
        self,
        payment_id: UUID,
        tenant_id: UUID,
        user_id: UUID,
        transaction_type: str,
        error_reason: str
    ):
        """Trigger actions after payment failure"""
        
        try:
            # Handle subscription payment failures
            if transaction_type == "subscription":
                # Mark subscription as past due
                # Send notification to customer
                # Implement dunning management
                pass
            
            # Send failure notification
            # Log for fraud analysis
            # Update failure metrics
            
        except Exception as e:
            self.logger.error(f"Payment failure actions failed: {e}")
    
    async def _trigger_subscription_cancelled_actions(
        self,
        subscription_id: UUID,
        tenant_id: UUID,
        user_id: UUID,
        reason: str
    ):
        """Trigger actions after subscription cancellation"""
        
        try:
            # Send cancellation confirmation
            # Update revenue metrics
            # Trigger retention campaigns
            # Archive subscription data
            
        except Exception as e:
            self.logger.error(f"Subscription cancellation actions failed: {e}")
    
    async def _trigger_dispute_notifications(
        self,
        payment_id: UUID,
        tenant_id: UUID,
        dispute_id: str,
        amount: Decimal,
        reason: str
    ):
        """Trigger dispute/chargeback notifications"""
        
        try:
            # Send immediate notification to admin
            # Create support ticket
            # Flag for manual review
            # Update risk metrics
            
        except Exception as e:
            self.logger.error(f"Dispute notification failed: {e}")
    
    async def get_webhook_statistics(
        self,
        gateway: PaymentGateway = None,
        days: int = 7
    ) -> Dict:
        """Get webhook processing statistics"""
        
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            async with get_db() as db:
                gateway_filter = "AND gateway = :gateway" if gateway else ""
                gateway_params = {"gateway": gateway.value} if gateway else {}
                
                stats_query = text(f"""
                    SELECT 
                        gateway,
                        COUNT(*) as total_webhooks,
                        COUNT(*) FILTER (WHERE processing_status = 'processed') as processed,
                        COUNT(*) FILTER (WHERE processing_status = 'failed') as failed,
                        COUNT(*) FILTER (WHERE processing_status = 'pending') as pending,
                        COUNT(*) FILTER (WHERE verification_status = 'verified') as verified,
                        COUNT(*) FILTER (WHERE verification_status = 'failed') as verification_failed,
                        AVG(EXTRACT(EPOCH FROM (processed_at - received_at))) FILTER (WHERE processed_at IS NOT NULL) as avg_processing_time_seconds
                    FROM payment_webhook_events
                    WHERE received_at >= :start_date
                    {gateway_filter}
                    GROUP BY gateway
                    ORDER BY total_webhooks DESC
                """)
                
                result = await db.execute(stats_query, {
                    "start_date": start_date,
                    **gateway_params
                })
                
                statistics = []
                for row in result:
                    success_rate = (row.processed / max(row.total_webhooks, 1)) * 100
                    verification_rate = (row.verified / max(row.total_webhooks, 1)) * 100
                    
                    statistics.append({
                        "gateway": row.gateway,
                        "total_webhooks": row.total_webhooks,
                        "processed": row.processed,
                        "failed": row.failed,
                        "pending": row.pending,
                        "success_rate": round(success_rate, 2),
                        "verification_rate": round(verification_rate, 2),
                        "avg_processing_time": round(float(row.avg_processing_time_seconds or 0), 2)
                    })
                
                return {
                    "success": True,
                    "period_days": days,
                    "statistics": statistics,
                    "generated_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "webhook_management",
                "action": "get_webhook_statistics"
            })
            return {
                "success": False,
                "error": str(e)
            }


# Add webhook priority column to existing table
async def add_webhook_priority_column():
    """Add priority column to webhook events table"""
    
    try:
        async with get_db() as db:
            alter_query = text("""
                ALTER TABLE payment_webhook_events 
                ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium',
                ADD COLUMN IF NOT EXISTS request_id VARCHAR(50),
                ADD COLUMN IF NOT EXISTS next_retry_at TIMESTAMP,
                ADD COLUMN IF NOT EXISTS processing_result JSONB,
                ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW()
            """)
            
            await db.execute(alter_query)
            await db.commit()
            
            # Create index on priority for faster processing
            index_query = text("""
                CREATE INDEX IF NOT EXISTS idx_webhook_events_priority_status 
                ON payment_webhook_events (priority DESC, processing_status, received_at)
            """)
            
            await db.execute(index_query)
            await db.commit()
            
    except Exception as e:
        logging.error(f"Failed to add webhook priority column: {e}")


# Create payment disputes table
async def create_payment_disputes_table():
    """Create payment disputes table"""
    
    try:
        async with get_db() as db:
            create_table_query = text("""
                CREATE TABLE IF NOT EXISTS payment_disputes (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    payment_id UUID REFERENCES payment_transactions(internal_payment_id) ON DELETE CASCADE,
                    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
                    gateway VARCHAR(50) NOT NULL,
                    gateway_dispute_id VARCHAR(255) NOT NULL,
                    amount DECIMAL(15,2) NOT NULL,
                    currency VARCHAR(3) DEFAULT 'INR',
                    reason TEXT,
                    status VARCHAR(50) DEFAULT 'open',
                    evidence JSONB,
                    resolution TEXT,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    resolved_at TIMESTAMP,
                    
                    INDEX idx_payment_disputes_payment_id (payment_id),
                    INDEX idx_payment_disputes_gateway (gateway),
                    INDEX idx_payment_disputes_status (status),
                    UNIQUE(gateway, gateway_dispute_id)
                )
            """)
            
            await db.execute(create_table_query)
            await db.commit()
            
    except Exception as e:
        logging.error(f"Failed to create payment disputes table: {e}")


# Global instance
webhook_service = WebhookManagementService()
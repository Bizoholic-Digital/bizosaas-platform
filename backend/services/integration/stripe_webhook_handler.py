"""
Comprehensive Stripe Webhook Handler for Payment Processing
Handles all payment events for production revenue management
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any
from uuid import UUID

import stripe
from sqlalchemy import text
from database import get_db


class StripeWebhookHandler:
    """Handle all Stripe webhook events for payment processing"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Event handlers mapping
        self.event_handlers = {
            # Payment and Invoice Events
            'invoice.payment_succeeded': self._handle_payment_succeeded,
            'invoice.payment_failed': self._handle_payment_failed,
            'invoice.created': self._handle_invoice_created,
            'invoice.finalized': self._handle_invoice_finalized,
            'invoice.updated': self._handle_invoice_updated,
            
            # Subscription Events
            'customer.subscription.created': self._handle_subscription_created,
            'customer.subscription.updated': self._handle_subscription_updated,
            'customer.subscription.deleted': self._handle_subscription_deleted,
            'customer.subscription.trial_will_end': self._handle_trial_ending,
            
            # Customer Events
            'customer.created': self._handle_customer_created,
            'customer.updated': self._handle_customer_updated,
            'customer.deleted': self._handle_customer_deleted,
            
            # Checkout Events
            'checkout.session.completed': self._handle_checkout_completed,
            'checkout.session.expired': self._handle_checkout_expired,
            
            # Payment Method Events
            'payment_method.attached': self._handle_payment_method_attached,
            'payment_method.detached': self._handle_payment_method_detached,
            
            # Dispute Events
            'charge.dispute.created': self._handle_dispute_created,
            
            # Usage Record Events (for usage-based billing)
            'usage_record.created': self._handle_usage_record_created
        }
    
    async def process_webhook(self, payload: str, signature: str, webhook_secret: str) -> Dict[str, Any]:
        """Process incoming Stripe webhook"""
        try:
            # Verify webhook signature
            event = stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            
            event_type = event['type']
            event_data = event['data']['object']
            
            self.logger.info(f"Processing webhook event: {event_type}")
            
            # Store webhook event for audit
            await self._store_webhook_event(event)
            
            # Handle the event
            if event_type in self.event_handlers:
                result = await self.event_handlers[event_type](event_data)
                self.logger.info(f"Successfully processed {event_type}")
                return {'success': True, 'event_type': event_type, 'result': result}
            else:
                self.logger.warning(f"Unhandled webhook event type: {event_type}")
                return {'success': True, 'event_type': event_type, 'message': 'Event type not handled'}
        
        except stripe.error.SignatureVerificationError as e:
            self.logger.error(f"Webhook signature verification failed: {e}")
            return {'success': False, 'error': 'Invalid signature'}
        except Exception as e:
            self.logger.error(f"Webhook processing failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _store_webhook_event(self, event: Dict[str, Any]) -> None:
        """Store webhook event for audit and debugging"""
        try:
            async with get_db() as db:
                query = text("""
                    INSERT INTO webhook_events (event_type, source, payload, status)
                    VALUES (:event_type, 'stripe', :payload, 'received')
                """)
                
                await db.execute(query, {
                    'event_type': event['type'],
                    'payload': json.dumps(event)
                })
                await db.commit()
        except Exception as e:
            self.logger.error(f"Failed to store webhook event: {e}")
    
    # Payment and Invoice Event Handlers
    async def _handle_payment_succeeded(self, invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Handle successful payment"""
        try:
            async with get_db() as db:
                # Update subscription status
                if invoice.get('subscription'):
                    update_query = text("""
                        UPDATE subscriptions 
                        SET status = 'active',
                            updated_at = NOW()
                        WHERE stripe_subscription_id = :subscription_id
                    """)
                    
                    await db.execute(update_query, {
                        'subscription_id': invoice['subscription']
                    })
                
                # Update billing cycle if exists
                if invoice.get('id'):
                    billing_query = text("""
                        UPDATE billing_cycles 
                        SET status = 'paid',
                            paid_at = NOW(),
                            updated_at = NOW()
                        WHERE stripe_invoice_id = :invoice_id
                    """)
                    
                    await db.execute(billing_query, {
                        'invoice_id': invoice['id']
                    })
                
                # Update tenant status to active
                tenant_query = text("""
                    UPDATE tenants t
                    SET status = 'active'
                    FROM subscriptions s
                    WHERE s.tenant_id = t.id 
                    AND s.stripe_subscription_id = :subscription_id
                """)
                
                await db.execute(tenant_query, {
                    'subscription_id': invoice.get('subscription')
                })
                
                await db.commit()
                
                # Send payment confirmation email
                await self._send_payment_confirmation_email(invoice)
                
                return {'status': 'payment_processed', 'invoice_id': invoice['id']}
                
        except Exception as e:
            self.logger.error(f"Failed to process payment success: {e}")
            raise
    
    async def _handle_payment_failed(self, invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Handle failed payment"""
        try:
            async with get_db() as db:
                # Update subscription status
                if invoice.get('subscription'):
                    update_query = text("""
                        UPDATE subscriptions 
                        SET status = 'past_due',
                            updated_at = NOW()
                        WHERE stripe_subscription_id = :subscription_id
                    """)
                    
                    await db.execute(update_query, {
                        'subscription_id': invoice['subscription']
                    })
                
                # Update billing cycle
                if invoice.get('id'):
                    billing_query = text("""
                        UPDATE billing_cycles 
                        SET status = 'failed',
                            updated_at = NOW()
                        WHERE stripe_invoice_id = :invoice_id
                    """)
                    
                    await db.execute(billing_query, {
                        'invoice_id': invoice['id']
                    })
                
                await db.commit()
                
                # Send payment failure notification
                await self._send_payment_failure_notification(invoice)
                
                return {'status': 'payment_failed', 'invoice_id': invoice['id']}
                
        except Exception as e:
            self.logger.error(f"Failed to process payment failure: {e}")
            raise
    
    async def _handle_invoice_created(self, invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Handle invoice creation"""
        try:
            # Log invoice creation for tracking
            self.logger.info(f"Invoice created: {invoice['id']} for {invoice['amount_due']/100}")
            return {'status': 'invoice_logged'}
        except Exception as e:
            self.logger.error(f"Failed to process invoice creation: {e}")
            raise
    
    async def _handle_invoice_finalized(self, invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Handle invoice finalization"""
        try:
            # Send invoice to customer if auto-send is enabled
            self.logger.info(f"Invoice finalized: {invoice['id']}")
            return {'status': 'invoice_finalized'}
        except Exception as e:
            self.logger.error(f"Failed to process invoice finalization: {e}")
            raise
    
    async def _handle_invoice_updated(self, invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Handle invoice updates"""
        try:
            async with get_db() as db:
                # Update local invoice record if exists
                update_query = text("""
                    UPDATE billing_cycles 
                    SET total_amount = :amount,
                        due_date = :due_date,
                        updated_at = NOW()
                    WHERE stripe_invoice_id = :invoice_id
                """)
                
                await db.execute(update_query, {
                    'amount': invoice['amount_due'] / 100,  # Convert from cents
                    'due_date': datetime.fromtimestamp(invoice['due_date']) if invoice.get('due_date') else None,
                    'invoice_id': invoice['id']
                })
                
                await db.commit()
                
                return {'status': 'invoice_updated'}
                
        except Exception as e:
            self.logger.error(f"Failed to process invoice update: {e}")
            raise
    
    # Subscription Event Handlers
    async def _handle_subscription_created(self, subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Handle subscription creation"""
        try:
            async with get_db() as db:
                # Update or create subscription record
                upsert_query = text("""
                    INSERT INTO subscriptions (
                        tenant_id, stripe_subscription_id, stripe_customer_id,
                        status, current_period_start, current_period_end
                    ) VALUES (
                        (SELECT tenant_id FROM users WHERE stripe_customer_id = :customer_id LIMIT 1),
                        :subscription_id, :customer_id, :status,
                        to_timestamp(:period_start), to_timestamp(:period_end)
                    )
                    ON CONFLICT (stripe_subscription_id)
                    DO UPDATE SET
                        status = EXCLUDED.status,
                        current_period_start = EXCLUDED.current_period_start,
                        current_period_end = EXCLUDED.current_period_end,
                        updated_at = NOW()
                """)
                
                await db.execute(upsert_query, {
                    'subscription_id': subscription['id'],
                    'customer_id': subscription['customer'],
                    'status': subscription['status'],
                    'period_start': subscription['current_period_start'],
                    'period_end': subscription['current_period_end']
                })
                
                await db.commit()
                
                return {'status': 'subscription_created', 'subscription_id': subscription['id']}
                
        except Exception as e:
            self.logger.error(f"Failed to process subscription creation: {e}")
            raise
    
    async def _handle_subscription_updated(self, subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Handle subscription updates"""
        try:
            async with get_db() as db:
                update_query = text("""
                    UPDATE subscriptions 
                    SET status = :status,
                        current_period_start = to_timestamp(:period_start),
                        current_period_end = to_timestamp(:period_end),
                        cancel_at_period_end = :cancel_at_period_end,
                        updated_at = NOW()
                    WHERE stripe_subscription_id = :subscription_id
                """)
                
                await db.execute(update_query, {
                    'status': subscription['status'],
                    'period_start': subscription['current_period_start'],
                    'period_end': subscription['current_period_end'],
                    'cancel_at_period_end': subscription.get('cancel_at_period_end', False),
                    'subscription_id': subscription['id']
                })
                
                await db.commit()
                
                return {'status': 'subscription_updated', 'subscription_id': subscription['id']}
                
        except Exception as e:
            self.logger.error(f"Failed to process subscription update: {e}")
            raise
    
    async def _handle_subscription_deleted(self, subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Handle subscription cancellation"""
        try:
            async with get_db() as db:
                update_query = text("""
                    UPDATE subscriptions 
                    SET status = 'canceled',
                        cancelled_at = NOW(),
                        updated_at = NOW()
                    WHERE stripe_subscription_id = :subscription_id
                """)
                
                await db.execute(update_query, {
                    'subscription_id': subscription['id']
                })
                
                # Update tenant status
                tenant_query = text("""
                    UPDATE tenants 
                    SET status = 'cancelled'
                    WHERE id = (
                        SELECT tenant_id FROM subscriptions 
                        WHERE stripe_subscription_id = :subscription_id
                    )
                """)
                
                await db.execute(tenant_query, {
                    'subscription_id': subscription['id']
                })
                
                await db.commit()
                
                # Send cancellation confirmation
                await self._send_cancellation_confirmation(subscription)
                
                return {'status': 'subscription_canceled', 'subscription_id': subscription['id']}
                
        except Exception as e:
            self.logger.error(f"Failed to process subscription deletion: {e}")
            raise
    
    async def _handle_trial_ending(self, subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Handle trial ending notification"""
        try:
            # Send trial ending reminder email
            await self._send_trial_ending_reminder(subscription)
            return {'status': 'trial_reminder_sent'}
        except Exception as e:
            self.logger.error(f"Failed to process trial ending: {e}")
            raise
    
    # Customer Event Handlers
    async def _handle_customer_created(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer creation"""
        try:
            # Update user record with Stripe customer ID
            async with get_db() as db:
                update_query = text("""
                    UPDATE users 
                    SET stripe_customer_id = :customer_id,
                        updated_at = NOW()
                    WHERE email = :email
                """)
                
                await db.execute(update_query, {
                    'customer_id': customer['id'],
                    'email': customer['email']
                })
                
                await db.commit()
                
                return {'status': 'customer_linked', 'customer_id': customer['id']}
                
        except Exception as e:
            self.logger.error(f"Failed to process customer creation: {e}")
            raise
    
    async def _handle_customer_updated(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer updates"""
        return {'status': 'customer_update_logged', 'customer_id': customer['id']}
    
    async def _handle_customer_deleted(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        """Handle customer deletion"""
        try:
            async with get_db() as db:
                # Remove Stripe customer ID from user record
                update_query = text("""
                    UPDATE users 
                    SET stripe_customer_id = NULL,
                        updated_at = NOW()
                    WHERE stripe_customer_id = :customer_id
                """)
                
                await db.execute(update_query, {
                    'customer_id': customer['id']
                })
                
                await db.commit()
                
                return {'status': 'customer_unlinked', 'customer_id': customer['id']}
                
        except Exception as e:
            self.logger.error(f"Failed to process customer deletion: {e}")
            raise
    
    # Checkout Event Handlers
    async def _handle_checkout_completed(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """Handle completed checkout session"""
        try:
            # Process successful checkout
            if session.get('mode') == 'subscription':
                # Handle subscription checkout
                await self._process_subscription_checkout(session)
            elif session.get('mode') == 'payment':
                # Handle one-time payment
                await self._process_payment_checkout(session)
            
            return {'status': 'checkout_processed', 'session_id': session['id']}
            
        except Exception as e:
            self.logger.error(f"Failed to process checkout completion: {e}")
            raise
    
    async def _handle_checkout_expired(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """Handle expired checkout session"""
        return {'status': 'checkout_expired', 'session_id': session['id']}
    
    # Payment Method Event Handlers
    async def _handle_payment_method_attached(self, payment_method: Dict[str, Any]) -> Dict[str, Any]:
        """Handle payment method attachment"""
        return {'status': 'payment_method_attached', 'payment_method_id': payment_method['id']}
    
    async def _handle_payment_method_detached(self, payment_method: Dict[str, Any]) -> Dict[str, Any]:
        """Handle payment method detachment"""
        return {'status': 'payment_method_detached', 'payment_method_id': payment_method['id']}
    
    # Dispute Event Handlers
    async def _handle_dispute_created(self, charge: Dict[str, Any]) -> Dict[str, Any]:
        """Handle dispute creation"""
        try:
            # Log dispute and alert administrators
            self.logger.warning(f"Dispute created for charge: {charge['id']}")
            await self._send_dispute_alert(charge)
            return {'status': 'dispute_logged', 'charge_id': charge['id']}
        except Exception as e:
            self.logger.error(f"Failed to process dispute: {e}")
            raise
    
    # Usage Record Event Handlers
    async def _handle_usage_record_created(self, usage_record: Dict[str, Any]) -> Dict[str, Any]:
        """Handle usage record creation"""
        return {'status': 'usage_record_logged', 'usage_record_id': usage_record['id']}
    
    # Helper methods for processing
    async def _process_subscription_checkout(self, session: Dict[str, Any]) -> None:
        """Process subscription checkout completion"""
        # Implementation for subscription setup
        pass
    
    async def _process_payment_checkout(self, session: Dict[str, Any]) -> None:
        """Process one-time payment checkout completion"""
        # Implementation for payment processing
        pass
    
    # Email notification methods (implement with your email service)
    async def _send_payment_confirmation_email(self, invoice: Dict[str, Any]) -> None:
        """Send payment confirmation email"""
        # Implement email sending logic
        pass
    
    async def _send_payment_failure_notification(self, invoice: Dict[str, Any]) -> None:
        """Send payment failure notification"""
        # Implement email sending logic
        pass
    
    async def _send_cancellation_confirmation(self, subscription: Dict[str, Any]) -> None:
        """Send subscription cancellation confirmation"""
        # Implement email sending logic
        pass
    
    async def _send_trial_ending_reminder(self, subscription: Dict[str, Any]) -> None:
        """Send trial ending reminder"""
        # Implement email sending logic
        pass
    
    async def _send_dispute_alert(self, charge: Dict[str, Any]) -> None:
        """Send dispute alert to administrators"""
        # Implement alert logic
        pass


# Global instance
stripe_webhook_handler = StripeWebhookHandler()
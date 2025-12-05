#!/usr/bin/env python3
"""
Razorpay Payment Handler for CoreLDove (INR)
"""

import os
import logging
import hashlib
import hmac
from typing import Dict, Any, Optional
from decimal import Decimal
import razorpay
import json

logger = logging.getLogger(__name__)

class RazorpayHandler:
    """Razorpay payment processor for INR payments (CoreLDove platform)"""
    
    def __init__(self):
        # Initialize Razorpay client
        self.key_id = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_placeholder')
        self.key_secret = os.getenv('RAZORPAY_KEY_SECRET', 'placeholder_secret')
        self.webhook_secret = os.getenv('RAZORPAY_WEBHOOK_SECRET', 'webhook_placeholder')
        
        if self.key_id.startswith('rzp_test_') or self.key_id == 'rzp_test_placeholder':
            logger.warning("Using Razorpay test mode - set RAZORPAY_KEY_ID for production")
        
        self.client = razorpay.Client(auth=(self.key_id, self.key_secret))
        
        # Default configuration
        self.supported_currencies = ['INR']
        self.supported_payment_methods = [
            'card',
            'upi',
            'netbanking',
            'wallet',
            'emi',
            'paylater'
        ]
        
        logger.info("✅ Razorpay handler initialized")
    
    async def create_payment(
        self, 
        amount: Decimal, 
        currency: str = 'INR',
        customer_email: str = None,
        customer_name: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a Razorpay Order"""
        try:
            if currency not in self.supported_currencies:
                raise ValueError(f"Currency {currency} not supported by Razorpay handler")
            
            # Convert amount to paisa (Razorpay expects smallest currency unit)
            amount_paisa = int(amount * 100)
            
            # Create customer if details provided
            customer = None
            if customer_email:
                try:
                    customer = self.client.customer.create({
                        "name": customer_name or "Customer",
                        "email": customer_email,
                        "contact": "",  # Add phone if available
                        "notes": metadata or {}
                    })
                    logger.info(f"Created Razorpay customer: {customer['id']}")
                except Exception as e:
                    logger.warning(f"Customer creation failed, continuing without: {str(e)}")
            
            # Create Order
            order_data = {
                "amount": amount_paisa,
                "currency": currency,
                "receipt": f"rcpt_{hash(customer_email or 'anonymous')}"[:40],
                "notes": {
                    "platform": "coreldove",
                    "customer_email": customer_email or "unknown",
                    "customer_name": customer_name or "unknown",
                    **(metadata or {})
                }
            }
            
            if customer:
                order_data["customer_id"] = customer['id']
            
            order = self.client.order.create(order_data)
            
            logger.info(f"Created Razorpay Order: {order['id']}")
            
            return {
                'id': order['id'],
                'razorpay_order_id': order['id'],
                'status': order['status'],
                'amount': amount,
                'currency': currency,
                'customer_id': customer['id'] if customer else None,
                'receipt': order['receipt'],
                'created_at': order['created_at'],
                'notes': order['notes'],
                'payment_url': f"https://checkout.razorpay.com/v1/checkout.js?order_id={order['id']}"
            }
            
        except Exception as e:
            logger.error(f"Razorpay order creation error: {str(e)}")
            raise Exception(f"Razorpay payment creation failed: {str(e)}")
    
    async def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Get payment status from Razorpay"""
        try:
            # Check if it's an order ID or payment ID
            if payment_id.startswith('order_'):
                # Get order details
                order = self.client.order.fetch(payment_id)
                
                # Get payments for this order
                payments = self.client.order.payments(payment_id)
                
                status = 'created'
                payment_method = None
                
                if payments['items']:
                    latest_payment = payments['items'][-1]  # Get latest payment attempt
                    status = self._map_razorpay_status(latest_payment['status'])
                    payment_method = latest_payment.get('method')
                
                return {
                    'id': order['id'],
                    'status': status,
                    'amount': order['amount'] / 100,  # Convert from paisa
                    'currency': order['currency'],
                    'payment_method': payment_method,
                    'created_at': order['created_at'],
                    'notes': order['notes']
                }
            else:
                # Assume it's a payment ID
                payment = self.client.payment.fetch(payment_id)
                
                return {
                    'id': payment['id'],
                    'status': self._map_razorpay_status(payment['status']),
                    'amount': payment['amount'] / 100,
                    'currency': payment['currency'],
                    'payment_method': payment.get('method'),
                    'created_at': payment['created_at'],
                    'order_id': payment.get('order_id')
                }
            
        except Exception as e:
            logger.error(f"Razorpay status check error: {str(e)}")
            raise Exception(f"Status check failed: {str(e)}")
    
    async def capture_payment(self, payment_id: str, amount: Decimal = None) -> Dict[str, Any]:
        """Capture a payment (for authorized payments)"""
        try:
            payment = self.client.payment.fetch(payment_id)
            
            capture_amount = int((amount or Decimal(payment['amount'] / 100)) * 100)
            
            captured_payment = self.client.payment.capture(payment_id, capture_amount)
            
            return {
                'id': captured_payment['id'],
                'status': captured_payment['status'],
                'amount': captured_payment['amount'] / 100,
                'currency': captured_payment['currency']
            }
            
        except Exception as e:
            logger.error(f"Payment capture error: {str(e)}")
            raise Exception(f"Payment capture failed: {str(e)}")
    
    async def refund_payment(self, payment_id: str, amount: Decimal = None, notes: Dict[str, Any] = None) -> Dict[str, Any]:
        """Refund a payment"""
        try:
            refund_data = {}
            
            if amount:
                refund_data['amount'] = int(amount * 100)  # Convert to paisa
            
            if notes:
                refund_data['notes'] = notes
            
            refund = self.client.payment.refund(payment_id, refund_data)
            
            return {
                'id': refund['id'],
                'payment_id': refund['payment_id'],
                'amount': refund['amount'] / 100,
                'currency': refund['currency'],
                'status': refund['status'],
                'created_at': refund['created_at']
            }
            
        except Exception as e:
            logger.error(f"Refund creation error: {str(e)}")
            raise Exception(f"Refund creation failed: {str(e)}")
    
    async def create_customer(self, email: str, name: str = None, contact: str = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a Razorpay customer"""
        try:
            customer_data = {
                "name": name or "Customer",
                "email": email,
                "contact": contact or "",
                "notes": metadata or {}
            }
            
            customer = self.client.customer.create(customer_data)
            
            return {
                'id': customer['id'],
                'email': customer['email'],
                'name': customer['name'],
                'contact': customer['contact'],
                'created_at': customer['created_at']
            }
            
        except Exception as e:
            logger.error(f"Customer creation error: {str(e)}")
            raise Exception(f"Customer creation failed: {str(e)}")
    
    async def create_subscription(
        self, 
        plan_id: str,
        customer_id: str = None,
        total_count: int = None,
        notes: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a subscription for a customer"""
        try:
            subscription_data = {
                "plan_id": plan_id,
                "total_count": total_count or 12,  # Default to 12 months
                "notes": notes or {}
            }
            
            if customer_id:
                subscription_data["customer_id"] = customer_id
            
            subscription = self.client.subscription.create(subscription_data)
            
            return {
                'id': subscription['id'],
                'plan_id': subscription['plan_id'],
                'customer_id': subscription.get('customer_id'),
                'status': subscription['status'],
                'current_start': subscription.get('current_start'),
                'current_end': subscription.get('current_end'),
                'created_at': subscription['created_at']
            }
            
        except Exception as e:
            logger.error(f"Subscription creation error: {str(e)}")
            raise Exception(f"Subscription creation failed: {str(e)}")
    
    def verify_webhook(self, payload: dict, signature: str) -> Dict[str, Any]:
        """Verify and parse Razorpay webhook"""
        try:
            # Verify signature
            expected_signature = hmac.new(
                self.webhook_secret.encode('utf-8'),
                json.dumps(payload, separators=(',', ':')).encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(expected_signature, signature):
                raise Exception("Invalid signature")
            
            event_type = payload.get('event')
            logger.info(f"Received Razorpay webhook: {event_type}")
            
            # Map Razorpay event to our internal format
            if event_type in ['payment.captured', 'payment.failed', 'order.paid']:
                payment_entity = payload.get('payload', {}).get('payment', {}).get('entity', {})
                order_entity = payload.get('payload', {}).get('order', {}).get('entity', {})
                
                # Use payment entity if available, otherwise order
                entity = payment_entity if payment_entity else order_entity
                
                return {
                    'external_id': entity.get('id'),
                    'status': self._map_razorpay_status(entity.get('status', 'unknown')),
                    'amount': entity.get('amount', 0) / 100,
                    'currency': entity.get('currency', 'INR'),
                    'event_type': event_type,
                    'created_at': entity.get('created_at')
                }
            
            return {
                'event_type': event_type,
                'processed': False
            }
            
        except Exception as e:
            logger.error(f"Webhook verification error: {str(e)}")
            raise Exception(f"Webhook verification failed: {str(e)}")
    
    def _map_razorpay_status(self, razorpay_status: str) -> str:
        """Map Razorpay status to our internal status"""
        status_mapping = {
            'created': 'created',
            'attempted': 'pending',
            'paid': 'succeeded',
            'captured': 'succeeded',
            'failed': 'failed',
            'refunded': 'refunded',
            'partially_refunded': 'partially_refunded'
        }
        
        return status_mapping.get(razorpay_status, 'unknown')
    
    def get_supported_currencies(self) -> list:
        """Get list of supported currencies"""
        return self.supported_currencies.copy()
    
    def get_supported_payment_methods(self) -> list:
        """Get list of supported payment methods"""
        return self.supported_payment_methods.copy()
    
    async def get_payment_methods_for_customer(self, customer_id: str) -> list:
        """Get saved payment methods for a customer"""
        try:
            # Razorpay doesn't have a direct API for saved payment methods
            # This would typically be implemented using tokens or saved cards
            # For now, return empty list
            logger.info(f"Payment methods requested for customer: {customer_id}")
            return []
            
        except Exception as e:
            logger.error(f"Error retrieving payment methods: {str(e)}")
            return []
    
    def generate_checkout_options(self, order_id: str, customer_email: str = None, customer_name: str = None) -> Dict[str, Any]:
        """Generate Razorpay checkout options for frontend"""
        options = {
            "key": self.key_id,
            "order_id": order_id,
            "currency": "INR",
            "name": "CoreLDove",
            "description": "AI-Powered E-commerce Platform",
            "image": "https://coreldove.com/logo.png",
            "theme": {
                "color": "#3399cc"
            },
            "modal": {
                "ondismiss": "function(){console.log('Checkout form closed');}"
            },
            "prefill": {},
            "notes": {
                "platform": "coreldove"
            }
        }
        
        if customer_email:
            options["prefill"]["email"] = customer_email
        if customer_name:
            options["prefill"]["name"] = customer_name
        
        return options
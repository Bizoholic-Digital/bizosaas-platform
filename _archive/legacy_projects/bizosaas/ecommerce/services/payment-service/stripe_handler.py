#!/usr/bin/env python3
"""
Stripe Payment Handler for Bizoholic (USD)
"""

import os
import logging
from typing import Dict, Any, Optional
from decimal import Decimal
import stripe
import json

logger = logging.getLogger(__name__)

class StripeHandler:
    """Stripe payment processor for USD payments (Bizoholic platform)"""
    
    def __init__(self):
        # Initialize Stripe with API key
        self.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_placeholder')
        self.webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_placeholder')
        
        if self.api_key.startswith('sk_test_') or self.api_key == 'sk_test_placeholder':
            logger.warning("Using Stripe test mode - set STRIPE_SECRET_KEY for production")
        
        stripe.api_key = self.api_key
        
        # Default configuration
        self.supported_currencies = ['USD']
        self.supported_payment_methods = [
            'card',
            'apple_pay', 
            'google_pay',
            'link',
            'us_bank_account'
        ]
        
        logger.info("✅ Stripe handler initialized")
    
    async def create_payment(
        self, 
        amount: Decimal, 
        currency: str = 'USD',
        customer_email: str = None,
        customer_name: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a Stripe Payment Intent"""
        try:
            if currency not in self.supported_currencies:
                raise ValueError(f"Currency {currency} not supported by Stripe handler")
            
            # Convert amount to cents (Stripe expects smallest currency unit)
            amount_cents = int(amount * 100) if currency == 'USD' else int(amount)
            
            # Create customer if email provided
            customer = None
            if customer_email:
                try:
                    customers = stripe.Customer.list(email=customer_email, limit=1)
                    if customers.data:
                        customer = customers.data[0]
                        logger.info(f"Found existing Stripe customer: {customer.id}")
                    else:
                        customer = stripe.Customer.create(
                            email=customer_email,
                            name=customer_name,
                            metadata=metadata or {}
                        )
                        logger.info(f"Created new Stripe customer: {customer.id}")
                except Exception as e:
                    logger.warning(f"Customer creation failed, continuing without: {str(e)}")
            
            # Create Payment Intent
            payment_intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency.lower(),
                customer=customer.id if customer else None,
                automatic_payment_methods={'enabled': True},
                metadata={
                    'platform': 'bizoholic',
                    'customer_email': customer_email or 'unknown',
                    'customer_name': customer_name or 'unknown',
                    **(metadata or {})
                },
                description=f"Bizoholic payment for {customer_email or 'customer'}"
            )
            
            logger.info(f"Created Stripe Payment Intent: {payment_intent.id}")
            
            return {
                'id': payment_intent.id,
                'client_secret': payment_intent.client_secret,
                'status': payment_intent.status,
                'amount': amount,
                'currency': currency,
                'customer_id': customer.id if customer else None,
                'payment_method_types': payment_intent.payment_method_types,
                'created': payment_intent.created,
                'metadata': payment_intent.metadata
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            raise Exception(f"Stripe payment creation failed: {str(e)}")
        except Exception as e:
            logger.error(f"Payment creation error: {str(e)}")
            raise Exception(f"Payment creation failed: {str(e)}")
    
    async def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Get payment status from Stripe"""
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_id)
            
            return {
                'id': payment_intent.id,
                'status': payment_intent.status,
                'amount': payment_intent.amount / 100,  # Convert from cents
                'currency': payment_intent.currency.upper(),
                'payment_method': payment_intent.payment_method,
                'created': payment_intent.created,
                'metadata': payment_intent.metadata
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe status check error: {str(e)}")
            raise Exception(f"Status check failed: {str(e)}")
    
    async def confirm_payment(self, payment_id: str, payment_method_id: str = None) -> Dict[str, Any]:
        """Confirm a payment intent"""
        try:
            confirm_params = {}
            if payment_method_id:
                confirm_params['payment_method'] = payment_method_id
            
            payment_intent = stripe.PaymentIntent.confirm(
                payment_id,
                **confirm_params
            )
            
            return {
                'id': payment_intent.id,
                'status': payment_intent.status,
                'amount': payment_intent.amount / 100,
                'currency': payment_intent.currency.upper(),
                'payment_method': payment_intent.payment_method,
                'next_action': payment_intent.next_action
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Payment confirmation error: {str(e)}")
            raise Exception(f"Payment confirmation failed: {str(e)}")
    
    async def cancel_payment(self, payment_id: str) -> Dict[str, Any]:
        """Cancel a payment intent"""
        try:
            payment_intent = stripe.PaymentIntent.cancel(payment_id)
            
            return {
                'id': payment_intent.id,
                'status': payment_intent.status,
                'cancelled_at': payment_intent.canceled_at
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Payment cancellation error: {str(e)}")
            raise Exception(f"Payment cancellation failed: {str(e)}")
    
    async def create_customer(self, email: str, name: str = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata=metadata or {}
            )
            
            return {
                'id': customer.id,
                'email': customer.email,
                'name': customer.name,
                'created': customer.created
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Customer creation error: {str(e)}")
            raise Exception(f"Customer creation failed: {str(e)}")
    
    async def create_subscription(
        self, 
        customer_id: str, 
        price_id: str, 
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a subscription for a customer"""
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': price_id}],
                payment_behavior='default_incomplete',
                payment_settings={
                    'save_default_payment_method': 'on_subscription'
                },
                expand=['latest_invoice.payment_intent'],
                metadata=metadata or {}
            )
            
            return {
                'id': subscription.id,
                'status': subscription.status,
                'customer': subscription.customer,
                'current_period_start': subscription.current_period_start,
                'current_period_end': subscription.current_period_end,
                'latest_invoice': subscription.latest_invoice,
                'client_secret': subscription.latest_invoice.payment_intent.client_secret if subscription.latest_invoice.payment_intent else None
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Subscription creation error: {str(e)}")
            raise Exception(f"Subscription creation failed: {str(e)}")
    
    def verify_webhook(self, payload: bytes, signature: str) -> Dict[str, Any]:
        """Verify and parse Stripe webhook"""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
            
            logger.info(f"Received Stripe webhook: {event['type']}")
            
            # Map Stripe event to our internal format
            if event['type'] in ['payment_intent.succeeded', 'payment_intent.payment_failed', 'payment_intent.canceled']:
                payment_intent = event['data']['object']
                
                return {
                    'external_id': payment_intent['id'],
                    'status': self._map_stripe_status(payment_intent['status']),
                    'amount': payment_intent['amount'] / 100,
                    'currency': payment_intent['currency'].upper(),
                    'event_type': event['type'],
                    'created': payment_intent['created']
                }
            
            return {
                'event_type': event['type'],
                'processed': False
            }
            
        except ValueError as e:
            logger.error(f"Invalid Stripe webhook payload: {str(e)}")
            raise Exception("Invalid payload")
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid Stripe webhook signature: {str(e)}")
            raise Exception("Invalid signature")
    
    def _map_stripe_status(self, stripe_status: str) -> str:
        """Map Stripe status to our internal status"""
        status_mapping = {
            'requires_payment_method': 'created',
            'requires_confirmation': 'pending',
            'requires_action': 'pending',
            'processing': 'processing',
            'succeeded': 'succeeded',
            'canceled': 'cancelled',
            'payment_failed': 'failed'
        }
        
        return status_mapping.get(stripe_status, 'unknown')
    
    def get_supported_currencies(self) -> list:
        """Get list of supported currencies"""
        return self.supported_currencies.copy()
    
    def get_supported_payment_methods(self) -> list:
        """Get list of supported payment methods"""
        return self.supported_payment_methods.copy()
    
    async def get_payment_methods_for_customer(self, customer_id: str) -> list:
        """Get saved payment methods for a customer"""
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type="card"
            )
            
            return [{
                'id': pm.id,
                'type': pm.type,
                'card': pm.card,
                'created': pm.created
            } for pm in payment_methods.data]
            
        except stripe.error.StripeError as e:
            logger.error(f"Error retrieving payment methods: {str(e)}")
            return []
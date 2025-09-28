#!/usr/bin/env python3
"""
PayPal Payment Handler (Global Backup)
"""

import os
import logging
from typing import Dict, Any, Optional
from decimal import Decimal
import json
import base64
import httpx

logger = logging.getLogger(__name__)

class PayPalHandler:
    """PayPal payment processor (backup for both platforms)"""
    
    def __init__(self):
        # Initialize PayPal credentials
        self.client_id = os.getenv('PAYPAL_CLIENT_ID', 'placeholder_client_id')
        self.client_secret = os.getenv('PAYPAL_CLIENT_SECRET', 'placeholder_secret')
        self.environment = os.getenv('PAYPAL_ENVIRONMENT', 'sandbox')  # sandbox or live
        
        # PayPal API endpoints
        self.base_url = 'https://api-m.sandbox.paypal.com' if self.environment == 'sandbox' else 'https://api-m.paypal.com'
        
        # Default configuration
        self.supported_currencies = ['USD', 'INR', 'EUR', 'GBP', 'CAD', 'AUD']
        self.supported_payment_methods = ['paypal', 'card']
        
        self._access_token = None
        self._token_expires_at = None
        
        logger.info(f"✅ PayPal handler initialized ({self.environment} mode)")
    
    async def _get_access_token(self) -> str:
        """Get or refresh PayPal access token"""
        try:
            if self._access_token and self._token_expires_at:
                # Check if token is still valid (with 5-minute buffer)
                import time
                if time.time() < (self._token_expires_at - 300):
                    return self._access_token
            
            # Get new access token
            auth_string = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1/oauth2/token",
                    headers={
                        "Authorization": f"Basic {auth_string}",
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    data="grant_type=client_credentials"
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    self._access_token = token_data['access_token']
                    self._token_expires_at = time.time() + token_data['expires_in']
                    return self._access_token
                else:
                    raise Exception(f"Token request failed: {response.text}")
                    
        except Exception as e:
            logger.error(f"PayPal token error: {str(e)}")
            raise Exception(f"PayPal authentication failed: {str(e)}")
    
    async def create_payment(
        self, 
        amount: Decimal, 
        currency: str = 'USD',
        customer_email: str = None,
        customer_name: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a PayPal order"""
        try:
            if currency not in self.supported_currencies:
                raise ValueError(f"Currency {currency} not supported by PayPal handler")
            
            access_token = await self._get_access_token()
            
            # Create PayPal order
            order_data = {
                "intent": "CAPTURE",
                "purchase_units": [{
                    "amount": {
                        "currency_code": currency,
                        "value": str(amount)
                    },
                    "description": "BizOSaaS Platform Payment",
                    "custom_id": f"bizosaas_{hash(customer_email or 'anonymous')}"
                }],
                "payment_source": {
                    "paypal": {
                        "experience_context": {
                            "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                            "brand_name": "BizOSaaS",
                            "locale": "en-US",
                            "landing_page": "LOGIN",
                            "user_action": "PAY_NOW",
                            "return_url": "https://bizosaas.com/payment/success",
                            "cancel_url": "https://bizosaas.com/payment/cancel"
                        }
                    }
                }
            }
            
            if customer_email:
                order_data["payer"] = {
                    "email_address": customer_email,
                    "name": {
                        "given_name": (customer_name or "Customer").split()[0],
                        "surname": " ".join((customer_name or "Customer").split()[1:]) or "User"
                    }
                }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v2/checkout/orders",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json",
                        "PayPal-Request-Id": f"bizosaas-{hash(str(order_data))}"
                    },
                    json=order_data
                )
                
                if response.status_code == 201:
                    order = response.json()
                    
                    # Find approval URL
                    approval_url = None
                    for link in order.get('links', []):
                        if link['rel'] == 'approve':
                            approval_url = link['href']
                            break
                    
                    logger.info(f"Created PayPal Order: {order['id']}")
                    
                    return {
                        'id': order['id'],
                        'status': order['status'],
                        'amount': amount,
                        'currency': currency,
                        'payment_url': approval_url,
                        'created_time': order.get('create_time'),
                        'links': order.get('links', [])
                    }
                else:
                    raise Exception(f"Order creation failed: {response.text}")
                    
        except Exception as e:
            logger.error(f"PayPal order creation error: {str(e)}")
            raise Exception(f"PayPal payment creation failed: {str(e)}")
    
    async def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Get payment status from PayPal"""
        try:
            access_token = await self._get_access_token()
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/v2/checkout/orders/{payment_id}",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    }
                )
                
                if response.status_code == 200:
                    order = response.json()
                    
                    return {
                        'id': order['id'],
                        'status': self._map_paypal_status(order['status']),
                        'amount': float(order['purchase_units'][0]['amount']['value']),
                        'currency': order['purchase_units'][0]['amount']['currency_code'],
                        'created_time': order.get('create_time'),
                        'update_time': order.get('update_time')
                    }
                else:
                    raise Exception(f"Status check failed: {response.text}")
                    
        except Exception as e:
            logger.error(f"PayPal status check error: {str(e)}")
            raise Exception(f"Status check failed: {str(e)}")
    
    async def capture_payment(self, payment_id: str) -> Dict[str, Any]:
        """Capture a PayPal order"""
        try:
            access_token = await self._get_access_token()
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v2/checkout/orders/{payment_id}/capture",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    }
                )
                
                if response.status_code == 201:
                    capture_result = response.json()
                    
                    return {
                        'id': capture_result['id'],
                        'status': self._map_paypal_status(capture_result['status']),
                        'amount': float(capture_result['purchase_units'][0]['payments']['captures'][0]['amount']['value']),
                        'currency': capture_result['purchase_units'][0]['payments']['captures'][0]['amount']['currency_code']
                    }
                else:
                    raise Exception(f"Capture failed: {response.text}")
                    
        except Exception as e:
            logger.error(f"PayPal capture error: {str(e)}")
            raise Exception(f"Payment capture failed: {str(e)}")
    
    def verify_webhook(self, payload: dict, headers: dict) -> Dict[str, Any]:
        """Verify and parse PayPal webhook (simplified)"""
        try:
            event_type = payload.get('event_type')
            logger.info(f"Received PayPal webhook: {event_type}")
            
            # Map PayPal events to our internal format
            if event_type in ['CHECKOUT.ORDER.APPROVED', 'PAYMENT.CAPTURE.COMPLETED', 'PAYMENT.CAPTURE.DENIED']:
                resource = payload.get('resource', {})
                
                return {
                    'external_id': resource.get('id'),
                    'status': self._map_paypal_status(resource.get('status', 'unknown')),
                    'amount': float(resource.get('amount', {}).get('value', 0)),
                    'currency': resource.get('amount', {}).get('currency_code', 'USD'),
                    'event_type': event_type,
                    'create_time': resource.get('create_time')
                }
            
            return {
                'event_type': event_type,
                'processed': False
            }
            
        except Exception as e:
            logger.error(f"PayPal webhook error: {str(e)}")
            raise Exception(f"Webhook processing failed: {str(e)}")
    
    def _map_paypal_status(self, paypal_status: str) -> str:
        """Map PayPal status to our internal status"""
        status_mapping = {
            'CREATED': 'created',
            'SAVED': 'created',
            'APPROVED': 'pending',
            'VOIDED': 'cancelled',
            'COMPLETED': 'succeeded',
            'PAYER_ACTION_REQUIRED': 'pending',
            'CAPTURED': 'succeeded',
            'DENIED': 'failed',
            'FAILED': 'failed'
        }
        
        return status_mapping.get(paypal_status, 'unknown')
    
    def get_supported_currencies(self) -> list:
        """Get list of supported currencies"""
        return self.supported_currencies.copy()
    
    def get_supported_payment_methods(self) -> list:
        """Get list of supported payment methods"""
        return self.supported_payment_methods.copy()
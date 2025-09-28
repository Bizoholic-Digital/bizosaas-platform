#!/usr/bin/env python3
"""
PayU Payment Handler for India (Secondary INR)
"""

import os
import logging
import hashlib
from typing import Dict, Any, Optional
from decimal import Decimal
import httpx
import json

logger = logging.getLogger(__name__)

class PayUHandler:
    """PayU payment processor for INR payments (secondary for CoreLDove)"""
    
    def __init__(self):
        # Initialize PayU credentials
        self.merchant_key = os.getenv('PAYU_MERCHANT_KEY', 'placeholder_key')
        self.merchant_salt = os.getenv('PAYU_MERCHANT_SALT', 'placeholder_salt')
        self.environment = os.getenv('PAYU_ENVIRONMENT', 'test')  # test or production
        
        # PayU API endpoints
        if self.environment == 'production':
            self.base_url = 'https://secure.payu.in'
            self.verify_url = 'https://info.payu.in/merchant/postservice'
        else:
            self.base_url = 'https://test.payu.in'
            self.verify_url = 'https://info.payu.in/merchant/postservice'
        
        # Default configuration
        self.supported_currencies = ['INR']
        self.supported_payment_methods = [
            'CC',  # Credit Card
            'DC',  # Debit Card
            'NB',  # Net Banking
            'UPI', # UPI
            'WALLET'  # Wallets
        ]
        
        logger.info(f"✅ PayU handler initialized ({self.environment} mode)")
    
    def _generate_hash(self, data: str) -> str:
        """Generate PayU hash"""
        return hashlib.sha512((data + self.merchant_salt).encode('utf-8')).hexdigest()
    
    async def create_payment(
        self, 
        amount: Decimal, 
        currency: str = 'INR',
        customer_email: str = None,
        customer_name: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a PayU payment form data"""
        try:
            if currency not in self.supported_currencies:
                raise ValueError(f"Currency {currency} not supported by PayU handler")
            
            # Generate transaction ID
            import time
            txnid = f"TXN{int(time.time())}{hash(customer_email or 'anonymous') % 10000}"
            
            # Prepare payment data
            payment_data = {
                'key': self.merchant_key,
                'txnid': txnid,
                'amount': str(amount),
                'productinfo': 'CoreLDove Platform Services',
                'firstname': (customer_name or 'Customer').split()[0],
                'email': customer_email or 'customer@coreldove.com',
                'phone': '9999999999',  # Default phone, should be collected from user
                'surl': 'https://coreldove.com/payment/success',  # Success URL
                'furl': 'https://coreldove.com/payment/failure',  # Failure URL
                'curl': 'https://coreldove.com/payment/cancel',   # Cancel URL
                'udf1': metadata.get('platform', 'coreldove'),
                'udf2': metadata.get('user_id', ''),
                'udf3': metadata.get('plan', ''),
                'udf4': '',
                'udf5': ''
            }
            
            # Generate hash
            hash_string = f"{payment_data['key']}|{payment_data['txnid']}|{payment_data['amount']}|{payment_data['productinfo']}|{payment_data['firstname']}|{payment_data['email']}|{payment_data['udf1']}|{payment_data['udf2']}|{payment_data['udf3']}|{payment_data['udf4']}|{payment_data['udf5']}"
            payment_data['hash'] = self._generate_hash(hash_string)
            
            logger.info(f"Created PayU payment data for txnid: {txnid}")
            
            return {
                'id': txnid,
                'status': 'created',
                'amount': amount,
                'currency': currency,
                'payment_url': f"{self.base_url}/_payment",
                'form_data': payment_data,
                'method': 'POST',
                'created_at': int(time.time())
            }
            
        except Exception as e:
            logger.error(f"PayU payment creation error: {str(e)}")
            raise Exception(f"PayU payment creation failed: {str(e)}")
    
    async def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Get payment status from PayU"""
        try:
            # PayU verify payment API
            verify_data = {
                'key': self.merchant_key,
                'command': 'verify_payment',
                'var1': payment_id,  # transaction ID
                'hash': self._generate_hash(f"{self.merchant_key}|verify_payment|{payment_id}")
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.verify_url,
                    data=verify_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('status') == 1 and result.get('transaction_details'):
                        transaction = result['transaction_details'][payment_id]
                        
                        return {
                            'id': payment_id,
                            'status': self._map_payu_status(transaction.get('status', 'unknown')),
                            'amount': float(transaction.get('amt', 0)),
                            'currency': 'INR',
                            'payment_mode': transaction.get('mode'),
                            'bank_ref_num': transaction.get('bank_ref_num'),
                            'created_at': transaction.get('addedon')
                        }
                    else:
                        return {
                            'id': payment_id,
                            'status': 'unknown',
                            'amount': 0,
                            'currency': 'INR'
                        }
                else:
                    raise Exception(f"Status check failed: {response.text}")
                    
        except Exception as e:
            logger.error(f"PayU status check error: {str(e)}")
            raise Exception(f"Status check failed: {str(e)}")
    
    async def verify_payment_response(self, response_data: dict) -> Dict[str, Any]:
        """Verify PayU payment response"""
        try:
            # Extract response data
            status = response_data.get('status')
            txnid = response_data.get('txnid')
            amount = response_data.get('amount')
            productinfo = response_data.get('productinfo')
            firstname = response_data.get('firstname')
            email = response_data.get('email')
            udf1 = response_data.get('udf1', '')
            udf2 = response_data.get('udf2', '')
            udf3 = response_data.get('udf3', '')
            udf4 = response_data.get('udf4', '')
            udf5 = response_data.get('udf5', '')
            received_hash = response_data.get('hash')
            
            # Generate expected hash for verification
            if status == 'success':
                hash_string = f"{self.merchant_salt}|{status}|||||||{udf5}|{udf4}|{udf3}|{udf2}|{udf1}|{email}|{firstname}|{productinfo}|{amount}|{txnid}|{self.merchant_key}"
            else:
                hash_string = f"{self.merchant_salt}|{status}|||||||{udf5}|{udf4}|{udf3}|{udf2}|{udf1}|{email}|{firstname}|{productinfo}|{amount}|{txnid}|{self.merchant_key}"
            
            expected_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()
            
            # Verify hash
            is_valid = (received_hash.lower() == expected_hash.lower())
            
            return {
                'id': txnid,
                'status': self._map_payu_status(status) if is_valid else 'failed',
                'amount': float(amount) if amount else 0,
                'currency': 'INR',
                'is_valid': is_valid,
                'payment_mode': response_data.get('mode'),
                'bank_ref_num': response_data.get('bank_ref_num'),
                'mihpayid': response_data.get('mihpayid')
            }
            
        except Exception as e:
            logger.error(f"PayU verification error: {str(e)}")
            raise Exception(f"Payment verification failed: {str(e)}")
    
    def verify_webhook(self, payload: dict, signature: str = None) -> Dict[str, Any]:
        """Verify and parse PayU webhook (PayU typically uses form POST)"""
        try:
            # PayU sends payment response as form data, not webhook
            # This method processes the payment response
            return self.verify_payment_response(payload)
            
        except Exception as e:
            logger.error(f"PayU webhook error: {str(e)}")
            raise Exception(f"Webhook processing failed: {str(e)}")
    
    def _map_payu_status(self, payu_status: str) -> str:
        """Map PayU status to our internal status"""
        status_mapping = {
            'success': 'succeeded',
            'failure': 'failed',
            'pending': 'pending',
            'cancelled': 'cancelled',
            'dropped': 'failed',
            'bounced': 'failed'
        }
        
        return status_mapping.get(payu_status.lower() if payu_status else '', 'unknown')
    
    def get_supported_currencies(self) -> list:
        """Get list of supported currencies"""
        return self.supported_currencies.copy()
    
    def get_supported_payment_methods(self) -> list:
        """Get list of supported payment methods"""
        return self.supported_payment_methods.copy()
    
    def generate_payment_form_html(self, payment_data: dict) -> str:
        """Generate HTML form for PayU payment (for frontend integration)"""
        form_fields = ""
        for key, value in payment_data['form_data'].items():
            form_fields += f'<input type="hidden" name="{key}" value="{value}" />\n'
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Processing Payment...</title>
        </head>
        <body>
            <form id="payuForm" action="{payment_data['payment_url']}" method="post">
                {form_fields}
                <input type="submit" value="Pay Now" id="submit" />
            </form>
            <script>
                // Auto-submit form
                document.getElementById('payuForm').submit();
            </script>
        </body>
        </html>
        """
        
        return html
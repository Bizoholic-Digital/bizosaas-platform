"""
Payment Processing Service
Multi-gateway payment processing with fraud detection and compliance
"""

import asyncio
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Any, Union
from uuid import uuid4
import hashlib
import hmac
import json

from ..models.order_models import PaymentMethod, PaymentStatus, PaymentDetails

logger = logging.getLogger(__name__)


class PaymentProcessor:
    """
    Multi-gateway payment processor
    Supports Stripe, PayPal, Razorpay, PayU with fraud detection
    """
    
    def __init__(self):
        self.config = {
            "default_gateway": "stripe",
            "enable_fraud_detection": True,
            "auto_capture": True,
            "capture_delay_hours": 24,
            "max_retry_attempts": 3,
            "retry_delay_seconds": 5,
            "webhook_timeout": 30
        }
        
        # Gateway configurations
        self.gateways = {
            "stripe": {
                "name": "Stripe",
                "api_url": "https://api.stripe.com/v1",
                "supported_methods": [
                    PaymentMethod.CREDIT_CARD,
                    PaymentMethod.DEBIT_CARD,
                    PaymentMethod.DIGITAL_WALLET
                ],
                "fees": {"percentage": 2.9, "fixed": Decimal("0.30")},
                "settlement_days": 2,
                "enabled": True
            },
            "paypal": {
                "name": "PayPal",
                "api_url": "https://api.paypal.com/v1",
                "supported_methods": [PaymentMethod.PAYPAL, PaymentMethod.DIGITAL_WALLET],
                "fees": {"percentage": 3.5, "fixed": Decimal("0.00")},
                "settlement_days": 1,
                "enabled": True
            },
            "razorpay": {
                "name": "Razorpay",
                "api_url": "https://api.razorpay.com/v1",
                "supported_methods": [
                    PaymentMethod.CREDIT_CARD,
                    PaymentMethod.DEBIT_CARD,
                    PaymentMethod.BANK_TRANSFER,
                    PaymentMethod.DIGITAL_WALLET
                ],
                "fees": {"percentage": 2.0, "fixed": Decimal("0.00")},
                "settlement_days": 2,
                "enabled": True
            },
            "payu": {
                "name": "PayU",
                "api_url": "https://secure.payu.in/_payment",
                "supported_methods": [
                    PaymentMethod.CREDIT_CARD,
                    PaymentMethod.DEBIT_CARD,
                    PaymentMethod.BANK_TRANSFER
                ],
                "fees": {"percentage": 2.5, "fixed": Decimal("0.00")},
                "settlement_days": 3,
                "enabled": True
            }
        }
        
        # In-memory storage (replace with database in production)
        self.transactions = {}
        self.fraud_rules = []
        self.payment_methods = {}
        
        self._initialize_fraud_rules()
    
    async def initialize(self):
        """Initialize payment processor"""
        logger.info("Initializing Payment Processor...")
        
        try:
            # Initialize gateway connections
            await self._initialize_gateways()
            
            # Start background tasks
            asyncio.create_task(self._process_pending_captures())
            asyncio.create_task(self._monitor_failed_payments())
            
            logger.info("Payment Processor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Payment Processor: {e}")
            raise
    
    async def shutdown(self):
        """Cleanup payment processor"""
        logger.info("Shutting down Payment Processor...")
    
    async def authorize_payment(
        self, 
        order_id: str, 
        amount: Decimal, 
        payment_method: PaymentMethod,
        billing_address: Dict[str, Any],
        payment_details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Authorize payment for order
        
        Args:
            order_id: Order identifier
            amount: Payment amount
            payment_method: Payment method type
            billing_address: Billing address
            payment_details: Additional payment details
            
        Returns:
            Dict with authorization result
        """
        logger.info(f"Authorizing payment for order {order_id}: {amount}")
        
        try:
            # Select gateway
            gateway = await self._select_gateway(payment_method, amount, billing_address)
            
            # Run fraud detection
            fraud_result = await self._detect_fraud(
                order_id, amount, payment_method, billing_address, payment_details
            )
            
            if fraud_result["high_risk"]:
                return {
                    "success": False,
                    "error": "Payment blocked due to fraud risk",
                    "fraud_score": fraud_result["score"],
                    "requires_review": True
                }
            
            # Process authorization
            transaction_id = str(uuid4())
            
            auth_result = await self._process_gateway_authorization(
                gateway, transaction_id, order_id, amount, payment_method, 
                billing_address, payment_details
            )
            
            if auth_result["success"]:
                # Store transaction
                transaction = {
                    "id": transaction_id,
                    "order_id": order_id,
                    "gateway": gateway,
                    "amount": amount,
                    "currency": "USD",  # Default currency
                    "status": PaymentStatus.AUTHORIZED,
                    "payment_method": payment_method,
                    "gateway_transaction_id": auth_result["gateway_transaction_id"],
                    "authorization_code": auth_result.get("authorization_code"),
                    "fraud_score": fraud_result["score"],
                    "created_at": datetime.utcnow(),
                    "authorized_at": datetime.utcnow(),
                    "expires_at": datetime.utcnow() + timedelta(days=7),  # Auth expiry
                    "gateway_response": auth_result.get("raw_response", {}),
                    "billing_address": billing_address
                }
                
                self.transactions[transaction_id] = transaction
                
                # Schedule auto-capture if enabled
                if self.config["auto_capture"]:
                    await self._schedule_auto_capture(transaction_id)
                
                return {
                    "success": True,
                    "payment_details": {
                        "id": transaction_id,
                        "method": payment_method,
                        "gateway": gateway,
                        "transaction_id": auth_result["gateway_transaction_id"],
                        "amount": amount,
                        "currency": "USD",
                        "status": PaymentStatus.AUTHORIZED,
                        "authorized_at": datetime.utcnow(),
                        "gateway_response": auth_result.get("gateway_response", {})
                    }
                }
            else:
                return {
                    "success": False,
                    "error": auth_result["error"],
                    "gateway": gateway,
                    "decline_reason": auth_result.get("decline_reason")
                }
                
        except Exception as e:
            logger.error(f"Payment authorization failed for order {order_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def capture_payment(self, order_id: str, payment_details: Dict[str, Any]) -> Dict[str, Any]:
        """Capture authorized payment"""
        logger.info(f"Capturing payment for order {order_id}")
        
        try:
            transaction_id = payment_details["id"]
            
            if transaction_id not in self.transactions:
                raise Exception(f"Transaction {transaction_id} not found")
            
            transaction = self.transactions[transaction_id]
            
            if transaction["status"] != PaymentStatus.AUTHORIZED:
                raise Exception(f"Transaction {transaction_id} cannot be captured - status: {transaction['status']}")
            
            # Process capture
            gateway = transaction["gateway"]
            capture_result = await self._process_gateway_capture(
                gateway, transaction_id, transaction["gateway_transaction_id"], transaction["amount"]
            )
            
            if capture_result["success"]:
                # Update transaction
                transaction["status"] = PaymentStatus.CAPTURED
                transaction["captured_at"] = datetime.utcnow()
                transaction["capture_transaction_id"] = capture_result.get("capture_transaction_id")
                transaction["gateway_response"].update(capture_result.get("raw_response", {}))
                
                return {
                    "success": True,
                    "transaction_id": transaction_id,
                    "captured_amount": transaction["amount"],
                    "captured_at": transaction["captured_at"]
                }
            else:
                return {
                    "success": False,
                    "error": capture_result["error"],
                    "transaction_id": transaction_id
                }
                
        except Exception as e:
            logger.error(f"Payment capture failed for order {order_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def process_refund(
        self, 
        order_id: str, 
        payment_details: Dict[str, Any],
        refund_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process payment refund"""
        logger.info(f"Processing refund for order {order_id}")
        
        try:
            transaction_id = payment_details["id"]
            
            if transaction_id not in self.transactions:
                raise Exception(f"Transaction {transaction_id} not found")
            
            transaction = self.transactions[transaction_id]
            
            if transaction["status"] not in [PaymentStatus.CAPTURED, PaymentStatus.AUTHORIZED]:
                raise Exception(f"Transaction {transaction_id} cannot be refunded - status: {transaction['status']}")
            
            # Calculate refund amount
            refund_amount = refund_data.get("amount")
            if not refund_amount:
                refund_amount = transaction["amount"]  # Full refund
            
            if refund_amount > transaction["amount"]:
                raise Exception("Refund amount cannot exceed original transaction amount")
            
            # Process refund
            gateway = transaction["gateway"]
            refund_result = await self._process_gateway_refund(
                gateway, transaction_id, transaction["gateway_transaction_id"], 
                refund_amount, refund_data["reason"]
            )
            
            if refund_result["success"]:
                # Update transaction
                refund_type = "full" if refund_amount == transaction["amount"] else "partial"
                
                if refund_type == "full":
                    transaction["status"] = PaymentStatus.REFUNDED
                else:
                    transaction["status"] = PaymentStatus.PARTIALLY_REFUNDED
                
                transaction["refunded_amount"] = refund_amount
                transaction["refunded_at"] = datetime.utcnow()
                transaction["refund_transaction_id"] = refund_result.get("refund_transaction_id")
                transaction["refund_reason"] = refund_data["reason"]
                transaction["gateway_response"].update(refund_result.get("raw_response", {}))
                
                return {
                    "success": True,
                    "refund_type": refund_type,
                    "refunded_amount": refund_amount,
                    "refund_transaction_id": refund_result.get("refund_transaction_id"),
                    "payment_update": {
                        "status": transaction["status"],
                        "refunded_amount": refund_amount,
                        "refunded_at": transaction["refunded_at"]
                    }
                }
            else:
                return {
                    "success": False,
                    "error": refund_result["error"],
                    "transaction_id": transaction_id
                }
                
        except Exception as e:
            logger.error(f"Refund processing failed for order {order_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def void_authorization(self, order_id: str, payment_details: Dict[str, Any]) -> Dict[str, Any]:
        """Void authorized payment"""
        logger.info(f"Voiding authorization for order {order_id}")
        
        try:
            transaction_id = payment_details["id"]
            
            if transaction_id not in self.transactions:
                raise Exception(f"Transaction {transaction_id} not found")
            
            transaction = self.transactions[transaction_id]
            
            if transaction["status"] != PaymentStatus.AUTHORIZED:
                raise Exception(f"Transaction {transaction_id} cannot be voided - status: {transaction['status']}")
            
            # Process void
            gateway = transaction["gateway"]
            void_result = await self._process_gateway_void(
                gateway, transaction_id, transaction["gateway_transaction_id"]
            )
            
            if void_result["success"]:
                # Update transaction
                transaction["status"] = PaymentStatus.CANCELLED
                transaction["voided_at"] = datetime.utcnow()
                transaction["gateway_response"].update(void_result.get("raw_response", {}))
                
                return {
                    "success": True,
                    "transaction_id": transaction_id,
                    "voided_at": transaction["voided_at"]
                }
            else:
                return {
                    "success": False,
                    "error": void_result["error"],
                    "transaction_id": transaction_id
                }
                
        except Exception as e:
            logger.error(f"Authorization void failed for order {order_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def cancel_authorization(self, order_id: str) -> Dict[str, Any]:
        """Cancel authorization for order"""
        logger.info(f"Cancelling authorization for order {order_id}")
        
        # Find active authorization for order
        transaction = next(
            (t for t in self.transactions.values() 
             if t["order_id"] == order_id and t["status"] == PaymentStatus.AUTHORIZED),
            None
        )
        
        if transaction:
            return await self.void_authorization(order_id, {"id": transaction["id"]})
        else:
            return {"success": True, "message": "No active authorization found"}
    
    async def get_payment_status(self, transaction_id: str) -> Dict[str, Any]:
        """Get payment transaction status"""
        
        if transaction_id not in self.transactions:
            raise Exception(f"Transaction {transaction_id} not found")
        
        transaction = self.transactions[transaction_id]
        
        return {
            "transaction_id": transaction_id,
            "order_id": transaction["order_id"],
            "status": transaction["status"],
            "amount": transaction["amount"],
            "currency": transaction["currency"],
            "gateway": transaction["gateway"],
            "created_at": transaction["created_at"],
            "authorized_at": transaction.get("authorized_at"),
            "captured_at": transaction.get("captured_at"),
            "refunded_at": transaction.get("refunded_at"),
            "refunded_amount": transaction.get("refunded_amount", Decimal("0"))
        }
    
    async def get_health(self) -> Dict[str, Any]:
        """Get payment processor health status"""
        
        gateway_health = {}
        for gateway_id, gateway_config in self.gateways.items():
            if gateway_config["enabled"]:
                # In production, this would ping gateway APIs
                gateway_health[gateway_id] = {
                    "status": "healthy",
                    "response_time_ms": 150,
                    "last_check": datetime.utcnow()
                }
        
        return {
            "status": "healthy",
            "active_transactions": len([t for t in self.transactions.values() if t["status"] in [PaymentStatus.AUTHORIZED, PaymentStatus.PENDING]]),
            "gateways": gateway_health,
            "fraud_rules_active": len(self.fraud_rules)
        }
    
    # Private helper methods
    
    def _initialize_fraud_rules(self):
        """Initialize fraud detection rules"""
        
        self.fraud_rules = [
            {
                "name": "high_amount",
                "description": "High transaction amount",
                "condition": lambda amount, **kwargs: amount > Decimal("1000"),
                "score": 25
            },
            {
                "name": "velocity_check",
                "description": "Multiple transactions in short time",
                "condition": self._check_velocity,
                "score": 30
            },
            {
                "name": "country_mismatch",
                "description": "Billing and shipping country mismatch",
                "condition": self._check_country_mismatch,
                "score": 20
            },
            {
                "name": "unusual_hour",
                "description": "Transaction at unusual hour",
                "condition": self._check_unusual_hour,
                "score": 10
            }
        ]
    
    async def _initialize_gateways(self):
        """Initialize gateway connections"""
        logger.info("Initializing payment gateways...")
        
        for gateway_id, gateway_config in self.gateways.items():
            if gateway_config["enabled"]:
                logger.info(f"Initialized gateway: {gateway_config['name']}")
    
    async def _select_gateway(
        self, 
        payment_method: PaymentMethod, 
        amount: Decimal, 
        billing_address: Dict[str, Any]
    ) -> str:
        """Select optimal payment gateway"""
        
        # Simple gateway selection logic
        # In production, this would be more sophisticated
        
        suitable_gateways = []
        
        for gateway_id, gateway_config in self.gateways.items():
            if (gateway_config["enabled"] and 
                payment_method in gateway_config["supported_methods"]):
                
                # Calculate total fees
                percentage_fee = amount * Decimal(str(gateway_config["fees"]["percentage"])) / 100
                total_fee = percentage_fee + gateway_config["fees"]["fixed"]
                
                suitable_gateways.append({
                    "id": gateway_id,
                    "name": gateway_config["name"],
                    "total_fee": total_fee,
                    "settlement_days": gateway_config["settlement_days"]
                })
        
        if not suitable_gateways:
            raise Exception(f"No suitable gateway found for payment method {payment_method}")
        
        # Select gateway with lowest fees
        selected = min(suitable_gateways, key=lambda g: g["total_fee"])
        
        logger.info(f"Selected gateway {selected['name']} for payment method {payment_method}")
        
        return selected["id"]
    
    async def _detect_fraud(
        self,
        order_id: str,
        amount: Decimal,
        payment_method: PaymentMethod,
        billing_address: Dict[str, Any],
        payment_details: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Run fraud detection on payment"""
        
        if not self.config["enable_fraud_detection"]:
            return {"score": 0.0, "high_risk": False, "triggered_rules": []}
        
        total_score = 0.0
        triggered_rules = []
        
        context = {
            "amount": amount,
            "payment_method": payment_method,
            "billing_address": billing_address,
            "payment_details": payment_details,
            "order_id": order_id
        }
        
        for rule in self.fraud_rules:
            try:
                if rule["condition"](**context):
                    total_score += rule["score"]
                    triggered_rules.append(rule["name"])
            except Exception as e:
                logger.warning(f"Fraud rule {rule['name']} failed: {e}")
        
        high_risk = total_score >= 75.0  # Risk threshold
        
        logger.info(f"Fraud score for order {order_id}: {total_score} (rules: {triggered_rules})")
        
        return {
            "score": total_score,
            "high_risk": high_risk,
            "triggered_rules": triggered_rules
        }
    
    def _check_velocity(self, **kwargs) -> bool:
        """Check for high transaction velocity"""
        # Simplified velocity check
        return False  # Would check recent transactions
    
    def _check_country_mismatch(self, billing_address: Dict[str, Any], **kwargs) -> bool:
        """Check for billing/shipping country mismatch"""
        # This would be implemented with shipping address comparison
        return False
    
    def _check_unusual_hour(self, **kwargs) -> bool:
        """Check for transactions at unusual hours"""
        current_hour = datetime.utcnow().hour
        return current_hour < 6 or current_hour > 23  # Late night/early morning
    
    async def _process_gateway_authorization(
        self,
        gateway: str,
        transaction_id: str,
        order_id: str,
        amount: Decimal,
        payment_method: PaymentMethod,
        billing_address: Dict[str, Any],
        payment_details: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Process authorization through gateway"""
        
        # Simulate gateway processing
        logger.info(f"Processing authorization through {gateway} for {amount}")
        
        # In production, this would make actual API calls to payment gateways
        
        # Simulate random success/failure for demo
        import random
        
        if random.random() < 0.95:  # 95% success rate
            gateway_transaction_id = f"{gateway}_{uuid4().hex[:16]}"
            
            return {
                "success": True,
                "gateway_transaction_id": gateway_transaction_id,
                "authorization_code": f"AUTH_{uuid4().hex[:8]}",
                "gateway_response": {
                    "gateway": gateway,
                    "response_code": "00",
                    "response_message": "Approved",
                    "processor_response": "Approved"
                },
                "raw_response": {
                    "transaction_id": gateway_transaction_id,
                    "status": "authorized",
                    "amount": str(amount),
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        else:
            return {
                "success": False,
                "error": "Payment declined by gateway",
                "decline_reason": "Insufficient funds",
                "gateway_response": {
                    "gateway": gateway,
                    "response_code": "05",
                    "response_message": "Declined"
                }
            }
    
    async def _process_gateway_capture(
        self,
        gateway: str,
        transaction_id: str,
        gateway_transaction_id: str,
        amount: Decimal
    ) -> Dict[str, Any]:
        """Process capture through gateway"""
        
        logger.info(f"Processing capture through {gateway} for {amount}")
        
        # Simulate gateway capture
        import random
        
        if random.random() < 0.98:  # 98% success rate
            capture_transaction_id = f"{gateway}_cap_{uuid4().hex[:16]}"
            
            return {
                "success": True,
                "capture_transaction_id": capture_transaction_id,
                "raw_response": {
                    "transaction_id": capture_transaction_id,
                    "original_transaction_id": gateway_transaction_id,
                    "status": "captured",
                    "amount": str(amount),
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        else:
            return {
                "success": False,
                "error": "Capture failed - authorization expired"
            }
    
    async def _process_gateway_refund(
        self,
        gateway: str,
        transaction_id: str,
        gateway_transaction_id: str,
        amount: Decimal,
        reason: str
    ) -> Dict[str, Any]:
        """Process refund through gateway"""
        
        logger.info(f"Processing refund through {gateway} for {amount}")
        
        # Simulate gateway refund
        import random
        
        if random.random() < 0.97:  # 97% success rate
            refund_transaction_id = f"{gateway}_ref_{uuid4().hex[:16]}"
            
            return {
                "success": True,
                "refund_transaction_id": refund_transaction_id,
                "raw_response": {
                    "transaction_id": refund_transaction_id,
                    "original_transaction_id": gateway_transaction_id,
                    "status": "refunded",
                    "amount": str(amount),
                    "reason": reason,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        else:
            return {
                "success": False,
                "error": "Refund failed - transaction not eligible"
            }
    
    async def _process_gateway_void(
        self,
        gateway: str,
        transaction_id: str,
        gateway_transaction_id: str
    ) -> Dict[str, Any]:
        """Process void through gateway"""
        
        logger.info(f"Processing void through {gateway}")
        
        # Simulate gateway void
        return {
            "success": True,
            "raw_response": {
                "transaction_id": gateway_transaction_id,
                "status": "voided",
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    async def _schedule_auto_capture(self, transaction_id: str):
        """Schedule automatic capture for transaction"""
        
        async def auto_capture():
            await asyncio.sleep(self.config["capture_delay_hours"] * 3600)
            
            try:
                if transaction_id in self.transactions:
                    transaction = self.transactions[transaction_id]
                    
                    if transaction["status"] == PaymentStatus.AUTHORIZED:
                        logger.info(f"Auto-capturing transaction {transaction_id}")
                        
                        await self.capture_payment(
                            transaction["order_id"],
                            {"id": transaction_id}
                        )
                        
            except Exception as e:
                logger.error(f"Auto-capture failed for transaction {transaction_id}: {e}")
        
        asyncio.create_task(auto_capture())
    
    async def _process_pending_captures(self):
        """Background task to process pending captures"""
        
        while True:
            try:
                # Find transactions pending capture
                current_time = datetime.utcnow()
                
                for transaction in self.transactions.values():
                    if (transaction["status"] == PaymentStatus.AUTHORIZED and
                        "auto_capture_at" in transaction and
                        transaction["auto_capture_at"] <= current_time):
                        
                        logger.info(f"Processing scheduled capture for transaction {transaction['id']}")
                        
                        await self.capture_payment(
                            transaction["order_id"],
                            {"id": transaction["id"]}
                        )
                
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"Pending captures processing failed: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry
    
    async def _monitor_failed_payments(self):
        """Background task to monitor and retry failed payments"""
        
        while True:
            try:
                # Find failed transactions that can be retried
                for transaction in self.transactions.values():
                    if (transaction["status"] == PaymentStatus.FAILED and
                        transaction.get("retry_count", 0) < self.config["max_retry_attempts"]):
                        
                        logger.info(f"Retrying failed transaction {transaction['id']}")
                        
                        # Implement retry logic here
                        # For now, just increment retry count
                        transaction["retry_count"] = transaction.get("retry_count", 0) + 1
                        transaction["last_retry"] = datetime.utcnow()
                
                await asyncio.sleep(1800)  # Check every 30 minutes
                
            except Exception as e:
                logger.error(f"Failed payment monitoring failed: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retry
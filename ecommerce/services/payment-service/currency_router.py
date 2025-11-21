"""
Currency Router - Smart payment method routing based on platform and currency
"""

from typing import Dict, List, Optional
from enum import Enum

class PaymentPlatform(str, Enum):
    BIZOHOLIC = "bizoholic"
    CORELDOVE = "coreldove"

class Currency(str, Enum):
    USD = "USD"
    INR = "INR"

class PaymentMethod(str, Enum):
    STRIPE = "stripe"
    RAZORPAY = "razorpay"
    PAYPAL = "paypal"
    PAYU = "payu"

class CurrencyRouter:
    """Smart payment routing based on platform, currency, and market optimization"""
    
    def __init__(self):
        self.routing_config = {
            # Bizoholic (US Market - USD)
            PaymentPlatform.BIZOHOLIC: {
                Currency.USD: [
                    {"method": PaymentMethod.STRIPE, "priority": 1, "success_rate": 0.98, "fees": 0.029},
                    {"method": PaymentMethod.PAYPAL, "priority": 2, "success_rate": 0.96, "fees": 0.029}
                ]
            },
            
            # CoreLDove (India Market - INR)
            PaymentPlatform.CORELDOVE: {
                Currency.INR: [
                    {"method": PaymentMethod.RAZORPAY, "priority": 1, "success_rate": 0.95, "fees": 0.020},
                    {"method": PaymentMethod.PAYU, "priority": 2, "success_rate": 0.92, "fees": 0.023},
                    {"method": PaymentMethod.PAYPAL, "priority": 3, "success_rate": 0.90, "fees": 0.044}
                ],
                # Allow USD for international customers
                Currency.USD: [
                    {"method": PaymentMethod.STRIPE, "priority": 1, "success_rate": 0.96, "fees": 0.029},
                    {"method": PaymentMethod.PAYPAL, "priority": 2, "success_rate": 0.94, "fees": 0.034}
                ]
            }
        }
    
    def get_primary_method(self, platform: PaymentPlatform, currency: Currency) -> PaymentMethod:
        """Get the primary (highest priority) payment method for platform/currency"""
        
        if platform in self.routing_config and currency in self.routing_config[platform]:
            methods = self.routing_config[platform][currency]
            primary = min(methods, key=lambda x: x["priority"])
            return primary["method"]
        
        # Fallback defaults
        if currency == Currency.USD:
            return PaymentMethod.STRIPE
        elif currency == Currency.INR:
            return PaymentMethod.RAZORPAY
        
        return PaymentMethod.STRIPE  # Ultimate fallback
    
    def get_all_methods(self, platform: PaymentPlatform, currency: Currency) -> List[Dict]:
        """Get all available payment methods for platform/currency sorted by priority"""
        
        if platform in self.routing_config and currency in self.routing_config[platform]:
            methods = self.routing_config[platform][currency]
            return sorted(methods, key=lambda x: x["priority"])
        
        return []
    
    def get_fallback_method(self, platform: PaymentPlatform, currency: Currency, 
                           failed_method: PaymentMethod) -> Optional[PaymentMethod]:
        """Get fallback payment method if primary fails"""
        
        methods = self.get_all_methods(platform, currency)
        
        # Find next priority method after the failed one
        for method in methods:
            if method["method"] != failed_method:
                return method["method"]
        
        return None
    
    def calculate_fees(self, platform: PaymentPlatform, currency: Currency, 
                      payment_method: PaymentMethod, amount: float) -> Dict:
        """Calculate fees for a payment method"""
        
        methods = self.get_all_methods(platform, currency)
        
        for method in methods:
            if method["method"] == payment_method:
                fee_rate = method["fees"]
                
                if currency == Currency.USD:
                    # USD: percentage + fixed fee
                    percentage_fee = amount * fee_rate
                    fixed_fee = 0.30 if payment_method in [PaymentMethod.STRIPE, PaymentMethod.PAYPAL] else 0
                    total_fee = percentage_fee + fixed_fee
                    
                elif currency == Currency.INR:
                    # INR: mostly percentage-based
                    if payment_method == PaymentMethod.PAYPAL:
                        percentage_fee = amount * fee_rate
                        fixed_fee = 15  # ₹15 fixed fee for PayPal
                        total_fee = percentage_fee + fixed_fee
                    else:
                        total_fee = amount * fee_rate
                
                return {
                    "fee_rate": fee_rate,
                    "total_fee": round(total_fee, 2),
                    "net_amount": round(amount - total_fee, 2),
                    "currency": currency
                }
        
        return {"error": "Payment method not found"}
    
    def get_market_preferences(self, platform: PaymentPlatform) -> Dict:
        """Get market-specific payment preferences"""
        
        if platform == PaymentPlatform.BIZOHOLIC:
            return {
                "market": "United States",
                "currency": "USD",
                "preferred_methods": ["Credit Card", "PayPal"],
                "customer_behavior": "Prefer card payments, trust Stripe/PayPal",
                "optimization": "Focus on conversion rate and security"
            }
        
        elif platform == PaymentPlatform.CORELDOVE:
            return {
                "market": "India", 
                "currency": "INR",
                "preferred_methods": ["UPI", "Cards", "Net Banking"],
                "customer_behavior": "UPI dominant, price-sensitive on fees",
                "optimization": "Focus on local payment methods and lower fees"
            }
        
        return {}
"""
Multi-Currency Payment Service - BizOSaaS
Handles USD payments for Bizoholic (US market) and INR payments for CoreLDove (India market)
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional, List
from datetime import datetime
import uvicorn
from decimal import Decimal
from enum import Enum
import asyncio
import httpx

# Import payment handlers
from currency_router import CurrencyRouter
from stripe_handler import StripeHandler
from razorpay_handler import RazorpayHandler  
from paypal_handler import PayPalHandler
from payu_handler import PayUHandler

app = FastAPI(
    title="BizOSaaS Payment Service",
    description="Multi-currency payment processing for Bizoholic (USD) and CoreLDove (INR)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class PaymentRequest(BaseModel):
    amount: Decimal
    currency: Currency
    platform: PaymentPlatform
    customer_email: EmailStr
    customer_name: str
    payment_method: Optional[PaymentMethod] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class PaymentResponse(BaseModel):
    payment_id: str
    status: str
    platform: str
    currency: str
    amount: Decimal
    payment_method: str
    client_secret: Optional[str] = None
    checkout_url: Optional[str] = None
    
# Initialize payment handlers
currency_router = CurrencyRouter()
stripe_handler = StripeHandler()
razorpay_handler = RazorpayHandler()
paypal_handler = PayPalHandler()
payu_handler = PayUHandler()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "payment-service",
        "supported_currencies": ["USD", "INR"],
        "supported_platforms": ["bizoholic", "coreldove"],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/payment-methods/{platform}")
async def get_payment_methods(platform: PaymentPlatform):
    """Get available payment methods for platform"""
    
    if platform == PaymentPlatform.BIZOHOLIC:
        return {
            "platform": "bizoholic",
            "currency": "USD",
            "market": "United States",
            "methods": [
                {
                    "id": "stripe",
                    "name": "Credit/Debit Card", 
                    "provider": "Stripe",
                    "priority": 1,
                    "fees": "2.9% + $0.30",
                    "supported": ["visa", "mastercard", "amex", "discover"]
                },
                {
                    "id": "paypal",
                    "name": "PayPal",
                    "provider": "PayPal", 
                    "priority": 2,
                    "fees": "2.9% + $0.30",
                    "supported": ["paypal_account", "credit_card"]
                }
            ]
        }
    
    elif platform == PaymentPlatform.CORELDOVE:
        return {
            "platform": "coreldove",
            "currency": "INR", 
            "market": "India",
            "methods": [
                {
                    "id": "razorpay",
                    "name": "UPI/Cards/Net Banking",
                    "provider": "Razorpay",
                    "priority": 1, 
                    "fees": "2.0%",
                    "supported": ["upi", "card", "netbanking", "wallet"]
                },
                {
                    "id": "payu",
                    "name": "PayU Money",
                    "provider": "PayU",
                    "priority": 2,
                    "fees": "2.3%", 
                    "supported": ["upi", "card", "netbanking", "emi"]
                },
                {
                    "id": "paypal",
                    "name": "PayPal International",
                    "provider": "PayPal",
                    "priority": 3,
                    "fees": "4.4% + ₹15",
                    "supported": ["paypal_account", "international_cards"]
                }
            ]
        }

@app.post("/payments/create", response_model=PaymentResponse)
async def create_payment(payment_request: PaymentRequest):
    """Create a new payment"""
    
    try:
        # Route payment method based on platform and currency
        if not payment_request.payment_method:
            payment_request.payment_method = currency_router.get_primary_method(
                payment_request.platform, 
                payment_request.currency
            )
        
        # Validate currency-platform combination
        if payment_request.platform == PaymentPlatform.BIZOHOLIC and payment_request.currency != Currency.USD:
            raise HTTPException(status_code=400, detail="Bizoholic only supports USD payments")
            
        if payment_request.platform == PaymentPlatform.CORELDOVE and payment_request.currency != Currency.INR:
            if payment_request.currency != Currency.USD:  # Allow USD for international customers
                raise HTTPException(status_code=400, detail="CoreLDove primarily supports INR payments")
        
        # Route to appropriate payment handler
        if payment_request.payment_method == PaymentMethod.STRIPE:
            result = await stripe_handler.create_payment(payment_request)
        elif payment_request.payment_method == PaymentMethod.RAZORPAY:
            result = await razorpay_handler.create_payment(payment_request)
        elif payment_request.payment_method == PaymentMethod.PAYPAL:
            result = await paypal_handler.create_payment(payment_request)
        elif payment_request.payment_method == PaymentMethod.PAYU:
            result = await payu_handler.create_payment(payment_request)
        else:
            raise HTTPException(status_code=400, detail="Unsupported payment method")
            
        return PaymentResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment creation failed: {str(e)}")

@app.get("/payments/{payment_id}")
async def get_payment_status(payment_id: str):
    """Get payment status"""
    
    # This would query your database to find the payment
    # For now, return a mock response
    return {
        "payment_id": payment_id,
        "status": "pending", 
        "created_at": datetime.utcnow().isoformat(),
        "message": "Payment status lookup - implement database integration"
    }

@app.post("/webhooks/stripe")
async def stripe_webhook(request: Dict[str, Any]):
    """Handle Stripe webhooks"""
    return await stripe_handler.handle_webhook(request)

@app.post("/webhooks/razorpay")
async def razorpay_webhook(request: Dict[str, Any]):
    """Handle Razorpay webhooks"""
    return await razorpay_handler.handle_webhook(request)

@app.post("/webhooks/paypal")
async def paypal_webhook(request: Dict[str, Any]):
    """Handle PayPal webhooks"""
    return await paypal_handler.handle_webhook(request)

@app.post("/webhooks/payu")
async def payu_webhook(request: Dict[str, Any]):
    """Handle PayU webhooks"""
    return await payu_handler.handle_webhook(request)

@app.get("/analytics/payments")
async def payment_analytics():
    """Payment analytics and metrics"""
    return {
        "total_payments": 0,
        "successful_payments": 0, 
        "failed_payments": 0,
        "revenue_by_platform": {
            "bizoholic_usd": 0.00,
            "coreldove_inr": 0.00
        },
        "top_payment_methods": [],
        "message": "Implement analytics with database integration"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
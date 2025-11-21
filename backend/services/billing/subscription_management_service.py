"""
Enhanced Subscription Management Service
Multi-gateway support with Indian pricing, usage-based billing, and lifecycle management
Supports Bizoholic SaaS, CoreLDove marketplace, and ThrillRing gaming subscriptions
"""

import asyncio
import logging
import json
from datetime import datetime, date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Dict, List, Optional, Union, Tuple
from uuid import UUID, uuid4

from sqlalchemy import text, select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from core.error_handler import ErrorHandler
from services.multi_payment_gateway_service import (
    multi_payment_service, PaymentGateway, Currency, TransactionType
)
from services.indian_tax_compliance_service import indian_tax_service


class SubscriptionStatus(Enum):
    ACTIVE = "active"
    TRIALING = "trialing"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    SUSPENDED = "suspended"
    EXPIRED = "expired"


class BillingInterval(Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    WEEKLY = "weekly"


class PlanTier(Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class Platform(Enum):
    BIZOSAAS = "bizosaas"  # AI Marketing Agency SaaS
    CORELDOVE = "coreldove"  # E-commerce marketplace
    THRILLRING = "thrillring"  # Gaming platform


class SubscriptionManagementService:
    """Main service for subscription lifecycle management"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_handler = ErrorHandler()
        
        # Usage-based pricing rates (per operation/transaction)
        self.usage_rates = {
            Platform.BIZOSAAS: {
                "ai_operation": Decimal('0.10'),  # ₹0.10 per AI operation
                "campaign_creation": Decimal('2.00'),  # ₹2 per campaign
                "report_generation": Decimal('1.50'),  # ₹1.50 per report
                "api_call": Decimal('0.05')  # ₹0.05 per API call
            },
            Platform.CORELDOVE: {
                "transaction": Decimal('0.02'),  # 2% of transaction value
                "listing_fee": Decimal('5.00'),  # ₹5 per product listing
                "featured_listing": Decimal('25.00'),  # ₹25 per featured listing
                "seller_verification": Decimal('500.00')  # ₹500 per verification
            },
            Platform.THRILLRING: {
                "tournament_entry": Decimal('0.20'),  # 20% of entry fee
                "premium_feature": Decimal('10.00'),  # ₹10 per premium feature unlock
                "leaderboard_boost": Decimal('50.00'),  # ₹50 per boost
                "custom_tournament": Decimal('200.00')  # ₹200 per custom tournament
            }
        }
    
    async def create_subscription(
        self,
        tenant_id: UUID,
        user_id: UUID,
        plan_id: UUID,
        payment_gateway: PaymentGateway,
        customer_data: Dict,
        trial_days: int = 0,
        custom_pricing: Dict = None
    ) -> Dict:
        """Create a new subscription with multi-gateway support"""
        
        try:
            # Get plan details
            plan_details = await self._get_plan_details(plan_id)
            if not plan_details:
                return {
                    "success": False,
                    "error": "Subscription plan not found"
                }
            
            # Determine currency based on customer location
            currency = self._determine_currency(customer_data.get("country", "IN"))
            
            # Get pricing for the currency
            pricing = self._get_plan_pricing(plan_details, currency, custom_pricing)
            
            # Calculate trial period
            trial_start = date.today() if trial_days > 0 else None
            trial_end = (date.today() + timedelta(days=trial_days)) if trial_days > 0 else None
            
            # Calculate first billing period
            if trial_end:
                period_start = trial_end + timedelta(days=1)
            else:
                period_start = date.today()
            
            period_end = self._calculate_period_end(period_start, plan_details["billing_interval"])
            
            # Calculate tax (for Indian customers)
            tax_calculation = None
            if currency == Currency.INR:
                tax_calc_result = await indian_tax_service.calculate_payment_tax(
                    tenant_id=tenant_id,
                    payment_data={
                        "amount": float(pricing["plan_amount"]),
                        "service_type": "saas_services",
                        "customer_state": customer_data.get("state", "MAHARASHTRA"),
                        "is_export": False
                    }
                )
                if tax_calc_result.get("success"):
                    tax_calculation = tax_calc_result["tax_calculation"]
            
            # Create gateway-specific subscription if not in trial
            gateway_subscription_id = None
            if trial_days == 0:
                gateway_result = await self._create_gateway_subscription(
                    payment_gateway=payment_gateway,
                    plan_details=plan_details,
                    pricing=pricing,
                    customer_data=customer_data,
                    tax_calculation=tax_calculation
                )
                
                if not gateway_result.get("success"):
                    return gateway_result
                
                gateway_subscription_id = gateway_result["subscription_id"]
            
            # Store subscription in database
            async with get_db() as db:
                insert_query = text("""
                    INSERT INTO enhanced_subscriptions (
                        tenant_id, user_id, plan_id, status, current_period_start, current_period_end,
                        payment_gateway, gateway_subscription_id, currency, plan_amount, total_amount,
                        tax_amount, tax_breakdown, ai_operations_limit, auto_renew, next_billing_date,
                        trial_start, trial_end, activated_at
                    ) VALUES (
                        :tenant_id, :user_id, :plan_id, :status, :period_start, :period_end,
                        :payment_gateway, :gateway_subscription_id, :currency, :plan_amount, :total_amount,
                        :tax_amount, :tax_breakdown, :ai_operations_limit, :auto_renew, :next_billing_date,
                        :trial_start, :trial_end, :activated_at
                    ) RETURNING id
                """)
                
                total_amount = pricing["plan_amount"]
                tax_amount = Decimal('0.00')
                if tax_calculation:
                    tax_amount = Decimal(str(tax_calculation["total_gst"]))
                    total_amount += tax_amount
                
                status = SubscriptionStatus.TRIALING.value if trial_days > 0 else SubscriptionStatus.ACTIVE.value
                
                result = await db.execute(insert_query, {
                    "tenant_id": str(tenant_id),
                    "user_id": str(user_id),
                    "plan_id": str(plan_id),
                    "status": status,
                    "period_start": period_start,
                    "period_end": period_end,
                    "payment_gateway": payment_gateway.value,
                    "gateway_subscription_id": gateway_subscription_id,
                    "currency": currency.value,
                    "plan_amount": float(pricing["plan_amount"]),
                    "total_amount": float(total_amount),
                    "tax_amount": float(tax_amount),
                    "tax_breakdown": json.dumps(tax_calculation) if tax_calculation else None,
                    "ai_operations_limit": plan_details["max_ai_operations"],
                    "auto_renew": True,
                    "next_billing_date": period_end if trial_days == 0 else period_start,
                    "trial_start": trial_start,
                    "trial_end": trial_end,
                    "activated_at": datetime.now()
                })
                
                subscription_id = result.scalar()
                await db.commit()
                
                self.logger.info(f"Subscription created: {subscription_id} for tenant {tenant_id}")
                
                return {
                    "success": True,
                    "subscription_id": str(subscription_id),
                    "status": status,
                    "trial_days": trial_days,
                    "next_billing_date": period_end.isoformat() if trial_days == 0 else period_start.isoformat(),
                    "pricing": {
                        "plan_amount": float(pricing["plan_amount"]),
                        "tax_amount": float(tax_amount),
                        "total_amount": float(total_amount),
                        "currency": currency.value
                    },
                    "gateway_subscription_id": gateway_subscription_id
                }
                
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "subscription_management",
                "action": "create_subscription",
                "tenant_id": str(tenant_id)
            })
            return {
                "success": False,
                "error": str(e)
            }
    
    async def process_subscription_billing(
        self,
        subscription_id: UUID,
        billing_date: date = None
    ) -> Dict:
        """Process subscription billing for a given period"""
        
        try:
            if not billing_date:
                billing_date = date.today()
            
            # Get subscription details
            subscription = await self._get_subscription_details(subscription_id)
            if not subscription:
                return {
                    "success": False,
                    "error": "Subscription not found"
                }
            
            # Check if billing is due
            if subscription["next_billing_date"] > billing_date:
                return {
                    "success": False,
                    "error": "Billing not due yet",
                    "next_billing_date": subscription["next_billing_date"].isoformat()
                }
            
            # Calculate usage charges for the period
            usage_charges = await self._calculate_usage_charges(
                tenant_id=UUID(subscription["tenant_id"]),
                subscription_id=subscription_id,
                period_start=subscription["current_period_start"],
                period_end=subscription["current_period_end"]
            )
            
            # Get plan pricing
            plan_amount = Decimal(str(subscription["plan_amount"]))
            total_usage_amount = Decimal(str(usage_charges["total_amount"]))
            
            # Calculate tax
            tax_calculation = None
            if subscription["currency"] == "INR":
                tax_calc_result = await indian_tax_service.calculate_payment_tax(
                    tenant_id=UUID(subscription["tenant_id"]),
                    payment_data={
                        "amount": float(plan_amount + total_usage_amount),
                        "service_type": "saas_services",
                        "customer_state": subscription.get("customer_state", "MAHARASHTRA")
                    }
                )
                if tax_calc_result.get("success"):
                    tax_calculation = tax_calc_result["tax_calculation"]
            
            # Calculate total amount
            subtotal = plan_amount + total_usage_amount
            tax_amount = Decimal(str(tax_calculation["total_gst"])) if tax_calculation else Decimal('0.00')
            total_amount = subtotal + tax_amount
            
            # Create payment
            payment_result = await multi_payment_service.create_payment(
                tenant_id=UUID(subscription["tenant_id"]),
                user_id=UUID(subscription["user_id"]),
                amount=total_amount,
                currency=Currency(subscription["currency"]),
                transaction_type=TransactionType.SUBSCRIPTION,
                description=f"Subscription billing for {subscription['plan_name']}",
                metadata={
                    "subscription_id": str(subscription_id),
                    "billing_period": f"{subscription['current_period_start']} to {subscription['current_period_end']}",
                    "plan_amount": float(plan_amount),
                    "usage_amount": float(total_usage_amount),
                    "usage_breakdown": usage_charges["breakdown"]
                },
                customer_data={
                    "name": subscription.get("customer_name"),
                    "email": subscription.get("customer_email"),
                    "phone": subscription.get("customer_phone"),
                    "country": subscription.get("customer_country", "IN"),
                    "state": subscription.get("customer_state")
                }
            )
            
            if not payment_result.get("success"):
                return {
                    "success": False,
                    "error": f"Payment creation failed: {payment_result.get('error')}"
                }
            
            # Update subscription with usage and next billing period
            next_period_start = subscription["current_period_end"] + timedelta(days=1)
            next_period_end = self._calculate_period_end(
                next_period_start, 
                subscription["billing_interval"]
            )
            
            async with get_db() as db:
                update_query = text("""
                    UPDATE enhanced_subscriptions SET
                        current_period_start = :next_period_start,
                        current_period_end = :next_period_end,
                        next_billing_date = :next_billing_date,
                        usage_amount = :usage_amount,
                        ai_operations_used = 0,  -- Reset usage counter
                        updated_at = NOW()
                    WHERE id = :subscription_id
                """)
                
                await db.execute(update_query, {
                    "subscription_id": str(subscription_id),
                    "next_period_start": next_period_start,
                    "next_period_end": next_period_end,
                    "next_billing_date": next_period_end,
                    "usage_amount": float(total_usage_amount)
                })
                await db.commit()
            
            # Generate invoice if Indian customer
            invoice_result = None
            if subscription["currency"] == "INR":
                invoice_data = {
                    "recipient_name": subscription.get("customer_name", "Customer"),
                    "recipient_email": subscription.get("customer_email"),
                    "recipient_state": subscription.get("customer_state", "MAHARASHTRA"),
                    "line_items": [
                        {
                            "description": f"Subscription: {subscription['plan_name']}",
                            "amount": float(plan_amount),
                            "gst_rate": "SAAS_SERVICES"
                        }
                    ]
                }
                
                # Add usage charges as separate line items
                if usage_charges["breakdown"]:
                    for usage_type, usage_data in usage_charges["breakdown"].items():
                        if usage_data["amount"] > 0:
                            invoice_data["line_items"].append({
                                "description": f"Usage charges: {usage_type}",
                                "amount": float(usage_data["amount"]),
                                "gst_rate": "SAAS_SERVICES"
                            })
                
                invoice_result = await indian_tax_service.generate_gst_invoice(
                    tenant_id=UUID(subscription["tenant_id"]),
                    invoice_data=invoice_data
                )
            
            return {
                "success": True,
                "subscription_id": str(subscription_id),
                "billing_summary": {
                    "plan_amount": float(plan_amount),
                    "usage_amount": float(total_usage_amount),
                    "tax_amount": float(tax_amount),
                    "total_amount": float(total_amount),
                    "currency": subscription["currency"],
                    "billing_period": f"{subscription['current_period_start']} to {subscription['current_period_end']}"
                },
                "usage_breakdown": usage_charges["breakdown"],
                "payment": {
                    "payment_id": payment_result["payment_id"],
                    "gateway": payment_result["gateway"]
                },
                "invoice": invoice_result if invoice_result and invoice_result.get("success") else None,
                "next_billing_date": next_period_end.isoformat()
            }
            
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "subscription_management",
                "action": "process_subscription_billing",
                "subscription_id": str(subscription_id)
            })
            return {
                "success": False,
                "error": str(e)
            }
    
    async def track_usage(
        self,
        tenant_id: UUID,
        subscription_id: UUID,
        usage_type: str,
        quantity: int = 1,
        value: Decimal = None,
        metadata: Dict = None
    ) -> Dict:
        """Track usage for subscription billing"""
        
        try:
            # Get subscription details
            subscription = await self._get_subscription_details(subscription_id)
            if not subscription:
                return {
                    "success": False,
                    "error": "Subscription not found"
                }
            
            # Determine platform and calculate cost
            platform = self._determine_platform_from_subscription(subscription)
            usage_rates = self.usage_rates.get(platform, {})
            
            if usage_type not in usage_rates:
                cost_per_unit = Decimal('0.10')  # Default rate
            else:
                cost_per_unit = usage_rates[usage_type]
            
            # For percentage-based pricing (like marketplace transactions)
            if usage_type == "transaction" and value:
                total_cost = value * cost_per_unit
            else:
                total_cost = cost_per_unit * quantity
            
            # Store usage record
            async with get_db() as db:
                insert_query = text("""
                    INSERT INTO subscription_usage_tracking (
                        subscription_id, tenant_id, usage_type, quantity, unit_cost, total_cost,
                        usage_date, metadata, billing_period_start, billing_period_end
                    ) VALUES (
                        :subscription_id, :tenant_id, :usage_type, :quantity, :unit_cost, :total_cost,
                        :usage_date, :metadata, :period_start, :period_end
                    ) RETURNING id
                """)
                
                result = await db.execute(insert_query, {
                    "subscription_id": str(subscription_id),
                    "tenant_id": str(tenant_id),
                    "usage_type": usage_type,
                    "quantity": quantity,
                    "unit_cost": float(cost_per_unit),
                    "total_cost": float(total_cost),
                    "usage_date": datetime.now(),
                    "metadata": json.dumps(metadata or {}),
                    "period_start": subscription["current_period_start"],
                    "period_end": subscription["current_period_end"]
                })
                
                usage_id = result.scalar()
                
                # Update subscription usage counter if it's AI operations
                if usage_type in ["ai_operation", "campaign_creation", "report_generation"]:
                    update_query = text("""
                        UPDATE enhanced_subscriptions SET
                            ai_operations_used = ai_operations_used + :quantity,
                            updated_at = NOW()
                        WHERE id = :subscription_id
                    """)
                    
                    await db.execute(update_query, {
                        "subscription_id": str(subscription_id),
                        "quantity": quantity
                    })
                
                await db.commit()
                
                return {
                    "success": True,
                    "usage_id": str(usage_id),
                    "cost_calculated": float(total_cost),
                    "usage_type": usage_type,
                    "quantity": quantity
                }
                
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "subscription_management",
                "action": "track_usage",
                "subscription_id": str(subscription_id)
            })
            return {
                "success": False,
                "error": str(e)
            }
    
    async def cancel_subscription(
        self,
        subscription_id: UUID,
        reason: str = None,
        immediate: bool = False
    ) -> Dict:
        """Cancel a subscription"""
        
        try:
            subscription = await self._get_subscription_details(subscription_id)
            if not subscription:
                return {
                    "success": False,
                    "error": "Subscription not found"
                }
            
            if subscription["status"] == SubscriptionStatus.CANCELLED.value:
                return {
                    "success": False,
                    "error": "Subscription already cancelled"
                }
            
            # Cancel gateway subscription if exists
            gateway_cancellation_result = None
            if subscription["gateway_subscription_id"]:
                gateway_cancellation_result = await self._cancel_gateway_subscription(
                    payment_gateway=PaymentGateway(subscription["payment_gateway"]),
                    gateway_subscription_id=subscription["gateway_subscription_id"],
                    immediate=immediate
                )
            
            # Update subscription status
            async with get_db() as db:
                if immediate:
                    status = SubscriptionStatus.CANCELLED.value
                    cancelled_at = datetime.now()
                    # Set period end to today for immediate cancellation
                    period_end = date.today()
                else:
                    status = subscription["status"]  # Keep current status until period ends
                    cancelled_at = datetime.now()
                    # Let subscription run until current period ends
                    period_end = subscription["current_period_end"]
                
                update_query = text("""
                    UPDATE enhanced_subscriptions SET
                        status = CASE 
                            WHEN :immediate THEN 'cancelled'
                            ELSE status
                        END,
                        cancelled_at = :cancelled_at,
                        cancelled_reason = :reason,
                        auto_renew = false,
                        current_period_end = CASE 
                            WHEN :immediate THEN :period_end
                            ELSE current_period_end
                        END,
                        updated_at = NOW()
                    WHERE id = :subscription_id
                """)
                
                await db.execute(update_query, {
                    "subscription_id": str(subscription_id),
                    "immediate": immediate,
                    "cancelled_at": cancelled_at,
                    "reason": reason,
                    "period_end": period_end
                })
                await db.commit()
                
                return {
                    "success": True,
                    "subscription_id": str(subscription_id),
                    "cancellation_type": "immediate" if immediate else "end_of_period",
                    "cancelled_at": cancelled_at.isoformat(),
                    "final_period_end": period_end.isoformat(),
                    "gateway_cancellation": gateway_cancellation_result
                }
                
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "subscription_management",
                "action": "cancel_subscription",
                "subscription_id": str(subscription_id)
            })
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_subscription_analytics(
        self,
        tenant_id: UUID = None,
        time_period: str = "last_30_days"
    ) -> Dict:
        """Get subscription analytics and metrics"""
        
        try:
            # Calculate date range
            if time_period == "last_30_days":
                start_date = date.today() - timedelta(days=30)
                end_date = date.today()
            elif time_period == "this_month":
                start_date = date.today().replace(day=1)
                end_date = date.today()
            elif time_period == "last_month":
                last_month_end = date.today().replace(day=1) - timedelta(days=1)
                start_date = last_month_end.replace(day=1)
                end_date = last_month_end
            else:
                start_date = date.today() - timedelta(days=30)
                end_date = date.today()
            
            async with get_db() as db:
                tenant_filter = "WHERE s.tenant_id = :tenant_id" if tenant_id else ""
                tenant_params = {"tenant_id": str(tenant_id)} if tenant_id else {}
                
                # Overall subscription metrics
                overview_query = text(f"""
                    SELECT 
                        COUNT(*) as total_subscriptions,
                        COUNT(*) FILTER (WHERE status = 'active') as active_subscriptions,
                        COUNT(*) FILTER (WHERE status = 'trialing') as trial_subscriptions,
                        COUNT(*) FILTER (WHERE status = 'cancelled') as cancelled_subscriptions,
                        SUM(plan_amount) FILTER (WHERE status = 'active') as total_mrr,
                        SUM(usage_amount) FILTER (WHERE status = 'active') as total_usage_revenue,
                        AVG(plan_amount) FILTER (WHERE status = 'active') as avg_plan_amount,
                        COUNT(DISTINCT currency) as currencies_active
                    FROM enhanced_subscriptions s
                    {tenant_filter}
                """)
                
                # Subscription changes in period
                changes_query = text(f"""
                    SELECT 
                        COUNT(*) FILTER (WHERE activated_at >= :start_date AND activated_at <= :end_date) as new_subscriptions,
                        COUNT(*) FILTER (WHERE cancelled_at >= :start_date AND cancelled_at <= :end_date) as cancelled_subscriptions,
                        SUM(plan_amount) FILTER (WHERE activated_at >= :start_date AND activated_at <= :end_date) as new_mrr,
                        SUM(plan_amount) FILTER (WHERE cancelled_at >= :start_date AND cancelled_at <= :end_date) as churned_mrr
                    FROM enhanced_subscriptions s
                    {tenant_filter}
                """)
                
                # Plan distribution
                plan_query = text(f"""
                    SELECT 
                        sp.name as plan_name,
                        sp.price_inr,
                        COUNT(s.id) as subscriber_count,
                        SUM(s.plan_amount) as plan_revenue
                    FROM enhanced_subscriptions s
                    JOIN enhanced_subscription_plans sp ON s.plan_id = sp.id
                    {tenant_filter.replace('s.tenant_id', 's.tenant_id')}
                    AND s.status = 'active'
                    GROUP BY sp.id, sp.name, sp.price_inr
                    ORDER BY subscriber_count DESC
                """)
                
                # Usage analytics
                usage_query = text(f"""
                    SELECT 
                        sut.usage_type,
                        COUNT(*) as usage_events,
                        SUM(sut.quantity) as total_quantity,
                        SUM(sut.total_cost) as total_usage_revenue,
                        AVG(sut.total_cost) as avg_cost_per_event
                    FROM subscription_usage_tracking sut
                    JOIN enhanced_subscriptions s ON sut.subscription_id = s.id
                    WHERE sut.usage_date >= :start_date 
                    AND sut.usage_date <= :end_date
                    {tenant_filter.replace('WHERE s.tenant_id', 'AND s.tenant_id')}
                    GROUP BY sut.usage_type
                    ORDER BY total_usage_revenue DESC
                """)
                
                params = {
                    "start_date": start_date,
                    "end_date": end_date,
                    **tenant_params
                }
                
                # Execute all queries
                overview_result = await db.execute(overview_query, tenant_params)
                changes_result = await db.execute(changes_query, params)
                plan_result = await db.execute(plan_query, tenant_params)
                usage_result = await db.execute(usage_query, params)
                
                # Process results
                overview_row = overview_result.first()
                changes_row = changes_result.first()
                
                plan_distribution = []
                for row in plan_result:
                    plan_distribution.append({
                        "plan_name": row.plan_name,
                        "price_inr": float(row.price_inr or 0),
                        "subscriber_count": row.subscriber_count,
                        "plan_revenue": float(row.plan_revenue or 0)
                    })
                
                usage_breakdown = []
                for row in usage_result:
                    usage_breakdown.append({
                        "usage_type": row.usage_type,
                        "usage_events": row.usage_events,
                        "total_quantity": row.total_quantity,
                        "total_revenue": float(row.total_usage_revenue or 0),
                        "avg_cost_per_event": float(row.avg_cost_per_event or 0)
                    })
                
                # Calculate key metrics
                mrr = float(overview_row.total_mrr or 0)
                arr = mrr * 12
                
                new_subscriptions = changes_row.new_subscriptions or 0
                cancelled_subscriptions = changes_row.cancelled_subscriptions or 0
                net_new = new_subscriptions - cancelled_subscriptions
                
                # Calculate churn rate
                active_count = overview_row.active_subscriptions or 1
                churn_rate = (cancelled_subscriptions / active_count) * 100
                
                return {
                    "success": True,
                    "period": f"{start_date} to {end_date}",
                    "overview": {
                        "total_subscriptions": overview_row.total_subscriptions or 0,
                        "active_subscriptions": overview_row.active_subscriptions or 0,
                        "trial_subscriptions": overview_row.trial_subscriptions or 0,
                        "cancelled_subscriptions": overview_row.cancelled_subscriptions or 0,
                        "mrr": mrr,
                        "arr": arr,
                        "total_usage_revenue": float(overview_row.total_usage_revenue or 0),
                        "avg_plan_amount": float(overview_row.avg_plan_amount or 0),
                        "currencies_active": overview_row.currencies_active or 0
                    },
                    "period_changes": {
                        "new_subscriptions": new_subscriptions,
                        "cancelled_subscriptions": cancelled_subscriptions,
                        "net_new_subscriptions": net_new,
                        "new_mrr": float(changes_row.new_mrr or 0),
                        "churned_mrr": float(changes_row.churned_mrr or 0),
                        "churn_rate": round(churn_rate, 2)
                    },
                    "plan_distribution": plan_distribution,
                    "usage_breakdown": usage_breakdown,
                    "generated_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "subscription_management",
                "action": "get_subscription_analytics",
                "tenant_id": str(tenant_id) if tenant_id else None
            })
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _get_plan_details(self, plan_id: UUID) -> Optional[Dict]:
        """Get subscription plan details"""
        
        try:
            async with get_db() as db:
                query = text("""
                    SELECT * FROM enhanced_subscription_plans 
                    WHERE id = :plan_id AND is_active = true
                """)
                
                result = await db.execute(query, {"plan_id": str(plan_id)})
                row = result.first()
                
                if row:
                    return {
                        "id": str(row.id),
                        "name": row.name,
                        "description": row.description,
                        "price_inr": Decimal(str(row.price_inr or 0)),
                        "price_usd": Decimal(str(row.price_usd or 0)),
                        "price_eur": Decimal(str(row.price_eur or 0)),
                        "billing_interval": row.billing_interval,
                        "trial_period_days": row.trial_period_days or 0,
                        "max_ai_operations": row.max_ai_operations,
                        "max_users": row.max_users,
                        "features": row.features or {}
                    }
                
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to get plan details: {e}")
            return None
    
    def _determine_currency(self, country: str) -> Currency:
        """Determine currency based on customer country"""
        
        country_currency_map = {
            "IN": Currency.INR,
            "US": Currency.USD,
            "GB": Currency.GBP,
            "AU": Currency.AUD,
            "CA": Currency.USD,
            "DE": Currency.EUR,
            "FR": Currency.EUR,
            "IT": Currency.EUR,
            "ES": Currency.EUR,
            "NL": Currency.EUR
        }
        
        return country_currency_map.get(country, Currency.INR)  # Default to INR
    
    def _get_plan_pricing(
        self,
        plan_details: Dict,
        currency: Currency,
        custom_pricing: Dict = None
    ) -> Dict:
        """Get plan pricing for the specified currency"""
        
        if custom_pricing:
            return {
                "plan_amount": Decimal(str(custom_pricing.get("amount", 0))),
                "currency": currency.value,
                "custom": True
            }
        
        price_field = f"price_{currency.value.lower()}"
        plan_amount = plan_details.get(price_field, Decimal('0.00'))
        
        return {
            "plan_amount": plan_amount,
            "currency": currency.value,
            "custom": False
        }
    
    def _calculate_period_end(self, start_date: date, billing_interval: str) -> date:
        """Calculate billing period end date"""
        
        if billing_interval == "monthly":
            if start_date.month == 12:
                return date(start_date.year + 1, 1, start_date.day) - timedelta(days=1)
            else:
                try:
                    return date(start_date.year, start_date.month + 1, start_date.day) - timedelta(days=1)
                except ValueError:
                    # Handle case where next month doesn't have the same day (e.g., Jan 31 -> Feb 28)
                    next_month = start_date.replace(day=1, month=start_date.month + 1)
                    return (next_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        elif billing_interval == "quarterly":
            return start_date + timedelta(days=90)
        
        elif billing_interval == "yearly":
            try:
                return date(start_date.year + 1, start_date.month, start_date.day) - timedelta(days=1)
            except ValueError:
                # Handle leap year edge case
                return date(start_date.year + 1, start_date.month, start_date.day - 1)
        
        elif billing_interval == "weekly":
            return start_date + timedelta(days=7)
        
        else:
            # Default to monthly
            return start_date + timedelta(days=30)
    
    async def _get_subscription_details(self, subscription_id: UUID) -> Optional[Dict]:
        """Get subscription details from database"""
        
        try:
            async with get_db() as db:
                query = text("""
                    SELECT 
                        s.*,
                        sp.name as plan_name,
                        sp.billing_interval,
                        u.email as customer_email,
                        u.name as customer_name
                    FROM enhanced_subscriptions s
                    JOIN enhanced_subscription_plans sp ON s.plan_id = sp.id
                    JOIN users u ON s.user_id = u.id
                    WHERE s.id = :subscription_id
                """)
                
                result = await db.execute(query, {"subscription_id": str(subscription_id)})
                row = result.first()
                
                if row:
                    return {
                        "id": str(row.id),
                        "tenant_id": row.tenant_id,
                        "user_id": row.user_id,
                        "plan_id": row.plan_id,
                        "plan_name": row.plan_name,
                        "status": row.status,
                        "current_period_start": row.current_period_start,
                        "current_period_end": row.current_period_end,
                        "payment_gateway": row.payment_gateway,
                        "gateway_subscription_id": row.gateway_subscription_id,
                        "currency": row.currency,
                        "plan_amount": row.plan_amount,
                        "usage_amount": row.usage_amount,
                        "total_amount": row.total_amount,
                        "billing_interval": row.billing_interval,
                        "next_billing_date": row.next_billing_date,
                        "customer_email": row.customer_email,
                        "customer_name": row.customer_name,
                        "ai_operations_used": row.ai_operations_used,
                        "ai_operations_limit": row.ai_operations_limit
                    }
                
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to get subscription details: {e}")
            return None
    
    async def _calculate_usage_charges(
        self,
        tenant_id: UUID,
        subscription_id: UUID,
        period_start: date,
        period_end: date
    ) -> Dict:
        """Calculate usage charges for billing period"""
        
        try:
            async with get_db() as db:
                query = text("""
                    SELECT 
                        usage_type,
                        SUM(quantity) as total_quantity,
                        SUM(total_cost) as total_cost,
                        COUNT(*) as usage_events
                    FROM subscription_usage_tracking
                    WHERE subscription_id = :subscription_id
                    AND usage_date >= :period_start
                    AND usage_date <= :period_end
                    GROUP BY usage_type
                """)
                
                result = await db.execute(query, {
                    "subscription_id": str(subscription_id),
                    "period_start": period_start,
                    "period_end": period_end
                })
                
                usage_breakdown = {}
                total_amount = Decimal('0.00')
                
                for row in result:
                    usage_data = {
                        "quantity": row.total_quantity,
                        "amount": Decimal(str(row.total_cost or 0)),
                        "events": row.usage_events
                    }
                    usage_breakdown[row.usage_type] = usage_data
                    total_amount += usage_data["amount"]
                
                return {
                    "breakdown": usage_breakdown,
                    "total_amount": float(total_amount)
                }
                
        except Exception as e:
            self.logger.error(f"Usage charges calculation failed: {e}")
            return {
                "breakdown": {},
                "total_amount": 0.0
            }
    
    def _determine_platform_from_subscription(self, subscription: Dict) -> Platform:
        """Determine platform based on subscription details"""
        
        # This could be enhanced to look at plan features, tenant settings, etc.
        # For now, defaulting to BIZOSAAS
        return Platform.BIZOSAAS
    
    async def _create_gateway_subscription(
        self,
        payment_gateway: PaymentGateway,
        plan_details: Dict,
        pricing: Dict,
        customer_data: Dict,
        tax_calculation: Dict = None
    ) -> Dict:
        """Create subscription at payment gateway level"""
        
        # This would integrate with each gateway's subscription API
        # For now, returning a mock response
        
        gateway_subscription_id = f"{payment_gateway.value}_{uuid4().hex[:12]}"
        
        return {
            "success": True,
            "subscription_id": gateway_subscription_id,
            "gateway": payment_gateway.value
        }
    
    async def _cancel_gateway_subscription(
        self,
        payment_gateway: PaymentGateway,
        gateway_subscription_id: str,
        immediate: bool = False
    ) -> Dict:
        """Cancel subscription at gateway level"""
        
        # This would integrate with each gateway's cancellation API
        # For now, returning a mock response
        
        return {
            "success": True,
            "cancelled": True,
            "gateway": payment_gateway.value,
            "cancellation_type": "immediate" if immediate else "end_of_period"
        }


# Create table for subscription usage tracking if it doesn't exist
async def create_usage_tracking_table():
    """Create subscription usage tracking table"""
    
    try:
        async with get_db() as db:
            create_table_query = text("""
                CREATE TABLE IF NOT EXISTS subscription_usage_tracking (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    subscription_id UUID REFERENCES enhanced_subscriptions(id) ON DELETE CASCADE,
                    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
                    usage_type VARCHAR(100) NOT NULL,
                    quantity INTEGER DEFAULT 1,
                    unit_cost DECIMAL(10,4) NOT NULL,
                    total_cost DECIMAL(15,2) NOT NULL,
                    usage_date TIMESTAMP DEFAULT NOW(),
                    metadata JSONB,
                    billing_period_start DATE,
                    billing_period_end DATE,
                    created_at TIMESTAMP DEFAULT NOW(),
                    
                    INDEX idx_subscription_usage_subscription_id (subscription_id),
                    INDEX idx_subscription_usage_tenant_id (tenant_id),
                    INDEX idx_subscription_usage_date (usage_date),
                    INDEX idx_subscription_usage_billing_period (billing_period_start, billing_period_end)
                )
            """)
            
            await db.execute(create_table_query)
            await db.commit()
            
    except Exception as e:
        logging.error(f"Failed to create usage tracking table: {e}")


# Global instance
subscription_service = SubscriptionManagementService()
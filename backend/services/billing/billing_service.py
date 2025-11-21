"""
Billing Service for Usage-Based AI Agent Cost Tracking and Revenue Management
Critical implementation for production revenue generation
"""

import asyncio
import logging
from datetime import datetime, date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional, Union
from uuid import UUID
import json

import stripe
from sqlalchemy import text, select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.auth_models import User
from core.error_handler import ErrorHandler


class UsageTracker:
    """Track AI agent usage and costs for billing purposes"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # AI Agent cost configuration (per operation)
        self.agent_costs = {
            'marketing_crew': {
                'digital_audit': Decimal('2.50'),
                'campaign_strategy': Decimal('5.00'),
                'content_generation': Decimal('1.50'),
                'optimization': Decimal('3.00')
            },
            'ecommerce_agent': {
                'product_validation': Decimal('1.25'),
                'market_analysis': Decimal('2.00'),
                'competitive_analysis': Decimal('3.50'),
                'recommendation': Decimal('0.75')
            },
            'hierarchical_crew': {
                'client_onboarding': Decimal('8.00'),
                'campaign_development': Decimal('12.00'),
                'content_approval': Decimal('4.00'),
                'execution_monitoring': Decimal('6.00')
            },
            'conservative_estimation': {
                'estimation_analysis': Decimal('2.25'),
                'buffer_optimization': Decimal('1.75'),
                'performance_tracking': Decimal('1.00')
            }
        }
        
        # Token cost calculation (OpenAI pricing)
        self.token_costs = {
            'input': Decimal('0.0010') / 1000,  # $0.0010 per 1K tokens
            'output': Decimal('0.0020') / 1000  # $0.0020 per 1K tokens
        }
    
    async def track_usage(
        self,
        tenant_id: UUID,
        user_id: UUID,
        agent_type: str,
        operation: str,
        tokens_used: int = 0,
        processing_time: int = 0,
        company_id: str = None,
        campaign_id: UUID = None,
        complexity_multiplier: float = 1.0,
        metadata: Dict = None
    ) -> UUID:
        """Track AI agent usage for billing"""
        
        try:
            # Calculate base cost
            base_cost = self.agent_costs.get(agent_type, {}).get(operation, Decimal('1.00'))
            
            # Add token costs if provided
            token_cost = Decimal('0.00')
            if tokens_used > 0:
                # Estimate 70% input, 30% output tokens
                input_tokens = int(tokens_used * 0.7)
                output_tokens = int(tokens_used * 0.3)
                token_cost = (
                    (input_tokens * self.token_costs['input']) +
                    (output_tokens * self.token_costs['output'])
                )
            
            # Apply complexity multiplier
            total_cost = (base_cost + token_cost) * Decimal(complexity_multiplier)
            total_cost = total_cost.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
            
            # Store usage record
            async with get_db() as db:
                query = text("""
                    SELECT track_ai_usage(
                        :tenant_id::UUID,
                        :user_id::UUID,
                        :agent_type,
                        :operation,
                        :cost_amount,
                        :tokens_used,
                        :processing_time,
                        :company_id,
                        :metadata::JSONB
                    )
                """)
                
                result = await db.execute(query, {
                    'tenant_id': str(tenant_id),
                    'user_id': str(user_id),
                    'agent_type': agent_type,
                    'operation': operation,
                    'cost_amount': float(total_cost),
                    'tokens_used': tokens_used,
                    'processing_time': processing_time,
                    'company_id': company_id,
                    'metadata': json.dumps(metadata or {})
                })
                
                usage_id = result.scalar()
                await db.commit()
                
                self.logger.info(f"Usage tracked: {agent_type}/{operation} - ${total_cost} for tenant {tenant_id}")
                return UUID(usage_id)
                
        except Exception as e:
            self.logger.error(f"Failed to track usage: {e}")
            raise


class BillingService:
    """Main billing service for revenue management"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.usage_tracker = UsageTracker()
        self.error_handler = ErrorHandler()
        
        # Initialize Stripe
        stripe.api_key = self._get_stripe_secret_key()
        
    def _get_stripe_secret_key(self) -> str:
        """Get Stripe secret key from environment or database"""
        import os
        return os.getenv('STRIPE_SECRET_KEY', 'sk_test_...')
    
    async def get_usage_summary(
        self,
        tenant_id: UUID,
        start_date: date = None,
        end_date: date = None,
        agent_type: str = None
    ) -> Dict:
        """Get usage summary for a tenant"""
        
        if not start_date:
            start_date = date.today().replace(day=1)  # Start of current month
        if not end_date:
            end_date = date.today()
        
        try:
            async with get_db() as db:
                query = text("""
                    SELECT 
                        agent_type,
                        COUNT(*) as operation_count,
                        SUM(cost_amount) as total_cost,
                        SUM(tokens_used) as total_tokens,
                        AVG(processing_time_seconds) as avg_processing_time
                    FROM ai_agent_usage 
                    WHERE tenant_id = :tenant_id
                    AND usage_date BETWEEN :start_date AND :end_date
                    AND billable = true
                    AND (:agent_type IS NULL OR agent_type = :agent_type)
                    GROUP BY agent_type
                    ORDER BY total_cost DESC
                """)
                
                result = await db.execute(query, {
                    'tenant_id': str(tenant_id),
                    'start_date': start_date,
                    'end_date': end_date,
                    'agent_type': agent_type
                })
                
                usage_data = []
                total_cost = Decimal('0.00')
                total_operations = 0
                
                for row in result:
                    usage_info = {
                        'agent_type': row.agent_type,
                        'operation_count': row.operation_count,
                        'total_cost': float(row.total_cost),
                        'total_tokens': row.total_tokens,
                        'avg_processing_time': float(row.avg_processing_time or 0)
                    }
                    usage_data.append(usage_info)
                    total_cost += Decimal(str(row.total_cost))
                    total_operations += row.operation_count
                
                return {
                    'tenant_id': str(tenant_id),
                    'period': f"{start_date} to {end_date}",
                    'total_cost': float(total_cost),
                    'total_operations': total_operations,
                    'usage_by_agent': usage_data,
                    'cost_per_operation': float(total_cost / total_operations) if total_operations > 0 else 0.00
                }
                
        except Exception as e:
            await self.error_handler.handle_error(e, {
                'component': 'billing_service',
                'action': 'get_usage_summary',
                'tenant_id': str(tenant_id)
            })
            raise
    
    async def calculate_monthly_charges(
        self,
        tenant_id: UUID,
        billing_month: date = None
    ) -> Dict:
        """Calculate monthly charges including subscription and usage"""
        
        if not billing_month:
            billing_month = date.today().replace(day=1)
        
        month_start = billing_month
        month_end = (billing_month.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        
        try:
            async with get_db() as db:
                # Get subscription details
                subscription_query = text("""
                    SELECT s.id, s.plan_id, sp.price_monthly, sp.name as plan_name
                    FROM subscriptions s
                    JOIN subscription_plans sp ON s.plan_id = sp.id
                    WHERE s.tenant_id = :tenant_id AND s.status = 'active'
                    ORDER BY s.created_at DESC
                    LIMIT 1
                """)
                
                subscription_result = await db.execute(subscription_query, {
                    'tenant_id': str(tenant_id)
                })
                subscription = subscription_result.first()
                
                if not subscription:
                    return {
                        'error': 'No active subscription found',
                        'tenant_id': str(tenant_id)
                    }
                
                # Get usage charges
                usage_query = text("""
                    SELECT calculate_usage_charges(:tenant_id::UUID, :start_date, :end_date)
                """)
                
                usage_result = await db.execute(usage_query, {
                    'tenant_id': str(tenant_id),
                    'start_date': month_start,
                    'end_date': month_end
                })
                
                usage_charges = Decimal(str(usage_result.scalar() or '0.00'))
                base_amount = Decimal(str(subscription.price_monthly))
                
                # Calculate tax (8% default)
                subtotal = base_amount + usage_charges
                tax_rate = Decimal('0.08')
                tax_amount = subtotal * tax_rate
                total_amount = subtotal + tax_amount
                
                return {
                    'tenant_id': str(tenant_id),
                    'billing_period': f"{month_start} to {month_end}",
                    'subscription': {
                        'plan_name': subscription.plan_name,
                        'base_amount': float(base_amount)
                    },
                    'usage_charges': float(usage_charges),
                    'subtotal': float(subtotal),
                    'tax_rate': float(tax_rate),
                    'tax_amount': float(tax_amount),
                    'total_amount': float(total_amount),
                    'currency': 'USD'
                }
                
        except Exception as e:
            await self.error_handler.handle_error(e, {
                'component': 'billing_service',
                'action': 'calculate_monthly_charges',
                'tenant_id': str(tenant_id)
            })
            raise
    
    async def create_usage_invoice(
        self,
        tenant_id: UUID,
        billing_month: date = None
    ) -> Dict:
        """Create Stripe invoice for monthly usage"""
        
        charges = await self.calculate_monthly_charges(tenant_id, billing_month)
        
        if 'error' in charges:
            return charges
        
        try:
            async with get_db() as db:
                # Get tenant and customer information
                tenant_query = text("""
                    SELECT t.name, u.email, u.stripe_customer_id
                    FROM tenants t
                    LEFT JOIN users u ON u.tenant_id = t.id AND u.role = 'owner'
                    WHERE t.id = :tenant_id
                    LIMIT 1
                """)
                
                tenant_result = await db.execute(tenant_query, {
                    'tenant_id': str(tenant_id)
                })
                tenant_info = tenant_result.first()
                
                if not tenant_info:
                    return {'error': 'Tenant not found'}
                
                # Create Stripe customer if needed
                stripe_customer_id = tenant_info.stripe_customer_id
                if not stripe_customer_id:
                    customer = stripe.Customer.create(
                        email=tenant_info.email,
                        name=tenant_info.name,
                        metadata={'tenant_id': str(tenant_id)}
                    )
                    stripe_customer_id = customer.id
                    
                    # Update user record
                    update_query = text("""
                        UPDATE users SET stripe_customer_id = :customer_id 
                        WHERE tenant_id = :tenant_id AND role = 'owner'
                    """)
                    await db.execute(update_query, {
                        'customer_id': stripe_customer_id,
                        'tenant_id': str(tenant_id)
                    })
                
                # Create Stripe invoice
                invoice_items = []
                
                # Base subscription charge
                invoice_items.append({
                    'customer': stripe_customer_id,
                    'amount': int(charges['subscription']['base_amount'] * 100),  # Stripe uses cents
                    'currency': 'usd',
                    'description': f"Subscription: {charges['subscription']['plan_name']}"
                })
                
                # Usage charges
                if charges['usage_charges'] > 0:
                    invoice_items.append({
                        'customer': stripe_customer_id,
                        'amount': int(charges['usage_charges'] * 100),
                        'currency': 'usd',
                        'description': f"AI Agent Usage ({charges['billing_period']})"
                    })
                
                # Create invoice items
                for item in invoice_items:
                    stripe.InvoiceItem.create(**item)
                
                # Create and send invoice
                invoice = stripe.Invoice.create(
                    customer=stripe_customer_id,
                    auto_advance=True,
                    metadata={
                        'tenant_id': str(tenant_id),
                        'billing_period': charges['billing_period']
                    }
                )
                
                invoice.finalize_invoice()
                
                # Store billing cycle record
                billing_query = text("""
                    INSERT INTO billing_cycles (
                        tenant_id, cycle_start, cycle_end, base_amount, 
                        usage_amount, tax_amount, total_amount, stripe_invoice_id, due_date
                    ) VALUES (
                        :tenant_id::UUID, :cycle_start, :cycle_end, :base_amount,
                        :usage_amount, :tax_amount, :total_amount, :stripe_invoice_id, :due_date
                    ) RETURNING id
                """)
                
                billing_result = await db.execute(billing_query, {
                    'tenant_id': str(tenant_id),
                    'cycle_start': charges['billing_period'].split(' to ')[0],
                    'cycle_end': charges['billing_period'].split(' to ')[1],
                    'base_amount': charges['subscription']['base_amount'],
                    'usage_amount': charges['usage_charges'],
                    'tax_amount': charges['tax_amount'],
                    'total_amount': charges['total_amount'],
                    'stripe_invoice_id': invoice.id,
                    'due_date': (date.today() + timedelta(days=14)).isoformat()
                })
                
                billing_cycle_id = billing_result.scalar()
                await db.commit()
                
                return {
                    'success': True,
                    'billing_cycle_id': str(billing_cycle_id),
                    'stripe_invoice_id': invoice.id,
                    'invoice_url': invoice.hosted_invoice_url,
                    'total_amount': charges['total_amount'],
                    'due_date': invoice.due_date
                }
                
        except Exception as e:
            await self.error_handler.handle_error(e, {
                'component': 'billing_service',
                'action': 'create_usage_invoice',
                'tenant_id': str(tenant_id)
            })
            raise


class RevenueAnalytics:
    """Revenue analytics and reporting service"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def get_revenue_dashboard(
        self,
        tenant_id: UUID = None,
        days: int = 30
    ) -> Dict:
        """Get comprehensive revenue dashboard data"""
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        try:
            async with get_db() as db:
                # Base query filter
                tenant_filter = "WHERE rm.tenant_id = :tenant_id" if tenant_id else ""
                tenant_param = {'tenant_id': str(tenant_id)} if tenant_id else {}
                
                # Get revenue metrics
                revenue_query = text(f"""
                    SELECT 
                        DATE(metric_date) as date,
                        SUM(mrr) as daily_mrr,
                        SUM(usage_revenue) as daily_usage,
                        SUM(gross_revenue) as daily_gross,
                        COUNT(DISTINCT tenant_id) as active_tenants
                    FROM revenue_metrics rm
                    {tenant_filter}
                    AND metric_date BETWEEN :start_date AND :end_date
                    GROUP BY DATE(metric_date)
                    ORDER BY date DESC
                """)
                
                revenue_result = await db.execute(revenue_query, {
                    'start_date': start_date,
                    'end_date': end_date,
                    **tenant_param
                })
                
                revenue_data = []
                total_mrr = Decimal('0.00')
                total_usage = Decimal('0.00')
                total_gross = Decimal('0.00')
                
                for row in revenue_result:
                    daily_data = {
                        'date': row.date.isoformat(),
                        'mrr': float(row.daily_mrr or 0),
                        'usage_revenue': float(row.daily_usage or 0),
                        'gross_revenue': float(row.daily_gross or 0),
                        'active_tenants': row.active_tenants
                    }
                    revenue_data.append(daily_data)
                    total_mrr += Decimal(str(row.daily_mrr or 0))
                    total_usage += Decimal(str(row.daily_usage or 0))
                    total_gross += Decimal(str(row.daily_gross or 0))
                
                # Get top usage agents
                usage_query = text(f"""
                    SELECT 
                        agent_type,
                        COUNT(*) as operations,
                        SUM(cost_amount) as total_cost,
                        AVG(cost_amount) as avg_cost
                    FROM ai_agent_usage aau
                    {tenant_filter.replace('rm.', 'aau.')}
                    AND usage_date BETWEEN :start_date AND :end_date
                    GROUP BY agent_type
                    ORDER BY total_cost DESC
                    LIMIT 10
                """)
                
                usage_result = await db.execute(usage_query, {
                    'start_date': start_date,
                    'end_date': end_date,
                    **tenant_param
                })
                
                usage_breakdown = []
                for row in usage_result:
                    usage_breakdown.append({
                        'agent_type': row.agent_type,
                        'operations': row.operations,
                        'total_cost': float(row.total_cost),
                        'avg_cost': float(row.avg_cost)
                    })
                
                return {
                    'period': f"{start_date} to {end_date}",
                    'summary': {
                        'total_mrr': float(total_mrr),
                        'total_arr': float(total_mrr * 12),
                        'total_usage_revenue': float(total_usage),
                        'total_gross_revenue': float(total_gross),
                        'revenue_growth': self._calculate_growth(revenue_data)
                    },
                    'daily_revenue': revenue_data,
                    'usage_breakdown': usage_breakdown,
                    'generated_at': datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Failed to generate revenue dashboard: {e}")
            raise
    
    def _calculate_growth(self, revenue_data: List[Dict]) -> float:
        """Calculate revenue growth rate"""
        if len(revenue_data) < 2:
            return 0.0
        
        current = revenue_data[0]['gross_revenue']
        previous = revenue_data[-1]['gross_revenue']
        
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        
        return ((current - previous) / previous) * 100


# Global instances
usage_tracker = UsageTracker()
billing_service = BillingService()
revenue_analytics = RevenueAnalytics()
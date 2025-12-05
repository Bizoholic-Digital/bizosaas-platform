"""
Revenue Analytics Service for Multi-Gateway Payment System
Comprehensive analytics for Indian and global payment processing
Real-time dashboards, reporting, and business intelligence
"""

import asyncio
import logging
import json
from datetime import datetime, date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Dict, List, Optional, Union, Tuple
from uuid import UUID
import pandas as pd

from sqlalchemy import text, select, and_, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from core.error_handler import ErrorHandler


class RevenueMetricType(Enum):
    GROSS_REVENUE = "gross_revenue"
    NET_REVENUE = "net_revenue"
    TAX_COLLECTED = "tax_collected"
    GATEWAY_FEES = "gateway_fees"
    MRR = "monthly_recurring_revenue"
    ARR = "annual_recurring_revenue"
    USAGE_REVENUE = "usage_revenue"
    CHURN_RATE = "churn_rate"
    LTV = "lifetime_value"


class TimePeriod(Enum):
    TODAY = "today"
    YESTERDAY = "yesterday"
    LAST_7_DAYS = "last_7_days"
    LAST_30_DAYS = "last_30_days"
    THIS_MONTH = "this_month"
    LAST_MONTH = "last_month"
    THIS_QUARTER = "this_quarter"
    LAST_QUARTER = "last_quarter"
    THIS_YEAR = "this_year"
    LAST_YEAR = "last_year"
    CUSTOM = "custom"


class Currency(Enum):
    INR = "INR"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    AUD = "AUD"
    ALL = "ALL"


class RevenueAnalyticsService:
    """Main service for revenue analytics and reporting"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_handler = ErrorHandler()
    
    async def get_revenue_dashboard(
        self,
        tenant_id: UUID = None,
        time_period: TimePeriod = TimePeriod.LAST_30_DAYS,
        currency: Currency = Currency.ALL,
        custom_start_date: date = None,
        custom_end_date: date = None
    ) -> Dict:
        """Get comprehensive revenue dashboard data"""
        
        try:
            # Calculate date range
            start_date, end_date = self._calculate_date_range(
                time_period, custom_start_date, custom_end_date
            )
            
            # Get all revenue metrics in parallel
            dashboard_data = await asyncio.gather(
                self._get_revenue_summary(tenant_id, start_date, end_date, currency),
                self._get_payment_gateway_performance(tenant_id, start_date, end_date, currency),
                self._get_revenue_trends(tenant_id, start_date, end_date, currency),
                self._get_subscription_metrics(tenant_id, start_date, end_date, currency),
                self._get_tax_compliance_summary(tenant_id, start_date, end_date),
                self._get_top_performing_services(tenant_id, start_date, end_date, currency),
                self._get_geographic_breakdown(tenant_id, start_date, end_date, currency),
                self._get_payment_method_analysis(tenant_id, start_date, end_date, currency),
                return_exceptions=True
            )
            
            # Process results
            (revenue_summary, gateway_performance, revenue_trends, subscription_metrics,
             tax_summary, top_services, geographic_breakdown, payment_methods) = dashboard_data
            
            # Handle any exceptions
            for i, result in enumerate(dashboard_data):
                if isinstance(result, Exception):
                    self.logger.error(f"Dashboard data component {i} failed: {result}")
            
            return {
                "success": True,
                "period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "period_type": time_period.value,
                    "currency_filter": currency.value
                },
                "revenue_summary": revenue_summary if not isinstance(revenue_summary, Exception) else {},
                "gateway_performance": gateway_performance if not isinstance(gateway_performance, Exception) else {},
                "revenue_trends": revenue_trends if not isinstance(revenue_trends, Exception) else {},
                "subscription_metrics": subscription_metrics if not isinstance(subscription_metrics, Exception) else {},
                "tax_compliance": tax_summary if not isinstance(tax_summary, Exception) else {},
                "top_services": top_services if not isinstance(top_services, Exception) else [],
                "geographic_breakdown": geographic_breakdown if not isinstance(geographic_breakdown, Exception) else {},
                "payment_methods": payment_methods if not isinstance(payment_methods, Exception) else {},
                "generated_at": datetime.now().isoformat(),
                "tenant_id": str(tenant_id) if tenant_id else "all_tenants"
            }
            
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "revenue_analytics",
                "action": "get_revenue_dashboard",
                "tenant_id": str(tenant_id) if tenant_id else None
            })
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _get_revenue_summary(
        self,
        tenant_id: UUID,
        start_date: date,
        end_date: date,
        currency: Currency
    ) -> Dict:
        """Get high-level revenue summary"""
        
        try:
            async with get_db() as db:
                # Build currency filter
                currency_filter = ""
                currency_params = {}
                if currency != Currency.ALL:
                    currency_filter = "AND pt.currency = :currency"
                    currency_params["currency"] = currency.value
                
                # Build tenant filter
                tenant_filter = ""
                tenant_params = {}
                if tenant_id:
                    tenant_filter = "AND pt.tenant_id = :tenant_id"
                    tenant_params["tenant_id"] = str(tenant_id)
                
                # Main revenue query
                revenue_query = text(f"""
                    WITH revenue_data AS (
                        SELECT 
                            pt.currency,
                            SUM(pt.captured_amount) as gross_revenue,
                            SUM(pt.fee_amount) as gateway_fees,
                            SUM(pt.captured_amount - pt.fee_amount) as net_revenue,
                            SUM(pt.total_tax_amount) as tax_collected,
                            COUNT(*) as total_transactions,
                            COUNT(*) FILTER (WHERE pt.status = 'success') as successful_transactions,
                            AVG(pt.captured_amount) FILTER (WHERE pt.status = 'success') as avg_transaction_value,
                            COUNT(DISTINCT pt.tenant_id) as active_tenants
                        FROM payment_transactions pt
                        WHERE pt.created_at >= :start_date
                        AND pt.created_at <= :end_date
                        {tenant_filter}
                        {currency_filter}
                        GROUP BY pt.currency
                    ),
                    previous_period_data AS (
                        SELECT 
                            pt.currency,
                            SUM(pt.captured_amount) as prev_gross_revenue,
                            COUNT(*) as prev_total_transactions
                        FROM payment_transactions pt
                        WHERE pt.created_at >= :prev_start_date
                        AND pt.created_at <= :prev_end_date
                        {tenant_filter}
                        {currency_filter}
                        GROUP BY pt.currency
                    )
                    SELECT 
                        rd.*,
                        ppd.prev_gross_revenue,
                        ppd.prev_total_transactions,
                        CASE 
                            WHEN ppd.prev_gross_revenue > 0 THEN 
                                ((rd.gross_revenue - ppd.prev_gross_revenue) / ppd.prev_gross_revenue) * 100
                            ELSE 0
                        END as revenue_growth_percentage,
                        CASE 
                            WHEN ppd.prev_total_transactions > 0 THEN 
                                ((rd.total_transactions - ppd.prev_total_transactions) / ppd.prev_total_transactions::DECIMAL) * 100
                            ELSE 0
                        END as transaction_growth_percentage
                    FROM revenue_data rd
                    LEFT JOIN previous_period_data ppd ON rd.currency = ppd.currency
                """)
                
                # Calculate previous period dates
                period_days = (end_date - start_date).days + 1
                prev_end_date = start_date - timedelta(days=1)
                prev_start_date = prev_end_date - timedelta(days=period_days - 1)
                
                result = await db.execute(revenue_query, {
                    "start_date": start_date,
                    "end_date": end_date,
                    "prev_start_date": prev_start_date,
                    "prev_end_date": prev_end_date,
                    **tenant_params,
                    **currency_params
                })
                
                currency_summaries = []
                total_gross_revenue = Decimal('0.00')
                total_net_revenue = Decimal('0.00')
                total_transactions = 0
                total_fees = Decimal('0.00')
                total_tax = Decimal('0.00')
                
                for row in result:
                    currency_data = {
                        "currency": row.currency,
                        "gross_revenue": float(row.gross_revenue or 0),
                        "net_revenue": float(row.net_revenue or 0),
                        "gateway_fees": float(row.gateway_fees or 0),
                        "tax_collected": float(row.tax_collected or 0),
                        "total_transactions": row.total_transactions or 0,
                        "successful_transactions": row.successful_transactions or 0,
                        "success_rate": (row.successful_transactions / max(row.total_transactions, 1)) * 100,
                        "avg_transaction_value": float(row.avg_transaction_value or 0),
                        "revenue_growth": float(row.revenue_growth_percentage or 0),
                        "transaction_growth": float(row.transaction_growth_percentage or 0),
                        "active_tenants": row.active_tenants or 0
                    }
                    currency_summaries.append(currency_data)
                    
                    # Aggregate totals (convert everything to INR for totals)
                    if row.currency == 'INR':
                        conversion_rate = 1.0
                    elif row.currency == 'USD':
                        conversion_rate = 83.25  # Should come from exchange rates table
                    else:
                        conversion_rate = 1.0  # Simplified for demo
                    
                    total_gross_revenue += Decimal(str(row.gross_revenue or 0)) * Decimal(str(conversion_rate))
                    total_net_revenue += Decimal(str(row.net_revenue or 0)) * Decimal(str(conversion_rate))
                    total_transactions += row.total_transactions or 0
                    total_fees += Decimal(str(row.gateway_fees or 0)) * Decimal(str(conversion_rate))
                    total_tax += Decimal(str(row.tax_collected or 0)) * Decimal(str(conversion_rate))
                
                # Calculate key metrics
                fee_percentage = (float(total_fees) / float(total_gross_revenue)) * 100 if total_gross_revenue > 0 else 0
                tax_percentage = (float(total_tax) / float(total_gross_revenue)) * 100 if total_gross_revenue > 0 else 0
                
                return {
                    "overview": {
                        "total_gross_revenue_inr": float(total_gross_revenue),
                        "total_net_revenue_inr": float(total_net_revenue),
                        "total_transactions": total_transactions,
                        "total_gateway_fees_inr": float(total_fees),
                        "total_tax_collected_inr": float(total_tax),
                        "average_fee_percentage": round(fee_percentage, 2),
                        "average_tax_percentage": round(tax_percentage, 2)
                    },
                    "by_currency": currency_summaries
                }
                
        except Exception as e:
            self.logger.error(f"Revenue summary calculation failed: {e}")
            raise
    
    async def _get_payment_gateway_performance(
        self,
        tenant_id: UUID,
        start_date: date,
        end_date: date,
        currency: Currency
    ) -> Dict:
        """Get payment gateway performance comparison"""
        
        try:
            async with get_db() as db:
                # Build filters
                currency_filter = "AND pt.currency = :currency" if currency != Currency.ALL else ""
                tenant_filter = "AND pt.tenant_id = :tenant_id" if tenant_id else ""
                
                gateway_query = text(f"""
                    SELECT 
                        pt.gateway,
                        pt.currency,
                        COUNT(*) as total_transactions,
                        COUNT(*) FILTER (WHERE pt.status = 'success') as successful_transactions,
                        COUNT(*) FILTER (WHERE pt.status = 'failed') as failed_transactions,
                        SUM(pt.captured_amount) as total_revenue,
                        SUM(pt.fee_amount) as total_fees,
                        AVG(pt.captured_amount) FILTER (WHERE pt.status = 'success') as avg_transaction_value,
                        AVG(
                            EXTRACT(EPOCH FROM (pt.completed_at - pt.initiated_at))
                        ) FILTER (WHERE pt.status = 'success' AND pt.completed_at IS NOT NULL) as avg_processing_time_seconds,
                        AVG(pt.fee_amount / NULLIF(pt.captured_amount, 0)) * 100 as avg_fee_percentage
                    FROM payment_transactions pt
                    WHERE pt.created_at >= :start_date
                    AND pt.created_at <= :end_date
                    {tenant_filter}
                    {currency_filter}
                    GROUP BY pt.gateway, pt.currency
                    ORDER BY total_revenue DESC
                """)
                
                params = {
                    "start_date": start_date,
                    "end_date": end_date
                }
                if tenant_id:
                    params["tenant_id"] = str(tenant_id)
                if currency != Currency.ALL:
                    params["currency"] = currency.value
                
                result = await db.execute(gateway_query, params)
                
                gateway_performance = []
                for row in result:
                    success_rate = (row.successful_transactions / max(row.total_transactions, 1)) * 100
                    
                    performance_data = {
                        "gateway": row.gateway,
                        "currency": row.currency,
                        "total_transactions": row.total_transactions,
                        "successful_transactions": row.successful_transactions,
                        "failed_transactions": row.failed_transactions,
                        "success_rate": round(success_rate, 2),
                        "total_revenue": float(row.total_revenue or 0),
                        "total_fees": float(row.total_fees or 0),
                        "avg_transaction_value": float(row.avg_transaction_value or 0),
                        "avg_processing_time_seconds": float(row.avg_processing_time_seconds or 0),
                        "avg_fee_percentage": round(float(row.avg_fee_percentage or 0), 2),
                        "market_share": 0.0  # Will be calculated below
                    }
                    gateway_performance.append(performance_data)
                
                # Calculate market share
                total_revenue = sum(gw["total_revenue"] for gw in gateway_performance)
                for gw in gateway_performance:
                    if total_revenue > 0:
                        gw["market_share"] = round((gw["total_revenue"] / total_revenue) * 100, 2)
                
                # Get gateway-specific insights
                gateway_insights = []
                
                # Best performing gateway
                if gateway_performance:
                    best_gateway = max(gateway_performance, key=lambda x: x["success_rate"])
                    gateway_insights.append({
                        "type": "best_performance",
                        "message": f"{best_gateway['gateway']} has the highest success rate at {best_gateway['success_rate']}%",
                        "gateway": best_gateway["gateway"]
                    })
                    
                    # Most cost-effective gateway
                    lowest_fee_gateway = min(gateway_performance, key=lambda x: x["avg_fee_percentage"])
                    gateway_insights.append({
                        "type": "most_cost_effective",
                        "message": f"{lowest_fee_gateway['gateway']} has the lowest average fees at {lowest_fee_gateway['avg_fee_percentage']}%",
                        "gateway": lowest_fee_gateway["gateway"]
                    })
                
                return {
                    "gateway_performance": gateway_performance,
                    "insights": gateway_insights,
                    "total_gateways": len(gateway_performance)
                }
                
        except Exception as e:
            self.logger.error(f"Gateway performance analysis failed: {e}")
            raise
    
    async def _get_revenue_trends(
        self,
        tenant_id: UUID,
        start_date: date,
        end_date: date,
        currency: Currency
    ) -> Dict:
        """Get revenue trends over time"""
        
        try:
            async with get_db() as db:
                # Determine appropriate time grouping based on date range
                date_diff = (end_date - start_date).days
                if date_diff <= 7:
                    time_trunc = 'day'
                elif date_diff <= 90:
                    time_trunc = 'day'
                elif date_diff <= 365:
                    time_trunc = 'week'
                else:
                    time_trunc = 'month'
                
                # Build filters
                currency_filter = "AND pt.currency = :currency" if currency != Currency.ALL else ""
                tenant_filter = "AND pt.tenant_id = :tenant_id" if tenant_id else ""
                
                trends_query = text(f"""
                    SELECT 
                        DATE_TRUNC('{time_trunc}', pt.created_at) as time_period,
                        pt.currency,
                        SUM(pt.captured_amount) as revenue,
                        SUM(pt.fee_amount) as fees,
                        COUNT(*) as transactions,
                        COUNT(*) FILTER (WHERE pt.status = 'success') as successful_transactions,
                        AVG(pt.captured_amount) FILTER (WHERE pt.status = 'success') as avg_transaction_value
                    FROM payment_transactions pt
                    WHERE pt.created_at >= :start_date
                    AND pt.created_at <= :end_date
                    {tenant_filter}
                    {currency_filter}
                    GROUP BY DATE_TRUNC('{time_trunc}', pt.created_at), pt.currency
                    ORDER BY time_period, pt.currency
                """)
                
                params = {
                    "start_date": start_date,
                    "end_date": end_date
                }
                if tenant_id:
                    params["tenant_id"] = str(tenant_id)
                if currency != Currency.ALL:
                    params["currency"] = currency.value
                
                result = await db.execute(trends_query, params)
                
                trends_data = []
                for row in result:
                    success_rate = (row.successful_transactions / max(row.transactions, 1)) * 100
                    
                    trend_point = {
                        "time_period": row.time_period.isoformat() if row.time_period else None,
                        "currency": row.currency,
                        "revenue": float(row.revenue or 0),
                        "fees": float(row.fees or 0),
                        "net_revenue": float((row.revenue or 0) - (row.fees or 0)),
                        "transactions": row.transactions,
                        "successful_transactions": row.successful_transactions,
                        "success_rate": round(success_rate, 2),
                        "avg_transaction_value": float(row.avg_transaction_value or 0)
                    }
                    trends_data.append(trend_point)
                
                # Calculate trend analysis
                trend_analysis = self._analyze_trends(trends_data)
                
                return {
                    "time_grouping": time_trunc,
                    "trends_data": trends_data,
                    "trend_analysis": trend_analysis
                }
                
        except Exception as e:
            self.logger.error(f"Revenue trends analysis failed: {e}")
            raise
    
    async def _get_subscription_metrics(
        self,
        tenant_id: UUID,
        start_date: date,
        end_date: date,
        currency: Currency
    ) -> Dict:
        """Get subscription-specific revenue metrics"""
        
        try:
            async with get_db() as db:
                # Build filters
                currency_filter = "AND s.currency = :currency" if currency != Currency.ALL else ""
                tenant_filter = "AND s.tenant_id = :tenant_id" if tenant_id else ""
                
                # Get current active subscriptions
                active_subscriptions_query = text(f"""
                    SELECT 
                        s.currency,
                        COUNT(*) as active_subscriptions,
                        SUM(s.plan_amount) as total_mrr,
                        SUM(s.usage_amount) as total_usage_revenue,
                        AVG(s.total_amount) as avg_revenue_per_user,
                        SUM(s.ai_operations_used) as total_ai_operations
                    FROM enhanced_subscriptions s
                    WHERE s.status = 'active'
                    AND s.current_period_end >= :end_date
                    {tenant_filter}
                    {currency_filter}
                    GROUP BY s.currency
                """)
                
                # Get subscription changes in period
                subscription_changes_query = text(f"""
                    SELECT 
                        'new' as change_type,
                        s.currency,
                        COUNT(*) as count,
                        SUM(s.plan_amount) as revenue_impact
                    FROM enhanced_subscriptions s
                    WHERE s.activated_at >= :start_date
                    AND s.activated_at <= :end_date
                    {tenant_filter}
                    {currency_filter}
                    GROUP BY s.currency
                    
                    UNION ALL
                    
                    SELECT 
                        'cancelled' as change_type,
                        s.currency,
                        COUNT(*) as count,
                        SUM(s.plan_amount) as revenue_impact
                    FROM enhanced_subscriptions s
                    WHERE s.cancelled_at >= :start_date
                    AND s.cancelled_at <= :end_date
                    {tenant_filter}
                    {currency_filter}
                    GROUP BY s.currency
                """)
                
                params = {
                    "start_date": start_date,
                    "end_date": end_date
                }
                if tenant_id:
                    params["tenant_id"] = str(tenant_id)
                if currency != Currency.ALL:
                    params["currency"] = currency.value
                
                # Execute queries
                active_result = await db.execute(active_subscriptions_query, params)
                changes_result = await db.execute(subscription_changes_query, params)
                
                # Process active subscriptions
                active_metrics = []
                total_mrr = Decimal('0.00')
                total_arr = Decimal('0.00')
                
                for row in active_result:
                    mrr = Decimal(str(row.total_mrr or 0))
                    arr = mrr * 12
                    
                    metrics = {
                        "currency": row.currency,
                        "active_subscriptions": row.active_subscriptions,
                        "mrr": float(mrr),
                        "arr": float(arr),
                        "usage_revenue": float(row.total_usage_revenue or 0),
                        "arpu": float(row.avg_revenue_per_user or 0),  # Average Revenue Per User
                        "total_ai_operations": row.total_ai_operations or 0
                    }
                    active_metrics.append(metrics)
                    
                    if row.currency == 'INR':
                        total_mrr += mrr
                        total_arr += arr
                    elif row.currency == 'USD':
                        total_mrr += mrr * Decimal('83.25')  # Convert to INR
                        total_arr += arr * Decimal('83.25')
                
                # Process subscription changes
                changes_data = {
                    "new_subscriptions": {},
                    "cancelled_subscriptions": {},
                    "net_change": {}
                }
                
                for row in changes_result:
                    change_data = {
                        "count": row.count,
                        "revenue_impact": float(row.revenue_impact or 0)
                    }
                    
                    if row.change_type == 'new':
                        changes_data["new_subscriptions"][row.currency] = change_data
                    else:
                        changes_data["cancelled_subscriptions"][row.currency] = change_data
                
                # Calculate churn rate and growth metrics
                churn_metrics = await self._calculate_churn_metrics(tenant_id, start_date, end_date)
                
                return {
                    "active_metrics": active_metrics,
                    "subscription_changes": changes_data,
                    "churn_metrics": churn_metrics,
                    "totals": {
                        "total_mrr_inr": float(total_mrr),
                        "total_arr_inr": float(total_arr)
                    }
                }
                
        except Exception as e:
            self.logger.error(f"Subscription metrics calculation failed: {e}")
            raise
    
    async def _get_tax_compliance_summary(
        self,
        tenant_id: UUID,
        start_date: date,
        end_date: date
    ) -> Dict:
        """Get Indian GST and tax compliance summary"""
        
        try:
            async with get_db() as db:
                tenant_filter = "AND pt.tenant_id = :tenant_id" if tenant_id else ""
                
                # GST summary query
                gst_query = text(f"""
                    SELECT 
                        SUM(pt.cgst_amount) as total_cgst,
                        SUM(pt.sgst_amount) as total_sgst,
                        SUM(pt.igst_amount) as total_igst,
                        SUM(pt.cess_amount) as total_cess,
                        SUM(pt.total_tax_amount) as total_gst,
                        SUM(pt.base_amount) as total_taxable_value,
                        COUNT(*) FILTER (WHERE pt.currency = 'INR') as inr_transactions,
                        COUNT(DISTINCT pt.customer_state) as states_served,
                        COUNT(*) FILTER (WHERE pt.igst_amount > 0) as inter_state_transactions,
                        COUNT(*) FILTER (WHERE pt.cgst_amount > 0 OR pt.sgst_amount > 0) as intra_state_transactions
                    FROM payment_transactions pt
                    WHERE pt.created_at >= :start_date
                    AND pt.created_at <= :end_date
                    AND pt.currency = 'INR'
                    {tenant_filter}
                """)
                
                # Invoice generation summary
                invoice_query = text(f"""
                    SELECT 
                        COUNT(*) as total_invoices,
                        COUNT(*) FILTER (WHERE status = 'generated') as generated_invoices,
                        COUNT(*) FILTER (WHERE status = 'sent') as sent_invoices,
                        COUNT(*) FILTER (WHERE status = 'paid') as paid_invoices,
                        SUM(total_amount) as total_invoice_value,
                        AVG(total_amount) as avg_invoice_value
                    FROM invoices
                    WHERE invoice_date >= :start_date
                    AND invoice_date <= :end_date
                    {tenant_filter.replace('pt.', '')}
                """)
                
                params = {
                    "start_date": start_date,
                    "end_date": end_date
                }
                if tenant_id:
                    params["tenant_id"] = str(tenant_id)
                
                gst_result = await db.execute(gst_query, params)
                invoice_result = await db.execute(invoice_query, params)
                
                gst_row = gst_result.first()
                invoice_row = invoice_result.first()
                
                # Calculate effective tax rate
                total_taxable = float(gst_row.total_taxable_value or 0)
                total_tax = float(gst_row.total_gst or 0)
                effective_rate = (total_tax / total_taxable * 100) if total_taxable > 0 else 0
                
                return {
                    "gst_summary": {
                        "total_cgst": float(gst_row.total_cgst or 0),
                        "total_sgst": float(gst_row.total_sgst or 0),
                        "total_igst": float(gst_row.total_igst or 0),
                        "total_cess": float(gst_row.total_cess or 0),
                        "total_gst_collected": total_tax,
                        "total_taxable_value": total_taxable,
                        "effective_tax_rate": round(effective_rate, 2),
                        "inr_transactions": gst_row.inr_transactions or 0,
                        "states_served": gst_row.states_served or 0,
                        "inter_state_ratio": round(
                            (gst_row.inter_state_transactions or 0) / max(gst_row.inr_transactions or 1, 1) * 100, 2
                        )
                    },
                    "invoice_summary": {
                        "total_invoices": invoice_row.total_invoices or 0,
                        "generated_invoices": invoice_row.generated_invoices or 0,
                        "sent_invoices": invoice_row.sent_invoices or 0,
                        "paid_invoices": invoice_row.paid_invoices or 0,
                        "total_invoice_value": float(invoice_row.total_invoice_value or 0),
                        "avg_invoice_value": float(invoice_row.avg_invoice_value or 0),
                        "invoice_completion_rate": round(
                            (invoice_row.paid_invoices or 0) / max(invoice_row.total_invoices or 1, 1) * 100, 2
                        )
                    }
                }
                
        except Exception as e:
            self.logger.error(f"Tax compliance summary failed: {e}")
            raise
    
    async def _get_top_performing_services(
        self,
        tenant_id: UUID,
        start_date: date,
        end_date: date,
        currency: Currency
    ) -> List[Dict]:
        """Get top performing services by revenue"""
        
        try:
            async with get_db() as db:
                currency_filter = "AND pt.currency = :currency" if currency != Currency.ALL else ""
                tenant_filter = "AND pt.tenant_id = :tenant_id" if tenant_id else ""
                
                services_query = text(f"""
                    SELECT 
                        pt.transaction_type,
                        pt.currency,
                        COUNT(*) as transaction_count,
                        SUM(pt.captured_amount) as total_revenue,
                        AVG(pt.captured_amount) as avg_revenue_per_transaction,
                        SUM(pt.fee_amount) as total_fees,
                        COUNT(*) FILTER (WHERE pt.status = 'success') as successful_transactions
                    FROM payment_transactions pt
                    WHERE pt.created_at >= :start_date
                    AND pt.created_at <= :end_date
                    AND pt.status = 'success'
                    {tenant_filter}
                    {currency_filter}
                    GROUP BY pt.transaction_type, pt.currency
                    ORDER BY total_revenue DESC
                    LIMIT 10
                """)
                
                params = {
                    "start_date": start_date,
                    "end_date": end_date
                }
                if tenant_id:
                    params["tenant_id"] = str(tenant_id)
                if currency != Currency.ALL:
                    params["currency"] = currency.value
                
                result = await db.execute(services_query, params)
                
                top_services = []
                for row in result:
                    service_data = {
                        "service_type": row.transaction_type,
                        "currency": row.currency,
                        "transaction_count": row.transaction_count,
                        "total_revenue": float(row.total_revenue or 0),
                        "avg_revenue_per_transaction": float(row.avg_revenue_per_transaction or 0),
                        "total_fees": float(row.total_fees or 0),
                        "fee_percentage": round(
                            (float(row.total_fees or 0) / float(row.total_revenue or 1)) * 100, 2
                        ),
                        "success_rate": round(
                            (row.successful_transactions / max(row.transaction_count, 1)) * 100, 2
                        )
                    }
                    top_services.append(service_data)
                
                return top_services
                
        except Exception as e:
            self.logger.error(f"Top services analysis failed: {e}")
            raise
    
    async def _get_geographic_breakdown(
        self,
        tenant_id: UUID,
        start_date: date,
        end_date: date,
        currency: Currency
    ) -> Dict:
        """Get revenue breakdown by geography"""
        
        try:
            async with get_db() as db:
                currency_filter = "AND pt.currency = :currency" if currency != Currency.ALL else ""
                tenant_filter = "AND pt.tenant_id = :tenant_id" if tenant_id else ""
                
                geo_query = text(f"""
                    SELECT 
                        COALESCE(pt.customer_country, 'Unknown') as country,
                        COALESCE(pt.customer_state, 'Unknown') as state,
                        pt.currency,
                        COUNT(*) as transaction_count,
                        SUM(pt.captured_amount) as total_revenue,
                        AVG(pt.captured_amount) as avg_transaction_value,
                        COUNT(*) FILTER (WHERE pt.status = 'success') as successful_transactions
                    FROM payment_transactions pt
                    WHERE pt.created_at >= :start_date
                    AND pt.created_at <= :end_date
                    {tenant_filter}
                    {currency_filter}
                    GROUP BY pt.customer_country, pt.customer_state, pt.currency
                    ORDER BY total_revenue DESC
                """)
                
                params = {
                    "start_date": start_date,
                    "end_date": end_date
                }
                if tenant_id:
                    params["tenant_id"] = str(tenant_id)
                if currency != Currency.ALL:
                    params["currency"] = currency.value
                
                result = await db.execute(geo_query, params)
                
                countries = {}
                states = {}
                
                for row in result:
                    success_rate = (row.successful_transactions / max(row.transaction_count, 1)) * 100
                    
                    geo_data = {
                        "transaction_count": row.transaction_count,
                        "total_revenue": float(row.total_revenue or 0),
                        "avg_transaction_value": float(row.avg_transaction_value or 0),
                        "success_rate": round(success_rate, 2),
                        "currency": row.currency
                    }
                    
                    # Group by country
                    if row.country not in countries:
                        countries[row.country] = {
                            "total_revenue": 0,
                            "transaction_count": 0,
                            "states": []
                        }
                    
                    countries[row.country]["total_revenue"] += geo_data["total_revenue"]
                    countries[row.country]["transaction_count"] += geo_data["transaction_count"]
                    
                    # Track states for India
                    if row.country == 'IN' and row.state != 'Unknown':
                        state_key = f"{row.country}_{row.state}"
                        states[state_key] = {
                            "state": row.state,
                            "country": row.country,
                            **geo_data
                        }
                
                return {
                    "by_country": countries,
                    "by_state": states,
                    "top_countries": sorted(
                        [{"country": k, **v} for k, v in countries.items()],
                        key=lambda x: x["total_revenue"],
                        reverse=True
                    )[:10],
                    "top_indian_states": sorted(
                        [v for v in states.values() if v["country"] == 'IN'],
                        key=lambda x: x["total_revenue"],
                        reverse=True
                    )[:10]
                }
                
        except Exception as e:
            self.logger.error(f"Geographic breakdown failed: {e}")
            raise
    
    async def _get_payment_method_analysis(
        self,
        tenant_id: UUID,
        start_date: date,
        end_date: date,
        currency: Currency
    ) -> Dict:
        """Get payment method performance analysis"""
        
        try:
            async with get_db() as db:
                currency_filter = "AND pt.currency = :currency" if currency != Currency.ALL else ""
                tenant_filter = "AND pt.tenant_id = :tenant_id" if tenant_id else ""
                
                method_query = text(f"""
                    SELECT 
                        COALESCE(pt.payment_method, 'unknown') as payment_method,
                        pt.gateway,
                        pt.currency,
                        COUNT(*) as transaction_count,
                        SUM(pt.captured_amount) as total_revenue,
                        AVG(pt.captured_amount) as avg_transaction_value,
                        COUNT(*) FILTER (WHERE pt.status = 'success') as successful_transactions,
                        COUNT(*) FILTER (WHERE pt.status = 'failed') as failed_transactions,
                        AVG(pt.fee_amount) as avg_fee_amount
                    FROM payment_transactions pt
                    WHERE pt.created_at >= :start_date
                    AND pt.created_at <= :end_date
                    {tenant_filter}
                    {currency_filter}
                    GROUP BY pt.payment_method, pt.gateway, pt.currency
                    ORDER BY total_revenue DESC
                """)
                
                params = {
                    "start_date": start_date,
                    "end_date": end_date
                }
                if tenant_id:
                    params["tenant_id"] = str(tenant_id)
                if currency != Currency.ALL:
                    params["currency"] = currency.value
                
                result = await db.execute(method_query, params)
                
                payment_methods = []
                for row in result:
                    success_rate = (row.successful_transactions / max(row.transaction_count, 1)) * 100
                    
                    method_data = {
                        "payment_method": row.payment_method,
                        "gateway": row.gateway,
                        "currency": row.currency,
                        "transaction_count": row.transaction_count,
                        "total_revenue": float(row.total_revenue or 0),
                        "avg_transaction_value": float(row.avg_transaction_value or 0),
                        "successful_transactions": row.successful_transactions,
                        "failed_transactions": row.failed_transactions,
                        "success_rate": round(success_rate, 2),
                        "avg_fee_amount": float(row.avg_fee_amount or 0)
                    }
                    payment_methods.append(method_data)
                
                # Group by payment method for summary
                method_summary = {}
                for method in payment_methods:
                    key = method["payment_method"]
                    if key not in method_summary:
                        method_summary[key] = {
                            "payment_method": key,
                            "total_revenue": 0,
                            "transaction_count": 0,
                            "gateways": []
                        }
                    
                    method_summary[key]["total_revenue"] += method["total_revenue"]
                    method_summary[key]["transaction_count"] += method["transaction_count"]
                    method_summary[key]["gateways"].append({
                        "gateway": method["gateway"],
                        "revenue": method["total_revenue"],
                        "success_rate": method["success_rate"]
                    })
                
                return {
                    "detailed_breakdown": payment_methods,
                    "method_summary": list(method_summary.values()),
                    "top_methods": sorted(
                        list(method_summary.values()),
                        key=lambda x: x["total_revenue"],
                        reverse=True
                    )[:5]
                }
                
        except Exception as e:
            self.logger.error(f"Payment method analysis failed: {e}")
            raise
    
    def _calculate_date_range(
        self,
        time_period: TimePeriod,
        custom_start_date: date = None,
        custom_end_date: date = None
    ) -> Tuple[date, date]:
        """Calculate start and end dates for the given time period"""
        
        today = date.today()
        
        if time_period == TimePeriod.CUSTOM:
            if not custom_start_date or not custom_end_date:
                raise ValueError("Custom dates required for CUSTOM time period")
            return custom_start_date, custom_end_date
        
        elif time_period == TimePeriod.TODAY:
            return today, today
        
        elif time_period == TimePeriod.YESTERDAY:
            yesterday = today - timedelta(days=1)
            return yesterday, yesterday
        
        elif time_period == TimePeriod.LAST_7_DAYS:
            return today - timedelta(days=7), today
        
        elif time_period == TimePeriod.LAST_30_DAYS:
            return today - timedelta(days=30), today
        
        elif time_period == TimePeriod.THIS_MONTH:
            return today.replace(day=1), today
        
        elif time_period == TimePeriod.LAST_MONTH:
            first_day_this_month = today.replace(day=1)
            last_month_end = first_day_this_month - timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)
            return last_month_start, last_month_end
        
        elif time_period == TimePeriod.THIS_QUARTER:
            quarter_start_month = ((today.month - 1) // 3) * 3 + 1
            return today.replace(month=quarter_start_month, day=1), today
        
        elif time_period == TimePeriod.THIS_YEAR:
            return today.replace(month=1, day=1), today
        
        elif time_period == TimePeriod.LAST_YEAR:
            last_year = today.year - 1
            return date(last_year, 1, 1), date(last_year, 12, 31)
        
        else:
            # Default to last 30 days
            return today - timedelta(days=30), today
    
    def _analyze_trends(self, trends_data: List[Dict]) -> Dict:
        """Analyze trends in the data and provide insights"""
        
        if len(trends_data) < 2:
            return {
                "trend_direction": "insufficient_data",
                "growth_rate": 0.0,
                "insights": []
            }
        
        # Calculate overall growth
        total_revenue = [point["revenue"] for point in trends_data]
        if len(total_revenue) >= 2:
            recent_avg = sum(total_revenue[-3:]) / min(3, len(total_revenue))
            earlier_avg = sum(total_revenue[:3]) / min(3, len(total_revenue))
            
            if earlier_avg > 0:
                growth_rate = ((recent_avg - earlier_avg) / earlier_avg) * 100
            else:
                growth_rate = 100.0 if recent_avg > 0 else 0.0
        else:
            growth_rate = 0.0
        
        # Determine trend direction
        if growth_rate > 10:
            trend_direction = "strong_growth"
        elif growth_rate > 0:
            trend_direction = "moderate_growth"
        elif growth_rate > -10:
            trend_direction = "stable"
        else:
            trend_direction = "declining"
        
        # Generate insights
        insights = []
        
        if trend_direction == "strong_growth":
            insights.append("Revenue is showing strong positive growth")
        elif trend_direction == "declining":
            insights.append("Revenue trend is declining, requires attention")
        
        # Check for volatility
        revenue_values = [point["revenue"] for point in trends_data]
        if len(revenue_values) > 3:
            avg_revenue = sum(revenue_values) / len(revenue_values)
            volatility = sum(abs(r - avg_revenue) for r in revenue_values) / len(revenue_values)
            if volatility > avg_revenue * 0.3:
                insights.append("Revenue shows high volatility")
        
        return {
            "trend_direction": trend_direction,
            "growth_rate": round(growth_rate, 2),
            "insights": insights
        }
    
    async def _calculate_churn_metrics(
        self,
        tenant_id: UUID,
        start_date: date,
        end_date: date
    ) -> Dict:
        """Calculate subscription churn metrics"""
        
        try:
            async with get_db() as db:
                tenant_filter = "AND tenant_id = :tenant_id" if tenant_id else ""
                
                # Get churn data
                churn_query = text(f"""
                    WITH period_start_subscriptions AS (
                        SELECT COUNT(*) as start_count
                        FROM enhanced_subscriptions
                        WHERE status = 'active'
                        AND current_period_start <= :start_date
                        {tenant_filter}
                    ),
                    churned_subscriptions AS (
                        SELECT COUNT(*) as churned_count
                        FROM enhanced_subscriptions
                        WHERE cancelled_at >= :start_date
                        AND cancelled_at <= :end_date
                        {tenant_filter}
                    ),
                    new_subscriptions AS (
                        SELECT COUNT(*) as new_count
                        FROM enhanced_subscriptions
                        WHERE activated_at >= :start_date
                        AND activated_at <= :end_date
                        {tenant_filter}
                    )
                    SELECT 
                        pss.start_count,
                        cs.churned_count,
                        ns.new_count
                    FROM period_start_subscriptions pss,
                         churned_subscriptions cs,
                         new_subscriptions ns
                """)
                
                params = {
                    "start_date": start_date,
                    "end_date": end_date
                }
                if tenant_id:
                    params["tenant_id"] = str(tenant_id)
                
                result = await db.execute(churn_query, params)
                row = result.first()
                
                if row and row.start_count > 0:
                    churn_rate = (row.churned_count / row.start_count) * 100
                    growth_rate = ((row.new_count - row.churned_count) / row.start_count) * 100
                else:
                    churn_rate = 0.0
                    growth_rate = 0.0
                
                return {
                    "churn_rate": round(churn_rate, 2),
                    "growth_rate": round(growth_rate, 2),
                    "churned_subscriptions": row.churned_count if row else 0,
                    "new_subscriptions": row.new_count if row else 0,
                    "net_change": (row.new_count - row.churned_count) if row else 0
                }
                
        except Exception as e:
            self.logger.error(f"Churn metrics calculation failed: {e}")
            return {
                "churn_rate": 0.0,
                "growth_rate": 0.0,
                "churned_subscriptions": 0,
                "new_subscriptions": 0,
                "net_change": 0
            }
    
    async def generate_revenue_report(
        self,
        tenant_id: UUID,
        report_type: str = "comprehensive",
        time_period: TimePeriod = TimePeriod.LAST_30_DAYS,
        format: str = "json"
    ) -> Dict:
        """Generate comprehensive revenue report"""
        
        try:
            # Get dashboard data
            dashboard_data = await self.get_revenue_dashboard(
                tenant_id=tenant_id,
                time_period=time_period
            )
            
            if not dashboard_data.get("success"):
                return dashboard_data
            
            # Enhanced report with additional insights
            report = {
                "report_id": str(UUID()),
                "report_type": report_type,
                "generated_at": datetime.now().isoformat(),
                "tenant_id": str(tenant_id) if tenant_id else "all_tenants",
                "period": dashboard_data["period"],
                
                # Executive Summary
                "executive_summary": self._generate_executive_summary(dashboard_data),
                
                # Detailed Data
                "detailed_data": dashboard_data,
                
                # Recommendations
                "recommendations": self._generate_recommendations(dashboard_data),
                
                # Export metadata
                "export_metadata": {
                    "format": format,
                    "total_data_points": self._count_data_points(dashboard_data),
                    "currencies_included": self._get_currencies_in_data(dashboard_data)
                }
            }
            
            return {
                "success": True,
                "report": report
            }
            
        except Exception as e:
            await self.error_handler.handle_error(e, {
                "component": "revenue_analytics",
                "action": "generate_revenue_report",
                "tenant_id": str(tenant_id) if tenant_id else None
            })
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_executive_summary(self, dashboard_data: Dict) -> Dict:
        """Generate executive summary from dashboard data"""
        
        revenue_summary = dashboard_data.get("revenue_summary", {}).get("overview", {})
        gateway_performance = dashboard_data.get("gateway_performance", {}).get("gateway_performance", [])
        
        # Key metrics
        total_revenue = revenue_summary.get("total_gross_revenue_inr", 0)
        total_transactions = revenue_summary.get("total_transactions", 0)
        
        # Best performing gateway
        best_gateway = None
        if gateway_performance:
            best_gateway = max(gateway_performance, key=lambda x: x.get("success_rate", 0))
        
        return {
            "key_metrics": {
                "total_revenue_inr": total_revenue,
                "total_transactions": total_transactions,
                "avg_transaction_value": total_revenue / max(total_transactions, 1)
            },
            "highlights": [
                f"Generated ₹{total_revenue:,.2f} in total revenue",
                f"Processed {total_transactions:,} transactions",
                f"Best performing gateway: {best_gateway['gateway']} ({best_gateway['success_rate']}% success rate)" if best_gateway else "No gateway data available"
            ],
            "performance_indicators": {
                "revenue_status": "strong" if total_revenue > 100000 else "moderate" if total_revenue > 10000 else "low",
                "transaction_volume": "high" if total_transactions > 1000 else "moderate" if total_transactions > 100 else "low"
            }
        }
    
    def _generate_recommendations(self, dashboard_data: Dict) -> List[Dict]:
        """Generate recommendations based on analytics data"""
        
        recommendations = []
        
        gateway_performance = dashboard_data.get("gateway_performance", {}).get("gateway_performance", [])
        revenue_summary = dashboard_data.get("revenue_summary", {}).get("overview", {})
        
        # Gateway optimization recommendations
        if gateway_performance:
            success_rates = [gw.get("success_rate", 0) for gw in gateway_performance]
            avg_success_rate = sum(success_rates) / len(success_rates)
            
            if avg_success_rate < 90:
                recommendations.append({
                    "type": "gateway_optimization",
                    "priority": "high",
                    "title": "Improve Payment Success Rate",
                    "description": f"Average success rate is {avg_success_rate:.1f}%. Consider optimizing gateway configurations.",
                    "action_items": [
                        "Review failing transactions",
                        "Optimize gateway routing rules",
                        "Consider alternative payment methods"
                    ]
                })
        
        # Fee optimization
        fee_percentage = revenue_summary.get("average_fee_percentage", 0)
        if fee_percentage > 3:
            recommendations.append({
                "type": "cost_optimization",
                "priority": "medium",
                "title": "Optimize Gateway Fees",
                "description": f"Current average fee rate is {fee_percentage:.2f}%. Consider negotiating better rates or switching gateways for certain transaction types.",
                "action_items": [
                    "Negotiate volume-based pricing",
                    "Optimize payment method routing",
                    "Consider direct bank integrations for high-value transactions"
                ]
            })
        
        return recommendations
    
    def _count_data_points(self, dashboard_data: Dict) -> int:
        """Count total data points in the dashboard"""
        
        count = 0
        if "revenue_trends" in dashboard_data:
            count += len(dashboard_data["revenue_trends"].get("trends_data", []))
        if "gateway_performance" in dashboard_data:
            count += len(dashboard_data["gateway_performance"].get("gateway_performance", []))
        
        return count
    
    def _get_currencies_in_data(self, dashboard_data: Dict) -> List[str]:
        """Get list of currencies in the dashboard data"""
        
        currencies = set()
        if "revenue_summary" in dashboard_data:
            for currency_data in dashboard_data["revenue_summary"].get("by_currency", []):
                currencies.add(currency_data.get("currency", ""))
        
        return list(currencies)


# Global instance
revenue_analytics = RevenueAnalyticsService()
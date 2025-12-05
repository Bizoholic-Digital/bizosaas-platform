"""
CoreLDove Hybrid Pricing Engine Service
===========================================
FastAPI service integrating HybridPricingEngine for outcome-based billing
Supporting the evolution from seat-based (15%) to hybrid models (41%) by 2026
"""

import logging
import asyncio
import json
from datetime import datetime, timedelta, date
from decimal import Decimal
from typing import Dict, List, Optional, Any, Union
from uuid import UUID, uuid4

from fastapi import HTTPException, Depends
from pydantic import BaseModel, Field, validator
from sqlalchemy import text, select, func
from cryptography.fernet import Fernet
import stripe
import os

from pricing_engine.outcome_pricing import (
    HybridPricingEngine, 
    OutcomeMeasurementSystem,
    PricingTier,
    OutcomeMetric,
    UsageMetric,
    CoreLDovePricingPlans
)
from database import get_db
from auth import current_active_user, require_admin
from models.auth_models import User

logger = logging.getLogger(__name__)

# =============================================================================
# PYDANTIC MODELS FOR API
# =============================================================================

class BusinessProfile(BaseModel):
    """Business profile for plan recommendations"""
    annual_revenue: Optional[int] = Field(None, description="Annual revenue in USD")
    employee_count: Optional[int] = Field(None, description="Number of employees")
    ai_maturity: str = Field("beginner", description="AI maturity: beginner, intermediate, advanced")
    expected_monthly_usage: Dict[str, int] = Field(default_factory=dict, description="Expected usage patterns")
    industry_vertical: Optional[str] = Field(None, description="Industry vertical")
    automation_goals: List[str] = Field(default_factory=list, description="Primary automation objectives")

class UsageDataRequest(BaseModel):
    """Usage data for billing calculations"""
    api_calls: int = Field(0, description="Number of API calls made")
    ai_analyses: int = Field(0, description="Number of AI analyses performed")
    automated_tasks: int = Field(0, description="Number of automated tasks executed")
    data_processed: int = Field(0, description="Amount of data processed (MB)")
    users_served: int = Field(0, description="Number of users served")
    transactions_processed: int = Field(0, description="Number of transactions processed")

class OutcomeDataRequest(BaseModel):
    """Outcome data for billing calculations"""
    revenue_increase: Optional[Decimal] = Field(None, description="Revenue increase in USD")
    conversion_improvement: Optional[Decimal] = Field(None, description="Conversion rate improvement value")
    cost_reduction: Optional[Decimal] = Field(None, description="Cost reduction achieved")
    time_savings: Optional[Decimal] = Field(None, description="Time savings value")
    customer_acquisition: Optional[Decimal] = Field(None, description="Customer acquisition value")
    retention_improvement: Optional[Decimal] = Field(None, description="Retention improvement value")
    operational_efficiency: Optional[Decimal] = Field(None, description="Operational efficiency gains")
    profit_margin_improvement: Optional[Decimal] = Field(None, description="Profit margin improvement")

    @validator('*', pre=True)
    def convert_to_decimal(cls, v):
        if v is not None:
            return Decimal(str(v)) if not isinstance(v, Decimal) else v
        return v

class BillingCalculationRequest(BaseModel):
    """Request for billing calculation"""
    plan_tier: PricingTier = Field(..., description="Pricing tier")
    usage_data: UsageDataRequest = Field(..., description="Usage metrics")
    outcome_data: OutcomeDataRequest = Field(..., description="Outcome metrics")
    billing_period: Optional[datetime] = Field(None, description="Billing period (defaults to current month)")

class BaselineSetupRequest(BaseModel):
    """Request for baseline measurement setup"""
    plan_tier: PricingTier = Field(..., description="Selected pricing tier")
    initial_metrics: Dict[str, Decimal] = Field(default_factory=dict, description="Initial baseline values")
    measurement_goals: List[str] = Field(default_factory=list, description="Primary measurement objectives")

class PlanUpgradeRequest(BaseModel):
    """Request for plan upgrade/downgrade"""
    new_tier: PricingTier = Field(..., description="New pricing tier")
    effective_date: Optional[datetime] = Field(None, description="Effective date for change")
    reason: str = Field(..., description="Reason for plan change")

# =============================================================================
# PRICING ENGINE SERVICE CLASS
# =============================================================================

class PricingEngineService:
    """
    FastAPI service for hybrid pricing engine integration
    """
    
    def __init__(self):
        self.pricing_engine = HybridPricingEngine()
        self.measurement_system = OutcomeMeasurementSystem(self.pricing_engine)
        self.encryption_key = self._get_encryption_key()
        self.stripe_client = self._init_stripe()
        
        # Initialize pricing tiers cache
        self._plans_cache = None
        self._cache_timestamp = None
        self._cache_duration = timedelta(hours=1)

    def _get_encryption_key(self) -> Fernet:
        """Initialize encryption for sensitive billing data"""
        key = os.getenv('BILLING_ENCRYPTION_KEY')
        if not key:
            # Generate new key in production - store securely
            key = Fernet.generate_key()
            logger.warning("Generated new encryption key - ensure secure storage in production")
        return Fernet(key.encode() if isinstance(key, str) else key)

    def _init_stripe(self):
        """Initialize Stripe client"""
        stripe_key = os.getenv('STRIPE_SECRET_KEY')
        if stripe_key:
            stripe.api_key = stripe_key
            return stripe
        logger.warning("Stripe not configured - payment processing disabled")
        return None

    async def get_available_plans(self) -> List[Dict[str, Any]]:
        """
        Get all available pricing plans with comprehensive details
        """
        try:
            # Check cache first
            if (self._plans_cache and self._cache_timestamp and 
                datetime.utcnow() - self._cache_timestamp < self._cache_duration):
                return self._plans_cache

            plans = self.pricing_engine.get_available_plans()
            
            # Enhance with market positioning and ROI estimates
            enhanced_plans = []
            for plan in plans:
                enhanced_plan = {
                    **plan,
                    "market_positioning": self._get_market_positioning(plan['tier']),
                    "roi_estimate": await self._calculate_roi_estimate(plan),
                    "typical_outcomes": await self._get_typical_outcomes(plan['tier']),
                    "implementation_timeline": self._get_implementation_timeline(plan['tier'])
                }
                enhanced_plans.append(enhanced_plan)

            # Update cache
            self._plans_cache = enhanced_plans
            self._cache_timestamp = datetime.utcnow()
            
            return enhanced_plans

        except Exception as e:
            logger.error(f"Error fetching available plans: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch plans: {str(e)}")

    def _get_market_positioning(self, tier: str) -> Dict[str, Any]:
        """Get market positioning for each tier"""
        positioning = {
            "starter": {
                "target_market": "Small businesses (1-10 employees)",
                "revenue_range": "$0-$500K annually",
                "ai_maturity": "Experimentation phase",
                "competitive_advantage": "Low-risk AI adoption with proven ROI"
            },
            "professional": {
                "target_market": "Growing businesses (10-50 employees)",
                "revenue_range": "$500K-$2M annually", 
                "ai_maturity": "Active implementation",
                "competitive_advantage": "Comprehensive automation with outcome guarantees"
            },
            "growth": {
                "target_market": "Scaling businesses (50-200 employees)",
                "revenue_range": "$2M-$10M annually",
                "ai_maturity": "Strategic transformation",
                "competitive_advantage": "Full AI ecosystem with custom solutions"
            },
            "enterprise": {
                "target_market": "Large enterprises (200+ employees)",
                "revenue_range": "$10M+ annually",
                "ai_maturity": "AI-first operations",
                "competitive_advantage": "Unlimited scale with dedicated support"
            }
        }
        return positioning.get(tier, {})

    async def _calculate_roi_estimate(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate typical ROI estimates for each plan"""
        base_price = plan['base_price']
        
        roi_multipliers = {
            "starter": {"conservative": 3.0, "typical": 5.0, "optimistic": 8.0},
            "professional": {"conservative": 4.0, "typical": 7.0, "optimistic": 12.0},
            "growth": {"conservative": 5.0, "typical": 10.0, "optimistic": 18.0},
            "enterprise": {"conservative": 6.0, "typical": 15.0, "optimistic": 25.0}
        }
        
        multiplier = roi_multipliers.get(plan['tier'], roi_multipliers['starter'])
        
        return {
            "monthly_investment": base_price,
            "conservative_monthly_return": base_price * multiplier['conservative'],
            "typical_monthly_return": base_price * multiplier['typical'],
            "optimistic_monthly_return": base_price * multiplier['optimistic'],
            "payback_period_months": round(12 / multiplier['typical'], 1),
            "annual_roi_percentage": round((multiplier['typical'] * 12 - 1) * 100, 0)
        }

    async def _get_typical_outcomes(self, tier: str) -> List[Dict[str, Any]]:
        """Get typical business outcomes for each tier"""
        outcomes = {
            "starter": [
                {"outcome": "Lead generation increase", "typical_improvement": "25-50%"},
                {"outcome": "Response time reduction", "typical_improvement": "60-80%"},
                {"outcome": "Cost per lead reduction", "typical_improvement": "30-45%"}
            ],
            "professional": [
                {"outcome": "Revenue increase", "typical_improvement": "15-35%"},
                {"outcome": "Conversion rate improvement", "typical_improvement": "40-70%"},
                {"outcome": "Operational cost reduction", "typical_improvement": "20-40%"},
                {"outcome": "Customer acquisition cost reduction", "typical_improvement": "25-50%"}
            ],
            "growth": [
                {"outcome": "Revenue increase", "typical_improvement": "25-50%"},
                {"outcome": "Profit margin improvement", "typical_improvement": "15-30%"},
                {"outcome": "Operational efficiency gains", "typical_improvement": "40-80%"},
                {"outcome": "Market share growth", "typical_improvement": "10-25%"}
            ],
            "enterprise": [
                {"outcome": "Revenue increase", "typical_improvement": "30-75%"},
                {"outcome": "Comprehensive transformation", "typical_improvement": "50-150%"},
                {"outcome": "Market leadership position", "typical_improvement": "Strategic advantage"},
                {"outcome": "Innovation acceleration", "typical_improvement": "2-5x faster"}
            ]
        }
        return outcomes.get(tier, [])

    def _get_implementation_timeline(self, tier: str) -> Dict[str, str]:
        """Get implementation timeline for each tier"""
        timelines = {
            "starter": {
                "setup": "1-2 weeks",
                "full_deployment": "2-4 weeks",
                "roi_realization": "1-2 months"
            },
            "professional": {
                "setup": "2-3 weeks",
                "full_deployment": "4-6 weeks",
                "roi_realization": "2-3 months"
            },
            "growth": {
                "setup": "3-4 weeks",
                "full_deployment": "6-8 weeks",
                "roi_realization": "2-4 months"
            },
            "enterprise": {
                "setup": "4-6 weeks",
                "full_deployment": "8-12 weeks",
                "roi_realization": "3-6 months"
            }
        }
        return timelines.get(tier, timelines['starter'])

    async def recommend_plan(
        self, 
        business_profile: BusinessProfile,
        user: User
    ) -> Dict[str, Any]:
        """
        Get AI-powered plan recommendation based on business profile
        """
        try:
            # Convert to format expected by pricing engine
            profile_dict = {
                "annual_revenue": business_profile.annual_revenue or 0,
                "employee_count": business_profile.employee_count or 1,
                "ai_maturity": business_profile.ai_maturity,
                "expected_monthly_usage": business_profile.expected_monthly_usage
            }
            
            # Get base recommendation
            recommendation = await self.pricing_engine.recommend_plan(profile_dict)
            
            # Enhance with industry-specific insights
            industry_insights = await self._get_industry_insights(
                business_profile.industry_vertical,
                business_profile.automation_goals
            )
            
            # Add competitive analysis
            competitive_analysis = await self._get_competitive_analysis(
                recommendation['recommended_tier']
            )
            
            # Calculate personalized ROI projection
            roi_projection = await self._calculate_personalized_roi(
                business_profile, recommendation['estimated_monthly_cost']
            )

            enhanced_recommendation = {
                **recommendation,
                "industry_insights": industry_insights,
                "competitive_analysis": competitive_analysis,
                "roi_projection": roi_projection,
                "implementation_support": {
                    "dedicated_onboarding": recommendation['recommended_tier'] in ['growth', 'enterprise'],
                    "training_included": True,
                    "success_manager": recommendation['recommended_tier'] in ['growth', 'enterprise'],
                    "sla_guarantee": recommendation['recommended_tier'] in ['professional', 'growth', 'enterprise']
                },
                "risk_mitigation": {
                    "money_back_guarantee": "30 days",
                    "performance_guarantee": recommendation['recommended_tier'] != 'starter',
                    "migration_assistance": True,
                    "data_security": "SOC 2 Type II compliant"
                }
            }
            
            # Log recommendation for analytics
            await self._log_recommendation(user.tenant_id, business_profile, enhanced_recommendation)
            
            return enhanced_recommendation

        except Exception as e:
            logger.error(f"Error generating plan recommendation: {e}")
            raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")

    async def _get_industry_insights(
        self, 
        industry: Optional[str], 
        goals: List[str]
    ) -> Dict[str, Any]:
        """Get industry-specific insights and recommendations"""
        
        if not industry:
            return {"message": "Provide industry information for customized recommendations"}
            
        # Industry-specific recommendations (would be enhanced with real data)
        industry_data = {
            "ecommerce": {
                "typical_roi": "8-15x",
                "key_automations": ["inventory management", "customer service", "marketing campaigns"],
                "success_stories": "Average 40% increase in conversion rates"
            },
            "healthcare": {
                "typical_roi": "5-12x",
                "key_automations": ["patient scheduling", "billing", "compliance monitoring"],
                "success_stories": "60% reduction in administrative overhead"
            },
            "professional_services": {
                "typical_roi": "6-18x", 
                "key_automations": ["client onboarding", "project management", "reporting"],
                "success_stories": "50% increase in billable hours"
            },
            "manufacturing": {
                "typical_roi": "10-25x",
                "key_automations": ["supply chain", "quality control", "predictive maintenance"],
                "success_stories": "30% reduction in operational costs"
            }
        }
        
        return industry_data.get(industry.lower(), {
            "message": f"Custom solutions available for {industry} industry",
            "recommendation": "Schedule consultation for industry-specific analysis"
        })

    async def _get_competitive_analysis(self, tier: str) -> Dict[str, Any]:
        """Get competitive analysis for the recommended tier"""
        
        competitive_data = {
            "starter": {
                "vs_competitors": [
                    "50% less expensive than enterprise solutions",
                    "3x faster implementation than custom development",
                    "Outcome-based pricing vs fixed costs"
                ],
                "unique_advantages": [
                    "Pay only for results achieved",
                    "No long-term contracts required",
                    "Industry-specific AI agents"
                ]
            },
            "professional": {
                "vs_competitors": [
                    "30% better ROI than traditional automation",
                    "Complete solution vs point solutions",
                    "Transparent outcome tracking"
                ],
                "unique_advantages": [
                    "Hybrid pricing with outcome guarantees",
                    "15 specialized AI agents",
                    "Priority support included"
                ]
            },
            "growth": {
                "vs_competitors": [
                    "Unlimited scalability vs capacity limits",
                    "25+ AI agents vs generic solutions",
                    "Custom development included"
                ],
                "unique_advantages": [
                    "White-label capabilities",
                    "Dedicated success management",
                    "API access for custom integrations"
                ]
            },
            "enterprise": {
                "vs_competitors": [
                    "Complete ecosystem vs fragmented tools",
                    "24/7 dedicated support vs ticket system",
                    "Unlimited customization capabilities"
                ],
                "unique_advantages": [
                    "Custom AI agent development",
                    "Enterprise-grade security & compliance",
                    "Strategic consulting included"
                ]
            }
        }
        
        return competitive_data.get(tier, competitive_data['starter'])

    async def _calculate_personalized_roi(
        self, 
        profile: BusinessProfile, 
        estimated_cost: Dict[str, float]
    ) -> Dict[str, Any]:
        """Calculate personalized ROI based on business profile"""
        
        annual_revenue = profile.annual_revenue or 500000  # Default assumption
        monthly_cost = estimated_cost.get('total_estimated', 500)
        
        # Industry multipliers for ROI calculation
        industry_multipliers = {
            "ecommerce": 1.8,
            "healthcare": 1.5,
            "professional_services": 2.0,
            "manufacturing": 2.2,
            "finance": 1.6,
            "real_estate": 1.7
        }
        
        multiplier = industry_multipliers.get(
            profile.industry_vertical.lower() if profile.industry_vertical else "default", 
            1.5
        )
        
        # Calculate conservative estimates
        monthly_savings = monthly_cost * 3 * multiplier  # Conservative 3x ROI
        annual_savings = monthly_savings * 12
        roi_percentage = ((annual_savings - (monthly_cost * 12)) / (monthly_cost * 12)) * 100
        
        return {
            "estimated_monthly_savings": round(monthly_savings, 2),
            "estimated_annual_savings": round(annual_savings, 2),
            "roi_percentage": round(roi_percentage, 1),
            "payback_period_months": round((monthly_cost * 12) / annual_savings * 12, 1),
            "five_year_value": round(annual_savings * 5, 2),
            "confidence_level": "Conservative estimate based on industry averages"
        }

    async def calculate_monthly_bill(
        self,
        request: BillingCalculationRequest,
        tenant_id: UUID,
        billing_period: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive monthly bill with hybrid pricing
        """
        try:
            if not billing_period:
                billing_period = datetime.utcnow().replace(day=1)

            # Convert usage data to dict
            usage_dict = {
                UsageMetric.API_CALLS.value: request.usage_data.api_calls,
                UsageMetric.AI_ANALYSES.value: request.usage_data.ai_analyses,
                UsageMetric.AUTOMATED_TASKS.value: request.usage_data.automated_tasks,
                UsageMetric.DATA_PROCESSED.value: request.usage_data.data_processed,
                UsageMetric.USERS_SERVED.value: request.usage_data.users_served,
                UsageMetric.TRANSACTIONS_PROCESSED.value: request.usage_data.transactions_processed
            }

            # Convert outcome data to dict (filter out None values)
            outcome_dict = {}
            outcome_mapping = {
                OutcomeMetric.REVENUE_INCREASE.value: request.outcome_data.revenue_increase,
                OutcomeMetric.CONVERSION_IMPROVEMENT.value: request.outcome_data.conversion_improvement,
                OutcomeMetric.COST_REDUCTION.value: request.outcome_data.cost_reduction,
                OutcomeMetric.TIME_SAVINGS.value: request.outcome_data.time_savings,
                OutcomeMetric.CUSTOMER_ACQUISITION.value: request.outcome_data.customer_acquisition,
                OutcomeMetric.RETENTION_IMPROVEMENT.value: request.outcome_data.retention_improvement,
                OutcomeMetric.OPERATIONAL_EFFICIENCY.value: request.outcome_data.operational_efficiency,
                OutcomeMetric.PROFIT_MARGIN_IMPROVEMENT.value: request.outcome_data.profit_margin_improvement
            }
            
            for key, value in outcome_mapping.items():
                if value is not None:
                    outcome_dict[key] = value

            # Calculate bill using pricing engine
            bill = await self.pricing_engine.calculate_monthly_bill(
                tenant_id=tenant_id,
                plan_tier=request.plan_tier,
                usage_data=usage_dict,
                outcome_data=outcome_dict,
                billing_period=billing_period
            )

            # Enhance bill with additional context
            enhanced_bill = {
                **bill,
                "pricing_model": "Hybrid: Base + Usage + Outcome",
                "market_evolution": "Aligned with 2026 outcome-based pricing trends",
                "transparency_note": "You only pay for measurable business value delivered",
                "payment_terms": {
                    "due_date": bill['payment_due_date'],
                    "payment_methods": ["Credit Card", "ACH", "Wire Transfer"],
                    "late_fee": "1.5% per month on overdue amounts",
                    "early_payment_discount": "2% if paid within 10 days"
                },
                "next_bill_preview": await self._generate_next_bill_preview(
                    tenant_id, request.plan_tier, usage_dict, outcome_dict
                )
            }

            # Store encrypted billing record
            await self._store_billing_record(tenant_id, enhanced_bill)
            
            # Create Stripe invoice if configured
            if self.stripe_client:
                stripe_invoice = await self._create_stripe_invoice(tenant_id, enhanced_bill)
                enhanced_bill["stripe_invoice_url"] = stripe_invoice.get("hosted_invoice_url")

            return enhanced_bill

        except Exception as e:
            logger.error(f"Error calculating monthly bill: {e}")
            raise HTTPException(status_code=500, detail=f"Billing calculation failed: {str(e)}")

    async def _generate_next_bill_preview(
        self, 
        tenant_id: UUID, 
        plan_tier: PricingTier, 
        usage_dict: Dict[str, int], 
        outcome_dict: Dict[str, Decimal]
    ) -> Dict[str, Any]:
        """Generate preview of next month's bill based on current trends"""
        
        # Project usage based on current trends (simple linear projection)
        projected_usage = {k: int(v * 1.1) for k, v in usage_dict.items()}  # 10% growth assumption
        projected_outcomes = {k: v * Decimal('1.05') for k, v in outcome_dict.items()}  # 5% improvement
        
        next_month = datetime.utcnow().replace(day=1) + timedelta(days=32)
        next_month = next_month.replace(day=1)
        
        preview_bill = await self.pricing_engine.calculate_monthly_bill(
            tenant_id=tenant_id,
            plan_tier=plan_tier,
            usage_data=projected_usage,
            outcome_data=projected_outcomes,
            billing_period=next_month
        )
        
        return {
            "projected_total": preview_bill["total_amount"],
            "growth_assumptions": {
                "usage_growth": "10%",
                "outcome_improvement": "5%"
            },
            "optimization_opportunities": [
                "Consider usage optimization to reduce overage charges",
                "Focus on high-ROI outcomes to maximize value"
            ]
        }

    async def setup_baseline_measurements(
        self,
        request: BaselineSetupRequest,
        tenant_id: UUID
    ) -> Dict[str, Any]:
        """
        Setup baseline measurements for outcome tracking
        """
        try:
            # Setup measurements using the measurement system
            baseline_setup = await self.measurement_system.setup_baseline_measurements(
                tenant_id=tenant_id,
                plan_tier=request.plan_tier
            )

            # Store initial metrics if provided
            if request.initial_metrics:
                await self._store_initial_metrics(tenant_id, request.initial_metrics)

            # Create measurement tracking schedule
            tracking_schedule = await self._create_tracking_schedule(
                tenant_id, request.plan_tier, request.measurement_goals
            )

            enhanced_setup = {
                **baseline_setup,
                "measurement_schedule": tracking_schedule,
                "integration_requirements": await self._get_integration_requirements(request.plan_tier),
                "success_criteria": await self._define_success_criteria(request.plan_tier),
                "reporting_schedule": {
                    "daily_metrics": "Automated data collection",
                    "weekly_reports": "Performance summaries",
                    "monthly_analysis": "ROI analysis and optimization recommendations",
                    "quarterly_reviews": "Strategic outcome assessment"
                }
            }

            return enhanced_setup

        except Exception as e:
            logger.error(f"Error setting up baseline measurements: {e}")
            raise HTTPException(status_code=500, detail=f"Baseline setup failed: {str(e)}")

    async def _get_integration_requirements(self, plan_tier: PricingTier) -> List[Dict[str, str]]:
        """Get required integrations for outcome tracking"""
        
        integrations = {
            PricingTier.STARTER: [
                {"system": "Google Analytics", "purpose": "Conversion tracking", "required": True},
                {"system": "Payment Processor", "purpose": "Revenue tracking", "required": True},
                {"system": "CRM System", "purpose": "Lead tracking", "required": False}
            ],
            PricingTier.PROFESSIONAL: [
                {"system": "Google Analytics", "purpose": "Advanced conversion tracking", "required": True},
                {"system": "Payment Processor", "purpose": "Revenue tracking", "required": True},
                {"system": "CRM System", "purpose": "Customer lifecycle tracking", "required": True},
                {"system": "Accounting Software", "purpose": "Cost analysis", "required": False},
                {"system": "Marketing Platforms", "purpose": "Campaign performance", "required": True}
            ],
            PricingTier.GROWTH: [
                {"system": "Google Analytics", "purpose": "Comprehensive analytics", "required": True},
                {"system": "Payment Processor", "purpose": "Revenue tracking", "required": True},
                {"system": "CRM System", "purpose": "Customer lifecycle management", "required": True},
                {"system": "Accounting Software", "purpose": "Financial analysis", "required": True},
                {"system": "Marketing Automation", "purpose": "Campaign optimization", "required": True},
                {"system": "ERP System", "purpose": "Operational efficiency", "required": False}
            ],
            PricingTier.ENTERPRISE: [
                {"system": "Custom Analytics", "purpose": "Enterprise-grade tracking", "required": True},
                {"system": "Enterprise Payment Systems", "purpose": "Multi-currency revenue tracking", "required": True},
                {"system": "Enterprise CRM", "purpose": "Advanced customer management", "required": True},
                {"system": "ERP Integration", "purpose": "Comprehensive operational tracking", "required": True},
                {"system": "BI Platforms", "purpose": "Advanced analytics", "required": True},
                {"system": "Custom APIs", "purpose": "Proprietary system integration", "required": False}
            ]
        }
        
        return integrations.get(plan_tier, integrations[PricingTier.STARTER])

    async def _define_success_criteria(self, plan_tier: PricingTier) -> Dict[str, Any]:
        """Define success criteria for each plan tier"""
        
        criteria = {
            PricingTier.STARTER: {
                "minimum_roi": "3x within 3 months",
                "key_metrics": ["Lead generation improvement", "Response time reduction"],
                "success_threshold": "25% improvement in primary metric"
            },
            PricingTier.PROFESSIONAL: {
                "minimum_roi": "5x within 6 months",
                "key_metrics": ["Revenue growth", "Conversion improvement", "Cost reduction"],
                "success_threshold": "40% improvement in combined metrics"
            },
            PricingTier.GROWTH: {
                "minimum_roi": "8x within 6 months",
                "key_metrics": ["Revenue growth", "Profit margins", "Operational efficiency"],
                "success_threshold": "60% improvement in business outcomes"
            },
            PricingTier.ENTERPRISE: {
                "minimum_roi": "12x within 12 months",
                "key_metrics": ["Market position", "Innovation speed", "Competitive advantage"],
                "success_threshold": "Transformational business impact"
            }
        }
        
        return criteria.get(plan_tier, criteria[PricingTier.STARTER])

    async def get_billing_history(
        self, 
        tenant_id: UUID,
        months: int = 12,
        include_predictions: bool = True
    ) -> Dict[str, Any]:
        """
        Get comprehensive billing history and analytics
        """
        try:
            async with get_db() as db:
                # Get historical billing data
                query = text("""
                    SELECT 
                        billing_period,
                        plan_tier,
                        base_charge,
                        usage_charges,
                        outcome_charges,
                        total_amount,
                        created_at
                    FROM billing_records 
                    WHERE tenant_id = :tenant_id 
                        AND billing_period >= :start_date
                    ORDER BY billing_period DESC
                """)
                
                start_date = datetime.utcnow() - timedelta(days=months * 30)
                result = await db.execute(query, {
                    'tenant_id': str(tenant_id),
                    'start_date': start_date
                })
                
                billing_history = []
                total_base = 0
                total_usage = 0
                total_outcome = 0
                total_paid = 0
                
                for row in result:
                    record = {
                        "billing_period": row.billing_period.isoformat(),
                        "plan_tier": row.plan_tier,
                        "base_charge": float(row.base_charge),
                        "usage_charges": float(row.usage_charges),
                        "outcome_charges": float(row.outcome_charges),
                        "total_amount": float(row.total_amount),
                        "created_at": row.created_at.isoformat()
                    }
                    billing_history.append(record)
                    
                    total_base += float(row.base_charge)
                    total_usage += float(row.usage_charges)
                    total_outcome += float(row.outcome_charges)
                    total_paid += float(row.total_amount)

                # Calculate trends and insights
                analytics = {
                    "summary": {
                        "total_periods": len(billing_history),
                        "total_base_charges": round(total_base, 2),
                        "total_usage_charges": round(total_usage, 2),
                        "total_outcome_charges": round(total_outcome, 2),
                        "total_paid": round(total_paid, 2),
                        "average_monthly_bill": round(total_paid / max(len(billing_history), 1), 2)
                    },
                    "trends": await self._calculate_billing_trends(billing_history),
                    "pricing_evolution": await self._analyze_pricing_evolution(billing_history),
                    "outcome_performance": await self._analyze_outcome_performance(billing_history)
                }

                # Add predictions if requested
                if include_predictions and billing_history:
                    analytics["predictions"] = await self._generate_billing_predictions(
                        tenant_id, billing_history
                    )

                return {
                    "billing_history": billing_history,
                    "analytics": analytics,
                    "next_billing_date": (datetime.utcnow().replace(day=1) + timedelta(days=32)).replace(day=1).isoformat(),
                    "cost_optimization_tips": await self._get_cost_optimization_tips(billing_history)
                }

        except Exception as e:
            logger.error(f"Error fetching billing history: {e}")
            raise HTTPException(status_code=500, detail=f"Billing history failed: {str(e)}")

    async def _calculate_billing_trends(self, history: List[Dict]) -> Dict[str, Any]:
        """Calculate billing trends from historical data"""
        
        if len(history) < 2:
            return {"message": "Insufficient data for trend analysis"}
        
        recent = history[:3]  # Last 3 months
        older = history[3:6] if len(history) > 3 else []
        
        if not older:
            return {"message": "Need more historical data for trend comparison"}
        
        recent_avg = sum(r["total_amount"] for r in recent) / len(recent)
        older_avg = sum(r["total_amount"] for r in older) / len(older)
        
        trend_percentage = ((recent_avg - older_avg) / older_avg) * 100 if older_avg > 0 else 0
        
        return {
            "recent_average": round(recent_avg, 2),
            "previous_average": round(older_avg, 2),
            "trend_percentage": round(trend_percentage, 1),
            "trend_direction": "increasing" if trend_percentage > 5 else "decreasing" if trend_percentage < -5 else "stable",
            "insight": self._get_trend_insight(trend_percentage)
        }

    def _get_trend_insight(self, trend_percentage: float) -> str:
        """Get insight based on billing trend"""
        
        if trend_percentage > 20:
            return "Significant increase - consider plan optimization or outcome improvements"
        elif trend_percentage > 10:
            return "Moderate increase - growth in usage or better outcomes"
        elif trend_percentage < -20:
            return "Significant decrease - possible usage reduction or plan downgrade"
        elif trend_percentage < -10:
            return "Moderate decrease - optimized usage or reduced activity"
        else:
            return "Stable billing pattern - consistent usage and outcomes"

    async def _analyze_pricing_evolution(self, history: List[Dict]) -> Dict[str, Any]:
        """Analyze evolution of pricing components"""
        
        if not history:
            return {}
        
        # Calculate component ratios over time
        evolution = []
        for record in reversed(history[-6:]):  # Last 6 months
            total = record["total_amount"]
            if total > 0:
                evolution.append({
                    "period": record["billing_period"],
                    "base_percentage": round((record["base_charge"] / total) * 100, 1),
                    "usage_percentage": round((record["usage_charges"] / total) * 100, 1),
                    "outcome_percentage": round((record["outcome_charges"] / total) * 100, 1)
                })
        
        # Market alignment analysis
        latest = evolution[-1] if evolution else None
        market_alignment = "Unknown"
        
        if latest:
            outcome_pct = latest["outcome_percentage"]
            if outcome_pct >= 30:
                market_alignment = "Advanced - Leading outcome-based adoption"
            elif outcome_pct >= 15:
                market_alignment = "Progressive - Strong outcome component" 
            elif outcome_pct >= 5:
                market_alignment = "Evolving - Growing outcome focus"
            else:
                market_alignment = "Traditional - Usage-based model"
        
        return {
            "component_evolution": evolution,
            "current_model_type": "Hybrid Pricing",
            "market_alignment": market_alignment,
            "trend_toward_outcomes": outcome_pct >= 15 if latest else False
        }

    async def _analyze_outcome_performance(self, history: List[Dict]) -> Dict[str, Any]:
        """Analyze outcome-based pricing performance"""
        
        outcome_charges = [h["outcome_charges"] for h in history if h["outcome_charges"] > 0]
        
        if not outcome_charges:
            return {
                "message": "No outcome-based charges recorded yet",
                "recommendation": "Focus on measurable business outcomes to unlock outcome-based value"
            }
        
        avg_outcome_charge = sum(outcome_charges) / len(outcome_charges)
        max_outcome = max(outcome_charges)
        total_outcome_value = sum(outcome_charges)
        
        # Estimate actual business value (outcome charges are % of value)
        estimated_business_value = total_outcome_value * 20  # Assume 5% rate = 20x multiplier
        
        return {
            "total_outcome_charges": round(total_outcome_value, 2),
            "average_monthly_outcomes": round(avg_outcome_charge, 2),
            "best_month_outcomes": round(max_outcome, 2),
            "estimated_business_value_created": round(estimated_business_value, 2),
            "outcome_consistency": len(outcome_charges) / len(history),
            "performance_rating": self._get_outcome_rating(avg_outcome_charge),
            "improvement_opportunities": await self._get_outcome_improvement_tips(avg_outcome_charge)
        }

    def _get_outcome_rating(self, avg_outcome: float) -> str:
        """Rate outcome performance"""
        
        if avg_outcome >= 500:
            return "Excellent - High-value outcomes consistently achieved"
        elif avg_outcome >= 200:
            return "Good - Solid outcome performance"
        elif avg_outcome >= 50:
            return "Fair - Moderate outcome achievement" 
        else:
            return "Developing - Focus on measurable outcomes"

    async def _get_outcome_improvement_tips(self, avg_outcome: float) -> List[str]:
        """Get tips for improving outcome performance"""
        
        if avg_outcome >= 500:
            return [
                "Excellent performance - consider sharing success story",
                "Explore additional outcome metrics to capture more value",
                "Consider enterprise tier for unlimited scaling"
            ]
        elif avg_outcome >= 200:
            return [
                "Strong performance - identify top-performing strategies",
                "Document and replicate successful approaches",
                "Consider growth tier for additional capabilities"
            ]
        else:
            return [
                "Focus on setting clear baseline measurements",
                "Implement proper tracking and attribution",
                "Work with success manager to identify high-impact opportunities",
                "Consider professional services for outcome optimization"
            ]

    async def _store_billing_record(self, tenant_id: UUID, bill: Dict[str, Any]):
        """Store encrypted billing record in database"""
        
        try:
            # Encrypt sensitive billing data
            encrypted_data = self.encryption_key.encrypt(
                json.dumps(bill, default=str).encode()
            )
            
            async with get_db() as db:
                query = text("""
                    INSERT INTO billing_records 
                    (tenant_id, billing_period, plan_tier, base_charge, usage_charges, 
                     outcome_charges, total_amount, encrypted_details, created_at)
                    VALUES 
                    (:tenant_id, :billing_period, :plan_tier, :base_charge, :usage_charges,
                     :outcome_charges, :total_amount, :encrypted_details, :created_at)
                """)
                
                await db.execute(query, {
                    'tenant_id': str(tenant_id),
                    'billing_period': datetime.fromisoformat(bill['billing_period'].replace('Z', '+00:00')),
                    'plan_tier': bill['plan'],
                    'base_charge': bill['base_charge'],
                    'usage_charges': bill['usage_charges']['total'],
                    'outcome_charges': bill['outcome_charges']['total'],
                    'total_amount': bill['total_amount'],
                    'encrypted_details': encrypted_data,
                    'created_at': datetime.utcnow()
                })
                
                await db.commit()
                
        except Exception as e:
            logger.error(f"Error storing billing record: {e}")
            # Don't fail the billing process for storage issues
            pass

    async def _create_stripe_invoice(self, tenant_id: UUID, bill: Dict[str, Any]) -> Dict[str, Any]:
        """Create Stripe invoice for the bill"""
        
        if not self.stripe_client:
            return {"error": "Stripe not configured"}
            
        try:
            # Get or create Stripe customer
            async with get_db() as db:
                query = text("""
                    SELECT stripe_customer_id, email 
                    FROM tenants t
                    JOIN users u ON t.id = u.tenant_id
                    WHERE t.id = :tenant_id AND u.is_primary = true
                    LIMIT 1
                """)
                
                result = await db.execute(query, {'tenant_id': str(tenant_id)})
                tenant_data = result.first()
                
                if not tenant_data:
                    return {"error": "Tenant not found"}
                
                stripe_customer_id = tenant_data.stripe_customer_id
                
                # Create customer if doesn't exist
                if not stripe_customer_id:
                    customer = self.stripe_client.Customer.create(
                        email=tenant_data.email,
                        metadata={'tenant_id': str(tenant_id)}
                    )
                    stripe_customer_id = customer.id
                    
                    # Update tenant with Stripe customer ID
                    update_query = text("""
                        UPDATE tenants SET stripe_customer_id = :customer_id 
                        WHERE id = :tenant_id
                    """)
                    await db.execute(update_query, {
                        'customer_id': stripe_customer_id,
                        'tenant_id': str(tenant_id)
                    })
                    await db.commit()
                
                # Create invoice
                invoice = self.stripe_client.Invoice.create(
                    customer=stripe_customer_id,
                    description=f"CoreLDove {bill['plan']} - {bill['billing_period'][:7]}",
                    metadata={
                        'tenant_id': str(tenant_id),
                        'billing_period': bill['billing_period'],
                        'plan': bill['plan']
                    },
                    auto_advance=False  # Manual review before sending
                )
                
                # Add invoice items
                self.stripe_client.InvoiceItem.create(
                    customer=stripe_customer_id,
                    invoice=invoice.id,
                    amount=int(bill['base_charge'] * 100),  # Stripe uses cents
                    currency='usd',
                    description=f"Base Subscription - {bill['plan']}"
                )
                
                if bill['usage_charges']['total'] > 0:
                    self.stripe_client.InvoiceItem.create(
                        customer=stripe_customer_id,
                        invoice=invoice.id,
                        amount=int(bill['usage_charges']['total'] * 100),
                        currency='usd',
                        description="Usage Overages"
                    )
                
                if bill['outcome_charges']['total'] > 0:
                    self.stripe_client.InvoiceItem.create(
                        customer=stripe_customer_id,
                        invoice=invoice.id,
                        amount=int(bill['outcome_charges']['total'] * 100),
                        currency='usd',
                        description="Outcome-Based Success Fees"
                    )
                
                # Finalize invoice
                invoice = self.stripe_client.Invoice.finalize_invoice(invoice.id)
                
                return {
                    "invoice_id": invoice.id,
                    "hosted_invoice_url": invoice.hosted_invoice_url,
                    "pdf_url": invoice.invoice_pdf,
                    "status": invoice.status
                }
                
        except Exception as e:
            logger.error(f"Error creating Stripe invoice: {e}")
            return {"error": str(e)}

    async def _log_recommendation(
        self, 
        tenant_id: UUID, 
        profile: BusinessProfile, 
        recommendation: Dict[str, Any]
    ):
        """Log plan recommendation for analytics"""
        
        try:
            async with get_db() as db:
                query = text("""
                    INSERT INTO plan_recommendations 
                    (tenant_id, business_profile, recommendation, created_at)
                    VALUES (:tenant_id, :profile, :recommendation, :created_at)
                """)
                
                await db.execute(query, {
                    'tenant_id': str(tenant_id),
                    'profile': json.dumps(profile.dict(), default=str),
                    'recommendation': json.dumps(recommendation, default=str),
                    'created_at': datetime.utcnow()
                })
                
                await db.commit()
                
        except Exception as e:
            logger.error(f"Error logging recommendation: {e}")
            # Don't fail for logging issues
            pass

    async def get_real_time_billing_status(self, tenant_id: UUID) -> Dict[str, Any]:
        """
        Get real-time billing status and current month projections
        """
        try:
            current_month = datetime.utcnow().replace(day=1)
            
            # Get current month usage from tracking
            async with get_db() as db:
                usage_query = text("""
                    SELECT 
                        agent_type,
                        operation,
                        COUNT(*) as operation_count,
                        SUM(tokens_used) as total_tokens,
                        SUM(cost_amount) as total_cost
                    FROM ai_agent_usage 
                    WHERE tenant_id = :tenant_id 
                        AND usage_date >= :current_month
                    GROUP BY agent_type, operation
                """)
                
                usage_result = await db.execute(usage_query, {
                    'tenant_id': str(tenant_id),
                    'current_month': current_month
                })
                
                current_usage = []
                total_cost = 0
                
                for row in usage_result:
                    usage_record = {
                        "agent_type": row.agent_type,
                        "operation": row.operation,
                        "operation_count": row.operation_count,
                        "total_tokens": row.total_tokens,
                        "total_cost": float(row.total_cost)
                    }
                    current_usage.append(usage_record)
                    total_cost += float(row.total_cost)
                
                # Get subscription details
                sub_query = text("""
                    SELECT 
                        s.status, s.current_period_start, s.current_period_end,
                        sp.name as plan_name, sp.price_monthly, sp.limits
                    FROM subscriptions s
                    JOIN subscription_plans sp ON s.plan_id = sp.id
                    WHERE s.tenant_id = :tenant_id AND s.status = 'active'
                    ORDER BY s.created_at DESC
                    LIMIT 1
                """)
                
                sub_result = await db.execute(sub_query, {'tenant_id': str(tenant_id)})
                subscription = sub_result.first()
                
                if not subscription:
                    raise HTTPException(status_code=404, detail="No active subscription found")
                
                # Calculate projected monthly total
                days_elapsed = (datetime.utcnow() - current_month).days + 1
                days_in_month = (current_month.replace(month=current_month.month % 12 + 1, day=1) - timedelta(days=1)).day
                
                projection_multiplier = days_in_month / days_elapsed if days_elapsed > 0 else 1
                projected_usage_cost = total_cost * projection_multiplier
                projected_total = float(subscription.price_monthly) + projected_usage_cost
                
                # Usage limits check
                limits = subscription.limits or {}
                usage_warnings = []
                
                monthly_operations = sum(u["operation_count"] for u in current_usage)
                if limits.get("monthly_operations") and monthly_operations > limits["monthly_operations"] * 0.8:
                    usage_warnings.append({
                        "type": "usage_limit",
                        "message": f"Approaching monthly operation limit ({monthly_operations}/{limits['monthly_operations']})"
                    })
                
                return {
                    "tenant_id": str(tenant_id),
                    "current_period": {
                        "start": subscription.current_period_start.isoformat(),
                        "end": subscription.current_period_end.isoformat(),
                        "days_elapsed": days_elapsed,
                        "days_remaining": (subscription.current_period_end - datetime.utcnow().date()).days
                    },
                    "subscription": {
                        "plan_name": subscription.plan_name,
                        "base_price": float(subscription.price_monthly),
                        "status": subscription.status
                    },
                    "current_usage": {
                        "total_operations": monthly_operations,
                        "total_cost": round(total_cost, 2),
                        "usage_breakdown": current_usage
                    },
                    "projections": {
                        "projected_usage_cost": round(projected_usage_cost, 2),
                        "projected_total": round(projected_total, 2),
                        "confidence": "Medium" if days_elapsed > 7 else "Low"
                    },
                    "warnings": usage_warnings,
                    "next_billing_date": subscription.current_period_end.isoformat(),
                    "cost_optimization": await self._get_real_time_optimization_tips(current_usage, limits)
                }

        except Exception as e:
            logger.error(f"Error getting real-time billing status: {e}")
            raise HTTPException(status_code=500, detail=f"Billing status failed: {str(e)}")

    async def _get_real_time_optimization_tips(
        self, 
        usage: List[Dict], 
        limits: Dict
    ) -> List[str]:
        """Get real-time cost optimization tips"""
        
        tips = []
        
        # Analyze usage patterns
        high_cost_operations = [u for u in usage if u["total_cost"] > 10]
        if high_cost_operations:
            tips.append("Consider optimizing high-cost operations or batch processing")
        
        # Check for usage concentration
        total_ops = sum(u["operation_count"] for u in usage)
        if usage and max(u["operation_count"] for u in usage) > total_ops * 0.6:
            tips.append("Usage concentrated in single operation - consider diversification")
        
        # Limit utilization check
        if limits.get("monthly_operations"):
            utilization = total_ops / limits["monthly_operations"]
            if utilization > 0.9:
                tips.append("Consider upgrading plan to avoid overage charges")
            elif utilization < 0.3:
                tips.append("Consider downgrading plan if consistent low usage")
        
        if not tips:
            tips.append("Usage patterns look optimal - continue current approach")
        
        return tips

# Initialize service instance
pricing_engine_service = PricingEngineService()
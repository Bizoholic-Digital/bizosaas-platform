"""
Multi-Project CrewAI Agent Management System

This module provides comprehensive agent management across multiple business projects
within the BizOSaaS platform ecosystem. It implements specialized agent crews for
different business domains with intelligent workflow orchestration and cross-project
collaboration capabilities.

Supported Projects:
- Bizoholic: AI Marketing Agency automation
- CoreLDove: E-commerce platform optimization  
- ThrillRing: Event management and social coordination
- QuantTrade: Financial trading and analysis
- BizOSaaS Core: Platform administration and tenant management
"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import structlog

# CrewAI imports
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool

# Import the advanced orchestrator
from crewai_workflow_orchestrator import (
    WorkflowOrchestrator, HierarchicalAgent, AgentRole, TaskPriority,
    WorkflowConfiguration, TaskDefinition, WorkflowResult, AdvancedAgentTool
)

# Import existing components
from review_management_agents import ReviewWorkflowCrew

logger = structlog.get_logger(__name__)


class ProjectType(Enum):
    """Supported project types in the BizOSaaS ecosystem"""
    BIZOHOLIC = "bizoholic"
    CORELDOVE = "coreldove"
    THRILLRING = "thrillring"
    QUANTTRADE = "quanttrade"
    BIZOSAAS_CORE = "bizosaas_core"


class BusinessDomain(Enum):
    """Business domains for agent specialization"""
    MARKETING = "marketing"
    ECOMMERCE = "ecommerce"
    EVENTS = "events"
    FINANCE = "finance"
    ADMINISTRATION = "administration"
    ANALYTICS = "analytics"
    CONTENT = "content"
    CUSTOMER_SERVICE = "customer_service"
    SALES = "sales"
    OPERATIONS = "operations"


@dataclass
class ProjectConfiguration:
    """Configuration for a specific project"""
    project_id: str
    project_type: ProjectType
    business_domain: BusinessDomain
    tenant_id: str
    config: Dict[str, Any]
    active_agents: List[str]
    resource_allocation: Dict[str, Any]
    integration_endpoints: Dict[str, str]


class BizoholicAgentTool(AdvancedAgentTool):
    """Specialized tool for Bizoholic marketing automation"""
    
    def __init__(self):
        super().__init__(
            name="bizoholic_marketing_automation",
            description="Execute marketing automation tasks for Bizoholic clients",
            func=self._execute_marketing_task
        )
    
    def _execute_marketing_task(self, task_type: str, client_data: Dict[str, Any], 
                               campaign_params: Dict[str, Any]) -> str:
        """Execute marketing automation tasks"""
        try:
            if task_type == "campaign_strategy":
                return self._generate_campaign_strategy(client_data, campaign_params)
            elif task_type == "content_generation":
                return self._generate_marketing_content(client_data, campaign_params)
            elif task_type == "performance_analysis":
                return self._analyze_campaign_performance(client_data, campaign_params)
            elif task_type == "audience_targeting":
                return self._optimize_audience_targeting(client_data, campaign_params)
            else:
                return json.dumps({"error": f"Unknown task type: {task_type}"})
        
        except Exception as e:
            logger.error(f"Bizoholic marketing task failed: {e}")
            return json.dumps({"error": str(e)})
    
    def _generate_campaign_strategy(self, client_data: Dict[str, Any], 
                                  params: Dict[str, Any]) -> str:
        """Generate comprehensive marketing campaign strategy"""
        strategy = {
            "campaign_type": params.get("type", "digital_marketing"),
            "target_audience": self._analyze_target_audience(client_data),
            "channel_strategy": self._recommend_channels(client_data),
            "budget_allocation": self._optimize_budget_allocation(params.get("budget", 10000)),
            "timeline": self._create_campaign_timeline(params.get("duration", 30)),
            "kpis": self._define_success_metrics(client_data),
            "creative_guidelines": self._generate_creative_guidelines(client_data),
            "implementation_plan": self._create_implementation_plan(client_data, params)
        }
        
        return json.dumps(strategy, indent=2)
    
    def _generate_marketing_content(self, client_data: Dict[str, Any], 
                                  params: Dict[str, Any]) -> str:
        """Generate marketing content for campaigns"""
        content = {
            "content_type": params.get("content_type", "social_media"),
            "brand_voice": client_data.get("brand_voice", "professional"),
            "generated_content": {
                "headlines": self._generate_headlines(client_data, params),
                "descriptions": self._generate_descriptions(client_data, params),
                "call_to_actions": self._generate_ctas(client_data, params),
                "hashtags": self._generate_hashtags(client_data, params)
            },
            "platform_optimization": self._optimize_for_platforms(params.get("platforms", [])),
            "a_b_test_variants": self._create_ab_test_variants(client_data, params)
        }
        
        return json.dumps(content, indent=2)
    
    def _analyze_campaign_performance(self, client_data: Dict[str, Any], 
                                    params: Dict[str, Any]) -> str:
        """Analyze marketing campaign performance"""
        analysis = {
            "campaign_id": params.get("campaign_id"),
            "performance_metrics": {
                "impressions": params.get("impressions", 10000),
                "clicks": params.get("clicks", 500),
                "conversions": params.get("conversions", 25),
                "ctr": params.get("clicks", 500) / params.get("impressions", 10000),
                "conversion_rate": params.get("conversions", 25) / params.get("clicks", 500),
                "cost_per_conversion": params.get("spend", 1000) / params.get("conversions", 25)
            },
            "insights": self._generate_performance_insights(params),
            "optimization_recommendations": self._recommend_optimizations(params),
            "competitor_analysis": self._analyze_competitor_performance(client_data),
            "next_steps": self._recommend_next_steps(params)
        }
        
        return json.dumps(analysis, indent=2)
    
    def _analyze_target_audience(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and define target audience"""
        return {
            "demographics": {
                "age_range": "25-45",
                "gender": "all",
                "income_level": "middle to upper-middle",
                "education": "college educated"
            },
            "psychographics": {
                "interests": ["technology", "business", "productivity"],
                "values": ["efficiency", "innovation", "quality"],
                "lifestyle": "busy professionals"
            },
            "behavioral_patterns": {
                "online_behavior": "active on LinkedIn and professional networks",
                "buying_behavior": "research-driven, value-conscious",
                "content_preferences": "educational, data-driven content"
            }
        }
    
    def _recommend_channels(self, client_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend marketing channels"""
        return [
            {"channel": "Google Ads", "priority": "high", "budget_allocation": 40},
            {"channel": "LinkedIn Ads", "priority": "high", "budget_allocation": 30},
            {"channel": "Content Marketing", "priority": "medium", "budget_allocation": 20},
            {"channel": "Email Marketing", "priority": "medium", "budget_allocation": 10}
        ]
    
    def _optimize_budget_allocation(self, total_budget: float) -> Dict[str, float]:
        """Optimize budget allocation across channels"""
        return {
            "paid_advertising": total_budget * 0.6,
            "content_creation": total_budget * 0.2,
            "tools_and_software": total_budget * 0.1,
            "analytics_and_tracking": total_budget * 0.1
        }
    
    def _create_campaign_timeline(self, duration_days: int) -> Dict[str, str]:
        """Create campaign timeline"""
        start_date = datetime.now()
        return {
            "planning_phase": f"{start_date.strftime('%Y-%m-%d')} - {(start_date + timedelta(days=7)).strftime('%Y-%m-%d')}",
            "launch_phase": f"{(start_date + timedelta(days=7)).strftime('%Y-%m-%d')} - {(start_date + timedelta(days=14)).strftime('%Y-%m-%d')}",
            "optimization_phase": f"{(start_date + timedelta(days=14)).strftime('%Y-%m-%d')} - {(start_date + timedelta(days=duration_days-7)).strftime('%Y-%m-%d')}",
            "analysis_phase": f"{(start_date + timedelta(days=duration_days-7)).strftime('%Y-%m-%d')} - {(start_date + timedelta(days=duration_days)).strftime('%Y-%m-%d')}"
        }
    
    def _define_success_metrics(self, client_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Define success metrics and KPIs"""
        return [
            {"metric": "Cost Per Acquisition", "target": "<$50", "importance": "high"},
            {"metric": "Conversion Rate", "target": ">3%", "importance": "high"},
            {"metric": "Return on Ad Spend", "target": ">4:1", "importance": "high"},
            {"metric": "Brand Awareness Lift", "target": ">20%", "importance": "medium"},
            {"metric": "Engagement Rate", "target": ">5%", "importance": "medium"}
        ]
    
    def _generate_creative_guidelines(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate creative guidelines for campaigns"""
        return {
            "brand_colors": ["#1a365d", "#2d3748", "#4a5568"],
            "typography": "Modern, clean sans-serif fonts",
            "imagery_style": "Professional, high-quality business imagery",
            "tone_of_voice": "Professional yet approachable, authoritative but friendly",
            "key_messages": ["Efficiency", "Innovation", "Results-driven", "Professional excellence"],
            "call_to_action_style": "Direct, action-oriented, value-focused"
        }
    
    def _create_implementation_plan(self, client_data: Dict[str, Any], 
                                  params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create detailed implementation plan"""
        return [
            {
                "phase": "Setup",
                "duration": "Week 1",
                "tasks": ["Set up tracking", "Create accounts", "Design creatives"],
                "deliverables": ["Tracking setup", "Campaign structure", "Creative assets"]
            },
            {
                "phase": "Launch",
                "duration": "Week 2",
                "tasks": ["Launch campaigns", "Monitor performance", "Initial optimizations"],
                "deliverables": ["Live campaigns", "Performance report", "Optimization log"]
            },
            {
                "phase": "Optimize",
                "duration": "Weeks 3-4",
                "tasks": ["A/B testing", "Bid optimization", "Audience refinement"],
                "deliverables": ["Test results", "Optimized campaigns", "Performance improvements"]
            }
        ]
    
    def _generate_headlines(self, client_data: Dict[str, Any], 
                          params: Dict[str, Any]) -> List[str]:
        """Generate compelling headlines"""
        return [
            "Transform Your Business with AI-Powered Marketing Solutions",
            "Boost ROI by 300% with Smart Marketing Automation",
            "From Strategy to Success: Complete Marketing Solutions",
            "Professional Marketing That Delivers Real Results"
        ]
    
    def _generate_descriptions(self, client_data: Dict[str, Any], 
                             params: Dict[str, Any]) -> List[str]:
        """Generate marketing descriptions"""
        return [
            "Discover how our AI-powered marketing platform can transform your business growth strategy and deliver measurable results.",
            "Join thousands of successful businesses using our comprehensive marketing automation platform to scale their operations.",
            "Get expert marketing strategy, implementation, and optimization - all in one powerful platform designed for growth."
        ]
    
    def _generate_ctas(self, client_data: Dict[str, Any], 
                      params: Dict[str, Any]) -> List[str]:
        """Generate call-to-action phrases"""
        return [
            "Start Your Free Trial Today",
            "Get Your Marketing Strategy Audit",
            "Schedule a Demo",
            "Claim Your Free Consultation",
            "Download Our Success Guide"
        ]
    
    def _generate_hashtags(self, client_data: Dict[str, Any], 
                         params: Dict[str, Any]) -> List[str]:
        """Generate relevant hashtags"""
        return [
            "#MarketingAutomation", "#BusinessGrowth", "#DigitalMarketing",
            "#AIMarketing", "#ROIOptimization", "#MarketingStrategy",
            "#BusinessSuccess", "#GrowthHacking", "#MarketingTech"
        ]
    
    def _optimize_for_platforms(self, platforms: List[str]) -> Dict[str, Dict[str, Any]]:
        """Optimize content for different platforms"""
        optimization = {}
        
        for platform in platforms:
            if platform.lower() == "linkedin":
                optimization[platform] = {
                    "character_limit": 1300,
                    "tone": "professional",
                    "content_type": "industry insights and thought leadership",
                    "best_times": ["Tuesday-Thursday 8-10am, 12-2pm"]
                }
            elif platform.lower() == "facebook":
                optimization[platform] = {
                    "character_limit": 500,
                    "tone": "friendly and engaging",
                    "content_type": "visual content with strong emotional appeal",
                    "best_times": ["Wednesday-Friday 1-3pm"]
                }
            elif platform.lower() == "google_ads":
                optimization[platform] = {
                    "headline_limit": 30,
                    "description_limit": 90,
                    "tone": "direct and action-oriented",
                    "focus": "keywords and search intent"
                }
        
        return optimization
    
    def _create_ab_test_variants(self, client_data: Dict[str, Any], 
                               params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create A/B testing variants"""
        return [
            {
                "variant": "A",
                "headline": "Transform Your Business with AI Marketing",
                "description": "Discover powerful marketing automation that drives results",
                "cta": "Start Free Trial",
                "focus": "transformation and AI"
            },
            {
                "variant": "B", 
                "headline": "Boost ROI by 300% with Smart Marketing",
                "description": "Join successful businesses scaling with our platform",
                "cta": "Get Demo",
                "focus": "specific results and social proof"
            }
        ]
    
    def _generate_performance_insights(self, params: Dict[str, Any]) -> List[str]:
        """Generate performance insights"""
        insights = []
        
        ctr = params.get("clicks", 500) / params.get("impressions", 10000)
        if ctr < 0.02:
            insights.append("Click-through rate is below industry average. Consider improving ad copy or targeting.")
        elif ctr > 0.05:
            insights.append("Excellent click-through rate! Your messaging resonates well with the audience.")
        
        conversion_rate = params.get("conversions", 25) / params.get("clicks", 500)
        if conversion_rate < 0.02:
            insights.append("Conversion rate needs improvement. Review landing page experience and offer clarity.")
        elif conversion_rate > 0.05:
            insights.append("Strong conversion rate indicates effective landing page and compelling offer.")
        
        return insights
    
    def _recommend_optimizations(self, params: Dict[str, Any]) -> List[Dict[str, str]]:
        """Recommend campaign optimizations"""
        return [
            {
                "area": "Targeting",
                "recommendation": "Expand successful audience segments and exclude low-performing demographics",
                "expected_impact": "15-25% improvement in conversion rate"
            },
            {
                "area": "Creative",
                "recommendation": "Test new ad formats and update creative assets based on performance data",
                "expected_impact": "10-20% improvement in engagement"
            },
            {
                "area": "Bidding",
                "recommendation": "Implement automated bidding strategies for better cost optimization",
                "expected_impact": "20-30% reduction in cost per conversion"
            }
        ]
    
    def _analyze_competitor_performance(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitor performance"""
        return {
            "competitive_position": "Above average performance in key metrics",
            "market_share_estimate": "15-20% in target segment",
            "competitive_advantages": [
                "Superior targeting precision",
                "Higher quality creative assets",
                "Better landing page conversion rates"
            ],
            "areas_for_improvement": [
                "Expand to additional platforms",
                "Increase content marketing efforts",
                "Improve remarketing strategies"
            ]
        }
    
    def _recommend_next_steps(self, params: Dict[str, Any]) -> List[Dict[str, str]]:
        """Recommend next steps"""
        return [
            {
                "priority": "High",
                "action": "Scale successful campaigns to additional markets",
                "timeline": "Next 2 weeks"
            },
            {
                "priority": "Medium", 
                "action": "Develop remarketing campaigns for website visitors",
                "timeline": "Next 30 days"
            },
            {
                "priority": "Medium",
                "action": "Create seasonal campaign variations",
                "timeline": "Next 45 days"
            }
        ]


class CoreLDoveAgentTool(AdvancedAgentTool):
    """Specialized tool for CoreLDove e-commerce optimization"""
    
    def __init__(self):
        super().__init__(
            name="coreldove_ecommerce_optimization",
            description="Execute e-commerce optimization tasks for CoreLDove platform",
            func=self._execute_ecommerce_task
        )
    
    def _execute_ecommerce_task(self, task_type: str, store_data: Dict[str, Any], 
                               optimization_params: Dict[str, Any]) -> str:
        """Execute e-commerce optimization tasks"""
        try:
            if task_type == "product_optimization":
                return self._optimize_product_listings(store_data, optimization_params)
            elif task_type == "pricing_strategy":
                return self._optimize_pricing_strategy(store_data, optimization_params)
            elif task_type == "inventory_management":
                return self._optimize_inventory_management(store_data, optimization_params)
            elif task_type == "customer_journey":
                return self._optimize_customer_journey(store_data, optimization_params)
            elif task_type == "conversion_optimization":
                return self._optimize_conversion_funnel(store_data, optimization_params)
            else:
                return json.dumps({"error": f"Unknown task type: {task_type}"})
        
        except Exception as e:
            logger.error(f"CoreLDove e-commerce task failed: {e}")
            return json.dumps({"error": str(e)})
    
    def _optimize_product_listings(self, store_data: Dict[str, Any], 
                                 params: Dict[str, Any]) -> str:
        """Optimize product listings for better visibility and conversion"""
        optimization = {
            "seo_optimization": {
                "title_optimization": self._optimize_product_titles(params.get("products", [])),
                "description_enhancement": self._enhance_product_descriptions(params.get("products", [])),
                "keyword_optimization": self._optimize_product_keywords(params.get("products", [])),
                "image_optimization": self._optimize_product_images(params.get("products", []))
            },
            "conversion_optimization": {
                "pricing_display": self._optimize_pricing_display(params.get("products", [])),
                "review_integration": self._optimize_review_display(params.get("products", [])),
                "urgency_indicators": self._add_urgency_indicators(params.get("products", [])),
                "cross_selling": self._optimize_cross_selling(params.get("products", []))
            },
            "performance_metrics": {
                "expected_improvements": {
                    "search_visibility": "25-40% increase",
                    "click_through_rate": "15-30% increase",
                    "conversion_rate": "10-20% increase"
                }
            }
        }
        
        return json.dumps(optimization, indent=2)
    
    def _optimize_pricing_strategy(self, store_data: Dict[str, Any], 
                                 params: Dict[str, Any]) -> str:
        """Optimize pricing strategy for maximum profitability"""
        strategy = {
            "dynamic_pricing": {
                "competitor_analysis": self._analyze_competitor_pricing(params.get("products", [])),
                "demand_elasticity": self._analyze_price_elasticity(params.get("products", [])),
                "seasonal_adjustments": self._recommend_seasonal_pricing(params.get("products", [])),
                "psychological_pricing": self._implement_psychological_pricing(params.get("products", []))
            },
            "promotion_strategy": {
                "discount_optimization": self._optimize_discount_strategies(store_data),
                "bundle_pricing": self._create_bundle_strategies(params.get("products", [])),
                "loyalty_pricing": self._design_loyalty_pricing(store_data),
                "flash_sales": self._plan_flash_sale_campaigns(params.get("products", []))
            },
            "revenue_optimization": {
                "price_testing": self._design_price_tests(params.get("products", [])),
                "margin_analysis": self._analyze_profit_margins(params.get("products", [])),
                "value_proposition": self._enhance_value_propositions(params.get("products", []))
            }
        }
        
        return json.dumps(strategy, indent=2)
    
    def _optimize_inventory_management(self, store_data: Dict[str, Any], 
                                     params: Dict[str, Any]) -> str:
        """Optimize inventory management for better efficiency"""
        optimization = {
            "demand_forecasting": {
                "sales_prediction": self._predict_sales_demand(params.get("historical_data", {})),
                "seasonal_patterns": self._identify_seasonal_patterns(params.get("historical_data", {})),
                "trend_analysis": self._analyze_product_trends(params.get("products", [])),
                "stock_recommendations": self._recommend_stock_levels(params.get("products", []))
            },
            "supplier_optimization": {
                "supplier_performance": self._analyze_supplier_performance(params.get("suppliers", [])),
                "lead_time_optimization": self._optimize_lead_times(params.get("suppliers", [])),
                "quality_metrics": self._track_quality_metrics(params.get("suppliers", [])),
                "cost_optimization": self._optimize_supplier_costs(params.get("suppliers", []))
            },
            "warehouse_efficiency": {
                "layout_optimization": self._optimize_warehouse_layout(store_data),
                "picking_efficiency": self._improve_picking_processes(store_data),
                "automation_opportunities": self._identify_automation_opportunities(store_data)
            }
        }
        
        return json.dumps(optimization, indent=2)
    
    def _optimize_customer_journey(self, store_data: Dict[str, Any], 
                                 params: Dict[str, Any]) -> str:
        """Optimize customer journey for better experience and conversion"""
        journey_optimization = {
            "discovery_phase": {
                "seo_optimization": self._optimize_search_discovery(store_data),
                "social_media_presence": self._enhance_social_presence(store_data),
                "content_marketing": self._develop_content_strategy(store_data),
                "paid_advertising": self._optimize_paid_campaigns(store_data)
            },
            "consideration_phase": {
                "product_comparison": self._enhance_product_comparison(store_data),
                "review_social_proof": self._leverage_social_proof(store_data),
                "educational_content": self._create_educational_content(store_data),
                "personalization": self._implement_personalization(store_data)
            },
            "purchase_phase": {
                "checkout_optimization": self._optimize_checkout_process(store_data),
                "payment_options": self._expand_payment_options(store_data),
                "security_trust": self._enhance_trust_signals(store_data),
                "urgency_scarcity": self._implement_urgency_tactics(store_data)
            },
            "post_purchase": {
                "order_confirmation": self._optimize_order_confirmation(store_data),
                "shipping_communication": self._improve_shipping_updates(store_data),
                "follow_up_campaigns": self._design_follow_up_campaigns(store_data),
                "loyalty_programs": self._enhance_loyalty_programs(store_data)
            }
        }
        
        return json.dumps(journey_optimization, indent=2)
    
    def _optimize_conversion_funnel(self, store_data: Dict[str, Any], 
                                  params: Dict[str, Any]) -> str:
        """Optimize conversion funnel for maximum efficiency"""
        funnel_optimization = {
            "traffic_analysis": {
                "source_performance": self._analyze_traffic_sources(params.get("analytics", {})),
                "landing_page_optimization": self._optimize_landing_pages(store_data),
                "mobile_optimization": self._optimize_mobile_experience(store_data),
                "page_speed": self._optimize_page_speed(store_data)
            },
            "engagement_optimization": {
                "content_personalization": self._personalize_content(store_data),
                "search_functionality": self._enhance_search_functionality(store_data),
                "product_recommendations": self._improve_recommendations(store_data),
                "user_experience": self._enhance_user_experience(store_data)
            },
            "conversion_optimization": {
                "checkout_optimization": self._streamline_checkout(store_data),
                "abandoned_cart_recovery": self._optimize_cart_recovery(store_data),
                "payment_optimization": self._optimize_payment_flow(store_data),
                "trust_building": self._build_customer_trust(store_data)
            }
        }
        
        return json.dumps(funnel_optimization, indent=2)
    
    # Helper methods for product optimization
    def _optimize_product_titles(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize product titles for SEO and conversion"""
        optimizations = []
        for product in products[:5]:  # Sample optimization
            optimizations.append({
                "product_id": product.get("id", "unknown"),
                "current_title": product.get("title", ""),
                "optimized_title": f"{product.get('title', '')} - Premium Quality, Fast Shipping",
                "improvements": ["Added quality indicator", "Added shipping benefit", "Enhanced SEO keywords"]
            })
        return optimizations
    
    def _enhance_product_descriptions(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhance product descriptions for better conversion"""
        enhancements = []
        for product in products[:5]:
            enhancements.append({
                "product_id": product.get("id", "unknown"),
                "enhancement_type": "conversion_focused",
                "improvements": [
                    "Added benefit-focused bullet points",
                    "Included social proof elements",
                    "Enhanced with emotional triggers",
                    "Optimized for featured snippets"
                ],
                "expected_impact": "15-25% increase in conversion rate"
            })
        return enhancements
    
    def _optimize_product_keywords(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Optimize product keywords for better search visibility"""
        return {
            "keyword_strategy": "Long-tail, high-intent keywords",
            "primary_keywords": ["premium quality", "fast shipping", "best price"],
            "semantic_keywords": ["top rated", "customer favorite", "trending"],
            "local_keywords": ["near me", "same day delivery", "local store"],
            "optimization_impact": "30-50% improvement in organic search visibility"
        }
    
    def _optimize_product_images(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Optimize product images for better performance"""
        return {
            "technical_optimization": [
                "Compress images for faster loading",
                "Add descriptive alt tags for SEO",
                "Implement lazy loading",
                "Use next-gen image formats (WebP)"
            ],
            "visual_optimization": [
                "Add lifestyle context images",
                "Include size comparison visuals",
                "Show product in use scenarios",
                "Add 360-degree product views"
            ],
            "conversion_optimization": [
                "Implement image zoom functionality",
                "Add image gallery with thumbnails",
                "Include product video demonstrations",
                "Show multiple product angles"
            ]
        }
    
    def _analyze_competitor_pricing(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze competitor pricing strategies"""
        return {
            "market_position": "Competitive pricing with premium positioning",
            "price_comparison": {
                "vs_amazon": "5-10% higher, justified by service quality",
                "vs_direct_competitors": "Within 3% range, competitive",
                "vs_discount_retailers": "20-30% premium, value-positioned"
            },
            "pricing_opportunities": [
                "Bundle pricing for higher margins",
                "Premium tier for enhanced features",
                "Loyalty discounts for repeat customers"
            ]
        }
    
    def _analyze_price_elasticity(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze price elasticity for products"""
        return {
            "elasticity_segments": {
                "price_sensitive": {"percentage": 30, "strategy": "Value pricing with discounts"},
                "quality_focused": {"percentage": 50, "strategy": "Premium pricing with quality emphasis"},
                "convenience_focused": {"percentage": 20, "strategy": "Convenience premium pricing"}
            },
            "optimal_price_points": {
                "budget_tier": "10-15% below market average",
                "standard_tier": "Market average pricing",
                "premium_tier": "15-25% above market average"
            }
        }


class MultiProjectAgentManager:
    """Manages CrewAI agents across multiple business projects"""
    
    def __init__(self):
        self.projects: Dict[str, ProjectConfiguration] = {}
        self.active_crews: Dict[str, Dict[str, Crew]] = {}
        self.orchestrator = None
        self.performance_tracker = {}
        self.cross_project_collaborations = {}
    
    async def initialize(self):
        """Initialize the multi-project agent manager"""
        from crewai_workflow_orchestrator import get_workflow_orchestrator
        self.orchestrator = await get_workflow_orchestrator()
        
        # Initialize project configurations
        await self._initialize_project_configurations()
        
        # Create specialized agent crews for each project
        await self._create_project_crews()
        
        logger.info("Multi-project agent manager initialized successfully")
    
    async def _initialize_project_configurations(self):
        """Initialize configurations for all supported projects"""
        # Bizoholic configuration
        self.projects["bizoholic"] = ProjectConfiguration(
            project_id="bizoholic",
            project_type=ProjectType.BIZOHOLIC,
            business_domain=BusinessDomain.MARKETING,
            tenant_id="bizoholic_main",
            config={
                "focus_areas": ["digital_marketing", "campaign_automation", "lead_generation"],
                "client_types": ["small_business", "agencies", "enterprises"],
                "service_offerings": ["strategy", "execution", "analytics", "optimization"]
            },
            active_agents=[],
            resource_allocation={"cpu": 0.3, "memory": 0.25, "priority": "high"},
            integration_endpoints={
                "wordpress_api": "http://localhost:3000/wp-json",
                "n8n_workflows": "http://localhost:5678/webhook",
                "analytics_api": "http://localhost:3006/api/brain/analytics"
            }
        )
        
        # CoreLDove configuration
        self.projects["coreldove"] = ProjectConfiguration(
            project_id="coreldove",
            project_type=ProjectType.CORELDOVE,
            business_domain=BusinessDomain.ECOMMERCE,
            tenant_id="coreldove_main",
            config={
                "focus_areas": ["product_optimization", "inventory_management", "customer_experience"],
                "platform_types": ["b2b", "b2c", "marketplace"],
                "optimization_goals": ["conversion", "revenue", "efficiency", "satisfaction"]
            },
            active_agents=[],
            resource_allocation={"cpu": 0.25, "memory": 0.3, "priority": "high"},
            integration_endpoints={
                "saleor_api": "http://localhost:8000/graphql",
                "inventory_api": "http://localhost:3006/api/brain/inventory",
                "analytics_api": "http://localhost:3006/api/brain/ecommerce-analytics"
            }
        )
        
        # ThrillRing configuration
        self.projects["thrillring"] = ProjectConfiguration(
            project_id="thrillring",
            project_type=ProjectType.THRILLRING,
            business_domain=BusinessDomain.EVENTS,
            tenant_id="thrillring_main",
            config={
                "focus_areas": ["event_planning", "social_coordination", "engagement_optimization"],
                "event_types": ["corporate", "social", "educational", "entertainment"],
                "automation_goals": ["registration", "communication", "feedback", "analytics"]
            },
            active_agents=[],
            resource_allocation={"cpu": 0.2, "memory": 0.2, "priority": "medium"},
            integration_endpoints={
                "event_api": "http://localhost:3006/api/brain/events",
                "notification_api": "http://localhost:3006/api/brain/notifications",
                "social_api": "http://localhost:3006/api/brain/social"
            }
        )
        
        # QuantTrade configuration
        self.projects["quanttrade"] = ProjectConfiguration(
            project_id="quanttrade",
            project_type=ProjectType.QUANTTRADE,
            business_domain=BusinessDomain.FINANCE,
            tenant_id="quanttrade_main",
            config={
                "focus_areas": ["market_analysis", "risk_management", "strategy_optimization"],
                "trading_types": ["algorithmic", "manual", "hybrid"],
                "analysis_goals": ["prediction", "risk_assessment", "performance_optimization"]
            },
            active_agents=[],
            resource_allocation={"cpu": 0.15, "memory": 0.15, "priority": "medium"},
            integration_endpoints={
                "trading_api": "http://localhost:3006/api/brain/trading",
                "market_data_api": "http://localhost:3006/api/brain/market-data",
                "risk_api": "http://localhost:3006/api/brain/risk-management"
            }
        )
        
        # BizOSaaS Core configuration
        self.projects["bizosaas_core"] = ProjectConfiguration(
            project_id="bizosaas_core",
            project_type=ProjectType.BIZOSAAS_CORE,
            business_domain=BusinessDomain.ADMINISTRATION,
            tenant_id="bizosaas_system",
            config={
                "focus_areas": ["tenant_management", "system_optimization", "security_monitoring"],
                "admin_types": ["super_admin", "tenant_admin", "support"],
                "automation_goals": ["provisioning", "monitoring", "maintenance", "reporting"]
            },
            active_agents=[],
            resource_allocation={"cpu": 0.1, "memory": 0.1, "priority": "low"},
            integration_endpoints={
                "admin_api": "http://localhost:3006/api/brain/admin",
                "monitoring_api": "http://localhost:3006/api/brain/monitoring",
                "security_api": "http://localhost:3006/api/brain/security"
            }
        )
    
    async def _create_project_crews(self):
        """Create specialized crews for each project"""
        # Initialize active crews dictionary
        for project_id in self.projects.keys():
            self.active_crews[project_id] = {}
        
        # Create Bizoholic crews
        await self._create_bizoholic_crews()
        
        # Create CoreLDove crews
        await self._create_coreldove_crews()
        
        # Create ThrillRing crews
        await self._create_thrillring_crews()
        
        # Create QuantTrade crews
        await self._create_quanttrade_crews()
        
        # Create BizOSaaS Core crews
        await self._create_bizosaas_core_crews()
    
    async def _create_bizoholic_crews(self):
        """Create specialized crews for Bizoholic marketing automation"""
        # Marketing Strategy Crew
        strategy_agent = Agent(
            role='Marketing Strategy Director',
            goal='Develop comprehensive marketing strategies for clients',
            backstory="""You are a senior marketing strategist with 15+ years of experience
            in digital marketing across various industries. You excel at creating data-driven
            marketing strategies that deliver measurable results.""",
            verbose=True,
            allow_delegation=True,
            tools=[BizoholicAgentTool()],
            memory=True
        )
        
        campaign_agent = Agent(
            role='Campaign Execution Specialist',
            goal='Execute and optimize marketing campaigns across multiple channels',
            backstory="""You are a campaign execution expert who specializes in multi-channel
            marketing campaigns. You know how to coordinate complex campaigns and optimize
            performance in real-time.""",
            verbose=True,
            tools=[BizoholicAgentTool()],
            memory=True
        )
        
        analytics_agent = Agent(
            role='Marketing Analytics Expert',
            goal='Analyze marketing performance and provide actionable insights',
            backstory="""You are a data analytics expert specialized in marketing metrics.
            You excel at identifying patterns, trends, and optimization opportunities
            from campaign data.""",
            verbose=True,
            tools=[BizoholicAgentTool()],
            memory=True
        )
        
        # Create marketing strategy crew
        strategy_crew = Crew(
            agents=[strategy_agent, campaign_agent, analytics_agent],
            verbose=True,
            process=Process.sequential
        )
        
        self.active_crews["bizoholic"]["marketing_strategy"] = strategy_crew
        
        # Content Generation Crew
        content_strategist = Agent(
            role='Content Strategy Lead',
            goal='Develop content strategies that drive engagement and conversions',
            backstory="""You are a content strategy expert who understands how to create
            compelling content that resonates with target audiences and drives business results.""",
            verbose=True,
            allow_delegation=True,
            tools=[BizoholicAgentTool()],
            memory=True
        )
        
        copywriter = Agent(
            role='Senior Copywriter',
            goal='Create compelling copy for various marketing channels and formats',
            backstory="""You are a master copywriter with expertise in direct response
            marketing, brand storytelling, and conversion optimization across all channels.""",
            verbose=True,
            tools=[BizoholicAgentTool()],
            memory=True
        )
        
        content_crew = Crew(
            agents=[content_strategist, copywriter],
            verbose=True,
            process=Process.hierarchical,
            manager_agent=content_strategist
        )
        
        self.active_crews["bizoholic"]["content_generation"] = content_crew
    
    async def _create_coreldove_crews(self):
        """Create specialized crews for CoreLDove e-commerce optimization"""
        # E-commerce Optimization Crew
        ecommerce_strategist = Agent(
            role='E-commerce Optimization Director',
            goal='Optimize e-commerce operations for maximum profitability and efficiency',
            backstory="""You are an e-commerce optimization expert with deep experience
            in online retail, conversion optimization, and customer experience design.""",
            verbose=True,
            allow_delegation=True,
            tools=[CoreLDoveAgentTool()],
            memory=True
        )
        
        product_manager = Agent(
            role='Product Optimization Specialist',
            goal='Optimize product listings, pricing, and positioning for better performance',
            backstory="""You are a product management expert specialized in e-commerce
            optimization. You excel at improving product visibility, conversion rates, and profitability.""",
            verbose=True,
            tools=[CoreLDoveAgentTool()],
            memory=True
        )
        
        customer_experience_agent = Agent(
            role='Customer Experience Optimizer',
            goal='Optimize customer journey and experience for higher satisfaction and retention',
            backstory="""You are a UX expert specialized in e-commerce customer journeys.
            You understand how to create seamless shopping experiences that convert and retain customers.""",
            verbose=True,
            tools=[CoreLDoveAgentTool()],
            memory=True
        )
        
        ecommerce_crew = Crew(
            agents=[ecommerce_strategist, product_manager, customer_experience_agent],
            verbose=True,
            process=Process.hierarchical,
            manager_agent=ecommerce_strategist
        )
        
        self.active_crews["coreldove"]["ecommerce_optimization"] = ecommerce_crew
        
        # Inventory Management Crew
        inventory_analyst = Agent(
            role='Inventory Analytics Expert',
            goal='Optimize inventory management through data-driven insights',
            backstory="""You are an inventory management expert who uses advanced analytics
            to optimize stock levels, reduce costs, and improve efficiency.""",
            verbose=True,
            tools=[CoreLDoveAgentTool()],
            memory=True
        )
        
        supply_chain_optimizer = Agent(
            role='Supply Chain Optimization Specialist',
            goal='Optimize supply chain operations for efficiency and cost reduction',
            backstory="""You are a supply chain expert who specializes in optimizing
            supplier relationships, logistics, and operational efficiency.""",
            verbose=True,
            tools=[CoreLDoveAgentTool()],
            memory=True
        )
        
        inventory_crew = Crew(
            agents=[inventory_analyst, supply_chain_optimizer],
            verbose=True,
            process=Process.sequential
        )
        
        self.active_crews["coreldove"]["inventory_management"] = inventory_crew
    
    async def _create_thrillring_crews(self):
        """Create specialized crews for ThrillRing event management"""
        # Event Planning Crew
        event_coordinator = Agent(
            role='Event Coordination Director',
            goal='Plan and coordinate successful events with maximum engagement',
            backstory="""You are an experienced event coordinator who excels at planning
            and executing events that create memorable experiences and achieve business objectives.""",
            verbose=True,
            allow_delegation=True,
            memory=True
        )
        
        engagement_specialist = Agent(
            role='Engagement Optimization Specialist',
            goal='Maximize attendee engagement and participation in events',
            backstory="""You are an engagement expert who knows how to create interactive
            and compelling event experiences that keep attendees engaged and participating.""",
            verbose=True,
            memory=True
        )
        
        event_crew = Crew(
            agents=[event_coordinator, engagement_specialist],
            verbose=True,
            process=Process.sequential
        )
        
        self.active_crews["thrillring"]["event_planning"] = event_crew
    
    async def _create_quanttrade_crews(self):
        """Create specialized crews for QuantTrade financial analysis"""
        # Market Analysis Crew
        market_analyst = Agent(
            role='Senior Market Analyst',
            goal='Analyze market trends and identify trading opportunities',
            backstory="""You are a quantitative analyst with expertise in financial markets,
            technical analysis, and algorithmic trading strategies.""",
            verbose=True,
            memory=True
        )
        
        risk_manager = Agent(
            role='Risk Management Specialist',
            goal='Assess and manage trading risks for optimal portfolio performance',
            backstory="""You are a risk management expert who specializes in quantifying
            and mitigating financial risks in trading operations.""",
            verbose=True,
            memory=True
        )
        
        trading_crew = Crew(
            agents=[market_analyst, risk_manager],
            verbose=True,
            process=Process.sequential
        )
        
        self.active_crews["quanttrade"]["market_analysis"] = trading_crew
    
    async def _create_bizosaas_core_crews(self):
        """Create specialized crews for BizOSaaS core administration"""
        # System Administration Crew
        system_admin = Agent(
            role='System Administration Lead',
            goal='Maintain and optimize BizOSaaS platform operations',
            backstory="""You are a systems administrator expert who ensures the BizOSaaS
            platform runs efficiently, securely, and reliably for all tenants.""",
            verbose=True,
            memory=True
        )
        
        monitoring_specialist = Agent(
            role='Platform Monitoring Specialist',
            goal='Monitor platform health and performance across all services',
            backstory="""You are a monitoring expert who ensures all platform components
            are functioning optimally and proactively identifies potential issues.""",
            verbose=True,
            memory=True
        )
        
        admin_crew = Crew(
            agents=[system_admin, monitoring_specialist],
            verbose=True,
            process=Process.sequential
        )
        
        self.active_crews["bizosaas_core"]["system_administration"] = admin_crew
    
    async def execute_project_workflow(self, project_id: str, crew_name: str, 
                                     workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow for a specific project and crew"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        if project_id not in self.active_crews or crew_name not in self.active_crews[project_id]:
            raise ValueError(f"Crew {crew_name} not found in project {project_id}")
        
        crew = self.active_crews[project_id][crew_name]
        
        try:
            # Create tasks based on workflow configuration
            tasks = self._create_tasks_for_workflow(workflow_config, crew.agents)
            
            # Update crew with tasks
            crew.tasks = tasks
            
            # Execute crew workflow
            start_time = time.time()
            result = crew.kickoff()
            execution_time = time.time() - start_time
            
            # Track performance
            self._track_performance(project_id, crew_name, execution_time, True)
            
            return {
                "status": "success",
                "project_id": project_id,
                "crew_name": crew_name,
                "result": result,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._track_performance(project_id, crew_name, execution_time, False)
            
            logger.error(f"Workflow execution failed for {project_id}/{crew_name}: {e}")
            return {
                "status": "error",
                "project_id": project_id,
                "crew_name": crew_name,
                "error": str(e),
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat()
            }
    
    def _create_tasks_for_workflow(self, workflow_config: Dict[str, Any], 
                                 agents: List[Agent]) -> List[Task]:
        """Create tasks based on workflow configuration"""
        tasks = []
        
        for task_config in workflow_config.get("tasks", []):
            # Find appropriate agent for task
            agent = self._find_agent_for_task(task_config, agents)
            if not agent:
                agent = agents[0]  # Default to first agent
            
            task = Task(
                description=task_config.get("description", "Execute task"),
                agent=agent,
                expected_output=task_config.get("expected_output", "Task completion report")
            )
            
            tasks.append(task)
        
        return tasks
    
    def _find_agent_for_task(self, task_config: Dict[str, Any], 
                           agents: List[Agent]) -> Optional[Agent]:
        """Find the most appropriate agent for a task"""
        task_type = task_config.get("type", "general")
        
        # Simple matching based on agent role and task type
        for agent in agents:
            agent_role = agent.role.lower()
            if task_type.lower() in agent_role or any(
                keyword in agent_role for keyword in task_config.get("keywords", [])
            ):
                return agent
        
        return None
    
    def _track_performance(self, project_id: str, crew_name: str, 
                         execution_time: float, success: bool):
        """Track performance metrics for crews"""
        key = f"{project_id}_{crew_name}"
        
        if key not in self.performance_tracker:
            self.performance_tracker[key] = {
                "total_executions": 0,
                "successful_executions": 0,
                "total_execution_time": 0.0,
                "average_execution_time": 0.0,
                "success_rate": 0.0
            }
        
        metrics = self.performance_tracker[key]
        metrics["total_executions"] += 1
        metrics["total_execution_time"] += execution_time
        metrics["average_execution_time"] = (
            metrics["total_execution_time"] / metrics["total_executions"]
        )
        
        if success:
            metrics["successful_executions"] += 1
        
        metrics["success_rate"] = (
            metrics["successful_executions"] / metrics["total_executions"]
        )
    
    async def execute_cross_project_workflow(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflows that span multiple projects"""
        results = {}
        
        for project_config in workflow_config.get("projects", []):
            project_id = project_config["project_id"]
            crew_name = project_config["crew_name"]
            project_workflow = project_config["workflow"]
            
            try:
                result = await self.execute_project_workflow(
                    project_id, crew_name, project_workflow
                )
                results[f"{project_id}_{crew_name}"] = result
            except Exception as e:
                results[f"{project_id}_{crew_name}"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return {
            "status": "completed",
            "cross_project_results": results,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_project_status(self, project_id: str) -> Dict[str, Any]:
        """Get status information for a specific project"""
        if project_id not in self.projects:
            return {"error": f"Project {project_id} not found"}
        
        project = self.projects[project_id]
        project_crews = self.active_crews.get(project_id, {})
        
        # Calculate performance metrics
        project_performance = {}
        for crew_name in project_crews.keys():
            key = f"{project_id}_{crew_name}"
            if key in self.performance_tracker:
                project_performance[crew_name] = self.performance_tracker[key]
        
        return {
            "project_id": project_id,
            "project_type": project.project_type.value,
            "business_domain": project.business_domain.value,
            "active_crews": list(project_crews.keys()),
            "resource_allocation": project.resource_allocation,
            "performance_metrics": project_performance,
            "integration_status": self._check_integration_status(project)
        }
    
    def _check_integration_status(self, project: ProjectConfiguration) -> Dict[str, str]:
        """Check integration status for project endpoints"""
        status = {}
        
        for endpoint_name, endpoint_url in project.integration_endpoints.items():
            # In a real implementation, this would actually check endpoint health
            status[endpoint_name] = "healthy"  # Placeholder
        
        return status
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Get overview of the entire multi-project system"""
        overview = {
            "total_projects": len(self.projects),
            "active_crews": sum(len(crews) for crews in self.active_crews.values()),
            "project_breakdown": {},
            "overall_performance": self._calculate_overall_performance(),
            "resource_utilization": self._calculate_resource_utilization(),
            "system_health": self._assess_system_health()
        }
        
        # Add project breakdown
        for project_id, project in self.projects.items():
            overview["project_breakdown"][project_id] = {
                "type": project.project_type.value,
                "domain": project.business_domain.value,
                "crews": len(self.active_crews.get(project_id, {})),
                "priority": project.resource_allocation.get("priority", "medium")
            }
        
        return overview
    
    def _calculate_overall_performance(self) -> Dict[str, float]:
        """Calculate overall system performance metrics"""
        if not self.performance_tracker:
            return {"success_rate": 0.0, "average_execution_time": 0.0}
        
        total_executions = sum(m["total_executions"] for m in self.performance_tracker.values())
        total_successful = sum(m["successful_executions"] for m in self.performance_tracker.values())
        total_time = sum(m["total_execution_time"] for m in self.performance_tracker.values())
        
        return {
            "success_rate": total_successful / total_executions if total_executions > 0 else 0.0,
            "average_execution_time": total_time / total_executions if total_executions > 0 else 0.0,
            "total_workflows_executed": total_executions
        }
    
    def _calculate_resource_utilization(self) -> Dict[str, float]:
        """Calculate current resource utilization"""
        total_cpu = sum(p.resource_allocation.get("cpu", 0) for p in self.projects.values())
        total_memory = sum(p.resource_allocation.get("memory", 0) for p in self.projects.values())
        
        return {
            "cpu_utilization": min(100.0, total_cpu * 100),
            "memory_utilization": min(100.0, total_memory * 100),
            "resource_efficiency": self._calculate_resource_efficiency()
        }
    
    def _calculate_resource_efficiency(self) -> float:
        """Calculate resource efficiency score"""
        # This would be more sophisticated in a real implementation
        performance = self._calculate_overall_performance()
        return performance.get("success_rate", 0.0) * 100
    
    def _assess_system_health(self) -> str:
        """Assess overall system health"""
        performance = self._calculate_overall_performance()
        
        if performance.get("success_rate", 0) > 0.9:
            return "excellent"
        elif performance.get("success_rate", 0) > 0.8:
            return "good"
        elif performance.get("success_rate", 0) > 0.7:
            return "fair"
        else:
            return "needs_attention"


# Global multi-project manager instance
_multi_project_manager: Optional[MultiProjectAgentManager] = None


async def get_multi_project_manager() -> MultiProjectAgentManager:
    """Get or create the global multi-project manager"""
    global _multi_project_manager
    
    if _multi_project_manager is None:
        _multi_project_manager = MultiProjectAgentManager()
        await _multi_project_manager.initialize()
    
    return _multi_project_manager


# Example usage
async def main():
    """Example usage of the multi-project agent manager"""
    # Initialize manager
    manager = await get_multi_project_manager()
    
    # Execute Bizoholic marketing workflow
    bizoholic_workflow = {
        "tasks": [
            {
                "type": "campaign_strategy",
                "description": "Generate comprehensive marketing strategy for new client",
                "keywords": ["strategy", "marketing", "campaign"],
                "expected_output": "Complete marketing strategy document"
            },
            {
                "type": "content_generation", 
                "description": "Create marketing content for social media campaigns",
                "keywords": ["content", "copywriter", "creative"],
                "expected_output": "Social media content package"
            }
        ]
    }
    
    result = await manager.execute_project_workflow(
        "bizoholic", 
        "marketing_strategy", 
        bizoholic_workflow
    )
    
    print(f"Bizoholic workflow result: {result['status']}")
    
    # Execute CoreLDove e-commerce optimization
    coreldove_workflow = {
        "tasks": [
            {
                "type": "product_optimization",
                "description": "Optimize product listings for better conversion",
                "keywords": ["product", "optimization", "ecommerce"],
                "expected_output": "Product optimization recommendations"
            }
        ]
    }
    
    result = await manager.execute_project_workflow(
        "coreldove",
        "ecommerce_optimization", 
        coreldove_workflow
    )
    
    print(f"CoreLDove workflow result: {result['status']}")
    
    # Get system overview
    overview = manager.get_system_overview()
    print(f"System overview: {json.dumps(overview, indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())
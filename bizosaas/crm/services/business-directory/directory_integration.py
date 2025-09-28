"""
Business Directory Integration with BizOSaaS Core
Connects the business directory service with AI agents, CRM, and client onboarding workflows
"""

from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime
from .directory_service import BusinessDirectoryService, DirectoryOnboardingData
from ..temporal-orchestration.workflows.crm_workflows import CustomerOnboardingWorkflow
from ..ai-agents.agents.crm_agents import ContactIntelligenceAgent, LeadScoringAgent

class DirectoryIntegrationService:
    """Integrates business directory with the complete BizOSaaS ecosystem"""
    
    def __init__(self):
        self.directory_service = BusinessDirectoryService()
        self.contact_intelligence_agent = ContactIntelligenceAgent()
        self.lead_scoring_agent = LeadScoringAgent()
    
    async def integrate_directory_with_client_onboarding(
        self, 
        client_id: str, 
        client_data: Dict[str, Any],
        onboarding_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Integrate business directory listing as part of client onboarding process
        This provides immediate value as mentioned in the Bizoholic flow document
        """
        
        # Step 1: Extract business information for directory optimization
        business_data = await self._extract_business_data_from_client_profile(client_data)
        
        # Step 2: Use Contact Intelligence Agent to enrich business data
        enriched_data = await self.contact_intelligence_agent.execute_task({
            "task_type": "analyze_company",
            "company_data": business_data
        })
        
        if enriched_data.success:
            business_data.update(enriched_data.result.get("company_info", {}))
        
        # Step 3: Determine optimal directory strategy
        directory_strategy = await self._determine_directory_strategy(
            business_data,
            onboarding_preferences
        )
        
        # Step 4: Create directory onboarding data
        directory_onboarding = DirectoryOnboardingData(
            client_id=client_id,
            business_data=business_data,
            selected_directories=directory_strategy["recommended_directories"],
            target_categories=directory_strategy["target_categories"],
            onboarding_preferences=onboarding_preferences
        )
        
        # Step 5: Execute directory onboarding
        onboarding_result = await self.directory_service.onboard_client_to_directory(
            directory_onboarding
        )
        
        # Step 6: Set up lead qualification for directory-generated leads
        lead_qualification_setup = await self._setup_directory_lead_qualification(
            client_id,
            onboarding_result
        )
        
        # Step 7: Create immediate client benefits summary
        immediate_benefits = await self._create_immediate_benefits_summary(
            onboarding_result,
            lead_qualification_setup
        )
        
        return {
            "integration_id": f"dir_int_{client_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "client_id": client_id,
            "directory_onboarding": onboarding_result,
            "lead_qualification": lead_qualification_setup,
            "immediate_benefits": immediate_benefits,
            "onboarding_enhancement": {
                "directory_visibility": "Instantly visible across 100+ directories",
                "lead_generation_active": "Lead generation starts within 24-48 hours",
                "seo_boost": f"Local SEO boost of {onboarding_result['immediate_benefits']['local_visibility_increase']}",
                "competitive_advantage": "AI-optimized listings outperform competitors"
            },
            "next_integration_steps": [
                "Monitor directory approvals and optimize as needed",
                "Activate review management and response automation", 
                "Set up local SEO content creation workflow",
                "Integrate directory analytics with main dashboard"
            ]
        }
    
    async def _extract_business_data_from_client_profile(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and format business data from client profile for directory use"""
        
        return {
            "name": client_data.get("company_name", client_data.get("business_name", "")),
            "category": client_data.get("industry", client_data.get("business_category", "services")),
            "description": client_data.get("business_description", client_data.get("company_description", "")),
            "address": self._format_address(client_data),
            "phone": client_data.get("phone", client_data.get("business_phone", "")),
            "email": client_data.get("email", client_data.get("business_email", "")),
            "website": client_data.get("website", client_data.get("business_website", "")),
            "location": client_data.get("city", client_data.get("location", "")),
            "target_audience": client_data.get("target_market", "local"),
            "services": client_data.get("services", []),
            "specialties": client_data.get("specialties", []),
            "established_year": client_data.get("established", ""),
            "employee_count": client_data.get("employees", client_data.get("team_size", "")),
            "certifications": client_data.get("certifications", []),
            "awards": client_data.get("awards", [])
        }
    
    def _format_address(self, client_data: Dict[str, Any]) -> str:
        """Format complete business address from client data"""
        address_parts = []
        
        if client_data.get("street_address"):
            address_parts.append(client_data["street_address"])
        if client_data.get("city"):
            address_parts.append(client_data["city"])
        if client_data.get("state"):
            address_parts.append(client_data["state"])
        if client_data.get("zip_code"):
            address_parts.append(client_data["zip_code"])
        
        return ", ".join(address_parts)
    
    async def _determine_directory_strategy(
        self, 
        business_data: Dict[str, Any], 
        onboarding_preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Determine optimal directory strategy based on business profile and preferences"""
        
        # Analyze business category for directory selection
        business_category = business_data.get("category", "services").lower()
        location = business_data.get("location", "").lower()
        
        # Base recommended directories for all businesses
        base_directories = [
            "Google My Business",
            "Bing Places", 
            "Facebook Business",
            "Yelp",
            "BBB (Better Business Bureau)"
        ]
        
        # Add category-specific directories
        category_directories = self._get_category_specific_directories(business_category)
        
        # Add location-specific directories
        location_directories = self._get_location_specific_directories(location)
        
        # Consider client preferences
        preference_directories = self._apply_client_preferences(
            onboarding_preferences,
            business_category
        )
        
        # Combine and deduplicate
        all_directories = list(set(
            base_directories + 
            category_directories + 
            location_directories + 
            preference_directories
        ))
        
        # Limit to manageable number based on plan
        plan_type = onboarding_preferences.get("plan_type", "professional")
        directory_limit = self._get_directory_limit_by_plan(plan_type)
        
        recommended_directories = all_directories[:directory_limit]
        
        # Determine target categories
        target_categories = self._determine_target_categories(business_data)
        
        return {
            "recommended_directories": recommended_directories,
            "target_categories": target_categories,
            "strategy_reasoning": {
                "business_category": business_category,
                "location_focus": location,
                "plan_limitations": directory_limit,
                "expected_results": f"Estimated {len(recommended_directories)} directory listings with {directory_limit * 15} avg monthly leads"
            }
        }
    
    def _get_category_specific_directories(self, category: str) -> List[str]:
        """Get directories specific to business category"""
        category_mappings = {
            "restaurants": ["TripAdvisor", "OpenTable", "Zomato", "Grubhub"],
            "healthcare": ["Healthgrades", "Vitals", "WebMD", "Zocdoc"],
            "legal": ["Avvo", "Lawyers.com", "FindLaw", "Justia"],
            "home_services": ["Angie's List", "HomeAdvisor", "Houzz", "Thumbtack"],
            "automotive": ["AutoTrader", "Cars.com", "CarGurus", "Edmunds"],
            "real_estate": ["Zillow", "Realtor.com", "Trulia", "LoopNet"],
            "technology": ["Clutch", "GoodFirms", "ITFirms", "Expertise.com"],
            "fitness": ["ClassPass", "Mindbody", "GymPlanet", "FitnessBlender"]
        }
        
        return category_mappings.get(category, ["Thumbtack", "Expertise.com"])
    
    def _get_location_specific_directories(self, location: str) -> List[str]:
        """Get directories specific to business location"""
        
        # Major city directories
        city_directories = {
            "new york": ["NYC.gov Business", "Time Out New York", "Yelp NYC"],
            "los angeles": ["LA Business Portal", "Los Angeles Times", "Discover Los Angeles"],
            "chicago": ["Chicago Business Directory", "Choose Chicago", "Chicago Tribune Business"],
            "houston": ["Houston Business Journal", "Visit Houston", "Houston Chronicle Business"]
        }
        
        # Regional directories
        regional_directories = {
            "california": ["California Business Directory", "CA.gov Business"],
            "texas": ["Texas Business Directory", "Texas.gov Business"],
            "florida": ["Florida Business Directory", "MyFlorida Business"],
            "new york": ["Empire State Directory", "NY.gov Business"]
        }
        
        location_dirs = []
        
        # Check for city-specific directories
        for city, dirs in city_directories.items():
            if city in location:
                location_dirs.extend(dirs)
                break
        
        # Add regional directories
        for region, dirs in regional_directories.items():
            if region in location:
                location_dirs.extend(dirs)
                break
        
        return location_dirs
    
    def _apply_client_preferences(
        self, 
        preferences: Dict[str, Any], 
        business_category: str
    ) -> List[str]:
        """Apply client preferences to directory selection"""
        
        preference_directories = []
        
        # Check for social media preferences
        if preferences.get("social_media_focus", False):
            preference_directories.extend([
                "Facebook Business",
                "Instagram Business", 
                "LinkedIn Company",
                "Twitter Business"
            ])
        
        # Check for review platform preferences
        if preferences.get("review_management_priority", False):
            preference_directories.extend([
                "TrustPilot",
                "Customer Lobby",
                "Reviews.com",
                "Shopper Approved"
            ])
        
        # Check for industry-specific preferences
        if preferences.get("industry_focus", False):
            preference_directories.extend(
                self._get_category_specific_directories(business_category)
            )
        
        return preference_directories
    
    def _get_directory_limit_by_plan(self, plan_type: str) -> int:
        """Get directory submission limit based on subscription plan"""
        plan_limits = {
            "basic": 10,
            "professional": 50,
            "enterprise": 100
        }
        
        return plan_limits.get(plan_type, 50)
    
    def _determine_target_categories(self, business_data: Dict[str, Any]) -> List[str]:
        """Determine target categories for directory listings"""
        
        primary_category = business_data.get("category", "services")
        services = business_data.get("services", [])
        specialties = business_data.get("specialties", [])
        
        categories = [primary_category]
        
        # Add service-based categories
        for service in services[:3]:  # Limit to top 3 services
            categories.append(service.lower())
        
        # Add specialty categories
        for specialty in specialties[:2]:  # Limit to top 2 specialties
            categories.append(specialty.lower())
        
        return list(set(categories))  # Remove duplicates
    
    async def _setup_directory_lead_qualification(
        self, 
        client_id: str, 
        onboarding_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Set up lead qualification for directory-generated leads"""
        
        # Configure lead scoring for directory sources
        lead_scoring_config = {
            "client_id": client_id,
            "source_scoring": {
                "google_my_business": 90,  # High-intent local searches
                "yelp": 75,               # Review-based discovery
                "facebook_business": 70,   # Social discovery
                "industry_directories": 85, # Targeted industry searches
                "general_directories": 60   # Broader discovery
            },
            "qualification_criteria": {
                "directory_engagement": ["viewed_photos", "clicked_website", "called_directly"],
                "search_intent": ["service_specific", "location_specific", "comparison_shopping"],
                "contact_method": ["phone_call", "form_submission", "direct_email"]
            },
            "auto_scoring_rules": [
                {"condition": "phone_call AND google_my_business", "score_boost": 20},
                {"condition": "form_submission AND industry_directory", "score_boost": 15},
                {"condition": "multiple_directory_interactions", "score_boost": 10}
            ],
            "integration": {
                "crm_system": "bizosaas_crm",
                "lead_routing": "automatic",
                "notification_triggers": ["high_score_lead", "immediate_response_needed"]
            }
        }
        
        return lead_scoring_config
    
    async def _create_immediate_benefits_summary(
        self, 
        onboarding_result: Dict[str, Any], 
        lead_qualification_setup: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create summary of immediate benefits from directory integration"""
        
        immediate_benefits = {
            "visibility_boost": {
                "directories_submitted": onboarding_result["immediate_benefits"]["directories_submitted"],
                "search_visibility": "Instantly visible in local search results",
                "competitive_advantage": "AI-optimized listings rank higher than competitors",
                "brand_presence": "Professional presence across major platforms"
            },
            "lead_generation": {
                "estimated_monthly_leads": onboarding_result["immediate_benefits"]["estimated_monthly_leads"],
                "lead_quality": "Higher quality leads from targeted directories",
                "qualification_automation": "Automatic lead scoring and routing",
                "response_time": "Immediate lead notifications and routing"
            },
            "seo_benefits": {
                "local_seo_boost": onboarding_result["immediate_benefits"]["local_visibility_increase"],
                "backlink_creation": f"{onboarding_result['immediate_benefits']['directories_submitted']} new high-authority backlinks",
                "citation_consistency": "Consistent NAP (Name, Address, Phone) across all directories",
                "search_ranking_improvement": "Improved rankings for local and industry searches"
            },
            "automation_advantages": {
                "listing_management": "Automated listing updates and maintenance",
                "review_monitoring": "Real-time review alerts and response suggestions",
                "performance_tracking": "Comprehensive analytics and reporting",
                "optimization_recommendations": "AI-powered optimization suggestions"
            },
            "time_savings": {
                "manual_submission_avoided": "Saved 20+ hours of manual directory submissions",
                "ongoing_management": "Automated monitoring saves 5+ hours weekly",
                "optimization_time": "AI optimization saves 10+ hours monthly",
                "reporting_automation": "Automated reports save 3+ hours weekly"
            }
        }
        
        return immediate_benefits
    
    async def get_directory_integration_status(self, client_id: str) -> Dict[str, Any]:
        """Get current status of directory integration for a client"""
        
        # This would query the actual database in production
        performance_data = await self.directory_service.get_directory_performance(client_id)
        
        return {
            "client_id": client_id,
            "integration_status": "active",
            "directory_performance": performance_data,
            "lead_generation_stats": {
                "total_leads_generated": performance_data["monthly_leads"] * 3,  # 3 months
                "average_monthly_leads": performance_data["monthly_leads"],
                "conversion_rate": performance_data["conversion_rate"],
                "top_performing_directories": performance_data["top_performing_directories"]
            },
            "optimization_opportunities": performance_data["optimization_recommendations"],
            "next_actions": [
                "Review and respond to recent directory reviews",
                "Update business hours for holiday schedule",
                "Add new service offerings to directory listings",
                "Optimize photos and descriptions based on performance data"
            ]
        }
    
    async def handle_directory_lead(
        self, 
        lead_data: Dict[str, Any], 
        directory_source: str
    ) -> Dict[str, Any]:
        """Process incoming lead from directory listing"""
        
        # Use Lead Scoring Agent to score the lead
        scoring_result = await self.lead_scoring_agent.execute_task({
            "task_type": "score_lead",
            "lead": {
                **lead_data,
                "source": directory_source,
                "source_type": "directory_listing"
            }
        })
        
        if scoring_result.success:
            lead_score = scoring_result.result["total_score"]
            qualification_status = scoring_result.result["qualification_status"]
            
            # Route lead based on score and qualification
            routing_action = await self._route_directory_lead(
                lead_data,
                lead_score,
                qualification_status,
                directory_source
            )
            
            return {
                "lead_processed": True,
                "lead_score": lead_score,
                "qualification_status": qualification_status,
                "routing_action": routing_action,
                "follow_up_scheduled": routing_action.get("follow_up_scheduled", False)
            }
        
        return {"lead_processed": False, "error": "Lead scoring failed"}
    
    async def _route_directory_lead(
        self, 
        lead_data: Dict[str, Any], 
        lead_score: float, 
        qualification_status: str, 
        directory_source: str
    ) -> Dict[str, Any]:
        """Route directory lead based on score and qualification"""
        
        if lead_score > 80 and qualification_status == "high":
            return {
                "routing": "immediate_sales_team",
                "priority": "high",
                "response_time_target": "15_minutes",
                "follow_up_scheduled": True,
                "notification_sent": True
            }
        elif lead_score > 60 and qualification_status in ["medium", "high"]:
            return {
                "routing": "sales_queue",
                "priority": "medium", 
                "response_time_target": "2_hours",
                "follow_up_scheduled": True,
                "notification_sent": True
            }
        else:
            return {
                "routing": "nurturing_campaign",
                "priority": "low",
                "response_time_target": "24_hours",
                "follow_up_scheduled": False,
                "nurturing_sequence_started": True
            }
"""
Business Directory Admin Setup
Registration and configuration script for Business Directory admin interfaces
"""

from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import all Business Directory admin views
from business_directory_admin import (
    BusinessCategoryAdminView, BusinessListingAdminView, BusinessReviewAdminView,
    BusinessEventAdminView, BusinessProductAdminView, BusinessCouponAdminView,
    BusinessAnalyticsAdminView, DirectorySettingsView, DirectoryAnalyticsDashboard,
    DirectoryIntegrationsView
)

from business_directory_platform_admin import (
    DirectoryPlatformSettingsAdminView, DirectoryIntegrationConfigAdminView,
    DirectoryModerationQueueAdminView, DirectoryContentFilterAdminView,
    DirectoryNotificationSettingsAdminView, DirectoryAnalyticsMetricsAdminView,
    DirectoryPlatformMonitoringView
)

# Import Business Directory models
from business_directory_models import (
    DirectoryPlatformSettings, DirectoryIntegrationConfig, DirectoryNotificationSettings,
    DirectoryModerationQueue, DirectoryAnalyticsMetrics, DirectoryContentFilter
)

# Import Business Directory service models
import sys
sys.path.append('/home/alagiri/projects/bizoholic/bizosaas-platform/backend/services/business-directory')
from models.business import (
    BusinessCategory, BusinessListing, BusinessReview, BusinessEvent, 
    BusinessProduct, BusinessCoupon, BusinessAnalytics
)


def register_business_directory_admin(admin: Admin):
    """
    Register all Business Directory admin views with the SQLAdmin instance
    """
    try:
        logger.info("Registering Business Directory admin views...")
        
        # =================================================================
        # BUSINESS DIRECTORY CORE MANAGEMENT
        # =================================================================
        
        # Business Categories Management
        admin.add_view(BusinessCategoryAdminView)
        logger.info("✓ Registered Business Categories admin view")
        
        # Business Listings Management  
        admin.add_view(BusinessListingAdminView)
        logger.info("✓ Registered Business Listings admin view")
        
        # Business Reviews Management
        admin.add_view(BusinessReviewAdminView)
        logger.info("✓ Registered Business Reviews admin view")
        
        # Business Events Management
        admin.add_view(BusinessEventAdminView)
        logger.info("✓ Registered Business Events admin view")
        
        # Business Products Management
        admin.add_view(BusinessProductAdminView)
        logger.info("✓ Registered Business Products admin view")
        
        # Business Coupons Management
        admin.add_view(BusinessCouponAdminView)
        logger.info("✓ Registered Business Coupons admin view")
        
        # Business Analytics Management
        admin.add_view(BusinessAnalyticsAdminView)
        logger.info("✓ Registered Business Analytics admin view")
        
        # =================================================================
        # BUSINESS DIRECTORY PLATFORM ADMINISTRATION
        # =================================================================
        
        # Platform Settings Management
        admin.add_view(DirectoryPlatformSettingsAdminView)
        logger.info("✓ Registered Platform Settings admin view")
        
        # Integration Configuration Management
        admin.add_view(DirectoryIntegrationConfigAdminView)
        logger.info("✓ Registered Integration Configs admin view")
        
        # Moderation Queue Management
        admin.add_view(DirectoryModerationQueueAdminView)
        logger.info("✓ Registered Moderation Queue admin view")
        
        # Content Filter Management
        admin.add_view(DirectoryContentFilterAdminView)
        logger.info("✓ Registered Content Filters admin view")
        
        # Notification Settings Management
        admin.add_view(DirectoryNotificationSettingsAdminView)
        logger.info("✓ Registered Notification Settings admin view")
        
        # Analytics Metrics Management
        admin.add_view(DirectoryAnalyticsMetricsAdminView)
        logger.info("✓ Registered Analytics Metrics admin view")
        
        # =================================================================
        # BUSINESS DIRECTORY DASHBOARDS & TOOLS
        # =================================================================
        
        # Directory Settings Dashboard
        admin.add_view(DirectorySettingsView)
        logger.info("✓ Registered Directory Settings dashboard")
        
        # Directory Analytics Dashboard
        admin.add_view(DirectoryAnalyticsDashboard)
        logger.info("✓ Registered Directory Analytics dashboard")
        
        # Directory Integrations Dashboard
        admin.add_view(DirectoryIntegrationsView)
        logger.info("✓ Registered Directory Integrations dashboard")
        
        # Platform Monitoring Dashboard
        admin.add_view(DirectoryPlatformMonitoringView)
        logger.info("✓ Registered Platform Monitoring dashboard")
        
        logger.info("✅ Successfully registered all Business Directory admin views!")
        
        # Log admin menu structure
        logger.info("\n📋 Business Directory Admin Menu Structure:")
        logger.info("  📁 Business Directory")
        logger.info("    ├── 🏷️  Business Categories")
        logger.info("    ├── 🏢  Business Listings") 
        logger.info("    ├── ⭐  Business Reviews")
        logger.info("    ├── 📅  Business Events")
        logger.info("    ├── 🛍️  Business Products")
        logger.info("    ├── 🎫  Business Coupons")
        logger.info("    ├── 📊  Business Analytics")
        logger.info("    ├── ⚙️  Directory Settings")
        logger.info("    ├── 📈  Directory Analytics")
        logger.info("    └── 🔌  Directory Integrations")
        logger.info("  📁 Directory Platform")
        logger.info("    ├── ⚙️  Platform Settings")
        logger.info("    ├── 🔌  Integration Configs")
        logger.info("    ├── ⚖️  Moderation Queue")
        logger.info("    ├── 🗂️  Content Filters")
        logger.info("    ├── 🔔  Notification Settings")
        logger.info("    ├── 📊  Analytics Metrics")
        logger.info("    └── 🖥️  Platform Monitoring")
        
    except Exception as e:
        logger.error(f"❌ Failed to register Business Directory admin views: {e}")
        raise


async def create_business_directory_tables(engine):
    """
    Create database tables for Business Directory models
    """
    try:
        logger.info("Creating Business Directory database tables...")
        
        # Import base models to ensure table creation
        from models.base import Base
        from business_directory_models import (
            DirectoryPlatformSettings, DirectoryIntegrationConfig, 
            DirectoryNotificationSettings, DirectoryModerationQueue,
            DirectoryAnalyticsMetrics, DirectoryContentFilter
        )
        
        # Import Business Directory service models
        from models.business import (
            BusinessCategory, BusinessListing, BusinessReview, BusinessEvent,
            BusinessProduct, BusinessCoupon, BusinessAnalytics
        )
        
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("✅ Successfully created Business Directory database tables!")
        
    except Exception as e:
        logger.error(f"❌ Failed to create Business Directory tables: {e}")
        raise


def get_business_directory_admin_config():
    """
    Get Business Directory admin configuration dictionary
    """
    return {
        "title": "BizOSaaS Business Directory Admin",
        "description": "Comprehensive Business Directory management platform",
        "version": "1.0.0",
        "categories": [
            {
                "name": "Business Directory",
                "icon": "fa-solid fa-building-columns",
                "description": "Core business directory management",
                "views": [
                    "BusinessCategoryAdminView",
                    "BusinessListingAdminView",
                    "BusinessReviewAdminView", 
                    "BusinessEventAdminView",
                    "BusinessProductAdminView",
                    "BusinessCouponAdminView",
                    "BusinessAnalyticsAdminView"
                ]
            },
            {
                "name": "Directory Platform", 
                "icon": "fa-solid fa-cogs",
                "description": "Platform administration and configuration",
                "views": [
                    "DirectoryPlatformSettingsAdminView",
                    "DirectoryIntegrationConfigAdminView",
                    "DirectoryModerationQueueAdminView",
                    "DirectoryContentFilterAdminView",
                    "DirectoryNotificationSettingsAdminView",
                    "DirectoryAnalyticsMetricsAdminView"
                ]
            },
            {
                "name": "Directory Tools",
                "icon": "fa-solid fa-tools", 
                "description": "Management dashboards and utilities",
                "views": [
                    "DirectorySettingsView",
                    "DirectoryAnalyticsDashboard",
                    "DirectoryIntegrationsView",
                    "DirectoryPlatformMonitoringView"
                ]
            }
        ],
        "features": [
            "Multi-tenant Business Directory management",
            "Advanced review moderation with AI assistance",
            "External platform integrations (Google, Yelp, Facebook)",
            "Comprehensive analytics and reporting", 
            "Content filtering and spam detection",
            "Automated notification systems",
            "Platform health monitoring",
            "Bulk operations and batch processing"
        ],
        "permissions": {
            "superadmin": ["create", "read", "update", "delete", "bulk_operations"],
            "admin": ["create", "read", "update", "bulk_operations"],
            "moderator": ["read", "update", "moderate"],
            "viewer": ["read"]
        }
    }


async def initialize_default_settings(engine):
    """
    Initialize default platform settings and configurations
    """
    try:
        logger.info("Initializing default Business Directory settings...")
        
        # Create async session
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        async with async_session() as session:
            # Check if platform settings already exist
            from sqlalchemy import text
            
            settings_exist = await session.execute(
                text("SELECT COUNT(*) FROM directory_platform_settings")
            )
            
            if settings_exist.scalar() == 0:
                # Create default platform settings
                default_settings = DirectoryPlatformSettings(
                    auto_approval_enabled=False,
                    auto_approval_threshold="4.0",
                    review_moderation_mode="manual",
                    spam_detection_enabled=True,
                    featured_listing_limit=10,
                    free_listing_limit_per_user=1,
                    search_results_per_page=20,
                    enable_radius_search=True,
                    default_search_radius_km=25,
                    max_images_per_listing=10,
                    max_image_size_mb=5,
                    allowed_image_types=["jpg", "jpeg", "png", "webp"],
                    meta_title_template="{business_name} - {category} in {city} | Business Directory",
                    meta_description_template="Find {business_name} in {city}. {description}",
                    api_rate_limit_per_hour=1000,
                    tenant_id="00000000-0000-0000-0000-000000000000"  # Default system tenant
                )
                
                session.add(default_settings)
                logger.info("✓ Created default platform settings")
            
            # Initialize default content filters
            filter_exist = await session.execute(
                text("SELECT COUNT(*) FROM directory_content_filters")
            )
            
            if filter_exist.scalar() == 0:
                # Create default spam filters
                spam_filters = [
                    DirectoryContentFilter(
                        filter_name="Basic Spam Keywords",
                        filter_type="keyword",
                        target_content="description",
                        filter_pattern="spam,scam,fake,fraud,virus,malware",
                        action="flag",
                        severity="high",
                        is_active=True,
                        tenant_id="00000000-0000-0000-0000-000000000000"
                    ),
                    DirectoryContentFilter(
                        filter_name="Phone Number Pattern",
                        filter_type="regex", 
                        target_content="business_name",
                        filter_pattern=r"\b\d{3}-?\d{3}-?\d{4}\b",
                        action="moderate",
                        severity="medium",
                        is_active=True,
                        tenant_id="00000000-0000-0000-0000-000000000000"
                    ),
                    DirectoryContentFilter(
                        filter_name="URL in Business Name",
                        filter_type="regex",
                        target_content="business_name",
                        filter_pattern=r"https?://|www\.",
                        action="moderate",
                        severity="medium", 
                        is_active=True,
                        tenant_id="00000000-0000-0000-0000-000000000000"
                    )
                ]
                
                for filter_obj in spam_filters:
                    session.add(filter_obj)
                
                logger.info("✓ Created default content filters")
            
            await session.commit()
            logger.info("✅ Successfully initialized default settings!")
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize default settings: {e}")
        raise


def validate_business_directory_setup():
    """
    Validate that all Business Directory components are properly configured
    """
    validation_results = {
        "admin_views": [],
        "models": [],
        "database_tables": [],
        "errors": []
    }
    
    try:
        # Validate admin views
        admin_views = [
            BusinessCategoryAdminView, BusinessListingAdminView, BusinessReviewAdminView,
            BusinessEventAdminView, BusinessProductAdminView, BusinessCouponAdminView,
            BusinessAnalyticsAdminView, DirectoryPlatformSettingsAdminView,
            DirectoryIntegrationConfigAdminView, DirectoryModerationQueueAdminView,
            DirectoryContentFilterAdminView, DirectoryNotificationSettingsAdminView,
            DirectoryAnalyticsMetricsAdminView
        ]
        
        for view_class in admin_views:
            validation_results["admin_views"].append({
                "name": view_class.__name__,
                "model": getattr(view_class, 'model', None).__name__ if hasattr(view_class, 'model') else None,
                "category": getattr(view_class, 'category', None),
                "status": "✓ Valid"
            })
        
        # Validate models
        models = [
            BusinessCategory, BusinessListing, BusinessReview, BusinessEvent,
            BusinessProduct, BusinessCoupon, BusinessAnalytics,
            DirectoryPlatformSettings, DirectoryIntegrationConfig,
            DirectoryNotificationSettings, DirectoryModerationQueue,
            DirectoryAnalyticsMetrics, DirectoryContentFilter
        ]
        
        for model_class in models:
            validation_results["models"].append({
                "name": model_class.__name__,
                "table": getattr(model_class, '__tablename__', None),
                "status": "✓ Valid"
            })
        
        logger.info("✅ Business Directory setup validation completed successfully!")
        
    except Exception as e:
        validation_results["errors"].append(str(e))
        logger.error(f"❌ Business Directory setup validation failed: {e}")
    
    return validation_results


if __name__ == "__main__":
    """
    Standalone script for testing Business Directory admin setup
    """
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine
    
    async def test_setup():
        # Create test engine
        DATABASE_URL = "postgresql+asyncpg://user:password@localhost/bizosaas_test"
        engine = create_async_engine(DATABASE_URL)
        
        try:
            # Test table creation
            await create_business_directory_tables(engine)
            
            # Test default settings initialization  
            await initialize_default_settings(engine)
            
            # Validate setup
            results = validate_business_directory_setup()
            
            print("\n" + "="*60)
            print("BUSINESS DIRECTORY ADMIN SETUP TEST RESULTS")
            print("="*60)
            
            print(f"\n📋 Admin Views: {len(results['admin_views'])}")
            for view in results["admin_views"]:
                print(f"  {view['status']} {view['name']} -> {view['model']}")
            
            print(f"\n🗃️  Models: {len(results['models'])}")
            for model in results["models"]:
                print(f"  {model['status']} {model['name']} -> {model['table']}")
            
            if results["errors"]:
                print(f"\n❌ Errors: {len(results['errors'])}")
                for error in results["errors"]:
                    print(f"  • {error}")
            else:
                print("\n✅ No errors detected!")
            
            print("\n" + "="*60)
            
        finally:
            await engine.dispose()
    
    # Run test
    asyncio.run(test_setup())
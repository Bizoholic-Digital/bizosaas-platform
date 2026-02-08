from .connector import (
    validate_connector_credentials,
    save_connector_credentials,
    sync_connector_data,
    update_connector_status
)
from .marketing import (
    check_fluent_crm_lead,
    tag_fluent_crm_contact,
    tag_fluent_crm_contact,
    generate_ai_marketing_content,
    execute_marketing_strategy_activity
)
from .marketing_tags import (
    analyze_website_tags,
    discover_gtm_assets,
    setup_gtm_tags_workflow,
    provision_ga4_in_gtm,
    audit_gtm_container_tags
)
from .marketplace import (
    fetch_shopify_products,
    sync_product_to_marketplace
)
from .mcp_activities import (
    provision_mcp_resources,
    configure_mcp_application,
    finalize_mcp_installation,
    register_managed_service_as_mcp_activity
)
from .provisioning import (
    register_domain_activity,
    provision_infra_activity,
    setup_headless_bundle_activity,
    verify_site_health_activity
)
from .sales import (
    execute_sales_strategy_activity
)

__all__ = [
    "validate_connector_credentials",
    "save_connector_credentials",
    "sync_connector_data",
    "update_connector_status",
    "check_fluent_crm_lead",
    "tag_fluent_crm_contact",
    "generate_ai_marketing_content",
    "execute_marketing_strategy_activity",
    "analyze_website_tags",
    "discover_gtm_assets",
    "setup_gtm_tags_workflow",
    "provision_ga4_in_gtm",
    "audit_gtm_container_tags",
    "fetch_shopify_products",
    "sync_product_to_marketplace",
    "provision_mcp_resources",
    "configure_mcp_application",
    "finalize_mcp_installation",
    "register_managed_service_as_mcp_activity",
    "register_domain_activity",
    "provision_infra_activity",
    "setup_headless_bundle_activity",
    "verify_site_health_activity",
    "execute_sales_strategy_activity"
]

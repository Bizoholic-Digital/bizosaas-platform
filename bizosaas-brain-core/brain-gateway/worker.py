import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker
from app.workflows.connector_setup import ConnectorSetupWorkflow, ConnectorSyncWorkflow
from app.workflows.marketing_workflow import LeadNurtureWorkflow, MarketingCampaignWorkflow
from app.workflows.strategic_marketing_workflow import StrategicMarketingWorkflow
from app.workflows.strategic_sales_workflow import StrategicSalesWorkflow
from app.workflows.gtm_workflow import GTMOnboardingWorkflow
from app.workflows.marketplace_sync import MarketplaceCatalogSyncWorkflow
from app.workflows.inventory_lock import MarketplaceInventoryLockWorkflow
from app.workflows.provisioning_workflow import ProvisionClientSiteWorkflow
from app.workflows.discovery_workflow import DiscoveryWorkflow, ContinuousImprovementWorkflow
from app.workflows.seo_workflow import RankTrackerWorkflow
from app.workflows.ecommerce_workflow import EcommerceSetupWorkflow
from app.workflows.reputation_workflow import ReputationManagementWorkflow
from app.workflows.reporting_workflow import ClientReportingWorkflow
from app.workflows.intel_workflow import CompetitorIntelWorkflow, LeadScoringWorkflow
from app.workflows.growth_workflow import SocialListeningWorkflow, TopicalClusterWorkflow
from app.workflows.infra_outreach_workflow import OutreachAutomationWorkflow, AutoSSLMaintenanceWorkflow
from app.activities import (
    validate_connector_credentials,
    save_connector_credentials,
    sync_connector_data,
    update_connector_status,
    check_fluent_crm_lead,
    tag_fluent_crm_contact,
    generate_ai_marketing_content,
    execute_marketing_strategy_activity,
    execute_sales_strategy_activity,
    analyze_website_tags,
    discover_gtm_assets,
    setup_gtm_tags_workflow,
    provision_ga4_in_gtm,
    audit_gtm_container_tags,
    fetch_shopify_products,
    sync_product_to_marketplace,
    register_domain_activity,
    provision_infra_activity,
    setup_headless_bundle_activity,
    verify_site_health_activity
)
from app.activities.discovery import run_discovery_cycle_activity
from app.activities.reputation import (
    fetch_latest_reviews_activity,
    process_reviews_and_draft_responses_activity,
    publish_review_responses_activity
)
from app.activities.reporting import (
    aggregate_performance_data_activity,
    generate_report_insights_activity,
    generate_pdf_report_activity,
    deliver_client_report_activity
)
from app.activities.intel import (
    scrape_competitor_data_activity,
    analyze_competitor_shifts_activity,
    trigger_intel_alert_activity,
    enrich_lead_data_activity,
    score_lead_activity,
    route_to_sales_activity
)
from app.activities.growth import (
    monitor_brand_mentions_activity,
    analyze_mentions_activity,
    draft_proactive_engagement_activity,
    research_topical_keywords_activity,
    cluster_keywords_activity,
    generate_topical_content_plan_activity
)
from app.activities.infra_outreach import (
    research_prospects_activity,
    draft_personalized_outreach_activity,
    deliver_outreach_messages_activity,
    check_ssl_expiry_activity,
    renew_ssl_certificate_activity,
    verify_ssl_propagation_activity
)
import app.connectors # Ensure connectors are registered

async def run_worker():
    import os
    import base64
    temporal_url = os.getenv("TEMPORAL_ADDRESS", "").strip() or os.getenv("TEMPORAL_HOST", "").strip() or "localhost:7233"
    
    # Check for file paths
    temporal_cert_path = os.getenv("TEMPORAL_MTLS_CERT")
    temporal_key_path = os.getenv("TEMPORAL_MTLS_KEY")
    
    # Check for direct content (Base64 encoded to avoid multiline env issues)
    temporal_cert_content_b64 = os.getenv("TEMPORAL_MTLS_CERT_CONTENT")
    temporal_key_content_b64 = os.getenv("TEMPORAL_MTLS_KEY_CONTENT")

    val_cert_data = None
    val_key_data = None

    if temporal_cert_content_b64 and temporal_key_content_b64:
        try:
            val_cert_data = base64.b64decode(temporal_cert_content_b64)
            val_key_data = base64.b64decode(temporal_key_content_b64)
        except Exception as e:
            print(f"Failed to decode base64 certs: {e}")
            val_cert_data = None
            val_key_data = None

    if not val_cert_data and temporal_cert_path and temporal_key_path:
        if os.path.exists(temporal_cert_path) and os.path.exists(temporal_key_path):
            with open(temporal_cert_path, "rb") as f:
                val_cert_data = f.read()
            with open(temporal_key_path, "rb") as f:
                val_key_data = f.read()

    namespace = os.getenv("TEMPORAL_NAMESPACE", "default").strip()
    if val_cert_data and val_key_data:
        client = await Client.connect(
            temporal_url, 
            namespace=namespace,
            tls=True,
            tls_client_cert_config={"client_cert": val_cert_data, "client_private_key": val_key_data}
        )
    else:
        client = await Client.connect(temporal_url, namespace=namespace)
    
    worker = Worker(
        client,
        task_queue="brain-tasks",
        workflows=[
            ConnectorSetupWorkflow, 
            ConnectorSyncWorkflow, 
            LeadNurtureWorkflow, 
            MarketingCampaignWorkflow,
            StrategicMarketingWorkflow, 
            StrategicSalesWorkflow, 
            GTMOnboardingWorkflow,
            MarketplaceCatalogSyncWorkflow,
            MarketplaceInventoryLockWorkflow,
            ProvisionClientSiteWorkflow,
            DiscoveryWorkflow,
            ContinuousImprovementWorkflow,
            RankTrackerWorkflow,
            EcommerceSetupWorkflow,
            ReputationManagementWorkflow,
            ClientReportingWorkflow,
            CompetitorIntelWorkflow,
            LeadScoringWorkflow,
            SocialListeningWorkflow,
            TopicalClusterWorkflow,
            OutreachAutomationWorkflow,
            AutoSSLMaintenanceWorkflow
        ],
        activities=[
            validate_connector_credentials,
            save_connector_credentials,
            sync_connector_data,
            update_connector_status,
            check_fluent_crm_lead,
            tag_fluent_crm_contact,
            generate_ai_marketing_content,
            execute_marketing_strategy_activity,
            execute_sales_strategy_activity,
            analyze_website_tags,
            discover_gtm_assets,
            setup_gtm_tags_workflow,
            provision_ga4_in_gtm,
            audit_gtm_container_tags,
            fetch_shopify_products,
            sync_product_to_marketplace,
            register_domain_activity,
            provision_infra_activity,
            setup_headless_bundle_activity,
            verify_site_health_activity,
            run_discovery_cycle_activity,
            fetch_latest_reviews_activity,
            process_reviews_and_draft_responses_activity,
            publish_review_responses_activity,
            aggregate_performance_data_activity,
            generate_report_insights_activity,
            generate_pdf_report_activity,
            deliver_client_report_activity,
            scrape_competitor_data_activity,
            analyze_competitor_shifts_activity,
            trigger_intel_alert_activity,
            enrich_lead_data_activity,
            score_lead_activity,
            route_to_sales_activity,
            monitor_brand_mentions_activity,
            analyze_mentions_activity,
            draft_proactive_engagement_activity,
            research_topical_keywords_activity,
            cluster_keywords_activity,
            generate_topical_content_plan_activity,
            research_prospects_activity,
            draft_personalized_outreach_activity,
            deliver_outreach_messages_activity,
            check_ssl_expiry_activity,
            renew_ssl_certificate_activity,
            verify_ssl_propagation_activity
        ],
    )
    
    logging.info("Starting Temporal Worker for Connectors...")
    await worker.run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_worker())

from datetime import timedelta
from temporalio import workflow
from typing import List, Dict, Any

# Import activities
with workflow.unsafe.imports_passed_through():
    from app.activities.wordpress_activities import WordPressActivities

@workflow.definition
class WordPressSetupWorkflow:
    """
    Orchestrates the setup of a WordPress environment:
    1. Provisioning (if needed)
    2. Connection validation
    3. Plugin installation (WooCommerce, FluentCRM, etc.)
    4. Sync initialization
    """
    
    @workflow.run
    async def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        tenant_id = data.get("tenant_id")
        site_url = data.get("site_url")
        plugins = data.get("plugins_to_install", [])
        
        results = {"steps": []}
        
        # Step 1: Provisioning (Skip if site_url provided)
        if not site_url:
            workflow.logger.info(f"Provisioning new WordPress site for {tenant_id}")
            provision_res = await workflow.execute_activity(
                WordPressActivities.provision_site,
                data,
                start_to_close_timeout=timedelta(minutes=10)
            )
            site_url = provision_res.get("site_url")
            results["steps"].append({"name": "Provisioning", "status": "COMPLETED", "result": provision_res})
        
        # Step 2: Connection Validation
        workflow.logger.info(f"Validating connection to {site_url}")
        validate_res = await workflow.execute_activity(
            WordPressActivities.validate_connection,
            {"tenant_id": tenant_id, "site_url": site_url},
            start_to_close_timeout=timedelta(minutes=2)
        )
        results["steps"].append({"name": "Connection Validation", "status": "COMPLETED"})
        
        # Step 3: Install Plugins
        for plugin in plugins:
            workflow.logger.info(f"Installing plugin: {plugin}")
            install_res = await workflow.execute_activity(
                WordPressActivities.install_plugin,
                {"tenant_id": tenant_id, "slug": plugin},
                start_to_close_timeout=timedelta(minutes=5)
            )
            results["steps"].append({"name": f"Install {plugin}", "status": "COMPLETED"})
            
        # Step 4: Final Sync
        workflow.logger.info(f"Starting initial sync for {tenant_id}")
        await workflow.execute_activity(
            WordPressActivities.initialize_sync,
            {"tenant_id": tenant_id},
            start_to_close_timeout=timedelta(minutes=5)
        )
        results["steps"].append({"name": "Initial Sync", "status": "COMPLETED"})
        
        return {
            "status": "COMPLETED",
            "site_url": site_url,
            "details": results
        }

from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any

with workflow.unsafe.imports_passed_through():
    from app.activities.provisioning import (
        register_domain_activity,
        provision_infra_activity,
        setup_headless_bundle_activity,
        verify_site_health_activity
    )
    from app.activities.mcp_activities import register_managed_service_as_mcp_activity

@workflow.defn
class ProvisionClientSiteWorkflow:
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates the creation of a new client site.
        """
        results = {
            "steps_completed": [],
            "status": "in_progress",
            "domain": params.get("domain")
        }
        
        # 1. Register Domain (if requested)
        if params.get("register_domain", True):
            domain_res = await workflow.execute_activity(
                register_domain_activity,
                params,
                start_to_close_timeout=timedelta(minutes=5),
            )
            if domain_res["status"] == "error":
                results["status"] = "failed"
                results["error"] = f"Domain registration failed: {domain_res['message']}"
                return results
            results["steps_completed"].append("domain_registration")
            results["domain_details"] = domain_res

        # 2. Provision Infrastructure (DB + Containers)
        infra_params = {
            **params,
            "plan_slug": params.get("plan_slug", "starter"),
            "provisioning_config": params.get("provisioning_config", {})
        }
        infra_res = await workflow.execute_activity(
            provision_infra_activity,
            infra_params,
            start_to_close_timeout=timedelta(minutes=10),
        )
        if infra_res["status"] == "error":
            results["status"] = "failed"
            results["error"] = f"Infrastructure provisioning failed: {infra_res.get('message')}"
            return results
        results["steps_completed"].append("infra_provisioning")
        results["infra_metadata"] = infra_res["infra_metadata"]

        # 3. Setup Headless Bundle (WP + Next.js wiring)
        setup_params = {
            **params, 
            "infra_metadata": infra_res["infra_metadata"],
            "plan_features": params.get("plan_features", []),
            "provisioning_config": params.get("provisioning_config", {})
        }
        setup_res = await workflow.execute_activity(
            setup_headless_bundle_activity,
            setup_params,
            start_to_close_timeout=timedelta(minutes=5),
        )
        if setup_res["status"] == "error":
            results["status"] = "failed"
            results["error"] = f"Site setup failed: {setup_res.get('message')}"
            return results
        results["steps_completed"].append("site_setup")
        results["urls"] = {
            "cms": setup_res["cms_url"],
            "frontend": setup_res["frontend_url"]
        }

        # 4. Register as MCP
        # This links the new site to the tenant's workspace so agents can use it immediately
        mcp_params = {
            **params,
            "infra_metadata": infra_res["infra_metadata"],
            "setup_data": setup_res
        }
        await workflow.execute_activity(
            register_managed_service_as_mcp_activity,
            mcp_params,
            start_to_close_timeout=timedelta(minutes=2),
        )
        results["steps_completed"].append("mcp_registration")

        # 5. Verify Health
        health_res = await workflow.execute_activity(
            verify_site_health_activity,
            params,
            start_to_close_timeout=timedelta(minutes=2),
        )
        results["health_check"] = health_res
        results["steps_completed"].append("verification")
        
        results["status"] = "completed"
        return results

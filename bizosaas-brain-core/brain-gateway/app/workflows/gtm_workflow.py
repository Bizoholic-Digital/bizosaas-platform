from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, List

# Activities are imported by the worker
# analyze_website_tags, discover_gtm_assets, setup_gtm_tags_workflow

@workflow.defn
class GTMOnboardingWorkflow:
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        GTM-First Onboarding Workflow:
        1. Analyze website to see if GTM/GA4/Pixels exist.
        2. If tokens available, discover accessible GTM accounts/containers.
        3. Determine best path (setup new vs analyze existing).
        4. Integrate identified properties.
        """
        website_url = params.get("website_url")
        google_access_token = params.get("google_access_token")
        tenant_id = params.get("tenant_id", "default")

        # 1. External Discovery: What is already on the site?
        site_analysis = await workflow.execute_activity(
            "analyze_website_tags",
            {"url": website_url},
            start_to_close_timeout=timedelta(seconds=20)
        )

        results = {
            "site_analysis": site_analysis,
            "actions_taken": []
        }

        # 2. Internal Discovery: What does the user own in Google?
        gtm_assets = {"status": "skipped"}
        if google_access_token:
            gtm_assets = await workflow.execute_activity(
                "discover_gtm_assets",
                {"access_token": google_access_token, "tenant_id": tenant_id},
                start_to_close_timeout=timedelta(seconds=30)
            )
            results["gtm_assets"] = gtm_assets

        # 3. Strategy Decision
        if site_analysis.get("gtm_detected"):
            # GTM exists. Check if it's one we have access to.
            gtm_id = site_analysis.get("gtm_id")
            found_in_assets = False
            if gtm_assets.get("status") == "success":
                for container in gtm_assets.get("containers", []):
                    if container["id"] == gtm_id:
                        found_in_assets = True
                        break
            
            if found_in_assets:
                results["strategy"] = "optimize_existing_gtm"
                # Here we would trigger an "Analysis" workflow to see what's inside
            else:
                results["strategy"] = "external_gtm_detected_limited_access"
        else:
            # GTM Missing. Priority is to set it up.
            results["strategy"] = "provision_new_gtm"
            if gtm_assets.get("status") == "success":
                # We have access to Google. We can try to create a container or use an existing empty one.
                # For now, we simulate a setup
                setup_results = await workflow.execute_activity(
                    "setup_gtm_tags_workflow",
                    {"container_id": "NEW-GTM-PROVISIONED", "tags": ["ga4", "ads", "fb_pixel"]},
                    start_to_close_timeout=timedelta(seconds=60)
                )
                results["setup_results"] = setup_results
                results["actions_taken"].append("provisioned_new_container")

        return {
            "status": "completed",
            "results": results,
            "tenant_id": tenant_id
        }

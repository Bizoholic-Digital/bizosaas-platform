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

        # 3. Strategy Decision & Execution
        if site_analysis.get("gtm_detected"):
            # Scenario B & C: GTM exists on site.
            gtm_id = site_analysis.get("gtm_id")
            results["actions_taken"].append(f"detected_existing_gtm_{gtm_id}")
            
            found_container = None
            if gtm_assets.get("status") == "success":
                for container in gtm_assets.get("containers", []):
                    if container["id"] == gtm_id:
                        found_container = container
                        break
            
            if found_container:
                results["strategy"] = "optimize_existing_gtm"
                # If GA4 is missing on site but we have access to GTM, let's provision it in GTM
                if not site_analysis.get("ga4_detected"):
                    # Provision GA4 in GTM
                    # For demo/real, we'd need a GA4 Measurement ID
                    measurement_id = params.get("ga4_measurement_id", "G-DEMO12345")
                    provision_res = await workflow.execute_activity(
                        "provision_ga4_in_gtm",
                        {
                            "access_token": google_access_token,
                            "workspace_path": found_container["workspacePath"],
                            "measurement_id": measurement_id
                        },
                        start_to_close_timeout=timedelta(seconds=30)
                    )
                    results["provision_res"] = provision_res
                    results["actions_taken"].append("provisioned_ga4_in_existing_gtm")

                # Perform Deep Audit of existing GTM
                audit_res = await workflow.execute_activity(
                    "audit_gtm_container_tags",
                    {
                        "access_token": google_access_token,
                        "workspace_path": found_container["workspacePath"]
                    },
                    start_to_close_timeout=timedelta(seconds=30)
                )
                results["audit"] = audit_res
                results["actions_taken"].append("audited_existing_gtm_tags")
            else:
                results["strategy"] = "external_gtm_unmanaged"
                results["message"] = "GTM detected on site but not found in your Google account. Please provide access or replace with our managed GTM."
        else:
            # Scenario A: Clean Slate or Hardcoded Tags (Migration)
            results["strategy"] = "provision_new_gtm_architecture"
            
            if gtm_assets.get("status") == "success" and gtm_assets.get("containers"):
                # Use first available container as target for migration/new setup
                target = gtm_assets["containers"][0]
                results["target_container"] = target["id"]
                
                # Provision everything needed in this container
                provision_res = await workflow.execute_activity(
                    "provision_ga4_in_gtm",
                    {
                        "access_token": google_access_token,
                        "workspace_path": target["workspacePath"],
                        "measurement_id": params.get("ga4_measurement_id", "G-NEW12345")
                    },
                    start_to_close_timeout=timedelta(seconds=30)
                )
                results["provision_res"] = provision_res
                results["actions_taken"].append("provisioned_new_gtm_architecture")
            else:
                results["strategy"] = "manual_setup_required"
                results["message"] = "No GTM containers found in your account. Please create one or grant permissions."

        return {
            "status": "completed",
            "results": results,
            "tenant_id": tenant_id
        }

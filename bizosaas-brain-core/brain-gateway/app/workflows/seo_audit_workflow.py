from datetime import timedelta
from temporalio import workflow
from typing import Dict, Any, List

# Import activity definitions by name string usage
# Actual imports handled in worker.py

@workflow.defn
class SiteAuditWorkflow:
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive Site Audit Workflow:
        1. Crawls the site structure.
        2. Runs Lighthouse audits (Performance, Accessibility, SEO).
        3. Analyzes on-page SEO quality via AI.
        4. Checks for broken links.
        5. Generates an actionable report.
        """
        tenant_id = params.get("tenant_id")
        url = params.get("url")
        max_pages = params.get("max_pages", 100)

        # 1. Crawl Site
        crawl_result = await workflow.execute_activity(
            "crawl_site_activity",
            args=[{"url": url, "max_pages": max_pages}],
            start_to_close_timeout=timedelta(minutes=10)
        )

        urls_to_audit = [p["url"] for p in crawl_result.get("pages", [])[:10]] # Limit to top 10 for lighthouse depth

        # 2. Lighthouse Audit (Parallel or Batch)
        lighthouse_result = await workflow.execute_activity(
            "run_lighthouse_audit_activity",
            args=[{"urls": urls_to_audit, "mobile": True}],
            start_to_close_timeout=timedelta(minutes=10)
        )

        # 3. On-Page Structure Analysis (AI)
        seo_analysis = await workflow.execute_activity(
            "analyze_onpage_seo_activity",
            args=[{"pages": crawl_result.get("pages", []), "tenant_id": tenant_id}],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # 4. Broken Link Check
        link_check = await workflow.execute_activity(
            "check_broken_links_activity",
            args=[{"url": url}],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # 5. Generate Report
        audit_data = {
            "crawl": crawl_result,
            "lighthouse": lighthouse_result,
            "onpage": seo_analysis,
            "links": link_check
        }

        final_report = await workflow.execute_activity(
            "generate_audit_report_activity",
            args=[{"audit_data": audit_data, "tenant_id": tenant_id}],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # 6. Store Results
        await workflow.execute_activity(
            "store_audit_results_activity",
            args=[{"tenant_id": tenant_id, "report": final_report}],
            start_to_close_timeout=timedelta(seconds=30)
        )

        # 7. Notify Tenant
        await workflow.execute_activity(
            "notify_tenant_activity",
            args=[{"tenant_id": tenant_id, "summary": "SEO Site Audit Completed"}],
            start_to_close_timeout=timedelta(seconds=30)
        )

        return {
            "status": "completed",
            "url": url,
            "pages_analyzed": len(urls_to_audit),
            "report_summary": final_report.get("summary", "Audit completed")
        }

@workflow.defn
class KeywordResearchWorkflow:
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-Driven Keyword Research Workflow:
        1. Fetch seeds.
        2. Expand via SERP/People Also Ask.
        3. Analyze metrics (Volume, CPC).
        4. Cluster by intent.
        """
        tenant_id = params.get("tenant_id")
        seed_keywords = params.get("seed_keywords", [])

        # 1. Fetch Seeds
        seeds = await workflow.execute_activity(
            "fetch_seed_keywords_activity",
            args=[{"tenant_id": tenant_id, "seed_keywords": seed_keywords}],
            start_to_close_timeout=timedelta(minutes=2)
        )

        # 2. Expand
        expanded = await workflow.execute_activity(
            "expand_keywords_via_serp_activity",
            args=[{"seeds": seeds}],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # 3. Analyze Metrics
        metrics = await workflow.execute_activity(
            "analyze_keyword_metrics_activity",
            args=[{"keywords": expanded}],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # 4. Cluster
        clusters = await workflow.execute_activity(
            "cluster_keywords_activity",
            args=[{"keywords_data": metrics}],
            start_to_close_timeout=timedelta(minutes=5)
        )

        return {
            "status": "completed",
            "keywords_found": len(metrics),
            "clusters": clusters
        }

@workflow.defn
class BacklinkMonitorWorkflow:
    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Backlink Monitoring Workflow.
        """
        tenant_id = params.get("tenant_id")
        domain = params.get("domain")

        # 1. Fetch Profile
        profile = await workflow.execute_activity(
            "fetch_backlink_profile_activity",
            args=[{"domain": domain}],
            start_to_close_timeout=timedelta(minutes=5)
        )

        # 2. Detect Changes
        diff = await workflow.execute_activity(
            "detect_new_lost_links_activity",
            args=[{"current_profile": profile, "tenant_id": tenant_id}],
            start_to_close_timeout=timedelta(minutes=2)
        )

        return {
            "status": "completed",
            "profile": profile,
            "changes": diff
        }

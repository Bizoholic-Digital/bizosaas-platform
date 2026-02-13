from temporalio import activity
from typing import Dict, Any, List, Optional
import logging
import httpx
import os
import json
from datetime import datetime
from urllib.parse import urlparse

from app.core.intelligence import call_ai_agent_with_rag

logger = logging.getLogger(__name__)

# --- Helper Functions --- (Consolidated in app.core.intelligence)

# --- Site Audit Activities ---

@activity.defn
async def crawl_site_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Crawl a website to map pages and structure."""
    url = params.get("url")
    max_pages = params.get("max_pages", 100)
    
    logger.info(f"Crawling site: {url} (max {max_pages} pages)")
    
    # Mocking crawl result for now
    # In production: Use scrapy or a library like `trafilatura` / `beautifulsoup`
    
    pages = [
        {"url": url, "title": "Home", "status": 200},
        {"url": f"{url}/about", "title": "About Us", "status": 200},
        {"url": f"{url}/services", "title": "Services", "status": 200},
        {"url": f"{url}/contact", "title": "Contact", "status": 200},
        {"url": f"{url}/blog", "title": "Blog", "status": 200},
        {"url": f"{url}/404-page", "title": "Not Found", "status": 404},
    ]
    
    return {
        "root_url": url,
        "pages_crawled": len(pages),
        "pages": pages,
        "status": "completed"
    }

@activity.defn
async def run_lighthouse_audit_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Run Google Lighthouse audit on key pages."""
    urls = params.get("urls", [])
    mobile = params.get("mobile", True)
    
    logger.info(f"Running Lighthouse audit for {len(urls)} pages")
    
    # In production: Use Google PageSpeed Insights API or a local lighthouse-ci container
    results = []
    for url in urls:
        # Mock scores
        results.append({
            "url": url,
            "performance": 85 if "blog" in url else 92,
            "accessibility": 90,
            "best_practices": 88,
            "seo": 95,
            "core_web_vitals": "pass"
        })
        
    return {"audits": results}

@activity.defn
async def analyze_onpage_seo_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze on-page SEO elements (meta tags, headers, content)."""
    pages = params.get("pages", [])
    tenant_id = params.get("tenant_id")
    
    # Helper to clean data for the agent
    clean_pages = [{"url": p["url"], "title": p["title"]} for p in pages]
    
    analysis = await call_ai_agent_with_rag(
        agent_type="seo_specialist",
        task_description="Analyze on-page SEO structure for these pages",
        payload={"pages": clean_pages},
        tenant_id=tenant_id
    )
    
    return analysis

@activity.defn
async def check_broken_links_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Check for broken internal and external links."""
    base_url = params.get("url")
    logger.info(f"Checking broken links for {base_url}")
    
    # Mock result
    broken = [
        {"source": f"{base_url}/blog", "target": "http://broken-external.com", "status": 404},
        {"source": f"{base_url}", "target": f"{base_url}/old-page", "status": 404}
    ]
    
    return {"broken_links_count": len(broken), "details": broken}

@activity.defn
async def generate_audit_report_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a comprehensive audit report with actionable insights."""
    audit_data = params.get("audit_data")
    tenant_id = params.get("tenant_id")
    
    report = await call_ai_agent_with_rag(
        agent_type="seo_specialist",
        task_description="Generate SEO Site Audit Report",
        payload={"audit_data": audit_data},
        tenant_id=tenant_id
    )
    
    return report

@activity.defn
async def store_audit_results_activity(params: Dict[str, Any]) -> bool:
    """Store audit results in the database."""
    tenant_id = params.get("tenant_id")
    report = params.get("report")
    
    # In production: write to postgres
    logger.info(f"Storing SEO audit report for tenant {tenant_id}")
    return True

@activity.defn
async def notify_tenant_activity(params: Dict[str, Any]) -> bool:
    """Notify tenant of completing audit."""
    tenant_id = params.get("tenant_id")
    summary = params.get("summary")
    
    logger.info(f"Notifying tenant {tenant_id}: {summary}")
    return True

# --- Keyword Research Activities ---

@activity.defn
async def fetch_seed_keywords_activity(params: Dict[str, Any]) -> List[str]:
    """Fetch seed keywords from tenant profile or input."""
    tenant_id = params.get("tenant_id")
    provided_seeds = params.get("seed_keywords", [])
    
    if provided_seeds:
        return provided_seeds
        
    # Fallback: fetch from DB/Profile
    return ["saas automation", "ai marketing", "workflow automation"]

@activity.defn
async def expand_keywords_via_serp_activity(params: Dict[str, Any]) -> List[str]:
    """Expand keywords using SERP 'People Also Ask' and related searches."""
    seeds = params.get("seeds", [])
    
    logger.info(f"Expanding keywords from seeds: {seeds}")
    
    # Mock SERP API call
    expanded = []
    for seed in seeds:
        expanded.append(seed)
        expanded.append(f"best {seed}")
        expanded.append(f"{seed} tools")
        expanded.append(f"how to do {seed}")
        
    return list(set(expanded))

@activity.defn
async def analyze_keyword_metrics_activity(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Fetch search volume, CPC, and difficulty metrics."""
    keywords = params.get("keywords", [])
    
    logger.info(f"Analyzing metrics for {len(keywords)} keywords")
    
    metrics = []
    for kw in keywords:
        metrics.append({
            "keyword": kw,
            "volume": 1000,
            "difficulty": 45,
            "cpc": 2.50
        })
    return metrics

@activity.defn
async def cluster_keywords_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Group keywords by search intent and topic."""
    keywords_data = params.get("keywords_data", [])
    
    clusters = await call_ai_agent_with_rag(
        agent_type="marketing_strategist", # or seo_specialist
        task_description="Cluster keywords by intent",
        payload={"keywords": keywords_data},
        tenant_id=params.get("tenant_id", "global") # Ensure tenant_id is passed if available
    )
    
    return clusters

# --- Backlink Monitor Activities ---

@activity.defn
async def fetch_backlink_profile_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch current backlink profile from provider."""
    domain = params.get("domain")
    
    logger.info(f"Fetching backlinks for {domain}")
    
    # Mock DataForSEO/Ahrefs response
    return {
        "total_backlinks": 150,
        "referring_domains": 45,
        "average_domain_authority": 35
    }

@activity.defn
async def detect_new_lost_links_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Compare current profile with previous to find new/lost links."""
    current = params.get("current_profile")
    tenant_id = params.get("tenant_id")
    
    # In production: load previous from DB
    
    return {
        "new_links": [],
        "lost_links": []
    }


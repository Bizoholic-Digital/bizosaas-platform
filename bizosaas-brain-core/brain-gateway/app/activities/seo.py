from temporalio import activity
from typing import Dict, Any, List, Optional
import logging
import httpx
import os
import json
from datetime import datetime
from urllib.parse import urlparse, urljoin

from app.core.intelligence import call_ai_agent_with_rag
from app.core.vault import get_config_val
from app.core.dataforseo_client import dataforseo_client
from app.core.backlink_monitor import backlink_monitor
from app.dependencies import get_db

logger = logging.getLogger(__name__)

# --- Site Audit Activities ---

@activity.defn
async def crawl_site_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Crawl a website to map pages and structure using BeautifulSoup."""
    url = params.get("url")
    max_pages = params.get("max_pages", 20)
    
    logger.info(f"Crawling site: {url} (max {max_pages} pages)")
    
    from bs4 import BeautifulSoup
    
    pages = []
    to_visit = [url]
    visited = set()
    
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        while to_visit and len(pages) < max_pages:
            current_url = to_visit.pop(0)
            if current_url in visited:
                continue
            
            visited.add(current_url)
            try:
                response = await client.get(current_url)
                if response.status_code != 200:
                    pages.append({"url": current_url, "status": response.status_code, "title": "Error"})
                    continue
                
                soup = BeautifulSoup(response.text, 'lxml')
                title = soup.title.string.strip() if soup.title else "No Title"
                pages.append({"url": current_url, "title": title, "status": 200})
                
                for a in soup.find_all('a', href=True):
                    next_url = urljoin(current_url, a['href'])
                    if urlparse(next_url).netloc == urlparse(url).netloc:
                        next_url = next_url.split('#')[0].rstrip('/')
                        if next_url not in visited and next_url not in to_visit:
                            to_visit.append(next_url)
                            
            except Exception as e:
                logger.error(f"Failed to crawl {current_url}: {str(e)}")
                pages.append({"url": current_url, "status": 500, "error": str(e)})

    return {
        "root_url": url,
        "pages_crawled": len(pages),
        "pages": pages,
        "status": "completed"
    }

@activity.defn
async def run_lighthouse_audit_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Run Google Lighthouse audit using PageSpeed Insights API."""
    urls = params.get("urls", [])
    strategy = "mobile" if params.get("mobile", True) else "desktop"
    api_key = get_config_val("PAGESPEED_API_KEY")
    
    if not api_key:
        logger.warning("PAGESPEED_API_KEY missing. Returning placeholders.")
        return {"audits": [{"url": u, "performance": 0, "error": "No API Key"} for u in urls]}

    results = []
    async with httpx.AsyncClient(timeout=60.0) as client:
        for url in urls:
            try:
                endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
                query_params = {
                    "url": url,
                    "key": api_key,
                    "strategy": strategy,
                    "category": ["performance", "accessibility", "best-practices", "seo"]
                }
                response = await client.get(endpoint, params=query_params)
                if response.status_code == 200:
                    data = response.json()
                    cats = data.get("lighthouseResult", {}).get("categories", {})
                    results.append({
                        "url": url,
                        "performance": int(cats.get("performance", {}).get("score", 0) * 100),
                        "accessibility": int(cats.get("accessibility", {}).get("score", 0) * 100),
                        "best_practices": int(cats.get("best-practices", {}).get("score", 0) * 100),
                        "seo": int(cats.get("seo", {}).get("score", 0) * 100),
                        "core_web_vitals": data.get("loadingExperience", {}).get("overall_category", "N/A")
                    })
                else:
                    results.append({"url": url, "error": response.status_code})
            except Exception as e:
                results.append({"url": url, "error": str(e)})
        
    return {"audits": results}

@activity.defn
async def analyze_onpage_seo_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze on-page SEO elements using LLM Specialist."""
    pages = params.get("pages", [])
    tenant_id = params.get("tenant_id")
    clean_pages = [{"url": p["url"], "title": p["title"]} for p in pages]
    
    return await call_ai_agent_with_rag(
        agent_type="seo_specialist",
        task_description="Analyze on-page SEO structure",
        payload={"pages": clean_pages},
        tenant_id=tenant_id
    )

@activity.defn
async def check_broken_links_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Check for broken links using parallel HEAD requests."""
    base_url = params.get("url")
    links_to_check = params.get("links", [])
    
    results = []
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        for link in links_to_check:
            try:
                resp = await client.head(link)
                if resp.status_code >= 400:
                    results.append({"url": link, "status": resp.status_code})
            except Exception:
                results.append({"url": link, "status": "failed"})
                
    return {"broken_links_count": len(results), "details": results}

@activity.defn
async def generate_audit_report_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Generate SEO Site Audit Report via AI."""
    return await call_ai_agent_with_rag(
        agent_type="seo_specialist",
        task_description="Generate SEO Site Audit Report",
        payload={"audit_data": params.get("audit_data")},
        tenant_id=params.get("tenant_id")
    )

@activity.defn
async def store_audit_results_activity(params: Dict[str, Any]) -> bool:
    logger.info(f"Storing audit for {params.get('tenant_id')}")
    return True

@activity.defn
async def run_onpage_audit_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Perform deep On-Page audit using DataforSEO."""
    target_url = params.get("target_url")
    max_pages = params.get("max_pages", 1)
    
    task_id = await dataforseo_client.post_on_page_task(target_url, max_pages)
    if not task_id:
        return {"status": "error", "message": "Failed to initiate on-page task"}
    
    return {"status": "initiated", "task_id": task_id, "source": "dataforseo"}

@activity.defn
async def fetch_onpage_results_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch results of a DataforSEO On-Page audit."""
    task_id = params.get("task_id")
    if not task_id:
        return {"status": "error", "message": "Missing task_id"}
    
    results = await dataforseo_client.get_on_page_results(task_id)
    return {"status": "completed", "results": results, "source": "dataforseo"}

# --- Keyword Research Activities ---

@activity.defn
async def fetch_seed_keywords_activity(params: Dict[str, Any]) -> List[str]:
    return params.get("seed_keywords") or ["saas automation", "ai marketing"]

@activity.defn
async def expand_keywords_via_serp_activity(params: Dict[str, Any]) -> List[str]:
    """Expand keywords using DataforSEO (Google Keywords for Keywords)."""
    seeds = params.get("seeds", [])
    if not seeds: return []
    
    suggestions = await dataforseo_client.get_keywords_suggestions(seeds)
    expanded = set(seeds)
    for item in suggestions:
        if "keyword" in item:
            expanded.add(item["keyword"])
    
    return list(expanded)

@activity.defn
async def analyze_keyword_metrics_activity(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Fetch search metrics using DataforSEO."""
    keywords = params.get("keywords", [])
    if not keywords: return []
    
    results = await dataforseo_client.get_keyword_data(keywords)
    formatted = []
    for item in results:
        formatted.append({
            "keyword": item.get("keyword"),
            "volume": item.get("search_volume", 0),
            "difficulty": item.get("competition_level", "medium"),
            "cpc": item.get("cpc", 0.0),
            "source": "dataforseo"
        })
    return formatted

@activity.defn
async def cluster_keywords_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    return await call_ai_agent_with_rag(
        agent_type="marketing_strategist",
        task_description="Cluster keywords by intent",
        payload={"keywords": params.get("keywords_data")},
        tenant_id=params.get("tenant_id")
    )

# --- Backlink Monitor Activities ---

@activity.defn
async def fetch_backlink_profile_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch backlink profile via DataforSEO and sync to DB."""
    domain = params.get("domain")
    tenant_id = params.get("tenant_id")
    if not domain: return {"total_backlinks": 0}
    
    # Update aggregate stats
    summary = await dataforseo_client.get_backlinks_summary(domain)
    
    # Synchronize with proprietary monitor (async)
    # Note: In a real temporal activity, we'd handle the DB session carefully.
    # For now, we'll return the summary and trigger sync.
    from app.dependencies import SessionLocal
    with SessionLocal() as db:
        await backlink_monitor.synchronize_backlinks(db, tenant_id, domain)
        report = backlink_monitor.get_links_report(db, tenant_id)

    return {
        "total_backlinks": summary.get("backlinks", 0),
        "referring_domains": summary.get("referring_domains", 0),
        "rank": summary.get("rank", 0),
        "new_links_tracked": report.get("new_30d", 0),
        "source": "dataforseo_proprietary"
    }

@activity.defn
async def detect_new_lost_links_activity(params: Dict[str, Any]) -> Dict[str, Any]:
    return {"new_links": [], "lost_links": []}

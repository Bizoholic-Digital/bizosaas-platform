import os
import httpx
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("link-checker")

SERVICES = {
    "CMS": os.getenv("CMS_URL", "http://cms:8002"),
    "CRM": os.getenv("CRM_URL", "http://crm:8003"),
    "AI_AGENTS": os.getenv("AI_AGENTS_URL", "http://ai-agents:8000"),
    "AUTH": os.getenv("AUTH_URL", "http://auth-service:8006"),
    "LOKI": os.getenv("LOKI_URL", "http://loki:3100"),
    "PROMETHEUS": os.getenv("PROMETHEUS_URL", "http://prometheus:9090"),
}

async def check_link(name, url):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5.0)
            if response.status_code < 400:
                logger.info(f"✅ {name}: {url} - {response.status_code}")
                return True
            else:
                logger.error(f"❌ {name}: {url} - {response.status_code}")
                return False
    except Exception as e:
        logger.error(f"❌ {name}: {url} - UNREACHABLE: {e}")
        return False

async def main():
    logger.info("Starting BizOSaaS Internal Link Checker...")
    tasks = [check_link(name, url) for name, url in SERVICES.items()]
    results = await asyncio.gather(*tasks)
    
    success_count = sum(1 for r in results if r)
    total_count = len(results)
    
    logger.info(f"Link Check Summary: {success_count}/{total_count} services reachable.")

if __name__ == "__main__":
    asyncio.run(main())

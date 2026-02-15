import sys
from unittest.mock import MagicMock
# Mock missing dependency
sys.modules["langcache"] = MagicMock()

import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from app.activities.intel import (
    google_search_activity, 
    web_scrape_activity, 
    analyze_research_activity,
    scrape_competitor_data_activity
)

@pytest.mark.asyncio
async def test_google_search_activity():
    with patch("app.activities.intel.MCPGateway") as MockGateway:
        mock_gateway = MockGateway.return_value
        mock_gateway.call_tool = AsyncMock(return_value={"results": [{"url": "http://example.com", "title": "Example"}]})
        
        with patch("app.activities.intel.SessionLocal") as MockSession:
            results = await google_search_activity("tenant1", "test topic")
            assert len(results) == 1
            assert results[0]["url"] == "http://example.com"
            mock_gateway.call_tool.assert_called_once()

@pytest.mark.asyncio
async def test_web_scrape_activity():
    with patch("app.activities.intel.MCPGateway") as MockGateway:
        mock_gateway = MockGateway.return_value
        mock_gateway.call_tool = AsyncMock(return_value={"content": "Scraped content"})
        
        with patch("app.activities.intel.SessionLocal") as MockSession:
            result = await web_scrape_activity("tenant1", "http://example.com")
            assert result["url"] == "http://example.com"
            assert result["content"] == "Scraped content"

@pytest.mark.asyncio
async def test_scrape_competitor_data_activity():
    with patch("app.activities.intel.MCPGateway") as MockGateway:
        mock_gateway = MockGateway.return_value
        mock_gateway.call_tool = AsyncMock(return_value={"content": "Competitor site content"})
        
        with patch("app.activities.intel.SessionLocal") as MockSession:
            results = await scrape_competitor_data_activity("tenant1", ["http://competitor.com"])
            assert len(results) == 1
            assert results[0]["site"] == "http://competitor.com"
            assert "Competitor site content" in results[0]["content"]

@pytest.mark.asyncio
async def test_analyze_research_activity():
    findings = [{"url": "http://example.com", "content": "Sample text"}]
    result = await analyze_research_activity("tenant1", findings)
    assert "Deep Research Report" in result["report"]
    assert "http://example.com" in result["report"]

if __name__ == "__main__":
    asyncio.run(test_google_search_activity())
    asyncio.run(test_web_scrape_activity())
    asyncio.run(test_scrape_competitor_data_activity())
    asyncio.run(test_analyze_research_activity())
    print("All Phase 5 activity tests passed!")

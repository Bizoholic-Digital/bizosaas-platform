#!/usr/bin/env python3
"""
Test script for Amazon Data Scraper
Tests real image and price extraction for verified ASINs
"""

import asyncio
import httpx
import json
from datetime import datetime

# Verified ASINs for testing
VERIFIED_ASINS = [
    "B0CR7G9V56",  # Bodyband Abs Roller
    "B0DX1QJFK4",  # Boldfit Yoga Mat
    "B0BLSQPPKT",  # Boldfit NBR Yoga Mat
    "B0FGYDCPRR",  # pTron Bassbuds Earbuds
    "B08D8J5BVR",  # Boldfit Resistance Band Red
    "B08H7XCSTS",  # Boldfit Resistance Band Purple
    "B0C4Q5HNMH",  # Noise Halo Plus Smartwatch
]

async def test_single_asin(asin: str):
    """Test scraping for a single ASIN"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"http://localhost:8080/scraper/test/{asin}")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}", "asin": asin}
        except Exception as e:
            return {"error": str(e), "asin": asin}

async def test_batch_asins():
    """Test batch scraping for all verified ASINs"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8080/scraper/batch-test",
                json=VERIFIED_ASINS,
                timeout=60.0
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

async def test_product_search():
    """Test product search with scraping integration"""
    async with httpx.AsyncClient() as client:
        try:
            search_request = {
                "query": "yoga mat",
                "limit": 3
            }
            response = await client.post(
                "http://localhost:8080/sourcing/search",
                json=search_request,
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

async def main():
    """Run all tests and generate report"""
    print("🧪 Testing Amazon Data Scraper Implementation")
    print("=" * 60)
    
    # Test 1: Single ASIN test
    print("\n1. Testing Single ASIN Scraping...")
    test_asin = "B0CR7G9V56"  # Bodyband Abs Roller
    single_result = await test_single_asin(test_asin)
    print(f"   ASIN {test_asin}:")
    print(f"   Success: {single_result.get('status', 'unknown')}")
    if 'scraped_data' in single_result:
        data = single_result['scraped_data']
        print(f"   Has Image: {bool(data.get('image_url'))}")
        print(f"   Has Price: {bool(data.get('price'))}")
        print(f"   Price: ₹{data.get('price', 'N/A')}")
        if data.get('image_url'):
            print(f"   Image URL: {data['image_url'][:80]}...")
    
    # Test 2: Batch testing
    print("\n2. Testing Batch ASIN Scraping...")
    batch_result = await test_batch_asins()
    if 'error' not in batch_result:
        print(f"   Total ASINs: {batch_result.get('total_asins', 0)}")
        print(f"   Successful Scrapes: {batch_result.get('successful_scrapes', 0)}")
        print(f"   Images Found: {batch_result.get('images_found', 0)}")
        print(f"   Prices Found: {batch_result.get('prices_found', 0)}")
        print(f"   Success Rate: {batch_result.get('success_rate', 0):.2%}")
        
        # Show detailed results for each ASIN
        print("\n   Detailed Results:")
        for result in batch_result.get('results', []):
            status = "✅" if result['success'] else "❌"
            img_status = "🖼️" if result['has_image'] else "📷"
            price_status = "💰" if result['has_price'] else "🚫"
            print(f"   {status} {result['asin']}: {img_status} {price_status} ₹{result.get('price', 'N/A')}")
    else:
        print(f"   Error: {batch_result['error']}")
    
    # Test 3: Integration with product search
    print("\n3. Testing Product Search Integration...")
    search_result = await test_product_search()
    if 'error' not in search_result and isinstance(search_result, list):
        print(f"   Products returned: {len(search_result)}")
        real_images = sum(1 for p in search_result if p.get('image_url') and not p['image_url'].startswith('/images/'))
        print(f"   Real Amazon images: {real_images}")
        print(f"   Real image rate: {real_images/len(search_result):.2%}")
        
        # Show sample products
        print("\n   Sample Products:")
        for i, product in enumerate(search_result[:3]):
            image_type = "Real" if product.get('image_url') and not product['image_url'].startswith('/images/') else "Placeholder"
            print(f"   {i+1}. {product.get('title', 'Unknown')[:50]}...")
            print(f"      Price: ₹{product.get('price', 'N/A')} | Image: {image_type}")
    else:
        print(f"   Error: {search_result.get('error', 'Unknown error')}")
    
    # Generate JSON report
    report = {
        "test_timestamp": datetime.now().isoformat(),
        "single_asin_test": single_result,
        "batch_test": batch_result,
        "search_integration_test": search_result,
        "summary": {
            "single_test_passed": single_result.get('status') == 'success',
            "batch_test_passed": batch_result.get('success_rate', 0) > 0,
            "search_integration_passed": isinstance(search_result, list) and len(search_result) > 0
        }
    }
    
    # Save report
    report_filename = f"scraper_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📊 Test Report saved to: {report_filename}")
    print("\n🎯 Summary:")
    print(f"   Single ASIN Test: {'✅ PASS' if report['summary']['single_test_passed'] else '❌ FAIL'}")
    print(f"   Batch Test: {'✅ PASS' if report['summary']['batch_test_passed'] else '❌ FAIL'}")
    print(f"   Search Integration: {'✅ PASS' if report['summary']['search_integration_passed'] else '❌ FAIL'}")

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Amazon India ASIN Validator and Testing Tool
Tests ASINs for accessibility, availability, and dropship eligibility
"""

import asyncio
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ASINTestResult:
    """Results from testing an ASIN"""
    asin: str
    status: str  # 'valid', 'invalid', 'unavailable', 'error'
    url: str
    title: Optional[str] = None
    price: Optional[str] = None
    availability: Optional[str] = None
    seller_name: Optional[str] = None
    seller_rating: Optional[str] = None
    prime_eligible: bool = False
    error_message: Optional[str] = None
    redirect_url: Optional[str] = None
    product_images: List[str] = None
    features: List[str] = None
    
    def __post_init__(self):
        if self.product_images is None:
            self.product_images = []
        if self.features is None:
            self.features = []

class AmazonASINValidator:
    """Amazon India ASIN validation and testing service"""
    
    def __init__(self):
        self.base_url = "https://www.amazon.in"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers=self.headers,
            follow_redirects=True
        )
    
    async def test_asin(self, asin: str) -> ASINTestResult:
        """Test a single ASIN for validity and availability"""
        
        url = f"{self.base_url}/dp/{asin}"
        result = ASINTestResult(asin=asin, status="error", url=url)
        
        try:
            logger.info(f"Testing ASIN: {asin}")
            
            response = await self.client.get(url)
            
            # Check for redirects or page not found
            if response.status_code == 404:
                result.status = "invalid"
                result.error_message = "Product page not found (404)"
                return result
            
            if response.status_code != 200:
                result.status = "error"
                result.error_message = f"HTTP {response.status_code}"
                return result
            
            # Check if redirected to search page (indicates invalid ASIN)
            if "/s?" in str(response.url) or "search" in str(response.url):
                result.status = "invalid"
                result.error_message = "ASIN redirected to search page"
                result.redirect_url = str(response.url)
                return result
            
            # Parse the page content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract product title
            title_selectors = [
                '#productTitle',
                '.product-title',
                '[data-automation-id="title"]',
                'h1.a-size-large'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    result.title = title_elem.get_text().strip()
                    break
            
            # Extract price
            price_selectors = [
                '.a-price-whole',
                '.a-price .a-offscreen',
                '.pricePerUnit',
                '[data-automation-id="price"]',
                '.a-price-symbol + .a-price-whole'
            ]
            
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    result.price = price_elem.get_text().strip()
                    break
            
            # Check availability
            availability_indicators = [
                "Currently unavailable",
                "Out of stock",
                "Temporarily out of stock",
                "This item is currently unavailable",
                "We don't know when or if this item will be back in stock"
            ]
            
            page_text = soup.get_text().lower()
            
            for indicator in availability_indicators:
                if indicator.lower() in page_text:
                    result.status = "unavailable"
                    result.availability = indicator
                    return result
            
            # Look for positive availability indicators
            if "in stock" in page_text or "add to cart" in page_text:
                result.availability = "In Stock"
            
            # Extract seller information
            seller_selectors = [
                '#tabular-buybox-text',
                '.tabular-buybox-text',
                '[data-automation-id="seller-name"]',
                '.a-merchant-name'
            ]
            
            for selector in seller_selectors:
                seller_elem = soup.select_one(selector)
                if seller_elem:
                    seller_text = seller_elem.get_text().strip()
                    if "sold by" in seller_text.lower():
                        result.seller_name = seller_text.replace("Sold by", "").strip()
                    else:
                        result.seller_name = seller_text
                    break
            
            # Check for Prime eligibility
            if "prime" in page_text or "amazon prime" in page_text:
                result.prime_eligible = True
            
            # Extract product images
            img_selectors = [
                '#landingImage',
                '.a-dynamic-image',
                '[data-automation-id="hero-image"]'
            ]
            
            for selector in img_selectors:
                img_elem = soup.select_one(selector)
                if img_elem and img_elem.get('src'):
                    result.product_images.append(img_elem.get('src'))
            
            # Extract features
            feature_selectors = [
                '#feature-bullets ul li',
                '.a-unordered-list .a-list-item',
                '[data-automation-id="feature-list"] li'
            ]
            
            for selector in feature_selectors:
                feature_elems = soup.select(selector)
                if feature_elems:
                    for elem in feature_elems[:5]:  # Limit to 5 features
                        feature_text = elem.get_text().strip()
                        if feature_text and len(feature_text) > 5:
                            result.features.append(feature_text)
                    break
            
            # Determine final status
            if result.title:
                result.status = "valid"
            else:
                result.status = "invalid"
                result.error_message = "Could not extract product title"
            
            return result
            
        except Exception as e:
            logger.error(f"Error testing ASIN {asin}: {str(e)}")
            result.status = "error"
            result.error_message = str(e)
            return result
    
    async def search_replacement_products(self, category: str, keywords: List[str]) -> List[str]:
        """Search for replacement ASINs in a given category"""
        
        try:
            search_terms = "+".join(keywords)
            search_url = f"{self.base_url}/s?k={search_terms}&ref=sr_pg_1"
            
            logger.info(f"Searching for replacements: {search_terms}")
            
            response = await self.client.get(search_url)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract ASINs from search results
            asins = []
            product_containers = soup.select('[data-asin]')
            
            for container in product_containers[:10]:  # Limit to top 10 results
                asin = container.get('data-asin')
                if asin and asin != "" and len(asin) == 10 and asin.startswith('B'):
                    asins.append(asin)
            
            return asins
            
        except Exception as e:
            logger.error(f"Error searching for replacements: {str(e)}")
            return []
    
    async def generate_report(self, test_results: List[ASINTestResult]) -> Dict:
        """Generate a comprehensive test report"""
        
        valid_asins = [r for r in test_results if r.status == "valid"]
        invalid_asins = [r for r in test_results if r.status == "invalid"]
        unavailable_asins = [r for r in test_results if r.status == "unavailable"]
        error_asins = [r for r in test_results if r.status == "error"]
        
        report = {
            "test_summary": {
                "total_tested": len(test_results),
                "valid": len(valid_asins),
                "invalid": len(invalid_asins),
                "unavailable": len(unavailable_asins),
                "errors": len(error_asins)
            },
            "valid_products": [],
            "invalid_products": [],
            "unavailable_products": [],
            "error_products": [],
            "recommendations": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Process valid products
        for result in valid_asins:
            product_info = {
                "asin": result.asin,
                "title": result.title,
                "price": result.price,
                "availability": result.availability,
                "seller": result.seller_name,
                "prime_eligible": result.prime_eligible,
                "url": result.url,
                "features": result.features[:3],  # Top 3 features
                "images_count": len(result.product_images)
            }
            report["valid_products"].append(product_info)
        
        # Process invalid/unavailable products
        for result in invalid_asins + unavailable_asins:
            problem_info = {
                "asin": result.asin,
                "status": result.status,
                "error": result.error_message,
                "url": result.url
            }
            if result.status == "invalid":
                report["invalid_products"].append(problem_info)
            else:
                report["unavailable_products"].append(problem_info)
        
        # Process errors
        for result in error_asins:
            error_info = {
                "asin": result.asin,
                "error": result.error_message,
                "url": result.url
            }
            report["error_products"].append(error_info)
        
        # Generate recommendations
        if invalid_asins or unavailable_asins:
            report["recommendations"].append("Search for replacement ASINs for invalid/unavailable products")
            report["recommendations"].append("Focus on products sold by Amazon or highly rated sellers")
            report["recommendations"].append("Verify Prime eligibility for better customer experience")
        
        if len(valid_asins) < len(test_results) * 0.5:
            report["recommendations"].append("Consider updating ASIN list as less than 50% are valid")
        
        return report
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

async def test_current_asins():
    """Test the current ASINs used in the Amazon integration service"""
    
    # Current ASINs from the codebase
    current_asins = [
        "B0CR7G9V56",  # Bodyband Abs Roller
        "B09KG4WNXH",  # Strauss Yoga Mat 6mm
        "B08GKQP7HN",  # boAt Rockerz 255 Sports Bluetooth Earphones
        "B09XSWQKL2",  # Boldfit Heavy Resistance Bands
        "B09TXL8QRP"   # Fire-Boltt Phoenix Pro Smartwatch
    ]
    
    validator = AmazonASINValidator()
    
    try:
        logger.info("Starting ASIN validation tests...")
        
        # Test all ASINs
        test_results = []
        for asin in current_asins:
            result = await validator.test_asin(asin)
            test_results.append(result)
            
            # Add a small delay to avoid rate limiting
            await asyncio.sleep(1)
        
        # Generate comprehensive report
        report = await validator.generate_report(test_results)
        
        # Find replacement ASINs for invalid ones
        invalid_results = [r for r in test_results if r.status in ["invalid", "unavailable"]]
        
        if invalid_results:
            logger.info("Searching for replacement ASINs...")
            
            # Define search categories for replacements
            replacement_searches = [
                ("fitness", ["abs", "roller", "exercise", "wheel"]),
                ("yoga", ["yoga", "mat", "exercise", "6mm"]),
                ("electronics", ["bluetooth", "earphones", "wireless", "sports"]),
                ("fitness", ["resistance", "bands", "exercise", "heavy"]),
                ("electronics", ["smartwatch", "bluetooth", "calling", "fitness"])
            ]
            
            replacement_asins = []
            for category, keywords in replacement_searches:
                found_asins = await validator.search_replacement_products(category, keywords)
                replacement_asins.extend(found_asins[:2])  # Take top 2 from each search
                await asyncio.sleep(2)  # Delay between searches
            
            # Test replacement ASINs
            if replacement_asins:
                logger.info(f"Testing {len(replacement_asins)} replacement ASINs...")
                replacement_results = []
                
                for asin in replacement_asins[:10]:  # Limit to 10 replacements
                    result = await validator.test_asin(asin)
                    if result.status == "valid":
                        replacement_results.append(result)
                    await asyncio.sleep(1)
                
                report["replacement_suggestions"] = []
                for result in replacement_results:
                    suggestion = {
                        "asin": result.asin,
                        "title": result.title,
                        "price": result.price,
                        "seller": result.seller_name,
                        "prime_eligible": result.prime_eligible,
                        "url": result.url
                    }
                    report["replacement_suggestions"].append(suggestion)
        
        return report
        
    finally:
        await validator.close()

async def main():
    """Main function to run ASIN validation tests"""
    
    try:
        # Run the tests
        report = await test_current_asins()
        
        # Save report to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"/home/alagiri/projects/bizoholic/bizosaas/ecommerce/services/amazon-integration-service/asin_test_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print("\n" + "="*60)
        print("AMAZON INDIA ASIN VALIDATION REPORT")
        print("="*60)
        
        summary = report["test_summary"]
        print(f"\nTEST SUMMARY:")
        print(f"  Total ASINs Tested: {summary['total_tested']}")
        print(f"  ✅ Valid: {summary['valid']}")
        print(f"  ❌ Invalid: {summary['invalid']}")
        print(f"  🚫 Unavailable: {summary['unavailable']}")
        print(f"  ⚠️  Errors: {summary['errors']}")
        
        print(f"\nVALID PRODUCTS ({len(report['valid_products'])}):")
        for product in report["valid_products"]:
            print(f"  • {product['asin']}: {product['title'][:50]}...")
            print(f"    Price: {product['price']}, Seller: {product['seller']}")
            print(f"    URL: {product['url']}")
            print()
        
        if report.get("invalid_products"):
            print(f"\nINVALID PRODUCTS ({len(report['invalid_products'])}):")
            for product in report["invalid_products"]:
                print(f"  • {product['asin']}: {product['error']}")
                print(f"    URL: {product['url']}")
        
        if report.get("unavailable_products"):
            print(f"\nUNAVAILABLE PRODUCTS ({len(report['unavailable_products'])}):")
            for product in report["unavailable_products"]:
                print(f"  • {product['asin']}: {product['error']}")
                print(f"    URL: {product['url']}")
        
        if report.get("replacement_suggestions"):
            print(f"\nREPLACEMENT SUGGESTIONS ({len(report['replacement_suggestions'])}):")
            for suggestion in report["replacement_suggestions"]:
                print(f"  • {suggestion['asin']}: {suggestion['title'][:50]}...")
                print(f"    Price: {suggestion['price']}, Prime: {suggestion['prime_eligible']}")
                print(f"    URL: {suggestion['url']}")
                print()
        
        print(f"\nRECOMMENDATIONS:")
        for rec in report["recommendations"]:
            print(f"  • {rec}")
        
        print(f"\nDetailed report saved to: {report_file}")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Test execution failed: {str(e)}")
        print(f"\nERROR: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())

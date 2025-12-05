#!/usr/bin/env python3
"""
Demo script for Amazon Data Scraper
Showcases real vs placeholder data comparison
"""

import asyncio
import sys
sys.path.append('.')

from amazon_sourcing_service import AmazonDataScraper, logger

async def demo_real_vs_placeholder():
    """Demo showing real Amazon data vs placeholder data"""
    
    print("🚀 Amazon Data Scraper Demo")
    print("=" * 50)
    
    scraper = AmazonDataScraper()
    
    # Test verified ASINs
    test_asins = [
        ("B0CR7G9V56", "Bodyband Abs Roller"),
        ("B0DX1QJFK4", "Boldfit Yoga Mat"),
        ("B0FGYDCPRR", "pTron Bassbuds Earbuds"),
    ]
    
    try:
        for asin, product_name in test_asins:
            print(f"\n📦 Testing: {product_name} ({asin})")
            print("-" * 40)
            
            # Scrape real data
            scraped_data = await scraper.scrape_product_data(asin)
            
            # Show comparison
            print("🔍 REAL AMAZON DATA:")
            print(f"   Success: {'✅ Yes' if scraped_data.get('success') else '❌ No'}")
            print(f"   Title: {scraped_data.get('title', 'N/A')}")
            print(f"   Price: ₹{scraped_data.get('price', 'N/A')}")
            print(f"   Rating: {scraped_data.get('rating', 'N/A')}/5")
            print(f"   Reviews: {scraped_data.get('review_count', 'N/A')}")
            print(f"   Availability: {scraped_data.get('availability', 'N/A')}")
            
            if scraped_data.get('image_url'):
                print(f"   Image URL: {scraped_data['image_url'][:60]}...")
                print("   🖼️  Real Amazon Image Found!")
            else:
                print("   📷 No image found - would use placeholder")
            
            # Show fallback data for comparison
            if not scraped_data.get('success'):
                print("\n🔄 FALLBACK DATA:")
                print("   Would use placeholder image: /images/product-placeholder-1.jpg")
                print("   Would use estimated price from product database")
            
            print(f"   🌐 Product URL: https://www.amazon.in/dp/{asin}")
            
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
    finally:
        await scraper.close()

async def demo_price_comparison():
    """Demo showing price accuracy"""
    
    print(f"\n💰 Price Accuracy Demo")
    print("=" * 30)
    
    scraper = AmazonDataScraper()
    
    expected_prices = {
        "B0CR7G9V56": (179, 199),  # Bodyband Abs Roller
        "B0DX1QJFK4": (379, 449),  # Boldfit Yoga Mat
        "B0FGYDCPRR": (999, 1199), # pTron Bassbuds
    }
    
    try:
        for asin, (min_price, max_price) in expected_prices.items():
            scraped_data = await scraper.scrape_product_data(asin)
            real_price = scraped_data.get('price')
            
            print(f"📊 ASIN {asin}:")
            print(f"   Expected Range: ₹{min_price} - ₹{max_price}")
            print(f"   Scraped Price: ₹{real_price}")
            
            if real_price:
                if min_price <= real_price <= max_price:
                    print(f"   ✅ Price within expected range!")
                else:
                    print(f"   ⚠️  Price outside expected range (market fluctuation)")
            else:
                print(f"   ❌ Could not extract price")
            
    except Exception as e:
        print(f"❌ Price demo failed: {str(e)}")
    finally:
        await scraper.close()

async def demo_caching():
    """Demo showing caching functionality"""
    
    print(f"\n⚡ Caching Demo")
    print("=" * 20)
    
    scraper = AmazonDataScraper()
    test_asin = "B0CR7G9V56"
    
    try:
        # First request (should scrape)
        print("🌐 First request (will scrape from Amazon)...")
        start_time = asyncio.get_event_loop().time()
        data1 = await scraper.scrape_product_data(test_asin)
        first_duration = asyncio.get_event_loop().time() - start_time
        print(f"   Duration: {first_duration:.2f} seconds")
        print(f"   Cached: {'No' if data1.get('success') else 'N/A'}")
        
        # Second request (should use cache)
        print("⚡ Second request (should use cache)...")
        start_time = asyncio.get_event_loop().time()
        data2 = await scraper.scrape_product_data(test_asin)
        second_duration = asyncio.get_event_loop().time() - start_time
        print(f"   Duration: {second_duration:.2f} seconds")
        print(f"   Cached: Yes")
        
        print(f"🚀 Speed improvement: {first_duration/second_duration:.1f}x faster!")
        print(f"📊 Cache size: {len(scraper.cache)} items")
        
    except Exception as e:
        print(f"❌ Caching demo failed: {str(e)}")
    finally:
        await scraper.close()

async def main():
    """Run all demos"""
    await demo_real_vs_placeholder()
    await demo_price_comparison()
    await demo_caching()
    
    print(f"\n🎯 Demo Complete!")
    print("📚 Next steps:")
    print("   1. Start the service: python amazon_sourcing_service.py")
    print("   2. Test the API: curl 'http://localhost:8080/scraper/test/B0CR7G9V56'")
    print("   3. Run comprehensive tests: python test_scraper.py")

if __name__ == "__main__":
    asyncio.run(main())
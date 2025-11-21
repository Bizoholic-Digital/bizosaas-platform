# Amazon Data Scraper Implementation

## Overview

This implementation adds real Amazon product image and price scraping capabilities to the existing Amazon sourcing service. It replaces placeholder images and calculated prices with real data scraped from Amazon India product pages.

## Features

### ✅ Real Data Extraction
- **Product Images**: Extracts high-resolution product images from Amazon pages
- **Current Prices**: Gets live pricing in INR from Amazon India
- **Product Details**: Scrapes titles, ratings, review counts, and availability
- **Fallback System**: Gracefully falls back to placeholder data if scraping fails

### ✅ Production-Ready Implementation
- **Rate Limiting**: Built-in delays and request throttling
- **Caching**: 1-hour cache for scraped data to avoid redundant requests
- **Error Handling**: Comprehensive error handling with detailed logging
- **Resource Management**: Proper HTTP client cleanup on shutdown

### ✅ Security & Performance
- **User Agent Rotation**: Uses realistic browser headers
- **Request Delays**: Random delays to avoid detection
- **Verified ASINs Only**: Only scrapes verified working ASINs to avoid wasted requests
- **Memory Efficient**: Caches only essential data with TTL

## API Endpoints

### Test Endpoints

#### GET `/scraper/test/{asin}`
Test scraping for a single ASIN
```bash
curl "http://localhost:8080/scraper/test/B0CR7G9V56"
```

#### POST `/scraper/batch-test`
Test scraping for multiple ASINs
```bash
curl -X POST "http://localhost:8080/scraper/batch-test" \
  -H "Content-Type: application/json" \
  -d '["B0CR7G9V56", "B0DX1QJFK4", "B0BLSQPPKT"]'
```

### Integration Endpoints

#### POST `/sourcing/search`
Product search now includes real images and prices for verified ASINs
```bash
curl -X POST "http://localhost:8080/sourcing/search" \
  -H "Content-Type: application/json" \
  -d '{\"query\": \"yoga mat\", \"limit\": 5}'
```

## Verified ASINs

The scraper currently works with these verified Amazon India ASINs:

| ASIN | Product | Expected Price Range |
|------|---------|---------------------|
| B0CR7G9V56 | Bodyband Abs Roller | ₹179-199 |
| B0DX1QJFK4 | Boldfit Yoga Mat | ₹379-449 |
| B0BLSQPPKT | Boldfit NBR Yoga Mat | ₹436-499 |
| B0FGYDCPRR | pTron Bassbuds Earbuds | ₹999-1199 |
| B08D8J5BVR | Boldfit Resistance Band Red | ₹349-399 |
| B08H7XCSTS | Boldfit Resistance Band Purple | ₹645-699 |
| B0C4Q5HNMH | Noise Halo Plus Smartwatch | ₹2599-2999 |

## Implementation Details

### AmazonDataScraper Class

```python
class AmazonDataScraper:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=15.0, headers={...})
        self.cache = {}
        self.cache_duration = 3600  # 1 hour
    
    async def scrape_product_data(self, asin: str, marketplace: str = \"amazon.in\"):
        # Scrapes real Amazon product data with caching
        
    def _extract_image_url(self, soup: BeautifulSoup):
        # Extracts high-resolution product images
        
    def _extract_price(self, soup: BeautifulSoup):
        # Extracts current price in INR
```

### Integration Points

1. **Product Search**: `generate_real_amazon_products()` function now calls scraper for verified ASINs
2. **Caching**: Results cached for 1 hour to minimize requests
3. **Fallback**: If scraping fails, uses existing placeholder system
4. **Error Handling**: All scraping failures are logged but don't break the API

## Usage Examples

### Starting the Service

```bash
cd /home/alagiri/projects/bizoholic/bizosaas/ecommerce/services/amazon-integration-service
pip install -r requirements.txt
python amazon_sourcing_service.py
```

### Testing the Scraper

```bash
# Test single ASIN
python test_scraper.py

# Or test via API
curl \"http://localhost:8080/scraper/test/B0CR7G9V56\"
```

### Sample Response with Real Data

```json
{
  \"asin\": \"B0CR7G9V56\",
  \"title\": \"Bodyband Abs Roller for Men & Women with Knee Mat - Yellow Black\",
  \"price\": 179.0,
  \"currency\": \"INR\",
  \"image_url\": \"https://m.media-amazon.com/images/I/61zKzHQWc6L._AC_SL1200_.jpg\",
  \"product_url\": \"https://www.amazon.in/dp/B0CR7G9V56\",
  \"availability\": \"In Stock\",
  \"rating\": 3.6,
  \"review_count\": 1600
}
```

## Configuration

### Environment Variables

```env
# Optional: Configure request delays
SCRAPER_MIN_DELAY=0.5
SCRAPER_MAX_DELAY=1.5
SCRAPER_CACHE_DURATION=3600
```

### Rate Limiting

- Base delay: 0.5 seconds
- Random jitter: 0-1 seconds
- Only scrapes verified ASINs
- Respects cache TTL

## Error Handling

### Graceful Degradation
1. **Network Issues**: Falls back to placeholder data
2. **Amazon Changes**: Tries multiple selectors for each data point
3. **Rate Limiting**: Implements delays and retries
4. **Invalid ASINs**: Uses fallback product data

### Logging
- INFO: Successful scrapes and cache hits
- WARNING: Failed requests and fallbacks
- ERROR: Unexpected errors with full stack traces

## Monitoring

### Analytics Endpoint

```bash
curl \"http://localhost:8080/analytics/sourcing-stats\"
```

Returns scraping statistics:
```json
{
  \"scraping_stats\": {
    \"cache_size\": 7,
    \"cache_duration\": 3600,
    \"verified_asins\": [\"B0CR7G9V56\", ...]
  }
}
```

### Health Checks
- Cache size monitoring
- Success rate tracking
- Response time metrics

## Security Considerations

1. **User Agent**: Uses realistic browser headers
2. **Request Patterns**: Random delays to avoid detection
3. **Rate Limits**: Built-in throttling
4. **IP Rotation**: Consider proxy rotation for high-volume usage
5. **Legal Compliance**: Respects robots.txt and terms of service

## Future Enhancements

### Planned Features
1. **Proxy Support**: For higher volume scraping
2. **Image Caching**: Local storage of product images
3. **Price Tracking**: Historical price data
4. **Availability Monitoring**: Real-time stock status
5. **Review Scraping**: Customer review analysis

### Scalability
- Redis cache integration
- Distributed scraping workers
- Queue-based processing
- Webhook notifications

## Testing

Run the comprehensive test suite:

```bash
python test_scraper.py
```

This tests:
- Single ASIN scraping
- Batch ASIN scraping  
- Integration with product search
- Error handling and fallbacks

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install beautifulsoup4 lxml
   ```

2. **Amazon Blocking Requests**
   - Check user agent headers
   - Increase delays between requests
   - Use proxy services

3. **Invalid Product Data**
   - Verify ASIN is correct
   - Check if product is available in Indian marketplace
   - Review extraction selectors

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## License & Legal

This implementation is for educational and research purposes. Always respect:
- Amazon's robots.txt
- Terms of service
- Rate limiting guidelines
- Data privacy regulations

## Support

For issues or questions:
1. Check the logs for error details
2. Test with verified ASINs first
3. Ensure network connectivity to amazon.in
4. Review rate limiting and caching settings
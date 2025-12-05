"""
Enhanced Amazon Integration for CoreLDove
Real Amazon Product Advertising API and Order Processing
"""

import asyncio
import aiohttp
import json
import hashlib
import hmac
import base64
import urllib.parse
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

@dataclass
class AmazonCredentials:
    """Amazon API Credentials"""
    access_key: str
    secret_key: str
    partner_tag: str
    host: str = "webservices.amazon.in"  # Amazon India
    region: str = "eu-west-1"
    service: str = "ProductAdvertisingAPI"

@dataclass 
class AmazonProduct:
    """Amazon Product Data Structure"""
    asin: str
    title: str
    price: Optional[Decimal] = None
    list_price: Optional[Decimal] = None
    currency: str = "INR"
    availability: Optional[str] = None
    prime_eligible: bool = False
    rating: Optional[float] = None
    review_count: Optional[int] = None
    images: List[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    features: List[str] = None
    dimensions: Optional[Dict[str, Any]] = None
    weight: Optional[str] = None
    url: Optional[str] = None
    
    def __post_init__(self):
        if self.images is None:
            self.images = []
        if self.features is None:
            self.features = []

@dataclass
class ProfitAnalysis:
    """Profit Analysis for Products"""
    source_price: Decimal
    selling_price: Decimal
    profit_amount: Decimal
    profit_margin: float
    break_even_quantity: int
    roi_percentage: float
    recommended_action: str

class AmazonProductAdvertisingAPI:
    """
    Enhanced Amazon Product Advertising API Integration
    Supports real Amazon.in product search and data retrieval
    """
    
    def __init__(self, credentials: AmazonCredentials):
        self.credentials = credentials
        self.endpoint = f"https://{credentials.host}/paapi5"
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _generate_signature(self, method: str, uri: str, query_string: str, payload: str) -> Dict[str, str]:
        """Generate AWS Signature Version 4 for Amazon PA API"""
        
        # Step 1: Create canonical request
        canonical_headers = f"host:{self.credentials.host}\nx-amz-date:{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}\n"
        signed_headers = "host;x-amz-date"
        hashed_payload = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        
        canonical_request = f"{method}\n{uri}\n{query_string}\n{canonical_headers}\n{signed_headers}\n{hashed_payload}"
        
        # Step 2: Create string to sign
        algorithm = "AWS4-HMAC-SHA256"
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        date_stamp = datetime.now(timezone.utc).strftime('%Y%m%d')
        credential_scope = f"{date_stamp}/{self.credentials.region}/{self.credentials.service}/aws4_request"
        string_to_sign = f"{algorithm}\n{timestamp}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
        
        # Step 3: Calculate signature
        def sign(key: bytes, msg: str) -> bytes:
            return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
        
        k_date = sign(f"AWS4{self.credentials.secret_key}".encode('utf-8'), date_stamp)
        k_region = sign(k_date, self.credentials.region)
        k_service = sign(k_region, self.credentials.service)
        k_signing = sign(k_service, "aws4_request")
        signature = hmac.new(k_signing, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
        
        # Step 4: Create authorization header
        authorization = f"{algorithm} Credential={self.credentials.access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
        
        return {
            "Authorization": authorization,
            "X-Amz-Date": timestamp,
            "Content-Type": "application/json; charset=UTF-8"
        }
    
    async def search_products(self, 
                            keywords: List[str],
                            category: Optional[str] = None,
                            min_price: Optional[int] = None,
                            max_price: Optional[int] = None,
                            min_reviews: Optional[int] = None,
                            sort_by: str = "Relevance",
                            max_results: int = 10) -> List[AmazonProduct]:
        """
        Search for products on Amazon.in using Product Advertising API
        """
        
        try:
            # Prepare search request
            search_request = {
                "PartnerType": "Associates",
                "PartnerTag": self.credentials.partner_tag,
                "Keywords": " ".join(keywords),
                "Resources": [
                    "Images.Primary.Large",
                    "ItemInfo.Title",
                    "ItemInfo.Features",
                    "ItemInfo.ProductInfo",
                    "Offers.Listings.Price",
                    "Offers.Listings.ProgramEligibility.IsPrimeExclusive",
                    "CustomerReviews.StarRating",
                    "CustomerReviews.Count"
                ],
                "SearchIndex": category or "All",
                "ItemCount": min(max_results, 10),  # Max 10 per request
                "SortBy": sort_by
            }
            
            # Add price filters if specified
            if min_price is not None:
                search_request["MinPrice"] = min_price * 100  # Convert to paise
            if max_price is not None:
                search_request["MaxPrice"] = max_price * 100
                
            # Add review filter
            if min_reviews is not None:
                search_request["MinReviewsRating"] = min_reviews
            
            payload = json.dumps(search_request)
            headers = self._generate_signature("POST", "/paapi5/searchitems", "", payload)
            
            async with self.session.post(
                f"{self.endpoint}/searchitems",
                headers=headers,
                data=payload
            ) as response:
                
                if response.status != 200:
                    logger.error(f"Amazon API error: {response.status} - {await response.text()}")
                    return []
                
                data = await response.json()
                return self._parse_search_results(data)
                
        except Exception as e:
            logger.error(f"Amazon search error: {e}")
            return []
    
    async def get_product_details(self, asin: str) -> Optional[AmazonProduct]:
        """Get detailed information for a specific product by ASIN"""
        
        try:
            request_payload = {
                "PartnerType": "Associates", 
                "PartnerTag": self.credentials.partner_tag,
                "ItemIds": [asin],
                "Resources": [
                    "BrowseNodeInfo.BrowseNodes",
                    "Images.Primary.Large",
                    "Images.Variants.Large",
                    "ItemInfo.ByLineInfo",
                    "ItemInfo.ContentInfo",
                    "ItemInfo.ContentRating",
                    "ItemInfo.Features",
                    "ItemInfo.ManufactureInfo",
                    "ItemInfo.ProductInfo",
                    "ItemInfo.TechnicalInfo",
                    "ItemInfo.Title",
                    "ItemInfo.TradeInInfo",
                    "Offers.Listings.Availability.MaxOrderQuantity",
                    "Offers.Listings.Availability.Message",
                    "Offers.Listings.Availability.MinOrderQuantity",
                    "Offers.Listings.Availability.Type",
                    "Offers.Listings.Condition",
                    "Offers.Listings.DeliveryInfo.IsAmazonFulfilled",
                    "Offers.Listings.DeliveryInfo.IsFreeShippingEligible",
                    "Offers.Listings.DeliveryInfo.IsPrimeEligible",
                    "Offers.Listings.IsBuyBoxWinner",
                    "Offers.Listings.LoyaltyPoints.Points",
                    "Offers.Listings.MerchantInfo",
                    "Offers.Listings.Price",
                    "Offers.Listings.ProgramEligibility.IsPrimeExclusive",
                    "Offers.Listings.ProgramEligibility.IsPrimePantry",
                    "Offers.Listings.Promotions",
                    "Offers.Listings.SavingBasis",
                    "Offers.Summaries.HighestPrice",
                    "Offers.Summaries.LowestPrice",
                    "Offers.Summaries.OfferCount",
                    "CustomerReviews.Count",
                    "CustomerReviews.StarRating"
                ]
            }
            
            payload = json.dumps(request_payload)
            headers = self._generate_signature("POST", "/paapi5/getitems", "", payload)
            
            async with self.session.post(
                f"{self.endpoint}/getitems", 
                headers=headers,
                data=payload
            ) as response:
                
                if response.status != 200:
                    logger.error(f"Amazon product details error: {response.status}")
                    return None
                
                data = await response.json()
                results = self._parse_search_results(data)
                return results[0] if results else None
                
        except Exception as e:
            logger.error(f"Get product details error: {e}")
            return None
    
    def _parse_search_results(self, api_response: Dict[str, Any]) -> List[AmazonProduct]:
        """Parse Amazon PA API response into AmazonProduct objects"""
        
        products = []
        
        try:
            items = api_response.get("SearchResult", {}).get("Items", [])
            if not items:
                items = api_response.get("ItemsResult", {}).get("Items", [])
            
            for item in items:
                try:
                    # Basic product info
                    asin = item.get("ASIN", "")
                    title = item.get("ItemInfo", {}).get("Title", {}).get("DisplayValue", "")
                    
                    # Price information
                    price = None
                    list_price = None
                    
                    offers = item.get("Offers", {}).get("Listings", [])
                    if offers:
                        price_info = offers[0].get("Price")
                        if price_info:
                            price = Decimal(str(price_info.get("Amount", 0))) / 100  # Convert from paise
                            
                        savings_basis = offers[0].get("SavingBasis")
                        if savings_basis:
                            list_price = Decimal(str(savings_basis.get("Amount", 0))) / 100
                    
                    # Images
                    images = []
                    primary_image = item.get("Images", {}).get("Primary", {}).get("Large", {})
                    if primary_image.get("URL"):
                        images.append(primary_image["URL"])
                    
                    # Additional image variants
                    variants = item.get("Images", {}).get("Variants", [])
                    for variant in variants:
                        large_image = variant.get("Large", {})
                        if large_image.get("URL"):
                            images.append(large_image["URL"])
                    
                    # Brand and category
                    brand = item.get("ItemInfo", {}).get("ByLineInfo", {}).get("Brand", {}).get("DisplayValue")
                    
                    # Product features
                    features = []
                    feature_info = item.get("ItemInfo", {}).get("Features", {}).get("DisplayValues", [])
                    features.extend(feature_info)
                    
                    # Reviews and ratings
                    rating = None
                    review_count = None
                    
                    reviews = item.get("CustomerReviews", {})
                    if reviews.get("StarRating"):
                        rating = float(reviews["StarRating"]["Value"])
                    if reviews.get("Count"):
                        review_count = reviews["Count"]["Value"]
                    
                    # Prime eligibility
                    prime_eligible = False
                    if offers and offers[0].get("DeliveryInfo", {}).get("IsPrimeEligible"):
                        prime_eligible = True
                    
                    # Availability
                    availability = "Unknown"
                    if offers and offers[0].get("Availability", {}).get("Type"):
                        availability = offers[0]["Availability"]["Type"]
                    
                    # Product URL
                    url = item.get("DetailPageURL", "")
                    
                    # Dimensions and weight
                    dimensions = None
                    weight = None
                    
                    tech_info = item.get("ItemInfo", {}).get("TechnicalInfo", {})
                    if tech_info:
                        # Extract dimensions if available
                        dimensions_info = tech_info.get("Dimensions", {}).get("DisplayValue")
                        if dimensions_info:
                            dimensions = {"display": dimensions_info}
                        
                        # Extract weight if available  
                        weight_info = tech_info.get("Weight", {}).get("DisplayValue")
                        if weight_info:
                            weight = weight_info
                    
                    # Create product object
                    product = AmazonProduct(
                        asin=asin,
                        title=title,
                        price=price,
                        list_price=list_price,
                        currency="INR",
                        availability=availability,
                        prime_eligible=prime_eligible,
                        rating=rating,
                        review_count=review_count,
                        images=images,
                        brand=brand,
                        features=features,
                        dimensions=dimensions,
                        weight=weight,
                        url=url
                    )
                    
                    products.append(product)
                    
                except Exception as e:
                    logger.warning(f"Failed to parse product item: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Parse search results error: {e}")
        
        return products

class AmazonDropshippingAutomation:
    """
    Complete Amazon Dropshipping Automation System
    Handles product sourcing, profit analysis, and order processing
    """
    
    def __init__(self, credentials: AmazonCredentials, markup_percentage: float = 40.0):
        self.api = AmazonProductAdvertisingAPI(credentials)
        self.markup_percentage = markup_percentage
        
    async def analyze_product_profitability(self, 
                                          product: AmazonProduct,
                                          additional_costs: Dict[str, Decimal] = None) -> ProfitAnalysis:
        """
        Analyze profitability of an Amazon product for dropshipping
        """
        
        if not product.price:
            raise ValueError("Product price is required for profitability analysis")
        
        # Default additional costs
        if additional_costs is None:
            additional_costs = {
                "shipping": Decimal("50.00"),      # Average shipping cost in INR
                "payment_fees": Decimal("0.025"),  # 2.5% payment gateway fees
                "platform_fees": Decimal("0.02"),  # 2% platform fees  
                "packaging": Decimal("20.00"),     # Packaging costs
                "customer_service": Decimal("15.00"), # Customer service allocation
                "marketing": Decimal("0.05")       # 5% marketing allocation
            }
        
        source_price = product.price
        
        # Calculate additional costs
        total_additional_costs = Decimal("0.00")
        
        # Fixed costs
        total_additional_costs += additional_costs.get("shipping", Decimal("0"))
        total_additional_costs += additional_costs.get("packaging", Decimal("0"))
        total_additional_costs += additional_costs.get("customer_service", Decimal("0"))
        
        # Percentage-based costs (calculated on selling price)
        selling_price_before_percentage = source_price * (1 + (self.markup_percentage / 100))
        
        payment_fee_rate = additional_costs.get("payment_fees", Decimal("0"))
        platform_fee_rate = additional_costs.get("platform_fees", Decimal("0"))
        marketing_rate = additional_costs.get("marketing", Decimal("0"))
        
        total_percentage_rate = payment_fee_rate + platform_fee_rate + marketing_rate
        
        # Calculate final selling price including percentage-based costs
        selling_price = (selling_price_before_percentage + total_additional_costs) / (1 - total_percentage_rate)
        selling_price = selling_price.quantize(Decimal('0.01'))
        
        # Calculate percentage-based costs on final selling price
        percentage_costs = selling_price * total_percentage_rate
        
        # Total costs
        total_costs = source_price + total_additional_costs + percentage_costs
        
        # Profit calculations
        profit_amount = selling_price - total_costs
        profit_margin = float((profit_amount / selling_price) * 100)
        
        # ROI calculation
        roi_percentage = float((profit_amount / source_price) * 100)
        
        # Break-even analysis (assuming fixed costs of ₹1000/month)
        monthly_fixed_costs = Decimal("1000.00")
        break_even_quantity = int((monthly_fixed_costs / profit_amount).quantize(Decimal('1')))
        
        # Recommendation logic
        if profit_margin >= 25 and roi_percentage >= 30:
            recommendation = "highly_recommended"
        elif profit_margin >= 15 and roi_percentage >= 20:
            recommendation = "recommended"
        elif profit_margin >= 10 and roi_percentage >= 15:
            recommendation = "proceed_with_caution"
        else:
            recommendation = "not_recommended"
        
        return ProfitAnalysis(
            source_price=source_price,
            selling_price=selling_price,
            profit_amount=profit_amount,
            profit_margin=profit_margin,
            break_even_quantity=break_even_quantity,
            roi_percentage=roi_percentage,
            recommended_action=recommendation
        )
    
    async def find_profitable_products(self,
                                     keywords: List[str],
                                     min_profit_margin: float = 20.0,
                                     min_rating: float = 4.0,
                                     max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Find profitable products for dropshipping based on criteria
        """
        
        profitable_products = []
        
        try:
            async with self.api:
                # Search for products
                products = await self.api.search_products(
                    keywords=keywords,
                    min_reviews=50,  # Minimum reviews for reliability
                    max_results=max_results,
                    sort_by="Price:LowToHigh"  # Start with lower-priced items
                )
                
                for product in products:
                    try:
                        # Skip products without price or low ratings
                        if not product.price or (product.rating and product.rating < min_rating):
                            continue
                        
                        # Analyze profitability
                        profit_analysis = await self.analyze_product_profitability(product)
                        
                        # Filter by minimum profit margin
                        if profit_analysis.profit_margin >= min_profit_margin:
                            
                            product_data = {
                                "product": product,
                                "profit_analysis": profit_analysis,
                                "profitability_score": self._calculate_profitability_score(product, profit_analysis),
                                "market_potential": await self._assess_market_potential(product),
                                "competition_level": await self._assess_competition_level(product),
                                "recommendation_strength": self._get_recommendation_strength(profit_analysis)
                            }
                            
                            profitable_products.append(product_data)
                            
                    except Exception as e:
                        logger.warning(f"Failed to analyze product {product.asin}: {e}")
                        continue
            
            # Sort by profitability score (highest first)
            profitable_products.sort(
                key=lambda x: x["profitability_score"], 
                reverse=True
            )
            
            return profitable_products
            
        except Exception as e:
            logger.error(f"Find profitable products error: {e}")
            return []
    
    def _calculate_profitability_score(self, product: AmazonProduct, analysis: ProfitAnalysis) -> float:
        """Calculate overall profitability score (0-100)"""
        
        # Profit margin component (40% weight)
        profit_score = min(analysis.profit_margin * 2, 40.0)
        
        # ROI component (30% weight) 
        roi_score = min(analysis.roi_percentage * 0.75, 30.0)
        
        # Product rating component (15% weight)
        rating_score = 0.0
        if product.rating:
            rating_score = min((product.rating - 2) * 7.5, 15.0)  # Scale 2-5 to 0-15
        
        # Review count component (10% weight) - indicator of demand
        review_score = 0.0
        if product.review_count:
            review_score = min(product.review_count / 100, 10.0)  # Up to 1000 reviews = 10 points
        
        # Prime eligibility bonus (5% weight)
        prime_score = 5.0 if product.prime_eligible else 0.0
        
        total_score = profit_score + roi_score + rating_score + review_score + prime_score
        return round(total_score, 1)
    
    async def _assess_market_potential(self, product: AmazonProduct) -> Dict[str, Any]:
        """Assess market potential for the product"""
        
        # This would integrate with Google Trends API, keyword research tools, etc.
        # For now, return a basic assessment based on product data
        
        potential_score = 50  # Base score
        
        # High review count indicates demand
        if product.review_count:
            if product.review_count > 1000:
                potential_score += 20
            elif product.review_count > 500:
                potential_score += 15
            elif product.review_count > 100:
                potential_score += 10
        
        # Prime eligibility indicates popular category
        if product.prime_eligible:
            potential_score += 10
        
        # High rating indicates customer satisfaction
        if product.rating and product.rating >= 4.5:
            potential_score += 10
        elif product.rating and product.rating >= 4.0:
            potential_score += 5
        
        # Multiple images indicate well-presented products
        if len(product.images) >= 3:
            potential_score += 5
        
        potential_score = min(potential_score, 100)
        
        return {
            "score": potential_score,
            "level": "high" if potential_score >= 80 else "medium" if potential_score >= 60 else "low",
            "factors": {
                "review_count": product.review_count or 0,
                "rating": product.rating or 0,
                "prime_eligible": product.prime_eligible,
                "image_count": len(product.images)
            }
        }
    
    async def _assess_competition_level(self, product: AmazonProduct) -> Dict[str, Any]:
        """Assess competition level for the product category"""
        
        # This would integrate with competitor analysis tools
        # For now, return a basic assessment
        
        competition_score = 50  # Base score
        
        # High review count might indicate saturated market
        if product.review_count:
            if product.review_count > 5000:
                competition_score += 30  # High competition
            elif product.review_count > 2000:
                competition_score += 20
            elif product.review_count > 1000:
                competition_score += 10
            else:
                competition_score -= 10  # Lower competition
        
        # Generic brand names might indicate more competition
        if product.brand and len(product.brand) <= 5:
            competition_score += 15  # Generic brands = more competition
        
        competition_score = max(0, min(competition_score, 100))
        
        return {
            "score": competition_score,
            "level": "high" if competition_score >= 70 else "medium" if competition_score >= 40 else "low",
            "factors": {
                "market_saturation": "high" if product.review_count and product.review_count > 2000 else "medium",
                "brand_competition": "high" if product.brand and len(product.brand) <= 5 else "low"
            }
        }
    
    def _get_recommendation_strength(self, analysis: ProfitAnalysis) -> Dict[str, Any]:
        """Get recommendation strength based on profit analysis"""
        
        strength_mapping = {
            "highly_recommended": {"strength": 9, "confidence": "very_high"},
            "recommended": {"strength": 7, "confidence": "high"},
            "proceed_with_caution": {"strength": 5, "confidence": "medium"},
            "not_recommended": {"strength": 2, "confidence": "low"}
        }
        
        return strength_mapping.get(analysis.recommended_action, {"strength": 1, "confidence": "very_low"})
    
    async def generate_product_listing(self, 
                                     product: AmazonProduct, 
                                     profit_analysis: ProfitAnalysis,
                                     platform: str = "shopify") -> Dict[str, Any]:
        """
        Generate optimized product listing for dropshipping platform
        """
        
        # Enhanced title with profit-focused keywords
        enhanced_title = self._enhance_product_title(product)
        
        # Generate compelling description
        description = self._generate_product_description(product, profit_analysis)
        
        # Generate bullet points highlighting value
        bullet_points = self._generate_bullet_points(product)
        
        # SEO tags
        tags = self._generate_seo_tags(product)
        
        # Pricing strategy
        pricing = {
            "cost_price": float(profit_analysis.source_price),
            "selling_price": float(profit_analysis.selling_price),
            "compare_at_price": float(product.list_price) if product.list_price else None,
            "profit_margin": profit_analysis.profit_margin
        }
        
        return {
            "title": enhanced_title,
            "description": description,
            "bullet_points": bullet_points,
            "pricing": pricing,
            "images": product.images,
            "tags": tags,
            "sku": f"AMZ_{product.asin}",
            "inventory_management": "continuous",
            "shipping_info": {
                "weight": product.weight,
                "dimensions": product.dimensions,
                "origin": "India",
                "processing_time": "2-3 business days"
            },
            "platform_specific": self._get_platform_specific_config(platform)
        }
    
    def _enhance_product_title(self, product: AmazonProduct) -> str:
        """Enhance product title for better conversion"""
        
        title = product.title
        
        # Add value propositions
        value_adds = []
        
        if product.prime_eligible:
            value_adds.append("Fast Shipping")
        
        if product.rating and product.rating >= 4.5:
            value_adds.append("Top Rated")
        
        if product.brand and len(product.brand) > 5:
            value_adds.append(f"Genuine {product.brand}")
        
        if value_adds:
            title += f" - {' | '.join(value_adds)}"
        
        return title[:200]  # Keep within platform limits
    
    def _generate_product_description(self, product: AmazonProduct, analysis: ProfitAnalysis) -> str:
        """Generate compelling product description"""
        
        description_parts = []
        
        # Opening hook
        description_parts.append(f"🌟 **{product.title}** - Premium Quality at Unbeatable Value!")
        description_parts.append("")
        
        # Key features
        if product.features:
            description_parts.append("✨ **Key Features:**")
            for feature in product.features[:5]:  # Top 5 features
                description_parts.append(f"• {feature}")
            description_parts.append("")
        
        # Value proposition
        description_parts.append("🎯 **Why Choose This Product?**")
        
        if product.rating and product.rating >= 4.0:
            description_parts.append(f"⭐ **{product.rating}/5 Stars** from {product.review_count or 'thousands of'} satisfied customers")
        
        if product.prime_eligible:
            description_parts.append("🚚 **Fast & Reliable Shipping** - Quick delivery to your doorstep")
        
        if product.brand:
            description_parts.append(f"🏷️ **Authentic {product.brand}** - Genuine brand quality guaranteed")
        
        # Savings highlight
        if analysis.profit_margin > 20:
            description_parts.append(f"💰 **Great Value** - Premium quality at competitive pricing")
        
        description_parts.append("")
        
        # Trust signals
        description_parts.append("✅ **Our Promise:**")
        description_parts.append("• 100% Authentic Products")
        description_parts.append("• Secure Payment Processing")
        description_parts.append("• Responsive Customer Support")
        description_parts.append("• Easy Returns & Exchanges")
        
        return "\n".join(description_parts)
    
    def _generate_bullet_points(self, product: AmazonProduct) -> List[str]:
        """Generate compelling bullet points"""
        
        bullets = []
        
        # Product features (top 3)
        if product.features:
            for feature in product.features[:3]:
                bullets.append(f"✨ {feature}")
        
        # Quality assurance
        if product.rating and product.rating >= 4.0:
            bullets.append(f"⭐ Highly Rated - {product.rating}/5 stars from verified buyers")
        
        # Brand authenticity
        if product.brand:
            bullets.append(f"🏷️ Authentic {product.brand} - Genuine brand quality")
        
        # Shipping
        if product.prime_eligible:
            bullets.append("🚚 Fast Shipping - Quick and reliable delivery")
        
        # Support
        bullets.append("💬 24/7 Customer Support - We're here to help you")
        
        return bullets[:5]  # Limit to 5 bullets
    
    def _generate_seo_tags(self, product: AmazonProduct) -> List[str]:
        """Generate SEO tags for the product"""
        
        tags = []
        
        # Brand tag
        if product.brand:
            tags.append(product.brand.lower())
        
        # Category-based tags (extract from title)
        title_words = product.title.lower().split()
        
        # Common product keywords
        product_keywords = [
            "premium", "quality", "authentic", "genuine", "durable",
            "wireless", "bluetooth", "rechargeable", "waterproof", "portable"
        ]
        
        for word in title_words:
            if word in product_keywords:
                tags.append(word)
        
        # Rating-based tags
        if product.rating and product.rating >= 4.5:
            tags.append("top-rated")
            tags.append("bestseller")
        
        # Prime tag
        if product.prime_eligible:
            tags.append("fast-shipping")
            tags.append("prime-eligible")
        
        # Remove duplicates and limit
        tags = list(set(tags))[:15]
        
        return tags
    
    def _get_platform_specific_config(self, platform: str) -> Dict[str, Any]:
        """Get platform-specific configuration"""
        
        configs = {
            "shopify": {
                "product_type": "Physical",
                "vendor": "Amazon Sourced",
                "track_inventory": True,
                "requires_shipping": True,
                "taxable": True,
                "seo_title_suffix": " - Buy Online",
                "collection_rules": ["automated", "trending", "featured"]
            },
            "woocommerce": {
                "product_type": "simple",
                "catalog_visibility": "visible",
                "manage_stock": True,
                "stock_status": "instock",
                "meta_keywords": True,
                "cross_sell_upsell": True
            },
            "ebay": {
                "listing_type": "FixedPriceItem",
                "duration": "GTC",
                "payment_methods": ["PayPal", "CreditCard"],
                "return_policy": "ReturnsAccepted",
                "shipping_type": "Calculated"
            }
        }
        
        return configs.get(platform, {})

# Example usage and integration functions

async def create_enhanced_amazon_integration():
    """Create enhanced Amazon integration instance"""
    
    credentials = AmazonCredentials(
        access_key="YOUR_ACCESS_KEY",
        secret_key="YOUR_SECRET_KEY", 
        partner_tag="YOUR_PARTNER_TAG",
        host="webservices.amazon.in",
        region="eu-west-1"
    )
    
    return AmazonDropshippingAutomation(credentials, markup_percentage=35.0)

async def demo_profitable_product_search():
    """Demo function to search for profitable products"""
    
    automation = await create_enhanced_amazon_integration()
    
    # Search for profitable products
    profitable_products = await automation.find_profitable_products(
        keywords=["wireless", "bluetooth", "headphones"],
        min_profit_margin=25.0,
        min_rating=4.0,
        max_results=20
    )
    
    print(f"Found {len(profitable_products)} profitable products:")
    
    for product_data in profitable_products[:5]:  # Show top 5
        product = product_data["product"]
        analysis = product_data["profit_analysis"]
        
        print(f"\n📦 {product.title[:50]}...")
        print(f"💰 Profit: ₹{analysis.profit_amount:.2f} ({analysis.profit_margin:.1f}%)")
        print(f"⭐ Rating: {product.rating}/5 ({product.review_count} reviews)")
        print(f"🎯 Score: {product_data['profitability_score']}/100")
        print(f"📊 Market: {product_data['market_potential']['level']}")
        print(f"🏆 Recommendation: {analysis.recommended_action}")

if __name__ == "__main__":
    # Run demo
    asyncio.run(demo_profitable_product_search())
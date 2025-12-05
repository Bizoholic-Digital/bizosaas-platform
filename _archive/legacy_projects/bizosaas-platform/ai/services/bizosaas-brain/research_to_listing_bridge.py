"""
Research-to-Listing Bridge Service for BizOSaaS Platform

Converts product research data into optimized Amazon listing format.
Handles data transformation, enhancement, and Amazon-specific formatting.
"""

import asyncio
import json
import logging
import re
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from decimal import Decimal
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AmazonListingData:
    """Complete Amazon listing data structure"""
    # Basic product information
    title: str
    description: str
    bullet_points: List[str]
    keywords: List[str]

    # Amazon-specific data
    product_type: str
    category_path: str
    brand_name: str
    manufacturer: str

    # Pricing and inventory
    price: Optional[Decimal] = None
    compare_at_price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None

    # Product specifications
    attributes: Dict[str, Any] = None
    variations: List[Dict[str, Any]] = None
    dimensions: Dict[str, float] = None
    weight: Optional[float] = None

    # Images and media
    main_image_url: Optional[str] = None
    additional_images: List[str] = None
    video_urls: List[str] = None

    # SEO and marketing
    search_terms: List[str] = None
    target_audience: List[str] = None
    intended_use: List[str] = None

    # Compliance and categorization
    age_restrictions: Optional[str] = None
    safety_warnings: List[str] = None
    certifications: List[str] = None

    # Metadata
    confidence_score: float = 0.0
    data_sources: List[str] = None
    generated_at: datetime = None

@dataclass
class ContentOptimization:
    """Content optimization parameters"""
    max_title_length: int = 200
    max_description_length: int = 2000
    max_bullet_points: int = 5
    max_search_terms: int = 250
    keyword_density_target: float = 0.02
    readability_target: str = "conversational"
    tone: str = "professional"
    target_market: str = "indian_consumers"

class ResearchToListingBridge:
    """Service to convert research data to Amazon listing format"""

    def __init__(self):
        self.content_optimization = ContentOptimization()
        self.amazon_categories = self._load_amazon_categories()
        self.product_types = self._load_product_types()

    async def convert_research_to_listing(
        self,
        research_data: Dict[str, Any],
        customization_params: Dict[str, Any] = None
    ) -> AmazonListingData:
        """Convert comprehensive research data to Amazon listing format"""

        logger.info("🔄 Converting research data to Amazon listing format")

        try:
            # Extract research components
            discovery_data = research_data.get("stage_2_discovery", {})
            trend_data = research_data.get("stage_1_trends", {})
            competition_data = research_data.get("stage_3_competition", {})
            profit_data = research_data.get("stage_4_profitability", {})
            quality_data = research_data.get("stage_5_quality_risk", {})

            # Get primary product data
            products = discovery_data.get("products", [])
            if not products:
                raise ValueError("No product data found in research results")

            primary_product = products[0]  # Use first/best product

            # Generate optimized content
            listing_data = await self._generate_listing_content(
                primary_product, research_data, customization_params
            )

            # Enhance with competitive intelligence
            listing_data = await self._enhance_with_competition_data(
                listing_data, competition_data
            )

            # Apply pricing strategy
            listing_data = await self._apply_pricing_strategy(
                listing_data, profit_data
            )

            # Optimize for Amazon algorithm
            listing_data = await self._optimize_for_amazon_algorithm(
                listing_data, trend_data
            )

            # Final validation and scoring
            listing_data.confidence_score = self._calculate_listing_confidence(
                listing_data, research_data
            )

            listing_data.generated_at = datetime.utcnow()
            listing_data.data_sources = ["product_research", "competitive_analysis", "trend_analysis"]

            logger.info(f"✅ Listing conversion completed with confidence score: {listing_data.confidence_score:.2f}")
            return listing_data

        except Exception as e:
            logger.error(f"❌ Failed to convert research to listing: {str(e)}")
            raise

    async def _generate_listing_content(
        self,
        primary_product: Dict[str, Any],
        research_data: Dict[str, Any],
        customization_params: Dict[str, Any] = None
    ) -> AmazonListingData:
        """Generate core listing content from product data"""

        # Extract basic product information
        base_title = primary_product.get("title", "")
        base_description = primary_product.get("description", "")
        base_price = primary_product.get("price", 0)

        # Generate optimized title
        optimized_title = await self._generate_optimized_title(
            base_title, primary_product, research_data
        )

        # Generate enhanced description
        enhanced_description = await self._generate_enhanced_description(
            base_description, primary_product, research_data
        )

        # Generate bullet points
        bullet_points = await self._generate_bullet_points(
            primary_product, research_data
        )

        # Extract and optimize keywords
        keywords = await self._extract_and_optimize_keywords(
            primary_product, research_data
        )

        # Determine category and product type
        category_path, product_type = await self._determine_category_and_type(
            primary_product, research_data
        )

        # Extract brand and manufacturer
        brand_name = primary_product.get("brand", "Generic")
        manufacturer = brand_name  # Default to brand name

        # Process attributes
        attributes = await self._process_product_attributes(
            primary_product, research_data
        )

        # Handle pricing
        pricing = self._process_pricing_data(primary_product, base_price)

        # Process images
        main_image, additional_images = self._process_image_data(primary_product)

        # Generate search terms
        search_terms = await self._generate_search_terms(keywords, primary_product)

        return AmazonListingData(
            title=optimized_title,
            description=enhanced_description,
            bullet_points=bullet_points,
            keywords=keywords,
            product_type=product_type,
            category_path=category_path,
            brand_name=brand_name,
            manufacturer=manufacturer,
            price=pricing["price"],
            compare_at_price=pricing["compare_price"],
            cost_price=pricing["cost_price"],
            attributes=attributes,
            main_image_url=main_image,
            additional_images=additional_images,
            search_terms=search_terms
        )

    async def _generate_optimized_title(
        self,
        base_title: str,
        product_data: Dict[str, Any],
        research_data: Dict[str, Any]
    ) -> str:
        """Generate SEO-optimized Amazon title"""

        # Extract key information
        brand = product_data.get("brand", "")
        category = product_data.get("category", "")
        key_features = product_data.get("features", [])

        # Get trending keywords from research
        trend_data = research_data.get("stage_1_trends", {})
        trending_keywords = []

        for keyword_trend in trend_data.get("social_media_trends", {}).values():
            if isinstance(keyword_trend, dict) and keyword_trend.get("overall_score", 0) > 60:
                trending_keywords.extend(keyword_trend.get("keywords", []))

        # Title optimization logic
        title_parts = []

        # Add brand if present and not already in title
        if brand and brand.lower() not in base_title.lower():
            title_parts.append(brand)

        # Clean and enhance base title
        cleaned_title = self._clean_title_text(base_title)
        title_parts.append(cleaned_title)

        # Add key trending keywords if not present
        for keyword in trending_keywords[:2]:  # Max 2 trending keywords
            if keyword.lower() not in " ".join(title_parts).lower():
                title_parts.append(keyword)

        # Add important features
        for feature in key_features[:2]:  # Max 2 key features
            if len(feature) <= 30 and feature.lower() not in " ".join(title_parts).lower():
                title_parts.append(feature)

        # Construct final title
        optimized_title = " | ".join(title_parts)

        # Ensure title meets Amazon requirements
        if len(optimized_title) > self.content_optimization.max_title_length:
            optimized_title = optimized_title[:self.content_optimization.max_title_length - 3] + "..."

        return optimized_title.strip()

    def _clean_title_text(self, title: str) -> str:
        """Clean and normalize title text"""
        if not title:
            return ""

        # Remove excessive punctuation and special characters
        cleaned = re.sub(r'[^\w\s\-\(\)&/]', '', title)

        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        # Capitalize properly
        cleaned = cleaned.title()

        return cleaned

    async def _generate_enhanced_description(
        self,
        base_description: str,
        product_data: Dict[str, Any],
        research_data: Dict[str, Any]
    ) -> str:
        """Generate enhanced product description with SEO optimization"""

        description_parts = []

        # Start with compelling opening
        opening = await self._generate_description_opening(product_data, research_data)
        description_parts.append(opening)

        # Add key benefits and features
        benefits = await self._extract_product_benefits(product_data, research_data)
        if benefits:
            description_parts.append("Key Benefits:")
            description_parts.extend([f"• {benefit}" for benefit in benefits])

        # Add detailed specifications
        specifications = self._extract_specifications(product_data)
        if specifications:
            description_parts.append("\nSpecifications:")
            for spec_name, spec_value in specifications.items():
                description_parts.append(f"• {spec_name}: {spec_value}")

        # Add usage instructions or applications
        usage_info = self._extract_usage_information(product_data)
        if usage_info:
            description_parts.append(f"\nUsage: {usage_info}")

        # Add quality assurance information
        quality_info = self._generate_quality_assurance_text(research_data)
        if quality_info:
            description_parts.append(f"\nQuality Assurance: {quality_info}")

        # Combine all parts
        enhanced_description = "\n\n".join(description_parts)

        # Ensure description meets Amazon requirements
        if len(enhanced_description) > self.content_optimization.max_description_length:
            enhanced_description = enhanced_description[:self.content_optimization.max_description_length - 3] + "..."

        return enhanced_description

    async def _generate_description_opening(
        self,
        product_data: Dict[str, Any],
        research_data: Dict[str, Any]
    ) -> str:
        """Generate compelling opening for product description"""

        title = product_data.get("title", "")
        category = product_data.get("category", "product")

        # Extract unique selling points from research
        competition_data = research_data.get("stage_3_competition", {})
        unique_features = competition_data.get("differentiation_opportunities", [])

        opening_templates = [
            f"Discover the perfect {category.lower()} that combines quality, functionality, and style.",
            f"Experience superior {category.lower()} performance with this carefully crafted solution.",
            f"Transform your {category.lower()} experience with this innovative and reliable choice."
        ]

        # Choose template based on available data
        base_opening = opening_templates[0]

        # Add unique selling points if available
        if unique_features:
            usp = unique_features[0] if isinstance(unique_features, list) else str(unique_features)
            base_opening += f" {usp}"

        return base_opening

    async def _extract_product_benefits(
        self,
        product_data: Dict[str, Any],
        research_data: Dict[str, Any]
    ) -> List[str]:
        """Extract and prioritize product benefits"""

        benefits = []

        # Extract from product features
        features = product_data.get("features", [])
        for feature in features[:5]:  # Top 5 features
            if len(feature) > 10:  # Skip very short features
                benefits.append(feature)

        # Extract from competitive analysis
        competition_data = research_data.get("stage_3_competition", {})
        advantages = competition_data.get("competitive_advantages", [])
        for advantage in advantages[:3]:  # Top 3 advantages
            if isinstance(advantage, str) and advantage not in benefits:
                benefits.append(advantage)

        # Extract from quality assessment
        quality_data = research_data.get("stage_5_quality_risk", {})
        quality_points = quality_data.get("quality_highlights", [])
        for point in quality_points[:2]:  # Top 2 quality points
            if isinstance(point, str) and point not in benefits:
                benefits.append(point)

        return benefits[:8]  # Maximum 8 benefits

    def _extract_specifications(self, product_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract product specifications"""

        specifications = {}

        # Get specifications from product data
        specs = product_data.get("specifications", {})
        if isinstance(specs, dict):
            for key, value in specs.items():
                if isinstance(value, (str, int, float)) and str(value).strip():
                    specifications[key.title()] = str(value)

        # Extract dimensions if available
        dimensions = product_data.get("dimensions", {})
        if isinstance(dimensions, dict):
            for dim_key, dim_value in dimensions.items():
                specifications[f"Dimension ({dim_key})"] = str(dim_value)

        # Extract weight
        weight = product_data.get("weight")
        if weight:
            specifications["Weight"] = str(weight)

        # Extract material information
        material = product_data.get("material")
        if material:
            specifications["Material"] = str(material)

        # Extract color/style information
        color = product_data.get("color")
        if color:
            specifications["Color"] = str(color)

        return specifications

    def _extract_usage_information(self, product_data: Dict[str, Any]) -> str:
        """Extract usage instructions or applications"""

        usage_info = []

        # Check for explicit usage instructions
        instructions = product_data.get("instructions", "")
        if instructions:
            usage_info.append(instructions)

        # Check for intended use
        intended_use = product_data.get("intended_use", [])
        if intended_use:
            if isinstance(intended_use, list):
                usage_info.extend(intended_use)
            else:
                usage_info.append(str(intended_use))

        # Check for applications
        applications = product_data.get("applications", [])
        if applications:
            if isinstance(applications, list):
                usage_info.extend(applications)
            else:
                usage_info.append(str(applications))

        return ". ".join(usage_info) if usage_info else ""

    def _generate_quality_assurance_text(self, research_data: Dict[str, Any]) -> str:
        """Generate quality assurance text from research"""

        quality_data = research_data.get("stage_5_quality_risk", {})
        quality_summary = quality_data.get("summary", {})

        quality_text_parts = []

        # Extract quality score information
        quality_score = quality_summary.get("average_quality", 0)
        if quality_score > 80:
            quality_text_parts.append("Premium quality verified through comprehensive analysis.")
        elif quality_score > 60:
            quality_text_parts.append("Good quality standards maintained and verified.")

        # Extract risk assessment
        risk_score = quality_summary.get("average_risk", 100)
        if risk_score < 30:
            quality_text_parts.append("Low-risk product with reliable performance track record.")

        # Extract recommended status
        recommended_products = quality_summary.get("recommended_products", 0)
        if recommended_products > 0:
            quality_text_parts.append("Recommended based on quality and performance analysis.")

        return " ".join(quality_text_parts)

    async def _generate_bullet_points(
        self,
        product_data: Dict[str, Any],
        research_data: Dict[str, Any]
    ) -> List[str]:
        """Generate Amazon bullet points"""

        bullet_points = []

        # Extract key features
        features = product_data.get("features", [])
        for feature in features[:3]:  # Top 3 features
            if len(feature) > 15:  # Skip very short features
                formatted_feature = f"✓ {feature}"
                bullet_points.append(formatted_feature)

        # Extract benefits from research
        benefits = await self._extract_product_benefits(product_data, research_data)
        for benefit in benefits[:2]:  # Top 2 benefits
            if benefit not in [bp.replace("✓ ", "") for bp in bullet_points]:
                formatted_benefit = f"⭐ {benefit}"
                bullet_points.append(formatted_benefit)

        # Add unique selling points
        competition_data = research_data.get("stage_3_competition", {})
        unique_points = competition_data.get("differentiation_opportunities", [])
        for point in unique_points[:1]:  # Top unique point
            if isinstance(point, str) and point not in [bp.replace("🎯 ", "") for bp in bullet_points]:
                formatted_point = f"🎯 {point}"
                bullet_points.append(formatted_point)

        # Ensure we have enough bullet points
        while len(bullet_points) < 3:
            generic_points = [
                "✓ High-quality construction for long-lasting durability",
                "⭐ Easy to use with user-friendly design",
                "🎯 Perfect for both personal and professional use"
            ]
            for generic in generic_points:
                if generic not in bullet_points:
                    bullet_points.append(generic)
                    break

        return bullet_points[:self.content_optimization.max_bullet_points]

    async def _extract_and_optimize_keywords(
        self,
        product_data: Dict[str, Any],
        research_data: Dict[str, Any]
    ) -> List[str]:
        """Extract and optimize keywords for Amazon SEO"""

        keywords = set()

        # Extract from product title and description
        title = product_data.get("title", "")
        description = product_data.get("description", "")

        title_keywords = self._extract_keywords_from_text(title)
        desc_keywords = self._extract_keywords_from_text(description)

        keywords.update(title_keywords)
        keywords.update(desc_keywords)

        # Extract from trend analysis
        trend_data = research_data.get("stage_1_trends", {})
        for keyword_trend in trend_data.get("social_media_trends", {}).values():
            if isinstance(keyword_trend, dict):
                trend_keywords = keyword_trend.get("keywords", [])
                keywords.update(trend_keywords)

        # Extract from competitive analysis
        competition_data = research_data.get("stage_3_competition", {})
        competitive_keywords = competition_data.get("top_keywords", [])
        keywords.update(competitive_keywords)

        # Extract category-related keywords
        category = product_data.get("category", "")
        if category:
            category_keywords = self._get_category_keywords(category)
            keywords.update(category_keywords)

        # Filter and prioritize keywords
        filtered_keywords = self._filter_and_prioritize_keywords(
            list(keywords), product_data, research_data
        )

        return filtered_keywords[:25]  # Amazon recommended limit

    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        if not text:
            return []

        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

        # Remove common stop words
        stop_words = {
            'the', 'and', 'for', 'with', 'this', 'that', 'from', 'are', 'was', 'will',
            'can', 'has', 'have', 'had', 'been', 'you', 'your', 'our', 'their', 'they',
            'when', 'where', 'what', 'how', 'why', 'who', 'which', 'than', 'more',
            'most', 'very', 'just', 'only', 'also', 'even', 'much', 'many', 'some'
        }

        keywords = [word for word in words if word not in stop_words and len(word) >= 3]

        # Return unique keywords
        return list(set(keywords))

    def _get_category_keywords(self, category: str) -> List[str]:
        """Get relevant keywords for product category"""

        category_keywords_map = {
            "electronics": ["electronic", "device", "gadget", "technology", "digital"],
            "clothing": ["apparel", "fashion", "wear", "style", "clothing"],
            "home": ["household", "domestic", "interior", "decor", "furniture"],
            "health": ["wellness", "fitness", "healthcare", "medical", "therapeutic"],
            "beauty": ["cosmetic", "skincare", "personal care", "grooming", "beauty"],
            "sports": ["athletic", "fitness", "exercise", "outdoor", "sports"],
            "toys": ["educational", "entertainment", "children", "kids", "play"],
            "books": ["educational", "reference", "literature", "reading", "knowledge"],
            "automotive": ["vehicle", "car", "auto", "driving", "transportation"]
        }

        category_lower = category.lower()
        for cat_key, keywords in category_keywords_map.items():
            if cat_key in category_lower:
                return keywords

        return [category.lower()]

    def _filter_and_prioritize_keywords(
        self,
        keywords: List[str],
        product_data: Dict[str, Any],
        research_data: Dict[str, Any]
    ) -> List[str]:
        """Filter and prioritize keywords based on relevance and search volume"""

        # Score keywords based on various factors
        keyword_scores = {}

        for keyword in keywords:
            score = 0

            # Length preference (3-15 characters optimal)
            if 3 <= len(keyword) <= 15:
                score += 10

            # Brand relevance
            brand = product_data.get("brand", "").lower()
            if brand and brand in keyword.lower():
                score += 20

            # Category relevance
            category = product_data.get("category", "").lower()
            if category and category in keyword.lower():
                score += 15

            # Trend analysis boost
            trend_data = research_data.get("stage_1_trends", {})
            trend_summary = trend_data.get("trend_summary", {})
            trending_keywords = trend_summary.get("trending_keywords", 0)
            if trending_keywords > 0:
                score += 5

            # Competition analysis boost
            competition_data = research_data.get("stage_3_competition", {})
            if keyword in str(competition_data):
                score += 8

            keyword_scores[keyword] = score

        # Sort by score and return top keywords
        sorted_keywords = sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)
        return [keyword for keyword, score in sorted_keywords]

    async def _determine_category_and_type(
        self,
        product_data: Dict[str, Any],
        research_data: Dict[str, Any]
    ) -> tuple[str, str]:
        """Determine Amazon category path and product type"""

        # Try to get category from product data
        base_category = product_data.get("category", "")

        # Map to Amazon category
        amazon_category = self._map_to_amazon_category(base_category, product_data)

        # Determine product type
        product_type = self._determine_product_type(amazon_category, product_data)

        return amazon_category, product_type

    def _map_to_amazon_category(self, base_category: str, product_data: Dict[str, Any]) -> str:
        """Map product category to Amazon category path"""

        # Amazon India category mappings
        category_mappings = {
            "electronics": "Electronics > Consumer Electronics",
            "mobile": "Electronics > Mobiles & Accessories",
            "computer": "Computers & Accessories",
            "clothing": "Clothing & Accessories",
            "shoes": "Shoes & Handbags",
            "home": "Home & Kitchen",
            "health": "Health & Personal Care",
            "beauty": "Beauty & Personal Care",
            "sports": "Sports, Fitness & Outdoors",
            "toys": "Toys & Games",
            "books": "Books",
            "automotive": "Car & Motorbike",
            "garden": "Garden & Outdoors",
            "jewelry": "Jewellery",
            "watches": "Watches"
        }

        category_lower = base_category.lower()

        # Find best matching category
        for key, amazon_path in category_mappings.items():
            if key in category_lower:
                return amazon_path

        # Default fallback
        return "Home & Kitchen > Generic"

    def _determine_product_type(self, amazon_category: str, product_data: Dict[str, Any]) -> str:
        """Determine Amazon product type based on category"""

        # Product type mappings
        type_mappings = {
            "Electronics": "ELECTRONICS",
            "Mobiles": "MOBILE_PHONE",
            "Computers": "COMPUTER",
            "Clothing": "APPAREL",
            "Shoes": "SHOES",
            "Home": "HOME",
            "Health": "HEALTH_PERSONAL_CARE",
            "Beauty": "BEAUTY",
            "Sports": "SPORTING_GOODS",
            "Toys": "TOYS_AND_GAMES",
            "Books": "BOOKS",
            "Car": "AUTOMOTIVE",
            "Garden": "LAWN_AND_GARDEN",
            "Jewellery": "JEWELRY",
            "Watches": "WATCH"
        }

        # Find matching product type
        for category_keyword, product_type in type_mappings.items():
            if category_keyword.lower() in amazon_category.lower():
                return product_type

        return "PRODUCT"  # Generic fallback

    async def _process_product_attributes(
        self,
        product_data: Dict[str, Any],
        research_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process and format product attributes for Amazon"""

        attributes = {}

        # Basic attributes
        brand = product_data.get("brand")
        if brand:
            attributes["brand"] = [{"value": brand, "language_tag": "en_IN"}]

        manufacturer = product_data.get("manufacturer") or brand
        if manufacturer:
            attributes["manufacturer"] = [{"value": manufacturer, "language_tag": "en_IN"}]

        # Dimensions and weight
        dimensions = product_data.get("dimensions", {})
        if dimensions:
            if "length" in dimensions:
                attributes["item_length"] = [{"value": dimensions["length"], "unit": "centimeters"}]
            if "width" in dimensions:
                attributes["item_width"] = [{"value": dimensions["width"], "unit": "centimeters"}]
            if "height" in dimensions:
                attributes["item_height"] = [{"value": dimensions["height"], "unit": "centimeters"}]

        weight = product_data.get("weight")
        if weight:
            attributes["item_weight"] = [{"value": weight, "unit": "grams"}]

        # Material and color
        material = product_data.get("material")
        if material:
            attributes["material_type"] = [{"value": material, "language_tag": "en_IN"}]

        color = product_data.get("color")
        if color:
            attributes["color"] = [{"value": color, "language_tag": "en_IN"}]

        # Additional specifications
        specifications = product_data.get("specifications", {})
        if isinstance(specifications, dict):
            for spec_key, spec_value in specifications.items():
                if isinstance(spec_value, (str, int, float)):
                    attr_key = spec_key.lower().replace(" ", "_")
                    attributes[attr_key] = [{"value": str(spec_value), "language_tag": "en_IN"}]

        return attributes

    def _process_pricing_data(self, product_data: Dict[str, Any], base_price: float) -> Dict[str, Optional[Decimal]]:
        """Process pricing information"""

        price = None
        compare_price = None
        cost_price = None

        try:
            if base_price and base_price > 0:
                price = Decimal(str(base_price))

                # Calculate compare at price (typically 10-20% higher)
                compare_price = price * Decimal('1.15')  # 15% markup

                # Estimate cost price (typically 60-70% of selling price)
                cost_price = price * Decimal('0.65')  # 65% of selling price

        except (ValueError, TypeError):
            logger.warning(f"Invalid price data: {base_price}")

        return {
            "price": price,
            "compare_price": compare_price,
            "cost_price": cost_price
        }

    def _process_image_data(self, product_data: Dict[str, Any]) -> tuple[Optional[str], List[str]]:
        """Process product image data"""

        images = product_data.get("images", [])
        if not images:
            return None, []

        # Use first image as main image
        main_image = images[0] if images else None

        # Additional images (excluding main image)
        additional_images = images[1:8] if len(images) > 1 else []  # Amazon allows up to 9 images total

        return main_image, additional_images

    async def _generate_search_terms(self, keywords: List[str], product_data: Dict[str, Any]) -> List[str]:
        """Generate search terms for Amazon internal search"""

        search_terms = set()

        # Add all keywords
        search_terms.update(keywords)

        # Add variations and synonyms
        for keyword in keywords[:10]:  # Process top 10 keywords
            variations = self._generate_keyword_variations(keyword)
            search_terms.update(variations)

        # Add brand and category terms
        brand = product_data.get("brand", "")
        if brand:
            search_terms.add(brand.lower())

        category = product_data.get("category", "")
        if category:
            search_terms.add(category.lower())

        # Convert to list and limit
        search_terms_list = list(search_terms)

        # Join terms to stay within character limit
        search_terms_string = " ".join(search_terms_list)
        if len(search_terms_string) > self.content_optimization.max_search_terms:
            # Truncate to fit within limit
            truncated = search_terms_string[:self.content_optimization.max_search_terms]
            # Split back to terms, removing incomplete last term
            search_terms_list = truncated.rsplit(' ', 1)[0].split(' ')

        return search_terms_list

    def _generate_keyword_variations(self, keyword: str) -> List[str]:
        """Generate variations of a keyword"""

        variations = []

        # Plural/singular variations
        if keyword.endswith('s'):
            variations.append(keyword[:-1])  # Remove 's'
        else:
            variations.append(keyword + 's')  # Add 's'

        # Common suffixes
        suffixes = ['ing', 'ed', 'er', 'ly']
        for suffix in suffixes:
            if not keyword.endswith(suffix) and len(keyword + suffix) <= 20:
                variations.append(keyword + suffix)

        # Remove original keyword if present
        variations = [v for v in variations if v != keyword]

        return variations[:3]  # Limit variations

    async def _enhance_with_competition_data(
        self,
        listing_data: AmazonListingData,
        competition_data: Dict[str, Any]
    ) -> AmazonListingData:
        """Enhance listing with competitive intelligence"""

        if not competition_data:
            return listing_data

        # Extract competitive advantages
        advantages = competition_data.get("competitive_advantages", [])
        if advantages:
            # Add to description
            competitive_text = f"\n\nCompetitive Advantages: {', '.join(advantages[:3])}"
            if len(listing_data.description + competitive_text) <= self.content_optimization.max_description_length:
                listing_data.description += competitive_text

        # Extract pricing insights
        pricing_insights = competition_data.get("pricing_analysis", {})
        if pricing_insights and listing_data.price:
            avg_competitor_price = pricing_insights.get("average_price", 0)
            if avg_competitor_price > 0:
                competitor_price = Decimal(str(avg_competitor_price))
                # Adjust compare_at_price based on competitive data
                listing_data.compare_at_price = max(listing_data.compare_at_price or 0, competitor_price * Decimal('1.1'))

        # Extract top keywords from competitors
        competitor_keywords = competition_data.get("top_keywords", [])
        if competitor_keywords:
            # Add unique competitive keywords
            for keyword in competitor_keywords[:5]:
                if keyword not in listing_data.keywords:
                    listing_data.keywords.append(keyword)

        return listing_data

    async def _apply_pricing_strategy(
        self,
        listing_data: AmazonListingData,
        profit_data: Dict[str, Any]
    ) -> AmazonListingData:
        """Apply pricing strategy based on profit analysis"""

        if not profit_data or not listing_data.price:
            return listing_data

        # Extract profit analysis results
        profit_analyses = profit_data.get("individual_analyses", [])
        if not profit_analyses:
            return listing_data

        # Get the first profit analysis (for primary product)
        profit_analysis = profit_analyses[0].get("profit_analysis", {})

        # Extract profit margin and pricing recommendations
        profit_margin = profit_analysis.get("profit_margin_percent", 0)
        recommended_price = profit_analysis.get("recommended_selling_price")

        if recommended_price and recommended_price > 0:
            listing_data.price = Decimal(str(recommended_price))

        # Adjust pricing based on profit margin
        if profit_margin < 20:  # Low margin
            # Increase price slightly for better profitability
            listing_data.price = listing_data.price * Decimal('1.05')
        elif profit_margin > 50:  # High margin
            # Consider competitive pricing
            listing_data.price = listing_data.price * Decimal('0.95')

        # Update compare_at_price accordingly
        if listing_data.price:
            listing_data.compare_at_price = listing_data.price * Decimal('1.15')

        return listing_data

    async def _optimize_for_amazon_algorithm(
        self,
        listing_data: AmazonListingData,
        trend_data: Dict[str, Any]
    ) -> AmazonListingData:
        """Optimize listing for Amazon's search algorithm"""

        if not trend_data:
            return listing_data

        # Extract trending keywords and adjust content
        trend_summary = trend_data.get("trend_summary", {})
        overall_trend_score = trend_summary.get("overall_trend_score", 0)

        if overall_trend_score > 60:  # Good trending score
            # Add trending indicator to title if space allows
            trending_suffix = " | Trending"
            if len(listing_data.title + trending_suffix) <= self.content_optimization.max_title_length:
                listing_data.title += trending_suffix

        # Extract and prioritize trending keywords
        trending_keywords = []
        for keyword_trend in trend_data.get("social_media_trends", {}).values():
            if isinstance(keyword_trend, dict) and keyword_trend.get("overall_score", 0) > 70:
                trending_keywords.extend(keyword_trend.get("keywords", []))

        # Add trending keywords to search terms
        for keyword in trending_keywords[:5]:
            if keyword not in listing_data.search_terms:
                listing_data.search_terms.append(keyword)

        # Optimize keyword density in description
        target_keywords = listing_data.keywords[:5]  # Top 5 keywords
        listing_data.description = self._optimize_keyword_density(
            listing_data.description, target_keywords
        )

        return listing_data

    def _optimize_keyword_density(self, description: str, target_keywords: List[str]) -> str:
        """Optimize keyword density in description"""

        if not description or not target_keywords:
            return description

        # Calculate current keyword density
        description_words = len(description.split())
        target_density = self.content_optimization.keyword_density_target

        for keyword in target_keywords:
            current_count = description.lower().count(keyword.lower())
            target_count = max(1, int(description_words * target_density))

            # Add keyword if under-represented
            if current_count < target_count:
                additions_needed = target_count - current_count
                for _ in range(min(additions_needed, 2)):  # Max 2 additional mentions
                    if len(description) < self.content_optimization.max_description_length - 50:
                        description += f" {keyword.title()}"

        return description

    def _calculate_listing_confidence(
        self,
        listing_data: AmazonListingData,
        research_data: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for the generated listing"""

        confidence_factors = []

        # Content completeness
        required_fields = [
            listing_data.title,
            listing_data.description,
            listing_data.bullet_points,
            listing_data.keywords,
            listing_data.category_path
        ]

        completeness = sum(1 for field in required_fields if field) / len(required_fields)
        confidence_factors.append(completeness)

        # Research data quality
        research_confidence = 0.0
        stage_weights = {
            "stage_1_trends": 0.2,
            "stage_2_discovery": 0.3,
            "stage_3_competition": 0.2,
            "stage_4_profitability": 0.3
        }

        for stage, weight in stage_weights.items():
            stage_data = research_data.get(stage, {})
            if stage_data and not stage_data.get("error"):
                research_confidence += weight

        confidence_factors.append(research_confidence)

        # Content quality indicators
        content_quality = 0.0

        # Title quality
        if listing_data.title and 50 <= len(listing_data.title) <= 200:
            content_quality += 0.25

        # Description quality
        if listing_data.description and len(listing_data.description) >= 200:
            content_quality += 0.25

        # Keywords quality
        if len(listing_data.keywords) >= 5:
            content_quality += 0.25

        # Bullet points quality
        if len(listing_data.bullet_points) >= 3:
            content_quality += 0.25

        confidence_factors.append(content_quality)

        # Price availability
        if listing_data.price and listing_data.price > 0:
            confidence_factors.append(1.0)
        else:
            confidence_factors.append(0.5)

        # Calculate overall confidence
        overall_confidence = sum(confidence_factors) / len(confidence_factors)
        return min(1.0, max(0.0, overall_confidence))

    def _load_amazon_categories(self) -> Dict[str, List[str]]:
        """Load Amazon category mappings"""
        # In production, this would load from a database or external service
        return {
            "electronics": ["Electronics", "Consumer Electronics"],
            "mobile": ["Electronics", "Mobiles & Accessories"],
            "computer": ["Computers & Accessories"],
            "clothing": ["Clothing & Accessories"],
            "home": ["Home & Kitchen"],
            "health": ["Health & Personal Care"],
            "beauty": ["Beauty & Personal Care"],
            "sports": ["Sports, Fitness & Outdoors"],
            "toys": ["Toys & Games"],
            "books": ["Books"],
            "automotive": ["Car & Motorbike"]
        }

    def _load_product_types(self) -> Dict[str, str]:
        """Load Amazon product type mappings"""
        # In production, this would load from a database or external service
        return {
            "electronics": "ELECTRONICS",
            "mobile": "MOBILE_PHONE",
            "computer": "COMPUTER",
            "clothing": "APPAREL",
            "home": "HOME",
            "health": "HEALTH_PERSONAL_CARE",
            "beauty": "BEAUTY",
            "sports": "SPORTING_GOODS",
            "toys": "TOYS_AND_GAMES",
            "books": "BOOKS",
            "automotive": "AUTOMOTIVE"
        }

# Export main classes
__all__ = ["ResearchToListingBridge", "AmazonListingData", "ContentOptimization"]
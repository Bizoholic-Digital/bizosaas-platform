#!/usr/bin/env python3
"""
Amazon Product Data Simulator
Realistic product data generator for testing the Amazon sourcing workflow

This module provides realistic Amazon product data simulation including:
- Product categories and subcategories
- Pricing models and variations
- Review patterns and ratings
- Image URLs and metadata
- Seller information
- Inventory status
"""

import random
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class ProductCategory(Enum):
    ELECTRONICS = "electronics"
    SPORTS_OUTDOORS = "sports_outdoors"
    HEALTH_PERSONAL_CARE = "health_personal_care"
    HOME_KITCHEN = "home_kitchen"
    CLOTHING_SHOES = "clothing_shoes"
    BOOKS = "books"
    TOYS_GAMES = "toys_games"
    AUTOMOTIVE = "automotive"

class PriceRange(Enum):
    BUDGET = (5.0, 25.0)
    AFFORDABLE = (25.0, 100.0)
    PREMIUM = (100.0, 500.0)
    LUXURY = (500.0, 2000.0)

@dataclass
class AmazonProductTemplate:
    category: ProductCategory
    subcategories: List[str]
    title_templates: List[str]
    description_templates: List[str]
    feature_templates: List[str]
    price_range: PriceRange
    common_brands: List[str]
    typical_ratings: tuple  # (min, max)
    review_count_range: tuple  # (min, max)

class AmazonProductSimulator:
    """Generates realistic Amazon product data for testing"""
    
    def __init__(self):
        self.product_templates = self._initialize_product_templates()
        self.seller_names = self._generate_seller_names()
        self.image_domains = ["images-na.ssl-images-amazon.com", "m.media-amazon.com", "images.unsplash.com"]
        
    def _initialize_product_templates(self) -> Dict[ProductCategory, AmazonProductTemplate]:
        """Initialize product templates for different categories"""
        return {
            ProductCategory.ELECTRONICS: AmazonProductTemplate(
                category=ProductCategory.ELECTRONICS,
                subcategories=[
                    "smartphones", "laptops", "tablets", "headphones", "speakers",
                    "smartwatches", "cameras", "gaming", "accessories", "smart_home"
                ],
                title_templates=[
                    "{brand} {product_type} - {feature1} with {feature2}",
                    "Premium {brand} {product_type} | {feature1} & {feature2}",
                    "{brand} {model} {product_type} - {feature1}, {feature2}",
                    "Professional {product_type} by {brand} - {feature1}"
                ],
                description_templates=[
                    "Experience cutting-edge technology with the {brand} {product_type}. "
                    "Featuring {feature1} and {feature2}, this device delivers exceptional performance "
                    "for both personal and professional use.",
                    "Discover the power of {brand}'s latest {product_type}. "
                    "With advanced {feature1} and innovative {feature2}, "
                    "you'll enjoy seamless connectivity and superior functionality.",
                ],
                feature_templates=[
                    "wireless connectivity", "long battery life", "fast charging", "water resistant",
                    "premium build quality", "advanced processor", "high-resolution display",
                    "noise cancellation", "touch controls", "voice assistant compatible"
                ],
                price_range=PriceRange.PREMIUM,
                common_brands=["Apple", "Samsung", "Sony", "LG", "HP", "Dell", "Asus", "Logitech"],
                typical_ratings=(3.8, 4.7),
                review_count_range=(50, 3000)
            ),
            
            ProductCategory.SPORTS_OUTDOORS: AmazonProductTemplate(
                category=ProductCategory.SPORTS_OUTDOORS,
                subcategories=[
                    "fitness", "outdoor_recreation", "sports_equipment", "exercise",
                    "camping", "cycling", "running", "yoga", "strength_training"
                ],
                title_templates=[
                    "{brand} {product_type} - {feature1} for {activity}",
                    "Professional {product_type} | {feature1} & {feature2}",
                    "{brand} Premium {product_type} - {feature1}",
                    "{activity} {product_type} with {feature1}"
                ],
                description_templates=[
                    "Elevate your {activity} experience with the {brand} {product_type}. "
                    "Designed for performance with {feature1} and {feature2}, "
                    "this equipment helps you achieve your fitness goals.",
                    "Take your {activity} to the next level. "
                    "This premium {product_type} features {feature1} and {feature2} "
                    "for maximum comfort and effectiveness."
                ],
                feature_templates=[
                    "ergonomic design", "durable construction", "adjustable settings",
                    "lightweight material", "anti-slip grip", "quick setup",
                    "portable design", "weather resistant", "easy storage"
                ],
                price_range=PriceRange.AFFORDABLE,
                common_brands=["Nike", "Adidas", "Under Armour", "Bowflex", "NordicTrack", "Spalding"],
                typical_ratings=(4.0, 4.6),
                review_count_range=(25, 1500)
            ),
            
            ProductCategory.HEALTH_PERSONAL_CARE: AmazonProductTemplate(
                category=ProductCategory.HEALTH_PERSONAL_CARE,
                subcategories=[
                    "skincare", "vitamins", "personal_hygiene", "beauty", "wellness",
                    "oral_care", "hair_care", "supplements", "medical_supplies"
                ],
                title_templates=[
                    "{brand} {product_type} - {feature1} Formula",
                    "Premium {product_type} with {feature1} & {feature2}",
                    "{brand} Professional {product_type} - {feature1}",
                    "Natural {product_type} | {feature1} for {benefit}"
                ],
                description_templates=[
                    "Transform your daily routine with {brand}'s {product_type}. "
                    "Formulated with {feature1} and {feature2}, "
                    "this product delivers visible results you can trust.",
                    "Experience the difference of professional-grade {product_type}. "
                    "Our {feature1} formula provides {benefit} for lasting confidence."
                ],
                feature_templates=[
                    "organic ingredients", "dermatologist tested", "paraben-free",
                    "hypoallergenic", "clinical strength", "natural extracts",
                    "vitamin enriched", "gentle formula", "fast absorbing"
                ],
                price_range=PriceRange.AFFORDABLE,
                common_brands=["CeraVe", "Neutrogena", "Olay", "L'Oreal", "Dove", "Johnson's"],
                typical_ratings=(4.1, 4.5),
                review_count_range=(100, 5000)
            ),
            
            ProductCategory.HOME_KITCHEN: AmazonProductTemplate(
                category=ProductCategory.HOME_KITCHEN,
                subcategories=[
                    "cookware", "appliances", "storage", "dining", "cleaning",
                    "decor", "organization", "bedding", "furniture", "lighting"
                ],
                title_templates=[
                    "{brand} {product_type} Set - {feature1} & {feature2}",
                    "Premium {product_type} | {feature1} Design",
                    "{brand} Professional {product_type} - {feature1}",
                    "Modern {product_type} with {feature1}"
                ],
                description_templates=[
                    "Upgrade your home with the {brand} {product_type}. "
                    "Featuring {feature1} and {feature2}, "
                    "this collection combines style with functionality.",
                    "Create the perfect space with our premium {product_type}. "
                    "The {feature1} design and {feature2} make this an essential addition."
                ],
                feature_templates=[
                    "dishwasher safe", "non-stick coating", "space saving",
                    "easy clean", "durable construction", "modern design",
                    "stackable", "heat resistant", "ergonomic handles"
                ],
                price_range=PriceRange.AFFORDABLE,
                common_brands=["KitchenAid", "Cuisinart", "OXO", "Pyrex", "Rubbermaid", "Hamilton Beach"],
                typical_ratings=(4.2, 4.6),
                review_count_range=(75, 2000)
            )
        }
    
    def _generate_seller_names(self) -> List[str]:
        """Generate realistic seller names"""
        prefixes = ["Amazon", "Prime", "Global", "Direct", "Express", "Quality", "Best", "Top"]
        suffixes = ["Store", "Shop", "Outlet", "Deals", "Plus", "Pro", "Market", "Supply"]
        
        sellers = ["Amazon.com", "Amazon Warehouse"]  # Official Amazon sellers
        
        # Generate third-party sellers
        for _ in range(20):
            prefix = random.choice(prefixes)
            suffix = random.choice(suffixes)
            sellers.append(f"{prefix} {suffix}")
        
        return sellers
    
    def generate_product(self, 
                        category: Optional[ProductCategory] = None,
                        asin: Optional[str] = None,
                        price_range: Optional[PriceRange] = None) -> Dict[str, Any]:
        """Generate a single realistic Amazon product"""
        
        if category is None:
            category = random.choice(list(ProductCategory))
        
        template = self.product_templates[category]
        
        if asin is None:
            asin = self._generate_asin()
        
        if price_range is None:
            price_range = template.price_range
        
        # Generate basic product info
        brand = random.choice(template.common_brands)
        subcategory = random.choice(template.subcategories)
        product_type = subcategory.replace('_', ' ').title()
        
        # Select features
        selected_features = random.sample(template.feature_templates, min(3, len(template.feature_templates)))
        feature1, feature2 = selected_features[0], selected_features[1]
        
        # Generate title
        title_template = random.choice(template.title_templates)
        title = title_template.format(
            brand=brand,
            product_type=product_type,
            feature1=feature1,
            feature2=feature2,
            model=f"{brand[0]}{random.randint(100, 999)}",
            activity=subcategory.replace('_', ' ')
        )
        
        # Generate description
        desc_template = random.choice(template.description_templates)
        description = desc_template.format(
            brand=brand,
            product_type=product_type.lower(),
            feature1=feature1,
            feature2=feature2,
            activity=subcategory.replace('_', ' '),
            benefit="enhanced results"
        )
        
        # Generate pricing
        price_min, price_max = price_range.value
        base_price = round(random.uniform(price_min, price_max), 2)
        
        # Apply discounts occasionally
        has_discount = random.random() < 0.3
        if has_discount:
            discount_percent = random.randint(5, 30)
            discounted_price = round(base_price * (1 - discount_percent/100), 2)
            list_price = base_price
            current_price = discounted_price
        else:
            list_price = base_price
            current_price = base_price
        
        # Generate ratings and reviews
        rating_min, rating_max = template.typical_ratings
        rating = round(random.uniform(rating_min, rating_max), 1)
        
        review_min, review_max = template.review_count_range
        review_count = random.randint(review_min, review_max)
        
        # Generate seller info
        is_amazon_seller = random.random() < 0.4  # 40% chance of Amazon as seller
        if is_amazon_seller:
            seller_name = "Amazon.com" if random.random() < 0.7 else "Amazon Warehouse"
            seller_rating = 5.0
            prime_eligible = True
        else:
            seller_name = random.choice(self.seller_names)
            seller_rating = round(random.uniform(3.5, 4.9), 1)
            prime_eligible = random.random() < 0.6
        
        # Generate images
        images = self._generate_product_images(asin, subcategory)
        
        # Generate availability
        availability_options = [
            "In Stock", "In Stock", "In Stock",  # Most common
            "Only 3 left in stock", "Only 1 left in stock",
            "Usually ships within 1-2 days",
            "Temporarily out of stock"
        ]
        availability = random.choice(availability_options)
        
        # Generate shipping options
        shipping_options = []
        if prime_eligible:
            shipping_options.append("FREE Prime delivery")
        shipping_options.append("FREE Standard shipping")
        if current_price > 25:
            shipping_options.append("FREE shipping on orders over $25")
        
        return {
            "id": str(uuid.uuid4()),
            "asin": asin,
            "title": title,
            "description": description,
            "category": category.value,
            "subcategory": subcategory,
            "brand": brand,
            "price": {
                "current": current_price,
                "list": list_price,
                "currency": "USD",
                "discount_percent": round((list_price - current_price) / list_price * 100, 1) if has_discount else 0
            },
            "rating": rating,
            "review_count": review_count,
            "images": images,
            "features": selected_features,
            "seller": {
                "name": seller_name,
                "rating": seller_rating,
                "fulfilled_by_amazon": is_amazon_seller or random.random() < 0.3,
                "prime_eligible": prime_eligible
            },
            "availability": availability,
            "shipping": shipping_options,
            "product_details": self._generate_product_details(category, subcategory),
            "keywords": self._generate_keywords(title, brand, subcategory),
            "created_at": datetime.utcnow().isoformat(),
            "last_updated": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat()
        }
    
    def _generate_asin(self) -> str:
        """Generate realistic Amazon ASIN"""
        # ASINs are 10 character alphanumeric codes
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return "B" + "".join(random.choices(chars, k=9))  # Most ASINs start with 'B'
    
    def _generate_product_images(self, asin: str, subcategory: str) -> List[str]:
        """Generate realistic product image URLs"""
        domain = random.choice(self.image_domains)
        image_count = random.randint(3, 8)
        
        images = []
        for i in range(image_count):
            # Simulate different image types
            image_types = ["main", "alt", "detail", "lifestyle", "packaging"]
            image_type = image_types[i] if i < len(image_types) else "alt"
            
            # Generate realistic image URL
            image_url = f"https://{domain}/images/I/{asin}_{image_type}_{i+1}.jpg"
            images.append({
                "url": image_url,
                "type": image_type,
                "width": random.choice([500, 679, 1000, 1500]),
                "height": random.choice([375, 500, 679, 1000])
            })
        
        return images
    
    def _generate_product_details(self, category: ProductCategory, subcategory: str) -> Dict[str, Any]:
        """Generate category-specific product details"""
        common_details = {
            "package_dimensions": f"{random.randint(5, 20)} x {random.randint(5, 20)} x {random.randint(2, 10)} inches",
            "item_weight": f"{random.uniform(0.5, 10):.1f} pounds",
            "customer_reviews": f"{random.uniform(4.0, 4.8):.1f} out of 5 stars",
            "best_sellers_rank": f"#{random.randint(100, 50000):,} in {category.value.replace('_', ' ').title()}"
        }
        
        # Add category-specific details
        if category == ProductCategory.ELECTRONICS:
            common_details.update({
                "batteries": "1 Lithium ion batteries required" if random.random() < 0.6 else "No batteries required",
                "warranty": f"{random.choice(['1 year', '2 years', '90 days'])} limited warranty",
                "connectivity": random.choice(["Bluetooth", "WiFi", "USB", "Wireless"])
            })
        elif category == ProductCategory.SPORTS_OUTDOORS:
            common_details.update({
                "material": random.choice(["Stainless Steel", "Aluminum", "Plastic", "Rubber", "Fabric"]),
                "activity": subcategory.replace('_', ' ').title(),
                "skill_level": random.choice(["Beginner", "Intermediate", "Advanced", "All Levels"])
            })
        elif category == ProductCategory.HEALTH_PERSONAL_CARE:
            common_details.update({
                "ingredients": "See product label for complete ingredient list",
                "skin_type": random.choice(["All Skin Types", "Sensitive Skin", "Dry Skin", "Oily Skin"]),
                "dermatologist_tested": random.choice([True, False])
            })
        
        return common_details
    
    def _generate_keywords(self, title: str, brand: str, subcategory: str) -> List[str]:
        """Generate SEO keywords for the product"""
        keywords = []
        
        # Extract keywords from title
        title_words = [word.lower() for word in title.split() if len(word) > 3]
        keywords.extend(title_words[:5])
        
        # Add brand keywords
        keywords.append(brand.lower())
        keywords.append(f"{brand.lower()} products")
        
        # Add category keywords
        keywords.append(subcategory.replace('_', ' '))
        keywords.append(f"best {subcategory.replace('_', ' ')}")
        keywords.append(f"buy {subcategory.replace('_', ' ')}")
        
        # Add generic commerce keywords
        commercial_keywords = [
            "best price", "on sale", "discount", "deal", "free shipping",
            "amazon choice", "highly rated", "customer favorite"
        ]
        keywords.extend(random.sample(commercial_keywords, 3))
        
        return list(set(keywords))  # Remove duplicates
    
    def generate_product_batch(self, 
                              count: int,
                              category: Optional[ProductCategory] = None,
                              price_range: Optional[PriceRange] = None) -> List[Dict[str, Any]]:
        """Generate a batch of products"""
        products = []
        
        for _ in range(count):
            # Vary categories if not specified
            selected_category = category or random.choice(list(ProductCategory))
            product = self.generate_product(selected_category, price_range=price_range)
            products.append(product)
        
        return products
    
    def generate_category_products(self, 
                                  category: ProductCategory,
                                  count: int = 10) -> List[Dict[str, Any]]:
        """Generate products for a specific category"""
        return self.generate_product_batch(count, category)
    
    def simulate_search_results(self, 
                               search_query: str,
                               max_results: int = 20) -> List[Dict[str, Any]]:
        """Simulate Amazon search results for a query"""
        # Simple simulation based on query keywords
        query_lower = search_query.lower()
        
        # Determine likely category based on query
        category_mapping = {
            "electronics": ProductCategory.ELECTRONICS,
            "phone": ProductCategory.ELECTRONICS,
            "laptop": ProductCategory.ELECTRONICS,
            "fitness": ProductCategory.SPORTS_OUTDOORS,
            "sports": ProductCategory.SPORTS_OUTDOORS,
            "exercise": ProductCategory.SPORTS_OUTDOORS,
            "skincare": ProductCategory.HEALTH_PERSONAL_CARE,
            "health": ProductCategory.HEALTH_PERSONAL_CARE,
            "kitchen": ProductCategory.HOME_KITCHEN,
            "home": ProductCategory.HOME_KITCHEN
        }
        
        target_category = None
        for keyword, cat in category_mapping.items():
            if keyword in query_lower:
                target_category = cat
                break
        
        # Generate relevant products
        products = self.generate_product_batch(max_results, target_category)
        
        # Sort by relevance (simulated by rating * review_count)
        for product in products:
            relevance_score = product["rating"] * min(product["review_count"] / 1000, 5)
            # Boost score if title contains query terms
            title_words = product["title"].lower().split()
            query_words = query_lower.split()
            title_match_score = sum(1 for word in query_words if any(word in title_word for title_word in title_words))
            relevance_score += title_match_score * 10
            product["_relevance_score"] = relevance_score
        
        # Sort by relevance and return
        products.sort(key=lambda x: x.get("_relevance_score", 0), reverse=True)
        
        # Remove internal relevance score before returning
        for product in products:
            product.pop("_relevance_score", None)
        
        return products
    
    def save_products_to_file(self, products: List[Dict[str, Any]], filename: str):
        """Save generated products to JSON file"""
        with open(filename, 'w') as f:
            json.dump({
                "generated_at": datetime.utcnow().isoformat(),
                "product_count": len(products),
                "products": products
            }, f, indent=2)

# Example usage and testing
if __name__ == "__main__":
    simulator = AmazonProductSimulator()
    
    print("🏪 Amazon Product Simulator - Testing")
    print("=" * 50)
    
    # Generate sample products
    print("Generating electronics products...")
    electronics = simulator.generate_category_products(ProductCategory.ELECTRONICS, 3)
    
    print("Generating sports products...")
    sports = simulator.generate_category_products(ProductCategory.SPORTS_OUTDOORS, 3)
    
    print("Simulating search results...")
    search_results = simulator.simulate_search_results("wireless headphones", 5)
    
    # Display samples
    print(f"\n📱 Sample Electronics Product:")
    print(f"Title: {electronics[0]['title']}")
    print(f"Price: ${electronics[0]['price']['current']}")
    print(f"Rating: {electronics[0]['rating']} ({electronics[0]['review_count']} reviews)")
    print(f"ASIN: {electronics[0]['asin']}")
    
    print(f"\n🏃 Sample Sports Product:")
    print(f"Title: {sports[0]['title']}")
    print(f"Price: ${sports[0]['price']['current']}")
    print(f"Rating: {sports[0]['rating']} ({sports[0]['review_count']} reviews)")
    
    print(f"\n🔍 Search Results Sample:")
    print(f"Query: 'wireless headphones'")
    print(f"Results: {len(search_results)} products")
    print(f"Top result: {search_results[0]['title']}")
    
    # Save to file
    all_products = electronics + sports + search_results
    simulator.save_products_to_file(all_products, "/tmp/amazon-products-sample.json")
    print(f"\n💾 Saved {len(all_products)} products to /tmp/amazon-products-sample.json")
    
    print("\n✅ Amazon Product Simulator test completed!")
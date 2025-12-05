"""
Advanced Saleor GraphQL Integration for Amazon Sourcing Workflow
Comprehensive product management, categories, variants, and inventory
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Union
from decimal import Decimal
from datetime import datetime, timezone
import httpx
import uuid
import base64
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SaleorProductInput:
    """Input data for Saleor product creation"""
    name: str
    description: str
    product_type_id: str
    category_id: Optional[str] = None
    collections: List[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    slug: Optional[str] = None
    weight: Optional[Decimal] = None
    is_published: bool = False
    visible_in_listings: bool = True
    metadata: Dict[str, str] = None
    private_metadata: Dict[str, str] = None

@dataclass
class SaleorVariantInput:
    """Input data for Saleor product variant"""
    sku: Optional[str] = None
    price: Decimal = None
    cost_price: Optional[Decimal] = None
    track_inventory: bool = True
    weight: Optional[Decimal] = None
    attributes: Dict[str, str] = None
    stocks: List[Dict[str, Any]] = None

@dataclass
class SaleorImageInput:
    """Input data for Saleor product image"""
    image_url: str
    alt_text: Optional[str] = None
    sort_order: int = 0

class SaleorGraphQLClient:
    """Advanced Saleor GraphQL client for Amazon sourcing integration"""
    
    def __init__(self, base_url: str = "http://localhost:8024", api_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.graphql_url = f"{self.base_url}/graphql/"
        self.api_token = api_token
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if api_token:
            headers['Authorization'] = f'Bearer {api_token}'
        
        self.client = httpx.AsyncClient(
            base_url=self.graphql_url,
            headers=headers,
            timeout=30.0
        )
        
        # Cache for frequently accessed data
        self._category_cache = {}
        self._product_type_cache = {}
        self._attribute_cache = {}
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute GraphQL query with error handling"""
        try:
            payload = {
                'query': query,
                'variables': variables or {}
            }
            
            response = await self.client.post('/', json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('errors'):
                logger.error(f"GraphQL errors: {result['errors']}")
                raise ValueError(f"GraphQL errors: {result['errors']}")
            
            return result.get('data', {})
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error executing GraphQL query: {e}")
            raise
        except Exception as e:
            logger.error(f"Error executing GraphQL query: {e}")
            raise
    
    async def get_shop_info(self) -> Dict[str, Any]:
        """Get basic shop information"""
        query = """
        query GetShopInfo {
            shop {
                name
                description
                domain {
                    host
                    url
                }
                defaultCountry {
                    code
                    country
                }
                defaultCurrency
                languages {
                    code
                    languageName
                }
                permissions {
                    code
                    name
                }
            }
        }
        """
        
        result = await self.execute_query(query)
        return result.get('shop', {})
    
    async def get_categories(self) -> List[Dict[str, Any]]:
        """Get all product categories"""
        if self._category_cache:
            return self._category_cache
        
        query = """
        query GetCategories {
            categories(first: 100) {
                edges {
                    node {
                        id
                        name
                        slug
                        description
                        seoTitle
                        seoDescription
                        level
                        parent {
                            id
                            name
                        }
                        children(first: 20) {
                            edges {
                                node {
                                    id
                                    name
                                    slug
                                }
                            }
                        }
                    }
                }
            }
        }
        """
        
        result = await self.execute_query(query)
        categories = [edge['node'] for edge in result.get('categories', {}).get('edges', [])]
        
        self._category_cache = categories
        return categories
    
    async def get_product_types(self) -> List[Dict[str, Any]]:
        """Get all product types"""
        if self._product_type_cache:
            return self._product_type_cache
        
        query = """
        query GetProductTypes {
            productTypes(first: 100) {
                edges {
                    node {
                        id
                        name
                        slug
                        hasVariants
                        isShippingRequired
                        weight {
                            unit
                            value
                        }
                        productAttributes {
                            id
                            name
                            slug
                            type
                            inputType
                            choices(first: 20) {
                                edges {
                                    node {
                                        id
                                        name
                                        value
                                    }
                                }
                            }
                        }
                        variantAttributes {
                            id
                            name
                            slug
                            type
                            inputType
                        }
                    }
                }
            }
        }
        """
        
        result = await self.execute_query(query)
        product_types = [edge['node'] for edge in result.get('productTypes', {}).get('edges', [])]
        
        self._product_type_cache = product_types
        return product_types
    
    async def create_category_if_not_exists(self, name: str, parent_id: Optional[str] = None) -> str:
        """Create category if it doesn't exist, return category ID"""
        # Check if category exists
        categories = await self.get_categories()
        
        for category in categories:
            if category['name'].lower() == name.lower():
                return category['id']
        
        # Create new category
        mutation = """
        mutation CreateCategory($input: CategoryInput!) {
            categoryCreate(input: $input) {
                category {
                    id
                    name
                    slug
                }
                errors {
                    field
                    message
                    code
                }
            }
        }
        """
        
        variables = {
            'input': {
                'name': name,
                'slug': name.lower().replace(' ', '-').replace('_', '-'),
                'description': f'Auto-created category for {name}',
                'parent': parent_id
            }
        }
        
        result = await self.execute_query(mutation, variables)
        
        category_result = result.get('categoryCreate', {})
        
        if category_result.get('errors'):
            raise ValueError(f"Failed to create category: {category_result['errors']}")
        
        category = category_result.get('category', {})
        category_id = category.get('id')
        
        logger.info(f"✅ Created category: {name} (ID: {category_id})")
        
        # Update cache
        self._category_cache.append(category)
        
        return category_id
    
    async def create_product(self, product_input: SaleorProductInput) -> Dict[str, Any]:
        """Create a new product in Saleor"""
        logger.info(f"🏪 Creating Saleor product: {product_input.name}")
        
        # Ensure category exists
        category_id = product_input.category_id
        if not category_id and 'Electronics' not in [cat['name'] for cat in await self.get_categories()]:
            category_id = await self.create_category_if_not_exists('Electronics')
        
        mutation = """
        mutation CreateProduct($input: ProductCreateInput!) {
            productCreate(input: $input) {
                product {
                    id
                    name
                    slug
                    description
                    isPublished
                    visibleInListings
                    seoTitle
                    seoDescription
                    category {
                        id
                        name
                    }
                    productType {
                        id
                        name
                    }
                    defaultVariant {
                        id
                        sku
                        name
                    }
                    metadata {
                        key
                        value
                    }
                    privateMetadata {
                        key
                        value
                    }
                    created
                    updatedAt
                }
                errors {
                    field
                    message
                    code
                }
            }
        }
        """
        
        # Build input object
        input_data = {
            'name': product_input.name,
            'description': product_input.description or '',
            'productType': product_input.product_type_id,
            'isPublished': product_input.is_published,
            'visibleInListings': product_input.visible_in_listings
        }
        
        if category_id:
            input_data['category'] = category_id
        
        if product_input.collections:
            input_data['collections'] = product_input.collections
        
        if product_input.seo_title:
            input_data['seo'] = {
                'title': product_input.seo_title,
                'description': product_input.seo_description or ''
            }
        
        if product_input.slug:
            input_data['slug'] = product_input.slug
        
        if product_input.weight:
            input_data['weight'] = float(product_input.weight)
        
        if product_input.metadata:
            input_data['metadata'] = [
                {'key': k, 'value': v} for k, v in product_input.metadata.items()
            ]
        
        if product_input.private_metadata:
            input_data['privateMetadata'] = [
                {'key': k, 'value': v} for k, v in product_input.private_metadata.items()
            ]
        
        variables = {'input': input_data}
        
        result = await self.execute_query(mutation, variables)
        
        product_result = result.get('productCreate', {})
        
        if product_result.get('errors'):
            raise ValueError(f"Failed to create product: {product_result['errors']}")
        
        product = product_result.get('product', {})
        product_id = product.get('id')
        
        logger.info(f"✅ Created product: {product_input.name} (ID: {product_id})")
        
        return product
    
    async def create_product_variant(
        self, 
        product_id: str, 
        variant_input: SaleorVariantInput
    ) -> Dict[str, Any]:
        """Create a product variant"""
        logger.info(f"🔧 Creating product variant for product: {product_id}")
        
        mutation = """
        mutation CreateProductVariant($input: ProductVariantCreateInput!) {
            productVariantCreate(input: $input) {
                productVariant {
                    id
                    name
                    sku
                    product {
                        id
                        name
                    }
                    pricing {
                        price {
                            gross {
                                amount
                                currency
                            }
                        }
                    }
                    costPrice {
                        amount
                        currency
                    }
                    trackInventory
                    weight {
                        unit
                        value
                    }
                    attributes {
                        attribute {
                            id
                            name
                        }
                        values {
                            id
                            name
                            value
                        }
                    }
                    stocks {
                        id
                        warehouse {
                            id
                            name
                        }
                        quantity
                        quantityAllocated
                    }
                    created
                }
                errors {
                    field
                    message
                    code
                }
            }
        }
        """
        
        # Build input object
        input_data = {
            'product': product_id
        }
        
        if variant_input.sku:
            input_data['sku'] = variant_input.sku
        
        if variant_input.price:
            input_data['price'] = float(variant_input.price)
        
        if variant_input.cost_price:
            input_data['costPrice'] = float(variant_input.cost_price)
        
        if variant_input.track_inventory is not None:
            input_data['trackInventory'] = variant_input.track_inventory
        
        if variant_input.weight:
            input_data['weight'] = float(variant_input.weight)
        
        if variant_input.attributes:
            input_data['attributes'] = [
                {'id': attr_id, 'values': [value]} 
                for attr_id, value in variant_input.attributes.items()
            ]
        
        if variant_input.stocks:
            input_data['stocks'] = variant_input.stocks
        
        variables = {'input': input_data}
        
        result = await self.execute_query(mutation, variables)
        
        variant_result = result.get('productVariantCreate', {})
        
        if variant_result.get('errors'):
            raise ValueError(f"Failed to create variant: {variant_result['errors']}")
        
        variant = variant_result.get('productVariant', {})
        variant_id = variant.get('id')
        
        logger.info(f"✅ Created product variant (ID: {variant_id})")
        
        return variant
    
    async def upload_product_image(
        self, 
        product_id: str, 
        image_input: SaleorImageInput
    ) -> Dict[str, Any]:
        """Upload product image from URL"""
        logger.info(f"🖼️ Uploading product image: {image_input.image_url}")
        
        mutation = """
        mutation CreateProductImage($input: ProductImageCreateInput!) {
            productImageCreate(input: $input) {
                productImage {
                    id
                    url
                    alt
                    sortOrder
                    product {
                        id
                        name
                    }
                }
                errors {
                    field
                    message
                    code
                }
            }
        }
        """
        
        # Download image and convert to base64 (for demo purposes)
        # In production, you'd handle this more efficiently
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(image_input.image_url, timeout=10.0)
                response.raise_for_status()
                
                # Convert image to base64
                image_data = base64.b64encode(response.content).decode('utf-8')
                
                # Determine content type
                content_type = response.headers.get('content-type', 'image/jpeg')
                
                # Create data URI
                image_data_uri = f"data:{content_type};base64,{image_data}"
        
        except Exception as e:
            logger.error(f"Failed to download image: {e}")
            raise ValueError(f"Failed to download image from {image_input.image_url}: {e}")
        
        input_data = {
            'product': product_id,
            'image': image_data_uri,
            'alt': image_input.alt_text or ''
        }
        
        variables = {'input': input_data}
        
        result = await self.execute_query(mutation, variables)
        
        image_result = result.get('productImageCreate', {})
        
        if image_result.get('errors'):
            logger.warning(f"Failed to create image: {image_result['errors']}")
            # Don't fail the entire workflow for image upload failures
            return None
        
        image = image_result.get('productImage', {})
        image_id = image.get('id')
        
        logger.info(f"✅ Uploaded product image (ID: {image_id})")
        
        return image
    
    async def update_product_seo(
        self, 
        product_id: str, 
        seo_title: str, 
        seo_description: str
    ) -> Dict[str, Any]:
        """Update product SEO information"""
        logger.info(f"🔍 Updating SEO for product: {product_id}")
        
        mutation = """
        mutation UpdateProductSeo($id: ID!, $input: SeoInput!) {
            productUpdate(id: $id, input: { seo: $input }) {
                product {
                    id
                    seoTitle
                    seoDescription
                }
                errors {
                    field
                    message
                    code
                }
            }
        }
        """
        
        variables = {
            'id': product_id,
            'input': {
                'title': seo_title,
                'description': seo_description
            }
        }
        
        result = await self.execute_query(mutation, variables)
        
        update_result = result.get('productUpdate', {})
        
        if update_result.get('errors'):
            logger.warning(f"Failed to update SEO: {update_result['errors']}")
            return None
        
        product = update_result.get('product', {})
        
        logger.info(f"✅ Updated SEO for product: {product_id}")
        
        return product
    
    async def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get product details by ID"""
        query = """
        query GetProduct($id: ID!) {
            product(id: $id) {
                id
                name
                slug
                description
                isPublished
                visibleInListings
                seoTitle
                seoDescription
                category {
                    id
                    name
                }
                productType {
                    id
                    name
                }
                variants {
                    id
                    name
                    sku
                    pricing {
                        price {
                            gross {
                                amount
                                currency
                            }
                        }
                    }
                }
                images {
                    id
                    url
                    alt
                }
                metadata {
                    key
                    value
                }
                created
                updatedAt
            }
        }
        """
        
        variables = {'id': product_id}
        result = await self.execute_query(query, variables)
        
        return result.get('product')
    
    async def search_products(
        self, 
        search_term: Optional[str] = None,
        category_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for products"""
        query = """
        query SearchProducts($search: String, $category: ID, $first: Int) {
            products(filter: { search: $search, categories: [$category] }, first: $first) {
                edges {
                    node {
                        id
                        name
                        slug
                        description
                        isPublished
                        category {
                            id
                            name
                        }
                        defaultVariant {
                            id
                            pricing {
                                price {
                                    gross {
                                        amount
                                        currency
                                    }
                                }
                            }
                        }
                        thumbnail {
                            url
                        }
                        created
                    }
                }
            }
        }
        """
        
        variables = {
            'search': search_term,
            'category': category_id,
            'first': limit
        }
        
        result = await self.execute_query(query, variables)
        
        return [edge['node'] for edge in result.get('products', {}).get('edges', [])]
    
    async def get_warehouses(self) -> List[Dict[str, Any]]:
        """Get available warehouses for stock management"""
        query = """
        query GetWarehouses {
            warehouses(first: 20) {
                edges {
                    node {
                        id
                        name
                        slug
                        email
                        isPrivate
                        address {
                            streetAddress1
                            city
                            country {
                                code
                                country
                            }
                        }
                    }
                }
            }
        }
        """
        
        result = await self.execute_query(query)
        return [edge['node'] for edge in result.get('warehouses', {}).get('edges', [])]

# Helper functions for Amazon sourcing workflow integration

async def create_amazon_sourced_product(
    client: SaleorGraphQLClient,
    amazon_data: Dict[str, Any],
    ai_enhancements: Dict[str, Any],
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a complete product in Saleor from Amazon data with AI enhancements
    """
    logger.info("🚀 Creating Amazon-sourced product in Saleor")
    
    try:
        # Get default product type
        product_types = await client.get_product_types()
        default_product_type = next(
            (pt for pt in product_types if pt['name'].lower() in ['default', 'simple']),
            product_types[0] if product_types else None
        )
        
        if not default_product_type:
            raise ValueError("No product types found in Saleor")
        
        # Prepare product input
        product_name = ai_enhancements.get('optimized_title', amazon_data.get('title', 'Untitled Product'))
        product_description = ai_enhancements.get('seo_description', amazon_data.get('description', ''))
        
        product_input = SaleorProductInput(
            name=product_name,
            description=product_description,
            product_type_id=default_product_type['id'],
            seo_title=ai_enhancements.get('optimized_title'),
            seo_description=ai_enhancements.get('seo_description'),
            slug=product_name.lower().replace(' ', '-').replace('_', '-')[:50],
            is_published=config.get('auto_publish', False),
            visible_in_listings=True,
            metadata={
                'amazon_asin': amazon_data.get('asin', ''),
                'source': 'amazon_sourcing_workflow',
                'ai_enhanced': 'true',
                'imported_at': datetime.now(timezone.utc).isoformat()
            }
        )
        
        # Create category if specified in AI enhancements
        if ai_enhancements.get('category_suggestions'):
            suggested_category = ai_enhancements['category_suggestions'][0]
            category_id = await client.create_category_if_not_exists(suggested_category)
            product_input.category_id = category_id
        
        # Create the product
        product = await client.create_product(product_input)
        product_id = product['id']
        
        # Create product variant with pricing
        price = amazon_data.get('price')
        if price:
            # Apply pricing rules if configured
            markup_percentage = config.get('pricing_rules', {}).get('markup_percentage', 0)
            if markup_percentage:
                price = price * (1 + markup_percentage / 100)
            
            variant_input = SaleorVariantInput(
                sku=f"AMZ-{amazon_data.get('asin', uuid.uuid4().hex[:8])}",
                price=price,
                track_inventory=True
            )
            
            variant = await client.create_product_variant(product_id, variant_input)
        
        # Upload product images
        uploaded_images = []
        images = amazon_data.get('images', [])
        
        for i, image_url in enumerate(images[:5]):  # Limit to 5 images
            try:
                image_input = SaleorImageInput(
                    image_url=image_url,
                    alt_text=f"{product_name} - Image {i+1}",
                    sort_order=i
                )
                
                uploaded_image = await client.upload_product_image(product_id, image_input)
                if uploaded_image:
                    uploaded_images.append(uploaded_image)
            
            except Exception as e:
                logger.warning(f"Failed to upload image {image_url}: {e}")
        
        # Update SEO if AI enhancements are available
        if ai_enhancements.get('seo_description'):
            await client.update_product_seo(
                product_id,
                ai_enhancements.get('optimized_title', product_name),
                ai_enhancements.get('seo_description')
            )
        
        result = {
            'product_id': product_id,
            'product_name': product_name,
            'product_slug': product.get('slug'),
            'variant_id': variant.get('id') if 'variant' in locals() else None,
            'category_id': product.get('category', {}).get('id'),
            'images_uploaded': len(uploaded_images),
            'saleor_url': f"/dashboard/products/{product_id}",
            'created_at': product.get('created'),
            'metadata': product.get('metadata', [])
        }
        
        logger.info(f"✅ Successfully created Amazon-sourced product: {product_name} (ID: {product_id})")
        return result
    
    except Exception as e:
        logger.error(f"❌ Failed to create Amazon-sourced product: {e}")
        raise

# Export classes and functions
__all__ = [
    'SaleorGraphQLClient',
    'SaleorProductInput', 
    'SaleorVariantInput',
    'SaleorImageInput',
    'create_amazon_sourced_product'
]
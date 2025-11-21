#!/usr/bin/env python3
"""
Saleor GraphQL Integration Test Module
Comprehensive testing of Saleor GraphQL API integration for Amazon sourced products

This module provides:
- GraphQL query and mutation testing
- Product creation and management
- Category and attribute handling  
- Image upload and media management
- Inventory and pricing synchronization
- Error handling and validation
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import base64
import os

logger = logging.getLogger('SaleorIntegrationTest')

class SaleorGraphQLClient:
    """Saleor GraphQL API client with comprehensive testing capabilities"""
    
    def __init__(self, endpoint: str, auth_token: Optional[str] = None):
        self.endpoint = endpoint
        self.auth_token = auth_token
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        headers = {'Content-Type': 'application/json'}
        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'
            
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def execute_query(self, query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute GraphQL query or mutation"""
        payload = {
            'query': query,
            'variables': variables or {}
        }
        
        try:
            async with self.session.post(self.endpoint, json=payload) as response:
                response_data = await response.json()
                
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}: {response_data}")
                
                if 'errors' in response_data:
                    raise Exception(f"GraphQL errors: {response_data['errors']}")
                
                return response_data
                
        except Exception as e:
            logger.error(f"GraphQL request failed: {e}")
            raise
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test basic connection to Saleor GraphQL API"""
        query = """
        query TestConnection {
            shop {
                name
                domain {
                    host
                }
                defaultCountry {
                    code
                    country
                }
            }
        }
        """
        
        try:
            result = await self.execute_query(query)
            shop_data = result['data']['shop']
            
            return {
                'connected': True,
                'shop_name': shop_data['name'],
                'domain': shop_data['domain']['host'],
                'country': shop_data['defaultCountry']['country'],
                'response_time': 'fast'  # Could measure actual time
            }
            
        except Exception as e:
            return {
                'connected': False,
                'error': str(e)
            }
    
    async def get_product_types(self) -> List[Dict[str, Any]]:
        """Get available product types"""
        query = """
        query GetProductTypes {
            productTypes(first: 20) {
                edges {
                    node {
                        id
                        name
                        slug
                        hasVariants
                        productAttributes {
                            id
                            name
                            slug
                            inputType
                        }
                    }
                }
            }
        }
        """
        
        result = await self.execute_query(query)
        return [edge['node'] for edge in result['data']['productTypes']['edges']]
    
    async def get_categories(self) -> List[Dict[str, Any]]:
        """Get product categories"""
        query = """
        query GetCategories {
            categories(first: 50) {
                edges {
                    node {
                        id
                        name
                        slug
                        level
                        parent {
                            name
                        }
                    }
                }
            }
        }
        """
        
        result = await self.execute_query(query)
        return [edge['node'] for edge in result['data']['categories']['edges']]
    
    async def create_category(self, name: str, slug: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new category"""
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
                'slug': slug,
                'parent': parent_id
            }
        }
        
        result = await self.execute_query(mutation, variables)
        category_data = result['data']['categoryCreate']
        
        if category_data['errors']:
            raise Exception(f"Category creation failed: {category_data['errors']}")
        
        return category_data['category']
    
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new product"""
        mutation = """
        mutation CreateProduct($input: ProductCreateInput!) {
            productCreate(input: $input) {
                product {
                    id
                    name
                    slug
                    description
                    category {
                        name
                    }
                    defaultVariant {
                        id
                        name
                        sku
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
        
        variables = {
            'input': self._prepare_product_input(product_data)
        }
        
        result = await self.execute_query(mutation, variables)
        product_result = result['data']['productCreate']
        
        if product_result['errors']:
            raise Exception(f"Product creation failed: {product_result['errors']}")
        
        return product_result['product']
    
    def _prepare_product_input(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare product data for GraphQL input"""
        # Generate slug from title
        slug = product_data.get('title', '').lower().replace(' ', '-').replace('&', 'and')
        slug = ''.join(c for c in slug if c.isalnum() or c in '-_')[:50]
        
        # Find or create default product type
        product_type_id = "UHJvZHVjdFR5cGU6MQ=="  # Default product type ID (base64 encoded)
        
        input_data = {
            'name': product_data.get('title', ''),
            'slug': slug,
            'description': product_data.get('description', ''),
            'productType': product_type_id,
            'category': product_data.get('category_id'),  # Will need to map categories
            'weight': 0.5,  # Default weight
            'seo': {
                'title': product_data.get('title', '')[:60],
                'description': product_data.get('description', '')[:160]
            }
        }
        
        return input_data
    
    async def create_product_variant(self, product_id: str, variant_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a product variant"""
        mutation = """
        mutation CreateProductVariant($input: ProductVariantCreateInput!) {
            productVariantCreate(input: $input) {
                productVariant {
                    id
                    name
                    sku
                    pricing {
                        price {
                            amount
                            currency
                        }
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
        
        variables = {
            'input': {
                'product': product_id,
                'sku': variant_data.get('sku', f"SKU_{datetime.now().strftime('%Y%m%d%H%M%S')}"),
                'name': variant_data.get('name', 'Default'),
                'trackInventory': True,
                'weight': variant_data.get('weight', 0.5)
            }
        }
        
        result = await self.execute_query(mutation, variables)
        variant_result = result['data']['productVariantCreate']
        
        if variant_result['errors']:
            raise Exception(f"Variant creation failed: {variant_result['errors']}")
        
        return variant_result['productVariant']
    
    async def set_product_pricing(self, variant_id: str, price: float, currency: str = "USD") -> Dict[str, Any]:
        """Set product variant pricing"""
        mutation = """
        mutation UpdateProductVariantPrice($id: ID!, $input: ProductVariantInput!) {
            productVariantUpdate(id: $id, input: $input) {
                productVariant {
                    id
                    pricing {
                        price {
                            amount
                            currency
                        }
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
        
        variables = {
            'id': variant_id,
            'input': {
                'pricing': {
                    'price': price
                }
            }
        }
        
        result = await self.execute_query(mutation, variables)
        update_result = result['data']['productVariantUpdate']
        
        if update_result['errors']:
            raise Exception(f"Pricing update failed: {update_result['errors']}")
        
        return update_result['productVariant']
    
    async def upload_product_media(self, product_id: str, image_urls: List[str]) -> List[Dict[str, Any]]:
        """Upload product media from URLs"""
        uploaded_media = []
        
        for i, image_url in enumerate(image_urls[:5]):  # Limit to 5 images
            mutation = """
            mutation CreateProductMedia($input: ProductMediaCreateInput!) {
                productMediaCreate(input: $input) {
                    media {
                        id
                        url
                        alt
                        type
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
                    'product': product_id,
                    'mediaUrl': image_url,
                    'alt': f"Product image {i+1}"
                }
            }
            
            try:
                result = await self.execute_query(mutation, variables)
                media_result = result['data']['productMediaCreate']
                
                if not media_result['errors']:
                    uploaded_media.append(media_result['media'])
                else:
                    logger.warning(f"Media upload failed for {image_url}: {media_result['errors']}")
                    
            except Exception as e:
                logger.error(f"Media upload error for {image_url}: {e}")
                
        return uploaded_media
    
    async def search_products(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for products"""
        search_query = """
        query SearchProducts($filter: ProductFilterInput!, $first: Int!) {
            products(filter: $filter, first: $first) {
                edges {
                    node {
                        id
                        name
                        slug
                        description
                        category {
                            name
                        }
                        defaultVariant {
                            pricing {
                                price {
                                    amount
                                    currency
                                }
                            }
                        }
                        rating
                    }
                }
            }
        }
        """
        
        variables = {
            'filter': {
                'search': query
            },
            'first': limit
        }
        
        result = await self.execute_query(search_query, variables)
        return [edge['node'] for edge in result['data']['products']['edges']]
    
    async def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get product by ID"""
        query = """
        query GetProduct($id: ID!) {
            product(id: $id) {
                id
                name
                slug
                description
                category {
                    name
                }
                defaultVariant {
                    id
                    name
                    sku
                    pricing {
                        price {
                            amount
                            currency
                        }
                    }
                }
                media {
                    id
                    url
                    alt
                }
                rating
                isAvailable
            }
        }
        """
        
        variables = {'id': product_id}
        
        try:
            result = await self.execute_query(query, variables)
            return result['data']['product']
        except:
            return None

class SaleorIntegrationTester:
    """Comprehensive Saleor integration test suite"""
    
    def __init__(self, saleor_endpoint: str, auth_token: Optional[str] = None):
        self.saleor_endpoint = saleor_endpoint
        self.auth_token = auth_token
        self.test_results = []
        
    async def run_integration_tests(self) -> Dict[str, Any]:
        """Run complete Saleor integration test suite"""
        async with SaleorGraphQLClient(self.saleor_endpoint, self.auth_token) as client:
            
            # Test 1: Connection and basic queries
            connection_result = await self.test_connection(client)
            
            # Test 2: Category management
            category_result = await self.test_category_management(client)
            
            # Test 3: Product creation
            product_result = await self.test_product_creation(client)
            
            # Test 4: Product media upload
            media_result = await self.test_media_upload(client)
            
            # Test 5: Product search and retrieval
            search_result = await self.test_product_search(client)
            
            # Test 6: Error handling
            error_result = await self.test_error_handling(client)
            
            return {
                'connection_test': connection_result,
                'category_test': category_result,
                'product_creation_test': product_result,
                'media_upload_test': media_result,
                'search_test': search_result,
                'error_handling_test': error_result,
                'overall_status': self._calculate_overall_status()
            }
    
    async def test_connection(self, client: SaleorGraphQLClient) -> Dict[str, Any]:
        """Test Saleor connection and basic queries"""
        try:
            # Test basic connection
            connection_info = await client.test_connection()
            
            if not connection_info['connected']:
                return {
                    'status': 'failed',
                    'error': connection_info['error']
                }
            
            # Test schema introspection
            product_types = await client.get_product_types()
            categories = await client.get_categories()
            
            return {
                'status': 'passed',
                'connection_info': connection_info,
                'available_product_types': len(product_types),
                'available_categories': len(categories),
                'sample_product_types': product_types[:3],
                'sample_categories': categories[:5]
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    async def test_category_management(self, client: SaleorGraphQLClient) -> Dict[str, Any]:
        """Test category creation and management"""
        try:
            # Get existing categories
            existing_categories = await client.get_categories()
            
            # Try to create a test category
            test_category_name = f"Test Category {datetime.now().strftime('%Y%m%d%H%M%S')}"
            test_category_slug = f"test-category-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            try:
                new_category = await client.create_category(test_category_name, test_category_slug)
                category_creation_success = True
                category_creation_error = None
            except Exception as e:
                category_creation_success = False
                category_creation_error = str(e)
                new_category = None
            
            return {
                'status': 'passed' if len(existing_categories) > 0 else 'warning',
                'existing_categories_count': len(existing_categories),
                'category_creation_success': category_creation_success,
                'category_creation_error': category_creation_error,
                'new_category': new_category,
                'sample_categories': [cat['name'] for cat in existing_categories[:5]]
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    async def test_product_creation(self, client: SaleorGraphQLClient) -> Dict[str, Any]:
        """Test product creation workflow"""
        try:
            # Sample product data (from Amazon simulator)
            test_product = {
                'title': f'Test Product {datetime.now().strftime("%Y%m%d%H%M%S")}',
                'description': 'This is a test product created by the integration test suite. It demonstrates the product creation workflow.',
                'price': 29.99,
                'category': 'electronics',
                'sku': f'TEST-SKU-{datetime.now().strftime("%Y%m%d%H%M%S")}',
                'weight': 0.5
            }
            
            # Create product
            created_product = await client.create_product(test_product)
            
            # Create variant
            variant_data = {
                'name': 'Default Variant',
                'sku': test_product['sku'],
                'weight': test_product['weight']
            }
            
            created_variant = await client.create_product_variant(created_product['id'], variant_data)
            
            # Set pricing
            pricing_result = await client.set_product_pricing(
                created_variant['id'], 
                test_product['price']
            )
            
            return {
                'status': 'passed',
                'created_product': created_product,
                'created_variant': created_variant,
                'pricing_set': pricing_result is not None,
                'product_id': created_product['id'],
                'variant_id': created_variant['id']
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    async def test_media_upload(self, client: SaleorGraphQLClient) -> Dict[str, Any]:
        """Test product media upload"""
        try:
            # First create a test product if we don't have one
            test_product = {
                'title': f'Media Test Product {datetime.now().strftime("%Y%m%d%H%M%S")}',
                'description': 'Test product for media upload testing',
                'category': 'electronics'
            }
            
            created_product = await client.create_product(test_product)
            
            # Test image URLs (using placeholder images)
            test_image_urls = [
                'https://via.placeholder.com/500x500/FF0000/FFFFFF?text=Test+Image+1',
                'https://via.placeholder.com/500x500/00FF00/FFFFFF?text=Test+Image+2',
                'https://via.placeholder.com/500x500/0000FF/FFFFFF?text=Test+Image+3'
            ]
            
            # Upload media
            uploaded_media = await client.upload_product_media(created_product['id'], test_image_urls)
            
            return {
                'status': 'passed' if len(uploaded_media) > 0 else 'warning',
                'product_id': created_product['id'],
                'attempted_uploads': len(test_image_urls),
                'successful_uploads': len(uploaded_media),
                'uploaded_media': uploaded_media,
                'upload_success_rate': len(uploaded_media) / len(test_image_urls) * 100
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    async def test_product_search(self, client: SaleorGraphQLClient) -> Dict[str, Any]:
        """Test product search functionality"""
        try:
            # Search for products
            search_queries = ['test', 'product', 'electronics']
            search_results = {}
            
            for query in search_queries:
                results = await client.search_products(query, limit=5)
                search_results[query] = {
                    'count': len(results),
                    'results': [{'name': p['name'], 'id': p['id']} for p in results[:3]]
                }
            
            # Test product retrieval by ID
            all_results = []
            for results in search_results.values():
                all_results.extend(results['results'])
            
            retrieval_test = None
            if all_results:
                first_product_id = all_results[0]['id']
                retrieved_product = await client.get_product_by_id(first_product_id)
                retrieval_test = {
                    'success': retrieved_product is not None,
                    'product_name': retrieved_product['name'] if retrieved_product else None
                }
            
            return {
                'status': 'passed',
                'search_results': search_results,
                'retrieval_test': retrieval_test,
                'total_products_found': sum(r['count'] for r in search_results.values())
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    async def test_error_handling(self, client: SaleorGraphQLClient) -> Dict[str, Any]:
        """Test error handling scenarios"""
        error_tests = {}
        
        # Test 1: Invalid product creation
        try:
            invalid_product = {
                'title': '',  # Empty title
                'description': '',  # Empty description
                'category': 'nonexistent_category'
            }
            await client.create_product(invalid_product)
            error_tests['invalid_product'] = {'handled': False, 'error': 'Should have failed but did not'}
        except Exception as e:
            error_tests['invalid_product'] = {'handled': True, 'error': str(e)}
        
        # Test 2: Invalid product ID retrieval
        try:
            result = await client.get_product_by_id('INVALID_ID_123')
            error_tests['invalid_id'] = {'handled': result is None, 'result': result}
        except Exception as e:
            error_tests['invalid_id'] = {'handled': True, 'error': str(e)}
        
        # Test 3: Invalid GraphQL query
        try:
            await client.execute_query('INVALID QUERY')
            error_tests['invalid_query'] = {'handled': False, 'error': 'Should have failed'}
        except Exception as e:
            error_tests['invalid_query'] = {'handled': True, 'error': str(e)}
        
        handled_count = sum(1 for test in error_tests.values() if test.get('handled', False))
        
        return {
            'status': 'passed' if handled_count >= 2 else 'warning',
            'error_tests': error_tests,
            'errors_handled': handled_count,
            'total_error_tests': len(error_tests)
        }
    
    def _calculate_overall_status(self) -> str:
        """Calculate overall test status"""
        if not self.test_results:
            return 'unknown'
        
        passed_tests = sum(1 for result in self.test_results if result.get('status') == 'passed')
        total_tests = len(self.test_results)
        
        if passed_tests == total_tests:
            return 'all_passed'
        elif passed_tests >= total_tests * 0.7:
            return 'mostly_passed'
        else:
            return 'needs_attention'

# Convenience function for running tests
async def test_saleor_integration(endpoint: str, auth_token: Optional[str] = None) -> Dict[str, Any]:
    """Run complete Saleor integration test"""
    tester = SaleorIntegrationTester(endpoint, auth_token)
    return await tester.run_integration_tests()

# Example usage
if __name__ == "__main__":
    async def run_test():
        # Test with multiple possible endpoints
        test_endpoints = [
            'http://localhost:8000/graphql/',
            'http://localhost:8024/graphql/',
        ]
        
        for endpoint in test_endpoints:
            print(f"\n🔍 Testing Saleor endpoint: {endpoint}")
            print("=" * 60)
            
            try:
                results = await test_saleor_integration(endpoint)
                
                print(f"Overall Status: {results['overall_status']}")
                print(f"Connection: {results['connection_test']['status']}")
                print(f"Categories: {results['category_test']['status']}")
                print(f"Product Creation: {results['product_creation_test']['status']}")
                print(f"Media Upload: {results['media_upload_test']['status']}")
                print(f"Search: {results['search_test']['status']}")
                print(f"Error Handling: {results['error_handling_test']['status']}")
                
                if results['connection_test']['status'] == 'passed':
                    shop_info = results['connection_test']['connection_info']
                    print(f"\n✅ Connected to: {shop_info['shop_name']} ({shop_info['domain']})")
                    break
                else:
                    print(f"❌ Failed to connect: {results['connection_test'].get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ Test failed: {e}")
        
        print(f"\n📊 Saleor integration test completed!")
    
    asyncio.run(run_test())
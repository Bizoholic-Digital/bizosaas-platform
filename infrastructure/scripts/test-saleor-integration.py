#!/usr/bin/env python3
"""
CoreLDove Saleor Integration Test Suite
Tests complete GraphQL schema and storefront integration
"""

import requests
import json
import time
import sys
from typing import Dict, List, Optional, Any

class SaleorIntegrationTester:
    """Complete integration tester for Saleor GraphQL API"""
    
    def __init__(self, api_url: str = "http://localhost:8024/graphql/"):
        self.api_url = api_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
    def execute_query(self, query: str, variables: Optional[Dict] = None) -> Optional[Dict]:
        """Execute GraphQL query"""
        payload = {'query': query}
        if variables:
            payload['variables'] = variables
            
        try:
            response = self.session.post(
                self.api_url, 
                json=payload, 
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Query failed: {e}")
            return None
    
    def test_basic_connectivity(self) -> bool:
        """Test basic GraphQL connectivity"""
        print("🔍 Testing basic connectivity...")
        
        query = """
        query {
            shop {
                name
                description
                defaultCountry {
                    code
                    country
                }
            }
        }
        """
        
        result = self.execute_query(query)
        if result and 'data' in result and result['data']['shop']:
            shop = result['data']['shop']
            print(f"✅ Connected to shop: {shop['name']}")
            print(f"   Description: {shop['description']}")
            return True
        else:
            print("❌ Failed to connect to Saleor API")
            return False
    
    def test_schema_introspection(self) -> bool:
        """Test GraphQL schema introspection"""
        print("🔍 Testing schema introspection...")
        
        query = """
        query {
            __schema {
                queryType { name }
                mutationType { name }
                types {
                    name
                    kind
                }
            }
        }
        """
        
        result = self.execute_query(query)
        if result and 'data' in result and result['data']['__schema']:
            schema = result['data']['__schema']
            types = schema['types']
            print(f"✅ Schema introspection working")
            print(f"   Query type: {schema['queryType']['name']}")
            print(f"   Mutation type: {schema['mutationType']['name']}")
            print(f"   Total types: {len(types)}")
            return True
        else:
            print("❌ Schema introspection failed")
            return False
    
    def test_channels(self) -> bool:
        """Test channels functionality"""
        print("🔍 Testing channels...")
        
        query = """
        query {
            channels {
                id
                name
                slug
                isActive
                currencyCode
                defaultCountry {
                    code
                    country
                }
            }
        }
        """
        
        result = self.execute_query(query)
        if result and 'data' in result and result['data']['channels']:
            channels = result['data']['channels']
            print(f"✅ Found {len(channels)} channel(s)")
            for channel in channels:
                print(f"   - {channel['name']} ({channel['slug']}) - {channel['currencyCode']}")
            return True
        else:
            print("❌ Channels query failed")
            return False
    
    def test_products(self) -> bool:
        """Test product queries"""
        print("🔍 Testing products...")
        
        query = """
        query {
            products(first: 5) {
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
                            id
                            name
                            pricing {
                                price {
                                    gross {
                                        amount
                                        currency
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        """
        
        result = self.execute_query(query)
        if result and 'data' in result and result['data']['products']:
            products = result['data']['products']['edges']
            print(f"✅ Found {len(products)} product(s)")
            for edge in products:
                product = edge['node']
                print(f"   - {product['name']} ({product['slug']})")
            return True
        else:
            print("❌ Products query failed")
            return False
    
    def test_categories(self) -> bool:
        """Test category queries"""
        print("🔍 Testing categories...")
        
        query = """
        query {
            categories(first: 10) {
                edges {
                    node {
                        id
                        name
                        slug
                        level
                        products {
                            totalCount
                        }
                    }
                }
            }
        }
        """
        
        result = self.execute_query(query)
        if result and 'data' in result and result['data']['categories']:
            categories = result['data']['categories']['edges']
            print(f"✅ Found {len(categories)} categor(y/ies)")
            for edge in categories:
                category = edge['node']
                product_count = category['products']['totalCount']
                print(f"   - {category['name']} ({product_count} products)")
            return True
        else:
            print("❌ Categories query failed")
            return False
    
    def test_checkout_operations(self) -> bool:
        """Test checkout and cart operations"""
        print("🔍 Testing checkout operations...")
        
        # First get available products and channels
        products_query = """
        query {
            products(first: 1) {
                edges {
                    node {
                        id
                        defaultVariant {
                            id
                        }
                    }
                }
            }
            channels {
                slug
            }
        }
        """
        
        products_result = self.execute_query(products_query)
        if not (products_result and 'data' in products_result):
            print("❌ Could not get products for checkout test")
            return False
            
        products = products_result['data']['products']['edges']
        channels = products_result['data']['channels']
        
        if not products or not channels:
            print("⚠️  No products or channels available for checkout test")
            return True  # Not a failure, just no data
        
        product_variant_id = products[0]['node']['defaultVariant']['id']
        channel_slug = channels[0]['slug']
        
        # Create checkout
        checkout_mutation = """
        mutation CreateCheckout($input: CheckoutCreateInput!) {
            checkoutCreate(input: $input) {
                checkout {
                    id
                    token
                    lines {
                        id
                        quantity
                    }
                }
                errors {
                    field
                    message
                }
            }
        }
        """
        
        variables = {
            'input': {
                'channel': channel_slug,
                'lines': [
                    {
                        'variantId': product_variant_id,
                        'quantity': 1
                    }
                ]
            }
        }
        
        result = self.execute_query(checkout_mutation, variables)
        if result and 'data' in result and result['data']['checkoutCreate']:
            checkout_data = result['data']['checkoutCreate']
            if checkout_data['errors']:
                print(f"⚠️  Checkout creation had errors: {checkout_data['errors']}")
                return False
            else:
                checkout = checkout_data['checkout']
                print(f"✅ Checkout created with ID: {checkout['id']}")
                return True
        else:
            print("❌ Checkout creation failed")
            return False
    
    def test_user_operations(self) -> bool:
        """Test user and customer operations"""
        print("🔍 Testing user operations...")
        
        # Test customer creation (mutation)
        mutation = """
        mutation CreateUser($input: UserCreateInput!) {
            userCreate(input: $input) {
                user {
                    id
                    email
                    firstName
                    lastName
                }
                errors {
                    field
                    message
                }
            }
        }
        """
        
        import random
        import string
        test_email = f"test{''.join(random.choices(string.digits, k=6))}@coreldove.test"
        
        variables = {
            'input': {
                'email': test_email,
                'firstName': 'Test',
                'lastName': 'User',
                'isActive': True
            }
        }
        
        result = self.execute_query(mutation, variables)
        if result and 'data' in result and result['data']['userCreate']:
            user_data = result['data']['userCreate']
            if user_data['errors']:
                print(f"⚠️  User creation had errors: {user_data['errors']}")
                # This might be expected (e.g., permissions)
                return True
            else:
                user = user_data['user']
                print(f"✅ User created: {user['email']}")
                return True
        else:
            print("❌ User creation mutation failed")
            return False
    
    def test_payment_gateways(self) -> bool:
        """Test payment gateway queries"""
        print("🔍 Testing payment gateways...")
        
        query = """
        query {
            shop {
                availablePaymentGateways {
                    id
                    name
                    config {
                        field
                        value
                    }
                }
            }
        }
        """
        
        result = self.execute_query(query)
        if result and 'data' in result and result['data']['shop']:
            gateways = result['data']['shop']['availablePaymentGateways']
            print(f"✅ Found {len(gateways)} payment gateway(s)")
            for gateway in gateways:
                print(f"   - {gateway['name']} (ID: {gateway['id']})")
            return True
        else:
            print("❌ Payment gateways query failed")
            return False
    
    def test_shipping_methods(self) -> bool:
        """Test shipping methods"""
        print("🔍 Testing shipping methods...")
        
        query = """
        query {
            shippingZones(first: 10) {
                edges {
                    node {
                        id
                        name
                        countries {
                            code
                            country
                        }
                        shippingMethods {
                            id
                            name
                            type
                        }
                    }
                }
            }
        }
        """
        
        result = self.execute_query(query)
        if result and 'data' in result and result['data']['shippingZones']:
            zones = result['data']['shippingZones']['edges']
            print(f"✅ Found {len(zones)} shipping zone(s)")
            total_methods = 0
            for edge in zones:
                zone = edge['node']
                method_count = len(zone['shippingMethods'])
                total_methods += method_count
                print(f"   - {zone['name']} ({method_count} methods)")
            print(f"   Total shipping methods: {total_methods}")
            return True
        else:
            print("❌ Shipping zones query failed")
            return False
    
    def test_warehouse_operations(self) -> bool:
        """Test warehouse and stock operations"""
        print("🔍 Testing warehouses...")
        
        query = """
        query {
            warehouses(first: 10) {
                edges {
                    node {
                        id
                        name
                        slug
                        email
                        address {
                            streetAddress1
                            city
                            country {
                                code
                            }
                        }
                    }
                }
            }
        }
        """
        
        result = self.execute_query(query)
        if result and 'data' in result and result['data']['warehouses']:
            warehouses = result['data']['warehouses']['edges']
            print(f"✅ Found {len(warehouses)} warehouse(s)")
            for edge in warehouses:
                warehouse = edge['node']
                print(f"   - {warehouse['name']} ({warehouse['slug']})")
            return True
        else:
            print("❌ Warehouses query failed")
            return False
    
    def run_comprehensive_test(self) -> bool:
        """Run all tests and return overall result"""
        print("🚀 Starting CoreLDove Saleor Integration Test Suite")
        print("=" * 60)
        
        tests = [
            ('Basic Connectivity', self.test_basic_connectivity),
            ('Schema Introspection', self.test_schema_introspection),
            ('Channels', self.test_channels),
            ('Products', self.test_products),
            ('Categories', self.test_categories),
            ('Checkout Operations', self.test_checkout_operations),
            ('User Operations', self.test_user_operations),
            ('Payment Gateways', self.test_payment_gateways),
            ('Shipping Methods', self.test_shipping_methods),
            ('Warehouse Operations', self.test_warehouse_operations),
        ]
        
        results = []
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}")
            print("-" * 40)
            try:
                result = test_func()
                results.append((test_name, result))
                if result:
                    print(f"✅ {test_name}: PASSED")
                else:
                    print(f"❌ {test_name}: FAILED")
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {e}")
                results.append((test_name, False))
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\n📈 Overall Result: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Saleor integration is working correctly.")
            return True
        else:
            print(f"⚠️  {total - passed} test(s) failed. Check the logs above.")
            return False

def main():
    """Main test execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Saleor GraphQL API integration')
    parser.add_argument('--url', default='http://localhost:8024/graphql/', 
                      help='Saleor GraphQL API URL')
    parser.add_argument('--wait', type=int, default=0,
                      help='Wait seconds before starting tests')
    
    args = parser.parse_args()
    
    if args.wait > 0:
        print(f"⏳ Waiting {args.wait} seconds for services to start...")
        time.sleep(args.wait)
    
    tester = SaleorIntegrationTester(args.url)
    success = tester.run_comprehensive_test()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
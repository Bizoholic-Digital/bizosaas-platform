#!/usr/bin/env python3
"""
Saleor GraphQL Schema Validation Script
Verifies that the complete Saleor schema includes all required fields for the CoreLDove storefront
"""

import requests
import json
import sys
from typing import List, Dict, Any

# Required schema fields for storefront compatibility
REQUIRED_TYPES = [
    'Query',
    'Mutation',
    'Shop',
    'Product',
    'ProductVariant',
    'Category',
    'Collection',
    'Checkout',
    'CheckoutLine',
    'Order',
    'OrderLine',
    'User',
    'Address',
    'Channel',
    'Warehouse',
    'ShippingMethod',
    'PaymentGateway',
    'ProductImage',
    'Money',
    'TaxedMoney',
    'CountryDisplay',
    'AttributeValue',
    'Attribute',
]

REQUIRED_QUERIES = [
    'shop',
    'products',
    'product',
    'categories',
    'category',
    'collections',
    'collection',
    'checkout',
    'order',
    'user',
    'attributes',
]

REQUIRED_MUTATIONS = [
    'checkoutCreate',
    'checkoutLinesAdd',
    'checkoutLinesUpdate',
    'checkoutLinesDelete',
    'checkoutShippingAddressUpdate',
    'checkoutBillingAddressUpdate',
    'checkoutComplete',
    'userCreate',
    'tokenCreate',
    'tokenRefresh',
    'tokenVerify',
]

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(message: str) -> None:
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message: str) -> None:
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message: str) -> None:
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def print_info(message: str) -> None:
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

def fetch_graphql_schema(endpoint: str) -> Dict[str, Any]:
    """
    Fetch the complete GraphQL schema from the endpoint
    """
    query = {
        "query": """
        {
            __schema {
                queryType { name }
                mutationType { name }
                subscriptionType { name }
                types {
                    kind
                    name
                    description
                    fields {
                        name
                        description
                        type {
                            kind
                            name
                            ofType {
                                kind
                                name
                                ofType {
                                    kind
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }
        """
    }
    
    try:
        response = requests.post(
            endpoint,
            json=query,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to fetch schema from {endpoint}: {e}")
        return {}

def validate_schema_types(schema_data: Dict[str, Any]) -> bool:
    """
    Validate that all required types are present in the schema
    """
    if 'data' not in schema_data or '__schema' not in schema_data['data']:
        print_error("Invalid schema response format")
        return False
    
    schema = schema_data['data']['__schema']
    available_types = {type_def['name'] for type_def in schema['types'] if type_def['name']}
    
    print_info(f"Found {len(available_types)} types in schema")
    
    missing_types = []
    found_types = []
    
    for required_type in REQUIRED_TYPES:
        if required_type in available_types:
            found_types.append(required_type)
        else:
            missing_types.append(required_type)
    
    print_success(f"Found required types: {len(found_types)}/{len(REQUIRED_TYPES)}")
    
    if missing_types:
        print_error(f"Missing required types: {', '.join(missing_types)}")
        return False
    
    return True

def validate_query_fields(schema_data: Dict[str, Any]) -> bool:
    """
    Validate that all required query fields are present
    """
    schema = schema_data['data']['__schema']
    query_type = next((t for t in schema['types'] if t['name'] == 'Query'), None)
    
    if not query_type or not query_type.get('fields'):
        print_error("Query type not found or has no fields")
        return False
    
    available_queries = {field['name'] for field in query_type['fields']}
    
    missing_queries = []
    found_queries = []
    
    for required_query in REQUIRED_QUERIES:
        if required_query in available_queries:
            found_queries.append(required_query)
        else:
            missing_queries.append(required_query)
    
    print_success(f"Found required queries: {len(found_queries)}/{len(REQUIRED_QUERIES)}")
    
    if missing_queries:
        print_error(f"Missing required queries: {', '.join(missing_queries)}")
        return False
    
    return True

def validate_mutation_fields(schema_data: Dict[str, Any]) -> bool:
    """
    Validate that all required mutation fields are present
    """
    schema = schema_data['data']['__schema']
    mutation_type = next((t for t in schema['types'] if t['name'] == 'Mutation'), None)
    
    if not mutation_type or not mutation_type.get('fields'):
        print_error("Mutation type not found or has no fields")
        return False
    
    available_mutations = {field['name'] for field in mutation_type['fields']}
    
    missing_mutations = []
    found_mutations = []
    
    for required_mutation in REQUIRED_MUTATIONS:
        if required_mutation in available_mutations:
            found_mutations.append(required_mutation)
        else:
            missing_mutations.append(required_mutation)
    
    print_success(f"Found required mutations: {len(found_mutations)}/{len(REQUIRED_MUTATIONS)}")
    
    if missing_mutations:
        print_error(f"Missing required mutations: {', '.join(missing_mutations)}")
        return False
    
    return True

def test_sample_queries(endpoint: str) -> bool:
    """
    Test some sample queries to ensure the API is working correctly
    """
    sample_queries = [
        {
            'name': 'Shop Information',
            'query': '{ shop { name description } }'
        },
        {
            'name': 'Products List',
            'query': '{ products(first: 5) { edges { node { id name slug } } } }'
        },
        {
            'name': 'Categories List',
            'query': '{ categories(first: 5) { edges { node { id name slug } } } }'
        }
    ]
    
    all_passed = True
    
    for sample in sample_queries:
        try:
            response = requests.post(
                endpoint,
                json={'query': sample['query']},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            if 'errors' in result:
                print_error(f"{sample['name']} query failed: {result['errors']}")
                all_passed = False
            else:
                print_success(f"{sample['name']} query succeeded")
                
        except requests.exceptions.RequestException as e:
            print_error(f"{sample['name']} query failed: {e}")
            all_passed = False
    
    return all_passed

def main():
    """
    Main validation function
    """
    endpoint = 'http://localhost:8024/graphql/'
    
    print(f"{Colors.BOLD}Saleor GraphQL Schema Validation{Colors.END}")
    print("=" * 50)
    print_info(f"Testing endpoint: {endpoint}")
    print()
    
    # Test connectivity
    try:
        response = requests.get('http://localhost:8024', timeout=5)
        print_success("Saleor API is accessible")
    except requests.exceptions.RequestException:
        print_error("Cannot connect to Saleor API. Is it running?")
        sys.exit(1)
    
    # Fetch schema
    print_info("Fetching GraphQL schema...")
    schema_data = fetch_graphql_schema(endpoint)
    
    if not schema_data:
        print_error("Failed to fetch schema")
        sys.exit(1)
    
    # Validate schema components
    validations = [
        ("Schema Types", validate_schema_types),
        ("Query Fields", validate_query_fields),
        ("Mutation Fields", validate_mutation_fields),
    ]
    
    all_valid = True
    
    for validation_name, validation_func in validations:
        print(f"\n{Colors.BOLD}Validating {validation_name}...{Colors.END}")
        if not validation_func(schema_data):
            all_valid = False
    
    # Test sample queries
    print(f"\n{Colors.BOLD}Testing Sample Queries...{Colors.END}")
    if not test_sample_queries(endpoint):
        all_valid = False
    
    # Final result
    print("\n" + "=" * 50)
    if all_valid:
        print_success("All validations passed! 🎉")
        print_success("The Saleor API is ready for CoreLDove storefront integration.")
        sys.exit(0)
    else:
        print_error("Some validations failed. ❌")
        print_error("The API may not be fully compatible with the storefront.")
        sys.exit(1)

if __name__ == '__main__':
    main()
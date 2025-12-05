/**
 * API Route Adapter for CoreLDove Backend Integration
 * This endpoint acts as a bridge between the Saleor storefront and CoreLDove backend
 */

import { NextRequest, NextResponse } from 'next/server';

const CORELDOVE_API_BASE = 'http://localhost:8024';

interface CoreLDoveProduct {
  id: string;
  name: string;
  description?: string;
  price: number;
  category: string;
}

// Transform CoreLDove product to Saleor-compatible format
function transformProduct(product: CoreLDoveProduct) {
  return {
    id: product.id,
    name: product.name,
    description: product.description || '',
    slug: product.name.toLowerCase().replace(/\s+/g, '-'),
    thumbnail: {
      url: `https://via.placeholder.com/400x400?text=${encodeURIComponent(product.name)}`,
      alt: product.name,
    },
    pricing: {
      priceRange: {
        start: {
          gross: {
            amount: product.price,
            currency: 'USD',
          },
        },
      },
    },
    category: {
      name: product.category,
      slug: product.category.toLowerCase().replace(/\s+/g, '-'),
    },
    variants: [
      {
        id: `${product.id}-default`,
        name: 'Default',
        pricing: {
          price: {
            gross: {
              amount: product.price,
              currency: 'USD',
            },
          },
        },
        quantityAvailable: 10, // Mock inventory
      },
    ],
  };
}

// Fetch data from CoreLDove backend
async function fetchFromCoreLDove(query: string, variables?: any) {
  try {
    const response = await fetch(`${CORELDOVE_API_BASE}/graphql/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        variables,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('CoreLDove API Error:', error);
    throw error;
  }
}

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const action = searchParams.get('action');
  const id = searchParams.get('id');

  try {
    switch (action) {
      case 'products': {
        // Fetch products from CoreLDove
        const result = await fetchFromCoreLDove(`
          query GetProducts {
            products {
              id
              name
              description
              price
              category
            }
          }
        `);

        const transformedProducts = (result.data?.products || []).map(transformProduct);

        return NextResponse.json({
          success: true,
          data: {
            products: transformedProducts,
            totalCount: transformedProducts.length,
          },
        });
      }

      case 'product': {
        if (!id) {
          return NextResponse.json(
            { success: false, error: 'Product ID is required' },
            { status: 400 }
          );
        }

        // Fetch single product from CoreLDove
        const result = await fetchFromCoreLDove(`
          query GetProduct($id: ID!) {
            product(id: $id) {
              id
              name
              description
              price
              category
            }
          }
        `, { id });

        const product = result.data?.product;
        if (!product) {
          return NextResponse.json(
            { success: false, error: 'Product not found' },
            { status: 404 }
          );
        }

        return NextResponse.json({
          success: true,
          data: {
            product: transformProduct(product),
          },
        });
      }

      case 'categories': {
        // Fetch categories from CoreLDove
        const result = await fetchFromCoreLDove(`
          query GetCategories {
            categories {
              id
              name
            }
          }
        `);

        const categories = (result.data?.categories || []).map((cat: any) => ({
          id: cat.id,
          name: cat.name,
          slug: cat.name.toLowerCase().replace(/\s+/g, '-'),
        }));

        return NextResponse.json({
          success: true,
          data: {
            categories,
          },
        });
      }

      case 'featured': {
        // Mock featured products for now
        const featuredProducts = [
          {
            id: '1',
            name: 'Wireless Bluetooth Headphones',
            description: 'Premium sound quality with noise cancellation',
            price: 79.99,
            category: 'Electronics',
          },
          {
            id: '2',
            name: 'Smart Fitness Watch',
            description: 'Track your health and fitness goals',
            price: 199.99,
            category: 'Electronics',
          },
          {
            id: '3',
            name: 'Portable Phone Charger',
            description: '10000mAh fast charging power bank',
            price: 29.99,
            category: 'Electronics',
          },
        ];

        const transformedProducts = featuredProducts.map(transformProduct);

        return NextResponse.json({
          success: true,
          data: {
            products: transformedProducts,
          },
        });
      }

      default: {
        return NextResponse.json(
          { success: false, error: 'Invalid action parameter' },
          { status: 400 }
        );
      }
    }
  } catch (error) {
    console.error('API Adapter Error:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, data } = body;

    switch (action) {
      case 'addToCart': {
        // Mock add to cart functionality
        return NextResponse.json({
          success: true,
          message: 'Product added to cart',
          cartId: 'mock-cart-id',
        });
      }

      case 'createOrder': {
        // Mock order creation
        return NextResponse.json({
          success: true,
          message: 'Order created successfully',
          orderId: `order-${Date.now()}`,
        });
      }

      default: {
        return NextResponse.json(
          { success: false, error: 'Invalid action parameter' },
          { status: 400 }
        );
      }
    }
  } catch (error) {
    console.error('API Adapter POST Error:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}
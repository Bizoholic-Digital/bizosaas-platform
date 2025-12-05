/**
 * Test API endpoint to add our processed sports/fitness product to CorelDove
 * This simulates adding the product from our Amazon workflow to the Saleor backend
 */

import { NextRequest, NextResponse } from 'next/server'

// Our processed product data from the Amazon workflow test
const testSportsProduct = {
  id: "test-boldfit-yoga-mat-001",
  name: "Premium Boldfit Yoga Mat for Gym Workout and Flooring Exercise Long Size Yoga Mat for Men & Women with Carrying Strap - Professional Grade Fitness Equipment",
  slug: "premium-boldfit-yoga-mat-long-size",
  description: "Experience the perfect fusion of comfort, durability, and performance with the Premium Boldfit Yoga Mat. Meticulously crafted for fitness enthusiasts, this professional-grade exercise mat transforms your workout space into a sanctuary of wellness. Whether you're practicing yoga, pilates, or high-intensity training, this mat delivers exceptional support and stability.\n\nEngineered with advanced NBR material and superior grip technology, this yoga mat ensures optimal performance during every session. The extra-long size provides ample space for all body types and exercise routines, while the premium construction guarantees long-lasting durability. The included carrying strap makes transportation effortless, perfect for gym sessions, outdoor workouts, or travel.\n\nTrusted by thousands of satisfied customers with an impressive 4.3-star rating and over 2,847 verified reviews, this Boldfit yoga mat represents the pinnacle of fitness equipment excellence. Join the community of fitness enthusiasts who have made this their go-to choice for reliable, high-performance workout gear.",
  images: [
    {
      url: "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=800&fit=crop&auto=format&q=80",
      alt: "Premium Boldfit Yoga Mat - Main Product Image"
    },
    {
      url: "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=800&fit=crop&auto=format&q=80",
      alt: "Yoga Mat in Use - Workout Session"
    },
    {
      url: "https://images.unsplash.com/photo-1506629905607-4aa67a3bb96e?w=800&h=800&fit=crop&auto=format&q=80",
      alt: "Yoga Mat Features and Benefits"
    }
  ],
  price: {
    amount: 499,
    currency: "INR"
  },
  originalPrice: {
    amount: 599,
    currency: "INR"
  },
  discount: {
    percentage: 17,
    amount: 100
  },
  category: {
    id: "sports-fitness",
    name: "Sports & Fitness",
    slug: "sports-fitness"
  },
  brand: "Boldfit",
  rating: 4.3,
  reviews: 2847,
  inStock: true,
  stockQuantity: 50,
  featured: true,

  // Key features/bullet points
  bulletPoints: [
    "PREMIUM BOLDFIT QUALITY - Professional-grade fitness equipment designed for optimal performance and long-lasting durability",
    "SUPERIOR PERFORMANCE - Advanced NBR material with enhanced grip technology for secure, slip-free workouts",
    "VERSATILE USE - Perfect for yoga, pilates, home gym workouts, professional training, and outdoor fitness activities",
    "TRUSTED BRAND - Backed by 2,847 verified customer reviews with an impressive 4.3/5 star rating",
    "SATISFACTION GUARANTEED - 30-day money-back guarantee with fast and secure delivery for peace of mind",
    "FAST DELIVERY - Quick and secure shipping with real-time tracking and delivery updates"
  ],

  // SEO and marketing data
  seoKeywords: [
    "yoga mat", "boldfit", "exercise mat", "fitness equipment", "gym mat",
    "pilates mat", "workout mat", "non-slip", "premium quality", "long size",
    "home gym", "fitness gear", "sports equipment", "training mat", "NBR material",
    "grip technology", "professional grade", "carrying strap", "durable", "comfort"
  ],

  // Technical specifications
  specifications: {
    material: "Premium NBR (Nitrile Butadiene Rubber)",
    dimensions: "72\" x 24\" x 6mm (183cm x 61cm x 6mm)",
    weight: "1.2 kg",
    thickness: "6mm",
    surface: "Non-slip textured surface",
    features: ["Eco-friendly", "Easy to clean", "Odor-resistant", "Portable"],
    warranty: "1 year manufacturer warranty"
  },

  // Amazon workflow metadata
  workflowData: {
    sourceASIN: "B0DX1QJFK4",
    sourcePlatform: "Amazon India",
    sourcePrice: 379,
    profitMargin: 31.7,
    qualityScore: 92,
    processingTime: "4.09s",
    workflowId: "test-workflow-001",
    processedAt: new Date().toISOString()
  },

  // Social proof
  customerReviews: [
    {
      rating: 5,
      comment: "Excellent quality yoga mat! Very comfortable and durable.",
      reviewer: "Fitness Enthusiast",
      verified: true
    },
    {
      rating: 4,
      comment: "Great mat for home workouts. Non-slip surface works perfectly.",
      reviewer: "Home Gym Owner",
      verified: true
    }
  ],

  // Tags for filtering
  tags: ["premium", "non-slip", "durable", "bestseller", "eco-friendly"],

  // Shipping info
  shipping: {
    freeShipping: true,
    estimatedDelivery: "3-5 business days",
    weight: "1.2 kg",
    dimensions: "75cm x 25cm x 8cm"
  }
}

export async function GET(request: NextRequest) {
  try {
    // Return our test product data
    return NextResponse.json({
      success: true,
      product: testSportsProduct,
      message: "Test sports product loaded successfully",
      source: "Amazon workflow automation",
      metadata: {
        totalProducts: 1,
        category: "Sports & Fitness",
        workflowSource: "Automated Amazon listing system",
        lastUpdated: new Date().toISOString()
      }
    })
  } catch (error) {
    console.error('Error loading test product:', error)
    return NextResponse.json({
      success: false,
      error: 'Failed to load test product',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // Simulate adding product to Saleor backend
    const response = {
      success: true,
      message: "Product would be added to Saleor backend",
      productId: testSportsProduct.id,
      addedAt: new Date().toISOString(),
      listing: {
        platform: "CorelDove (Saleor)",
        status: "pending_review",
        url: `/products/${testSportsProduct.slug}`,
        nextSteps: [
          "Review product listing on CorelDove website",
          "Approve for Amazon SP-API submission",
          "Monitor performance and optimize"
        ]
      },
      ...body
    }

    console.log('Simulated product addition:', response)

    return NextResponse.json(response)
  } catch (error) {
    console.error('Error adding test product:', error)
    return NextResponse.json({
      success: false,
      error: 'Failed to add test product',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}
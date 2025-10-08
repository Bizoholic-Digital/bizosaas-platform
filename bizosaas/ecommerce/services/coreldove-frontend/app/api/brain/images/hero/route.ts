/**
 * Hero Images API - Serves hero section images via BizOSaaS Brain API
 * Uses existing product_image_handler.py integration
 */

import { NextRequest, NextResponse } from 'next/server'

// Environment variables
const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    // Call BizOSaaS Brain API for hero images
    const response = await fetch(`${BRAIN_API_URL}/api/brain/images/hero`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3003',
      }
    })

    if (!response.ok) {
      console.error('Brain API error:', response.status, response.statusText)
      // Fallback to direct Unsplash integration
      return NextResponse.json({
        success: true,
        images: getHeroImagesFallback()
      })
    }

    const heroData = await response.json()
    return NextResponse.json({
      success: true,
      images: heroData
    })

  } catch (error) {
    console.error('Hero images API error:', error)
    
    // Fallback response with direct Unsplash integration
    return NextResponse.json({
      success: true,
      images: getHeroImagesFallback()
    })
  }
}

// Fallback function using existing Unsplash category mappings
function getHeroImagesFallback() {
  const heroImages = [
    {
      url: "https://images.unsplash.com/photo-1498049794561-7780e7231661?w=300&h=300&fit=crop&auto=format&q=80",
      alt: "Electronics - Premium Quality Products",
      title: "Electronics | High-Tech Gadgets | Shop Online",
      category: "Electronics",
      featured: true
    },
    {
      url: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=300&h=300&fit=crop&auto=format&q=80", 
      alt: "Fashion - Trendy Clothing Collection",
      title: "Fashion | Latest Trends | Premium Clothing",
      category: "Clothing",
      featured: true
    },
    {
      url: "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300&h=300&fit=crop&auto=format&q=80",
      alt: "Home & Kitchen - Quality Home Products", 
      title: "Home & Kitchen | Quality Products | Fast Delivery",
      category: "Home & Kitchen",
      featured: true
    },
    {
      url: "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=300&h=300&fit=crop&auto=format&q=80",
      alt: "Beauty Products - Premium Cosmetics",
      title: "Beauty Products | Premium Cosmetics | Shop Now",
      category: "Beauty Products", 
      featured: true
    }
  ]

  return heroImages.map((image, index) => ({
    ...image,
    id: `hero-${index + 1}`,
    width: 300,
    height: 300,
    source: 'unsplash',
    seo_optimized: true
  }))
}
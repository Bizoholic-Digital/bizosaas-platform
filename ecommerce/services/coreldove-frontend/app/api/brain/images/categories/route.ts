/**
 * Category Images API - Serves category images via BizOSaaS Brain API
 * Uses existing product_image_handler.py integration
 */

import { NextRequest, NextResponse } from 'next/server'

// Environment variables
const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const categoryName = searchParams.get('category')
    const size = searchParams.get('size') || 'medium'
    
    if (!categoryName) {
      return NextResponse.json({ error: 'Category name is required' }, { status: 400 })
    }

    // Call BizOSaaS Brain API for category image
    const response = await fetch(`${BRAIN_API_URL}/api/brain/images/category`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3003',
      },
      body: JSON.stringify({
        category_name: categoryName,
        size: size,
        seo_optimized: true
      })
    })

    if (!response.ok) {
      console.error('Brain API error:', response.status, response.statusText)
      // Fallback to direct Unsplash integration
      return NextResponse.json({
        success: true,
        image: getCategoryImageFallback(categoryName, size)
      })
    }

    const imageData = await response.json()
    return NextResponse.json({
      success: true,
      image: imageData
    })

  } catch (error) {
    console.error('Category images API error:', error)
    
    // Fallback response with direct Unsplash integration
    const categoryName = new URL(request.url).searchParams.get('category') || 'Electronics'
    const size = new URL(request.url).searchParams.get('size') || 'medium'
    
    return NextResponse.json({
      success: true,
      image: getCategoryImageFallback(categoryName, size)
    })
  }
}

// Fallback function using existing Unsplash category mappings
function getCategoryImageFallback(categoryName: string, size: string) {
  const categoryImages = {
    "Mobile Accessories": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91",
    "Home & Kitchen": "https://images.unsplash.com/photo-1586201375761-83865001e31c", 
    "Clothing": "https://images.unsplash.com/photo-1441986300917-64674bd600d8",
    "Electronics": "https://images.unsplash.com/photo-1498049794561-7780e7231661",
    "Fitness Equipment": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b",
    "Beauty Products": "https://images.unsplash.com/photo-1596462502278-27bfdc403348",
    "Home Decor": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7",
    "Automotive Accessories": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d",
    "Sports & Outdoor": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b",
    "Books": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570",
    "Toys": "https://images.unsplash.com/photo-1558877385-9daf4b6a7f62",
    "Jewelry": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338"
  }

  // Size configurations
  const sizeParams = {
    'thumbnail': 'w=160&h=160',
    'small': 'w=300&h=300', 
    'medium': 'w=600&h=400',
    'large': 'w=1000&h=800'
  }

  // Get base image URL
  const normalizedName = categoryName?.trim() || ''
  let baseUrl = categoryImages["Electronics"] // Default fallback
  
  // Try exact match
  if (categoryImages[normalizedName as keyof typeof categoryImages]) {
    baseUrl = categoryImages[normalizedName as keyof typeof categoryImages]
  } else {
    // Try partial match
    const categoryKeys = Object.keys(categoryImages)
    const matchedKey = categoryKeys.find(key => 
      key.toLowerCase().includes(normalizedName.toLowerCase()) ||
      normalizedName.toLowerCase().includes(key.toLowerCase())
    )
    if (matchedKey) {
      baseUrl = categoryImages[matchedKey as keyof typeof categoryImages]
    }
  }

  // Build optimized URL
  const params = sizeParams[size as keyof typeof sizeParams] || sizeParams.medium
  const optimizedUrl = `${baseUrl}?${params}&fit=crop&auto=format&q=80`

  return {
    url: optimizedUrl,
    alt: `${categoryName} - Premium Products Category`,
    title: `${categoryName} | Best Deals | Shop ${categoryName} Products Online`,
    width: parseInt(params.match(/w=(\d+)/)?.[1] || '600'),
    height: parseInt(params.match(/h=(\d+)/)?.[1] || '400'),
    source: 'unsplash',
    seo_optimized: true
  }
}
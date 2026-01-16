import { NextRequest, NextResponse } from 'next/server';

// Backend API configuration
const BACKEND_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Mock featured businesses for fallback
const mockFeaturedBusinesses = [
  {
    id: 'biz_001',
    name: 'Bizoholic Marketing Agency',
    category: {
      id: 'marketing',
      name: 'Marketing',
      slug: 'marketing',
      icon: '📈',
      description: 'Digital marketing services',
      subcategories: [],
      businessCount: 15
    },
    subcategory: 'Digital Marketing',
    description: 'Full-service digital marketing agency specializing in AI-powered marketing automation',
    location: {
      address: '123 Marketing St',
      city: 'Business City',
      state: 'BC',
      zipCode: '12345',
      country: 'USA',
      coordinates: {
        lat: 40.7128,
        lng: -74.0060
      }
    },
    contact: {
      phone: '+1-555-MARKETING',
      email: 'hello@bizoholic.com',
      website: 'https://bizoholic.com'
    },
    rating: 4.8,
    reviewCount: 127,
    verified: true,
    claimed: true,
    featured: true,
    images: [
      'https://bizoholic.com/images/office1.jpg',
      'https://bizoholic.com/images/team.jpg'
    ],
    services: ['SEO', 'PPC', 'Social Media Marketing', 'Content Marketing', 'Email Marketing'],
    pricing: {
      range: '$$',
      currency: 'USD',
      description: 'Moderate pricing'
    },
    socialMedia: {
      facebook: 'https://facebook.com/bizoholic',
      twitter: 'https://twitter.com/bizoholic'
    },
    hours: {}
  }
];

export async function GET(request: NextRequest) {
  try {
    const backendUrl = `${BACKEND_API_URL}/api/brain/business-directory/businesses?featured=true`;
    console.log(`[BUSINESS-DIRECTORY] GET featured businesses: ${backendUrl}`);

    try {
      const response = await fetch(backendUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Business-Directory-Frontend/1.0.0'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log(`[BUSINESS-DIRECTORY] Featured businesses success: ${data.businesses?.length || 0} businesses`);

        // Extract just the businesses array for the featured endpoint
        return NextResponse.json(data.businesses || []);
      } else {
        console.warn(`[BUSINESS-DIRECTORY] Backend error: ${response.status}`);
        throw new Error(`Backend API error: ${response.status}`);
      }
    } catch (backendError) {
      console.error('[BUSINESS-DIRECTORY] Backend connection failed:', backendError);
      console.log('[BUSINESS-DIRECTORY] Using fallback featured businesses');

      return NextResponse.json(mockFeaturedBusinesses);
    }
  } catch (error) {
    console.error('[BUSINESS-DIRECTORY] API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error.message },
      { status: 500 }
    );
  }
}
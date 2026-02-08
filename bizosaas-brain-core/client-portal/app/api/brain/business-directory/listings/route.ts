import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Fallback data for development
const fallbackData = {
  listings: [
    {
      id: '1',
      name: 'Acme Restaurant',
      description: 'Fine dining experience with fresh seafood and premium steaks in a sophisticated atmosphere.',
      category: {
        id: '1',
        name: 'Restaurants',
        slug: 'restaurants'
      },
      subcategory: 'Fine Dining',
      location: {
        address: '123 Harbor View Drive',
        city: 'San Francisco',
        state: 'CA',
        zipCode: '94102',
        country: 'USA'
      },
      contact: {
        phone: '(555) 123-4567',
        email: 'info@acmerestaurant.com',
        website: 'https://acmerestaurant.com'
      },
      rating: 4.8,
      reviewCount: 234,
      status: 'active',
      verified: true,
      featured: true,
      images: [
        '/images/acme-restaurant-1.jpg',
        '/images/acme-restaurant-2.jpg'
      ],
      tags: ['fine dining', 'seafood', 'romantic', 'reservations'],
      hours: {
        monday: { open: '17:00', close: '22:00', closed: false },
        tuesday: { open: '17:00', close: '22:00', closed: false },
        wednesday: { open: '17:00', close: '22:00', closed: false },
        thursday: { open: '17:00', close: '22:00', closed: false },
        friday: { open: '17:00', close: '23:00', closed: false },
        saturday: { open: '17:00', close: '23:00', closed: false },
        sunday: { open: '17:00', close: '21:00', closed: false }
      },
      analytics: {
        views: 1234,
        clicks: 89,
        callClicks: 23,
        websiteClicks: 45,
        directionsClicks: 21
      },
      lastUpdated: '2024-01-13T10:30:00Z',
      createdAt: '2023-06-15T08:00:00Z'
    },
    {
      id: '2',
      name: 'Tech Solutions Hub',
      description: 'Professional computer repair and IT services for businesses and individuals.',
      category: {
        id: '4',
        name: 'Services',
        slug: 'services'
      },
      subcategory: 'Technology Services',
      location: {
        address: '456 Innovation Way',
        city: 'San Francisco',
        state: 'CA',
        zipCode: '94105',
        country: 'USA'
      },
      contact: {
        phone: '(555) 987-6543',
        email: 'support@techsolutionshub.com',
        website: 'https://techsolutionshub.com'
      },
      rating: 4.6,
      reviewCount: 78,
      status: 'active',
      verified: true,
      featured: false,
      images: [
        '/images/tech-hub-1.jpg'
      ],
      tags: ['computer repair', 'IT services', 'business support'],
      hours: {
        monday: { open: '09:00', close: '18:00', closed: false },
        tuesday: { open: '09:00', close: '18:00', closed: false },
        wednesday: { open: '09:00', close: '18:00', closed: false },
        thursday: { open: '09:00', close: '18:00', closed: false },
        friday: { open: '09:00', close: '18:00', closed: false },
        saturday: { open: '10:00', close: '16:00', closed: false },
        sunday: { open: '', close: '', closed: true }
      },
      analytics: {
        views: 892,
        clicks: 67,
        callClicks: 34,
        websiteClicks: 23,
        directionsClicks: 10
      },
      lastUpdated: '2024-01-10T15:45:00Z',
      createdAt: '2023-08-20T12:00:00Z'
    }
  ],
  total: 2,
  page: 1,
  limit: 20
};

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const page = searchParams.get('page') || '1';
    const limit = searchParams.get('limit') || '20';
    const status = searchParams.get('status') || '';

    const response = await fetch(`${BRAIN_API_URL}/api/brain/business-directory/listings?page=${page}&limit=${limit}&status=${status}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
    });

    if (!response.ok) {
      console.error('Business Directory Listings API error:', response.status);
      return NextResponse.json(fallbackData, { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Business Directory Listings API error:', error);
    return NextResponse.json(fallbackData, { status: 200 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/business-directory/listings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3006',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      console.error('Business Directory Create Listing API error:', response.status);
      return NextResponse.json({ 
        success: false, 
        message: 'Failed to create listing. Using fallback response.',
        listing: {
          id: Date.now().toString(),
          ...body,
          status: 'active',
          createdAt: new Date().toISOString()
        }
      }, { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Business Directory Create Listing API error:', error);
    return NextResponse.json({ 
      success: false, 
      message: 'Failed to create listing',
      error: error.message 
    }, { status: 500 });
  }
}
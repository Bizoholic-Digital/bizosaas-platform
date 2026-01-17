import { NextRequest, NextResponse } from 'next/server';
import { transformBusinessList } from '@/lib/business-hours-transformer';

// Backend API configuration - connects through Central Hub
const BACKEND_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Mock data for fallback when backend is unavailable
const mockBusinesses = [
  {
    id: '1',
    name: 'Blue Ocean Restaurant',
    description: 'Fresh seafood and coastal cuisine in a relaxed waterfront setting.',
    category: { id: '1', name: 'Restaurants', slug: 'restaurants' },
    subcategory: 'Fine Dining',
    contact: {
      phone: '(555) 123-4567',
      email: 'info@blueocean.com',
      website: 'https://blueocean.com'
    },
    location: {
      address: '123 Harbor View Drive',
      city: 'San Francisco',
      state: 'CA',
      zipCode: '94102',
      country: 'USA',
      coordinates: { lat: 37.7749, lng: -122.4194 }
    },
    rating: 4.5,
    reviewCount: 342,
    featured: true,
    verified: true,
    status: 'open',
    tags: ['seafood', 'waterfront', 'romantic', 'groups'],
    pricing: { range: '$$$', currency: 'USD', description: 'Premium dining experience' },
  },
  {
    id: '2',
    name: 'TechFix Solutions',
    description: 'Professional computer and smartphone repair services with same-day turnaround.',
    category: { id: '4', name: 'Services', slug: 'services' },
    subcategory: 'Electronics Repair',
    contact: {
      phone: '(555) 987-6543',
      email: 'support@techfix.com',
      website: 'https://techfix.com'
    },
    location: {
      address: '456 Tech Street',
      city: 'San Francisco',
      state: 'CA',
      zipCode: '94105',
      country: 'USA',
      coordinates: { lat: 37.7849, lng: -122.4094 }
    },
    rating: 4.8,
    reviewCount: 156,
    featured: false,
    verified: true,
    status: 'open',
    tags: ['computer repair', 'smartphone', 'fast service', 'warranty'],
    pricing: { range: '$$', currency: 'USD', description: 'Competitive repair pricing' },
  }
];

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const query = searchParams.get('query') || '';
    const location = searchParams.get('location') || '';
    const category = searchParams.get('category') || '';
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '20');

    // Build query string for backend
    const queryString = new URLSearchParams({
      query,
      location,
      category,
      page: page.toString(),
      limit: limit.toString()
    }).toString();

    console.log(`[BUSINESS-DIRECTORY] Searching businesses: ${BACKEND_API_URL}/api/brain/business-directory/businesses?${queryString}`);

    // Try to fetch from backend service
    try {
      const backendResponse = await fetch(`${BACKEND_API_URL}/api/brain/business-directory/search?${queryString}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Business-Directory-Frontend/1.0.0'
        }
      });

      if (backendResponse.ok) {
        const backendData = await backendResponse.json();
        console.log(`[BUSINESS-DIRECTORY] Backend response successful: ${backendData.businesses?.length || 0} businesses`);

        // Transform backend data to match frontend expectations
        const businesses = transformBusinessList(backendData.businesses || backendData.data || []);

        const response = {
          businesses,
          total: backendData.total || 0,
          page,
          limit,
          filters: { query, location, category },
          suggestions: backendData.suggestions || ['restaurants', 'tech repair', 'seafood', 'electronics', 'healthcare', 'retail'],
          source: 'backend'
        };

        return NextResponse.json(response);
      } else {
        console.warn(`[BUSINESS-DIRECTORY] Backend returned ${backendResponse.status}: ${backendResponse.statusText}`);
        throw new Error(`Backend API error: ${backendResponse.status}`);
      }
    } catch (backendError) {
      console.error('[BUSINESS-DIRECTORY] Backend connection failed:', backendError);

      // Fallback to mock data
      console.log('[BUSINESS-DIRECTORY] Using fallback mock data');

      // Filter mock businesses based on search criteria
      let filteredBusinesses = mockBusinesses;

      if (query) {
        filteredBusinesses = filteredBusinesses.filter(business =>
          business.name.toLowerCase().includes(query.toLowerCase()) ||
          business.description.toLowerCase().includes(query.toLowerCase()) ||
          (business.tags || []).some(tag => tag.toLowerCase().includes(query.toLowerCase()))
        );
      }

      if (location) {
        filteredBusinesses = filteredBusinesses.filter(business =>
          (business.location?.city || '').toLowerCase().includes(location.toLowerCase()) ||
          (business.location?.state || '').toLowerCase().includes(location.toLowerCase())
        );
      }

      if (category) {
        filteredBusinesses = filteredBusinesses.filter(business =>
          business.category.slug === category
        );
      }

      // Simulate pagination
      const startIndex = (page - 1) * limit;
      const endIndex = startIndex + limit;
      const paginatedBusinesses = filteredBusinesses.slice(startIndex, endIndex);

      const response = {
        businesses: paginatedBusinesses,
        total: filteredBusinesses.length,
        page,
        limit,
        filters: { query, location, category },
        suggestions: ['restaurants', 'tech repair', 'seafood', 'electronics', 'healthcare', 'retail'],
        source: 'fallback',
        warning: 'Backend service unavailable, using mock data'
      };

      return NextResponse.json(response);
    }
  } catch (error) {
    console.error('Business Directory API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: (error as any).message },
      { status: 500 }
    );
  }
}
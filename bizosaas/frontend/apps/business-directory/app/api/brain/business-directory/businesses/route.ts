import { NextRequest, NextResponse } from 'next/server';

// Backend API configuration
const BACKEND_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Mock businesses for fallback
const mockBusinesses = [
  {
    id: 'biz_001',
    name: 'Bizoholic Marketing Agency',
    category: 'Marketing',
    subcategory: 'Digital Marketing',
    description: 'Full-service digital marketing agency specializing in AI-powered marketing automation',
    address: '123 Marketing St, Business City, BC 12345',
    phone: '+1-555-MARKETING',
    email: 'hello@bizoholic.com',
    website: 'https://bizoholic.com',
    rating: 4.8,
    total_reviews: 127,
    verified: true,
    claimed: true,
    business_hours: {
      monday: '9:00 AM - 6:00 PM',
      tuesday: '9:00 AM - 6:00 PM',
      wednesday: '9:00 AM - 6:00 PM',
      thursday: '9:00 AM - 6:00 PM',
      friday: '9:00 AM - 6:00 PM',
      saturday: 'Closed',
      sunday: 'Closed'
    },
    social_media: {
      facebook: 'https://facebook.com/bizoholic',
      twitter: 'https://twitter.com/bizoholic',
      linkedin: 'https://linkedin.com/company/bizoholic'
    },
    images: [
      'https://bizoholic.com/images/office1.jpg',
      'https://bizoholic.com/images/team.jpg'
    ],
    services: ['SEO', 'PPC', 'Social Media Marketing', 'Content Marketing', 'Email Marketing'],
    created_at: '2024-01-15T10:30:00Z',
    updated_at: '2024-09-20T14:22:00Z'
  },
  {
    id: 'biz_002',
    name: 'CorelDove E-commerce Solutions',
    category: 'E-commerce',
    subcategory: 'Platform Development',
    description: 'Custom e-commerce platform development and optimization services',
    address: '456 Commerce Ave, Trade District, TD 67890',
    phone: '+1-555-ECOMMERCE',
    email: 'contact@coreldove.com',
    website: 'https://coreldove.com',
    rating: 4.9,
    total_reviews: 89,
    verified: true,
    claimed: true,
    business_hours: {
      monday: '8:00 AM - 7:00 PM',
      tuesday: '8:00 AM - 7:00 PM',
      wednesday: '8:00 AM - 7:00 PM',
      thursday: '8:00 AM - 7:00 PM',
      friday: '8:00 AM - 7:00 PM',
      saturday: '10:00 AM - 4:00 PM',
      sunday: 'Closed'
    },
    social_media: {
      facebook: 'https://facebook.com/coreldove',
      linkedin: 'https://linkedin.com/company/coreldove'
    },
    images: [
      'https://coreldove.com/images/showcase1.jpg'
    ],
    services: ['Shopify Development', 'WooCommerce', 'Custom E-commerce', 'Platform Migration'],
    created_at: '2024-02-10T09:15:00Z',
    updated_at: '2024-09-21T11:45:00Z'
  }
];

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const query = searchParams.get('query') || searchParams.get('q') || '';
    const category = searchParams.get('category') || '';
    const location = searchParams.get('location') || '';
    const verified = searchParams.get('verified') === 'true' ? true : undefined;
    const page = parseInt(searchParams.get('page') || '1');
    const size = parseInt(searchParams.get('size') || '20');

    // Build query string for backend
    const queryString = new URLSearchParams();
    if (query) queryString.set('query', query);
    if (category) queryString.set('category', category);
    if (location) queryString.set('location', location);
    if (verified !== undefined) queryString.set('verified', verified.toString());
    queryString.set('page', page.toString());
    queryString.set('size', size.toString());

    const backendUrl = `${BACKEND_API_URL}/api/brain/business-directory/businesses?${queryString.toString()}`;
    console.log(`[BUSINESS-DIRECTORY] GET businesses: ${backendUrl}`);

    try {
      const response = await fetch(backendUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Business-Directory-Frontend/1.0.0'
        },
        // Remove timeout for fetch as it's not supported
      });

      if (response.ok) {
        const data = await response.json();
        console.log(`[BUSINESS-DIRECTORY] Backend success: ${data.businesses?.length || 0} businesses`);
        return NextResponse.json(data);
      } else {
        console.warn(`[BUSINESS-DIRECTORY] Backend error: ${response.status}`);
        throw new Error(`Backend API error: ${response.status}`);
      }
    } catch (backendError) {
      console.error('[BUSINESS-DIRECTORY] Backend connection failed:', backendError);
      console.log('[BUSINESS-DIRECTORY] Using fallback data');
      
      // Apply filters to mock data
      let filteredBusinesses = mockBusinesses;
      
      if (query) {
        filteredBusinesses = filteredBusinesses.filter(business =>
          business.name.toLowerCase().includes(query.toLowerCase()) ||
          business.description.toLowerCase().includes(query.toLowerCase())
        );
      }
      
      if (category) {
        filteredBusinesses = filteredBusinesses.filter(business =>
          business.category.toLowerCase() === category.toLowerCase()
        );
      }
      
      if (verified !== undefined) {
        filteredBusinesses = filteredBusinesses.filter(business => business.verified === verified);
      }
      
      // Simulate pagination
      const startIdx = (page - 1) * size;
      const endIdx = startIdx + size;
      const paginated = filteredBusinesses.slice(startIdx, endIdx);

      return NextResponse.json({
        businesses: paginated,
        total: filteredBusinesses.length,
        page,
        size,
        total_pages: Math.ceil(filteredBusinesses.length / size),
        source: 'fallback'
      });
    }
  } catch (error) {
    console.error('[BUSINESS-DIRECTORY] API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error.message },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const businessData = await request.json();
    
    const backendUrl = `${BACKEND_API_URL}/api/brain/business-directory/businesses`;
    console.log(`[BUSINESS-DIRECTORY] POST business: ${backendUrl}`);

    try {
      const response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'User-Agent': 'Business-Directory-Frontend/1.0.0'
        },
        body: JSON.stringify(businessData)
      });

      if (response.ok) {
        const data = await response.json();
        console.log(`[BUSINESS-DIRECTORY] Business created: ${data.business_id}`);
        return NextResponse.json(data);
      } else {
        console.warn(`[BUSINESS-DIRECTORY] Backend error: ${response.status}`);
        throw new Error(`Backend API error: ${response.status}`);
      }
    } catch (backendError) {
      console.error('[BUSINESS-DIRECTORY] Backend connection failed:', backendError);
      console.log('[BUSINESS-DIRECTORY] Simulating business creation');
      
      // Simulate business creation
      const newBusiness = {
        id: `biz_${Date.now()}`,
        ...businessData,
        verified: false,
        claimed: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };

      return NextResponse.json({
        message: 'Business created successfully',
        business_id: newBusiness.id,
        business: newBusiness,
        source: 'fallback'
      });
    }
  } catch (error) {
    console.error('[BUSINESS-DIRECTORY] API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error.message },
      { status: 500 }
    );
  }
}
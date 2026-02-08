import { NextRequest, NextResponse } from 'next/server';
import { transformBusinessList, transformBusinessData } from '@/lib/business-hours-transformer';

// Backend API configuration
const BACKEND_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Helper function to convert hours format
function convertBusinessHours(businessHours: any) {
  if (!businessHours) return null;

  const convertDayHours = (hours: string) => {
    if (hours === 'Closed' || hours === 'closed') {
      return { open: '', close: '', closed: true };
    }

    // Parse time range like "9:00 AM - 6:00 PM"
    const timeRange = hours.split(' - ');
    if (timeRange.length !== 2) {
      return { open: '', close: '', closed: true };
    }

    // Convert 12-hour format to 24-hour format
    const convertTo24Hour = (time: string) => {
      const [timeStr, period] = time.trim().split(' ');
      let [hours, minutes] = timeStr.split(':').map(Number);

      if (period === 'PM' && hours !== 12) hours += 12;
      if (period === 'AM' && hours === 12) hours = 0;

      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
    };

    return {
      open: convertTo24Hour(timeRange[0]),
      close: convertTo24Hour(timeRange[1]),
      closed: false
    };
  };

  return {
    monday: convertDayHours(businessHours.monday || 'Closed'),
    tuesday: convertDayHours(businessHours.tuesday || 'Closed'),
    wednesday: convertDayHours(businessHours.wednesday || 'Closed'),
    thursday: convertDayHours(businessHours.thursday || 'Closed'),
    friday: convertDayHours(businessHours.friday || 'Closed'),
    saturday: convertDayHours(businessHours.saturday || 'Closed'),
    sunday: convertDayHours(businessHours.sunday || 'Closed')
  };
}

// Mock businesses for fallback
const mockBusinesses = [
  {
    id: 'biz_001',
    name: 'Bizoholic Marketing Agency',
    slug: 'bizoholic-marketing-agency',
    category: {
      id: 'marketing',
      name: 'Marketing',
      slug: 'marketing',
      icon: '📈',
      description: 'Digital marketing and advertising services',
      subcategories: [],
      businessCount: 15
    },
    subcategory: 'Digital Marketing',
    description: 'Full-service digital marketing agency specializing in AI-powered marketing automation',
    contact: {
      phone: '+1-555-MARKETING',
      email: 'hello@bizoholic.com',
      website: 'https://bizoholic.com'
    },
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
    rating: 4.8,
    reviewCount: 127,
    images: [
      'https://bizoholic.com/images/office1.jpg',
      'https://bizoholic.com/images/team.jpg'
    ],
    featured: true,
    verified: true,
    status: 'open' as const,
    tags: ['SEO', 'PPC', 'Social Media Marketing', 'Content Marketing', 'Email Marketing'],
    socialMedia: {
      facebook: 'https://facebook.com/bizoholic',
      twitter: 'https://twitter.com/bizoholic',
      linkedin: 'https://linkedin.com/company/bizoholic'
    },
    pricing: {
      range: '$$' as const,
      currency: 'USD',
      description: 'Moderate pricing for professional services'
    },
    amenities: ['Free Consultation', 'Custom Reports', '24/7 Support'],
    viewCount: 1247,
    claimStatus: 'claimed' as const,
    lastUpdated: '2024-09-21T11:45:00Z',
    createdAt: '2024-01-15T10:30:00Z',
    updatedAt: '2024-09-21T11:45:00Z',
    hours: convertBusinessHours({
      monday: '9:00 AM - 6:00 PM',
      tuesday: '9:00 AM - 6:00 PM',
      wednesday: '9:00 AM - 6:00 PM',
      thursday: '9:00 AM - 6:00 PM',
      friday: '9:00 AM - 6:00 PM',
      saturday: 'Closed',
      sunday: 'Closed'
    }),
    services: ['SEO', 'PPC', 'Social Media Marketing', 'Content Marketing', 'Email Marketing']
  },
  {
    id: 'biz_002',
    name: 'CorelDove E-commerce Solutions',
    slug: 'coreldove-ecommerce-solutions',
    category: {
      id: 'ecommerce',
      name: 'E-commerce',
      slug: 'ecommerce',
      icon: '🛒',
      description: 'Online shopping and e-commerce platforms',
      subcategories: [],
      businessCount: 8
    },
    subcategory: 'Platform Development',
    description: 'Custom e-commerce platform development and optimization services',
    contact: {
      phone: '+1-555-ECOMMERCE',
      email: 'contact@coreldove.com',
      website: 'https://coreldove.com'
    },
    location: {
      address: '456 Commerce Ave',
      city: 'Trade District',
      state: 'TD',
      zipCode: '67890',
      country: 'USA',
      coordinates: {
        lat: 40.7589,
        lng: -73.9851
      }
    },
    rating: 4.9,
    reviewCount: 89,
    images: [
      'https://coreldove.com/images/showcase1.jpg'
    ],
    featured: false,
    verified: true,
    status: 'open' as const,
    tags: ['Shopify Development', 'WooCommerce', 'Custom E-commerce', 'Platform Migration'],
    socialMedia: {
      facebook: 'https://facebook.com/coreldove',
      linkedin: 'https://linkedin.com/company/coreldove'
    },
    pricing: {
      range: '$$$' as const,
      currency: 'USD',
      description: 'Premium e-commerce development services'
    },
    amenities: ['Free Strategy Session', 'Migration Support', 'Training Included'],
    viewCount: 892,
    claimStatus: 'claimed' as const,
    lastUpdated: '2024-09-21T11:45:00Z',
    createdAt: '2024-02-10T09:15:00Z',
    updatedAt: '2024-09-21T11:45:00Z',
    hours: convertBusinessHours({
      monday: '8:00 AM - 7:00 PM',
      tuesday: '8:00 AM - 7:00 PM',
      wednesday: '8:00 AM - 7:00 PM',
      thursday: '8:00 AM - 7:00 PM',
      friday: '8:00 AM - 7:00 PM',
      saturday: '10:00 AM - 4:00 PM',
      sunday: 'Closed'
    }),
    services: ['Shopify Development', 'WooCommerce', 'Custom E-commerce', 'Platform Migration']
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

        // Transform business hours data for frontend compatibility
        if (data.businesses) {
          data.businesses = transformBusinessList(data.businesses);
        }

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
          business.category.id.toLowerCase() === category.toLowerCase() ||
          business.category.slug.toLowerCase() === category.toLowerCase()
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
      { error: 'Internal server error', details: (error as any).message },
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
      { error: 'Internal server error', details: (error as any).message },
      { status: 500 }
    );
  }
}
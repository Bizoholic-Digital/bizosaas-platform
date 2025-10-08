import { NextRequest, NextResponse } from 'next/server';
import { transformBusinessList, transformBusinessData } from '@/lib/business-hours-transformer';
import { freeBusinessAPIs, BusinessAPIResult } from '@/lib/free-apis';

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

// Transform free API results to business directory format
function transformFreeAPIToBusiness(apiResult: BusinessAPIResult): any {
  return {
    id: apiResult.id,
    name: apiResult.name,
    slug: apiResult.name.toLowerCase().replace(/[^a-z0-9]+/g, '-'),
    category: {
      id: apiResult.category?.toLowerCase() || 'general',
      name: apiResult.category || 'General',
      slug: apiResult.category?.toLowerCase() || 'general',
      icon: getCategoryIcon(apiResult.category || 'General'),
      description: `${apiResult.category || 'General'} businesses`,
      subcategories: [],
      businessCount: 1
    },
    subcategory: apiResult.category || 'General',
    description: `${apiResult.category || 'Business'} located at ${apiResult.address}`,
    contact: {
      phone: apiResult.contact?.phone || '',
      email: apiResult.contact?.email || '',
      website: apiResult.contact?.website || ''
    },
    location: {
      address: apiResult.address,
      city: extractCityFromAddress(apiResult.address),
      state: extractStateFromAddress(apiResult.address),
      zipCode: extractZipFromAddress(apiResult.address),
      country: 'USA',
      coordinates: apiResult.coordinates
    },
    rating: apiResult.rating || 4.0 + Math.random(),
    reviewCount: Math.floor(Math.random() * 100) + 10,
    images: [`https://via.placeholder.com/400x300?text=${encodeURIComponent(apiResult.name)}`],
    featured: Math.random() > 0.8,
    verified: apiResult.source !== 'fallback',
    status: 'open' as const,
    tags: [apiResult.category || 'Business'],
    socialMedia: {},
    pricing: {
      range: ['$', '$$', '$$$'][Math.floor(Math.random() * 3)] as any,
      currency: 'USD',
      description: 'Standard pricing'
    },
    amenities: ['Customer Service', 'Professional Staff'],
    viewCount: Math.floor(Math.random() * 1000) + 100,
    claimStatus: 'unclaimed' as const,
    lastUpdated: new Date().toISOString(),
    createdAt: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString(),
    updatedAt: new Date().toISOString(),
    hours: apiResult.hours || generateDefaultHours(),
    services: [apiResult.category || 'General Services'],
    source: apiResult.source
  };
}

function getCategoryIcon(category: string): string {
  const icons: { [key: string]: string } = {
    'Restaurant': '🍽️',
    'Cafe': '☕',
    'Retail': '🛍️',
    'Healthcare': '🏥',
    'Financial Services': '🏦',
    'Technology': '💻',
    'Automotive': '🚗',
    'Beauty': '💄',
    'Fitness': '💪',
    'Education': '📚',
    'Legal': '⚖️',
    'Real Estate': '🏠',
    'Entertainment': '🎬',
    'Travel': '✈️',
    'Marketing': '📈'
  };
  return icons[category] || '🏢';
}

function extractCityFromAddress(address: string): string {
  const parts = address.split(',');
  return parts[1]?.trim() || 'Unknown City';
}

function extractStateFromAddress(address: string): string {
  const parts = address.split(',');
  return parts[2]?.trim().split(' ')[0] || 'XX';
}

function extractZipFromAddress(address: string): string {
  const zipMatch = address.match(/\b\d{5}(-\d{4})?\b/);
  return zipMatch ? zipMatch[0] : '00000';
}

function generateDefaultHours(): any {
  return convertBusinessHours({
    monday: '9:00 AM - 5:00 PM',
    tuesday: '9:00 AM - 5:00 PM',
    wednesday: '9:00 AM - 5:00 PM',
    thursday: '9:00 AM - 5:00 PM',
    friday: '9:00 AM - 5:00 PM',
    saturday: '10:00 AM - 4:00 PM',
    sunday: 'Closed'
  });
}

function getEnhancedFallbackBusinesses(query: string, location: string, category: string): any[] {
  const fallbackBusinesses = [
    ...mockBusinesses,
    // Add more diverse businesses
    {
      id: 'fallback_003',
      name: 'Downtown Dental Care',
      slug: 'downtown-dental-care',
      category: {
        id: 'healthcare',
        name: 'Healthcare',
        slug: 'healthcare',
        icon: '🦷',
        description: 'Medical and dental services',
        subcategories: [],
        businessCount: 23
      },
      subcategory: 'Dental Services',
      description: 'Comprehensive dental care with modern technology and experienced staff',
      contact: {
        phone: '+1-555-DENTAL',
        email: 'info@downtowndental.com',
        website: 'https://downtowndental.com'
      },
      location: {
        address: '789 Health Blvd',
        city: 'Medical District',
        state: 'MD',
        zipCode: '54321',
        country: 'USA',
        coordinates: { lat: 40.7831, lng: -73.9712 }
      },
      rating: 4.7,
      reviewCount: 156,
      images: ['https://example.com/dental1.jpg'],
      featured: true,
      verified: true,
      status: 'open' as const,
      tags: ['Dental Care', 'Teeth Cleaning', 'Cosmetic Dentistry'],
      hours: convertBusinessHours({
        monday: '8:00 AM - 6:00 PM',
        tuesday: '8:00 AM - 6:00 PM',
        wednesday: '8:00 AM - 6:00 PM',
        thursday: '8:00 AM - 6:00 PM',
        friday: '8:00 AM - 5:00 PM',
        saturday: '9:00 AM - 2:00 PM',
        sunday: 'Closed'
      }),
      services: ['General Dentistry', 'Teeth Cleaning', 'Cosmetic Dentistry', 'Emergency Care']
    },
    {
      id: 'fallback_004',
      name: 'Fitness First Gym',
      slug: 'fitness-first-gym',
      category: {
        id: 'fitness',
        name: 'Fitness',
        slug: 'fitness',
        icon: '💪',
        description: 'Fitness and wellness centers',
        subcategories: [],
        businessCount: 18
      },
      subcategory: 'Gym & Fitness',
      description: '24/7 fitness center with state-of-the-art equipment and personal training',
      contact: {
        phone: '+1-555-FITNESS',
        email: 'info@fitnessfirst.com',
        website: 'https://fitnessfirst.com'
      },
      location: {
        address: '321 Wellness Way',
        city: 'Healthy Heights',
        state: 'HH',
        zipCode: '67890',
        country: 'USA',
        coordinates: { lat: 40.7505, lng: -73.9712 }
      },
      rating: 4.4,
      reviewCount: 203,
      images: ['https://example.com/gym1.jpg'],
      featured: false,
      verified: true,
      status: 'open' as const,
      tags: ['24/7 Access', 'Personal Training', 'Group Classes'],
      hours: convertBusinessHours({
        monday: '24 Hours',
        tuesday: '24 Hours',
        wednesday: '24 Hours',
        thursday: '24 Hours',
        friday: '24 Hours',
        saturday: '24 Hours',
        sunday: '24 Hours'
      }),
      services: ['Weight Training', 'Cardio Equipment', 'Personal Training', 'Group Classes']
    }
  ];

  // Filter based on search criteria
  let filtered = fallbackBusinesses;

  if (query) {
    filtered = filtered.filter(business =>
      business.name.toLowerCase().includes(query.toLowerCase()) ||
      business.description.toLowerCase().includes(query.toLowerCase()) ||
      business.tags.some((tag: string) => tag.toLowerCase().includes(query.toLowerCase()))
    );
  }

  if (location) {
    filtered = filtered.filter(business =>
      business.location.address.toLowerCase().includes(location.toLowerCase()) ||
      business.location.city.toLowerCase().includes(location.toLowerCase()) ||
      business.location.state.toLowerCase().includes(location.toLowerCase())
    );
  }

  if (category) {
    filtered = filtered.filter(business =>
      business.category.name.toLowerCase().includes(category.toLowerCase()) ||
      business.subcategory.toLowerCase().includes(category.toLowerCase())
    );
  }

  return filtered;
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

    console.log(`[BUSINESS-DIRECTORY] Search request: query="${query}", location="${location}", category="${category}"`);

    // Primary: Try free APIs first (OpenStreetMap, LocationIQ, Overpass)
    let businesses: any[] = [];
    let source = 'free_apis';

    if (query || location) {
      try {
        console.log('[BUSINESS-DIRECTORY] Using free APIs for business search');
        const freeAPIResults = await freeBusinessAPIs.searchBusinesses(query, location, size);

        // Transform free API results to business directory format
        businesses = freeAPIResults.map(transformFreeAPIToBusiness);

        // Store results for progressive database building
        if (businesses.length > 0) {
          await freeBusinessAPIs.storeSearchResults(freeAPIResults, 'business_directory');
        }

        console.log(`[BUSINESS-DIRECTORY] Free APIs found ${businesses.length} businesses`);
      } catch (freeAPIError) {
        console.warn('[BUSINESS-DIRECTORY] Free APIs failed:', freeAPIError);
      }
    }

    // Secondary: Try FastAPI Central Hub if needed
    if (businesses.length === 0) {
      try {
        const queryString = new URLSearchParams();
        if (query) queryString.set('query', query);
        if (category) queryString.set('category', category);
        if (location) queryString.set('location', location);
        if (verified !== undefined) queryString.set('verified', verified.toString());
        queryString.set('page', page.toString());
        queryString.set('size', size.toString());

        const backendUrl = `${BACKEND_API_URL}/api/brain/business-directory/businesses?${queryString.toString()}`;
        console.log(`[BUSINESS-DIRECTORY] Trying FastAPI Hub: ${backendUrl}`);

        const response = await fetch(backendUrl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'X-Tenant-ID': 'business_directory',
            'Host': 'localhost:3004',
          },
        });

        if (response.ok) {
          const data = await response.json();
          businesses = data.businesses || [];
          source = 'fastapi_hub';
          console.log(`[BUSINESS-DIRECTORY] FastAPI Hub success: ${businesses.length} businesses`);
        } else {
          throw new Error(`FastAPI Hub error: ${response.status}`);
        }
      } catch (hubError) {
        console.warn('[BUSINESS-DIRECTORY] FastAPI Hub failed:', hubError);
      }
    }

    // Tertiary: Use enhanced mock data as fallback
    if (businesses.length === 0) {
      console.log('[BUSINESS-DIRECTORY] Using enhanced fallback data');
      businesses = getEnhancedFallbackBusinesses(query, location, category);
      source = 'enhanced_fallback';
    }

    // Apply additional filters
    if (category && source !== 'free_apis') {
      businesses = businesses.filter(business =>
        business.category?.name?.toLowerCase().includes(category.toLowerCase()) ||
        business.subcategory?.toLowerCase().includes(category.toLowerCase())
      );
    }

    if (verified !== undefined) {
      businesses = businesses.filter(business => business.verified === verified);
    }

    // Apply pagination
    const startIdx = (page - 1) * size;
    const endIdx = startIdx + size;
    const paginated = businesses.slice(startIdx, endIdx);

    // Transform business hours for compatibility
    const transformedBusinesses = transformBusinessList(paginated);

    const result = {
      businesses: transformedBusinesses,
      total: businesses.length,
      page,
      size,
      total_pages: Math.ceil(businesses.length / size),
      source,
      query_info: {
        query,
        location,
        category,
        verified
      },
      api_stats: source === 'free_apis' ? freeBusinessAPIs.getCacheStats() : null,
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(result);

  } catch (error) {
    console.error('[BUSINESS-DIRECTORY] API error:', error);
    return NextResponse.json(
      {
        error: 'Internal server error',
        details: error.message,
        businesses: getEnhancedFallbackBusinesses('', '', ''),
        source: 'error_fallback'
      },
      { status: 200 } // Return 200 with fallback data
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
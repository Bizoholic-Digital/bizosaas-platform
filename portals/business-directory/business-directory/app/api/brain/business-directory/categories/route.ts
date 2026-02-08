import { NextRequest, NextResponse } from 'next/server';

// Backend API configuration
const BACKEND_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Mock categories for fallback
const mockCategories = [
  {
    id: 'cat_marketing',
    name: 'Marketing',
    description: 'Marketing and advertising services',
    subcategories: [
      { id: 'subcat_digital', name: 'Digital Marketing' },
      { id: 'subcat_traditional', name: 'Traditional Marketing' },
      { id: 'subcat_social', name: 'Social Media Marketing' }
    ],
    businessCount: 45,
    slug: 'marketing',
    icon: '📈'
  },
  {
    id: 'cat_ecommerce',
    name: 'E-commerce',
    description: 'Online retail and e-commerce services',
    subcategories: [
      { id: 'subcat_platform', name: 'Platform Development' },
      { id: 'subcat_design', name: 'Store Design' },
      { id: 'subcat_optimization', name: 'Conversion Optimization' }
    ],
    businessCount: 32,
    slug: 'ecommerce',
    icon: '🛒'
  },
  {
    id: 'cat_technology',
    name: 'Technology',
    description: 'Technology and software services',
    subcategories: [
      { id: 'subcat_software', name: 'Software Development' },
      { id: 'subcat_web', name: 'Web Development' },
      { id: 'subcat_mobile', name: 'Mobile Development' }
    ],
    businessCount: 78,
    slug: 'technology',
    icon: '💻'
  }
];

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const parent_id = searchParams.get('parent_id');

    // Build query string for backend
    const queryString = new URLSearchParams();
    if (parent_id) queryString.set('parent_id', parent_id);

    const backendUrl = `${BACKEND_API_URL}/api/brain/business-directory/categories?${queryString.toString()}`;
    console.log(`[BUSINESS-DIRECTORY] GET categories: ${backendUrl}`);

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
        console.log(`[BUSINESS-DIRECTORY] Categories success: ${data.categories?.length || 0} categories`);
        
        // Extract just the categories array for the frontend
        return NextResponse.json(data.categories || []);
      } else {
        console.warn(`[BUSINESS-DIRECTORY] Backend error: ${response.status}`);
        throw new Error(`Backend API error: ${response.status}`);
      }
    } catch (backendError) {
      console.error('[BUSINESS-DIRECTORY] Backend connection failed:', backendError);
      console.log('[BUSINESS-DIRECTORY] Using fallback categories');
      
      return NextResponse.json(mockCategories);
    }
  } catch (error) {
    console.error('[BUSINESS-DIRECTORY] API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: (error as any).message },
      { status: 500 }
    );
  }
}
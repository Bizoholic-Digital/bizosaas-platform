import { NextRequest, NextResponse } from "next/server";

const BRAIN_HUB_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://bizosaas-brain-unified:8001";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const queryString = searchParams.toString();
    const url = `${BRAIN_HUB_URL}/api/brain/wagtail/pages${queryString ? `?${queryString}` : ""}`;

    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": request.headers.get("authorization") || "",
      },
    });

    if (!response.ok) {
      throw new Error(`Brain Hub responded with status: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
    
  } catch (error) {
    console.error("Wagtail Pages API Error:", error);
    
    // Return fallback data for development
    const fallbackData = {
      success: true,
      pages: [
        {
          id: '1',
          title: 'Homepage',
          slug: 'home',
          status: 'published',
          created_at: '2024-01-15T10:00:00Z',
          updated_at: '2024-01-20T14:30:00Z',
          author: 'John Doe',
          views: 1245,
          content_type: 'homepage',
          meta_description: 'Welcome to our AI-powered marketing agency',
          seo_title: 'BizOSaaS - AI Marketing Solutions',
          featured_image: '/images/homepage-hero.jpg'
        },
        {
          id: '2',
          title: 'About Us',
          slug: 'about',
          status: 'published',
          created_at: '2024-01-10T09:00:00Z',
          updated_at: '2024-01-18T16:45:00Z',
          author: 'Jane Smith',
          views: 892,
          content_type: 'standard',
          meta_description: 'Learn about our mission to revolutionize digital marketing',
          seo_title: 'About BizOSaaS - Our Story',
          featured_image: '/images/about-team.jpg'
        },
        {
          id: '3',
          title: 'Services Overview',
          slug: 'services',
          status: 'draft',
          created_at: '2024-01-25T11:15:00Z',
          updated_at: '2024-01-25T11:15:00Z',
          author: 'Mike Johnson',
          views: 0,
          content_type: 'services',
          meta_description: 'Comprehensive marketing services powered by AI',
          seo_title: 'Marketing Services - BizOSaaS',
          featured_image: '/images/services-overview.jpg'
        },
        {
          id: '4',
          title: 'Case Studies',
          slug: 'case-studies',
          status: 'published',
          created_at: '2024-01-12T13:20:00Z',
          updated_at: '2024-01-22T10:15:00Z',
          author: 'Sarah Wilson',
          views: 567,
          content_type: 'case_studies',
          meta_description: 'Success stories from our clients',
          seo_title: 'Client Success Stories - BizOSaaS',
          featured_image: '/images/case-studies.jpg'
        },
        {
          id: '5',
          title: 'Contact Us',
          slug: 'contact',
          status: 'published',
          created_at: '2024-01-08T15:30:00Z',
          updated_at: '2024-01-16T09:45:00Z',
          author: 'David Chen',
          views: 334,
          content_type: 'contact',
          meta_description: 'Get in touch with our marketing experts',
          seo_title: 'Contact BizOSaaS - Let\'s Talk',
          featured_image: '/images/contact-hero.jpg'
        }
      ],
      pagination: {
        current_page: 1,
        total_pages: 1,
        total_count: 5,
        has_next: false,
        has_previous: false
      },
      filters: {
        available_statuses: ['published', 'draft', 'archived'],
        available_content_types: ['homepage', 'standard', 'services', 'case_studies', 'contact']
      },
      message: "Using fallback data - Brain Hub connection failed"
    };
    
    return NextResponse.json(fallbackData);
  }
}

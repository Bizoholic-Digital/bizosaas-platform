import { NextRequest, NextResponse } from "next/server";

const BRAIN_HUB_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://bizosaas-brain-unified:8001";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const queryString = searchParams.toString();
    const url = `${BRAIN_HUB_URL}/api/brain/wagtail/posts${queryString ? `?${queryString}` : ""}`;

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
    console.error("Wagtail Posts API Error:", error);

    // Return fallback data for development
    const fallbackData = {
      success: true,
      posts: [
        {
          id: '1',
          title: 'AI Marketing Trends for 2024',
          slug: 'ai-marketing-trends-2024',
          excerpt: 'Discover the latest AI marketing trends that are shaping the industry this year.',
          status: 'published',
          created_at: '2024-01-20T10:00:00Z',
          author: 'Sarah Wilson',
          category: 'Marketing',
          tags: ['AI', 'Marketing', 'Trends', '2024'],
          featured_image: '/blog/ai-marketing-trends.jpg',
          read_time: 5,
          views: 2341
        },
        {
          id: '2',
          title: 'Building Effective Email Campaigns',
          slug: 'building-effective-email-campaigns',
          excerpt: 'Learn how to create email campaigns that convert and engage your audience.',
          status: 'published',
          created_at: '2024-01-18T14:30:00Z',
          author: 'David Chen',
          category: 'Email Marketing',
          tags: ['Email', 'Campaigns', 'Conversion'],
          featured_image: '/blog/email-campaigns.jpg',
          read_time: 7,
          views: 1876
        },
        {
          id: '3',
          title: 'Social Media Strategy Guide',
          slug: 'social-media-strategy-guide',
          excerpt: 'A comprehensive guide to developing winning social media strategies.',
          status: 'draft',
          created_at: '2024-01-25T09:15:00Z',
          author: 'Lisa Park',
          category: 'Social Media',
          tags: ['Social Media', 'Strategy', 'Guide'],
          read_time: 8,
          views: 0
        },
        {
          id: '4',
          title: 'SEO Best Practices for 2024',
          slug: 'seo-best-practices-2024',
          excerpt: 'Stay ahead with the latest SEO techniques and algorithm updates.',
          status: 'published',
          created_at: '2024-01-22T11:45:00Z',
          author: 'Mike Johnson',
          category: 'SEO',
          tags: ['SEO', 'Best Practices', 'Algorithm'],
          featured_image: '/blog/seo-practices.jpg',
          read_time: 6,
          views: 3102
        }
      ],
      pagination: {
        current_page: 1,
        total_pages: 1,
        total_count: 4,
        has_next: false,
        has_previous: false
      },
      categories: ['Marketing', 'Email Marketing', 'Social Media', 'SEO', 'Content Marketing'],
      message: "Using fallback data - Brain Hub connection failed"
    };

    return NextResponse.json(fallbackData);
  }
}
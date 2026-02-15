import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth/auth-options";

const BRAIN_HUB_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://bizosaas-brain-unified:8001";

export async function GET(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    const { searchParams } = new URL(request.url);

    // Add tenant_id from session if available
    if (session?.user?.tenant_id) {
      searchParams.set('tenant_id', session.user.tenant_id);
    }

    const queryString = searchParams.toString();
    const url = `${BRAIN_HUB_URL}/api/brain/saleor/products${queryString ? `?${queryString}` : ""}`;

    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    // Add Authorization header from session
    if (session?.access_token) {
      headers["Authorization"] = `Bearer ${session.access_token}`;
    } else if (request.headers.get("authorization")) {
      headers["Authorization"] = request.headers.get("authorization")!;
    }

    const response = await fetch(url, {
      method: "GET",
      headers,
    });

    if (!response.ok) {
      throw new Error(`Brain Hub responded with status: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error("Saleor Products API Error:", errorMessage);

    // Return comprehensive fallback data for development
    const fallbackData = {
      success: true,
      products: [
        // Digital Marketing Services
        {
          id: "prod_001",
          name: "AI Campaign Management - Starter",
          sku: "AI-CAMP-START",
          description: "Automated campaign management for up to 3 platforms",
          price: 299.00,
          currency: "USD",
          stock: 999,
          category: "Digital Services",
          status: "active",
          image: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400",
          features: ["Google Ads", "Meta Ads", "LinkedIn Ads", "Monthly Reports"],
          rating: 4.8,
          reviews: 124
        },
        {
          id: "prod_002",
          name: "AI Campaign Management - Professional",
          sku: "AI-CAMP-PRO",
          description: "Full-service campaign management across all platforms",
          price: 799.00,
          currency: "USD",
          stock: 999,
          category: "Digital Services",
          status: "active",
          image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400",
          features: ["40+ Platforms", "AI Optimization", "24/7 Monitoring", "Weekly Reports"],
          rating: 4.9,
          reviews: 89
        },
        {
          id: "prod_003",
          name: "Content Generation Package",
          sku: "CONTENT-GEN-001",
          description: "AI-powered content creation for blogs and social media",
          price: 199.00,
          currency: "USD",
          stock: 999,
          category: "Digital Services",
          status: "active",
          image: "https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=400",
          features: ["10 Blog Posts/month", "30 Social Posts", "SEO Optimized", "Unlimited Revisions"],
          rating: 4.7,
          reviews: 156
        },
        {
          id: "prod_004",
          name: "SEO Optimization Service",
          sku: "SEO-OPT-001",
          description: "Complete SEO audit and optimization service",
          price: 499.00,
          currency: "USD",
          stock: 999,
          category: "Digital Services",
          status: "active",
          image: "https://images.unsplash.com/photo-1432888622747-4eb9a8f2c293?w=400",
          features: ["Technical SEO", "On-page Optimization", "Link Building", "Monthly Reports"],
          rating: 4.9,
          reviews: 203
        },
        {
          id: "prod_005",
          name: "Social Media Management - Basic",
          sku: "SMM-BASIC",
          description: "Professional social media management for 3 platforms",
          price: 349.00,
          currency: "USD",
          stock: 999,
          category: "Digital Services",
          status: "active",
          image: "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=400",
          features: ["3 Platforms", "20 Posts/month", "Community Management", "Analytics"],
          rating: 4.6,
          reviews: 178
        },
        // Marketing Tools & Software
        {
          id: "prod_006",
          name: "Marketing Analytics Dashboard",
          sku: "ANALYTICS-DASH",
          description: "Real-time marketing analytics and reporting tool",
          price: 49.00,
          currency: "USD",
          stock: 999,
          category: "Software",
          status: "active",
          image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400",
          features: ["Real-time Data", "Custom Reports", "API Access", "Unlimited Users"],
          rating: 4.8,
          reviews: 312
        },
        {
          id: "prod_007",
          name: "Email Marketing Platform",
          sku: "EMAIL-PLAT-001",
          description: "Complete email marketing automation platform",
          price: 79.00,
          currency: "USD",
          stock: 999,
          category: "Software",
          status: "active",
          image: "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=400",
          features: ["Unlimited Emails", "Automation", "A/B Testing", "Analytics"],
          rating: 4.7,
          reviews: 267
        },
        {
          id: "prod_008",
          name: "Landing Page Builder",
          sku: "LANDING-BUILD",
          description: "Drag-and-drop landing page builder with templates",
          price: 39.00,
          currency: "USD",
          stock: 999,
          category: "Software",
          status: "active",
          image: "https://images.unsplash.com/photo-1547658719-da2b51169166?w=400",
          features: ["100+ Templates", "Drag & Drop", "Mobile Responsive", "A/B Testing"],
          rating: 4.5,
          reviews: 445
        },
        // Training & Courses
        {
          id: "prod_009",
          name: "Digital Marketing Masterclass",
          sku: "COURSE-DM-001",
          description: "Complete digital marketing course with certification",
          price: 199.00,
          currency: "USD",
          stock: 999,
          category: "Education",
          status: "active",
          image: "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400",
          features: ["20 Hours Video", "Certificate", "Lifetime Access", "Community Support"],
          rating: 4.9,
          reviews: 892
        },
        {
          id: "prod_010",
          name: "SEO Fundamentals Course",
          sku: "COURSE-SEO-001",
          description: "Learn SEO from basics to advanced techniques",
          price: 149.00,
          currency: "USD",
          stock: 999,
          category: "Education",
          status: "active",
          image: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400",
          features: ["15 Hours Video", "Practical Projects", "SEO Tools Access", "Certificate"],
          rating: 4.8,
          reviews: 567
        },
        // Consultation Services
        {
          id: "prod_011",
          name: "Marketing Strategy Session",
          sku: "CONSULT-STRAT",
          description: "1-hour strategy consultation with marketing expert",
          price: 199.00,
          currency: "USD",
          stock: 50,
          category: "Consultation",
          status: "active",
          image: "https://images.unsplash.com/photo-1552664730-d307ca884978?w=400",
          features: ["1 Hour Session", "Action Plan", "Follow-up Email", "Recording"],
          rating: 5.0,
          reviews: 45
        },
        {
          id: "prod_012",
          name: "Website Audit Service",
          sku: "AUDIT-WEB-001",
          description: "Comprehensive website audit and recommendations",
          price: 299.00,
          currency: "USD",
          stock: 100,
          category: "Consultation",
          status: "active",
          image: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400",
          features: ["Technical Audit", "SEO Analysis", "UX Review", "Detailed Report"],
          rating: 4.9,
          reviews: 78
        }
      ],
      pagination: {
        total: 12,
        page: 1,
        pages: 1,
        per_page: 20
      },
      categories: [
        { id: "cat_001", name: "Digital Services", count: 5 },
        { id: "cat_002", name: "Software", count: 3 },
        { id: "cat_003", name: "Education", count: 2 },
        { id: "cat_004", name: "Consultation", count: 2 }
      ],
      message: "Using fallback data - Brain Hub connection failed",
      source: "fallback"
    };

    return NextResponse.json(fallbackData);
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    const body = await request.json();

    const url = `${BRAIN_HUB_URL}/api/brain/saleor/products`;

    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    if (session?.access_token) {
      headers["Authorization"] = `Bearer ${session.access_token}`;
    } else if (request.headers.get("authorization")) {
      headers["Authorization"] = request.headers.get("authorization")!;
    }

    const response = await fetch(url, {
      method: "POST",
      headers,
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error(`Brain Hub responded with status: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error("Error creating product:", errorMessage);
    return NextResponse.json({ error: "Failed to create product", details: errorMessage }, { status: 500 });
  }
}

export async function PUT(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    const body = await request.json();
    const { searchParams } = new URL(request.url);
    const productId = searchParams.get('product_id');

    if (!productId) {
      return NextResponse.json({ error: "Product ID is required" }, { status: 400 });
    }

    const url = `${BRAIN_HUB_URL}/api/brain/saleor/products/${productId}`;

    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    if (session?.access_token) {
      headers["Authorization"] = `Bearer ${session.access_token}`;
    } else if (request.headers.get("authorization")) {
      headers["Authorization"] = request.headers.get("authorization")!;
    }

    const response = await fetch(url, {
      method: "PUT",
      headers,
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error(`Brain Hub responded with status: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error("Error updating product:", errorMessage);
    return NextResponse.json({ error: "Failed to update product", details: errorMessage }, { status: 500 });
  }
}

import { NextRequest, NextResponse } from "next/server";

const BRAIN_HUB_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || "http://bizosaas-brain-unified:8001";

export async function GET(request: NextRequest) {
    try {
        const { searchParams } = new URL(request.url);
        const queryString = searchParams.toString();
        const url = `${BRAIN_HUB_URL}/api/v1/cms/posts/${queryString ? `?${queryString}` : ""}`;

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
        console.error("Wagtail Blog API Error:", error);

        // Return fallback data for development
        const fallbackData = {
            success: true,
            posts: [
                {
                    id: 1,
                    title: "Getting Started with Digital Marketing",
                    author: "Marketing Team",
                    category: "Marketing",
                    published_date: "2024-03-01",
                    excerpt: "Learn the basics of digital marketing..."
                },
                {
                    id: 2,
                    title: "10 SEO Tips for 2024",
                    author: "SEO Expert",
                    category: "SEO",
                    published_date: "2024-02-15",
                    excerpt: "Boost your search rankings with these tips..."
                }
            ],
            message: "Using fallback data - Brain Hub connection failed"
        };

        return NextResponse.json(fallbackData);
    }
}

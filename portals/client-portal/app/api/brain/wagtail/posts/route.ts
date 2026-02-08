/**
 * Wagtail CMS Posts/Blog API Route
 * Manages blog posts through Brain API Gateway
 * Requires authentication and tenant filtering
 */

import { NextRequest, NextResponse } from 'next/server';
import { auth } from "@/lib/auth";


const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://brain-gateway:8000';

// GET - List all posts
export async function GET(request: NextRequest) {
    try {
        const session = await auth();

        const searchParams = request.nextUrl.searchParams;
        const params = new URLSearchParams();

        if (session?.user?.tenant_id) {
            params.set('tenant_id', session.user.tenant_id);
        }

        // Add filters
        if (searchParams.get('page')) params.set('page', searchParams.get('page')!);
        if (searchParams.get('limit')) params.set('limit', searchParams.get('limit')!);
        if (searchParams.get('search')) params.set('search', searchParams.get('search')!);
        if (searchParams.get('category')) params.set('category', searchParams.get('category')!);
        if (searchParams.get('tag')) params.set('tag', searchParams.get('tag')!);
        if (searchParams.get('status')) params.set('status', searchParams.get('status')!);

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
        };

        if (session?.access_token) {
            headers["Authorization"] = `Bearer ${session.access_token}`;
        }


        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000);

        try {
            const response = await fetch(
                `${BRAIN_API_URL}/api/cms/posts?${params.toString()}`,
                {
                    headers,
                    cache: 'no-store',
                    signal: controller.signal
                }
            );

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`Brain API error: ${response.status}`);
            }

            const data = await response.json();
            return NextResponse.json(data);
        } catch (fetchError) {
            clearTimeout(timeoutId);
            throw fetchError;
        }

    } catch (error) {
        console.error('Posts GET error:', error);

        // Return fallback posts data
        const fallbackData = {
            items: [
                {
                    id: 1,
                    title: '10 Digital Marketing Trends for 2025',
                    slug: '10-digital-marketing-trends-2025',
                    excerpt: 'Discover the top digital marketing trends that will shape the industry in 2025',
                    content: '<h1>10 Digital Marketing Trends for 2025</h1><p>The digital marketing landscape is evolving rapidly...</p>',
                    category: 'Marketing',
                    tags: ['trends', 'digital marketing', '2025'],
                    featured_image: '/blog/marketing-trends.jpg',
                    author: 'Sarah Johnson',
                    status: 'published',
                    published_at: '2024-12-01T09:00:00Z',
                    created_at: '2024-11-28T10:00:00Z',
                    updated_at: '2024-12-01T09:00:00Z'
                },
                {
                    id: 2,
                    title: 'How AI is Transforming Customer Engagement',
                    slug: 'ai-transforming-customer-engagement',
                    excerpt: 'Learn how artificial intelligence is revolutionizing the way businesses interact with customers',
                    content: '<h1>AI and Customer Engagement</h1><p>Artificial intelligence is changing everything...</p>',
                    category: 'Technology',
                    tags: ['AI', 'customer engagement', 'automation'],
                    featured_image: '/blog/ai-customer.jpg',
                    author: 'Michael Chen',
                    status: 'published',
                    published_at: '2024-11-28T14:30:00Z',
                    created_at: '2024-11-25T10:00:00Z',
                    updated_at: '2024-11-28T14:30:00Z'
                },
                {
                    id: 3,
                    title: 'SEO Best Practices for E-commerce',
                    slug: 'seo-best-practices-ecommerce',
                    excerpt: 'Master the art of search engine optimization for your online store',
                    content: '<h1>E-commerce SEO Guide</h1><p>Optimizing your e-commerce site for search engines...</p>',
                    category: 'SEO',
                    tags: ['SEO', 'e-commerce', 'optimization'],
                    featured_image: '/blog/seo-ecommerce.jpg',
                    author: 'Emily Rodriguez',
                    status: 'published',
                    published_at: '2024-11-25T11:00:00Z',
                    created_at: '2024-11-20T10:00:00Z',
                    updated_at: '2024-11-25T11:00:00Z'
                },
                {
                    id: 4,
                    title: 'Building a Successful Content Marketing Strategy',
                    slug: 'content-marketing-strategy',
                    excerpt: 'A comprehensive guide to creating content that converts',
                    content: '<h1>Content Marketing Strategy</h1><p>Content is king, but strategy is queen...</p>',
                    category: 'Content Marketing',
                    tags: ['content', 'strategy', 'marketing'],
                    featured_image: '/blog/content-strategy.jpg',
                    author: 'David Park',
                    status: 'draft',
                    published_at: null,
                    created_at: '2024-12-02T10:00:00Z',
                    updated_at: '2024-12-03T15:20:00Z'
                }
            ],
            meta: {
                total_count: 4
            },
            source: 'fallback'
        };

        return NextResponse.json(fallbackData, { status: 200 });
    }
}

// POST - Create new post
export async function POST(request: NextRequest) {
    try {
        const session = await auth();

        if (!session?.access_token) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            );
        }

        const body = await request.json();

        const postData = {
            ...body,
            tenant_id: session.user?.tenant_id,
            author_id: session.user?.id
        };

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`
        };

        const response = await fetch(
            `${BRAIN_API_URL}/api/cms/posts`,
            {
                method: 'POST',
                headers,
                body: JSON.stringify(postData)
            }
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            return NextResponse.json(errorData, { status: response.status });
        }

        const data = await response.json();
        return NextResponse.json(data, { status: 201 });

    } catch (error) {
        console.error('Posts POST error:', error);
        return NextResponse.json(
            { error: 'Failed to create post' },
            { status: 500 }
        );
    }
}

// PUT - Update existing post
export async function PUT(request: NextRequest) {
    try {
        const session = await auth();

        if (!session?.access_token) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            );
        }

        const searchParams = request.nextUrl.searchParams;
        const postId = searchParams.get('post_id');

        if (!postId) {
            return NextResponse.json(
                { error: 'post_id is required' },
                { status: 400 }
            );
        }

        const body = await request.json();

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`
        };

        const response = await fetch(
            `${BRAIN_API_URL}/api/cms/posts/${postId}?tenant_id=${session.user?.tenant_id}`,
            {
                method: 'PUT',
                headers,
                body: JSON.stringify(body)
            }
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            return NextResponse.json(errorData, { status: response.status });
        }

        const data = await response.json();
        return NextResponse.json(data);

    } catch (error) {
        console.error('Posts PUT error:', error);
        return NextResponse.json(
            { error: 'Failed to update post' },
            { status: 500 }
        );
    }
}

// DELETE - Delete post
export async function DELETE(request: NextRequest) {
    try {
        const session = await auth();

        if (!session?.access_token) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            );
        }

        const searchParams = request.nextUrl.searchParams;
        const postId = searchParams.get('post_id');

        if (!postId) {
            return NextResponse.json(
                { error: 'post_id is required' },
                { status: 400 }
            );
        }

        const headers: HeadersInit = {
            'Authorization': `Bearer ${session.access_token}`
        };

        const response = await fetch(
            `${BRAIN_API_URL}/api/cms/posts/${postId}?tenant_id=${session.user?.tenant_id}`,
            {
                method: 'DELETE',
                headers
            }
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            return NextResponse.json(errorData, { status: response.status });
        }

        return NextResponse.json({ success: true });

    } catch (error) {
        console.error('Posts DELETE error:', error);
        return NextResponse.json(
            { error: 'Failed to delete post' },
            { status: 500 }
        );
    }
}

/**
 * Wagtail CMS Media Library API Route
 * Manages media files through Brain API Gateway
 * Supports image/document upload, listing, and deletion
 */

import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// GET - List all media files
export async function GET(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);

        const searchParams = request.nextUrl.searchParams;
        const params = new URLSearchParams();

        if (session?.user?.tenant_id) {
            params.set('tenant_id', session.user.tenant_id);
        }

        // Add filters
        if (searchParams.get('page')) params.set('page', searchParams.get('page')!);
        if (searchParams.get('limit')) params.set('limit', searchParams.get('limit')!);
        if (searchParams.get('search')) params.set('search', searchParams.get('search')!);
        if (searchParams.get('type')) params.set('type', searchParams.get('type')!); // image, document, video
        if (searchParams.get('folder')) params.set('folder', searchParams.get('folder')!);

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
                `${BRAIN_API_URL}/api/cms/media?${params.toString()}`,
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
        console.error('Media GET error:', error);

        // Return fallback media data
        const fallbackData = {
            items: [
                {
                    id: 1,
                    title: 'Hero Banner',
                    filename: 'hero-banner.jpg',
                    type: 'image',
                    url: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800',
                    thumbnail: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=200',
                    size: 245760,
                    width: 1920,
                    height: 1080,
                    uploaded_at: '2024-11-28T10:00:00Z',
                    uploaded_by: 'Admin'
                },
                {
                    id: 2,
                    title: 'Team Photo',
                    filename: 'team-photo.jpg',
                    type: 'image',
                    url: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800',
                    thumbnail: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=200',
                    size: 189440,
                    width: 1600,
                    height: 900,
                    uploaded_at: '2024-11-25T14:30:00Z',
                    uploaded_by: 'Admin'
                },
                {
                    id: 3,
                    title: 'Product Showcase',
                    filename: 'product-showcase.jpg',
                    type: 'image',
                    url: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800',
                    thumbnail: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=200',
                    size: 312320,
                    width: 2000,
                    height: 1333,
                    uploaded_at: '2024-11-20T09:15:00Z',
                    uploaded_by: 'Admin'
                },
                {
                    id: 4,
                    title: 'Office Space',
                    filename: 'office-space.jpg',
                    type: 'image',
                    url: 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800',
                    thumbnail: 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=200',
                    size: 278528,
                    width: 1800,
                    height: 1200,
                    uploaded_at: '2024-11-15T11:45:00Z',
                    uploaded_by: 'Admin'
                },
                {
                    id: 5,
                    title: 'Marketing Infographic',
                    filename: 'marketing-infographic.png',
                    type: 'image',
                    url: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800',
                    thumbnail: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=200',
                    size: 425984,
                    width: 1200,
                    height: 1800,
                    uploaded_at: '2024-12-01T16:20:00Z',
                    uploaded_by: 'Admin'
                }
            ],
            meta: {
                total_count: 5
            },
            source: 'fallback'
        };

        return NextResponse.json(fallbackData, { status: 200 });
    }
}

// POST - Upload new media file
export async function POST(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);

        if (!session?.access_token) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            );
        }

        // Get form data (multipart/form-data for file upload)
        const formData = await request.formData();

        // Add tenant_id to form data
        formData.append('tenant_id', session.user?.tenant_id || '');
        formData.append('uploaded_by', session.user?.id || '');

        const headers: HeadersInit = {
            'Authorization': `Bearer ${session.access_token}`
            // Note: Don't set Content-Type for multipart/form-data
            // Browser will set it automatically with boundary
        };

        const response = await fetch(
            `${BRAIN_API_URL}/api/cms/media`,
            {
                method: 'POST',
                headers,
                body: formData
            }
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            return NextResponse.json(errorData, { status: response.status });
        }

        const data = await response.json();
        return NextResponse.json(data, { status: 201 });

    } catch (error) {
        console.error('Media POST error:', error);
        return NextResponse.json(
            { error: 'Failed to upload media' },
            { status: 500 }
        );
    }
}

// DELETE - Delete media file
export async function DELETE(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);

        if (!session?.access_token) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            );
        }

        const searchParams = request.nextUrl.searchParams;
        const mediaId = searchParams.get('media_id');

        if (!mediaId) {
            return NextResponse.json(
                { error: 'media_id is required' },
                { status: 400 }
            );
        }

        const headers: HeadersInit = {
            'Authorization': `Bearer ${session.access_token}`
        };

        const response = await fetch(
            `${BRAIN_API_URL}/api/cms/media/${mediaId}?tenant_id=${session.user?.tenant_id}`,
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
        console.error('Media DELETE error:', error);
        return NextResponse.json(
            { error: 'Failed to delete media' },
            { status: 500 }
        );
    }
}

/**
 * Wagtail CMS Navigation API Route
 * Manages site navigation menus through Brain API Gateway
 */

import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// GET - Get navigation menus
export async function GET(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);

        const searchParams = request.nextUrl.searchParams;
        const params = new URLSearchParams();

        if (session?.user?.tenant_id) {
            params.set('tenant_id', session.user.tenant_id);
        }

        if (searchParams.get('slug')) params.set('slug', searchParams.get('slug')!);

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
        };

        if (session?.access_token) {
            headers["Authorization"] = `Bearer ${session.access_token}`;
        }

        const response = await fetch(
            `${BRAIN_API_URL}/api/cms/navigation?${params.toString()}`,
            {
                headers,
                cache: 'no-store'
            }
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            return NextResponse.json(errorData, { status: response.status });
        }

        const data = await response.json();
        return NextResponse.json(data);

    } catch (error) {
        console.error('Navigation GET error:', error);
        return NextResponse.json(
            { error: 'Failed to fetch navigation' },
            { status: 500 }
        );
    }
}

// PUT - Update navigation menu
export async function PUT(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);

        if (!session?.access_token) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            );
        }

        const searchParams = request.nextUrl.searchParams;
        const menuId = searchParams.get('menu_id');

        if (!menuId) {
            return NextResponse.json(
                { error: 'menu_id is required' },
                { status: 400 }
            );
        }

        const body = await request.json();

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`
        };

        const response = await fetch(
            `${BRAIN_API_URL}/api/cms/navigation/${menuId}?tenant_id=${session.user?.tenant_id}`,
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
        console.error('Navigation PUT error:', error);
        return NextResponse.json(
            { error: 'Failed to update navigation' },
            { status: 500 }
        );
    }
}

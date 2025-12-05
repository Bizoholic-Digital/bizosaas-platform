/**
 * Wagtail CMS Forms API Route
 * Manages form submissions and definitions
 */

import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// GET - List form submissions
export async function GET(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);

        if (!session?.access_token) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            );
        }

        const searchParams = request.nextUrl.searchParams;
        const params = new URLSearchParams();

        if (session?.user?.tenant_id) {
            params.set('tenant_id', session.user.tenant_id);
        }

        if (searchParams.get('form_id')) params.set('form_id', searchParams.get('form_id')!);
        if (searchParams.get('page')) params.set('page', searchParams.get('page')!);
        if (searchParams.get('limit')) params.set('limit', searchParams.get('limit')!);

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`
        };

        const response = await fetch(
            `${BRAIN_API_URL}/api/cms/forms/submissions?${params.toString()}`,
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
        console.error('Forms GET error:', error);
        return NextResponse.json(
            { error: 'Failed to fetch form submissions' },
            { status: 500 }
        );
    }
}

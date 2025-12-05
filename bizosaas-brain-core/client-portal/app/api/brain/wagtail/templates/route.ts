/**
 * Wagtail CMS Templates API Route
 * Manages page templates
 */

import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// GET - List available templates
export async function GET(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
        };

        if (session?.access_token) {
            headers["Authorization"] = `Bearer ${session.access_token}`;
        }

        const response = await fetch(
            `${BRAIN_API_URL}/api/cms/templates`,
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
        console.error('Templates GET error:', error);
        return NextResponse.json(
            { error: 'Failed to fetch templates' },
            { status: 500 }
        );
    }
}

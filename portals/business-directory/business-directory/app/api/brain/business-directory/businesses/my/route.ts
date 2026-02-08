import { NextRequest, NextResponse } from 'next/server';

// Backend API configuration
const BACKEND_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function GET(request: NextRequest) {
    try {
        const backendUrl = `${BACKEND_API_URL}/api/brain/business-directory/businesses/my`;

        // Forward the Authorization header if present
        const authHeader = request.headers.get('authorization');

        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
            'User-Agent': 'Business-Directory-Frontend/1.0.0'
        };

        if (authHeader) {
            headers['Authorization'] = authHeader;
        }

        const response = await fetch(backendUrl, {
            method: 'GET',
            headers: headers,
        });

        if (response.ok) {
            const data = await response.json();
            return NextResponse.json(data);
        } else {
            return NextResponse.json(
                { error: 'Failed to fetch user listings' },
                { status: response.status }
            );
        }
    } catch (error: any) {
        console.error('[BUSINESS-DIRECTORY] API proxy error:', error);
        return NextResponse.json(
            { error: 'Internal server error', details: error.message },
            { status: 500 }
        );
    }
}

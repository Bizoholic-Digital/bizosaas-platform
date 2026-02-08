import { NextRequest, NextResponse } from 'next/server';

const BACKEND_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function POST(
    request: NextRequest,
    { params }: { params: { id: string } }
) {
    const businessId = params.id;

    try {
        const url = `${BACKEND_API_URL}/api/brain/business-directory/businesses/${businessId}/analyze`;
        console.log(`[BUSINESS-DIRECTORY] Proxying analyze for business ${businessId} to ${url}`);

        // Forward Authorization header if present
        const authHeader = request.headers.get('authorization');
        const headers: HeadersInit = {
            'Content-Type': 'application/json',
            'User-Agent': 'Business-Directory-Frontend/1.0.0'
        };
        if (authHeader) {
            headers['Authorization'] = authHeader;
        }

        const response = await fetch(url, {
            method: 'POST',
            headers: headers
        });

        const data = await response.json();

        if (response.ok) {
            return NextResponse.json(data);
        } else {
            return NextResponse.json(data, { status: response.status });
        }
    } catch (error: any) {
        console.error('[BUSINESS-DIRECTORY] Analyze API proxy error:', error);
        return NextResponse.json(
            { error: 'Internal server error', details: error.message },
            { status: 500 }
        );
    }
}

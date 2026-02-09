import { NextRequest, NextResponse } from 'next/server';

const BACKEND_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function POST(
    request: NextRequest,
    { params }: { params: { id: string } }
) {
    const claimId = params.id;

    try {
        const body = await request.json();
        const backendUrl = `${BACKEND_API_URL}/api/brain/business-directory/claims/${claimId}/verify`;

        console.log(`[BUSINESS-DIRECTORY] Proxying verification for claim ${claimId} to ${backendUrl}`);

        const response = await fetch(backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'User-Agent': 'Business-Directory-Frontend/1.0.0'
            },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (response.ok) {
            return NextResponse.json(data);
        } else {
            console.warn(`[BUSINESS-DIRECTORY] Verify backend error: ${response.status}`, data);
            return NextResponse.json(data, { status: response.status });
        }
    } catch (error: any) {
        console.error('[BUSINESS-DIRECTORY] Verify API proxy error:', error);
        return NextResponse.json(
            { error: 'Internal server error', details: error.message },
            { status: 500 }
        );
    }
}

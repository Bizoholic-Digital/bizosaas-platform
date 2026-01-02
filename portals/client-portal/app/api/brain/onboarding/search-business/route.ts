import { NextRequest, NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

export async function GET(request: NextRequest) {
    try {
        const token = await getToken({ req: request });
        if (!token) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const { searchParams } = new URL(request.url);
        const q = searchParams.get('q');

        if (!q) {
            return NextResponse.json({ error: 'Query parameter q is required' }, { status: 400 });
        }

        // Use internal Docker network URL or public URL
        const backendUrl = process.env.BRAIN_GATEWAY_URL || 'http://brain-gateway:8000';

        const response = await fetch(`${backendUrl}/api/onboarding/search-business?q=${encodeURIComponent(q)}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token.accessToken}`,
            },
        });

        const data = await response.json();

        if (!response.ok) {
            return NextResponse.json(data, { status: response.status });
        }

        return NextResponse.json(data);
    } catch (error) {
        console.error('Business search error:', error);
        return NextResponse.json(
            { error: 'Internal Server Error' },
            { status: 500 }
        );
    }
}

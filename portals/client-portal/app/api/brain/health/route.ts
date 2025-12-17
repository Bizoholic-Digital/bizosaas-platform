import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
    try {
        const backendUrl = process.env.BRAIN_GATEWAY_URL || 'http://localhost:8001';
        const response = await fetch(`${backendUrl}/health`, {
            next: { revalidate: 30 }
        });

        if (response.ok) {
            return NextResponse.json({ status: 'healthy' });
        }
        return NextResponse.json({ status: 'degraded' }, { status: 503 });
    } catch (error) {
        return NextResponse.json({ status: 'down' }, { status: 503 });
    }
}

import { NextRequest, NextResponse } from 'next/server';
import { BRAIN_GATEWAY_URL } from '../config';
import { auth } from '@clerk/nextjs/server';

export async function GET(request: NextRequest) {
    try {
        const { getToken } = await auth();
        const token = await getToken();

        const response = await fetch(`${BRAIN_GATEWAY_URL}/health`, {
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

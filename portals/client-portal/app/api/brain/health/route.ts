import { NextRequest, NextResponse } from 'next/server';
import { BRAIN_GATEWAY_URL } from '../config';
import { auth } from '@/lib/auth';

export async function GET(request: NextRequest) {
    try {
        const response = await fetch(`${BRAIN_GATEWAY_URL}/health`, {
            next: { revalidate: 30 }
        });

        const data = await response.json();

        if (response.ok) {
            return NextResponse.json(data);
        }
        return NextResponse.json(data, { status: response.status });
    } catch (error) {
        return NextResponse.json({ status: 'down', message: 'Could not connect to Brain Gateway' }, { status: 503 });
    }
}

import { NextResponse } from 'next/server';
import { BRAIN_GATEWAY_URL } from '../brain/config';

export const dynamic = 'force-dynamic';

export async function GET() {
    // Only allow in development or staging
    if (process.env.NODE_ENV === 'production' && !process.env.BRAIN_GATEWAY_URL?.includes('staging')) {
        // return NextResponse.json({ error: 'Not allowed' }, { status: 403 });
        // Allow for now since we are debugging staging production
    }

    return NextResponse.json({
        config_value: BRAIN_GATEWAY_URL,
        process_env_brain_gateway: process.env.BRAIN_GATEWAY_URL,
        process_env_next_public_brain_gateway: process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL,
        node_env: process.env.NODE_ENV,
        // Check if we can resolve the host
        timestamp: new Date().toISOString()
    });
}

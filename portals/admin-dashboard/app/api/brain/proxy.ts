import { NextRequest, NextResponse } from 'next/server';
import { BRAIN_GATEWAY_URL } from './config';
import { auth } from '@clerk/nextjs/server';

export async function proxyRequest(request: NextRequest, targetPath: string) {
    const url = `${BRAIN_GATEWAY_URL}/${targetPath.replace(/^\//, '')}`;

    try {
        const headers = new Headers(request.headers);
        headers.delete('host');
        headers.delete('connection');

        // 1. Get Clerk Token (Server-Side)
        let sessionToken: string | null = null;
        try {
            const { getToken } = await auth();
            sessionToken = await getToken();
        } catch (authError) {
            console.warn("Proxy: Failed to retrieve Clerk token", authError);
        }

        // 2. Pass auth token (Priority to server session)
        if (sessionToken) {
            headers.set('Authorization', `Bearer ${sessionToken}`);
        } else {
            const authHeader = request.headers.get('authorization');
            if (authHeader) {
                headers.set('Authorization', authHeader);
            }
        }

        const body = request.body;

        // Fetch from Gateway
        const response = await fetch(url, {
            method: request.method,
            headers: headers,
            body: ['GET', 'HEAD'].includes(request.method) ? undefined : body,
            // @ts-ignore - duplex is needed for streaming body proxying
            duplex: 'half'
        });

        const data = await response.text();

        // Forward response
        return new NextResponse(data, {
            status: response.status,
            headers: {
                'Content-Type': response.headers.get('Content-Type') || 'application/json',
            }
        });
    } catch (error: any) {
        console.error(`Proxy Error to ${url}:`, error);
        return NextResponse.json({ error: 'Gateway unavailable', details: error.message }, { status: 502 });
    }
}

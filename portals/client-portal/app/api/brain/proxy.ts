import { NextRequest, NextResponse } from 'next/server';
import { BRAIN_GATEWAY_URL } from './config';
import { auth } from '@/lib/auth';

export async function proxyRequest(request: NextRequest, targetPath: string) {
    const url = `${BRAIN_GATEWAY_URL}/${targetPath.replace(/^\//, '')}`;

    try {
        const headers = new Headers(request.headers);
        headers.delete('host');
        headers.delete('connection');

        // 1. Get Session Token (Server-Side) with Error Handling
        let sessionToken: string | undefined;
        try {
            const session = await auth();
            // @ts-ignore
            sessionToken = session?.access_token;
        } catch (authError) {
            console.warn("Proxy: Failed to retrieve auth session", authError);
            // Continue without session token
        }

        // 2. Pass auth token (Session priority, fallback to header)
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
            // @ts-ignore - duplplex is needed for streaming body proxying in node environment, though fetch might handle it
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

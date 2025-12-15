import { NextRequest, NextResponse } from 'next/server';
import { BRAIN_GATEWAY_URL } from './config';

export async function proxyRequest(request: NextRequest, targetPath: string) {
    const url = `${BRAIN_GATEWAY_URL}/${targetPath.replace(/^\//, '')}`;

    try {
        const headers = new Headers(request.headers);
        headers.delete('host');
        headers.delete('connection');

        // Pass auth token if present
        const authHeader = request.headers.get('authorization');
        if (authHeader) {
            headers.set('Authorization', authHeader);
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

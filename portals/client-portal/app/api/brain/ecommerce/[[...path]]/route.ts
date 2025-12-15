import { NextRequest } from 'next/server';
import { proxyRequest } from '../../proxy';

// Handler for all methods
async function handler(request: NextRequest, { params }: { params: { path?: string[] } }) {
    const pathSegments = params.path || [];
    const path = pathSegments.join('/');
    // Forward to /api/ecommerce/...
    return proxyRequest(request, `api/ecommerce/${path}`);
}

export const GET = handler;
export const POST = handler;
export const PUT = handler;
export const DELETE = handler;

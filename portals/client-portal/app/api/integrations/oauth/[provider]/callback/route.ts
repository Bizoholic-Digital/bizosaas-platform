import { NextRequest, NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

export async function GET(
    request: NextRequest,
    { params }: { params: { provider: string } }
) {
    // Note: This endpoint is called by the Provider (Google, etc.) as a redirect
    // Use cookies or state to validate session if JWT isn't available in headers (it won't be on callback)

    const { searchParams } = new URL(request.url);
    const code = searchParams.get('code');
    const state = searchParams.get('state');
    const error = searchParams.get('error');

    if (error) {
        return NextResponse.redirect(new URL(`/dashboard?tab=connectors&error=${error}`, request.url));
    }

    if (!code || !state) {
        return NextResponse.redirect(new URL(`/dashboard?tab=connectors&error=missing_params`, request.url));
    }

    try {
        const decodedState = JSON.parse(Buffer.from(state, 'base64').toString('utf-8'));
        const { userId, tenantId, redirectUrl } = decodedState;

        // In a real implementation:
        // 1. Call Brain Service to exchange code for tokens
        // 2. Brain Service stores tokens in Vault
        // 3. Brain Service triggers Temporal workflow for data sync

        const BRAIN_GATEWAY_URL = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8001';
        const response = await fetch(`${BRAIN_GATEWAY_URL}/api/v1/integrations/oauth/callback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // We might need a system-to-system secret here if we can't propagate user context easily
                'X-System-Secret': process.env.SYSTEM_SECRET || 'development-secret'
            },
            body: JSON.stringify({
                provider: params.provider,
                code,
                redirectUri: `${process.env.NEXTAUTH_URL}/api/integrations/oauth/${params.provider}/callback`,
                userId,
                tenantId
            })
        });

        if (!response.ok) {
            console.error('Failed to exchange token via Brain:', await response.text());
            return NextResponse.redirect(new URL(`${redirectUrl}&error=exchange_failed`, request.url));
        }

        return NextResponse.redirect(new URL(`${redirectUrl}&success=true`, request.url));

    } catch (e) {
        console.error('OAuth callback error:', e);
        return NextResponse.redirect(new URL(`/dashboard?tab=connectors&error=server_error`, request.url));
    }
}

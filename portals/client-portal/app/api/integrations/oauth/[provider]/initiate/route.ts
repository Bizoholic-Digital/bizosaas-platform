import { NextRequest, NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

export async function GET(
    request: NextRequest,
    { params }: { params: { provider: string } }
) {
    const token = await getToken({ req: request });
    if (!token) {
        return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { provider } = params;
    const { searchParams } = new URL(request.url);
    const redirectUrl = searchParams.get('redirectUrl') || '/dashboard?tab=connectors';

    // In a real implementation:
    // 1. Generate CSRF state
    // 2. Construct OAuth URL for the provider (Google, HubSpot, etc.)
    // 3. Store state in redis/db linked to user session

    let oauthUrl = '';
    const state = Buffer.from(JSON.stringify({
        userId: token.id,
        tenantId: token.tenant_id,
        redirectUrl,
        nonce: Math.random().toString(36).substring(7)
    })).toString('base64');

    const CLIENT_ID = process.env[`${provider.toUpperCase()}_CLIENT_ID`];
    const CALLBACK_URL = `${process.env.NEXTAUTH_URL}/api/integrations/oauth/${provider}/callback`;

    switch (provider) {
        case 'google-analytics':
            oauthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${CLIENT_ID}&redirect_uri=${CALLBACK_URL}&response_type=code&scope=https://www.googleapis.com/auth/analytics.readonly&state=${state}&access_type=offline&prompt=consent`;
            break;
        case 'hubspot':
            oauthUrl = `https://app.hubspot.com/oauth/authorize?client_id=${CLIENT_ID}&redirect_uri=${CALLBACK_URL}&scope=crm.objects.contacts.read&state=${state}`;
            break;
        default:
            return NextResponse.json({ error: 'Unsupported provider' }, { status: 400 });
    }

    // For now, return the URL so frontend can redirect
    return NextResponse.json({ url: oauthUrl });
}

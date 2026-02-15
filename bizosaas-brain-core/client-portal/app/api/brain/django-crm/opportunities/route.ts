import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth/auth-options";

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

export async function GET(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);
        const searchParams = request.nextUrl.searchParams;
        const params = new URLSearchParams();

        // Add tenant_id from session if available
        if (session?.user?.tenant_id) {
            params.set('tenant_id', session.user.tenant_id);
        }

        // Add any query params
        searchParams.forEach((value, key) => {
            params.set(key, value);
        });

        const url = `${BRAIN_API_URL}/api/crm/opportunities${params.toString() ? `?${params.toString()}` : ''}`;

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
        };

        if (session?.access_token) {
            headers["Authorization"] = `Bearer ${session.access_token}`;
        } else if (request.headers.get("authorization")) {
            headers["Authorization"] = request.headers.get("authorization")!;
        }

        const response = await fetch(url, {
            headers,
            cache: 'no-store',
        })

        if (!response.ok) {
            throw new Error(`FastAPI AI Central Hub responded with status: ${response.status}`)
        }

        const data = await response.json()
        return NextResponse.json(data)
    } catch (error) {
        console.error('Error fetching opportunities from Django CRM via Brain API:', error)

        // Fallback data
        const fallbackData = {
            opportunities: [
                { id: 1, title: 'Q1 Expansion Deal', value: 75000, stage: 'Discovery', company: 'MegaCorp Inc.' },
                { id: 2, title: 'Annual Renewal', value: 25000, stage: 'Proposal', company: 'Local Business LLC' }
            ]
        }
        return NextResponse.json(fallbackData)
    }
}

export async function POST(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);
        const body = await request.json();

        const url = `${BRAIN_API_URL}/api/crm/opportunities`;

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
        };

        if (session?.access_token) {
            headers["Authorization"] = `Bearer ${session.access_token}`;
        } else if (request.headers.get("authorization")) {
            headers["Authorization"] = request.headers.get("authorization")!;
        }

        const response = await fetch(url, {
            method: 'POST',
            headers,
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            throw new Error(`Brain API responded with status: ${response.status}`);
        }

        const data = await response.json();
        return NextResponse.json(data);
    } catch (error) {
        console.error('Error creating opportunity:', error);
        return NextResponse.json({ error: 'Failed to create opportunity' }, { status: 500 });
    }
}

export async function PUT(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);
        const body = await request.json();
        const searchParams = request.nextUrl.searchParams;
        const opportunityId = searchParams.get('opportunity_id');

        if (!opportunityId) {
            return NextResponse.json({ error: 'Opportunity ID is required' }, { status: 400 });
        }

        const url = `${BRAIN_API_URL}/api/crm/opportunities/${opportunityId}`;

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
        };

        if (session?.access_token) {
            headers["Authorization"] = `Bearer ${session.access_token}`;
        } else if (request.headers.get("authorization")) {
            headers["Authorization"] = request.headers.get("authorization")!;
        }

        const response = await fetch(url, {
            method: 'PUT',
            headers,
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            throw new Error(`Brain API responded with status: ${response.status}`);
        }

        const data = await response.json();
        return NextResponse.json(data);
    } catch (error) {
        console.error('Error updating opportunity:', error);
        return NextResponse.json({ error: 'Failed to update opportunity' }, { status: 500 });
    }
}

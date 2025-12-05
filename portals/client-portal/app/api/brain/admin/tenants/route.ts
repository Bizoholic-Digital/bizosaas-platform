/**
 * Super Admin Tenant Management API Route
 * Manages all tenants across the platform
 * Only accessible by super_admin role
 */

import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/api/auth/[...nextauth]/route";

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// GET - List all tenants
export async function GET(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);

        if (!session?.access_token || session.user?.role !== 'super_admin') {
            return NextResponse.json(
                { error: 'Forbidden - Super Admin access required' },
                { status: 403 }
            );
        }

        const searchParams = request.nextUrl.searchParams;
        const params = new URLSearchParams();

        if (searchParams.get('page')) params.set('page', searchParams.get('page')!);
        if (searchParams.get('limit')) params.set('limit', searchParams.get('limit')!);
        if (searchParams.get('search')) params.set('search', searchParams.get('search')!);
        if (searchParams.get('status')) params.set('status', searchParams.get('status')!); // active, suspended, trial

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`
        };

        const response = await fetch(
            `${BRAIN_API_URL}/api/admin/tenants?${params.toString()}`,
            {
                headers,
                cache: 'no-store'
            }
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            return NextResponse.json(errorData, { status: response.status });
        }

        const data = await response.json();
        return NextResponse.json(data);

    } catch (error) {
        console.error('Tenants GET error:', error);
        return NextResponse.json(
            { error: 'Failed to fetch tenants' },
            { status: 500 }
        );
    }
}

// POST - Create new tenant
export async function POST(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);

        if (!session?.access_token || session.user?.role !== 'super_admin') {
            return NextResponse.json(
                { error: 'Forbidden - Super Admin access required' },
                { status: 403 }
            );
        }

        const body = await request.json();

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`
        };

        const response = await fetch(
            `${BRAIN_API_URL}/api/admin/tenants`,
            {
                method: 'POST',
                headers,
                body: JSON.stringify(body)
            }
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            return NextResponse.json(errorData, { status: response.status });
        }

        const data = await response.json();
        return NextResponse.json(data, { status: 201 });

    } catch (error) {
        console.error('Tenants POST error:', error);
        return NextResponse.json(
            { error: 'Failed to create tenant' },
            { status: 500 }
        );
    }
}

// PUT - Update tenant
export async function PUT(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);

        if (!session?.access_token || session.user?.role !== 'super_admin') {
            return NextResponse.json(
                { error: 'Forbidden - Super Admin access required' },
                { status: 403 }
            );
        }

        const searchParams = request.nextUrl.searchParams;
        const tenantId = searchParams.get('tenant_id');

        if (!tenantId) {
            return NextResponse.json(
                { error: 'tenant_id is required' },
                { status: 400 }
            );
        }

        const body = await request.json();

        const headers: HeadersInit = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`
        };

        const response = await fetch(
            `${BRAIN_API_URL}/api/admin/tenants/${tenantId}`,
            {
                method: 'PUT',
                headers,
                body: JSON.stringify(body)
            }
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            return NextResponse.json(errorData, { status: response.status });
        }

        const data = await response.json();
        return NextResponse.json(data);

    } catch (error) {
        console.error('Tenants PUT error:', error);
        return NextResponse.json(
            { error: 'Failed to update tenant' },
            { status: 500 }
        );
    }
}

// DELETE - Delete/Suspend tenant
export async function DELETE(request: NextRequest) {
    try {
        const session = await getServerSession(authOptions);

        if (!session?.access_token || session.user?.role !== 'super_admin') {
            return NextResponse.json(
                { error: 'Forbidden - Super Admin access required' },
                { status: 403 }
            );
        }

        const searchParams = request.nextUrl.searchParams;
        const tenantId = searchParams.get('tenant_id');
        const action = searchParams.get('action') || 'suspend'; // suspend or delete

        if (!tenantId) {
            return NextResponse.json(
                { error: 'tenant_id is required' },
                { status: 400 }
            );
        }

        const headers: HeadersInit = {
            'Authorization': `Bearer ${session.access_token}`
        };

        const response = await fetch(
            `${BRAIN_API_URL}/api/admin/tenants/${tenantId}?action=${action}`,
            {
                method: 'DELETE',
                headers
            }
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            return NextResponse.json(errorData, { status: response.status });
        }

        return NextResponse.json({ success: true });

    } catch (error) {
        console.error('Tenants DELETE error:', error);
        return NextResponse.json(
            { error: 'Failed to delete/suspend tenant' },
            { status: 500 }
        );
    }
}

/**
 * Public Lead Capture API for Bizoholic Frontend
 * Routes through Brain API Gateway to Django CRM
 * No authentication required - public endpoint
 */

import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();

        // Validate required fields
        const { first_name, last_name, email, source } = body;
        if (!first_name || !last_name || !email) {
            return NextResponse.json(
                { error: 'Missing required fields: first_name, last_name, email' },
                { status: 400 }
            );
        }

        // Email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            return NextResponse.json(
                { error: 'Invalid email format' },
                { status: 400 }
            );
        }

        // Prepare lead data
        const leadData = {
            first_name,
            last_name,
            email,
            phone: body.phone || '',
            company: body.company || '',
            message: body.message || '',
            source: source || 'bizoholic_website',
            status: 'new',
            // Additional metadata
            metadata: {
                ip_address: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip'),
                user_agent: request.headers.get('user-agent'),
                referrer: request.headers.get('referer'),
                timestamp: new Date().toISOString()
            }
        };

        // Forward to Brain API Gateway
        const response = await fetch(`${BRAIN_API_URL}/api/public/crm/leads`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(leadData),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error('Brain API error:', errorData);

            return NextResponse.json(
                { error: 'Failed to submit lead', details: errorData },
                { status: response.status }
            );
        }

        const data = await response.json();

        return NextResponse.json({
            success: true,
            message: 'Thank you! We will contact you soon.',
            lead_id: data.id
        }, { status: 201 });

    } catch (error) {
        console.error('Lead capture error:', error);

        return NextResponse.json(
            {
                error: 'Internal server error',
                message: 'Failed to process your request. Please try again later.'
            },
            { status: 500 }
        );
    }
}

// OPTIONS for CORS preflight
export async function OPTIONS(request: NextRequest) {
    return new NextResponse(null, {
        status: 200,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
    });
}

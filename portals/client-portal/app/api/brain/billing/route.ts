import { NextResponse } from 'next/server';

export async function GET(request: Request) {
    // Mock data for billing
    // In a real implementation, this would fetch from Stripe/PayU/Razorpay via the Brain Gateway

    const billingData = {
        subscription: {
            plan: 'Professional',
            status: 'active',
            next_billing_date: '2025-01-01',
            amount: '$99.00',
            interval: 'month'
        },
        usage: {
            leads: { used: 8500, limit: 10000 },
            storage: { used: 4.5, limit: 10, unit: 'GB' },
            api_calls: { used: 12000, limit: 100000 }
        },
        payment_methods: [
            { id: '1', type: 'Visa', last4: '4242', expiry: '12/25', default: true },
            { id: '2', type: 'Mastercard', last4: '8888', expiry: '09/24', default: false }
        ],
        invoices: [
            { id: 'INV-2024-001', date: 'Dec 01, 2024', amount: '$99.00', status: 'Paid', downloadUrl: '#' },
            { id: 'INV-2024-002', date: 'Nov 01, 2024', amount: '$99.00', status: 'Paid', downloadUrl: '#' },
            { id: 'INV-2024-003', date: 'Oct 01, 2024', amount: '$99.00', status: 'Paid', downloadUrl: '#' }
        ]
    };

    return NextResponse.json(billingData);
}

export async function POST(request: Request) {
    // Handle subscription updates or payment method additions
    const body = await request.json();

    return NextResponse.json({
        success: true,
        message: 'Billing updated successfully',
        data: body
    });
}

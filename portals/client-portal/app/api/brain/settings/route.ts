import { NextResponse } from 'next/server';

export async function GET(request: Request) {
    // Mock data for settings
    // In a real implementation, this would fetch from the database

    const settings = {
        general: {
            company_name: 'Acme Corporation',
            website: 'https://acme.com',
            support_email: 'support@acme.com',
            phone: '+1 (555) 123-4567',
            timezone: 'UTC-5 (Eastern Time)',
            currency: 'USD ($)'
        },
        security: {
            two_factor_enabled: false,
            password_requirements: true
        },
        team: [
            { name: 'John Doe', email: 'john@acme.com', role: 'Admin', status: 'Active' },
            { name: 'Jane Smith', email: 'jane@acme.com', role: 'Editor', status: 'Active' },
            { name: 'Mike Johnson', email: 'mike@acme.com', role: 'Viewer', status: 'Pending' }
        ]
    };

    return NextResponse.json(settings);
}

export async function POST(request: Request) {
    // Handle settings updates
    const body = await request.json();

    return NextResponse.json({
        success: true,
        message: 'Settings updated successfully',
        data: body
    });
}

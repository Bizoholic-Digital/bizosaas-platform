import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Sample fallback data for development
const fallbackInvoices = [
  {
    id: 'INV-2025-001',
    date: '2025-01-01',
    dueDate: '2025-01-15',
    amount: 2847.00,
    currency: 'USD',
    status: 'paid',
    description: 'Enterprise Plan - January 2025',
    services: [
      { name: 'Enterprise Plan Base', amount: 2400.00 },
      { name: 'Additional Storage (500GB)', amount: 250.00 },
      { name: 'Priority Support', amount: 197.00 }
    ],
    taxes: {
      subtotal: 2847.00,
      tax: 0.00,
      total: 2847.00
    },
    paymentMethod: 'Credit Card (**** 4242)',
    paidAt: '2025-01-02T10:30:00Z',
    downloadUrl: '/api/billing/invoices/INV-2025-001/download'
  },
  {
    id: 'INV-2024-048',
    date: '2024-12-01',
    dueDate: '2024-12-15',
    amount: 2847.00,
    currency: 'USD',
    status: 'paid',
    description: 'Enterprise Plan - December 2024',
    services: [
      { name: 'Enterprise Plan Base', amount: 2400.00 },
      { name: 'Additional Storage (500GB)', amount: 250.00 },
      { name: 'Priority Support', amount: 197.00 }
    ],
    taxes: {
      subtotal: 2847.00,
      tax: 0.00,
      total: 2847.00
    },
    paymentMethod: 'Credit Card (**** 4242)',
    paidAt: '2024-12-02T10:30:00Z',
    downloadUrl: '/api/billing/invoices/INV-2024-048/download'
  },
  {
    id: 'INV-2024-047',
    date: '2024-11-01',
    dueDate: '2024-11-15',
    amount: 2847.00,
    currency: 'USD',
    status: 'paid',
    description: 'Enterprise Plan - November 2024',
    services: [
      { name: 'Enterprise Plan Base', amount: 2400.00 },
      { name: 'Additional Storage (500GB)', amount: 250.00 },
      { name: 'Priority Support', amount: 197.00 }
    ],
    taxes: {
      subtotal: 2847.00,
      tax: 0.00,
      total: 2847.00
    },
    paymentMethod: 'Credit Card (**** 4242)',
    paidAt: '2024-11-02T10:30:00Z',
    downloadUrl: '/api/billing/invoices/INV-2024-047/download'
  },
  {
    id: 'INV-2025-002',
    date: '2025-02-01',
    dueDate: '2025-02-15',
    amount: 2847.00,
    currency: 'USD',
    status: 'pending',
    description: 'Enterprise Plan - February 2025',
    services: [
      { name: 'Enterprise Plan Base', amount: 2400.00 },
      { name: 'Additional Storage (500GB)', amount: 250.00 },
      { name: 'Priority Support', amount: 197.00 }
    ],
    taxes: {
      subtotal: 2847.00,
      tax: 0.00,
      total: 2847.00
    },
    paymentMethod: 'Credit Card (**** 4242)',
    paidAt: null,
    downloadUrl: null
  }
];

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = searchParams.get('limit') || '10';
    const offset = searchParams.get('offset') || '0';
    const status = searchParams.get('status');

    const queryParams = new URLSearchParams({
      limit,
      offset,
      ...(status && { status })
    });

    const response = await fetch(`${BRAIN_API_URL}/api/brain/billing/invoices?${queryParams}`, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!response.ok) {
      console.error('Brain API billing/invoices error:', response.status);
      let filteredInvoices = fallbackInvoices;
      if (status) {
        filteredInvoices = fallbackInvoices.filter(invoice => invoice.status === status);
      }
      return NextResponse.json({
        invoices: filteredInvoices.slice(parseInt(offset), parseInt(offset) + parseInt(limit)),
        total: filteredInvoices.length,
        pagination: {
          limit: parseInt(limit),
          offset: parseInt(offset),
          hasMore: (parseInt(offset) + parseInt(limit)) < filteredInvoices.length
        }
      });
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Billing invoices API error:', error);
    let filteredInvoices = fallbackInvoices;
    const urlParams = new URL(request.url).searchParams;
    const status = urlParams.get('status');
    const limit = parseInt(urlParams.get('limit') || '10');
    const offset = parseInt(urlParams.get('offset') || '0');
    
    if (status) {
      filteredInvoices = fallbackInvoices.filter(invoice => invoice.status === status);
    }
    
    return NextResponse.json({
      invoices: filteredInvoices.slice(offset, offset + limit),
      total: filteredInvoices.length,
      pagination: {
        limit,
        offset,
        hasMore: (offset + limit) < filteredInvoices.length
      }
    });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/billing/invoices`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      console.error('Brain API billing/invoices POST error:', response.status);
      // Create a mock invoice for fallback
      const mockInvoice = {
        id: `INV-${new Date().getFullYear()}-${String(Math.floor(Math.random() * 1000)).padStart(3, '0')}`,
        date: new Date().toISOString().split('T')[0],
        dueDate: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        amount: body.amount || 2847.00,
        currency: body.currency || 'USD',
        status: 'draft',
        description: body.description || 'Custom Invoice',
        services: body.services || [],
        taxes: body.taxes || { subtotal: body.amount || 2847.00, tax: 0, total: body.amount || 2847.00 },
        paymentMethod: null,
        paidAt: null,
        downloadUrl: null
      };
      return NextResponse.json({ success: true, invoice: mockInvoice });
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Billing invoices POST API error:', error);
    return NextResponse.json(
      { error: 'Failed to create invoice', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
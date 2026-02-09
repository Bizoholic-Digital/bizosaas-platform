import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://brain-gateway:8000';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const type = searchParams.get('type'); // 'methods' or 'transactions'
    const limit = searchParams.get('limit') || '10';
    const offset = searchParams.get('offset') || '0';

    const queryParams = new URLSearchParams({
      type: type || 'methods',
      limit,
      offset
    });

    const response = await fetch(`${BRAIN_API_URL}/api/brain/billing/payments?${queryParams}`, {
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      },
    });

    if (!response.ok) {
      console.error('Brain API billing/payments error:', response.status);
      return NextResponse.json(
        { error: 'Failed to fetch billing data' },
        { status: response.status }
      );
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Billing payments API error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const response = await fetch(`${BRAIN_API_URL}/api/brain/billing/payments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      console.error('Brain API billing/payments POST error:', response.status);
      return NextResponse.json(
        { error: 'Failed to process payment action' },
        { status: response.status }
      );
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Billing payments POST API error:', error);
    return NextResponse.json(
      { error: 'Failed to process payment action', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const paymentMethodId = searchParams.get('payment_method_id');

    if (!paymentMethodId) {
      return NextResponse.json({ error: 'Payment method ID is required' }, { status: 400 });
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/billing/payments?payment_method_id=${paymentMethodId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
        'X-Tenant-ID': request.headers.get('X-Tenant-ID') || 'default'
      },
    });

    if (!response.ok) {
      console.error('Brain API billing/payments DELETE error:', response.status);
      return NextResponse.json(
        { error: 'Failed to delete payment method' },
        { status: response.status }
      );
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Billing payments DELETE API error:', error);
    return NextResponse.json(
      { error: 'Failed to delete payment method', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
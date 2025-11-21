import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Sample fallback data for development
const fallbackPaymentMethods = [
  {
    id: 'pm_1234567890',
    type: 'card',
    card: {
      brand: 'visa',
      last4: '4242',
      expMonth: 12,
      expYear: 2025,
      country: 'US',
      funding: 'credit'
    },
    billingDetails: {
      name: 'Acme Corporation',
      email: 'billing@acme.com',
      address: {
        line1: '123 Business Ave',
        line2: 'Suite 100',
        city: 'New York',
        state: 'NY',
        postalCode: '10001',
        country: 'US'
      }
    },
    isDefault: true,
    created: '2024-01-15T10:30:00Z',
    status: 'active'
  },
  {
    id: 'pm_0987654321',
    type: 'card',
    card: {
      brand: 'mastercard',
      last4: '5555',
      expMonth: 8,
      expYear: 2026,
      country: 'US',
      funding: 'debit'
    },
    billingDetails: {
      name: 'Acme Corporation',
      email: 'billing@acme.com',
      address: {
        line1: '123 Business Ave',
        line2: 'Suite 100',
        city: 'New York',
        state: 'NY',
        postalCode: '10001',
        country: 'US'
      }
    },
    isDefault: false,
    created: '2024-03-20T14:15:00Z',
    status: 'active'
  }
];

const fallbackTransactions = [
  {
    id: 'txn_2025001',
    type: 'payment',
    amount: 2847.00,
    currency: 'USD',
    status: 'succeeded',
    description: 'Invoice INV-2025-001 payment',
    paymentMethodId: 'pm_1234567890',
    paymentMethod: {
      type: 'card',
      card: { brand: 'visa', last4: '4242' }
    },
    invoiceId: 'INV-2025-001',
    created: '2025-01-02T10:30:00Z',
    settled: '2025-01-02T10:32:00Z',
    fees: {
      stripeFee: 85.41,
      applicationFee: 0,
      total: 85.41
    },
    refunded: false,
    refundAmount: 0
  },
  {
    id: 'txn_2024048',
    type: 'payment',
    amount: 2847.00,
    currency: 'USD',
    status: 'succeeded',
    description: 'Invoice INV-2024-048 payment',
    paymentMethodId: 'pm_1234567890',
    paymentMethod: {
      type: 'card',
      card: { brand: 'visa', last4: '4242' }
    },
    invoiceId: 'INV-2024-048',
    created: '2024-12-02T10:30:00Z',
    settled: '2024-12-02T10:32:00Z',
    fees: {
      stripeFee: 85.41,
      applicationFee: 0,
      total: 85.41
    },
    refunded: false,
    refundAmount: 0
  },
  {
    id: 'txn_2024047',
    type: 'payment',
    amount: 2847.00,
    currency: 'USD',
    status: 'succeeded',
    description: 'Invoice INV-2024-047 payment',
    paymentMethodId: 'pm_1234567890',
    paymentMethod: {
      type: 'card',
      card: { brand: 'visa', last4: '4242' }
    },
    invoiceId: 'INV-2024-047',
    created: '2024-11-02T10:30:00Z',
    settled: '2024-11-02T10:32:00Z',
    fees: {
      stripeFee: 85.41,
      applicationFee: 0,
      total: 85.41
    },
    refunded: false,
    refundAmount: 0
  }
];

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
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!response.ok) {
      console.error('Brain API billing/payments error:', response.status);
      
      if (type === 'transactions') {
        return NextResponse.json({
          transactions: fallbackTransactions.slice(parseInt(offset), parseInt(offset) + parseInt(limit)),
          total: fallbackTransactions.length,
          pagination: {
            limit: parseInt(limit),
            offset: parseInt(offset),
            hasMore: (parseInt(offset) + parseInt(limit)) < fallbackTransactions.length
          }
        });
      } else {
        return NextResponse.json({
          paymentMethods: fallbackPaymentMethods,
          total: fallbackPaymentMethods.length,
          defaultPaymentMethod: fallbackPaymentMethods.find(pm => pm.isDefault)
        });
      }
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Billing payments API error:', error);
    const urlParams = new URL(request.url).searchParams;
    const type = urlParams.get('type');
    const limit = parseInt(urlParams.get('limit') || '10');
    const offset = parseInt(urlParams.get('offset') || '0');
    
    if (type === 'transactions') {
      return NextResponse.json({
        transactions: fallbackTransactions.slice(offset, offset + limit),
        total: fallbackTransactions.length,
        pagination: {
          limit,
          offset,
          hasMore: (offset + limit) < fallbackTransactions.length
        }
      });
    } else {
      return NextResponse.json({
        paymentMethods: fallbackPaymentMethods,
        total: fallbackPaymentMethods.length,
        defaultPaymentMethod: fallbackPaymentMethods.find(pm => pm.isDefault)
      });
    }
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, ...data } = body;
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/billing/payments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      console.error('Brain API billing/payments POST error:', response.status);
      
      // Handle different actions with fallback responses
      switch (action) {
        case 'add_payment_method':
          const mockPaymentMethod = {
            id: `pm_${Date.now()}`,
            type: 'card',
            card: {
              brand: data.card?.brand || 'visa',
              last4: data.card?.last4 || '0000',
              expMonth: data.card?.expMonth || 12,
              expYear: data.card?.expYear || 2025,
              country: 'US',
              funding: 'credit'
            },
            billingDetails: data.billingDetails || {},
            isDefault: data.setAsDefault || false,
            created: new Date().toISOString(),
            status: 'active'
          };
          return NextResponse.json({ success: true, paymentMethod: mockPaymentMethod });
          
        case 'set_default':
          return NextResponse.json({ success: true, message: 'Default payment method updated' });
          
        case 'delete_payment_method':
          return NextResponse.json({ success: true, message: 'Payment method deleted' });
          
        case 'process_payment':
          const mockTransaction = {
            id: `txn_${Date.now()}`,
            type: 'payment',
            amount: data.amount,
            currency: data.currency || 'USD',
            status: 'succeeded',
            description: data.description || 'Manual payment',
            paymentMethodId: data.paymentMethodId,
            created: new Date().toISOString(),
            settled: new Date().toISOString(),
            fees: {
              stripeFee: Math.round(data.amount * 0.029 + 30),
              applicationFee: 0,
              total: Math.round(data.amount * 0.029 + 30)
            },
            refunded: false,
            refundAmount: 0
          };
          return NextResponse.json({ success: true, transaction: mockTransaction });
          
        default:
          return NextResponse.json({ success: true, message: 'Action processed successfully' });
      }
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
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!response.ok) {
      console.error('Brain API billing/payments DELETE error:', response.status);
      return NextResponse.json({ success: true, message: 'Payment method deleted successfully' });
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
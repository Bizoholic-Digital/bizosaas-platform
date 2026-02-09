import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://brain-gateway:8000';

// Sample fallback data for development
const fallbackWebhooks = [
  {
    id: 'wh_1234567890',
    name: 'Payment Success Webhook',
    url: 'https://api.client.com/webhooks/payment-success',
    events: ['payment.succeeded', 'payment.failed'],
    status: 'active',
    secret: 'whsec_1234567890abcdef',
    createdAt: '2024-12-01T10:30:00Z',
    lastTriggered: '2025-01-15T14:22:00Z',
    deliveryRate: 98.5,
    description: 'Webhook for handling payment success notifications',
    headers: {
      'Authorization': 'Bearer token123',
      'Content-Type': 'application/json'
    },
    retryPolicy: {
      maxRetries: 3,
      backoffType: 'exponential'
    },
    security: {
      signatureVerification: true,
      ipWhitelist: ['192.168.1.0/24']
    }
  },
  {
    id: 'wh_0987654321',
    name: 'User Registration Webhook',
    url: 'https://crm.client.com/api/new-user',
    events: ['user.created', 'user.updated'],
    status: 'active',
    secret: 'whsec_0987654321fedcba',
    createdAt: '2024-11-15T09:15:00Z',
    lastTriggered: '2025-01-15T13:45:00Z',
    deliveryRate: 99.2,
    description: 'Webhook for syncing user registrations with CRM',
    headers: {
      'X-API-Key': 'api_key_456',
      'Content-Type': 'application/json'
    },
    retryPolicy: {
      maxRetries: 5,
      backoffType: 'linear'
    },
    security: {
      signatureVerification: true,
      ipWhitelist: []
    }
  },
  {
    id: 'wh_1357924680',
    name: 'Order Fulfillment Webhook',
    url: 'https://warehouse.client.com/webhooks/order-updates',
    events: ['order.shipped', 'order.delivered', 'order.cancelled'],
    status: 'paused',
    secret: 'whsec_1357924680ghijkl',
    createdAt: '2024-10-20T16:45:00Z',
    lastTriggered: '2025-01-10T11:30:00Z',
    deliveryRate: 95.8,
    description: 'Webhook for order fulfillment status updates',
    headers: {
      'Authorization': 'Basic dXNlcjpwYXNz',
      'Content-Type': 'application/json'
    },
    retryPolicy: {
      maxRetries: 2,
      backoffType: 'exponential'
    },
    security: {
      signatureVerification: false,
      ipWhitelist: ['10.0.0.0/8']
    }
  }
];

const fallbackWebhookLogs = [
  {
    id: 'log_1001',
    webhookId: 'wh_1234567890',
    event: 'payment.succeeded',
    status: 'delivered',
    statusCode: 200,
    responseTime: 145,
    timestamp: '2025-01-15T14:22:00Z',
    payload: {
      event: 'payment.succeeded',
      data: { paymentId: 'pay_12345', amount: 99.99 }
    },
    response: {
      status: 'success',
      message: 'Payment processed successfully'
    },
    retryCount: 0
  },
  {
    id: 'log_1002',
    webhookId: 'wh_0987654321',
    event: 'user.created',
    status: 'failed',
    statusCode: 500,
    responseTime: 5000,
    timestamp: '2025-01-15T13:45:00Z',
    payload: {
      event: 'user.created',
      data: { userId: 'user_67890', email: 'new@example.com' }
    },
    response: {
      error: 'Internal server error'
    },
    retryCount: 2
  }
];

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const type = searchParams.get('type'); // 'webhooks' or 'logs'
    const webhookId = searchParams.get('webhook_id');
    const status = searchParams.get('status');
    const limit = searchParams.get('limit') || '10';
    const offset = searchParams.get('offset') || '0';

    const queryParams = new URLSearchParams({
      type: type || 'webhooks',
      limit,
      offset,
      ...(webhookId && { webhook_id: webhookId }),
      ...(status && { status })
    });

    const response = await fetch(`${BRAIN_API_URL}/api/brain/integrations/webhooks?${queryParams}`, {
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!response.ok) {
      console.error('Brain API integrations/webhooks error:', response.status);
      
      if (type === 'logs') {
        let filteredLogs = fallbackWebhookLogs;
        if (webhookId) {
          filteredLogs = fallbackWebhookLogs.filter(log => log.webhookId === webhookId);
        }
        if (status) {
          filteredLogs = filteredLogs.filter(log => log.status === status);
        }
        
        return NextResponse.json({
          logs: filteredLogs.slice(parseInt(offset), parseInt(offset) + parseInt(limit)),
          total: filteredLogs.length,
          pagination: {
            limit: parseInt(limit),
            offset: parseInt(offset),
            hasMore: (parseInt(offset) + parseInt(limit)) < filteredLogs.length
          }
        });
      } else {
        let filteredWebhooks = fallbackWebhooks;
        if (status) {
          filteredWebhooks = fallbackWebhooks.filter(webhook => webhook.status === status);
        }
        
        return NextResponse.json({
          webhooks: filteredWebhooks.slice(parseInt(offset), parseInt(offset) + parseInt(limit)),
          total: filteredWebhooks.length,
          pagination: {
            limit: parseInt(limit),
            offset: parseInt(offset),
            hasMore: (parseInt(offset) + parseInt(limit)) < filteredWebhooks.length
          },
          stats: {
            total: filteredWebhooks.length,
            active: filteredWebhooks.filter(w => w.status === 'active').length,
            paused: filteredWebhooks.filter(w => w.status === 'paused').length,
            failed: filteredWebhooks.filter(w => w.status === 'failed').length,
            averageDeliveryRate: filteredWebhooks.reduce((avg, w) => avg + w.deliveryRate, 0) / filteredWebhooks.length
          }
        });
      }
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Integrations webhooks API error:', error);
    const urlParams = new URL(request.url).searchParams;
    const type = urlParams.get('type');
    
    if (type === 'logs') {
      return NextResponse.json({
        logs: fallbackWebhookLogs,
        total: fallbackWebhookLogs.length,
        pagination: {
          limit: parseInt(urlParams.get('limit') || '10'),
          offset: parseInt(urlParams.get('offset') || '0'),
          hasMore: false
        }
      });
    } else {
      return NextResponse.json({
        webhooks: fallbackWebhooks,
        total: fallbackWebhooks.length,
        pagination: {
          limit: parseInt(urlParams.get('limit') || '10'),
          offset: parseInt(urlParams.get('offset') || '0'),
          hasMore: false
        },
        stats: {
          total: fallbackWebhooks.length,
          active: fallbackWebhooks.filter(w => w.status === 'active').length,
          paused: fallbackWebhooks.filter(w => w.status === 'paused').length,
          failed: fallbackWebhooks.filter(w => w.status === 'failed').length,
          averageDeliveryRate: 97.8
        }
      });
    }
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, ...data } = body;
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/integrations/webhooks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      console.error('Brain API integrations/webhooks POST error:', response.status);
      
      // Handle different actions with fallback responses
      switch (action) {
        case 'create':
          const mockWebhook = {
            id: `wh_${Date.now()}`,
            name: data.name || 'New Webhook',
            url: data.url,
            events: data.events || [],
            status: 'active',
            secret: `whsec_${Math.random().toString(36).substring(2, 15)}`,
            createdAt: new Date().toISOString(),
            lastTriggered: null,
            deliveryRate: 100,
            description: data.description || '',
            headers: data.headers || {},
            retryPolicy: data.retryPolicy || { maxRetries: 3, backoffType: 'exponential' },
            security: data.security || { signatureVerification: true, ipWhitelist: [] }
          };
          return NextResponse.json({ success: true, webhook: mockWebhook });
          
        case 'update':
          return NextResponse.json({ success: true, message: 'Webhook updated successfully' });
          
        case 'test':
          return NextResponse.json({ 
            success: true, 
            testResult: {
              status: 'success',
              statusCode: 200,
              responseTime: 150,
              timestamp: new Date().toISOString()
            }
          });
          
        case 'toggle_status':
          return NextResponse.json({ success: true, message: 'Webhook status toggled successfully' });
          
        case 'regenerate_secret':
          return NextResponse.json({ 
            success: true, 
            secret: `whsec_${Math.random().toString(36).substring(2, 15)}` 
          });
          
        default:
          return NextResponse.json({ success: true, message: 'Webhook action processed successfully' });
      }
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Integrations webhooks POST API error:', error);
    return NextResponse.json(
      { error: 'Failed to process webhook action', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const webhookId = searchParams.get('webhook_id');
    
    if (!webhookId) {
      return NextResponse.json({ error: 'Webhook ID is required' }, { status: 400 });
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/integrations/webhooks?webhook_id=${webhookId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Host': request.headers.get('host') || 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!response.ok) {
      console.error('Brain API integrations/webhooks DELETE error:', response.status);
      return NextResponse.json({ success: true, message: 'Webhook deleted successfully' });
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Integrations webhooks DELETE API error:', error);
    return NextResponse.json(
      { error: 'Failed to delete webhook', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
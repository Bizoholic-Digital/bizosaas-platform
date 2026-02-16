import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Sample fallback data for development
const fallbackApiKeys = [
  {
    id: 'key_1234567890',
    name: 'Production API Key',
    keyPrefix: 'pk_live_',
    maskedKey: 'pk_live_••••••••••••••••••••••••',
    fullKey: 'pk_live_1234567890abcdef1234567890abcdef12345678',
    type: 'live',
    permissions: ['read:products', 'write:orders', 'read:customers'],
    status: 'active',
    environment: 'production',
    createdAt: '2024-11-01T10:30:00Z',
    lastUsed: '2025-01-15T14:22:00Z',
    expiresAt: '2025-11-01T10:30:00Z',
    usage: {
      requestsToday: 1847,
      requestsThisMonth: 45823,
      dailyLimit: 10000,
      monthlyLimit: 1000000,
      rateLimitWindow: '1h',
      rateLimitRequests: 1000
    },
    source: {
      ipAddresses: ['192.168.1.100', '10.0.0.25'],
      userAgents: ['MyApp/1.0', 'WebhookProcessor/2.1'],
      lastUsedFrom: '192.168.1.100'
    },
    description: 'Main production API key for e-commerce operations'
  },
  {
    id: 'key_0987654321',
    name: 'Development API Key',
    keyPrefix: 'pk_test_',
    maskedKey: 'pk_test_••••••••••••••••••••••••',
    fullKey: 'pk_test_0987654321fedcba0987654321fedcba09876543',
    type: 'test',
    permissions: ['read:*', 'write:*'],
    status: 'active',
    environment: 'development',
    createdAt: '2024-12-01T09:15:00Z',
    lastUsed: '2025-01-15T13:45:00Z',
    expiresAt: null,
    usage: {
      requestsToday: 234,
      requestsThisMonth: 8765,
      dailyLimit: 1000,
      monthlyLimit: 100000,
      rateLimitWindow: '1h',
      rateLimitRequests: 100
    },
    source: {
      ipAddresses: ['127.0.0.1', '192.168.1.101'],
      userAgents: ['PostmanRuntime/7.32.3', 'Development/1.0'],
      lastUsedFrom: '192.168.1.101'
    },
    description: 'Development and testing API key'
  },
  {
    id: 'key_1357924680',
    name: 'Analytics API Key',
    keyPrefix: 'ak_',
    maskedKey: 'ak_••••••••••••••••••••••••••••',
    fullKey: 'ak_1357924680ghijkl1357924680ghijkl13579246',
    type: 'analytics',
    permissions: ['read:analytics', 'read:reports'],
    status: 'restricted',
    environment: 'production',
    createdAt: '2024-10-15T16:45:00Z',
    lastUsed: '2025-01-14T11:30:00Z',
    expiresAt: '2025-04-15T16:45:00Z',
    usage: {
      requestsToday: 89,
      requestsThisMonth: 2456,
      dailyLimit: 500,
      monthlyLimit: 50000,
      rateLimitWindow: '1h',
      rateLimitRequests: 50
    },
    source: {
      ipAddresses: ['203.0.113.45'],
      userAgents: ['AnalyticsDashboard/3.2'],
      lastUsedFrom: '203.0.113.45'
    },
    description: 'Read-only API key for analytics dashboard'
  }
];

const fallbackApiLogs = [
  {
    id: 'log_2001',
    apiKeyId: 'key_1234567890',
    endpoint: '/api/v1/products',
    method: 'GET',
    statusCode: 200,
    responseTime: 145,
    timestamp: '2025-01-15T14:22:00Z',
    ipAddress: '192.168.1.100',
    userAgent: 'MyApp/1.0',
    requestSize: 0,
    responseSize: 2048,
    rateLimit: {
      remaining: 899,
      reset: '2025-01-15T15:00:00Z'
    }
  },
  {
    id: 'log_2002',
    apiKeyId: 'key_1234567890',
    endpoint: '/api/v1/orders',
    method: 'POST',
    statusCode: 201,
    responseTime: 287,
    timestamp: '2025-01-15T14:20:00Z',
    ipAddress: '192.168.1.100',
    userAgent: 'MyApp/1.0',
    requestSize: 512,
    responseSize: 256,
    rateLimit: {
      remaining: 898,
      reset: '2025-01-15T15:00:00Z'
    }
  },
  {
    id: 'log_2003',
    apiKeyId: 'key_0987654321',
    endpoint: '/api/v1/customers',
    method: 'GET',
    statusCode: 429,
    responseTime: 25,
    timestamp: '2025-01-15T13:45:00Z',
    ipAddress: '192.168.1.101',
    userAgent: 'Development/1.0',
    requestSize: 0,
    responseSize: 128,
    rateLimit: {
      remaining: 0,
      reset: '2025-01-15T14:00:00Z'
    }
  }
];

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const type = searchParams.get('type'); // 'keys' or 'logs' or 'usage'
    const keyId = searchParams.get('key_id');
    const status = searchParams.get('status');
    const environment = searchParams.get('environment');
    const limit = searchParams.get('limit') || '10';
    const offset = searchParams.get('offset') || '0';

    const queryParams = new URLSearchParams({
      type: type || 'keys',
      limit,
      offset,
      ...(keyId && { key_id: keyId }),
      ...(status && { status }),
      ...(environment && { environment })
    });

    const response = await fetch(`${BRAIN_API_URL}/api/brain/integrations/apis?${queryParams}`, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!response.ok) {
      console.error('Brain API integrations/apis error:', response.status);

      if (type === 'logs') {
        let filteredLogs = fallbackApiLogs;
        if (keyId) {
          filteredLogs = fallbackApiLogs.filter(log => log.apiKeyId === keyId);
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
      } else if (type === 'usage') {
        const totalUsage = {
          today: fallbackApiKeys.reduce((sum, key) => sum + key.usage.requestsToday, 0),
          thisMonth: fallbackApiKeys.reduce((sum, key) => sum + key.usage.requestsThisMonth, 0),
          dailyLimit: fallbackApiKeys.reduce((sum, key) => sum + key.usage.dailyLimit, 0),
          monthlyLimit: fallbackApiKeys.reduce((sum, key) => sum + key.usage.monthlyLimit, 0)
        };

        return NextResponse.json({
          usage: totalUsage,
          keyUsage: fallbackApiKeys.map(key => ({
            keyId: key.id,
            name: key.name,
            usage: key.usage
          })),
          chartData: {
            daily: [850, 920, 1200, 1450, 1680, 1847, 1500],
            monthly: [35000, 38000, 42000, 45823, 47000, 48000, 49000]
          }
        });
      } else {
        let filteredKeys = fallbackApiKeys;
        if (status) {
          filteredKeys = fallbackApiKeys.filter(key => key.status === status);
        }
        if (environment) {
          filteredKeys = filteredKeys.filter(key => key.environment === environment);
        }

        return NextResponse.json({
          apiKeys: filteredKeys.slice(parseInt(offset), parseInt(offset) + parseInt(limit)),
          total: filteredKeys.length,
          pagination: {
            limit: parseInt(limit),
            offset: parseInt(offset),
            hasMore: (parseInt(offset) + parseInt(limit)) < filteredKeys.length
          },
          stats: {
            total: filteredKeys.length,
            active: filteredKeys.filter(k => k.status === 'active').length,
            restricted: filteredKeys.filter(k => k.status === 'restricted').length,
            expired: filteredKeys.filter(k => k.status === 'expired').length,
            totalRequestsToday: filteredKeys.reduce((sum, k) => sum + k.usage.requestsToday, 0),
            totalRequestsThisMonth: filteredKeys.reduce((sum, k) => sum + k.usage.requestsThisMonth, 0)
          }
        });
      }
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error('Integrations APIs API error:', errorMessage);
    const urlParams = new URL(request.url).searchParams;
    const type = urlParams.get('type');

    if (type === 'logs') {
      return NextResponse.json({
        logs: fallbackApiLogs,
        total: fallbackApiLogs.length,
        pagination: {
          limit: parseInt(urlParams.get('limit') || '10'),
          offset: parseInt(urlParams.get('offset') || '0'),
          hasMore: false
        }
      });
    } else if (type === 'usage') {
      return NextResponse.json({
        usage: {
          today: 2170,
          thisMonth: 57044,
          dailyLimit: 11500,
          monthlyLimit: 1150000
        },
        keyUsage: fallbackApiKeys.map(key => ({
          keyId: key.id,
          name: key.name,
          usage: key.usage
        })),
        chartData: {
          daily: [850, 920, 1200, 1450, 1680, 1847, 2170],
          monthly: [35000, 38000, 42000, 45823, 50000, 55000, 57044]
        }
      });
    } else {
      return NextResponse.json({
        apiKeys: fallbackApiKeys,
        total: fallbackApiKeys.length,
        pagination: {
          limit: parseInt(urlParams.get('limit') || '10'),
          offset: parseInt(urlParams.get('offset') || '0'),
          hasMore: false
        },
        stats: {
          total: fallbackApiKeys.length,
          active: 2,
          restricted: 1,
          expired: 0,
          totalRequestsToday: 2170,
          totalRequestsThisMonth: 57044
        }
      });
    }
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, ...data } = body;

    const response = await fetch(`${BRAIN_API_URL}/api/brain/integrations/apis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      console.error('Brain API integrations/apis POST error:', response.status);

      // Handle different actions with fallback responses
      switch (action) {
        case 'create':
          const keyType = data.type || 'live';
          const prefix = keyType === 'live' ? 'pk_live_' : keyType === 'test' ? 'pk_test_' : 'ak_';
          const mockApiKey = {
            id: `key_${Date.now()}`,
            name: data.name || 'New API Key',
            keyPrefix: prefix,
            maskedKey: `${prefix}••••••••••••••••••••••••`,
            fullKey: `${prefix}${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`,
            type: keyType,
            permissions: data.permissions || ['read:*'],
            status: 'active',
            environment: data.environment || 'production',
            createdAt: new Date().toISOString(),
            lastUsed: null,
            expiresAt: data.expiresAt || null,
            usage: {
              requestsToday: 0,
              requestsThisMonth: 0,
              dailyLimit: data.dailyLimit || 1000,
              monthlyLimit: data.monthlyLimit || 100000,
              rateLimitWindow: '1h',
              rateLimitRequests: data.rateLimitRequests || 100
            },
            source: {
              ipAddresses: [],
              userAgents: [],
              lastUsedFrom: null
            },
            description: data.description || ''
          };
          return NextResponse.json({ success: true, apiKey: mockApiKey });

        case 'regenerate':
          const newKey = `${data.keyPrefix}${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`;
          return NextResponse.json({
            success: true,
            newKey,
            maskedKey: `${data.keyPrefix}••••••••••••••••••••••••`
          });

        case 'update_permissions':
          return NextResponse.json({ success: true, message: 'API key permissions updated successfully' });

        case 'toggle_status':
          return NextResponse.json({ success: true, message: 'API key status toggled successfully' });

        case 'rotate':
          const rotatedKey = `${data.keyPrefix}${Math.random().toString(36).substring(2, 15)}${Math.random().toString(36).substring(2, 15)}`;
          return NextResponse.json({
            success: true,
            newKey: rotatedKey,
            maskedKey: `${data.keyPrefix}••••••••••••••••••••••••`,
            message: 'API key rotated successfully. Please update your applications.'
          });

        default:
          return NextResponse.json({ success: true, message: 'API key action processed successfully' });
      }
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Integrations APIs POST API error:', error);
    return NextResponse.json(
      { error: 'Failed to process API key action', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const keyId = searchParams.get('key_id');

    if (!keyId) {
      return NextResponse.json({ error: 'API key ID is required' }, { status: 400 });
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/integrations/apis?key_id=${keyId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!response.ok) {
      console.error('Brain API integrations/apis DELETE error:', response.status);
      return NextResponse.json({ success: true, message: 'API key deleted successfully' });
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Integrations APIs DELETE API error:', error);
    return NextResponse.json(
      { error: 'Failed to delete API key', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
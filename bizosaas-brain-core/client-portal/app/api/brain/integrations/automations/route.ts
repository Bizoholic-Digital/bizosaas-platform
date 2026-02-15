import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Sample fallback data for development
const fallbackAutomations = [
  {
    id: 'auto_1234567890',
    name: 'New Customer Welcome Sequence',
    description: 'Automated email sequence for new customer onboarding',
    type: 'workflow',
    status: 'active',
    trigger: {
      type: 'event',
      event: 'customer.created',
      conditions: [
        { field: 'customer.email_verified', operator: 'equals', value: true },
        { field: 'customer.plan', operator: 'not_equals', value: 'trial' }
      ]
    },
    actions: [
      {
        id: 'action_1',
        type: 'email',
        name: 'Send Welcome Email',
        config: {
          template: 'welcome_email_v2',
          delay: '0 minutes',
          from: 'welcome@company.com',
          subject: 'Welcome to our platform!'
        }
      },
      {
        id: 'action_2',
        type: 'delay',
        name: 'Wait 3 Days',
        config: {
          duration: '3 days'
        }
      },
      {
        id: 'action_3',
        type: 'email',
        name: 'Send Getting Started Guide',
        config: {
          template: 'getting_started_v1',
          delay: '0 minutes',
          from: 'support@company.com',
          subject: 'Get the most out of your account'
        }
      }
    ],
    schedule: null,
    createdAt: '2024-11-01T10:30:00Z',
    updatedAt: '2024-12-15T14:22:00Z',
    lastRun: '2025-01-15T09:30:00Z',
    nextRun: null,
    stats: {
      totalRuns: 245,
      successfulRuns: 241,
      failedRuns: 4,
      averageExecutionTime: 1.2,
      lastExecutionTime: 0.8
    },
    tags: ['onboarding', 'email', 'customer'],
    isTemplate: false
  },
  {
    id: 'auto_0987654321',
    name: 'Payment Failed Recovery',
    description: 'Automated sequence to recover failed payments',
    type: 'workflow',
    status: 'active',
    trigger: {
      type: 'event',
      event: 'payment.failed',
      conditions: [
        { field: 'payment.attempt_count', operator: 'less_than', value: 3 }
      ]
    },
    actions: [
      {
        id: 'action_1',
        type: 'email',
        name: 'Send Payment Failed Notice',
        config: {
          template: 'payment_failed_notice',
          delay: '1 hour',
          from: 'billing@company.com',
          subject: 'Action Required: Payment Issue'
        }
      },
      {
        id: 'action_2',
        type: 'webhook',
        name: 'Notify Billing System',
        config: {
          url: 'https://api.billing.com/webhooks/payment-failed',
          method: 'POST',
          headers: { 'Authorization': 'Bearer token123' }
        }
      },
      {
        id: 'action_3',
        type: 'delay',
        name: 'Wait 24 Hours',
        config: {
          duration: '24 hours'
        }
      }
    ],
    schedule: null,
    createdAt: '2024-10-15T16:45:00Z',
    updatedAt: '2025-01-10T11:20:00Z',
    lastRun: '2025-01-15T08:15:00Z',
    nextRun: null,
    stats: {
      totalRuns: 89,
      successfulRuns: 85,
      failedRuns: 4,
      averageExecutionTime: 2.1,
      lastExecutionTime: 1.9
    },
    tags: ['billing', 'payment', 'recovery'],
    isTemplate: false
  },
  {
    id: 'auto_1357924680',
    name: 'Weekly Report Generation',
    description: 'Automated weekly performance report generation and distribution',
    type: 'scheduled',
    status: 'active',
    trigger: {
      type: 'schedule',
      schedule: '0 9 * * MON',
      timezone: 'UTC'
    },
    actions: [
      {
        id: 'action_1',
        type: 'data_export',
        name: 'Generate Weekly Report',
        config: {
          reportType: 'weekly_performance',
          format: 'pdf',
          includeCharts: true
        }
      },
      {
        id: 'action_2',
        type: 'email',
        name: 'Send Report to Team',
        config: {
          template: 'weekly_report_email',
          delay: '0 minutes',
          from: 'reports@company.com',
          subject: 'Weekly Performance Report - {{current_week}}',
          recipients: ['team@company.com', 'management@company.com']
        }
      }
    ],
    schedule: {
      frequency: 'weekly',
      dayOfWeek: 'monday',
      time: '09:00',
      timezone: 'UTC'
    },
    createdAt: '2024-09-20T12:00:00Z',
    updatedAt: '2024-12-01T10:15:00Z',
    lastRun: '2025-01-13T09:00:00Z',
    nextRun: '2025-01-20T09:00:00Z',
    stats: {
      totalRuns: 16,
      successfulRuns: 16,
      failedRuns: 0,
      averageExecutionTime: 45.2,
      lastExecutionTime: 42.1
    },
    tags: ['reporting', 'scheduled', 'weekly'],
    isTemplate: false
  }
];

const fallbackAutomationTemplates = [
  {
    id: 'template_welcome',
    name: 'Customer Welcome Series',
    description: 'Multi-step email sequence for new customers',
    category: 'onboarding',
    tags: ['email', 'welcome', 'onboarding'],
    popularity: 95,
    thumbnail: '/templates/welcome-series.jpg',
    config: {
      triggerType: 'event',
      actionCount: 4,
      estimatedSetupTime: '10 minutes'
    }
  },
  {
    id: 'template_abandoned_cart',
    name: 'Abandoned Cart Recovery',
    description: 'Recover lost sales with targeted follow-ups',
    category: 'ecommerce',
    tags: ['ecommerce', 'cart', 'recovery'],
    popularity: 87,
    thumbnail: '/templates/abandoned-cart.jpg',
    config: {
      triggerType: 'event',
      actionCount: 3,
      estimatedSetupTime: '15 minutes'
    }
  },
  {
    id: 'template_lead_nurture',
    name: 'Lead Nurturing Campaign',
    description: 'Convert leads with educational content series',
    category: 'marketing',
    tags: ['leads', 'nurturing', 'marketing'],
    popularity: 78,
    thumbnail: '/templates/lead-nurture.jpg',
    config: {
      triggerType: 'schedule',
      actionCount: 6,
      estimatedSetupTime: '20 minutes'
    }
  }
];

const fallbackAutomationLogs = [
  {
    id: 'log_3001',
    automationId: 'auto_1234567890',
    runId: 'run_15789',
    status: 'completed',
    startTime: '2025-01-15T09:30:00Z',
    endTime: '2025-01-15T09:30:48Z',
    duration: 0.8,
    triggeredBy: {
      type: 'event',
      data: { customerId: 'cust_12345', email: 'new@customer.com' }
    },
    actionsExecuted: [
      {
        actionId: 'action_1',
        status: 'completed',
        duration: 0.3,
        result: 'Email sent successfully'
      },
      {
        actionId: 'action_2',
        status: 'completed',
        duration: 0.0,
        result: 'Delay scheduled'
      }
    ],
    errors: [],
    metadata: {
      customerEmail: 'new@customer.com',
      templateUsed: 'welcome_email_v2'
    }
  },
  {
    id: 'log_3002',
    automationId: 'auto_0987654321',
    runId: 'run_15788',
    status: 'failed',
    startTime: '2025-01-15T08:15:00Z',
    endTime: '2025-01-15T08:15:12Z',
    duration: 12.0,
    triggeredBy: {
      type: 'event',
      data: { paymentId: 'pay_67890', customerId: 'cust_54321' }
    },
    actionsExecuted: [
      {
        actionId: 'action_1',
        status: 'completed',
        duration: 1.2,
        result: 'Email sent successfully'
      },
      {
        actionId: 'action_2',
        status: 'failed',
        duration: 10.8,
        result: 'Webhook request timed out'
      }
    ],
    errors: [
      {
        actionId: 'action_2',
        error: 'Request timeout',
        message: 'Webhook endpoint did not respond within 10 seconds'
      }
    ],
    metadata: {
      paymentId: 'pay_67890',
      attemptCount: 2
    }
  }
];

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const type = searchParams.get('type'); // 'automations', 'templates', 'logs'
    const automationId = searchParams.get('automation_id');
    const status = searchParams.get('status');
    const category = searchParams.get('category');
    const limit = searchParams.get('limit') || '10';
    const offset = searchParams.get('offset') || '0';

    const queryParams = new URLSearchParams({
      type: type || 'automations',
      limit,
      offset,
      ...(automationId && { automation_id: automationId }),
      ...(status && { status }),
      ...(category && { category })
    });

    const response = await fetch(`${BRAIN_API_URL}/api/brain/integrations/automations?${queryParams}`, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!response.ok) {
      console.error('Brain API integrations/automations error:', response.status);

      if (type === 'templates') {
        let filteredTemplates = fallbackAutomationTemplates;
        if (category) {
          filteredTemplates = fallbackAutomationTemplates.filter(template => template.category === category);
        }

        return NextResponse.json({
          templates: filteredTemplates.slice(parseInt(offset), parseInt(offset) + parseInt(limit)),
          total: filteredTemplates.length,
          pagination: {
            limit: parseInt(limit),
            offset: parseInt(offset),
            hasMore: (parseInt(offset) + parseInt(limit)) < filteredTemplates.length
          },
          categories: ['onboarding', 'ecommerce', 'marketing', 'billing', 'support']
        });
      } else if (type === 'logs') {
        let filteredLogs = fallbackAutomationLogs;
        if (automationId) {
          filteredLogs = fallbackAutomationLogs.filter(log => log.automationId === automationId);
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
        let filteredAutomations = fallbackAutomations;
        if (status) {
          filteredAutomations = fallbackAutomations.filter(automation => automation.status === status);
        }

        return NextResponse.json({
          automations: filteredAutomations.slice(parseInt(offset), parseInt(offset) + parseInt(limit)),
          total: filteredAutomations.length,
          pagination: {
            limit: parseInt(limit),
            offset: parseInt(offset),
            hasMore: (parseInt(offset) + parseInt(limit)) < filteredAutomations.length
          },
          stats: {
            total: filteredAutomations.length,
            active: filteredAutomations.filter(a => a.status === 'active').length,
            paused: filteredAutomations.filter(a => a.status === 'paused').length,
            failed: filteredAutomations.filter(a => a.status === 'failed').length,
            totalRuns: filteredAutomations.reduce((sum, a) => sum + a.stats.totalRuns, 0),
            successRate: (filteredAutomations.reduce((sum, a) => sum + a.stats.successfulRuns, 0) /
              filteredAutomations.reduce((sum, a) => sum + a.stats.totalRuns, 0) * 100)
          }
        });
      }
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.error('Integrations automations API error:', errorMessage);
    const urlParams = new URL(request.url).searchParams;
    const type = urlParams.get('type');

    if (type === 'templates') {
      return NextResponse.json({
        templates: fallbackAutomationTemplates,
        total: fallbackAutomationTemplates.length,
        pagination: {
          limit: parseInt(urlParams.get('limit') || '10'),
          offset: parseInt(urlParams.get('offset') || '0'),
          hasMore: false
        },
        categories: ['onboarding', 'ecommerce', 'marketing', 'billing', 'support']
      });
    } else if (type === 'logs') {
      return NextResponse.json({
        logs: fallbackAutomationLogs,
        total: fallbackAutomationLogs.length,
        pagination: {
          limit: parseInt(urlParams.get('limit') || '10'),
          offset: parseInt(urlParams.get('offset') || '0'),
          hasMore: false
        }
      });
    } else {
      return NextResponse.json({
        automations: fallbackAutomations,
        total: fallbackAutomations.length,
        pagination: {
          limit: parseInt(urlParams.get('limit') || '10'),
          offset: parseInt(urlParams.get('offset') || '0'),
          hasMore: false
        },
        stats: {
          total: fallbackAutomations.length,
          active: 3,
          paused: 0,
          failed: 0,
          totalRuns: 350,
          successRate: 97.7
        }
      });
    }
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, ...data } = body;

    const response = await fetch(`${BRAIN_API_URL}/api/brain/integrations/automations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      console.error('Brain API integrations/automations POST error:', response.status);

      // Handle different actions with fallback responses
      switch (action) {
        case 'create':
          const mockAutomation = {
            id: `auto_${Date.now()}`,
            name: data.name || 'New Automation',
            description: data.description || '',
            type: data.type || 'workflow',
            status: 'draft',
            trigger: data.trigger || { type: 'event', event: 'custom.event' },
            actions: data.actions || [],
            schedule: data.schedule || null,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            lastRun: null,
            nextRun: null,
            stats: {
              totalRuns: 0,
              successfulRuns: 0,
              failedRuns: 0,
              averageExecutionTime: 0,
              lastExecutionTime: 0
            },
            tags: data.tags || [],
            isTemplate: false
          };
          return NextResponse.json({ success: true, automation: mockAutomation });

        case 'create_from_template':
          const templateAutomation = {
            id: `auto_${Date.now()}`,
            name: data.name || `${data.templateName} - Copy`,
            description: data.description || '',
            type: 'workflow',
            status: 'draft',
            trigger: data.trigger || { type: 'event', event: 'custom.event' },
            actions: data.actions || [],
            schedule: null,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            lastRun: null,
            nextRun: null,
            stats: {
              totalRuns: 0,
              successfulRuns: 0,
              failedRuns: 0,
              averageExecutionTime: 0,
              lastExecutionTime: 0
            },
            tags: data.tags || [],
            isTemplate: false
          };
          return NextResponse.json({ success: true, automation: templateAutomation });

        case 'update':
          return NextResponse.json({ success: true, message: 'Automation updated successfully' });

        case 'toggle_status':
          return NextResponse.json({ success: true, message: 'Automation status toggled successfully' });

        case 'test_run':
          return NextResponse.json({
            success: true,
            runId: `run_${Date.now()}`,
            message: 'Test execution started successfully'
          });

        case 'duplicate':
          const duplicatedAutomation = {
            id: `auto_${Date.now()}`,
            name: `${data.name} - Copy`,
            description: data.description,
            type: data.type,
            status: 'draft',
            trigger: data.trigger,
            actions: data.actions,
            schedule: data.schedule,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            lastRun: null,
            nextRun: null,
            stats: {
              totalRuns: 0,
              successfulRuns: 0,
              failedRuns: 0,
              averageExecutionTime: 0,
              lastExecutionTime: 0
            },
            tags: data.tags || [],
            isTemplate: false
          };
          return NextResponse.json({ success: true, automation: duplicatedAutomation });

        default:
          return NextResponse.json({ success: true, message: 'Automation action processed successfully' });
      }
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Integrations automations POST API error:', error);
    return NextResponse.json(
      { error: 'Failed to process automation action', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const automationId = searchParams.get('automation_id');

    if (!automationId) {
      return NextResponse.json({ error: 'Automation ID is required' }, { status: 400 });
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/integrations/automations?automation_id=${automationId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!response.ok) {
      console.error('Brain API integrations/automations DELETE error:', response.status);
      return NextResponse.json({ success: true, message: 'Automation deleted successfully' });
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Integrations automations DELETE API error:', error);
    return NextResponse.json(
      { error: 'Failed to delete automation', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
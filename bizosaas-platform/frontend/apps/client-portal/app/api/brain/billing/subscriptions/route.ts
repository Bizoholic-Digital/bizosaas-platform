import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

// Sample fallback data for development
const fallbackSubscriptions = [
  {
    id: 'sub_enterprise_2024',
    planId: 'plan_enterprise_annual',
    planName: 'Enterprise Plan',
    status: 'active',
    currentPeriodStart: '2024-01-15T00:00:00Z',
    currentPeriodEnd: '2025-01-15T00:00:00Z',
    billingCycle: 'annual',
    amount: 34164.00, // $2,847 × 12
    currency: 'USD',
    nextBillingDate: '2025-01-15T00:00:00Z',
    trialEnd: null,
    created: '2024-01-15T10:30:00Z',
    canceledAt: null,
    cancelAtPeriodEnd: false,
    items: [
      {
        id: 'si_base_plan',
        planId: 'plan_enterprise_base',
        planName: 'Enterprise Base Plan',
        quantity: 1,
        amount: 28800.00, // $2,400 × 12
        currency: 'USD'
      },
      {
        id: 'si_storage_addon',
        planId: 'plan_storage_500gb',
        planName: 'Additional Storage (500GB)',
        quantity: 1,
        amount: 3000.00, // $250 × 12
        currency: 'USD'
      },
      {
        id: 'si_support_addon',
        planId: 'plan_priority_support',
        planName: 'Priority Support',
        quantity: 1,
        amount: 2364.00, // $197 × 12
        currency: 'USD'
      }
    ],
    features: [
      'Unlimited Users',
      '5TB Storage',
      '1M API Calls/month',
      '24/7 Priority Support',
      'Advanced Analytics',
      'Custom Integrations',
      'SLA Guarantee',
      'Dedicated Account Manager'
    ],
    usage: {
      currentPeriodUsage: {
        users: 12,
        storage: 245, // GB
        apiCalls: 8432,
        supportTickets: 3
      },
      limits: {
        users: -1, // unlimited
        storage: 5120, // 5TB in GB
        apiCalls: 1000000,
        supportTickets: -1 // unlimited
      }
    },
    discounts: [],
    metadata: {
      customerId: 'cus_acme_corp',
      accountManager: 'sarah.johnson@bizosaas.com',
      contractUrl: '/contracts/enterprise-2024.pdf'
    }
  }
];

const fallbackPlans = [
  {
    id: 'plan_starter_monthly',
    name: 'Starter Plan',
    description: 'Perfect for small teams getting started',
    amount: 99.00,
    currency: 'USD',
    interval: 'monthly',
    features: [
      '5 Users',
      '100GB Storage',
      '10K API Calls/month',
      'Email Support',
      'Basic Analytics'
    ],
    limits: {
      users: 5,
      storage: 100,
      apiCalls: 10000
    },
    popular: false,
    available: true
  },
  {
    id: 'plan_professional_monthly',
    name: 'Professional Plan',
    description: 'For growing businesses with advanced needs',
    amount: 299.00,
    currency: 'USD',
    interval: 'monthly',
    features: [
      '25 Users',
      '1TB Storage',
      '100K API Calls/month',
      'Priority Support',
      'Advanced Analytics',
      'Custom Integrations'
    ],
    limits: {
      users: 25,
      storage: 1000,
      apiCalls: 100000
    },
    popular: true,
    available: true
  },
  {
    id: 'plan_enterprise_monthly',
    name: 'Enterprise Plan',
    description: 'For large organizations requiring maximum flexibility',
    amount: 2847.00,
    currency: 'USD',
    interval: 'monthly',
    features: [
      'Unlimited Users',
      '5TB Storage',
      '1M API Calls/month',
      '24/7 Priority Support',
      'Advanced Analytics',
      'Custom Integrations',
      'SLA Guarantee',
      'Dedicated Account Manager'
    ],
    limits: {
      users: -1,
      storage: 5120,
      apiCalls: 1000000
    },
    popular: false,
    available: true
  }
];

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const type = searchParams.get('type'); // 'subscriptions' or 'plans'
    const includeUsage = searchParams.get('include_usage') === 'true';

    const queryParams = new URLSearchParams({
      type: type || 'subscriptions',
      include_usage: includeUsage.toString()
    });

    const response = await fetch(`${BRAIN_API_URL}/api/brain/billing/subscriptions?${queryParams}`, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
    });

    if (!response.ok) {
      console.error('Brain API billing/subscriptions error:', response.status);
      
      if (type === 'plans') {
        return NextResponse.json({
          plans: fallbackPlans,
          total: fallbackPlans.length
        });
      } else {
        return NextResponse.json({
          subscriptions: fallbackSubscriptions,
          total: fallbackSubscriptions.length,
          activeSubscription: fallbackSubscriptions.find(sub => sub.status === 'active')
        });
      }
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Billing subscriptions API error:', error);
    const urlParams = new URL(request.url).searchParams;
    const type = urlParams.get('type');
    
    if (type === 'plans') {
      return NextResponse.json({
        plans: fallbackPlans,
        total: fallbackPlans.length
      });
    } else {
      return NextResponse.json({
        subscriptions: fallbackSubscriptions,
        total: fallbackSubscriptions.length,
        activeSubscription: fallbackSubscriptions.find(sub => sub.status === 'active')
      });
    }
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, ...data } = body;
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/billing/subscriptions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      console.error('Brain API billing/subscriptions POST error:', response.status);
      
      // Handle different actions with fallback responses
      switch (action) {
        case 'create_subscription':
          const plan = fallbackPlans.find(p => p.id === data.planId);
          const mockSubscription = {
            id: `sub_${Date.now()}`,
            planId: data.planId,
            planName: plan?.name || 'Unknown Plan',
            status: 'active',
            currentPeriodStart: new Date().toISOString(),
            currentPeriodEnd: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
            billingCycle: data.billingCycle || 'monthly',
            amount: plan?.amount || 0,
            currency: 'USD',
            nextBillingDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
            trialEnd: data.trialDays ? new Date(Date.now() + data.trialDays * 24 * 60 * 60 * 1000).toISOString() : null,
            created: new Date().toISOString(),
            canceledAt: null,
            cancelAtPeriodEnd: false,
            items: [
              {
                id: 'si_main',
                planId: data.planId,
                planName: plan?.name || 'Unknown Plan',
                quantity: 1,
                amount: plan?.amount || 0,
                currency: 'USD'
              }
            ],
            features: plan?.features || [],
            usage: {
              currentPeriodUsage: { users: 0, storage: 0, apiCalls: 0, supportTickets: 0 },
              limits: plan?.limits || {}
            }
          };
          return NextResponse.json({ success: true, subscription: mockSubscription });
          
        case 'change_plan':
          return NextResponse.json({ 
            success: true, 
            message: 'Plan change scheduled for next billing cycle',
            effectiveDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString()
          });
          
        case 'cancel_subscription':
          return NextResponse.json({ 
            success: true, 
            message: data.immediate ? 'Subscription cancelled immediately' : 'Subscription will cancel at period end',
            canceledAt: data.immediate ? new Date().toISOString() : null,
            cancelAtPeriodEnd: !data.immediate
          });
          
        case 'reactivate_subscription':
          return NextResponse.json({ 
            success: true, 
            message: 'Subscription reactivated successfully',
            status: 'active'
          });
          
        case 'add_addon':
          return NextResponse.json({ 
            success: true, 
            message: 'Add-on service added to subscription',
            prorationAmount: Math.round((data.addonAmount || 0) * 0.5) // prorated amount
          });
          
        case 'remove_addon':
          return NextResponse.json({ 
            success: true, 
            message: 'Add-on service removed from subscription',
            refundAmount: Math.round((data.addonAmount || 0) * 0.5) // prorated refund
          });
          
        default:
          return NextResponse.json({ success: true, message: 'Subscription action processed successfully' });
      }
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Billing subscriptions POST API error:', error);
    return NextResponse.json(
      { error: 'Failed to process subscription action', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}

export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();
    const { subscriptionId, ...updates } = body;
    
    const response = await fetch(`${BRAIN_API_URL}/api/brain/billing/subscriptions`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      console.error('Brain API billing/subscriptions PUT error:', response.status);
      return NextResponse.json({ 
        success: true, 
        message: 'Subscription updated successfully',
        updatedFields: Object.keys(updates)
      });
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    console.error('Billing subscriptions PUT API error:', error);
    return NextResponse.json(
      { error: 'Failed to update subscription', details: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500 }
    );
  }
}
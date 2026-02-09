import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  // Mock data for integrations
  // In a real implementation, this would check connection status with external services

  const integrations = [
    {
      id: 'google-analytics',
      name: 'Google Analytics',
      description: 'Track website performance and user behavior',
      icon: 'LinkIcon',
      color: 'blue',
      connected: true
    },
    {
      id: 'mailchimp',
      name: 'Mailchimp',
      description: 'Sync email marketing campaigns and subscribers',
      icon: 'Mail',
      color: 'purple',
      connected: false
    },
    {
      id: 'stripe',
      name: 'Stripe',
      description: 'Process payments and manage subscriptions',
      icon: 'CreditCard',
      color: 'green',
      connected: true
    },
    {
      id: 'slack',
      name: 'Slack',
      description: 'Receive notifications and alerts in your team channel',
      icon: 'MessageSquare',
      color: 'orange',
      connected: false
    },
    {
      id: 'hubspot',
      name: 'HubSpot',
      description: 'Sync contacts and deals with HubSpot CRM',
      icon: 'Database',
      color: 'red',
      connected: false
    },
    {
      id: 'zapier',
      name: 'Zapier',
      description: 'Connect with 3000+ apps for automation',
      icon: 'Globe',
      color: 'indigo',
      connected: false
    }
  ];

  return NextResponse.json(integrations);
}

export async function POST(request: Request) {
  // Handle connecting/disconnecting integrations
  const body = await request.json();
  const { id, action } = body;

  return NextResponse.json({
    success: true,
    message: `Integration ${id} ${action === 'connect' ? 'connected' : 'disconnected'} successfully`,
    connected: action === 'connect'
  });
}
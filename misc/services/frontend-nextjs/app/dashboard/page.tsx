'use client';

import React from 'react';
import { RealtimeDashboard } from '@/components/realtime/RealtimeDashboard';
import { RealtimeProvider } from '@/components/providers/RealtimeProvider';

export default function DashboardPage() {
  return (
    <RealtimeProvider
      config={{
        url: process.env.NEXT_PUBLIC_WEBSOCKET_URL || 'ws://localhost:8001/ws/realtime'
      }}
      subscription={{
        metrics: ['dashboard', 'social_media', 'campaigns', 'leads', 'system_health', 'ai_agents'],
        notifications: true,
        events: ['campaign', 'lead', 'payment', 'system', 'ai_agent'],
        real_time_updates: true
      }}
      enableToasts={true}
    >
      <RealtimeDashboard />
    </RealtimeProvider>
  );
}
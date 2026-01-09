'use client';

import React from 'react';
import DashboardOverview from '@/components/dashboard/DashboardOverview';
import { AgentOptimizations } from '@/components/dashboard/AgentOptimizations';
import { PageHeader } from '@/components/dashboard/PageHeader';

export default function DashboardPage() {
  return (
    <div className="min-h-full bg-slate-50 dark:bg-slate-950 p-4 md:p-6 space-y-6 md:space-y-10 animate-in fade-in duration-500">
      <PageHeader
        title="Dashboard Overview"
        description="Unified Command Center for platform-wide operations and health."
      />

      <DashboardOverview />

      <div className="pt-4">
        <AgentOptimizations />
      </div>
    </div>
  );
}
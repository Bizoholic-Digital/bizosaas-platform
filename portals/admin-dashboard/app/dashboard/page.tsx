'use client';

import React from 'react';
import DashboardOverview from '@/components/dashboard/DashboardOverview';
import { AgentOptimizations } from '@/components/dashboard/AgentOptimizations';

export default function DashboardPage() {
  return (
    <div className="min-h-full bg-slate-50 dark:bg-slate-950 p-4 md:p-6 space-y-6 md:space-y-10 animate-in fade-in duration-500">
      {/* Header removed for standardization */}

      <DashboardOverview />

      <div className="pt-4">
        <AgentOptimizations />
      </div>
    </div>
  );
}
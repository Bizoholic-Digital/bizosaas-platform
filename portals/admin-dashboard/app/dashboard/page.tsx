'use client';

import React from 'react';
import DashboardOverview from '@/components/dashboard/DashboardOverview';
import { AgentOptimizations } from '@/components/dashboard/AgentOptimizations';

export default function DashboardPage() {
  return (
    <div className="min-h-full bg-slate-50 dark:bg-slate-950 p-6 space-y-10 animate-in fade-in duration-500">
      <div>
        <h1 className="text-4xl font-black tracking-tighter text-slate-900 dark:text-white uppercase italic">
          Admin <span className="text-indigo-600">Overview</span>
        </h1>
        <p className="text-lg text-slate-600 dark:text-slate-400 mt-2 font-medium">Centralized orchestration and platform health at a glance.</p>
      </div>

      <DashboardOverview />

      <div className="pt-4">
        <AgentOptimizations />
      </div>
    </div>
  );
}
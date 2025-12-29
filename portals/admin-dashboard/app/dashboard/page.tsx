'use client';

import React from 'react';
import DashboardOverview from '@/components/dashboard/DashboardOverview';

export default function DashboardPage() {
  return (
    <div className="min-h-full bg-slate-50 dark:bg-slate-950 p-6 space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white">Admin Overview</h1>
        <p className="text-lg text-slate-600 dark:text-slate-400 mt-2">Centralized orchestration and platform health at a glance.</p>
      </div>

      <DashboardOverview />
    </div>
  );
}
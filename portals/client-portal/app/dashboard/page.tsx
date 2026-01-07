'use client';

import React from 'react';
import { useUser } from "@clerk/nextjs";
import { Plug, Sparkles, BarChart3, TrendingUp } from 'lucide-react';
import { getUserDisplayInfoFromSession } from '@/utils/rbac';
import { ProjectTasksWidget } from '@/components/dashboard/widgets/ProjectTasksWidget';
import { MagicDiscovery } from '@/components/discovery/MagicDiscovery';

export default function DashboardPage() {
  const { user } = useUser();

  const sessionUser = user ? {
    role: user.publicMetadata?.role || 'user',
    tenant_id: user.publicMetadata?.tenant_id,
    name: user.fullName,
    email: user.primaryEmailAddress?.emailAddress
  } : null;

  const userInfo = getUserDisplayInfoFromSession(sessionUser);
  const { tenantId } = userInfo;

  return (
    <div className="p-4 md:p-6 space-y-4 md:space-y-6">
      <MagicDiscovery />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-gray-900 p-4 md:p-6 rounded-xl border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-10 h-10 md:w-12 md:h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
              <Plug className="w-5 h-5 md:w-6 md:h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div className="ml-3 md:ml-4">
              <p className="text-[10px] md:text-sm font-bold text-gray-400 uppercase tracking-tight">Connectors</p>
              <p className="text-lg md:text-2xl font-black text-gray-900 dark:text-white leading-none mt-1">3</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-4 md:p-6 rounded-xl border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-10 h-10 md:w-12 md:h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
              <Sparkles className="w-5 h-5 md:w-6 md:h-6 text-green-600 dark:text-green-400" />
            </div>
            <div className="ml-3 md:ml-4">
              <p className="text-[10px] md:text-sm font-bold text-gray-400 uppercase tracking-tight">AI Tasks</p>
              <p className="text-lg md:text-2xl font-black text-gray-900 dark:text-white leading-none mt-1">128</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-4 md:p-6 rounded-xl border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-10 h-10 md:w-12 md:h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-5 h-5 md:w-6 md:h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <div className="ml-3 md:ml-4">
              <p className="text-[10px] md:text-sm font-bold text-gray-400 uppercase tracking-tight">Traffic</p>
              <p className="text-lg md:text-2xl font-black text-gray-900 dark:text-white leading-none mt-1">12.5k</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-4 md:p-6 rounded-xl border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-10 h-10 md:w-12 md:h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-5 h-5 md:w-6 md:h-6 text-orange-600 dark:text-orange-400" />
            </div>
            <div className="ml-3 md:ml-4">
              <p className="text-[10px] md:text-sm font-bold text-gray-400 uppercase tracking-tight">Conv.</p>
              <p className="text-lg md:text-2xl font-black text-gray-900 dark:text-white leading-none mt-1">4.2%</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* GraphQL Powered Widget */}
        <ProjectTasksWidget tenantId={tenantId} />

        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Recent Activity</h3>
            <button className="text-sm text-blue-500 hover:underline">View All</button>
          </div>
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 text-xs">AI</div>
              <div>
                <p className="text-sm font-medium">Agent "SEO Expert" generated a report</p>
                <p className="text-xs text-gray-500">2 minutes ago</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-600 text-xs">CRM</div>
              <div>
                <p className="text-sm font-medium">New Lead via HubSpot</p>
                <p className="text-xs text-gray-500">1 hour ago</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-900 p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-sm">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Welcome to Bizo</h3>
        <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">
          Your central hub for managing your digital presence. Connect your platforms, activate AI agents, and scale your business effortlessly.
        </p>
      </div>
    </div>
  );
}
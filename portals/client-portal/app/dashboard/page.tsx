'use client';

import React from 'react';
import { useSession } from 'next-auth/react';
import { Plug, Sparkles, BarChart3, TrendingUp } from 'lucide-react';
import { getUserDisplayInfoFromSession } from '@/utils/rbac';
import { ProjectTasksWidget } from '@/components/dashboard/widgets/ProjectTasksWidget';

export default function DashboardPage() {
  const { data: session } = useSession();
  const userInfo = getUserDisplayInfoFromSession(session?.user);
  const { tenantId } = userInfo;

  return (
    <div className="p-6 space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
              <Plug className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Active Connectors</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">3</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">AI Tasks</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">128</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Traffic</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">12.5k</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-orange-600 dark:text-orange-400" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Conversions</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">4.2%</p>
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

      <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Welcome to BizOSaaS</h3>
        <p className="text-gray-600 dark:text-gray-400">
          Your central hub for managing your digital presence. Connect your existing platforms, leverage AI agents, and grow your business.
        </p>
      </div>
    </div>
  );
}
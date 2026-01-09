'use client';

import Link from 'next/link';
import DashboardLayout from '@/components/ui/dashboard-layout';
import { Settings as SettingsIcon, User, Bell, Lock, Palette, Globe } from 'lucide-react';

export default function SettingsPage() {
  return (
    <DashboardLayout
      title="Settings"
      description="Manage your account and preferences"
    >
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Link href="/settings/profile" className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition-shadow cursor-pointer block border border-transparent hover:border-blue-200 dark:hover:border-blue-900">
            <div className="flex items-center gap-4 mb-4">
              <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-lg">
                <User className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">Profile</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">Manage your account details</p>
              </div>
            </div>
          </Link>

          <Link href="/settings/notifications" className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition-shadow cursor-pointer block border border-transparent hover:border-purple-200 dark:hover:border-purple-900">
            <div className="flex items-center gap-4 mb-4">
              <div className="p-3 bg-purple-100 dark:bg-purple-900 rounded-lg">
                <Bell className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">Notifications</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">Configure alerts and emails</p>
              </div>
            </div>
          </Link>

          <Link href="/settings/security" className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition-shadow cursor-pointer block border border-transparent hover:border-green-200 dark:hover:border-green-900">
            <div className="flex items-center gap-4 mb-4">
              <div className="p-3 bg-green-100 dark:bg-green-900 rounded-lg">
                <Lock className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">Security</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">Password and 2FA settings</p>
              </div>
            </div>
          </Link>

          <Link href="/settings/appearance" className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition-shadow cursor-pointer block border border-transparent hover:border-orange-200 dark:hover:border-orange-900">
            <div className="flex items-center gap-4 mb-4">
              <div className="p-3 bg-orange-100 dark:bg-orange-900 rounded-lg">
                <Palette className="w-6 h-6 text-orange-600 dark:text-orange-400" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">Appearance</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">Theme and display options</p>
              </div>
            </div>
          </Link>

          <Link href="/settings/localization" className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition-shadow cursor-pointer block border border-transparent hover:border-indigo-200 dark:hover:border-indigo-900">
            <div className="flex items-center gap-4 mb-4">
              <div className="p-3 bg-indigo-100 dark:bg-indigo-900 rounded-lg">
                <Globe className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">Localization</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">Currency and regional settings</p>
              </div>
            </div>
          </Link>

          <Link href="/settings/integrations" className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition-shadow cursor-pointer block border border-transparent hover:border-red-200 dark:hover:border-red-900">
            <div className="flex items-center gap-4 mb-4">
              <div className="p-3 bg-red-100 dark:bg-red-900 rounded-lg">
                <SettingsIcon className="w-6 h-6 text-red-600 dark:text-red-400" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">Advanced</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">API keys and integrations</p>
              </div>
            </div>
          </Link>
        </div>

        <div className="mt-6 bg-white dark:bg-gray-800 rounded-lg shadow p-6 border border-slate-100 dark:border-slate-700">
          <div className="text-center py-8">
            <SettingsIcon className="w-12 h-12 mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Settings Dashboard
            </h3>
            <p className="text-gray-500 dark:text-gray-400">
              Select a category above to manage your workspace preferences.
            </p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

'use client'

import { useState } from 'react'
import { Settings, Save, RefreshCw } from 'lucide-react'

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    platform_name: 'BizOSaaS',
    maintenance_mode: false,
    registration_enabled: true,
    email_notifications: true,
    auto_backup: true,
    session_timeout: 30,
    max_file_size: 10
  })

  const handleSave = () => {
    // Save settings logic here
    console.log('Saving settings:', settings)
  }

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">System Settings</h1>
        <p className="text-gray-600">Platform configuration and global settings</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
            <Settings className="h-5 w-5 mr-2" />
            General Settings
          </h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Platform Name</label>
              <input
                type="text"
                value={settings.platform_name}
                onChange={(e) => setSettings({...settings, platform_name: e.target.value})}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Session Timeout (minutes)</label>
              <input
                type="number"
                value={settings.session_timeout}
                onChange={(e) => setSettings({...settings, session_timeout: parseInt(e.target.value)})}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Max File Size (MB)</label>
              <input
                type="number"
                value={settings.max_file_size}
                onChange={(e) => setSettings({...settings, max_file_size: parseInt(e.target.value)})}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">System Controls</h3>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-sm font-medium text-gray-900">Maintenance Mode</h4>
                <p className="text-sm text-gray-500">Temporarily disable access for maintenance</p>
              </div>
              <button
                className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                  settings.maintenance_mode ? 'bg-blue-600' : 'bg-gray-200'
                }`}
                onClick={() => setSettings({...settings, maintenance_mode: !settings.maintenance_mode})}
              >
                <span
                  className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                    settings.maintenance_mode ? 'translate-x-5' : 'translate-x-0'
                  }`}
                />
              </button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-sm font-medium text-gray-900">Registration Enabled</h4>
                <p className="text-sm text-gray-500">Allow new user registrations</p>
              </div>
              <button
                className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                  settings.registration_enabled ? 'bg-blue-600' : 'bg-gray-200'
                }`}
                onClick={() => setSettings({...settings, registration_enabled: !settings.registration_enabled})}
              >
                <span
                  className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                    settings.registration_enabled ? 'translate-x-5' : 'translate-x-0'
                  }`}
                />
              </button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-sm font-medium text-gray-900">Email Notifications</h4>
                <p className="text-sm text-gray-500">Send system notifications via email</p>
              </div>
              <button
                className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                  settings.email_notifications ? 'bg-blue-600' : 'bg-gray-200'
                }`}
                onClick={() => setSettings({...settings, email_notifications: !settings.email_notifications})}
              >
                <span
                  className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                    settings.email_notifications ? 'translate-x-5' : 'translate-x-0'
                  }`}
                />
              </button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-sm font-medium text-gray-900">Auto Backup</h4>
                <p className="text-sm text-gray-500">Automatically backup system data</p>
              </div>
              <button
                className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                  settings.auto_backup ? 'bg-blue-600' : 'bg-gray-200'
                }`}
                onClick={() => setSettings({...settings, auto_backup: !settings.auto_backup})}
              >
                <span
                  className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                    settings.auto_backup ? 'translate-x-5' : 'translate-x-0'
                  }`}
                />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-end gap-3">
        <button className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
          <RefreshCw className="h-4 w-4 mr-2" />
          Reset
        </button>
        <button 
          onClick={handleSave}
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700"
        >
          <Save className="h-4 w-4 mr-2" />
          Save Changes
        </button>
      </div>
    </div>
  )
}
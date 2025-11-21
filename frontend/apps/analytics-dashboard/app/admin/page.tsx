'use client'

export default function AdminPage() {
  return (
    <div className="space-y-6">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Admin Panel</h2>
        <p className="text-gray-600 mt-2">Platform administration and management interface</p>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Admin Features</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
            <h4 className="font-medium text-gray-900">User Management</h4>
            <p className="text-gray-600 text-sm mt-1">Manage platform users and permissions</p>
          </div>
          <div className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
            <h4 className="font-medium text-gray-900">System Settings</h4>
            <p className="text-gray-600 text-sm mt-1">Configure platform settings and features</p>
          </div>
          <div className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
            <h4 className="font-medium text-gray-900">Analytics Configuration</h4>
            <p className="text-gray-600 text-sm mt-1">Set up analytics tracking and reports</p>
          </div>
        </div>
      </div>

      <div className="bg-green-50 border border-green-200 rounded-lg p-6">
        <div className="flex items-center">
          <div className="p-2 rounded-full bg-green-100">
            <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-green-800">Admin Panel Active</h3>
            <p className="text-sm text-green-700">Analytics Dashboard with Admin functionality is now running on port 3009</p>
          </div>
        </div>
      </div>
    </div>
  )
}
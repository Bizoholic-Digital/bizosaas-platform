'use client'

import { useAuth } from '@/lib/auth'

export default function SettingsPage() {
  const { user } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Account Settings</h1>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <form className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
              <input type="text" defaultValue={user?.name} className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <input type="email" defaultValue={user?.email} className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
            </div>
            <button type="submit" className="btn-primary px-6 py-2">Save Changes</button>
          </form>
        </div>
      </div>
    </div>
  )
}

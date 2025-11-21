'use client'

export default function TeamPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Team Management</h1>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <button className="btn-primary mb-6">Invite Team Member</button>
          <p className="text-gray-600">Team members list will be displayed here.</p>
        </div>
      </div>
    </div>
  )
}

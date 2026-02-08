'use client'

export default function NewCampaignPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Create New Campaign</h1>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <form className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Campaign Name</label>
              <input type="text" placeholder="Enter campaign name" className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Campaign Type</label>
              <select className="w-full px-4 py-2 border border-gray-300 rounded-lg">
                <option>SEO Campaign</option>
                <option>PPC Campaign</option>
                <option>Social Media Campaign</option>
                <option>Email Campaign</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Budget</label>
              <input type="number" placeholder="0" className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
            </div>
            <button type="submit" className="btn-primary px-6 py-2">Create Campaign</button>
          </form>
        </div>
      </div>
    </div>
  )
}

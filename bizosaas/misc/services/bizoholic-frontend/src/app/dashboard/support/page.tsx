'use client'

export default function SupportPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Support</h1>
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-xl font-semibold mb-4">Create Support Ticket</h2>
          <form className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Subject</label>
              <input type="text" className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
              <textarea rows={5} className="w-full px-4 py-2 border border-gray-300 rounded-lg"></textarea>
            </div>
            <button type="submit" className="btn-primary px-6 py-2">Submit Ticket</button>
          </form>
        </div>
      </div>
    </div>
  )
}

'use client'

export default function BillingPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Billing & Invoices</h1>
        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-xl font-semibold mb-4">Current Plan</h2>
            <p className="text-3xl font-bold text-primary-600 mb-2">$599/month</p>
            <p className="text-gray-600">Growth SEO Plan</p>
          </div>
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-xl font-semibold mb-4">Payment Method</h2>
            <p className="text-gray-600">Visa ending in 4242</p>
          </div>
        </div>
      </div>
    </div>
  )
}

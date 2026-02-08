'use client'

import { useEffect } from 'react'

export default function LoginRedirectPage() {
  useEffect(() => {
    // Redirect to BizOSaaS ecommerce management section
    // This will eventually redirect to the Saleor admin integration within BizOSaaS
    window.location.href = 'http://localhost:3000/auth/login?redirect=ecommerce'
  }, [])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center max-w-md">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <h2 className="mt-4 text-xl font-semibold text-gray-800">CoreLDove Admin Access</h2>
        <p className="mt-2 text-gray-600">Redirecting to unified ecommerce management...</p>
        <p className="text-sm text-gray-500 mt-4">
          Access your store management, products, orders, and marketing automation from one dashboard.
        </p>
        <p className="text-xs text-gray-400 mt-2">
          If you're not redirected automatically, <a href="http://localhost:3000/auth/login?redirect=ecommerce" className="text-blue-600 underline">click here</a>
        </p>
      </div>
    </div>
  )
}
'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function LoginRedirectPage() {
  const router = useRouter()

  useEffect(() => {
    // Redirect to Wagtail admin login
    window.location.href = 'http://localhost:8005/admin/login/'
  }, [])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="mt-4 text-gray-600">Redirecting to Wagtail Admin...</p>
        <p className="text-sm text-gray-500 mt-2">
          If you're not redirected automatically, <a href="http://localhost:8005/admin/login/" className="text-blue-600 underline">click here</a>
        </p>
      </div>
    </div>
  )
}
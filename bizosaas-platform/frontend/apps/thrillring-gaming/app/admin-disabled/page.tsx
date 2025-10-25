/**
 * BizOSaaS Admin Portal Entry Point
 * This handles authentication and redirects to the appropriate dashboard
 * Access via: localhost:3000/admin (redirects to localhost:3005)
 */

'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function AdminPage() {
  const router = useRouter()

  useEffect(() => {
    // Redirect to the admin portal on localhost:3005
    window.location.href = 'http://localhost:3005'
  }, [])

  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <div className="text-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent mx-auto mb-4" />
        <p className="text-muted-foreground">Redirecting to Admin Portal...</p>
      </div>
    </div>
  )
}
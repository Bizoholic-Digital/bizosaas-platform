'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function BizosaasPage() {
  const router = useRouter()
  
  useEffect(() => {
    router.replace('/portal/login')
  }, [router])
  
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Redirecting to Client Portal...</h1>
        <p className="text-muted-foreground">Please wait while we redirect you to the login page.</p>
      </div>
    </div>
  )
}

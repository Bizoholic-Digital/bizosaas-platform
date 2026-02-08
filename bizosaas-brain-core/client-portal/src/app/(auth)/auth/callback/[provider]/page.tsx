'use client'

import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useAuth } from '@/lib/auth'

export default function OAuthCallbackPage({
  params,
}: {
  params: Promise<{ provider: string }>
}) {
  const [provider, setProvider] = useState<string>('')

  useEffect(() => {
    params.then((p) => setProvider(p.provider))
  }, [params])
  const router = useRouter()
  const searchParams = useSearchParams()
  const { refreshUser } = useAuth()
  const [error, setError] = useState<string | null>(null)
  const [processing, setProcessing] = useState(true)

  useEffect(() => {
    const handleCallback = async () => {
      if (!provider) return // Wait for provider to be set

      try {
        const code = searchParams.get('code')
        const state = searchParams.get('state')
        const errorParam = searchParams.get('error')

        // Check for OAuth provider errors
        if (errorParam) {
          setError(`Authentication failed: ${errorParam}`)
          setProcessing(false)
          return
        }

        if (!code || !state) {
          setError('Missing authorization code or state parameter')
          setProcessing(false)
          return
        }

        // Exchange code for tokens via backend
        const response = await fetch(
          `/api/auth/oauth/${provider}/callback?code=${code}&state=${state}`,
          {
            method: 'GET',
            credentials: 'include',
          }
        )

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({ detail: 'Authentication failed' }))
          throw new Error(errorData.detail || 'OAuth callback failed')
        }

        const data = await response.json()

        // Backend sets HttpOnly refresh_token cookie automatically
        // Access token is returned in response
        if (data.access_token) {
          // Refresh user state to load authenticated user
          await refreshUser()

          // Redirect to dashboard
          router.push('/dashboard')
        } else {
          throw new Error('No access token received')
        }
      } catch (err: any) {
        console.error('OAuth callback error:', err)
        setError(err.message || 'Authentication failed')
        setProcessing(false)
      }
    }

    handleCallback()
  }, [provider, searchParams, router, refreshUser])

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-red-100">
              <svg className="h-8 w-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <h2 className="mt-6 text-3xl font-bold text-gray-900">
              Authentication Failed
            </h2>
            <p className="mt-2 text-sm text-gray-600">
              {error}
            </p>
            <div className="mt-6">
              <a
                href="/login"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Back to Login
              </a>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center h-16 w-16">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600"></div>
          </div>
          <h2 className="mt-6 text-3xl font-bold text-gray-900">
            Completing Sign In
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Please wait while we sign you in with {provider}...
          </p>
        </div>
      </div>
    </div>
  )
}

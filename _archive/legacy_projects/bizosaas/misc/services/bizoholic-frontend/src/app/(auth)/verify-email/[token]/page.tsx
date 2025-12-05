'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useParams } from 'next/navigation'
import { authClient } from '@bizoholic-digital/auth'
import { CheckCircle, XCircle, Loader2 } from 'lucide-react'

export default function VerifyEmailPage() {
  const router = useRouter()
  const params = useParams()
  const token = params.token as string
  const [verifying, setVerifying] = useState(true)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    const verify = async () => {
      try {
        await authClient.verifyEmail(token)
        setSuccess(true)
        setVerifying(false)
        // Redirect to dashboard after 3 seconds
        setTimeout(() => {
          router.push('/dashboard')
        }, 3000)
      } catch (err: any) {
        setError(err.message || 'Failed to verify email. The link may have expired.')
        setVerifying(false)
      }
    }

    verify()
  }, [token, router])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {verifying ? (
            <div className="text-center space-y-4">
              {/* Loading Icon */}
              <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
              </div>

              {/* Loading Message */}
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Verifying your email
                </h3>
                <p className="text-gray-600">
                  Please wait while we verify your email address...
                </p>
              </div>
            </div>
          ) : success ? (
            <div className="text-center space-y-4">
              {/* Success Icon */}
              <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                <CheckCircle className="w-8 h-8 text-green-600" />
              </div>

              {/* Success Message */}
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Email verified successfully!
                </h3>
                <p className="text-gray-600 mb-4">
                  Your email has been verified. You can now access all features of your Bizoholic account.
                </p>
                <p className="text-sm text-gray-500">
                  Redirecting to dashboard...
                </p>
              </div>

              {/* Dashboard Link */}
              <Link
                href="/dashboard"
                className="inline-block btn-primary px-6 py-2"
              >
                Go to dashboard
              </Link>
            </div>
          ) : (
            <div className="text-center space-y-4">
              {/* Error Icon */}
              <div className="mx-auto w-16 h-16 bg-red-100 rounded-full flex items-center justify-center">
                <XCircle className="w-8 h-8 text-red-600" />
              </div>

              {/* Error Message */}
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Verification failed
                </h3>
                <p className="text-gray-600 mb-4">
                  {error}
                </p>
                <p className="text-sm text-gray-500 mb-6">
                  The verification link may have expired or already been used. Please request a new verification email.
                </p>
              </div>

              {/* Action Buttons */}
              <div className="space-y-3">
                <Link
                  href="/resend-verification"
                  className="block w-full btn-primary px-6 py-2 text-center"
                >
                  Resend verification email
                </Link>
                <Link
                  href="/contact"
                  className="block w-full btn-secondary px-6 py-2 text-center"
                >
                  Contact support
                </Link>
              </div>
            </div>
          )}
        </div>

        {/* Help Text */}
        {!verifying && !success && (
          <p className="text-center text-sm text-gray-600">
            Need help?{' '}
            <Link
              href="/contact"
              className="font-medium text-primary-600 hover:text-primary-500 transition-colors"
            >
              Contact our support team
            </Link>
          </p>
        )}
      </div>
    </div>
  )
}

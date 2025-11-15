'use client'

import { useState } from 'react'
import Link from 'next/link'
import { authClient } from '@/lib/auth'
import { ArrowLeft, Mail } from 'lucide-react'

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setSuccess(false)
    setLoading(true)

    try {
      await authClient.requestPasswordReset(email)
      setSuccess(true)
    } catch (err: any) {
      setError(err.message || 'Failed to send reset email. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <h2 className="text-4xl font-bold text-gray-900">
            Forgot password?
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            No worries, we&apos;ll send you reset instructions
          </p>
        </div>

        {/* Form */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {!success ? (
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Error Message */}
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
                  {error}
                </div>
              )}

              {/* Email Field */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email address
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="you@company.com"
                />
                <p className="text-xs text-gray-500 mt-2">
                  Enter the email address associated with your account
                </p>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Sending...' : 'Reset password'}
              </button>
            </form>
          ) : (
            <div className="text-center space-y-4">
              {/* Success Icon */}
              <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                <Mail className="w-8 h-8 text-green-600" />
              </div>

              {/* Success Message */}
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Check your email
                </h3>
                <p className="text-gray-600 mb-4">
                  We sent a password reset link to
                </p>
                <p className="text-sm font-medium text-gray-900 mb-4">
                  {email}
                </p>
                <p className="text-sm text-gray-500">
                  Click the link in the email to reset your password. If you don&apos;t see the email, check your spam folder.
                </p>
              </div>

              {/* Resend Button */}
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="text-sm text-primary-600 hover:text-primary-500 font-medium transition-colors disabled:opacity-50"
              >
                Didn&apos;t receive the email? Click to resend
              </button>
            </div>
          )}
        </div>

        {/* Back to Login */}
        <div className="text-center">
          <Link
            href="/login"
            className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to login
          </Link>
        </div>
      </div>
    </div>
  )
}

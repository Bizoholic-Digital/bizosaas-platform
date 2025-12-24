'use client'

import { useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Eye, EyeOff, Mail, Lock, ArrowRight } from 'lucide-react'

export interface UnifiedLoginFormProps {
    /** Authentication mode: 'sso' for SSO only, 'credentials' for email/password, 'both' for both options */
    mode: 'sso' | 'credentials' | 'both'

    /** Platform name to display */
    platformName: string

    /** Platform subtitle/description */
    platformSubtitle?: string

    /** SSO provider name (e.g., 'Authentik', 'Okta') */
    ssoProviderName?: string

    /** SSO provider ID for NextAuth */
    ssoProviderId?: string

    /** Default redirect URL after login */
    defaultRedirectUrl?: string

    /** Custom branding component */
    BrandingComponent?: React.ComponentType<any>

    /** Show demo credentials (for development) */
    showDemoCredentials?: boolean

    /** Custom CSS classes */
    className?: string

    /** Callback for credentials login */
    onCredentialsLogin?: (email: string, password: string) => Promise<{ ok: boolean; error?: string }>

    /** Callback for SSO login */
    onSSOLogin?: () => Promise<void>
}

export function UnifiedLoginForm({
    mode,
    platformName,
    platformSubtitle,
    ssoProviderName = 'SSO',
    ssoProviderId = 'authentik',
    defaultRedirectUrl = '/',
    BrandingComponent,
    showDemoCredentials = false,
    className = '',
    onCredentialsLogin,
    onSSOLogin,
}: UnifiedLoginFormProps) {
    const [email, setEmail] = useState(showDemoCredentials ? 'admin@bizoholic.com' : '')
    const [password, setPassword] = useState(showDemoCredentials ? 'AdminDemo2024!' : '')
    const [showPassword, setShowPassword] = useState(false)
    const [rememberMe, setRememberMe] = useState(false)
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const router = useRouter()
    const searchParams = useSearchParams()
    const callbackUrl = searchParams?.get('callbackUrl') || defaultRedirectUrl

    const handleCredentialsSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError(null)

        if (!email || !password) {
            setError('Please enter both email and password.')
            return
        }

        setIsLoading(true)

        try {
            if (onCredentialsLogin) {
                const result = await onCredentialsLogin(email, password)
                if (result.ok) {
                    router.push(callbackUrl)
                    router.refresh()
                } else {
                    setError(result.error || 'Invalid credentials')
                }
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Login failed')
        } finally {
            setIsLoading(false)
        }
    }

    const handleSSOLogin = async () => {
        setIsLoading(true)
        setError(null)

        try {
            if (onSSOLogin) {
                await onSSOLogin()
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'SSO login failed')
            setIsLoading(false)
        }
    }

    return (
        <div className={`min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950 ${className}`}>
            <div className="max-w-md w-full mx-4">
                <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-2xl p-8 space-y-8 border border-gray-200 dark:border-gray-800">
                    {/* Header */}
                    <div className="text-center space-y-4">
                        {BrandingComponent && (
                            <div className="flex justify-center">
                                <BrandingComponent />
                            </div>
                        )}
                        <div>
                            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
                                {platformName}
                            </h2>
                            {platformSubtitle && (
                                <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                                    {platformSubtitle}
                                </p>
                            )}
                        </div>
                    </div>

                    {/* Error Message */}
                    {error && (
                        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                            <p className="text-sm text-red-700 dark:text-red-400">{error}</p>
                        </div>
                    )}

                    {/* Credentials Form */}
                    {(mode === 'credentials' || mode === 'both') && (
                        <form onSubmit={handleCredentialsSubmit} className="space-y-4">
                            <div className="space-y-2">
                                <label htmlFor="email" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                    Email address
                                </label>
                                <div className="relative">
                                    <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                                    <input
                                        id="email"
                                        type="email"
                                        placeholder="Enter your email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                                        required
                                        disabled={isLoading}
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <label htmlFor="password" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                    Password
                                </label>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                                    <input
                                        id="password"
                                        type={showPassword ? 'text' : 'password'}
                                        placeholder="Enter your password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        className="w-full pl-10 pr-12 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                                        required
                                        disabled={isLoading}
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                                        disabled={isLoading}
                                    >
                                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                    </button>
                                </div>
                            </div>

                            <div className="flex items-center">
                                <input
                                    id="remember"
                                    type="checkbox"
                                    checked={rememberMe}
                                    onChange={(e) => setRememberMe(e.target.checked)}
                                    className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                                    disabled={isLoading}
                                />
                                <label htmlFor="remember" className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                                    Remember me
                                </label>
                            </div>

                            <button
                                type="submit"
                                className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center"
                                disabled={isLoading}
                            >
                                {isLoading ? (
                                    <>
                                        <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent mr-2" />
                                        Signing in...
                                    </>
                                ) : (
                                    <>
                                        Sign In
                                        <ArrowRight className="ml-2 h-4 w-4" />
                                    </>
                                )}
                            </button>

                            {showDemoCredentials && (
                                <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-950 rounded-lg border border-blue-200 dark:border-blue-800">
                                    <p className="text-sm text-blue-700 dark:text-blue-300">
                                        <strong>Demo Credentials:</strong><br />
                                        Email: admin@bizoholic.com<br />
                                        Password: AdminDemo2024!
                                    </p>
                                </div>
                            )}
                        </form>
                    )}

                    {/* Divider for 'both' mode */}
                    {mode === 'both' && (
                        <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                                <div className="w-full border-t border-gray-300 dark:border-gray-700"></div>
                            </div>
                            <div className="relative flex justify-center text-sm">
                                <span className="px-2 bg-white dark:bg-gray-900 text-gray-500">Or continue with</span>
                            </div>
                        </div>
                    )}

                    {/* SSO Button */}
                    {(mode === 'sso' || mode === 'both') && (
                        <div className="space-y-4">
                            {mode === 'sso' && (
                                <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                                    <div className="flex items-start space-x-3">
                                        <svg className="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                        </svg>
                                        <div className="flex-1">
                                            <p className="text-sm font-medium text-blue-900 dark:text-blue-300">
                                                Secure SSO Authentication
                                            </p>
                                            <p className="text-xs text-blue-700 dark:text-blue-400 mt-1">
                                                Sign in with your organization credentials via {ssoProviderName}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            )}

                            <button
                                type="button"
                                onClick={handleSSOLogin}
                                className="w-full h-12 text-base font-semibold bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all duration-200 rounded-lg flex items-center justify-center"
                                disabled={isLoading}
                            >
                                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                                </svg>
                                Sign in with {ssoProviderName}
                            </button>
                        </div>
                    )}

                    {/* Footer */}
                    <div className="pt-6 border-t border-gray-200 dark:border-gray-800">
                        <p className="text-xs text-center text-gray-500 dark:text-gray-400">
                            {mode === 'sso' || mode === 'both'
                                ? 'Access restricted to authorized users only'
                                : 'Secure authentication powered by BizOSaaS'}
                        </p>
                    </div>
                </div>

                {/* Signup CTA */}
                <div className="mt-6 space-y-3">
                    <div className="relative">
                        <div className="absolute inset-0 flex items-center">
                            <div className="w-full border-t border-gray-300 dark:border-gray-700"></div>
                        </div>
                        <div className="relative flex justify-center text-xs">
                            <span className="px-2 bg-white dark:bg-gray-900 text-gray-500">New to BizOSaaS?</span>
                        </div>
                    </div>

                    <a
                        href="/signup"
                        className="block w-full py-3 px-4 bg-white dark:bg-gray-800 border-2 border-blue-600 dark:border-blue-500 text-blue-600 dark:text-blue-400 font-semibold rounded-lg hover:bg-blue-50 dark:hover:bg-gray-700 transition-all duration-200 text-center"
                    >
                        Create New Account
                    </a>

                    <p className="text-xs text-center text-gray-500 dark:text-gray-500">
                        Having trouble?{' '}
                        <a href="mailto:support@bizosaas.com" className="text-blue-600 dark:text-blue-400 hover:underline">
                            Contact Support
                        </a>
                    </p>
                </div>
            </div>
        </div>
    )
}

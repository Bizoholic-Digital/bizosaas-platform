'use client'

import React, { useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Eye, EyeOff, Mail, Lock, ArrowRight, Shield } from 'lucide-react'

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
                        {BrandingComponent ? (
                            <div className="flex justify-center">
                                <BrandingComponent />
                            </div>
                        ) : (
                            <div className="flex flex-col items-center">
                                <div className="w-16 h-16 bg-gradient-to-tr from-blue-600 to-purple-600 rounded-2xl shadow-xl flex items-center justify-center mb-4 transform -rotate-6">
                                    <span className="text-2xl font-black text-white">BH</span>
                                </div>
                                <h1 className="text-xl font-bold tracking-tight text-slate-900 dark:text-white">
                                    BIZOSaaS Platform
                                </h1>
                            </div>
                        )}
                        <div>
                            <h2 className="text-3xl font-bold text-gray-900 dark:text-white tracking-tight">
                                {platformName}
                            </h2>
                            {platformSubtitle && (
                                <p className="mt-2 text-sm text-gray-600 dark:text-gray-400 font-medium">
                                    {platformSubtitle}
                                </p>
                            )}
                        </div>
                    </div>

                    {/* Error Message */}
                    {error && (
                        <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 rounded-r-lg p-4 animate-in fade-in slide-in-from-top-1">
                            <p className="text-sm text-red-700 dark:text-red-400 font-medium">{error}</p>
                        </div>
                    )}

                    {/* Credentials Form */}
                    {(mode === 'credentials' || mode === 'both') && (
                        <form onSubmit={handleCredentialsSubmit} className="space-y-5">
                            <div className="space-y-2">
                                <label htmlFor="email" className="text-sm font-semibold text-gray-700 dark:text-gray-300 ml-1">
                                    Email address
                                </label>
                                <div className="relative group">
                                    <Mail className="absolute left-3 top-3.5 h-4 w-4 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
                                    <input
                                        id="email"
                                        type="email"
                                        placeholder="Enter your email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="w-full pl-10 pr-4 py-3 border border-gray-200 dark:border-gray-800 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 dark:bg-gray-800/50 dark:text-white transition-all outline-none"
                                        required
                                        disabled={isLoading}
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <label htmlFor="password" className="text-sm font-semibold text-gray-700 dark:text-gray-300 ml-1">
                                    Password
                                </label>
                                <div className="relative group">
                                    <Lock className="absolute left-3 top-3.5 h-4 w-4 text-gray-400 group-focus-within:text-blue-500 transition-colors" />
                                    <input
                                        id="password"
                                        type={showPassword ? 'text' : 'password'}
                                        placeholder="Enter your password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        className="w-full pl-10 pr-12 py-3 border border-gray-200 dark:border-gray-800 rounded-xl focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 dark:bg-gray-800/50 dark:text-white transition-all outline-none"
                                        required
                                        disabled={isLoading}
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        className="absolute right-3 top-3.5 text-gray-400 hover:text-gray-600 transition-colors"
                                        disabled={isLoading}
                                    >
                                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                    </button>
                                </div>
                            </div>

                            <div className="flex items-center justify-between px-1">
                                <div className="flex items-center">
                                    <input
                                        id="remember"
                                        type="checkbox"
                                        checked={rememberMe}
                                        onChange={(e) => setRememberMe(e.target.checked)}
                                        className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 transition-all cursor-pointer"
                                        disabled={isLoading}
                                    />
                                    <label htmlFor="remember" className="ml-2 text-sm text-gray-600 dark:text-gray-400 cursor-pointer">
                                        Remember me
                                    </label>
                                </div>
                                <a href="#" className="text-sm font-semibold text-blue-600 hover:text-blue-700 dark:text-blue-400">
                                    Forgot password?
                                </a>
                            </div>

                            <button
                                type="submit"
                                className="w-full py-3.5 px-4 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 hover:from-blue-700 hover:via-indigo-700 hover:to-purple-700 text-white font-bold rounded-xl shadow-lg shadow-blue-500/20 hover:shadow-xl hover:shadow-blue-500/30 transform hover:-translate-y-0.5 transition-all duration-200 flex items-center justify-center border border-white/10"
                                disabled={isLoading}
                            >
                                {isLoading ? (
                                    <>
                                        <div className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent mr-2" />
                                        Authenticating...
                                    </>
                                ) : (
                                    <>
                                        Sign In
                                        <ArrowRight className="ml-2 h-4 w-4" />
                                    </>
                                )}
                            </button>

                            {showDemoCredentials && (
                                <div className="mt-4 p-4 bg-blue-50/50 dark:bg-blue-900/20 rounded-xl border border-blue-100 dark:border-blue-900/30 backdrop-blur-sm">
                                    <p className="text-xs text-blue-800 dark:text-blue-300 leading-relaxed">
                                        <span className="font-bold flex items-center mb-1">
                                            <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mr-2"></span>
                                            Demo Credentials
                                        </span>
                                        Email: admin@bizoholic.com<br />
                                        Password: AdminDemo2024!
                                    </p>
                                </div>
                            )}
                        </form>
                    )}

                    {/* Divider for 'both' mode */}
                    {mode === 'both' && (
                        <div className="relative py-2">
                            <div className="absolute inset-0 flex items-center">
                                <div className="w-full border-t border-gray-100 dark:border-gray-800"></div>
                            </div>
                            <div className="relative flex justify-center text-xs uppercase tracking-widest font-bold">
                                <span className="px-4 bg-white dark:bg-gray-900 text-gray-400">Or Secure SSO</span>
                            </div>
                        </div>
                    )}

                    {/* SSO Button */}
                    {(mode === 'sso' || mode === 'both') && (
                        <div className="space-y-4">
                            <button
                                type="button"
                                onClick={handleSSOLogin}
                                className="w-full py-3.5 px-4 bg-slate-950 hover:bg-slate-900 dark:bg-white dark:hover:bg-slate-100 text-white dark:text-slate-950 font-bold rounded-xl shadow-lg transform hover:-translate-y-0.5 transition-all duration-200 flex items-center justify-center border border-slate-800 dark:border-slate-200"
                                disabled={isLoading}
                            >
                                <Shield className="w-5 h-5 mr-3 text-blue-500" />
                                Sign in with {ssoProviderName}
                            </button>
                        </div>
                    )}

                    {/* Footer */}
                    <div className="pt-6 border-t border-gray-50 dark:border-gray-801">
                        <p className="text-[10px] text-center text-gray-400 dark:text-gray-500 uppercase tracking-widest font-bold font-sans">
                            {mode === 'sso' || mode === 'both'
                                ? 'Strictly Restricted Access • BizOSaaS 2024'
                                : 'Enterprise Grade Security • Powered by BizOSaaS'}
                        </p>
                    </div>
                </div>

                {/* Bottom Links */}
                <div className="mt-8 text-center space-y-4">
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                        Don't have an account?{' '}
                        <a href="/signup" className="font-bold text-blue-600 hover:text-blue-700 dark:text-blue-400">
                            Get Started
                        </a>
                    </p>
                    <div className="flex justify-center space-x-4 text-xs font-semibold text-gray-400">
                        <a href="#" className="hover:text-gray-600">Privacy Policy</a>
                        <span>•</span>
                        <a href="#" className="hover:text-gray-600">Terms of Service</a>
                        <span>•</span>
                        <a href="mailto:support@bizosaas.com" className="hover:text-gray-600 font-bold text-slate-500">Contact Support</a>
                    </div>
                </div>
            </div>
        </div>
    )
}

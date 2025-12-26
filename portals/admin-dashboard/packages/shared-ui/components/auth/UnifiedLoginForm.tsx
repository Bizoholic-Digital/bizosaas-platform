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

    /** Custom CSS classes */
    className?: string

    /** Show demo credentials (for development) */
    showDemoCredentials?: boolean

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
    className = '',
    showDemoCredentials = false,
    onCredentialsLogin,
    onSSOLogin,
}: UnifiedLoginFormProps) {
    const [email, setEmail] = useState(showDemoCredentials ? 'admin@bizoholic.net' : '')
    const [password, setPassword] = useState(showDemoCredentials ? 'admin123' : '')
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
                    window.location.href = callbackUrl
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
        <div className={`min-h-screen flex items-center justify-center p-4 ${className}`}>
            <div className="max-w-md w-full">
                <div className="bg-white dark:bg-slate-900 rounded-[2.5rem] shadow-2xl p-8 md:p-12 space-y-8 border border-slate-100 dark:border-slate-800">
                    {/* Header */}
                    <div className="text-center space-y-6">
                        <div className="flex flex-col items-center">
                            <div className="w-16 h-16 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-2xl shadow-xl flex items-center justify-center mb-6 transform -rotate-12 hover:rotate-0 transition-transform duration-300">
                                <span className="text-2xl font-black text-white tracking-tighter">BH</span>
                            </div>
                            <h1 className="text-xs font-black uppercase tracking-[0.35em] text-blue-600 dark:text-blue-400 mb-2">
                                BIZOSaaS Platform
                            </h1>
                            <h2 className="text-4xl font-black text-slate-900 dark:text-white tracking-tighter leading-none">
                                {platformName}
                            </h2>
                            {platformSubtitle && (
                                <p className="mt-4 text-sm text-slate-500 dark:text-slate-400 font-medium leading-relaxed">
                                    {platformSubtitle}
                                </p>
                            )}
                        </div>
                    </div>

                    {/* Error Message */}
                    {error && (
                        <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 rounded-r-xl p-4 animate-in fade-in slide-in-from-top-1">
                            <p className="text-sm text-red-700 dark:text-red-300 font-bold">{error}</p>
                        </div>
                    )}

                    {/* Form */}
                    {(mode === 'credentials' || mode === 'both') && (
                        <form onSubmit={handleCredentialsSubmit} className="space-y-6">
                            <div className="space-y-2">
                                <label htmlFor="email" className="text-xs font-black uppercase tracking-widest text-slate-500 dark:text-slate-400 ml-1">
                                    Email address
                                </label>
                                <div className="relative group">
                                    <div className="absolute left-4 top-1/2 -translate-y-1/2 flex items-center justify-center pointer-events-none z-10">
                                        <Mail className="h-5 w-5 text-slate-400 group-focus-within:text-blue-500 transition-colors" />
                                    </div>
                                    <input
                                        id="email"
                                        type="email"
                                        placeholder="Enter your email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        className="w-full pl-12 pr-4 py-4 bg-slate-50 dark:bg-slate-800/50 border border-transparent focus:border-blue-500 rounded-2xl focus:ring-4 focus:ring-blue-500/10 dark:text-white transition-all outline-none text-base font-medium"
                                        required
                                        disabled={isLoading}
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <label htmlFor="password" className="text-xs font-black uppercase tracking-widest text-slate-500 dark:text-slate-400 ml-1">
                                    Password
                                </label>
                                <div className="relative group">
                                    <div className="absolute left-4 top-1/2 -translate-y-1/2 flex items-center justify-center pointer-events-none z-10">
                                        <Lock className="h-5 w-5 text-slate-400 group-focus-within:text-blue-500 transition-colors" />
                                    </div>
                                    <input
                                        id="password"
                                        type={showPassword ? 'text' : 'password'}
                                        placeholder="Enter your password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        className="w-full pl-12 pr-14 py-4 bg-slate-50 dark:bg-slate-800/50 border border-transparent focus:border-blue-500 rounded-2xl focus:ring-4 focus:ring-blue-500/10 dark:text-white transition-all outline-none text-base font-medium"
                                        required
                                        disabled={isLoading}
                                    />
                                    <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center justify-center z-10">
                                        <button
                                            type="button"
                                            onClick={() => setShowPassword(!showPassword)}
                                            className="p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors rounded-lg hover:bg-white dark:hover:bg-slate-700 shadow-sm border border-transparent hover:border-slate-100 dark:hover:border-slate-600"
                                            disabled={isLoading}
                                        >
                                            {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div className="flex items-center justify-between px-1">
                                <div className="flex items-center">
                                    <input
                                        id="remember"
                                        type="checkbox"
                                        checked={rememberMe}
                                        onChange={(e) => setRememberMe(e.target.checked)}
                                        className="h-4 w-4 text-blue-600 border-slate-300 rounded focus:ring-blue-500 transition-all cursor-pointer"
                                        disabled={isLoading}
                                    />
                                    <label htmlFor="remember" className="ml-2 text-sm text-slate-600 dark:text-slate-400 font-bold cursor-pointer">
                                        Remember me
                                    </label>
                                </div>
                                <a href="#" className="text-sm font-black text-blue-600 hover:text-blue-700 dark:text-blue-400">
                                    Forgot password?
                                </a>
                            </div>

                            <button
                                type="submit"
                                className="w-full py-4 px-6 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-black rounded-2xl shadow-xl shadow-blue-500/20 hover:shadow-2xl hover:shadow-blue-500/30 transform hover:-translate-y-0.5 transition-all duration-300 flex items-center justify-center text-lg active:scale-[0.98]"
                                disabled={isLoading}
                            >
                                {isLoading ? (
                                    <div className="h-6 w-6 animate-spin rounded-full border-3 border-white border-t-transparent" />
                                ) : (
                                    <>
                                        Sign In
                                        <ArrowRight className="ml-2 h-5 w-5" />
                                    </>
                                )}
                            </button>
                        </form>
                    )}

                    {/* Divider */}
                    {mode === 'both' && (
                        <div className="relative py-4">
                            <div className="absolute inset-0 flex items-center">
                                <div className="w-full border-t border-slate-100 dark:border-slate-800"></div>
                            </div>
                            <div className="relative flex justify-center text-[10px] uppercase tracking-[0.4em] font-black">
                                <span className="px-6 bg-white dark:bg-slate-900 text-slate-400">OR SECURE SSO</span>
                            </div>
                        </div>
                    )}

                    {/* SSO Button */}
                    {(mode === 'sso' || mode === 'both') && (
                        <button
                            type="button"
                            onClick={handleSSOLogin}
                            className="w-full py-4 px-6 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-900 dark:text-white font-black rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700 transform hover:-translate-y-0.5 transition-all duration-300 flex items-center justify-center group active:scale-[0.98]"
                            disabled={isLoading}
                        >
                            <Shield className="w-6 h-6 mr-3 text-blue-500 group-hover:scale-110 transition-transform" />
                            Sign in with {ssoProviderName}
                        </button>
                    )}

                    {/* Footer */}
                    <div className="pt-8 border-t border-slate-50 dark:border-slate-800">
                        <p className="text-[10px] text-center text-slate-400 dark:text-slate-500 uppercase tracking-[0.25em] font-black leading-relaxed">
                            {mode === 'both' || mode === 'sso'
                                ? 'Strictly Restricted Access • BizOSaaS 2024'
                                : 'Enterprise Grade Security • Powered by BizOSaaS'}
                        </p>
                    </div>
                </div>

                {/* Bottom Links */}
                <div className="mt-10 text-center space-y-6">
                    <p className="text-sm text-slate-500 dark:text-slate-400 font-bold">
                        Don't have an account?{' '}
                        <a href="#" className="text-blue-600 hover:text-blue-700 dark:text-blue-400 underline decoration-2 underline-offset-4">
                            Get Started
                        </a>
                    </p>
                    <div className="flex flex-wrap justify-center gap-x-6 gap-y-2 text-[10px] font-black uppercase tracking-widest text-slate-400">
                        <a href="#" className="hover:text-slate-600 dark:hover:text-slate-200 transition-colors">Privacy</a>
                        <a href="#" className="hover:text-slate-600 dark:hover:text-slate-200 transition-colors">Terms</a>
                        <a href="#" className="hover:text-slate-600 dark:hover:text-slate-200 transition-colors">Support</a>
                    </div>
                </div>
            </div>
        </div>
    )
}

'use client';

import React, { useState, Suspense } from 'react';
import { signIn } from 'next-auth/react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Lock, Mail, Shield, Zap, Layout, Server, Gauge, Chrome } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';

function AdminLoginFormContent() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const router = useRouter();
    const searchParams = useSearchParams();
    const callbackUrl = searchParams?.get('callbackUrl') || '/dashboard';

    const handleCredentialsLogin = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            const result = await signIn('credentials', {
                email,
                password,
                redirect: false,
                callbackUrl,
            });

            if (result?.error) {
                console.error("Admin Login Error:", result.error);
                setError(`Login failed: ${result.error === 'CredentialsSignin' ? 'Invalid admin credentials' : result.error}`);
            } else if (result?.ok) {
                window.location.href = callbackUrl;
            } else {
                setError('Login failed. Please try again.');
            }
        } catch (err) {
            setError('An error occurred during authentication.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleSSOLogin = async () => {
        setIsLoading(true);
        try {
            await signIn('authentik', { callbackUrl });
        } catch (err) {
            setError('SSO login failed. Please try again.');
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col space-y-6">
            <Card className="w-full max-w-md shadow-2xl border-slate-200 dark:border-slate-800">
                <CardHeader className="text-center space-y-4 pb-4">
                    <div className="mx-auto h-16 w-16 flex items-center justify-center rounded-xl bg-slate-950 text-white shadow-lg">
                        <Shield className="h-8 w-8 text-blue-400" />
                    </div>

                    <div>
                        <CardTitle className="text-2xl font-bold tracking-tight">Admin Dashboard</CardTitle>
                        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">BizOSaaS Platform Management</p>
                    </div>
                </CardHeader>

                <CardContent className="space-y-6">
                    {/* Social SSO Options */}
                    <div className="grid grid-cols-2 gap-4">
                        <Button
                            variant="outline"
                            onClick={() => signIn('google', { callbackUrl })}
                            disabled={isLoading}
                            className="h-12 border-slate-200 hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-900 transition-all flex items-center justify-center gap-2"
                        >
                            <Chrome className="h-5 w-5 text-red-500" />
                            <span className="font-medium">Google</span>
                        </Button>
                        <Button
                            variant="outline"
                            onClick={handleSSOLogin}
                            disabled={isLoading}
                            className="h-12 border-slate-200 hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-900 transition-all flex items-center justify-center gap-2"
                        >
                            <Shield className="h-5 w-5 text-blue-500" />
                            <span className="font-medium">BizOSaaS SSO</span>
                        </Button>
                    </div>

                    <div className="relative">
                        <div className="absolute inset-0 flex items-center">
                            <Separator />
                        </div>
                        <div className="relative flex justify-center text-xs uppercase">
                            <span className="bg-white dark:bg-slate-950 px-2 text-slate-500">
                                Or use credentials
                            </span>
                        </div>
                    </div>

                    {/* Email/Password Form */}
                    <form onSubmit={handleCredentialsLogin} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="email">Admin Email</Label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                                <Input
                                    id="email"
                                    type="email"
                                    placeholder="admin@bizoholic.com"
                                    value={email}
                                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
                                    className="pl-10 h-11"
                                    required
                                    disabled={isLoading}
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="password">Password</Label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-3 h-4 w-4 text-slate-400" />
                                <Input
                                    id="password"
                                    type="password"
                                    placeholder="Enter your password"
                                    value={password}
                                    onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
                                    className="pl-10 h-11"
                                    required
                                    disabled={isLoading}
                                />
                            </div>
                        </div>

                        {error && (
                            <div className="rounded-lg bg-red-50 dark:bg-red-900/20 p-3 border border-red-100 dark:border-red-900/30">
                                <p className="text-sm text-red-700 dark:text-red-300 font-medium">{error}</p>
                            </div>
                        )}

                        <Button
                            type="submit"
                            className="w-full h-11 bg-slate-900 hover:bg-slate-800 dark:bg-blue-600 dark:hover:bg-blue-700 text-white font-semibold transition-all shadow-md"
                            disabled={isLoading}
                        >
                            {isLoading ? (
                                <div className="flex items-center gap-2">
                                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                    <span>Authenticating...</span>
                                </div>
                            ) : (
                                'Access System Dashboard'
                            )}
                        </Button>
                    </form>

                    {/* Quick Stats Footer */}
                    <div className="grid grid-cols-3 gap-2 pt-4 border-t border-slate-100 dark:border-slate-800">
                        <div className="flex flex-col items-center p-2 rounded-lg bg-slate-50 dark:bg-slate-900/50">
                            <Server className="h-4 w-4 text-blue-500 mb-1" />
                            <span className="text-[10px] font-medium text-slate-500 uppercase">Gateway</span>
                            <span className="text-[10px] font-bold text-green-500">Active</span>
                        </div>
                        <div className="flex flex-col items-center p-2 rounded-lg bg-slate-50 dark:bg-slate-900/50">
                            <Layout className="h-4 w-4 text-purple-500 mb-1" />
                            <span className="text-[10px] font-medium text-slate-500 uppercase">Portals</span>
                            <span className="text-[10px] font-bold text-blue-500">6 Live</span>
                        </div>
                        <div className="flex flex-col items-center p-2 rounded-lg bg-slate-50 dark:bg-slate-900/50">
                            <Gauge className="h-4 w-4 text-amber-500 mb-1" />
                            <span className="text-[10px] font-medium text-slate-500 uppercase">System</span>
                            <span className="text-[10px] font-bold text-blue-500">99.9%</span>
                        </div>
                    </div>
                </CardContent>
            </Card>

            <p className="text-center text-xs text-slate-400">
                Secure Access Gate • BizOSaaS Architecture v4.2
            </p>
        </div>
    );
}

export default function AdminLoginForm() {
    return (
        <Suspense fallback={<div className="flex items-center justify-center p-8">Loading Security Interface...</div>}>
            <AdminLoginFormContent />
        </Suspense>
    );
}

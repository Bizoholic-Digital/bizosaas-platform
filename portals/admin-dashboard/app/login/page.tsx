'use client'

import React, { Suspense } from 'react'
import { signIn } from 'next-auth/react'
import { ThemeToggle } from '@/components/theme-toggle'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import { ShieldCheck, Github, Chrome } from 'lucide-react'

function LoginForm() {
  const handleLogin = (provider: string = 'authentik') => {
    signIn('authentik', { callbackUrl: '/dashboard' })
  }

  return (
    <Card className="w-[420px] shadow-2xl bg-white/70 dark:bg-black/70 backdrop-blur-md border-0 ring-1 ring-white/20">
      <CardHeader className="space-y-1 text-center pb-8">
        <div className="flex justify-center mb-6">
          <div className="p-4 bg-gradient-to-tr from-red-600 to-orange-500 rounded-2xl shadow-lg ring-4 ring-red-500/20">
            <ShieldCheck className="w-8 h-8 text-white" />
          </div>
        </div>
        <CardTitle className="text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-500 dark:from-white dark:to-gray-400">
          Admin Control Center
        </CardTitle>
        <CardDescription className="text-base font-medium">
          Authorized personnel only. Sessions are audited.
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-6">
        <div className="grid grid-cols-2 gap-4">
          <Button
            variant="outline"
            className="flex items-center justify-center gap-2 h-12 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-900 transition-all active:scale-95"
            onClick={() => handleLogin()}
          >
            <Chrome className="w-5 h-5 text-red-500" />
            <span className="font-semibold">Google</span>
          </Button>
          <Button
            variant="outline"
            className="flex items-center justify-center gap-2 h-12 border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-900 transition-all active:scale-95"
            onClick={() => handleLogin()}
          >
            <Github className="w-5 h-5" />
            <span className="font-semibold">GitHub</span>
          </Button>
        </div>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-slate-200 dark:border-slate-800" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-white/0 px-2 text-muted-foreground backdrop-blur-none bg-inherit">
              Standard Authentication
            </span>
          </div>
        </div>

        <Button
          className="w-full text-lg font-bold h-14 bg-gradient-to-r from-red-600 to-red-800 hover:from-red-700 hover:to-red-900 shadow-xl transition-all hover:scale-[1.02] active:scale-[0.98]"
          size="lg"
          onClick={() => handleLogin()}
        >
          Sign in via Secure SSO
        </Button>
      </CardContent>
      <CardFooter className="flex flex-col space-y-2 pt-4 text-center text-sm text-muted-foreground italic">
        <p>Locked by BizOSaaS Security Core</p>
      </CardFooter>
    </Card>
  )
}

export default function AdminLoginPage() {
  return (
    <div className="relative min-h-screen w-full overflow-hidden flex items-center justify-center p-4">
      {/* Heavy Duty Background for Admin */}
      <div className="fixed inset-0 bg-slate-100 dark:bg-slate-950 -z-20" />
      <div className="fixed inset-0 -z-10">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-red-500/5 via-transparent to-transparent opacity-50" />
        <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-red-600/5 rounded-full blur-[150px]" />
        <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-slate-600/5 rounded-full blur-[150px]" />
      </div>

      <div className="absolute top-8 right-8 z-50">
        <ThemeToggle />
      </div>

      <div className="z-10 w-full max-w-[420px]" data-testid="login-form">
        <Suspense fallback={
          <div className="flex flex-col items-center gap-4">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-4 border-red-600"></div>
            <p className="text-sm font-bold tracking-widest uppercase animate-pulse">Establishing Secure Link...</p>
          </div>
        }>
          <LoginForm />
        </Suspense>
      </div>
    </div>
  )
}
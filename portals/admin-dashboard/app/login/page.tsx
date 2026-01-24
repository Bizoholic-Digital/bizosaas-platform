'use client'

import React, { Suspense } from 'react'
import { signIn } from 'next-auth/react'
import { ThemeToggle } from '@/components/theme-toggle'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card'
import { ShieldCheck } from 'lucide-react'

function LoginForm() {
  const handleLogin = () => {
    signIn('authentik', { callbackUrl: '/dashboard' })
  }

  return (
    <Card className="w-[400px] shadow-2xl bg-white/80 dark:bg-black/80 backdrop-blur-sm border-0">
      <CardHeader className="space-y-1 text-center">
        <div className="flex justify-center mb-4">
          <div className="p-3 bg-red-100 dark:bg-red-900/30 rounded-full">
            <ShieldCheck className="w-8 h-8 text-red-600 dark:text-red-400" />
          </div>
        </div>
        <CardTitle className="text-2xl font-bold tracking-tight">Admin Portal</CardTitle>
        <CardDescription>
          Authorized personnel only. All actions are logged.
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4">
        <Button
          className="w-full text-lg h-12 transition-all hover:scale-[1.02] bg-red-600 hover:bg-red-700"
          size="lg"
          onClick={handleLogin}
        >
          Sign in with Authentik
        </Button>
      </CardContent>
      <CardFooter className="flex flex-col space-y-2 text-center text-sm text-muted-foreground">
        <div>
          Restricted Access System
        </div>
      </CardFooter>
    </Card>
  )
}

export default function AdminLoginPage() {
  return (
    <div className="relative min-h-screen w-full overflow-hidden flex items-center justify-center">
      {/* Animated Gradient Background - Full Page */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-red-50 to-orange-50 dark:from-slate-950 dark:via-red-950 dark:to-orange-950 -z-10">
        <div className="absolute top-0 -left-4 w-72 h-72 bg-purple-300 dark:bg-purple-900 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute top-0 -right-4 w-72 h-72 bg-yellow-300 dark:bg-yellow-900 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-red-300 dark:bg-red-900 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <div className="absolute top-6 right-6 z-50 flex items-center gap-4">
        <ThemeToggle />
      </div>

      <div className="z-10" data-testid="login-form">
        <Suspense fallback={<div className="min-h-screen flex items-center justify-center"><div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div></div>}>
          <LoginForm />
        </Suspense>
      </div>

      <style jsx global>{`
        @keyframes blob {
          0% { transform: translate(0px, 0px) scale(1); }
          33% { transform: translate(30px, -50px) scale(1.1); }
          66% { transform: translate(-20px, 20px) scale(0.9); }
          100% { transform: translate(0px, 0px) scale(1); }
        }
        .animate-blob { animation: blob 7s infinite; }
        .animation-delay-2000 { animation-delay: 2s; }
        .animation-delay-4000 { animation-delay: 4s; }
      `}</style>
    </div>
  )
}
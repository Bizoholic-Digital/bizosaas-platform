'use client'
import { SignIn } from '@clerk/nextjs'
import { ThemeToggle } from '@/components/theme-toggle'

export default function AdminLoginPage() {
  console.log('AdminLoginPage rendering');
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-red-500/10">
      <div className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow-xl">
        <h1 className="text-2xl font-bold mb-4">Admin Login</h1>
        <div className="mb-4">
          <ThemeToggle />
        </div>
        <div className="debug-info mb-4 text-xs text-red-500">
          Domain: {typeof window !== 'undefined' ? window.location.hostname : 'ssr'}
        </div>
        <SignIn routing="path" path="/login" />
      </div>
    </div>
  )
}
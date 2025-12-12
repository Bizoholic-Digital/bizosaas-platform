import { ClientLoginForm } from './ClientLoginForm'
import { ThemeToggle } from '@/components/theme-toggle'
import { Suspense } from 'react'

export default function LoginPage() {
  return (
    <div className="relative min-h-screen flex items-center justify-center p-4 bg-gray-50 dark:bg-gray-900">
      <div className="absolute top-4 right-4 z-10">
        <ThemeToggle />
      </div>
      <div className="w-full max-w-md">
        <Suspense fallback={<div className="flex justify-center items-center">Loading...</div>}>
          <ClientLoginForm />
        </Suspense>
      </div>
    </div>
  )
}
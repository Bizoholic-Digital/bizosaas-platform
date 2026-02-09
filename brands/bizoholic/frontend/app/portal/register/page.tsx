import { RegisterForm } from '@/components/auth/register-form'
import Link from 'next/link'
import Image from 'next/image'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'

export default function PortalRegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 px-4">
      <div className="w-full max-w-md space-y-6">
        {/* Brand Logo & Welcome */}
        <div className="text-center space-y-4">
          <div className="flex justify-center">
            <Image
              src="/bizoholic-logo-hq.png"
              alt="Bizoholic Digital"
              width={240}
              height={60}
              className="h-12 w-auto"
              priority
            />
          </div>
          <h1 className="text-3xl font-bold">Create Your Account</h1>
          <p className="text-muted-foreground">
            Join Bizoholic and unlock AI-powered marketing tools
          </p>
        </div>

        <Card className="shadow-xl">
          <CardContent className="p-6 space-y-6">
            {/* Registration Form */}
            <RegisterForm />

            <div className="text-center">
              <p className="text-sm text-muted-foreground">
                Already have an account?{' '}
                <Link href="/portal/login" className="text-primary hover:underline font-medium">
                  Sign in
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>

        <p className="text-center text-xs text-muted-foreground">
          By continuing, you agree to our{' '}
          <Link href="/terms" className="underline hover:text-primary">Terms of Service</Link>
          {' '}and{' '}
          <Link href="/privacy" className="underline hover:text-primary">Privacy Policy</Link>
        </p>
      </div>
    </div>
  )
}

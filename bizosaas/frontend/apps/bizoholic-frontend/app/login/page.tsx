import { LoginForm } from '@/components/auth/login-form'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { Card, CardContent } from '@/components/ui/card'
import { Github, Mail } from 'lucide-react'

export default function LoginPage() {
  return (
    <div className="space-y-6">
      <div className="text-center space-y-2">
        <h1 className="text-2xl font-bold">Welcome back</h1>
        <p className="text-muted-foreground">
          Access your AI-powered marketing platform with 28+ autonomous agents
        </p>
      </div>

      {/* Demo Credentials Helper */}
      <Card className="bg-blue-50 dark:bg-blue-950 border-blue-200 dark:border-blue-800">
        <CardContent className="p-4">
          <h3 className="font-semibold text-blue-800 dark:text-blue-200 mb-2">Demo Credentials</h3>
          <div className="text-sm text-blue-700 dark:text-blue-300 space-y-1">
            <div><strong>Client:</strong> client@bizosaas.com / ClientDemo2024!</div>
            <div><strong>Admin:</strong> admin@bizoholic.com / AdminDemo2024!</div>
            <div><strong>Seller:</strong> seller@coreldove.com / SellerDemo2024!</div>
            <div><strong>Marketplace Admin:</strong> admin@coreldove.com / MarketplaceAdmin2024!</div>
          </div>
        </CardContent>
      </Card>

      {/* Social Login */}
      <div className="grid grid-cols-2 gap-3">
        <Button variant="outline" className="w-full" disabled>
          <Github className="h-4 w-4 mr-2" />
          GitHub
        </Button>
        <Button variant="outline" className="w-full" disabled>
          <Mail className="h-4 w-4 mr-2" />
          Google
        </Button>
      </div>

      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <Separator className="w-full" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-2 text-muted-foreground">Or continue with email</span>
        </div>
      </div>

      {/* Login Form with Demo Credentials */}
      <LoginForm />

      <div className="text-center">
        <p className="text-sm text-muted-foreground">
          Don't have an account?{' '}
          <Link href="/auth/register" className="text-primary hover:underline font-medium">
            Sign up for free
          </Link>
        </p>
      </div>
    </div>
  )
}
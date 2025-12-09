'use client';

import { useState, useEffect, Suspense } from 'react';
import { signIn } from 'next-auth/react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Github, Layout, Lock, Mail, Mail as Google } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';

// Brand configuration
const BRANDS = {
  bizoholic: {
    name: 'Bizoholic Digital',
    tagline: 'Digital Marketing Excellence',
    primaryColor: '#2563eb',
  },
  coreldove: {
    name: 'CoreLDove',
    tagline: 'E-commerce Made Simple',
    primaryColor: '#dc2626',
  },
  thrillring: {
    name: 'ThrillRing',
    tagline: 'Entertainment & Events',
    primaryColor: '#7c3aed',
  },
  quanttrade: {
    name: 'QuantTrade',
    tagline: 'Algorithmic Trading Platform',
    primaryColor: '#059669',
  },
  'business-directory': {
    name: 'Business Directory',
    tagline: 'Connect Local Businesses',
    primaryColor: '#ea580c',
  },
} as const;

type Brand = keyof typeof BRANDS;

function LoginContent() {
  const [brand, setBrand] = useState<Brand>('bizoholic');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const router = useRouter();
  const searchParams = useSearchParams();

  // Detect brand from URL or localStorage
  useEffect(() => {
    const brandParam = searchParams?.get('brand') as Brand;
    const storedBrand = (typeof window !== 'undefined' ? localStorage.getItem('selected_brand') : null) as Brand;

    if (brandParam && BRANDS[brandParam]) {
      setBrand(brandParam);
      if (typeof window !== 'undefined') {
        localStorage.setItem('selected_brand', brandParam);
      }
    } else if (storedBrand && BRANDS[storedBrand]) {
      setBrand(storedBrand);
    }
  }, [searchParams]);

  const handleCredentialsLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      console.log('Attempting login with:', { email, brand });
      const result = await signIn('credentials', {
        email,
        password,
        brand,
        redirect: false,
        callbackUrl: '/onboarding',
      });

      console.log('Login result:', result);

      if (result?.error) {
        console.error('Login error:', result.error);
        setError('Invalid credentials. Please check your email and password.');
      } else if (result?.ok) {
        console.log('Login successful, redirecting to onboarding');
        // Use window.location for a hard redirect to ensure clean state
        window.location.href = '/onboarding';
      } else {
        setError('Login failed. Please try again.');
      }
    } catch (err) {
      console.error('Login exception:', err);
      setError('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAuthentikLogin = async () => {
    setIsLoading(true);
    setError('');

    try {
      await signIn('authentik', {
        callbackUrl: '/onboarding',
        redirect: true,
      });
    } catch (err) {
      setError('SSO login failed. Please try again.');
      setIsLoading(false);
    }
  };

  const brandConfig = BRANDS[brand];

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 px-4 py-12">
      <Card className="w-full max-w-md shadow-2xl">
        <CardHeader className="text-center space-y-4 pb-4">
          {/* Brand Logo - Bizoholic Exclusive */}
          <div className="mx-auto h-20 w-20 flex items-center justify-center rounded-2xl transition-all shadow-lg bg-blue-600 text-white mb-2">
            <span className="text-4xl font-bold">B</span>
          </div>

          <div>
            <CardTitle className="text-2xl font-bold text-gray-900 dark:text-white">Bizoholic Digital</CardTitle>
            <p className="text-sm text-muted-foreground mt-2">Unified Enterprise SaaS Platform</p>
          </div>
        </CardHeader>

        <CardContent className="space-y-6 pt-2">
          {/* Authentik SSO Login */}
          <Button
            type="button"
            variant="default"
            onClick={handleAuthentikLogin}
            disabled={isLoading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white"
            size="lg"
          >
            <Lock className="h-5 w-5 mr-2" />
            Sign in with BizOSaaS SSO
          </Button>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <Separator />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-white dark:bg-gray-950 px-2 text-muted-foreground">
                Or continue with email
              </span>
            </div>
          </div>

          {/* Email/Password Form */}
          <form onSubmit={handleCredentialsLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  id="email"
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-10"
                  required
                  disabled={isLoading}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-10"
                  required
                  disabled={isLoading}
                />
              </div>
            </div>

            {error && (
              <div className="rounded-md bg-red-50 dark:bg-red-900/20 p-3 border border-red-200 dark:border-red-800">
                <p className="text-sm text-red-800 dark:text-red-200">{error}</p>
              </div>
            )}

            <Button
              type="submit"
              className="w-full text-white font-medium"
              disabled={isLoading}
              style={{ backgroundColor: brandConfig.primaryColor }}
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Signing in...
                </>
              ) : (
                'Sign in to Dashboard'
              )}
            </Button>
          </form>

          {/* Demo Credentials */}
          <Card className="bg-blue-50 dark:bg-blue-950 border-blue-200 dark:border-blue-800">
            <CardContent className="p-3">
              <p className="text-xs font-semibold text-blue-800 dark:text-blue-200 mb-1">
                SSO Login Credentials
              </p>
              <div className="text-xs text-blue-700 dark:text-blue-300 space-y-1">
                <div><strong>Admin:</strong> akadmin / Admin@123</div>
                <div className="text-[10px] opacity-70">Use "Sign in with BizOSaaS SSO" button above</div>
              </div>
            </CardContent>
          </Card>

          {/* Port Info & Security */}
          <div className="text-center text-xs text-muted-foreground space-y-1">
            <p>🎯 Port 3003: Unified Dashboard</p>
            <p className="text-[10px] opacity-70 flex items-center justify-center gap-1">
              <Lock className="w-3 h-3" /> Secured by HashiCorp Vault. GDPR Compliant.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default function UnifiedLoginPage() {
  return (
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center">Loading...</div>}>
      <LoginContent />
    </Suspense>
  );
}
'use client';

import { useState, useEffect, Suspense } from 'react';
import { signIn } from 'next-auth/react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Github, Mail as Google, Lock, Mail } from 'lucide-react';
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

// Prevent static generation
export const dynamic = 'force-dynamic';

function LoginPageContent() {
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
        callbackUrl: '/',
      });

      console.log('Login result:', result);

      if (result?.error) {
        console.error('Login error:', result.error);
        setError('Invalid credentials. Please check your email and password.');
      } else if (result?.ok) {
        console.log('Login successful, redirecting to dashboard');
        // Use window.location for a hard redirect to ensure clean state
        window.location.href = '/';
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

  const handleSocialLogin = async (provider: 'github' | 'google') => {
    setIsLoading(true);
    setError('');

    try {
      await signIn(provider, {
        callbackUrl: '/',
        redirect: true,
      });
    } catch (err) {
      setError(`${provider} login failed. Please try again.`);
      setIsLoading(false);
    }
  };

  const brandConfig = BRANDS[brand];

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 px-4 py-12">
      <Card className="w-full max-w-md shadow-2xl">
        <CardHeader className="text-center space-y-4 pb-4">
          {/* Brand Logo */}
          <div className="mx-auto h-16 w-16 flex items-center justify-center rounded-full transition-all"
            style={{ backgroundColor: `${brandConfig.primaryColor}20` }}>
            <div className="text-3xl font-bold transition-all" style={{ color: brandConfig.primaryColor }}>
              {brandConfig.name.charAt(0)}
            </div>
          </div>

          <div>
            <CardTitle className="text-2xl font-bold">{brandConfig.name}</CardTitle>
            <p className="text-sm text-muted-foreground mt-1">{brandConfig.tagline}</p>
          </div>

          {/* Brand Switcher */}
          <div className="flex flex-wrap gap-2 justify-center pt-2">
            {Object.keys(BRANDS).map((b) => (
              <button
                key={b}
                onClick={() => {
                  setBrand(b as Brand);
                  if (typeof window !== 'undefined') {
                    localStorage.setItem('selected_brand', b);
                  }
                }}
                className={`px-3 py-1 text-xs rounded-full transition-all font-medium ${brand === b
                  ? 'text-white shadow-md'
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                  }`}
                style={brand === b ? { backgroundColor: brandConfig.primaryColor } : {}}
              >
                {BRANDS[b as Brand].name}
              </button>
            ))}
          </div>
        </CardHeader>

        <CardContent className="space-y-6 pt-2">
          {/* Social Login */}
          <div className="grid grid-cols-2 gap-3">
            <Button
              variant="outline"
              onClick={() => handleSocialLogin('github')}
              disabled={isLoading}
              className="w-full"
            >
              <Github className="h-4 w-4 mr-2" />
              GitHub
            </Button>
            <Button
              variant="outline"
              onClick={() => handleSocialLogin('google')}
              disabled={isLoading}
              className="w-full"
            >
              <Google className="h-4 w-4 mr-2" />
              Google
            </Button>
          </div>

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
                Demo Credentials
              </p>
              <div className="text-xs text-blue-700 dark:text-blue-300 space-y-1">
                <div><strong>Admin:</strong> admin@bizoholic.com / AdminDemo2024!</div>
                <div><strong>Client:</strong> client@bizosaas.com / ClientDemo2024!</div>
              </div>
            </CardContent>
          </Card>

          {/* Port Info */}
          <div className="text-center text-xs text-muted-foreground">
            <p>🎯 Port 3003: Unified Dashboard</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default function UnifiedLoginPage() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center h-screen">Loading login...</div>}>
      <LoginPageContent />
    </Suspense>
  );
}
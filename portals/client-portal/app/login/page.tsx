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
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 px-4 py-12">
      <Card className="w-full max-w-md shadow-2xl border-0 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
        <CardHeader className="text-center space-y-6 pb-6">
          {/* Brand Logo with subtle animation */}
          <div className="mx-auto flex items-center justify-center mb-2 transition-transform hover:scale-105 duration-300">
            <img
              src="/logo.png"
              alt="Bizoholic Digital"
              className="h-24 w-auto object-contain drop-shadow-lg"
            />
          </div>

          <div className="space-y-2">
            <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
              Welcome Back
            </CardTitle>
            <p className="text-sm text-muted-foreground">
              Sign in to access your enterprise dashboard
            </p>
          </div>
        </CardHeader>

        <CardContent className="space-y-6 pt-2">
          {/* Primary SSO Login */}
          <div className="space-y-3">
            <Button
              type="button"
              variant="default"
              onClick={handleAuthentikLogin}
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white py-6 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300"
              size="lg"
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                  Connecting...
                </>
              ) : (
                <>
                  <Lock className="h-5 w-5 mr-3" />
                  Sign in with SSO
                </>
              )}
            </Button>

            <Button
              type="button"
              variant="outline"
              onClick={handleAuthentikLogin}
              disabled={isLoading}
              className="w-full border-2 border-blue-600 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 py-6 text-lg font-semibold transition-all duration-300"
              size="lg"
            >
              <Mail className="h-5 w-5 mr-3" />
              Create New Account
            </Button>
          </div>

          {/* Social Login Hint */}
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <Separator />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-white dark:bg-gray-900 px-3 text-muted-foreground font-medium">
                SSO includes social login
              </span>
            </div>
          </div>

          {/* Social Icons (Visual hint - actual auth via Authentik) */}
          <div className="flex justify-center gap-4 opacity-60">
            <div className="w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
              <Google className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            </div>
            <div className="w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
              <Github className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            </div>
            <div className="w-10 h-10 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
              <Layout className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            </div>
          </div>

          {error && (
            <div className="rounded-lg bg-red-50 dark:bg-red-900/20 p-4 border border-red-200 dark:border-red-800 animate-in fade-in slide-in-from-top-2 duration-300">
              <p className="text-sm text-red-800 dark:text-red-200 font-medium">{error}</p>
            </div>
          )}

          {/* Support Links */}
          <div className="flex justify-center gap-6 text-sm">
            <a
              href="https://sso.bizoholic.net/if/flow/default-recovery-flow/"
              className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium transition-colors"
              target="_blank"
              rel="noopener noreferrer"
            >
              Forgot Password?
            </a>
            <span className="text-gray-300 dark:text-gray-700">|</span>
            <a
              href="#"
              className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium transition-colors"
            >
              Need Help?
            </a>
          </div>

          {/* Footer - Legal & Security */}
          <div className="text-center space-y-3 pt-4 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground">
              <Lock className="w-3 h-3" />
              <span>Enterprise-grade security with GDPR compliance</span>
            </div>
            <div className="flex justify-center gap-4 text-xs text-muted-foreground">
              <a href="#" className="hover:text-blue-600 transition-colors">Privacy Policy</a>
              <span>•</span>
              <a href="#" className="hover:text-blue-600 transition-colors">Terms of Service</a>
            </div>
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
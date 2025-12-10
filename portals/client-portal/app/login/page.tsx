'use client';

import { useState, useEffect, Suspense } from 'react';
import { signIn } from 'next-auth/react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Github, Mail, Lock, HelpCircle, Chrome } from 'lucide-react';
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
        callbackUrl: '/dashboard',
      });

      console.log('Login result:', result);

      if (result?.error) {
        console.error('Login error:', result.error);
        setError('Invalid credentials. Please check your email and password.');
      } else if (result?.ok) {
        console.log('Login successful, redirecting to dashboard');
        window.location.href = '/dashboard';
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

  const handleSocialLogin = async (provider: 'google' | 'github' | 'azure-ad') => {
    setIsLoading(true);
    setError('');

    try {
      await signIn(provider, {
        callbackUrl: '/dashboard',
        redirect: true,
      });
    } catch (err) {
      setError(`${provider} login failed. Please try again.`);
      setIsLoading(false);
    }
  };

  const handleAuthentikLogin = async () => {
    setIsLoading(true);
    setError('');

    try {
      await signIn('authentik', {
        callbackUrl: '/dashboard',
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
          {/* Brand Logo */}
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
          {/* Email/Password Form */}
          <form onSubmit={handleCredentialsLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email" className="text-sm font-medium">
                Email Address
              </Label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  id="email"
                  type="email"
                  placeholder="you@company.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-10"
                  required
                  disabled={isLoading}
                />
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password" className="text-sm font-medium">
                  Password
                </Label>
                <a
                  href="https://sso.bizoholic.net/if/flow/default-password-change/"
                  className="text-xs text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 transition-colors"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Forgot password?
                </a>
              </div>
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
              <div className="rounded-lg bg-red-50 dark:bg-red-900/20 p-4 border border-red-200 dark:border-red-800 animate-in fade-in slide-in-from-top-2 duration-300">
                <p className="text-sm text-red-800 dark:text-red-200 font-medium">{error}</p>
              </div>
            )}

            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white py-6 text-base font-semibold shadow-lg hover:shadow-xl transition-all duration-300"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Signing in...
                </>
              ) : (
                'Sign In'
              )}
            </Button>
          </form>

          {/* Divider */}
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <Separator />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-white dark:bg-gray-900 px-3 text-muted-foreground font-medium">
                Or continue with
              </span>
            </div>
          </div>

          {/* Social Login Buttons */}
          <div className="grid grid-cols-3 gap-3">
            <Button
              type="button"
              variant="outline"
              onClick={() => handleSocialLogin('google')}
              disabled={isLoading}
              className="w-full py-5 border-2 hover:bg-gray-50 dark:hover:bg-gray-800 transition-all duration-300"
            >
              <Chrome className="h-5 w-5 text-red-500" />
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={() => handleSocialLogin('github')}
              disabled={isLoading}
              className="w-full py-5 border-2 hover:bg-gray-50 dark:hover:bg-gray-800 transition-all duration-300"
            >
              <Github className="h-5 w-5" />
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={() => handleSocialLogin('azure-ad')}
              disabled={isLoading}
              className="w-full py-5 border-2 hover:bg-gray-50 dark:hover:bg-gray-800 transition-all duration-300"
            >
              <svg className="h-5 w-5" viewBox="0 0 23 23" fill="none">
                <path d="M0 0h11v11H0z" fill="#f25022" />
                <path d="M12 0h11v11H12z" fill="#00a4ef" />
                <path d="M0 12h11v11H0z" fill="#ffb900" />
                <path d="M12 12h11v11H12z" fill="#7fba00" />
              </svg>
            </Button>
          </div>

          {/* SSO Option */}
          <Button
            type="button"
            variant="outline"
            onClick={handleAuthentikLogin}
            disabled={isLoading}
            className="w-full border-2 border-blue-600 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 py-5 text-sm font-semibold transition-all duration-300"
          >
            <Lock className="h-4 w-4 mr-2" />
            Enterprise SSO Login
          </Button>

          {/* Support Links */}
          <div className="flex justify-center gap-6 text-sm pt-2">
            <a
              href="mailto:support@bizoholic.net"
              className="flex items-center gap-1 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium transition-colors"
            >
              <HelpCircle className="h-4 w-4" />
              Need Help?
            </a>
          </div>

          {/* Sign Up Link */}
          <div className="text-center text-sm">
            <span className="text-muted-foreground">Don't have an account? </span>
            <a
              href="https://sso.bizoholic.net/if/flow/enrollment/"
              className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-semibold transition-colors"
              target="_blank"
              rel="noopener noreferrer"
            >
              Sign up
            </a>
          </div>

          {/* Footer - Legal & Security */}
          <div className="text-center space-y-3 pt-4 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-center gap-2 text-xs text-muted-foreground">
              <Lock className="w-3 h-3" />
              <span>Enterprise-grade security with GDPR compliance</span>
            </div>
            <div className="flex justify-center gap-4 text-xs text-muted-foreground">
              <a href="/privacy" className="hover:text-blue-600 transition-colors">Privacy Policy</a>
              <span>•</span>
              <a href="/terms" className="hover:text-blue-600 transition-colors">Terms of Service</a>
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
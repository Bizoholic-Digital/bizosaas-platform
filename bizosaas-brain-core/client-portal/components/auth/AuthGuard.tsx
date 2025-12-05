"use client";

import { useAuth } from './AuthProvider';
import { useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

interface AuthGuardProps {
  children: React.ReactNode;
  requireAuth?: boolean;
  allowedRoles?: string[];
}

export default function AuthGuard({
  children,
  requireAuth = true,
  allowedRoles = []
}: AuthGuardProps) {
  const { user, isLoading, checkAuth } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    // Handle authentication token from URL (from unified auth redirect)
    const handleAuthToken = async () => {
      const token = searchParams.get('token');
      const userData = searchParams.get('user');

      if (token && userData) {
        try {
          // Store the authentication data
          const decodedUser = JSON.parse(decodeURIComponent(userData));
          localStorage.setItem('access_token', token);
          localStorage.setItem('user_data', JSON.stringify(decodedUser));

          // Refresh auth state
          await checkAuth();

          // Clean up URL
          const url = new URL(window.location.href);
          url.searchParams.delete('token');
          url.searchParams.delete('user');
          router.replace(url.pathname + url.search);
        } catch (error) {
          console.error('Error handling auth token:', error);
        }
      }
    };

    handleAuthToken();
  }, [searchParams, checkAuth, router]);

  // Show loading state
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Authenticating...</p>
        </div>
      </div>
    );
  }

  // Check if authentication is required
  if (requireAuth && !user) {
    // Redirect to unified auth portal
    if (typeof window !== 'undefined') {
      const returnUrl = encodeURIComponent(window.location.pathname + window.location.search);
      window.location.href = `http://localhost:3010?return_url=${returnUrl}`;
    }
    return null;
  }

  // Check role-based access
  if (user && allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Access Denied</h1>
          <p className="text-gray-600 mb-4">You don't have permission to access this resource.</p>
          <p className="text-sm text-gray-500">Required roles: {allowedRoles.join(', ')}</p>
          <p className="text-sm text-gray-500">Your role: {user.role}</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
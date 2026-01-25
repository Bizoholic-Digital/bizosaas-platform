"use client";

import { useAuth } from './AuthProvider';
import { useRouter } from 'next/navigation';


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
  const { user, isLoading, login } = useAuth();
  const router = useRouter();

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
    // Redirect to Clerk Login
    // We use openSignIn for client-side redirection or let middleware handle it.
    // However, if we are here, middleware might have let us through (e.g. public page that uses AuthGuard locally)
    // or we are in a transition state.

    // safe to trigger sign-in
    login();
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
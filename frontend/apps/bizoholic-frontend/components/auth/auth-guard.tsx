'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/use-auth'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { Shield, AlertTriangle } from 'lucide-react'

interface AuthGuardProps {
  children: React.ReactNode
  requiredRole?: string
  requiredService?: string
  fallback?: React.ReactNode
  redirectTo?: string
}

export function AuthGuard({ 
  children, 
  requiredRole,
  requiredService,
  fallback,
  redirectTo = '/auth/login' 
}: AuthGuardProps) {
  const { user, isLoading, isAuthenticated, hasRole, hasServiceAccess } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push(redirectTo)
    }
  }, [isLoading, isAuthenticated, router, redirectTo])

  // Show loading skeleton while checking authentication
  if (isLoading) {
    return fallback || <AuthLoadingSkeleton />
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return null
  }

  // Check role requirement
  if (requiredRole && !hasRole(requiredRole)) {
    return <AccessDenied reason="insufficient_role" requiredRole={requiredRole} />
  }

  // Check service access requirement
  if (requiredService && !hasServiceAccess(requiredService)) {
    return <AccessDenied reason="service_access_denied" requiredService={requiredService} />
  }

  return <>{children}</>
}

function AuthLoadingSkeleton() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-4">
          <div className="flex items-center justify-center">
            <Shield className="h-12 w-12 text-blue-600 animate-pulse" />
          </div>
          <div className="text-center">
            <Skeleton className="h-6 w-48 mx-auto mb-2" />
            <Skeleton className="h-4 w-64 mx-auto" />
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-3/4" />
          <Skeleton className="h-4 w-1/2" />
        </CardContent>
      </Card>
    </div>
  )
}

interface AccessDeniedProps {
  reason: 'insufficient_role' | 'service_access_denied'
  requiredRole?: string
  requiredService?: string
}

function AccessDenied({ reason, requiredRole, requiredService }: AccessDeniedProps) {
  const router = useRouter()
  
  const getMessage = () => {
    switch (reason) {
      case 'insufficient_role':
        return `This page requires ${requiredRole} role or higher.`
      case 'service_access_denied':
        return `You don't have access to the ${requiredService} service.`
      default:
        return 'Access denied.'
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="flex items-center justify-center mb-4">
            <AlertTriangle className="h-12 w-12 text-red-500" />
          </div>
          <CardTitle className="text-red-600">Access Denied</CardTitle>
          <CardDescription>{getMessage()}</CardDescription>
        </CardHeader>
        <CardContent className="text-center">
          <p className="text-sm text-muted-foreground mb-4">
            Please contact your administrator if you believe this is an error.
          </p>
          <button
            onClick={() => router.back()}
            className="text-blue-600 hover:underline text-sm"
          >
            Go back
          </button>
        </CardContent>
      </Card>
    </div>
  )
}

// Specific guard components for common use cases
export function SuperAdminGuard({ children, fallback }: { children: React.ReactNode, fallback?: React.ReactNode }) {
  return (
    <AuthGuard requiredRole="super_admin" fallback={fallback}>
      {children}
    </AuthGuard>
  )
}

export function TenantAdminGuard({ children, fallback }: { children: React.ReactNode, fallback?: React.ReactNode }) {
  return (
    <AuthGuard requiredRole="tenant_admin" fallback={fallback}>
      {children}
    </AuthGuard>
  )
}

export function ServiceGuard({ 
  serviceName, 
  children, 
  fallback 
}: { 
  serviceName: string
  children: React.ReactNode
  fallback?: React.ReactNode 
}) {
  return (
    <AuthGuard requiredService={serviceName} fallback={fallback}>
      {children}
    </AuthGuard>
  )
}
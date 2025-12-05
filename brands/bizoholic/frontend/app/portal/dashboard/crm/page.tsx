'use client'

import { useAuth } from '@/hooks/use-auth'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Users, AlertCircle, ExternalLink, Loader2 } from 'lucide-react'

export default function CRMDashboardPage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [iframeLoading, setIframeLoading] = useState(true)

  useEffect(() => {
    console.log('Current User:', user) // Debugging
    if (!loading && !user) {
      router.push('/portal/login')
    }
  }, [user, loading, router])

  // Check if user has CRM access (admin, sales, or support roles)
  // TEMPORARY: Allow all users for testing/demo purposes
  const hasCRMAccess = true;
  /*
  const hasCRMAccess = user?.role === 'admin' || 
                       user?.role === 'sales' || 
                       user?.role === 'support' ||
                       user?.role === 'content_editor' ||
                       user?.email === 'demo@bizoholic.com' // Allow demo user
  */

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-primary" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    )
  }

  if (!hasCRMAccess) {
    return (
      <div className="container py-20">
        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <div className="flex items-center gap-2 mb-2">
              <AlertCircle className="h-6 w-6 text-destructive" />
              <CardTitle>Access Denied</CardTitle>
            </div>
            <CardDescription>
              You don't have permission to access the CRM dashboard.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              CRM access is only available to users with Admin, Sales, or Support roles.
            </p>
            <p className="text-sm text-muted-foreground mb-6">
              If you believe you should have access, please contact your administrator.
            </p>
            <Button onClick={() => router.push('/portal/dashboard')}>
              Back to Dashboard
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <div className="border-b bg-background">
        <div className="container py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Users className="h-6 w-6 text-primary" />
              <div>
                <h1 className="text-2xl font-bold">Customer Relationship Management</h1>
                <p className="text-sm text-muted-foreground">
                  Manage customers, leads, and sales pipeline with Django CRM
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="secondary">
                {user?.role === 'admin' ? 'Admin' :
                  user?.role === 'sales' ? 'Sales' :
                    user?.role === 'support' ? 'Support' : 'User'}
              </Badge>
              <Button
                variant="outline"
                size="sm"
                onClick={() => router.push('/portal/dashboard')}
              >
                Back to Dashboard
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Django CRM Iframe */}
      <div className="flex-1 relative bg-muted/30">
        {iframeLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-background/80 z-10">
            <div className="text-center">
              <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-primary" />
              <p className="text-muted-foreground">Loading CRM Dashboard...</p>
            </div>
          </div>
        )}

        <iframe
          src={process.env.NEXT_PUBLIC_CRM_URL || 'http://localhost:8005/admin'}
          className="w-full h-full border-0"
          title="Django CRM Dashboard"
          onLoad={() => setIframeLoading(false)}
          sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-modals"
        />
      </div>

      {/* Footer Info */}
      <div className="border-t bg-muted/30">
        <div className="container py-2">
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <div className="flex items-center gap-4">
              <span>Powered by Django CRM</span>
              <a
                href="https://docs.djangoproject.com/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1 hover:text-primary transition-colors"
              >
                Documentation
                <ExternalLink className="h-3 w-3" />
              </a>
            </div>
            <span>Logged in as {user?.email}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

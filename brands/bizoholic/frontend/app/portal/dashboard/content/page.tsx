'use client'

import { useAuth } from '@/hooks/use-auth'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { FileText, AlertCircle, ExternalLink, Loader2 } from 'lucide-react'

export default function ContentEditorPage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [iframeLoading, setIframeLoading] = useState(true)
  const [ssoUrl, setSsoUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!loading && !user) {
      router.push('/portal/login')
    }
  }, [user, loading, router])

  // Fetch SSO URL
  useEffect(() => {
    const fetchSsoUrl = async () => {
      if (!user) return

      try {
        const response = await fetch('/api/brain/auth/sso/wagtail', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: user.email?.split('@')[0] || 'admin', // Fallback to admin for now
            email: user.email
          }),
        })

        if (!response.ok) {
          throw new Error('Failed to generate SSO token')
        }

        const data = await response.json()
        setSsoUrl(data.sso_url)
      } catch (err) {
        console.error('SSO Error:', err)
        setError('Failed to authenticate with CMS')
        // Fallback to direct URL if SSO fails
        setSsoUrl(process.env.NEXT_PUBLIC_WAGTAIL_URL || 'http://localhost:8002/admin')
      }
    }

    if (user && !ssoUrl) {
      fetchSsoUrl()
    }
  }, [user, ssoUrl])

  // Check if user has content editor permissions
  // TEMPORARY: Allow all users for testing/demo purposes
  const hasContentEditorAccess = true;

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

  if (!hasContentEditorAccess) {
    return (
      <div className="container py-20">
        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <div className="flex items-center gap-2 mb-2">
              <AlertCircle className="h-6 w-6 text-destructive" />
              <CardTitle>Access Denied</CardTitle>
            </div>
            <CardDescription>
              You don't have permission to access the content editor.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Content editing is only available to users with Content Editor or Admin roles.
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
              <FileText className="h-6 w-6 text-primary" />
              <div>
                <h1 className="text-2xl font-bold">Content Management System</h1>
                <p className="text-sm text-muted-foreground">
                  Manage your website content with Wagtail CMS
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="secondary">
                {user?.role === 'admin' ? 'Admin' : 'Content Editor'}
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

      {/* Wagtail CMS Iframe */}
      <div className="flex-1 relative bg-muted/30">
        {(iframeLoading || !ssoUrl) && (
          <div className="absolute inset-0 flex items-center justify-center bg-background/80 z-10">
            <div className="text-center">
              <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-primary" />
              <p className="text-muted-foreground">
                {!ssoUrl ? 'Authenticating...' : 'Loading Content Editor...'}
              </p>
            </div>
          </div>
        )}

        {ssoUrl && (
          <iframe
            src={ssoUrl}
            className="w-full h-full border-0"
            title="Wagtail Content Management System"
            onLoad={() => setIframeLoading(false)}
            sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-modals"
          />
        )}
      </div>

      {/* Footer Info */}
      <div className="border-t bg-muted/30">
        <div className="container py-2">
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <div className="flex items-center gap-4">
              <span>Powered by Wagtail CMS</span>
              <a
                href="https://docs.wagtail.org/"
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

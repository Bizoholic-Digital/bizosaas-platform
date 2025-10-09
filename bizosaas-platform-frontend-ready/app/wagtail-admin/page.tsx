'use client'

import { useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ExternalLink, FileText, Settings, Users } from 'lucide-react'

export default function WagtailAdminPage() {
  useEffect(() => {
    // Redirect to Wagtail admin after a short delay
    const timer = setTimeout(() => {
      window.location.href = 'http://localhost:8006/admin/'
    }, 2000)

    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-6">
        <div className="text-center">
          <div className="mx-auto w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mb-4">
            <FileText className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Wagtail CMS Admin
          </h1>
          <p className="text-gray-600">
            Redirecting to content management system...
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Settings className="h-5 w-5 mr-2" />
              Content Management
            </CardTitle>
            <CardDescription>
              Manage website content, pages, and media assets
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <FileText className="h-4 w-4 text-green-600" />
                </div>
                <div>
                  <h4 className="font-medium">Page Management</h4>
                  <p className="text-sm text-muted-foreground">Create and edit website pages</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <Users className="h-4 w-4 text-blue-600" />
                </div>
                <div>
                  <h4 className="font-medium">User Management</h4>
                  <p className="text-sm text-muted-foreground">Manage CMS users and permissions</p>
                </div>
              </div>
              
              <div className="pt-4 border-t">
                <Button asChild className="w-full">
                  <a href="http://localhost:8006/admin/" target="_blank" rel="noopener noreferrer">
                    <ExternalLink className="h-4 w-4 mr-2" />
                    Access Wagtail Admin
                  </a>
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="text-center text-sm text-gray-600">
          <p>
            Having trouble? Visit{' '}
            <a 
              href="http://localhost:8006/admin/" 
              className="text-blue-600 hover:underline"
              target="_blank" 
              rel="noopener noreferrer"
            >
              localhost:8006/admin/
            </a>
            {' '}directly
          </p>
        </div>
      </div>
    </div>
  )
}
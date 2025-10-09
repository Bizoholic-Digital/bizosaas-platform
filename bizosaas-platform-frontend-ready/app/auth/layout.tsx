"use client"

import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Logo } from '@/components/ui/logo'
// import { useTenantTheme } from '@bizosaas/shared-ui' // Temporarily disabled

interface AuthLayoutProps {
  children: React.ReactNode
}

export default function AuthLayout({ children }: AuthLayoutProps) {
  // const { config } = useTenantTheme() // Temporarily disabled
  const config = { branding: { companyName: 'BizOSaaS' } } // Fallback config
  
  return (
    <div className="min-h-screen grid lg:grid-cols-2">
      {/* Left side - Auth Form */}
      <div className="flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-20 xl:px-24">
        <div className="mx-auto w-full max-w-sm lg:w-96">
          {/* Header */}
          <div className="mb-8">
            <Link href="/" className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-6">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to home
            </Link>
            
            <div className="mb-6">
              <Logo 
                href="/" 
                priority={true}
                showText={false}
                width={140}
                height={45}
                className=""
              />
            </div>
          </div>
          
          {/* Auth Form */}
          {children}
          
          {/* Footer */}
          <div className="mt-8 text-center">
            <p className="text-xs text-muted-foreground">
              By continuing, you agree to our{' '}
              <Link href="/terms" className="underline hover:text-foreground">
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link href="/privacy" className="underline hover:text-foreground">
                Privacy Policy
              </Link>
            </p>
          </div>
        </div>
      </div>

      {/* Right side - Marketing Content */}
      <div className="hidden lg:block relative bg-gradient-to-br from-primary/10 via-primary/5 to-accent/10">
        <div className="absolute inset-0 bg-grid-pattern opacity-10" />
        
        <div className="flex flex-col justify-center h-full px-12 xl:px-16">
          <div className="max-w-md">
            <h2 className="text-3xl font-bold mb-6">
              Join thousands of businesses using <span className="text-primary">AI</span> to transform their {config.branding.companyName === 'BizOSaaS' ? 'business operations' : 'marketing strategies'}
            </h2>
            
            <div className="space-y-6">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-6 h-6 bg-primary/20 rounded-full flex items-center justify-center mt-1">
                  <div className="w-2 h-2 bg-primary rounded-full" />
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Autonomous Campaign Management</h3>
                  <p className="text-sm text-muted-foreground">
                    AI agents handle campaign creation, optimization, and performance monitoring 24/7.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-6 h-6 bg-primary/20 rounded-full flex items-center justify-center mt-1">
                  <div className="w-2 h-2 bg-primary rounded-full" />
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Multi-Platform Integration</h3>
                  <p className="text-sm text-muted-foreground">
                    Connect Google Ads, Meta, LinkedIn, and 40+ other marketing platforms.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-6 h-6 bg-primary/20 rounded-full flex items-center justify-center mt-1">
                  <div className="w-2 h-2 bg-primary rounded-full" />
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Enterprise Security</h3>
                  <p className="text-sm text-muted-foreground">
                    SOC 2 compliant with advanced encryption and access controls.
                  </p>
                </div>
              </div>
            </div>
            
            {/* Testimonial */}
            <div className="mt-12 p-6 bg-background/50 backdrop-blur-sm rounded-lg border">
              <blockquote className="text-sm mb-3">
                "{config.branding.companyName} increased our ROI by 340% in just 3 months. The AI agents work around the clock to optimize everything."
              </blockquote>
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-br from-primary to-accent rounded-full flex items-center justify-center text-xs font-semibold text-white">
                  JS
                </div>
                <div>
                  <div className="text-xs font-semibold">Jane Smith</div>
                  <div className="text-xs text-muted-foreground">CMO, TechCorp</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
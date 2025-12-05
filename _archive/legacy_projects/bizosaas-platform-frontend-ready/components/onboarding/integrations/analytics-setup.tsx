'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  BarChart3, CheckCircle, Zap, TrendingUp, 
  Eye, MousePointer, Users, ArrowRight,
  RefreshCw, Globe, Smartphone
} from 'lucide-react'

interface AnalyticsSetupProps {
  businessData: any
  onComplete: (data: any) => void
  onCancel: () => void
}

export function AnalyticsSetup({ businessData, onComplete, onCancel }: AnalyticsSetupProps) {
  const [isSettingUp, setIsSettingUp] = useState(false)
  const [setupStatus, setSetupStatus] = useState<'idle' | 'setting_up' | 'success'>('idle')
  const [analyticsData, setAnalyticsData] = useState<any>(null)

  const handleSetupAnalytics = async () => {
    setIsSettingUp(true)
    setSetupStatus('setting_up')

    try {
      // Simulate analytics setup process
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Mock analytics setup result
      const mockData = {
        trackingId: `BZ-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
        dashboardUrl: 'https://analytics.bizosaas.com/dashboard',
        features: {
          real_time: true,
          conversion_tracking: true,
          funnel_analysis: true,
          cohort_analysis: true,
          custom_events: true,
          automated_reports: true
        },
        metrics: {
          page_views: true,
          unique_visitors: true,
          bounce_rate: true,
          session_duration: true,
          goal_conversions: true,
          revenue_tracking: true
        }
      }
      
      setAnalyticsData(mockData)
      setSetupStatus('success')
    } catch (error) {
      console.error('Analytics setup error:', error)
      setSetupStatus('idle')
    } finally {
      setIsSettingUp(false)
    }
  }

  const handleComplete = () => {
    const setupData = {
      provider: 'bizosaas_analytics',
      trackingId: analyticsData.trackingId,
      dashboardUrl: analyticsData.dashboardUrl,
      features: analyticsData.features,
      metrics: analyticsData.metrics,
      connectedAt: new Date().toISOString(),
      autoReporting: {
        daily_summary: true,
        weekly_insights: true,
        monthly_deep_dive: true,
        anomaly_alerts: true
      }
    }
    
    onComplete(setupData)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-start gap-3">
        <BarChart3 className="h-6 w-6 text-purple-600 mt-1" />
        <div>
          <h3 className="font-semibold text-lg">Analytics Dashboard</h3>
          <p className="text-sm text-muted-foreground">
            Track your marketing performance and website analytics
          </p>
        </div>
      </div>

      {setupStatus === 'idle' && (
        <div className="space-y-6">
          <Alert className="border-purple-200 bg-purple-50">
            <Zap className="h-4 w-4 text-purple-600" />
            <AlertDescription className="text-purple-700">
              <strong>Instant Analytics Setup</strong> - Our built-in analytics system provides 
              comprehensive tracking without any external dependencies. Setup takes under 30 seconds!
            </AlertDescription>
          </Alert>

          {/* Features Preview */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm">What You'll Get Instantly</CardTitle>
              <CardDescription>
                Comprehensive analytics and reporting capabilities
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-3">
                  <h5 className="font-medium flex items-center gap-2">
                    <TrendingUp className="h-4 w-4 text-green-600" />
                    Real-time Analytics
                  </h5>
                  <div className="space-y-2 text-sm text-muted-foreground">
                    {[
                      'Live visitor tracking',
                      'Real-time conversions',
                      'Active user monitoring',
                      'Traffic source analysis'
                    ].map((feature) => (
                      <div key={feature} className="flex items-center gap-2">
                        <CheckCircle className="h-3 w-3 text-green-500" />
                        {feature}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-3">
                  <h5 className="font-medium flex items-center gap-2">
                    <Eye className="h-4 w-4 text-blue-600" />
                    Conversion Tracking
                  </h5>
                  <div className="space-y-2 text-sm text-muted-foreground">
                    {[
                      'Goal completion tracking',
                      'E-commerce revenue',
                      'Lead generation metrics',
                      'Custom event tracking'
                    ].map((feature) => (
                      <div key={feature} className="flex items-center gap-2">
                        <CheckCircle className="h-3 w-3 text-green-500" />
                        {feature}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-3">
                  <h5 className="font-medium flex items-center gap-2">
                    <Users className="h-4 w-4 text-orange-600" />
                    Audience Insights
                  </h5>
                  <div className="space-y-2 text-sm text-muted-foreground">
                    {[
                      'Demographic breakdown',
                      'Behavior flow analysis',
                      'User journey mapping',
                      'Cohort analysis'
                    ].map((feature) => (
                      <div key={feature} className="flex items-center gap-2">
                        <CheckCircle className="h-3 w-3 text-green-500" />
                        {feature}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-3">
                  <h5 className="font-medium flex items-center gap-2">
                    <MousePointer className="h-4 w-4 text-purple-600" />
                    Campaign Performance
                  </h5>
                  <div className="space-y-2 text-sm text-muted-foreground">
                    {[
                      'Multi-channel attribution',
                      'ROI calculation',
                      'A/B test results',
                      'Automated reporting'
                    ].map((feature) => (
                      <div key={feature} className="flex items-center gap-2">
                        <CheckCircle className="h-3 w-3 text-green-500" />
                        {feature}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Setup Benefits */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              {
                icon: Globe,
                title: 'Privacy-First',
                desc: 'GDPR compliant, no external cookies'
              },
              {
                icon: Zap,
                title: 'Lightning Fast',
                desc: 'Real-time data, instant insights'
              },
              {
                icon: Smartphone,
                title: 'Mobile Optimized',
                desc: 'Perfect tracking across all devices'
              }
            ].map(({ icon: Icon, title, desc }) => (
              <div key={title} className="text-center p-4 rounded-lg bg-gray-50">
                <Icon className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                <h4 className="font-semibold text-sm">{title}</h4>
                <p className="text-xs text-muted-foreground">{desc}</p>
              </div>
            ))}
          </div>

          <div className="text-center">
            <Button 
              onClick={handleSetupAnalytics}
              disabled={isSettingUp}
              size="lg"
              className="min-w-[250px] bg-purple-600 hover:bg-purple-700"
            >
              <BarChart3 className="mr-2 h-4 w-4" />
              Set Up Analytics Dashboard
            </Button>
            <p className="text-xs text-muted-foreground mt-2">
              Setup completes automatically - no configuration needed
            </p>
          </div>
        </div>
      )}

      {setupStatus === 'setting_up' && (
        <Alert className="border-blue-200 bg-blue-50">
          <RefreshCw className="h-4 w-4 text-blue-600 animate-spin" />
          <AlertDescription className="text-blue-700">
            <div className="space-y-2">
              <strong>Setting up your analytics dashboard...</strong>
              <div className="text-sm">
                • Creating tracking infrastructure<br/>
                • Configuring real-time data pipeline<br/>
                • Initializing reporting engine<br/>
                • Testing data collection
              </div>
            </div>
          </AlertDescription>
        </Alert>
      )}

      {setupStatus === 'success' && (
        <div className="space-y-4">
          <Alert className="border-green-200 bg-green-50">
            <CheckCircle className="h-4 w-4 text-green-600" />
            <AlertDescription className="text-green-700">
              <div className="space-y-3">
                <strong>Analytics dashboard is live!</strong>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center justify-between">
                    <span>Tracking ID:</span>
                    <code className="bg-white px-2 py-1 rounded text-xs font-mono">
                      {analyticsData?.trackingId}
                    </code>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Dashboard:</span>
                    <Badge variant="outline">Ready</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Data Collection:</span>
                    <Badge variant="default" className="bg-green-500">Active</Badge>
                  </div>
                </div>
              </div>
            </AlertDescription>
          </Alert>

          {/* Dashboard Preview */}
          <Card className="border-dashed">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm">Your Analytics Dashboard</CardTitle>
              <CardDescription>
                Data collection starts immediately - view your first insights within minutes
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                {[
                  { metric: 'Page Views', value: '0', trend: '↑', color: 'text-blue-600' },
                  { metric: 'Visitors', value: '0', trend: '↑', color: 'text-green-600' },
                  { metric: 'Bounce Rate', value: '-%', trend: '↓', color: 'text-orange-600' },
                  { metric: 'Conversions', value: '0', trend: '↑', color: 'text-purple-600' }
                ].map(({ metric, value, trend, color }) => (
                  <div key={metric} className="p-3 rounded-lg bg-gray-50">
                    <div className={`text-2xl font-bold ${color}`}>{value}</div>
                    <div className="text-xs text-muted-foreground">{metric}</div>
                    <div className={`text-sm ${color}`}>{trend}</div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Next Steps */}
          <Card className="border-blue-200 bg-blue-50">
            <CardContent className="pt-6">
              <h4 className="font-medium mb-2">What's Next?</h4>
              <div className="space-y-2 text-sm text-muted-foreground">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-3 w-3 text-green-500" />
                  Analytics tracking is now active on your website
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-3 w-3 text-green-500" />
                  Daily email reports will begin tomorrow
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-3 w-3 text-green-500" />
                  AI insights will be generated as data accumulates
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex justify-between">
        <Button variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        
        <Button
          onClick={handleComplete}
          disabled={setupStatus !== 'success'}
        >
          Complete Setup
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}
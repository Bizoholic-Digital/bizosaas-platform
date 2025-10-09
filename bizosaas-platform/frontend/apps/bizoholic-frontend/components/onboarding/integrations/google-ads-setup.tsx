'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { 
  Globe, ExternalLink, CheckCircle, Clock, 
  AlertTriangle, ArrowRight, RefreshCw, Shield,
  Search, Target, TrendingUp
} from 'lucide-react'

interface GoogleAdsSetupProps {
  businessData: any
  onComplete: (data: any) => void
  onCancel: () => void
}

export function GoogleAdsSetup({ businessData, onComplete, onCancel }: GoogleAdsSetupProps) {
  const [setupMethod, setSetupMethod] = useState<'guided' | 'existing'>('guided')
  const [setupStatus, setSetupStatus] = useState<'idle' | 'connecting' | 'success' | 'pending'>('idle')
  const [isProcessing, setIsProcessing] = useState(false)

  const handleGuidedSetup = async () => {
    setIsProcessing(true)
    setSetupStatus('connecting')

    try {
      // Simulate guided setup process
      await new Promise(resolve => setTimeout(resolve, 2000))
      setSetupStatus('pending')
    } catch (error) {
      setSetupStatus('idle')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleComplete = () => {
    const setupData = {
      method: setupMethod,
      status: setupStatus,
      provider: 'google_ads',
      connectedAt: new Date().toISOString(),
      features: {
        search_campaigns: true,
        display_campaigns: true,
        smart_bidding: true,
        conversion_tracking: true,
        automated_optimization: true
      },
      pendingApproval: setupStatus === 'pending'
    }
    
    onComplete(setupData)
  }

  const renderGuidedSetup = () => (
    <div className="space-y-6">
      <Alert className="border-blue-200 bg-blue-50">
        <Shield className="h-4 w-4 text-blue-600" />
        <AlertDescription className="text-blue-700">
          <strong>Recommended:</strong> We'll guide you through the entire Google Ads setup process, 
          including account creation, billing setup, and campaign configuration.
        </AlertDescription>
      </Alert>

      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { icon: Search, title: 'Account Setup', desc: 'Create & verify Google Ads account' },
            { icon: Target, title: 'Campaign Creation', desc: 'AI-optimized campaign structure' },
            { icon: TrendingUp, title: 'Performance Tracking', desc: 'Advanced analytics & reporting' }
          ].map(({ icon: Icon, title, desc }) => (
            <div key={title} className="text-center p-4 rounded-lg bg-gray-50">
              <Icon className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <h4 className="font-semibold text-sm">{title}</h4>
              <p className="text-xs text-muted-foreground">{desc}</p>
            </div>
          ))}
        </div>

        {setupStatus === 'idle' && (
          <div className="text-center space-y-4">
            <div>
              <Button 
                onClick={handleGuidedSetup}
                disabled={isProcessing}
                size="lg"
                className="min-w-[250px] bg-blue-600 hover:bg-blue-700"
              >
                {isProcessing ? (
                  <>
                    <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                    Setting Up Account...
                  </>
                ) : (
                  <>
                    Start Guided Setup
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </>
                )}
              </Button>
              <p className="text-xs text-muted-foreground mt-2">
                We'll handle the technical setup for you
              </p>
            </div>

            <Card className="border-yellow-200 bg-yellow-50">
              <CardContent className="p-4">
                <div className="flex items-start gap-3">
                  <Clock className="h-5 w-5 text-yellow-600 mt-0.5" />
                  <div className="text-sm text-yellow-700">
                    <strong>Setup Time:</strong> 15-30 minutes guided session<br/>
                    <strong>Activation:</strong> Same day (after Google approval)<br/>
                    <strong>First Campaign:</strong> Live within 2-4 hours
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {setupStatus === 'connecting' && (
          <Alert className="border-blue-200 bg-blue-50">
            <RefreshCw className="h-4 w-4 text-blue-600 animate-spin" />
            <AlertDescription className="text-blue-700">
              <div className="space-y-2">
                <strong>Creating your Google Ads foundation...</strong>
                <div className="text-sm space-y-1">
                  • Preparing account structure<br/>
                  • Configuring conversion tracking<br/>
                  • Setting up automated bidding<br/>
                  • Initializing campaign templates
                </div>
              </div>
            </AlertDescription>
          </Alert>
        )}

        {setupStatus === 'pending' && (
          <Alert className="border-orange-200 bg-orange-50">
            <Clock className="h-4 w-4 text-orange-600" />
            <AlertDescription className="text-orange-700">
              <div className="space-y-3">
                <strong>Google Ads setup initiated!</strong>
                <div className="text-sm space-y-2">
                  <div>✅ Account structure created</div>
                  <div>✅ Conversion tracking configured</div>
                  <div>⏳ Awaiting Google review (typically 24-48 hours)</div>
                  <div>📧 You'll receive email updates on approval status</div>
                </div>
              </div>
            </AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  )

  const renderExistingSetup = () => (
    <div className="space-y-6">
      <Alert className="border-yellow-200 bg-yellow-50">
        <AlertTriangle className="h-4 w-4 text-yellow-600" />
        <AlertDescription className="text-yellow-700">
          If you already have a Google Ads account, we can connect to it directly. 
          You'll need admin access to authorize the connection.
        </AlertDescription>
      </Alert>

      <div className="space-y-4">
        <div>
          <Label htmlFor="customer-id">Google Ads Customer ID</Label>
          <Input
            id="customer-id"
            placeholder="123-456-7890"
            className="font-mono"
          />
          <p className="text-xs text-muted-foreground mt-1">
            Find this in your Google Ads account under Settings → Account Settings
          </p>
        </div>

        <div className="flex gap-3">
          <Button
            onClick={() => setSetupStatus('success')}
          >
            Connect Account
          </Button>
          
          <Button 
            variant="outline"
            onClick={() => window.open('https://ads.google.com', '_blank')}
          >
            Open Google Ads
            <ExternalLink className="ml-2 h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="flex items-start gap-3">
        <Globe className="h-6 w-6 text-blue-600 mt-1" />
        <div>
          <h3 className="font-semibold text-lg">Google Ads Integration</h3>
          <p className="text-sm text-muted-foreground">
            Connect Google Ads for search and display advertising campaigns
          </p>
        </div>
      </div>

      <Tabs value={setupMethod} onValueChange={(value) => setSetupMethod(value as 'guided' | 'existing')}>
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="guided" className="flex items-center gap-2">
            <Shield className="h-4 w-4" />
            Guided Setup
            <Badge variant="secondary" className="text-xs">Recommended</Badge>
          </TabsTrigger>
          <TabsTrigger value="existing" className="flex items-center gap-2">
            <Globe className="h-4 w-4" />
            Existing Account
          </TabsTrigger>
        </TabsList>

        <TabsContent value="guided">
          {renderGuidedSetup()}
        </TabsContent>

        <TabsContent value="existing">
          {renderExistingSetup()}
        </TabsContent>
      </Tabs>

      {/* What You'll Get */}
      <Card className="border-dashed">
        <CardHeader className="pb-3">
          <CardTitle className="text-sm">Google Ads Capabilities</CardTitle>
        </CardHeader>
        <CardContent className="pt-0">
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              'Search campaign automation',
              'Display advertising',
              'YouTube video ads',
              'Smart bidding strategies',
              'Conversion tracking',
              'Audience targeting',
              'A/B testing',
              'Performance reporting'
            ].map((feature) => (
              <div key={feature} className="flex items-center gap-2">
                <CheckCircle className="h-3 w-3 text-green-500" />
                {feature}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex justify-between">
        <Button variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        
        <Button
          onClick={handleComplete}
          disabled={setupStatus === 'idle'}
        >
          Continue
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}
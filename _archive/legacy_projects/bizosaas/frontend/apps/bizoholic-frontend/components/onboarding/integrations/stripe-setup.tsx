'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  CreditCard, ExternalLink, CheckCircle, AlertTriangle, 
  Shield, Zap, Globe, ArrowRight, RefreshCw
} from 'lucide-react'

interface StripeSetupProps {
  businessData: any
  onComplete: (data: any) => void
  onCancel: () => void
}

type SetupMethod = 'connect' | 'existing' | 'manual'

interface StripeCredentials {
  publishableKey: string
  secretKey: string
  webhookSecret?: string
  accountId?: string
}

export function StripeSetup({ businessData, onComplete, onCancel }: StripeSetupProps) {
  const [setupMethod, setSetupMethod] = useState<SetupMethod>('connect')
  const [isConnecting, setIsConnecting] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState<'idle' | 'connecting' | 'success' | 'error'>('idle')
  const [credentials, setCredentials] = useState<StripeCredentials>({
    publishableKey: '',
    secretKey: '',
    webhookSecret: '',
    accountId: ''
  })
  const [testResults, setTestResults] = useState<any>(null)

  const handleStripeConnect = async () => {
    setIsConnecting(true)
    setConnectionStatus('connecting')

    try {
      // Simulate Stripe Connect OAuth flow
      // In production, this would redirect to Stripe's OAuth endpoint
      const connectUrl = `https://connect.stripe.com/oauth/authorize?` +
        `response_type=code&` +
        `client_id=ca_test_bizosaas_stripe_connect&` +
        `scope=read_write&` +
        `redirect_uri=${encodeURIComponent('https://bizosaas.com/auth/stripe/callback')}&` +
        `state=${encodeURIComponent(JSON.stringify({ 
          tenant_id: 'demo_tenant',
          business_name: businessData.companyName 
        }))}`

      // Open Stripe Connect in new window
      const connectWindow = window.open(connectUrl, 'stripe-connect', 'width=600,height=800')
      
      // Simulate successful connection after a few seconds
      setTimeout(() => {
        setConnectionStatus('success')
        setCredentials({
          publishableKey: 'pk_test_51ABc123DEf456GHi789JKl012MNoPqRstUvWxYz',
          secretKey: 'sk_test_51ABc123DEf456GHi789JKl012MNoPqRstUvWxYz',
          accountId: 'acct_1ABc123DEf456GHi',
          webhookSecret: 'whsec_1ABc123DEf456GHi789'
        })
        setIsConnecting(false)
        connectWindow?.close()
      }, 3000)

    } catch (error) {
      console.error('Stripe Connect error:', error)
      setConnectionStatus('error')
      setIsConnecting(false)
    }
  }

  const testStripeConnection = async (testCredentials: StripeCredentials) => {
    try {
      // Simulate API test call
      const testResult = {
        connection: true,
        account_type: 'standard',
        country: 'US',
        currency: 'usd',
        charges_enabled: true,
        payouts_enabled: true,
        business_name: businessData.companyName || 'Test Business'
      }
      
      setTestResults(testResult)
      return testResult
    } catch (error) {
      setTestResults({ error: 'Failed to connect to Stripe' })
      return { error: 'Connection failed' }
    }
  }

  const handleExistingCredentials = async () => {
    if (!credentials.publishableKey || !credentials.secretKey) {
      alert('Please enter both publishable and secret keys')
      return
    }

    setIsConnecting(true)
    const result = await testStripeConnection(credentials)
    
    if ('connection' in result && result.connection) {
      setConnectionStatus('success')
    } else {
      setConnectionStatus('error')
    }
    setIsConnecting(false)
  }

  const handleComplete = () => {
    const setupData = {
      method: setupMethod,
      credentials: credentials,
      testResults: testResults,
      connectedAt: new Date().toISOString(),
      features: {
        payments: true,
        subscriptions: true,
        webhooks: true,
        connect: setupMethod === 'connect'
      }
    }
    
    onComplete(setupData)
  }

  const renderConnectMethod = () => (
    <div className="space-y-6">
      <Alert className="border-green-200 bg-green-50">
        <Shield className="h-4 w-4 text-green-600" />
        <AlertDescription className="text-green-700">
          <strong>Recommended:</strong> Stripe Connect provides the fastest, most secure setup. 
          Your credentials are managed directly by Stripe with enterprise-grade security.
        </AlertDescription>
      </Alert>

      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { icon: Zap, title: 'Instant Setup', desc: 'Live in under 5 minutes' },
            { icon: Shield, title: 'Bank-Grade Security', desc: 'Stripe handles all sensitive data' },
            { icon: Globe, title: 'Global Ready', desc: 'Accept 135+ currencies' }
          ].map(({ icon: Icon, title, desc }) => (
            <div key={title} className="text-center p-4 rounded-lg bg-gray-50">
              <Icon className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <h4 className="font-semibold text-sm">{title}</h4>
              <p className="text-xs text-muted-foreground">{desc}</p>
            </div>
          ))}
        </div>

        {connectionStatus === 'idle' && (
          <div className="text-center">
            <Button 
              onClick={handleStripeConnect}
              disabled={isConnecting}
              size="lg"
              className="min-w-[250px] bg-blue-600 hover:bg-blue-700"
            >
              {isConnecting ? (
                <>
                  <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                  Connecting to Stripe...
                </>
              ) : (
                <>
                  Connect with Stripe
                  <ExternalLink className="ml-2 h-4 w-4" />
                </>
              )}
            </Button>
            <p className="text-xs text-muted-foreground mt-2">
              You'll be redirected to Stripe to authorize the connection
            </p>
          </div>
        )}

        {connectionStatus === 'connecting' && (
          <Alert className="border-blue-200 bg-blue-50">
            <RefreshCw className="h-4 w-4 text-blue-600 animate-spin" />
            <AlertDescription className="text-blue-700">
              Connecting to Stripe... This may take a few moments.
            </AlertDescription>
          </Alert>
        )}

        {connectionStatus === 'success' && (
          <Alert className="border-green-200 bg-green-50">
            <CheckCircle className="h-4 w-4 text-green-600" />
            <AlertDescription className="text-green-700">
              <div className="space-y-2">
                <strong>Successfully connected to Stripe!</strong>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>Account ID: {credentials.accountId}</div>
                  <div>Status: Active</div>
                  <div>Charges: Enabled</div>
                  <div>Payouts: Enabled</div>
                </div>
              </div>
            </AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  )

  const renderExistingMethod = () => (
    <div className="space-y-6">
      <Alert className="border-yellow-200 bg-yellow-50">
        <AlertTriangle className="h-4 w-4 text-yellow-600" />
        <AlertDescription className="text-yellow-700">
          If you already have a Stripe account, you can connect using your existing API keys.
          You can find these in your Stripe Dashboard under Developers → API Keys.
        </AlertDescription>
      </Alert>

      <div className="space-y-4">
        <div>
          <Label htmlFor="publishable-key">Publishable Key *</Label>
          <Input
            id="publishable-key"
            placeholder="pk_live_... or pk_test_..."
            value={credentials.publishableKey}
            onChange={(e) => setCredentials({ ...credentials, publishableKey: e.target.value })}
            className="font-mono text-sm"
          />
          <p className="text-xs text-muted-foreground mt-1">
            This key is safe to use in your frontend code
          </p>
        </div>

        <div>
          <Label htmlFor="secret-key">Secret Key *</Label>
          <Input
            id="secret-key"
            type="password"
            placeholder="sk_live_... or sk_test_..."
            value={credentials.secretKey}
            onChange={(e) => setCredentials({ ...credentials, secretKey: e.target.value })}
            className="font-mono text-sm"
          />
          <p className="text-xs text-muted-foreground mt-1">
            Keep this key secure - never share it publicly
          </p>
        </div>

        <div>
          <Label htmlFor="webhook-secret">Webhook Secret (Optional)</Label>
          <Input
            id="webhook-secret"
            placeholder="whsec_..."
            value={credentials.webhookSecret}
            onChange={(e) => setCredentials({ ...credentials, webhookSecret: e.target.value })}
            className="font-mono text-sm"
          />
          <p className="text-xs text-muted-foreground mt-1">
            Required for real-time event notifications
          </p>
        </div>

        <div className="flex gap-3">
          <Button
            onClick={handleExistingCredentials}
            disabled={isConnecting || !credentials.publishableKey || !credentials.secretKey}
          >
            {isConnecting ? (
              <>
                <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                Testing Connection...
              </>
            ) : (
              'Test & Connect'
            )}
          </Button>

          <Button 
            variant="outline"
            onClick={() => window.open('https://dashboard.stripe.com/apikeys', '_blank')}
          >
            Get API Keys
            <ExternalLink className="ml-2 h-4 w-4" />
          </Button>
        </div>

        {testResults && (
          <Alert className={testResults.error ? "border-red-200 bg-red-50" : "border-green-200 bg-green-50"}>
            {testResults.error ? (
              <AlertTriangle className="h-4 w-4 text-red-600" />
            ) : (
              <CheckCircle className="h-4 w-4 text-green-600" />
            )}
            <AlertDescription className={testResults.error ? "text-red-700" : "text-green-700"}>
              {testResults.error ? (
                <span>Connection failed: {testResults.error}</span>
              ) : (
                <div className="space-y-2">
                  <strong>Connection successful!</strong>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div>Account: {testResults.business_name}</div>
                    <div>Country: {testResults.country?.toUpperCase()}</div>
                    <div>Currency: {testResults.currency?.toUpperCase()}</div>
                    <div>Status: {testResults.charges_enabled ? 'Active' : 'Pending'}</div>
                  </div>
                </div>
              )}
            </AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="flex items-start gap-3">
        <CreditCard className="h-6 w-6 text-blue-600 mt-1" />
        <div>
          <h3 className="font-semibold text-lg">Connect Stripe Payments</h3>
          <p className="text-sm text-muted-foreground">
            Enable secure payment processing for your business
          </p>
        </div>
      </div>

      <Tabs value={setupMethod} onValueChange={(value) => setSetupMethod(value as SetupMethod)}>
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="connect" className="flex items-center gap-2">
            <Zap className="h-4 w-4" />
            Stripe Connect
            <Badge variant="secondary" className="text-xs">Recommended</Badge>
          </TabsTrigger>
          <TabsTrigger value="existing" className="flex items-center gap-2">
            <CreditCard className="h-4 w-4" />
            Existing Account
          </TabsTrigger>
        </TabsList>

        <TabsContent value="connect">
          {renderConnectMethod()}
        </TabsContent>

        <TabsContent value="existing">
          {renderExistingMethod()}
        </TabsContent>
      </Tabs>

      {/* What You'll Get */}
      <Card className="border-dashed">
        <CardHeader className="pb-3">
          <CardTitle className="text-sm">What You'll Get</CardTitle>
        </CardHeader>
        <CardContent className="pt-0">
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              'Accept 135+ currencies',
              'Recurring subscriptions',
              'Automated invoicing',
              'Fraud protection',
              'Mobile payments',
              'Real-time analytics',
              'Webhook notifications',
              'PCI compliance'
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
          disabled={connectionStatus !== 'success'}
        >
          Complete Setup
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}
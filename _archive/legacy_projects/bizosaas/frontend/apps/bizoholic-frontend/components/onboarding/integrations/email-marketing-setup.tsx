'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Checkbox } from '@/components/ui/checkbox'
import { 
  Mail, ExternalLink, CheckCircle, AlertTriangle, 
  Zap, Users, BarChart3, ArrowRight, RefreshCw
} from 'lucide-react'

interface EmailMarketingSetupProps {
  businessData: any
  onComplete: (data: any) => void
  onCancel: () => void
}

type EmailProvider = 'mailchimp' | 'sendgrid' | 'resend' | 'built_in'

interface EmailCredentials {
  provider: EmailProvider
  apiKey: string
  domain?: string
  fromEmail: string
  fromName: string
}

const EMAIL_PROVIDERS = {
  built_in: {
    name: 'BizoSaaS Email',
    description: 'Our built-in email system - ready to use immediately',
    icon: '🚀',
    features: ['Instant setup', 'Basic templates', 'Analytics', 'CAN-SPAM compliant'],
    setup_time: '1 minute',
    recommended: true
  },
  mailchimp: {
    name: 'Mailchimp',
    description: 'Popular email marketing platform with advanced automation',
    icon: '🐵',
    features: ['Advanced automation', 'A/B testing', 'Audience insights', 'Landing pages'],
    setup_time: '10 minutes',
    recommended: false
  },
  sendgrid: {
    name: 'SendGrid',
    description: 'Enterprise email delivery with high deliverability',
    icon: '📧',
    features: ['High deliverability', 'Transactional emails', 'Email validation', 'Analytics'],
    setup_time: '15 minutes',
    recommended: false
  },
  resend: {
    name: 'Resend',
    description: 'Developer-first email platform with modern API',
    icon: '⚡',
    features: ['Developer-friendly', 'React templates', 'Webhooks', 'High performance'],
    setup_time: '5 minutes',
    recommended: false
  }
}

export function EmailMarketingSetup({ businessData, onComplete, onCancel }: EmailMarketingSetupProps) {
  const [selectedProvider, setSelectedProvider] = useState<EmailProvider>('built_in')
  const [credentials, setCredentials] = useState<EmailCredentials>({
    provider: 'built_in',
    apiKey: '',
    fromEmail: '',
    fromName: businessData.companyName || '',
    domain: ''
  })
  const [isConnecting, setIsConnecting] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState<'idle' | 'connecting' | 'success' | 'error'>('idle')
  const [selectedFeatures, setSelectedFeatures] = useState<string[]>([
    'welcome_sequence',
    'newsletters',
    'campaign_updates'
  ])

  const handleProviderSelect = (provider: EmailProvider) => {
    setSelectedProvider(provider)
    setCredentials({ ...credentials, provider })
    setConnectionStatus('idle')
  }

  const handleConnect = async () => {
    setIsConnecting(true)
    setConnectionStatus('connecting')

    try {
      // Simulate connection process
      if (selectedProvider === 'built_in') {
        // Built-in email is always ready
        setTimeout(() => {
          setConnectionStatus('success')
          setCredentials({
            ...credentials,
            fromEmail: credentials.fromEmail || `hello@${businessData.companyName?.toLowerCase().replace(/\s+/g, '')}.com`,
            fromName: credentials.fromName || businessData.companyName
          })
          setIsConnecting(false)
        }, 1000)
      } else {
        // External providers need API validation
        setTimeout(() => {
          if (credentials.apiKey && credentials.fromEmail) {
            setConnectionStatus('success')
          } else {
            setConnectionStatus('error')
          }
          setIsConnecting(false)
        }, 2000)
      }
    } catch (error) {
      setConnectionStatus('error')
      setIsConnecting(false)
    }
  }

  const handleComplete = () => {
    const setupData = {
      provider: selectedProvider,
      credentials,
      features: selectedFeatures,
      connectedAt: new Date().toISOString(),
      emailLists: {
        main: `${businessData.companyName} Newsletter`,
        customers: `${businessData.companyName} Customers`,
        prospects: `${businessData.companyName} Prospects`
      }
    }
    
    onComplete(setupData)
  }

  const renderProviderCard = (provider: EmailProvider) => {
    const config = EMAIL_PROVIDERS[provider]
    const isSelected = selectedProvider === provider
    
    return (
      <Card 
        key={provider}
        className={`cursor-pointer transition-all ${
          isSelected ? 'ring-2 ring-blue-500 border-blue-200' : 'hover:shadow-md'
        }`}
        onClick={() => handleProviderSelect(provider)}
      >
        <CardHeader className="pb-2">
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-2xl">{config.icon}</span>
              <div>
                <div className="flex items-center gap-2">
                  {config.name}
                  {config.recommended && (
                    <Badge variant="default" className="text-xs">
                      Recommended
                    </Badge>
                  )}
                </div>
                <div className="text-xs text-muted-foreground font-normal">
                  Setup: {config.setup_time}
                </div>
              </div>
            </div>
            {isSelected && <CheckCircle className="h-5 w-5 text-blue-600" />}
          </CardTitle>
          <CardDescription>{config.description}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {config.features.map((feature) => (
              <div key={feature} className="flex items-center gap-2 text-sm text-muted-foreground">
                <CheckCircle className="h-3 w-3 text-green-500" />
                {feature}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  const renderCredentialsForm = () => {
    if (selectedProvider === 'built_in') {
      return (
        <div className="space-y-4">
          <Alert className="border-green-200 bg-green-50">
            <Zap className="h-4 w-4 text-green-600" />
            <AlertDescription className="text-green-700">
              <strong>Perfect choice!</strong> Our built-in email system is ready to use immediately. 
              We'll handle deliverability, compliance, and infrastructure for you.
            </AlertDescription>
          </Alert>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="from-name">From Name</Label>
              <Input
                id="from-name"
                placeholder="Your Company Name"
                value={credentials.fromName}
                onChange={(e) => setCredentials({ ...credentials, fromName: e.target.value })}
              />
              <p className="text-xs text-muted-foreground mt-1">
                This appears as the sender name
              </p>
            </div>

            <div>
              <Label htmlFor="from-email">From Email</Label>
              <Input
                id="from-email"
                placeholder="hello@yourcompany.com"
                value={credentials.fromEmail}
                onChange={(e) => setCredentials({ ...credentials, fromEmail: e.target.value })}
              />
              <p className="text-xs text-muted-foreground mt-1">
                We'll verify domain ownership
              </p>
            </div>
          </div>
        </div>
      )
    }

    return (
      <div className="space-y-4">
        <Alert className="border-blue-200 bg-blue-50">
          <Mail className="h-4 w-4 text-blue-600" />
          <AlertDescription className="text-blue-700">
            You'll need an API key from {EMAIL_PROVIDERS[selectedProvider].name}. 
            <Button 
              variant="link" 
              className="p-0 h-auto ml-1"
              onClick={() => {
                const urls = {
                  mailchimp: 'https://mailchimp.com/help/about-api-keys/',
                  sendgrid: 'https://docs.sendgrid.com/ui/account-and-settings/api-keys',
                  resend: 'https://resend.com/api-keys'
                }
                window.open(urls[selectedProvider], '_blank')
              }}
            >
              Get your API key here
              <ExternalLink className="ml-1 h-3 w-3" />
            </Button>
          </AlertDescription>
        </Alert>

        <div className="space-y-4">
          <div>
            <Label htmlFor="api-key">API Key *</Label>
            <Input
              id="api-key"
              type="password"
              placeholder={`${selectedProvider === 'mailchimp' ? 'abc123-us1' : 
                              selectedProvider === 'sendgrid' ? 'SG.abc123...' : 
                              're_abc123...'}`}
              value={credentials.apiKey}
              onChange={(e) => setCredentials({ ...credentials, apiKey: e.target.value })}
              className="font-mono"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="from-name-ext">From Name</Label>
              <Input
                id="from-name-ext"
                placeholder="Your Company Name"
                value={credentials.fromName}
                onChange={(e) => setCredentials({ ...credentials, fromName: e.target.value })}
              />
            </div>

            <div>
              <Label htmlFor="from-email-ext">From Email</Label>
              <Input
                id="from-email-ext"
                placeholder="hello@yourcompany.com"
                value={credentials.fromEmail}
                onChange={(e) => setCredentials({ ...credentials, fromEmail: e.target.value })}
              />
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-start gap-3">
        <Mail className="h-6 w-6 text-green-600 mt-1" />
        <div>
          <h3 className="font-semibold text-lg">Email Marketing Setup</h3>
          <p className="text-sm text-muted-foreground">
            Connect your email marketing platform for automated campaigns
          </p>
        </div>
      </div>

      {/* Provider Selection */}
      <div className="space-y-4">
        <h4 className="font-medium">Choose your email provider:</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(EMAIL_PROVIDERS).map(([provider, config]) => 
            renderProviderCard(provider as EmailProvider)
          )}
        </div>
      </div>

      {/* Credentials Form */}
      <div className="space-y-4">
        <h4 className="font-medium">Configuration:</h4>
        {renderCredentialsForm()}
      </div>

      {/* Email Features */}
      <div className="space-y-4">
        <h4 className="font-medium">Email automation features to enable:</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[
            { id: 'welcome_sequence', label: 'Welcome Email Sequence', desc: 'Automated onboarding emails' },
            { id: 'newsletters', label: 'Regular Newsletters', desc: 'Weekly/monthly updates' },
            { id: 'campaign_updates', label: 'Campaign Updates', desc: 'Performance notifications' },
            { id: 'abandoned_cart', label: 'Abandoned Cart Recovery', desc: 'Win back lost sales' },
            { id: 'birthday_emails', label: 'Birthday & Anniversary', desc: 'Personal touch campaigns' },
            { id: 'feedback_requests', label: 'Feedback Requests', desc: 'Customer satisfaction surveys' }
          ].map((feature) => (
            <div key={feature.id} className="flex items-start space-x-3 p-3 rounded-lg border">
              <Checkbox
                id={feature.id}
                checked={selectedFeatures.includes(feature.id)}
                onCheckedChange={(checked) => {
                  if (checked) {
                    setSelectedFeatures([...selectedFeatures, feature.id])
                  } else {
                    setSelectedFeatures(selectedFeatures.filter(f => f !== feature.id))
                  }
                }}
                className="mt-1"
              />
              <div className="flex-1">
                <Label htmlFor={feature.id} className="font-medium cursor-pointer">
                  {feature.label}
                </Label>
                <p className="text-sm text-muted-foreground">{feature.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Test Connection */}
      <div className="space-y-4">
        <Button
          onClick={handleConnect}
          disabled={isConnecting || connectionStatus === 'success'}
          className="w-full"
        >
          {isConnecting ? (
            <>
              <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
              Testing Connection...
            </>
          ) : connectionStatus === 'success' ? (
            <>
              <CheckCircle className="mr-2 h-4 w-4" />
              Connected Successfully
            </>
          ) : (
            'Test & Connect'
          )}
        </Button>

        {connectionStatus === 'success' && (
          <Alert className="border-green-200 bg-green-50">
            <CheckCircle className="h-4 w-4 text-green-600" />
            <AlertDescription className="text-green-700">
              <div className="space-y-2">
                <strong>Email marketing is ready!</strong>
                <div className="text-sm space-y-1">
                  <div>Provider: {EMAIL_PROVIDERS[selectedProvider].name}</div>
                  <div>From: {credentials.fromName} &lt;{credentials.fromEmail}&gt;</div>
                  <div>Features: {selectedFeatures.length} automation{selectedFeatures.length !== 1 ? 's' : ''} enabled</div>
                </div>
              </div>
            </AlertDescription>
          </Alert>
        )}

        {connectionStatus === 'error' && (
          <Alert className="border-red-200 bg-red-50">
            <AlertTriangle className="h-4 w-4 text-red-600" />
            <AlertDescription className="text-red-700">
              Connection failed. Please check your credentials and try again.
            </AlertDescription>
          </Alert>
        )}
      </div>

      {/* Preview */}
      {connectionStatus === 'success' && (
        <Card className="border-dashed">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              What You'll Get
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="grid grid-cols-2 gap-3 text-sm">
              {[
                'Automated welcome sequences',
                'Campaign performance tracking',
                'A/B testing capabilities',
                'CAN-SPAM compliance',
                'Unsubscribe management',
                'Email deliverability optimization',
                'Customer segmentation',
                'Template library'
              ].map((feature) => (
                <div key={feature} className="flex items-center gap-2">
                  <CheckCircle className="h-3 w-3 text-green-500" />
                  {feature}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

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
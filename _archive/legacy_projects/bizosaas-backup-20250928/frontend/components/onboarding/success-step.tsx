'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Progress } from '@/components/ui/progress'
import { 
  Rocket, CheckCircle, ArrowRight, ExternalLink, 
  Calendar, Users, BarChart3, Mail, CreditCard,
  Zap, Clock, Shield, Trophy, Sparkles
} from 'lucide-react'

interface SuccessStepProps {
  businessData: any
  integrationData: any
  onComplete: () => void
}

export function SuccessStep({ businessData, integrationData, onComplete }: SuccessStepProps) {
  const [countdown, setCountdown] = useState(5)
  const [isGeneratingInsights, setIsGeneratingInsights] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsGeneratingInsights(false)
    }, 3000)

    return () => clearTimeout(timer)
  }, [])

  useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000)
      return () => clearTimeout(timer)
    }
  }, [countdown])

  const completedIntegrations = integrationData?.completedIntegrations || []
  const totalIntegrations = 7 // Total available integrations
  const completionRate = (completedIntegrations.length / totalIntegrations) * 100

  const getIntegrationIcon = (integration: string) => {
    const icons: { [key: string]: React.ComponentType<{ className?: string }> } = {
      stripe: CreditCard,
      email_marketing: Mail,
      basic_analytics: BarChart3,
      google_ads: Zap,
      ecommerce: Shield
    }
    return icons[integration] || CheckCircle
  }

  const mockAIInsights = [
    {
      category: 'Quick Wins',
      insight: 'Based on your industry (Technology), implementing abandoned cart emails could increase revenue by 15-25%',
      priority: 'high',
      timeframe: '1-2 weeks'
    },
    {
      category: 'Audience Targeting',
      insight: 'Your target audience shows high engagement on LinkedIn - consider prioritizing LinkedIn Ads setup',
      priority: 'medium',
      timeframe: '2-3 weeks'
    },
    {
      category: 'Content Strategy',
      insight: 'Companies in your budget range see 40% better performance with video content in email campaigns',
      priority: 'medium',
      timeframe: '1 month'
    }
  ]

  return (
    <div className="space-y-8">
      {/* Success Header */}
      <div className="text-center space-y-4">
        <div className="flex justify-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-green-500 text-white">
            <Trophy className="h-8 w-8" />
          </div>
        </div>
        <div>
          <h2 className="text-2xl font-bold text-green-700">🎉 Congratulations!</h2>
          <p className="text-lg text-muted-foreground">
            Your AI marketing platform is ready to drive growth
          </p>
        </div>
      </div>

      {/* Setup Summary */}
      <Card className="border-green-200 bg-green-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-green-800">
            <Rocket className="h-5 w-5" />
            Platform Setup Complete
          </CardTitle>
          <CardDescription className="text-green-700">
            {businessData.companyName} is now powered by autonomous AI marketing
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Integration Progress</span>
              <Badge variant="default" className="bg-green-500">
                {completedIntegrations.length}/{totalIntegrations} Connected
              </Badge>
            </div>
            <Progress value={completionRate} className="h-2" />
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {completedIntegrations.map((integration: string) => {
                const Icon = getIntegrationIcon(integration)
                return (
                  <div key={integration} className="flex items-center gap-2 text-sm">
                    <Icon className="h-4 w-4 text-green-600" />
                    <span className="capitalize">{integration.replace('_', ' ')}</span>
                    <CheckCircle className="h-3 w-3 text-green-500 ml-auto" />
                  </div>
                )
              })}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* AI Insights Generation */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-purple-600" />
            AI Strategy Insights
            {isGeneratingInsights && <Badge variant="outline">Generating...</Badge>}
          </CardTitle>
          <CardDescription>
            Our AI has analyzed your business profile and created personalized recommendations
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isGeneratingInsights ? (
            <Alert className="border-blue-200 bg-blue-50">
              <Zap className="h-4 w-4 text-blue-600 animate-pulse" />
              <AlertDescription className="text-blue-700">
                <div className="space-y-2">
                  <strong>AI analyzing your business profile...</strong>
                  <div className="text-sm space-y-1">
                    • Processing industry benchmarks<br/>
                    • Analyzing target audience behavior<br/>
                    • Identifying growth opportunities<br/>
                    • Creating personalized strategy
                  </div>
                </div>
              </AlertDescription>
            </Alert>
          ) : (
            <div className="space-y-4">
              {mockAIInsights.map((insight, index) => (
                <Card key={index} className="border-l-4 border-l-purple-500">
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <Badge 
                        variant="outline" 
                        className={`${insight.priority === 'high' ? 'border-red-300 text-red-700' : 
                          'border-yellow-300 text-yellow-700'}`}
                      >
                        {insight.priority.toUpperCase()} PRIORITY
                      </Badge>
                      <div className="text-xs text-muted-foreground">
                        {insight.timeframe}
                      </div>
                    </div>
                    <h4 className="font-medium mb-2">{insight.category}</h4>
                    <p className="text-sm text-muted-foreground">{insight.insight}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Next Steps */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-sm">
              <Calendar className="h-4 w-4 text-blue-600" />
              Immediate Next Steps
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              'Review your AI-generated strategy recommendations',
              'Set up your first automated email campaign',
              'Configure payment processing for immediate sales',
              'Monitor real-time analytics dashboard',
              'Schedule onboarding call with success manager'
            ].map((step, index) => (
              <div key={index} className="flex items-start gap-3">
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-blue-100 text-blue-600 text-xs font-bold">
                  {index + 1}
                </div>
                <span className="text-sm">{step}</span>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-sm">
              <Users className="h-4 w-4 text-green-600" />
              Your Success Team
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="space-y-2">
              <div className="flex items-center gap-3">
                <div className="h-8 w-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white text-sm font-bold">
                  AI
                </div>
                <div>
                  <div className="font-medium text-sm">16 AI Marketing Specialists</div>
                  <div className="text-xs text-muted-foreground">Working 24/7 on your campaigns</div>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <div className="h-8 w-8 rounded-full bg-gradient-to-r from-green-500 to-blue-500 flex items-center justify-center text-white text-sm font-bold">
                  AH
                </div>
                <div>
                  <div className="font-medium text-sm">Alex Harris</div>
                  <div className="text-xs text-muted-foreground">Senior Marketing Strategist</div>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <div className="h-8 w-8 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center text-white text-sm font-bold">
                  24
                </div>
                <div>
                  <div className="font-medium text-sm">24/7 Support Team</div>
                  <div className="text-xs text-muted-foreground">Phone, email, and live chat</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Launch Dashboard */}
      <div className="text-center space-y-4">
        <Alert className="border-purple-200 bg-purple-50">
          <Trophy className="h-4 w-4 text-purple-600" />
          <AlertDescription className="text-purple-700">
            <strong>Your AI marketing system is now live!</strong> 
            Visit your dashboard to start creating campaigns, viewing analytics, and growing your business.
          </AlertDescription>
        </Alert>

        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Button 
            onClick={onComplete}
            size="lg"
            className="min-w-[200px] bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
          >
            Launch Dashboard
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
          
          <Button 
            variant="outline" 
            size="lg"
            onClick={() => window.open('https://calendar.bizosaas.com/onboarding', '_blank')}
          >
            Schedule Success Call
            <ExternalLink className="ml-2 h-4 w-4" />
          </Button>
        </div>

        {countdown > 0 && (
          <p className="text-xs text-muted-foreground">
            Auto-redirecting to dashboard in {countdown} seconds...
          </p>
        )}
      </div>

      {/* Support Information */}
      <Card className="border-dashed">
        <CardContent className="p-4 text-center">
          <p className="text-sm text-muted-foreground mb-2">
            Questions about your setup?
          </p>
          <div className="flex justify-center gap-4 text-sm">
            <Button variant="link" className="p-0 h-auto">
              📧 success@bizosaas.com
            </Button>
            <Button variant="link" className="p-0 h-auto">
              📞 (555) 123-BIZO
            </Button>
            <Button variant="link" className="p-0 h-auto">
              💬 Live Chat
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
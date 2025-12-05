"use client"

import React, { useState, useEffect } from 'react'
import { UseFormReturn } from 'react-hook-form'
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from '../../ui/card'
import { Button } from '../../ui/button'
import { Badge } from '../../ui/badge'
import { Input } from '../../ui/input'
import { 
  Monitor, 
  Bell, 
  DollarSign, 
  Activity, 
  AlertTriangle,
  CheckCircle,
  Mail,
  MessageSquare,
  Webhook,
  Clock,
  TrendingUp,
  Shield,
  Zap,
  Database,
  Globe,
  Settings,
  BarChart3,
  Users,
  Phone
} from 'lucide-react'
import { cn } from '../../../lib/utils'

interface MonitoringSetupStepProps {
  form: UseFormReturn<any>
  configurations: any[]
  setConfigurations: React.Dispatch<React.SetStateAction<any[]>>
}

interface AlertChannel {
  id: string
  type: 'email' | 'slack' | 'webhook' | 'sms' | 'teams'
  name: string
  icon: React.ReactNode
  description: string
  enabled: boolean
  config: Record<string, any>
  testStatus?: 'pending' | 'success' | 'error'
}

interface MonitoringRule {
  id: string
  name: string
  description: string
  metric: string
  condition: 'greater_than' | 'less_than' | 'equals' | 'not_equals'
  threshold: number
  unit: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  enabled: boolean
  cooldown: number // minutes
}

interface UsageThreshold {
  serviceId: string
  serviceName: string
  requests: {
    daily: number
    monthly: number
    enabled: boolean
  }
  cost: {
    daily: number
    monthly: number
    enabled: boolean
  }
  responseTime: {
    avgThreshold: number
    enabled: boolean
  }
  errorRate: {
    threshold: number
    enabled: boolean
  }
}

const ALERT_CHANNELS: AlertChannel[] = [
  {
    id: 'email',
    type: 'email',
    name: 'Email Notifications',
    icon: <Mail className="h-5 w-5" />,
    description: 'Send alerts via email to specified recipients',
    enabled: true,
    config: {
      recipients: ['admin@bizosaas.com'],
      template: 'default'
    }
  },
  {
    id: 'slack',
    type: 'slack',
    name: 'Slack Integration',
    icon: <MessageSquare className="h-5 w-5" />,
    description: 'Post alerts to Slack channels',
    enabled: false,
    config: {
      webhookUrl: '',
      channel: '#alerts',
      mention: '@channel'
    }
  },
  {
    id: 'webhook',
    type: 'webhook',
    name: 'Custom Webhooks',
    icon: <Webhook className="h-5 w-5" />,
    description: 'Send alerts to custom webhook endpoints',
    enabled: false,
    config: {
      url: '',
      method: 'POST',
      headers: {}
    }
  },
  {
    id: 'sms',
    type: 'sms',
    name: 'SMS Alerts',
    icon: <Phone className="h-5 w-5" />,
    description: 'Send critical alerts via SMS',
    enabled: false,
    config: {
      phoneNumbers: [],
      provider: 'twilio'
    }
  }
]

const DEFAULT_MONITORING_RULES: MonitoringRule[] = [
  {
    id: 'response_time',
    name: 'High Response Time',
    description: 'Alert when average response time exceeds threshold',
    metric: 'response_time_avg',
    condition: 'greater_than',
    threshold: 2000,
    unit: 'ms',
    severity: 'medium',
    enabled: true,
    cooldown: 15
  },
  {
    id: 'error_rate',
    name: 'High Error Rate',
    description: 'Alert when error rate exceeds acceptable levels',
    metric: 'error_rate',
    condition: 'greater_than',
    threshold: 5,
    unit: '%',
    severity: 'high',
    enabled: true,
    cooldown: 10
  },
  {
    id: 'rate_limit',
    name: 'Rate Limit Exceeded',
    description: 'Alert when API rate limits are hit',
    metric: 'rate_limit_hit',
    condition: 'greater_than',
    threshold: 0,
    unit: 'count',
    severity: 'high',
    enabled: true,
    cooldown: 5
  },
  {
    id: 'auth_failures',
    name: 'Authentication Failures',
    description: 'Alert on suspicious authentication failure patterns',
    metric: 'auth_failures',
    condition: 'greater_than',
    threshold: 10,
    unit: 'count/hour',
    severity: 'critical',
    enabled: true,
    cooldown: 5
  },
  {
    id: 'quota_usage',
    name: 'API Quota Usage',
    description: 'Alert when approaching API quota limits',
    metric: 'quota_usage',
    condition: 'greater_than',
    threshold: 80,
    unit: '%',
    severity: 'medium',
    enabled: true,
    cooldown: 60
  }
]

export function MonitoringSetupStep({ 
  form,
  configurations,
  setConfigurations
}: MonitoringSetupStepProps) {
  const [alertChannels, setAlertChannels] = useState<AlertChannel[]>(ALERT_CHANNELS)
  const [monitoringRules, setMonitoringRules] = useState<MonitoringRule[]>(DEFAULT_MONITORING_RULES)
  const [usageThresholds, setUsageThresholds] = useState<UsageThreshold[]>([])
  const [isTestingChannels, setIsTestingChannels] = useState(false)
  const [customThresholds, setCustomThresholds] = useState<Record<string, any>>({})

  const formData = form.watch()
  const selectedServices = formData.selectedServices || []

  useEffect(() => {
    initializeUsageThresholds()
  }, [selectedServices])

  const initializeUsageThresholds = () => {
    const thresholds: UsageThreshold[] = selectedServices.map((serviceId: string) => ({
      serviceId,
      serviceName: getServiceName(serviceId),
      requests: {
        daily: getDefaultRequestThreshold(serviceId, 'daily'),
        monthly: getDefaultRequestThreshold(serviceId, 'monthly'),
        enabled: true
      },
      cost: {
        daily: getDefaultCostThreshold(serviceId, 'daily'),
        monthly: getDefaultCostThreshold(serviceId, 'monthly'),
        enabled: true
      },
      responseTime: {
        avgThreshold: 2000,
        enabled: true
      },
      errorRate: {
        threshold: 5,
        enabled: true
      }
    }))
    
    setUsageThresholds(thresholds)
  }

  const getServiceName = (serviceId: string): string => {
    const serviceNames: Record<string, string> = {
      stripe: 'Stripe',
      paypal: 'PayPal',
      'google-ads': 'Google Ads',
      openai: 'OpenAI',
      'facebook-ads': 'Meta Ads',
      anthropic: 'Anthropic Claude'
    }
    return serviceNames[serviceId] || serviceId
  }

  const getDefaultRequestThreshold = (serviceId: string, period: 'daily' | 'monthly'): number => {
    const defaults: Record<string, { daily: number, monthly: number }> = {
      stripe: { daily: 10000, monthly: 300000 },
      paypal: { daily: 5000, monthly: 150000 },
      'google-ads': { daily: 50000, monthly: 1500000 },
      openai: { daily: 1000, monthly: 30000 },
      'facebook-ads': { daily: 25000, monthly: 750000 },
      anthropic: { daily: 500, monthly: 15000 }
    }
    return defaults[serviceId]?.[period] || (period === 'daily' ? 1000 : 30000)
  }

  const getDefaultCostThreshold = (serviceId: string, period: 'daily' | 'monthly'): number => {
    const defaults: Record<string, { daily: number, monthly: number }> = {
      stripe: { daily: 100, monthly: 3000 },
      paypal: { daily: 50, monthly: 1500 },
      'google-ads': { daily: 500, monthly: 15000 },
      openai: { daily: 100, monthly: 3000 },
      'facebook-ads': { daily: 300, monthly: 9000 },
      anthropic: { daily: 50, monthly: 1500 }
    }
    return defaults[serviceId]?.[period] || (period === 'daily' ? 50 : 1500)
  }

  const toggleAlertChannel = (channelId: string) => {
    setAlertChannels(prev => prev.map(channel => 
      channel.id === channelId 
        ? { ...channel, enabled: !channel.enabled }
        : channel
    ))
  }

  const updateChannelConfig = (channelId: string, config: Record<string, any>) => {
    setAlertChannels(prev => prev.map(channel => 
      channel.id === channelId 
        ? { ...channel, config: { ...channel.config, ...config } }
        : channel
    ))
  }

  const toggleMonitoringRule = (ruleId: string) => {
    setMonitoringRules(prev => prev.map(rule => 
      rule.id === ruleId 
        ? { ...rule, enabled: !rule.enabled }
        : rule
    ))
  }

  const updateMonitoringRule = (ruleId: string, updates: Partial<MonitoringRule>) => {
    setMonitoringRules(prev => prev.map(rule => 
      rule.id === ruleId 
        ? { ...rule, ...updates }
        : rule
    ))
  }

  const updateUsageThreshold = (serviceId: string, section: string, field: string, value: any) => {
    setUsageThresholds(prev => prev.map(threshold => 
      threshold.serviceId === serviceId 
        ? {
            ...threshold,
            [section]: {
              ...((threshold as any)[section] || {}),
              [field]: value
            }
          }
        : threshold
    ))
  }

  const testAlertChannels = async () => {
    setIsTestingChannels(true)
    
    for (const channel of alertChannels.filter(c => c.enabled)) {
      setAlertChannels(prev => prev.map(c => 
        c.id === channel.id 
          ? { ...c, testStatus: 'pending' }
          : c
      ))
      
      // Simulate test
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const success = Math.random() > 0.2 // 80% success rate
      setAlertChannels(prev => prev.map(c => 
        c.id === channel.id 
          ? { ...c, testStatus: success ? 'success' : 'error' }
          : c
      ))
    }
    
    setIsTestingChannels(false)
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'text-red-600 bg-red-50 border-red-200'
      case 'high':
        return 'text-orange-600 bg-orange-50 border-orange-200'
      case 'medium':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      case 'low':
        return 'text-blue-600 bg-blue-50 border-blue-200'
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  const getTotalEnabledChannels = () => alertChannels.filter(c => c.enabled).length
  const getTotalEnabledRules = () => monitoringRules.filter(r => r.enabled).length

  return (
    <div className="space-y-6">
      {/* Monitoring Overview */}
      <Card className="border-green-200 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-950 dark:to-emerald-950">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Monitor className="h-5 w-5 text-green-600" />
            <span>Monitoring & Alerting Configuration</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{selectedServices.length}</div>
              <div className="text-sm text-gray-600">Services</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{getTotalEnabledChannels()}</div>
              <div className="text-sm text-gray-600">Alert Channels</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">{getTotalEnabledRules()}</div>
              <div className="text-sm text-gray-600">Monitoring Rules</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">24/7</div>
              <div className="text-sm text-gray-600">Coverage</div>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <CheckCircle className="h-5 w-5 text-green-600" />
            <span className="text-sm font-medium text-green-800 dark:text-green-200">
              Real-time monitoring and alerting will be activated
            </span>
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              Enterprise Grade
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* Alert Channels Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Bell className="h-5 w-5" />
              <span>Alert Channels</span>
            </div>
            <Button
              variant="outline"
              onClick={testAlertChannels}
              disabled={isTestingChannels || getTotalEnabledChannels() === 0}
            >
              {isTestingChannels ? (
                <Activity className="h-4 w-4 mr-2 animate-pulse" />
              ) : (
                <Zap className="h-4 w-4 mr-2" />
              )}
              Test Channels
            </Button>
          </CardTitle>
          <CardDescription>
            Configure how and where to receive alerts
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {alertChannels.map(channel => (
              <Card key={channel.id} className={cn(
                "transition-all duration-200",
                channel.enabled 
                  ? "ring-1 ring-blue-200 bg-blue-50 dark:bg-blue-950" 
                  : "bg-gray-50 dark:bg-gray-800"
              )}>
                <CardContent className="p-4">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className={cn(
                        "p-2 rounded-lg",
                        channel.enabled ? "bg-blue-100 text-blue-600" : "bg-gray-200 text-gray-500"
                      )}>
                        {channel.icon}
                      </div>
                      <div>
                        <h4 className="font-medium">{channel.name}</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {channel.description}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      {channel.testStatus && (
                        <div className="flex items-center space-x-1">
                          {channel.testStatus === 'pending' && (
                            <Activity className="h-4 w-4 text-blue-500 animate-pulse" />
                          )}
                          {channel.testStatus === 'success' && (
                            <CheckCircle className="h-4 w-4 text-green-500" />
                          )}
                          {channel.testStatus === 'error' && (
                            <AlertTriangle className="h-4 w-4 text-red-500" />
                          )}
                        </div>
                      )}
                      
                      <Button
                        variant={channel.enabled ? "default" : "outline"}
                        size="sm"
                        onClick={() => toggleAlertChannel(channel.id)}
                      >
                        {channel.enabled ? 'Enabled' : 'Enable'}
                      </Button>
                    </div>
                  </div>
                  
                  {channel.enabled && (
                    <div className="space-y-3 pl-11">
                      {channel.type === 'email' && (
                        <div>
                          <label className="block text-sm font-medium mb-1">
                            Email Recipients
                          </label>
                          <Input
                            placeholder="Enter email addresses separated by commas"
                            value={channel.config.recipients?.join(', ') || ''}
                            onChange={(e) => updateChannelConfig(channel.id, {
                              recipients: e.target.value.split(',').map(email => email.trim())
                            })}
                          />
                        </div>
                      )}
                      
                      {channel.type === 'slack' && (
                        <div className="space-y-2">
                          <div>
                            <label className="block text-sm font-medium mb-1">
                              Webhook URL
                            </label>
                            <Input
                              placeholder="https://hooks.slack.com/services/..."
                              value={channel.config.webhookUrl || ''}
                              onChange={(e) => updateChannelConfig(channel.id, {
                                webhookUrl: e.target.value
                              })}
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium mb-1">
                              Channel
                            </label>
                            <Input
                              placeholder="#alerts"
                              value={channel.config.channel || ''}
                              onChange={(e) => updateChannelConfig(channel.id, {
                                channel: e.target.value
                              })}
                            />
                          </div>
                        </div>
                      )}
                      
                      {channel.type === 'webhook' && (
                        <div>
                          <label className="block text-sm font-medium mb-1">
                            Webhook URL
                          </label>
                          <Input
                            placeholder="https://your-webhook-endpoint.com/alerts"
                            value={channel.config.url || ''}
                            onChange={(e) => updateChannelConfig(channel.id, {
                              url: e.target.value
                            })}
                          />
                        </div>
                      )}
                      
                      {channel.type === 'sms' && (
                        <div>
                          <label className="block text-sm font-medium mb-1">
                            Phone Numbers
                          </label>
                          <Input
                            placeholder="+1234567890, +0987654321"
                            value={channel.config.phoneNumbers?.join(', ') || ''}
                            onChange={(e) => updateChannelConfig(channel.id, {
                              phoneNumbers: e.target.value.split(',').map(phone => phone.trim())
                            })}
                          />
                        </div>
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Usage Thresholds */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <BarChart3 className="h-5 w-5" />
            <span>Usage Thresholds</span>
          </CardTitle>
          <CardDescription>
            Set limits for API usage, costs, and performance metrics
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {usageThresholds.map(threshold => (
              <div key={threshold.serviceId} className="border rounded-lg p-4">
                <h4 className="font-medium mb-4">{threshold.serviceName} Thresholds</h4>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Request Limits */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h5 className="text-sm font-medium">Request Limits</h5>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => updateUsageThreshold(threshold.serviceId, 'requests', 'enabled', !threshold.requests.enabled)}
                      >
                        {threshold.requests.enabled ? 'Enabled' : 'Disabled'}
                      </Button>
                    </div>
                    
                    {threshold.requests.enabled && (
                      <div className="space-y-2">
                        <div>
                          <label className="block text-xs text-gray-600 mb-1">Daily Limit</label>
                          <Input
                            type="number"
                            value={threshold.requests.daily}
                            onChange={(e) => updateUsageThreshold(threshold.serviceId, 'requests', 'daily', parseInt(e.target.value))}
                          />
                        </div>
                        <div>
                          <label className="block text-xs text-gray-600 mb-1">Monthly Limit</label>
                          <Input
                            type="number"
                            value={threshold.requests.monthly}
                            onChange={(e) => updateUsageThreshold(threshold.serviceId, 'requests', 'monthly', parseInt(e.target.value))}
                          />
                        </div>
                      </div>
                    )}
                  </div>
                  
                  {/* Cost Limits */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h5 className="text-sm font-medium">Cost Limits (USD)</h5>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => updateUsageThreshold(threshold.serviceId, 'cost', 'enabled', !threshold.cost.enabled)}
                      >
                        {threshold.cost.enabled ? 'Enabled' : 'Disabled'}
                      </Button>
                    </div>
                    
                    {threshold.cost.enabled && (
                      <div className="space-y-2">
                        <div>
                          <label className="block text-xs text-gray-600 mb-1">Daily Budget</label>
                          <Input
                            type="number"
                            value={threshold.cost.daily}
                            onChange={(e) => updateUsageThreshold(threshold.serviceId, 'cost', 'daily', parseFloat(e.target.value))}
                          />
                        </div>
                        <div>
                          <label className="block text-xs text-gray-600 mb-1">Monthly Budget</label>
                          <Input
                            type="number"
                            value={threshold.cost.monthly}
                            onChange={(e) => updateUsageThreshold(threshold.serviceId, 'cost', 'monthly', parseFloat(e.target.value))}
                          />
                        </div>
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
                  {/* Response Time */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h5 className="text-sm font-medium">Response Time Alert</h5>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => updateUsageThreshold(threshold.serviceId, 'responseTime', 'enabled', !threshold.responseTime.enabled)}
                      >
                        {threshold.responseTime.enabled ? 'Enabled' : 'Disabled'}
                      </Button>
                    </div>
                    
                    {threshold.responseTime.enabled && (
                      <div>
                        <label className="block text-xs text-gray-600 mb-1">Threshold (ms)</label>
                        <Input
                          type="number"
                          value={threshold.responseTime.avgThreshold}
                          onChange={(e) => updateUsageThreshold(threshold.serviceId, 'responseTime', 'avgThreshold', parseInt(e.target.value))}
                        />
                      </div>
                    )}
                  </div>
                  
                  {/* Error Rate */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h5 className="text-sm font-medium">Error Rate Alert</h5>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => updateUsageThreshold(threshold.serviceId, 'errorRate', 'enabled', !threshold.errorRate.enabled)}
                      >
                        {threshold.errorRate.enabled ? 'Enabled' : 'Disabled'}
                      </Button>
                    </div>
                    
                    {threshold.errorRate.enabled && (
                      <div>
                        <label className="block text-xs text-gray-600 mb-1">Threshold (%)</label>
                        <Input
                          type="number"
                          value={threshold.errorRate.threshold}
                          onChange={(e) => updateUsageThreshold(threshold.serviceId, 'errorRate', 'threshold', parseFloat(e.target.value))}
                        />
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Monitoring Rules */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Shield className="h-5 w-5" />
            <span>Security & Performance Rules</span>
          </CardTitle>
          <CardDescription>
            Advanced monitoring rules for security and performance
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {monitoringRules.map(rule => (
              <div key={rule.id} className={cn(
                "flex items-center justify-between p-4 border rounded-lg",
                rule.enabled ? "bg-blue-50 dark:bg-blue-950 border-blue-200" : "bg-gray-50 dark:bg-gray-800"
              )}>
                <div className="flex items-center space-x-3">
                  <div className={cn(
                    "p-2 rounded-lg",
                    rule.enabled ? getSeverityColor(rule.severity) : "bg-gray-200 text-gray-500"
                  )}>
                    <AlertTriangle className="h-4 w-4" />
                  </div>
                  <div>
                    <h4 className="font-medium">{rule.name}</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{rule.description}</p>
                    <div className="flex items-center space-x-2 mt-1">
                      <Badge variant="outline" className="text-xs">
                        {rule.metric}
                      </Badge>
                      <Badge variant="outline" className="text-xs">
                        {rule.condition} {rule.threshold} {rule.unit}
                      </Badge>
                      <Badge variant="outline" className={cn("text-xs", getSeverityColor(rule.severity))}>
                        {rule.severity}
                      </Badge>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <div className="flex items-center space-x-2 text-sm">
                    <Clock className="h-4 w-4 text-gray-400" />
                    <span>{rule.cooldown}m cooldown</span>
                  </div>
                  <Button
                    variant={rule.enabled ? "default" : "outline"}
                    size="sm"
                    onClick={() => toggleMonitoringRule(rule.id)}
                  >
                    {rule.enabled ? 'Enabled' : 'Enable'}
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Monitoring Dashboard Preview */}
      <Card className="border-purple-200 bg-purple-50 dark:bg-purple-950 dark:border-purple-800">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5 text-purple-600" />
            <span>Monitoring Dashboard Preview</span>
          </CardTitle>
          <CardDescription>
            Your monitoring setup will provide these insights
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 border rounded-lg bg-white dark:bg-gray-800">
              <Activity className="h-8 w-8 text-blue-500 mx-auto mb-2" />
              <h4 className="font-medium">Real-time Metrics</h4>
              <p className="text-sm text-gray-600">Live API performance data</p>
            </div>
            
            <div className="text-center p-4 border rounded-lg bg-white dark:bg-gray-800">
              <Bell className="h-8 w-8 text-yellow-500 mx-auto mb-2" />
              <h4 className="font-medium">Smart Alerts</h4>
              <p className="text-sm text-gray-600">Proactive issue detection</p>
            </div>
            
            <div className="text-center p-4 border rounded-lg bg-white dark:bg-gray-800">
              <BarChart3 className="h-8 w-8 text-green-500 mx-auto mb-2" />
              <h4 className="font-medium">Usage Analytics</h4>
              <p className="text-sm text-gray-600">Cost and usage insights</p>
            </div>
          </div>
          
          <div className="mt-4 p-3 bg-purple-100 dark:bg-purple-900 rounded-lg">
            <div className="flex items-center space-x-2">
              <Database className="h-4 w-4 text-purple-600" />
              <span className="text-sm font-medium text-purple-800 dark:text-purple-200">
                All monitoring data will be stored securely with 90-day retention
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default MonitoringSetupStep
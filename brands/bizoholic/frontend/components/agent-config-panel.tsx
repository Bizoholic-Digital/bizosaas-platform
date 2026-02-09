'use client'

import { useState, useEffect } from 'react'
// import { AIAgent, AgentConfig } from '@/lib/api/agents-api'
// import { useAgents } from '@/hooks/use-agents'

// Stub interfaces for missing lib
export interface AgentConfig {
  enabled: boolean;
  parameters: Record<string, any>;
  schedule?: {
    type: 'manual' | 'interval' | 'cron';
    value: string;
  };
  notifications: {
    onSuccess: boolean;
    onError: boolean;
    onWarning: boolean;
    email?: string;
    webhook?: string;
  };
  limits: {
    maxExecutionTime: number;
    maxRetries: number;
    rateLimit?: number;
  };
  integrations: Record<string, { enabled: boolean; config: any }>;
}

export interface AIAgent {
  id: string;
  name: string;
  config: AgentConfig;
}

// Stub hook for missing hook
const useAgents = () => ({
  updateAgentConfig: async (id: string, config: any) => {
    console.log('Stub updateAgentConfig', id, config);
    return Promise.resolve();
  }
});
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import {
  Settings,
  Save,
  RefreshCw,
  Clock,
  Bell,
  Shield,
  Plug,
  AlertTriangle,
  CheckCircle,
  Info
} from 'lucide-react'

interface AgentConfigPanelProps {
  agent: AIAgent
  onConfigUpdate?: (agentId: string, config: Partial<AgentConfig>) => void
}

export function AgentConfigPanel({ agent, onConfigUpdate }: AgentConfigPanelProps) {
  const [config, setConfig] = useState<AgentConfig>(agent.config)
  const [loading, setLoading] = useState(false)
  const [saved, setSaved] = useState(false)
  const { updateAgentConfig } = useAgents()

  useEffect(() => {
    setConfig(agent.config)
  }, [agent.config])

  const handleSave = async () => {
    try {
      setLoading(true)
      await updateAgentConfig(agent.id, config)
      onConfigUpdate?.(agent.id, config)
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } catch (error) {
      console.error('Failed to save config:', error)
    } finally {
      setLoading(false)
    }
  }

  const updateConfig = (path: string, value: any) => {
    setConfig(prev => {
      const newConfig = { ...prev }
      const keys = path.split('.')
      let current = newConfig as any

      for (let i = 0; i < keys.length - 1; i++) {
        if (!(keys[i] in current)) {
          current[keys[i]] = {}
        }
        current = current[keys[i]]
      }

      current[keys[keys.length - 1]] = value
      return newConfig
    })
  }

  const getScheduleDisplay = () => {
    if (!config.schedule) return 'Manual execution only'
    if (config.schedule.type === 'manual') return 'Manual execution only'
    if (config.schedule.type === 'interval') return `Every ${config.schedule.value} minutes`
    if (config.schedule.type === 'cron') return `Cron: ${config.schedule.value}`
    return 'Unknown schedule'
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm">
          <Settings className="h-4 w-4 mr-2" />
          Configure
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            Configure {agent.name}
          </DialogTitle>
          <DialogDescription>
            Customize settings, schedule, and integrations for this AI agent
          </DialogDescription>
        </DialogHeader>

        <Tabs defaultValue="general" className="w-full">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="general">General</TabsTrigger>
            <TabsTrigger value="schedule">Schedule</TabsTrigger>
            <TabsTrigger value="notifications">Notifications</TabsTrigger>
            <TabsTrigger value="limits">Limits</TabsTrigger>
            <TabsTrigger value="integrations">Integrations</TabsTrigger>
          </TabsList>

          {/* General Settings */}
          <TabsContent value="general" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">General Settings</CardTitle>
                <CardDescription>Basic configuration options for the agent</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label className="text-base">Enable Agent</Label>
                    <div className="text-sm text-muted-foreground">
                      Turn the agent on or off
                    </div>
                  </div>
                  <Switch
                    checked={config.enabled}
                    onCheckedChange={(checked) => updateConfig('enabled', checked)}
                  />
                </div>

                <Separator />

                <div className="space-y-2">
                  <Label>Agent Parameters</Label>
                  <div className="space-y-2">
                    {Object.entries(config.parameters).map(([key, value]) => (
                      <div key={key} className="flex items-center gap-2">
                        <Label className="w-32 text-sm">{key}</Label>
                        <Input
                          value={typeof value === 'object' ? JSON.stringify(value) : String(value)}
                          onChange={(e) => {
                            try {
                              const parsed = JSON.parse(e.target.value)
                              updateConfig(`parameters.${key}`, parsed)
                            } catch {
                              updateConfig(`parameters.${key}`, e.target.value)
                            }
                          }}
                          className="flex-1"
                        />
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Schedule Settings */}
          <TabsContent value="schedule" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Clock className="h-5 w-5" />
                  Schedule Configuration
                </CardTitle>
                <CardDescription>
                  Set when and how often the agent should run
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label>Schedule Type</Label>
                  <Select
                    value={config.schedule?.type || 'manual'}
                    onValueChange={(value) => updateConfig('schedule.type', value)}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select schedule type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="manual">Manual Only</SelectItem>
                      <SelectItem value="interval">Interval</SelectItem>
                      <SelectItem value="cron">Cron Expression</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {config.schedule?.type === 'interval' && (
                  <div className="space-y-2">
                    <Label>Interval (minutes)</Label>
                    <Input
                      type="number"
                      value={config.schedule.value || '60'}
                      onChange={(e) => updateConfig('schedule.value', e.target.value)}
                      placeholder="60"
                    />
                  </div>
                )}

                {config.schedule?.type === 'cron' && (
                  <div className="space-y-2">
                    <Label>Cron Expression</Label>
                    <Input
                      value={config.schedule.value || '0 */4 * * *'}
                      onChange={(e) => updateConfig('schedule.value', e.target.value)}
                      placeholder="0 */4 * * *"
                    />
                    <div className="text-sm text-muted-foreground">
                      Current schedule: {getScheduleDisplay()}
                    </div>
                  </div>
                )}

                <div className="bg-blue-50 p-3 rounded-md">
                  <div className="flex items-start gap-2">
                    <Info className="h-4 w-4 text-blue-600 mt-0.5" />
                    <div className="text-sm text-blue-800">
                      <strong>Current Schedule:</strong> {getScheduleDisplay()}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Notifications Settings */}
          <TabsContent value="notifications" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Bell className="h-5 w-5" />
                  Notification Settings
                </CardTitle>
                <CardDescription>
                  Configure when and how to receive notifications
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label className="text-base">Success Notifications</Label>
                    <div className="text-sm text-muted-foreground">
                      Notify when tasks complete successfully
                    </div>
                  </div>
                  <Switch
                    checked={config.notifications.onSuccess}
                    onCheckedChange={(checked) => updateConfig('notifications.onSuccess', checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label className="text-base">Error Notifications</Label>
                    <div className="text-sm text-muted-foreground">
                      Notify when tasks fail or encounter errors
                    </div>
                  </div>
                  <Switch
                    checked={config.notifications.onError}
                    onCheckedChange={(checked) => updateConfig('notifications.onError', checked)}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label className="text-base">Warning Notifications</Label>
                    <div className="text-sm text-muted-foreground">
                      Notify about warnings and potential issues
                    </div>
                  </div>
                  <Switch
                    checked={config.notifications.onWarning}
                    onCheckedChange={(checked) => updateConfig('notifications.onWarning', checked)}
                  />
                </div>

                <Separator />

                <div className="space-y-2">
                  <Label>Email Notifications</Label>
                  <Input
                    type="email"
                    value={config.notifications.email || ''}
                    onChange={(e) => updateConfig('notifications.email', e.target.value)}
                    placeholder="your@email.com"
                  />
                </div>

                <div className="space-y-2">
                  <Label>Webhook URL</Label>
                  <Input
                    value={config.notifications.webhook || ''}
                    onChange={(e) => updateConfig('notifications.webhook', e.target.value)}
                    placeholder="https://your-webhook-url.com"
                  />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Limits Settings */}
          <TabsContent value="limits" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  Execution Limits
                </CardTitle>
                <CardDescription>
                  Set safety limits and resource constraints
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label>Max Execution Time (seconds)</Label>
                  <Input
                    type="number"
                    value={config.limits.maxExecutionTime}
                    onChange={(e) => updateConfig('limits.maxExecutionTime', parseInt(e.target.value))}
                    placeholder="3600"
                  />
                </div>

                <div className="space-y-2">
                  <Label>Max Retries</Label>
                  <Input
                    type="number"
                    value={config.limits.maxRetries}
                    onChange={(e) => updateConfig('limits.maxRetries', parseInt(e.target.value))}
                    placeholder="3"
                  />
                </div>

                <div className="space-y-2">
                  <Label>Rate Limit (requests per minute)</Label>
                  <Input
                    type="number"
                    value={config.limits.rateLimit || ''}
                    onChange={(e) => updateConfig('limits.rateLimit', e.target.value ? parseInt(e.target.value) : undefined)}
                    placeholder="60"
                  />
                </div>

                <div className="bg-yellow-50 p-3 rounded-md">
                  <div className="flex items-start gap-2">
                    <AlertTriangle className="h-4 w-4 text-yellow-600 mt-0.5" />
                    <div className="text-sm text-yellow-800">
                      <strong>Warning:</strong> Setting limits too low may cause task failures.
                      Monitor agent performance after making changes.
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Integrations Settings */}
          <TabsContent value="integrations" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Plug className="h-5 w-5" />
                  Integration Settings
                </CardTitle>
                <CardDescription>
                  Configure external service integrations
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {Object.entries(config.integrations).map(([integrationName, integrationConfig]) => (
                  <div key={integrationName} className="border rounded-lg p-4 space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Badge variant="secondary">{integrationName}</Badge>
                        {integrationConfig.enabled ? (
                          <CheckCircle className="h-4 w-4 text-green-600" />
                        ) : (
                          <AlertTriangle className="h-4 w-4 text-gray-400" />
                        )}
                      </div>
                      <Switch
                        checked={integrationConfig.enabled}
                        onCheckedChange={(checked) =>
                          updateConfig(`integrations.${integrationName}.enabled`, checked)
                        }
                      />
                    </div>

                    {integrationConfig.enabled && (
                      <div className="space-y-2">
                        <Label className="text-sm">Configuration</Label>
                        <Textarea
                          value={JSON.stringify(integrationConfig.config, null, 2)}
                          onChange={(e) => {
                            try {
                              const parsed = JSON.parse(e.target.value)
                              updateConfig(`integrations.${integrationName}.config`, parsed)
                            } catch {
                              // Ignore invalid JSON
                            }
                          }}
                          placeholder="{}"
                          className="font-mono text-sm"
                          rows={3}
                        />
                      </div>
                    )}
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        <DialogFooter className="flex gap-2">
          <Button variant="outline" onClick={() => setConfig(agent.config)}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Reset
          </Button>
          <Button onClick={handleSave} disabled={loading}>
            {loading ? (
              <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
            ) : saved ? (
              <CheckCircle className="h-4 w-4 mr-2" />
            ) : (
              <Save className="h-4 w-4 mr-2" />
            )}
            {saved ? 'Saved!' : 'Save Configuration'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Badge } from '../ui/badge'
import { Input } from '../ui/input'
import { Label } from '../ui'
import {
  Settings,
  Play,
  Pause,
  Square,
  RotateCcw,
  Save,
  X,
  AlertTriangle,
  CheckCircle,
  Clock,
  Zap,
  Cpu,
  HardDrive,
  Network,
  Eye,
  EyeOff,
  Upload,
  Download,
  RefreshCw,
  Power,
  Activity
} from 'lucide-react'

interface AgentControlsProps {
  agentId: string
  onClose: () => void
}

interface AgentConfig {
  name: string
  description: string
  enabled: boolean
  autoRestart: boolean
  maxRetries: number
  timeout: number
  memoryLimit: number
  cpuLimit: number
  logLevel: string
  priority: number
  dependencies: string[]
  environment: Record<string, string>
  schedule?: string
}

interface AgentStatus {
  status: 'active' | 'inactive' | 'error' | 'starting' | 'stopping'
  uptime: number
  memoryUsage: number
  cpuUsage: number
  lastHeartbeat: string
  errorCount: number
  restartCount: number
  version: string
}

export function AgentControls({ agentId, onClose }: AgentControlsProps) {
  const [config, setConfig] = useState<AgentConfig>({
    name: 'Lead Scoring Agent',
    description: 'AI-powered lead qualification and scoring system',
    enabled: true,
    autoRestart: true,
    maxRetries: 3,
    timeout: 30000,
    memoryLimit: 512,
    cpuLimit: 1,
    logLevel: 'info',
    priority: 5,
    dependencies: ['crm-supervisor', 'data-collection'],
    environment: {
      API_KEY: '***hidden***',
      MODEL_VERSION: '2.1.0',
      BATCH_SIZE: '50'
    }
  })

  const [status, setStatus] = useState<AgentStatus>({
    status: 'active',
    uptime: 86400000, // 24 hours in milliseconds
    memoryUsage: 245,
    cpuUsage: 15,
    lastHeartbeat: new Date().toISOString(),
    errorCount: 2,
    restartCount: 1,
    version: '1.4.2'
  })

  const [isLoading, setIsLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('status')
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const [showSensitiveData, setShowSensitiveData] = useState(false)

  useEffect(() => {
    // Simulate real-time status updates
    const interval = setInterval(() => {
      setStatus(prev => ({
        ...prev,
        lastHeartbeat: new Date().toISOString(),
        memoryUsage: Math.max(200, Math.min(500, prev.memoryUsage + (Math.random() - 0.5) * 20)),
        cpuUsage: Math.max(0, Math.min(100, prev.cpuUsage + (Math.random() - 0.5) * 10)),
        uptime: prev.uptime + 5000
      }))
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const formatUptime = (milliseconds: number) => {
    const days = Math.floor(milliseconds / (24 * 60 * 60 * 1000))
    const hours = Math.floor((milliseconds % (24 * 60 * 60 * 1000)) / (60 * 60 * 1000))
    const minutes = Math.floor((milliseconds % (60 * 60 * 1000)) / (60 * 1000))
    
    if (days > 0) return `${days}d ${hours}h ${minutes}m`
    if (hours > 0) return `${hours}h ${minutes}m`
    return `${minutes}m`
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'inactive':
        return <Pause className="h-5 w-5 text-gray-500" />
      case 'error':
        return <AlertTriangle className="h-5 w-5 text-red-500" />
      case 'starting':
        return <Clock className="h-5 w-5 text-yellow-500" />
      case 'stopping':
        return <Square className="h-5 w-5 text-orange-500" />
      default:
        return <Activity className="h-5 w-5 text-blue-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'inactive':
        return 'bg-gray-100 text-gray-800'
      case 'error':
        return 'bg-red-100 text-red-800'
      case 'starting':
        return 'bg-yellow-100 text-yellow-800'
      case 'stopping':
        return 'bg-orange-100 text-orange-800'
      default:
        return 'bg-blue-100 text-blue-800'
    }
  }

  const handleStart = async () => {
    setIsLoading(true)
    setStatus(prev => ({ ...prev, status: 'starting' }))
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    setStatus(prev => ({ ...prev, status: 'active', restartCount: prev.restartCount + 1 }))
    setIsLoading(false)
  }

  const handleStop = async () => {
    setIsLoading(true)
    setStatus(prev => ({ ...prev, status: 'stopping' }))
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    setStatus(prev => ({ ...prev, status: 'inactive' }))
    setIsLoading(false)
  }

  const handleRestart = async () => {
    setIsLoading(true)
    setStatus(prev => ({ ...prev, status: 'stopping' }))
    
    // Simulate stop then start
    await new Promise(resolve => setTimeout(resolve, 1000))
    setStatus(prev => ({ ...prev, status: 'starting' }))
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    setStatus(prev => ({ ...prev, status: 'active', restartCount: prev.restartCount + 1 }))
    setIsLoading(false)
  }

  const handleSaveConfig = async () => {
    setIsLoading(true)
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    setHasUnsavedChanges(false)
    setIsLoading(false)
  }

  const handleConfigChange = (field: keyof AgentConfig, value: any) => {
    setConfig(prev => ({ ...prev, [field]: value }))
    setHasUnsavedChanges(true)
  }

  const handleEnvironmentChange = (key: string, value: string) => {
    setConfig(prev => ({
      ...prev,
      environment: { ...prev.environment, [key]: value }
    }))
    setHasUnsavedChanges(true)
  }

  const exportConfig = () => {
    const dataStr = JSON.stringify(config, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${agentId}-config.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div>
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Settings className="h-6 w-6 text-blue-600" />
              Agent Control Panel
            </h2>
            <p className="text-gray-600">{config.name} ({agentId})</p>
          </div>
          <div className="flex items-center gap-2">
            {hasUnsavedChanges && (
              <Badge variant="outline" className="bg-yellow-50 text-yellow-800">
                Unsaved Changes
              </Badge>
            )}
            <Button variant="outline" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Content */}
        <div className="flex h-[calc(90vh-120px)]">
          {/* Sidebar */}
          <div className="w-64 border-r bg-gray-50 p-4">
            <nav className="space-y-2">
              {[
                { id: 'status', label: 'Status & Monitoring', icon: Activity },
                { id: 'controls', label: 'Agent Controls', icon: Power },
                { id: 'config', label: 'Configuration', icon: Settings },
                { id: 'environment', label: 'Environment', icon: HardDrive },
                { id: 'performance', label: 'Performance', icon: Zap }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-left transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-100 text-blue-700'
                      : 'hover:bg-gray-100 text-gray-700'
                  }`}
                >
                  <tab.icon className="h-4 w-4" />
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>

          {/* Main Content */}
          <div className="flex-1 p-6 overflow-y-auto">
            {/* Status & Monitoring Tab */}
            {activeTab === 'status' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold mb-4">Current Status</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Card>
                      <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-sm text-gray-600">Agent Status</p>
                            <div className="flex items-center gap-2 mt-1">
                              {getStatusIcon(status.status)}
                              <Badge className={getStatusColor(status.status)}>
                                {status.status.toUpperCase()}
                              </Badge>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="text-sm text-gray-600">Uptime</p>
                            <p className="font-semibold">{formatUptime(status.uptime)}</p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    <Card>
                      <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-sm text-gray-600">Version</p>
                            <p className="font-semibold">{status.version}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm text-gray-600">Last Heartbeat</p>
                            <p className="font-semibold text-xs">
                              {new Date(status.lastHeartbeat).toLocaleTimeString()}
                            </p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-4">Resource Usage</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Card>
                      <CardContent className="p-4">
                        <div className="flex items-center gap-3">
                          <HardDrive className="h-8 w-8 text-blue-600" />
                          <div className="flex-1">
                            <p className="text-sm text-gray-600">Memory Usage</p>
                            <div className="flex items-center gap-2 mt-1">
                              <div className="flex-1 bg-gray-200 rounded-full h-2">
                                <div
                                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                                  style={{ width: `${(status.memoryUsage / config.memoryLimit) * 100}%` }}
                                />
                              </div>
                              <span className="text-sm font-medium">
                                {status.memoryUsage}MB / {config.memoryLimit}MB
                              </span>
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    <Card>
                      <CardContent className="p-4">
                        <div className="flex items-center gap-3">
                          <Cpu className="h-8 w-8 text-green-600" />
                          <div className="flex-1">
                            <p className="text-sm text-gray-600">CPU Usage</p>
                            <div className="flex items-center gap-2 mt-1">
                              <div className="flex-1 bg-gray-200 rounded-full h-2">
                                <div
                                  className="bg-green-600 h-2 rounded-full transition-all duration-300"
                                  style={{ width: `${status.cpuUsage}%` }}
                                />
                              </div>
                              <span className="text-sm font-medium">{status.cpuUsage}%</span>
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-4">Statistics</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Card>
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-red-600">{status.errorCount}</div>
                        <p className="text-sm text-gray-600">Errors (24h)</p>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-blue-600">{status.restartCount}</div>
                        <p className="text-sm text-gray-600">Restarts</p>
                      </CardContent>
                    </Card>
                    <Card>
                      <CardContent className="p-4 text-center">
                        <div className="text-2xl font-bold text-green-600">99.2%</div>
                        <p className="text-sm text-gray-600">Availability</p>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              </div>
            )}

            {/* Controls Tab */}
            {activeTab === 'controls' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold mb-4">Agent Controls</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <Button
                      onClick={handleStart}
                      disabled={isLoading || status.status === 'active'}
                      className="h-16 flex flex-col items-center gap-1"
                    >
                      <Play className="h-5 w-5" />
                      Start
                    </Button>
                    <Button
                      variant="outline"
                      onClick={handleStop}
                      disabled={isLoading || status.status === 'inactive'}
                      className="h-16 flex flex-col items-center gap-1"
                    >
                      <Pause className="h-5 w-5" />
                      Stop
                    </Button>
                    <Button
                      variant="outline"
                      onClick={handleRestart}
                      disabled={isLoading}
                      className="h-16 flex flex-col items-center gap-1"
                    >
                      <RotateCcw className="h-5 w-5" />
                      Restart
                    </Button>
                    <Button
                      variant="outline"
                      disabled={isLoading}
                      className="h-16 flex flex-col items-center gap-1"
                    >
                      <RefreshCw className="h-5 w-5" />
                      Reload Config
                    </Button>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 border rounded-lg">
                      <div>
                        <p className="font-medium">Auto Restart</p>
                        <p className="text-sm text-gray-600">Automatically restart on failure</p>
                      </div>
                      <input
                        type="checkbox"
                        checked={config.autoRestart}
                        onChange={(e) => handleConfigChange('autoRestart', e.target.checked)}
                        className="h-4 w-4"
                      />
                    </div>
                    <div className="flex items-center justify-between p-3 border rounded-lg">
                      <div>
                        <p className="font-medium">Enabled</p>
                        <p className="text-sm text-gray-600">Agent is enabled for execution</p>
                      </div>
                      <input
                        type="checkbox"
                        checked={config.enabled}
                        onChange={(e) => handleConfigChange('enabled', e.target.checked)}
                        className="h-4 w-4"
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Configuration Tab */}
            {activeTab === 'config' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Configuration</h3>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={exportConfig}>
                      <Download className="h-3 w-3 mr-1" />
                      Export
                    </Button>
                    <Button variant="outline" size="sm">
                      <Upload className="h-3 w-3 mr-1" />
                      Import
                    </Button>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <Label>Agent Name</Label>
                      <Input
                        value={config.name}
                        onChange={(e) => handleConfigChange('name', e.target.value)}
                      />
                    </div>
                    <div>
                      <Label>Description</Label>
                      <textarea
                        value={config.description}
                        onChange={(e) => handleConfigChange('description', e.target.value)}
                        className="w-full p-2 border rounded-lg"
                        rows={3}
                      />
                    </div>
                    <div>
                      <Label>Log Level</Label>
                      <select
                        value={config.logLevel}
                        onChange={(e) => handleConfigChange('logLevel', e.target.value)}
                        className="w-full p-2 border rounded-lg"
                      >
                        <option value="debug">Debug</option>
                        <option value="info">Info</option>
                        <option value="warning">Warning</option>
                        <option value="error">Error</option>
                      </select>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <Label>Max Retries</Label>
                      <Input
                        type="number"
                        value={config.maxRetries}
                        onChange={(e) => handleConfigChange('maxRetries', parseInt(e.target.value))}
                      />
                    </div>
                    <div>
                      <Label>Timeout (ms)</Label>
                      <Input
                        type="number"
                        value={config.timeout}
                        onChange={(e) => handleConfigChange('timeout', parseInt(e.target.value))}
                      />
                    </div>
                    <div>
                      <Label>Priority (1-10)</Label>
                      <Input
                        type="number"
                        min="1"
                        max="10"
                        value={config.priority}
                        onChange={(e) => handleConfigChange('priority', parseInt(e.target.value))}
                      />
                    </div>
                  </div>
                </div>

                <div>
                  <Label>Resource Limits</Label>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
                    <div>
                      <Label className="text-sm">Memory Limit (MB)</Label>
                      <Input
                        type="number"
                        value={config.memoryLimit}
                        onChange={(e) => handleConfigChange('memoryLimit', parseInt(e.target.value))}
                      />
                    </div>
                    <div>
                      <Label className="text-sm">CPU Limit (cores)</Label>
                      <Input
                        type="number"
                        step="0.1"
                        value={config.cpuLimit}
                        onChange={(e) => handleConfigChange('cpuLimit', parseFloat(e.target.value))}
                      />
                    </div>
                  </div>
                </div>

                <div>
                  <Label>Dependencies</Label>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {config.dependencies.map((dep, index) => (
                      <Badge key={index} variant="outline">
                        {dep}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Environment Tab */}
            {activeTab === 'environment' && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-semibold">Environment Variables</h3>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setShowSensitiveData(!showSensitiveData)}
                  >
                    {showSensitiveData ? <EyeOff className="h-3 w-3 mr-1" /> : <Eye className="h-3 w-3 mr-1" />}
                    {showSensitiveData ? 'Hide' : 'Show'} Sensitive
                  </Button>
                </div>

                <div className="space-y-3">
                  {Object.entries(config.environment).map(([key, value]) => (
                    <div key={key} className="grid grid-cols-1 md:grid-cols-2 gap-4 p-3 border rounded-lg">
                      <div>
                        <Label className="text-sm">Key</Label>
                        <Input value={key} disabled />
                      </div>
                      <div>
                        <Label className="text-sm">Value</Label>
                        <Input
                          type={!showSensitiveData && key.toLowerCase().includes('key') ? 'password' : 'text'}
                          value={value}
                          onChange={(e) => handleEnvironmentChange(key, e.target.value)}
                        />
                      </div>
                    </div>
                  ))}
                </div>

                <Button variant="outline" className="w-full">
                  Add Environment Variable
                </Button>
              </div>
            )}

            {/* Performance Tab */}
            {activeTab === 'performance' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold">Performance Metrics</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-base">Resource Utilization</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div>
                          <div className="flex justify-between text-sm mb-1">
                            <span>Memory</span>
                            <span>{status.memoryUsage}MB / {config.memoryLimit}MB</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full"
                              style={{ width: `${(status.memoryUsage / config.memoryLimit) * 100}%` }}
                            />
                          </div>
                        </div>
                        <div>
                          <div className="flex justify-between text-sm mb-1">
                            <span>CPU</span>
                            <span>{status.cpuUsage}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-green-600 h-2 rounded-full"
                              style={{ width: `${status.cpuUsage}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-base">Performance History</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="h-32 bg-gray-50 rounded-lg flex items-center justify-center">
                        <p className="text-gray-500">Performance chart placeholder</p>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-6 border-t bg-gray-50">
          <div className="text-sm text-gray-600">
            Last updated: {new Date().toLocaleString()}
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button 
              onClick={handleSaveConfig}
              disabled={!hasUnsavedChanges || isLoading}
              className="flex items-center gap-2"
            >
              <Save className="h-4 w-4" />
              Save Changes
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
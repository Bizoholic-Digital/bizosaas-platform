"use client"

import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import {
  Bot, Zap, Settings, ChevronDown, Info, Key,
  Clock, DollarSign, Cpu, Activity
} from 'lucide-react'
import { useAuth } from '@/hooks/use-auth'

interface AIModel {
  id: string
  name: string
  provider: 'openai' | 'anthropic' | 'google' | 'cohere' | 'mistral' | 'custom'
  type: 'chat' | 'completion' | 'embedding' | 'multimodal'
  capabilities: string[]
  maxTokens: number
  costPer1kTokens: number
  responseTime: 'fast' | 'medium' | 'slow'
  status: 'active' | 'inactive' | 'error'
  isDefault?: boolean
  byokConfig?: {
    keyName: string
    endpoint?: string
    addedDate: string
    lastUsed?: string
  }
}

interface ModelSelectorProps {
  selectedModel: string
  onModelChange: (modelId: string) => void
  className?: string
}

export function ModelSelector({ selectedModel, onModelChange, className = "" }: ModelSelectorProps) {
  const { user } = useAuth()
  const [availableModels, setAvailableModels] = useState<AIModel[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showDetails, setShowDetails] = useState(false)

  const tenantId = user?.tenant_id || 'demo'
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://api.bizoholic.net'

  // Load tenant's available BYOK models
  useEffect(() => {
    loadAvailableModels()
  }, [tenantId])

  const loadAvailableModels = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE_URL}/api/tenant/models`, {
        headers: {
          'x-tenant-id': tenantId
        }
      })

      if (!response.ok) {
        throw new Error(`Failed to load models: ${response.statusText}`)
      }

      const data = await response.json()
      setAvailableModels(data.models || [])

      // Set default model if none selected
      if (!selectedModel && data.models.length > 0) {
        const defaultModel = data.models.find((m: AIModel) => m.isDefault) || data.models[0]
        onModelChange(defaultModel.id)
      }

    } catch (error) {
      console.error('Failed to load available models:', error)
      setError(error instanceof Error ? error.message : 'Failed to load models')

      // Fallback to demo models if API fails
      setAvailableModels([
        {
          id: 'demo-gpt-4',
          name: 'GPT-4 (Demo)',
          provider: 'openai',
          type: 'chat',
          capabilities: ['chat', 'reasoning', 'code'],
          maxTokens: 8192,
          costPer1kTokens: 0.03,
          responseTime: 'medium',
          status: 'active',
          isDefault: true
        }
      ])

      if (!selectedModel) {
        onModelChange('demo-gpt-4')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const getCurrentModel = () => {
    return availableModels.find(model => model.id === selectedModel)
  }

  const getProviderIcon = (provider: string) => {
    switch (provider) {
      case 'openai': return '🟢'
      case 'anthropic': return '🔵'
      case 'google': return '🔴'
      case 'cohere': return '🟣'
      case 'mistral': return '🟠'
      default: return '⚪'
    }
  }

  const getResponseTimeColor = (time: string) => {
    switch (time) {
      case 'fast': return 'text-green-600'
      case 'medium': return 'text-yellow-600'
      case 'slow': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  const currentModel = getCurrentModel()

  if (isLoading) {
    return (
      <div className={`flex items-center space-x-2 ${className}`}>
        <div className="w-4 h-4 rounded-full bg-gray-300 animate-pulse"></div>
        <span className="text-sm text-muted-foreground">Loading models...</span>
      </div>
    )
  }

  if (error && availableModels.length === 0) {
    return (
      <Alert className={`${className}`}>
        <Info className="h-4 w-4" />
        <AlertDescription>
          No AI models available. Contact admin to configure BYOK models.
        </AlertDescription>
      </Alert>
    )
  }

  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      {/* Model Selector */}
      <Select value={selectedModel} onValueChange={onModelChange}>
        <SelectTrigger className="w-48">
          <div className="flex items-center space-x-2">
            <span className="text-lg">{currentModel ? getProviderIcon(currentModel.provider) : '🤖'}</span>
            <SelectValue placeholder="Select AI Model" />
          </div>
        </SelectTrigger>
        <SelectContent>
          {availableModels.map((model) => (
            <SelectItem key={model.id} value={model.id}>
              <div className="flex items-center justify-between w-full">
                <div className="flex items-center space-x-2">
                  <span className="text-lg">{getProviderIcon(model.provider)}</span>
                  <span className="font-medium">{model.name}</span>
                  {model.byokConfig && (
                    <span title="BYOK Model">
                      <Key className="w-3 h-3 text-blue-500" />
                    </span>
                  )}
                </div>
                <div className="flex items-center space-x-2">
                  <Badge
                    variant={model.status === 'active' ? 'default' : 'destructive'}
                    className="text-xs"
                  >
                    {model.status}
                  </Badge>
                  <span className={`text-xs ${getResponseTimeColor(model.responseTime)}`}>
                    {model.responseTime}
                  </span>
                </div>
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      {/* Model Details Button */}
      {currentModel && (
        <Dialog open={showDetails} onOpenChange={setShowDetails}>
          <DialogTrigger asChild>
            <Button variant="outline" size="sm">
              <Info className="w-4 h-4" />
            </Button>
          </DialogTrigger>

          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle className="flex items-center space-x-2">
                <span className="text-2xl">{getProviderIcon(currentModel.provider)}</span>
                <span>{currentModel.name}</span>
              </DialogTitle>
            </DialogHeader>

            <div className="space-y-4">
              {/* Model Status */}
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm flex items-center space-x-2">
                    <Activity className="w-4 h-4" />
                    <span>Status & Performance</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Status:</span>
                    <Badge variant={currentModel.status === 'active' ? 'default' : 'destructive'}>
                      {currentModel.status}
                    </Badge>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Response Time:</span>
                    <span className={`text-sm font-medium ${getResponseTimeColor(currentModel.responseTime)}`}>
                      {currentModel.responseTime}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Max Tokens:</span>
                    <span className="text-sm font-medium">{currentModel.maxTokens.toLocaleString()}</span>
                  </div>
                </CardContent>
              </Card>

              {/* Capabilities */}
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm flex items-center space-x-2">
                    <Cpu className="w-4 h-4" />
                    <span>Capabilities</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-1">
                    {currentModel.capabilities.map((capability, index) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {capability}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Cost Information */}
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm flex items-center space-x-2">
                    <DollarSign className="w-4 h-4" />
                    <span>Usage Cost</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-sm">
                    <span className="text-muted-foreground">Per 1K tokens:</span>
                    <span className="font-medium ml-1">${currentModel.costPer1kTokens}</span>
                  </div>
                </CardContent>
              </Card>

              {/* BYOK Information */}
              {currentModel.byokConfig && (
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <Key className="w-4 h-4" />
                      <span>BYOK Configuration</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Key Name:</span>
                      <span className="text-sm font-medium">{currentModel.byokConfig.keyName}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Added:</span>
                      <span className="text-sm font-medium">
                        {new Date(currentModel.byokConfig.addedDate).toLocaleDateString()}
                      </span>
                    </div>
                    {currentModel.byokConfig.lastUsed && (
                      <div className="flex justify-between">
                        <span className="text-sm text-muted-foreground">Last Used:</span>
                        <span className="text-sm font-medium">
                          {new Date(currentModel.byokConfig.lastUsed).toLocaleDateString()}
                        </span>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )}

              <Button
                onClick={() => setShowDetails(false)}
                className="w-full"
              >
                Close
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      )}

      {/* Quick Status Indicator */}
      {currentModel && (
        <div className="flex items-center space-x-1">
          <div className={`w-2 h-2 rounded-full ${currentModel.status === 'active' ? 'bg-green-500' :
            currentModel.status === 'error' ? 'bg-red-500' : 'bg-gray-500'
            }`} />
          <span className="text-xs text-muted-foreground">
            {currentModel.byokConfig ? 'BYOK' : 'Default'}
          </span>
        </div>
      )}
    </div>
  )
}
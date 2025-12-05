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
import { Progress } from '../../ui/progress'
import { 
  FileText, 
  Download, 
  Code, 
  Database, 
  Users, 
  CheckCircle,
  Copy,
  ExternalLink,
  Shield,
  Clock,
  Rocket,
  Settings,
  Key,
  Monitor,
  Globe,
  Lock,
  Zap,
  AlertTriangle,
  BookOpen,
  Archive
} from 'lucide-react'
import { cn } from '../../../lib/utils'

interface DocumentationDeploymentStepProps {
  form: UseFormReturn<any>
  configurations: any[]
  setConfigurations: React.Dispatch<React.SetStateAction<any[]>>
}

interface DocumentationItem {
  id: string
  title: string
  description: string
  type: 'guide' | 'reference' | 'example' | 'security'
  content: string
  language?: string
  generated: boolean
  downloadUrl?: string
}

interface DeploymentTask {
  id: string
  title: string
  description: string
  status: 'pending' | 'running' | 'completed' | 'error'
  progress: number
  dependencies: string[]
  category: 'vault' | 'monitoring' | 'documentation' | 'team' | 'validation'
}

interface TeamMember {
  id: string
  email: string
  role: 'admin' | 'developer' | 'viewer'
  permissions: string[]
  status: 'pending' | 'invited' | 'active'
}

const DOCUMENTATION_TEMPLATES: DocumentationItem[] = [
  {
    id: 'quick-start',
    title: 'Quick Start Guide',
    description: 'Get started with your API keys in minutes',
    type: 'guide',
    content: '',
    generated: false
  },
  {
    id: 'api-reference',
    title: 'API Reference Documentation',
    description: 'Complete API documentation for all integrated services',
    type: 'reference',
    content: '',
    generated: false
  },
  {
    id: 'code-examples',
    title: 'Code Examples & SDKs',
    description: 'Ready-to-use code examples in multiple languages',
    type: 'example',
    content: '',
    language: 'javascript',
    generated: false
  },
  {
    id: 'security-guide',
    title: 'Security Best Practices',
    description: 'Security guidelines and compliance information',
    type: 'security',
    content: '',
    generated: false
  },
  {
    id: 'troubleshooting',
    title: 'Troubleshooting Guide',
    description: 'Common issues and solutions',
    type: 'guide',
    content: '',
    generated: false
  },
  {
    id: 'monitoring-setup',
    title: 'Monitoring & Alerting Setup',
    description: 'Configure monitoring dashboards and alerts',
    type: 'guide',
    content: '',
    generated: false
  }
]

const DEPLOYMENT_TASKS: DeploymentTask[] = [
  {
    id: 'vault-setup',
    title: 'HashiCorp Vault Configuration',
    description: 'Set up secure credential storage',
    status: 'pending',
    progress: 0,
    dependencies: [],
    category: 'vault'
  },
  {
    id: 'key-deployment',
    title: 'API Key Deployment',
    description: 'Deploy generated keys to Vault',
    status: 'pending',
    progress: 0,
    dependencies: ['vault-setup'],
    category: 'vault'
  },
  {
    id: 'monitoring-setup',
    title: 'Monitoring Infrastructure',
    description: 'Deploy monitoring and alerting systems',
    status: 'pending',
    progress: 0,
    dependencies: ['key-deployment'],
    category: 'monitoring'
  },
  {
    id: 'documentation-generation',
    title: 'Generate Documentation',
    description: 'Create comprehensive API documentation',
    status: 'pending',
    progress: 0,
    dependencies: [],
    category: 'documentation'
  },
  {
    id: 'team-setup',
    title: 'Team Access Configuration',
    description: 'Set up team member access and permissions',
    status: 'pending',
    progress: 0,
    dependencies: ['vault-setup'],
    category: 'team'
  },
  {
    id: 'final-validation',
    title: 'Final System Validation',
    description: 'End-to-end system validation and testing',
    status: 'pending',
    progress: 0,
    dependencies: ['key-deployment', 'monitoring-setup', 'team-setup'],
    category: 'validation'
  }
]

export function DocumentationDeploymentStep({ 
  form,
  configurations,
  setConfigurations
}: DocumentationDeploymentStepProps) {
  const [documentation, setDocumentation] = useState<DocumentationItem[]>(DOCUMENTATION_TEMPLATES)
  const [deploymentTasks, setDeploymentTasks] = useState<DeploymentTask[]>(DEPLOYMENT_TASKS)
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([])
  const [isGeneratingDocs, setIsGeneratingDocs] = useState(false)
  const [isDeploying, setIsDeploying] = useState(false)
  const [deploymentProgress, setDeploymentProgress] = useState(0)
  const [newMemberEmail, setNewMemberEmail] = useState('')
  const [backupStrategy, setBackupStrategy] = useState('automated')

  const formData = form.watch()
  const selectedServices = formData.selectedServices || []
  const securityConfig = formData.securityConfiguration || {}

  useEffect(() => {
    // Auto-generate basic documentation when services are selected
    if (selectedServices.length > 0) {
      generateDocumentation()
    }
  }, [selectedServices])

  const generateDocumentation = async () => {
    setIsGeneratingDocs(true)
    
    for (let i = 0; i < documentation.length; i++) {
      const doc = documentation[i]
      
      // Simulate documentation generation
      await new Promise(resolve => setTimeout(resolve, 800))
      
      setDocumentation(prev => prev.map(d => 
        d.id === doc.id 
          ? {
              ...d,
              content: generateDocumentationContent(d.id, selectedServices, securityConfig),
              generated: true,
              downloadUrl: `/api/documentation/${d.id}/download`
            }
          : d
      ))
    }
    
    setIsGeneratingDocs(false)
  }

  const generateDocumentationContent = (docId: string, services: string[], security: any): string => {
    switch (docId) {
      case 'quick-start':
        return `# Quick Start Guide

## Overview
This guide will help you get started with your ${services.length} integrated API service${services.length !== 1 ? 's' : ''}.

## Services Configured
${services.map(service => `- ${getServiceName(service)}`).join('\n')}

## Environment
- **Environment**: ${security.environment || 'development'}
- **Security Level**: ${security.securityLevel || 'enhanced'}
- **Key Rotation**: ${security.keyRotationPolicy || '90-days'}

## Next Steps
1. Download your API keys from the secure vault
2. Implement the provided code examples
3. Set up monitoring and alerts
4. Review security best practices`

      case 'api-reference':
        return `# API Reference Documentation

## Integrated Services

${services.map(service => `
### ${getServiceName(service)}
- **Base URL**: ${getServiceBaseUrl(service)}
- **Authentication**: API Key
- **Rate Limits**: ${getServiceRateLimit(service)}
- **Documentation**: ${getServiceDocs(service)}
`).join('\n')}

## Authentication
All API requests require proper authentication using your assigned API keys.

## Error Handling
Standard HTTP status codes are used to indicate the success or failure of requests.`

      case 'code-examples':
        return `# Code Examples

## JavaScript/Node.js

\`\`\`javascript
// ${getServiceName(services[0])} Integration Example
const apiKey = process.env.${services[0].toUpperCase()}_API_KEY;

async function makeApiCall() {
  const response = await fetch('${getServiceBaseUrl(services[0])}/endpoint', {
    headers: {
      'Authorization': \`Bearer \${apiKey}\`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.json();
}
\`\`\`

## Python

\`\`\`python
import os
import requests

api_key = os.getenv('${services[0].toUpperCase()}_API_KEY')

def make_api_call():
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get('${getServiceBaseUrl(services[0])}/endpoint', headers=headers)
    return response.json()
\`\`\``

      case 'security-guide':
        return `# Security Best Practices

## Key Management
- Store API keys in environment variables or secure vaults
- Never commit keys to version control
- Rotate keys regularly (configured: ${security.keyRotationPolicy || '90-days'})

## Access Control
- Use minimum required permissions
- Implement IP whitelisting where possible
- Enable two-factor authentication: ${security.accessControl?.requireTwoFactor ? 'Enabled' : 'Disabled'}

## Monitoring
- Monitor API usage patterns
- Set up alerts for unusual activity
- Track rate limit usage

## Compliance
This configuration meets the following standards:
- SOC 2 Type II
- GDPR compliance
- ${security.securityLevel === 'enterprise' ? 'HIPAA ready' : 'Industry standard security'}`

      default:
        return '# Documentation Content\n\nContent will be generated based on your configuration.'
    }
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

  const getServiceBaseUrl = (serviceId: string): string => {
    const baseUrls: Record<string, string> = {
      stripe: 'https://api.stripe.com',
      paypal: 'https://api.paypal.com',
      'google-ads': 'https://googleads.googleapis.com',
      openai: 'https://api.openai.com',
      'facebook-ads': 'https://graph.facebook.com',
      anthropic: 'https://api.anthropic.com'
    }
    return baseUrls[serviceId] || 'https://api.example.com'
  }

  const getServiceRateLimit = (serviceId: string): string => {
    const rateLimits: Record<string, string> = {
      stripe: '100 requests/second',
      paypal: '50 requests/second',
      'google-ads': '10,000 requests/day',
      openai: '3,500 requests/minute',
      'facebook-ads': '200 requests/hour',
      anthropic: '1,000 requests/minute'
    }
    return rateLimits[serviceId] || '1,000 requests/hour'
  }

  const getServiceDocs = (serviceId: string): string => {
    const docs: Record<string, string> = {
      stripe: 'https://stripe.com/docs/api',
      paypal: 'https://developer.paypal.com/docs/api',
      'google-ads': 'https://developers.google.com/google-ads/api',
      openai: 'https://platform.openai.com/docs',
      'facebook-ads': 'https://developers.facebook.com/docs/marketing-apis',
      anthropic: 'https://docs.anthropic.com'
    }
    return docs[serviceId] || 'https://docs.example.com'
  }

  const addTeamMember = () => {
    if (!newMemberEmail.trim()) return
    
    const newMember: TeamMember = {
      id: Date.now().toString(),
      email: newMemberEmail.trim(),
      role: 'developer',
      permissions: ['read', 'use_keys'],
      status: 'pending'
    }
    
    setTeamMembers(prev => [...prev, newMember])
    setNewMemberEmail('')
  }

  const updateTeamMemberRole = (memberId: string, role: 'admin' | 'developer' | 'viewer') => {
    setTeamMembers(prev => prev.map(member => 
      member.id === memberId 
        ? {
            ...member,
            role,
            permissions: getPermissionsForRole(role)
          }
        : member
    ))
  }

  const getPermissionsForRole = (role: string): string[] => {
    switch (role) {
      case 'admin':
        return ['read', 'write', 'delete', 'manage_keys', 'manage_team', 'view_audit']
      case 'developer':
        return ['read', 'use_keys', 'view_docs']
      case 'viewer':
        return ['read', 'view_docs']
      default:
        return ['read']
    }
  }

  const removeTeamMember = (memberId: string) => {
    setTeamMembers(prev => prev.filter(member => member.id !== memberId))
  }

  const startDeployment = async () => {
    setIsDeploying(true)
    setDeploymentProgress(0)
    
    // Execute deployment tasks in dependency order
    const taskOrder = ['vault-setup', 'key-deployment', 'documentation-generation', 'team-setup', 'monitoring-setup', 'final-validation']
    
    for (let i = 0; i < taskOrder.length; i++) {
      const taskId = taskOrder[i]
      
      setDeploymentTasks(prev => prev.map(task => 
        task.id === taskId 
          ? { ...task, status: 'running', progress: 0 }
          : task
      ))
      
      // Simulate task execution with progress
      for (let progress = 0; progress <= 100; progress += 10) {
        await new Promise(resolve => setTimeout(resolve, 200))
        
        setDeploymentTasks(prev => prev.map(task => 
          task.id === taskId 
            ? { ...task, progress }
            : task
        ))
        
        setDeploymentProgress(((i * 100) + progress) / taskOrder.length)
      }
      
      setDeploymentTasks(prev => prev.map(task => 
        task.id === taskId 
          ? { ...task, status: 'completed', progress: 100 }
          : task
      ))
    }
    
    setIsDeploying(false)
    setDeploymentProgress(100)
  }

  const downloadDocumentation = (docId: string) => {
    const doc = documentation.find(d => d.id === docId)
    if (!doc || !doc.generated) return
    
    const blob = new Blob([doc.content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${doc.id}.md`
    link.click()
    URL.revokeObjectURL(url)
  }

  const downloadAllDocumentation = () => {
    const allDocs = documentation
      .filter(doc => doc.generated)
      .map(doc => `# ${doc.title}\n\n${doc.content}`)
      .join('\n\n---\n\n')
    
    const blob = new Blob([allDocs], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'api-documentation-complete.md'
    link.click()
    URL.revokeObjectURL(url)
  }

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text)
    } catch (error) {
      console.error('Failed to copy to clipboard:', error)
    }
  }

  const getTaskIcon = (category: string) => {
    switch (category) {
      case 'vault':
        return <Lock className="h-4 w-4" />
      case 'monitoring':
        return <Monitor className="h-4 w-4" />
      case 'documentation':
        return <FileText className="h-4 w-4" />
      case 'team':
        return <Users className="h-4 w-4" />
      case 'validation':
        return <CheckCircle className="h-4 w-4" />
      default:
        return <Settings className="h-4 w-4" />
    }
  }

  const completedTasks = deploymentTasks.filter(task => task.status === 'completed').length
  const totalDocs = documentation.filter(doc => doc.generated).length
  const isDeploymentReady = completedTasks === deploymentTasks.length

  return (
    <div className="space-y-6">
      {/* Deployment Overview */}
      <Card className="border-green-200 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-950 dark:to-emerald-950">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Rocket className="h-5 w-5 text-green-600" />
            <span>Documentation & Deployment</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{totalDocs}</div>
              <div className="text-sm text-gray-600">Documentation</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{completedTasks}/{deploymentTasks.length}</div>
              <div className="text-sm text-gray-600">Tasks Complete</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">{teamMembers.length}</div>
              <div className="text-sm text-gray-600">Team Members</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">
                {Math.round(deploymentProgress)}%
              </div>
              <div className="text-sm text-gray-600">Progress</div>
            </div>
          </div>
          
          {isDeploying && (
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">Deploying BizOSaaS API Management</span>
                <span className="text-sm text-gray-500">{Math.round(deploymentProgress)}%</span>
              </div>
              <Progress value={deploymentProgress} className="h-2" />
            </div>
          )}
          
          <div className="flex space-x-2 mt-4">
            <Button 
              onClick={startDeployment}
              disabled={isDeploying || isDeploymentReady}
              className="flex items-center space-x-2"
            >
              {isDeploying ? (
                <Zap className="h-4 w-4 animate-pulse" />
              ) : isDeploymentReady ? (
                <CheckCircle className="h-4 w-4" />
              ) : (
                <Rocket className="h-4 w-4" />
              )}
              <span>
                {isDeploying ? 'Deploying...' : isDeploymentReady ? 'Deployment Complete' : 'Start Deployment'}
              </span>
            </Button>
            
            {totalDocs > 0 && (
              <Button variant="outline" onClick={downloadAllDocumentation}>
                <Download className="h-4 w-4 mr-2" />
                Download All Docs
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Documentation Generation */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <FileText className="h-5 w-5" />
              <span>Generated Documentation</span>
            </div>
            <Button
              variant="outline"
              onClick={generateDocumentation}
              disabled={isGeneratingDocs}
            >
              {isGeneratingDocs ? (
                <Zap className="h-4 w-4 mr-2 animate-pulse" />
              ) : (
                <BookOpen className="h-4 w-4 mr-2" />
              )}
              {isGeneratingDocs ? 'Generating...' : 'Regenerate'}
            </Button>
          </CardTitle>
          <CardDescription>
            Comprehensive documentation for your API integration
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {documentation.map(doc => (
              <Card key={doc.id} className={cn(
                "transition-all duration-200",
                doc.generated 
                  ? "ring-1 ring-green-200 bg-green-50 dark:bg-green-950" 
                  : "bg-gray-50 dark:bg-gray-800"
              )}>
                <CardContent className="p-4">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className={cn(
                        "p-2 rounded-lg",
                        doc.generated ? "bg-green-100 text-green-600" : "bg-gray-200 text-gray-500"
                      )}>
                        {doc.type === 'guide' && <BookOpen className="h-4 w-4" />}
                        {doc.type === 'reference' && <Database className="h-4 w-4" />}
                        {doc.type === 'example' && <Code className="h-4 w-4" />}
                        {doc.type === 'security' && <Shield className="h-4 w-4" />}
                      </div>
                      <div>
                        <h4 className="font-medium">{doc.title}</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {doc.description}
                        </p>
                      </div>
                    </div>
                    
                    {doc.generated && (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    )}
                  </div>
                  
                  {doc.generated && (
                    <div className="flex space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => downloadDocumentation(doc.id)}
                      >
                        <Download className="h-3 w-3 mr-1" />
                        Download
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => copyToClipboard(doc.content)}
                      >
                        <Copy className="h-3 w-3 mr-1" />
                        Copy
                      </Button>
                    </div>
                  )}
                  
                  {doc.language && (
                    <Badge variant="outline" className="mt-2 text-xs">
                      {doc.language}
                    </Badge>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Team Access Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Users className="h-5 w-5" />
            <span>Team Access & Permissions</span>
          </CardTitle>
          <CardDescription>
            Configure team member access to API keys and documentation
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Add Team Member */}
            <div className="flex space-x-2">
              <Input
                placeholder="Enter team member email"
                value={newMemberEmail}
                onChange={(e) => setNewMemberEmail(e.target.value)}
                className="flex-1"
              />
              <Button onClick={addTeamMember} disabled={!newMemberEmail.trim()}>
                Add Member
              </Button>
            </div>
            
            {/* Team Members List */}
            {teamMembers.length > 0 && (
              <div className="space-y-2">
                <h4 className="font-medium">Team Members</h4>
                {teamMembers.map(member => (
                  <div key={member.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 bg-blue-100 text-blue-600 rounded-lg">
                        <Users className="h-4 w-4" />
                      </div>
                      <div>
                        <div className="font-medium">{member.email}</div>
                        <div className="text-sm text-gray-600">
                          {member.permissions.join(', ')}
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <select
                        value={member.role}
                        onChange={(e) => updateTeamMemberRole(member.id, e.target.value as any)}
                        className="px-3 py-1 border rounded text-sm"
                      >
                        <option value="viewer">Viewer</option>
                        <option value="developer">Developer</option>
                        <option value="admin">Admin</option>
                      </select>
                      
                      <Badge variant="outline" className={cn(
                        "text-xs",
                        member.status === 'active' ? 'text-green-700 border-green-300' :
                        member.status === 'pending' ? 'text-yellow-700 border-yellow-300' :
                        'text-gray-700 border-gray-300'
                      )}>
                        {member.status}
                      </Badge>
                      
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => removeTeamMember(member.id)}
                      >
                        Remove
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Deployment Tasks */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Database className="h-5 w-5" />
            <span>Deployment Tasks</span>
          </CardTitle>
          <CardDescription>
            System deployment and configuration tasks
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {deploymentTasks.map(task => (
              <div key={task.id} className={cn(
                "flex items-center justify-between p-4 border rounded-lg",
                task.status === 'completed' ? "bg-green-50 dark:bg-green-950 border-green-200" :
                task.status === 'running' ? "bg-blue-50 dark:bg-blue-950 border-blue-200" :
                task.status === 'error' ? "bg-red-50 dark:bg-red-950 border-red-200" :
                "bg-gray-50 dark:bg-gray-800"
              )}>
                <div className="flex items-center space-x-3">
                  <div className={cn(
                    "p-2 rounded-lg",
                    task.status === 'completed' ? "bg-green-100 text-green-600" :
                    task.status === 'running' ? "bg-blue-100 text-blue-600" :
                    task.status === 'error' ? "bg-red-100 text-red-600" :
                    "bg-gray-200 text-gray-500"
                  )}>
                    {getTaskIcon(task.category)}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-medium">{task.title}</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{task.description}</p>
                    {task.dependencies.length > 0 && (
                      <div className="text-xs text-gray-500 mt-1">
                        Depends on: {task.dependencies.join(', ')}
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  {task.status === 'running' && (
                    <div className="w-24">
                      <Progress value={task.progress} className="h-2" />
                    </div>
                  )}
                  
                  <Badge variant="outline" className={cn(
                    "text-xs",
                    task.status === 'completed' ? 'text-green-700 border-green-300' :
                    task.status === 'running' ? 'text-blue-700 border-blue-300' :
                    task.status === 'error' ? 'text-red-700 border-red-300' :
                    'text-gray-700 border-gray-300'
                  )}>
                    {task.status}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Backup & Recovery Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Archive className="h-5 w-5" />
            <span>Backup & Recovery</span>
          </CardTitle>
          <CardDescription>
            Configure backup strategies for your API keys and configurations
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Backup Strategy</label>
              <select
                value={backupStrategy}
                onChange={(e) => setBackupStrategy(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg"
              >
                <option value="automated">Automated Daily Backups</option>
                <option value="manual">Manual Backups Only</option>
                <option value="continuous">Continuous Backup</option>
                <option value="none">No Backups</option>
              </select>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 border rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <Database className="h-4 w-4 text-blue-500" />
                  <span className="font-medium">Vault Backup</span>
                </div>
                <p className="text-sm text-gray-600">Secure backup of all API keys</p>
                <Badge variant="outline" className="mt-2 text-xs">
                  {backupStrategy === 'none' ? 'Disabled' : 'Enabled'}
                </Badge>
              </div>
              
              <div className="p-4 border rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <Settings className="h-4 w-4 text-green-500" />
                  <span className="font-medium">Config Backup</span>
                </div>
                <p className="text-sm text-gray-600">Backup of all configurations</p>
                <Badge variant="outline" className="mt-2 text-xs">
                  {backupStrategy === 'none' ? 'Disabled' : 'Enabled'}
                </Badge>
              </div>
              
              <div className="p-4 border rounded-lg">
                <div className="flex items-center space-x-2 mb-2">
                  <Clock className="h-4 w-4 text-purple-500" />
                  <span className="font-medium">Retention</span>
                </div>
                <p className="text-sm text-gray-600">90-day backup retention</p>
                <Badge variant="outline" className="mt-2 text-xs">
                  Standard
                </Badge>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Final Status */}
      {isDeploymentReady && (
        <Card className="border-green-200 bg-green-50 dark:bg-green-950 dark:border-green-800">
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <CheckCircle className="h-6 w-6 text-green-600" />
              <div>
                <div className="font-semibold text-lg text-green-800 dark:text-green-200">
                  Deployment Complete! 🎉
                </div>
                <div className="text-sm text-green-700 dark:text-green-300">
                  Your API key management system is ready for production use
                </div>
              </div>
              
              <div className="ml-auto">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => window.open('/dashboard/api-keys', '_blank')}
                >
                  <ExternalLink className="h-4 w-4 mr-2" />
                  Open Dashboard
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default DocumentationDeploymentStep
'use client'

import { useState, useEffect } from 'react'
import { Globe, CheckCircle, XCircle, AlertCircle, Settings, RefreshCw } from 'lucide-react'

interface Integration {
  id: string
  name: string
  type: 'api' | 'webhook' | 'database' | 'analytics' | 'payment'
  status: 'connected' | 'disconnected' | 'error' | 'pending'
  lastSync: string | null
  endpoint: string
  description: string
  health_score: number
}

export default function IntegrationsPage() {
  const [integrations, setIntegrations] = useState<Integration[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Mock data - replace with actual API call
    const mockIntegrations: Integration[] = [
      {
        id: 'int-001',
        name: 'Django CRM',
        type: 'api',
        status: 'connected',
        lastSync: '2024-09-26T08:00:00Z',
        endpoint: 'http://localhost:8000',
        description: 'Customer relationship management system',
        health_score: 98
      },
      {
        id: 'int-002',
        name: 'Wagtail CMS',
        type: 'api',
        status: 'connected',
        lastSync: '2024-09-26T07:45:00Z',
        endpoint: 'http://localhost:8006',
        description: 'Content management system',
        health_score: 95
      },
      {
        id: 'int-003',
        name: 'Saleor E-commerce',
        type: 'api',
        status: 'connected',
        lastSync: '2024-09-26T08:10:00Z',
        endpoint: 'http://localhost:8003',
        description: 'E-commerce platform',
        health_score: 92
      },
      {
        id: 'int-004',
        name: 'Stripe Payments',
        type: 'payment',
        status: 'connected',
        lastSync: '2024-09-26T07:30:00Z',
        endpoint: 'https://api.stripe.com',
        description: 'Payment processing',
        health_score: 99
      },
      {
        id: 'int-005',
        name: 'Analytics Dashboard',
        type: 'analytics',
        status: 'error',
        lastSync: null,
        endpoint: 'http://localhost:3009',
        description: 'Business intelligence platform',
        health_score: 45
      }
    ]
    
    setIntegrations(mockIntegrations)
    setIsLoading(false)
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected': return 'text-green-600 bg-green-100'
      case 'disconnected': return 'text-gray-600 bg-gray-100'
      case 'error': return 'text-red-600 bg-red-100'
      case 'pending': return 'text-yellow-600 bg-yellow-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected': return <CheckCircle className="h-4 w-4" />
      case 'disconnected': return <XCircle className="h-4 w-4" />
      case 'error': return <AlertCircle className="h-4 w-4" />
      case 'pending': return <RefreshCw className="h-4 w-4 animate-spin" />
      default: return <XCircle className="h-4 w-4" />
    }
  }

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Never'
    return new Date(dateString).toLocaleString()
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading integrations...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Integration Status</h1>
          <p className="text-gray-600">Monitor third-party integrations and API connections</p>
        </div>
      </div>

      {/* Integration Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {integrations.map((integration) => (
          <div key={integration.id} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <Globe className="h-8 w-8 text-blue-600" />
                <div>
                  <h3 className="text-lg font-medium text-gray-900">{integration.name}</h3>
                  <p className="text-sm text-gray-500">{integration.description}</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(integration.status)}`}>
                  {getStatusIcon(integration.status)}
                  <span className="ml-1 capitalize">{integration.status}</span>
                </span>
              </div>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Endpoint:</span>
                <span className="text-gray-900 font-mono text-xs">{integration.endpoint}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Last Sync:</span>
                <span className="text-gray-900">{formatDate(integration.lastSync)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Health Score:</span>
                <span className="text-gray-900">{integration.health_score}%</span>
              </div>

              {/* Health Bar */}
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full ${
                    integration.health_score >= 90 ? 'bg-green-600' :
                    integration.health_score >= 70 ? 'bg-yellow-600' : 'bg-red-600'
                  }`}
                  style={{ width: `${integration.health_score}%` }}
                ></div>
              </div>
            </div>

            <div className="mt-4 flex gap-2">
              <button className="flex items-center px-3 py-1 text-sm bg-blue-50 text-blue-700 rounded hover:bg-blue-100">
                <Settings className="h-4 w-4 mr-1" />
                Configure
              </button>
              <button className="flex items-center px-3 py-1 text-sm bg-green-50 text-green-700 rounded hover:bg-green-100">
                <RefreshCw className="h-4 w-4 mr-1" />
                Test
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
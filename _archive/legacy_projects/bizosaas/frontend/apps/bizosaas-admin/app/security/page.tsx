'use client'

import { useState, useEffect } from 'react'
import { Shield, AlertTriangle, CheckCircle, Clock, Eye } from 'lucide-react'

interface SecurityEvent {
  id: string
  type: 'login_attempt' | 'failed_auth' | 'suspicious_activity' | 'data_access' | 'policy_violation'
  severity: 'low' | 'medium' | 'high' | 'critical'
  description: string
  timestamp: string
  user_email: string
  ip_address: string
}

export default function SecurityPage() {
  const [events, setEvents] = useState<SecurityEvent[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const mockEvents: SecurityEvent[] = [
      {
        id: 'sec-001',
        type: 'failed_auth',
        severity: 'medium',
        description: 'Multiple failed login attempts detected',
        timestamp: '2024-09-26T08:05:00Z',
        user_email: 'suspicious@example.com',
        ip_address: '192.168.1.100'
      },
      {
        id: 'sec-002',
        type: 'login_attempt',
        severity: 'low',
        description: 'Successful login from new location',
        timestamp: '2024-09-26T07:45:00Z',
        user_email: 'john.doe@acmecorp.com',
        ip_address: '10.0.0.50'
      },
      {
        id: 'sec-003',
        type: 'policy_violation',
        severity: 'high',
        description: 'User account suspended for policy violation',
        timestamp: '2024-09-26T05:50:00Z',
        user_email: 'david.wilson@acmecorp.com',
        ip_address: '172.16.0.75'
      }
    ]
    
    setEvents(mockEvents)
    setIsLoading(false)
  }, [])

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'low': return 'text-green-600 bg-green-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'high': return 'text-orange-600 bg-orange-100'
      case 'critical': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading security events...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Security & Audit</h1>
        <p className="text-gray-600">Security monitoring and audit logs</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <Shield className="h-8 w-8 text-green-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-500">Security Score</p>
              <p className="text-2xl font-bold text-gray-900">94%</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <AlertTriangle className="h-8 w-8 text-yellow-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-500">Alerts Today</p>
              <p className="text-2xl font-bold text-gray-900">3</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <CheckCircle className="h-8 w-8 text-green-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-500">Resolved</p>
              <p className="text-2xl font-bold text-gray-900">127</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <Clock className="h-8 w-8 text-blue-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-500">Avg Response</p>
              <p className="text-2xl font-bold text-gray-900">12min</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Recent Security Events</h3>
        </div>
        <div className="divide-y divide-gray-200">
          {events.map((event) => (
            <div key={event.id} className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <AlertTriangle className="h-6 w-6 text-yellow-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2">
                      <p className="text-sm font-medium text-gray-900">{event.description}</p>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getSeverityColor(event.severity)}`}>
                        {event.severity}
                      </span>
                    </div>
                    <div className="mt-1 text-sm text-gray-500">
                      <span>{event.user_email}</span> • <span>{event.ip_address}</span> • <span>{new Date(event.timestamp).toLocaleString()}</span>
                    </div>
                  </div>
                </div>
                <button className="text-blue-600 hover:text-blue-900">
                  <Eye className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
'use client'

import React, { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Badge } from '../ui/badge'
import {
  Activity,
  AlertTriangle,
  CheckCircle,
  Info,
  Search,
  Filter,
  Download,
  Pause,
  Play,
  Trash2,
  Calendar,
  Clock,
  User,
  Settings,
  RefreshCw
} from 'lucide-react'

interface LogEntry {
  id: string
  timestamp: string
  level: 'info' | 'warning' | 'error' | 'success' | 'debug'
  agentId: string
  agentName: string
  message: string
  details?: any
  duration?: number
  userId?: string
  sessionId?: string
}

interface AgentLogsProps {
  selectedAgent: string | null
}

export function AgentLogs({ selectedAgent }: AgentLogsProps) {
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [filteredLogs, setFilteredLogs] = useState<LogEntry[]>([])
  const [isStreaming, setIsStreaming] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [levelFilter, setLevelFilter] = useState<string>('all')
  const [timeFilter, setTimeFilter] = useState('24h')
  const [autoScroll, setAutoScroll] = useState(true)
  const [expandedLog, setExpandedLog] = useState<string | null>(null)
  const logsEndRef = useRef<HTMLDivElement>(null)

  // Mock log data for demonstration
  const mockLogs: LogEntry[] = [
    {
      id: '1',
      timestamp: new Date().toISOString(),
      level: 'info',
      agentId: 'lead-scoring',
      agentName: 'Lead Scoring Agent',
      message: 'Successfully processed lead qualification for TechCorp inquiry',
      duration: 2300,
      userId: 'user-123',
      sessionId: 'session-abc'
    },
    {
      id: '2',
      timestamp: new Date(Date.now() - 120000).toISOString(),
      level: 'success',
      agentId: 'nurturing-campaign',
      agentName: 'Nurturing Campaign Agent',
      message: 'Email sequence automation completed - 45 emails sent successfully',
      duration: 1800,
      details: { emailsSent: 45, bounceRate: 2.1, openRate: 24.5 }
    },
    {
      id: '3',
      timestamp: new Date(Date.now() - 180000).toISOString(),
      level: 'warning',
      agentId: 'inventory-optimization',
      agentName: 'Inventory Optimization Agent',
      message: 'Low stock alert for Product SKU: TECH-001 - Only 5 units remaining',
      details: { sku: 'TECH-001', currentStock: 5, reorderLevel: 10 }
    },
    {
      id: '4',
      timestamp: new Date(Date.now() - 300000).toISOString(),
      level: 'error',
      agentId: 'price-optimization',
      agentName: 'Price Optimization Agent',
      message: 'Failed to update pricing for marketplace integration - API rate limit exceeded',
      duration: 950,
      details: { error: 'RateLimitExceeded', retryAfter: 300, marketplace: 'Amazon' }
    },
    {
      id: '5',
      timestamp: new Date(Date.now() - 420000).toISOString(),
      level: 'info',
      agentId: 'data-collection',
      agentName: 'Data Collection Agent',
      message: 'Scheduled data sync completed - 1,247 records processed',
      duration: 4200,
      details: { recordsProcessed: 1247, source: 'CRM', errors: 0 }
    },
    {
      id: '6',
      timestamp: new Date(Date.now() - 480000).toISOString(),
      level: 'debug',
      agentId: 'master-supervisor',
      agentName: 'Master Business Supervisor',
      message: 'Resource allocation optimization cycle initiated',
      details: { cycle: 'hourly', agentsEvaluated: 32, optimizationsApplied: 5 }
    },
    {
      id: '7',
      timestamp: new Date(Date.now() - 540000).toISOString(),
      level: 'success',
      agentId: 'report-generation',
      agentName: 'Report Generation Agent',
      message: 'Weekly performance report generated and delivered to stakeholders',
      duration: 3100,
      details: { recipients: 8, reportType: 'weekly-performance', size: '2.4MB' }
    },
    {
      id: '8',
      timestamp: new Date(Date.now() - 660000).toISOString(),
      level: 'warning',
      agentId: 'fraud-detection',
      agentName: 'Fraud Detection Agent',
      message: 'Suspicious transaction pattern detected - flagged for manual review',
      details: { transactionId: 'TXN-789456', amount: 2500, riskScore: 85 }
    }
  ]

  useEffect(() => {
    setLogs(mockLogs)
    setFilteredLogs(mockLogs)
  }, [])

  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    if (autoScroll) {
      logsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [logs, autoScroll])

  // Filter logs based on search term, level, and selected agent
  useEffect(() => {
    let filtered = logs

    // Filter by selected agent
    if (selectedAgent && selectedAgent !== 'all') {
      filtered = filtered.filter(log => log.agentId === selectedAgent)
    }

    // Filter by level
    if (levelFilter !== 'all') {
      filtered = filtered.filter(log => log.level === levelFilter)
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(log => 
        log.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.agentName.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Filter by time range
    const now = Date.now()
    const timeFilters = {
      '1h': 60 * 60 * 1000,
      '24h': 24 * 60 * 60 * 1000,
      '7d': 7 * 24 * 60 * 60 * 1000,
      '30d': 30 * 24 * 60 * 60 * 1000
    }
    
    if (timeFilter in timeFilters) {
      const cutoff = now - timeFilters[timeFilter as keyof typeof timeFilters]
      filtered = filtered.filter(log => new Date(log.timestamp).getTime() > cutoff)
    }

    setFilteredLogs(filtered)
  }, [logs, selectedAgent, levelFilter, searchTerm, timeFilter])

  const getLevelIcon = (level: string) => {
    switch (level) {
      case 'error':
        return <AlertTriangle className="h-4 w-4 text-red-500" />
      case 'warning':
        return <AlertTriangle className="h-4 w-4 text-yellow-500" />
      case 'success':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'info':
        return <Info className="h-4 w-4 text-blue-500" />
      case 'debug':
        return <Settings className="h-4 w-4 text-gray-500" />
      default:
        return <Activity className="h-4 w-4 text-gray-500" />
    }
  }

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'error':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'warning':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'success':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'info':
        return 'bg-blue-100 text-blue-800 border-blue-200'
      case 'debug':
        return 'bg-gray-100 text-gray-800 border-gray-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp)
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  }

  const simulateNewLog = () => {
    const newLog: LogEntry = {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      level: ['info', 'success', 'warning', 'error'][Math.floor(Math.random() * 4)] as any,
      agentId: 'lead-scoring',
      agentName: 'Lead Scoring Agent',
      message: 'Simulated log entry for testing real-time updates',
      duration: Math.floor(Math.random() * 3000) + 500
    }
    setLogs(prevLogs => [newLog, ...prevLogs])
  }

  const clearLogs = () => {
    setLogs([])
    setFilteredLogs([])
  }

  const exportLogs = () => {
    const dataStr = JSON.stringify(filteredLogs, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `agent-logs-${new Date().toISOString().split('T')[0]}.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  const toggleLogExpansion = (logId: string) => {
    setExpandedLog(expandedLog === logId ? null : logId)
  }

  return (
    <div className="space-y-6">
      {/* Header with Controls */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-6 w-6 text-blue-600" />
                Agent Activity Logs
                {selectedAgent && (
                  <Badge variant="outline" className="ml-2">
                    Agent: {selectedAgent}
                  </Badge>
                )}
              </CardTitle>
              <p className="text-gray-600 mt-1">
                Real-time activity monitoring and error tracking
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setAutoScroll(!autoScroll)}
                className={autoScroll ? 'bg-blue-50' : ''}
              >
                Auto-scroll {autoScroll ? 'On' : 'Off'}
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsStreaming(!isStreaming)}
                className={`flex items-center gap-1 ${isStreaming ? 'bg-green-50' : ''}`}
              >
                {isStreaming ? <Pause className="h-3 w-3" /> : <Play className="h-3 w-3" />}
                {isStreaming ? 'Streaming' : 'Paused'}
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {/* Filters */}
          <div className="flex flex-col md:flex-row gap-4 mb-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search logs by message or agent name..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <select
                value={levelFilter}
                onChange={(e) => setLevelFilter(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Levels</option>
                <option value="error">Errors</option>
                <option value="warning">Warnings</option>
                <option value="success">Success</option>
                <option value="info">Info</option>
                <option value="debug">Debug</option>
              </select>
              <select
                value={timeFilter}
                onChange={(e) => setTimeFilter(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="1h">Last Hour</option>
                <option value="24h">Last 24 Hours</option>
                <option value="7d">Last 7 Days</option>
                <option value="30d">Last 30 Days</option>
              </select>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={simulateNewLog}
              className="flex items-center gap-1"
            >
              <RefreshCw className="h-3 w-3" />
              Add Test Log
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={exportLogs}
              className="flex items-center gap-1"
            >
              <Download className="h-3 w-3" />
              Export
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={clearLogs}
              className="flex items-center gap-1 text-red-600 hover:text-red-700"
            >
              <Trash2 className="h-3 w-3" />
              Clear
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Logs Display */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg">
              Activity Stream ({filteredLogs.length} entries)
            </CardTitle>
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <div className="flex items-center gap-1">
                <div className={`w-2 h-2 rounded-full ${isStreaming ? 'bg-green-500' : 'bg-gray-400'}`} />
                {isStreaming ? 'Live' : 'Paused'}
              </div>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="max-h-96 overflow-y-auto space-y-2">
            {filteredLogs.length === 0 ? (
              <div className="text-center py-8">
                <Activity className="h-12 w-12 text-gray-400 mx-auto mb-2" />
                <p className="text-gray-500">No logs found matching current filters</p>
              </div>
            ) : (
              filteredLogs.map((log) => (
                <div
                  key={log.id}
                  className={`border rounded-lg p-4 transition-all duration-200 hover:shadow-sm cursor-pointer ${getLevelColor(log.level)}`}
                  onClick={() => toggleLogExpansion(log.id)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3 flex-1">
                      {getLevelIcon(log.level)}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-medium text-sm">{log.agentName}</span>
                          <Badge variant="outline" className="text-xs">
                            {log.level.toUpperCase()}
                          </Badge>
                          {log.duration && (
                            <span className="text-xs text-gray-500 flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              {log.duration}ms
                            </span>
                          )}
                        </div>
                        <p className="text-sm text-gray-800 mb-2">{log.message}</p>
                        <div className="flex items-center gap-4 text-xs text-gray-500">
                          <span className="flex items-center gap-1">
                            <Calendar className="h-3 w-3" />
                            {formatTimestamp(log.timestamp)}
                          </span>
                          {log.userId && (
                            <span className="flex items-center gap-1">
                              <User className="h-3 w-3" />
                              {log.userId}
                            </span>
                          )}
                          {log.sessionId && (
                            <span>Session: {log.sessionId}</span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Expanded details */}
                  {expandedLog === log.id && log.details && (
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <h4 className="text-sm font-medium mb-2">Details:</h4>
                      <pre className="text-xs bg-gray-50 p-3 rounded overflow-x-auto">
                        {JSON.stringify(log.details, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              ))
            )}
            <div ref={logsEndRef} />
          </div>
        </CardContent>
      </Card>

      {/* Log Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        {['error', 'warning', 'success', 'info', 'debug'].map((level) => {
          const count = filteredLogs.filter(log => log.level === level).length
          return (
            <Card key={level} className="text-center">
              <CardContent className="p-4">
                <div className="flex items-center justify-center mb-2">
                  {getLevelIcon(level)}
                </div>
                <div className="text-2xl font-bold">{count}</div>
                <div className="text-sm text-gray-600 capitalize">{level}</div>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
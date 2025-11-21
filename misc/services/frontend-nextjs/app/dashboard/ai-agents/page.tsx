'use client';

// BizOSaaS AI Agents Management Dashboard
// Enhanced with real-time monitoring and advanced agent control capabilities

import { useEffect, useState } from 'react';
import { 
  Bot,
  Activity,
  Clock,
  CheckCircle,
  AlertCircle,
  PauseCircle,
  PlayCircle,
  Settings,
  Plus,
  Filter,
  Search,
  TrendingUp,
  BarChart3,
  Monitor,
  Zap,
  Grid3X3,
  List,
  Maximize2,
  Minimize2,
  RefreshCw
} from 'lucide-react';
import { RealTimeAgentGrid } from '@/components/monitoring/RealTimeAgentGrid';
import { LiveActivityMonitor } from '@/components/monitoring/LiveActivityMonitor';
import { useDashboardStore, useRealTimeStore } from '@/lib/store';
import { useRealTimeConnection } from '@/lib/websocket';

// Mock data for AI Agents with detailed information - using store-compatible format
const mockAIAgents = [
  {
    id: '1',
    name: 'Campaign Optimizer Pro',
    type: 'campaign_optimizer',
    status: 'active' as const,
    tenant_id: '00000000-0000-4000-8000-000000000001',
    capabilities: ['facebook_ads_optimization', 'google_ads_optimization', 'budget_allocation', 'a_b_testing'],
    current_task: 'Optimizing Q1 Lead Generation campaign for conversion rate',
    progress: 75,
    efficiency_score: 89,
    tasks_completed: 245,
    success_rate: 94.3,
    created_at: '2024-01-01T00:00:00Z',
    last_activity: new Date().toISOString(),
    last_updated: new Date().toISOString(),
  },
  {
    id: '2',
    name: 'Lead Scoring Intelligence',
    type: 'lead_scorer',
    status: 'busy' as const,
    tenant_id: '00000000-0000-4000-8000-000000000001',
    capabilities: ['lead_qualification', 'behavior_analysis', 'predictive_scoring', 'crm_integration'],
    current_task: 'Analyzing 150 new leads from recent campaign',
    progress: 42,
    efficiency_score: 92,
    tasks_completed: 189,
    success_rate: 96.1,
    created_at: '2024-01-01T00:00:00Z',
    last_activity: new Date().toISOString(),
    last_updated: new Date().toISOString(),
  },
  {
    id: '3',
    name: 'Content Curator AI',
    type: 'content_generator',
    status: 'idle' as const,
    tenant_id: '00000000-0000-4000-8000-000000000001',
    capabilities: ['content_generation', 'social_media_posts', 'email_templates', 'blog_articles'],
    current_task: null,
    progress: 0,
    efficiency_score: 87,
    tasks_completed: 156,
    success_rate: 91.2,
    created_at: '2024-01-01T00:00:00Z',
    last_activity: new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
    last_updated: new Date().toISOString(),
  },
  {
    id: '4',
    name: 'Audience Analyzer Pro',
    type: 'audience_analyzer',
    status: 'active' as const,
    tenant_id: '00000000-0000-4000-8000-000000000001',
    capabilities: ['demographic_analysis', 'interest_profiling', 'lookalike_audiences', 'segmentation'],
    current_task: 'Building lookalike audiences from top converting customers',
    progress: 88,
    efficiency_score: 94,
    tasks_completed: 98,
    success_rate: 97.8,
    created_at: '2024-01-01T00:00:00Z',
    last_activity: new Date().toISOString(),
    last_updated: new Date().toISOString(),
  },
  {
    id: '5',
    name: 'Performance Monitor',
    type: 'performance_monitor',
    status: 'error' as const,
    tenant_id: '00000000-0000-4000-8000-000000000001',
    capabilities: ['campaign_monitoring', 'alert_generation', 'performance_tracking', 'anomaly_detection'],
    current_task: null,
    progress: 0,
    efficiency_score: 76,
    tasks_completed: 321,
    success_rate: 88.4,
    created_at: '2024-01-01T00:00:00Z',
    last_activity: new Date(Date.now() - 1800000).toISOString(), // 30 minutes ago
    last_updated: new Date().toISOString(),
  },
  {
    id: '6',
    name: 'ROI Optimization Engine',
    type: 'roi_optimizer',
    status: 'active' as const,
    tenant_id: '00000000-0000-4000-8000-000000000001',
    capabilities: ['budget_optimization', 'bid_management', 'roi_analysis', 'cost_reduction'],
    current_task: 'Optimizing budget allocation across 5 active campaigns',
    progress: 63,
    efficiency_score: 91,
    tasks_completed: 134,
    success_rate: 93.7,
    created_at: '2024-01-01T00:00:00Z',
    last_activity: new Date().toISOString(),
    last_updated: new Date().toISOString(),
  }
];

export default function AIAgentsPage() {
  const [viewMode, setViewMode] = useState<'grid' | 'list' | 'monitoring'>('monitoring');
  const [isActivityExpanded, setIsActivityExpanded] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  
  // Dashboard store for agent data
  const { aiAgents, setAIAgents, agentsLoading, setAgentsLoading } = useDashboardStore();
  
  // Real-time connection
  const { connected, lastUpdate } = useRealTimeConnection(true);

  // Initialize mock data
  useEffect(() => {
    setAIAgents(mockAIAgents);
  }, [setAIAgents]);

  // Handle manual refresh
  const handleRefresh = async () => {
    setRefreshing(true);
    setAgentsLoading(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Update agents with slight changes to simulate real activity
    const updatedAgents = mockAIAgents.map(agent => ({
      ...agent,
      last_updated: new Date().toISOString(),
      efficiency_score: Math.max(70, Math.min(98, agent.efficiency_score + (Math.random() - 0.5) * 4)),
      progress: agent.current_task ? Math.max(0, Math.min(100, agent.progress + Math.random() * 10)) : 0,
    }));
    
    setAIAgents(updatedAgents);
    setAgentsLoading(false);
    setRefreshing(false);
  };

  const getViewModeTitle = () => {
    switch (viewMode) {
      case 'grid': return 'Agent Grid View';
      case 'list': return 'Agent List View';  
      case 'monitoring': return 'Real-time Monitoring';
      default: return 'AI Agent Management';
    }
  };

  const getViewModeDescription = () => {
    switch (viewMode) {
      case 'grid': return 'Interactive grid with agent cards and controls';
      case 'list': return 'Detailed list view with comprehensive agent information';
      case 'monitoring': return 'Live monitoring with real-time updates and activity streams';
      default: return 'Manage and monitor your autonomous AI agents';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Enhanced Header */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">AI Agent Management</h1>
              <p className="text-gray-600 mt-1">
                {getViewModeDescription()}
              </p>
            </div>
            
            <div className="flex items-center gap-4">
              {/* Real-time Status */}
              <div className="flex items-center gap-2 text-sm">
                <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
                <span className={connected ? 'text-green-600' : 'text-red-600'}>
                  {connected ? 'Real-time Active' : 'Connection Lost'}
                </span>
                {lastUpdate && (
                  <span className="text-gray-500 text-xs">
                    Updated {new Date(lastUpdate).toLocaleTimeString()}
                  </span>
                )}
              </div>

              {/* Refresh Button */}
              <button
                onClick={handleRefresh}
                disabled={refreshing}
                className="flex items-center gap-2 px-3 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors disabled:opacity-50"
              >
                <RefreshCw className={`h-4 w-4 ${refreshing ? 'animate-spin' : ''}`} />
                {refreshing ? 'Refreshing...' : 'Refresh'}
              </button>
            </div>
          </div>

          {/* View Mode Toggle */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-gray-700">View Mode:</span>
              <div className="flex rounded-lg bg-gray-100 p-1">
                <button
                  onClick={() => setViewMode('monitoring')}
                  className={`flex items-center gap-2 px-3 py-1 rounded-md text-sm transition-colors ${
                    viewMode === 'monitoring' 
                      ? 'bg-white text-gray-900 shadow-sm' 
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <Monitor className="h-4 w-4" />
                  Real-time Monitoring
                </button>
                <button
                  onClick={() => setViewMode('grid')}
                  className={`flex items-center gap-2 px-3 py-1 rounded-md text-sm transition-colors ${
                    viewMode === 'grid' 
                      ? 'bg-white text-gray-900 shadow-sm' 
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <Grid3X3 className="h-4 w-4" />
                  Grid View
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`flex items-center gap-2 px-3 py-1 rounded-md text-sm transition-colors ${
                    viewMode === 'list' 
                      ? 'bg-white text-gray-900 shadow-sm' 
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <List className="h-4 w-4" />
                  List View
                </button>
              </div>
            </div>

            {/* Activity Monitor Toggle */}
            {viewMode === 'monitoring' && (
              <button
                onClick={() => setIsActivityExpanded(!isActivityExpanded)}
                className="flex items-center gap-2 px-3 py-2 bg-purple-50 text-purple-600 rounded-lg hover:bg-purple-100 transition-colors"
              >
                {isActivityExpanded ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
                {isActivityExpanded ? 'Minimize' : 'Expand'} Activity Monitor
              </button>
            )}
          </div>
        </div>

        {/* Real-time Monitoring View */}
        {viewMode === 'monitoring' && (
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
            {/* Agent Grid - Takes up 2 columns on XL screens */}
            <div className="xl:col-span-2">
              <RealTimeAgentGrid />
            </div>
            
            {/* Live Activity Monitor - Takes up 1 column */}
            <div className="xl:col-span-1">
              <LiveActivityMonitor 
                className={isActivityExpanded ? 'xl:col-span-3' : ''}
                maxItems={isActivityExpanded ? 100 : 30}
              />
            </div>
          </div>
        )}

        {/* Grid View */}
        {viewMode === 'grid' && (
          <RealTimeAgentGrid />
        )}

        {/* List View - Legacy detailed view */}
        {viewMode === 'list' && (
          <div className="space-y-6">
            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
                <div className="flex items-center">
                  <Bot className="h-8 w-8 text-blue-600" />
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">{aiAgents.length}</h3>
                    <p className="text-sm text-gray-600">Total Agents</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
                <div className="flex items-center">
                  <CheckCircle className="h-8 w-8 text-green-600" />
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {aiAgents.filter(a => a.status === 'active' || a.status === 'busy').length}
                    </h3>
                    <p className="text-sm text-gray-600">Active Agents</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
                <div className="flex items-center">
                  <TrendingUp className="h-8 w-8 text-purple-600" />
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {Math.round(aiAgents.reduce((sum, a) => sum + (a.efficiency_score || 0), 0) / aiAgents.length)}%
                    </h3>
                    <p className="text-sm text-gray-600">Avg Efficiency</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
                <div className="flex items-center">
                  <BarChart3 className="h-8 w-8 text-green-600" />
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {aiAgents.reduce((sum, a) => sum + (a.tasks_completed || 0), 0)}
                    </h3>
                    <p className="text-sm text-gray-600">Total Tasks</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Detailed Agent List */}
            <div className="bg-white rounded-lg shadow border border-gray-200">
              <div className="p-6">
                <div className="space-y-6">
                  {aiAgents.map((agent) => (
                    <div key={agent.id} className="border border-gray-200 rounded-lg p-6">
                      <div className="flex items-start justify-between">
                        <div className="flex items-start space-x-4">
                          <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg">
                            <Bot className="h-6 w-6 text-blue-600" />
                          </div>
                          
                          <div className="flex-1">
                            <div className="flex items-center space-x-3 mb-2">
                              <h3 className="text-lg font-semibold text-gray-900">{agent.name}</h3>
                              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${
                                agent.status === 'active' ? 'bg-green-100 text-green-800' :
                                agent.status === 'busy' ? 'bg-yellow-100 text-yellow-800' :
                                agent.status === 'idle' ? 'bg-gray-100 text-gray-800' :
                                agent.status === 'error' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'
                              }`}>
                                {agent.status}
                              </span>
                            </div>
                            
                            <p className="text-sm text-gray-600 mb-3">
                              {agent.capabilities.join(', ')}
                            </p>
                            
                            {agent.current_task && (
                              <div className="mb-3">
                                <p className="text-sm text-gray-700 mb-1">
                                  <span className="font-medium">Current Task:</span> {agent.current_task}
                                </p>
                                <div className="w-full bg-gray-200 rounded-full h-2">
                                  <div 
                                    className="bg-blue-600 h-2 rounded-full transition-all duration-300" 
                                    style={{ width: `${agent.progress || 0}%` }}
                                  />
                                </div>
                                <p className="text-xs text-gray-500 mt-1">{agent.progress || 0}% complete</p>
                              </div>
                            )}
                            
                            <div className="grid grid-cols-3 gap-4 text-sm">
                              <div>
                                <span className="text-gray-500">Efficiency:</span>
                                <span className="ml-1 font-medium">{agent.efficiency_score || 0}%</span>
                              </div>
                              <div>
                                <span className="text-gray-500">Success Rate:</span>
                                <span className="ml-1 font-medium">{agent.success_rate || 0}%</span>
                              </div>
                              <div>
                                <span className="text-gray-500">Tasks Done:</span>
                                <span className="ml-1 font-medium">{agent.tasks_completed || 0}</span>
                              </div>
                            </div>
                            
                            <div className="mt-4">
                              <p className="text-xs text-gray-500">
                                Last activity: {new Date(agent.last_activity).toLocaleString()}
                              </p>
                            </div>
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-2">
                          <button className="flex items-center px-3 py-1 bg-gray-50 text-gray-600 rounded-md hover:bg-gray-100 transition-colors">
                            <Settings className="mr-1 h-4 w-4" />
                            Configure
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
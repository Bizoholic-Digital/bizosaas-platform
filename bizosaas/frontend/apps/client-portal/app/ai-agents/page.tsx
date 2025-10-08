'use client';

import React, { useState, useEffect } from 'react';
import {
  Bot, Zap, Activity, Clock, CheckCircle, AlertTriangle,
  Pause, Play, Settings, TrendingUp, Users, Target,
  BarChart3, RefreshCw, Plus, Eye, Edit, Trash2,
  Filter, Search, ChevronDown, ChevronRight
} from 'lucide-react';

interface Agent {
  id: string;
  name: string;
  role: string;
  status: 'active' | 'paused' | 'error';
}

interface Crew {
  id: string;
  name: string;
  description: string;
  agents: Agent[];
  status: 'active' | 'paused' | 'error';
  created_at: string;
  last_activity: string;
  total_tasks: number;
  success_rate: number;
}

interface AgentStats {
  active_agents: number;
  running_tasks: number;
  success_rate: number;
  total_executions: number;
}

interface RecentActivity {
  id: number;
  type: string;
  agent?: string;
  crew?: string;
  task?: string;
  timestamp: string;
}

export default function AIAgentsDashboard() {
  const [stats, setStats] = useState<AgentStats>({
    active_agents: 0,
    running_tasks: 0,
    success_rate: 0,
    total_executions: 0
  });
  const [crews, setCrews] = useState<Crew[]>([]);
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [expandedCrews, setExpandedCrews] = useState<{[key: string]: boolean}>({});
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadAIAgentsData();
  }, []);

  const loadAIAgentsData = async () => {
    try {
      setLoading(true);

      // Load overview data
      const overviewRes = await fetch('/api/brain/ai-agents/overview');
      if (overviewRes.ok) {
        const overviewData = await overviewRes.json();
        if (overviewData.success) {
          setStats(overviewData.data.stats);
          setRecentActivity(overviewData.data.recent_activity);
        }
      }

      // Load crews data
      const crewsRes = await fetch('/api/brain/ai-agents/crews');
      if (crewsRes.ok) {
        const crewsData = await crewsRes.json();
        if (crewsData.success) {
          setCrews(crewsData.data);
        }
      }

    } catch (error) {
      console.error('Error loading AI agents data:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleCrewExpansion = (crewId: string) => {
    setExpandedCrews(prev => ({
      ...prev,
      [crewId]: !prev[crewId]
    }));
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100';
      case 'paused': return 'text-yellow-600 bg-yellow-100';
      case 'error': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircle className="w-4 h-4" />;
      case 'paused': return <Pause className="w-4 h-4" />;
      case 'error': return <AlertTriangle className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };

  const filteredCrews = crews.filter(crew => {
    const matchesFilter = filter === 'all' || crew.status === filter;
    const matchesSearch = crew.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         crew.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading AI agents...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">🤖 AI Agents Hub</h1>
              <p className="text-gray-600 dark:text-gray-400 mt-2">
                Manage and monitor your 93 AI agents across all business operations
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={loadAIAgentsData}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2"
              >
                <RefreshCw className="w-4 h-4" />
                <span>Refresh</span>
              </button>
              <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center space-x-2">
                <Plus className="w-4 h-4" />
                <span>Deploy New Crew</span>
              </button>
            </div>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center">
                <Bot className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Active Agents</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.active_agents}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Running Tasks</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.running_tasks}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Success Rate</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.success_rate}%</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-orange-600 dark:text-orange-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Executions</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.total_executions.toLocaleString()}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white dark:bg-gray-900 rounded-lg border mb-6">
          <div className="flex space-x-8 p-4 overflow-x-auto">
            {[
              { id: 'overview', label: 'Overview', icon: BarChart3 },
              { id: 'crews', label: 'Agent Crews', icon: Users },
              { id: 'tasks', label: 'Active Tasks', icon: Activity },
              { id: 'tools', label: 'Tools & Integrations', icon: Settings }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
                      : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Agent Crews Summary */}
            <div className="bg-white dark:bg-gray-900 rounded-lg border p-6">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Agent Crews</h2>
              <div className="space-y-4">
                {crews.slice(0, 3).map((crew) => (
                  <div key={crew.id} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded-lg ${getStatusColor(crew.status)}`}>
                        {getStatusIcon(crew.status)}
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-white">{crew.name}</h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {crew.agents.length} agents • {crew.success_rate}% success
                        </p>
                      </div>
                    </div>
                    <button className="text-gray-400 hover:text-gray-600">
                      <Eye className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-white dark:bg-gray-900 rounded-lg border p-6">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Recent Activity</h2>
              <div className="space-y-4">
                {recentActivity.map((activity) => (
                  <div key={activity.id} className="flex items-start space-x-3">
                    <div className="w-2 h-2 bg-blue-600 rounded-full mt-2"></div>
                    <div className="flex-1">
                      <p className="text-sm text-gray-900 dark:text-white">
                        {activity.type === 'task_completed' && `✅ ${activity.agent} completed "${activity.task}"`}
                        {activity.type === 'crew_deployed' && `🚀 ${activity.crew} was deployed`}
                        {activity.type === 'task_failed' && `❌ ${activity.agent} failed "${activity.task}"`}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        {new Date(activity.timestamp).toLocaleString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'crews' && (
          <div>
            {/* Filters */}
            <div className="bg-white dark:bg-gray-900 rounded-lg border p-4 mb-6">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <Filter className="w-4 h-4 text-gray-400" />
                  <select
                    value={filter}
                    onChange={(e) => setFilter(e.target.value)}
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                  >
                    <option value="all">All Status</option>
                    <option value="active">Active</option>
                    <option value="paused">Paused</option>
                    <option value="error">Error</option>
                  </select>
                </div>
                <div className="flex-1 relative">
                  <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search crews..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                  />
                </div>
              </div>
            </div>

            {/* Crews List */}
            <div className="space-y-4">
              {filteredCrews.map((crew) => (
                <div key={crew.id} className="bg-white dark:bg-gray-900 rounded-lg border">
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-3">
                        <button
                          onClick={() => toggleCrewExpansion(crew.id)}
                          className="p-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded"
                        >
                          {expandedCrews[crew.id] ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                        </button>
                        <div className={`p-2 rounded-lg ${getStatusColor(crew.status)}`}>
                          {getStatusIcon(crew.status)}
                        </div>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{crew.name}</h3>
                          <p className="text-sm text-gray-600 dark:text-gray-400">{crew.description}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <button className="p-2 text-gray-400 hover:text-blue-600 rounded">
                          <Eye className="w-4 h-4" />
                        </button>
                        <button className="p-2 text-gray-400 hover:text-green-600 rounded">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button className="p-2 text-gray-400 hover:text-yellow-600 rounded">
                          <Settings className="w-4 h-4" />
                        </button>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-gray-900 dark:text-white">{crew.agents.length}</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">Agents</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-gray-900 dark:text-white">{crew.total_tasks}</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">Total Tasks</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">{crew.success_rate}%</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">Success Rate</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-gray-900 dark:text-white">
                          {new Date(crew.last_activity).toLocaleDateString()}
                        </div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">Last Active</div>
                      </div>
                    </div>

                    {expandedCrews[crew.id] && (
                      <div className="border-t pt-4">
                        <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Agents in this Crew</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                          {crew.agents.map((agent) => (
                            <div key={agent.id} className="flex items-center space-x-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                              <div className={`w-2 h-2 rounded-full ${
                                agent.status === 'active' ? 'bg-green-500' :
                                agent.status === 'paused' ? 'bg-yellow-500' : 'bg-red-500'
                              }`}></div>
                              <div>
                                <div className="font-medium text-gray-900 dark:text-white">{agent.name}</div>
                                <div className="text-sm text-gray-600 dark:text-gray-400">{agent.role}</div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'tasks' && (
          <div className="bg-white dark:bg-gray-900 rounded-lg border p-8 text-center">
            <Activity className="w-12 h-12 text-blue-600 mx-auto mb-4" />
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Active Tasks</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Monitor and manage all active AI agent tasks in real-time
            </p>
            <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
              View Task Queue
            </button>
          </div>
        )}

        {activeTab === 'tools' && (
          <div className="bg-white dark:bg-gray-900 rounded-lg border p-8 text-center">
            <Settings className="w-12 h-12 text-blue-600 mx-auto mb-4" />
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Tools & Integrations</h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Configure AI agent tools and external service integrations
            </p>
            <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
              Manage Tools
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
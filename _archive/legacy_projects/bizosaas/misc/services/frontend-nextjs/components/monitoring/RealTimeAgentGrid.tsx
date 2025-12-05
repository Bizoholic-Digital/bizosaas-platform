'use client';

// Real-time AI Agent Grid Component for BizOSaaS Dashboard
// Displays live agent status, tasks, and performance metrics

import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { 
  Activity, 
  Bot, 
  Brain, 
  CheckCircle, 
  Circle, 
  AlertCircle, 
  XCircle,
  Play,
  Pause,
  Square,
  TrendingUp,
  Clock,
  Zap
} from 'lucide-react';
import { useDashboardStore, useRealTimeStore } from '@/lib/store';
import { useRealTimeConnection } from '@/lib/websocket';
import { AIAgent } from '@/lib/types';

interface AgentCardProps {
  agent: AIAgent;
  onAction: (agentId: string, action: 'start' | 'pause' | 'stop') => void;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent, onAction }) => {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active': return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'idle': return <Circle className="h-4 w-4 text-blue-500" />;
      case 'busy': return <Activity className="h-4 w-4 text-yellow-500 animate-pulse" />;
      case 'error': return <XCircle className="h-4 w-4 text-red-500" />;
      case 'stopped': return <Square className="h-4 w-4 text-gray-500" />;
      default: return <AlertCircle className="h-4 w-4 text-orange-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800 border-green-200';
      case 'idle': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'busy': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'error': return 'bg-red-100 text-red-800 border-red-200';
      case 'stopped': return 'bg-gray-100 text-gray-800 border-gray-200';
      default: return 'bg-orange-100 text-orange-800 border-orange-200';
    }
  };

  const getEfficiencyColor = (score: number) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 75) return 'text-blue-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Bot className="h-5 w-5 text-blue-600" />
            <CardTitle className="text-base">{agent.name}</CardTitle>
          </div>
          <Badge className={getStatusColor(agent.status)} variant="outline">
            {getStatusIcon(agent.status)}
            <span className="ml-1 capitalize">{agent.status}</span>
          </Badge>
        </div>
        <CardDescription className="text-sm">
          {agent.capabilities.slice(0, 2).join(', ')}
          {agent.capabilities.length > 2 && ` +${agent.capabilities.length - 2} more`}
        </CardDescription>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Current Task */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Brain className="h-4 w-4" />
            <span>Current Task</span>
          </div>
          <div className="bg-gray-50 rounded-md p-2 text-sm">
            {agent.current_task || 'No active task'}
          </div>
          {agent.current_task && (
            <Progress 
              value={agent.progress || 0} 
              className="h-2"
            />
          )}
        </div>

        {/* Performance Metrics */}
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center">
            <div className="text-xs text-gray-500 mb-1">Efficiency</div>
            <div className={`text-lg font-semibold ${getEfficiencyColor(agent.efficiency_score || 0)}`}>
              {agent.efficiency_score || 0}%
            </div>
          </div>
          <div className="text-center">
            <div className="text-xs text-gray-500 mb-1">Tasks Done</div>
            <div className="text-lg font-semibold text-gray-700">
              {agent.tasks_completed || 0}
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        {agent.last_activity && (
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs text-gray-500">
              <Clock className="h-3 w-3" />
              <span>Last Active: {new Date(agent.last_activity).toLocaleTimeString()}</span>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-2 pt-2 border-t">
          {agent.status === 'stopped' && (
            <Button
              size="sm"
              variant="outline"
              onClick={() => onAction(agent.id, 'start')}
              className="flex-1"
            >
              <Play className="h-3 w-3 mr-1" />
              Start
            </Button>
          )}
          
          {(agent.status === 'active' || agent.status === 'busy') && (
            <Button
              size="sm"
              variant="outline"
              onClick={() => onAction(agent.id, 'pause')}
              className="flex-1"
            >
              <Pause className="h-3 w-3 mr-1" />
              Pause
            </Button>
          )}
          
          {agent.status !== 'stopped' && (
            <Button
              size="sm"
              variant="outline"
              onClick={() => onAction(agent.id, 'stop')}
              className="flex-1"
            >
              <Square className="h-3 w-3 mr-1" />
              Stop
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

interface RealTimeAgentGridProps {
  className?: string;
}

export const RealTimeAgentGrid: React.FC<RealTimeAgentGridProps> = ({ className }) => {
  const { aiAgents, agentsLoading, setAgentsLoading } = useDashboardStore();
  const { connected, lastUpdate } = useRealTimeConnection(true);
  const [filter, setFilter] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'name' | 'efficiency' | 'status'>('name');

  // Filter agents based on status
  const filteredAgents = aiAgents.filter(agent => {
    if (filter === 'all') return true;
    if (filter === 'active') return agent.status === 'active' || agent.status === 'busy';
    if (filter === 'inactive') return agent.status === 'idle' || agent.status === 'stopped';
    if (filter === 'error') return agent.status === 'error';
    return agent.status === filter;
  });

  // Sort agents
  const sortedAgents = [...filteredAgents].sort((a, b) => {
    switch (sortBy) {
      case 'efficiency':
        return (b.efficiency_score || 0) - (a.efficiency_score || 0);
      case 'status':
        return a.status.localeCompare(b.status);
      case 'name':
      default:
        return a.name.localeCompare(b.name);
    }
  });

  const handleAgentAction = async (agentId: string, action: 'start' | 'pause' | 'stop') => {
    try {
      setAgentsLoading(true);
      
      // In a real implementation, this would call the API
      console.log(`[Agent Control] ${action} agent ${agentId}`);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Update agent status optimistically
      const dashboardStore = useDashboardStore.getState();
      const newStatus = action === 'start' ? 'active' : action === 'pause' ? 'idle' : 'stopped';
      dashboardStore.updateAIAgent(agentId, { status: newStatus });
      
    } catch (error) {
      console.error('[Agent Control] Failed to control agent:', error);
    } finally {
      setAgentsLoading(false);
    }
  };

  const getActiveAgentCount = () => {
    return aiAgents.filter(agent => agent.status === 'active' || agent.status === 'busy').length;
  };

  const getAverageEfficiency = () => {
    const scores = aiAgents.map(agent => agent.efficiency_score || 0).filter(score => score > 0);
    return scores.length > 0 ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0;
  };

  return (
    <div className={`space-y-6 ${className || ''}`}>
      {/* Header with Real-time Status */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">AI Agent Monitoring</h2>
          <p className="text-gray-600">
            Real-time status and performance of autonomous AI agents
          </p>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-sm">
            <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
            <span className={connected ? 'text-green-600' : 'text-red-600'}>
              {connected ? 'Live' : 'Disconnected'}
            </span>
          </div>
          
          {lastUpdate && (
            <div className="text-xs text-gray-500">
              Updated: {new Date(lastUpdate).toLocaleTimeString()}
            </div>
          )}
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-green-600" />
              <div>
                <div className="text-sm text-gray-600">Active Agents</div>
                <div className="text-2xl font-bold text-green-600">
                  {getActiveAgentCount()}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <Bot className="h-5 w-5 text-blue-600" />
              <div>
                <div className="text-sm text-gray-600">Total Agents</div>
                <div className="text-2xl font-bold text-blue-600">
                  {aiAgents.length}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-purple-600" />
              <div>
                <div className="text-sm text-gray-600">Avg Efficiency</div>
                <div className="text-2xl font-bold text-purple-600">
                  {getAverageEfficiency()}%
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center gap-2">
              <Zap className="h-5 w-5 text-yellow-600" />
              <div>
                <div className="text-sm text-gray-600">Tasks Today</div>
                <div className="text-2xl font-bold text-yellow-600">
                  {aiAgents.reduce((total, agent) => total + (agent.tasks_completed || 0), 0)}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters and Sorting */}
      <div className="flex flex-wrap items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium">Filter:</span>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="border border-gray-300 rounded-md px-2 py-1 text-sm"
          >
            <option value="all">All Agents</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="error">Error</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-sm font-medium">Sort by:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="border border-gray-300 rounded-md px-2 py-1 text-sm"
          >
            <option value="name">Name</option>
            <option value="efficiency">Efficiency</option>
            <option value="status">Status</option>
          </select>
        </div>
      </div>

      {/* Agent Grid */}
      {agentsLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {[...Array(8)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardHeader>
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="h-3 bg-gray-200 rounded"></div>
                  <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                  <div className="h-8 bg-gray-200 rounded"></div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : sortedAgents.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {sortedAgents.map(agent => (
            <AgentCard
              key={agent.id}
              agent={agent}
              onAction={handleAgentAction}
            />
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="p-8 text-center">
            <Bot className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No Agents Found
            </h3>
            <p className="text-gray-600">
              No AI agents match the current filter criteria.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
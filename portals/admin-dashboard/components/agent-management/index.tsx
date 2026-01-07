'use client';

import React, { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import {
  Bot,
  Activity,
  Settings,
  Target,
  BarChart3,
  Shield,
  FlaskConical,
  ChevronLeft
} from 'lucide-react';

// Import all agent management components
import AgentManagementDashboard from './AgentManagementDashboard';
import AgentStatusMonitor from './AgentStatusMonitor';
import AgentConfigurationManager from './AgentConfigurationManager';
import TaskManagementInterface from './TaskManagementInterface';
import PerformanceAnalyticsDashboard from './PerformanceAnalyticsDashboard';
import AgentAccessControl from './AgentAccessControl';
import PlaygroundManager from './PlaygroundManager';

// Component interface for dynamic loading
interface AgentManagementComponent {
  id: string;
  name: string;
  description: string;
  icon: React.ElementType;
  component: React.ComponentType<any>;
  requiresAgentId?: boolean;
  permissions?: string[];
}

// Available components configuration
const AGENT_MANAGEMENT_COMPONENTS: AgentManagementComponent[] = [
  {
    id: 'dashboard',
    name: 'Agent Overview',
    description: 'Complete hierarchical view of all 88 agents across 6 domains',
    icon: Bot,
    component: AgentManagementDashboard,
    permissions: ['agent.view']
  },
  {
    id: 'monitoring',
    name: 'Real-time Monitoring',
    description: 'Live status, performance metrics, and health monitoring',
    icon: Activity,
    component: AgentStatusMonitor,
    requiresAgentId: true,
    permissions: ['monitor.view']
  },
  {
    id: 'configuration',
    name: 'Configuration Management',
    description: 'Agent settings, resource allocation, and API configurations',
    icon: Settings,
    component: AgentConfigurationManager,
    requiresAgentId: true,
    permissions: ['config.view', 'config.modify']
  },
  {
    id: 'tasks',
    name: 'Task Management',
    description: 'Assign tasks, monitor progress, and track completion',
    icon: Target,
    component: TaskManagementInterface,
    permissions: ['task.view', 'task.create']
  },
  {
    id: 'analytics',
    name: 'Performance Analytics',
    description: 'Efficiency metrics, success rates, and ROI analysis',
    icon: BarChart3,
    component: PerformanceAnalyticsDashboard,
    permissions: ['analytics.view']
  },
  {
    id: 'security',
    name: 'Access Control',
    description: 'Role-based permissions and security management',
    icon: Shield,
    component: AgentAccessControl,
    permissions: ['user.manage', 'system.admin']
  },
  {
    id: 'playground',
    name: 'Agent Playground',
    description: 'Sandboxed environment for testing and fine-tuning agents safely',
    icon: FlaskConical,
    component: PlaygroundManager,
    requiresAgentId: true,
    permissions: ['agent.playground']
  }
];

// Simple permission check (would be replaced with actual auth system)
const hasPermission = (permissions: string[] = []): boolean => {
  // Simulate admin user with all permissions for demo
  return true;
};

// Main Agent Management Interface
export default function AgentManagementInterface() {
  const [activeComponent, setActiveComponent] = useState<string>('dashboard');
  const [selectedAgentId, setSelectedAgentId] = useState<string>('lead-scoring-agent');

  // Filter components based on permissions
  const availableComponents = AGENT_MANAGEMENT_COMPONENTS.filter(component =>
    hasPermission(component.permissions)
  );

  const currentComponent = availableComponents.find(c => c.id === activeComponent);

  const renderComponent = () => {
    if (!currentComponent) return null;

    const ComponentToRender = currentComponent.component;
    const props = currentComponent.requiresAgentId ? { agentId: selectedAgentId } : {};

    return <ComponentToRender {...props} />;
  };

  const getComponentStats = () => {
    // Mock stats for the header
    return {
      totalAgents: 88,
      activeAgents: 76,
      domainsManaged: 6,
      tasksInProgress: 145
    };
  };

  const stats = getComponentStats();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Bot className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  BizOSaaS Agent Management Center
                </h1>
                <p className="text-gray-600">
                  Comprehensive AI Agent Ecosystem Control Panel
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {/* Quick Stats */}
            <div className="hidden md:flex items-center space-x-6 text-sm">
              <div className="text-center">
                <p className="font-semibold text-gray-900">{stats.totalAgents}</p>
                <p className="text-gray-500">Total Agents</p>
              </div>
              <div className="text-center">
                <p className="font-semibold text-green-600">{stats.activeAgents}</p>
                <p className="text-gray-500">Active</p>
              </div>
              <div className="text-center">
                <p className="font-semibold text-blue-600">{stats.domainsManaged}</p>
                <p className="text-gray-500">Domains</p>
              </div>
              <div className="text-center">
                <p className="font-semibold text-orange-600">{stats.tasksInProgress}</p>
                <p className="text-gray-500">Tasks</p>
              </div>
            </div>

            {/* Current user indicator */}
            <Badge variant="outline" className="bg-green-100 text-green-800">
              Super Admin
            </Badge>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200 px-6">
        <Tabs value={activeComponent} onValueChange={setActiveComponent}>
          <TabsList className="bg-transparent border-b-0 h-auto p-0">
            {availableComponents.map((component) => {
              const Icon = component.icon;
              return (
                <TabsTrigger
                  key={component.id}
                  value={component.id}
                  className="flex items-center space-x-2 px-4 py-3 border-b-2 border-transparent data-[state=active]:border-blue-500 data-[state=active]:bg-transparent data-[state=active]:text-blue-600 hover:text-blue-600 transition-colors"
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden sm:inline">{component.name}</span>
                </TabsTrigger>
              );
            })}
          </TabsList>
        </Tabs>
      </div>

      {/* Current Component Info */}
      {currentComponent && (
        <div className="bg-blue-50 border-b border-blue-200 px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <currentComponent.icon className="w-5 h-5 text-blue-600" />
              <div>
                <h2 className="font-medium text-blue-900">{currentComponent.name}</h2>
                <p className="text-sm text-blue-700">{currentComponent.description}</p>
              </div>
            </div>

            {/* Agent selector for agent-specific components */}
            {currentComponent.requiresAgentId && (
              <div className="flex items-center space-x-2">
                <span className="text-sm text-blue-700">Viewing:</span>
                <select
                  value={selectedAgentId}
                  onChange={(e) => setSelectedAgentId(e.target.value)}
                  className="px-3 py-1 border border-blue-300 rounded-md bg-white text-blue-900 text-sm"
                >
                  <option value="lead-scoring-agent">Lead Scoring Agent</option>
                  <option value="content-creation-agent">Content Creation Agent</option>
                  <option value="product-recommendation-agent">Product Recommendation Agent</option>
                  <option value="payment-processing-agent">Payment Processing Agent</option>
                  <option value="seo-optimization-agent">SEO Optimization Agent</option>
                  <option value="data-collection-agent">Data Collection Agent</option>
                </select>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Main Content Area */}
      <div className="p-6">
        <Tabs value={activeComponent}>
          {availableComponents.map((component) => (
            <TabsContent key={component.id} value={component.id} className="mt-0">
              {renderComponent()}
            </TabsContent>
          ))}
        </Tabs>
      </div>

      {/* Footer */}
      <div className="bg-white border-t border-gray-200 px-6 py-4 mt-12">
        <div className="flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center space-x-4">
            <span>BizOSaaS Agent Management v2.1.0</span>
            <span>•</span>
            <span>88 Agents Across 6 Domains</span>
            <span>•</span>
            <span>Master Orchestration + Domain Supervisors + Specialist Agents</span>
          </div>
          <div className="flex items-center space-x-2">
            <Badge variant="outline" className="bg-green-100 text-green-800">
              System Healthy
            </Badge>
          </div>
        </div>
      </div>
    </div>
  );
}

// Export individual components for direct use
export {
  AgentManagementDashboard,
  AgentStatusMonitor,
  AgentConfigurationManager,
  TaskManagementInterface,
  PerformanceAnalyticsDashboard,
  AgentAccessControl,

  PlaygroundManager,
  AgentManagementInterface,
};
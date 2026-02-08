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
  ChevronLeft,
  Network
} from 'lucide-react';

// Import all agent management components
import AgentManagementDashboard from './AgentManagementDashboard';
import AgentStatusMonitor from './AgentStatusMonitor';
import AgentConfigurationManager from './AgentConfigurationManager';
import TaskManagementInterface from './TaskManagementInterface';
import PerformanceAnalyticsDashboard from './PerformanceAnalyticsDashboard';
import AgentAccessControl from './AgentAccessControl';
import PlaygroundManager from './PlaygroundManager';
import AgentMeshVisualizer from './AgentMeshVisualizer';
import { AgentDashboard } from './agent-dashboard';

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
    id: 'mesh',
    name: 'Agent Mesh',
    description: 'Real-time specialist agent interaction matrix and coordination visualizer',
    icon: Network,
    component: AgentMeshVisualizer,
    permissions: ['mesh.view']
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

import { PageHeader } from '../dashboard/PageHeader';

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
    <div className="min-h-full bg-slate-50 dark:bg-slate-950 flex flex-col animate-in fade-in duration-500">
      <Tabs value={activeComponent} onValueChange={setActiveComponent} className="flex flex-col flex-1 w-full">
        {/* Header - Standardized with PageHeader */}
        <div className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-6 pt-6 -mb-8">
          <PageHeader
            title={
              <div className="flex items-center space-x-2">
                <Bot className="w-8 h-8 text-indigo-600" />
                <div>
                  <h1 className="text-3xl font-black text-slate-900 dark:text-white leading-tight uppercase italic tracking-tighter">
                    Agent <span className="text-indigo-600">Hub</span>
                  </h1>
                  <p className="text-[10px] md:text-xs text-slate-500 dark:text-slate-400 uppercase tracking-[0.2em] font-bold">
                    Core Autonomous Ecosystem
                  </p>
                </div>
              </div>
            }
            description={null}
          >
            <div className="flex items-center space-x-4">
              {/* Quick Stats - Premium Cards Style */}
              <div className="hidden lg:flex items-center space-x-6 text-sm">
                <div className="text-center bg-slate-100 dark:bg-slate-800 px-3 py-1 rounded-lg border border-slate-200 dark:border-slate-700">
                  <p className="font-black text-slate-900 dark:text-white">{stats.totalAgents}</p>
                  <p className="text-[10px] uppercase font-bold text-slate-500">Total</p>
                </div>
                <div className="text-center bg-emerald-50 dark:bg-emerald-900/20 px-3 py-1 rounded-lg border border-emerald-100 dark:border-emerald-900/30">
                  <p className="font-black text-emerald-600 dark:text-emerald-400">{stats.activeAgents}</p>
                  <p className="text-[10px] uppercase font-bold text-emerald-500">Active</p>
                </div>
                <div className="text-center bg-blue-50 dark:bg-blue-900/20 px-3 py-1 rounded-lg border border-blue-100 dark:border-blue-900/30">
                  <p className="font-black text-blue-600 dark:text-blue-400">{stats.domainsManaged}</p>
                  <p className="text-[10px] uppercase font-bold text-blue-500">Domains</p>
                </div>
              </div>

              {/* Current user indicator */}
              <Badge className="bg-indigo-600 hover:bg-indigo-700 text-white border-none font-bold italic tracking-tighter h-8">
                Super Admin
              </Badge>
            </div>
          </PageHeader>
        </div>

        {/* Navigation Tabs - Mobile App Style */}
        <div className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-4 md:px-6 overflow-x-auto scrollbar-hide">
          <TabsList className="bg-transparent border-b-0 h-auto p-0 flex whitespace-nowrap space-x-1 py-1">
            {availableComponents.map((component) => {
              const Icon = component.icon;
              return (
                <TabsTrigger
                  key={component.id}
                  value={component.id}
                  className="flex items-center space-x-2 px-6 py-3 rounded-t-xl border-b-2 border-transparent data-[state=active]:border-indigo-500 data-[state=active]:bg-indigo-50 dark:data-[state=active]:bg-indigo-900/20 data-[state=active]:text-indigo-600 dark:data-[state=active]:text-indigo-400 hover:text-indigo-600 transition-all font-black uppercase text-[10px] tracking-widest"
                >
                  <Icon className="w-4 h-4" />
                  <span>{component.name}</span>
                </TabsTrigger>
              );
            })}
          </TabsList>
        </div>

        {/* Current Component Info - Premium Context Bar */}
        {currentComponent && (
          <div className="bg-slate-100/50 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-700 px-6 py-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-white dark:bg-slate-900 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700">
                  <currentComponent.icon className="w-4 h-4 md:w-5 md:h-5 text-indigo-600 shrink-0" />
                </div>
                <div className="min-w-0">
                  <h2 className="font-black text-xs md:text-sm text-slate-900 dark:text-white uppercase tracking-wider">{currentComponent.name}</h2>
                  <p className="text-[10px] md:text-xs text-slate-500 dark:text-slate-400 truncate font-medium">{currentComponent.description}</p>
                </div>
              </div>

              {/* Agent selector for agent-specific components */}
              {currentComponent.requiresAgentId && (
                <div className="flex items-center space-x-2">
                  <span className="text-[10px] uppercase font-bold text-slate-400">Viewing:</span>
                  <select
                    value={selectedAgentId}
                    onChange={(e) => setSelectedAgentId(e.target.value)}
                    className="px-3 py-1.5 border border-slate-200 dark:border-slate-700 rounded-xl bg-white dark:bg-slate-900 text-slate-900 dark:text-white text-[10px] md:text-xs font-bold outline-none focus:ring-2 focus:ring-indigo-500 transition-all shadow-sm"
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
        <div className="p-2 md:p-6 flex-1 overflow-x-hidden">
          {availableComponents.map((component) => (
            <TabsContent key={component.id} value={component.id} className="mt-0 h-full">
              {activeComponent === component.id && renderComponent()}
            </TabsContent>
          ))}
        </div>
      </Tabs>

      {/* Footer */}
      <div className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between text-sm text-gray-500">
          <div className="flex flex-col md:flex-row items-center gap-2 md:space-x-4">
            <span className="text-[10px] md:text-xs">Agent Mesh v2.1.0</span>
            <span className="hidden md:inline">•</span>
            <Badge variant="outline" className="bg-green-100 text-green-800 text-[9px] border-0">
              System Healthy
            </Badge>
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
  AgentDashboard,
};
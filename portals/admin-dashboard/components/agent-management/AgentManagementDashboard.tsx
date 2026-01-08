'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Activity,
  Bot,
  Brain,
  BarChart3,
  Settings,
  Play,
  Pause,
  Square,
  MoreVertical,
  Users,
  Target,
  Zap,
  ShieldCheck,
  AlertCircle,
  CheckCircle,
  Clock,
  TrendingUp,
  Database,
  Cpu,
  Layers,
  Network,
  Eye,
  ChevronDown,
  ChevronRight,
  Filter,
  Search,
  RefreshCw
} from 'lucide-react';
import { Input } from "@/components/ui/input";

// Agent Status Types
type AgentStatus = 'active' | 'idle' | 'error' | 'maintenance' | 'disabled';

// Agent Priority Types
type AgentPriority = 'high' | 'medium' | 'low';

// Agent Hierarchy Interface
interface Agent {
  id: string;
  name: string;
  role: string;
  service: string;
  port?: number;
  status: AgentStatus;
  priority: AgentPriority;
  performance: {
    successRate: number;
    averageResponseTime: number;
    tasksCompleted: number;
    errors: number;
  };
  resources: {
    cpuUsage: number;
    memoryUsage: number;
    diskUsage: number;
  };
  lastActivity: Date;
  subordinates?: Agent[];
  capabilities?: string[];
  tools?: string[];
}

// Domain Supervisor Structure
interface DomainSupervisor {
  id: string;
  name: string;
  domain: string;
  status: AgentStatus;
  specialistAgents: Agent[];
  performance: {
    overallHealth: number;
    activeAgents: number;
    totalTasks: number;
    successRate: number;
  };
}

// Mock data based on the consolidated workflow tracker
const mockAgentHierarchy: {
  ceoAgent: Agent;
  domainSupervisors: DomainSupervisor[];
} = {
  ceoAgent: {
    id: 'ceo-orchestrator',
    name: 'CEO Orchestrator',
    role: 'Chief Executive Orchestrator',
    service: 'bizosaas-agent-orchestration',
    port: 30320,
    status: 'active',
    priority: 'high',
    performance: {
      successRate: 98.5,
      averageResponseTime: 150,
      tasksCompleted: 1247,
      errors: 3
    },
    resources: {
      cpuUsage: 65,
      memoryUsage: 78,
      diskUsage: 45
    },
    lastActivity: new Date(),
    capabilities: ['Global strategy coordination', 'Resource allocation', 'Quality assurance'],
    tools: ['system_monitor', 'resource_allocator', 'quality_assessor']
  },
  domainSupervisors: [
    {
      id: 'crm-supervisor',
      name: 'CRM Domain Supervisor',
      domain: 'Customer Relationship Management',
      status: 'active',
      performance: {
        overallHealth: 100,
        activeAgents: 6,
        totalTasks: 3245,
        successRate: 94.2
      },
      specialistAgents: [
        {
          id: 'lead-scoring-agent',
          name: 'Lead Scoring Agent',
          role: 'AI-powered lead qualification and scoring',
          service: 'bizosaas-crm-ai',
          status: 'active',
          priority: 'high',
          performance: {
            successRate: 96.8,
            averageResponseTime: 89,
            tasksCompleted: 2847,
            errors: 12
          },
          resources: {
            cpuUsage: 45,
            memoryUsage: 62,
            diskUsage: 23
          },
          lastActivity: new Date(),
          capabilities: ['Lead qualification', 'Scoring algorithms', 'Behavioral analysis']
        },
        {
          id: 'lead-assignment-agent',
          name: 'Lead Assignment Agent',
          role: 'Intelligent distribution based on skills/territory',
          service: 'bizosaas-crm-ai',
          status: 'active',
          priority: 'high',
          performance: {
            successRate: 98.2,
            averageResponseTime: 67,
            tasksCompleted: 1924,
            errors: 5
          },
          resources: {
            cpuUsage: 32,
            memoryUsage: 45,
            diskUsage: 18
          },
          lastActivity: new Date(),
          capabilities: ['Territory mapping', 'Skills matching', 'Load balancing']
        }
      ]
    },
    {
      id: 'ecommerce-supervisor',
      name: 'E-commerce Domain Supervisor',
      domain: 'E-commerce & Product Management',
      status: 'active',
      performance: {
        overallHealth: 75,
        activeAgents: 3,
        totalTasks: 1876,
        successRate: 89.4
      },
      specialistAgents: [
        {
          id: 'product-recommendation-agent',
          name: 'Product Recommendation Agent',
          role: 'AI-powered product suggestions',
          service: 'bizosaas-ecommerce-ai',
          status: 'active',
          priority: 'high',
          performance: {
            successRate: 92.3,
            averageResponseTime: 156,
            tasksCompleted: 5642,
            errors: 28
          },
          resources: {
            cpuUsage: 58,
            memoryUsage: 71,
            diskUsage: 34
          },
          lastActivity: new Date(),
          capabilities: ['Collaborative filtering', 'Content-based recommendations', 'Real-time personalization']
        },
        {
          id: 'inventory-optimization-agent',
          name: 'Inventory Optimization Agent',
          role: 'Stock level prediction and management',
          service: 'bizosaas-ecommerce-ai',
          status: 'maintenance',
          priority: 'medium',
          performance: {
            successRate: 85.7,
            averageResponseTime: 234,
            tasksCompleted: 987,
            errors: 45
          },
          resources: {
            cpuUsage: 0,
            memoryUsage: 0,
            diskUsage: 28
          },
          lastActivity: new Date(Date.now() - 3600000), // 1 hour ago
          capabilities: ['Demand forecasting', 'Stock optimization', 'Supply chain analysis']
        }
      ]
    },
    {
      id: 'analytics-supervisor',
      name: 'Analytics Domain Supervisor',
      domain: 'Analytics & Performance Intelligence',
      status: 'active',
      performance: {
        overallHealth: 91,
        activeAgents: 5,
        totalTasks: 8934,
        successRate: 96.1
      },
      specialistAgents: [
        {
          id: 'data-collection-agent',
          name: 'Data Collection Agent',
          role: 'Automated data gathering from multiple sources',
          service: 'bizosaas-analytics-ai',
          port: 30308,
          status: 'active',
          priority: 'high',
          performance: {
            successRate: 99.1,
            averageResponseTime: 45,
            tasksCompleted: 15678,
            errors: 8
          },
          resources: {
            cpuUsage: 72,
            memoryUsage: 84,
            diskUsage: 67
          },
          lastActivity: new Date(),
          capabilities: ['Multi-source integration', 'Real-time collection', 'Data validation']
        },
        {
          id: 'report-generation-agent',
          name: 'Report Generation Agent',
          role: 'Dynamic report creation and scheduling',
          service: 'bizosaas-analytics-ai',
          status: 'active',
          priority: 'medium',
          performance: {
            successRate: 94.8,
            averageResponseTime: 2340,
            tasksCompleted: 847,
            errors: 23
          },
          resources: {
            cpuUsage: 41,
            memoryUsage: 56,
            diskUsage: 42
          },
          lastActivity: new Date(),
          capabilities: ['Automated reporting', 'Custom templates', 'Scheduled delivery']
        }
      ]
    },
    {
      id: 'billing-supervisor',
      name: 'Billing Domain Supervisor',
      domain: 'Payment & Financial Management',
      status: 'active',
      performance: {
        overallHealth: 100,
        activeAgents: 6,
        totalTasks: 2156,
        successRate: 99.8
      },
      specialistAgents: [
        {
          id: 'payment-processing-agent',
          name: 'Payment Processing Agent',
          role: 'Multi-gateway payment handling',
          service: 'bizosaas-billing-ai',
          status: 'active',
          priority: 'high',
          performance: {
            successRate: 99.9,
            averageResponseTime: 234,
            tasksCompleted: 8923,
            errors: 2
          },
          resources: {
            cpuUsage: 28,
            memoryUsage: 34,
            diskUsage: 15
          },
          lastActivity: new Date(),
          capabilities: ['Multi-gateway support', 'Fraud detection', 'Real-time processing']
        }
      ]
    },
    {
      id: 'cms-supervisor',
      name: 'CMS Domain Supervisor',
      domain: 'Content Management & SEO',
      status: 'active',
      performance: {
        overallHealth: 87,
        activeAgents: 4,
        totalTasks: 4567,
        successRate: 91.5
      },
      specialistAgents: [
        {
          id: 'content-creation-agent',
          name: 'Content Creation Agent',
          role: 'AI-powered content generation',
          service: 'bizosaas-cms-ai',
          status: 'active',
          priority: 'high',
          performance: {
            successRate: 93.4,
            averageResponseTime: 3450,
            tasksCompleted: 1234,
            errors: 67
          },
          resources: {
            cpuUsage: 67,
            memoryUsage: 89,
            diskUsage: 45
          },
          lastActivity: new Date(),
          capabilities: ['Content generation', 'SEO optimization', 'Multi-format support']
        },
        {
          id: 'seo-optimization-agent',
          name: 'SEO Optimization Agent',
          role: 'Search engine optimization automation',
          service: 'bizosaas-cms-ai',
          status: 'active',
          priority: 'high',
          performance: {
            successRate: 89.7,
            averageResponseTime: 1890,
            tasksCompleted: 892,
            errors: 34
          },
          resources: {
            cpuUsage: 52,
            memoryUsage: 67,
            diskUsage: 38
          },
          lastActivity: new Date(),
          capabilities: ['Keyword optimization', 'Meta tag generation', 'Content analysis']
        }
      ]
    },
    {
      id: 'integration-supervisor',
      name: 'Integration Domain Supervisor',
      domain: 'API & System Integration',
      status: 'active',
      performance: {
        overallHealth: 82,
        activeAgents: 3,
        totalTasks: 3456,
        successRate: 88.9
      },
      specialistAgents: [
        {
          id: 'api-gateway-agent',
          name: 'API Gateway Agent',
          role: 'Request routing and rate limiting',
          service: 'bizosaas-integration-ai',
          status: 'active',
          priority: 'high',
          performance: {
            successRate: 97.8,
            averageResponseTime: 67,
            tasksCompleted: 23456,
            errors: 123
          },
          resources: {
            cpuUsage: 78,
            memoryUsage: 65,
            diskUsage: 34
          },
          lastActivity: new Date(),
          capabilities: ['Request routing', 'Rate limiting', 'Authentication']
        },
        {
          id: 'data-sync-agent',
          name: 'Data Synchronization Agent',
          role: 'Real-time data sync across platforms',
          service: 'bizosaas-integration-ai',
          status: 'error',
          priority: 'high',
          performance: {
            successRate: 76.4,
            averageResponseTime: 890,
            tasksCompleted: 2345,
            errors: 234
          },
          resources: {
            cpuUsage: 12,
            memoryUsage: 23,
            diskUsage: 45
          },
          lastActivity: new Date(Date.now() - 1800000), // 30 minutes ago
          capabilities: ['Real-time sync', 'Conflict resolution', 'Data validation']
        }
      ]
    }
  ]
};

const StatusBadge: React.FC<{ status: AgentStatus }> = ({ status }) => {
  const statusConfig = {
    active: { color: 'bg-green-500', text: 'Active', icon: CheckCircle },
    idle: { color: 'bg-yellow-500', text: 'Idle', icon: Clock },
    error: { color: 'bg-red-500', text: 'Error', icon: AlertCircle },
    maintenance: { color: 'bg-blue-500', text: 'Maintenance', icon: Settings },
    disabled: { color: 'bg-gray-500', text: 'Disabled', icon: Square }
  };

  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <Badge variant="outline" className={`${config.color} text-white border-0`}>
      <Icon className="w-3 h-3 mr-1" />
      {config.text}
    </Badge>
  );
};

const PriorityBadge: React.FC<{ priority: AgentPriority }> = ({ priority }) => {
  const priorityConfig = {
    high: { color: 'bg-red-100 text-red-800', text: 'High' },
    medium: { color: 'bg-yellow-100 text-yellow-800', text: 'Medium' },
    low: { color: 'bg-green-100 text-green-800', text: 'Low' }
  };

  return (
    <Badge variant="outline" className={priorityConfig[priority].color}>
      {priorityConfig[priority].text}
    </Badge>
  );
};

const AgentCard: React.FC<{ agent: Agent; onManage: (agent: Agent) => void }> = ({ agent, onManage }) => {
  return (
    <Card className="hover:shadow-lg transition-shadow bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bot className="w-5 h-5 text-indigo-600" />
            <CardTitle className="text-sm font-bold uppercase tracking-tight">{agent.name}</CardTitle>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm">
                <MoreVertical className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={() => onManage(agent)}>
                <Settings className="w-4 h-4 mr-2" />
                Configure
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Eye className="w-4 h-4 mr-2" />
                View Details
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Activity className="w-4 h-4 mr-2" />
                View Logs
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
        <CardDescription className="text-[10px] uppercase font-bold text-slate-400">{agent.role}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex items-center justify-between">
          <StatusBadge status={agent.status} />
          <PriorityBadge priority={agent.priority} />
        </div>

        <div className="grid grid-cols-2 gap-2 text-[10px] uppercase font-bold text-slate-500">
          <div>
            <p className="text-gray-400">Success</p>
            <p className="text-sm text-slate-900 dark:text-white font-black">{agent.performance.successRate}%</p>
          </div>
          <div>
            <p className="text-gray-400">Latency</p>
            <p className="text-sm text-slate-900 dark:text-white font-black">{agent.performance.averageResponseTime}ms</p>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex justify-between text-[10px] uppercase font-bold">
            <span className="text-slate-500">CPU</span>
            <span className="text-indigo-600">{agent.resources.cpuUsage}%</span>
          </div>
          <Progress value={agent.resources.cpuUsage} className="h-1 bg-slate-100 dark:bg-slate-800" />

          <div className="flex justify-between text-[10px] uppercase font-bold">
            <span className="text-slate-500">RAM</span>
            <span className="text-emerald-600">{agent.resources.memoryUsage}%</span>
          </div>
          <Progress value={agent.resources.memoryUsage} className="h-1 bg-slate-100 dark:bg-slate-800" />
        </div>
      </CardContent>
    </Card>
  );
};

const DomainCard: React.FC<{
  supervisor: DomainSupervisor;
  expanded: boolean;
  onToggle: () => void;
  onManageAgent: (agent: Agent) => void;
}> = ({ supervisor, expanded, onToggle, onManageAgent }) => {
  return (
    <Card className="border-none shadow-sm bg-white dark:bg-slate-900 overflow-hidden border-l-4 border-l-indigo-500">
      <CardHeader className="cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors" onClick={onToggle}>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-2 bg-indigo-50 dark:bg-indigo-900/20 rounded-xl">
              <Brain className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <CardTitle className="text-lg font-black uppercase italic tracking-tighter text-slate-900 dark:text-white">
                {supervisor.name}
              </CardTitle>
              <CardDescription className="text-xs font-medium text-slate-500 uppercase tracking-widest">
                {supervisor.domain}
              </CardDescription>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <StatusBadge status={supervisor.status} />
            {expanded ? <ChevronDown className="w-5 h-5 text-slate-400" /> : <ChevronRight className="w-5 h-5 text-slate-400" />}
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <div className="bg-slate-50 dark:bg-slate-800/10 p-3 rounded-2xl border border-slate-100 dark:border-slate-800">
            <p className="text-xl md:text-2xl font-black text-emerald-600 tracking-tighter italic">{supervisor.performance.overallHealth}%</p>
            <p className="text-[10px] uppercase font-black text-slate-400 tracking-widest mt-1">Health</p>
          </div>
          <div className="bg-slate-50 dark:bg-slate-800/10 p-3 rounded-2xl border border-slate-100 dark:border-slate-800">
            <p className="text-xl md:text-2xl font-black text-indigo-600 tracking-tighter italic">{supervisor.performance.activeAgents}</p>
            <p className="text-[10px] uppercase font-black text-slate-400 tracking-widest mt-1">Live</p>
          </div>
          <div className="bg-slate-50 dark:bg-slate-800/10 p-3 rounded-2xl border border-slate-100 dark:border-slate-800">
            <p className="text-xl md:text-2xl font-black text-blue-600 tracking-tighter italic">{supervisor.performance.totalTasks}</p>
            <p className="text-[10px] uppercase font-black text-slate-400 tracking-widest mt-1">Tasks</p>
          </div>
          <div className="bg-slate-50 dark:bg-slate-800/10 p-3 rounded-2xl border border-slate-100 dark:border-slate-800">
            <p className="text-xl md:text-2xl font-black text-amber-600 tracking-tighter italic">{supervisor.performance.successRate}%</p>
            <p className="text-[10px] uppercase font-black text-slate-400 tracking-widest mt-1">ROI</p>
          </div>
        </div>

        {expanded && (
          <div className="mt-8 animate-in slide-in-from-top-4 duration-500">
            <div className="flex items-center justify-between mb-6">
              <h4 className="text-xs font-black uppercase tracking-[0.2em] text-slate-500 flex items-center">
                <Users className="w-4 h-4 mr-2" />
                Specialist Agent Mesh ({supervisor.specialistAgents.length})
              </h4>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {supervisor.specialistAgents.map((agent) => (
                <AgentCard key={agent.id} agent={agent} onManage={onManageAgent} />
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default function AgentManagementDashboard() {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<AgentStatus | 'all'>('all');
  const [expandedDomains, setExpandedDomains] = useState<Set<string>>(new Set());
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [agentData, setAgentData] = useState(mockAgentHierarchy);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setLastUpdate(new Date());
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const toggleDomain = (domainId: string) => {
    const newExpanded = new Set(expandedDomains);
    if (newExpanded.has(domainId)) {
      newExpanded.delete(domainId);
    } else {
      newExpanded.add(domainId);
    }
    setExpandedDomains(newExpanded);
  };

  const handleManageAgent = (agent: Agent) => {
    setSelectedAgent(agent);
  };

  const filteredSupervisors = agentData.domainSupervisors.filter(supervisor => {
    if (statusFilter !== 'all' && supervisor.status !== statusFilter) return false;
    if (searchTerm && !supervisor.name.toLowerCase().includes(searchTerm.toLowerCase())) return false;
    return true;
  });

  const totalAgents = agentData.domainSupervisors.reduce((sum, supervisor) => sum + supervisor.specialistAgents.length, 0) + 1;
  const activeAgents = agentData.domainSupervisors.reduce((sum, supervisor) =>
    sum + supervisor.specialistAgents.filter(agent => agent.status === 'active').length, 0
  ) + (agentData.ceoAgent.status === 'active' ? 1 : 0);
  const errorAgents = agentData.domainSupervisors.reduce((sum, supervisor) =>
    sum + supervisor.specialistAgents.filter(agent => agent.status === 'error').length, 0
  );
  const averageSuccessRate = agentData.domainSupervisors.reduce((sum, supervisor) => sum + supervisor.performance.successRate, 0) / agentData.domainSupervisors.length;

  return (
    <div className="space-y-4 md:space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700 pb-20 lg:pb-10">
      {/* Overview Stats - Premium Minimal Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="shadow-sm border-none bg-indigo-50/50 dark:bg-indigo-900/10 border-l-4 border-l-indigo-500">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[10px] uppercase font-black text-indigo-600 tracking-widest">Total Agents</p>
                <p className="text-xl md:text-3xl font-black text-slate-900 dark:text-white mt-1">{totalAgents}</p>
              </div>
              <div className="p-2 bg-white dark:bg-slate-800 rounded-xl shadow-sm">
                <Bot className="w-5 h-5 md:w-6 md:h-6 text-indigo-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-sm border-none bg-emerald-50/50 dark:bg-emerald-900/10 border-l-4 border-l-emerald-500">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[10px] uppercase font-black text-emerald-600 tracking-widest">Active Mesh</p>
                <p className="text-xl md:text-3xl font-black text-slate-900 dark:text-white mt-1">{activeAgents}</p>
              </div>
              <div className="p-2 bg-white dark:bg-slate-800 rounded-xl shadow-sm">
                <Activity className="w-5 h-5 md:w-6 md:h-6 text-emerald-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-sm border-none bg-red-50/50 dark:bg-red-900/10 border-l-4 border-l-red-500">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[10px] uppercase font-black text-red-600 tracking-widest">System Errors</p>
                <p className="text-xl md:text-3xl font-black text-slate-900 dark:text-white mt-1">{errorAgents}</p>
              </div>
              <div className="p-2 bg-white dark:bg-slate-800 rounded-xl shadow-sm">
                <AlertCircle className="w-5 h-5 md:w-6 md:h-6 text-red-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-sm border-none bg-amber-50/50 dark:bg-amber-900/10 border-l-4 border-l-amber-500">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-[10px] uppercase font-black text-amber-600 tracking-widest">Global Success</p>
                <p className="text-xl md:text-3xl font-black text-slate-900 dark:text-white mt-1">{averageSuccessRate.toFixed(1)}%</p>
              </div>
              <div className="p-2 bg-white dark:bg-slate-800 rounded-xl shadow-sm">
                <TrendingUp className="w-5 h-5 md:w-6 md:h-6 text-amber-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters and Search */}
      <div className="flex items-center space-x-4">
        <div className="flex-1">
          <Input
            placeholder="Search agents or domains..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="max-w-sm bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800"
          />
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="border-slate-200 dark:border-slate-800">
              <Filter className="w-4 h-4 mr-2" />
              Status: {statusFilter === 'all' ? 'All' : statusFilter}
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="dark:bg-slate-900 border-slate-200 dark:border-slate-800">
            <DropdownMenuItem onClick={() => setStatusFilter('all')}>All</DropdownMenuItem>
            <DropdownMenuItem onClick={() => setStatusFilter('active')}>Active</DropdownMenuItem>
            <DropdownMenuItem onClick={() => setStatusFilter('idle')}>Idle</DropdownMenuItem>
            <DropdownMenuItem onClick={() => setStatusFilter('error')}>Error</DropdownMenuItem>
            <DropdownMenuItem onClick={() => setStatusFilter('maintenance')}>Maintenance</DropdownMenuItem>
            <DropdownMenuItem onClick={() => setStatusFilter('disabled')}>Disabled</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      {/* CEO Agent - Premium Centerpiece */}
      <Card className="border-none bg-slate-950 text-white overflow-hidden relative group shadow-2xl">
        <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:scale-110 transition-transform duration-700">
          <Target className="w-32 h-32" />
        </div>
        <CardHeader className="relative z-10">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-indigo-600 rounded-2xl shadow-xl shadow-indigo-500/20">
                <Target className="w-8 h-8 text-white" />
              </div>
              <div>
                <CardTitle className="text-2xl font-black uppercase italic tracking-tighter">Master Business <span className="text-indigo-400">Supervisor</span></CardTitle>
                <CardDescription className="text-slate-400 font-bold uppercase text-[10px] tracking-widest mt-1">{agentData.ceoAgent.role}</CardDescription>
              </div>
            </div>
            <Badge className="bg-emerald-500 text-white font-black italic px-4 py-1">ACTIVE SYSTEM</Badge>
          </div>
        </CardHeader>
        <CardContent className="relative z-10">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm">
              <p className="text-3xl md:text-4xl font-black text-indigo-400 tracking-tighter italic">{agentData.ceoAgent.performance.successRate}%</p>
              <p className="text-[10px] uppercase font-black text-slate-500 tracking-[0.2em] mt-2">Core Success</p>
            </div>
            <div className="text-center p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm">
              <p className="text-3xl md:text-4xl font-black text-blue-400 tracking-tighter italic">{agentData.ceoAgent.performance.tasksCompleted}</p>
              <p className="text-[10px] uppercase font-black text-slate-500 tracking-[0.2em] mt-2">Executions</p>
            </div>
            <div className="text-center p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm">
              <p className="text-3xl md:text-4xl font-black text-amber-400 tracking-tighter italic">{agentData.ceoAgent.performance.averageResponseTime}ms</p>
              <p className="text-[10px] uppercase font-black text-slate-500 tracking-[0.2em] mt-2">System Latency</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Domain Supervisors */}
      <div className="space-y-6">
        <h2 className="text-2xl font-black text-slate-900 dark:text-white uppercase italic tracking-tighter flex items-center">
          <Brain className="w-6 h-6 mr-3 text-indigo-600" />
          Domain <span className="text-indigo-600 ml-2">Supervisors</span>
          <span className="ml-4 text-xs font-bold text-slate-400 normal-case tracking-normal">({agentData.domainSupervisors.length} Nodes)</span>
        </h2>

        <div className="grid grid-cols-1 gap-6">
          {filteredSupervisors.map((supervisor) => (
            <DomainCard
              key={supervisor.id}
              supervisor={supervisor}
              expanded={expandedDomains.has(supervisor.id)}
              onToggle={() => toggleDomain(supervisor.id)}
              onManageAgent={handleManageAgent}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
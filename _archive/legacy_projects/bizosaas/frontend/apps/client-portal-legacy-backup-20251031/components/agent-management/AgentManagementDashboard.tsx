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
  Memory,
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
        },
        // Add more CRM agents...
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

// Status badge component
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

// Priority badge component
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

// Agent card component
const AgentCard: React.FC<{ agent: Agent; onManage: (agent: Agent) => void }> = ({ agent, onManage }) => {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bot className="w-5 h-5 text-blue-600" />
            <CardTitle className="text-sm font-medium">{agent.name}</CardTitle>
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
        <CardDescription className="text-xs">{agent.role}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex items-center justify-between">
          <StatusBadge status={agent.status} />
          <PriorityBadge priority={agent.priority} />
        </div>
        
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div>
            <p className="text-gray-500">Success Rate</p>
            <p className="font-medium">{agent.performance.successRate}%</p>
          </div>
          <div>
            <p className="text-gray-500">Avg. Response</p>
            <p className="font-medium">{agent.performance.averageResponseTime}ms</p>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex justify-between text-xs">
            <span>CPU</span>
            <span>{agent.resources.cpuUsage}%</span>
          </div>
          <Progress value={agent.resources.cpuUsage} className="h-1" />
          
          <div className="flex justify-between text-xs">
            <span>Memory</span>
            <span>{agent.resources.memoryUsage}%</span>
          </div>
          <Progress value={agent.resources.memoryUsage} className="h-1" />
        </div>

        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Tasks: {agent.performance.tasksCompleted}</span>
          <span>Errors: {agent.performance.errors}</span>
        </div>
      </CardContent>
    </Card>
  );
};

// Domain supervisor card component
const DomainCard: React.FC<{ 
  supervisor: DomainSupervisor; 
  expanded: boolean;
  onToggle: () => void;
  onManageAgent: (agent: Agent) => void;
}> = ({ supervisor, expanded, onToggle, onManageAgent }) => {
  return (
    <Card className="border-l-4 border-blue-500">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Button variant="ghost" size="sm" onClick={onToggle}>
              {expanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
            </Button>
            <Brain className="w-6 h-6 text-blue-600" />
            <div>
              <CardTitle className="text-lg">{supervisor.name}</CardTitle>
              <CardDescription>{supervisor.domain}</CardDescription>
            </div>
          </div>
          <StatusBadge status={supervisor.status} />
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="grid grid-cols-4 gap-4 mb-4">
          <div className="text-center">
            <p className="text-2xl font-bold text-green-600">{supervisor.performance.overallHealth}%</p>
            <p className="text-xs text-gray-500">Health</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-blue-600">{supervisor.performance.activeAgents}</p>
            <p className="text-xs text-gray-500">Active Agents</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-purple-600">{supervisor.performance.totalTasks}</p>
            <p className="text-xs text-gray-500">Total Tasks</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-orange-600">{supervisor.performance.successRate}%</p>
            <p className="text-xs text-gray-500">Success Rate</p>
          </div>
        </div>

        {expanded && (
          <div className="mt-4">
            <h4 className="font-medium mb-3 flex items-center">
              <Users className="w-4 h-4 mr-2" />
              Specialist Agents ({supervisor.specialistAgents.length})
            </h4>
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

// Main dashboard component
export default function AgentManagementDashboard() {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<AgentStatus | 'all'>('all');
  const [expandedDomains, setExpandedDomains] = useState<Set<string>>(new Set());
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [agentData, setAgentData] = useState(mockAgentHierarchy);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // Mock real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setLastUpdate(new Date());
      // Here you would fetch real data from your API
    }, 30000); // Update every 30 seconds

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

  // Calculate overall statistics
  const totalAgents = agentData.domainSupervisors.reduce((sum, supervisor) => sum + supervisor.specialistAgents.length, 0) + 1; // +1 for CEO
  const activeAgents = agentData.domainSupervisors.reduce((sum, supervisor) => 
    sum + supervisor.specialistAgents.filter(agent => agent.status === 'active').length, 0
  ) + (agentData.ceoAgent.status === 'active' ? 1 : 0);
  const errorAgents = agentData.domainSupervisors.reduce((sum, supervisor) => 
    sum + supervisor.specialistAgents.filter(agent => agent.status === 'error').length, 0
  );
  const averageSuccessRate = agentData.domainSupervisors.reduce((sum, supervisor) => sum + supervisor.performance.successRate, 0) / agentData.domainSupervisors.length;

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Agent Management Dashboard</h1>
          <p className="text-gray-600">Monitor and manage your 88-agent BizOSaaS ecosystem</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={() => setLastUpdate(new Date())}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
          <span className="text-xs text-gray-500">
            Last updated: {lastUpdate.toLocaleTimeString()}
          </span>
        </div>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Agents</p>
                <p className="text-2xl font-bold">{totalAgents}</p>
              </div>
              <Bot className="w-8 h-8 text-blue-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Active Agents</p>
                <p className="text-2xl font-bold text-green-600">{activeAgents}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Error Agents</p>
                <p className="text-2xl font-bold text-red-600">{errorAgents}</p>
              </div>
              <AlertCircle className="w-8 h-8 text-red-600" />
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Avg Success Rate</p>
                <p className="text-2xl font-bold text-purple-600">{averageSuccessRate.toFixed(1)}%</p>
              </div>
              <TrendingUp className="w-8 h-8 text-purple-600" />
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
            className="max-w-sm"
          />
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline">
              <Filter className="w-4 h-4 mr-2" />
              Status: {statusFilter === 'all' ? 'All' : statusFilter}
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent>
            <DropdownMenuItem onClick={() => setStatusFilter('all')}>All</DropdownMenuItem>
            <DropdownMenuItem onClick={() => setStatusFilter('active')}>Active</DropdownMenuItem>
            <DropdownMenuItem onClick={() => setStatusFilter('idle')}>Idle</DropdownMenuItem>
            <DropdownMenuItem onClick={() => setStatusFilter('error')}>Error</DropdownMenuItem>
            <DropdownMenuItem onClick={() => setStatusFilter('maintenance')}>Maintenance</DropdownMenuItem>
            <DropdownMenuItem onClick={() => setStatusFilter('disabled')}>Disabled</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      {/* CEO Agent */}
      <Card className="border-l-4 border-purple-500">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Target className="w-8 h-8 text-purple-600" />
              <div>
                <CardTitle className="text-xl">Master Business Supervisor</CardTitle>
                <CardDescription>{agentData.ceoAgent.role}</CardDescription>
              </div>
            </div>
            <StatusBadge status={agentData.ceoAgent.status} />
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-purple-600">{agentData.ceoAgent.performance.successRate}%</p>
              <p className="text-xs text-gray-500">Success Rate</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{agentData.ceoAgent.performance.tasksCompleted}</p>
              <p className="text-xs text-gray-500">Tasks Completed</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-orange-600">{agentData.ceoAgent.performance.averageResponseTime}ms</p>
              <p className="text-xs text-gray-500">Avg Response Time</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Domain Supervisors */}
      <div className="space-y-4">
        <h2 className="text-2xl font-bold flex items-center">
          <Brain className="w-6 h-6 mr-2" />
          Domain Supervisors ({agentData.domainSupervisors.length})
        </h2>
        
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
  );
}
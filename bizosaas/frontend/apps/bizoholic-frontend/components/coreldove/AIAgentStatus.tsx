"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Bot, Brain, Zap, RefreshCw, CheckCircle, AlertCircle, Clock,
  TrendingUp, Target, Package, ShoppingCart, BarChart3, Activity,
  Sparkles, Eye, DollarSign, Users
} from 'lucide-react';

interface AIAgent {
  id: string;
  name: string;
  type: 'classification' | 'pricing' | 'sourcing' | 'marketing' | 'analytics' | 'fraud_detection';
  status: 'idle' | 'running' | 'completed' | 'error' | 'paused';
  progress: number;
  current_task: string;
  last_run: string;
  next_scheduled?: string;
  performance: {
    success_rate: number;
    avg_processing_time: number;
    total_processed: number;
    today_processed: number;
  };
  capabilities: string[];
  recent_results: Array<{
    timestamp: string;
    action: string;
    result: string;
    impact?: string;
  }>;
}

interface AIAgentStatusProps {
  onAgentAction?: (agentId: string, action: string) => void;
  className?: string;
}

export function AIAgentStatus({ onAgentAction, className = '' }: AIAgentStatusProps) {
  const [agents, setAgents] = useState<AIAgent[]>([]);
  const [loading, setLoading] = useState(true);
  const [systemHealth, setSystemHealth] = useState({
    overall_status: 'healthy' as 'healthy' | 'degraded' | 'down',
    active_agents: 0,
    processing_queue: 0,
    avg_response_time: 0,
    uptime: '99.8%'
  });

  // Mock data - Replace with actual API calls
  useEffect(() => {
    const mockAgents: AIAgent[] = [
      {
        id: 'classification-crew',
        name: 'Product Classification Crew',
        type: 'classification',
        status: 'running',
        progress: 65,
        current_task: 'Analyzing 24 new products from supplier catalog',
        last_run: '2025-01-05T15:30:00Z',
        next_scheduled: '2025-01-05T18:00:00Z',
        performance: {
          success_rate: 94.5,
          avg_processing_time: 45,
          total_processed: 1247,
          today_processed: 24
        },
        capabilities: [
          'Product categorization',
          'Profit potential scoring',
          'Market demand analysis',
          'Competition assessment'
        ],
        recent_results: [
          {
            timestamp: '2025-01-05T15:25:00Z',
            action: 'Classified product B08N5WRWNW',
            result: 'HERO classification with 92 dropship score',
            impact: 'High profit potential identified'
          },
          {
            timestamp: '2025-01-05T15:20:00Z',
            action: 'Market analysis completed',
            result: 'Fitness category showing 28% growth',
            impact: 'Recommend inventory increase'
          }
        ]
      },
      {
        id: 'pricing-optimizer',
        name: 'Dynamic Pricing Optimizer',
        type: 'pricing',
        status: 'idle',
        progress: 0,
        current_task: 'Ready for pricing analysis',
        last_run: '2025-01-05T12:15:00Z',
        performance: {
          success_rate: 96.8,
          avg_processing_time: 28,
          total_processed: 892,
          today_processed: 15
        },
        capabilities: [
          'Competitive price analysis',
          'Demand elasticity calculation',
          'Profit margin optimization',
          'Market positioning'
        ],
        recent_results: [
          {
            timestamp: '2025-01-05T12:10:00Z',
            action: 'Optimized pricing for FIT-001',
            result: 'Recommended price increase to $84.99',
            impact: '$1,200 additional monthly revenue'
          }
        ]
      },
      {
        id: 'sourcing-scout',
        name: 'Product Sourcing Scout',
        type: 'sourcing',
        status: 'completed',
        progress: 100,
        current_task: 'Sourcing analysis completed',
        last_run: '2025-01-05T14:45:00Z',
        performance: {
          success_rate: 88.2,
          avg_processing_time: 120,
          total_processed: 456,
          today_processed: 8
        },
        capabilities: [
          'Amazon product discovery',
          'Supplier verification',
          'Market trend identification',
          'Profit potential calculation'
        ],
        recent_results: [
          {
            timestamp: '2025-01-05T14:40:00Z',
            action: 'Discovered 8 high-potential products',
            result: '3 HERO, 4 GOOD, 1 MODERATE classifications',
            impact: 'Est. $15K monthly revenue potential'
          }
        ]
      },
      {
        id: 'fraud-detector',
        name: 'Fraud Detection Engine',
        type: 'fraud_detection',
        status: 'running',
        progress: 30,
        current_task: 'Analyzing order risk patterns',
        last_run: '2025-01-05T15:35:00Z',
        performance: {
          success_rate: 98.9,
          avg_processing_time: 12,
          total_processed: 2341,
          today_processed: 67
        },
        capabilities: [
          'Real-time fraud scoring',
          'Pattern recognition',
          'Risk assessment',
          'Automated flagging'
        ],
        recent_results: [
          {
            timestamp: '2025-01-05T15:30:00Z',
            action: 'Flagged high-risk order ORD-20250105-0003',
            result: 'Risk score: 85% - Manual review required',
            impact: 'Potential fraud prevention'
          }
        ]
      },
      {
        id: 'marketing-strategist',
        name: 'Marketing Strategy Agent',
        type: 'marketing',
        status: 'idle',
        progress: 0,
        current_task: 'Ready for campaign analysis',
        last_run: '2025-01-05T11:20:00Z',
        performance: {
          success_rate: 91.3,
          avg_processing_time: 85,
          total_processed: 234,
          today_processed: 3
        },
        capabilities: [
          'Campaign optimization',
          'Audience targeting',
          'Content strategy',
          'ROI prediction'
        ],
        recent_results: [
          {
            timestamp: '2025-01-05T11:15:00Z',
            action: 'Generated marketing strategy for fitness category',
            result: 'Recommended 3 campaigns with 280% ROI',
            impact: 'Est. $8.5K additional revenue'
          }
        ]
      }
    ];

    setAgents(mockAgents);
    setSystemHealth({
      overall_status: 'healthy',
      active_agents: mockAgents.filter(a => a.status === 'running').length,
      processing_queue: 15,
      avg_response_time: 245,
      uptime: '99.8%'
    });
    setLoading(false);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'completed': return 'bg-green-100 text-green-800 border-green-200';
      case 'error': return 'bg-red-100 text-red-800 border-red-200';
      case 'paused': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return <RefreshCw className="w-4 h-4 animate-spin text-blue-500" />;
      case 'completed': return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'error': return <AlertCircle className="w-4 h-4 text-red-500" />;
      case 'paused': return <Clock className="w-4 h-4 text-yellow-500" />;
      default: return <Bot className="w-4 h-4 text-gray-500" />;
    }
  };

  const getAgentIcon = (type: string) => {
    switch (type) {
      case 'classification': return <Sparkles className="w-5 h-5 text-purple-500" />;
      case 'pricing': return <DollarSign className="w-5 h-5 text-green-500" />;
      case 'sourcing': return <Package className="w-5 h-5 text-blue-500" />;
      case 'marketing': return <Target className="w-5 h-5 text-orange-500" />;
      case 'analytics': return <BarChart3 className="w-5 h-5 text-indigo-500" />;
      case 'fraud_detection': return <Eye className="w-5 h-5 text-red-500" />;
      default: return <Brain className="w-5 h-5 text-gray-500" />;
    }
  };

  const handleAgentAction = async (agentId: string, action: string) => {
    // Update agent status optimistically
    setAgents(prev => prev.map(agent => 
      agent.id === agentId 
        ? { ...agent, status: 'running', progress: 10, current_task: 'Starting...' }
        : agent
    ));

    // Call parent callback
    onAgentAction?.(agentId, action);

    // Simulate progress updates
    const progressSteps = [25, 50, 75, 100];
    for (const progress of progressSteps) {
      await new Promise(resolve => setTimeout(resolve, 2000));
      setAgents(prev => prev.map(agent => 
        agent.id === agentId 
          ? { 
              ...agent, 
              progress,
              current_task: progress === 100 ? 'Completed successfully' : `Processing... ${progress}%`
            }
          : agent
      ));
    }

    // Mark as completed
    setAgents(prev => prev.map(agent => 
      agent.id === agentId 
        ? { ...agent, status: 'completed', last_run: new Date().toISOString() }
        : agent
    ));
  };

  if (loading) {
    return (
      <div className={`space-y-6 ${className}`}>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-64 bg-gray-200 rounded-lg animate-pulse" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* System Health Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-green-500" />
            AI System Health
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <div className="text-center">
              <div className={`text-2xl font-bold ${
                systemHealth.overall_status === 'healthy' ? 'text-green-600' :
                systemHealth.overall_status === 'degraded' ? 'text-yellow-600' :
                'text-red-600'
              }`}>
                {systemHealth.overall_status.toUpperCase()}
              </div>
              <div className="text-sm text-gray-600">System Status</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{systemHealth.active_agents}</div>
              <div className="text-sm text-gray-600">Active Agents</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">{systemHealth.processing_queue}</div>
              <div className="text-sm text-gray-600">Queue Size</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">{systemHealth.avg_response_time}ms</div>
              <div className="text-sm text-gray-600">Avg Response</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{systemHealth.uptime}</div>
              <div className="text-sm text-gray-600">Uptime</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Active Agents Alert */}
      {agents.some(agent => agent.status === 'error') && (
        <Alert className="border-red-200 bg-red-50">
          <AlertCircle className="w-4 h-4 text-red-600" />
          <AlertDescription className="text-red-700">
            <strong>{agents.filter(a => a.status === 'error').length} agents</strong> require attention. 
            Check agent status and restart if necessary.
          </AlertDescription>
        </Alert>
      )}

      {/* AI Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent) => (
          <Card key={agent.id} className="hover:shadow-lg transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  {getAgentIcon(agent.type)}
                  <h3 className="font-semibold text-sm">{agent.name}</h3>
                </div>
                <Badge className={getStatusColor(agent.status)} variant="outline">
                  {getStatusIcon(agent.status)}
                  {agent.status.toUpperCase()}
                </Badge>
              </div>
            </CardHeader>

            <CardContent className="space-y-4">
              {/* Current Task */}
              <div className="space-y-2">
                <div className="text-sm font-medium">Current Task:</div>
                <div className="text-xs text-gray-600 bg-gray-50 p-2 rounded">
                  {agent.current_task}
                </div>
                {agent.status === 'running' && (
                  <Progress value={agent.progress} className="h-2" />
                )}
              </div>

              {/* Performance Metrics */}
              <div className="space-y-2">
                <div className="text-sm font-medium">Performance:</div>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="bg-green-50 p-2 rounded text-center">
                    <div className="font-bold text-green-600">{agent.performance.success_rate}%</div>
                    <div className="text-green-700">Success Rate</div>
                  </div>
                  <div className="bg-blue-50 p-2 rounded text-center">
                    <div className="font-bold text-blue-600">{agent.performance.today_processed}</div>
                    <div className="text-blue-700">Today</div>
                  </div>
                  <div className="bg-purple-50 p-2 rounded text-center">
                    <div className="font-bold text-purple-600">{agent.performance.total_processed}</div>
                    <div className="text-purple-700">Total</div>
                  </div>
                  <div className="bg-orange-50 p-2 rounded text-center">
                    <div className="font-bold text-orange-600">{agent.performance.avg_processing_time}s</div>
                    <div className="text-orange-700">Avg Time</div>
                  </div>
                </div>
              </div>

              {/* Recent Results */}
              <div className="space-y-2">
                <div className="text-sm font-medium">Recent Activity:</div>
                <div className="space-y-2 max-h-32 overflow-y-auto">
                  {agent.recent_results.slice(0, 2).map((result, index) => (
                    <div key={index} className="text-xs bg-gray-50 p-2 rounded">
                      <div className="font-medium">{result.action}</div>
                      <div className="text-gray-600">{result.result}</div>
                      {result.impact && (
                        <div className="text-green-600 mt-1">→ {result.impact}</div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Capabilities */}
              <div className="space-y-2">
                <div className="text-sm font-medium">Capabilities:</div>
                <div className="flex flex-wrap gap-1">
                  {agent.capabilities.slice(0, 3).map((capability, index) => (
                    <Badge key={index} variant="secondary" className="text-xs">
                      {capability}
                    </Badge>
                  ))}
                  {agent.capabilities.length > 3 && (
                    <Badge variant="secondary" className="text-xs">
                      +{agent.capabilities.length - 3} more
                    </Badge>
                  )}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-2 pt-2 border-t">
                {agent.status === 'idle' || agent.status === 'completed' ? (
                  <Button 
                    size="sm" 
                    className="flex-1 bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600"
                    onClick={() => handleAgentAction(agent.id, 'start')}
                  >
                    <Zap className="w-3 h-3 mr-1" />
                    Start
                  </Button>
                ) : agent.status === 'running' ? (
                  <Button 
                    size="sm" 
                    variant="outline" 
                    className="flex-1"
                    onClick={() => handleAgentAction(agent.id, 'pause')}
                  >
                    <Clock className="w-3 h-3 mr-1" />
                    Pause
                  </Button>
                ) : (
                  <Button 
                    size="sm" 
                    variant="outline" 
                    className="flex-1"
                    onClick={() => handleAgentAction(agent.id, 'restart')}
                  >
                    <RefreshCw className="w-3 h-3 mr-1" />
                    Restart
                  </Button>
                )}
                <Button size="sm" variant="ghost">
                  <Eye className="w-3 h-3" />
                </Button>
              </div>

              {/* Scheduling Info */}
              <div className="text-xs text-gray-500 pt-2 border-t">
                <div>Last run: {new Date(agent.last_run).toLocaleString()}</div>
                {agent.next_scheduled && (
                  <div>Next: {new Date(agent.next_scheduled).toLocaleString()}</div>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* System Actions */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bot className="w-5 h-5 text-purple-500" />
            System Actions
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-3">
            <Button variant="outline" className="flex items-center gap-2">
              <RefreshCw className="w-4 h-4" />
              Refresh All Status
            </Button>
            <Button variant="outline" className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4" />
              Run Health Check
            </Button>
            <Button variant="outline" className="flex items-center gap-2">
              <Activity className="w-4 h-4" />
              View Logs
            </Button>
            <Button variant="outline" className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4" />
              Performance Report
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
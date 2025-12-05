'use client';

import { useEffect, useState } from 'react';
import { 
  Activity,
  Server,
  Database,
  Zap,
  Globe,
  Shield,
  Clock,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Wifi,
  HardDrive,
  Cpu,
  MemoryStick,
  Network,
  Eye,
  RefreshCw
} from 'lucide-react';

// Mock comprehensive system health data
const mockSystemServices = [
  {
    service_name: 'API Gateway',
    status: 'healthy',
    response_time: 45,
    uptime_percentage: 99.9,
    port: 8080,
    version: '1.2.3',
    last_check: '2024-01-15T11:55:00Z',
    health_endpoint: '/health',
    description: 'Multi-tenant routing and access control',
    dependencies: ['Auth Service', 'Event Bus'],
    metrics: {
      requests_per_minute: 1250,
      error_rate: 0.02,
      cpu_usage: 35,
      memory_usage: 512,
      disk_usage: 15
    },
    errors: []
  },
  {
    service_name: 'AI Agents',
    status: 'healthy',
    response_time: 120,
    uptime_percentage: 99.5,
    port: 8001,
    version: '2.1.0',
    last_check: '2024-01-15T11:55:00Z',
    health_endpoint: '/health',
    description: 'Autonomous AI agent orchestration',
    dependencies: ['API Gateway', 'Event Bus', 'Temporal'],
    metrics: {
      requests_per_minute: 890,
      error_rate: 0.05,
      cpu_usage: 72,
      memory_usage: 2048,
      disk_usage: 45
    },
    errors: []
  },
  {
    service_name: 'Django CRM',
    status: 'healthy',
    response_time: 80,
    uptime_percentage: 99.8,
    port: 8007,
    version: '3.2.1',
    last_check: '2024-01-15T11:55:00Z',
    health_endpoint: '/health',
    description: 'Customer relationship management system',
    dependencies: ['Database', 'API Gateway'],
    metrics: {
      requests_per_minute: 450,
      error_rate: 0.01,
      cpu_usage: 28,
      memory_usage: 1024,
      disk_usage: 35
    },
    errors: []
  },
  {
    service_name: 'Wagtail CMS',
    status: 'degraded',
    response_time: 250,
    uptime_percentage: 97.2,
    port: 8006,
    version: '4.1.2',
    last_check: '2024-01-15T11:55:00Z',
    health_endpoint: '/admin/health',
    description: 'Content management system',
    dependencies: ['Database', 'Media Storage'],
    metrics: {
      requests_per_minute: 120,
      error_rate: 0.15,
      cpu_usage: 85,
      memory_usage: 1536,
      disk_usage: 75
    },
    errors: [
      {
        timestamp: '2024-01-15T11:30:00Z',
        error_type: 'high_response_time',
        message: 'Response time exceeded threshold (>200ms)',
        severity: 'medium'
      },
      {
        timestamp: '2024-01-15T10:45:00Z',
        error_type: 'database_timeout',
        message: 'Database query timeout on media files',
        severity: 'low'
      }
    ]
  },
  {
    service_name: 'Event Bus',
    status: 'healthy',
    response_time: 35,
    uptime_percentage: 99.9,
    port: 8009,
    version: '1.0.5',
    last_check: '2024-01-15T11:55:00Z',
    health_endpoint: '/health',
    description: 'Domain event coordination and messaging',
    dependencies: ['Database'],
    metrics: {
      requests_per_minute: 2100,
      error_rate: 0.001,
      cpu_usage: 15,
      memory_usage: 256,
      disk_usage: 10
    },
    errors: []
  },
  {
    service_name: 'Domain Repository',
    status: 'healthy',
    response_time: 60,
    uptime_percentage: 99.7,
    port: 8011,
    version: '1.1.0',
    last_check: '2024-01-15T11:55:00Z',
    health_endpoint: '/health',
    description: 'Business entity management and storage',
    dependencies: ['Database', 'Event Bus'],
    metrics: {
      requests_per_minute: 780,
      error_rate: 0.02,
      cpu_usage: 42,
      memory_usage: 768,
      disk_usage: 25
    },
    errors: []
  },
  {
    service_name: 'Vault Service',
    status: 'healthy',
    response_time: 90,
    uptime_percentage: 99.4,
    port: 8201,
    version: '1.12.1',
    last_check: '2024-01-15T11:55:00Z',
    health_endpoint: '/v1/sys/health',
    description: 'Secrets management and security',
    dependencies: ['Consul Backend'],
    metrics: {
      requests_per_minute: 150,
      error_rate: 0.005,
      cpu_usage: 20,
      memory_usage: 512,
      disk_usage: 5
    },
    errors: []
  },
  {
    service_name: 'Temporal Integration',
    status: 'healthy',
    response_time: 110,
    uptime_percentage: 99.6,
    port: 8202,
    version: '1.20.0',
    last_check: '2024-01-15T11:55:00Z',
    health_endpoint: '/health',
    description: 'Workflow orchestration and execution',
    dependencies: ['Database', 'Event Bus'],
    metrics: {
      requests_per_minute: 320,
      error_rate: 0.01,
      cpu_usage: 55,
      memory_usage: 1024,
      disk_usage: 30
    },
    errors: []
  }
];

const mockInfrastructureMetrics = {
  database: {
    status: 'healthy',
    connections_active: 45,
    connections_max: 200,
    query_avg_time: 25,
    storage_used: '12.5 GB',
    storage_total: '100 GB'
  },
  cache: {
    status: 'healthy',
    hit_rate: 94.2,
    memory_used: '2.1 GB',
    memory_total: '4 GB',
    keys_count: 145000
  },
  load_balancer: {
    status: 'healthy',
    requests_per_second: 850,
    active_connections: 1200,
    backend_servers: 3,
    healthy_backends: 3
  },
  monitoring: {
    status: 'healthy',
    metrics_collected: 25000,
    alerts_active: 2,
    dashboards_count: 12
  }
};

const getStatusColor = (status: string) => {
  switch (status.toLowerCase()) {
    case 'healthy':
      return 'text-green-600 bg-green-50 border-green-200';
    case 'degraded':
      return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    case 'down':
      return 'text-red-600 bg-red-50 border-red-200';
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200';
  }
};

const getStatusIcon = (status: string) => {
  switch (status.toLowerCase()) {
    case 'healthy':
      return <CheckCircle className="h-5 w-5" />;
    case 'degraded':
      return <AlertTriangle className="h-5 w-5" />;
    case 'down':
      return <XCircle className="h-5 w-5" />;
    default:
      return <Clock className="h-5 w-5" />;
  }
};

const formatTimestamp = (timestamp: string) => {
  return new Date(timestamp).toLocaleString();
};

const getResponseTimeColor = (responseTime: number) => {
  if (responseTime < 100) return 'text-green-600';
  if (responseTime < 200) return 'text-yellow-600';
  return 'text-red-600';
};

const getUptimeColor = (uptime: number) => {
  if (uptime >= 99.5) return 'text-green-600';
  if (uptime >= 95) return 'text-yellow-600';
  return 'text-red-600';
};

export default function SystemStatusPage() {
  const [services, setServices] = useState(mockSystemServices);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [autoRefresh, setAutoRefresh] = useState(true);

  const healthyServices = services.filter(s => s.status === 'healthy').length;
  const degradedServices = services.filter(s => s.status === 'degraded').length;
  const downServices = services.filter(s => s.status === 'down').length;
  const totalErrors = services.reduce((sum, s) => sum + s.errors.length, 0);

  useEffect(() => {
    if (!autoRefresh) return;
    
    const interval = setInterval(() => {
      // Simulate real-time updates
      setLastUpdated(new Date());
      // In a real app, this would fetch fresh data from the API
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, [autoRefresh]);

  const handleRefresh = () => {
    setLastUpdated(new Date());
    // In a real app, this would trigger an API call to refresh all service data
  };

  return (
    <div className="min-h-screen bg-gray-50 pl-64">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 flex items-center">
                <Activity className="mr-3 h-8 w-8 text-blue-600" />
                System Status
              </h1>
              <p className="text-sm text-gray-600">Real-time monitoring of BizOSaaS platform services</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${autoRefresh ? 'bg-green-500 animate-pulse' : 'bg-gray-300'}`}></div>
                <span className="text-sm text-gray-600">
                  {autoRefresh ? 'Auto-refresh enabled' : 'Auto-refresh disabled'}
                </span>
              </div>
              <button
                onClick={() => setAutoRefresh(!autoRefresh)}
                className={`px-3 py-1 text-xs rounded-md ${autoRefresh ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'}`}
              >
                {autoRefresh ? 'Disable' : 'Enable'}
              </button>
              <button
                onClick={handleRefresh}
                className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <RefreshCw className="mr-2 h-4 w-4" />
                Refresh
              </button>
            </div>
          </div>
          <div className="mt-2 text-sm text-gray-500">
            Last updated: {lastUpdated.toLocaleTimeString()}
          </div>
        </div>
      </header>

      <main className="p-6 space-y-6">
        {/* Overall Health Status */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
            <div className="flex items-center">
              <CheckCircle className="h-8 w-8 text-green-600" />
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">{healthyServices}</h3>
                <p className="text-sm text-gray-600">Healthy Services</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
            <div className="flex items-center">
              <AlertTriangle className="h-8 w-8 text-yellow-600" />
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">{degradedServices}</h3>
                <p className="text-sm text-gray-600">Degraded Services</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
            <div className="flex items-center">
              <XCircle className="h-8 w-8 text-red-600" />
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">{downServices}</h3>
                <p className="text-sm text-gray-600">Down Services</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
            <div className="flex items-center">
              <AlertTriangle className="h-8 w-8 text-orange-600" />
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">{totalErrors}</h3>
                <p className="text-sm text-gray-600">Active Alerts</p>
              </div>
            </div>
          </div>
        </div>

        {/* Service Status Grid */}
        <div className="bg-white rounded-lg shadow border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900 flex items-center">
              <Server className="mr-2 h-5 w-5" />
              Service Health
            </h2>
          </div>
          <div className="p-6">
            <div className="space-y-6">
              {services.map((service) => (
                <div key={service.service_name} className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="flex items-center justify-center w-10 h-10 bg-blue-100 rounded-lg">
                        <Server className="h-5 w-5 text-blue-600" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{service.service_name}</h3>
                        <p className="text-sm text-gray-600">{service.description}</p>
                      </div>
                    </div>
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(service.status)}`}>
                      {getStatusIcon(service.status)}
                      <span className="ml-1">{service.status.charAt(0).toUpperCase() + service.status.slice(1)}</span>
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-4">
                    <div className="space-y-2">
                      <h4 className="text-sm font-medium text-gray-700">Connection Info</h4>
                      <div className="space-y-1 text-sm text-gray-600">
                        <div>Port: {service.port}</div>
                        <div>Version: {service.version}</div>
                        <div>Endpoint: {service.health_endpoint}</div>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <h4 className="text-sm font-medium text-gray-700">Performance</h4>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Response Time:</span>
                          <span className={`font-medium ${getResponseTimeColor(service.response_time)}`}>
                            {service.response_time}ms
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Uptime:</span>
                          <span className={`font-medium ${getUptimeColor(service.uptime_percentage)}`}>
                            {service.uptime_percentage}%
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Requests/min:</span>
                          <span className="font-medium text-gray-900">{service.metrics.requests_per_minute}</span>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <h4 className="text-sm font-medium text-gray-700">Resources</h4>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">CPU:</span>
                          <span className="font-medium text-gray-900">{service.metrics.cpu_usage}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Memory:</span>
                          <span className="font-medium text-gray-900">{service.metrics.memory_usage}MB</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Disk:</span>
                          <span className="font-medium text-gray-900">{service.metrics.disk_usage}%</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {service.errors.length > 0 && (
                    <div className="bg-red-50 rounded-lg p-4">
                      <h4 className="text-sm font-medium text-red-800 mb-2">Recent Errors</h4>
                      <div className="space-y-2">
                        {service.errors.map((error, index) => (
                          <div key={index} className="text-sm">
                            <div className="flex items-center justify-between">
                              <span className="text-red-700">{error.error_type}</span>
                              <span className={`px-2 py-1 rounded text-xs ${
                                error.severity === 'high' ? 'bg-red-200 text-red-800' :
                                error.severity === 'medium' ? 'bg-yellow-200 text-yellow-800' :
                                'bg-gray-200 text-gray-800'
                              }`}>
                                {error.severity}
                              </span>
                            </div>
                            <p className="text-red-600">{error.message}</p>
                            <p className="text-red-500 text-xs">{formatTimestamp(error.timestamp)}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <div className="flex items-center justify-between">
                      <div className="text-sm text-gray-500">
                        Dependencies: {service.dependencies.join(', ')}
                      </div>
                      <div className="text-sm text-gray-500">
                        Last checked: {formatTimestamp(service.last_check)}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Infrastructure Overview */}
        <div className="bg-white rounded-lg shadow border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900 flex items-center">
              <Database className="mr-2 h-5 w-5" />
              Infrastructure Health
            </h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center mb-3">
                  <Database className="h-6 w-6 text-blue-600" />
                  <h3 className="ml-2 font-medium text-gray-900">Database</h3>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Status:</span>
                    <span className="font-medium text-green-600">Healthy</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Connections:</span>
                    <span className="font-medium text-gray-900">
                      {mockInfrastructureMetrics.database.connections_active}/{mockInfrastructureMetrics.database.connections_max}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Avg Query Time:</span>
                    <span className="font-medium text-gray-900">{mockInfrastructureMetrics.database.query_avg_time}ms</span>
                  </div>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center mb-3">
                  <Zap className="h-6 w-6 text-purple-600" />
                  <h3 className="ml-2 font-medium text-gray-900">Cache</h3>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Status:</span>
                    <span className="font-medium text-green-600">Healthy</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Hit Rate:</span>
                    <span className="font-medium text-gray-900">{mockInfrastructureMetrics.cache.hit_rate}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Keys:</span>
                    <span className="font-medium text-gray-900">{mockInfrastructureMetrics.cache.keys_count.toLocaleString()}</span>
                  </div>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center mb-3">
                  <Network className="h-6 w-6 text-green-600" />
                  <h3 className="ml-2 font-medium text-gray-900">Load Balancer</h3>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Status:</span>
                    <span className="font-medium text-green-600">Healthy</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">RPS:</span>
                    <span className="font-medium text-gray-900">{mockInfrastructureMetrics.load_balancer.requests_per_second}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Backends:</span>
                    <span className="font-medium text-gray-900">
                      {mockInfrastructureMetrics.load_balancer.healthy_backends}/{mockInfrastructureMetrics.load_balancer.backend_servers}
                    </span>
                  </div>
                </div>
              </div>

              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center mb-3">
                  <Eye className="h-6 w-6 text-orange-600" />
                  <h3 className="ml-2 font-medium text-gray-900">Monitoring</h3>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Status:</span>
                    <span className="font-medium text-green-600">Healthy</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Active Alerts:</span>
                    <span className="font-medium text-gray-900">{mockInfrastructureMetrics.monitoring.alerts_active}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Dashboards:</span>
                    <span className="font-medium text-gray-900">{mockInfrastructureMetrics.monitoring.dashboards_count}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
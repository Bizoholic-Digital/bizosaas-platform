'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Slider } from "@/components/ui/slider";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { 
  Settings,
  Bot,
  Cpu,
  Memory,
  HardDrive,
  Network,
  Zap,
  Shield,
  Clock,
  Target,
  AlertCircle,
  CheckCircle,
  Save,
  RotateCcw,
  Copy,
  Download,
  Upload,
  Play,
  Pause,
  Square,
  Trash2,
  Plus,
  Edit,
  Key,
  Database,
  Server,
  Globe,
  Lock,
  Unlock,
  Eye,
  EyeOff,
  Code,
  FileJson,
  Terminal
} from 'lucide-react';

// Configuration interfaces
interface AgentConfiguration {
  id: string;
  name: string;
  version: string;
  status: 'active' | 'inactive' | 'maintenance';
  
  // Basic Settings
  basic: {
    enabled: boolean;
    priority: 'low' | 'medium' | 'high' | 'critical';
    description: string;
    tags: string[];
    environment: 'development' | 'staging' | 'production';
  };

  // Resource Allocation
  resources: {
    cpu: {
      min: number;
      max: number;
      current: number;
    };
    memory: {
      min: number; // MB
      max: number; // MB
      current: number; // MB
    };
    disk: {
      min: number; // GB
      max: number; // GB
      current: number; // GB
    };
    network: {
      bandwidth: number; // Mbps
      connections: number;
    };
  };

  // Performance Settings
  performance: {
    maxConcurrentTasks: number;
    responseTimeoutMs: number;
    retryAttempts: number;
    backoffMultiplier: number;
    rateLimitRpm: number; // requests per minute
    cacheEnabled: boolean;
    cacheTtlSeconds: number;
  };

  // API & Integration Settings
  integrations: {
    apiKeys: { [key: string]: string };
    webhookUrls: string[];
    allowedOrigins: string[];
    rateLimit: {
      enabled: boolean;
      requestsPerMinute: number;
      burstLimit: number;
    };
  };

  // Security Settings
  security: {
    encryption: {
      enabled: boolean;
      algorithm: string;
    };
    authentication: {
      required: boolean;
      method: 'api_key' | 'oauth' | 'jwt';
    };
    ipWhitelist: string[];
    auditLogging: boolean;
  };

  // Monitoring & Alerts
  monitoring: {
    healthCheckInterval: number; // seconds
    metricsRetention: number; // days
    alertThresholds: {
      cpuUsage: number;
      memoryUsage: number;
      errorRate: number;
      responseTime: number;
    };
    notificationChannels: string[];
  };

  // AI-Specific Settings
  aiSettings: {
    model: string;
    temperature: number;
    maxTokens: number;
    tools: string[];
    capabilities: string[];
    learningEnabled: boolean;
    knowledgeBase: {
      enabled: boolean;
      updateFrequency: number; // hours
      sources: string[];
    };
  };
}

// Mock configuration data
const createMockConfiguration = (agentId: string): AgentConfiguration => ({
  id: agentId,
  name: 'Lead Scoring Agent',
  version: '2.1.4',
  status: 'active',
  
  basic: {
    enabled: true,
    priority: 'high',
    description: 'AI-powered lead qualification and scoring system with behavioral analysis',
    tags: ['CRM', 'Lead Management', 'AI', 'Scoring'],
    environment: 'production'
  },

  resources: {
    cpu: { min: 10, max: 80, current: 45 },
    memory: { min: 512, max: 4096, current: 2048 },
    disk: { min: 10, max: 100, current: 25 },
    network: { bandwidth: 100, connections: 1000 }
  },

  performance: {
    maxConcurrentTasks: 50,
    responseTimeoutMs: 30000,
    retryAttempts: 3,
    backoffMultiplier: 2.0,
    rateLimitRpm: 1000,
    cacheEnabled: true,
    cacheTtlSeconds: 300
  },

  integrations: {
    apiKeys: {
      'openai': '***************',
      'hubspot': '***************',
      'salesforce': '***************'
    },
    webhookUrls: [
      'https://api.bizosaas.com/webhooks/lead-scored',
      'https://api.crm.example.com/lead-update'
    ],
    allowedOrigins: ['https://app.bizosaas.com', 'https://admin.bizosaas.com'],
    rateLimit: {
      enabled: true,
      requestsPerMinute: 1000,
      burstLimit: 100
    }
  },

  security: {
    encryption: {
      enabled: true,
      algorithm: 'AES-256-GCM'
    },
    authentication: {
      required: true,
      method: 'jwt'
    },
    ipWhitelist: ['10.0.0.0/8', '172.16.0.0/12'],
    auditLogging: true
  },

  monitoring: {
    healthCheckInterval: 30,
    metricsRetention: 30,
    alertThresholds: {
      cpuUsage: 80,
      memoryUsage: 85,
      errorRate: 5,
      responseTime: 5000
    },
    notificationChannels: ['email', 'slack', 'webhook']
  },

  aiSettings: {
    model: 'gpt-4-turbo',
    temperature: 0.3,
    maxTokens: 4000,
    tools: ['lead_analyzer', 'scoring_engine', 'behavioral_tracker'],
    capabilities: ['lead_qualification', 'scoring', 'behavioral_analysis', 'predictive_modeling'],
    learningEnabled: true,
    knowledgeBase: {
      enabled: true,
      updateFrequency: 24,
      sources: ['crm_data', 'lead_history', 'industry_standards']
    }
  }
});

// Resource allocation component
const ResourceAllocation: React.FC<{
  resources: AgentConfiguration['resources'];
  onChange: (resources: AgentConfiguration['resources']) => void;
}> = ({ resources, onChange }) => {
  const updateResource = (type: 'cpu' | 'memory' | 'disk', field: string, value: number) => {
    onChange({
      ...resources,
      [type]: {
        ...resources[type],
        [field]: value
      }
    });
  };

  const ResourceSlider = ({ 
    type, 
    label, 
    unit, 
    min, 
    max 
  }: { 
    type: 'cpu' | 'memory' | 'disk';
    label: string;
    unit: string;
    min: number;
    max: number;
  }) => (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <Label className="text-sm font-medium">{label}</Label>
        <span className="text-sm text-gray-500">
          {resources[type].current}{unit} / {resources[type].max}{unit}
        </span>
      </div>
      <Slider
        value={[resources[type].current]}
        onValueChange={([value]) => updateResource(type, 'current', value)}
        min={resources[type].min}
        max={resources[type].max}
        step={type === 'cpu' ? 1 : type === 'memory' ? 64 : 1}
        className="w-full"
      />
      <div className="flex justify-between text-xs text-gray-500">
        <span>Min: {resources[type].min}{unit}</span>
        <span>Max: {resources[type].max}{unit}</span>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <ResourceSlider type="cpu" label="CPU Allocation" unit="%" min={0} max={100} />
      <ResourceSlider type="memory" label="Memory Allocation" unit="MB" min={0} max={8192} />
      <ResourceSlider type="disk" label="Disk Space" unit="GB" min={0} max={500} />
      
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="bandwidth">Network Bandwidth (Mbps)</Label>
          <Input
            id="bandwidth"
            type="number"
            value={resources.network.bandwidth}
            onChange={(e) => onChange({
              ...resources,
              network: {
                ...resources.network,
                bandwidth: parseInt(e.target.value) || 0
              }
            })}
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="connections">Max Connections</Label>
          <Input
            id="connections"
            type="number"
            value={resources.network.connections}
            onChange={(e) => onChange({
              ...resources,
              network: {
                ...resources.network,
                connections: parseInt(e.target.value) || 0
              }
            })}
          />
        </div>
      </div>
    </div>
  );
};

// API Keys management component
const APIKeysManager: React.FC<{
  apiKeys: { [key: string]: string };
  onChange: (apiKeys: { [key: string]: string }) => void;
}> = ({ apiKeys, onChange }) => {
  const [showKeys, setShowKeys] = useState<{ [key: string]: boolean }>({});
  const [newKeyName, setNewKeyName] = useState('');
  const [newKeyValue, setNewKeyValue] = useState('');
  const [isAddingKey, setIsAddingKey] = useState(false);

  const toggleKeyVisibility = (keyName: string) => {
    setShowKeys(prev => ({
      ...prev,
      [keyName]: !prev[keyName]
    }));
  };

  const addApiKey = () => {
    if (newKeyName && newKeyValue) {
      onChange({
        ...apiKeys,
        [newKeyName]: newKeyValue
      });
      setNewKeyName('');
      setNewKeyValue('');
      setIsAddingKey(false);
    }
  };

  const removeApiKey = (keyName: string) => {
    const newKeys = { ...apiKeys };
    delete newKeys[keyName];
    onChange(newKeys);
  };

  const updateApiKey = (keyName: string, value: string) => {
    onChange({
      ...apiKeys,
      [keyName]: value
    });
  };

  return (
    <div className="space-y-4">
      {Object.entries(apiKeys).map(([keyName, keyValue]) => (
        <div key={keyName} className="flex items-center space-x-2 p-3 border rounded-lg">
          <Key className="w-4 h-4 text-gray-500" />
          <div className="flex-1">
            <Label className="text-sm font-medium">{keyName}</Label>
            <div className="flex items-center space-x-2 mt-1">
              <Input
                type={showKeys[keyName] ? 'text' : 'password'}
                value={keyValue}
                onChange={(e) => updateApiKey(keyName, e.target.value)}
                className="font-mono text-sm"
              />
              <Button
                variant="ghost"
                size="sm"
                onClick={() => toggleKeyVisibility(keyName)}
              >
                {showKeys[keyName] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeApiKey(keyName)}
                className="text-red-600 hover:text-red-700"
              >
                <Trash2 className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      ))}

      {isAddingKey ? (
        <div className="space-y-2 p-3 border-2 border-dashed rounded-lg">
          <Input
            placeholder="API Key Name (e.g., openai, stripe)"
            value={newKeyName}
            onChange={(e) => setNewKeyName(e.target.value)}
          />
          <Input
            placeholder="API Key Value"
            type="password"
            value={newKeyValue}
            onChange={(e) => setNewKeyValue(e.target.value)}
          />
          <div className="flex space-x-2">
            <Button size="sm" onClick={addApiKey}>Add Key</Button>
            <Button size="sm" variant="outline" onClick={() => setIsAddingKey(false)}>
              Cancel
            </Button>
          </div>
        </div>
      ) : (
        <Button
          variant="outline"
          size="sm"
          onClick={() => setIsAddingKey(true)}
          className="w-full border-dashed"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add API Key
        </Button>
      )}
    </div>
  );
};

// Main configuration manager component
export default function AgentConfigurationManager({ agentId }: { agentId: string }) {
  const [config, setConfig] = useState<AgentConfiguration>(createMockConfiguration(agentId));
  const [hasChanges, setHasChanges] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [activeTab, setActiveTab] = useState('basic');

  // Track changes
  useEffect(() => {
    setHasChanges(true);
  }, [config]);

  const updateConfig = (path: string[], value: any) => {
    setConfig(prev => {
      const newConfig = { ...prev };
      let current = newConfig;
      
      for (let i = 0; i < path.length - 1; i++) {
        current = current[path[i]] = { ...current[path[i]] };
      }
      
      current[path[path.length - 1]] = value;
      return newConfig;
    });
  };

  const saveConfiguration = async () => {
    setIsSaving(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    setHasChanges(false);
    setIsSaving(false);
  };

  const resetConfiguration = () => {
    setConfig(createMockConfiguration(agentId));
    setHasChanges(false);
  };

  const exportConfiguration = () => {
    const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${config.name.toLowerCase().replace(/\s+/g, '-')}-config.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center">
            <Settings className="w-6 h-6 mr-2" />
            Agent Configuration - {config.name}
          </h2>
          <p className="text-gray-600">
            Version {config.version} | Status: 
            <Badge variant="outline" className="ml-2">
              {config.status}
            </Badge>
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={exportConfiguration}>
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
          <Button variant="outline" size="sm" onClick={resetConfiguration}>
            <RotateCcw className="w-4 h-4 mr-2" />
            Reset
          </Button>
          <Button 
            onClick={saveConfiguration} 
            disabled={!hasChanges || isSaving}
            className={hasChanges ? 'bg-blue-600 hover:bg-blue-700' : ''}
          >
            <Save className="w-4 h-4 mr-2" />
            {isSaving ? 'Saving...' : 'Save Changes'}
          </Button>
        </div>
      </div>

      {/* Configuration Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-7">
          <TabsTrigger value="basic">Basic</TabsTrigger>
          <TabsTrigger value="resources">Resources</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="integrations">Integrations</TabsTrigger>
          <TabsTrigger value="security">Security</TabsTrigger>
          <TabsTrigger value="monitoring">Monitoring</TabsTrigger>
          <TabsTrigger value="ai">AI Settings</TabsTrigger>
        </TabsList>

        {/* Basic Settings */}
        <TabsContent value="basic" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Basic Configuration</CardTitle>
              <CardDescription>Fundamental agent settings and metadata</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="agent-name">Agent Name</Label>
                  <Input
                    id="agent-name"
                    value={config.name}
                    onChange={(e) => updateConfig(['name'], e.target.value)}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="priority">Priority Level</Label>
                  <Select
                    value={config.basic.priority}
                    onValueChange={(value) => updateConfig(['basic', 'priority'], value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="low">Low</SelectItem>
                      <SelectItem value="medium">Medium</SelectItem>
                      <SelectItem value="high">High</SelectItem>
                      <SelectItem value="critical">Critical</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  value={config.basic.description}
                  onChange={(e) => updateConfig(['basic', 'description'], e.target.value)}
                  rows={3}
                />
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  id="enabled"
                  checked={config.basic.enabled}
                  onCheckedChange={(checked) => updateConfig(['basic', 'enabled'], checked)}
                />
                <Label htmlFor="enabled">Agent Enabled</Label>
              </div>

              <div className="space-y-2">
                <Label>Environment</Label>
                <Select
                  value={config.basic.environment}
                  onValueChange={(value) => updateConfig(['basic', 'environment'], value)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="development">Development</SelectItem>
                    <SelectItem value="staging">Staging</SelectItem>
                    <SelectItem value="production">Production</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Tags</Label>
                <div className="flex flex-wrap gap-2">
                  {config.basic.tags.map((tag, index) => (
                    <Badge key={index} variant="secondary" className="cursor-pointer">
                      {tag}
                      <button
                        onClick={() => {
                          const newTags = config.basic.tags.filter((_, i) => i !== index);
                          updateConfig(['basic', 'tags'], newTags);
                        }}
                        className="ml-1 text-red-500 hover:text-red-700"
                      >
                        ×
                      </button>
                    </Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Resource Allocation */}
        <TabsContent value="resources" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Cpu className="w-5 h-5 mr-2" />
                Resource Allocation
              </CardTitle>
              <CardDescription>Configure CPU, memory, disk, and network resources</CardDescription>
            </CardHeader>
            <CardContent>
              <ResourceAllocation
                resources={config.resources}
                onChange={(resources) => updateConfig(['resources'], resources)}
              />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Performance Settings */}
        <TabsContent value="performance" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Zap className="w-5 h-5 mr-2" />
                Performance Settings
              </CardTitle>
              <CardDescription>Configure performance parameters and optimization settings</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="max-tasks">Max Concurrent Tasks</Label>
                  <Input
                    id="max-tasks"
                    type="number"
                    value={config.performance.maxConcurrentTasks}
                    onChange={(e) => updateConfig(['performance', 'maxConcurrentTasks'], parseInt(e.target.value))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="timeout">Response Timeout (ms)</Label>
                  <Input
                    id="timeout"
                    type="number"
                    value={config.performance.responseTimeoutMs}
                    onChange={(e) => updateConfig(['performance', 'responseTimeoutMs'], parseInt(e.target.value))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="retry-attempts">Retry Attempts</Label>
                  <Input
                    id="retry-attempts"
                    type="number"
                    value={config.performance.retryAttempts}
                    onChange={(e) => updateConfig(['performance', 'retryAttempts'], parseInt(e.target.value))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="rate-limit">Rate Limit (req/min)</Label>
                  <Input
                    id="rate-limit"
                    type="number"
                    value={config.performance.rateLimitRpm}
                    onChange={(e) => updateConfig(['performance', 'rateLimitRpm'], parseInt(e.target.value))}
                  />
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  id="cache-enabled"
                  checked={config.performance.cacheEnabled}
                  onCheckedChange={(checked) => updateConfig(['performance', 'cacheEnabled'], checked)}
                />
                <Label htmlFor="cache-enabled">Enable Caching</Label>
              </div>

              {config.performance.cacheEnabled && (
                <div className="space-y-2">
                  <Label htmlFor="cache-ttl">Cache TTL (seconds)</Label>
                  <Input
                    id="cache-ttl"
                    type="number"
                    value={config.performance.cacheTtlSeconds}
                    onChange={(e) => updateConfig(['performance', 'cacheTtlSeconds'], parseInt(e.target.value))}
                  />
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Integrations */}
        <TabsContent value="integrations" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Globe className="w-5 h-5 mr-2" />
                API Keys & Integrations
              </CardTitle>
              <CardDescription>Manage external service integrations and API credentials</CardDescription>
            </CardHeader>
            <CardContent>
              <APIKeysManager
                apiKeys={config.integrations.apiKeys}
                onChange={(apiKeys) => updateConfig(['integrations', 'apiKeys'], apiKeys)}
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Webhook Configuration</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {config.integrations.webhookUrls.map((url, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <Input
                    value={url}
                    onChange={(e) => {
                      const newUrls = [...config.integrations.webhookUrls];
                      newUrls[index] = e.target.value;
                      updateConfig(['integrations', 'webhookUrls'], newUrls);
                    }}
                    placeholder="https://api.example.com/webhook"
                  />
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => {
                      const newUrls = config.integrations.webhookUrls.filter((_, i) => i !== index);
                      updateConfig(['integrations', 'webhookUrls'], newUrls);
                    }}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              ))}
              <Button
                variant="outline"
                size="sm"
                onClick={() => {
                  const newUrls = [...config.integrations.webhookUrls, ''];
                  updateConfig(['integrations', 'webhookUrls'], newUrls);
                }}
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Webhook URL
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Security Settings */}
        <TabsContent value="security" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Shield className="w-5 h-5 mr-2" />
                Security Configuration
              </CardTitle>
              <CardDescription>Configure security, encryption, and access controls</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center space-x-2">
                <Switch
                  id="encryption-enabled"
                  checked={config.security.encryption.enabled}
                  onCheckedChange={(checked) => updateConfig(['security', 'encryption', 'enabled'], checked)}
                />
                <Label htmlFor="encryption-enabled">Enable Encryption</Label>
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  id="auth-required"
                  checked={config.security.authentication.required}
                  onCheckedChange={(checked) => updateConfig(['security', 'authentication', 'required'], checked)}
                />
                <Label htmlFor="auth-required">Require Authentication</Label>
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  id="audit-logging"
                  checked={config.security.auditLogging}
                  onCheckedChange={(checked) => updateConfig(['security', 'auditLogging'], checked)}
                />
                <Label htmlFor="audit-logging">Enable Audit Logging</Label>
              </div>

              <div className="space-y-2">
                <Label>Authentication Method</Label>
                <Select
                  value={config.security.authentication.method}
                  onValueChange={(value) => updateConfig(['security', 'authentication', 'method'], value)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="api_key">API Key</SelectItem>
                    <SelectItem value="oauth">OAuth 2.0</SelectItem>
                    <SelectItem value="jwt">JWT Token</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Monitoring Settings */}
        <TabsContent value="monitoring" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Target className="w-5 h-5 mr-2" />
                Monitoring & Alerts
              </CardTitle>
              <CardDescription>Configure monitoring thresholds and alert notifications</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="health-check">Health Check Interval (seconds)</Label>
                  <Input
                    id="health-check"
                    type="number"
                    value={config.monitoring.healthCheckInterval}
                    onChange={(e) => updateConfig(['monitoring', 'healthCheckInterval'], parseInt(e.target.value))}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="metrics-retention">Metrics Retention (days)</Label>
                  <Input
                    id="metrics-retention"
                    type="number"
                    value={config.monitoring.metricsRetention}
                    onChange={(e) => updateConfig(['monitoring', 'metricsRetention'], parseInt(e.target.value))}
                  />
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="font-medium">Alert Thresholds</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="cpu-threshold">CPU Usage (%)</Label>
                    <Input
                      id="cpu-threshold"
                      type="number"
                      value={config.monitoring.alertThresholds.cpuUsage}
                      onChange={(e) => updateConfig(['monitoring', 'alertThresholds', 'cpuUsage'], parseInt(e.target.value))}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="memory-threshold">Memory Usage (%)</Label>
                    <Input
                      id="memory-threshold"
                      type="number"
                      value={config.monitoring.alertThresholds.memoryUsage}
                      onChange={(e) => updateConfig(['monitoring', 'alertThresholds', 'memoryUsage'], parseInt(e.target.value))}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="error-threshold">Error Rate (%)</Label>
                    <Input
                      id="error-threshold"
                      type="number"
                      value={config.monitoring.alertThresholds.errorRate}
                      onChange={(e) => updateConfig(['monitoring', 'alertThresholds', 'errorRate'], parseInt(e.target.value))}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="response-threshold">Response Time (ms)</Label>
                    <Input
                      id="response-threshold"
                      type="number"
                      value={config.monitoring.alertThresholds.responseTime}
                      onChange={(e) => updateConfig(['monitoring', 'alertThresholds', 'responseTime'], parseInt(e.target.value))}
                    />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* AI Settings */}
        <TabsContent value="ai" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Bot className="w-5 h-5 mr-2" />
                AI Configuration
              </CardTitle>
              <CardDescription>Configure AI model settings and capabilities</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="ai-model">AI Model</Label>
                  <Select
                    value={config.aiSettings.model}
                    onValueChange={(value) => updateConfig(['aiSettings', 'model'], value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="gpt-4-turbo">GPT-4 Turbo</SelectItem>
                      <SelectItem value="gpt-4">GPT-4</SelectItem>
                      <SelectItem value="gpt-3.5-turbo">GPT-3.5 Turbo</SelectItem>
                      <SelectItem value="claude-3-opus">Claude 3 Opus</SelectItem>
                      <SelectItem value="claude-3-sonnet">Claude 3 Sonnet</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="max-tokens">Max Tokens</Label>
                  <Input
                    id="max-tokens"
                    type="number"
                    value={config.aiSettings.maxTokens}
                    onChange={(e) => updateConfig(['aiSettings', 'maxTokens'], parseInt(e.target.value))}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="temperature">Temperature: {config.aiSettings.temperature}</Label>
                <Slider
                  value={[config.aiSettings.temperature]}
                  onValueChange={([value]) => updateConfig(['aiSettings', 'temperature'], value)}
                  min={0}
                  max={2}
                  step={0.1}
                  className="w-full"
                />
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  id="learning-enabled"
                  checked={config.aiSettings.learningEnabled}
                  onCheckedChange={(checked) => updateConfig(['aiSettings', 'learningEnabled'], checked)}
                />
                <Label htmlFor="learning-enabled">Enable Learning</Label>
              </div>

              <div className="flex items-center space-x-2">
                <Switch
                  id="knowledge-base"
                  checked={config.aiSettings.knowledgeBase.enabled}
                  onCheckedChange={(checked) => updateConfig(['aiSettings', 'knowledgeBase', 'enabled'], checked)}
                />
                <Label htmlFor="knowledge-base">Enable Knowledge Base</Label>
              </div>

              <div className="space-y-2">
                <Label>Capabilities</Label>
                <div className="flex flex-wrap gap-2">
                  {config.aiSettings.capabilities.map((capability, index) => (
                    <Badge key={index} variant="secondary">
                      {capability}
                    </Badge>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label>Tools</Label>
                <div className="flex flex-wrap gap-2">
                  {config.aiSettings.tools.map((tool, index) => (
                    <Badge key={index} variant="outline">
                      {tool}
                    </Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
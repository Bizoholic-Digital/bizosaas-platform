'use client';

import { AgentRoleManagement } from './AgentRoleManagement';
import { AgentPerformancePanel } from './AgentPerformancePanel';
import { AgentOptimizationQueue } from './AgentOptimizationQueue';
import PlaygroundManager from './PlaygroundManager';
import { useAgentStore } from '../../lib/stores/agent-store';
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
import { Label } from "@/components/ui/label";
import {
    Settings, Bot, Cpu, HardDrive, Network, Zap, Shield, Clock, Target,
    AlertCircle, CheckCircle, Save, RotateCcw, Copy, Download, Upload, Play, Pause,
    Square, Trash2, Plus, Edit, Key, Database, Globe, Lock, Unlock, Eye,
    EyeOff, Code, FileJson, Terminal, X, Power, Activity, RefreshCw, Users, Sparkles, Server, FlaskConical
} from 'lucide-react';

interface AgentManagementControlsProps {
    agentId: string;
    onClose: () => void;
}

interface AgentConfig {
    id: string;
    name: string;
    version: string;
    status: 'active' | 'inactive' | 'maintenance' | 'error' | 'starting' | 'stopping';

    // Basic Settings
    basic: {
        enabled: boolean;
        autoRestart: boolean;
        priority: 'low' | 'medium' | 'high' | 'critical';
        description: string;
        tags: string[];
        environment: 'development' | 'staging' | 'production';
    };

    // Resource Allocation
    resources: {
        cpu: { min: number; max: number; current: number; limit: number };
        memory: { min: number; max: number; current: number; limit: number };
        disk: { min: number; max: number; current: number };
        network: { bandwidth: number; connections: number };
    };

    // Performance Settings
    performance: {
        maxConcurrentTasks: number;
        responseTimeoutMs: number;
        retryAttempts: number;
        backoffMultiplier: number;
        rateLimitRpm: number;
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
        encryption: { enabled: boolean; algorithm: string };
        authentication: { required: boolean; method: 'api_key' | 'oauth' | 'jwt' };
        ipWhitelist: string[];
        auditLogging: boolean;
    };

    // Monitoring & Alerts
    monitoring: {
        healthCheckInterval: number;
        metricsRetention: number;
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
        knowledgeBase: { enabled: boolean; updateFrequency: number; sources: string[] };
    };
}

// Mock configuration generator with seeding from agent store
import { Agent as StoreAgent } from '../../lib/stores/agent-store';

const createMockConfiguration = (agentId: string, storeAgent?: StoreAgent): AgentConfig => ({
    id: agentId,
    name: storeAgent?.name || 'Lead Scoring Agent',
    version: '2.1.4',
    status: (storeAgent?.status as any) || 'active',

    basic: {
        enabled: storeAgent?.status === 'active',
        autoRestart: true,
        priority: 'high',
        description: storeAgent?.description || 'AI-powered lead qualification and scoring system with behavioral analysis',
        tags: [storeAgent?.team || 'CRM', 'AI'],
        environment: 'production'
    },

    resources: {
        cpu: { min: 10, max: 80, current: 45, limit: 2.0 },
        memory: { min: 512, max: 4096, current: 2048, limit: 4096 },
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
            'openai': 'sk-proj-********************',
            'hubspot': 'pat-na1-*******************',
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
        encryption: { enabled: true, algorithm: 'AES-256-GCM' },
        authentication: { required: true, method: 'jwt' },
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
        tools: storeAgent?.tools || ['lead_analyzer', 'scoring_engine', 'behavioral_tracker'],
        capabilities: storeAgent?.tasks || ['lead_qualification', 'scoring', 'behavioral_analysis', 'predictive_modeling'],
        learningEnabled: true,
        knowledgeBase: {
            enabled: true,
            updateFrequency: 24,
            sources: ['crm_data', 'lead_history', 'industry_standards']
        }
    }
});

export function AgentManagementControls({ agentId, onClose }: AgentManagementControlsProps) {
    const { agents } = useAgentStore();
    const storeAgent = agents.find(a => a.id === agentId);

    const [config, setConfig] = useState<AgentConfig>(createMockConfiguration(agentId, storeAgent));
    const [activeTab, setActiveTab] = useState('status');
    const [isLoading, setIsLoading] = useState(false);
    const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

    // Real-time status simulation
    useEffect(() => {
        const interval = setInterval(() => {
            setConfig(prev => ({
                ...prev,
                resources: {
                    ...prev.resources,
                    cpu: { ...prev.resources.cpu, current: Math.min(100, Math.max(0, prev.resources.cpu.current + (Math.random() - 0.5) * 10)) },
                    memory: { ...prev.resources.memory, current: Math.min(prev.resources.memory.limit, Math.max(200, prev.resources.memory.current + (Math.random() - 0.5) * 50)) }
                }
            }));
        }, 3000);
        return () => clearInterval(interval);
    }, []);

    const updateConfig = (path: string[], value: any) => {
        setConfig(prev => {
            const newConfig = { ...prev };
            let current: any = newConfig;
            for (let i = 0; i < path.length - 1; i++) {
                current = current[path[i]] = { ...current[path[i]] };
            }
            current[path[path.length - 1]] = value;
            return newConfig as AgentConfig;
        });
        setHasUnsavedChanges(true);
    };

    const handleStart = async () => {
        setIsLoading(true);
        setConfig(prev => ({ ...prev, status: 'starting' }));
        await new Promise(resolve => setTimeout(resolve, 2000));
        setConfig(prev => ({ ...prev, status: 'active' }));
        setIsLoading(false);
    };

    const handleStop = async () => {
        setIsLoading(true);
        setConfig(prev => ({ ...prev, status: 'stopping' }));
        await new Promise(resolve => setTimeout(resolve, 1500));
        setConfig(prev => ({ ...prev, status: 'inactive' }));
        setIsLoading(false);
    };

    const handleRestart = async () => {
        await handleStop();
        await handleStart();
    };

    const handleSave = async () => {
        setIsLoading(true);
        await new Promise(resolve => setTimeout(resolve, 1000));
        setHasUnsavedChanges(false);
        setIsLoading(false);
    };

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
            <div className="bg-white dark:bg-gray-900 rounded-xl shadow-2xl w-full max-w-6xl max-h-[90vh] flex flex-col overflow-hidden border border-gray-200 dark:border-gray-800 animate-in fade-in zoom-in-95 duration-200">

                {/* Header */}
                <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-900/50">
                    <div className="flex items-center gap-4">
                        <div className="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-xl text-blue-600 dark:text-blue-400">
                            <Bot className="w-8 h-8" />
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
                                {config.name}
                                <Badge variant="outline" className={
                                    config.status === 'active' ? 'text-green-600 bg-green-50 border-green-200' :
                                        config.status === 'error' ? 'text-red-600 bg-red-50 border-red-200' :
                                            'text-gray-600 bg-gray-50 border-gray-200'
                                }>
                                    {config.status.toUpperCase()}
                                </Badge>
                            </h2>
                            <p className="text-gray-500 dark:text-gray-400 text-sm mt-1 font-mono">ID: {agentId} • v{config.version}</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-3">
                        <Button variant="outline" onClick={onClose}>Cancel</Button>
                        <Button onClick={handleSave} disabled={!hasUnsavedChanges || isLoading}>
                            <Save className="w-4 h-4 mr-2" />
                            Save Changes
                        </Button>
                    </div>
                </div>

                {/* Main Content */}
                <div className="flex flex-1 overflow-hidden">
                    {/* Sidebar */}
                    <div className="w-64 border-r border-gray-200 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-900/50 p-4 overflow-y-auto">
                        <div className="space-y-1">
                            <NavButton id="status" label="Status & Control" icon={Activity} active={activeTab} onClick={setActiveTab} />
                            <NavButton id="basic" label="Basic Settings" icon={Settings} active={activeTab} onClick={setActiveTab} />
                            <NavButton id="roles" label="Role Management" icon={Users} active={activeTab} onClick={setActiveTab} />
                            <NavButton id="resources" label="Resources" icon={Cpu} active={activeTab} onClick={setActiveTab} />
                            <NavButton id="performance" label="Performance" icon={Zap} active={activeTab} onClick={setActiveTab} />
                            <NavButton id="optimizations" label="Optimizations" icon={Sparkles} active={activeTab} onClick={setActiveTab} />
                            <NavButton id="ai" label="AI Configuration" icon={Bot} active={activeTab} onClick={setActiveTab} />
                            <NavButton id="playground" label="Playground" icon={FlaskConical} active={activeTab} onClick={setActiveTab} />
                            <NavButton id="integrations" label="Integrations" icon={Globe} active={activeTab} onClick={setActiveTab} />
                            <NavButton id="security" label="Security" icon={Shield} active={activeTab} onClick={setActiveTab} />
                            <NavButton id="monitoring" label="Monitoring" icon={Target} active={activeTab} onClick={setActiveTab} />
                        </div>
                    </div>

                    {/* Content Area */}
                    <div className="flex-1 overflow-y-auto p-8 bg-white dark:bg-gray-900">
                        {activeTab === 'status' && (
                            <div className="space-y-6">
                                {/* Status Cards */}
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                    <StatusCard
                                        title="Uptime"
                                        value="99.9%"
                                        icon={Clock}
                                        color="text-green-600"
                                        footer="Last 30 days"
                                    />
                                    <StatusCard
                                        title="Success Rate"
                                        value="95.2%"
                                        icon={CheckCircle}
                                        color="text-blue-600"
                                        footer="4.8% error rate"
                                    />
                                    <StatusCard
                                        title="Total Requests"
                                        value="1.2M"
                                        icon={Activity}
                                        color="text-purple-600"
                                        footer="+12% vs last week"
                                    />
                                </div>

                                {/* Control Buttons */}
                                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                                    <ControlButton
                                        label="Start Agent"
                                        icon={Play}
                                        onClick={handleStart}
                                        disabled={config.status === 'active' || isLoading}
                                        className="bg-green-50 text-green-700 hover:bg-green-100 border-green-200"
                                    />
                                    <ControlButton
                                        label="Stop Agent"
                                        icon={Square}
                                        onClick={handleStop}
                                        disabled={config.status === 'inactive' || isLoading}
                                        className="bg-red-50 text-red-700 hover:bg-red-100 border-red-200"
                                    />
                                    <ControlButton
                                        label="Restart"
                                        icon={RotateCcw}
                                        onClick={handleRestart}
                                        disabled={isLoading}
                                        className="bg-blue-50 text-blue-700 hover:bg-blue-100 border-blue-200"
                                    />
                                    <ControlButton
                                        label="Reload Config"
                                        icon={RefreshCw}
                                        onClick={() => { }}
                                        disabled={isLoading}
                                        className="bg-gray-50 text-gray-700 hover:bg-gray-100 border-gray-200"
                                    />
                                </div>

                                {/* Continuous Feedback Loop & Optimization */}
                                <Card className="border-blue-200 bg-blue-50/30">
                                    <CardHeader className="pb-2">
                                        <div className="flex items-center justify-between">
                                            <CardTitle className="text-lg flex items-center gap-2">
                                                <RefreshCw className="w-5 h-5 text-blue-600 animate-spin-slow" />
                                                Continuous Feedback Loop
                                            </CardTitle>
                                            <Badge variant="secondary" className="bg-blue-100 text-blue-700 border-blue-200">
                                                Auto-Optimizing
                                            </Badge>
                                        </div>
                                    </CardHeader>
                                    <CardContent className="space-y-4">
                                        <div className="grid grid-cols-2 gap-4">
                                            <div className="p-3 bg-white rounded-lg border border-blue-100 shadow-sm">
                                                <p className="text-xs text-gray-500 uppercase font-bold tracking-wider">Learning Rate</p>
                                                <p className="text-xl font-bold text-blue-700">0.02</p>
                                                <div className="w-full bg-gray-100 h-1 mt-2 rounded-full overflow-hidden">
                                                    <div className="bg-blue-500 h-full w-[20%]" />
                                                </div>
                                            </div>
                                            <div className="p-3 bg-white rounded-lg border border-blue-100 shadow-sm">
                                                <p className="text-xs text-gray-500 uppercase font-bold tracking-wider">Data Points</p>
                                                <p className="text-xl font-bold text-blue-700">4,281</p>
                                                <p className="text-[10px] text-green-600 mt-1 flex items-center gap-1 font-medium">
                                                    <Zap className="w-3 h-3" /> +12 per/min
                                                </p>
                                            </div>
                                        </div>
                                        <div className="text-sm text-gray-600 bg-white/50 p-3 rounded-lg border border-blue-50">
                                            <p className="font-medium flex items-center gap-2 mb-1">
                                                <Cpu className="w-4 h-4 text-blue-500" />
                                                Recent Optimization
                                            </p>
                                            <p className="text-xs italic">"Bidding threshold adjusted by -5% based on conversion decay in the last 24h cycle."</p>
                                        </div>
                                        <div className="flex gap-2">
                                            <Button variant="outline" size="sm" className="flex-1 bg-white">View Feedback Data</Button>
                                            <Button variant="default" size="sm" className="flex-1 bg-blue-600 hover:bg-blue-700">Manual Override</Button>
                                        </div>
                                    </CardContent>
                                </Card>
                            </div>
                        )}

                        {activeTab === 'basic' && (
                            <div className="space-y-6 max-w-3xl">
                                <div className="space-y-4">
                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <Label>Agent Name</Label>
                                            <Input value={config.name} onChange={(e) => updateConfig(['name'], e.target.value)} />
                                        </div>
                                        <div className="space-y-2">
                                            <Label>Environment</Label>
                                            <Select
                                                value={config.basic.environment}
                                                onValueChange={(val) => updateConfig(['basic', 'environment'], val)}
                                            >
                                                <SelectTrigger><SelectValue /></SelectTrigger>
                                                <SelectContent>
                                                    <SelectItem value="development">Development</SelectItem>
                                                    <SelectItem value="staging">Staging</SelectItem>
                                                    <SelectItem value="production">Production</SelectItem>
                                                </SelectContent>
                                            </Select>
                                        </div>
                                    </div>
                                    <div className="space-y-2">
                                        <Label>Description</Label>
                                        <Textarea
                                            value={config.basic.description}
                                            onChange={(e) => updateConfig(['basic', 'description'], e.target.value)}
                                            rows={3}
                                        />
                                    </div>
                                    <div className="flex items-center justify-between p-4 border rounded-lg bg-gray-50">
                                        <div className="space-y-0.5">
                                            <Label>Agent Enabled</Label>
                                            <p className="text-sm text-gray-500">Enable or disable this agent's operation</p>
                                        </div>
                                        <Switch
                                            checked={config.basic.enabled}
                                            onCheckedChange={(c) => updateConfig(['basic', 'enabled'], c)}
                                        />
                                    </div>
                                    <div className="flex items-center justify-between p-4 border rounded-lg bg-gray-50">
                                        <div className="space-y-0.5">
                                            <Label>Auto Restart</Label>
                                            <p className="text-sm text-gray-500">Automatically restart if the agent crashes</p>
                                        </div>
                                        <Switch
                                            checked={config.basic.autoRestart}
                                            onCheckedChange={(c) => updateConfig(['basic', 'autoRestart'], c)}
                                        />
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeTab === 'roles' && (
                            <AgentRoleManagement agentId={agentId} />
                        )}

                        {activeTab === 'performance' && (
                            <AgentPerformancePanel agentId={agentId} />
                        )}

                        {activeTab === 'optimizations' && (
                            <AgentOptimizationQueue agentId={agentId} />
                        )}

                        {activeTab === 'ai' && (
                            <div className="space-y-6 max-w-3xl">
                                <div className="grid grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <Label>AI Model</Label>
                                        <Select value={config.aiSettings.model} onValueChange={(v) => updateConfig(['aiSettings', 'model'], v)}>
                                            <SelectTrigger><SelectValue /></SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="gpt-4-turbo">GPT-4 Turbo</SelectItem>
                                                <SelectItem value="gpt-3.5-turbo">GPT-3.5 Turbo</SelectItem>
                                                <SelectItem value="claude-3-opus">Claude 3 Opus</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>
                                    <div className="space-y-2">
                                        <Label>Max Tokens</Label>
                                        <Input
                                            type="number"
                                            value={config.aiSettings.maxTokens}
                                            onChange={(e) => updateConfig(['aiSettings', 'maxTokens'], parseInt(e.target.value))}
                                        />
                                    </div>
                                </div>
                                <div className="space-y-4 pt-4 border-t">
                                    <div className="space-y-2">
                                        <div className="flex justify-between">
                                            <Label>Temperature</Label>
                                            <span className="text-sm text-gray-500">{config.aiSettings.temperature}</span>
                                        </div>
                                        <Slider
                                            value={[config.aiSettings.temperature]}
                                            max={1}
                                            step={0.1}
                                            onValueChange={(val: number[]) => updateConfig(['aiSettings', 'temperature'], val[0])}
                                        />
                                        <p className="text-xs text-gray-400">Controls randomness: Lower is more deterministic, higher is more creative.</p>
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    <Label>Tools & Services</Label>
                                    <div className="flex flex-wrap gap-2 p-4 border rounded-lg bg-gray-50 min-h-[60px]">
                                        {config.aiSettings.tools.length > 0 ? (
                                            config.aiSettings.tools.map(tool => (
                                                <Badge key={tool} variant="secondary" className="px-3 py-1 text-sm bg-white shadow-sm border">{tool}</Badge>
                                            ))
                                        ) : (
                                            <p className="text-sm text-gray-400 italic">No specific tools defined</p>
                                        )}
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    <Label>Core Tasks & Capabilities</Label>
                                    <div className="flex flex-wrap gap-2 p-4 border rounded-lg bg-gray-50 min-h-[60px]">
                                        {config.aiSettings.capabilities.length > 0 ? (
                                            config.aiSettings.capabilities.map(cap => (
                                                <Badge key={cap} variant="outline" className="px-3 py-1 text-sm bg-blue-50 text-blue-700 border-blue-100">{cap}</Badge>
                                            ))
                                        ) : (
                                            <p className="text-sm text-gray-400 italic">No specific capabilities defined</p>
                                        )}
                                    </div>
                                </div>
                            </div>
                        )}

                        {activeTab === 'playground' && (
                            <PlaygroundManager agentId={agentId} />
                        )}

                        {(activeTab === 'resources' || activeTab === 'integrations' || activeTab === 'security' || activeTab === 'monitoring') && (
                            <div className="flex flex-col items-center justify-center py-20 text-center space-y-4 text-gray-500">
                                <div className="p-4 bg-gray-100 rounded-full">
                                    <Settings className="w-8 h-8" />
                                </div>
                                <h3 className="text-lg font-medium text-gray-900">Advanced Configuration</h3>
                                <p className="max-w-md">The settings for <span className="font-mono font-medium text-gray-700">{activeTab}</span> are fully managed via the Brain Core. These controls will be available in the next update.</p>
                                <Button variant="outline">View Raw Config</Button>
                            </div>
                        )}

                    </div>
                </div>
            </div>
        </div>
    );
}

function NavButton({ id, label, icon: Icon, active, onClick }: { id: string, label: string, icon: any, active: string, onClick: (id: string) => void }) {
    return (
        <button
            onClick={() => onClick(id)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${active === id
                ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
                }`}
        >
            <Icon className="w-4 h-4" />
            {label}
        </button>
    );
}

function StatusCard({ title, value, icon: Icon, color, footer }: any) {
    return (
        <Card>
            <CardContent className="p-6">
                <div className="flex items-center justify-between">
                    <div>
                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">{title}</p>
                        <p className="text-2xl font-bold mt-1 text-gray-900 dark:text-white">{value}</p>
                    </div>
                    <div className={`p-3 rounded-xl bg-opacity-10 ${color.replace('text-', 'bg-')}`}>
                        <Icon className={`w-6 h-6 ${color}`} />
                    </div>
                </div>
                {footer && <p className="text-xs text-gray-500 mt-4">{footer}</p>}
            </CardContent>
        </Card>
    );
}

function ControlButton({ label, icon: Icon, onClick, disabled, className }: any) {
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={`flex flex-col items-center justify-center p-4 rounded-xl border transition-all disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
        >
            <Icon className="w-6 h-6 mb-2" />
            <span className="text-sm font-medium">{label}</span>
        </button>
    );
}

function MetricBar({ label, value, max, unit, color }: any) {
    return (
        <div className="space-y-2">
            <div className="flex justify-between text-sm">
                <span className="font-medium text-gray-700 dark:text-gray-300">{label}</span>
                <span className="text-gray-500">{Math.round(value)}{unit} / {max}{unit}</span>
            </div>
            <div className="h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                <div
                    className={`h-full ${color} transition-all duration-500`}
                    style={{ width: `${Math.min(100, (value / max) * 100)}%` }}
                />
            </div>
        </div>
    );
}

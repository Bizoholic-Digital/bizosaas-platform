'use client';

import React, { useState, useEffect } from 'react';
import {
  Brain,
  Cpu,
  Zap,
  TrendingUp,
  Settings,
  CheckCircle,
  XCircle,
  BarChart3,
  DollarSign,
  Clock,
  Activity,
  Shield,
  RefreshCw
} from 'lucide-react';

interface LLMProvider {
  id: string;
  name: string;
  type: 'primary' | 'fallback';
  status: 'active' | 'inactive' | 'error';
  models: number;
  apiKey: string;
  requests: number;
  cost: number;
  avgResponseTime: number;
  successRate: number;
  capabilities: string[];
  lastUsed: string;
}

interface Model {
  id: string;
  name: string;
  provider: string;
  category: 'chat' | 'embedding' | 'vision' | 'reasoning';
  contextWindow: number;
  costPer1k: number;
  enabled: boolean;
  usage: number;
}

export default function LLMProvidersPage() {
  const [showPlanned, setShowPlanned] = useState(false);

  const [providers, setProviders] = useState<LLMProvider[]>([
    {
      id: 'openrouter',
      name: 'OpenRouter',
      type: 'primary',
      status: 'active',
      models: 200,
      apiKey: '*********************xyz',
      requests: 45678,
      cost: 1234.56,
      avgResponseTime: 1.2,
      successRate: 98.5,
      capabilities: ['200+ models', 'Model routing', 'Fallback handling', 'Cost optimization'],
      lastUsed: '2 minutes ago'
    },
    {
      id: 'openai',
      name: 'OpenAI',
      type: 'fallback',
      status: 'active',
      models: 8,
      apiKey: '*********************abc',
      requests: 8934,
      cost: 234.12,
      avgResponseTime: 0.8,
      successRate: 99.2,
      capabilities: ['GPT-4', 'GPT-3.5', 'DALL-E', 'Embeddings'],
      lastUsed: '15 minutes ago'
    },
    {
      id: 'anthropic',
      name: 'Anthropic Claude',
      type: 'fallback',
      status: 'active',
      models: 3,
      apiKey: '*********************def',
      requests: 5621,
      cost: 187.34,
      avgResponseTime: 1.5,
      successRate: 99.8,
      capabilities: ['Claude-3 Opus', 'Claude-3 Sonnet', 'Claude-3 Haiku', '200k context'],
      lastUsed: '5 minutes ago'
    },
    {
      id: 'gemini',
      name: 'Google Gemini',
      type: 'fallback',
      status: 'active',
      models: 2,
      apiKey: '*********************ghi',
      requests: 3456,
      cost: 98.45,
      avgResponseTime: 1.1,
      successRate: 97.9,
      capabilities: ['Gemini Pro', 'Gemini Pro Vision', 'Multi-modal'],
      lastUsed: '30 minutes ago'
    }
  ]);

  const [integratedProviders] = useState([
    {
      id: 'deepseek',
      name: 'DeepSeek',
      priority: 'Very High',
      reasoning: 'Best ROI at ~$0.55/million tokens, OpenAI-compatible API',
      models: 'DeepSeek-V3 (671B), DeepSeek-R1',
      useCases: 'Cost-optimized tasks, reasoning',
      effort: 'Low',
      status: '✅ Integrated',
      agents: 4,
      integrationDate: '2025-10-06'
    },
    {
      id: 'mistral',
      name: 'Mistral AI',
      priority: 'Very High',
      reasoning: 'EU compliance, self-hosting option, beats Llama 4 & DeepSeek',
      models: 'Mistral Large, Medium 3, Small, Ministral 3B',
      useCases: 'European clients, on-premise deployment',
      effort: 'Medium',
      status: '✅ Integrated',
      agents: 4,
      integrationDate: '2025-10-06'
    },
    {
      id: 'cohere',
      name: 'Cohere',
      priority: 'High',
      reasoning: 'Best-in-class RAG and reranking capabilities',
      models: 'Command (chat), Rerank, Embed',
      useCases: 'Knowledge base search, document analysis',
      effort: 'Medium',
      status: '✅ Integrated',
      agents: 5,
      integrationDate: '2025-10-06'
    },
    {
      id: 'bedrock',
      name: 'Amazon Bedrock',
      priority: 'Medium',
      reasoning: 'Multi-model AWS platform with unified API',
      models: 'Claude, Llama, Mistral, Titan, Jurassic',
      useCases: 'AWS-native deployments, model experimentation',
      effort: 'Medium-High',
      status: '✅ Integrated',
      agents: 4,
      integrationDate: '2025-10-06'
    },
    {
      id: 'azure-openai',
      name: 'Azure OpenAI',
      priority: 'Medium',
      reasoning: 'Enterprise SLAs, Microsoft 365 integration',
      models: 'GPT-4, GPT-3.5, DALL-E 3, Whisper',
      useCases: 'Enterprise compliance, AD integration',
      effort: 'Medium',
      status: '✅ Integrated',
      agents: 5,
      integrationDate: '2025-10-06'
    },
    {
      id: 'vertex-ai',
      name: 'Google Vertex AI',
      priority: 'Medium',
      reasoning: 'Unified GCP platform with custom training',
      models: 'Gemini, PaLM 2, Codey, Imagen',
      useCases: 'GCP-native deployments, custom models',
      effort: 'Medium-High',
      status: '✅ Integrated',
      agents: 5,
      integrationDate: '2025-10-06'
    },
    {
      id: 'perplexity',
      name: 'Perplexity API',
      priority: 'Low-Medium',
      reasoning: 'Real-time web search + LLM with citations',
      models: 'Perplexity models with live web',
      useCases: 'Market research, trend analysis',
      effort: 'Low',
      status: '✅ Integrated',
      agents: 4,
      integrationDate: '2025-10-06'
    },
    {
      id: 'huggingface',
      name: 'Hugging Face',
      priority: 'Low-Medium',
      reasoning: '1000+ open-source models, cost-effective',
      models: 'Llama, Falcon, BLOOM, StarCoder',
      useCases: 'Experimentation, specialized tasks',
      effort: 'Low',
      status: '✅ Integrated',
      agents: 7,
      integrationDate: '2025-10-06'
    }
  ]);

  const [selectedProvider, setSelectedProvider] = useState<string>('openrouter');
  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Simulate loading models for selected provider
    setLoading(true);
    setTimeout(() => {
      const mockModels: Model[] = [];
      if (selectedProvider === 'openrouter') {
        mockModels.push(
          { id: 'or-gpt4', name: 'OpenAI GPT-4', provider: 'OpenRouter', category: 'chat', contextWindow: 8192, costPer1k: 0.03, enabled: true, usage: 12456 },
          { id: 'or-claude', name: 'Claude-3 Opus', provider: 'OpenRouter', category: 'reasoning', contextWindow: 200000, costPer1k: 0.015, enabled: true, usage: 8934 },
          { id: 'or-gemini', name: 'Gemini Pro', provider: 'OpenRouter', category: 'chat', contextWindow: 32000, costPer1k: 0.001, enabled: true, usage: 5678 },
          { id: 'or-llama', name: 'Llama 3 70B', provider: 'OpenRouter', category: 'chat', contextWindow: 8192, costPer1k: 0.0008, enabled: false, usage: 0 }
        );
      } else if (selectedProvider === 'openai') {
        mockModels.push(
          { id: 'gpt-4', name: 'GPT-4', provider: 'OpenAI', category: 'chat', contextWindow: 8192, costPer1k: 0.03, enabled: true, usage: 4532 },
          { id: 'gpt-3.5', name: 'GPT-3.5 Turbo', provider: 'OpenAI', category: 'chat', contextWindow: 16384, costPer1k: 0.002, enabled: true, usage: 2341 },
          { id: 'ada-002', name: 'Text Embedding Ada 002', provider: 'OpenAI', category: 'embedding', contextWindow: 8191, costPer1k: 0.0001, enabled: true, usage: 1234 },
          { id: 'dall-e-3', name: 'DALL-E 3', provider: 'OpenAI', category: 'vision', contextWindow: 0, costPer1k: 0.04, enabled: false, usage: 0 }
        );
      } else if (selectedProvider === 'anthropic') {
        mockModels.push(
          { id: 'claude-opus', name: 'Claude-3 Opus', provider: 'Anthropic', category: 'reasoning', contextWindow: 200000, costPer1k: 0.015, enabled: true, usage: 3456 },
          { id: 'claude-sonnet', name: 'Claude-3 Sonnet', provider: 'Anthropic', category: 'chat', contextWindow: 200000, costPer1k: 0.003, enabled: true, usage: 1987 },
          { id: 'claude-haiku', name: 'Claude-3 Haiku', provider: 'Anthropic', category: 'chat', contextWindow: 200000, costPer1k: 0.00025, enabled: false, usage: 0 }
        );
      } else if (selectedProvider === 'gemini') {
        mockModels.push(
          { id: 'gemini-pro', name: 'Gemini Pro', provider: 'Google', category: 'chat', contextWindow: 32000, costPer1k: 0.001, enabled: true, usage: 2341 },
          { id: 'gemini-vision', name: 'Gemini Pro Vision', provider: 'Google', category: 'vision', contextWindow: 16384, costPer1k: 0.002, enabled: true, usage: 1115 }
        );
      }
      setModels(mockModels);
      setLoading(false);
    }, 500);
  }, [selectedProvider]);

  const totalCost = providers.reduce((sum, p) => sum + p.cost, 0);
  const totalRequests = providers.reduce((sum, p) => sum + p.requests, 0);
  const avgSuccessRate = providers.reduce((sum, p) => sum + p.successRate, 0) / providers.length;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Brain className="w-8 h-8 text-blue-600" />
          <h1 className="text-3xl font-bold text-gray-900">LLM Provider Management</h1>
        </div>
        <p className="text-gray-600">
          Manage AI model providers, configure API keys, monitor usage, and optimize costs across the platform
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <Cpu className="w-6 h-6 text-blue-600" />
            </div>
            <span className="text-sm text-green-600 font-medium">Active</span>
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-1">
            {providers.filter(p => p.status === 'active').length}
          </h3>
          <p className="text-sm text-gray-600">Active Providers</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-6 h-6 text-purple-600" />
            </div>
            <span className="text-sm text-gray-500">{totalRequests.toLocaleString()}</span>
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-1">{avgSuccessRate.toFixed(1)}%</h3>
          <p className="text-sm text-gray-600">Avg Success Rate</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <DollarSign className="w-6 h-6 text-green-600" />
            </div>
            <span className="text-sm text-gray-500">This month</span>
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-1">${totalCost.toLocaleString()}</h3>
          <p className="text-sm text-gray-600">Total API Cost</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
              <Activity className="w-6 h-6 text-orange-600" />
            </div>
            <span className="text-sm text-green-600">+12%</span>
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-1">{totalRequests.toLocaleString()}</h3>
          <p className="text-sm text-gray-600">Total Requests</p>
        </div>
      </div>

      {/* Providers Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {providers.map((provider) => (
          <div
            key={provider.id}
            className={`bg-white rounded-lg shadow hover:shadow-lg transition-shadow cursor-pointer ${
              selectedProvider === provider.id ? 'ring-2 ring-blue-500' : ''
            }`}
            onClick={() => setSelectedProvider(provider.id)}
          >
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                    provider.type === 'primary' ? 'bg-blue-100' : 'bg-gray-100'
                  }`}>
                    <Brain className={`w-6 h-6 ${
                      provider.type === 'primary' ? 'text-blue-600' : 'text-gray-600'
                    }`} />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{provider.name}</h3>
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`text-xs px-2 py-1 rounded ${
                        provider.type === 'primary'
                          ? 'bg-blue-100 text-blue-700'
                          : 'bg-gray-100 text-gray-700'
                      }`}>
                        {provider.type}
                      </span>
                      <span className={`flex items-center gap-1 text-xs ${
                        provider.status === 'active' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {provider.status === 'active' ? (
                          <CheckCircle className="w-3 h-3" />
                        ) : (
                          <XCircle className="w-3 h-3" />
                        )}
                        {provider.status}
                      </span>
                    </div>
                  </div>
                </div>
                <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                  <Settings className="w-5 h-5 text-gray-600" />
                </button>
              </div>

              {/* Metrics Grid */}
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <p className="text-xs text-gray-500 mb-1">Models Available</p>
                  <p className="text-lg font-semibold text-gray-900">{provider.models}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">Total Requests</p>
                  <p className="text-lg font-semibold text-gray-900">{provider.requests.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">Avg Response Time</p>
                  <p className="text-lg font-semibold text-gray-900">{provider.avgResponseTime}s</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">Success Rate</p>
                  <p className="text-lg font-semibold text-green-600">{provider.successRate}%</p>
                </div>
              </div>

              {/* Cost */}
              <div className="bg-gray-50 rounded-lg p-3 mb-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Total Cost (30 days)</span>
                  <span className="text-lg font-bold text-gray-900">${provider.cost.toLocaleString()}</span>
                </div>
              </div>

              {/* Capabilities */}
              <div className="mb-4">
                <p className="text-xs text-gray-500 mb-2">Capabilities</p>
                <div className="flex flex-wrap gap-2">
                  {provider.capabilities.map((cap, idx) => (
                    <span key={idx} className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded">
                      {cap}
                    </span>
                  ))}
                </div>
              </div>

              {/* API Key */}
              <div className="flex items-center justify-between text-xs text-gray-500 pt-3 border-t">
                <div className="flex items-center gap-1">
                  <Shield className="w-3 h-3" />
                  <span>API Key: {provider.apiKey}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  <span>{provider.lastUsed}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Planned Integrations Section */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">✅ Recently Integrated Providers</h2>
            <p className="text-sm text-gray-600 mt-1">8 new LLM providers added to the platform - All integrations complete!</p>
          </div>
          <button
            onClick={() => setShowPlanned(!showPlanned)}
            className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            <CheckCircle className="w-4 h-4" />
            {showPlanned ? 'Hide' : 'Show'} New Integrations ({integratedProviders.length})
          </button>
        </div>

        {showPlanned && (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="p-4 bg-green-50 border-b border-green-200">
              <div className="flex items-center gap-2 text-green-800">
                <CheckCircle className="w-5 h-5" />
                <p className="font-semibold">All Integrations Complete - 38 Specialized Agents Deployed</p>
              </div>
            </div>
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Provider</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Agents</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Key Models</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Use Cases</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {integratedProviders.map((provider) => (
                  <tr key={provider.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div>
                        <p className="font-semibold text-gray-900">{provider.name}</p>
                        <p className="text-xs text-gray-500 mt-1">{provider.reasoning}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="flex items-center gap-2 text-xs px-2 py-1 rounded bg-green-100 text-green-700">
                        <CheckCircle className="w-3 h-3" />
                        {provider.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-semibold text-blue-600">{provider.agents} agents</span>
                    </td>
                    <td className="px-6 py-4">
                      <p className="text-sm text-gray-900">{provider.models}</p>
                    </td>
                    <td className="px-6 py-4">
                      <p className="text-sm text-gray-600">{provider.useCases}</p>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-xs text-gray-600">{provider.integrationDate}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="p-4 bg-gray-50 border-t border-gray-200">
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <p className="text-2xl font-bold text-blue-600">{integratedProviders.length}</p>
                  <p className="text-xs text-gray-600">New Providers</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-green-600">{integratedProviders.reduce((sum, p) => sum + p.agents, 0)}</p>
                  <p className="text-xs text-gray-600">Specialized Agents</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-purple-600">12</p>
                  <p className="text-xs text-gray-600">Total LLM Providers</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Models Table */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-gray-900">
                Available Models - {providers.find(p => p.id === selectedProvider)?.name}
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                {models.filter(m => m.enabled).length} enabled / {models.length} total models
              </p>
            </div>
            <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              <RefreshCw className="w-4 h-4" />
              Refresh Models
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Model Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Category
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Context Window
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Cost per 1K
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Usage (30d)
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {loading ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-gray-500">
                    <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" />
                    Loading models...
                  </td>
                </tr>
              ) : models.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-gray-500">
                    No models available
                  </td>
                </tr>
              ) : (
                models.map((model) => (
                  <tr key={model.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <Cpu className="w-4 h-4 text-gray-400" />
                        <span className="text-sm font-medium text-gray-900">{model.name}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`text-xs px-2 py-1 rounded ${
                        model.category === 'chat' ? 'bg-blue-100 text-blue-700' :
                        model.category === 'reasoning' ? 'bg-purple-100 text-purple-700' :
                        model.category === 'embedding' ? 'bg-green-100 text-green-700' :
                        'bg-orange-100 text-orange-700'
                      }`}>
                        {model.category}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {model.contextWindow > 0 ? model.contextWindow.toLocaleString() : 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      ${model.costPer1k.toFixed(4)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {model.usage.toLocaleString()} requests
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={model.enabled}
                          onChange={() => {
                            const updated = models.map(m =>
                              m.id === model.id ? { ...m, enabled: !m.enabled } : m
                            );
                            setModels(updated);
                          }}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                      </label>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

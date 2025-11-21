'use client';

import React, { useState } from 'react';
import {
  ToggleLeft,
  ToggleRight,
  Search,
  Filter,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Settings,
  Users,
  Globe,
  Zap,
  Shield,
  Clock
} from 'lucide-react';

interface Feature {
  id: string;
  name: string;
  description: string;
  category: 'core' | 'ai' | 'integration' | 'analytics' | 'security';
  enabled: boolean;
  global: boolean;
  affectedUsers: number;
  lastModified: string;
  modifiedBy: string;
  dependencies: string[];
  risks: 'low' | 'medium' | 'high';
}

export default function FeatureTogglesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState<string>('all');

  const [features, setFeatures] = useState<Feature[]>([
    {
      id: 'llm-openrouter',
      name: 'OpenRouter LLM Integration',
      description: 'Primary LLM provider with 200+ models and intelligent routing',
      category: 'ai',
      enabled: true,
      global: true,
      affectedUsers: 8429,
      lastModified: '2025-10-06 04:15:00',
      modifiedBy: 'admin@bizosaas.com',
      dependencies: ['ai-agents', 'chat-interface'],
      risks: 'medium'
    },
    {
      id: 'llm-openai',
      name: 'OpenAI Native API',
      description: 'Direct OpenAI integration for GPT-4, DALL-E, and embeddings',
      category: 'ai',
      enabled: true,
      global: true,
      affectedUsers: 8429,
      lastModified: '2025-10-05 18:30:00',
      modifiedBy: 'admin@bizosaas.com',
      dependencies: ['ai-agents'],
      risks: 'low'
    },
    {
      id: 'llm-anthropic',
      name: 'Anthropic Claude API',
      description: 'Claude-3 models for advanced reasoning and content generation',
      category: 'ai',
      enabled: true,
      global: true,
      affectedUsers: 8429,
      lastModified: '2025-10-05 18:30:00',
      modifiedBy: 'admin@bizosaas.com',
      dependencies: ['ai-agents'],
      risks: 'low'
    },
    {
      id: 'llm-gemini',
      name: 'Google Gemini API',
      description: 'Gemini Pro and Vision models for multi-modal AI capabilities',
      category: 'ai',
      enabled: true,
      global: true,
      affectedUsers: 8429,
      lastModified: '2025-10-05 18:30:00',
      modifiedBy: 'admin@bizosaas.com',
      dependencies: ['ai-agents', 'vision-analysis'],
      risks: 'low'
    },
    {
      id: 'ai-agents',
      name: 'AI Agents System',
      description: 'Autonomous AI agents for marketing, analytics, and automation',
      category: 'ai',
      enabled: true,
      global: true,
      affectedUsers: 8429,
      lastModified: '2025-10-06 03:00:00',
      modifiedBy: 'admin@bizosaas.com',
      dependencies: [],
      risks: 'high'
    },
    {
      id: 'chat-interface',
      name: 'AI Chat Interface',
      description: 'Multi-model chat interface with file upload and conversation history',
      category: 'ai',
      enabled: true,
      global: true,
      affectedUsers: 8429,
      lastModified: '2025-10-06 02:45:00',
      modifiedBy: 'admin@bizosaas.com',
      dependencies: ['llm-openrouter'],
      risks: 'low'
    },
    {
      id: 'elasticsearch',
      name: 'Elasticsearch Search',
      description: 'Unified search engine with isolated indexes per service',
      category: 'core',
      enabled: false,
      global: true,
      affectedUsers: 0,
      lastModified: '2025-09-28 10:00:00',
      modifiedBy: 'system',
      dependencies: [],
      risks: 'medium'
    },
    {
      id: 'prometheus-monitoring',
      name: 'Prometheus Monitoring',
      description: 'Real-time metrics collection and performance monitoring',
      category: 'analytics',
      enabled: false,
      global: true,
      affectedUsers: 0,
      lastModified: '2025-09-28 10:00:00',
      modifiedBy: 'system',
      dependencies: [],
      risks: 'low'
    },
    {
      id: 'grafana-dashboards',
      name: 'Grafana Dashboards',
      description: 'Visual analytics and real-time operational dashboards',
      category: 'analytics',
      enabled: false,
      global: true,
      affectedUsers: 0,
      lastModified: '2025-09-28 10:00:00',
      modifiedBy: 'system',
      dependencies: ['prometheus-monitoring'],
      risks: 'low'
    },
    {
      id: 'multi-tenancy',
      name: 'Multi-Tenancy System',
      description: 'Row-level security and tenant isolation across all services',
      category: 'core',
      enabled: true,
      global: true,
      affectedUsers: 8429,
      lastModified: '2025-09-15 12:00:00',
      modifiedBy: 'system',
      dependencies: [],
      risks: 'high'
    },
    {
      id: 'rbac',
      name: 'Role-Based Access Control',
      description: 'Permission system with 5 roles and granular access control',
      category: 'security',
      enabled: true,
      global: true,
      affectedUsers: 8429,
      lastModified: '2025-09-15 12:00:00',
      modifiedBy: 'system',
      dependencies: ['multi-tenancy'],
      risks: 'high'
    },
    {
      id: 'sso',
      name: 'Single Sign-On',
      description: 'JWT-based authentication with cross-service token validation',
      category: 'security',
      enabled: true,
      global: true,
      affectedUsers: 8429,
      lastModified: '2025-09-20 14:30:00',
      modifiedBy: 'admin@bizosaas.com',
      dependencies: ['rbac'],
      risks: 'high'
    },
    {
      id: 'wagtail-cms',
      name: 'Wagtail CMS Integration',
      description: 'Content management system for marketing website',
      category: 'integration',
      enabled: true,
      global: false,
      affectedUsers: 247,
      lastModified: '2025-09-25 16:00:00',
      modifiedBy: 'admin@bizosaas.com',
      dependencies: [],
      risks: 'low'
    },
    {
      id: 'saleor-ecommerce',
      name: 'Saleor E-commerce',
      description: 'Complete e-commerce platform for product sales',
      category: 'integration',
      enabled: true,
      global: false,
      affectedUsers: 1245,
      lastModified: '2025-09-25 16:00:00',
      modifiedBy: 'admin@bizosaas.com',
      dependencies: [],
      risks: 'medium'
    },
    {
      id: 'django-crm',
      name: 'Django CRM',
      description: 'Customer relationship management with lead scoring',
      category: 'integration',
      enabled: true,
      global: false,
      affectedUsers: 3456,
      lastModified: '2025-09-25 16:00:00',
      modifiedBy: 'admin@bizosaas.com',
      dependencies: [],
      risks: 'medium'
    }
  ]);

  const toggleFeature = (featureId: string) => {
    setFeatures(features.map(f =>
      f.id === featureId
        ? { ...f, enabled: !f.enabled, lastModified: new Date().toISOString(), modifiedBy: 'admin@bizosaas.com' }
        : f
    ));
  };

  const filteredFeatures = features.filter(feature => {
    const matchesSearch = feature.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         feature.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = filterCategory === 'all' || feature.category === filterCategory;
    return matchesSearch && matchesCategory;
  });

  const stats = {
    total: features.length,
    enabled: features.filter(f => f.enabled).length,
    disabled: features.filter(f => !f.enabled).length,
    highRisk: features.filter(f => f.risks === 'high' && f.enabled).length
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'core': return Settings;
      case 'ai': return Zap;
      case 'integration': return Globe;
      case 'analytics': return ToggleLeft;
      case 'security': return Shield;
      default: return Settings;
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'high': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <ToggleLeft className="w-8 h-8 text-purple-600" />
          <h1 className="text-3xl font-bold text-gray-900">Feature Toggle Management</h1>
        </div>
        <p className="text-gray-600">
          Enable or disable platform features globally across all tenants with granular control
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <Settings className="w-6 h-6 text-blue-600" />
            </div>
            <span className="text-2xl font-bold text-gray-900">{stats.total}</span>
          </div>
          <p className="text-sm text-gray-600">Total Features</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <span className="text-2xl font-bold text-green-600">{stats.enabled}</span>
          </div>
          <p className="text-sm text-gray-600">Enabled Features</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
              <XCircle className="w-6 h-6 text-gray-600" />
            </div>
            <span className="text-2xl font-bold text-gray-600">{stats.disabled}</span>
          </div>
          <p className="text-sm text-gray-600">Disabled Features</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
              <AlertTriangle className="w-6 h-6 text-red-600" />
            </div>
            <span className="text-2xl font-bold text-red-600">{stats.highRisk}</span>
          </div>
          <p className="text-sm text-gray-600">High Risk Active</p>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search features..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-gray-400" />
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="all">All Categories</option>
              <option value="core">Core</option>
              <option value="ai">AI & ML</option>
              <option value="integration">Integrations</option>
              <option value="analytics">Analytics</option>
              <option value="security">Security</option>
            </select>
          </div>
        </div>
      </div>

      {/* Features List */}
      <div className="space-y-4">
        {filteredFeatures.map((feature) => {
          const CategoryIcon = getCategoryIcon(feature.category);
          return (
            <div key={feature.id} className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-start gap-4 flex-1">
                    <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                      feature.enabled ? 'bg-purple-100' : 'bg-gray-100'
                    }`}>
                      <CategoryIcon className={`w-6 h-6 ${
                        feature.enabled ? 'text-purple-600' : 'text-gray-400'
                      }`} />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900">{feature.name}</h3>
                        <span className={`text-xs px-2 py-1 rounded ${
                          feature.category === 'core' ? 'bg-blue-100 text-blue-700' :
                          feature.category === 'ai' ? 'bg-purple-100 text-purple-700' :
                          feature.category === 'integration' ? 'bg-green-100 text-green-700' :
                          feature.category === 'analytics' ? 'bg-orange-100 text-orange-700' :
                          'bg-red-100 text-red-700'
                        }`}>
                          {feature.category}
                        </span>
                        <span className={`text-xs px-2 py-1 rounded ${getRiskColor(feature.risks)}`}>
                          {feature.risks} risk
                        </span>
                        {feature.global && (
                          <span className="text-xs px-2 py-1 rounded bg-gray-100 text-gray-700">
                            Global
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-gray-600 mb-3">{feature.description}</p>

                      <div className="flex items-center gap-4 text-xs text-gray-500">
                        <div className="flex items-center gap-1">
                          <Users className="w-3 h-3" />
                          <span>{feature.affectedUsers.toLocaleString()} users</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          <span>Modified {new Date(feature.lastModified).toLocaleDateString()}</span>
                        </div>
                      </div>

                      {feature.dependencies.length > 0 && (
                        <div className="mt-3 pt-3 border-t border-gray-100">
                          <p className="text-xs text-gray-500 mb-1">Dependencies:</p>
                          <div className="flex flex-wrap gap-1">
                            {feature.dependencies.map((dep) => (
                              <span key={dep} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                                {dep}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Toggle Switch */}
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={feature.enabled}
                      onChange={() => toggleFeature(feature.id)}
                      className="sr-only peer"
                    />
                    <div className="w-14 h-7 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-purple-600"></div>
                  </label>
                </div>
              </div>
            </div>
          );
        })}

        {filteredFeatures.length === 0 && (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <Filter className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No features found matching your criteria</p>
          </div>
        )}
      </div>
    </div>
  );
}

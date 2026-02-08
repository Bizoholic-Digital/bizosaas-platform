'use client';

import React, { useState } from 'react';
import {
  Key, Globe, Shield, CheckCircle, AlertTriangle,
  Plus, Eye, EyeOff, X, Edit, Save, ExternalLink,
  Zap, CreditCard, Mail, MessageSquare, BarChart3,
  Search, Database, Lock
} from 'lucide-react';
import SettingsLayout from '@/components/settings/SettingsLayout';

interface APIKey {
  id: string;
  name: string;
  service: string;
  key: string;
  isVisible: boolean;
  status: 'active' | 'inactive' | 'error';
  lastUsed: string;
  created: string;
}

interface Integration {
  id: string;
  name: string;
  category: string;
  icon: React.ReactNode;
  status: 'connected' | 'disconnected' | 'error';
  description: string;
  configured: boolean;
  requiresKey: boolean;
}

const IntegrationsPage = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [apiKeys, setApiKeys] = useState<APIKey[]>([
    {
      id: '1',
      name: 'Production OpenAI',
      service: 'OpenAI',
      key: 'sk-proj-••••••••••••••••••••••••••••••••••••••••••••••••••••',
      isVisible: false,
      status: 'active',
      lastUsed: '2 hours ago',
      created: '2025-09-20'
    },
    {
      id: '2',
      name: 'Stripe Payment Gateway',
      service: 'Stripe',
      key: 'sk_live_••••••••••••••••••••••••••••••••••••••••••••••••••••',
      isVisible: false,
      status: 'active',
      lastUsed: '1 day ago',
      created: '2025-09-18'
    },
    {
      id: '3',
      name: 'Google Ads API',
      service: 'Google Ads',
      key: 'goog_••••••••••••••••••••••••••••••••••••••••••••••••••••',
      isVisible: false,
      status: 'inactive',
      lastUsed: 'Never',
      created: '2025-09-15'
    }
  ]);

  const [integrations] = useState<Integration[]>([
    {
      id: 'openai',
      name: 'OpenAI',
      category: 'AI & Machine Learning',
      icon: <Zap className="w-5 h-5" />,
      status: 'connected',
      description: 'GPT-4, ChatGPT, and DALL-E integration for AI-powered features',
      configured: true,
      requiresKey: true
    },
    {
      id: 'stripe',
      name: 'Stripe',
      category: 'Payments',
      icon: <CreditCard className="w-5 h-5" />,
      status: 'connected',
      description: 'Accept online payments and manage subscriptions',
      configured: true,
      requiresKey: true
    },
    {
      id: 'google-ads',
      name: 'Google Ads',
      category: 'Marketing',
      icon: <Search className="w-5 h-5" />,
      status: 'disconnected',
      description: 'Manage Google Ads campaigns and track performance',
      configured: false,
      requiresKey: true
    },
    {
      id: 'mailgun',
      name: 'Mailgun',
      category: 'Communication',
      icon: <Mail className="w-5 h-5" />,
      status: 'connected',
      description: 'Send transactional emails and marketing campaigns',
      configured: true,
      requiresKey: true
    },
    {
      id: 'slack',
      name: 'Slack',
      category: 'Communication',
      icon: <MessageSquare className="w-5 h-5" />,
      status: 'error',
      description: 'Team notifications and workflow automation',
      configured: false,
      requiresKey: true
    },
    {
      id: 'google-analytics',
      name: 'Google Analytics',
      category: 'Analytics',
      icon: <BarChart3 className="w-5 h-5" />,
      status: 'connected',
      description: 'Track website traffic and user behavior',
      configured: true,
      requiresKey: true
    }
  ]);

  const [newKeyForm, setNewKeyForm] = useState({
    name: '',
    service: '',
    key: '',
    showForm: false
  });

  const toggleKeyVisibility = (id: string) => {
    setApiKeys(keys =>
      keys.map(key =>
        key.id === id ? { ...key, isVisible: !key.isVisible } : key
      )
    );
  };

  const deleteApiKey = (id: string) => {
    setApiKeys(keys => keys.filter(key => key.id !== id));
  };

  const addNewKey = () => {
    if (newKeyForm.name && newKeyForm.service && newKeyForm.key) {
      const newKey: APIKey = {
        id: Date.now().toString(),
        name: newKeyForm.name,
        service: newKeyForm.service,
        key: newKeyForm.key,
        isVisible: false,
        status: 'active',
        lastUsed: 'Never',
        created: new Date().toISOString().split('T')[0]
      };
      setApiKeys(keys => [...keys, newKey]);
      setNewKeyForm({ name: '', service: '', key: '', showForm: false });
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
      case 'connected':
        return 'text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-400';
      case 'inactive':
      case 'disconnected':
        return 'text-gray-600 bg-gray-100 dark:bg-gray-800 dark:text-gray-400';
      case 'error':
        return 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
      case 'connected':
        return <CheckCircle className="w-4 h-4 text-green-600 dark:text-green-400" />;
      case 'error':
        return <AlertTriangle className="w-4 h-4 text-red-600 dark:text-red-400" />;
      default:
        return <X className="w-4 h-4 text-gray-600 dark:text-gray-400" />;
    }
  };

  const categories = Array.from(new Set(integrations.map(i => i.category)));

  const tabs = [
    { id: 'overview', label: 'Overview', icon: <Globe className="w-4 h-4" /> },
    { id: 'api-keys', label: 'API Keys', icon: <Key className="w-4 h-4" /> },
    { id: 'security', label: 'Security', icon: <Shield className="w-4 h-4" /> }
  ];

  return (
    <SettingsLayout
      title="Integrations & API Keys"
      description="Connect external services and manage API access"
    >
      <div className="flex flex-col">
        {/* Internal Tabs */}
        <div className="flex border-b border-slate-100 dark:border-slate-800">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-4 text-sm font-medium transition-colors border-b-2 ${activeTab === tab.id
                  ? 'border-blue-600 text-blue-600 bg-blue-50/50 dark:bg-blue-900/10'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800'
                }`}
            >
              {tab.icon}
              {tab.label}
            </button>
          ))}
        </div>

        {/* Main Content Area */}
        <div className="p-6">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Integration Overview</h3>
                <div className="flex items-center gap-3">
                  <span className="text-sm text-gray-500">
                    {integrations.filter(i => i.status === 'connected').length} of {integrations.length} connected
                  </span>
                  <div className="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{
                        width: `${(integrations.filter(i => i.status === 'connected').length / integrations.length) * 100}%`
                      }}
                    ></div>
                  </div>
                </div>
              </div>

              {categories.map((category) => (
                <div key={category} className="mb-8">
                  <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-4">{category}</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {integrations
                      .filter(integration => integration.category === category)
                      .map((integration) => (
                        <div key={integration.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-white dark:bg-slate-900/50">
                          <div className="flex items-start justify-between">
                            <div className="flex items-center gap-3">
                              <div className="w-10 h-10 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center">
                                {integration.icon}
                              </div>
                              <div>
                                <h5 className="font-medium text-gray-900 dark:text-white">{integration.name}</h5>
                                <p className="text-sm text-gray-500 dark:text-gray-400">{integration.description}</p>
                              </div>
                            </div>
                            <div className="flex items-center gap-2">
                              {getStatusIcon(integration.status)}
                              <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(integration.status)}`}>
                                {integration.status}
                              </span>
                            </div>
                          </div>
                          <div className="mt-4 flex justify-end">
                            <button className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300">
                              {integration.configured ? 'Configure' : 'Set up'}
                            </button>
                          </div>
                        </div>
                      ))
                    }
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* API Keys Tab */}
          {activeTab === 'api-keys' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white">API Keys Management</h3>
                <button
                  onClick={() => setNewKeyForm({ ...newKeyForm, showForm: true })}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  Add New Key
                </button>
              </div>

              {/* Security Warning */}
              <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
                <div className="flex items-start gap-3">
                  <AlertTriangle className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-yellow-900 dark:text-yellow-100">Keep your API keys secure</h4>
                    <p className="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                      Never share your API keys publicly or include them in client-side code. All keys are encrypted in our secure vault.
                    </p>
                  </div>
                </div>
              </div>

              {/* New Key Form */}
              {newKeyForm.showForm && (
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-gray-50 dark:bg-gray-900/50">
                  <h4 className="font-medium text-gray-900 dark:text-white mb-4">Add New API Key</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Key Name
                      </label>
                      <input
                        type="text"
                        value={newKeyForm.name}
                        onChange={(e) => setNewKeyForm({ ...newKeyForm, name: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white"
                        placeholder="e.g., Production OpenAI"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Service
                      </label>
                      <select
                        value={newKeyForm.service}
                        onChange={(e) => setNewKeyForm({ ...newKeyForm, service: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white"
                      >
                        <option value="">Select service</option>
                        <option value="OpenAI">OpenAI</option>
                        <option value="Stripe">Stripe</option>
                        <option value="Google Ads">Google Ads</option>
                        <option value="Mailgun">Mailgun</option>
                        <option value="Slack">Slack</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        API Key
                      </label>
                      <input
                        type="password"
                        value={newKeyForm.key}
                        onChange={(e) => setNewKeyForm({ ...newKeyForm, key: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white"
                        placeholder="Enter API key"
                      />
                    </div>
                  </div>
                  <div className="flex justify-end gap-2 mt-4">
                    <button
                      onClick={() => setNewKeyForm({ name: '', service: '', key: '', showForm: false })}
                      className="px-4 py-2 text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={addNewKey}
                      className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                    >
                      <Save className="w-4 h-4" />
                      Save Key
                    </button>
                  </div>
                </div>
              )}

              {/* API Keys List */}
              <div className="space-y-4">
                {apiKeys.map((apiKey) => (
                  <div key={apiKey.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-white dark:bg-slate-900/50">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h4 className="font-medium text-gray-900 dark:text-white">{apiKey.name}</h4>
                          <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(apiKey.status)}`}>
                            {apiKey.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-500 dark:text-gray-400 font-mono">
                          {apiKey.isVisible ? apiKey.key : apiKey.key.substring(0, 12) + '••••••••••••••••••••••••••••••••••••••••'}
                        </p>
                        <div className="flex items-center gap-4 mt-2 text-xs text-gray-400">
                          <span>Service: {apiKey.service}</span>
                          <span>Last used: {apiKey.lastUsed}</span>
                          <span>Created: {apiKey.created}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2 ml-4">
                        <button
                          onClick={() => toggleKeyVisibility(apiKey.id)}
                          className="p-2 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
                        >
                          {apiKey.isVisible ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </button>
                        <button className="p-2 text-gray-400 hover:text-blue-600 dark:text-gray-500 dark:hover:text-blue-400">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => deleteApiKey(apiKey.id)}
                          className="p-2 text-gray-400 hover:text-red-600 dark:text-gray-500 dark:hover:text-red-400"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* API Documentation */}
              <div className="mt-8 border-t border-gray-200 dark:border-gray-700 pt-6">
                <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-4">API Documentation</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                  Learn how to integrate with our APIs to automate your workflows and build custom solutions.
                </p>
                <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                  <ExternalLink className="w-4 h-4" />
                  View Documentation
                </button>
              </div>
            </div>
          )}

          {/* Security Tab */}
          {activeTab === 'security' && (
            <div className="space-y-6">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">Security Settings</h3>

              <div className="space-y-6">
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-white dark:bg-slate-900/50">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white">API Key Encryption</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">All API keys are encrypted using AES-256 encryption</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Lock className="w-4 h-4 text-green-600 dark:text-green-400" />
                      <span className="text-sm text-green-600 dark:text-green-400 font-medium">Enabled</span>
                    </div>
                  </div>
                </div>

                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-white dark:bg-slate-900/50">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white">Vault Integration</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Secure key storage using HashiCorp Vault</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Database className="w-4 h-4 text-green-600 dark:text-green-400" />
                      <span className="text-sm text-green-600 dark:text-green-400 font-medium">Connected</span>
                    </div>
                  </div>
                </div>

                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-white dark:bg-slate-900/50">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white">Access Logging</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">All API key usage is logged and monitored</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <BarChart3 className="w-4 h-4 text-green-600 dark:text-green-400" />
                      <span className="text-sm text-green-600 dark:text-green-400 font-medium">Active</span>
                    </div>
                  </div>
                </div>

                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-white dark:bg-slate-900/50">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white">Key Rotation</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Automatic key rotation for enhanced security</p>
                    </div>
                    <button className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 transition-colors">
                      Configure
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </SettingsLayout>
  );
};

export default IntegrationsPage;
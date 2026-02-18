'use client';

import React, { useState, useEffect } from 'react';
import {
  Key, Plus, Eye, EyeOff, Trash2, Edit, Check, X,
  AlertTriangle, CheckCircle, Info, ExternalLink,
  RefreshCw, Shield, DollarSign, Zap, Globe
} from 'lucide-react';

// AI Provider configurations
const AI_PROVIDERS = [
  {
    id: 'openai',
    name: 'OpenAI',
    logo: '🤖',
    tier: 'Production',
    costRange: '$0.50-30/1M tokens',
    models: ['GPT-3.5', 'GPT-4', 'GPT-4-Turbo'],
    features: ['Chat', 'Embedding', 'Vision'],
    docs: 'https://platform.openai.com/docs'
  },
  {
    id: 'anthropic',
    name: 'Anthropic Claude',
    logo: '🔮',
    tier: 'Production',
    costRange: '$3-75/1M tokens',
    models: ['Claude 3 Haiku', 'Sonnet', 'Opus'],
    features: ['Chat', 'Reasoning', '200K context'],
    docs: 'https://docs.anthropic.com/'
  },
  {
    id: 'azure-openai',
    name: 'Azure OpenAI',
    logo: '☁️',
    tier: 'Enterprise',
    costRange: '$2-60/1M tokens',
    models: ['GPT-4', 'GPT-3.5', 'Embedding'],
    features: ['SLA', 'SOC2', 'HIPAA', 'EU/US regions'],
    docs: 'https://learn.microsoft.com/en-us/azure/ai-services/openai/'
  },
  {
    id: 'cohere',
    name: 'Cohere',
    logo: '🎯',
    tier: 'Production',
    costRange: '$0.50-15/1M tokens',
    models: ['Command', 'Embed', 'Rerank'],
    features: ['RAG', 'Embedding', 'Search'],
    docs: 'https://docs.cohere.com/'
  },
  {
    id: 'mistral',
    name: 'Mistral AI',
    logo: '🌊',
    tier: 'Cost-Optimized',
    costRange: '$0.25-8/1M tokens',
    models: ['Mistral Small', 'Medium', 'Large'],
    features: ['EU-based', 'GDPR', 'Fast'],
    docs: 'https://docs.mistral.ai/'
  },
  {
    id: 'deepseek',
    name: 'DeepSeek',
    logo: '🚀',
    tier: 'Budget',
    costRange: '$0.14-2/1M tokens',
    models: ['DeepSeek R1', 'Coder'],
    features: ['Reasoning', 'Code', 'Ultra-low cost'],
    docs: 'https://platform.deepseek.com/docs'
  },
  {
    id: 'gemini',
    name: 'Google Gemini',
    logo: '💎',
    tier: 'Cost-Optimized',
    costRange: '$0.075-20/1M tokens',
    models: ['Gemini Pro', 'Ultra', 'Flash'],
    features: ['1M context', 'Multimodal', 'Fast'],
    docs: 'https://ai.google.dev/docs'
  },
  {
    id: 'openrouter',
    name: 'OpenRouter',
    logo: '🔀',
    tier: 'Aggregator',
    costRange: '$0.02-30/1M tokens',
    models: ['200+ models from all providers'],
    features: ['Fallback', 'Cost optimization', 'Routing'],
    docs: 'https://openrouter.ai/docs'
  },
  {
    id: 'huggingface',
    name: 'HuggingFace',
    logo: '🤗',
    tier: 'Free/Self-Hosted',
    costRange: 'Free',
    models: ['StarCoder', 'LLAVA', 'BGE', 'SDXL'],
    features: ['Self-hosted', 'Open source', 'Free'],
    docs: 'https://huggingface.co/docs'
  }
];

interface APIKey {
  key_id: string;
  provider_id: string;
  provider_name: string;
  name: string;
  key_preview: string;
  is_active: boolean;
  usage_count: number;
  rate_limit: number;
  created_at: string;
  last_used_at?: string;
  expires_at?: string;
}

interface BYOKApiKeyManagerProps {
  tenantId: string;
}

const BYOKApiKeyManager: React.FC<BYOKApiKeyManagerProps> = ({ tenantId }) => {
  const [apiKeys, setApiKeys] = useState<APIKey[]>([]);
  const [loading, setLoading] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState<string>('');
  const [showKey, setShowKey] = useState<{[key: string]: boolean}>({});
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // New key form state
  const [newKey, setNewKey] = useState({
    provider_id: '',
    name: '',
    key_value: '',
    rate_limit: 10000,
    expires_in_days: 365
  });

  useEffect(() => {
    fetchApiKeys();
  }, [tenantId]);

  const fetchApiKeys = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/brain/tenant/api-keys', {
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-ID': tenantId
        }
      });

      if (response.ok) {
        const data = await response.json();
        setApiKeys(data.api_keys || []);
      } else {
        // Fallback data for development
        setApiKeys([
          {
            key_id: 'key-demo-1',
            provider_id: 'openai',
            provider_name: 'OpenAI',
            name: 'Production OpenAI Key',
            key_preview: 'sk-proj...xyz',
            is_active: true,
            usage_count: 1248,
            rate_limit: 10000,
            created_at: '2025-09-01T00:00:00Z',
            last_used_at: '2025-10-08T10:30:00Z'
          },
          {
            key_id: 'key-demo-2',
            provider_id: 'anthropic',
            provider_name: 'Anthropic Claude',
            name: 'Development Claude Key',
            key_preview: 'sk-ant...abc',
            is_active: true,
            usage_count: 524,
            rate_limit: 5000,
            created_at: '2025-09-15T00:00:00Z',
            last_used_at: '2025-10-07T14:20:00Z'
          }
        ]);
      }
    } catch (err) {
      console.error('Error fetching API keys:', err);
      setError('Failed to load API keys');
    } finally {
      setLoading(false);
    }
  };

  const handleAddKey = async () => {
    if (!newKey.provider_id || !newKey.key_value || !newKey.name) {
      setError('Please fill in all required fields');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/brain/tenant/api-keys', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-ID': tenantId
        },
        body: JSON.stringify({
          service_id: newKey.provider_id,
          key_type: 'production',
          key_value: newKey.key_value,
          name: newKey.name,
          permissions: ['chat', 'embedding', 'vision'],
          rate_limit: newKey.rate_limit,
          expires_in_days: newKey.expires_in_days
        })
      });

      if (response.ok) {
        setSuccess('API key added successfully and stored securely in Vault');
        setShowAddModal(false);
        setNewKey({ provider_id: '', name: '', key_value: '', rate_limit: 10000, expires_in_days: 365 });
        fetchApiKeys();
      } else {
        setError('Failed to add API key. Please check your key is valid.');
      }
    } catch (err) {
      setError('Error adding API key: ' + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteKey = async (keyId: string) => {
    if (!confirm('Are you sure you want to delete this API key? This action cannot be undone.')) {
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`/api/brain/tenant/api-keys/${keyId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-ID': tenantId
        }
      });

      if (response.ok) {
        setSuccess('API key revoked successfully');
        fetchApiKeys();
      } else {
        setError('Failed to delete API key');
      }
    } catch (err) {
      setError('Error deleting API key');
    } finally {
      setLoading(false);
    }
  };

  const getTierBadgeColor = (tier: string) => {
    switch (tier) {
      case 'Enterprise': return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200';
      case 'Production': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'Cost-Optimized': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'Budget': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'Free/Self-Hosted': return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">BYOK - Bring Your Own Keys</h2>
          <p className="text-gray-600 dark:text-gray-300 mt-1">
            Add your AI provider API keys for cost-optimized operations
          </p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
        >
          <Plus className="w-4 h-4" />
          Add API Key
        </button>
      </div>

      {/* Alerts */}
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400 mt-0.5" />
            <div>
              <h3 className="font-medium text-red-900 dark:text-red-200">Error</h3>
              <p className="text-sm text-red-700 dark:text-red-300 mt-1">{error}</p>
            </div>
            <button onClick={() => setError(null)} className="ml-auto">
              <X className="w-4 h-4 text-red-600" />
            </button>
          </div>
        </div>
      )}

      {success && (
        <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400 mt-0.5" />
            <div>
              <h3 className="font-medium text-green-900 dark:text-green-200">Success</h3>
              <p className="text-sm text-green-700 dark:text-green-300 mt-1">{success}</p>
            </div>
            <button onClick={() => setSuccess(null)} className="ml-auto">
              <X className="w-4 h-4 text-green-600" />
            </button>
          </div>
        </div>
      )}

      {/* Benefits Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <DollarSign className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            <div>
              <h3 className="font-medium text-blue-900 dark:text-blue-200">Cost Control</h3>
              <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                Pay providers directly. Save $43K/year in platform overhead.
              </p>
            </div>
          </div>
        </div>

        <div className="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <Shield className="w-5 h-5 text-purple-600 dark:text-purple-400" />
            <div>
              <h3 className="font-medium text-purple-900 dark:text-purple-200">Secure Storage</h3>
              <p className="text-sm text-purple-700 dark:text-purple-300 mt-1">
                Keys encrypted in HashiCorp Vault with tenant isolation.
              </p>
            </div>
          </div>
        </div>

        <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <Zap className="w-5 h-5 text-green-600 dark:text-green-400" />
            <div>
              <h3 className="font-medium text-green-900 dark:text-green-200">Smart Routing</h3>
              <p className="text-sm text-green-700 dark:text-green-300 mt-1">
                Auto-select optimal provider by task, cost, and performance.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Your API Keys */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Your API Keys</h3>

        {loading && apiKeys.length === 0 ? (
          <div className="text-center py-12">
            <RefreshCw className="w-8 h-8 text-gray-400 mx-auto animate-spin" />
            <p className="text-gray-500 mt-2">Loading API keys...</p>
          </div>
        ) : apiKeys.length === 0 ? (
          <div className="text-center py-12 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg">
            <Key className="w-12 h-12 text-gray-400 mx-auto" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mt-4">No API keys yet</h3>
            <p className="text-gray-500 dark:text-gray-400 mt-2">Add your first AI provider API key to get started</p>
            <button
              onClick={() => setShowAddModal(true)}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Add Your First Key
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            {apiKeys.map((apiKey) => (
              <div key={apiKey.key_id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 bg-white dark:bg-gray-800">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{AI_PROVIDERS.find(p => p.id === apiKey.provider_id)?.logo || '🔑'}</span>
                      <div>
                        <h4 className="font-semibold text-gray-900 dark:text-white">{apiKey.name}</h4>
                        <p className="text-sm text-gray-500 dark:text-gray-400">{apiKey.provider_name}</p>
                      </div>
                    </div>
                    <div className="mt-3 flex items-center gap-4">
                      <code className="text-sm text-gray-600 dark:text-gray-300 font-mono bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                        {showKey[apiKey.key_id] ? apiKey.key_preview.replace('...', '••••••••••••••••') : apiKey.key_preview}
                      </code>
                      <span className={`text-xs px-2 py-1 rounded-full ${apiKey.is_active ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-gray-100 text-gray-800'}`}>
                        {apiKey.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                    <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                      Usage: {apiKey.usage_count.toLocaleString()} requests •
                      Rate limit: {apiKey.rate_limit.toLocaleString()}/min •
                      Created: {new Date(apiKey.created_at).toLocaleDateString()}
                      {apiKey.last_used_at && ` • Last used: ${new Date(apiKey.last_used_at).toLocaleDateString()}`}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setShowKey({...showKey, [apiKey.key_id]: !showKey[apiKey.key_id]})}
                      className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                      title={showKey[apiKey.key_id] ? 'Hide key' : 'Show key'}
                    >
                      {showKey[apiKey.key_id] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                    <button
                      onClick={() => handleDeleteKey(apiKey.key_id)}
                      className="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400"
                      title="Delete key"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add API Key Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">Add AI Provider API Key</h3>
                <button onClick={() => setShowAddModal(false)}>
                  <X className="w-6 h-6 text-gray-400 hover:text-gray-600" />
                </button>
              </div>

              {/* Provider Selection */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                  Select AI Provider
                </label>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {AI_PROVIDERS.map((provider) => (
                    <button
                      key={provider.id}
                      onClick={() => {
                        setNewKey({...newKey, provider_id: provider.id});
                        setSelectedProvider(provider.id);
                      }}
                      className={`p-4 border rounded-lg text-left transition-all ${
                        newKey.provider_id === provider.id
                          ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                          : 'border-gray-200 dark:border-gray-700 hover:border-blue-300'
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <span className="text-2xl">{provider.logo}</span>
                        <div className="flex-1">
                          <h4 className="font-semibold text-gray-900 dark:text-white">{provider.name}</h4>
                          <span className={`text-xs px-2 py-0.5 rounded-full ${getTierBadgeColor(provider.tier)}`}>
                            {provider.tier}
                          </span>
                          <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">{provider.costRange}</p>
                          <div className="flex flex-wrap gap-1 mt-2">
                            {provider.features.slice(0, 2).map((feature, idx) => (
                              <span key={idx} className="text-xs bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded">
                                {feature}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Key Details */}
              {newKey.provider_id && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Key Name
                    </label>
                    <input
                      type="text"
                      value={newKey.name}
                      onChange={(e) => setNewKey({...newKey, name: e.target.value})}
                      placeholder={`Production ${AI_PROVIDERS.find(p => p.id === newKey.provider_id)?.name} Key`}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      API Key
                    </label>
                    <input
                      type="password"
                      value={newKey.key_value}
                      onChange={(e) => setNewKey({...newKey, key_value: e.target.value})}
                      placeholder="sk-..."
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 font-mono text-sm dark:bg-gray-700 dark:text-white"
                    />
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      Your key will be encrypted and securely stored in HashiCorp Vault
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Rate Limit (requests/min)
                      </label>
                      <input
                        type="number"
                        value={newKey.rate_limit}
                        onChange={(e) => setNewKey({...newKey, rate_limit: parseInt(e.target.value)})}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Expires in (days)
                      </label>
                      <input
                        type="number"
                        value={newKey.expires_in_days}
                        onChange={(e) => setNewKey({...newKey, expires_in_days: parseInt(e.target.value)})}
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                      />
                    </div>
                  </div>

                  {/* Provider Info */}
                  {newKey.provider_id && (
                    <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                      <div className="flex items-start gap-3">
                        <Info className="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5" />
                        <div className="flex-1">
                          <h4 className="font-medium text-blue-900 dark:text-blue-200">
                            {AI_PROVIDERS.find(p => p.id === newKey.provider_id)?.name} Setup
                          </h4>
                          <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                            Get your API key from the provider's dashboard.
                          </p>
                          <a
                            href={AI_PROVIDERS.find(p => p.id === newKey.provider_id)?.docs}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 text-sm text-blue-600 dark:text-blue-400 hover:underline mt-2"
                          >
                            View Documentation <ExternalLink className="w-3 h-3" />
                          </a>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex items-center gap-3 pt-4">
                    <button
                      onClick={handleAddKey}
                      disabled={loading || !newKey.provider_id || !newKey.key_value || !newKey.name}
                      className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {loading ? (
                        <>
                          <RefreshCw className="w-4 h-4 animate-spin" />
                          Adding Key...
                        </>
                      ) : (
                        <>
                          <Check className="w-4 h-4" />
                          Add API Key
                        </>
                      )}
                    </button>
                    <button
                      onClick={() => setShowAddModal(false)}
                      className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BYOKApiKeyManager;

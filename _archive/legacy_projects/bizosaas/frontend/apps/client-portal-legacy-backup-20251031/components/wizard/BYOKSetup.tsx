'use client';

import React, { useState } from 'react';
import {
  Key, DollarSign, Shield, Zap, CheckCircle,
  AlertTriangle, Info, ExternalLink, Eye, EyeOff,
  ArrowRight, SkipForward
} from 'lucide-react';

interface BYOKSetupProps {
  onComplete: (apiKeys: APIKeyData[]) => void;
  onSkip?: () => void;
  tenantId: string;
}

interface APIKeyData {
  provider_id: string;
  name: string;
  key_value: string;
  budget_tier: string;
}

const AI_PROVIDERS_QUICK = [
  {
    id: 'openai',
    name: 'OpenAI',
    logo: '🤖',
    tier: 'Production',
    costRange: '$0.50-30/1M',
    recommended: true,
    setupUrl: 'https://platform.openai.com/api-keys',
    description: 'Best for general-purpose AI tasks, chat, and embeddings'
  },
  {
    id: 'anthropic',
    name: 'Anthropic Claude',
    logo: '🔮',
    tier: 'Production',
    costRange: '$3-75/1M',
    recommended: true,
    setupUrl: 'https://console.anthropic.com/settings/keys',
    description: 'Excellent for reasoning, long context, and complex tasks'
  },
  {
    id: 'deepseek',
    name: 'DeepSeek',
    logo: '🚀',
    tier: 'Budget',
    costRange: '$0.14-2/1M',
    recommended: true,
    setupUrl: 'https://platform.deepseek.com/api_keys',
    description: 'Ultra-low cost option for high-volume operations'
  },
  {
    id: 'gemini',
    name: 'Google Gemini',
    logo: '💎',
    tier: 'Cost-Optimized',
    costRange: '$0.075-20/1M',
    recommended: false,
    setupUrl: 'https://makersuite.google.com/app/apikey',
    description: 'Multimodal with 1M context window'
  },
  {
    id: 'openrouter',
    name: 'OpenRouter',
    logo: '🔀',
    tier: 'Aggregator',
    costRange: '$0.02-30/1M',
    recommended: false,
    setupUrl: 'https://openrouter.ai/keys',
    description: 'Access 200+ models with automatic fallback'
  }
];

const BUDGET_TIERS = [
  { id: 'LOW', name: 'Budget', cost: '$50-200/month', icon: '💰', providers: ['deepseek', 'gemini'] },
  { id: 'MEDIUM', name: 'Balanced', cost: '$200-500/month', icon: '⚖️', providers: ['openai', 'gemini', 'openrouter'] },
  { id: 'HIGH', name: 'Performance', cost: '$500-2000/month', icon: '🚀', providers: ['openai', 'anthropic'] },
  { id: 'UNLIMITED', name: 'Enterprise', cost: '$2000+/month', icon: '👑', providers: ['anthropic', 'azure-openai'] }
];

export function BYOKSetup({ onComplete, onSkip, tenantId }: BYOKSetupProps) {
  const [step, setStep] = useState<'intro' | 'budget' | 'providers' | 'keys'>('intro');
  const [selectedBudget, setSelectedBudget] = useState<string>('MEDIUM');
  const [selectedProviders, setSelectedProviders] = useState<string[]>([]);
  const [apiKeys, setApiKeys] = useState<{[key: string]: {name: string, key: string, show: boolean}}>({});
  const [skipBYOK, setSkipBYOK] = useState(false);

  const handleProviderToggle = (providerId: string) => {
    if (selectedProviders.includes(providerId)) {
      setSelectedProviders(selectedProviders.filter(p => p !== providerId));
      const newKeys = {...apiKeys};
      delete newKeys[providerId];
      setApiKeys(newKeys);
    } else {
      setSelectedProviders([...selectedProviders, providerId]);
    }
  };

  const handleKeyChange = (providerId: string, field: 'name' | 'key', value: string) => {
    setApiKeys({
      ...apiKeys,
      [providerId]: {
        ...apiKeys[providerId],
        [field]: value,
        show: apiKeys[providerId]?.show || false
      }
    });
  };

  const handleComplete = () => {
    if (skipBYOK) {
      onComplete([]);
      return;
    }

    const keys: APIKeyData[] = selectedProviders
      .filter(p => apiKeys[p]?.key)
      .map(p => ({
        provider_id: p,
        name: apiKeys[p].name || `${AI_PROVIDERS_QUICK.find(pr => pr.id === p)?.name} Key`,
        key_value: apiKeys[p].key,
        budget_tier: selectedBudget
      }));

    onComplete(keys);
  };

  // Step 1: Introduction
  if (step === 'intro') {
    return (
      <div className="max-w-4xl mx-auto p-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-blue-100 dark:bg-blue-900 rounded-full mb-4">
            <Key className="w-10 h-10 text-blue-600 dark:text-blue-400" />
          </div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Bring Your Own Keys (BYOK)
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Use your own AI provider API keys for maximum cost control and flexibility
          </p>
        </div>

        {/* Benefits */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 border border-blue-200 dark:border-blue-700 rounded-xl p-6">
            <DollarSign className="w-8 h-8 text-blue-600 dark:text-blue-400 mb-3" />
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Cost Control</h3>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Pay providers directly at wholesale rates. Save up to $43,200/year compared to platform markup.
            </p>
          </div>

          <div className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/30 dark:to-purple-800/30 border border-purple-200 dark:border-purple-700 rounded-xl p-6">
            <Shield className="w-8 h-8 text-purple-600 dark:text-purple-400 mb-3" />
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Secure Storage</h3>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Keys encrypted with 256-bit AES and stored in HashiCorp Vault with tenant isolation.
            </p>
          </div>

          <div className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/30 dark:to-green-800/30 border border-green-200 dark:border-green-700 rounded-xl p-6">
            <Zap className="w-8 h-8 text-green-600 dark:text-green-400 mb-3" />
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Smart Routing</h3>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              AI automatically selects the best provider based on task type, cost, and performance.
            </p>
          </div>
        </div>

        {/* CTA Buttons */}
        <div className="flex items-center gap-4">
          <button
            onClick={() => setStep('budget')}
            className="flex-1 flex items-center justify-center gap-2 px-6 py-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 font-semibold"
          >
            Set Up BYOK
            <ArrowRight className="w-5 h-5" />
          </button>
          {onSkip && (
            <button
              onClick={() => {
                setSkipBYOK(true);
                handleComplete();
              }}
              className="px-6 py-4 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 font-semibold"
            >
              <SkipForward className="w-5 h-5 inline mr-2" />
              Skip for Now
            </button>
          )}
        </div>

        <p className="text-sm text-gray-500 dark:text-gray-400 text-center mt-4">
          You can always add API keys later in Settings
        </p>
      </div>
    );
  }

  // Step 2: Budget Selection
  if (step === 'budget') {
    return (
      <div className="max-w-4xl mx-auto p-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Choose Your Budget Tier
        </h2>
        <p className="text-gray-600 dark:text-gray-300 mb-8">
          Select your expected monthly AI usage budget. This helps us recommend the best providers.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          {BUDGET_TIERS.map((tier) => (
            <button
              key={tier.id}
              onClick={() => setSelectedBudget(tier.id)}
              className={`p-6 border-2 rounded-xl text-left transition-all ${
                selectedBudget === tier.id
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                  : 'border-gray-200 dark:border-gray-700 hover:border-blue-300'
              }`}
            >
              <div className="flex items-start justify-between mb-3">
                <span className="text-3xl">{tier.icon}</span>
                {selectedBudget === tier.id && (
                  <CheckCircle className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                )}
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-1">
                {tier.name}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                {tier.cost}
              </p>
              <div className="flex flex-wrap gap-1">
                {tier.providers.map((p) => (
                  <span key={p} className="text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                    {AI_PROVIDERS_QUICK.find(pr => pr.id === p)?.name}
                  </span>
                ))}
              </div>
            </button>
          ))}
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={() => setStep('intro')}
            className="px-6 py-3 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800"
          >
            Back
          </button>
          <button
            onClick={() => setStep('providers')}
            className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
          >
            Continue to Provider Selection
          </button>
        </div>
      </div>
    );
  }

  // Step 3: Provider Selection
  if (step === 'providers') {
    const recommendedProviders = BUDGET_TIERS.find(t => t.id === selectedBudget)?.providers || [];

    return (
      <div className="max-w-4xl mx-auto p-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Select AI Providers
        </h2>
        <p className="text-gray-600 dark:text-gray-300 mb-8">
          Choose which AI providers you'd like to use. We recommend starting with 1-2 providers.
        </p>

        <div className="space-y-3 mb-8">
          {AI_PROVIDERS_QUICK.map((provider) => {
            const isRecommended = recommendedProviders.includes(provider.id);
            const isSelected = selectedProviders.includes(provider.id);

            return (
              <button
                key={provider.id}
                onClick={() => handleProviderToggle(provider.id)}
                className={`w-full p-5 border-2 rounded-xl text-left transition-all ${
                  isSelected
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-gray-200 dark:border-gray-700 hover:border-blue-300'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-4 flex-1">
                    <span className="text-3xl">{provider.logo}</span>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                          {provider.name}
                        </h3>
                        {isRecommended && (
                          <span className="text-xs bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-2 py-0.5 rounded-full">
                            Recommended
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        {provider.description}
                      </p>
                      <div className="flex items-center gap-3 text-xs text-gray-500 dark:text-gray-400">
                        <span className="font-semibold">{provider.costRange}</span>
                        <span>•</span>
                        <span>{provider.tier}</span>
                      </div>
                    </div>
                  </div>
                  {isSelected && (
                    <CheckCircle className="w-6 h-6 text-blue-600 dark:text-blue-400 flex-shrink-0" />
                  )}
                </div>
              </button>
            );
          })}
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={() => setStep('budget')}
            className="px-6 py-3 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800"
          >
            Back
          </button>
          <button
            onClick={() => setStep('keys')}
            disabled={selectedProviders.length === 0}
            className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Continue to API Keys ({selectedProviders.length})
          </button>
        </div>
      </div>
    );
  }

  // Step 4: API Key Entry
  return (
    <div className="max-w-4xl mx-auto p-8">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        Add Your API Keys
      </h2>
      <p className="text-gray-600 dark:text-gray-300 mb-8">
        Enter your API keys for the selected providers. Keys are encrypted and stored securely.
      </p>

      {/* Security Notice */}
      <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 mb-6">
        <div className="flex items-start gap-3">
          <Shield className="w-5 h-5 text-yellow-600 dark:text-yellow-400 mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="font-medium text-yellow-900 dark:text-yellow-200">Secure Storage</h4>
            <p className="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
              Your API keys are encrypted with 256-bit AES and stored in HashiCorp Vault.
              Only you can access them.
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-6 mb-8">
        {selectedProviders.map((providerId) => {
          const provider = AI_PROVIDERS_QUICK.find(p => p.id === providerId)!;
          const keyData = apiKeys[providerId] || {name: '', key: '', show: false};

          return (
            <div key={providerId} className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
              <div className="flex items-start gap-4 mb-4">
                <span className="text-3xl">{provider.logo}</span>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {provider.name}
                  </h3>
                  <a
                    href={provider.setupUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-sm text-blue-600 dark:text-blue-400 hover:underline"
                  >
                    Get API Key <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Key Name (Optional)
                  </label>
                  <input
                    type="text"
                    value={keyData.name}
                    onChange={(e) => handleKeyChange(providerId, 'name', e.target.value)}
                    placeholder={`Production ${provider.name} Key`}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    API Key *
                  </label>
                  <div className="relative">
                    <input
                      type={keyData.show ? 'text' : 'password'}
                      value={keyData.key}
                      onChange={(e) => handleKeyChange(providerId, 'key', e.target.value)}
                      placeholder="sk-..."
                      className="w-full px-4 py-2 pr-12 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 font-mono text-sm dark:bg-gray-800 dark:text-white"
                    />
                    <button
                      type="button"
                      onClick={() => handleKeyChange(providerId, 'show' as any, !keyData.show as any)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                    >
                      {keyData.show ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="flex items-center gap-4">
        <button
          onClick={() => setStep('providers')}
          className="px-6 py-3 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800"
        >
          Back
        </button>
        <button
          onClick={handleComplete}
          className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 font-semibold"
        >
          Complete BYOK Setup
        </button>
      </div>
    </div>
  );
}

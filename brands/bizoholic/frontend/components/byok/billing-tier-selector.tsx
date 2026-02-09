/**
 * BYOK Billing Tier Selector Component
 * Displays billing tier comparison and cost estimation
 */

'use client';

import { useState, useEffect } from 'react';
import { 
  Check, 
  DollarSign, 
  TrendingUp, 
  Calculator, 
  Shield,
  Key,
  Zap,
  Bot
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { useBillingEstimation } from '@/hooks/use-byok';
import { CREDENTIAL_STRATEGIES } from '@/lib/api/byok-api';

interface BillingTierSelectorProps {
  currentStrategy?: string;
  onStrategySelect?: (strategy: string) => void;
  showEstimation?: boolean;
  className?: string;
}

const strategyIcons = {
  bring_your_own_key: Key,
  platform_managed: Shield,
  hybrid_mode: Zap,
  auto_resolve: Bot,
};

const strategyColors = {
  bring_your_own_key: 'bg-blue-50 border-blue-200',
  platform_managed: 'bg-purple-50 border-purple-200',
  hybrid_mode: 'bg-green-50 border-green-200',
  auto_resolve: 'bg-yellow-50 border-yellow-200',
};

export function BillingTierSelector({
  currentStrategy,
  onStrategySelect,
  showEstimation = true,
  className
}: BillingTierSelectorProps) {
  const { tierComparison, estimates, loading, estimateCostChange } = useBillingEstimation();
  const [selectedStrategy, setSelectedStrategy] = useState<string>(currentStrategy || 'bring_your_own_key');

  useEffect(() => {
    if (currentStrategy) {
      setSelectedStrategy(currentStrategy);
    }
  }, [currentStrategy]);

  const handleStrategyChange = async (strategy: string) => {
    setSelectedStrategy(strategy);
    
    if (showEstimation && strategy !== currentStrategy) {
      await estimateCostChange(strategy);
    }
    
    if (onStrategySelect) {
      onStrategySelect(strategy);
    }
  };

  if (loading.comparison || !tierComparison) {
    return (
      <Card className={className}>
        <CardContent className="flex items-center justify-center p-6">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-900"></div>
          <span className="ml-2">Loading billing tiers...</span>
        </CardContent>
      </Card>
    );
  }

  const getTierByStrategy = (strategy: string) => {
    const strategyToBilling = {
      'bring_your_own_key': 'byok_discounted',
      'platform_managed': 'full_service',
      'hybrid_mode': 'pay_per_use',
      'auto_resolve': 'pay_per_use'
    };
    
    return tierComparison[strategyToBilling[strategy as keyof typeof strategyToBilling]];
  };

  return (
    <div className={className}>
      {/* Strategy Selection Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {Object.entries(CREDENTIAL_STRATEGIES).map(([strategyKey, strategyInfo]) => {
          const tier = getTierByStrategy(strategyKey);
          const IconComponent = strategyIcons[strategyKey as keyof typeof strategyIcons];
          const isSelected = selectedStrategy === strategyKey;
          const isCurrentStrategy = currentStrategy === strategyKey;
          
          return (
            <Card 
              key={strategyKey}
              className={`cursor-pointer transition-all hover:shadow-lg ${
                isSelected ? 'ring-2 ring-primary' : ''
              } ${strategyColors[strategyKey as keyof typeof strategyColors]}`}
              onClick={() => handleStrategyChange(strategyKey)}
            >
              <CardHeader className="pb-3">
                <CardTitle className="flex items-center gap-2 text-sm">
                  <IconComponent className="h-4 w-4" />
                  {strategyInfo.name}
                  {isCurrentStrategy && (
                    <Badge variant="secondary" className="text-xs">Current</Badge>
                  )}
                </CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold">
                    ${tier?.monthly_base_fee || 0}
                  </span>
                  <span className="text-sm text-muted-foreground">/month</span>
                </div>
                
                <p className="text-sm text-muted-foreground">
                  {strategyInfo.description}
                </p>
                
                <div className="text-xs space-y-1">
                  <p className="font-medium text-green-600">✓ Benefits:</p>
                  <ul className="space-y-0.5">
                    {strategyInfo.benefits.slice(0, 2).map((benefit, index) => (
                      <li key={index} className="text-muted-foreground">• {benefit}</li>
                    ))}
                  </ul>
                </div>
                
                <p className="text-xs text-muted-foreground font-medium">
                  {tier?.best_for || 'General purpose'}
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Cost Estimation */}
      {showEstimation && estimates[selectedStrategy] && selectedStrategy !== currentStrategy && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calculator className="h-5 w-5" />
              Cost Impact Analysis
            </CardTitle>
          </CardHeader>
          
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">
                  ${estimates[selectedStrategy].current_monthly_cost.toFixed(0)}
                </div>
                <div className="text-sm text-blue-700">Current Cost</div>
                <div className="text-xs text-muted-foreground">
                  {estimates[selectedStrategy].current_strategy.replace('_', ' ')}
                </div>
              </div>
              
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">
                  ${estimates[selectedStrategy].proposed_monthly_cost.toFixed(0)}
                </div>
                <div className="text-sm text-green-700">Proposed Cost</div>
                <div className="text-xs text-muted-foreground">
                  {estimates[selectedStrategy].proposed_strategy.replace('_', ' ')}
                </div>
              </div>
              
              <div className={`text-center p-4 rounded-lg ${
                estimates[selectedStrategy].monthly_savings > 0 
                  ? 'bg-emerald-50' 
                  : 'bg-red-50'
              }`}>
                <div className={`text-2xl font-bold ${
                  estimates[selectedStrategy].monthly_savings > 0 
                    ? 'text-emerald-600' 
                    : 'text-red-600'
                }`}>
                  {estimates[selectedStrategy].monthly_savings > 0 ? '+' : ''}
                  ${estimates[selectedStrategy].monthly_savings.toFixed(0)}
                </div>
                <div className={`text-sm ${
                  estimates[selectedStrategy].monthly_savings > 0 
                    ? 'text-emerald-700' 
                    : 'text-red-700'
                }`}>
                  Monthly {estimates[selectedStrategy].monthly_savings > 0 ? 'Savings' : 'Increase'}
                </div>
                <div className="text-xs text-muted-foreground">
                  {estimates[selectedStrategy].savings_percentage.toFixed(1)}% change
                </div>
              </div>
            </div>
            
            <Alert className="mt-4">
              <TrendingUp className="h-4 w-4" />
              <AlertDescription>
                <strong>Annual Impact:</strong> {' '}
                {estimates[selectedStrategy].annual_savings > 0 ? 'Save' : 'Additional cost of'} {' '}
                ${Math.abs(estimates[selectedStrategy].annual_savings).toFixed(0)} per year. {' '}
                <strong>Recommendation:</strong> {' '}
                {estimates[selectedStrategy].recommendation === 'switch' ? 
                  `✅ Switch to ${selectedStrategy.replace('_', ' ')} strategy` :
                  `⏸️ Stay with current ${currentStrategy?.replace('_', ' ')} strategy`
                }
              </AlertDescription>
            </Alert>
          </CardContent>
        </Card>
      )}

      {/* Detailed Tier Comparison */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <DollarSign className="h-5 w-5" />
            Detailed Pricing Comparison
          </CardTitle>
        </CardHeader>
        
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left p-2">Feature</th>
                  <th className="text-center p-2">BYOK</th>
                  <th className="text-center p-2">Platform</th>
                  <th className="text-center p-2">Usage-Based</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b">
                  <td className="p-2 font-medium">Monthly Base Fee</td>
                  <td className="text-center p-2">${tierComparison.byok_discounted?.monthly_base_fee}</td>
                  <td className="text-center p-2">${tierComparison.full_service?.monthly_base_fee}</td>
                  <td className="text-center p-2">${tierComparison.pay_per_use?.monthly_base_fee}</td>
                </tr>
                <tr className="border-b">
                  <td className="p-2 font-medium">API Calls (per 1000)</td>
                  <td className="text-center p-2">${(tierComparison.byok_discounted?.usage_rates?.api_call * 1000).toFixed(2)}</td>
                  <td className="text-center p-2">${(tierComparison.full_service?.usage_rates?.api_call * 1000).toFixed(2)}</td>
                  <td className="text-center p-2">${(tierComparison.pay_per_use?.usage_rates?.api_call * 1000).toFixed(2)}</td>
                </tr>
                <tr className="border-b">
                  <td className="p-2 font-medium">Campaign Execution</td>
                  <td className="text-center p-2">${tierComparison.byok_discounted?.usage_rates?.campaign_execution}</td>
                  <td className="text-center p-2">${tierComparison.full_service?.usage_rates?.campaign_execution}</td>
                  <td className="text-center p-2">${tierComparison.pay_per_use?.usage_rates?.campaign_execution}</td>
                </tr>
                <tr className="border-b">
                  <td className="p-2 font-medium">Free API Calls</td>
                  <td className="text-center p-2">{tierComparison.byok_discounted?.included_quotas?.api_call?.toLocaleString()}</td>
                  <td className="text-center p-2">{tierComparison.full_service?.included_quotas?.api_call?.toLocaleString()}</td>
                  <td className="text-center p-2">{tierComparison.pay_per_use?.included_quotas?.api_call?.toLocaleString()}</td>
                </tr>
                <tr>
                  <td className="p-2 font-medium">Best For</td>
                  <td className="text-center p-2 text-xs">{tierComparison.byok_discounted?.best_for}</td>
                  <td className="text-center p-2 text-xs">{tierComparison.full_service?.best_for}</td>
                  <td className="text-center p-2 text-xs">{tierComparison.pay_per_use?.best_for}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default BillingTierSelector;
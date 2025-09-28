'use client';

import React, { useState } from 'react';
import { useFormContext } from 'react-hook-form';
import { 
  CreditCard, Smartphone, Shield, Settings, Check, 
  AlertTriangle, Eye, EyeOff, TestTube, Globe
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Label } from '../../ui/label';
import { Badge } from '../../ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select-new';
import { Checkbox } from '../../ui/checkbox';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../ui/tabs';

import { StoreSetupData } from '../types';
import { PAYMENT_GATEWAYS, DIGITAL_WALLETS } from '../constants';

interface PaymentGatewaysStepProps {
  data: StoreSetupData['paymentGateways'];
  onChange: (data: Partial<StoreSetupData['paymentGateways']>) => void;
  readonly?: boolean;
}

export function PaymentGatewaysStep({ data, onChange, readonly = false }: PaymentGatewaysStepProps) {
  const { register, formState: { errors } } = useFormContext();
  const [selectedGateway, setSelectedGateway] = useState<string>('');
  const [showSecrets, setShowSecrets] = useState<{ [key: string]: boolean }>({});
  const [testResults, setTestResults] = useState<{ [key: string]: 'success' | 'error' | 'testing' | null }>({});

  // Toggle gateway enabled/disabled
  const toggleGateway = (gatewayId: string) => {
    const enabled = data.enabled.includes(gatewayId)
      ? data.enabled.filter(id => id !== gatewayId)
      : [...data.enabled, gatewayId];

    onChange({ ...data, enabled });

    // If disabling the primary gateway, clear it
    if (!enabled.includes(data.primary)) {
      onChange({ ...data, enabled, primary: enabled[0] || '' });
    }
  };

  // Set primary gateway
  const setPrimaryGateway = (gatewayId: string) => {
    if (data.enabled.includes(gatewayId)) {
      onChange({ ...data, primary: gatewayId });
    }
  };

  // Update gateway configuration
  const updateGatewayConfig = (gatewayId: string, config: any) => {
    onChange({
      ...data,
      configurations: {
        ...data.configurations,
        [gatewayId]: { ...data.configurations[gatewayId], ...config }
      }
    });
  };

  // Toggle digital wallet
  const toggleDigitalWallet = (walletId: string) => {
    const digitalWallets = data.digitalWallets.includes(walletId)
      ? data.digitalWallets.filter(id => id !== walletId)
      : [...data.digitalWallets, walletId];

    onChange({ ...data, digitalWallets });
  };

  // Test gateway connection
  const testGatewayConnection = async (gatewayId: string) => {
    setTestResults({ ...testResults, [gatewayId]: 'testing' });
    
    try {
      // Simulate API call to test gateway
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock test result (in real implementation, this would call the actual gateway API)
      const success = Math.random() > 0.3; // 70% success rate for demo
      
      setTestResults({ 
        ...testResults, 
        [gatewayId]: success ? 'success' : 'error' 
      });
    } catch (error) {
      setTestResults({ ...testResults, [gatewayId]: 'error' });
    }
  };

  // Toggle secret visibility
  const toggleSecretVisibility = (gatewayId: string, field: string) => {
    const key = `${gatewayId}-${field}`;
    setShowSecrets({ ...showSecrets, [key]: !showSecrets[key] });
  };

  // Calculate total fees
  const calculateFees = (amount: number, gatewayId: string) => {
    const gateway = PAYMENT_GATEWAYS.find(g => g.id === gatewayId);
    if (!gateway) return 0;

    const config = data.configurations[gatewayId];
    const feeStructure = config?.feeStructure || gateway.feeStructure.domestic;
    
    return (amount * feeStructure.percentage / 100) + feeStructure.fixedFee;
  };

  return (
    <div className="space-y-6">
      {/* Payment Gateway Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <CreditCard className="h-5 w-5" />
            <span>Payment Gateway Selection</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {PAYMENT_GATEWAYS.map((gateway) => (
              <div
                key={gateway.id}
                className={`relative p-4 border-2 rounded-lg cursor-pointer transition-all ${
                  data.enabled.includes(gateway.id)
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => !readonly && toggleGateway(gateway.id)}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <img
                      src={gateway.logo}
                      alt={gateway.name}
                      className="w-8 h-8 object-contain"
                      onError={(e) => {
                        (e.target as HTMLImageElement).src = '/icons/payment-default.svg';
                      }}
                    />
                    <h4 className="font-medium text-gray-900">{gateway.name}</h4>
                  </div>
                  
                  {data.enabled.includes(gateway.id) && (
                    <div className="flex space-x-1">
                      <Check className="h-5 w-5 text-green-600" />
                      {data.primary === gateway.id && (
                        <Badge variant="default" className="text-xs">Primary</Badge>
                      )}
                    </div>
                  )}
                </div>

                <p className="text-sm text-gray-600 mb-3">{gateway.description}</p>

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Domestic Fee:</span>
                    <span className="font-medium">
                      {gateway.feeStructure.domestic.percentage}% + ₹{gateway.feeStructure.domestic.fixedFee}
                    </span>
                  </div>
                  
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">International Fee:</span>
                    <span className="font-medium">
                      {gateway.feeStructure.international.percentage}% + ₹{gateway.feeStructure.international.fixedFee}
                    </span>
                  </div>
                </div>

                <div className="mt-3 flex flex-wrap gap-1">
                  {gateway.features.slice(0, 3).map((feature) => (
                    <Badge key={feature} variant="outline" className="text-xs">
                      {feature}
                    </Badge>
                  ))}
                  {gateway.features.length > 3 && (
                    <Badge variant="outline" className="text-xs">
                      +{gateway.features.length - 3}
                    </Badge>
                  )}
                </div>

                {data.enabled.includes(gateway.id) && !readonly && (
                  <div className="mt-3 pt-3 border-t">
                    <Button
                      type="button"
                      variant={data.primary === gateway.id ? 'default' : 'outline'}
                      size="sm"
                      className="w-full"
                      onClick={(e) => {
                        e.stopPropagation();
                        setPrimaryGateway(gateway.id);
                      }}
                    >
                      {data.primary === gateway.id ? 'Primary Gateway' : 'Set as Primary'}
                    </Button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Gateway Configuration */}
      {data.enabled.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Settings className="h-5 w-5" />
              <span>Gateway Configuration</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs value={selectedGateway || data.enabled[0]} onValueChange={setSelectedGateway}>
              <TabsList className="grid w-full grid-cols-4">
                {data.enabled.slice(0, 4).map((gatewayId) => {
                  const gateway = PAYMENT_GATEWAYS.find(g => g.id === gatewayId);
                  return (
                    <TabsTrigger key={gatewayId} value={gatewayId} className="text-sm">
                      {gateway?.name}
                    </TabsTrigger>
                  );
                })}
              </TabsList>

              {data.enabled.map((gatewayId) => {
                const gateway = PAYMENT_GATEWAYS.find(g => g.id === gatewayId);
                const config = data.configurations[gatewayId] || {
                  apiKey: '',
                  secretKey: '',
                  merchantId: '',
                  testMode: true,
                  feeStructure: gateway?.feeStructure.domestic || { percentage: 2.0, fixedFee: 0 }
                };

                return (
                  <TabsContent key={gatewayId} value={gatewayId} className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h4 className="text-lg font-medium">{gateway?.name} Configuration</h4>
                      <div className="flex items-center space-x-2">
                        <Badge variant={config.testMode ? 'destructive' : 'default'}>
                          {config.testMode ? 'Test Mode' : 'Live Mode'}
                        </Badge>
                        {testResults[gatewayId] && (
                          <Badge 
                            variant={testResults[gatewayId] === 'success' ? 'default' : 'destructive'}
                          >
                            {testResults[gatewayId] === 'success' ? 'Connected' : 'Failed'}
                          </Badge>
                        )}
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {gateway?.setup.requiredFields.map((field) => (
                        <div key={field.name}>
                          <Label htmlFor={field.name}>{field.label} {field.required && '*'}</Label>
                          <div className="relative">
                            <Input
                              id={field.name}
                              type={
                                field.type === 'password' && !showSecrets[`${gatewayId}-${field.name}`]
                                  ? 'password'
                                  : 'text'
                              }
                              placeholder={`Enter ${field.label.toLowerCase()}`}
                              value={config[field.name as keyof typeof config] || ''}
                              onChange={(e) => updateGatewayConfig(gatewayId, {
                                [field.name]: e.target.value
                              })}
                              disabled={readonly}
                              className={field.required && !config[field.name as keyof typeof config] ? 'border-red-300' : ''}
                            />
                            {field.type === 'password' && (
                              <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                className="absolute right-2 top-1/2 transform -translate-y-1/2 h-6 w-6 p-0"
                                onClick={() => toggleSecretVisibility(gatewayId, field.name)}
                              >
                                {showSecrets[`${gatewayId}-${field.name}`] ? (
                                  <EyeOff className="h-4 w-4" />
                                ) : (
                                  <Eye className="h-4 w-4" />
                                )}
                              </Button>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Test Mode Toggle */}
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id={`testMode-${gatewayId}`}
                        checked={config.testMode}
                        onCheckedChange={(checked) => updateGatewayConfig(gatewayId, {
                          testMode: checked
                        })}
                        disabled={readonly}
                      />
                      <Label htmlFor={`testMode-${gatewayId}`} className="flex items-center space-x-2">
                        <TestTube className="h-4 w-4" />
                        <span>Enable Test Mode</span>
                      </Label>
                    </div>

                    {/* Fee Structure */}
                    <div className="border-t pt-4">
                      <h5 className="font-medium mb-3">Fee Structure</h5>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <Label htmlFor={`percentage-${gatewayId}`}>Percentage Fee (%)</Label>
                          <Input
                            id={`percentage-${gatewayId}`}
                            type="number"
                            step="0.01"
                            value={config.feeStructure.percentage}
                            onChange={(e) => updateGatewayConfig(gatewayId, {
                              feeStructure: {
                                ...config.feeStructure,
                                percentage: parseFloat(e.target.value) || 0
                              }
                            })}
                            disabled={readonly}
                          />
                        </div>
                        <div>
                          <Label htmlFor={`fixedFee-${gatewayId}`}>Fixed Fee (₹)</Label>
                          <Input
                            id={`fixedFee-${gatewayId}`}
                            type="number"
                            step="0.01"
                            value={config.feeStructure.fixedFee}
                            onChange={(e) => updateGatewayConfig(gatewayId, {
                              feeStructure: {
                                ...config.feeStructure,
                                fixedFee: parseFloat(e.target.value) || 0
                              }
                            })}
                            disabled={readonly}
                          />
                        </div>
                      </div>
                    </div>

                    {/* Test Connection */}
                    <div className="flex justify-between items-center pt-4 border-t">
                      <div>
                        <p className="text-sm text-gray-600">
                          Test your gateway configuration to ensure it's working correctly.
                        </p>
                      </div>
                      <Button
                        type="button"
                        variant="outline"
                        onClick={() => testGatewayConnection(gatewayId)}
                        disabled={readonly || testResults[gatewayId] === 'testing'}
                      >
                        {testResults[gatewayId] === 'testing' ? (
                          <>Testing...</>
                        ) : (
                          <>
                            <TestTube className="h-4 w-4 mr-2" />
                            Test Connection
                          </>
                        )}
                      </Button>
                    </div>

                    {/* Fee Calculator */}
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h5 className="font-medium mb-2">Fee Calculator</h5>
                      <div className="flex items-center space-x-4">
                        <div>
                          <Label htmlFor={`amount-${gatewayId}`}>Transaction Amount (₹)</Label>
                          <Input
                            id={`amount-${gatewayId}`}
                            type="number"
                            placeholder="1000"
                            onChange={(e) => {
                              const amount = parseFloat(e.target.value) || 0;
                              const fee = calculateFees(amount, gatewayId);
                              const element = document.getElementById(`fee-${gatewayId}`);
                              if (element) {
                                element.textContent = `Fee: ₹${fee.toFixed(2)}`;
                              }
                            }}
                          />
                        </div>
                        <div className="text-sm">
                          <span id={`fee-${gatewayId}`} className="font-medium text-blue-600">
                            Fee: ₹0.00
                          </span>
                        </div>
                      </div>
                    </div>
                  </TabsContent>
                );
              })}
            </Tabs>
          </CardContent>
        </Card>
      )}

      {/* Digital Wallets */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Smartphone className="h-5 w-5" />
            <span>Digital Wallets</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-600 mb-4">
            Enable popular digital wallets to increase conversion rates in India.
          </p>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {DIGITAL_WALLETS.map((wallet) => (
              <div
                key={wallet.id}
                className={`p-3 border-2 rounded-lg cursor-pointer text-center transition-all ${
                  data.digitalWallets.includes(wallet.id)
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => !readonly && toggleDigitalWallet(wallet.id)}
              >
                <img
                  src={wallet.icon}
                  alt={wallet.name}
                  className="w-8 h-8 mx-auto mb-2"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src = '/icons/wallet-default.svg';
                  }}
                />
                <p className="text-sm font-medium">{wallet.name}</p>
                {data.digitalWallets.includes(wallet.id) && (
                  <Check className="h-4 w-4 text-green-600 mx-auto mt-1" />
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Payment Summary */}
      {data.enabled.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Shield className="h-5 w-5" />
              <span>Payment Configuration Summary</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Enabled Payment Methods</h4>
                  <div className="space-y-2">
                    {data.enabled.map((gatewayId) => {
                      const gateway = PAYMENT_GATEWAYS.find(g => g.id === gatewayId);
                      return (
                        <div key={gatewayId} className="flex items-center justify-between">
                          <span className="text-sm">{gateway?.name}</span>
                          <div className="flex items-center space-x-2">
                            {data.primary === gatewayId && (
                              <Badge variant="default" className="text-xs">Primary</Badge>
                            )}
                            {testResults[gatewayId] === 'success' && (
                              <Check className="h-4 w-4 text-green-600" />
                            )}
                            {testResults[gatewayId] === 'error' && (
                              <AlertTriangle className="h-4 w-4 text-red-600" />
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Digital Wallets</h4>
                  <div className="flex flex-wrap gap-2">
                    {data.digitalWallets.map((walletId) => {
                      const wallet = DIGITAL_WALLETS.find(w => w.id === walletId);
                      return (
                        <Badge key={walletId} variant="outline" className="text-xs">
                          {wallet?.name}
                        </Badge>
                      );
                    })}
                    {data.digitalWallets.length === 0 && (
                      <p className="text-sm text-gray-500">No digital wallets enabled</p>
                    )}
                  </div>
                </div>
              </div>

              {data.primary && (
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h5 className="font-medium text-blue-900 mb-2">Primary Gateway: {PAYMENT_GATEWAYS.find(g => g.id === data.primary)?.name}</h5>
                  <p className="text-sm text-blue-800">
                    This will be the default payment method for your customers. 
                    You can change the primary gateway anytime from the settings.
                  </p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
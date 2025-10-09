/**
 * Credential Input Form Component for BYOK
 * Handles secure API key input with validation and testing
 */

'use client';

import { useState, useCallback } from 'react';
import { Eye, EyeOff, Check, X, Loader2, AlertTriangle, Key } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { SUPPORTED_PLATFORMS } from '@/lib/api/byok-api';
import { useIntegrationManagement } from '@/hooks/use-byok';

interface CredentialFormProps {
  platformId: string;
  existingCredentials?: Record<string, string>;
  integrationId?: string;
  onSuccess?: (integration: any) => void;
  onCancel?: () => void;
  className?: string;
}

export function CredentialForm({
  platformId,
  existingCredentials = {},
  integrationId,
  onSuccess,
  onCancel,
  className
}: CredentialFormProps) {
  const platform = SUPPORTED_PLATFORMS.find(p => p.id === platformId);
  const { createIntegration, updateIntegration, testIntegration, loading } = useIntegrationManagement();
  
  const [credentials, setCredentials] = useState<Record<string, string>>(existingCredentials);
  const [showSecrets, setShowSecrets] = useState<Record<string, boolean>>({});
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});
  const [testResult, setTestResult] = useState<{ success: boolean; error?: string } | null>(null);

  if (!platform) {
    return (
      <Alert>
        <AlertTriangle className="h-4 w-4" />
        <AlertDescription>
          Unsupported platform: {platformId}
        </AlertDescription>
      </Alert>
    );
  }

  const handleInputChange = useCallback((key: string, value: string) => {
    setCredentials(prev => ({ ...prev, [key]: value }));
    
    // Clear validation error when user starts typing
    if (validationErrors[key]) {
      setValidationErrors(prev => ({ ...prev, [key]: '' }));
    }
  }, [validationErrors]);

  const toggleSecretVisibility = useCallback((key: string) => {
    setShowSecrets(prev => ({ ...prev, [key]: !prev[key] }));
  }, []);

  const validateCredentials = useCallback(() => {
    const errors: Record<string, string> = {};
    
    platform.credentials.forEach(cred => {
      if (cred.required && !credentials[cred.key]?.trim()) {
        errors[cred.key] = `${cred.label} is required`;
      }
    });

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  }, [platform.credentials, credentials]);

  const handleTest = useCallback(async () => {
    if (!validateCredentials()) return;

    try {
      setTestResult(null);
      
      // For existing integrations, test directly
      if (integrationId) {
        const result = await testIntegration(integrationId);
        setTestResult(result);
      } else {
        // For new integrations, create and test
        const integration = await createIntegration(platform.id, credentials);
        const result = await testIntegration(integration.id);
        setTestResult(result);
        
        if (result.success && onSuccess) {
          onSuccess(integration);
        }
      }
    } catch (error) {
      setTestResult({ 
        success: false, 
        error: error instanceof Error ? error.message : 'Test failed' 
      });
    }
  }, [validateCredentials, integrationId, testIntegration, platform.id, credentials, createIntegration, onSuccess]);

  const handleSave = useCallback(async () => {
    if (!validateCredentials()) return;

    try {
      if (integrationId) {
        // Update existing integration
        await updateIntegration(integrationId, credentials);
        if (onSuccess) {
          onSuccess({ id: integrationId, credentials });
        }
      } else {
        // Create new integration
        const integration = await createIntegration(platform.id, credentials);
        if (onSuccess) {
          onSuccess(integration);
        }
      }
    } catch (error) {
      console.error('Failed to save integration:', error);
    }
  }, [validateCredentials, integrationId, updateIntegration, credentials, createIntegration, platform.id, onSuccess]);

  const isLoading = loading[platform.id] || loading[integrationId || ''] || loading[`test-${integrationId}`];

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <span className="text-2xl">{platform.icon}</span>
          <div>
            <h3>{platform.name} Integration</h3>
            <p className="text-sm text-muted-foreground font-normal">
              {platform.description}
            </p>
          </div>
        </CardTitle>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Credential Input Fields */}
        <div className="space-y-4">
          {platform.credentials.map((cred) => {
            const isSecret = cred.type === 'password';
            const showValue = !isSecret || showSecrets[cred.key];
            const hasError = !!validationErrors[cred.key];
            
            return (
              <div key={cred.key} className="space-y-2">
                <Label htmlFor={cred.key} className="flex items-center gap-2">
                  {isSecret && <Key className="h-3 w-3" />}
                  {cred.label}
                  {cred.required && <span className="text-red-500">*</span>}
                </Label>
                
                <div className="relative">
                  <Input
                    id={cred.key}
                    type={showValue ? 'text' : 'password'}
                    placeholder={cred.placeholder}
                    value={credentials[cred.key] || ''}
                    onChange={(e) => handleInputChange(cred.key, e.target.value)}
                    className={hasError ? 'border-red-500' : ''}
                    disabled={isLoading}
                  />
                  
                  {isSecret && (
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-full px-3 hover:bg-transparent"
                      onClick={() => toggleSecretVisibility(cred.key)}
                      disabled={isLoading}
                    >
                      {showValue ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </Button>
                  )}
                </div>
                
                {hasError && (
                  <p className="text-sm text-red-500">{validationErrors[cred.key]}</p>
                )}
              </div>
            );
          })}
        </div>

        {/* Test Result Display */}
        {testResult && (
          <Alert className={testResult.success ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50'}>
            <div className="flex items-center gap-2">
              {testResult.success ? (
                <Check className="h-4 w-4 text-green-600" />
              ) : (
                <X className="h-4 w-4 text-red-600" />
              )}
              <AlertDescription className={testResult.success ? 'text-green-800' : 'text-red-800'}>
                {testResult.success 
                  ? `✅ Connection to ${platform.name} successful!`
                  : `❌ Connection failed: ${testResult.error}`
                }
              </AlertDescription>
            </div>
          </Alert>
        )}

        {/* Action Buttons */}
        <div className="flex items-center justify-between">
          <div className="flex gap-2">
            <Button
              onClick={handleTest}
              disabled={isLoading}
              variant="outline"
              className="flex items-center gap-2"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Key className="h-4 w-4" />
              )}
              Test Connection
            </Button>
            
            <Button
              onClick={handleSave}
              disabled={isLoading}
              className="flex items-center gap-2"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Check className="h-4 w-4" />
              )}
              {integrationId ? 'Update' : 'Save'} Integration
            </Button>
          </div>
          
          {onCancel && (
            <Button
              onClick={onCancel}
              variant="ghost"
              disabled={isLoading}
            >
              Cancel
            </Button>
          )}
        </div>

        {/* Security Notice */}
        <Alert>
          <Key className="h-4 w-4" />
          <AlertDescription>
            <strong>Security Notice:</strong> Your API keys are encrypted and stored securely. 
            They are only used to manage your campaigns and are never shared with third parties.
          </AlertDescription>
        </Alert>
      </CardContent>
    </Card>
  );
}

export default CredentialForm;
/**
 * BYOK Strategy Migration Wizard Component
 * Guides users through migrating credential strategies
 */

'use client';

import { useState } from 'react';
import { 
  ArrowRight, 
  ArrowLeft, 
  CheckCircle, 
  AlertTriangle, 
  Loader2,
  Key,
  Shield,
  Zap,
  Bot,
  DollarSign
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { Checkbox } from '@/components/ui/checkbox';
import { useCredentialMigration, useBillingEstimation } from '@/hooks/use-byok';
import { CREDENTIAL_STRATEGIES, SUPPORTED_PLATFORMS } from '@/lib/api/byok-api';

interface MigrationWizardProps {
  currentStrategy: string;
  onComplete?: () => void;
  onCancel?: () => void;
  className?: string;
}

const strategyIcons = {
  bring_your_own_key: Key,
  platform_managed: Shield,
  hybrid_mode: Zap,
  auto_resolve: Bot,
};

export function StrategyMigrationWizard({
  currentStrategy,
  onComplete,
  onCancel,
  className
}: MigrationWizardProps) {
  const [step, setStep] = useState(1);
  const [selectedStrategy, setSelectedStrategy] = useState<string>('');
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [confirmed, setConfirmed] = useState(false);
  
  const { migrateStrategy, migrationResult, loading, error } = useCredentialMigration();
  const { estimateCostChange, estimates } = useBillingEstimation();

  const totalSteps = 4;
  
  const handleStrategySelect = async (strategy: string) => {
    setSelectedStrategy(strategy);
    if (strategy !== currentStrategy) {
      await estimateCostChange(strategy);
    }
  };

  const handlePlatformToggle = (platformId: string) => {
    setSelectedPlatforms(prev => 
      prev.includes(platformId) 
        ? prev.filter(id => id !== platformId)
        : [...prev, platformId]
    );
  };

  const handleMigration = async () => {
    await migrateStrategy(selectedStrategy, selectedPlatforms.length > 0 ? selectedPlatforms : undefined);
  };

  const handleComplete = () => {
    if (onComplete) {
      onComplete();
    }
  };

  const getStepTitle = (stepNumber: number) => {
    switch (stepNumber) {
      case 1: return 'Select New Strategy';
      case 2: return 'Choose Platforms';
      case 3: return 'Review Changes';
      case 4: return 'Migration Complete';
      default: return '';
    }
  };

  const canProceedToStep = (stepNumber: number) => {
    switch (stepNumber) {
      case 2: return selectedStrategy !== '';
      case 3: return selectedPlatforms.length > 0;
      case 4: return confirmed;
      default: return true;
    }
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">Choose Your New Credential Strategy</h3>
              <p className="text-muted-foreground">
                Select how you want to manage your platform API credentials
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(CREDENTIAL_STRATEGIES).map(([strategyKey, strategyInfo]) => {
                if (strategyKey === currentStrategy) return null;
                
                const IconComponent = strategyIcons[strategyKey as keyof typeof strategyIcons];
                const isSelected = selectedStrategy === strategyKey;
                
                return (
                  <Card 
                    key={strategyKey}
                    className={`cursor-pointer transition-all hover:shadow-lg ${
                      isSelected ? 'ring-2 ring-primary bg-primary/5' : ''
                    }`}
                    onClick={() => handleStrategySelect(strategyKey)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-center gap-3 mb-3">
                        <IconComponent className="h-6 w-6" />
                        <h4 className="font-semibold">{strategyInfo.name}</h4>
                      </div>
                      
                      <p className="text-sm text-muted-foreground mb-4">
                        {strategyInfo.description}
                      </p>
                      
                      <div className="space-y-2">
                        <div className="text-xs">
                          <p className="font-medium text-green-600 mb-1">Benefits:</p>
                          <ul className="space-y-0.5">
                            {strategyInfo.benefits.slice(0, 2).map((benefit, index) => (
                              <li key={index} className="text-muted-foreground">• {benefit}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>

            {/* Cost Impact Preview */}
            {selectedStrategy && estimates[selectedStrategy] && (
              <Alert>
                <DollarSign className="h-4 w-4" />
                <AlertDescription>
                  <strong>Cost Impact:</strong> {' '}
                  {estimates[selectedStrategy].monthly_savings > 0 ? 'Save' : 'Additional cost of'} {' '}
                  ${Math.abs(estimates[selectedStrategy].monthly_savings).toFixed(0)}/month {' '}
                  ({estimates[selectedStrategy].savings_percentage.toFixed(1)}% change)
                </AlertDescription>
              </Alert>
            )}
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">Select Platforms to Migrate</h3>
              <p className="text-muted-foreground">
                Choose which platform integrations should use the new credential strategy
              </p>
            </div>

            <div className="space-y-3">
              <div className="flex items-center gap-2 mb-4">
                <Checkbox
                  id="select-all"
                  checked={selectedPlatforms.length === SUPPORTED_PLATFORMS.length}
                  onCheckedChange={(checked) => {
                    if (checked) {
                      setSelectedPlatforms(SUPPORTED_PLATFORMS.map(p => p.id));
                    } else {
                      setSelectedPlatforms([]);
                    }
                  }}
                />
                <label htmlFor="select-all" className="font-medium">
                  Select All Platforms
                </label>
              </div>

              {SUPPORTED_PLATFORMS.map((platform) => (
                <div key={platform.id} className="flex items-center gap-3 p-3 border rounded-lg">
                  <Checkbox
                    id={platform.id}
                    checked={selectedPlatforms.includes(platform.id)}
                    onCheckedChange={() => handlePlatformToggle(platform.id)}
                  />
                  <span className="text-xl">{platform.icon}</span>
                  <div className="flex-1">
                    <label htmlFor={platform.id} className="font-medium cursor-pointer">
                      {platform.name}
                    </label>
                    <p className="text-sm text-muted-foreground">{platform.description}</p>
                  </div>
                </div>
              ))}
            </div>

            {selectedPlatforms.length === 0 && (
              <Alert>
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  Select at least one platform to migrate, or cancel to keep current settings.
                </AlertDescription>
              </Alert>
            )}
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">Review Migration Plan</h3>
              <p className="text-muted-foreground">
                Please review the changes before proceeding with the migration
              </p>
            </div>

            {/* Migration Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Migration Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm font-medium">Current Strategy</p>
                    <p className="text-muted-foreground">
                      {CREDENTIAL_STRATEGIES[currentStrategy as keyof typeof CREDENTIAL_STRATEGIES]?.name}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm font-medium">New Strategy</p>
                    <p className="text-muted-foreground">
                      {CREDENTIAL_STRATEGIES[selectedStrategy as keyof typeof CREDENTIAL_STRATEGIES]?.name}
                    </p>
                  </div>
                </div>

                <div>
                  <p className="text-sm font-medium mb-2">
                    Platforms to Migrate ({selectedPlatforms.length})
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {selectedPlatforms.map(platformId => {
                      const platform = SUPPORTED_PLATFORMS.find(p => p.id === platformId);
                      return (
                        <Badge key={platformId} variant="secondary">
                          {platform?.icon} {platform?.name}
                        </Badge>
                      );
                    })}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Cost Impact */}
            {estimates[selectedStrategy] && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Cost Impact</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="text-center">
                      <p className="text-2xl font-bold">${estimates[selectedStrategy].current_monthly_cost.toFixed(0)}</p>
                      <p className="text-sm text-muted-foreground">Current</p>
                    </div>
                    <div className="text-center">
                      <ArrowRight className="h-8 w-8 mx-auto text-muted-foreground" />
                    </div>
                    <div className="text-center">
                      <p className="text-2xl font-bold">${estimates[selectedStrategy].proposed_monthly_cost.toFixed(0)}</p>
                      <p className="text-sm text-muted-foreground">New</p>
                    </div>
                  </div>
                  
                  <Alert className="mt-4">
                    <DollarSign className="h-4 w-4" />
                    <AlertDescription>
                      {estimates[selectedStrategy].monthly_savings > 0 ? 'You will save' : 'Additional cost of'} {' '}
                      <strong>${Math.abs(estimates[selectedStrategy].monthly_savings).toFixed(0)}</strong> per month
                    </AlertDescription>
                  </Alert>
                </CardContent>
              </Card>
            )}

            {/* Confirmation */}
            <div className="flex items-center gap-2">
              <Checkbox
                id="confirm"
                checked={confirmed}
                onCheckedChange={(checked) => setConfirmed(checked === true)}
              />
              <label htmlFor="confirm" className="text-sm">
                I understand this will change how my platform credentials are managed and may affect my billing.
              </label>
            </div>

            {error && (
              <Alert>
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
          </div>
        );

      case 4:
        return (
          <div className="space-y-6 text-center">
            {migrationResult?.successful_platforms.length === selectedPlatforms.length ? (
              <>
                <CheckCircle className="h-16 w-16 text-green-500 mx-auto" />
                <div>
                  <h3 className="text-lg font-semibold text-green-600 mb-2">
                    Migration Completed Successfully!
                  </h3>
                  <p className="text-muted-foreground">
                    All selected platforms have been migrated to the new credential strategy.
                  </p>
                </div>
              </>
            ) : (
              <>
                <AlertTriangle className="h-16 w-16 text-yellow-500 mx-auto" />
                <div>
                  <h3 className="text-lg font-semibold text-yellow-600 mb-2">
                    Migration Partially Completed
                  </h3>
                  <p className="text-muted-foreground">
                    Some platforms were successfully migrated, but others encountered issues.
                  </p>
                </div>
              </>
            )}

            {migrationResult && (
              <Card>
                <CardContent className="p-4 space-y-3">
                  {migrationResult.successful_platforms.length > 0 && (
                    <div>
                      <p className="font-medium text-green-600 mb-2">✅ Successfully Migrated:</p>
                      <div className="flex flex-wrap gap-2">
                        {migrationResult.successful_platforms.map(platformId => {
                          const platform = SUPPORTED_PLATFORMS.find(p => p.id === platformId);
                          return (
                            <Badge key={platformId} className="bg-green-100 text-green-800">
                              {platform?.icon} {platform?.name}
                            </Badge>
                          );
                        })}
                      </div>
                    </div>
                  )}

                  {migrationResult.failed_platforms.length > 0 && (
                    <div>
                      <p className="font-medium text-red-600 mb-2">❌ Migration Failed:</p>
                      <div className="flex flex-wrap gap-2">
                        {migrationResult.failed_platforms.map(platformId => {
                          const platform = SUPPORTED_PLATFORMS.find(p => p.id === platformId);
                          return (
                            <Badge key={platformId} className="bg-red-100 text-red-800">
                              {platform?.icon} {platform?.name}
                            </Badge>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            <Alert>
              <CheckCircle className="h-4 w-4" />
              <AlertDescription>
                Your credential strategy has been updated. You can view and manage your integrations 
                from the main dashboard.
              </AlertDescription>
            </Alert>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Migrate Credential Strategy</span>
          <Badge variant="outline">
            Step {step} of {totalSteps}
          </Badge>
        </CardTitle>
        <Progress value={(step / totalSteps) * 100} className="h-2" />
      </CardHeader>

      <CardContent className="space-y-6">
        <div className="text-center">
          <h4 className="font-medium">{getStepTitle(step)}</h4>
        </div>

        {renderStep()}

        {/* Navigation Buttons */}
        <div className="flex items-center justify-between">
          <Button
            variant="outline"
            onClick={() => step > 1 ? setStep(step - 1) : onCancel?.()}
            disabled={loading}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            {step === 1 ? 'Cancel' : 'Back'}
          </Button>

          {step < 3 && (
            <Button
              onClick={() => setStep(step + 1)}
              disabled={!canProceedToStep(step + 1) || loading}
            >
              Next
              <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          )}

          {step === 3 && (
            <Button
              onClick={handleMigration}
              disabled={!confirmed || loading}
              className="flex items-center gap-2"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <CheckCircle className="h-4 w-4" />
              )}
              Start Migration
            </Button>
          )}

          {step === 4 && (
            <Button onClick={handleComplete}>
              Complete
              <CheckCircle className="h-4 w-4 ml-2" />
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

export default StrategyMigrationWizard;
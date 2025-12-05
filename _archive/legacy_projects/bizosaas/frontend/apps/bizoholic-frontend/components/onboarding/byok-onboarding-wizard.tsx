/**
 * BYOK Onboarding Wizard Component
 * Guides new tenants through credential strategy selection during initial setup
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
  DollarSign,
  Users,
  Building,
  Target,
  TrendingUp,
  Clock,
  Eye
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

// Import BYOK components and hooks
import BillingTierSelector from '@/components/byok/billing-tier-selector';
import CredentialForm from '@/components/byok/credential-form';
import { useBillingEstimation, useIntegrationManagement } from '@/hooks/use-byok';
import { CREDENTIAL_STRATEGIES, SUPPORTED_PLATFORMS } from '@/lib/api/byok-api';

interface OnboardingData {
  companyName: string;
  industry: string;
  teamSize: string;
  marketingGoals: string[];
  credentialStrategy: string;
  selectedPlatforms: string[];
  monthlyBudget: number;
}

interface OnboardingWizardProps {
  onComplete: (data: OnboardingData) => void;
  onCancel?: () => void;
  className?: string;
}

const strategyIcons = {
  bring_your_own_key: Key,
  platform_managed: Shield,
  hybrid_mode: Zap,
  auto_resolve: Bot,
};

const industries = [
  'Technology & Software',
  'E-commerce & Retail',
  'Healthcare & Medical',
  'Financial Services',
  'Real Estate',
  'Professional Services',
  'Manufacturing',
  'Education',
  'Non-profit',
  'Other'
];

const teamSizes = [
  '1-5 employees',
  '6-20 employees', 
  '21-50 employees',
  '51-200 employees',
  '200+ employees'
];

const marketingGoalOptions = [
  { id: 'brand_awareness', label: 'Brand Awareness', icon: Eye },
  { id: 'lead_generation', label: 'Lead Generation', icon: Target },
  { id: 'customer_acquisition', label: 'Customer Acquisition', icon: Users },
  { id: 'revenue_growth', label: 'Revenue Growth', icon: TrendingUp },
  { id: 'market_expansion', label: 'Market Expansion', icon: Building },
  { id: 'customer_retention', label: 'Customer Retention', icon: Shield }
];

export function BYOKOnboardingWizard({
  onComplete,
  onCancel,
  className
}: OnboardingWizardProps) {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [onboardingData, setOnboardingData] = useState<OnboardingData>({
    companyName: '',
    industry: '',
    teamSize: '',
    marketingGoals: [],
    credentialStrategy: '',
    selectedPlatforms: [],
    monthlyBudget: 5000
  });

  const { estimateCostChange, estimates } = useBillingEstimation();
  const { createIntegration } = useIntegrationManagement();

  const totalSteps = 5;

  const updateOnboardingData = <K extends keyof OnboardingData>(
    key: K, 
    value: OnboardingData[K]
  ) => {
    setOnboardingData(prev => ({ ...prev, [key]: value }));
  };

  const handleStrategySelect = async (strategy: string) => {
    updateOnboardingData('credentialStrategy', strategy);
    if (strategy !== 'bring_your_own_key') {
      await estimateCostChange(strategy);
    }
  };

  const handlePlatformToggle = (platformId: string) => {
    const updatedPlatforms = onboardingData.selectedPlatforms.includes(platformId)
      ? onboardingData.selectedPlatforms.filter(id => id !== platformId)
      : [...onboardingData.selectedPlatforms, platformId];
    
    updateOnboardingData('selectedPlatforms', updatedPlatforms);
  };

  const handleMarketingGoalToggle = (goalId: string) => {
    const updatedGoals = onboardingData.marketingGoals.includes(goalId)
      ? onboardingData.marketingGoals.filter(id => id !== goalId)
      : [...onboardingData.marketingGoals, goalId];
    
    updateOnboardingData('marketingGoals', updatedGoals);
  };

  const handleComplete = async () => {
    setLoading(true);
    try {
      // In a real implementation, this would save the onboarding data
      // and set up the tenant's initial configuration
      await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate API call
      
      if (onComplete) {
        onComplete(onboardingData);
      }
    } catch (error) {
      console.error('Onboarding completion failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const canProceedToStep = (stepNumber: number) => {
    switch (stepNumber) {
      case 2:
        return onboardingData.companyName && onboardingData.industry && onboardingData.teamSize;
      case 3:
        return onboardingData.marketingGoals.length > 0;
      case 4:
        return onboardingData.credentialStrategy !== '';
      case 5:
        return onboardingData.selectedPlatforms.length > 0;
      default:
        return true;
    }
  };

  const getStepTitle = (stepNumber: number) => {
    switch (stepNumber) {
      case 1: return 'Welcome to BizoSaaS!';
      case 2: return 'Tell us about your company';
      case 3: return 'What are your marketing goals?';
      case 4: return 'Choose your credential strategy';
      case 5: return 'Select marketing platforms';
      default: return '';
    }
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-6 text-center">
            <div className="space-y-4">
              <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto">
                <Bot className="h-8 w-8 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold mb-2">Welcome to BizoSaaS!</h2>
                <p className="text-muted-foreground text-lg">
                  The AI-powered marketing automation platform that grows with your business
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 my-8">
              <Card className="p-4">
                <div className="text-center space-y-2">
                  <Target className="h-8 w-8 text-primary mx-auto" />
                  <h3 className="font-semibold">AI-Powered Campaigns</h3>
                  <p className="text-sm text-muted-foreground">
                    Create and optimize campaigns across multiple platforms automatically
                  </p>
                </div>
              </Card>

              <Card className="p-4">
                <div className="text-center space-y-2">
                  <Key className="h-8 w-8 text-primary mx-auto" />
                  <h3 className="font-semibold">Bring Your Own Keys</h3>
                  <p className="text-sm text-muted-foreground">
                    Use your own API keys for maximum control and cost savings
                  </p>
                </div>
              </Card>

              <Card className="p-4">
                <div className="text-center space-y-2">
                  <TrendingUp className="h-8 w-8 text-primary mx-auto" />
                  <h3 className="font-semibold">Real-time Analytics</h3>
                  <p className="text-sm text-muted-foreground">
                    Monitor performance and optimize ROI with advanced insights
                  </p>
                </div>
              </Card>
            </div>

            <p className="text-muted-foreground">
              Let's get you set up in just a few minutes. This wizard will help you configure 
              your account for maximum success.
            </p>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <h3 className="text-lg font-semibold mb-2">Tell us about your company</h3>
              <p className="text-muted-foreground">
                This helps us customize your experience and provide relevant recommendations
              </p>
            </div>

            <div className="space-y-4 max-w-md mx-auto">
              <div>
                <Label htmlFor="company-name">Company Name</Label>
                <Input
                  id="company-name"
                  value={onboardingData.companyName}
                  onChange={(e) => updateOnboardingData('companyName', e.target.value)}
                  placeholder="Enter your company name"
                />
              </div>

              <div>
                <Label htmlFor="industry">Industry</Label>
                <Select value={onboardingData.industry} onValueChange={(value) => updateOnboardingData('industry', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select your industry" />
                  </SelectTrigger>
                  <SelectContent>
                    {industries.map(industry => (
                      <SelectItem key={industry} value={industry}>{industry}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="team-size">Team Size</Label>
                <Select value={onboardingData.teamSize} onValueChange={(value) => updateOnboardingData('teamSize', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select your team size" />
                  </SelectTrigger>
                  <SelectContent>
                    {teamSizes.map(size => (
                      <SelectItem key={size} value={size}>{size}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="monthly-budget">Monthly Marketing Budget (USD)</Label>
                <Input
                  id="monthly-budget"
                  type="number"
                  value={onboardingData.monthlyBudget}
                  onChange={(e) => updateOnboardingData('monthlyBudget', parseInt(e.target.value) || 0)}
                  placeholder="5000"
                  min="100"
                  step="100"
                />
                <p className="text-sm text-muted-foreground mt-1">
                  This helps us recommend the right pricing tier for you
                </p>
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <h3 className="text-lg font-semibold mb-2">What are your marketing goals?</h3>
              <p className="text-muted-foreground">
                Select all that apply. We'll optimize your campaigns for these objectives.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
              {marketingGoalOptions.map(goal => {
                const IconComponent = goal.icon;
                const isSelected = onboardingData.marketingGoals.includes(goal.id);
                
                return (
                  <Card 
                    key={goal.id}
                    className={`cursor-pointer transition-all hover:shadow-md ${
                      isSelected ? 'ring-2 ring-primary bg-primary/5' : ''
                    }`}
                    onClick={() => handleMarketingGoalToggle(goal.id)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-center gap-3">
                        <Checkbox
                          checked={isSelected}
                          onChange={() => {}} // Handled by card click
                        />
                        <IconComponent className="h-5 w-5" />
                        <span className="font-medium">{goal.label}</span>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>

            {onboardingData.marketingGoals.length === 0 && (
              <Alert>
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  Please select at least one marketing goal to continue.
                </AlertDescription>
              </Alert>
            )}
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <h3 className="text-lg font-semibold mb-2">Choose your credential strategy</h3>
              <p className="text-muted-foreground">
                This determines how you'll manage API keys for advertising platforms
              </p>
            </div>

            <BillingTierSelector
              currentStrategy={onboardingData.credentialStrategy}
              onStrategySelect={handleStrategySelect}
              showEstimation={true}
            />

            {onboardingData.credentialStrategy && estimates[onboardingData.credentialStrategy] && (
              <Alert>
                <DollarSign className="h-4 w-4" />
                <AlertDescription>
                  <strong>Estimated monthly cost:</strong> ${estimates[onboardingData.credentialStrategy].proposed_monthly_cost.toFixed(0)}
                  {estimates[onboardingData.credentialStrategy].monthly_savings > 0 && (
                    <span className="text-green-600">
                      {' '}(Save ${estimates[onboardingData.credentialStrategy].monthly_savings.toFixed(0)}/month)
                    </span>
                  )}
                </AlertDescription>
              </Alert>
            )}
          </div>
        );

      case 5:
        return (
          <div className="space-y-6">
            <div className="text-center mb-6">
              <h3 className="text-lg font-semibold mb-2">Select marketing platforms</h3>
              <p className="text-muted-foreground">
                Choose which platforms you want to advertise on. You can add more later.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {SUPPORTED_PLATFORMS.map(platform => {
                const isSelected = onboardingData.selectedPlatforms.includes(platform.id);
                
                return (
                  <Card 
                    key={platform.id}
                    className={`cursor-pointer transition-all hover:shadow-md ${
                      isSelected ? 'ring-2 ring-primary bg-primary/5' : ''
                    }`}
                    onClick={() => handlePlatformToggle(platform.id)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-2">
                          <span className="text-2xl">{platform.icon}</span>
                          <h4 className="font-semibold">{platform.name}</h4>
                        </div>
                        <Checkbox
                          checked={isSelected}
                          onChange={() => {}} // Handled by card click
                        />
                      </div>
                      
                      <p className="text-sm text-muted-foreground mb-3">
                        {platform.description}
                      </p>

                      {(platform as any).popular && (
                        <Badge variant="secondary" className="text-xs">
                          Popular
                        </Badge>
                      )}
                    </CardContent>
                  </Card>
                );
              })}
            </div>

            {onboardingData.selectedPlatforms.length === 0 && (
              <Alert>
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  Please select at least one platform to get started.
                </AlertDescription>
              </Alert>
            )}

            {onboardingData.credentialStrategy === 'bring_your_own_key' && onboardingData.selectedPlatforms.length > 0 && (
              <Alert>
                <Key className="h-4 w-4" />
                <AlertDescription>
                  After completing setup, you'll be guided to add your API keys for the selected platforms.
                </AlertDescription>
              </Alert>
            )}
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
          <span>{getStepTitle(step)}</span>
          <Badge variant="outline">
            Step {step} of {totalSteps}
          </Badge>
        </CardTitle>
        <Progress value={(step / totalSteps) * 100} className="h-2" />
      </CardHeader>

      <CardContent className="space-y-6">
        {renderStep()}

        {/* Navigation Buttons */}
        <div className="flex items-center justify-between pt-6">
          <Button
            variant="outline"
            onClick={() => step > 1 ? setStep(step - 1) : onCancel?.()}
            disabled={loading}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            {step === 1 ? 'Cancel' : 'Back'}
          </Button>

          {step < totalSteps ? (
            <Button
              onClick={() => setStep(step + 1)}
              disabled={!canProceedToStep(step + 1) || loading}
            >
              Next
              <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          ) : (
            <Button
              onClick={handleComplete}
              disabled={!canProceedToStep(step) || loading}
              className="flex items-center gap-2"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <CheckCircle className="h-4 w-4" />
              )}
              Complete Setup
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

export default BYOKOnboardingWizard;
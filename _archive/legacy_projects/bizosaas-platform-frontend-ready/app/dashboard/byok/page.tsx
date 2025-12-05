/**
 * BYOK Management Dashboard Page
 * Main interface for managing Bring Your Own Key configurations
 */

'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { 
  Key, 
  Plus, 
  Settings, 
  TrendingUp, 
  Shield,
  AlertTriangle,
  Zap,
  Activity,
  Heart,
  CheckCircle
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';

// BYOK Components
import HealthDashboard from '@/components/byok/health-dashboard';
import BillingTierSelector from '@/components/byok/billing-tier-selector';
import CredentialForm from '@/components/byok/credential-form';
import StrategyMigrationWizard from '@/components/byok/strategy-migration-wizard';
import { HealthMonitorDashboard } from '@/components/byok/health-monitor-dashboard';

// Hooks
import { useCredentialHealth, useIntegrationManagement } from '@/hooks/use-byok';
import { SUPPORTED_PLATFORMS } from '@/lib/api/byok-api';

export default function BYOKDashboard() {
  const searchParams = useSearchParams();
  const isOnboarding = searchParams?.get('onboarding') === 'true';
  
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedPlatform, setSelectedPlatform] = useState<string | null>(null);
  const [showCredentialForm, setShowCredentialForm] = useState(false);
  const [showMigrationWizard, setShowMigrationWizard] = useState(false);
  const [showOnboardingWelcome, setShowOnboardingWelcome] = useState(isOnboarding);
  
  const { health } = useCredentialHealth();
  const { integrations, fetchIntegrations } = useIntegrationManagement();

  // Mock current strategy - in real implementation, get from tenant settings
  const currentStrategy = 'bring_your_own_key';

  const handleAddIntegration = (platformId: string) => {
    setSelectedPlatform(platformId);
    setShowCredentialForm(true);
  };

  const handleIntegrationSuccess = () => {
    setShowCredentialForm(false);
    setSelectedPlatform(null);
    fetchIntegrations();
  };

  const handleMigrationComplete = () => {
    setShowMigrationWizard(false);
    // Refresh health and integrations
    fetchIntegrations();
  };

  const getIntegrationStatus = (platformId: string) => {
    const integration = integrations.find(i => i.platform_name === platformId);
    const healthStatus = health?.health_statuses.find(h => h.platform === platformId);
    
    if (!integration) return { status: 'not_configured', color: 'gray' };
    if (!healthStatus?.is_healthy) return { status: 'error', color: 'red' };
    return { status: 'healthy', color: 'green' };
  };

  const getStatusBadge = (platformId: string) => {
    const { status, color } = getIntegrationStatus(platformId);
    
    const variants = {
      not_configured: 'secondary',
      error: 'destructive', 
      healthy: 'default'
    };
    
    const labels = {
      not_configured: 'Not Connected',
      error: 'Connection Error',
      healthy: 'Connected'
    };
    
    return (
      <Badge variant={variants[status as keyof typeof variants] as "default" | "destructive" | "outline" | "secondary" | null | undefined}>
        {labels[status as keyof typeof labels]}
      </Badge>
    );
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* Onboarding Welcome Banner */}
      {showOnboardingWelcome && (
        <Alert className="border-green-200 bg-green-50 mb-6">
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertDescription>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-green-800 mb-1">🎉 Welcome to BYOK!</p>
                <p className="text-green-700">
                  You've chosen the Bring Your Own Key strategy. Let's set up your first platform integration to get started.
                </p>
              </div>
              <Button 
                variant="outline" 
                size="sm" 
                onClick={() => setShowOnboardingWelcome(false)}
                className="border-green-300 text-green-700 hover:bg-green-100"
              >
                Got it
              </Button>
            </div>
          </AlertDescription>
        </Alert>
      )}

      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">BYOK Management</h1>
          <p className="text-muted-foreground">
            Manage your Bring Your Own Key configurations and billing preferences
          </p>
        </div>
        
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => setShowMigrationWizard(true)}
            className="flex items-center gap-2"
          >
            <Zap className="h-4 w-4" />
            Change Strategy
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="integrations">Integrations</TabsTrigger>
          <TabsTrigger value="health">
            <Activity className="w-4 h-4 mr-2" />
            Health Monitor
          </TabsTrigger>
          <TabsTrigger value="billing">Billing</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Current Strategy Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  Current Strategy
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <Key className="h-4 w-4" />
                    <span className="font-medium">Bring Your Own Keys</span>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    You manage your own API keys for maximum control and cost savings.
                  </p>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setShowMigrationWizard(true)}
                  >
                    Change Strategy
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Health Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Health Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="text-2xl font-bold">
                    {health?.healthy_count || 0}/{health?.total_integrations || 0}
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Platforms Connected
                  </p>
                  {health && health.healthy_count < health.total_integrations && (
                    <Alert>
                      <AlertTriangle className="h-4 w-4" />
                      <AlertDescription>
                        Some integrations need attention
                      </AlertDescription>
                    </Alert>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Plus className="h-5 w-5" />
                  Quick Actions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <Button 
                    className="w-full justify-start" 
                    variant="outline"
                    onClick={() => setActiveTab('integrations')}
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Add Integration
                  </Button>
                  <Button 
                    className="w-full justify-start" 
                    variant="outline"
                    onClick={() => setActiveTab('billing')}
                  >
                    <TrendingUp className="h-4 w-4 mr-2" />
                    View Billing
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Health Dashboard */}
          <HealthDashboard />
        </TabsContent>

        {/* Integrations Tab */}
        <TabsContent value="integrations" className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">Platform Integrations</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {SUPPORTED_PLATFORMS.map((platform) => {
              const integration = integrations.find(i => i.platform_name === platform.id);
              
              return (
                <Card key={platform.id} className="hover:shadow-lg transition-shadow">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <span className="text-2xl">{platform.icon}</span>
                        <h3 className="font-semibold">{platform.name}</h3>
                      </div>
                      {getStatusBadge(platform.id)}
                    </div>
                    
                    <p className="text-sm text-muted-foreground mb-4">
                      {platform.description}
                    </p>
                    
                    <Button
                      variant={integration ? "outline" : "default"}
                      size="sm"
                      onClick={() => handleAddIntegration(platform.id)}
                      className="w-full"
                    >
                      {integration ? 'Update Keys' : 'Connect Platform'}
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </TabsContent>

        {/* Billing Tab */}
        <TabsContent value="billing" className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">Billing & Pricing</h2>
          </div>

          <BillingTierSelector
            currentStrategy={currentStrategy}
            onStrategySelect={(strategy) => {
              // Handle strategy selection - could trigger migration wizard
              console.log('Strategy selected:', strategy);
            }}
            showEstimation={true}
          />
        </TabsContent>

        {/* Health Monitor Tab */}
        <TabsContent value="health" className="space-y-6">
          <HealthMonitorDashboard />
        </TabsContent>

        {/* Settings Tab */}
        <TabsContent value="settings" className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">BYOK Settings</h2>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="h-5 w-5" />
                General Settings
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Alert>
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  Settings page is under development. Use the other tabs to manage your BYOK configuration.
                </AlertDescription>
              </Alert>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Credential Form Dialog */}
      <Dialog open={showCredentialForm} onOpenChange={setShowCredentialForm}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {selectedPlatform && 
                `Configure ${SUPPORTED_PLATFORMS.find(p => p.id === selectedPlatform)?.name} Integration`
              }
            </DialogTitle>
          </DialogHeader>
          {selectedPlatform && (
            <CredentialForm
              platformId={selectedPlatform}
              existingCredentials={
                integrations.find(i => i.platform_name === selectedPlatform)?.credentials || {}
              }
              integrationId={integrations.find(i => i.platform_name === selectedPlatform)?.id}
              onSuccess={handleIntegrationSuccess}
              onCancel={() => setShowCredentialForm(false)}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Migration Wizard Dialog */}
      <Dialog open={showMigrationWizard} onOpenChange={setShowMigrationWizard}>
        <DialogContent className="max-w-4xl">
          <StrategyMigrationWizard
            currentStrategy={currentStrategy}
            onComplete={handleMigrationComplete}
            onCancel={() => setShowMigrationWizard(false)}
          />
        </DialogContent>
      </Dialog>
    </div>
  );
}
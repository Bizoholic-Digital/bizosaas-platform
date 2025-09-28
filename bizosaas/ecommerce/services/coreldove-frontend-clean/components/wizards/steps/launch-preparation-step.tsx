'use client';

import React, { useState, useEffect } from 'react';
import { useFormContext } from 'react-hook-form';
import { 
  Rocket, Globe, Shield, BarChart, Mail, TestTube,
  CheckCircle, AlertTriangle, Clock, ExternalLink,
  Copy, RefreshCw, Zap, Trophy, Confetti
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Button } from '../../ui/button';
import { Input } from '../../ui/input';
import { Label } from '../../ui/label';
import { Badge } from '../../ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select-new';
import { Checkbox } from '../../ui/checkbox';
import { Progress } from '../../ui/progress';

import { StoreSetupData } from '../types';
import { LAUNCH_CHECKLIST_ITEMS } from '../constants';

interface LaunchPreparationStepProps {
  data: StoreSetupData['launch'];
  onChange: (data: Partial<StoreSetupData['launch']>) => void;
  onComplete?: (data: StoreSetupData) => void;
  readonly?: boolean;
}

export function LaunchPreparationStep({ 
  data, 
  onChange, 
  onComplete, 
  readonly = false 
}: LaunchPreparationStepProps) {
  const { register, formState: { errors } } = useFormContext();
  const [testResults, setTestResults] = useState<{ [key: string]: 'pass' | 'fail' | 'testing' | null }>({});
  const [isLaunching, setIsLaunching] = useState(false);
  const [launchComplete, setLaunchComplete] = useState(false);

  // Auto-generate subdomain from store name
  const generateSubdomain = (storeName: string) => {
    return storeName
      .toLowerCase()
      .replace(/[^a-z0-9]/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '');
  };

  // Update domain configuration
  const updateDomain = (field: keyof StoreSetupData['launch']['domain'], value: any) => {
    onChange({
      ...data,
      domain: { ...data.domain, [field]: value }
    });
  };

  // Update analytics configuration
  const updateAnalytics = (field: keyof StoreSetupData['launch']['analytics'], value: string) => {
    onChange({
      ...data,
      analytics: { ...data.analytics, [field]: value }
    });
  };

  // Update marketing configuration
  const updateMarketing = (field: keyof StoreSetupData['launch']['marketing'], value: boolean) => {
    onChange({
      ...data,
      marketing: { ...data.marketing, [field]: value }
    });
  };

  // Toggle checklist item
  const toggleChecklistItem = (itemId: string) => {
    onChange({
      ...data,
      launchChecklist: {
        ...data.launchChecklist,
        [itemId]: !data.launchChecklist[itemId]
      }
    });
  };

  // Run specific test
  const runTest = async (testType: string) => {
    setTestResults({ ...testResults, [testType]: 'testing' });
    
    // Simulate test execution
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mock test results (in real implementation, these would be actual tests)
    const success = Math.random() > 0.2; // 80% success rate for demo
    
    setTestResults({ 
      ...testResults, 
      [testType]: success ? 'pass' : 'fail' 
    });

    // Auto-check corresponding checklist item on success
    if (success) {
      const checklistMapping: { [key: string]: string } = {
        'domain': 'domain_configured',
        'payment': 'payment_tested',
        'shipping': 'shipping_configured',
        'analytics': 'analytics_setup'
      };
      
      const checklistItem = checklistMapping[testType];
      if (checklistItem) {
        onChange({
          ...data,
          launchChecklist: {
            ...data.launchChecklist,
            [checklistItem]: true
          }
        });
      }
    }
  };

  // Run all tests
  const runAllTests = async () => {
    const tests = ['domain', 'payment', 'shipping', 'analytics'];
    for (const test of tests) {
      await runTest(test);
    }
  };

  // Calculate completion percentage
  const completionPercentage = () => {
    const completed = Object.values(data.launchChecklist).filter(Boolean).length;
    const total = LAUNCH_CHECKLIST_ITEMS.length;
    return (completed / total) * 100;
  };

  // Check if ready to launch
  const isReadyToLaunch = () => {
    const criticalItems = LAUNCH_CHECKLIST_ITEMS.filter(item => item.critical);
    return criticalItems.every(item => data.launchChecklist[item.id]);
  };

  // Launch store
  const launchStore = async () => {
    setIsLaunching(true);
    
    try {
      // Simulate launch process
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      onChange({ ...data, isLive: true });
      setLaunchComplete(true);
      
      if (onComplete) {
        // Get full store data from form context or parent
        // For now, we'll pass the launch data
        onComplete(data as any);
      }
    } catch (error) {
      console.error('Launch failed:', error);
    } finally {
      setIsLaunching(false);
    }
  };

  // Copy store URL
  const copyStoreUrl = () => {
    const url = data.domain.custom || `${data.domain.subdomain}.coreldove.com`;
    navigator.clipboard.writeText(`https://${url}`);
  };

  useEffect(() => {
    // Auto-enable SSL if not set
    if (!data.domain.sslEnabled) {
      updateDomain('sslEnabled', true);
    }
  }, []);

  if (launchComplete) {
    return (
      <div className="text-center py-12">
        <div className="mb-6">
          <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Trophy className="h-12 w-12 text-green-600" />
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            🎉 Congratulations! Your Store is Live!
          </h2>
          <p className="text-lg text-gray-600">
            Your e-commerce store has been successfully launched and is now accepting orders.
          </p>
        </div>

        <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
          <h3 className="font-medium text-green-900 mb-2">Your Store URL</h3>
          <div className="flex items-center justify-center space-x-2">
            <code className="bg-white px-3 py-2 rounded border text-green-800">
              https://{data.domain.custom || `${data.domain.subdomain}.coreldove.com`}
            </code>
            <Button type="button" variant="outline" size="sm" onClick={copyStoreUrl}>
              <Copy className="h-4 w-4" />
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Button
            type="button"
            variant="default"
            className="flex items-center space-x-2"
            onClick={() => window.open(`https://${data.domain.custom || `${data.domain.subdomain}.coreldove.com`}`, '_blank')}
          >
            <ExternalLink className="h-4 w-4" />
            <span>Visit Your Store</span>
          </Button>
          <Button type="button" variant="outline">
            <BarChart className="h-4 w-4 mr-2" />
            View Analytics
          </Button>
          <Button type="button" variant="outline">
            <Mail className="h-4 w-4 mr-2" />
            Marketing Center
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Domain Configuration */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Globe className="h-5 w-5" />
            <span>Domain Configuration</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="subdomain">CoreLDove Subdomain *</Label>
              <div className="flex">
                <Input
                  id="subdomain"
                  placeholder="yourstore"
                  value={data.domain.subdomain}
                  onChange={(e) => updateDomain('subdomain', e.target.value)}
                  disabled={readonly}
                  className={errors.launch?.domain?.subdomain ? 'border-red-500 rounded-r-none' : 'rounded-r-none'}
                />
                <div className="bg-gray-100 border border-l-0 px-3 py-2 rounded-r text-sm text-gray-600">
                  .coreldove.com
                </div>
              </div>
              {errors.launch?.domain?.subdomain && (
                <p className="text-sm text-red-500 mt-1">{errors.launch.domain.subdomain.message}</p>
              )}
            </div>

            <div>
              <Label htmlFor="customDomain">Custom Domain (Optional)</Label>
              <Input
                id="customDomain"
                placeholder="www.yourstore.com"
                value={data.domain.custom || ''}
                onChange={(e) => updateDomain('custom', e.target.value)}
                disabled={readonly}
              />
              <p className="text-xs text-gray-500 mt-1">
                You can connect your own domain later from settings
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <Checkbox
              id="sslEnabled"
              checked={data.domain.sslEnabled}
              onCheckedChange={(checked) => updateDomain('sslEnabled', checked)}
              disabled={readonly}
            />
            <Label htmlFor="sslEnabled" className="flex items-center space-x-2">
              <Shield className="h-4 w-4" />
              <span>Enable SSL Certificate (Recommended)</span>
            </Label>
          </div>

          <div className="bg-blue-50 p-4 rounded-lg">
            <h5 className="font-medium text-blue-900 mb-2">Your Store URL Preview</h5>
            <div className="flex items-center space-x-2">
              <code className="bg-white px-3 py-2 rounded border text-blue-800">
                https://{data.domain.custom || `${data.domain.subdomain || 'yourstore'}.coreldove.com`}
              </code>
              <Button type="button" variant="outline" size="sm" onClick={copyStoreUrl}>
                <Copy className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Analytics & Tracking */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <BarChart className="h-5 w-5" />
            <span>Analytics & Tracking</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="googleAnalytics">Google Analytics ID</Label>
              <Input
                id="googleAnalytics"
                placeholder="G-XXXXXXXXXX"
                value={data.analytics.googleAnalytics || ''}
                onChange={(e) => updateAnalytics('googleAnalytics', e.target.value)}
                disabled={readonly}
              />
              <p className="text-xs text-gray-500 mt-1">
                Get from Google Analytics 4 property
              </p>
            </div>

            <div>
              <Label htmlFor="facebookPixel">Facebook Pixel ID</Label>
              <Input
                id="facebookPixel"
                placeholder="123456789012345"
                value={data.analytics.facebookPixel || ''}
                onChange={(e) => updateAnalytics('facebookPixel', e.target.value)}
                disabled={readonly}
              />
              <p className="text-xs text-gray-500 mt-1">
                For Facebook Ads tracking
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Marketing Setup */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Mail className="h-5 w-5" />
            <span>Marketing Automation</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <Checkbox
                id="emailSequences"
                checked={data.marketing.emailSequences}
                onCheckedChange={(checked) => updateMarketing('emailSequences', checked)}
                disabled={readonly}
              />
              <Label htmlFor="emailSequences">
                Enable Welcome Email Sequences
              </Label>
            </div>

            <div className="flex items-center space-x-2">
              <Checkbox
                id="socialMediaCampaigns"
                checked={data.marketing.socialMediaCampaigns}
                onCheckedChange={(checked) => updateMarketing('socialMediaCampaigns', checked)}
                disabled={readonly}
              />
              <Label htmlFor="socialMediaCampaigns">
                Setup Social Media Marketing Campaigns
              </Label>
            </div>
          </div>

          {(data.marketing.emailSequences || data.marketing.socialMediaCampaigns) && (
            <div className="bg-green-50 p-4 rounded-lg">
              <h5 className="font-medium text-green-900 mb-2">Marketing Features Enabled</h5>
              <ul className="text-sm text-green-800 space-y-1">
                {data.marketing.emailSequences && (
                  <li>• Automated welcome emails for new customers</li>
                )}
                {data.marketing.socialMediaCampaigns && (
                  <li>• Social media campaign templates ready</li>
                )}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Pre-Launch Tests */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TestTube className="h-5 w-5" />
            <span>Pre-Launch Tests</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex justify-between items-center mb-4">
            <p className="text-gray-600">
              Run tests to ensure your store is ready for launch.
            </p>
            <Button
              type="button"
              variant="outline"
              onClick={runAllTests}
              disabled={readonly}
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              Run All Tests
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              { id: 'domain', label: 'Domain Configuration', description: 'SSL and domain setup' },
              { id: 'payment', label: 'Payment Processing', description: 'Payment gateway connectivity' },
              { id: 'shipping', label: 'Shipping Calculation', description: 'Shipping zones and rates' },
              { id: 'analytics', label: 'Analytics Tracking', description: 'Google Analytics setup' }
            ].map((test) => (
              <div key={test.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="font-medium">{test.label}</h4>
                    <p className="text-sm text-gray-600">{test.description}</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    {testResults[test.id] === 'pass' && (
                      <CheckCircle className="h-5 w-5 text-green-600" />
                    )}
                    {testResults[test.id] === 'fail' && (
                      <AlertTriangle className="h-5 w-5 text-red-600" />
                    )}
                    {testResults[test.id] === 'testing' && (
                      <Clock className="h-5 w-5 text-blue-600 animate-spin" />
                    )}
                  </div>
                </div>
                
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => runTest(test.id)}
                  disabled={readonly || testResults[test.id] === 'testing'}
                  className="w-full"
                >
                  {testResults[test.id] === 'testing' ? 'Testing...' : 'Run Test'}
                </Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Launch Checklist */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-5 w-5" />
              <span>Launch Checklist</span>
            </div>
            <Badge variant="secondary">
              {Math.round(completionPercentage())}% Complete
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Progress value={completionPercentage()} className="mb-4" />
          
          <div className="space-y-3">
            {LAUNCH_CHECKLIST_ITEMS.map((item) => (
              <div
                key={item.id}
                className={`flex items-start space-x-3 p-3 rounded-lg border ${
                  data.launchChecklist[item.id] 
                    ? 'bg-green-50 border-green-200' 
                    : item.critical 
                    ? 'bg-red-50 border-red-200' 
                    : 'bg-gray-50 border-gray-200'
                }`}
              >
                <Checkbox
                  id={item.id}
                  checked={data.launchChecklist[item.id] || false}
                  onCheckedChange={() => !readonly && toggleChecklistItem(item.id)}
                  disabled={readonly}
                />
                <div className="flex-1">
                  <Label htmlFor={item.id} className="flex items-center space-x-2">
                    <span>{item.label}</span>
                    {item.critical && (
                      <Badge variant="destructive" className="text-xs">Critical</Badge>
                    )}
                  </Label>
                </div>
                {data.launchChecklist[item.id] && (
                  <CheckCircle className="h-5 w-5 text-green-600" />
                )}
              </div>
            ))}
          </div>

          <div className="border-t pt-4">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Ready to Launch?</h4>
                <p className="text-sm text-gray-600">
                  {isReadyToLaunch() 
                    ? 'All critical items completed. Your store is ready to go live!'
                    : 'Complete all critical items before launching.'
                  }
                </p>
              </div>
              
              <Button
                type="button"
                onClick={launchStore}
                disabled={readonly || !isReadyToLaunch() || isLaunching}
                className="flex items-center space-x-2"
              >
                {isLaunching ? (
                  <>
                    <Clock className="h-4 w-4 animate-spin" />
                    <span>Launching...</span>
                  </>
                ) : (
                  <>
                    <Rocket className="h-4 w-4" />
                    <span>Launch Store</span>
                  </>
                )}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
/**
 * Campaign Creation Wizard with BYOK Platform Validation
 * Multi-step campaign creation with credential validation and platform selection
 */

'use client';

import { useState, useEffect } from 'react';
import { 
  ArrowRight, 
  ArrowLeft, 
  CheckCircle, 
  AlertTriangle, 
  Loader2,
  Target,
  Settings,
  CreditCard,
  Zap,
  Eye,
  Play,
  Key
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { Checkbox } from '@/components/ui/checkbox';
import { Slider } from '@/components/ui/slider';

// BYOK Integration
import { useCredentialResolution } from '@/hooks/use-byok';
import { SUPPORTED_PLATFORMS } from '@/lib/api/byok-api';

interface CampaignWizardProps {
  onComplete?: (campaign: any) => void;
  onCancel?: () => void;
  className?: string;
}

interface CampaignData {
  name: string;
  description: string;
  campaign_type: string;
  objective: string;
  budget: number;
  budget_type: 'daily' | 'total';
  duration: number;
  target_audience: {
    age_range: [number, number];
    locations: string[];
    interests: string[];
    custom_audiences: string[];
  };
  creative_assets: {
    headlines: string[];
    descriptions: string[];
    images: string[];
    videos: string[];
  };
  platforms: string[];
  advanced_settings: {
    bid_strategy: string;
    optimization_goal: string;
    placement_types: string[];
    schedule: any;
  };
}

const CAMPAIGN_OBJECTIVES = [
  { id: 'awareness', name: 'Brand Awareness', description: 'Increase brand recognition and reach' },
  { id: 'traffic', name: 'Website Traffic', description: 'Drive visitors to your website' },
  { id: 'engagement', name: 'Engagement', description: 'Increase likes, comments, and shares' },
  { id: 'leads', name: 'Lead Generation', description: 'Collect leads and contact information' },
  { id: 'conversions', name: 'Conversions', description: 'Drive sales and specific actions' },
  { id: 'app_installs', name: 'App Installs', description: 'Increase mobile app downloads' },
];

export function CampaignWizard({
  onComplete,
  onCancel,
  className
}: CampaignWizardProps) {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [campaignData, setCampaignData] = useState<CampaignData>({
    name: '',
    description: '',
    campaign_type: 'paid_ads',
    objective: '',
    budget: 100,
    budget_type: 'daily',
    duration: 30,
    target_audience: {
      age_range: [25, 45],
      locations: [],
      interests: [],
      custom_audiences: []
    },
    creative_assets: {
      headlines: [''],
      descriptions: [''],
      images: [],
      videos: []
    },
    platforms: [],
    advanced_settings: {
      bid_strategy: 'auto',
      optimization_goal: 'conversions',
      placement_types: ['feed', 'stories'],
      schedule: null
    }
  });

  const { resolvedCredentials, loading: credentialsLoading, resolveCredentials } = useCredentialResolution();
  const [platformValidation, setPlatformValidation] = useState<Record<string, any>>({});

  const totalSteps = 6;

  useEffect(() => {
    // Validate selected platforms when they change
    if (campaignData.platforms.length > 0) {
      campaignData.platforms.forEach(platform => {
        if (!resolvedCredentials[platform]) {
          resolveCredentials(platform);
        }
      });
    }
  }, [campaignData.platforms, resolvedCredentials, resolveCredentials]);

  const updateCampaignData = (field: string, value: any) => {
    setCampaignData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const updateNestedField = (parent: string, field: string, value: any) => {
    setCampaignData(prev => ({
      ...prev,
      [parent]: {
        ...(prev[parent as keyof CampaignData] as any),
        [field]: value
      }
    }));
  };

  const handlePlatformToggle = (platformId: string) => {
    const updatedPlatforms = campaignData.platforms.includes(platformId)
      ? campaignData.platforms.filter(p => p !== platformId)
      : [...campaignData.platforms, platformId];
    
    updateCampaignData('platforms', updatedPlatforms);
  };

  const canProceedToStep = (stepNumber: number) => {
    switch (stepNumber) {
      case 2:
        return campaignData.name && campaignData.objective;
      case 3:
        return campaignData.platforms.length > 0;
      case 4:
        return campaignData.creative_assets.headlines[0] && campaignData.creative_assets.descriptions[0];
      case 5:
        return campaignData.budget > 0 && campaignData.duration > 0;
      case 6:
        return true;
      default:
        return true;
    }
  };

  const getStepTitle = (stepNumber: number) => {
    switch (stepNumber) {
      case 1: return 'Campaign Basics';
      case 2: return 'Target Audience';
      case 3: return 'Platform Selection';
      case 4: return 'Creative Assets';
      case 5: return 'Budget & Schedule';
      case 6: return 'Review & Launch';
      default: return '';
    }
  };

  const handleCreateCampaign = async () => {
    setLoading(true);
    try {
      // Create temporal workflow for multi-platform campaign creation
      const workflowData = {
        campaign: {
          campaign_name: campaignData.name,
          description: campaignData.description,
          objective: campaignData.objective,
          platforms: campaignData.platforms,
          budget_total: campaignData.budget_type === 'daily' 
            ? campaignData.budget * campaignData.duration 
            : campaignData.budget,
          budget_type: campaignData.budget_type,
          duration_days: campaignData.duration,
          start_date: new Date().toISOString(),
          target_locations: campaignData.target_audience.locations,
          target_demographics: {
            age_min: campaignData.target_audience.age_range[0],
            age_max: campaignData.target_audience.age_range[1]
          },
          target_interests: campaignData.target_audience.interests,
          custom_audiences: campaignData.target_audience.custom_audiences,
          headlines: campaignData.creative_assets.headlines,
          descriptions: campaignData.creative_assets.descriptions,
          images: campaignData.creative_assets.images,
          videos: campaignData.creative_assets.videos
        },
        audience: {
          age_min: campaignData.target_audience.age_range[0],
          age_max: campaignData.target_audience.age_range[1],
          languages: ['en']
        },
        config: {
          require_strategy_approval: true,
          conservative_estimation: true
        }
      };

      const response = await fetch('/api/workflows/campaign-creation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(workflowData)
      });
      
      if (response.ok) {
        const workflowResult = await response.json();
        if (onComplete) {
          onComplete({
            type: 'temporal_workflow',
            workflow_id: workflowResult.workflow_id,
            campaign_data: campaignData,
            status: 'initiated'
          });
        }
      } else {
        throw new Error('Failed to initiate campaign creation workflow');
      }
    } catch (error) {
      console.error('Campaign creation workflow failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">Campaign Basics</h3>
              <p className="text-muted-foreground">
                Set up your campaign name, objective, and budget
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <Label htmlFor="campaign-name">Campaign Name *</Label>
                <Input
                  id="campaign-name"
                  value={campaignData.name}
                  onChange={(e) => updateCampaignData('name', e.target.value)}
                  placeholder="e.g., Holiday Sale 2024"
                />
              </div>

              <div>
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  value={campaignData.description}
                  onChange={(e) => updateCampaignData('description', e.target.value)}
                  placeholder="Brief description of your campaign goals..."
                  rows={3}
                />
              </div>

              <div>
                <Label>Campaign Objective *</Label>
                <div className="grid grid-cols-2 gap-2 mt-2">
                  {CAMPAIGN_OBJECTIVES.map((objective) => (
                    <Card
                      key={objective.id}
                      className={`cursor-pointer transition-all hover:shadow-md ${
                        campaignData.objective === objective.id ? 'ring-2 ring-primary bg-primary/5' : ''
                      }`}
                      onClick={() => updateCampaignData('objective', objective.id)}
                    >
                      <CardContent className="p-3">
                        <h4 className="font-medium text-sm">{objective.name}</h4>
                        <p className="text-xs text-muted-foreground">{objective.description}</p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Budget Type</Label>
                  <Select
                    value={campaignData.budget_type}
                    onValueChange={(value: 'daily' | 'total') => updateCampaignData('budget_type', value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="daily">Daily Budget</SelectItem>
                      <SelectItem value="total">Total Budget</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label>Budget Amount ($)</Label>
                  <Input
                    type="number"
                    value={campaignData.budget}
                    onChange={(e) => updateCampaignData('budget', parseFloat(e.target.value))}
                    min="1"
                  />
                </div>
              </div>

              <div>
                <Label>Duration (days)</Label>
                <Input
                  type="number"
                  value={campaignData.duration}
                  onChange={(e) => updateCampaignData('duration', parseInt(e.target.value))}
                  min="1"
                />
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">Target Audience</h3>
              <p className="text-muted-foreground">
                Define who you want to reach with your campaign
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <Label>Age Range: {campaignData.target_audience.age_range[0]} - {campaignData.target_audience.age_range[1]}</Label>
                <div className="mt-2 px-2">
                  <Slider
                    value={campaignData.target_audience.age_range}
                    onValueChange={(value) => updateNestedField('target_audience', 'age_range', value)}
                    min={13}
                    max={65}
                    step={1}
                    className="w-full"
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="locations">Locations (comma-separated)</Label>
                <Input
                  id="locations"
                  value={campaignData.target_audience.locations.join(', ')}
                  onChange={(e) => updateNestedField('target_audience', 'locations', 
                    e.target.value.split(',').map(l => l.trim()).filter(l => l)
                  )}
                  placeholder="United States, Canada, United Kingdom"
                />
              </div>

              <div>
                <Label htmlFor="interests">Interests (comma-separated)</Label>
                <Input
                  id="interests"
                  value={campaignData.target_audience.interests.join(', ')}
                  onChange={(e) => updateNestedField('target_audience', 'interests', 
                    e.target.value.split(',').map(i => i.trim()).filter(i => i)
                  )}
                  placeholder="Technology, Marketing, E-commerce"
                />
              </div>

              <div>
                <Label htmlFor="custom-audiences">Custom Audiences</Label>
                <Textarea
                  id="custom-audiences"
                  value={campaignData.target_audience.custom_audiences.join('\n')}
                  onChange={(e) => updateNestedField('target_audience', 'custom_audiences', 
                    e.target.value.split('\n').filter(a => a.trim())
                  )}
                  placeholder="Website visitors&#10;Email subscribers&#10;Lookalike audience"
                  rows={3}
                />
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">Platform Selection</h3>
              <p className="text-muted-foreground">
                Choose which platforms to run your campaign on
              </p>
            </div>

            <div className="space-y-4">
              {SUPPORTED_PLATFORMS.filter(p => ['google_ads', 'facebook_ads', 'linkedin_ads'].includes(p.id)).map((platform) => {
                const isSelected = campaignData.platforms.includes(platform.id);
                const credentials = resolvedCredentials[platform.id];
                const hasValidCredentials = credentials && credentials.health_status === 'healthy';
                const isLoading = credentialsLoading[platform.id];

                return (
                  <Card
                    key={platform.id}
                    className={`cursor-pointer transition-all hover:shadow-md ${
                      isSelected ? 'ring-2 ring-primary bg-primary/5' : ''
                    }`}
                    onClick={() => handlePlatformToggle(platform.id)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <Checkbox checked={isSelected} disabled />
                          <span className="text-2xl">{platform.icon}</span>
                          <div>
                            <h4 className="font-medium">{platform.name}</h4>
                            <p className="text-sm text-muted-foreground">{platform.description}</p>
                          </div>
                        </div>

                        <div className="flex items-center gap-2">
                          {isLoading ? (
                            <Loader2 className="h-4 w-4 animate-spin" />
                          ) : credentials ? (
                            <div className="flex items-center gap-2">
                              <Badge 
                                variant={hasValidCredentials ? "default" : "destructive"}
                                className="text-xs"
                              >
                                {hasValidCredentials ? 'Ready' : 'Error'}
                              </Badge>
                              <Badge variant="outline" className="text-xs">
                                {credentials.source === 'tenant' ? 'BYOK' : 'Platform'}
                              </Badge>
                            </div>
                          ) : (
                            <Badge variant="secondary" className="text-xs">
                              Not Connected
                            </Badge>
                          )}
                        </div>
                      </div>

                      {isSelected && credentials && !hasValidCredentials && (
                        <Alert className="mt-3">
                          <AlertTriangle className="h-4 w-4" />
                          <AlertDescription>
                            Platform credentials have issues. Please check your{' '}
                            <a href="/dashboard/byok" className="text-primary hover:underline">
                              BYOK settings
                            </a>.
                          </AlertDescription>
                        </Alert>
                      )}

                      {isSelected && !credentials && (
                        <Alert className="mt-3">
                          <Key className="h-4 w-4" />
                          <AlertDescription>
                            Platform not configured. Set up credentials in{' '}
                            <a href="/dashboard/byok" className="text-primary hover:underline">
                              BYOK Management
                            </a>.
                          </AlertDescription>
                        </Alert>
                      )}
                    </CardContent>
                  </Card>
                );
              })}
            </div>

            {campaignData.platforms.length === 0 && (
              <Alert>
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  Select at least one platform to run your campaign.
                </AlertDescription>
              </Alert>
            )}
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">Creative Assets</h3>
              <p className="text-muted-foreground">
                Add headlines, descriptions, and media for your campaign
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <Label htmlFor="headlines">Headlines (one per line)</Label>
                <Textarea
                  id="headlines"
                  value={campaignData.creative_assets.headlines.join('\n')}
                  onChange={(e) => updateNestedField('creative_assets', 'headlines', 
                    e.target.value.split('\n').filter(h => h.trim())
                  )}
                  placeholder="Transform Your Business with AI&#10;Boost ROI by 300%&#10;Get Results in 30 Days"
                  rows={4}
                />
              </div>

              <div>
                <Label htmlFor="descriptions">Descriptions (one per line)</Label>
                <Textarea
                  id="descriptions"
                  value={campaignData.creative_assets.descriptions.join('\n')}
                  onChange={(e) => updateNestedField('creative_assets', 'descriptions', 
                    e.target.value.split('\n').filter(d => d.trim())
                  )}
                  placeholder="Discover how AI can revolutionize your marketing strategy&#10;Join thousands of businesses already using our platform&#10;Start your free trial today and see results"
                  rows={4}
                />
              </div>

              <div>
                <Label htmlFor="images">Image URLs (one per line)</Label>
                <Textarea
                  id="images"
                  value={campaignData.creative_assets.images.join('\n')}
                  onChange={(e) => updateNestedField('creative_assets', 'images', 
                    e.target.value.split('\n').filter(i => i.trim())
                  )}
                  placeholder="https://example.com/image1.jpg&#10;https://example.com/image2.jpg"
                  rows={3}
                />
              </div>

              <div>
                <Label htmlFor="videos">Video URLs (optional)</Label>
                <Textarea
                  id="videos"
                  value={campaignData.creative_assets.videos.join('\n')}
                  onChange={(e) => updateNestedField('creative_assets', 'videos', 
                    e.target.value.split('\n').filter(v => v.trim())
                  )}
                  placeholder="https://example.com/video1.mp4"
                  rows={2}
                />
              </div>
            </div>
          </div>
        );

      case 5:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">Budget & Schedule</h3>
              <p className="text-muted-foreground">
                Configure advanced budget allocation and scheduling
              </p>
            </div>

            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Bid Strategy</Label>
                  <Select
                    value={campaignData.advanced_settings.bid_strategy}
                    onValueChange={(value) => updateNestedField('advanced_settings', 'bid_strategy', value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="auto">Automatic Bidding</SelectItem>
                      <SelectItem value="manual_cpc">Manual CPC</SelectItem>
                      <SelectItem value="target_cpa">Target CPA</SelectItem>
                      <SelectItem value="target_roas">Target ROAS</SelectItem>
                      <SelectItem value="maximize_clicks">Maximize Clicks</SelectItem>
                      <SelectItem value="maximize_conversions">Maximize Conversions</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label>Optimization Goal</Label>
                  <Select
                    value={campaignData.advanced_settings.optimization_goal}
                    onValueChange={(value) => updateNestedField('advanced_settings', 'optimization_goal', value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="conversions">Conversions</SelectItem>
                      <SelectItem value="clicks">Clicks</SelectItem>
                      <SelectItem value="impressions">Impressions</SelectItem>
                      <SelectItem value="reach">Reach</SelectItem>
                      <SelectItem value="video_views">Video Views</SelectItem>
                      <SelectItem value="engagement">Engagement</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <Label className="mb-3 block">Placement Types</Label>
                <div className="grid grid-cols-2 gap-2">
                  {[
                    { id: 'feed', label: 'News Feed' },
                    { id: 'stories', label: 'Stories' },
                    { id: 'reels', label: 'Reels/Shorts' },
                    { id: 'search', label: 'Search Results' },
                    { id: 'display', label: 'Display Network' },
                    { id: 'video', label: 'Video Placements' }
                  ].map((placement) => (
                    <div key={placement.id} className="flex items-center space-x-2">
                      <Checkbox
                        id={`placement-${placement.id}`}
                        checked={campaignData.advanced_settings.placement_types.includes(placement.id)}
                        onCheckedChange={(checked) => {
                          const current = campaignData.advanced_settings.placement_types;
                          const updated = checked
                            ? [...current, placement.id]
                            : current.filter(p => p !== placement.id);
                          updateNestedField('advanced_settings', 'placement_types', updated);
                        }}
                      />
                      <Label htmlFor={`placement-${placement.id}`} className="text-sm">
                        {placement.label}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>

              <Alert>
                <Zap className="h-4 w-4" />
                <AlertDescription>
                  <strong>AI Optimization:</strong> Our AI agents will continuously optimize your campaign settings based on performance data. Initial settings will be refined automatically within the first 48 hours.
                </AlertDescription>
              </Alert>
            </div>
          </div>
        );

      case 6:
        return (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">Review & Launch</h3>
              <p className="text-muted-foreground">
                Review your campaign settings before launching
              </p>
            </div>

            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base">Campaign Summary</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm font-medium">Name</p>
                      <p className="text-muted-foreground">{campaignData.name}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium">Objective</p>
                      <p className="text-muted-foreground">
                        {CAMPAIGN_OBJECTIVES.find(o => o.id === campaignData.objective)?.name}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm font-medium">Budget</p>
                      <p className="text-muted-foreground">
                        ${campaignData.budget} {campaignData.budget_type}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm font-medium">Duration</p>
                      <p className="text-muted-foreground">{campaignData.duration} days</p>
                    </div>
                  </div>

                  <div>
                    <p className="text-sm font-medium mb-2">Platforms ({campaignData.platforms.length})</p>
                    <div className="flex flex-wrap gap-2">
                      {campaignData.platforms.map(platformId => {
                        const platform = SUPPORTED_PLATFORMS.find(p => p.id === platformId);
                        const credentials = resolvedCredentials[platformId];
                        return (
                          <Badge key={platformId} variant="secondary" className="flex items-center gap-1">
                            {platform?.icon} {platform?.name}
                            {credentials?.source === 'tenant' && (
                              <span className="text-xs">BYOK</span>
                            )}
                          </Badge>
                        );
                      })}
                    </div>
                  </div>

                  <div>
                    <p className="text-sm font-medium mb-2">Target Audience</p>
                    <p className="text-muted-foreground text-sm">
                      Ages {campaignData.target_audience.age_range[0]}-{campaignData.target_audience.age_range[1]} • {' '}
                      {campaignData.target_audience.locations.length} location(s) • {' '}
                      {campaignData.target_audience.interests.length} interest(s)
                    </p>
                  </div>

                  <div>
                    <p className="text-sm font-medium mb-2">Creative Assets</p>
                    <p className="text-muted-foreground text-sm">
                      {campaignData.creative_assets.headlines.length} headline(s) • {' '}
                      {campaignData.creative_assets.descriptions.length} description(s) • {' '}
                      {campaignData.creative_assets.images.length} image(s)
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* Cost Estimation */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <CreditCard className="h-4 w-4" />
                    Estimated Costs
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm font-medium">Campaign Budget</p>
                      <p className="text-2xl font-bold">
                        ${campaignData.budget_type === 'daily' 
                          ? (campaignData.budget * campaignData.duration).toFixed(0)
                          : campaignData.budget.toFixed(0)
                        }
                      </p>
                    </div>
                    <div>
                      <p className="text-sm font-medium">Platform Fees</p>
                      <p className="text-2xl font-bold text-green-600">
                        ${campaignData.platforms.filter(p => resolvedCredentials[p]?.source === 'tenant').length * 5}*
                      </p>
                      <p className="text-xs text-muted-foreground">*BYOK savings applied</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
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
          <div className="flex items-center gap-2">
            <Target className="h-5 w-5" />
            Create New Campaign
          </div>
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
              onClick={handleCreateCampaign}
              disabled={loading}
              className="flex items-center gap-2"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Play className="h-4 w-4" />
              )}
              Launch Campaign
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

export default CampaignWizard;
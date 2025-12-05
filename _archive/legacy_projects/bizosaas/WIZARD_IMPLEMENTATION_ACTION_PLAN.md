# BizOSaaS Platform - Wizard Implementation Action Plan

## 🎯 Executive Action Items

**Priority Level:** 🚨 Critical  
**Timeline:** Complete within 2 weeks  
**Impact:** Enable full wizard functionality across all platforms  

## 📋 Critical Issue Resolution

### 🚨 Issue #1: Missing Wizard Routes (Highest Priority)

**Problem:** Wizard components exist but routes are not implemented, causing 404 errors.

**Solution:** Implement Next.js route handlers for all wizard paths.

#### Client Portal Routes to Implement:

```typescript
// 1. Create: /frontend/apps/client-portal/app/onboarding/page.tsx
'use client';

import { DirectoryManagementWizard } from '@/components/DirectoryManagementWizard';

export default function OnboardingPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <DirectoryManagementWizard />
    </div>
  );
}
```

```typescript
// 2. Create: /frontend/apps/client-portal/app/campaigns/new/page.tsx
'use client';

import { CampaignSetupWizard } from '@/components/wizard/CampaignSetupWizard';

export default function NewCampaignPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Create New Campaign</h1>
        <CampaignSetupWizard />
      </div>
    </div>
  );
}
```

```typescript
// 3. Create: /frontend/apps/client-portal/app/analytics/setup/page.tsx
'use client';

import { AnalyticsSetupWizard } from '@/components/wizard/AnalyticsSetupWizard';

export default function AnalyticsSetupPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Analytics Dashboard Setup</h1>
        <AnalyticsSetupWizard />
      </div>
    </div>
  );
}
```

```typescript
// 4. Create: /frontend/apps/client-portal/app/billing/setup/page.tsx
'use client';

import { BillingSetupWizard } from '@/components/wizard/BillingSetupWizard';

export default function BillingSetupPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Payment & Billing Setup</h1>
        <BillingSetupWizard />
      </div>
    </div>
  );
}
```

#### CoreLDove Frontend Routes:

```typescript
// 5. Create: /frontend/apps/coreldove-frontend/app/store-setup/page.tsx
'use client';

import { EcommerceStoreWizard } from '@/components/wizards/ecommerce-store-wizard';

export default function StoreSetupPage() {
  return (
    <div className="min-h-screen">
      <EcommerceStoreWizard />
    </div>
  );
}
```

```typescript
// 6. Create: /frontend/apps/coreldove-frontend/app/sourcing/wizard/page.tsx
'use client';

import { ProductSourcingWizard } from '@/components/wizard/ProductSourcingWizard';

export default function SourcingWizardPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Product Sourcing Wizard</h1>
        <ProductSourcingWizard />
      </div>
    </div>
  );
}
```

#### Business Directory Routes:

```typescript
// 7. Create: /frontend/apps/business-directory/app/listing/create/page.tsx
'use client';

import { BusinessListingWizard } from '@/components/wizard/BusinessListingWizard';

export default function CreateListingPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Create Business Listing</h1>
        <BusinessListingWizard />
      </div>
    </div>
  );
}
```

#### BizOSaaS Admin Routes:

```typescript
// 8. Create: /frontend/apps/bizosaas-admin/app/tenants/setup/page.tsx
'use client';

import { TenantSetupWizard } from '@/components/wizard/TenantSetupWizard';

export default function TenantSetupPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Multi-Tenant Setup</h1>
        <TenantSetupWizard />
      </div>
    </div>
  );
}
```

```typescript
// 9. Create: /frontend/apps/bizosaas-admin/app/ai/setup/page.tsx
'use client';

import { AISetupWizard } from '@/components/wizard/AISetupWizard';

export default function AISetupPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">AI Agent Configuration</h1>
        <AISetupWizard />
      </div>
    </div>
  );
}
```

```typescript
// 10. Create: /frontend/apps/bizosaas-admin/app/integrations/setup/page.tsx
'use client';

import { IntegrationSetupWizard } from '@/components/wizard/IntegrationSetupWizard';

export default function IntegrationSetupPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Integration Setup</h1>
        <IntegrationSetupWizard />
      </div>
    </div>
  );
}
```

```typescript
// 11. Create: /frontend/apps/bizosaas-admin/app/users/roles/setup/page.tsx
'use client';

import { UserRoleSetupWizard } from '@/components/wizard/UserRoleSetupWizard';

export default function UserRoleSetupPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">User Role & Permissions Setup</h1>
        <UserRoleSetupWizard />
      </div>
    </div>
  );
}
```

### 🚨 Issue #2: Fix Bizoholic Frontend Service

**Problem:** Platform returning 404 errors, service appears down.

**Diagnosis Commands:**
```bash
# Check container status
docker ps | grep bizoholic-frontend

# Check logs
docker logs bizoholic-frontend

# Check port availability
netstat -tulpn | grep 3001

# Check service health
curl -I http://localhost:3001
```

**Solution:**
```bash
# 1. Restart the service
docker restart bizoholic-frontend

# 2. If container doesn't exist, start it
cd /home/alagiri/projects/bizoholic/bizosaas-platform
docker-compose up -d bizoholic-frontend

# 3. Check and fix dockerfile if needed
# Verify: frontend/apps/bizoholic-frontend/Dockerfile exists

# 4. Rebuild if necessary
docker-compose build bizoholic-frontend
docker-compose up -d bizoholic-frontend
```

## 📋 Missing Wizard Components to Create

### 1. Campaign Setup Wizard
```typescript
// Create: /frontend/apps/client-portal/components/wizard/CampaignSetupWizard.tsx
'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const campaignSchema = z.object({
  campaignName: z.string().min(1, 'Campaign name is required'),
  platforms: z.array(z.string()).min(1, 'Select at least one platform'),
  targeting: z.object({
    demographics: z.object({
      ageRange: z.tuple([z.number(), z.number()]),
      gender: z.enum(['all', 'male', 'female']),
      location: z.string()
    }),
    interests: z.array(z.string()),
    keywords: z.array(z.string())
  }),
  budget: z.object({
    total: z.number().min(100, 'Minimum budget is $100'),
    dailyLimit: z.number().min(10, 'Minimum daily budget is $10'),
    bidStrategy: z.enum(['auto', 'manual', 'target-cpa'])
  }),
  creative: z.object({
    headlines: z.array(z.string()).min(3, 'Minimum 3 headlines required'),
    descriptions: z.array(z.string()).min(2, 'Minimum 2 descriptions required'),
    images: z.array(z.string()),
    videos: z.array(z.string()).optional()
  }),
  schedule: z.object({
    startDate: z.date(),
    endDate: z.date().optional(),
    dayParting: z.object({
      monday: z.object({ start: z.string(), end: z.string() }),
      tuesday: z.object({ start: z.string(), end: z.string() }),
      // ... other days
    })
  })
});

type CampaignFormData = z.infer<typeof campaignSchema>;

const WIZARD_STEPS = [
  { id: 1, title: 'Campaign Basics', description: 'Name and platform selection' },
  { id: 2, title: 'Audience Targeting', description: 'Define your target audience' },
  { id: 3, title: 'Budget & Bidding', description: 'Set budget and bid strategy' },
  { id: 4, title: 'Creative Assets', description: 'Add headlines, descriptions, and media' },
  { id: 5, title: 'Schedule & Launch', description: 'Set timing and launch campaign' },
  { id: 6, title: 'Review & Submit', description: 'Final review and submission' }
];

export function CampaignSetupWizard() {
  const [currentStep, setCurrentStep] = useState(1);
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);

  const methods = useForm<CampaignFormData>({
    resolver: zodResolver(campaignSchema),
    mode: 'onChange'
  });

  const nextStep = async () => {
    const isValid = await methods.trigger();
    if (isValid && currentStep < WIZARD_STEPS.length) {
      setCompletedSteps(prev => [...prev, currentStep]);
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const renderCurrentStep = () => {
    switch (currentStep) {
      case 1:
        return <CampaignBasicsStep />;
      case 2:
        return <AudienceTargetingStep />;
      case 3:
        return <BudgetBiddingStep />;
      case 4:
        return <CreativeAssetsStep />;
      case 5:
        return <ScheduleLaunchStep />;
      case 6:
        return <ReviewSubmitStep />;
      default:
        return null;
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Progress indicator */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {WIZARD_STEPS.map((step) => (
            <div
              key={step.id}
              className={`flex items-center ${
                step.id < WIZARD_STEPS.length ? 'flex-1' : ''
              }`}
            >
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center ${
                  completedSteps.includes(step.id)
                    ? 'bg-green-500 text-white'
                    : step.id === currentStep
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-500'
                }`}
              >
                {completedSteps.includes(step.id) ? '✓' : step.id}
              </div>
              {step.id < WIZARD_STEPS.length && (
                <div
                  className={`flex-1 h-1 mx-4 ${
                    completedSteps.includes(step.id)
                      ? 'bg-green-500'
                      : 'bg-gray-200'
                  }`}
                />
              )}
            </div>
          ))}
        </div>
        <div className="mt-4">
          <h2 className="text-2xl font-bold">
            {WIZARD_STEPS[currentStep - 1].title}
          </h2>
          <p className="text-gray-600">
            {WIZARD_STEPS[currentStep - 1].description}
          </p>
        </div>
      </div>

      {/* Step content */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        {renderCurrentStep()}
      </div>

      {/* Navigation */}
      <div className="flex justify-between">
        <button
          onClick={prevStep}
          disabled={currentStep === 1}
          className="px-6 py-2 border border-gray-300 rounded-md disabled:opacity-50"
        >
          Previous
        </button>
        <button
          onClick={nextStep}
          className="px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
        >
          {currentStep === WIZARD_STEPS.length ? 'Submit Campaign' : 'Next'}
        </button>
      </div>
    </div>
  );
}

// Step components would be implemented separately
function CampaignBasicsStep() { /* Implementation */ }
function AudienceTargetingStep() { /* Implementation */ }
function BudgetBiddingStep() { /* Implementation */ }
function CreativeAssetsStep() { /* Implementation */ }
function ScheduleLaunchStep() { /* Implementation */ }
function ReviewSubmitStep() { /* Implementation */ }
```

### 2. Analytics Setup Wizard
```typescript
// Create: /frontend/apps/client-portal/components/wizard/AnalyticsSetupWizard.tsx
'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const analyticsSchema = z.object({
  dataSources: z.object({
    googleAnalytics: z.boolean(),
    googleAds: z.boolean(),
    facebookAds: z.boolean(),
    linkedinAds: z.boolean(),
    customSources: z.array(z.string())
  }),
  metrics: z.object({
    primaryKPIs: z.array(z.string()).min(1, 'Select at least one primary KPI'),
    secondaryKPIs: z.array(z.string()),
    customMetrics: z.array(z.object({
      name: z.string(),
      formula: z.string(),
      description: z.string()
    }))
  }),
  visualization: z.object({
    dashboardLayout: z.enum(['executive', 'detailed', 'custom']),
    chartTypes: z.array(z.string()),
    refreshFrequency: z.enum(['realtime', 'hourly', 'daily', 'weekly']),
    alerts: z.object({
      enabled: z.boolean(),
      thresholds: z.array(z.object({
        metric: z.string(),
        condition: z.enum(['above', 'below', 'equals']),
        value: z.number(),
        notification: z.enum(['email', 'slack', 'webhook'])
      }))
    })
  })
});

const ANALYTICS_STEPS = [
  { id: 1, title: 'Data Sources', description: 'Connect your data sources' },
  { id: 2, title: 'Key Metrics', description: 'Select metrics to track' },
  { id: 3, title: 'Dashboard Setup', description: 'Configure visualization and alerts' }
];

export function AnalyticsSetupWizard() {
  // Similar structure to CampaignSetupWizard
  // Implementation details...
}
```

### 3. Product Sourcing Wizard
```typescript
// Create: /frontend/apps/coreldove-frontend/components/wizard/ProductSourcingWizard.tsx
'use client';

import React, { useState } from 'react';

const sourcingSchema = z.object({
  productCategory: z.string().min(1, 'Product category is required'),
  criteria: z.object({
    priceRange: z.tuple([z.number(), z.number()]),
    minimumRating: z.number().min(1).max(5),
    shippingTime: z.number().max(30),
    supplierLocation: z.array(z.string()),
    certifications: z.array(z.string())
  }),
  profitMargin: z.object({
    targetMargin: z.number().min(20, 'Minimum 20% margin recommended'),
    competitorAnalysis: z.boolean(),
    pricingStrategy: z.enum(['cost-plus', 'competitive', 'value-based'])
  }),
  supplierPreferences: z.object({
    verified: z.boolean(),
    goldSupplier: z.boolean(),
    minimumOrders: z.number(),
    paymentTerms: z.array(z.string()),
    tradeAssurance: z.boolean()
  })
});

const SOURCING_STEPS = [
  { id: 1, title: 'Product Selection', description: 'Choose product category and specifications' },
  { id: 2, title: 'Quality Criteria', description: 'Set quality and supplier requirements' },
  { id: 3, title: 'Profit Analysis', description: 'Configure pricing and margin settings' },
  { id: 4, title: 'Supplier Matching', description: 'Find and evaluate suppliers' }
];

export function ProductSourcingWizard() {
  // Implementation with Amazon API integration
  // Profit calculation tools
  // Supplier comparison features
}
```

## ⚡ Quick Implementation Script

Create this script to rapidly implement all missing routes:

```bash
#!/bin/bash
# File: implement_wizard_routes.sh

# Client Portal Routes
mkdir -p frontend/apps/client-portal/app/onboarding
mkdir -p frontend/apps/client-portal/app/campaigns/new
mkdir -p frontend/apps/client-portal/app/analytics/setup
mkdir -p frontend/apps/client-portal/app/billing/setup

# CoreLDove Routes
mkdir -p frontend/apps/coreldove-frontend/app/store-setup
mkdir -p frontend/apps/coreldove-frontend/app/sourcing/wizard

# Business Directory Routes
mkdir -p frontend/apps/business-directory/app/listing/create

# BizOSaaS Admin Routes
mkdir -p frontend/apps/bizosaas-admin/app/tenants/setup
mkdir -p frontend/apps/bizosaas-admin/app/ai/setup
mkdir -p frontend/apps/bizosaas-admin/app/integrations/setup
mkdir -p frontend/apps/bizosaas-admin/app/users/roles/setup

echo "✅ All wizard route directories created!"
echo "📋 Next: Add page.tsx files to each directory"
```

## 🛡️ Accessibility Improvements

### Add to all wizards:
```typescript
// Accessibility enhancements
const AccessibilityEnhancedWizard = () => {
  return (
    <div 
      role="region" 
      aria-labelledby="wizard-title"
      aria-describedby="wizard-description"
    >
      <h1 id="wizard-title">Wizard Title</h1>
      <p id="wizard-description">Step-by-step guide description</p>
      
      {/* Progress indicator with ARIA */}
      <nav aria-label="Wizard Progress" className="mb-8">
        <ol className="flex items-center">
          {steps.map((step, index) => (
            <li 
              key={step.id}
              aria-current={currentStep === index + 1 ? 'step' : undefined}
              className="flex items-center"
            >
              <button
                aria-label={`Step ${index + 1}: ${step.title}`}
                aria-pressed={currentStep === index + 1}
                disabled={index + 1 > currentStep}
                className="step-button"
              >
                {index + 1}
              </button>
            </li>
          ))}
        </ol>
      </nav>

      {/* Form with proper labels */}
      <form>
        <div className="form-group">
          <label htmlFor="business-name" className="required">
            Business Name
          </label>
          <input
            id="business-name"
            type="text"
            aria-required="true"
            aria-invalid={errors.businessName ? 'true' : 'false'}
            aria-describedby={errors.businessName ? 'business-name-error' : undefined}
          />
          {errors.businessName && (
            <div id="business-name-error" role="alert" className="error">
              {errors.businessName.message}
            </div>
          )}
        </div>
      </form>

      {/* Navigation with keyboard support */}
      <div className="wizard-navigation" role="navigation" aria-label="Wizard Navigation">
        <button
          type="button"
          onClick={prevStep}
          disabled={currentStep === 1}
          aria-label="Go to previous step"
        >
          Previous
        </button>
        <button
          type="button"
          onClick={nextStep}
          aria-label={`Go to next step: ${steps[currentStep]?.title}`}
        >
          Next
        </button>
      </div>
    </div>
  );
};
```

## 📊 Testing Strategy

### 1. Create Automated Tests
```typescript
// tests/wizards/wizard-navigation.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CampaignSetupWizard } from '@/components/wizard/CampaignSetupWizard';

describe('Campaign Setup Wizard', () => {
  test('should navigate between steps', async () => {
    render(<CampaignSetupWizard />);
    
    // Check initial step
    expect(screen.getByText('Campaign Basics')).toBeInTheDocument();
    
    // Fill required fields
    fireEvent.change(screen.getByLabelText('Campaign Name'), {
      target: { value: 'Test Campaign' }
    });
    
    // Navigate to next step
    fireEvent.click(screen.getByText('Next'));
    
    await waitFor(() => {
      expect(screen.getByText('Audience Targeting')).toBeInTheDocument();
    });
  });

  test('should prevent navigation with invalid data', async () => {
    render(<CampaignSetupWizard />);
    
    // Try to navigate without filling required fields
    fireEvent.click(screen.getByText('Next'));
    
    // Should stay on same step and show error
    expect(screen.getByText('Campaign name is required')).toBeInTheDocument();
    expect(screen.getByText('Campaign Basics')).toBeInTheDocument();
  });
});
```

### 2. Performance Testing
```typescript
// tests/performance/wizard-performance.test.ts
import { performance } from 'perf_hooks';

describe('Wizard Performance', () => {
  test('should load within 2 seconds', async () => {
    const start = performance.now();
    
    // Load wizard component
    const result = await import('@/components/wizard/CampaignSetupWizard');
    
    const end = performance.now();
    const loadTime = end - start;
    
    expect(loadTime).toBeLessThan(2000); // 2 seconds
  });
});
```

## 📈 Success Metrics & Monitoring

### Implementation Checklist:
- [ ] All 11 wizard routes implemented
- [ ] Bizoholic Frontend service restored
- [ ] Accessibility features added (ARIA labels, keyboard navigation)
- [ ] Auto-save functionality implemented
- [ ] Performance optimizations applied
- [ ] Test suite created and passing
- [ ] Documentation updated

### KPI Targets:
- **Route Coverage:** 0% → 100% (11/11 routes)
- **Accessibility Score:** 25% → 90%
- **Load Time:** Current → <2 seconds
- **Error Rate:** Current → <1%
- **User Completion Rate:** Measure after implementation

### Monitoring Setup:
```typescript
// Add to all wizards
useEffect(() => {
  // Track wizard start
  analytics.track('wizard_started', {
    wizard_type: 'campaign_setup',
    step: currentStep,
    timestamp: new Date().toISOString()
  });
}, []);

useEffect(() => {
  // Track step completion
  analytics.track('wizard_step_completed', {
    wizard_type: 'campaign_setup',
    step: currentStep,
    completion_time: stepCompletionTime,
    timestamp: new Date().toISOString()
  });
}, [currentStep]);
```

## 🎯 Next Steps

1. **Immediate (Today):**
   - Run implementation script to create route directories
   - Fix Bizoholic Frontend service
   - Implement at least 3 critical wizard routes

2. **This Week:**
   - Complete all 11 wizard route implementations
   - Add basic accessibility features
   - Implement auto-save functionality

3. **Next Week:**
   - Advanced accessibility compliance
   - Performance optimization
   - Comprehensive testing

4. **Following Week:**
   - User testing and feedback integration
   - Advanced features (AI personalization)
   - Documentation and training materials

---

**Implementation Status:** 🚨 Critical - Immediate Action Required  
**Expected Completion:** 2 weeks from September 26, 2025  
**Success Measure:** All wizards functional with >90% accessibility score
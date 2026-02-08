'use client';

import React, { useState, useCallback } from 'react';
import { useForm, FormProvider } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
// import { motion, AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight, CheckCircle, Circle, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Progress, Badge, useToast } from '../ui';

import { StoreSetupData, WizardStep } from './types';
import { storeSetupSchema } from './validation';

// Step Components
import { StoreInfoStep } from './steps/store-info-step';
import { ProductCatalogStep } from './steps/product-catalog-step';
import { PaymentGatewaysStep } from './steps/payment-gateways-step';
import { ShippingAndTaxStep } from './steps/shipping-and-tax-step';
import { CustomizationStep } from './steps/customization-step';
import { LaunchPreparationStep } from './steps/launch-preparation-step';

// State management hook
import { useStoreSetupStore } from './store/store-setup-store';

interface EcommerceStoreWizardProps {
  onComplete?: (data: StoreSetupData) => void;
  onSave?: (data: Partial<StoreSetupData>) => void;
  initialData?: Partial<StoreSetupData>;
  readonly?: boolean;
}

const WIZARD_STEPS: WizardStep[] = [
  {
    id: 1,
    title: 'Store Information',
    description: 'Basic store details and branding',
    completed: false,
    current: true
  },
  {
    id: 2,
    title: 'Product Catalog',
    description: 'Add products and configure catalog',
    completed: false,
    current: false
  },
  {
    id: 3,
    title: 'Payment Gateways',
    description: 'Configure payment methods',
    completed: false,
    current: false
  },
  {
    id: 4,
    title: 'Shipping & Tax',
    description: 'Set up shipping and tax rules',
    completed: false,
    current: false
  },
  {
    id: 5,
    title: 'Store Customization',
    description: 'Choose theme and customize design',
    completed: false,
    current: false
  },
  {
    id: 6,
    title: 'Launch Preparation',
    description: 'Final checks and go live',
    completed: false,
    current: false
  }
];

export function EcommerceStoreWizard({
  onComplete,
  onSave,
  initialData,
  readonly = false
}: EcommerceStoreWizardProps) {
  const { toast } = useToast();
  const [currentStep, setCurrentStep] = useState(1);
  const [steps, setSteps] = useState(WIZARD_STEPS);
  const [isLoading, setIsLoading] = useState(false);
  const [previewMode, setPreviewMode] = useState(false);

  // Initialize store with initial data
  const {
    data,
    updateStoreInfo,
    updateProductCatalog,
    updatePaymentGateways,
    updateShippingAndTax,
    updateCustomization,
    updateLaunch,
    isStepValid,
    saveProgress,
    loadProgress
  } = useStoreSetupStore(initialData);

  // Form setup with validation
  const methods = useForm<StoreSetupData>({
    resolver: zodResolver(storeSetupSchema),
    defaultValues: data,
    mode: 'onChange'
  });

  const { handleSubmit, trigger, formState: { errors, isValid } } = methods;

  // Auto-save functionality
  const autoSave = useCallback(async () => {
    if (onSave) {
      try {
        await saveProgress();
        onSave(data);
        toast({
          title: 'Progress saved',
          description: 'Your progress has been automatically saved.',
        });
      } catch (error) {
        console.error('Auto-save failed:', error);
      }
    }
  }, [data, onSave, saveProgress, toast]);

  // Navigate to next step
  const nextStep = async () => {
    const isCurrentStepValid = await trigger(getCurrentStepKey());
    
    if (!isCurrentStepValid) {
      toast({
        title: 'Please fix errors',
        description: 'There are validation errors in the current step.',
        variant: 'destructive',
      });
      return;
    }

    if (currentStep < WIZARD_STEPS.length) {
      // Mark current step as completed
      setSteps(prev => prev.map(step => ({
        ...step,
        completed: step.id === currentStep ? true : step.completed,
        current: step.id === currentStep + 1
      })));
      
      setCurrentStep(prev => prev + 1);
      await autoSave();
    }
  };

  // Navigate to previous step
  const prevStep = () => {
    if (currentStep > 1) {
      setSteps(prev => prev.map(step => ({
        ...step,
        current: step.id === currentStep - 1
      })));
      
      setCurrentStep(prev => prev - 1);
    }
  };

  // Jump to specific step
  const goToStep = async (stepNumber: number) => {
    if (stepNumber <= currentStep || steps[stepNumber - 1].completed) {
      setSteps(prev => prev.map(step => ({
        ...step,
        current: step.id === stepNumber
      })));
      
      setCurrentStep(stepNumber);
    }
  };

  // Get current step validation key
  const getCurrentStepKey = (): keyof StoreSetupData => {
    const stepKeys: { [key: number]: keyof StoreSetupData } = {
      1: 'storeInfo',
      2: 'productCatalog',
      3: 'paymentGateways',
      4: 'shippingAndTax',
      5: 'customization',
      6: 'launch'
    };
    return stepKeys[currentStep];
  };

  // Render current step component
  const renderCurrentStep = () => {
    switch (currentStep) {
      case 1:
        return <StoreInfoStep data={data.storeInfo} onChange={updateStoreInfo} readonly={readonly} />;
      case 2:
        return <ProductCatalogStep data={data.productCatalog} onChange={updateProductCatalog} readonly={readonly} />;
      case 3:
        return <PaymentGatewaysStep data={data.paymentGateways} onChange={updatePaymentGateways} readonly={readonly} />;
      case 4:
        return <ShippingAndTaxStep data={data.shippingAndTax} onChange={updateShippingAndTax} readonly={readonly} />;
      case 5:
        return <CustomizationStep data={data.customization} onChange={updateCustomization} readonly={readonly} />;
      case 6:
        return <LaunchPreparationStep data={data.launch} onChange={updateLaunch} onComplete={onComplete} readonly={readonly} />;
      default:
        return null;
    }
  };

  // Calculate overall progress
  const progress = (steps.filter(step => step.completed).length / steps.length) * 100;

  // Handle final submission
  const onSubmit = async (formData: StoreSetupData) => {
    setIsLoading(true);
    try {
      if (onComplete) {
        await onComplete(formData);
      }
      toast({
        title: 'Store setup completed!',
        description: 'Your e-commerce store has been successfully configured.',
      });
    } catch (error) {
      toast({
        title: 'Setup failed',
        description: 'There was an error completing the store setup. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            E-commerce Store Setup Wizard
          </h1>
          <p className="text-lg text-gray-600">
            Create your professional online store in 6 simple steps
          </p>
        </div>

        {/* Progress Bar */}
        <Card className="mb-8">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Setup Progress</h3>
              <Badge variant="secondary" className="text-sm">
                {Math.round(progress)}% Complete
              </Badge>
            </div>
            <Progress value={progress} className="mb-4" />
            
            {/* Step Navigation */}
            <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
              {steps.map((step, index) => (
                <div
                  key={step.id}
                  className={`cursor-pointer p-3 rounded-lg border transition-all ${
                    step.current
                      ? 'border-blue-500 bg-blue-50'
                      : step.completed
                      ? 'border-green-500 bg-green-50'
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                  onClick={() => goToStep(step.id)}
                >
                  <div className="flex items-center space-x-2">
                    {step.completed ? (
                      <CheckCircle className="h-5 w-5 text-green-600" />
                    ) : step.current ? (
                      <div className="h-5 w-5 rounded-full border-2 border-blue-600 bg-blue-600" />
                    ) : (
                      <Circle className="h-5 w-5 text-gray-400" />
                    )}
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm font-medium truncate ${
                        step.current ? 'text-blue-900' : 
                        step.completed ? 'text-green-900' : 'text-gray-600'
                      }`}>
                        {step.title}
                      </p>
                      <p className={`text-xs truncate ${
                        step.current ? 'text-blue-600' : 
                        step.completed ? 'text-green-600' : 'text-gray-500'
                      }`}>
                        {step.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <FormProvider {...methods}>
          <form onSubmit={handleSubmit(onSubmit)}>
            {/* Main Content */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
              {/* Step Content */}
              <div className="lg:col-span-3">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <span className="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">
                        {currentStep}
                      </span>
                      <span>{steps[currentStep - 1].title}</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div key={currentStep}>
                      {renderCurrentStep()}
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Sidebar */}
              <div className="space-y-6">
                {/* Current Step Info */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Current Step</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <h4 className="font-semibold text-gray-900 mb-2">
                      {steps[currentStep - 1].title}
                    </h4>
                    <p className="text-sm text-gray-600 mb-4">
                      {steps[currentStep - 1].description}
                    </p>
                    
                    {/* Step-specific help */}
                    <div className="space-y-2">
                      {currentStep === 1 && (
                        <div className="text-xs text-gray-500">
                          <p>• Store name will be your brand identity</p>
                          <p>• GST registration is required for Indian businesses</p>
                          <p>• Upload a high-quality logo (PNG/JPG)</p>
                        </div>
                      )}
                      {currentStep === 2 && (
                        <div className="text-xs text-gray-500">
                          <p>• Add at least 5 products to start selling</p>
                          <p>• Use CSV import for bulk product addition</p>
                          <p>• High-quality images increase sales</p>
                        </div>
                      )}
                      {currentStep === 3 && (
                        <div className="text-xs text-gray-500">
                          <p>• Razorpay is most popular in India</p>
                          <p>• Enable UPI for higher conversion</p>
                          <p>• Test payments before going live</p>
                        </div>
                      )}
                      {currentStep === 4 && (
                        <div className="text-xs text-gray-500">
                          <p>• Free shipping increases conversions</p>
                          <p>• GST is automatically calculated</p>
                          <p>• Multiple delivery partners reduce costs</p>
                        </div>
                      )}
                      {currentStep === 5 && (
                        <div className="text-xs text-gray-500">
                          <p>• Choose theme matching your business</p>
                          <p>• SEO optimization is crucial</p>
                          <p>• Mobile responsiveness is essential</p>
                        </div>
                      )}
                      {currentStep === 6 && (
                        <div className="text-xs text-gray-500">
                          <p>• Complete all checklist items</p>
                          <p>• Test your store thoroughly</p>
                          <p>• Backup before going live</p>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>

                {/* Preview Store */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Store Preview</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Button
                      variant="outline"
                      className="w-full"
                      onClick={() => setPreviewMode(true)}
                      disabled={!data.storeInfo.name}
                    >
                      Preview Your Store
                    </Button>
                    {!data.storeInfo.name && (
                      <p className="text-xs text-gray-500 mt-2 text-center">
                        Complete store info to preview
                      </p>
                    )}
                  </CardContent>
                </Card>

                {/* Quick Actions */}
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Quick Actions</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <Button
                      variant="outline"
                      size="sm"
                      className="w-full"
                      onClick={autoSave}
                      disabled={isLoading}
                    >
                      Save Progress
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      className="w-full"
                      onClick={() => loadProgress()}
                    >
                      Load Saved Progress
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* Navigation */}
            <div className="flex justify-between items-center mt-8 p-6 bg-white rounded-lg border">
              <Button
                type="button"
                variant="outline"
                onClick={prevStep}
                disabled={currentStep === 1}
                className="flex items-center space-x-2"
              >
                <ChevronLeft className="h-4 w-4" />
                <span>Previous</span>
              </Button>

              <div className="text-sm text-gray-500">
                Step {currentStep} of {steps.length}
              </div>

              {currentStep < steps.length ? (
                <Button
                  type="button"
                  onClick={nextStep}
                  disabled={isLoading}
                  className="flex items-center space-x-2"
                >
                  <span>Next</span>
                  <ChevronRight className="h-4 w-4" />
                </Button>
              ) : (
                <Button
                  type="submit"
                  disabled={isLoading || !isValid}
                  className="flex items-center space-x-2"
                >
                  {isLoading ? 'Launching...' : 'Launch Store'}
                  <CheckCircle className="h-4 w-4" />
                </Button>
              )}
            </div>
          </form>
        </FormProvider>

        {/* Error Summary */}
        {Object.keys(errors).length > 0 && (
          <Card className="mt-4 border-red-200 bg-red-50">
            <CardContent className="p-4">
              <div className="flex items-center space-x-2 text-red-800">
                <AlertCircle className="h-5 w-5" />
                <h4 className="font-semibold">Please fix the following errors:</h4>
              </div>
              <ul className="mt-2 text-sm text-red-700">
                {Object.entries(errors).map(([key, error]) => (
                  <li key={key} className="flex items-center space-x-1">
                    <span>•</span>
                    <span>{error.message}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
'use client';

import React from 'react';
import { EcommerceStoreWizard } from '../../components/wizards';
import { StoreSetupData } from '../../components/wizards/types';

export default function StoreSetupPage() {
  // Handle wizard completion
  const handleWizardComplete = async (data: StoreSetupData) => {
    console.log('Store setup completed:', data);
    
    try {
      // Send data to Brain API
      const response = await fetch('http://bizosaas-brain:8001/api/ecommerce/store-setup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Store created successfully:', result);
        
        // Redirect to store dashboard or show success message
        window.location.href = `/store/${result.storeId}/dashboard`;
      } else {
        throw new Error('Failed to create store');
      }
    } catch (error) {
      console.error('Error creating store:', error);
      alert('Failed to create store. Please try again.');
    }
  };

  // Handle progress save
  const handleProgressSave = async (data: Partial<StoreSetupData>) => {
    console.log('Saving progress:', data);
    
    try {
      // Save progress to local storage or server
      localStorage.setItem('coreldove-store-setup-progress', JSON.stringify({
        data,
        timestamp: new Date().toISOString()
      }));
    } catch (error) {
      console.error('Error saving progress:', error);
    }
  };

  // Load initial data from saved progress
  const getInitialData = (): Partial<StoreSetupData> | undefined => {
    try {
      const saved = localStorage.getItem('coreldove-store-setup-progress');
      if (saved) {
        const { data } = JSON.parse(saved);
        return data;
      }
    } catch (error) {
      console.error('Error loading saved progress:', error);
    }
    return undefined;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <EcommerceStoreWizard
        onComplete={handleWizardComplete}
        onSave={handleProgressSave}
        initialData={getInitialData()}
      />
    </div>
  );
}
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { StoreSetupData } from '../types';

interface StoreSetupStore {
  data: StoreSetupData;
  isDirty: boolean;
  lastSaved: Date | null;
  
  // Actions
  updateStoreInfo: (storeInfo: Partial<StoreSetupData['storeInfo']>) => void;
  updateProductCatalog: (productCatalog: Partial<StoreSetupData['productCatalog']>) => void;
  updatePaymentGateways: (paymentGateways: Partial<StoreSetupData['paymentGateways']>) => void;
  updateShippingAndTax: (shippingAndTax: Partial<StoreSetupData['shippingAndTax']>) => void;
  updateCustomization: (customization: Partial<StoreSetupData['customization']>) => void;
  updateLaunch: (launch: Partial<StoreSetupData['launch']>) => void;
  
  // Validation helpers
  isStepValid: (step: keyof StoreSetupData) => boolean;
  getCompletionPercentage: () => number;
  
  // Persistence
  saveProgress: () => Promise<void>;
  loadProgress: () => Promise<void>;
  clearProgress: () => void;
  
  // Reset
  resetStore: () => void;
}

// Default store data
const defaultStoreData: StoreSetupData = {
  storeInfo: {
    name: '',
    description: '',
    businessType: '',
    brandColor: '#3B82F6',
    contactInfo: {
      email: '',
      phone: '',
      address: {
        street: '',
        city: '',
        state: '',
        pincode: '',
        country: 'India'
      }
    },
    currency: {
      primary: 'INR',
      supported: ['INR']
    },
    businessRegistration: {}
  },
  productCatalog: {
    categories: [],
    importMethod: 'manual',
    products: [],
    pricingStrategy: 'fixed',
    inventoryTracking: true
  },
  paymentGateways: {
    enabled: [],
    primary: '',
    configurations: {},
    digitalWallets: []
  },
  shippingAndTax: {
    shippingZones: [],
    taxConfiguration: {
      gst: {
        cgst: 9,
        sgst: 9,
        igst: 18
      },
      international: []
    },
    deliveryPartners: []
  },
  customization: {
    theme: '',
    layout: {
      homepage: 'grid',
      navigation: [],
      footer: {
        copyright: '',
        links: []
      }
    },
    seo: {
      title: '',
      description: '',
      keywords: []
    },
    socialMedia: {}
  },
  launch: {
    domain: {
      subdomain: '',
      sslEnabled: true
    },
    analytics: {},
    marketing: {
      emailSequences: false,
      socialMediaCampaigns: false
    },
    launchChecklist: {},
    isLive: false
  }
};

export const useStoreSetupStore = (initialData?: Partial<StoreSetupData>) => {
  return create<StoreSetupStore>()(
    persist(
      (set, get) => ({
        data: initialData ? { ...defaultStoreData, ...initialData } : defaultStoreData,
        isDirty: false,
        lastSaved: null,

        updateStoreInfo: (storeInfo) => {
          set((state) => ({
            data: {
              ...state.data,
              storeInfo: { ...state.data.storeInfo, ...storeInfo }
            },
            isDirty: true
          }));
        },

        updateProductCatalog: (productCatalog) => {
          set((state) => ({
            data: {
              ...state.data,
              productCatalog: { ...state.data.productCatalog, ...productCatalog }
            },
            isDirty: true
          }));
        },

        updatePaymentGateways: (paymentGateways) => {
          set((state) => ({
            data: {
              ...state.data,
              paymentGateways: { ...state.data.paymentGateways, ...paymentGateways }
            },
            isDirty: true
          }));
        },

        updateShippingAndTax: (shippingAndTax) => {
          set((state) => ({
            data: {
              ...state.data,
              shippingAndTax: { ...state.data.shippingAndTax, ...shippingAndTax }
            },
            isDirty: true
          }));
        },

        updateCustomization: (customization) => {
          set((state) => ({
            data: {
              ...state.data,
              customization: { ...state.data.customization, ...customization }
            },
            isDirty: true
          }));
        },

        updateLaunch: (launch) => {
          set((state) => ({
            data: {
              ...state.data,
              launch: { ...state.data.launch, ...launch }
            },
            isDirty: true
          }));
        },

        isStepValid: (step) => {
          const state = get();
          const stepData = state.data[step];
          
          switch (step) {
            case 'storeInfo':
              return !!(
                stepData.name &&
                stepData.description &&
                stepData.businessType &&
                stepData.contactInfo.email &&
                stepData.contactInfo.phone
              );
            
            case 'productCatalog':
              return !!(
                stepData.categories.length > 0 &&
                stepData.products.length > 0
              );
            
            case 'paymentGateways':
              return !!(
                stepData.enabled.length > 0 &&
                stepData.primary
              );
            
            case 'shippingAndTax':
              return !!(
                stepData.shippingZones.length > 0 &&
                stepData.deliveryPartners.length > 0
              );
            
            case 'customization':
              return !!(
                stepData.theme &&
                stepData.seo.title &&
                stepData.seo.description
              );
            
            case 'launch':
              return !!(
                stepData.domain.subdomain &&
                Object.values(stepData.launchChecklist).filter(Boolean).length >= 6
              );
            
            default:
              return false;
          }
        },

        getCompletionPercentage: () => {
          const state = get();
          const steps: (keyof StoreSetupData)[] = [
            'storeInfo',
            'productCatalog', 
            'paymentGateways',
            'shippingAndTax',
            'customization',
            'launch'
          ];
          
          const validSteps = steps.filter(step => state.isStepValid(step));
          return (validSteps.length / steps.length) * 100;
        },

        saveProgress: async () => {
          const state = get();
          try {
            // Save to local storage (handled by persist middleware)
            // Additionally, you could save to server here
            const response = await fetch('/api/store-setup/save', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(state.data),
            });

            if (response.ok) {
              set({ isDirty: false, lastSaved: new Date() });
            }
          } catch (error) {
            console.error('Failed to save progress:', error);
            // Still mark as saved locally
            set({ isDirty: false, lastSaved: new Date() });
          }
        },

        loadProgress: async () => {
          try {
            const response = await fetch('/api/store-setup/load');
            if (response.ok) {
              const savedData = await response.json();
              set({ 
                data: { ...defaultStoreData, ...savedData },
                isDirty: false,
                lastSaved: new Date(savedData.lastSaved)
              });
            }
          } catch (error) {
            console.error('Failed to load progress:', error);
          }
        },

        clearProgress: () => {
          set({
            data: defaultStoreData,
            isDirty: false,
            lastSaved: null
          });
        },

        resetStore: () => {
          set({
            data: defaultStoreData,
            isDirty: false,
            lastSaved: null
          });
        }
      }),
      {
        name: 'coreldove-store-setup',
        storage: createJSONStorage(() => localStorage),
        partialize: (state) => ({
          data: state.data,
          lastSaved: state.lastSaved
        }),
      }
    )
  );
};
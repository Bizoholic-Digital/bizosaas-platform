export interface StoreSetupData {
  // Step 1: Store Information & Branding
  storeInfo: {
    name: string;
    description: string;
    businessType: string;
    logo?: File;
    brandColor: string;
    contactInfo: {
      email: string;
      phone: string;
      address: {
        street: string;
        city: string;
        state: string;
        pincode: string;
        country: string;
      };
    };
    currency: {
      primary: string;
      supported: string[];
    };
    businessRegistration: {
      gst?: string;
      pan?: string;
      registrationNumber?: string;
    };
  };

  // Step 2: Product Catalog Setup
  productCatalog: {
    categories: string[];
    importMethod: 'manual' | 'csv' | 'excel' | 'api';
    products: Array<{
      name: string;
      description: string;
      category: string;
      price: number;
      images: File[];
      inventory: number;
      sku: string;
    }>;
    pricingStrategy: 'fixed' | 'dynamic' | 'tiered';
    inventoryTracking: boolean;
  };

  // Step 3: Payment Gateway Configuration
  paymentGateways: {
    enabled: string[];
    primary: string;
    configurations: {
      [key: string]: {
        apiKey: string;
        secretKey: string;
        merchantId?: string;
        testMode: boolean;
        feeStructure: {
          percentage: number;
          fixedFee: number;
        };
      };
    };
    digitalWallets: string[];
  };

  // Step 4: Shipping & Tax Configuration
  shippingAndTax: {
    shippingZones: Array<{
      name: string;
      countries: string[];
      states?: string[];
      rates: Array<{
        method: string;
        cost: number;
        freeThreshold?: number;
      }>;
    }>;
    taxConfiguration: {
      gst: {
        cgst: number;
        sgst: number;
        igst: number;
      };
      international: Array<{
        country: string;
        rate: number;
      }>;
    };
    deliveryPartners: string[];
  };

  // Step 5: Store Customization & Themes
  customization: {
    theme: string;
    layout: {
      homepage: string;
      navigation: Array<{
        label: string;
        url: string;
        children?: Array<{
          label: string;
          url: string;
        }>;
      }>;
      footer: {
        copyright: string;
        links: Array<{
          label: string;
          url: string;
        }>;
      };
    };
    seo: {
      title: string;
      description: string;
      keywords: string[];
    };
    socialMedia: {
      facebook?: string;
      instagram?: string;
      twitter?: string;
      youtube?: string;
    };
  };

  // Step 6: Launch Preparation
  launch: {
    domain: {
      custom?: string;
      subdomain: string;
      sslEnabled: boolean;
    };
    analytics: {
      googleAnalytics?: string;
      facebookPixel?: string;
    };
    marketing: {
      emailSequences: boolean;
      socialMediaCampaigns: boolean;
    };
    launchChecklist: {
      [key: string]: boolean;
    };
    isLive: boolean;
  };
}

export interface WizardStep {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  current: boolean;
}

export interface BusinessTemplate {
  id: string;
  name: string;
  description: string;
  categories: string[];
  defaultTheme: string;
  recommendedPaymentGateways: string[];
  sampleProducts: Array<{
    name: string;
    category: string;
    price: number;
  }>;
  gstConfiguration?: {
    hsnCodes: string[];
    defaultRate: number;
  };
}

export interface PaymentGateway {
  id: string;
  name: string;
  logo: string;
  description: string;
  feeStructure: {
    domestic: {
      percentage: number;
      fixedFee: number;
    };
    international: {
      percentage: number;
      fixedFee: number;
    };
  };
  supportedCurrencies: string[];
  features: string[];
  setup: {
    testMode: boolean;
    requiredFields: Array<{
      name: string;
      label: string;
      type: string;
      required: boolean;
    }>;
  };
}

export interface ShippingZone {
  id: string;
  name: string;
  type: 'domestic' | 'international';
  coverage: {
    countries?: string[];
    states?: string[];
    pincodes?: string[];
  };
  methods: Array<{
    id: string;
    name: string;
    description: string;
    calculation: 'flat' | 'weight' | 'zone';
    rate: number;
    freeThreshold?: number;
    estimatedDays: string;
  }>;
}

export interface Theme {
  id: string;
  name: string;
  description: string;
  preview: string;
  category: string;
  features: string[];
  customizable: {
    colors: boolean;
    fonts: boolean;
    layout: boolean;
  };
  responsive: boolean;
  price: number;
}
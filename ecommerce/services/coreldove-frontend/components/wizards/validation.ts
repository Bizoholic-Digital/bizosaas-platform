import { z } from 'zod';

// Step 1: Store Information & Branding
export const storeInfoSchema = z.object({
  name: z.string().min(2, 'Store name must be at least 2 characters').max(100, 'Store name too long'),
  description: z.string().min(10, 'Description must be at least 10 characters').max(500, 'Description too long'),
  businessType: z.string().min(1, 'Please select a business type'),
  logo: z.instanceof(File).optional(),
  brandColor: z.string().regex(/^#[0-9A-F]{6}$/i, 'Please select a valid color'),
  contactInfo: z.object({
    email: z.string().email('Please enter a valid email address'),
    phone: z.string().regex(/^(\+91)?[6-9]\d{9}$/, 'Please enter a valid Indian phone number'),
    address: z.object({
      street: z.string().min(5, 'Street address must be at least 5 characters'),
      city: z.string().min(2, 'City name must be at least 2 characters'),
      state: z.string().min(1, 'Please select a state'),
      pincode: z.string().regex(/^[1-9][0-9]{5}$/, 'Please enter a valid 6-digit pincode'),
      country: z.string().default('India')
    })
  }),
  currency: z.object({
    primary: z.string().default('INR'),
    supported: z.array(z.string()).min(1, 'At least one currency must be supported')
  }),
  businessRegistration: z.object({
    gst: z.string().regex(/^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/, 'Please enter a valid GST number').optional(),
    pan: z.string().regex(/^[A-Z]{5}[0-9]{4}[A-Z]{1}$/, 'Please enter a valid PAN number').optional(),
    registrationNumber: z.string().optional()
  })
});

// Step 2: Product Catalog Setup
export const productCatalogSchema = z.object({
  categories: z.array(z.string()).min(1, 'At least one category must be selected'),
  importMethod: z.enum(['manual', 'csv', 'excel', 'api']),
  products: z.array(z.object({
    name: z.string().min(2, 'Product name must be at least 2 characters'),
    description: z.string().min(10, 'Product description must be at least 10 characters'),
    category: z.string().min(1, 'Please select a category'),
    price: z.number().min(0.01, 'Price must be greater than 0'),
    images: z.array(z.instanceof(File)).min(1, 'At least one image is required'),
    inventory: z.number().int().min(0, 'Inventory cannot be negative'),
    sku: z.string().min(1, 'SKU is required')
  })).min(1, 'At least one product must be added'),
  pricingStrategy: z.enum(['fixed', 'dynamic', 'tiered']),
  inventoryTracking: z.boolean()
});

// Step 3: Payment Gateway Configuration
export const paymentGatewaysSchema = z.object({
  enabled: z.array(z.string()).min(1, 'At least one payment gateway must be enabled'),
  primary: z.string().min(1, 'Please select a primary payment gateway'),
  configurations: z.record(z.object({
    apiKey: z.string().min(1, 'API Key is required'),
    secretKey: z.string().min(1, 'Secret Key is required'),
    merchantId: z.string().optional(),
    testMode: z.boolean(),
    feeStructure: z.object({
      percentage: z.number().min(0).max(10, 'Fee percentage cannot exceed 10%'),
      fixedFee: z.number().min(0)
    })
  })),
  digitalWallets: z.array(z.string())
});

// Step 4: Shipping & Tax Configuration
export const shippingAndTaxSchema = z.object({
  shippingZones: z.array(z.object({
    name: z.string().min(2, 'Zone name must be at least 2 characters'),
    countries: z.array(z.string()).min(1, 'At least one country must be selected'),
    states: z.array(z.string()).optional(),
    rates: z.array(z.object({
      method: z.string().min(1, 'Shipping method is required'),
      cost: z.number().min(0, 'Shipping cost cannot be negative'),
      freeThreshold: z.number().min(0).optional()
    })).min(1, 'At least one shipping rate must be configured')
  })).min(1, 'At least one shipping zone must be configured'),
  taxConfiguration: z.object({
    gst: z.object({
      cgst: z.number().min(0).max(28, 'CGST rate cannot exceed 28%'),
      sgst: z.number().min(0).max(28, 'SGST rate cannot exceed 28%'),
      igst: z.number().min(0).max(28, 'IGST rate cannot exceed 28%')
    }),
    international: z.array(z.object({
      country: z.string().min(1, 'Country is required'),
      rate: z.number().min(0).max(100, 'Tax rate cannot exceed 100%')
    }))
  }),
  deliveryPartners: z.array(z.string()).min(1, 'At least one delivery partner must be selected')
});

// Step 5: Store Customization & Themes
export const customizationSchema = z.object({
  theme: z.string().min(1, 'Please select a theme'),
  layout: z.object({
    homepage: z.string().min(1, 'Please select a homepage layout'),
    navigation: z.array(z.object({
      label: z.string().min(1, 'Navigation label is required'),
      url: z.string().url('Please enter a valid URL'),
      children: z.array(z.object({
        label: z.string().min(1, 'Sub-navigation label is required'),
        url: z.string().url('Please enter a valid URL')
      })).optional()
    })),
    footer: z.object({
      copyright: z.string().min(1, 'Copyright text is required'),
      links: z.array(z.object({
        label: z.string().min(1, 'Footer link label is required'),
        url: z.string().url('Please enter a valid URL')
      }))
    })
  }),
  seo: z.object({
    title: z.string().min(10, 'SEO title must be at least 10 characters').max(60, 'SEO title should not exceed 60 characters'),
    description: z.string().min(50, 'SEO description must be at least 50 characters').max(160, 'SEO description should not exceed 160 characters'),
    keywords: z.array(z.string()).min(3, 'At least 3 keywords are recommended').max(10, 'Too many keywords')
  }),
  socialMedia: z.object({
    facebook: z.string().url('Please enter a valid Facebook URL').optional(),
    instagram: z.string().url('Please enter a valid Instagram URL').optional(),
    twitter: z.string().url('Please enter a valid Twitter URL').optional(),
    youtube: z.string().url('Please enter a valid YouTube URL').optional()
  })
});

// Step 6: Launch Preparation
export const launchSchema = z.object({
  domain: z.object({
    custom: z.string().regex(/^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$/, 'Please enter a valid domain name').optional(),
    subdomain: z.string().regex(/^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]$/, 'Please enter a valid subdomain'),
    sslEnabled: z.boolean()
  }),
  analytics: z.object({
    googleAnalytics: z.string().regex(/^G-[A-Z0-9]{10}$/, 'Please enter a valid Google Analytics ID').optional(),
    facebookPixel: z.string().regex(/^[0-9]{15,16}$/, 'Please enter a valid Facebook Pixel ID').optional()
  }),
  marketing: z.object({
    emailSequences: z.boolean(),
    socialMediaCampaigns: z.boolean()
  }),
  launchChecklist: z.record(z.boolean()),
  isLive: z.boolean()
});

// Complete store setup schema
export const storeSetupSchema = z.object({
  storeInfo: storeInfoSchema,
  productCatalog: productCatalogSchema,
  paymentGateways: paymentGatewaysSchema,
  shippingAndTax: shippingAndTaxSchema,
  customization: customizationSchema,
  launch: launchSchema
});

export type StoreInfoFormData = z.infer<typeof storeInfoSchema>;
export type ProductCatalogFormData = z.infer<typeof productCatalogSchema>;
export type PaymentGatewaysFormData = z.infer<typeof paymentGatewaysSchema>;
export type ShippingAndTaxFormData = z.infer<typeof shippingAndTaxSchema>;
export type CustomizationFormData = z.infer<typeof customizationSchema>;
export type LaunchFormData = z.infer<typeof launchSchema>;
export type StoreSetupFormData = z.infer<typeof storeSetupSchema>;
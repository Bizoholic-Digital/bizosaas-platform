import { BusinessTemplate, PaymentGateway, ShippingZone, Theme } from './types';

export const BUSINESS_TEMPLATES: BusinessTemplate[] = [
  {
    id: 'fashion-apparel',
    name: 'Fashion & Apparel',
    description: 'Perfect for clothing, accessories, and footwear stores',
    categories: ['Men\'s Clothing', 'Women\'s Clothing', 'Accessories', 'Footwear', 'Bags'],
    defaultTheme: 'fashion-pro',
    recommendedPaymentGateways: ['razorpay', 'payu', 'stripe'],
    sampleProducts: [
      { name: 'Cotton T-Shirt', category: 'Men\'s Clothing', price: 599 },
      { name: 'Designer Saree', category: 'Women\'s Clothing', price: 2999 },
      { name: 'Leather Wallet', category: 'Accessories', price: 899 }
    ],
    gstConfiguration: {
      hsnCodes: ['6109', '6204', '4202'],
      defaultRate: 12
    }
  },
  {
    id: 'electronics',
    name: 'Electronics & Gadgets',
    description: 'For mobile phones, computers, and electronic accessories',
    categories: ['Mobile Phones', 'Laptops', 'Accessories', 'Home Appliances', 'Gaming'],
    defaultTheme: 'tech-modern',
    recommendedPaymentGateways: ['razorpay', 'payu', 'ccavenue'],
    sampleProducts: [
      { name: 'Smartphone', category: 'Mobile Phones', price: 15999 },
      { name: 'Wireless Earbuds', category: 'Accessories', price: 2499 },
      { name: 'Gaming Mouse', category: 'Gaming', price: 1299 }
    ],
    gstConfiguration: {
      hsnCodes: ['8517', '8471', '8518'],
      defaultRate: 18
    }
  },
  {
    id: 'home-garden',
    name: 'Home & Garden',
    description: 'Furniture, home decor, and kitchen essentials',
    categories: ['Furniture', 'Home Decor', 'Kitchen', 'Garden', 'Storage'],
    defaultTheme: 'home-elegant',
    recommendedPaymentGateways: ['razorpay', 'payu'],
    sampleProducts: [
      { name: 'Wooden Coffee Table', category: 'Furniture', price: 8999 },
      { name: 'Decorative Vase', category: 'Home Decor', price: 1499 },
      { name: 'Non-stick Pan Set', category: 'Kitchen', price: 2999 }
    ],
    gstConfiguration: {
      hsnCodes: ['9403', '6913', '7323'],
      defaultRate: 18
    }
  },
  {
    id: 'health-beauty',
    name: 'Health & Beauty',
    description: 'Cosmetics, wellness products, and personal care',
    categories: ['Skincare', 'Makeup', 'Hair Care', 'Wellness', 'Personal Care'],
    defaultTheme: 'beauty-spa',
    recommendedPaymentGateways: ['razorpay', 'payu', 'stripe'],
    sampleProducts: [
      { name: 'Moisturizing Cream', category: 'Skincare', price: 799 },
      { name: 'Lipstick Set', category: 'Makeup', price: 1299 },
      { name: 'Hair Oil', category: 'Hair Care', price: 499 }
    ],
    gstConfiguration: {
      hsnCodes: ['3304', '3305', '3401'],
      defaultRate: 18
    }
  },
  {
    id: 'books-media',
    name: 'Books & Media',
    description: 'Books, digital content, and educational materials',
    categories: ['Fiction', 'Non-Fiction', 'Educational', 'Digital Content', 'Stationery'],
    defaultTheme: 'bookstore-classic',
    recommendedPaymentGateways: ['razorpay', 'stripe', 'paypal'],
    sampleProducts: [
      { name: 'Business Strategy Book', category: 'Non-Fiction', price: 699 },
      { name: 'Online Course', category: 'Digital Content', price: 2999 },
      { name: 'Notebook Set', category: 'Stationery', price: 299 }
    ],
    gstConfiguration: {
      hsnCodes: ['4901', '4820', '9999'],
      defaultRate: 5
    }
  },
  {
    id: 'handcrafts',
    name: 'Handcrafts & Traditional',
    description: 'Traditional Indian crafts, jewelry, and handmade items',
    categories: ['Jewelry', 'Handicrafts', 'Traditional Wear', 'Art', 'Religious Items'],
    defaultTheme: 'heritage-craft',
    recommendedPaymentGateways: ['razorpay', 'payu'],
    sampleProducts: [
      { name: 'Silver Earrings', category: 'Jewelry', price: 1999 },
      { name: 'Wooden Sculpture', category: 'Handicrafts', price: 3499 },
      { name: 'Silk Dupatta', category: 'Traditional Wear', price: 1299 }
    ],
    gstConfiguration: {
      hsnCodes: ['7113', '4420', '5007'],
      defaultRate: 3
    }
  },
  {
    id: 'food-beverages',
    name: 'Food & Beverages',
    description: 'Packaged foods, spices, and beverages',
    categories: ['Spices', 'Snacks', 'Beverages', 'Organic Food', 'Packaged Food'],
    defaultTheme: 'food-fresh',
    recommendedPaymentGateways: ['razorpay', 'payu'],
    sampleProducts: [
      { name: 'Organic Turmeric', category: 'Spices', price: 299 },
      { name: 'Healthy Snack Mix', category: 'Snacks', price: 199 },
      { name: 'Herbal Tea', category: 'Beverages', price: 449 }
    ],
    gstConfiguration: {
      hsnCodes: ['0910', '1905', '0902'],
      defaultRate: 5
    }
  }
];

export const PAYMENT_GATEWAYS: PaymentGateway[] = [
  {
    id: 'razorpay',
    name: 'Razorpay',
    logo: '/icons/razorpay.svg',
    description: 'Most popular payment gateway in India with comprehensive features',
    feeStructure: {
      domestic: { percentage: 2.0, fixedFee: 0 },
      international: { percentage: 3.0, fixedFee: 0 }
    },
    supportedCurrencies: ['INR', 'USD', 'EUR', 'GBP'],
    features: ['UPI', 'Net Banking', 'Cards', 'Wallets', 'EMI', 'Subscriptions'],
    setup: {
      testMode: true,
      requiredFields: [
        { name: 'key_id', label: 'Key ID', type: 'text', required: true },
        { name: 'key_secret', label: 'Key Secret', type: 'password', required: true },
        { name: 'webhook_secret', label: 'Webhook Secret', type: 'password', required: false }
      ]
    }
  },
  {
    id: 'payu',
    name: 'PayU',
    logo: '/icons/payu.svg',
    description: 'Trusted payment solution with strong fraud protection',
    feeStructure: {
      domestic: { percentage: 2.0, fixedFee: 0 },
      international: { percentage: 3.5, fixedFee: 0 }
    },
    supportedCurrencies: ['INR', 'USD'],
    features: ['Cards', 'Net Banking', 'UPI', 'Wallets', 'EMI'],
    setup: {
      testMode: true,
      requiredFields: [
        { name: 'merchant_key', label: 'Merchant Key', type: 'text', required: true },
        { name: 'merchant_salt', label: 'Merchant Salt', type: 'password', required: true },
        { name: 'auth_header', label: 'Auth Header', type: 'text', required: false }
      ]
    }
  },
  {
    id: 'ccavenue',
    name: 'CCAvenue',
    logo: '/icons/ccavenue.svg',
    description: 'Established payment gateway with extensive banking partnerships',
    feeStructure: {
      domestic: { percentage: 2.25, fixedFee: 0 },
      international: { percentage: 3.5, fixedFee: 0 }
    },
    supportedCurrencies: ['INR', 'USD', 'EUR'],
    features: ['Cards', 'Net Banking', 'Wallets', 'International Cards'],
    setup: {
      testMode: true,
      requiredFields: [
        { name: 'merchant_id', label: 'Merchant ID', type: 'text', required: true },
        { name: 'access_code', label: 'Access Code', type: 'text', required: true },
        { name: 'working_key', label: 'Working Key', type: 'password', required: true }
      ]
    }
  },
  {
    id: 'stripe',
    name: 'Stripe',
    logo: '/icons/stripe.svg',
    description: 'Global payment platform ideal for international businesses',
    feeStructure: {
      domestic: { percentage: 2.9, fixedFee: 30 },
      international: { percentage: 3.4, fixedFee: 30 }
    },
    supportedCurrencies: ['USD', 'EUR', 'GBP', 'INR', 'AUD'],
    features: ['Cards', 'Digital Wallets', 'Subscriptions', 'Marketplace'],
    setup: {
      testMode: true,
      requiredFields: [
        { name: 'publishable_key', label: 'Publishable Key', type: 'text', required: true },
        { name: 'secret_key', label: 'Secret Key', type: 'password', required: true },
        { name: 'webhook_endpoint_secret', label: 'Webhook Secret', type: 'password', required: false }
      ]
    }
  },
  {
    id: 'paypal',
    name: 'PayPal',
    logo: '/icons/paypal.svg',
    description: 'Widely recognized international payment solution',
    feeStructure: {
      domestic: { percentage: 3.0, fixedFee: 30 },
      international: { percentage: 4.4, fixedFee: 30 }
    },
    supportedCurrencies: ['USD', 'EUR', 'GBP', 'AUD', 'CAD'],
    features: ['PayPal Balance', 'Cards', 'Buyer Protection'],
    setup: {
      testMode: true,
      requiredFields: [
        { name: 'client_id', label: 'Client ID', type: 'text', required: true },
        { name: 'client_secret', label: 'Client Secret', type: 'password', required: true }
      ]
    }
  }
];

export const SHIPPING_ZONES: ShippingZone[] = [
  {
    id: 'domestic-metro',
    name: 'Metro Cities',
    type: 'domestic',
    coverage: {
      states: ['Delhi', 'Maharashtra', 'Karnataka', 'Tamil Nadu', 'West Bengal']
    },
    methods: [
      {
        id: 'express',
        name: 'Express Delivery',
        description: 'Next day delivery in metro cities',
        calculation: 'flat',
        rate: 99,
        freeThreshold: 499,
        estimatedDays: '1-2 days'
      },
      {
        id: 'standard',
        name: 'Standard Delivery',
        description: 'Regular delivery',
        calculation: 'flat',
        rate: 49,
        freeThreshold: 799,
        estimatedDays: '3-5 days'
      }
    ]
  },
  {
    id: 'domestic-tier1',
    name: 'Tier 1 Cities',
    type: 'domestic',
    coverage: {
      states: ['Gujarat', 'Rajasthan', 'Punjab', 'Haryana', 'Uttar Pradesh', 'Madhya Pradesh']
    },
    methods: [
      {
        id: 'standard',
        name: 'Standard Delivery',
        description: 'Regular delivery to tier 1 cities',
        calculation: 'flat',
        rate: 69,
        freeThreshold: 999,
        estimatedDays: '3-7 days'
      }
    ]
  },
  {
    id: 'domestic-tier2',
    name: 'Tier 2/3 Cities & Rural',
    type: 'domestic',
    coverage: {
      states: ['All Other States']
    },
    methods: [
      {
        id: 'standard',
        name: 'Standard Delivery',
        description: 'Delivery to smaller cities and rural areas',
        calculation: 'flat',
        rate: 99,
        freeThreshold: 1499,
        estimatedDays: '5-10 days'
      }
    ]
  },
  {
    id: 'international',
    name: 'International',
    type: 'international',
    coverage: {
      countries: ['USA', 'Canada', 'UK', 'Australia', 'UAE', 'Singapore']
    },
    methods: [
      {
        id: 'international-express',
        name: 'International Express',
        description: 'Fast international shipping',
        calculation: 'weight',
        rate: 1500,
        estimatedDays: '7-14 days'
      },
      {
        id: 'international-standard',
        name: 'International Standard',
        description: 'Economy international shipping',
        calculation: 'weight',
        rate: 800,
        estimatedDays: '14-21 days'
      }
    ]
  }
];

export const THEMES: Theme[] = [
  {
    id: 'fashion-pro',
    name: 'Fashion Pro',
    description: 'Modern and stylish theme perfect for fashion brands',
    preview: '/themes/fashion-pro.jpg',
    category: 'Fashion',
    features: ['Product zoom', 'Color swatches', 'Size guides', 'Instagram feed'],
    customizable: { colors: true, fonts: true, layout: true },
    responsive: true,
    price: 0
  },
  {
    id: 'tech-modern',
    name: 'Tech Modern',
    description: 'Clean and technical design for electronics stores',
    preview: '/themes/tech-modern.jpg',
    category: 'Electronics',
    features: ['Comparison tables', 'Product filters', 'Reviews system', 'Tech specs'],
    customizable: { colors: true, fonts: true, layout: true },
    responsive: true,
    price: 0
  },
  {
    id: 'home-elegant',
    name: 'Home Elegant',
    description: 'Elegant and sophisticated theme for home decor',
    preview: '/themes/home-elegant.jpg',
    category: 'Home & Garden',
    features: ['Room visualizer', 'Material samples', 'Inspiration gallery', 'Wishlist'],
    customizable: { colors: true, fonts: true, layout: true },
    responsive: true,
    price: 0
  },
  {
    id: 'beauty-spa',
    name: 'Beauty Spa',
    description: 'Luxurious theme for beauty and wellness brands',
    preview: '/themes/beauty-spa.jpg',
    category: 'Beauty',
    features: ['Ingredient lists', 'Skin type quiz', 'Beauty tips blog', 'Rewards program'],
    customizable: { colors: true, fonts: true, layout: true },
    responsive: true,
    price: 0
  },
  {
    id: 'bookstore-classic',
    name: 'Bookstore Classic',
    description: 'Traditional and warm design for book retailers',
    preview: '/themes/bookstore-classic.jpg',
    category: 'Books',
    features: ['Reading lists', 'Author profiles', 'Book previews', 'Reading club'],
    customizable: { colors: true, fonts: true, layout: false },
    responsive: true,
    price: 0
  },
  {
    id: 'heritage-craft',
    name: 'Heritage Craft',
    description: 'Traditional Indian design for handicrafts and art',
    preview: '/themes/heritage-craft.jpg',
    category: 'Handicrafts',
    features: ['Artisan stories', 'Cultural context', 'Custom orders', 'Gift wrapping'],
    customizable: { colors: true, fonts: false, layout: true },
    responsive: true,
    price: 0
  },
  {
    id: 'food-fresh',
    name: 'Food Fresh',
    description: 'Fresh and appetizing theme for food businesses',
    preview: '/themes/food-fresh.jpg',
    category: 'Food',
    features: ['Recipe integration', 'Nutrition facts', 'Expiry tracking', 'Subscription boxes'],
    customizable: { colors: true, fonts: true, layout: true },
    responsive: true,
    price: 0
  }
];

export const INDIAN_STATES = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
  'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
  'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
  'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
  'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
  'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu',
  'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
];

export const CURRENCIES = [
  { code: 'INR', name: 'Indian Rupee', symbol: '₹' },
  { code: 'USD', name: 'US Dollar', symbol: '$' },
  { code: 'EUR', name: 'Euro', symbol: '€' },
  { code: 'GBP', name: 'British Pound', symbol: '£' },
  { code: 'AUD', name: 'Australian Dollar', symbol: 'A$' },
  { code: 'CAD', name: 'Canadian Dollar', symbol: 'C$' }
];

export const BUSINESS_TYPES = [
  'Sole Proprietorship',
  'Partnership',
  'Private Limited Company',
  'Public Limited Company',
  'Limited Liability Partnership (LLP)',
  'One Person Company (OPC)',
  'Non-Profit Organization'
];

export const DIGITAL_WALLETS = [
  { id: 'phonepe', name: 'PhonePe', icon: '/icons/phonepe.svg' },
  { id: 'googlepay', name: 'Google Pay', icon: '/icons/googlepay.svg' },
  { id: 'paytm', name: 'Paytm', icon: '/icons/paytm.svg' },
  { id: 'amazonpay', name: 'Amazon Pay', icon: '/icons/amazonpay.svg' },
  { id: 'mobikwik', name: 'MobiKwik', icon: '/icons/mobikwik.svg' },
  { id: 'freecharge', name: 'FreeCharge', icon: '/icons/freecharge.svg' }
];

export const DELIVERY_PARTNERS = [
  { id: 'bluedart', name: 'BlueDart', icon: '/icons/bluedart.svg' },
  { id: 'fedex', name: 'FedEx', icon: '/icons/fedex.svg' },
  { id: 'dhl', name: 'DHL', icon: '/icons/dhl.svg' },
  { id: 'indiapost', name: 'India Post', icon: '/icons/indiapost.svg' },
  { id: 'dtdc', name: 'DTDC', icon: '/icons/dtdc.svg' },
  { id: 'ekart', name: 'Ekart (Flipkart)', icon: '/icons/ekart.svg' },
  { id: 'delhivery', name: 'Delhivery', icon: '/icons/delhivery.svg' }
];

export const LAUNCH_CHECKLIST_ITEMS = [
  { id: 'domain_configured', label: 'Domain name configured and SSL enabled', critical: true },
  { id: 'payment_tested', label: 'Payment gateways tested in live mode', critical: true },
  { id: 'products_added', label: 'At least 5 products added with images', critical: true },
  { id: 'shipping_configured', label: 'Shipping zones and rates configured', critical: true },
  { id: 'tax_setup', label: 'Tax configuration completed', critical: true },
  { id: 'legal_pages', label: 'Legal pages added (Privacy Policy, Terms)', critical: true },
  { id: 'analytics_setup', label: 'Analytics and tracking configured', critical: false },
  { id: 'social_media', label: 'Social media accounts linked', critical: false },
  { id: 'email_sequences', label: 'Welcome email sequence configured', critical: false },
  { id: 'backup_plan', label: 'Data backup and recovery plan in place', critical: false }
];
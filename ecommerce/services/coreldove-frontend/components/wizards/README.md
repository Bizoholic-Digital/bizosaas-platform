# CoreLDove E-commerce Store Setup Wizard

A comprehensive 6-step wizard for setting up e-commerce stores on the CoreLDove platform, specifically designed for Indian market requirements with multi-currency support and international capabilities.

## Features

### 🏪 **Step 1: Store Information & Branding**
- Store name, description, and business type selection
- Logo upload with preview functionality
- Brand color picker with predefined color palette
- Complete contact information including Indian address validation
- Multi-currency support (INR primary, international options)
- Indian business registration (GST, PAN, Registration Number)

### 📦 **Step 2: Product Catalog Setup**
- Business template selection with pre-configured categories
- Multiple import methods:
  - Manual product entry
  - CSV bulk upload with downloadable template
  - Excel file import
  - API integration for existing catalogs
- Product management with image uploads
- Pricing strategies (fixed, dynamic, tiered)
- Inventory tracking configuration
- Category management system

### 💳 **Step 3: Payment Gateway Configuration**
- **Indian Focus**: Razorpay, PayU, CCAvenue, Paytm
- **International**: Stripe, PayPal
- **Digital Wallets**: PhonePe, Google Pay, Amazon Pay, Paytm
- Real-time fee calculation and comparison
- Test mode and live mode configuration
- Payment method prioritization
- Connection testing functionality

### 🚚 **Step 4: Shipping & Tax Configuration**
- **Shipping Zones**:
  - Predefined Indian zones (Metro, Tier 1, Tier 2/3)
  - International shipping configuration
  - Multiple delivery methods per zone
  - Free shipping thresholds
- **GST Configuration**:
  - CGST, SGST, IGST rate setup
  - Automatic tax calculation
  - HSN code support
- **International Tax**: Country-specific rates
- **Delivery Partners**: BlueDart, FedEx, DHL, India Post, DTDC

### 🎨 **Step 5: Store Customization & Themes**
- **Theme Selection**: 7 professionally designed themes
  - Fashion Pro, Tech Modern, Home Elegant
  - Beauty Spa, Bookstore Classic, Heritage Craft, Food Fresh
- **Layout Configuration**: Homepage layouts and navigation setup
- **SEO Optimization**: Title, description, keywords with character limits
- **Social Media Integration**: Facebook, Instagram, Twitter, YouTube
- **Preview Functionality**: Desktop and mobile previews

### 🚀 **Step 6: Launch Preparation & Go-Live**
- **Domain Setup**: CoreLDove subdomain + custom domain support
- **SSL Configuration**: Automatic SSL certificate setup
- **Analytics Integration**: Google Analytics 4, Facebook Pixel
- **Marketing Automation**: Email sequences, social campaigns
- **Pre-Launch Testing**: Automated testing for all systems
- **Launch Checklist**: 10-item comprehensive checklist
- **Go-Live Process**: One-click store launch

## Technical Architecture

### **Frontend Framework**
- **Next.js 15** with TypeScript for modern React development
- **ShadCN UI Components** for consistent design system
- **React Hook Form** with Zod validation for robust form handling
- **Zustand** for global state management with persistence
- **Tailwind CSS** for responsive design and styling

### **State Management**
- Persistent state with localStorage backup
- Auto-save functionality every 30 seconds
- Step-by-step validation with real-time feedback
- Progress tracking with percentage completion
- Draft management for incomplete setups

### **Validation & Error Handling**
- **Zod schemas** for type-safe validation
- Real-time field validation with helpful error messages
- Cross-field validation (e.g., GST number format)
- Required field indicators and form submission blocking
- Comprehensive error boundary with user-friendly messages

### **Data Flow**
```
User Input → Form Validation → Zustand Store → Auto-save → API Integration
     ↓
Progress Tracking → Step Completion → Launch Preparation → Store Creation
```

## Indian Market Specialization

### **Business Compliance**
- GST registration validation with proper format checking
- PAN number validation and optional linking
- Indian business types support
- State-wise shipping configuration
- Indian pincode validation

### **Payment Ecosystem**
- UPI integration support
- Net banking for all major Indian banks
- Digital wallet ecosystem (PhonePe, Google Pay, etc.)
- EMI options for high-value purchases
- Cash on Delivery (COD) configuration

### **Logistics & Delivery**
- Pincode-based delivery estimation
- Major Indian courier partners integration
- Zone-wise shipping calculation
- Festival season surge pricing
- Return and exchange policy templates

### **Localization**
- Multi-language support preparation (Hindi, Regional)
- Indian currency formatting (₹)
- Local business hour settings
- Festival calendar integration
- Regional payment preference settings

## Usage Examples

### **Basic Implementation**
```tsx
import { EcommerceStoreWizard } from '@/components/wizards';

function StoreSetupPage() {
  const handleComplete = async (data: StoreSetupData) => {
    // Send to Brain API
    await fetch('/api/store-setup', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  };

  return (
    <EcommerceStoreWizard
      onComplete={handleComplete}
      onSave={(data) => localStorage.setItem('progress', JSON.stringify(data))}
    />
  );
}
```

### **With Initial Data**
```tsx
const initialData = {
  storeInfo: {
    name: 'My Store',
    businessType: 'Private Limited Company',
    currency: { primary: 'INR', supported: ['INR', 'USD'] }
  }
};

<EcommerceStoreWizard
  initialData={initialData}
  onComplete={handleComplete}
  readonly={false}
/>
```

### **Step-by-Step Access**
```tsx
import { 
  StoreInfoStep, 
  ProductCatalogStep,
  PaymentGatewaysStep 
} from '@/components/wizards';

// Use individual steps for custom workflows
function CustomSetup() {
  return (
    <div>
      <StoreInfoStep data={storeData} onChange={updateStore} />
      <ProductCatalogStep data={catalogData} onChange={updateCatalog} />
    </div>
  );
}
```

## API Integration

### **Brain API Endpoints**
- `POST /api/ecommerce/store-setup` - Complete store creation
- `POST /api/ecommerce/store-setup/save` - Save progress
- `GET /api/ecommerce/store-setup/load` - Load saved progress
- `POST /api/ecommerce/validate-domain` - Domain availability check
- `POST /api/ecommerce/test-payment` - Payment gateway testing

### **Data Structure**
```typescript
interface StoreSetupData {
  storeInfo: StoreInfo;
  productCatalog: ProductCatalog;
  paymentGateways: PaymentGateways;
  shippingAndTax: ShippingAndTax;
  customization: Customization;
  launch: LaunchConfiguration;
}
```

## Performance Optimizations

### **Code Splitting**
- Lazy loading of wizard steps
- Dynamic import of payment gateway configurations
- Progressive image loading for themes and previews

### **Bundle Size**
- Tree-shaking for unused components
- Minimal external dependencies
- Optimized icon usage with Lucide React

### **User Experience**
- Auto-save every 30 seconds
- Optimistic UI updates
- Loading states for all async operations
- Progressive disclosure of complex forms
- Mobile-first responsive design

## Accessibility Features

### **WCAG 2.1 AA Compliance**
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support
- Focus management across steps
- Alternative text for all images

### **Form Accessibility**
- Proper ARIA labels and descriptions
- Error message association
- Required field indicators
- Logical tab order
- Form validation announcements

## Testing

### **Unit Tests**
- Form validation logic
- State management functions
- Individual component rendering
- Utility function testing

### **Integration Tests**
- Multi-step wizard flow
- Data persistence across steps
- API integration testing
- Payment gateway connections

### **E2E Tests**
- Complete store setup workflow
- Error handling scenarios
- Different business template flows
- Mobile responsiveness testing

## Browser Support

- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: iOS Safari 14+, Android Chrome 90+
- **Progressive Enhancement**: Graceful degradation for older browsers

## Deployment

### **Environment Variables**
```env
NEXT_PUBLIC_BRAIN_API_URL=http://bizosaas-brain:8001
NEXT_PUBLIC_CORELDOVE_DOMAIN=coreldove.com
NEXT_PUBLIC_ANALYTICS_ID=G-XXXXXXXXXX
```

### **Build Configuration**
```javascript
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: ['lucide-react']
  },
  images: {
    domains: ['images.coreldove.com']
  }
};
```

## Contributing

### **Development Setup**
```bash
npm install
npm run dev
```

### **Code Standards**
- TypeScript strict mode
- ESLint + Prettier configuration
- Conventional commit messages
- Component documentation requirements

### **Adding New Features**
1. Create feature branch
2. Add TypeScript types
3. Implement component with validation
4. Add tests and documentation
5. Submit PR with demo

## Roadmap

### **Phase 2 Features**
- [ ] Advanced analytics dashboard
- [ ] A/B testing for themes
- [ ] Multi-store management
- [ ] Advanced SEO tools
- [ ] Marketplace integrations

### **Phase 3 Features**
- [ ] AI-powered store optimization
- [ ] Voice commerce setup
- [ ] AR/VR product preview
- [ ] Advanced inventory management
- [ ] Customer segmentation tools

## Support

For technical support and feature requests:
- **Documentation**: [CoreLDove Docs](https://docs.coreldove.com)
- **Community**: [Discord Server](https://discord.gg/coreldove)
- **Issues**: [GitHub Issues](https://github.com/coreldove/platform/issues)
- **Email**: support@coreldove.com

---

Built with ❤️ for the Indian e-commerce ecosystem by the CoreLDove team.
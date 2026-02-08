export type PaymentGateway = 'razorpay' | 'paypal' | 'payu' | 'stripe';

export interface PaymentGatewayConfig {
    enabled: boolean;
    label: string;
}

export const paymentGateways: Record<PaymentGateway, PaymentGatewayConfig> = {
    razorpay: { enabled: true, label: 'Razorpay' },
    paypal: { enabled: true, label: 'PayPal' },
    payu: { enabled: true, label: 'PayU' },
    stripe: { enabled: true, label: 'Stripe' },
};

export interface SubscriptionPlan {
    id: string;
    name: string;
    description: string;
    popular?: boolean;
    features: string[];
    pricing: {
        INR: { monthly: number; yearly: number };
        USD: { monthly: number; yearly: number };
    };
}

export const subscriptionPlans: SubscriptionPlan[] = [
    {
        id: 'starter',
        name: 'Starter',
        description: 'Perfect for individuals and small startups',
        features: ['Up to 5 AI Agents', 'Basic Analytics', 'Community Support'],
        pricing: {
            INR: { monthly: 2999, yearly: 29990 },
            USD: { monthly: 39, yearly: 390 }
        }
    },
    {
        id: 'professional',
        name: 'Professional',
        description: 'Best for growing businesses',
        popular: true,
        features: ['Up to 20 AI Agents', 'Advanced Analytics', 'Priority Support', 'Custom Integrations'],
        pricing: {
            INR: { monthly: 6999, yearly: 69990 },
            USD: { monthly: 89, yearly: 890 }
        }
    },
    {
        id: 'enterprise',
        name: 'Enterprise',
        description: 'Full-scale solution for large organizations',
        features: ['Unlimited AI Agents', 'Real-time Analytics', '24/7 Dedicated Support', 'White-labeling'],
        pricing: {
            INR: { monthly: 19999, yearly: 199990 },
            USD: { monthly: 249, yearly: 2490 }
        }
    }
];

export const paymentUtils = {
    formatPrice: (amount: number, currency: 'INR' | 'USD') => {
        return new Intl.NumberFormat(currency === 'INR' ? 'en-IN' : 'en-US', {
            style: 'currency',
            currency,
            minimumFractionDigits: 0,
        }).format(amount / 100);
    },
    getGatewayDisplayName: (gateway: PaymentGateway) => {
        return paymentGateways[gateway]?.label || gateway;
    }
};

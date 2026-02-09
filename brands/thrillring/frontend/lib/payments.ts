const processPayment = async () => {
    console.warn("Payments stub called");
    return { success: false, message: "Not implemented" };
};

const getPaymentHistory = async () => {
    return [];
};


export type Currency = 'USD' | 'EUR' | 'GBP';

export const subscriptionPlans = [
    {
        id: 'starter',
        name: 'Starter',
        price: 29,
        description: 'Perfect for small businesses',
        features: ['Up to 5 AI Agents', 'Basic Analytics', 'Email Support'],
        popular: false
    },
    {
        id: 'professional',
        name: 'Professional',
        price: 79,
        description: 'For growing companies',
        features: ['Unlimited AI Agents', 'Advanced Analytics', 'Priority Support', 'Custom Integration'],
        popular: true
    },
    {
        id: 'enterprise',
        name: 'Enterprise',
        price: 299,
        description: 'Full-scale solution',
        features: ['Dedicated Account Manager', 'SLA', 'Custom Development', 'White-labeling'],
        popular: false
    }
];

export const subscriptionMetrics = {
    revenue: 0,
    activeSubscriptions: 0,
    churnRate: 0
};

export const paymentUtils = {
    processPayment,
    getPaymentHistory,
    subscriptionPlans,
    subscriptionMetrics,
    getPlanPrice: (plan: any, currency: Currency, billingCycle: 'monthly' | 'yearly') => {
        let price = plan.price;
        if (billingCycle === 'yearly') {
            price = price * 12 * 0.8; // 20% discount
        }
        return price;
    },
    formatPrice: (price: number, currency: Currency) => {
        return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(price);
    },
    getSavingsPercentage: (plan: any, currency: Currency) => 20
};

export const paymentGateways = [
    { id: 'stripe', name: 'Stripe', status: 'active' },
    { id: 'paypal', name: 'PayPal', status: 'available' }
];

export default paymentUtils;

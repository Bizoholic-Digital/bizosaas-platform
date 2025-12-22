import { brainApi, ApiResponse } from './brain-client';

export interface SubscriptionPlan {
    id: string;
    name: string;
    code: string;
    amount: number;
    currency: string;
    interval: string;
    trial_period_days?: number;
}

export interface Customer {
    id?: string;
    email: string;
    name?: string;
    currency?: string;
    metadata?: Record<string, any>;
}

export interface Subscription {
    id: string;
    plan_id: string;
    status: string;
    current_period_end: string;
}

export interface Invoice {
    id: string;
    amount_due: number;
    currency: string;
    status: string;
    created_at: string;
    pdf_url?: string;
}

export class BillingApi {
    async getStatus(): Promise<ApiResponse<{ connected: boolean; platform?: string }>> {
        return brainApi.get<{ connected: boolean; platform?: string }>('/api/brain/billing/status');
    }

    async getPlans(): Promise<ApiResponse<SubscriptionPlan[]>> {
        return brainApi.get<SubscriptionPlan[]>('/api/brain/billing/plans');
    }

    async createCustomer(customer: Customer): Promise<ApiResponse<Customer>> {
        return brainApi.post('/api/brain/billing/customers', customer);
    }

    async createSubscription(planCode: string): Promise<ApiResponse<Subscription>> {
        return brainApi.post(`/api/brain/billing/subscriptions`, { plan_code: planCode });
    }

    async getSubscriptions(): Promise<ApiResponse<Subscription[]>> {
        return brainApi.get<Subscription[]>('/api/brain/billing/subscriptions');
    }

    async getInvoices(): Promise<ApiResponse<Invoice[]>> {
        return brainApi.get<Invoice[]>('/api/brain/billing/invoices');
    }
}

export const billingApi = new BillingApi();

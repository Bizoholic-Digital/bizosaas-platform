import { brainApi, ApiResponse } from './brain-client';

export interface SubscriptionPlan {
    id: string;
    name: string;
    slug: string;
    amount: number;
    currency: string;
    interval: string;
    description?: string;
}

export interface Subscription {
    id: string;
    plan_slug: string;
    status: string;
    current_period_end: string;
}

export interface Invoice {
    id: string;
    amount: number;
    currency: string;
    status: string;
    created_at: string;
    paid_at?: string;
    pdf_url?: string;
}

export class BillingApi {
    async getStatus(): Promise<ApiResponse<{ connected: boolean; platform?: string }>> {
        return brainApi.get<{ connected: boolean; platform?: string }>('/api/brain/billing/status');
    }

    async getPlans(): Promise<ApiResponse<SubscriptionPlan[]>> {
        return brainApi.get<SubscriptionPlan[]>('/api/brain/billing/plans');
    }

    async getSubscription(): Promise<ApiResponse<Subscription>> {
        return brainApi.get<Subscription>('/api/brain/billing/subscription');
    }

    async subscribe(planSlug: string): Promise<ApiResponse<Subscription>> {
        return brainApi.post(`/api/brain/billing/subscribe?plan_slug=${planSlug}`, {});
    }

    async getInvoices(): Promise<ApiResponse<Invoice[]>> {
        return brainApi.get<Invoice[]>('/api/brain/billing/invoices');
    }
}

export const billingApi = new BillingApi();

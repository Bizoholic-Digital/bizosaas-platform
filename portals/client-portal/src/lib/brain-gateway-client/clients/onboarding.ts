import { apiClient } from '../utils/base-client'

export interface BusinessProfile {
    name: string
    description: string
    category: string
    subcategory: string
    keywords: string[]
    address: {
        street: string
        city: string
        state: string
        zipCode: string
        country: string
    }
    contact: {
        phone: string
        email: string
        website: string
    }
}

export interface OnboardingStatus {
    step: string
    is_completed: boolean
    last_updated: string
}

export class OnboardingClient {
    private basePath = '/api/onboarding'

    async getStatus(): Promise<OnboardingStatus> {
        return apiClient.get<OnboardingStatus>(`${this.basePath}/status`)
    }

    async getBusinessProfile(): Promise<BusinessProfile> {
        return apiClient.get<BusinessProfile>(`${this.basePath}/business-profile`)
    }

    async updateBusinessProfile(data: BusinessProfile): Promise<any> {
        return apiClient.post(`${this.basePath}/business-profile`, data)
    }

    async saveDigitalPresence(data: any): Promise<any> {
        return apiClient.post(`${this.basePath}/digital-presence`, data)
    }

    async saveIntegrations(data: any): Promise<any> {
        return apiClient.post(`${this.basePath}/integrations`, data)
    }

    async discover(data: any): Promise<any> {
        return apiClient.post(`${this.basePath}/discover`, data)
    }

    async complete(): Promise<any> {
        return apiClient.post(`${this.basePath}/complete`, {})
    }
}

export const onboardingClient = new OnboardingClient()

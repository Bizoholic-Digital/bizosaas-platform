import { BaseApiClient } from '../utils/base-client'

export interface SocialPostRequest {
    platform: string
    topic: string
    persona_id?: string
    scheduled_at?: string
    require_approval?: boolean
    as_thread?: boolean
    context?: string
}

export class SocialClient {
    constructor(private apiClient: BaseApiClient) { }

    async generateContent(data: SocialPostRequest) {
        return this.apiClient.post<{ workflow_id: string; status: string }>('/social/generate', data)
    }

    async getStatus(workflowId: string) {
        return this.apiClient.get<{ workflow_id: string; status: string; draft: any }>(`/social/status/${workflowId}`)
    }

    async approvePost(workflowId: string, notes?: string) {
        return this.apiClient.post(`/social/approve/${workflowId}`, { notes })
    }

    async rejectPost(workflowId: string, notes: string) {
        return this.apiClient.post(`/social/reject/${workflowId}`, { notes })
    }
}

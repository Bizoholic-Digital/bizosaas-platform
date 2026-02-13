import { BaseApiClient } from '../utils/base-client'

export interface Persona {
    core_persona: {
        name: string
        role: string
        tone: string
        style: string
        values: string[]
        description: string
    }
    platform_variants?: Record<string, any>
}

export interface PersonaUpdateRequest {
    core_persona: Partial<Persona['core_persona']>
    platform_variants?: Record<string, any>
}

export class PersonaClient extends BaseApiClient {
    async getPersona(): Promise<Persona> {
        return this.get<Persona>('/api/persona/')
    }

    async generatePersona(params: { website_url?: string; onboarding_data?: any }): Promise<{ workflow_id: string }> {
        return this.post<{ workflow_id: string }>('/api/persona/generate', params)
    }

    async updatePersona(data: PersonaUpdateRequest): Promise<{ status: string }> {
        return this.put<{ status: string }>('/api/persona/', data)
    }
}

export const personaClient = new PersonaClient()

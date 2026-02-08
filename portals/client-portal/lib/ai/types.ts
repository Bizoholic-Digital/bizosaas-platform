/**
 * AI Agent System - Type Definitions
 * Core types for the AI agent infrastructure
 */

// ============================================================================
// Agent Types
// ============================================================================

export type AgentCategory =
    | 'general'
    | 'marketing'
    | 'content'
    | 'seo'
    | 'social_media'
    | 'analytics'
    | 'email_marketing'
    | 'crm'
    | 'ecommerce'
    | 'design'
    | 'automation'
    | 'research'
    | 'customer_support';

export type CostTier = 'free' | 'standard' | 'premium';

export type AgentStatus = 'active' | 'inactive' | 'maintenance' | 'error';

export interface AgentCapability {
    id: string;
    name: string;
    description: string;
    requiredTools?: string[];
    requiredServices?: string[];
}

export interface AgentMetadata {
    version: string;
    author: string;
    lastUpdated: string;
    tags: string[];
    documentation?: string;
}

export interface AIAgent {
    id: string;
    name: string;
    description: string;
    category: AgentCategory;
    capabilities: AgentCapability[];
    requiredTools: string[];
    requiredServices: string[];
    requiredAPIs: APIRequirement[];
    mcpServers?: string[];
    costTier: CostTier;
    permissions: string[];
    status: AgentStatus;
    metadata: AgentMetadata;
    promptTemplate?: string;
    systemPrompt?: string;
    modelPreferences?: ModelPreference[];
}

// ============================================================================
// Tool & Service Types
// ============================================================================

export type ToolType = 'api' | 'internal' | 'mcp' | 'direct';

export interface Tool {
    id: string;
    name: string;
    type: ToolType;
    description: string;
    category: string;
    requiredAPIs?: string[];
    configuration?: Record<string, any>;
    enabled: boolean;
}

export interface Service {
    id: string;
    name: string;
    category: string;
    description: string;
    apiEndpoint?: string;
    authType?: 'api_key' | 'oauth' | 'jwt' | 'none';
    requiredKeys?: string[];
    documentation?: string;
    healthCheckEndpoint?: string;
}

export interface MCPServer {
    id: string;
    name: string;
    description: string;
    endpoint: string;
    protocol: 'http' | 'websocket';
    capabilities: string[];
    enabled: boolean;
}

// ============================================================================
// API & Authentication Types
// ============================================================================

export interface APIRequirement {
    service: string;
    keyType: string;
    required: boolean;
    fallbackToPlatform?: boolean;
}

export interface APIKey {
    id: string;
    service: string;
    keyType: string;
    value: string; // Encrypted/masked
    tenantId?: string;
    createdAt: string;
    updatedAt: string;
    expiresAt?: string;
    lastUsed?: string;
    usageCount?: number;
    isValid: boolean;
}

// ============================================================================
// LLM Provider Types
// ============================================================================

export type LLMProvider = 'openai' | 'anthropic' | 'openrouter' | 'google' | 'local';

export interface ModelPreference {
    provider: LLMProvider;
    model: string;
    priority: number;
    maxTokens?: number;
    temperature?: number;
    topP?: number;
    frequencyPenalty?: number;
    presencePenalty?: number;
}

export interface LLMConfig {
    provider: LLMProvider;
    model: string;
    apiKey: string;
    baseURL?: string;
    maxTokens?: number;
    temperature?: number;
    topP?: number;
    frequencyPenalty?: number;
    presencePenalty?: number;
    streamingEnabled?: boolean;
}

// ============================================================================
// Conversation & Context Types
// ============================================================================

export interface Message {
    id: string;
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp: string;
    agentId?: string;
    metadata?: Record<string, any>;
}

export interface ConversationContext {
    conversationId: string;
    tenantId: string;
    userId: string;
    messages: Message[];
    metadata: Record<string, any>;
    createdAt: string;
    updatedAt: string;
}

export interface AgentContext {
    conversation: ConversationContext;
    userProfile?: UserProfile;
    tenantSettings?: TenantSettings;
    availableTools: Tool[];
    availableServices: Service[];
    previousResults?: AgentResult[];
}

// ============================================================================
// Agent Execution Types
// ============================================================================

export interface AgentTask {
    id: string;
    type: 'single' | 'sequential' | 'parallel';
    agentIds: string[];
    input: string;
    context: AgentContext;
    priority?: number;
    timeout?: number;
}

export interface AgentResult {
    agentId: string;
    success: boolean;
    response: string;
    data?: Record<string, any>;
    suggestions?: string[];
    toolsUsed?: string[];
    tokensUsed?: number;
    cost?: number;
    executionTime?: number;
    error?: string;
    timestamp: string;
}

export interface OrchestratorResult {
    taskId: string;
    agentResults: AgentResult[];
    finalResponse: string;
    totalCost: number;
    totalTokens: number;
    executionTime: number;
    success: boolean;
}

// ============================================================================
// User & Tenant Types
// ============================================================================

export interface UserProfile {
    id: string;
    tenantId: string;
    role: string;
    permissions: string[];
    preferences?: Record<string, any>;
}

export interface TenantSettings {
    tenantId: string;
    aiPreferences?: {
        defaultProvider?: LLMProvider;
        defaultModel?: string;
        maxCostPerRequest?: number;
        maxCostPerDay?: number;
        enabledAgents?: string[];
        disabledAgents?: string[];
    };
    apiKeys?: Record<string, APIKey>;
    customPrompts?: Record<string, string>;
}

// ============================================================================
// Analytics & Monitoring Types
// ============================================================================

export interface UsageMetrics {
    tenantId: string;
    agentId?: string;
    period: 'hour' | 'day' | 'week' | 'month';
    totalRequests: number;
    successfulRequests: number;
    failedRequests: number;
    totalCost: number;
    totalTokens: number;
    averageResponseTime: number;
    topAgents?: Array<{ agentId: string; count: number }>;
    topTools?: Array<{ toolId: string; count: number }>;
}

export interface AgentPerformance {
    agentId: string;
    successRate: number;
    averageResponseTime: number;
    totalRequests: number;
    userSatisfaction?: number;
    errorRate: number;
    costEfficiency?: number;
}

// ============================================================================
// BYOK Types
// ============================================================================

export interface BYOKConfig {
    tenantId: string;
    service: string;
    keyType: string;
    enabled: boolean;
    fallbackToPlatform: boolean;
    usageLimit?: number;
    costLimit?: number;
}

export interface KeyValidationResult {
    isValid: boolean;
    strength: number; // 0-100
    compliance: {
        pciDss: boolean;
        soc2: boolean;
        gdpr: boolean;
        hipaa: boolean;
    };
    recommendations?: string[];
    error?: string;
}

// ============================================================================
// Admin Types
// ============================================================================

export interface AgentConfig {
    agentId: string;
    enabled: boolean;
    promptOverride?: string;
    systemPromptOverride?: string;
    modelOverride?: ModelPreference;
    costLimit?: number;
    rateLimit?: number;
    allowedTenants?: string[];
    deniedTenants?: string[];
}

export interface AdminAction {
    id: string;
    adminId: string;
    action: string;
    targetType: 'agent' | 'tool' | 'service' | 'mcp' | 'tenant';
    targetId: string;
    changes: Record<string, any>;
    timestamp: string;
    reason?: string;
}

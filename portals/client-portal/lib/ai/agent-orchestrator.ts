/**
 * AI Agent Orchestrator
 * Coordinates multiple AI agents for complex tasks
 */

import type {
    AIAgent,
    AgentTask,
    AgentResult,
    AgentContext,
    OrchestratorResult,
    Message,
    LLMConfig,
} from './types';
import { getAgentById, searchAgents, getActiveAgents } from './agent-registry';
import { getBYOKManager } from './byok-manager';

// ============================================================================
// Configuration
// ============================================================================

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';
const DEFAULT_TIMEOUT = 30000; // 30 seconds
const MAX_RETRIES = 3;

// ============================================================================
// Agent Orchestrator Class
// ============================================================================

export class AgentOrchestrator {
    private tenantId: string;
    private userId: string;
    private byokManager: ReturnType<typeof getBYOKManager>;

    constructor(tenantId: string, userId: string) {
        this.tenantId = tenantId;
        this.userId = userId;
        this.byokManager = getBYOKManager(tenantId);
    }

    /**
     * Execute a task with the appropriate agent(s)
     */
    async executeTask(task: AgentTask): Promise<OrchestratorResult> {
        const startTime = Date.now();

        try {
            let agentResults: AgentResult[];

            switch (task.type) {
                case 'single':
                    agentResults = await this.executeSingleAgent(task);
                    break;

                case 'sequential':
                    agentResults = await this.executeSequential(task);
                    break;

                case 'parallel':
                    agentResults = await this.executeParallel(task);
                    break;

                default:
                    throw new Error(`Unknown task type: ${task.type}`);
            }

            // Aggregate results
            const finalResponse = this.aggregateResults(agentResults);
            const totalCost = agentResults.reduce((sum, r) => sum + (r.cost || 0), 0);
            const totalTokens = agentResults.reduce((sum, r) => sum + (r.tokensUsed || 0), 0);

            return {
                taskId: task.id,
                agentResults,
                finalResponse,
                totalCost,
                totalTokens,
                executionTime: Date.now() - startTime,
                success: agentResults.every((r) => r.success),
            };
        } catch (error) {
            console.error('Task execution error:', error);

            return {
                taskId: task.id,
                agentResults: [],
                finalResponse: `Error executing task: ${error instanceof Error ? error.message : 'Unknown error'}`,
                totalCost: 0,
                totalTokens: 0,
                executionTime: Date.now() - startTime,
                success: false,
            };
        }
    }

    /**
     * Execute a single agent
     */
    private async executeSingleAgent(task: AgentTask): Promise<AgentResult[]> {
        const agentId = task.agentIds[0];
        const agent = getAgentById(agentId);

        if (!agent) {
            throw new Error(`Agent not found: ${agentId}`);
        }

        const result = await this.executeAgent(agent, task.input, task.context);
        return [result];
    }

    /**
     * Execute agents sequentially (output of one feeds into next)
     */
    private async executeSequential(task: AgentTask): Promise<AgentResult[]> {
        const results: AgentResult[] = [];
        let currentInput = task.input;
        let currentContext = task.context;

        for (const agentId of task.agentIds) {
            const agent = getAgentById(agentId);
            if (!agent) {
                console.warn(`Agent not found: ${agentId}, skipping`);
                continue;
            }

            // Update context with previous results
            currentContext = {
                ...currentContext,
                previousResults: results,
            };

            const result = await this.executeAgent(agent, currentInput, currentContext);
            results.push(result);

            // Use this agent's output as input for next agent
            if (result.success) {
                currentInput = result.response;
            } else {
                // Stop on failure
                break;
            }
        }

        return results;
    }

    /**
     * Execute agents in parallel
     */
    private async executeParallel(task: AgentTask): Promise<AgentResult[]> {
        const promises = task.agentIds.map(async (agentId) => {
            const agent = getAgentById(agentId);
            if (!agent) {
                console.warn(`Agent not found: ${agentId}, skipping`);
                return null;
            }

            return this.executeAgent(agent, task.input, task.context);
        });

        const results = await Promise.all(promises);
        return results.filter((r): r is AgentResult => r !== null);
    }

    /**
     * Execute a single agent with retry logic
     */
    private async executeAgent(
        agent: AIAgent,
        input: string,
        context: AgentContext,
        retryCount: number = 0
    ): Promise<AgentResult> {
        const startTime = Date.now();

        try {
            // Check if agent is active
            if (agent.status !== 'active') {
                return {
                    agentId: agent.id,
                    success: false,
                    response: `Agent ${agent.name} is currently ${agent.status}`,
                    error: `Agent status: ${agent.status}`,
                    timestamp: new Date().toISOString(),
                };
            }

            // Get LLM configuration with BYOK
            const llmConfig = await this.getLLMConfigForAgent(agent);

            if (!llmConfig.apiKey) {
                return {
                    agentId: agent.id,
                    success: false,
                    response: 'No API key configured for this agent',
                    error: 'Missing API key',
                    timestamp: new Date().toISOString(),
                };
            }

            // Build the prompt
            const prompt = this.buildPrompt(agent, input, context);

            // Call LLM
            const llmResponse = await this.callLLM(llmConfig, prompt, agent);

            // Parse response and extract suggestions
            const suggestions = this.extractSuggestions(llmResponse.content, agent);

            return {
                agentId: agent.id,
                success: true,
                response: llmResponse.content,
                data: llmResponse.data,
                suggestions,
                toolsUsed: agent.requiredTools,
                tokensUsed: llmResponse.tokensUsed,
                cost: llmResponse.cost,
                executionTime: Date.now() - startTime,
                timestamp: new Date().toISOString(),
            };
        } catch (error) {
            console.error(`Error executing agent ${agent.id}:`, error);

            // Retry logic
            if (retryCount < MAX_RETRIES) {
                console.log(`Retrying agent ${agent.id} (attempt ${retryCount + 1}/${MAX_RETRIES})`);
                await this.delay(1000 * (retryCount + 1)); // Exponential backoff
                return this.executeAgent(agent, input, context, retryCount + 1);
            }

            return {
                agentId: agent.id,
                success: false,
                response: `Failed to execute agent: ${error instanceof Error ? error.message : 'Unknown error'}`,
                error: error instanceof Error ? error.message : 'Unknown error',
                executionTime: Date.now() - startTime,
                timestamp: new Date().toISOString(),
            };
        }
    }

    /**
     * Get LLM configuration for an agent
     */
    private async getLLMConfigForAgent(agent: AIAgent): Promise<LLMConfig> {
        // Determine which LLM provider to use based on agent preferences
        const preferredProvider = agent.modelPreferences?.[0]?.provider || 'openai';
        const preferredModel = agent.modelPreferences?.[0]?.model || 'gpt-4-turbo-preview';

        // Get API key via BYOK
        const llmConfig = await this.byokManager.getLLMConfig(preferredProvider);

        return {
            provider: preferredProvider,
            model: preferredModel,
            apiKey: llmConfig.apiKey || '',
            baseURL: llmConfig.baseURL,
            maxTokens: agent.modelPreferences?.[0]?.maxTokens || 2000,
            temperature: agent.modelPreferences?.[0]?.temperature || 0.7,
            topP: agent.modelPreferences?.[0]?.topP,
            frequencyPenalty: agent.modelPreferences?.[0]?.frequencyPenalty,
            presencePenalty: agent.modelPreferences?.[0]?.presencePenalty,
        };
    }

    /**
     * Build prompt for agent
     */
    private buildPrompt(agent: AIAgent, input: string, context: AgentContext): string {
        let prompt = '';

        // Add system prompt
        if (agent.systemPrompt) {
            prompt += `${agent.systemPrompt}\n\n`;
        }

        // Add agent description and capabilities
        prompt += `You are ${agent.name}. ${agent.description}\n\n`;
        prompt += `Your capabilities include:\n`;
        agent.capabilities.forEach((cap) => {
            prompt += `- ${cap.name}: ${cap.description}\n`;
        });
        prompt += '\n';

        // Add conversation history if available
        if (context.conversation.messages.length > 0) {
            prompt += 'Previous conversation:\n';
            context.conversation.messages.slice(-5).forEach((msg) => {
                prompt += `${msg.role}: ${msg.content}\n`;
            });
            prompt += '\n';
        }

        // Add previous agent results if in sequential execution
        if (context.previousResults && context.previousResults.length > 0) {
            prompt += 'Previous agent outputs:\n';
            context.previousResults.forEach((result) => {
                prompt += `${result.agentId}: ${result.response}\n`;
            });
            prompt += '\n';
        }

        // Add the current user input
        prompt += `User request: ${input}\n\n`;

        // Add instructions for structured output
        prompt += `Please provide:\n`;
        prompt += `1. A helpful response to the user's request\n`;
        prompt += `2. Any relevant data or insights\n`;
        prompt += `3. 2-3 follow-up suggestions for the user\n`;

        return prompt;
    }

    /**
     * Call LLM API
     */
    private async callLLM(
        config: LLMConfig,
        prompt: string,
        agent: AIAgent
    ): Promise<{
        content: string;
        data?: Record<string, any>;
        tokensUsed: number;
        cost: number;
    }> {
        // For now, use Brain API as proxy to LLM
        // In production, this would call OpenAI/Anthropic/OpenRouter directly

        try {
            const response = await fetch(`${BRAIN_API_URL}/api/brain/llm/completion`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    provider: config.provider,
                    model: config.model,
                    apiKey: config.apiKey,
                    prompt,
                    maxTokens: config.maxTokens,
                    temperature: config.temperature,
                    topP: config.topP,
                    frequencyPenalty: config.frequencyPenalty,
                    presencePenalty: config.presencePenalty,
                    tenantId: this.tenantId,
                    agentId: agent.id,
                }),
            });

            if (!response.ok) {
                throw new Error(`LLM API error: ${response.statusText}`);
            }

            const data = await response.json();

            return {
                content: data.content || data.response || '',
                data: data.data,
                tokensUsed: data.tokensUsed || 0,
                cost: data.cost || 0,
            };
        } catch (error) {
            console.error('LLM API call failed:', error);
            throw error;
        }
    }

    /**
     * Extract suggestions from agent response
     */
    private extractSuggestions(response: string, agent: AIAgent): string[] {
        // Simple extraction - look for numbered lists or bullet points
        const suggestions: string[] = [];

        // Try to find suggestions section
        const suggestionsMatch = response.match(/(?:suggestions?|next steps?|follow-up):\s*([\s\S]*?)(?:\n\n|$)/i);

        if (suggestionsMatch) {
            const suggestionText = suggestionsMatch[1];
            const lines = suggestionText.split('\n');

            lines.forEach((line) => {
                // Match numbered or bulleted items
                const match = line.match(/^[\s]*(?:\d+\.|[-*•])\s*(.+)$/);
                if (match && match[1]) {
                    suggestions.push(match[1].trim());
                }
            });
        }

        // If no suggestions found, provide default based on agent type
        if (suggestions.length === 0) {
            suggestions.push(
                `Ask ${agent.name} for more details`,
                `Explore other ${agent.category} capabilities`,
                `View related insights`
            );
        }

        return suggestions.slice(0, 3); // Limit to 3 suggestions
    }

    /**
     * Aggregate results from multiple agents
     */
    private aggregateResults(results: AgentResult[]): string {
        if (results.length === 0) {
            return 'No results available';
        }

        if (results.length === 1) {
            return results[0].response;
        }

        // Combine multiple agent responses
        let aggregated = 'Here are the insights from multiple agents:\n\n';

        results.forEach((result, index) => {
            const agent = getAgentById(result.agentId);
            const agentName = agent?.name || result.agentId;

            aggregated += `**${agentName}:**\n${result.response}\n\n`;
        });

        return aggregated;
    }

    /**
     * Analyze user intent and select appropriate agents
     */
    async analyzeIntent(message: string): Promise<{
        primaryAgent: AIAgent | null;
        supportingAgents: AIAgent[];
        confidence: number;
    }> {
        const messageLower = message.toLowerCase();

        // Simple keyword-based intent analysis
        // In production, this would use an LLM for better intent detection

        const keywords = {
            lead: ['lead', 'contact', 'crm', 'prospect'],
            campaign: ['campaign', 'ad', 'marketing', 'promote'],
            content: ['blog', 'content', 'write', 'article', 'post'],
            seo: ['seo', 'keyword', 'ranking', 'search', 'optimize'],
            analytics: ['analytics', 'report', 'performance', 'data', 'metrics'],
            product: ['product', 'ecommerce', 'sales', 'inventory'],
            social: ['social', 'facebook', 'instagram', 'twitter', 'linkedin'],
            email: ['email', 'newsletter', 'campaign'],
        };

        let bestMatch: { category: string; score: number } | null = null;

        for (const [category, words] of Object.entries(keywords)) {
            const score = words.filter((word) => messageLower.includes(word)).length;
            if (score > 0 && (!bestMatch || score > bestMatch.score)) {
                bestMatch = { category, score };
            }
        }

        if (!bestMatch) {
            return {
                primaryAgent: getAgentById('personal_assistant'),
                supportingAgents: [],
                confidence: 0.5,
            };
        }

        // Map category to agent
        const agentMap: Record<string, string> = {
            lead: 'lead_qualifier',
            campaign: 'campaign_manager',
            content: 'blog_writer',
            seo: 'seo_strategist',
            analytics: 'data_analyst',
            product: 'product_recommender',
            social: 'social_media_manager',
            email: 'email_campaign_manager',
        };

        const primaryAgentId = agentMap[bestMatch.category];
        const primaryAgent = primaryAgentId ? getAgentById(primaryAgentId) : null;

        return {
            primaryAgent,
            supportingAgents: [],
            confidence: Math.min(0.9, 0.5 + bestMatch.score * 0.1),
        };
    }

    /**
     * Create a task from user message
     */
    async createTaskFromMessage(
        message: string,
        conversationId: string,
        context?: Partial<AgentContext>
    ): Promise<AgentTask> {
        const intent = await this.analyzeIntent(message);

        const agentIds = intent.primaryAgent
            ? [intent.primaryAgent.id, ...intent.supportingAgents.map((a) => a.id)]
            : ['personal_assistant'];

        const fullContext: AgentContext = {
            conversation: {
                conversationId,
                tenantId: this.tenantId,
                userId: this.userId,
                messages: context?.conversation?.messages || [],
                metadata: context?.conversation?.metadata || {},
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
            },
            userProfile: context?.userProfile,
            tenantSettings: context?.tenantSettings,
            availableTools: context?.availableTools || [],
            availableServices: context?.availableServices || [],
            previousResults: context?.previousResults,
        };

        return {
            id: `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            type: agentIds.length === 1 ? 'single' : 'sequential',
            agentIds,
            input: message,
            context: fullContext,
            timeout: DEFAULT_TIMEOUT,
        };
    }

    /**
     * Utility: Delay execution
     */
    private delay(ms: number): Promise<void> {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }
}

// ============================================================================
// Export singleton factory
// ============================================================================

const orchestrators = new Map<string, AgentOrchestrator>();

export function getOrchestrator(tenantId: string, userId: string): AgentOrchestrator {
    const key = `${tenantId}:${userId}`;
    if (!orchestrators.has(key)) {
        orchestrators.set(key, new AgentOrchestrator(tenantId, userId));
    }
    return orchestrators.get(key)!;
}

/**
 * LLM Completion API Route
 * Proxy endpoint for LLM providers (OpenAI, Anthropic, OpenRouter)
 * Handles BYOK and cost tracking
 */

import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth/auth-options';

// LLM Provider SDKs (will be installed)
// import OpenAI from 'openai';
// import Anthropic from '@anthropic-ai/sdk';

interface LLMRequest {
    provider: 'openai' | 'anthropic' | 'openrouter' | 'google';
    model: string;
    apiKey: string;
    prompt: string;
    maxTokens?: number;
    temperature?: number;
    topP?: number;
    frequencyPenalty?: number;
    presencePenalty?: number;
    tenantId: string;
    agentId: string;
}

interface LLMResponse {
    content: string;
    data?: Record<string, any>;
    tokensUsed: number;
    cost: number;
}

// Cost per 1K tokens (approximate, update with actual pricing)
const COST_PER_1K_TOKENS: Record<string, { input: number; output: number }> = {
    'gpt-4-turbo-preview': { input: 0.01, output: 0.03 },
    'gpt-4': { input: 0.03, output: 0.06 },
    'gpt-3.5-turbo': { input: 0.0005, output: 0.0015 },
    'claude-3-opus-20240229': { input: 0.015, output: 0.075 },
    'claude-3-sonnet-20240229': { input: 0.003, output: 0.015 },
    'claude-3-haiku-20240307': { input: 0.00025, output: 0.00125 },
};

export async function POST(request: NextRequest) {
    try {
        // Authenticate user
        const session = await getServerSession(authOptions);
        if (!session?.user) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            );
        }

        // Parse request
        const body: LLMRequest = await request.json();
        const {
            provider,
            model,
            apiKey,
            prompt,
            maxTokens = 2000,
            temperature = 0.7,
            topP,
            frequencyPenalty,
            presencePenalty,
            tenantId,
            agentId,
        } = body;

        // Validate required fields
        if (!provider || !model || !apiKey || !prompt) {
            return NextResponse.json(
                { error: 'Missing required fields' },
                { status: 400 }
            );
        }

        // Call appropriate LLM provider
        let response: LLMResponse;

        switch (provider) {
            case 'openai':
                response = await callOpenAI({
                    model,
                    apiKey,
                    prompt,
                    maxTokens,
                    temperature,
                    topP,
                    frequencyPenalty,
                    presencePenalty,
                });
                break;

            case 'anthropic':
                response = await callAnthropic({
                    model,
                    apiKey,
                    prompt,
                    maxTokens,
                    temperature,
                    topP,
                });
                break;

            case 'openrouter':
                response = await callOpenRouter({
                    model,
                    apiKey,
                    prompt,
                    maxTokens,
                    temperature,
                    topP,
                    frequencyPenalty,
                    presencePenalty,
                });
                break;

            case 'google':
                response = await callGoogleAI({
                    model,
                    apiKey,
                    prompt,
                    maxTokens,
                    temperature,
                    topP,
                });
                break;

            default:
                return NextResponse.json(
                    { error: `Unsupported provider: ${provider}` },
                    { status: 400 }
                );
        }

        // Log usage for analytics (would be stored in database)
        await logUsage({
            tenantId,
            agentId,
            provider,
            model,
            tokensUsed: response.tokensUsed,
            cost: response.cost,
            timestamp: new Date().toISOString(),
        });

        return NextResponse.json(response);
    } catch (error) {
        console.error('LLM API error:', error);
        return NextResponse.json(
            {
                error: 'Failed to process LLM request',
                details: error instanceof Error ? error.message : 'Unknown error',
            },
            { status: 500 }
        );
    }
}

// ============================================================================
// LLM Provider Implementations
// ============================================================================

async function callOpenAI(params: {
    model: string;
    apiKey: string;
    prompt: string;
    maxTokens: number;
    temperature: number;
    topP?: number;
    frequencyPenalty?: number;
    presencePenalty?: number;
}): Promise<LLMResponse> {
    // TODO: Install OpenAI SDK: npm install openai
    // For now, use fetch API

    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${params.apiKey}`,
            },
            body: JSON.stringify({
                model: params.model,
                messages: [
                    {
                        role: 'user',
                        content: params.prompt,
                    },
                ],
                max_tokens: params.maxTokens,
                temperature: params.temperature,
                top_p: params.topP,
                frequency_penalty: params.frequencyPenalty,
                presence_penalty: params.presencePenalty,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(`OpenAI API error: ${error.error?.message || response.statusText}`);
        }

        const data = await response.json();
        const content = data.choices[0]?.message?.content || '';
        const tokensUsed = data.usage?.total_tokens || 0;
        const cost = calculateCost(params.model, tokensUsed);

        return {
            content,
            tokensUsed,
            cost,
        };
    } catch (error) {
        console.error('OpenAI API call failed:', error);
        throw error;
    }
}

async function callAnthropic(params: {
    model: string;
    apiKey: string;
    prompt: string;
    maxTokens: number;
    temperature: number;
    topP?: number;
}): Promise<LLMResponse> {
    // TODO: Install Anthropic SDK: npm install @anthropic-ai/sdk

    try {
        const response = await fetch('https://api.anthropic.com/v1/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': params.apiKey,
                'anthropic-version': '2023-06-01',
            },
            body: JSON.stringify({
                model: params.model,
                max_tokens: params.maxTokens,
                temperature: params.temperature,
                top_p: params.topP,
                messages: [
                    {
                        role: 'user',
                        content: params.prompt,
                    },
                ],
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(`Anthropic API error: ${error.error?.message || response.statusText}`);
        }

        const data = await response.json();
        const content = data.content[0]?.text || '';
        const tokensUsed = (data.usage?.input_tokens || 0) + (data.usage?.output_tokens || 0);
        const cost = calculateCost(params.model, tokensUsed);

        return {
            content,
            tokensUsed,
            cost,
        };
    } catch (error) {
        console.error('Anthropic API call failed:', error);
        throw error;
    }
}

async function callOpenRouter(params: {
    model: string;
    apiKey: string;
    prompt: string;
    maxTokens: number;
    temperature: number;
    topP?: number;
    frequencyPenalty?: number;
    presencePenalty?: number;
}): Promise<LLMResponse> {
    try {
        const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${params.apiKey}`,
                'HTTP-Referer': process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3003',
                'X-Title': 'BizOSaaS AI Assistant',
            },
            body: JSON.stringify({
                model: params.model,
                messages: [
                    {
                        role: 'user',
                        content: params.prompt,
                    },
                ],
                max_tokens: params.maxTokens,
                temperature: params.temperature,
                top_p: params.topP,
                frequency_penalty: params.frequencyPenalty,
                presence_penalty: params.presencePenalty,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(`OpenRouter API error: ${error.error?.message || response.statusText}`);
        }

        const data = await response.json();
        const content = data.choices[0]?.message?.content || '';
        const tokensUsed = data.usage?.total_tokens || 0;
        const cost = calculateCost(params.model, tokensUsed);

        return {
            content,
            tokensUsed,
            cost,
        };
    } catch (error) {
        console.error('OpenRouter API call failed:', error);
        throw error;
    }
}

async function callGoogleAI(params: {
    model: string;
    apiKey: string;
    prompt: string;
    maxTokens: number;
    temperature: number;
    topP?: number;
}): Promise<LLMResponse> {
    try {
        const response = await fetch(
            `https://generativelanguage.googleapis.com/v1beta/models/${params.model}:generateContent?key=${params.apiKey}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    contents: [
                        {
                            parts: [
                                {
                                    text: params.prompt,
                                },
                            ],
                        },
                    ],
                    generationConfig: {
                        maxOutputTokens: params.maxTokens,
                        temperature: params.temperature,
                        topP: params.topP,
                    },
                }),
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(`Google AI API error: ${error.error?.message || response.statusText}`);
        }

        const data = await response.json();
        const content = data.candidates?.[0]?.content?.parts?.[0]?.text || '';
        const tokensUsed = data.usageMetadata?.totalTokenCount || 0;
        const cost = calculateCost(params.model, tokensUsed);

        return {
            content,
            tokensUsed,
            cost,
        };
    } catch (error) {
        console.error('Google AI API call failed:', error);
        throw error;
    }
}

// ============================================================================
// Helper Functions
// ============================================================================

function calculateCost(model: string, tokensUsed: number): number {
    const pricing = COST_PER_1K_TOKENS[model];

    if (!pricing) {
        // Default pricing if model not found
        return (tokensUsed / 1000) * 0.002;
    }

    // Approximate: assume 50% input, 50% output
    const inputTokens = tokensUsed * 0.5;
    const outputTokens = tokensUsed * 0.5;

    const cost =
        (inputTokens / 1000) * pricing.input + (outputTokens / 1000) * pricing.output;

    return Math.round(cost * 100000) / 100000; // Round to 5 decimal places
}

async function logUsage(params: {
    tenantId: string;
    agentId: string;
    provider: string;
    model: string;
    tokensUsed: number;
    cost: number;
    timestamp: string;
}): Promise<void> {
    // TODO: Store in database
    // For now, just log to console
    console.log('LLM Usage:', params);

    // In production, this would insert into a usage_logs table:
    // await db.usageLogs.create({
    //   data: {
    //     tenantId: params.tenantId,
    //     agentId: params.agentId,
    //     provider: params.provider,
    //     model: params.model,
    //     tokensUsed: params.tokensUsed,
    //     cost: params.cost,
    //     timestamp: params.timestamp,
    //   },
    // });
}

import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const provider = searchParams.get('provider') || 'openrouter';

    const response = await fetch(`${BRAIN_API_URL}/api/llm/models?provider=${provider}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3009',
      },
    });

    if (!response.ok) {
      // Fallback data for development
      const fallbackModels: Record<string, any[]> = {
        openrouter: [
          { id: 'or-gpt4', name: 'OpenAI GPT-4', provider: 'OpenRouter', category: 'chat', contextWindow: 8192, costPer1k: 0.03, enabled: true, usage: 12456 },
          { id: 'or-claude', name: 'Claude-3 Opus', provider: 'OpenRouter', category: 'reasoning', contextWindow: 200000, costPer1k: 0.015, enabled: true, usage: 8934 },
          { id: 'or-gemini', name: 'Gemini Pro', provider: 'OpenRouter', category: 'chat', contextWindow: 32000, costPer1k: 0.001, enabled: true, usage: 5678 },
          { id: 'or-llama', name: 'Llama 3 70B', provider: 'OpenRouter', category: 'chat', contextWindow: 8192, costPer1k: 0.0008, enabled: false, usage: 0 }
        ],
        openai: [
          { id: 'gpt-4', name: 'GPT-4', provider: 'OpenAI', category: 'chat', contextWindow: 8192, costPer1k: 0.03, enabled: true, usage: 4532 },
          { id: 'gpt-3.5', name: 'GPT-3.5 Turbo', provider: 'OpenAI', category: 'chat', contextWindow: 16384, costPer1k: 0.002, enabled: true, usage: 2341 },
          { id: 'ada-002', name: 'Text Embedding Ada 002', provider: 'OpenAI', category: 'embedding', contextWindow: 8191, costPer1k: 0.0001, enabled: true, usage: 1234 },
          { id: 'dall-e-3', name: 'DALL-E 3', provider: 'OpenAI', category: 'vision', contextWindow: 0, costPer1k: 0.04, enabled: false, usage: 0 }
        ],
        anthropic: [
          { id: 'claude-opus', name: 'Claude-3 Opus', provider: 'Anthropic', category: 'reasoning', contextWindow: 200000, costPer1k: 0.015, enabled: true, usage: 3456 },
          { id: 'claude-sonnet', name: 'Claude-3 Sonnet', provider: 'Anthropic', category: 'chat', contextWindow: 200000, costPer1k: 0.003, enabled: true, usage: 1987 },
          { id: 'claude-haiku', name: 'Claude-3 Haiku', provider: 'Anthropic', category: 'chat', contextWindow: 200000, costPer1k: 0.00025, enabled: false, usage: 0 }
        ],
        gemini: [
          { id: 'gemini-pro', name: 'Gemini Pro', provider: 'Google', category: 'chat', contextWindow: 32000, costPer1k: 0.001, enabled: true, usage: 2341 },
          { id: 'gemini-vision', name: 'Gemini Pro Vision', provider: 'Google', category: 'vision', contextWindow: 16384, costPer1k: 0.002, enabled: true, usage: 1115 }
        ]
      };

      return NextResponse.json({
        success: true,
        provider,
        models: fallbackModels[provider] || []
      });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('LLM models API error:', error);

    // Return empty fallback on error
    return NextResponse.json({
      success: false,
      error: error instanceof Error ? error.message : 'Failed to fetch models',
      models: []
    });
  }
}

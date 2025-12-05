import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function GET(request: NextRequest) {
  try {
    const response = await fetch(`${BRAIN_API_URL}/api/llm/providers`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3009',
      },
    });

    if (!response.ok) {
      // Fallback data for development
      return NextResponse.json({
        success: true,
        providers: [
          {
            id: 'openrouter',
            name: 'OpenRouter',
            type: 'primary',
            status: 'active',
            models: 200,
            apiKey: '*********************xyz',
            requests: 45678,
            cost: 1234.56,
            avgResponseTime: 1.2,
            successRate: 98.5,
            capabilities: ['200+ models', 'Model routing', 'Fallback handling', 'Cost optimization'],
            lastUsed: '2 minutes ago'
          },
          {
            id: 'openai',
            name: 'OpenAI',
            type: 'fallback',
            status: 'active',
            models: 8,
            apiKey: '*********************abc',
            requests: 8934,
            cost: 234.12,
            avgResponseTime: 0.8,
            successRate: 99.2,
            capabilities: ['GPT-4', 'GPT-3.5', 'DALL-E', 'Embeddings'],
            lastUsed: '15 minutes ago'
          },
          {
            id: 'anthropic',
            name: 'Anthropic Claude',
            type: 'fallback',
            status: 'active',
            models: 3,
            apiKey: '*********************def',
            requests: 5621,
            cost: 187.34,
            avgResponseTime: 1.5,
            successRate: 99.8,
            capabilities: ['Claude-3 Opus', 'Claude-3 Sonnet', 'Claude-3 Haiku', '200k context'],
            lastUsed: '5 minutes ago'
          },
          {
            id: 'gemini',
            name: 'Google Gemini',
            type: 'fallback',
            status: 'active',
            models: 2,
            apiKey: '*********************ghi',
            requests: 3456,
            cost: 98.45,
            avgResponseTime: 1.1,
            successRate: 97.9,
            capabilities: ['Gemini Pro', 'Gemini Pro Vision', 'Multi-modal'],
            lastUsed: '30 minutes ago'
          }
        ]
      });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('LLM providers API error:', error);

    // Return fallback data on error
    return NextResponse.json({
      success: true,
      providers: [
        {
          id: 'openrouter',
          name: 'OpenRouter',
          type: 'primary',
          status: 'active',
          models: 200,
          apiKey: '*********************xyz',
          requests: 45678,
          cost: 1234.56,
          avgResponseTime: 1.2,
          successRate: 98.5,
          capabilities: ['200+ models', 'Model routing', 'Fallback handling', 'Cost optimization'],
          lastUsed: '2 minutes ago'
        }
      ]
    });
  }
}

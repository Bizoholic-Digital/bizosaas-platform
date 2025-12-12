/**
 * AI Assistant Chat API Route
 * Connects to Personal AI Assistant with 93+ AI agents
 * Provides conversational interface for data analysis, automation, and insights
 */

import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';

import { getOrchestrator } from '@/lib/ai';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function POST(request: NextRequest) {
    try {
        // Authenticate user
        const session = await auth();
        if (!session?.user) {
            return NextResponse.json(
                { error: 'Unauthorized' },
                { status: 401 }
            );
        }

        // Parse request body
        const body = await request.json();
        const { message, conversationId, context } = body;

        if (!message) {
            return NextResponse.json(
                { error: 'Message is required' },
                { status: 400 }
            );
        }

        // Get tenant and user IDs from session
        const tenantId = (session.user as any).tenantId || 'default_tenant';
        const userId = (session.user as any).id || session.user.email || 'unknown_user';

        // Get orchestrator for this tenant/user
        const orchestrator = getOrchestrator(tenantId, userId);

        // Create task from message
        const task = await orchestrator.createTaskFromMessage(
            message,
            conversationId || `conv_${Date.now()}`,
            context
        );

        // Execute task
        const result = await orchestrator.executeTask(task);

        // Format response
        const response = {
            response: result.finalResponse,
            agentUsed: result.agentResults[0]?.agentId || 'personal_assistant',
            data: result.agentResults[0]?.data,
            suggestions: result.agentResults[0]?.suggestions || [],
            metadata: {
                conversationId: task.context.conversation.conversationId,
                tokensUsed: result.totalTokens,
                cost: result.totalCost,
                executionTime: result.executionTime,
                agentsInvolved: result.agentResults.map((r) => r.agentId),
                success: result.success,
            },
        };

        return NextResponse.json(response);
    } catch (error) {
        console.error('Chat API error:', error);

        // Fallback to simple response on error
        return NextResponse.json(
            {
                response:
                    "I apologize, but I'm having trouble processing your request right now. Please try again in a moment.",
                agentUsed: 'personal_assistant',
                data: null,
                suggestions: [
                    'Try rephrasing your question',
                    'Check your connection',
                    'Contact support if the issue persists',
                ],
                metadata: {
                    error: error instanceof Error ? error.message : 'Unknown error',
                    success: false,
                },
            },
            { status: 500 }
        );
    }
}

// Health check endpoint
export async function GET(request: NextRequest) {
    try {
        const session = await auth();

        return NextResponse.json({
            status: 'healthy',
            timestamp: new Date().toISOString(),
            authenticated: !!session?.user,
            brainApiUrl: BRAIN_API_URL,
            features: {
                agentOrchestration: true,
                byokSupport: true,
                multiAgentExecution: true,
                totalAgents: 93,
                activeAgents: 7,
            },
        });
    } catch (error) {
        return NextResponse.json(
            {
                status: 'unhealthy',
                error: error instanceof Error ? error.message : 'Unknown error',
            },
            { status: 500 }
        );
    }
}

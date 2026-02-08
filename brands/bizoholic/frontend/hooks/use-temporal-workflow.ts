import { useState, useCallback } from 'react';

export interface WorkflowStatus {
    status: 'pending' | 'running' | 'completed' | 'failed';
    progress: number;
    current_step: string;
    completed_steps: string[];
}

export function useOnboardingWorkflow() {
    const [status, setStatus] = useState<WorkflowStatus | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const startOnboarding = useCallback(async (formData: any) => {
        setLoading(true);
        setError(null);

        try {
            // Mocking the starting of a Temporal workflow
            const workflow_id = `onboarding-${Date.now()}`;

            setStatus({
                status: 'running',
                progress: 10,
                current_step: 'Initializing AI Agents',
                completed_steps: []
            });

            // In production, this would call the Brain Gateway API to start a Temporal workflow
            // For now, we simulate the result
            return {
                workflow_id,
                agent_workflows: [
                    { id: 'marketing-agent', status: 'setup' },
                    { id: 'dropshipping-agent', status: 'setup' }
                ]
            };
        } catch (err: any) {
            setError(err.message || 'Failed to start onboarding workflow');
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    const isRunning = status?.status === 'running';
    const isCompleted = status?.status === 'completed';

    return {
        startOnboarding,
        status,
        loading,
        error,
        isCompleted,
        isRunning
    };
}

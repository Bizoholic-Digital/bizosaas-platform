'use client';

import { useState, useEffect } from 'react';

export function useAIAgentsData() {
    const [data, setData] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // Mock data for AI agents
        const mockAgents = {
            agents: [
                { id: 'marketing-strategist', name: 'Marketing Strategist', type: 'marketing' },
                { id: 'seo-optimizer', name: 'SEO Optimizer', type: 'seo' },
                { id: 'content-creator', name: 'Content Creator', type: 'content' },
                { id: 'digital-audit', name: 'Digital Audit', type: 'analytics' },
                { id: 'customer-support', name: 'Customer Support', type: 'support' },
                { id: 'ecommerce-specialist', name: 'E-commerce Specialist', type: 'ecommerce' }
            ]
        };

        setTimeout(() => {
            setData(mockAgents);
            setIsLoading(false);
        }, 500);
    }, []);

    return { data, isLoading };
}

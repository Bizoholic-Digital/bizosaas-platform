'use client';

import React, { useState, useEffect } from 'react';
import { Link as LinkIcon, Mail, CreditCard, MessageSquare, Database, Globe } from 'lucide-react';

interface IntegrationsContentProps {
    activeTab: string;
}

export const IntegrationsContent: React.FC<IntegrationsContentProps> = ({ activeTab }) => {
    const [integrations, setIntegrations] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    // Map icon names to components
    const iconMap: { [key: string]: any } = {
        LinkIcon: LinkIcon,
        Mail: Mail,
        CreditCard: CreditCard,
        MessageSquare: MessageSquare,
        Database: Database,
        Globe: Globe
    };

    useEffect(() => {
        fetchIntegrations();
    }, []);

    const fetchIntegrations = async () => {
        try {
            const response = await fetch('/api/brain/integrations');
            if (response.ok) {
                const data = await response.json();
                // Map string icons to components
                const mappedData = data.map((item: any) => ({
                    ...item,
                    icon: iconMap[item.icon] || Globe
                }));
                setIntegrations(mappedData);
            }
        } catch (error) {
            console.error('Failed to fetch integrations:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const toggleIntegration = async (id: string) => {
        const integration = integrations.find(i => i.id === id);
        if (!integration) return;

        const action = integration.connected ? 'disconnect' : 'connect';

        // Optimistic update
        setIntegrations(integrations.map(i => {
            if (i.id === id) {
                return { ...i, connected: !i.connected };
            }
            return i;
        }));

        try {
            await fetch('/api/brain/integrations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id, action })
            });
        } catch (error) {
            console.error('Failed to toggle integration:', error);
            // Revert on error
            fetchIntegrations();
        }
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Integrations</h2>
                <button className="bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                    Browse Marketplace
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {integrations.map((integration) => (
                    <div key={integration.id} className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800 flex flex-col h-full">
                        <div className="flex items-center gap-3 mb-4">
                            <div className={`w-12 h-12 rounded-lg flex items-center justify-center bg-${integration.color}-100 dark:bg-${integration.color}-900/30`}>
                                <integration.icon className={`w-6 h-6 text-${integration.color}-600 dark:text-${integration.color}-400`} />
                            </div>
                            <div>
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{integration.name}</h3>
                                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${integration.connected
                                    ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
                                    : 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-400'
                                    }`}>
                                    {integration.connected ? 'Connected' : 'Not Connected'}
                                </span>
                            </div>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-6 flex-1">
                            {integration.description}
                        </p>
                        <button
                            onClick={() => toggleIntegration(integration.id)}
                            className={`w-full py-2 rounded-lg font-medium transition-colors ${integration.connected
                                ? 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-700'
                                : 'bg-blue-600 text-white hover:bg-blue-700'
                                }`}
                        >
                            {integration.connected ? 'Manage' : 'Connect'}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

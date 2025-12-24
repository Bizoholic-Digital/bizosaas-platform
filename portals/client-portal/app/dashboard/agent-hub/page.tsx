'use client';

import DashboardLayout from '@/components/ui/dashboard-layout';
import AIAgentHub from '@/components/AIAgentHub';

export default function AgentHubPage() {
    return (
        <DashboardLayout
            title="AI Agent Hub"
            description="Autonomous intelligence at your service"
        >
            <AIAgentHub />
        </DashboardLayout>
    );
}

'use client';

import React from 'react';
import { AgentManagementInterface } from '../../../components/agent-management/index';

export default function AgentManagementPage() {
    return (
        <div className="h-full p-6 space-y-6 overflow-y-auto">
            <AgentManagementInterface />
        </div>
    );
}

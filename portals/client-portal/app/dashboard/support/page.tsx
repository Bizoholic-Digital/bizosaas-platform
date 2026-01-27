'use client';

import SupportContent from '@/components/SupportContent';
import { useSetHeader } from '@/lib/contexts/HeaderContext';

export default function SupportPage() {
    useSetHeader("Support Helpdesk", "Get help from our team and AI assistants.");

    return (
        <div className="p-6">
            <SupportContent />
        </div>
    );
}

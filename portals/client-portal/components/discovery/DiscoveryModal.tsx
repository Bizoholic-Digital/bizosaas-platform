'use client';

import React, { useState } from 'react';
import { Modal } from '../Modal';
import { CheckCircle2, Globe, BarChart3, Search, User, ShieldCheck, ChevronRight } from 'lucide-react';
import { Button } from '../ui/button';

interface DiscoveryResult {
    id: string;
    name: string;
    status: string;
    details?: string;
}

interface DiscoveryModalProps {
    isOpen: boolean;
    onClose: () => void;
    discoveredData: Record<string, any>;
    onConfirm: (selectedIds: string[]) => Promise<void>;
}

export const DiscoveryModal: React.FC<DiscoveryModalProps> = ({
    isOpen,
    onClose,
    discoveredData,
    onConfirm
}) => {
    const [selectedIds, setSelectedIds] = useState<string[]>(Object.keys(discoveredData));
    const [isLinking, setIsLinking] = useState(false);

    const toggleSelection = (id: string) => {
        if (selectedIds.includes(id)) {
            setSelectedIds(selectedIds.filter(i => i !== id));
        } else {
            setSelectedIds([...selectedIds, id]);
        }
    };

    const handleConfirm = async () => {
        setIsLinking(true);
        try {
            await onConfirm(selectedIds);
            onClose();
        } finally {
            setIsLinking(false);
        }
    };

    const getIcon = (id: string) => {
        if (id.includes('analytics')) return <BarChart3 className="w-5 h-5 text-orange-500" />;
        if (id.includes('search-console')) return <Search className="w-5 h-5 text-blue-500" />;
        if (id.includes('ads')) return <Globe className="w-5 h-5 text-green-500" />;
        if (id.includes('business-profile')) return <User className="w-5 h-5 text-blue-600" />;
        return <ShieldCheck className="w-5 h-5 text-purple-500" />;
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} title="Connect Discovered Accounts" size="md">
            <div className="space-y-6">
                <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-100 dark:border-blue-800">
                    <p className="text-sm text-blue-800 dark:text-blue-300">
                        We've found the following accounts associated with your Google profile.
                        Select the ones you'd like to link to BizOSaaS.
                    </p>
                </div>

                <div className="space-y-3">
                    {Object.entries(discoveredData).map(([id, result]) => (
                        <div
                            key={id}
                            onClick={() => toggleSelection(id)}
                            className={`flex items-center justify-between p-4 rounded-xl border transition-all cursor-pointer ${selectedIds.includes(id)
                                    ? 'border-blue-500 bg-blue-50/50 dark:bg-blue-900/10'
                                    : 'border-gray-200 dark:border-gray-800 hover:border-gray-300 dark:hover:border-gray-700'
                                }`}
                        >
                            <div className="flex items-center gap-4">
                                <div className="p-2 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-100 dark:border-gray-700">
                                    {getIcon(id)}
                                </div>
                                <div>
                                    <h4 className="font-semibold text-gray-900 dark:text-white capitalize">
                                        {id.replace(/-/g, ' ')}
                                    </h4>
                                    <p className="text-xs text-gray-500 dark:text-gray-400">
                                        {result.status === 'success' ? 'Ready to connect' : 'Detected'}
                                    </p>
                                </div>
                            </div>
                            <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${selectedIds.includes(id)
                                    ? 'bg-blue-600 border-blue-600'
                                    : 'border-gray-300 dark:border-gray-600'
                                }`}>
                                {selectedIds.includes(id) && <CheckCircle2 className="w-4 h-4 text-white" />}
                            </div>
                        </div>
                    ))}
                </div>

                <div className="flex gap-3 pt-4">
                    <Button variant="outline" onClick={onClose} className="flex-1">
                        Cancel
                    </Button>
                    <Button
                        onClick={handleConfirm}
                        disabled={selectedIds.length === 0 || isLinking}
                        className="flex-1 bg-blue-600 hover:bg-blue-700 text-white"
                    >
                        {isLinking ? 'Connecting...' : `Connect ${selectedIds.length} Accounts`}
                    </Button>
                </div>
            </div>
        </Modal>
    );
};

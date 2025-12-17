'use client';

import DashboardLayout from '@/components/ui/dashboard-layout';
import { Calendar as CalendarIcon, Plus } from 'lucide-react';

export default function CalendarPage() {
    return (
        <DashboardLayout
            title="Calendar"
            description="View and manage your tasks and project deadlines"
        >
            <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                        <CalendarIcon className="w-8 h-8 text-blue-600" />
                        <h2 className="text-2xl font-bold">Calendar View</h2>
                    </div>
                    <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                        <Plus className="w-4 h-4" />
                        Add Event
                    </button>
                </div>

                <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                    <div className="text-center py-12">
                        <CalendarIcon className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                        <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-2">
                            Calendar Coming Soon
                        </h3>
                        <p className="text-gray-500 dark:text-gray-400">
                            Task and project calendar integration will be available soon.
                        </p>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}

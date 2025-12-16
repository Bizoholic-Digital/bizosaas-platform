'use client';

import React from 'react';
import DashboardLayout from '@/components/ui/dashboard-layout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function MyTasksPage() {
    return (
        <DashboardLayout title="My Tasks" description="Track your personal to-dos">
            <div className="p-6">
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-muted-foreground">Detailed task list view coming soon.</p>
                    </CardContent>
                </Card>
            </div>
        </DashboardLayout>
    );
}

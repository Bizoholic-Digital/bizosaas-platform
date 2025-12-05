'use client';

import React from 'react';
import DashboardLayout from '../../components/ui/dashboard-layout';

export default function TestPage() {
  return (
    <DashboardLayout title="Test Page" description="Testing sidebar visibility">
      <div className="p-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h1 className="text-2xl font-bold mb-4">Test Page</h1>
          <p>This is a test page to verify that the sidebar is visible.</p>
          <p>If you can see the sidebar on the left, the layout is working correctly.</p>
          
          <div className="mt-4">
            <h2 className="text-lg font-semibold mb-2">Debug Information:</h2>
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Page: /test</li>
              <li>Layout: DashboardLayout</li>
              <li>Sidebar should be visible</li>
              <li>Navigation should be functional</li>
            </ul>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
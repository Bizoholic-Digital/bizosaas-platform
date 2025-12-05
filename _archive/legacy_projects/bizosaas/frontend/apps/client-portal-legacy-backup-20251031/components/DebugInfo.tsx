'use client';

import React from 'react';

interface DebugInfoProps {
  isVisible?: boolean;
  data: {
    activeTab: string;
    isSidebarOpen: boolean;
    theme: string;
    expandedSections: {[key: string]: boolean};
    isInitialized: boolean;
  };
}

export function DebugInfo({ isVisible = false, data }: DebugInfoProps) {
  if (!isVisible) return null;

  return (
    <div className="fixed bottom-4 right-4 bg-black text-white p-4 rounded-lg text-xs font-mono z-50 max-w-xs">
      <div className="font-bold mb-2">Debug Info:</div>
      <div>Active Tab: {data.activeTab}</div>
      <div>Sidebar Open: {data.isSidebarOpen ? 'Yes' : 'No'}</div>
      <div>Theme: {data.theme}</div>
      <div>Initialized: {data.isInitialized ? 'Yes' : 'No'}</div>
      <div className="mt-2">
        <div className="font-bold">Expanded Sections:</div>
        {Object.entries(data.expandedSections).map(([key, value]) => (
          <div key={key} className="text-xs">
            {key}: {value ? 'Yes' : 'No'}
          </div>
        ))}
      </div>
    </div>
  );
}
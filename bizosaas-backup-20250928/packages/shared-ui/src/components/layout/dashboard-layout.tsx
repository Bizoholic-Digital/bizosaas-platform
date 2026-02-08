'use client';

import React, { ReactNode } from 'react';
import { Sidebar } from '../sidebar';
import { PageHeader } from './page-header';

interface DashboardLayoutProps {
  children: ReactNode;
  title?: string;
  description?: string;
}

export function DashboardLayout({ children, title, description }: DashboardLayoutProps) {
  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <Sidebar />
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Page Header */}
        {(title || description) && (
          <PageHeader title={title} description={description} />
        )}
        
        {/* Main Content Area */}
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
'use client';

import React, { ReactNode } from 'react';
import { Separator } from '../separator';

interface PageHeaderProps {
  title?: string;
  description?: string;
  action?: ReactNode;
  breadcrumb?: ReactNode;
}

export function PageHeader({ title, description, action, breadcrumb }: PageHeaderProps) {
  return (
    <div className="border-b bg-white dark:bg-gray-900">
      <div className="px-6 py-4">
        {breadcrumb && (
          <div className="mb-2">
            {breadcrumb}
          </div>
        )}
        
        <div className="flex items-center justify-between">
          <div>
            {title && (
              <h1 className="text-2xl font-semibold text-gray-900 dark:text-white">
                {title}
              </h1>
            )}
            {description && (
              <p className="text-gray-600 dark:text-gray-400 mt-1">
                {description}
              </p>
            )}
          </div>
          
          {action && (
            <div className="flex items-center space-x-2">
              {action}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
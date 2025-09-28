'use client';

import React, { ReactNode } from 'react';
import { Card, CardContent } from '../card';

interface AuthLayoutProps {
  children: ReactNode;
  title?: string;
  subtitle?: string;
}

export function AuthLayout({ children, title, subtitle }: AuthLayoutProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="w-full max-w-md px-6">
        <Card className="shadow-2xl">
          <CardContent className="pt-6">
            {title && (
              <div className="text-center mb-6">
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {title}
                </h1>
                {subtitle && (
                  <p className="text-gray-600 dark:text-gray-400 mt-2">
                    {subtitle}
                  </p>
                )}
              </div>
            )}
            {children}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
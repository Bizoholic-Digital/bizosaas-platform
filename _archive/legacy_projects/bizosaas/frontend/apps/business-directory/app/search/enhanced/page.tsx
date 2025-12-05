'use client';

import React, { Suspense } from 'react';

function EnhancedSearchPage() {
  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
            Enhanced Business Search
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Enhanced search functionality coming soon...
          </p>
        </div>
      </div>
    </div>
  );
}

export default function WrappedEnhancedSearchPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    }>
      <EnhancedSearchPage />
    </Suspense>
  );
}
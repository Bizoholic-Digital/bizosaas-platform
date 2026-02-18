'use client';

import { ReactNode } from 'react';

interface SkeletonProps {
  className?: string;
  children?: ReactNode;
}

function SkeletonBase({ className = '', children }: SkeletonProps) {
  return (
    <div 
      className={`animate-pulse bg-gray-200 dark:bg-gray-700 rounded ${className}`}
      style={{
        background: 'linear-gradient(90deg, #f0f0f0 25%, transparent 50%, #f0f0f0 75%)',
        backgroundSize: '200% 100%',
        animation: 'loading 1.5s infinite',
      }}
    >
      {children}
    </div>
  );
}

export function CardSkeleton() {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 space-y-4">
      <div className="flex items-center space-x-4">
        <SkeletonBase className="w-12 h-12 rounded-full" />
        <div className="space-y-2 flex-1">
          <SkeletonBase className="h-4 w-3/4" />
          <SkeletonBase className="h-3 w-1/2" />
        </div>
      </div>
      <div className="space-y-2">
        <SkeletonBase className="h-4 w-full" />
        <SkeletonBase className="h-4 w-5/6" />
        <SkeletonBase className="h-4 w-4/6" />
      </div>
      <div className="flex justify-between items-center">
        <SkeletonBase className="h-6 w-20" />
        <SkeletonBase className="h-8 w-24 rounded-md" />
      </div>
    </div>
  );
}

export function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      {/* Header */}
      <div className="border-b border-gray-200 dark:border-gray-700 p-4">
        <div className="grid grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <SkeletonBase key={i} className="h-4" />
          ))}
        </div>
      </div>
      
      {/* Rows */}
      {[...Array(rows)].map((_, rowIndex) => (
        <div key={rowIndex} className="border-b border-gray-100 dark:border-gray-700 p-4 last:border-b-0">
          <div className="grid grid-cols-4 gap-4 items-center">
            <SkeletonBase className="h-4" />
            <SkeletonBase className="h-4" />
            <SkeletonBase className="h-4" />
            <SkeletonBase className="h-6 w-16 rounded" />
          </div>
        </div>
      ))}
    </div>
  );
}

export function DashboardSkeleton() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-4">
        <SkeletonBase className="h-8 w-64" />
        <SkeletonBase className="h-4 w-96" />
      </div>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div className="space-y-2">
                <SkeletonBase className="h-4 w-20" />
                <SkeletonBase className="h-8 w-16" />
              </div>
              <SkeletonBase className="w-8 h-8 rounded" />
            </div>
          </div>
        ))}
      </div>
      
      {/* Chart */}
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
        <div className="space-y-4">
          <SkeletonBase className="h-6 w-48" />
          <SkeletonBase className="h-64 w-full rounded" />
        </div>
      </div>
      
      {/* Table */}
      <TableSkeleton />
    </div>
  );
}

export function CampaignSkeleton() {
  return (
    <div className="space-y-6">
      {/* Campaign Header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between mb-4">
          <div className="space-y-2">
            <SkeletonBase className="h-6 w-48" />
            <SkeletonBase className="h-4 w-32" />
          </div>
          <SkeletonBase className="h-8 w-20 rounded" />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="text-center">
              <SkeletonBase className="h-8 w-20 mx-auto mb-2" />
              <SkeletonBase className="h-4 w-16 mx-auto" />
            </div>
          ))}
        </div>
      </div>
      
      {/* Campaign Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {[...Array(4)].map((_, i) => (
          <CardSkeleton key={i} />
        ))}
      </div>
    </div>
  );
}

export function FormSkeleton() {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 border border-gray-200 dark:border-gray-700 space-y-6">
      <div className="space-y-2">
        <SkeletonBase className="h-6 w-48" />
        <SkeletonBase className="h-4 w-64" />
      </div>
      
      {/* Form Fields */}
      {[...Array(4)].map((_, i) => (
        <div key={i} className="space-y-2">
          <SkeletonBase className="h-4 w-24" />
          <SkeletonBase className="h-10 w-full rounded-md" />
        </div>
      ))}
      
      {/* Buttons */}
      <div className="flex space-x-4">
        <SkeletonBase className="h-10 w-24 rounded-md" />
        <SkeletonBase className="h-10 w-20 rounded-md" />
      </div>
    </div>
  );
}

export function ListSkeleton({ items = 5 }: { items?: number }) {
  return (
    <div className="space-y-3">
      {[...Array(items)].map((_, i) => (
        <div key={i} className="flex items-center space-x-4 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
          <SkeletonBase className="w-10 h-10 rounded-full" />
          <div className="flex-1 space-y-2">
            <SkeletonBase className="h-4 w-3/4" />
            <SkeletonBase className="h-3 w-1/2" />
          </div>
          <SkeletonBase className="h-6 w-16 rounded" />
        </div>
      ))}
    </div>
  );
}

// Mobile-optimized skeletons
export function MobileCardSkeleton() {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4 space-y-3">
      <div className="flex items-center space-x-3">
        <SkeletonBase className="w-8 h-8 rounded-full" />
        <div className="space-y-1 flex-1">
          <SkeletonBase className="h-3 w-3/4" />
          <SkeletonBase className="h-2 w-1/2" />
        </div>
      </div>
      <div className="space-y-2">
        <SkeletonBase className="h-3 w-full" />
        <SkeletonBase className="h-3 w-5/6" />
      </div>
      <div className="flex justify-between items-center">
        <SkeletonBase className="h-4 w-16" />
        <SkeletonBase className="h-6 w-20 rounded" />
      </div>
    </div>
  );
}

export function MobileListSkeleton({ items = 3 }: { items?: number }) {
  return (
    <div className="space-y-2">
      {[...Array(items)].map((_, i) => (
        <div key={i} className="flex items-center space-x-3 p-3 bg-white dark:bg-gray-800 rounded-lg">
          <SkeletonBase className="w-6 h-6 rounded" />
          <div className="flex-1 space-y-1">
            <SkeletonBase className="h-3 w-2/3" />
            <SkeletonBase className="h-2 w-1/3" />
          </div>
        </div>
      ))}
    </div>
  );
}

// CSS for shimmer effect
const shimmerCSS = `
@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
`;

// Inject CSS
if (typeof document !== 'undefined') {
  const style = document.createElement('style');
  style.textContent = shimmerCSS;
  document.head.appendChild(style);
}

export default SkeletonBase;
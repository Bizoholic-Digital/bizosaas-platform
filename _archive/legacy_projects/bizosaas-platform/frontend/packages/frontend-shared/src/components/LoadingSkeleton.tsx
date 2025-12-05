/**
 * Loading Skeleton Component
 *
 * Shared across all frontend services to provide consistent loading states
 */

import React from 'react'

export interface LoadingSkeletonProps {
  count?: number
  height?: string
  className?: string
}

export const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({
  count = 1,
  height = '20px',
  className = ''
}) => {
  return (
    <>
      {Array.from({ length: count }).map((_, index) => (
        <div
          key={index}
          className={`animate-pulse bg-gray-200 rounded ${className}`}
          style={{ height, marginBottom: '8px' }}
        />
      ))}
    </>
  )
}

export default LoadingSkeleton

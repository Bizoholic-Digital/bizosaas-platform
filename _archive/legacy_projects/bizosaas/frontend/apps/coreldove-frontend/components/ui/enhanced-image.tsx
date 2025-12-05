'use client'

import React, { useState } from 'react'
import Image from 'next/image'
import { Package } from 'lucide-react'

interface EnhancedImageProps {
  src: string
  alt: string
  fill?: boolean
  width?: number
  height?: number
  className?: string
  priority?: boolean
  fallbackType?: 'primary' | 'secondary' | 'neutral'
  fallbackIcon?: React.ComponentType<{ className?: string }>
}

export function EnhancedImage({
  src,
  alt,
  fill = false,
  width,
  height,
  className = '',
  priority = false,
  fallbackType = 'primary',
  fallbackIcon: FallbackIcon = Package
}: EnhancedImageProps) {
  const [hasError, setHasError] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  const handleError = () => {
    setHasError(true)
    setIsLoading(false)
  }

  const handleLoad = () => {
    setIsLoading(false)
  }

  const getFallbackClassName = () => {
    switch (fallbackType) {
      case 'primary':
        return 'image-placeholder-primary'
      case 'secondary':
        return 'image-placeholder-secondary'
      default:
        return 'image-placeholder'
    }
  }

  if (hasError) {
    return (
      <div className={`w-full h-full ${getFallbackClassName()} ${className}`}>
        <FallbackIcon className="h-16 w-16" />
      </div>
    )
  }

  return (
    <>
      {isLoading && (
        <div className={`absolute inset-0 ${getFallbackClassName()} ${className}`}>
          <div className="animate-pulse">
            <FallbackIcon className="h-16 w-16 opacity-50" />
          </div>
        </div>
      )}
      <Image
        src={src}
        alt={alt}
        fill={fill}
        width={width}
        height={height}
        className={`${className} ${isLoading ? 'opacity-0' : 'opacity-100'} transition-opacity duration-300`}
        priority={priority}
        onError={handleError}
        onLoad={handleLoad}
      />
    </>
  )
}
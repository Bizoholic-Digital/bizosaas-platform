import React from 'react'

interface PlatformBrandingProps {
  platform?: string
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export function PlatformBranding({ platform = 'CLIENT_PORTAL', size = 'md', className }: PlatformBrandingProps) {
  const getTitle = () => {
    switch (platform) {
      case 'CLIENT_PORTAL':
        return 'Client Portal'
      case 'BIZOSAAS':
        return 'BizOSaaS'
      case 'BIZOHOLIC':
        return 'Bizoholic'
      default:
        return 'BizOSaaS'
    }
  }

  const getSizeClasses = () => {
    switch (size) {
      case 'sm':
        return { icon: 'w-6 h-6', title: 'text-sm font-medium', subtitle: 'text-xs' }
      case 'lg':
        return { icon: 'w-10 h-10', title: 'text-xl font-semibold', subtitle: 'text-sm' }
      default:
        return { icon: 'w-8 h-8', title: 'text-lg font-semibold', subtitle: 'text-sm' }
    }
  }

  const sizeClasses = getSizeClasses()

  return (
    <div className={className}>
      <div className="flex items-center space-x-2">
        <div className={`${sizeClasses.icon} bg-purple-600 rounded-lg flex items-center justify-center`}>
          <span className="text-white font-bold text-sm">
            {platform === 'CLIENT_PORTAL' ? 'CP' : platform === 'BIZOHOLIC' ? 'BH' : 'BS'}
          </span>
        </div>
        <div>
          <h3 className={`${sizeClasses.title} text-gray-900 dark:text-white`}>{getTitle()}</h3>
          <p className={`${sizeClasses.subtitle} text-gray-600 dark:text-gray-400`}>
            {platform === 'CLIENT_PORTAL' ? 'Customer Dashboard' : 'Platform Management'}
          </p>
        </div>
      </div>
    </div>
  )
}
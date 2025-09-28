'use client'

import Image from 'next/image'
import Link from 'next/link'
import { useTenantTheme } from '../theme/TenantThemeProvider'

interface LogoProps {
  href?: string
  className?: string
  width?: number
  height?: number
  priority?: boolean
  showText?: boolean
}

export function Logo({ 
  href = "/", 
  className = "", 
  width = 120, 
  height = 40,
  priority = false,
  showText = true
}: LogoProps) {
  const { config, loading } = useTenantTheme()

  // Use Bizoholic Digital logo as default to prevent flickering
  const logoSrc = loading ? '/bizoholic-logo-hq.png' : (config?.branding?.logo || '/bizoholic-logo-hq.png')
  const companyName = loading ? 'Bizoholic Digital' : (config?.branding?.companyName || 'Bizoholic Digital')
  const tagline = loading ? 'AI-Powered Marketing Solutions' : (config?.branding?.tagline || 'AI-Powered Marketing Solutions')

  const logoContent = (
    <div className={`flex items-center space-x-3 ${className}`}>
      <Image
        src={logoSrc}
        alt={`${companyName} Logo`}
        width={width}
        height={height}
        className="h-auto w-auto max-h-10"
        priority={priority}
        quality={100}
        style={{ 
          display: 'block',
          objectFit: 'contain'
        }}
        onError={(e) => {
          // Fallback to Bizoholic Digital logo
          e.currentTarget.src = '/bizoholic-logo-hq.png'
        }}
      />
      {showText && (
        <div className="flex flex-col">
          <span className="text-xl font-bold text-foreground">
            {companyName}
          </span>
          {tagline && (
            <span className="text-xs text-muted-foreground">
              {tagline}
            </span>
          )}
        </div>
      )}
    </div>
  )

  if (href) {
    return (
      <Link href={href} className="hover:opacity-80 transition-opacity">
        {logoContent}
      </Link>
    )
  }

  return logoContent
}

export default Logo
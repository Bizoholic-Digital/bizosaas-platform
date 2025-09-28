'use client'

import Image from 'next/image'
import Link from 'next/link'
import { useTenantTheme } from '@/hooks/useTenantTheme'
import { cn } from '@/lib/utils'

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
  const { config } = useTenantTheme()

  const logoContent = (
    <div className={cn("flex items-center space-x-3", className)}>
      <Image
        src={config.branding.logo}
        alt={`${config.branding.companyName} Logo`}
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
          // Fallback to a placeholder if logo fails to load
          e.currentTarget.src = '/logos/bizoholic-logo.png'
        }}
      />
      {showText && (
        <div className="flex flex-col">
          <span className="text-xl font-bold text-foreground">
            {config.branding.companyName}
          </span>
          {config.branding.tagline && (
            <span className="text-xs text-muted-foreground">
              {config.branding.tagline}
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
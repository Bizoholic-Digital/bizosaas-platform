import Link from 'next/link'
import { getPlatformConfig } from '@/lib/platform'

interface LogoProps {
  href?: string
  priority?: boolean
  showText?: boolean
  width?: number
  height?: number
  className?: string
}

export function Logo({ 
  href = '/', 
  showText = true, 
  width = 180, 
  height = 40, 
  className = '' 
}: LogoProps) {
  const config = getPlatformConfig()

  const LogoContent = () => (
    <div className={`flex items-center space-x-2 ${className}`}>
      <div 
        className="font-bold text-2xl bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent"
        style={{ width: `${width}px`, height: `${height}px`, lineHeight: `${height}px` }}
      >
        {config.name}
      </div>
      {showText && (
        <span className="text-sm text-muted-foreground">
          {config.description.split(' ').slice(0, 2).join(' ')}
        </span>
      )}
    </div>
  )

  if (href) {
    return (
      <Link href={href}>
        <LogoContent />
      </Link>
    )
  }

  return <LogoContent />
}
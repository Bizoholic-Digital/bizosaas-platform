"use client"

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { ArrowRight, Loader2, CheckCircle } from 'lucide-react'
import Link from 'next/link'

type ButtonState = 'default' | 'loading' | 'success'

interface ActionButtonProps {
  href?: string
  onClick?: () => Promise<void> | void
  children: React.ReactNode
  variant?: 'default' | 'outline' | 'ghost' | 'link' | 'destructive' | 'secondary'
  size?: 'default' | 'sm' | 'lg' | 'icon'
  className?: string
  showArrow?: boolean
  resetDelay?: number
}

export function ActionButton({
  href,
  onClick,
  children,
  variant = 'default',
  size = 'default',
  className = '',
  showArrow = false,
  resetDelay = 2000,
  ...props
}: ActionButtonProps) {
  const [state, setState] = useState<ButtonState>('default')

  const handleClick = async () => {
    if (onClick) {
      setState('loading')
      try {
        await onClick()
        setState('success')
        setTimeout(() => setState('default'), resetDelay)
      } catch (error) {
        setState('default')
        console.error('Button action failed:', error)
      }
    }
  }

  const getContent = () => {
    switch (state) {
      case 'loading':
        return (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Processing...
          </>
        )
      case 'success':
        return (
          <>
            <CheckCircle className="mr-2 h-4 w-4" />
            Success!
          </>
        )
      default:
        return (
          <>
            {children}
            {showArrow && <ArrowRight className="ml-2 h-4 w-4" />}
          </>
        )
    }
  }

  const getVariant = () => {
    switch (state) {
      case 'loading':
        return 'outline'
      case 'success':
        return 'default'
      default:
        return variant
    }
  }

  if (href && !onClick) {
    return (
      <Link href={href}>
        <Button
          variant={variant}
          size={size}
          className={`transition-all duration-200 ${className}`}
          {...props}
        >
          {children}
          {showArrow && <ArrowRight className="ml-2 h-4 w-4" />}
        </Button>
      </Link>
    )
  }

  return (
    <Button
      variant={getVariant()}
      size={size}
      className={`transition-all duration-200 ${className}`}
      onClick={handleClick}
      disabled={state === 'loading'}
      {...props}
    >
      {getContent()}
    </Button>
  )
}
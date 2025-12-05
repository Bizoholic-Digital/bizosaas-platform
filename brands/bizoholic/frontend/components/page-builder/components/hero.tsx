import React from 'react'
import { useNode } from '@craftjs/core'
import { cn } from '@/lib/utils'

interface HeroProps {
  title: string
  subtitle: string
  backgroundImage?: string
  backgroundColor?: {r: number, g: number, b: number, a: number}
  height?: string
  textColor?: string
  className?: string
}

export const Hero: React.FC<HeroProps> = ({
  title = 'Hero Title',
  subtitle = 'Hero subtitle text',
  backgroundImage,
  backgroundColor = {r: 59, g: 130, b: 246, a: 1},
  height = '400px',
  textColor = '#ffffff',
  className
}) => {
  const { connectors: {connect, drag}, selected, hovered } = useNode((state) => ({
    selected: state.events.selected,
    hovered: state.events.hovered
  }))

  const bgColor = `rgba(${backgroundColor.r}, ${backgroundColor.g}, ${backgroundColor.b}, ${backgroundColor.a})`

  return (
    <div
      ref={(ref) => {
        if (ref) connect(drag(ref));
      }}
      className={cn(
        'relative transition-all flex items-center justify-center text-center',
        selected && 'ring-2 ring-primary ring-offset-2',
        hovered && !selected && 'ring-1 ring-primary/50 ring-offset-1',
        className
      )}
      style={{
        height,
        backgroundColor: backgroundImage ? undefined : bgColor,
        backgroundImage: backgroundImage ? `url(${backgroundImage})` : undefined,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        color: textColor
      }}
    >
      {backgroundImage && (
        <div className="absolute inset-0 bg-black bg-opacity-40" />
      )}
      
      <div className="relative z-10 max-w-4xl mx-auto px-6">
        <h1 className="text-4xl md:text-6xl font-bold mb-6">
          {title}
        </h1>
        <p className="text-xl md:text-2xl opacity-90 max-w-2xl mx-auto">
          {subtitle}
        </p>
      </div>
      
      {selected && (
        <div className="absolute -top-8 left-0 bg-primary text-primary-foreground text-xs px-2 py-1 rounded">
          Hero Section
        </div>
      )}
    </div>
  )
}

(Hero as any).craft = {
  displayName: 'Hero',
  props: {
    title: 'Hero Title',
    subtitle: 'Hero subtitle text',
    backgroundImage: undefined,
    backgroundColor: {r: 59, g: 130, b: 246, a: 1},
    height: '400px',
    textColor: '#ffffff'
  },
  related: {
    toolbar: () => <div>Hero Settings</div>
  }
}
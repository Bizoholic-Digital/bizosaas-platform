import React from 'react'
import { useNode } from '@craftjs/core'
import { Button as UIButton } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface ButtonProps {
  text: string
  size?: 'sm' | 'default' | 'lg'
  variant?: 'default' | 'secondary' | 'outline' | 'ghost'
  margin?: string[]
  display?: 'inline' | 'block'
  width?: string
  className?: string
}

export const Button: React.FC<ButtonProps> = ({
  text = 'Click me',
  size = 'default',
  variant = 'default',
  margin = ['0', '0', '0', '0'],
  display = 'inline',
  width = 'auto',
  className
}) => {
  const { connectors: {connect, drag}, selected, hovered } = useNode((state) => ({
    selected: state.events.selected,
    hovered: state.events.hovered
  }))

  return (
    <div
      ref={(ref) => {
        if (ref) connect(drag(ref));
      }}
      className={cn(
        'relative transition-all',
        selected && 'ring-2 ring-primary ring-offset-2',
        hovered && !selected && 'ring-1 ring-primary/50 ring-offset-1',
        display === 'block' && 'block',
        className
      )}
      style={{
        marginTop: `${margin[0]}px`,
        marginRight: `${margin[1]}px`,
        marginBottom: `${margin[2]}px`,
        marginLeft: `${margin[3]}px`,
        width: width === 'auto' ? undefined : width
      }}
    >
      <UIButton 
        size={size} 
        variant={variant}
        style={{
          width: width === 'fit-content' ? 'fit-content' : width === 'auto' ? undefined : width
        }}
      >
        {text}
      </UIButton>
      {selected && (
        <div className="absolute -top-8 left-0 bg-primary text-primary-foreground text-xs px-2 py-1 rounded">
          Button
        </div>
      )}
    </div>
  )
}

(Button as any).craft = {
  displayName: 'Button',
  props: {
    text: 'Click me',
    size: 'default',
    variant: 'default',
    margin: ['0', '0', '0', '0'],
    display: 'inline',
    width: 'auto'
  },
  related: {
    toolbar: () => <div>Button Settings</div>
  }
}
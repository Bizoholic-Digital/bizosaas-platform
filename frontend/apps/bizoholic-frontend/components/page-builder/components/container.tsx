import React from 'react'
import { useNode } from '@craftjs/core'
import { cn } from '@/lib/utils'

interface ContainerProps {
  background?: {r: number, g: number, b: number, a: number}
  padding?: string[]
  margin?: string[]
  maxWidth?: string
  children: React.ReactNode
  className?: string
}

export const Container: React.FC<ContainerProps> = ({
  background = {r: 255, g: 255, b: 255, a: 1},
  padding = ['20', '20', '20', '20'],
  margin = ['0', '0', '0', '0'],
  maxWidth = 'none',
  children,
  className
}) => {
  const { connectors: {connect, drag}, selected, hovered } = useNode((state) => ({
    selected: state.events.selected,
    hovered: state.events.hovered
  }))

  const backgroundColor = `rgba(${background.r}, ${background.g}, ${background.b}, ${background.a})`

  return (
    <div
      ref={(ref) => {
        if (ref) connect(drag(ref));
      }}
      className={cn(
        'relative transition-all',
        selected && 'ring-2 ring-primary ring-offset-2',
        hovered && !selected && 'ring-1 ring-primary/50 ring-offset-1',
        className
      )}
      style={{
        backgroundColor,
        paddingTop: `${padding[0]}px`,
        paddingRight: `${padding[1]}px`,
        paddingBottom: `${padding[2]}px`,
        paddingLeft: `${padding[3]}px`,
        marginTop: `${margin[0]}px`,
        marginRight: `${margin[1]}px`,
        marginBottom: `${margin[2]}px`,
        marginLeft: `${margin[3]}px`,
        maxWidth: maxWidth === 'none' ? undefined : maxWidth
      }}
    >
      {children}
      {selected && (
        <div className="absolute -top-8 left-0 bg-primary text-primary-foreground text-xs px-2 py-1 rounded">
          Container
        </div>
      )}
    </div>
  )
}

(Container as any).craft = {
  displayName: 'Container',
  props: {
    background: {r: 255, g: 255, b: 255, a: 1},
    padding: ['20', '20', '20', '20'],
    margin: ['0', '0', '0', '0'],
    maxWidth: 'none'
  },
  related: {
    toolbar: () => <div>Container Settings</div>
  }
}
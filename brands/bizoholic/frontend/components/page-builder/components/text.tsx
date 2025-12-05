import React from 'react'
import { useNode } from '@craftjs/core'
import { cn } from '@/lib/utils'

interface TextProps {
  text: string
  fontSize?: number
  fontWeight?: number
  color?: string
  textAlign?: 'left' | 'center' | 'right'
  margin?: string[]
  className?: string
}

export const Text: React.FC<TextProps> = ({
  text = 'Edit this text',
  fontSize = 16,
  fontWeight = 400,
  color = '#000000',
  textAlign = 'left',
  margin = ['0', '0', '0', '0'],
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
        className
      )}
      style={{
        marginTop: `${margin[0]}px`,
        marginRight: `${margin[1]}px`,
        marginBottom: `${margin[2]}px`,
        marginLeft: `${margin[3]}px`,
      }}
    >
      <p
        style={{
          fontSize: `${fontSize}px`,
          fontWeight,
          color,
          textAlign,
          margin: 0
        }}
      >
        {text}
      </p>
      {selected && (
        <div className="absolute -top-8 left-0 bg-primary text-primary-foreground text-xs px-2 py-1 rounded">
          Text
        </div>
      )}
    </div>
  )
}

(Text as any).craft = {
  displayName: 'Text',
  props: {
    text: 'Edit this text',
    fontSize: 16,
    fontWeight: 400,
    color: '#000000',
    textAlign: 'left',
    margin: ['0', '0', '0', '0']
  },
  related: {
    toolbar: () => <div>Text Settings</div>
  }
}
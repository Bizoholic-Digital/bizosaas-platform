import React from 'react'
import { useNode } from '@craftjs/core'
import { Card as UICard, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { cn } from '@/lib/utils'

interface CardProps {
  title: string
  description: string
  icon?: string
  padding?: string[]
  margin?: string[]
  className?: string
}

export const Card: React.FC<CardProps> = ({
  title = 'Card Title',
  description = 'Card description text',
  icon = '✨',
  padding = ['24', '24', '24', '24'],
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
      <UICard className="h-full hover:shadow-lg transition-shadow">
        <CardHeader
          style={{
            paddingTop: `${padding[0]}px`,
            paddingRight: `${padding[1]}px`,
            paddingBottom: `${padding[2]}px`,
            paddingLeft: `${padding[3]}px`,
          }}
        >
          <div className="text-center">
            <div className="text-4xl mb-4">{icon}</div>
            <CardTitle className="text-lg">{title}</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="text-center">
          <p className="text-muted-foreground">{description}</p>
        </CardContent>
      </UICard>
      
      {selected && (
        <div className="absolute -top-8 left-0 bg-primary text-primary-foreground text-xs px-2 py-1 rounded">
          Card
        </div>
      )}
    </div>
  )
}

(Card as any).craft = {
  displayName: 'Card',
  props: {
    title: 'Card Title',
    description: 'Card description text',
    icon: '✨',
    padding: ['24', '24', '24', '24'],
    margin: ['0', '0', '0', '0']
  },
  related: {
    toolbar: () => <div>Card Settings</div>
  }
}
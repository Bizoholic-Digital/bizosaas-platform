'use client'

import { useState, useEffect } from 'react'
import { Wifi, WifiOff, RefreshCw } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'
import { useWebSocket } from '@/lib/websocket'

export function WebSocketStatus() {
  const { getConnectionState, reconnect } = useWebSocket()
  const [connectionState, setConnectionState] = useState<'connecting' | 'open' | 'closing' | 'closed'>('closed')

  useEffect(() => {
    const interval = setInterval(() => {
      setConnectionState(getConnectionState() ? 'open' : 'closed')
    }, 1000)

    return () => clearInterval(interval)
  }, [getConnectionState])

  const getStatusColor = () => {
    switch (connectionState) {
      case 'open':
        return 'bg-green-500'
      case 'connecting':
        return 'bg-yellow-500'
      case 'closing':
        return 'bg-orange-500'
      case 'closed':
        return 'bg-red-500'
      default:
        return 'bg-gray-500'
    }
  }

  const getStatusIcon = () => {
    switch (connectionState) {
      case 'open':
        return <Wifi className="h-3 w-3" />
      case 'connecting':
        return <RefreshCw className="h-3 w-3 animate-spin" />
      case 'closing':
        return <WifiOff className="h-3 w-3" />
      case 'closed':
        return <WifiOff className="h-3 w-3" />
      default:
        return <WifiOff className="h-3 w-3" />
    }
  }

  const getStatusText = () => {
    switch (connectionState) {
      case 'open':
        return 'Connected - Real-time updates active'
      case 'connecting':
        return 'Connecting to real-time server...'
      case 'closing':
        return 'Disconnecting from real-time server...'
      case 'closed':
        return 'Disconnected - Real-time updates unavailable'
      default:
        return 'Unknown connection state'
    }
  }

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div className="flex items-center gap-2">
            <div className="relative">
              <div className={`h-2 w-2 rounded-full ${getStatusColor()}`} />
              {connectionState === 'open' && (
                <div className={`absolute inset-0 rounded-full ${getStatusColor()} animate-ping opacity-75`} />
              )}
            </div>
            {connectionState === 'closed' && (
              <Button
                variant="ghost"
                size="sm"
                onClick={reconnect}
                className="h-6 px-2 text-xs"
              >
                Reconnect
              </Button>
            )}
          </div>
        </TooltipTrigger>
        <TooltipContent>
          <div className="flex items-center gap-2">
            {getStatusIcon()}
            <span>{getStatusText()}</span>
          </div>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}
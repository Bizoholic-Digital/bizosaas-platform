'use client'

import { useState, useEffect } from 'react'
import { Bell, X, CheckCircle, AlertTriangle, Info, XCircle, Zap } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { useWebSocket, WebSocketEvent, WebSocketEventType } from '@/lib/websocket'

interface Notification {
  id: string
  type: 'success' | 'warning' | 'error' | 'info'
  title: string
  message: string
  timestamp: string
  read: boolean
  eventType: WebSocketEventType
  data?: any
}

export function RealTimeNotifications() {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [isOpen, setIsOpen] = useState(false)
  const { subscribe, getConnectionState } = useWebSocket()

  useEffect(() => {
    // Subscribe to all real-time events
    const unsubscribers: (() => void)[] = []

    // Campaign updates
    unsubscribers.push(
      subscribe('campaign_update', (event) => {
        addNotification({
          type: 'info',
          title: 'Campaign Update',
          message: `Campaign "${event.data.campaign_name}" ${event.data.status}`,
          eventType: 'campaign_update',
          data: event.data
        })
      })
    )

    // Agent status changes
    unsubscribers.push(
      subscribe('agent_status_change', (event) => {
        const isError = event.data.status === 'error' || event.data.status === 'failed'
        addNotification({
          type: isError ? 'error' : 'info',
          title: 'AI Agent Status',
          message: `${event.data.agent_name} is now ${event.data.status}`,
          eventType: 'agent_status_change',
          data: event.data
        })
      })
    )

    // New leads
    unsubscribers.push(
      subscribe('lead_created', (event) => {
        addNotification({
          type: 'success',
          title: 'New Lead',
          message: `New lead from ${event.data.source}: ${event.data.name || event.data.email}`,
          eventType: 'lead_created',
          data: event.data
        })
      })
    )

    // System alerts
    unsubscribers.push(
      subscribe('system_alert', (event) => {
        addNotification({
          type: event.data.severity === 'critical' ? 'error' : 'warning',
          title: 'System Alert',
          message: event.data.message,
          eventType: 'system_alert',
          data: event.data
        })
      })
    )

    // Billing events
    unsubscribers.push(
      subscribe('billing_event', (event) => {
        const isError = event.data.type === 'payment_failed' || event.data.type === 'subscription_cancelled'
        addNotification({
          type: isError ? 'error' : 'success',
          title: 'Billing Update',
          message: event.data.message,
          eventType: 'billing_event',
          data: event.data
        })
      })
    )

    // Integration status
    unsubscribers.push(
      subscribe('integration_status', (event) => {
        addNotification({
          type: event.data.connected ? 'success' : 'warning',
          title: 'Integration Status',
          message: `${event.data.integration_name} ${event.data.connected ? 'connected' : 'disconnected'}`,
          eventType: 'integration_status',
          data: event.data
        })
      })
    )

    // Content generated
    unsubscribers.push(
      subscribe('content_generated', (event) => {
        addNotification({
          type: 'success',
          title: 'Content Ready',
          message: `AI generated ${event.data.content_type} for "${event.data.campaign_name}"`,
          eventType: 'content_generated',
          data: event.data
        })
      })
    )

    // Analytics updates
    unsubscribers.push(
      subscribe('analytics_update', (event) => {
        if (event.data.alert_type) {
          addNotification({
            type: event.data.alert_type === 'goal_achieved' ? 'success' : 'info',
            title: 'Analytics Alert',
            message: event.data.message,
            eventType: 'analytics_update',
            data: event.data
          })
        }
      })
    )

    return () => {
      unsubscribers.forEach(unsubscribe => unsubscribe())
    }
  }, [subscribe])

  const addNotification = (notificationData: Omit<Notification, 'id' | 'timestamp' | 'read'>) => {
    const notification: Notification = {
      id: Math.random().toString(36).substr(2, 9),
      timestamp: new Date().toISOString(),
      read: false,
      ...notificationData
    }

    setNotifications(prev => [notification, ...prev.slice(0, 49)]) // Keep only 50 notifications
  }

  const markAsRead = (id: string) => {
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n))
  }

  const markAllAsRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })))
  }

  const removeNotification = (id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id))
  }

  const clearAll = () => {
    setNotifications([])
  }

  const getNotificationIcon = (type: Notification['type']) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'warning':
        return <AlertTriangle className="h-4 w-4 text-yellow-500" />
      case 'error':
        return <XCircle className="h-4 w-4 text-red-500" />
      case 'info':
        return <Info className="h-4 w-4 text-blue-500" />
      default:
        return <Info className="h-4 w-4 text-gray-500" />
    }
  }

  const unreadCount = notifications.filter(n => !n.read).length
  const connectionState = getConnectionState()

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <Button variant="ghost" size="sm" className="relative">
          <Bell className="h-4 w-4" />
          {unreadCount > 0 && (
            <Badge 
              variant="destructive" 
              className="absolute -top-1 -right-1 h-5 w-5 rounded-full p-0 flex items-center justify-center text-xs"
            >
              {unreadCount > 99 ? '99+' : unreadCount}
            </Badge>
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent align="end" className="w-96 p-0">
        <Card className="border-0 shadow-none">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-lg">Notifications</CardTitle>
                <CardDescription className="flex items-center gap-2">
                  <Zap className="h-3 w-3" />
                  <span className={`capitalize ${connectionState === 'open' ? 'text-green-600' : 'text-red-600'}`}>
                    {connectionState}
                  </span>
                  {notifications.length > 0 && (
                    <>
                      • {unreadCount} unread
                    </>
                  )}
                </CardDescription>
              </div>
              {notifications.length > 0 && (
                <div className="flex gap-1">
                  {unreadCount > 0 && (
                    <Button variant="ghost" size="sm" onClick={markAllAsRead}>
                      Mark all read
                    </Button>
                  )}
                  <Button variant="ghost" size="sm" onClick={clearAll}>
                    Clear all
                  </Button>
                </div>
              )}
            </div>
          </CardHeader>
          <CardContent className="p-0">
            {notifications.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-8 text-center">
                <Bell className="h-8 w-8 text-muted-foreground mb-2" />
                <p className="text-sm text-muted-foreground">No notifications yet</p>
                <p className="text-xs text-muted-foreground">Real-time updates will appear here</p>
              </div>
            ) : (
              <ScrollArea className="h-96">
                <div className="space-y-1 p-3">
                  {notifications.map((notification) => (
                    <div
                      key={notification.id}
                      className={`relative flex gap-3 p-3 rounded-lg border cursor-pointer transition-colors ${
                        notification.read 
                          ? 'bg-muted/50 border-muted' 
                          : 'bg-background border-border hover:bg-muted/30'
                      }`}
                      onClick={() => !notification.read && markAsRead(notification.id)}
                    >
                      <div className="flex-shrink-0 mt-0.5">
                        {getNotificationIcon(notification.type)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <p className={`text-sm font-medium ${notification.read ? 'text-muted-foreground' : ''}`}>
                              {notification.title}
                            </p>
                            <p className={`text-xs ${notification.read ? 'text-muted-foreground' : 'text-muted-foreground'} mt-1`}>
                              {notification.message}
                            </p>
                            <p className="text-xs text-muted-foreground mt-1">
                              {new Date(notification.timestamp).toLocaleTimeString()}
                            </p>
                          </div>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-6 w-6 p-0 opacity-0 group-hover:opacity-100"
                            onClick={(e) => {
                              e.stopPropagation()
                              removeNotification(notification.id)
                            }}
                          >
                            <X className="h-3 w-3" />
                          </Button>
                        </div>
                        {!notification.read && (
                          <div className="absolute top-3 right-3 h-2 w-2 bg-primary rounded-full" />
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>
            )}
          </CardContent>
        </Card>
      </PopoverContent>
    </Popover>
  )
}
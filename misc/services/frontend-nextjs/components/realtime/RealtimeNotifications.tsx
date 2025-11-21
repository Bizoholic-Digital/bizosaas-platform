/**
 * Real-time Notification System
 * Live notifications with toast messages and notification center
 */

'use client';

import React, { useEffect, useState } from 'react';
import { 
  Bell, 
  X, 
  Check, 
  AlertTriangle, 
  Info, 
  CheckCircle2, 
  XCircle,
  ExternalLink,
  Filter,
  MoreHorizontal
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useRealtimeNotifications } from '@/lib/hooks/useRealtime';

interface ToastNotificationProps {
  notification: {
    id: string;
    title: string;
    message: string;
    severity: 'info' | 'warning' | 'error' | 'success';
    timestamp: number;
    category: 'system' | 'campaign' | 'lead' | 'payment' | 'ai_agent';
    action_url?: string;
    auto_dismiss?: boolean;
    dismiss_after?: number;
  };
  onDismiss: (id: string) => void;
  onAction?: (url: string) => void;
}

function ToastNotification({ notification, onDismiss, onAction }: ToastNotificationProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [isLeaving, setIsLeaving] = useState(false);

  const severityConfig = {
    info: {
      icon: Info,
      bgColor: 'bg-blue-50 border-blue-200',
      textColor: 'text-blue-800',
      iconColor: 'text-blue-600'
    },
    success: {
      icon: CheckCircle2,
      bgColor: 'bg-green-50 border-green-200',
      textColor: 'text-green-800',
      iconColor: 'text-green-600'
    },
    warning: {
      icon: AlertTriangle,
      bgColor: 'bg-yellow-50 border-yellow-200',
      textColor: 'text-yellow-800',
      iconColor: 'text-yellow-600'
    },
    error: {
      icon: XCircle,
      bgColor: 'bg-red-50 border-red-200',
      textColor: 'text-red-800',
      iconColor: 'text-red-600'
    }
  };

  const config = severityConfig[notification.severity];
  const IconComponent = config.icon;

  useEffect(() => {
    // Slide in animation
    setTimeout(() => setIsVisible(true), 100);

    // Auto dismiss
    if (notification.auto_dismiss && notification.dismiss_after) {
      setTimeout(() => {
        handleDismiss();
      }, notification.dismiss_after);
    }
  }, [notification]);

  const handleDismiss = () => {
    setIsLeaving(true);
    setTimeout(() => {
      onDismiss(notification.id);
    }, 300);
  };

  const handleAction = () => {
    if (notification.action_url && onAction) {
      onAction(notification.action_url);
    }
  };

  return (
    <div className={cn(
      "transform transition-all duration-300 ease-out",
      isVisible && !isLeaving ? "translate-x-0 opacity-100" : "translate-x-full opacity-0",
      isLeaving && "-translate-x-full opacity-0"
    )}>
      <div className={cn(
        "max-w-sm w-full shadow-lg rounded-lg border pointer-events-auto",
        config.bgColor
      )}>
        <div className="p-4">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <IconComponent className={cn("h-6 w-6", config.iconColor)} />
            </div>
            <div className="ml-3 w-0 flex-1 pt-0.5">
              <p className={cn("text-sm font-medium", config.textColor)}>
                {notification.title}
              </p>
              <p className={cn("mt-1 text-sm", config.textColor, "opacity-90")}>
                {notification.message}
              </p>
              {notification.action_url && (
                <div className="mt-3">
                  <button
                    onClick={handleAction}
                    className={cn(
                      "inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded",
                      "focus:outline-none focus:ring-2 focus:ring-offset-2",
                      notification.severity === 'info' && "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
                      notification.severity === 'success' && "bg-green-600 text-white hover:bg-green-700 focus:ring-green-500",
                      notification.severity === 'warning' && "bg-yellow-600 text-white hover:bg-yellow-700 focus:ring-yellow-500",
                      notification.severity === 'error' && "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500"
                    )}
                  >
                    View Details
                    <ExternalLink className="ml-1 h-3 w-3" />
                  </button>
                </div>
              )}
            </div>
            <div className="ml-4 flex-shrink-0 flex">
              <button
                onClick={handleDismiss}
                className={cn(
                  "rounded-md inline-flex focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
                  config.textColor, "opacity-70 hover:opacity-100"
                )}
              >
                <X className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Toast Container
export function RealtimeToastContainer() {
  const { notifications } = useRealtimeNotifications();
  const [toastNotifications, setToastNotifications] = useState<typeof notifications>([]);

  useEffect(() => {
    // Only show new notifications as toasts
    const newNotifications = notifications.filter(n => 
      !n.dismissed && 
      !toastNotifications.find(t => t.id === n.id) &&
      (Date.now() - n.timestamp) < 5000 // Only show notifications from last 5 seconds
    );

    if (newNotifications.length > 0) {
      setToastNotifications(prev => [...newNotifications, ...prev].slice(0, 5)); // Max 5 toasts
    }
  }, [notifications]);

  const handleDismiss = (id: string) => {
    setToastNotifications(prev => prev.filter(n => n.id !== id));
  };

  return (
    <div className="fixed top-4 right-4 z-50 space-y-4">
      {toastNotifications.map((notification) => (
        <ToastNotification
          key={notification.id}
          notification={notification}
          onDismiss={handleDismiss}
          onAction={(url) => window.open(url, '_blank')}
        />
      ))}
    </div>
  );
}

// Notification Center
interface NotificationCenterProps {
  isOpen: boolean;
  onClose: () => void;
}

export function RealtimeNotificationCenter({ isOpen, onClose }: NotificationCenterProps) {
  const { notifications, unreadCount, dismissNotification, dismissAll, markAsRead } = useRealtimeNotifications();
  const [filter, setFilter] = useState<'all' | 'unread' | 'system' | 'campaign' | 'lead' | 'payment' | 'ai_agent'>('all');

  const filteredNotifications = notifications.filter(notification => {
    if (filter === 'all') return true;
    if (filter === 'unread') return !notification.dismissed;
    return notification.category === filter;
  });

  const formatTime = (timestamp: number) => {
    const now = Date.now();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'Just now';
  };

  const severityConfig = {
    info: { icon: Info, color: 'text-blue-500' },
    success: { icon: CheckCircle2, color: 'text-green-500' },
    warning: { icon: AlertTriangle, color: 'text-yellow-500' },
    error: { icon: XCircle, color: 'text-red-500' }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      <div className="absolute inset-0 bg-black bg-opacity-50" onClick={onClose} />
      
      <div className="absolute right-0 top-0 h-full w-96 bg-white shadow-xl">
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold text-gray-900">Notifications</h2>
                {unreadCount > 0 && (
                  <p className="text-sm text-gray-600">{unreadCount} unread</p>
                )}
              </div>
              <div className="flex items-center space-x-2">
                {unreadCount > 0 && (
                  <button
                    onClick={dismissAll}
                    className="text-sm text-blue-600 hover:text-blue-800"
                  >
                    Mark all read
                  </button>
                )}
                <button
                  onClick={onClose}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>
            </div>

            {/* Filter */}
            <div className="mt-4">
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
              >
                <option value="all">All Notifications</option>
                <option value="unread">Unread Only</option>
                <option value="system">System</option>
                <option value="campaign">Campaigns</option>
                <option value="lead">Leads</option>
                <option value="payment">Payments</option>
                <option value="ai_agent">AI Agents</option>
              </select>
            </div>
          </div>

          {/* Notifications List */}
          <div className="flex-1 overflow-y-auto">
            {filteredNotifications.length === 0 ? (
              <div className="p-6 text-center text-gray-500">
                <Bell className="h-12 w-12 mx-auto mb-3 opacity-50" />
                <p>No notifications found</p>
              </div>
            ) : (
              <div className="space-y-0">
                {filteredNotifications.map((notification) => {
                  const config = severityConfig[notification.severity];
                  const IconComponent = config.icon;

                  return (
                    <div
                      key={notification.id}
                      className={cn(
                        "px-6 py-4 border-b border-gray-100 hover:bg-gray-50 transition-colors",
                        !notification.dismissed && "bg-blue-50"
                      )}
                    >
                      <div className="flex items-start space-x-3">
                        <IconComponent className={cn("h-5 w-5 mt-0.5", config.color)} />
                        
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between">
                            <p className="text-sm font-medium text-gray-900 truncate">
                              {notification.title}
                            </p>
                            <span className="text-xs text-gray-500 ml-2">
                              {formatTime(notification.timestamp)}
                            </span>
                          </div>
                          
                          <p className="text-sm text-gray-600 mt-1">
                            {notification.message}
                          </p>
                          
                          <div className="flex items-center justify-between mt-2">
                            <span className={cn(
                              "inline-flex items-center px-2 py-1 rounded-full text-xs font-medium",
                              notification.category === 'system' && "bg-gray-100 text-gray-800",
                              notification.category === 'campaign' && "bg-blue-100 text-blue-800",
                              notification.category === 'lead' && "bg-green-100 text-green-800",
                              notification.category === 'payment' && "bg-purple-100 text-purple-800",
                              notification.category === 'ai_agent' && "bg-orange-100 text-orange-800"
                            )}>
                              {notification.category.replace('_', ' ')}
                            </span>
                            
                            <div className="flex items-center space-x-2">
                              {notification.action_url && (
                                <button
                                  onClick={() => window.open(notification.action_url, '_blank')}
                                  className="text-blue-600 hover:text-blue-800"
                                >
                                  <ExternalLink className="h-4 w-4" />
                                </button>
                              )}
                              
                              {!notification.dismissed && (
                                <button
                                  onClick={() => markAsRead(notification.id)}
                                  className="text-gray-400 hover:text-gray-600"
                                >
                                  <Check className="h-4 w-4" />
                                </button>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// Notification Bell Icon with Badge
interface NotificationBellProps {
  onClick: () => void;
  className?: string;
}

export function RealtimeNotificationBell({ onClick, className }: NotificationBellProps) {
  const { unreadCount } = useRealtimeNotifications();

  return (
    <button
      onClick={onClick}
      className={cn(
        "relative p-2 text-gray-600 hover:text-gray-900 transition-colors",
        className
      )}
    >
      <Bell className="h-6 w-6" />
      {unreadCount > 0 && (
        <span className="absolute -top-1 -right-1 h-5 w-5 bg-red-500 text-white text-xs font-medium rounded-full flex items-center justify-center animate-pulse">
          {unreadCount > 99 ? '99+' : unreadCount}
        </span>
      )}
    </button>
  );
}

export default RealtimeNotificationCenter;
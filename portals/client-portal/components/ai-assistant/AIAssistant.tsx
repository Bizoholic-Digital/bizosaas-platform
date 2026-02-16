"use client";

import React, { useEffect, useRef, useCallback } from 'react';
import { 
  MessageSquare, 
  X, 
  Minus, 
  Plus,
  Wifi,
  WifiOff,
  Trash2,
  Settings,
  HelpCircle
} from 'lucide-react';
import { useAIAssistant } from './hooks/useAIAssistant';
import { MessageBubble } from './MessageBubble';
import { ChatInput } from './ChatInput';
import { TypingIndicator } from './TypingIndicator';
import { Button } from '../ui/button';
import { Card, CardContent, CardHeader } from '../ui/card';
import { Badge } from '../ui/badge';
import { ScrollArea } from '../ui/scroll-area';
import { cn } from '@/lib/utils';

interface AIAssistantProps {
  initialContext?: {
    userId: string;
    tenantId: string;
    currentPage?: string;
    userProfile?: any;
  };
  className?: string;
}

export function AIAssistant({ initialContext, className }: AIAssistantProps) {
  const {
    conversation,
    isOpen,
    isMinimized,
    isTyping,
    isConnected,
    openAssistant,
    closeAssistant,
    toggleMinimize,
    startConversation,
    endConversation,
    clearHistory,
    sendMessage,
    handleQuickAction,
    startVoiceInput,
    provideFeedback,
    isVoiceAvailable
  } = useAIAssistant();

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    if (conversation?.messages.length) {
      scrollToBottom();
    }
  }, [conversation?.messages.length, scrollToBottom]);

  // Initialize conversation when assistant opens
  useEffect(() => {
    if (isOpen && !conversation && initialContext) {
      startConversation({
        userId: initialContext.userId,
        tenantId: initialContext.tenantId,
        currentPage: initialContext.currentPage || window.location.pathname,
        userProfile: initialContext.userProfile,
        recentActions: [],
        platformContext: {
          activeFeatures: [],
          recentAlerts: [],
          accountStatus: { health: 'good' }
        }
      });
    }
  }, [isOpen, conversation, initialContext, startConversation]);

  const handleFileUpload = useCallback((files: FileList) => {
    // Handle file upload logic
    const fileNames = Array.from(files).map(f => f.name).join(', ');
    sendMessage(`I've uploaded these files: ${fileNames}. How can you help me with them?`);
  }, [sendMessage]);

  if (!isOpen) {
    return (
      <Button
        onClick={openAssistant}
        className={cn(
          "fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg z-50",
          "hover:scale-110 transition-transform duration-200",
          className
        )}
        aria-label="Open AI Assistant"
      >
        <MessageSquare className="h-6 w-6" />
      </Button>
    );
  }

  return (
    <div className={cn(
      "fixed bottom-6 right-6 w-96 h-[32rem] z-50 flex flex-col",
      "shadow-2xl border rounded-lg bg-background",
      isMinimized && "h-14",
      className
    )}>
      {/* Header */}
      <CardHeader className="flex flex-row items-center justify-between space-y-0 p-4 border-b">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2">
            <MessageSquare className="h-5 w-5 text-primary" />
            <h3 className="font-semibold text-sm">AI Assistant</h3>
          </div>
          
          {/* Connection Status */}
          <Badge 
            variant={isConnected ? "default" : "destructive"}
            className="text-xs"
          >
            {isConnected ? (
              <Wifi className="h-3 w-3 mr-1" />
            ) : (
              <WifiOff className="h-3 w-3 mr-1" />
            )}
            {isConnected ? 'Online' : 'Offline'}
          </Badge>
        </div>

        <div className="flex items-center gap-1">
          {/* Clear History */}
          {conversation && !isMinimized && (
            <Button
              variant="ghost"
              size="sm"
              onClick={clearHistory}
              className="h-8 w-8 p-0"
              title="Clear conversation"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          )}

          {/* Minimize/Maximize */}
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleMinimize}
            className="h-8 w-8 p-0"
            title={isMinimized ? "Expand" : "Minimize"}
          >
            {isMinimized ? (
              <Plus className="h-4 w-4" />
            ) : (
              <Minus className="h-4 w-4" />
            )}
          </Button>

          {/* Close */}
          <Button
            variant="ghost"
            size="sm"
            onClick={closeAssistant}
            className="h-8 w-8 p-0"
            title="Close assistant"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>

      {/* Chat Content */}
      {!isMinimized && (
        <>
          {/* Messages Area */}
          <div className="flex-1 flex flex-col min-h-0">
            {conversation ? (
              <ScrollArea 
                ref={messagesContainerRef}
                className="flex-1 p-4"
              >
                <div className="space-y-4">
                  {conversation.messages.map((message) => (
                    <MessageBubble
                      key={message.id}
                      message={message}
                      onQuickAction={handleQuickAction}
                      onFeedback={provideFeedback}
                    />
                  ))}
                  
                  {/* Typing Indicator */}
                  {isTyping && <TypingIndicator />}
                  
                  {/* Scroll anchor */}
                  <div ref={messagesEndRef} />
                </div>
              </ScrollArea>
            ) : (
              <div className="flex-1 flex items-center justify-center p-4">
                <div className="text-center text-muted-foreground">
                  <MessageSquare className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p className="text-sm">Starting conversation...</p>
                </div>
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="border-t p-4">
            <ChatInput
              onSendMessage={sendMessage}
              onStartVoiceInput={isVoiceAvailable ? startVoiceInput : undefined}
              onFileUpload={handleFileUpload}
              isLoading={isTyping}
              isVoiceAvailable={isVoiceAvailable}
              placeholder="Ask me anything about your account, analytics, or platform features..."
              disabled={!isConnected}
            />
          </div>
        </>
      )}

      {/* Minimized State Content */}
      {isMinimized && conversation && (
        <div className="flex-1 flex items-center px-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>{conversation.messages.length} messages</span>
            {isTyping && (
              <>
                <span>•</span>
                <span className="text-primary">AI typing...</span>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// Assistant trigger button for when closed
export function AIAssistantTrigger({ 
  onClick, 
  className 
}: { 
  onClick: () => void; 
  className?: string; 
}) {
  return (
    <Button
      onClick={onClick}
      className={cn(
        "fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg z-40",
        "hover:scale-110 transition-transform duration-200",
        "bg-primary hover:bg-primary/90",
        className
      )}
      aria-label="Open AI Assistant"
    >
      <MessageSquare className="h-6 w-6" />
    </Button>
  );
}
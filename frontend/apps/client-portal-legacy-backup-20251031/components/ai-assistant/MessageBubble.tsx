"use client";

import React, { useState } from 'react';
import { format } from 'date-fns';
import { 
  Bot, 
  User, 
  ThumbsUp, 
  ThumbsDown, 
  Copy, 
  ExternalLink,
  Clock,
  CheckCircle
} from 'lucide-react';
import { Message, QuickAction } from './types';
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar';
import { Button } from '../ui/button';
import { Card, CardContent } from '../ui/card';
import { Badge } from '../ui/badge';
import { cn } from '@/lib/utils';

interface MessageBubbleProps {
  message: Message;
  onQuickAction?: (action: QuickAction) => void;
  onFeedback?: (messageId: string, feedback: 'positive' | 'negative', comment?: string) => void;
  className?: string;
}

export function MessageBubble({ 
  message, 
  onQuickAction, 
  onFeedback,
  className 
}: MessageBubbleProps) {
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedbackComment, setFeedbackComment] = useState('');
  const [copiedText, setCopiedText] = useState(false);

  const isUser = message.type === 'user';
  const isSystem = message.type === 'system';

  const handleCopyMessage = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopiedText(true);
      setTimeout(() => setCopiedText(false), 2000);
    } catch (error) {
      console.error('Failed to copy text:', error);
    }
  };

  const handleFeedback = (type: 'positive' | 'negative') => {
    onFeedback?.(message.id, type, feedbackComment || undefined);
    setShowFeedback(false);
    setFeedbackComment('');
  };

  const renderQuickActions = () => {
    if (!message.metadata?.actions?.length) return null;

    return (
      <div className="flex flex-wrap gap-2 mt-3">
        {message.metadata.actions.map((action) => (
          <Button
            key={action.id}
            variant={action.variant as any || 'outline'}
            size="sm"
            onClick={() => onQuickAction?.(action)}
            className="text-xs"
          >
            {action.icon && (
              <span className="mr-1">
                {getIconByName(action.icon)}
              </span>
            )}
            {action.label}
            {action.type === 'link' && (
              <ExternalLink className="ml-1 h-3 w-3" />
            )}
          </Button>
        ))}
      </div>
    );
  };

  const renderMessageContent = () => {
    // Handle markdown-like formatting
    const content = message.content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code class="bg-muted px-1 rounded text-sm">$1</code>');

    return (
      <div 
        className="prose prose-sm max-w-none"
        dangerouslySetInnerHTML={{ __html: content }}
      />
    );
  };

  const renderAttachments = () => {
    if (!message.metadata?.attachments?.length) return null;

    return (
      <div className="mt-3 space-y-2">
        {message.metadata.attachments.map((attachment) => (
          <div key={attachment.id} className="border rounded-md p-3">
            {attachment.type === 'table' && (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  {/* Table rendering logic would go here */}
                  <caption className="text-xs text-muted-foreground">
                    {attachment.caption}
                  </caption>
                </table>
              </div>
            )}
            {attachment.type === 'chart' && (
              <div className="w-full h-48 bg-muted rounded flex items-center justify-center">
                <span className="text-muted-foreground">Chart: {attachment.caption}</span>
              </div>
            )}
            {attachment.type === 'image' && attachment.url && (
              <img 
                src={attachment.url} 
                alt={attachment.caption} 
                className="max-w-full h-auto rounded"
              />
            )}
          </div>
        ))}
      </div>
    );
  };

  const renderFollowUpQuestions = () => {
    if (!message.metadata?.followUpQuestions?.length) return null;

    return (
      <div className="mt-3">
        <p className="text-sm text-muted-foreground mb-2">Related questions:</p>
        <div className="space-y-1">
          {message.metadata.followUpQuestions.map((question, index) => (
            <button
              key={index}
              onClick={() => onQuickAction?.({
                id: `followup_${index}`,
                label: question,
                type: 'command',
                action: 'send_message',
                variant: 'outline'
              })}
              className="block text-left text-sm text-primary hover:underline"
            >
              • {question}
            </button>
          ))}
        </div>
      </div>
    );
  };

  if (isSystem) {
    return (
      <div className={cn("flex justify-center my-4", className)}>
        <Badge variant="secondary" className="text-xs">
          <Clock className="mr-1 h-3 w-3" />
          {message.content}
        </Badge>
      </div>
    );
  }

  return (
    <div className={cn(
      "flex gap-3 mb-4",
      isUser ? "flex-row-reverse" : "flex-row",
      className
    )}>
      {/* Avatar */}
      <Avatar className="h-8 w-8 flex-shrink-0">
        <AvatarFallback className={cn(
          isUser ? "bg-primary text-primary-foreground" : "bg-muted"
        )}>
          {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
        </AvatarFallback>
      </Avatar>

      {/* Message Content */}
      <div className={cn(
        "flex-1 max-w-[80%]",
        isUser ? "items-end" : "items-start"
      )}>
        <Card className={cn(
          "relative",
          isUser 
            ? "bg-primary text-primary-foreground ml-12" 
            : "bg-muted mr-12"
        )}>
          <CardContent className="p-3">
            {/* Message Text */}
            {renderMessageContent()}
            
            {/* Quick Actions */}
            {renderQuickActions()}
            
            {/* Attachments */}
            {renderAttachments()}
            
            {/* Follow-up Questions */}
            {renderFollowUpQuestions()}
            
            {/* Message Metadata */}
            <div className="flex items-center justify-between mt-2 pt-2 border-t border-border/20">
              <div className="flex items-center gap-2 text-xs opacity-70">
                <span>{format(message.timestamp, 'HH:mm')}</span>
                {message.metadata?.intent && (
                  <Badge variant="outline" className="text-xs">
                    {message.metadata.intent}
                  </Badge>
                )}
                {message.metadata?.confidence && (
                  <span>
                    {Math.round(message.metadata.confidence * 100)}%
                  </span>
                )}
              </div>
              
              {/* Message Actions */}
              <div className="flex items-center gap-1">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleCopyMessage}
                  className="h-6 w-6 p-0 opacity-70 hover:opacity-100"
                >
                  {copiedText ? (
                    <CheckCircle className="h-3 w-3" />
                  ) : (
                    <Copy className="h-3 w-3" />
                  )}
                </Button>
                
                {!isUser && onFeedback && (
                  <>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleFeedback('positive')}
                      className="h-6 w-6 p-0 opacity-70 hover:opacity-100 hover:text-green-600"
                    >
                      <ThumbsUp className="h-3 w-3" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setShowFeedback(true)}
                      className="h-6 w-6 p-0 opacity-70 hover:opacity-100 hover:text-red-600"
                    >
                      <ThumbsDown className="h-3 w-3" />
                    </Button>
                  </>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Feedback Form */}
        {showFeedback && (
          <Card className="mt-2 p-3 border-destructive/20">
            <div className="space-y-2">
              <p className="text-sm font-medium">Help us improve</p>
              <textarea
                value={feedbackComment}
                onChange={(e) => setFeedbackComment(e.target.value)}
                placeholder="What could be better about this response?"
                className="w-full p-2 text-sm border rounded resize-none"
                rows={2}
              />
              <div className="flex gap-2">
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={() => handleFeedback('negative')}
                >
                  Submit Feedback
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setShowFeedback(false)}
                >
                  Cancel
                </Button>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}

// Helper function to get icons by name
function getIconByName(iconName: string) {
  const icons: Record<string, React.ReactNode> = {
    'user': <User className="h-3 w-3" />,
    'bar-chart': <Bot className="h-3 w-3" />,
    'help-circle': <Bot className="h-3 w-3" />,
  };
  
  return icons[iconName] || <Bot className="h-3 w-3" />;
}
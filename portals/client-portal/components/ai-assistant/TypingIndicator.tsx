"use client";

import React from 'react';
import { Bot } from 'lucide-react';
import { Avatar, AvatarFallback } from '../ui/avatar';
import { Card, CardContent } from '../ui/card';
import { cn } from '@/lib/utils';

interface TypingIndicatorProps {
  className?: string;
}

export function TypingIndicator({ className }: TypingIndicatorProps) {
  return (
    <div className={cn("flex gap-3 mb-4", className)}>
      {/* Avatar */}
      <Avatar className="h-8 w-8 flex-shrink-0">
        <AvatarFallback className="bg-muted">
          <Bot className="h-4 w-4" />
        </AvatarFallback>
      </Avatar>

      {/* Typing bubble */}
      <div className="flex-1 max-w-[80%]">
        <Card className="bg-muted mr-12">
          <CardContent className="p-3">
            <div className="flex items-center gap-1">
              <span className="text-sm text-muted-foreground">AI is typing</span>
              <div className="flex gap-1 ml-2">
                <div className="w-2 h-2 bg-muted-foreground/60 rounded-full animate-bounce [animation-delay:-0.3s]" />
                <div className="w-2 h-2 bg-muted-foreground/60 rounded-full animate-bounce [animation-delay:-0.15s]" />
                <div className="w-2 h-2 bg-muted-foreground/60 rounded-full animate-bounce" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
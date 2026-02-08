"use client";

import React, { useState, useRef, useCallback } from 'react';
import { 
  Send, 
  Mic, 
  MicOff, 
  Paperclip, 
  Smile,
  Loader2,
  Square
} from 'lucide-react';
import { Button } from '../ui/button';
import { Textarea } from '../ui/textarea';
import { cn } from '@/lib/utils';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  onStartVoiceInput?: () => Promise<string | null>;
  onFileUpload?: (files: FileList) => void;
  isLoading?: boolean;
  isVoiceAvailable?: boolean;
  placeholder?: string;
  maxLength?: number;
  disabled?: boolean;
  className?: string;
}

export function ChatInput({
  onSendMessage,
  onStartVoiceInput,
  onFileUpload,
  isLoading = false,
  isVoiceAvailable = false,
  placeholder = "Type your message...",
  maxLength = 2000,
  disabled = false,
  className
}: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [isVoiceRecording, setIsVoiceRecording] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = useCallback((e?: React.FormEvent) => {
    e?.preventDefault();
    
    if (!message.trim() || isLoading || disabled) return;
    
    onSendMessage(message.trim());
    setMessage('');
    
    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  }, [message, isLoading, disabled, onSendMessage]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  }, [handleSubmit]);

  const handleVoiceInput = useCallback(async () => {
    if (!onStartVoiceInput || isVoiceRecording) return;

    setIsVoiceRecording(true);
    try {
      const transcript = await onStartVoiceInput();
      if (transcript) {
        setMessage(prev => prev + (prev ? ' ' : '') + transcript);
        
        // Auto-resize textarea
        if (textareaRef.current) {
          textareaRef.current.style.height = 'auto';
          textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
        }
      }
    } catch (error) {
      console.error('Voice input error:', error);
    } finally {
      setIsVoiceRecording(false);
    }
  }, [onStartVoiceInput, isVoiceRecording]);

  const handleFileSelect = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0 && onFileUpload) {
      onFileUpload(files);
    }
    // Reset input
    e.target.value = '';
  }, [onFileUpload]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files && files.length > 0 && onFileUpload) {
      onFileUpload(files);
    }
  }, [onFileUpload]);

  const handleTextareaChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    if (value.length <= maxLength) {
      setMessage(value);
      
      // Auto-resize
      e.target.style.height = 'auto';
      e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
    }
  }, [maxLength]);

  const canSend = message.trim().length > 0 && !isLoading && !disabled;

  return (
    <div className={cn("relative", className)}>
      {/* Drag overlay */}
      {isDragOver && (
        <div className="absolute inset-0 bg-primary/10 border-2 border-dashed border-primary rounded-lg flex items-center justify-center z-10">
          <div className="text-center">
            <Paperclip className="h-8 w-8 mx-auto mb-2 text-primary" />
            <p className="text-sm font-medium">Drop files here to attach</p>
          </div>
        </div>
      )}

      {/* File input */}
      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        multiple
        accept="image/*,.pdf,.doc,.docx,.txt"
        onChange={handleFileChange}
      />

      {/* Main input area */}
      <form onSubmit={handleSubmit} className="space-y-2">
        <div 
          className={cn(
            "relative border rounded-lg bg-background transition-colors",
            isDragOver && "border-primary bg-primary/5",
            disabled && "opacity-50"
          )}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          {/* Textarea */}
          <Textarea
            ref={textareaRef}
            value={message}
            onChange={handleTextareaChange}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled || isLoading}
            className={cn(
              "min-h-[44px] max-h-[120px] resize-none border-0 focus-visible:ring-0 pr-24",
              "placeholder:text-muted-foreground"
            )}
            style={{ height: 'auto' }}
          />

          {/* Input controls */}
          <div className="absolute right-2 bottom-2 flex items-center gap-1">
            {/* File upload button */}
            {onFileUpload && (
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={handleFileSelect}
                disabled={disabled || isLoading}
                className="h-8 w-8 p-0"
              >
                <Paperclip className="h-4 w-4" />
              </Button>
            )}

            {/* Voice input button */}
            {isVoiceAvailable && onStartVoiceInput && (
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={handleVoiceInput}
                disabled={disabled || isLoading}
                className={cn(
                  "h-8 w-8 p-0",
                  isVoiceRecording && "text-red-500 animate-pulse"
                )}
              >
                {isVoiceRecording ? (
                  <Square className="h-4 w-4" />
                ) : (
                  <Mic className="h-4 w-4" />
                )}
              </Button>
            )}

            {/* Send button */}
            <Button
              type="submit"
              size="sm"
              disabled={!canSend}
              className="h-8 w-8 p-0"
            >
              {isLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </div>
        </div>

        {/* Character counter and status */}
        <div className="flex items-center justify-between text-xs text-muted-foreground px-1">
          <div className="flex items-center gap-2">
            {isVoiceRecording && (
              <span className="text-red-500 animate-pulse flex items-center gap-1">
                <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
                Recording...
              </span>
            )}
            {isLoading && (
              <span className="text-primary flex items-center gap-1">
                <Loader2 className="h-3 w-3 animate-spin" />
                AI is thinking...
              </span>
            )}
          </div>
          
          <div className="flex items-center gap-2">
            {message.length > 0 && (
              <span className={cn(
                message.length > maxLength * 0.8 && "text-orange-500",
                message.length >= maxLength && "text-red-500"
              )}>
                {message.length}/{maxLength}
              </span>
            )}
          </div>
        </div>
      </form>

      {/* Quick suggestions */}
      {message.length === 0 && !isLoading && (
        <div className="mt-2 flex flex-wrap gap-1">
          {[
            "Check my account status",
            "Show analytics overview",
            "Help with integration",
            "Report a problem"
          ].map((suggestion) => (
            <Button
              key={suggestion}
              variant="outline"
              size="sm"
              onClick={() => setMessage(suggestion)}
              className="text-xs h-6"
            >
              {suggestion}
            </Button>
          ))}
        </div>
      )}
    </div>
  );
}
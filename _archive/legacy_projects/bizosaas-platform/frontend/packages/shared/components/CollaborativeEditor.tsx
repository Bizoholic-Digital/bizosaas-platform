/**
 * Collaborative Editor Component for BizOSaaS Platform
 * Provides real-time collaborative editing with AI assistance
 * Integrates with all 5 platforms: Bizoholic, CoreLDove, Business Directory, ThrillRing, QuantTrade
 */

import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { BizOSaaSCollaborationClient } from '../collaboration-client.js';

interface CollaboratorPresence {
  user_id: string;
  status: 'active' | 'idle' | 'away';
  cursor_position?: number;
  last_activity: string;
}

interface DocumentOperation {
  operation_id: string;
  operation_type: 'insert' | 'delete' | 'replace';
  position: number;
  length: number;
  content: string;
  user_id: string;
  timestamp: string;
}

interface AIResponse {
  response: string;
  query: string;
  agent_assignments?: Record<string, string>;
}

interface CollaborativeEditorProps {
  // Configuration
  tenantId: string;
  userId: string;
  platform: 'bizoholic' | 'coreldove' | 'business-directory' | 'thrillring' | 'quanttrade';
  documentId?: string;
  brainApiUrl?: string;

  // Content
  initialContent?: string;
  documentType?: 'campaign_brief' | 'content_strategy' | 'seo_report' | 'social_media_plan' | 'general_document';

  // Features
  enableAIAssistance?: boolean;
  enableRealTimeEditing?: boolean;
  enableUserPresence?: boolean;
  readOnly?: boolean;

  // Callbacks
  onContentChange?: (content: string) => void;
  onSave?: (content: string) => void;
  onError?: (error: Error) => void;

  // Styling
  className?: string;
  placeholder?: string;
  rows?: number;
}

export const CollaborativeEditor: React.FC<CollaborativeEditorProps> = ({
  tenantId,
  userId,
  platform,
  documentId,
  brainApiUrl = 'ws://localhost:8001',
  initialContent = '',
  documentType = 'general_document',
  enableAIAssistance = true,
  enableRealTimeEditing = true,
  enableUserPresence = true,
  readOnly = false,
  onContentChange,
  onSave,
  onError,
  className = '',
  placeholder = 'Start typing...',
  rows = 10
}) => {
  // State
  const [content, setContent] = useState(initialContent);
  const [isConnected, setIsConnected] = useState(false);
  const [collaborators, setCollaborators] = useState<Map<string, CollaboratorPresence>>(new Map());
  const [aiAssistantReady, setAIAssistantReady] = useState(false);
  const [isAIThinking, setIsAIThinking] = useState(false);
  const [aiResponses, setAIResponses] = useState<AIResponse[]>([]);
  const [showAIPanel, setShowAIPanel] = useState(false);
  const [isTyping, setIsTyping] = useState<Map<string, boolean>>(new Map());
  const [cursorPosition, setCursorPosition] = useState(0);

  // Refs
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const collaborationClientRef = useRef<BizOSaaSCollaborationClient | null>(null);
  const typingTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Memoized client configuration
  const clientConfig = useMemo(() => ({
    brainApiUrl,
    tenantId,
    userId,
    platform,
    scope: documentId ? 'document-specific' : 'tenant-wide',
    scopeId: documentId || 'general',
    debug: process.env.NODE_ENV === 'development'
  }), [brainApiUrl, tenantId, userId, platform, documentId]);

  // Initialize collaboration client
  useEffect(() => {
    if (!enableRealTimeEditing && !enableAIAssistance) return;

    const client = new BizOSaaSCollaborationClient(clientConfig);
    collaborationClientRef.current = client;

    // Connection events
    client.on('connected', handleConnected);
    client.on('disconnected', handleDisconnected);
    client.on('error', handleConnectionError);

    // Collaboration events
    if (enableRealTimeEditing) {
      client.on('collaboration-state-updated', handleCollaborationStateUpdated);
      client.on('user-joined', handleUserJoined);
      client.on('user-left', handleUserLeft);
      client.on('document-edit', handleDocumentEdit);
      client.on('cursor-position', handleCursorPosition);
      client.on('user-typing', handleUserTyping);
    }

    // AI events
    if (enableAIAssistance) {
      client.on('ai-assistant-ready', handleAIAssistantReady);
      client.on('ai-response', handleAIResponse);
      client.on('ai-thinking', handleAIThinking);
    }

    // Connect
    client.connect();

    // Cleanup
    return () => {
      client.disconnect();
      if (typingTimeoutRef.current) {
        clearTimeout(typingTimeoutRef.current);
      }
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }
    };
  }, [clientConfig, enableRealTimeEditing, enableAIAssistance]);

  // Event handlers
  const handleConnected = useCallback((data: any) => {
    setIsConnected(true);
    console.log('Connected to collaboration service:', data);
  }, []);

  const handleDisconnected = useCallback((data: any) => {
    setIsConnected(false);
    console.log('Disconnected from collaboration service:', data);
  }, []);

  const handleConnectionError = useCallback((error: any) => {
    console.error('Collaboration connection error:', error);
    onError?.(new Error('Collaboration connection failed'));
  }, [onError]);

  const handleCollaborationStateUpdated = useCallback((data: any) => {
    const newCollaborators = new Map();
    Object.entries(data.participants).forEach(([userId, presence]: [string, any]) => {
      newCollaborators.set(userId, presence);
    });
    setCollaborators(newCollaborators);
  }, []);

  const handleUserJoined = useCallback((presence: CollaboratorPresence) => {
    setCollaborators(prev => new Map(prev.set(presence.user_id, presence)));
  }, []);

  const handleUserLeft = useCallback((data: any) => {
    setCollaborators(prev => {
      const newMap = new Map(prev);
      // Remove user - we need user_id from metadata
      const userIdToRemove = Object.keys(Object.fromEntries(newMap)).find(id =>
        newMap.get(id)?.user_id === data.user_id
      );
      if (userIdToRemove) {
        newMap.delete(userIdToRemove);
      }
      return newMap;
    });
  }, []);

  const handleDocumentEdit = useCallback((operation: DocumentOperation) => {
    if (operation.user_id === userId) return; // Don't apply our own operations

    // Apply the operation to content
    setContent(prevContent => {
      let newContent = prevContent;

      switch (operation.operation_type) {
        case 'insert':
          newContent = prevContent.slice(0, operation.position) +
                     operation.content +
                     prevContent.slice(operation.position);
          break;
        case 'delete':
          newContent = prevContent.slice(0, operation.position) +
                     prevContent.slice(operation.position + operation.length);
          break;
        case 'replace':
          newContent = prevContent.slice(0, operation.position) +
                     operation.content +
                     prevContent.slice(operation.position + operation.length);
          break;
      }

      return newContent;
    });
  }, [userId]);

  const handleCursorPosition = useCallback((data: any) => {
    // Update collaborator cursor positions
    setCollaborators(prev => {
      const newMap = new Map(prev);
      const userPresence = newMap.get(data.user_id);
      if (userPresence) {
        newMap.set(data.user_id, {
          ...userPresence,
          cursor_position: data.position
        });
      }
      return newMap;
    });
  }, []);

  const handleUserTyping = useCallback((data: any) => {
    setIsTyping(prev => new Map(prev.set(data.user_id, data.is_typing)));

    // Clear typing indicator after timeout
    setTimeout(() => {
      setIsTyping(prev => {
        const newMap = new Map(prev);
        newMap.delete(data.user_id);
        return newMap;
      });
    }, 3000);
  }, []);

  const handleAIAssistantReady = useCallback((data: any) => {
    setAIAssistantReady(true);
    console.log('AI Assistant ready:', data);
  }, []);

  const handleAIResponse = useCallback((response: AIResponse) => {
    setIsAIThinking(false);
    setAIResponses(prev => [...prev, response]);
  }, []);

  const handleAIThinking = useCallback((data: any) => {
    setIsAIThinking(true);
  }, []);

  // Content change handler
  const handleContentChange = useCallback((event: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newContent = event.target.value;
    const previousContent = content;

    setContent(newContent);
    onContentChange?.(newContent);

    // Send real-time edit operations
    if (enableRealTimeEditing && collaborationClientRef.current && isConnected) {
      // Calculate operation (simplified)
      const operation: Partial<DocumentOperation> = {
        operation_type: newContent.length > previousContent.length ? 'insert' : 'delete',
        position: event.target.selectionStart || 0,
        content: newContent,
        user_id: userId
      };

      collaborationClientRef.current.sendDocumentEdit(operation);
    }

    // Send typing indicator
    if (enableRealTimeEditing && collaborationClientRef.current && isConnected) {
      collaborationClientRef.current.sendTypingIndicator(true, documentId);

      // Clear typing timeout and set new one
      if (typingTimeoutRef.current) {
        clearTimeout(typingTimeoutRef.current);
      }

      typingTimeoutRef.current = setTimeout(() => {
        collaborationClientRef.current?.sendTypingIndicator(false, documentId);
      }, 1000);
    }

    // Auto-save with debounce
    if (saveTimeoutRef.current) {
      clearTimeout(saveTimeoutRef.current);
    }

    saveTimeoutRef.current = setTimeout(() => {
      onSave?.(newContent);
    }, 2000);
  }, [content, enableRealTimeEditing, isConnected, userId, documentId, onContentChange, onSave]);

  // Cursor position handler
  const handleCursorChange = useCallback((event: React.SyntheticEvent<HTMLTextAreaElement>) => {
    const target = event.target as HTMLTextAreaElement;
    const position = target.selectionStart;
    setCursorPosition(position);

    // Send cursor position to collaborators
    if (enableRealTimeEditing && collaborationClientRef.current && isConnected) {
      collaborationClientRef.current.sendCursorPosition({
        position,
        user_id: userId,
        timestamp: new Date().toISOString()
      });
    }
  }, [enableRealTimeEditing, isConnected, userId]);

  // AI assistance functions
  const askAI = useCallback(async (query: string) => {
    if (!enableAIAssistance || !collaborationClientRef.current || !aiAssistantReady) {
      return;
    }

    try {
      setIsAIThinking(true);
      await collaborationClientRef.current.sendAIQuery(query, {
        document_type: documentType,
        current_content: content,
        cursor_position: cursorPosition,
        platform: platform
      });
    } catch (error) {
      setIsAIThinking(false);
      onError?.(error as Error);
    }
  }, [enableAIAssistance, aiAssistantReady, documentType, content, cursorPosition, platform, onError]);

  // Get collaborator indicators
  const getCollaboratorIndicators = () => {
    return Array.from(collaborators.values())
      .filter(collaborator => collaborator.user_id !== userId)
      .map(collaborator => (
        <div
          key={collaborator.user_id}
          className="flex items-center space-x-2 text-sm"
        >
          <div
            className={`w-2 h-2 rounded-full ${
              collaborator.status === 'active' ? 'bg-green-500' :
              collaborator.status === 'idle' ? 'bg-yellow-500' : 'bg-gray-500'
            }`}
          />
          <span>{collaborator.user_id}</span>
          {isTyping.get(collaborator.user_id) && (
            <span className="text-gray-500 italic">typing...</span>
          )}
        </div>
      ));
  };

  return (
    <div className={`collaborative-editor ${className}`}>
      {/* Header with connection status and collaborators */}
      <div className="flex items-center justify-between mb-4 p-3 bg-gray-50 rounded-lg">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div
              className={`w-3 h-3 rounded-full ${
                isConnected ? 'bg-green-500' : 'bg-red-500'
              }`}
            />
            <span className="text-sm font-medium">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>

          {enableAIAssistance && (
            <div className="flex items-center space-x-2">
              <div
                className={`w-3 h-3 rounded-full ${
                  aiAssistantReady ? 'bg-blue-500' : 'bg-gray-400'
                }`}
              />
              <span className="text-sm">
                AI Assistant {aiAssistantReady ? 'Ready' : 'Loading...'}
              </span>
            </div>
          )}
        </div>

        {enableUserPresence && (
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">Collaborators:</span>
            <div className="flex flex-col space-y-1">
              {getCollaboratorIndicators()}
            </div>
          </div>
        )}
      </div>

      {/* Main editor area */}
      <div className="flex space-x-4">
        {/* Text editor */}
        <div className="flex-1">
          <textarea
            ref={textareaRef}
            value={content}
            onChange={handleContentChange}
            onSelect={handleCursorChange}
            onClick={handleCursorChange}
            onKeyUp={handleCursorChange}
            placeholder={placeholder}
            rows={rows}
            readOnly={readOnly}
            className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none font-mono"
          />

          {enableRealTimeEditing && (
            <div className="mt-2 text-xs text-gray-500">
              Auto-save enabled • Real-time collaboration active
            </div>
          )}
        </div>

        {/* AI Assistant Panel */}
        {enableAIAssistance && (
          <div className="w-96">
            <button
              onClick={() => setShowAIPanel(!showAIPanel)}
              className="w-full mb-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              {showAIPanel ? 'Hide' : 'Show'} AI Assistant
            </button>

            {showAIPanel && (
              <div className="border border-gray-300 rounded-lg p-4 bg-white">
                <h3 className="font-semibold mb-3">AI Assistant</h3>

                {/* Quick actions */}
                <div className="mb-4">
                  <h4 className="text-sm font-medium mb-2">Quick Actions:</h4>
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      onClick={() => askAI('Improve the writing style and grammar')}
                      disabled={!aiAssistantReady || isAIThinking}
                      className="px-3 py-2 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors disabled:opacity-50"
                    >
                      Improve Writing
                    </button>
                    <button
                      onClick={() => askAI('Optimize for SEO')}
                      disabled={!aiAssistantReady || isAIThinking}
                      className="px-3 py-2 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors disabled:opacity-50"
                    >
                      SEO Optimize
                    </button>
                    <button
                      onClick={() => askAI('Make it more engaging')}
                      disabled={!aiAssistantReady || isAIThinking}
                      className="px-3 py-2 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors disabled:opacity-50"
                    >
                      More Engaging
                    </button>
                    <button
                      onClick={() => askAI('Create a summary')}
                      disabled={!aiAssistantReady || isAIThinking}
                      className="px-3 py-2 text-xs bg-gray-100 hover:bg-gray-200 rounded transition-colors disabled:opacity-50"
                    >
                      Summarize
                    </button>
                  </div>
                </div>

                {/* AI thinking indicator */}
                {isAIThinking && (
                  <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <div className="animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full"></div>
                      <span className="text-sm text-blue-700">AI is thinking...</span>
                    </div>
                  </div>
                )}

                {/* AI responses */}
                <div className="max-h-64 overflow-y-auto">
                  {aiResponses.map((response, index) => (
                    <div key={index} className="mb-3 p-3 bg-gray-50 rounded-lg">
                      <div className="text-xs text-gray-600 mb-1">
                        Query: {response.query}
                      </div>
                      <div className="text-sm">{response.response}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default CollaborativeEditor;
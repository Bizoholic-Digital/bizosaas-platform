"use client"

import React, { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Input } from '@/components/ui/input'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  MessageCircle, Send, Mic, MicOff, Bot, User,
  Activity, BarChart3, Settings, Users, Zap,
  CheckCircle, AlertTriangle, Clock, Loader2,
  TrendingUp, DollarSign, Target, Eye, Play,
  Pause, Square, RefreshCw, Download, X
} from 'lucide-react'
import { useAuth } from '@/hooks/use-auth'
import { useWebSocket } from '@/lib/websocket-client'
import { AICommandProcessor } from '@/lib/ai-command-processor'
import { ConversationalMemoryManager, ConversationMessage } from '@/lib/conversational-memory-manager'
import { ConversationHistory } from './conversation-history'
import { DocumentUpload } from './document-upload'
import { ModelSelector } from './model-selector'
import { HumanEscalation } from './human-escalation'
import { LanguageSelector } from './language-selector'
import { VoiceControls } from './voice-controls'
import { FeedbackWidget } from './feedback-widget'
import { AnalyticsDashboard } from './analytics-dashboard'
import { SentimentAnalyzer, SentimentResult } from '@/lib/sentiment-analyzer'
import { ConversationAnalyticsManager } from '@/lib/conversation-analytics'

interface ChatMessage {
  id: string
  type: 'user' | 'ai' | 'system' | 'action_result'
  content: string
  timestamp: string
  metadata?: {
    action?: string
    workflow_id?: string
    agent_id?: string
    data?: any
    actions?: any[]
    responseTime?: number
    sentiment?: any
    document_id?: string
    document_type?: string
    escalation?: any
    attachments?: Array<{
      type: 'chart' | 'table' | 'workflow' | 'report'
      title: string
      data: any
    }>
  }
}

interface ConversationContext {
  tenant_id: string
  user_role: string
  current_workflow?: string
  active_agents: string[]
  recent_queries: string[]
  session_context: Record<string, any>
}

interface AIResponse {
  message: string
  actions?: Array<{
    type: 'execute_workflow' | 'query_analytics' | 'control_agent' | 'system_command'
    payload: any
  }>
  suggestions?: string[]
  intent?: string
  context_update?: Partial<ConversationContext>
}

export function PrimaryAIInterface({ onTabNavigate }: { onTabNavigate?: (tabId: string) => void }) {
  const { user } = useAuth()
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const [suggestions, setSuggestions] = useState<string[]>([])
  const [context, setContext] = useState<ConversationContext>({
    tenant_id: user?.tenant_id || 'demo',
    user_role: user?.role || 'user',
    active_agents: [],
    recent_queries: [],
    session_context: {}
  })
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null)
  const [isTyping, setIsTyping] = useState(false)
  const [errorState, setErrorState] = useState<{
    hasError: boolean
    message?: string
    suggestions?: string[]
    retryAction?: () => void
  }>({ hasError: false })
  const [conversationMetrics, setConversationMetrics] = useState({
    messagesCount: 0,
    successfulResponses: 0,
    errors: 0,
    averageResponseTime: 0
  })
  const [selectedModel, setSelectedModel] = useState<string>('')
  const [currentSentiment, setCurrentSentiment] = useState<SentimentResult | null>(null)
  const [voiceSpeakFunction, setVoiceSpeakFunction] = useState<((text: string) => Promise<void>) | null>(null)
  const [showAnalytics, setShowAnalytics] = useState(false)

  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const commandProcessor = useRef<AICommandProcessor | null>(null)
  const memoryManager = useRef<ConversationalMemoryManager | null>(null)
  const sentimentAnalyzer = useRef<SentimentAnalyzer | null>(null)
  const analyticsManager = useRef<ConversationAnalyticsManager | null>(null)

  const { client, isConnected } = useWebSocket({
    tenantId: context.tenant_id,
    userRole: context.user_role,
    userId: user?.id || 'demo-user'
  })

  useEffect(() => {
    // Initialize command processor with tab navigation callback
    commandProcessor.current = new AICommandProcessor(
      process.env.NEXT_PUBLIC_API_BASE_URL || 'https://api.bizoholic.net',
      user?.role || 'user',
      user?.tenant_id || 'demo',
      onTabNavigate
    )

    // Initialize conversational memory manager
    memoryManager.current = new ConversationalMemoryManager(
      process.env.NEXT_PUBLIC_API_BASE_URL || 'https://api.bizoholic.net',
      user?.tenant_id || 'demo',
      user?.id || 'demo-user'
    )

    // Initialize sentiment analyzer
    sentimentAnalyzer.current = new SentimentAnalyzer()

    // Initialize analytics manager
    analyticsManager.current = new ConversationAnalyticsManager(
      process.env.NEXT_PUBLIC_API_BASE_URL || 'https://api.bizoholic.net',
      user?.tenant_id || 'demo',
      user?.id || 'demo-user'
    )

    // Initialize session
    initializeConversationSession()

    // Initialize with welcome message
    const welcomeMessage: ChatMessage = {
      id: 'welcome',
      type: 'ai',
      content: `Hello ${user?.first_name || 'there'}! 👋 I'm your BizOSaaS AI assistant. 

I can help you with ALL dashboard functions through natural language:

📊 **Analytics & Reporting**: "Show me today's revenue" or "What's our conversion rate?"
🤖 **AI Agent Management**: "Start marketing campaign workflow" or "Check agent status"
👥 **User & Tenant Management**: "Add new user" or "Update permissions"
⚡ **Workflow Creation**: "Create product sourcing workflow for electronics"
📈 **Real-time Monitoring**: "Show live metrics" or "Alert me when conversions drop"
🧭 **Dashboard Navigation**: "Switch to Overview tab" or "Open Agents Monitor"
📅 **Calendar & Scheduling**: "Show calendar" or "Schedule new meeting"
🏢 **Tenant Management**: "Show tenant metrics" or "Compare performance"

**New**: I can access ALL existing dashboard features - just tell me what you want to see!

What would you like to do today?`,
      timestamp: new Date().toISOString()
    }

    setMessages([welcomeMessage])

    // Set initial suggestions with dashboard navigation
    setSuggestions([
      "Show me today's analytics",
      "Switch to Overview tab",
      "Check active AI agents",
      "Open Agents Monitor",
      "Show system status",
      "Switch to Calendar tab"
    ])
  }, [user])

  // Initialize conversation session
  const initializeConversationSession = async () => {
    if (!memoryManager.current) return

    try {
      const sessionId = await memoryManager.current.initializeSession()
      setCurrentSessionId(sessionId)

      // Start analytics tracking
      if (analyticsManager.current) {
        analyticsManager.current.startConversationTracking(
          `conversation_${Date.now()}`,
          sessionId
        )
      }

      // Update suggestions based on context
      const contextualSuggestions = memoryManager.current.generateContextualSuggestions()
      if (contextualSuggestions.length > 0) {
        setSuggestions(prev => [...contextualSuggestions, ...prev.slice(contextualSuggestions.length)])
      }
    } catch (error) {
      console.error('Failed to initialize conversation session:', error)
    }
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (!client) return

    // Listen for real-time updates that should be communicated to user
    const unsubscribeActivity = client.onMessage('system_notification', (message) => {
      const notification: ChatMessage = {
        id: `notification_${Date.now()}`,
        type: 'system',
        content: `🔔 ${message.data.message}`,
        timestamp: new Date().toISOString(),
        metadata: message.data
      }
      setMessages(prev => [...prev, notification])
    })

    const unsubscribeWorkflow = client.onMessage('workflow_status_update', (message) => {
      const update: ChatMessage = {
        id: `workflow_${message.data.workflow_id}_${Date.now()}`,
        type: 'system',
        content: `⚡ Workflow "${message.data.workflow_name}" is now ${message.data.status}`,
        timestamp: new Date().toISOString(),
        metadata: message.data
      }
      setMessages(prev => [...prev, update])
    })

    return () => {
      unsubscribeActivity()
      unsubscribeWorkflow()
    }
  }, [client])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const processAICommand = async (userInput: string): Promise<AIResponse> => {
    if (!commandProcessor.current) {
      return {
        message: '❌ Command processor not initialized. Please refresh the page.',
        suggestions: ['Refresh page', 'Try again']
      }
    }

    try {
      return await commandProcessor.current.processCommand(userInput)
    } catch (error) {
      console.error('Command processing error:', error)
      return {
        message: `❌ **Error processing command**: ${userInput}

Please try rephrasing your request or contact support if the issue persists.

**Quick suggestions**:
• "Show analytics"
• "Check system status"
• "Help with workflows"`,
        suggestions: [
          'Show system status',
          'Help me get started',
          'What can you do?'
        ]
      }
    }
  }






  // Enhanced error handling with context-aware suggestions
  const handleError = (error: any, context: string, originalInput: string) => {
    console.error(`Error in ${context}:`, error)

    let errorMessage = '❌ Something went wrong. '
    let suggestions = ['Try again', 'Check system status', 'Contact support']
    let retryAction: (() => void) | undefined

    // Context-aware error handling
    if (context === 'command_processing') {
      errorMessage += "I couldn't process your request. Here are some things you can try:"
      suggestions = [
        'Rephrase your request more clearly',
        'Try a simpler command',
        'Ask "What can you help me with?"',
        'Check if the service is running'
      ]
      retryAction = () => {
        setInputMessage(originalInput)
        inputRef.current?.focus()
      }
    } else if (context === 'network_error') {
      errorMessage += "I'm having trouble connecting to the server."
      suggestions = [
        'Check your internet connection',
        'Retry in a few seconds',
        'Refresh the page',
        'Contact your administrator'
      ]
      retryAction = () => handleSendMessage()
    } else if (context === 'session_error') {
      errorMessage += "There's an issue with your session."
      suggestions = [
        'Refresh the page',
        'Log out and log back in',
        'Clear browser cache',
        'Try a different browser'
      ]
    }

    setErrorState({
      hasError: true,
      message: errorMessage,
      suggestions,
      retryAction
    })

    // Update metrics
    setConversationMetrics(prev => ({
      ...prev,
      errors: prev.errors + 1
    }))

    // Auto-clear error after 10 seconds
    setTimeout(() => {
      setErrorState({ hasError: false })
    }, 10000)
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const startTime = performance.now()
    const userMessage: ChatMessage = {
      id: `user_${Date.now()}`,
      type: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setIsTyping(true)
    setErrorState({ hasError: false }) // Clear any previous errors

    const currentInput = inputMessage
    setInputMessage('')

    // Analyze sentiment of user input
    let sentimentResult: SentimentResult | null = null
    if (sentimentAnalyzer.current) {
      sentimentResult = sentimentAnalyzer.current.analyzeSentiment(currentInput)
      setCurrentSentiment(sentimentResult)
    }

    // Update metrics
    setConversationMetrics(prev => ({
      ...prev,
      messagesCount: prev.messagesCount + 1
    }))

    // Track user message in analytics
    if (analyticsManager.current) {
      analyticsManager.current.trackMessage('user', undefined, sentimentResult?.score)
    }

    // Store user message in conversational memory
    if (memoryManager.current) {
      try {
        await memoryManager.current.addMessage('user', currentInput, {
          sentiment: sentimentResult
        })
      } catch (error) {
        console.warn('Failed to store message in memory:', error)
        // Continue processing even if memory storage fails
      }
    }

    try {
      // Simulate typing delay for better UX
      await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 1200))

      // Process the command with AI
      const aiResponse = await processAICommand(currentInput)
      const endTime = performance.now()
      const responseTime = endTime - startTime

      // Enhance AI response with sentiment awareness
      let enhancedMessage = aiResponse.message
      if (sentimentResult && sentimentAnalyzer.current) {
        // Add empathetic response if needed
        const empatheticPrefix = sentimentAnalyzer.current.generateEmpatheticResponse(sentimentResult, currentInput)
        if (empatheticPrefix) {
          enhancedMessage = empatheticPrefix + enhancedMessage
        }

        // Adjust tone based on sentiment
        enhancedMessage = sentimentAnalyzer.current.adjustToneForSentiment(enhancedMessage, sentimentResult)
      }

      // Add AI response
      const aiMessage: ChatMessage = {
        id: `ai_${Date.now()}`,
        type: 'ai',
        content: enhancedMessage,
        timestamp: new Date().toISOString(),
        metadata: {
          actions: aiResponse.actions,
          responseTime: Math.round(responseTime),
          sentiment: sentimentResult
        }
      }

      setMessages(prev => [...prev, aiMessage])

      // Track AI response in analytics
      if (analyticsManager.current) {
        analyticsManager.current.trackMessage('ai', responseTime, sentimentResult?.score)
        analyticsManager.current.trackCommand(
          aiResponse.intent || 'general',
          true,
          responseTime
        )
      }

      // Auto-speak AI response if voice is enabled
      if (voiceSpeakFunction) {
        try {
          await voiceSpeakFunction(enhancedMessage)
        } catch (error) {
          console.warn('Failed to speak AI response:', error)
        }
      }

      // Update metrics
      setConversationMetrics(prev => ({
        ...prev,
        successfulResponses: prev.successfulResponses + 1,
        averageResponseTime: (prev.averageResponseTime * prev.successfulResponses + responseTime) / (prev.successfulResponses + 1)
      }))

      // Store AI message in conversational memory
      if (memoryManager.current) {
        try {
          await memoryManager.current.addMessage('ai', aiResponse.message, {
            actions: aiResponse.actions,
            context_update: aiResponse.context_update,
            responseTime
          })
        } catch (error) {
          console.warn('Failed to store AI response in memory:', error)
        }
      }

      // Update suggestions - prioritize contextual suggestions
      if (memoryManager.current) {
        const contextualSuggestions = memoryManager.current.generateContextualSuggestions()
        if (contextualSuggestions.length > 0) {
          setSuggestions(contextualSuggestions)
        } else if (aiResponse.suggestions) {
          setSuggestions(aiResponse.suggestions)
        }
      } else if (aiResponse.suggestions) {
        setSuggestions(aiResponse.suggestions)
      }

      // Update context
      if (aiResponse.context_update) {
        setContext(prev => ({ ...prev, ...aiResponse.context_update }))
      }

      // Execute actions if any
      if (aiResponse.actions) {
        for (const action of aiResponse.actions) {
          try {
            await executeAction(action)
          } catch (actionError) {
            console.error('Action execution failed:', actionError)
            // Don't break the flow for individual action failures
          }
        }
      }

    } catch (error) {
      // Track error in analytics
      if (analyticsManager.current) {
        analyticsManager.current.trackError('command_processing', { userInput: currentInput, error })
        analyticsManager.current.trackCommand(
          'unknown',
          false,
          performance.now() - startTime
        )
      }

      handleError(error, 'command_processing', currentInput)

      const errorMessage: ChatMessage = {
        id: `error_${Date.now()}`,
        type: 'ai',
        content: `❌ I encountered an issue processing your request. I've noted this for improvement.

**What you can try:**
• Rephrase your request more clearly
• Try a simpler command
• Ask "What can you help me with?"
• Check if all services are running

Would you like me to help you with something else?`,
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])

      // Store error in memory for context
      if (memoryManager.current) {
        try {
          await memoryManager.current.addMessage('ai', errorMessage.content, { error: true })
        } catch (memError) {
          console.warn('Failed to store error in memory:', memError)
        }
      }
    } finally {
      setIsLoading(false)
      setIsTyping(false)
    }
  }

  const executeAction = async (action: any) => {
    if (!commandProcessor.current) return

    try {
      const result = await commandProcessor.current.executeAction(action)

      // Add the result as a new AI message
      const resultMessage: ChatMessage = {
        id: `action_result_${Date.now()}`,
        type: 'action_result',
        content: result.message,
        timestamp: new Date().toISOString(),
        metadata: {
          action: action.type,
          data: result
        }
      }

      setMessages(prev => [...prev, resultMessage])

      // Update suggestions if provided
      if (result.suggestions) {
        setSuggestions(result.suggestions)
      }
    } catch (error) {
      console.error('Action execution error:', error)
      const errorMessage: ChatMessage = {
        id: `action_error_${Date.now()}`,
        type: 'ai',
        content: `❌ Failed to execute action: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  // Handle conversation restoration
  const handleRestoreConversation = async (sessionId: string) => {
    if (!memoryManager.current) return

    try {
      setIsLoading(true)
      const newSessionId = await memoryManager.current.initializeSession(sessionId)
      setCurrentSessionId(newSessionId)

      // Load conversation history
      const history = memoryManager.current.getRecentHistory(50)
      const chatMessages: ChatMessage[] = history.map(msg => ({
        id: msg.id,
        type: msg.type as 'user' | 'ai' | 'system' | 'action_result',
        content: msg.content,
        timestamp: msg.timestamp,
        metadata: msg.metadata
      }))

      setMessages(chatMessages)

      // Update contextual suggestions
      const contextualSuggestions = memoryManager.current.generateContextualSuggestions()
      if (contextualSuggestions.length > 0) {
        setSuggestions(contextualSuggestions)
      }
    } catch (error) {
      console.error('Failed to restore conversation:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Handle message reference
  const handleReferenceMessage = (message: ConversationMessage) => {
    const referenceText = `[Referring to previous message: "${message.content.substring(0, 100)}${message.content.length > 100 ? '...' : ''}"]

`
    setInputMessage(prev => referenceText + prev)
    inputRef.current?.focus()
  }

  // Handle document processed
  const handleDocumentProcessed = async (document: any) => {
    const notification: ChatMessage = {
      id: `doc_processed_${Date.now()}`,
      type: 'system',
      content: `📄 Document "${document.filename}" has been processed successfully${document.metadata?.ecommerce_potential
        ? ` and ${document.metadata.product_count} products were detected.`
        : '.'
        }
      
${document.metadata?.ai_analysis || 'Ready for analysis and import operations.'}`,
      timestamp: new Date().toISOString(),
      metadata: {
        document_id: document.id,
        document_type: document.file_type
      }
    }

    setMessages(prev => [...prev, notification])

    // Store in conversational memory
    if (memoryManager.current) {
      await memoryManager.current.addMessage('system', notification.content, {
        document_id: document.id,
        document_type: document.file_type
      })
    }
  }

  // Handle document reference
  const handleReferenceDocument = (document: any) => {
    const referenceText = `[Document: "${document.filename}" - ${document.metadata?.ai_analysis || 'uploaded document'}]

`
    setInputMessage(prev => referenceText + prev)
    inputRef.current?.focus()

    // Add contextual suggestions for document operations
    const docSuggestions = []
    if (document.metadata?.ecommerce_potential) {
      docSuggestions.push(
        `Import products from ${document.filename}`,
        `Analyze ${document.filename} for product data`,
        `Show structure of ${document.filename}`
      )
    } else {
      docSuggestions.push(
        `Analyze content of ${document.filename}`,
        `Summarize ${document.filename}`,
        `Extract insights from ${document.filename}`
      )
    }

    setSuggestions(prev => [...docSuggestions, ...prev.slice(0, 3)])
  }

  const handleSuggestionClick = (suggestion: string) => {
    setInputMessage(suggestion)
    inputRef.current?.focus()
  }

  // Handle voice input from voice controls
  const handleVoiceInput = (text: string, confidence: number) => {
    // Set the voice input as the message
    setInputMessage(text)

    // Auto-submit if confidence is high enough
    if (confidence > 0.8) {
      // Slight delay to show the recognized text first
      setTimeout(() => {
        handleSendMessage()
      }, 500)
    } else {
      // Focus input for user to review and potentially edit
      inputRef.current?.focus()
    }
  }

  // Handle voice input start
  const startVoiceInput = () => {
    setIsListening(!isListening)
    // This would be connected to the VoiceControls component
  }

  // Set up voice speak function callback
  const handleVoiceSpeakSetup = (speakFn: (text: string) => Promise<void>) => {
    setVoiceSpeakFunction(() => speakFn)
  }

  const renderMessage = (message: ChatMessage) => {
    const isUser = message.type === 'user'
    const isSystem = message.type === 'system'

    return (
      <div
        key={message.id}
        className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
      >
        <div className={`flex max-w-[85%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start gap-3`}>
          <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isUser ? 'bg-blue-500' : isSystem ? 'bg-yellow-500' : 'bg-green-500'
            }`}>
            {isUser ? (
              <User className="w-4 h-4 text-white" />
            ) : isSystem ? (
              <Activity className="w-4 h-4 text-white" />
            ) : (
              <Bot className="w-4 h-4 text-white" />
            )}
          </div>

          <div className={`rounded-lg p-4 ${isUser
            ? 'bg-blue-500 text-white'
            : isSystem
              ? 'bg-yellow-50 text-yellow-900 border border-yellow-200'
              : 'bg-gray-50 text-gray-900 border border-gray-200'
            }`}>
            <div className="whitespace-pre-wrap text-sm leading-relaxed">
              {message.content}
            </div>

            <div className="mt-2 flex items-center justify-between">
              <div className="text-xs opacity-70">
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>

              {/* Feedback Widget for AI responses */}
              {!isUser && !isSystem && message.type === 'ai' && analyticsManager.current && (
                <FeedbackWidget
                  conversationId={analyticsManager.current.getCurrentMetrics()?.conversationId}
                  messageId={message.id}
                  messageContent={messages.find(m => m.timestamp < message.timestamp && m.type === 'user')?.content}
                  aiResponse={message.content}
                  onSubmitFeedback={async (feedback: any) => {
                    if (analyticsManager.current) {
                      return await analyticsManager.current.submitFeedback({
                        ...feedback,
                        conversationId: analyticsManager.current.getCurrentMetrics()?.conversationId || 'demo',
                        messageId: message.id
                      })
                    }
                    return false
                  }}
                  className="ml-2"
                />
              )}
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Main component render
  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b bg-white">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="font-semibold text-lg">BizOSaaS AI Assistant</h2>
            <p className="text-sm text-muted-foreground">
              Primary Admin Interface • {context.user_role} • {isConnected ? '🟢 Connected' : '🔴 Offline'}
              {memoryManager.current && (
                <span className="ml-2">
                  • Context: {memoryManager.current.getConversationContext()?.current_focus || 'general'}
                </span>
              )}
              <span className="ml-2">
                • {conversationMetrics.messagesCount} msgs • {conversationMetrics.successfulResponses} success
                {conversationMetrics.averageResponseTime > 0 && (
                  <span> • {Math.round(conversationMetrics.averageResponseTime)}ms avg</span>
                )}
              </span>
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="text-xs">
            {context.tenant_id}
          </Badge>

          {/* Language Selector */}
          <LanguageSelector />

          {/* Model Selector */}
          <ModelSelector
            selectedModel={selectedModel}
            onModelChange={setSelectedModel}
          />

          {/* Conversation History */}
          {memoryManager.current && (
            <ConversationHistory
              memoryManager={memoryManager.current}
              onRestoreConversation={handleRestoreConversation}
              onReferenceMessage={handleReferenceMessage}
            />
          )}

          {/* Document Upload */}
          <DocumentUpload
            onDocumentProcessed={handleDocumentProcessed}
            onReferenceDocument={handleReferenceDocument}
          />

          {/* Voice Controls */}
          <VoiceControls
            onVoiceInput={handleVoiceInput}
            onSpeakResponse={handleVoiceSpeakSetup}
            autoSpeakResponses={true}
          />

          {/* Analytics Dashboard Toggle */}
          <Button
            variant={showAnalytics ? "default" : "outline"}
            size="sm"
            onClick={() => setShowAnalytics(!showAnalytics)}
          >
            <BarChart3 className="w-4 h-4" />
          </Button>

          <Button variant="outline" size="sm">
            <Settings className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Content Area - Either Messages or Analytics */}
      {showAnalytics ? (
        <div className="flex-1 p-4 overflow-auto">
          {analyticsManager.current && (
            <AnalyticsDashboard analyticsManager={analyticsManager.current} />
          )}
        </div>
      ) : (
        <ScrollArea className="flex-1 p-4">
          <div className="space-y-4">
            {messages.map(renderMessage)}

            {/* Enhanced Typing Indicator */}
            {isTyping && (
              <div className="flex justify-start mb-4">
                <div className="flex items-start gap-3 max-w-[85%]">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-500 flex items-center justify-center">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center space-x-2">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                      </div>
                      <span className="text-sm text-muted-foreground">
                        {isLoading ? 'Processing your request...' : 'Typing...'}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Loading Indicator (when not typing) */}
            {isLoading && !isTyping && (
              <div className="flex justify-start mb-4">
                <div className="flex items-start gap-3 max-w-[85%]">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
                    <Loader2 className="w-4 h-4 text-white animate-spin" />
                  </div>
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div className="text-sm text-blue-700">
                      ⚡ Executing your command...
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
          <div ref={messagesEndRef} />
        </ScrollArea>
      )}

      {/* Error State Display */}
      {errorState.hasError && (
        <div className="p-4 border-t bg-red-50">
          <div className="flex items-start space-x-3">
            <AlertTriangle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <p className="text-sm text-red-700 mb-2">{errorState.message}</p>
              {errorState.suggestions && (
                <div className="flex flex-wrap gap-2 mb-2">
                  {errorState.suggestions.map((suggestion, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      size="sm"
                      className="text-xs border-red-200 text-red-700 hover:bg-red-100"
                      onClick={() => {
                        if (suggestion.startsWith('Rephrase') && errorState.retryAction) {
                          errorState.retryAction()
                        } else if (suggestion.startsWith('Retry') && errorState.retryAction) {
                          errorState.retryAction()
                        } else {
                          setInputMessage(suggestion)
                          inputRef.current?.focus()
                        }
                      }}
                    >
                      {suggestion}
                    </Button>
                  ))}
                </div>
              )}
              <Button
                variant="ghost"
                size="sm"
                className="text-xs text-red-600 hover:text-red-800 p-0 h-auto"
                onClick={() => setErrorState({ hasError: false })}
              >
                <X className="w-3 h-3 mr-1" />
                Dismiss
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Suggestions */}
      {suggestions.length > 0 && (
        <div className="p-4 border-t bg-gray-50">
          <p className="text-sm text-muted-foreground mb-2">Suggestions:</p>
          <div className="flex flex-wrap gap-2">
            {suggestions.map((suggestion, index) => (
              <Button
                key={index}
                variant="outline"
                size="sm"
                className="text-xs"
                onClick={() => handleSuggestionClick(suggestion)}
              >
                {suggestion}
              </Button>
            ))}
          </div>
        </div>
      )}

      {/* Human Escalation */}
      <div className="px-4">
        <HumanEscalation
          conversationId={currentSessionId || 'default'}
          conversationContext={memoryManager.current?.getRecentHistory(5)?.map(msg => msg.content).join('\n') || ''}
          userSentiment={currentSentiment ? {
            sentiment: currentSentiment.sentiment,
            confidence: currentSentiment.confidence,
            frustrated: currentSentiment.empathy_trigger
          } : undefined}
          onEscalationRequested={(request) => {
            // Add system message about escalation
            const escalationMessage: ChatMessage = {
              id: `escalation_${Date.now()}`,
              type: 'system',
              content: `🚀 **Human Support Requested**\n\nYour request has been submitted and you'll be connected with a human agent shortly.\n\n**Request ID:** ${request.id}\n**Priority:** ${request.priority}\n**Reason:** ${request.reason}`,
              timestamp: new Date().toISOString(),
              metadata: { escalation: request }
            }
            setMessages(prev => [...prev, escalationMessage])
          }}
        />
      </div>

      {/* Input */}
      <div className="p-4 border-t bg-white">
        <div className="flex items-center space-x-2">
          <div className="flex-1 relative">
            <Input
              ref={inputRef}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask me anything about your platform, analytics, workflows, or system management..."
              className="pr-12"
              disabled={isLoading}
            />
            <Button
              size="sm"
              variant="ghost"
              className="absolute right-1 top-1 h-8 w-8 p-0"
              onClick={startVoiceInput}
              disabled={isLoading}
            >
              {isListening ? (
                <MicOff className="w-4 h-4 text-red-500" />
              ) : (
                <Mic className="w-4 h-4" />
              )}
            </Button>
          </div>
          <Button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="px-6"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
      </div>
    </div>
  )
}
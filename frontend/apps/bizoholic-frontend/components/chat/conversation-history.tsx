'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import {
  History,
  Search,
  Calendar,
  MessageCircle,
  Archive,
  Download,
  Eye,
  Clock,
  Tag,
  Filter,
  RefreshCw
} from 'lucide-react'
import { ConversationalMemoryManager, ConversationSession, ConversationMessage } from '@/lib/conversational-memory-manager'
import { useAuth } from '@/hooks/use-auth'

interface ConversationHistoryProps {
  memoryManager?: ConversationalMemoryManager
  onRestoreConversation?: (sessionId: string) => void
  onReferenceMessage?: (message: ConversationMessage) => void
}

export function ConversationHistory({ 
  memoryManager, 
  onRestoreConversation,
  onReferenceMessage 
}: ConversationHistoryProps) {
  const { user } = useAuth()
  const [sessions, setSessions] = useState<ConversationSession[]>([])
  const [selectedSession, setSelectedSession] = useState<ConversationSession | null>(null)
  const [sessionMessages, setSessionMessages] = useState<ConversationMessage[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<ConversationMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('sessions')

  // Load conversation sessions
  useEffect(() => {
    loadSessions()
  }, [memoryManager])

  const loadSessions = async () => {
    if (!memoryManager) return
    
    setIsLoading(true)
    try {
      const sessions = await memoryManager.getConversationSessions(50)
      setSessions(sessions)
    } catch (error) {
      console.error('Failed to load sessions:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const loadSessionMessages = async (session: ConversationSession) => {
    if (!memoryManager) return

    setSelectedSession(session)
    setIsLoading(true)
    
    try {
      // In a real implementation, we'd load messages for the specific session
      // For now, we'll show recent messages from the memory manager
      const messages = memoryManager.getRecentHistory(50)
      setSessionMessages(messages)
    } catch (error) {
      console.error('Failed to load session messages:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSearch = async () => {
    if (!memoryManager || !searchQuery.trim()) return

    setIsLoading(true)
    try {
      const results = await memoryManager.searchConversations(searchQuery)
      setSearchResults(results)
      setActiveTab('search')
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleRestoreSession = (session: ConversationSession) => {
    if (onRestoreConversation) {
      onRestoreConversation(session.id)
    }
  }

  const handleReferenceMessage = (message: ConversationMessage) => {
    if (onReferenceMessage) {
      onReferenceMessage(message)
    }
  }

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMins / 60)
    const diffDays = Math.floor(diffHours / 24)

    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    if (diffDays < 7) return `${diffDays}d ago`
    return date.toLocaleDateString()
  }

  const getSessionStatusBadge = (status: string) => {
    const colors = {
      'active': 'bg-green-500',
      'completed': 'bg-blue-500',
      'archived': 'bg-gray-500'
    }
    return colors[status as keyof typeof colors] || 'bg-gray-500'
  }

  const renderSessionCard = (session: ConversationSession) => (
    <Card key={session.id} className="cursor-pointer hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-medium truncate">
            {session.title}
          </CardTitle>
          <Badge 
            variant="outline" 
            className={`text-xs text-white ${getSessionStatusBadge(session.status)}`}
          >
            {session.status}
          </Badge>
        </div>
        <div className="flex items-center text-xs text-muted-foreground space-x-4">
          <div className="flex items-center space-x-1">
            <Clock className="w-3 h-3" />
            <span>{formatTimestamp(session.updated_at)}</span>
          </div>
          <div className="flex items-center space-x-1">
            <MessageCircle className="w-3 h-3" />
            <span>{session.message_count} messages</span>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        {session.summary && (
          <p className="text-xs text-muted-foreground mb-3 line-clamp-2">
            {session.summary}
          </p>
        )}
        {session.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-3">
            {session.tags.slice(0, 3).map((tag, index) => (
              <Badge key={index} variant="secondary" className="text-xs">
                {tag}
              </Badge>
            ))}
          </div>
        )}
        <div className="flex space-x-2">
          <Button 
            size="sm" 
            variant="outline"
            onClick={() => loadSessionMessages(session)}
            className="text-xs"
          >
            <Eye className="w-3 h-3 mr-1" />
            View
          </Button>
          <Button 
            size="sm" 
            variant="outline"
            onClick={() => handleRestoreSession(session)}
            className="text-xs"
          >
            <RefreshCw className="w-3 h-3 mr-1" />
            Restore
          </Button>
        </div>
      </CardContent>
    </Card>
  )

  const renderMessageCard = (message: ConversationMessage) => {
    const isUser = message.type === 'user'
    const isSystem = message.type === 'system'
    
    return (
      <Card key={message.id} className="cursor-pointer hover:shadow-sm transition-shadow">
        <CardContent className="p-3">
          <div className="flex items-start space-x-3">
            <div className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs ${
              isUser ? 'bg-blue-500 text-white' : 
              isSystem ? 'bg-yellow-500 text-white' : 'bg-green-500 text-white'
            }`}>
              {isUser ? 'U' : isSystem ? 'S' : 'AI'}
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-medium text-muted-foreground">
                  {message.type === 'user' ? 'You' : message.type === 'system' ? 'System' : 'AI Assistant'}
                </span>
                <span className="text-xs text-muted-foreground">
                  {formatTimestamp(message.timestamp)}
                </span>
              </div>
              
              <p className="text-sm text-gray-900 line-clamp-3 mb-2">
                {message.content}
              </p>
              
              {message.metadata && (
                <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                  {message.metadata.intent && (
                    <Badge variant="outline" className="text-xs">
                      {message.metadata.intent}
                    </Badge>
                  )}
                  {message.metadata.action && (
                    <Badge variant="outline" className="text-xs">
                      {message.metadata.action}
                    </Badge>
                  )}
                </div>
              )}
              
              <div className="mt-2">
                <Button 
                  size="sm" 
                  variant="ghost"
                  onClick={() => handleReferenceMessage(message)}
                  className="text-xs p-1 h-auto"
                >
                  Reference in chat
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm" className="text-xs">
          <History className="w-4 h-4 mr-1" />
          Conversation History
        </Button>
      </DialogTrigger>
      
      <DialogContent className="max-w-4xl max-h-[80vh]">
        <DialogHeader>
          <DialogTitle className="flex items-center space-x-2">
            <History className="w-5 h-5" />
            <span>Conversation History</span>
          </DialogTitle>
        </DialogHeader>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
          <div className="flex items-center justify-between">
            <TabsList className="grid grid-cols-3 w-[400px]">
              <TabsTrigger value="sessions">Sessions</TabsTrigger>
              <TabsTrigger value="search">Search</TabsTrigger>
              <TabsTrigger value="messages">Current Session</TabsTrigger>
            </TabsList>
            
            <Button variant="outline" size="sm" onClick={loadSessions}>
              <RefreshCw className="w-4 h-4 mr-1" />
              Refresh
            </Button>
          </div>

          {/* Sessions Tab */}
          <TabsContent value="sessions" className="space-y-4">
            <div className="text-sm text-muted-foreground">
              Your conversation sessions with the AI assistant
            </div>
            
            <ScrollArea className="h-[500px]">
              <div className="space-y-3">
                {isLoading ? (
                  <div className="flex items-center justify-center py-8">
                    <RefreshCw className="w-6 h-6 animate-spin" />
                    <span className="ml-2">Loading sessions...</span>
                  </div>
                ) : sessions.length > 0 ? (
                  sessions.map(renderSessionCard)
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    <MessageCircle className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p>No conversation history found</p>
                    <p className="text-xs">Start chatting to build your history!</p>
                  </div>
                )}
              </div>
            </ScrollArea>
          </TabsContent>

          {/* Search Tab */}
          <TabsContent value="search" className="space-y-4">
            <div className="flex space-x-2">
              <Input
                placeholder="Search conversations..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="flex-1"
              />
              <Button onClick={handleSearch} disabled={!searchQuery.trim()}>
                <Search className="w-4 h-4" />
              </Button>
            </div>

            <ScrollArea className="h-[450px]">
              <div className="space-y-3">
                {isLoading ? (
                  <div className="flex items-center justify-center py-8">
                    <RefreshCw className="w-6 h-6 animate-spin" />
                    <span className="ml-2">Searching...</span>
                  </div>
                ) : searchResults.length > 0 ? (
                  searchResults.map(renderMessageCard)
                ) : searchQuery ? (
                  <div className="text-center py-8 text-muted-foreground">
                    <Search className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p>No results found for "{searchQuery}"</p>
                  </div>
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    <p>Enter a search term to find messages</p>
                  </div>
                )}
              </div>
            </ScrollArea>
          </TabsContent>

          {/* Current Session Messages */}
          <TabsContent value="messages" className="space-y-4">
            {selectedSession ? (
              <>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium">{selectedSession.title}</h3>
                    <p className="text-xs text-muted-foreground">
                      {selectedSession.message_count} messages • {formatTimestamp(selectedSession.updated_at)}
                    </p>
                  </div>
                  <Badge className={`text-white ${getSessionStatusBadge(selectedSession.status)}`}>
                    {selectedSession.status}
                  </Badge>
                </div>

                <ScrollArea className="h-[450px]">
                  <div className="space-y-3">
                    {sessionMessages.length > 0 ? (
                      sessionMessages.map(renderMessageCard)
                    ) : (
                      <div className="text-center py-8 text-muted-foreground">
                        <MessageCircle className="w-12 h-12 mx-auto mb-4 opacity-50" />
                        <p>No messages in this session</p>
                      </div>
                    )}
                  </div>
                </ScrollArea>
              </>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                <MessageCircle className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>Select a session to view messages</p>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  )
}
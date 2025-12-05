'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Trash2, StopCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { brainApi } from '@/lib/brain-api'

interface ChatMessage {
    id: string
    role: 'user' | 'assistant'
    content: string
    timestamp: Date
}

interface AgentChatProps {
    agentId: string
    agentName: string
    agentIcon: string
    agentColor: string
}

export function AgentChat({ agentId, agentName, agentIcon, agentColor }: AgentChatProps) {
    const [messages, setMessages] = useState<ChatMessage[]>([])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const scrollAreaRef = useRef<HTMLDivElement>(null)

    // Load history on mount
    useEffect(() => {
        const loadHistory = async () => {
            try {
                const history = await brainApi.agents.getHistory(agentId)
                if (history && history.length > 0) {
                    setMessages(history.map((msg: any, index: number) => ({
                        id: `hist-${index}`,
                        role: msg.role,
                        content: msg.content,
                        timestamp: new Date(msg.timestamp)
                    })))
                } else {
                    // Add welcome message if no history
                    setMessages([{
                        id: 'welcome',
                        role: 'assistant',
                        content: `Hello! I'm ${agentName}. How can I help you today?`,
                        timestamp: new Date()
                    }])
                }
            } catch (error) {
                console.error('Failed to load history:', error)
            }
        }
        loadHistory()
    }, [agentId, agentName])

    // Auto-scroll to bottom
    useEffect(() => {
        if (scrollAreaRef.current) {
            const scrollContainer = scrollAreaRef.current.querySelector('[data-radix-scroll-area-viewport]')
            if (scrollContainer) {
                scrollContainer.scrollTop = scrollContainer.scrollHeight
            }
        }
    }, [messages])

    const handleSend = async () => {
        if (!input.trim() || loading) return

        const userMessage: ChatMessage = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
            timestamp: new Date()
        }

        setMessages(prev => [...prev, userMessage])
        setInput('')
        setLoading(true)

        try {
            const response = await brainApi.agents.chat(agentId, userMessage.content)

            const botMessage: ChatMessage = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: response.message,
                timestamp: new Date()
            }

            setMessages(prev => [...prev, botMessage])
        } catch (error) {
            console.error('Chat error:', error)
            const errorMessage: ChatMessage = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: "I'm sorry, I encountered an error processing your request. Please try again.",
                timestamp: new Date()
            }
            setMessages(prev => [...prev, errorMessage])
        } finally {
            setLoading(false)
        }
    }

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    return (
        <div className="flex flex-col h-[600px] border rounded-lg bg-background">
            {/* Messages Area */}
            <ScrollArea className="flex-1 p-4" ref={scrollAreaRef}>
                <div className="space-y-4">
                    {messages.map((message) => (
                        <div
                            key={message.id}
                            className={`flex items-start gap-3 ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
                                }`}
                        >
                            <Avatar>
                                {message.role === 'user' ? (
                                    <>
                                        <AvatarImage src="/avatars/user.png" />
                                        <AvatarFallback><User className="h-4 w-4" /></AvatarFallback>
                                    </>
                                ) : (
                                    <div className="flex h-full w-full items-center justify-center rounded-full" style={{ backgroundColor: agentColor + '20' }}>
                                        <span className="text-lg">{agentIcon}</span>
                                    </div>
                                )}
                            </Avatar>
                            <div
                                className={`rounded-lg px-4 py-2 max-w-[80%] whitespace-pre-wrap ${message.role === 'user'
                                        ? 'bg-primary text-primary-foreground'
                                        : 'bg-muted'
                                    }`}
                            >
                                {message.content}
                            </div>
                        </div>
                    ))}
                    {loading && (
                        <div className="flex items-start gap-3">
                            <Avatar>
                                <div className="flex h-full w-full items-center justify-center rounded-full bg-muted">
                                    <Bot className="h-4 w-4" />
                                </div>
                            </Avatar>
                            <div className="rounded-lg px-4 py-2 bg-muted">
                                <span className="animate-pulse">Thinking...</span>
                            </div>
                        </div>
                    )}
                </div>
            </ScrollArea>

            {/* Input Area */}
            <div className="p-4 border-t">
                <div className="flex gap-2">
                    <Textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder={`Message ${agentName}...`}
                        className="min-h-[60px] resize-none"
                    />
                    <Button
                        onClick={handleSend}
                        disabled={loading || !input.trim()}
                        className="h-[60px] px-6"
                    >
                        {loading ? <StopCircle className="h-4 w-4" /> : <Send className="h-4 w-4" />}
                    </Button>
                </div>
                <div className="text-xs text-muted-foreground mt-2 text-center">
                    AI can make mistakes. Consider checking important information.
                </div>
            </div>
        </div>
    )
}

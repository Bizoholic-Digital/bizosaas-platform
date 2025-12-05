/**
 * Real-time Collaboration Client for BizOSaaS Platform
 * Provides WebSocket-based real-time collaboration and AI assistance
 * Works across all 5 platforms: Bizoholic, CoreLDove, Business Directory, ThrillRing, QuantTrade
 */

class BizOSaaSCollaborationClient {
    constructor(config = {}) {
        this.config = {
            brainApiUrl: config.brainApiUrl || 'ws://localhost:8001',
            tenantId: config.tenantId,
            userId: config.userId,
            platform: config.platform,
            reconnectInterval: config.reconnectInterval || 5000,
            maxReconnectAttempts: config.maxReconnectAttempts || 10,
            heartbeatInterval: config.heartbeatInterval || 30000,
            debug: config.debug || false,
            ...config
        };

        // Connection state
        this.ws = null;
        this.isConnected = false;
        this.sessionId = null;
        this.reconnectAttempts = 0;
        this.heartbeatTimer = null;

        // Event handlers
        this.eventHandlers = new Map();
        this.messageQueue = [];

        // Document collaboration state
        this.activeDocument = null;
        this.collaborators = new Map();
        this.pendingOperations = [];

        // AI assistance state
        this.aiAssistantReady = false;
        this.conversationHistory = [];

        this.log('BizOSaaS Collaboration Client initialized');
    }

    // ========================================================================================
    // CONNECTION MANAGEMENT
    // ========================================================================================

    /**
     * Connect to collaboration service
     */
    async connect() {
        if (this.isConnected) {
            this.log('Already connected');
            return;
        }

        try {
            const wsUrl = this.buildWebSocketUrl();
            this.log(`Connecting to: ${wsUrl}`);

            this.ws = new WebSocket(wsUrl);

            this.ws.onopen = this.handleOpen.bind(this);
            this.ws.onmessage = this.handleMessage.bind(this);
            this.ws.onclose = this.handleClose.bind(this);
            this.ws.onerror = this.handleError.bind(this);

        } catch (error) {
            this.log('Connection error:', error);
            this.handleConnectionError(error);
        }
    }

    /**
     * Disconnect from collaboration service
     */
    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        this.cleanup();
    }

    /**
     * Build WebSocket URL based on connection type
     */
    buildWebSocketUrl() {
        const baseUrl = this.config.brainApiUrl.replace(/^http/, 'ws');

        if (this.config.connectionType === 'ai-assistant') {
            return `${baseUrl}/ws/ai-assistant/${this.config.platform}/${this.config.tenantId}?user_id=${this.config.userId}`;
        } else {
            // Default to collaboration endpoint
            const scope = this.config.scope || 'tenant-wide';
            const scopeId = this.config.scopeId || 'general';
            return `${baseUrl}/ws/collaboration/${this.config.platform}/${scope}/${scopeId}?tenant_id=${this.config.tenantId}&user_id=${this.config.userId}`;
        }
    }

    // ========================================================================================
    // EVENT HANDLING
    // ========================================================================================

    handleOpen(event) {
        this.log('WebSocket connected');
        this.isConnected = true;
        this.reconnectAttempts = 0;

        this.startHeartbeat();
        this.emit('connected', { sessionId: this.sessionId });

        // Process queued messages
        this.processMessageQueue();
    }

    handleMessage(event) {
        try {
            const message = JSON.parse(event.data);
            this.log('Received message:', message);

            switch (message.type) {
                case 'collaboration_state':
                    this.handleCollaborationState(message.data);
                    break;

                case 'ai_assistant_ready':
                    this.handleAIAssistantReady(message.data);
                    break;

                case 'ai_response':
                    this.handleAIResponse(message.data);
                    break;

                case 'ai_thinking':
                    this.handleAIThinking(message.data);
                    break;

                case 'user_join':
                    this.handleUserJoin(message.data);
                    break;

                case 'user_leave':
                    this.handleUserLeave(message.data);
                    break;

                case 'document_edit':
                    this.handleDocumentEdit(message.data);
                    break;

                case 'cursor_position':
                    this.handleCursorPosition(message.data);
                    break;

                case 'user_typing':
                    this.handleUserTyping(message.data);
                    break;

                case 'document_lock':
                    this.handleDocumentLock(message.data);
                    break;

                case 'document_unlock':
                    this.handleDocumentUnlock(message.data);
                    break;

                case 'system_broadcast':
                    this.handleSystemBroadcast(message.data);
                    break;

                case 'notification':
                    this.handleNotification(message.data);
                    break;

                case 'error':
                    this.handleServerError(message.data);
                    break;

                case 'heartbeat':
                    this.handleHeartbeat(message.data);
                    break;

                default:
                    this.log('Unknown message type:', message.type);
                    this.emit('message', message);
            }

        } catch (error) {
            this.log('Error parsing message:', error);
        }
    }

    handleClose(event) {
        this.log('WebSocket closed:', event.code, event.reason);
        this.cleanup();

        this.emit('disconnected', { code: event.code, reason: event.reason });

        // Attempt to reconnect if not intentional disconnect
        if (event.code !== 1000 && this.reconnectAttempts < this.config.maxReconnectAttempts) {
            this.scheduleReconnect();
        }
    }

    handleError(error) {
        this.log('WebSocket error:', error);
        this.emit('error', error);
    }

    // ========================================================================================
    // COLLABORATION FEATURES
    // ========================================================================================

    /**
     * Handle collaboration state updates
     */
    handleCollaborationState(data) {
        this.sessionId = data.session_id;

        // Update collaborators
        this.collaborators.clear();
        for (const [userId, presence] of Object.entries(data.participants)) {
            this.collaborators.set(userId, presence);
        }

        this.emit('collaboration-state-updated', {
            sessionId: this.sessionId,
            participants: data.participants,
            activeLocks: data.active_locks,
            sharedState: data.shared_state
        });
    }

    /**
     * Handle user joining collaboration
     */
    handleUserJoin(data) {
        const { user_presence } = data;
        this.collaborators.set(user_presence.user_id, user_presence);
        this.emit('user-joined', user_presence);
    }

    /**
     * Handle user leaving collaboration
     */
    handleUserLeave(data) {
        // Remove from collaborators map
        // Note: user_id should be in metadata
        this.emit('user-left', data);
    }

    /**
     * Handle document edit operations
     */
    handleDocumentEdit(data) {
        this.emit('document-edit', data);
    }

    /**
     * Handle cursor position updates
     */
    handleCursorPosition(data) {
        this.emit('cursor-position', data);
    }

    /**
     * Handle user typing indicators
     */
    handleUserTyping(data) {
        this.emit('user-typing', data);
    }

    /**
     * Handle document lock/unlock
     */
    handleDocumentLock(data) {
        this.emit('document-lock', data);
    }

    handleDocumentUnlock(data) {
        this.emit('document-unlock', data);
    }

    // ========================================================================================
    // AI ASSISTANCE FEATURES
    // ========================================================================================

    /**
     * Handle AI assistant ready state
     */
    handleAIAssistantReady(data) {
        this.aiAssistantReady = true;
        this.emit('ai-assistant-ready', data);
    }

    /**
     * Handle AI responses
     */
    handleAIResponse(data) {
        // Add to conversation history
        this.conversationHistory.push({
            type: 'ai_response',
            timestamp: new Date().toISOString(),
            data: data
        });

        this.emit('ai-response', data);
    }

    /**
     * Handle AI thinking state
     */
    handleAIThinking(data) {
        this.emit('ai-thinking', data);
    }

    /**
     * Send message to AI assistant
     */
    async sendAIQuery(query, context = {}) {
        if (!this.aiAssistantReady) {
            throw new Error('AI Assistant not ready');
        }

        const message = {
            type: 'ai_query',
            data: {
                query: query,
                context: context,
                conversation_id: this.generateConversationId()
            }
        };

        // Add to conversation history
        this.conversationHistory.push({
            type: 'user_query',
            timestamp: new Date().toISOString(),
            query: query
        });

        this.sendMessage(message);
    }

    // ========================================================================================
    // DOCUMENT COLLABORATION
    // ========================================================================================

    /**
     * Send document edit operation
     */
    sendDocumentEdit(operation) {
        const message = {
            type: 'document_edit',
            data: operation
        };
        this.sendMessage(message);
    }

    /**
     * Send cursor position update
     */
    sendCursorPosition(position) {
        const message = {
            type: 'cursor_position',
            data: position
        };
        this.sendMessage(message);
    }

    /**
     * Send typing indicator
     */
    sendTypingIndicator(isTyping, documentId = null) {
        const message = {
            type: 'user_typing',
            data: {
                is_typing: isTyping,
                document_id: documentId,
                timestamp: new Date().toISOString()
            }
        };
        this.sendMessage(message);
    }

    /**
     * Request document lock
     */
    requestDocumentLock(resourceId, lockType = 'range', startPos = null, endPos = null) {
        const message = {
            type: 'document_lock',
            data: {
                resource_id: resourceId,
                lock_type: lockType,
                start_position: startPos,
                end_position: endPos
            }
        };
        this.sendMessage(message);
    }

    /**
     * Release document lock
     */
    releaseDocumentLock(resourceId) {
        const message = {
            type: 'document_unlock',
            data: {
                resource_id: resourceId
            }
        };
        this.sendMessage(message);
    }

    // ========================================================================================
    // UTILITY METHODS
    // ========================================================================================

    /**
     * Send message to server
     */
    sendMessage(message) {
        if (!this.isConnected) {
            this.messageQueue.push(message);
            return;
        }

        try {
            this.ws.send(JSON.stringify(message));
            this.log('Sent message:', message);
        } catch (error) {
            this.log('Error sending message:', error);
        }
    }

    /**
     * Process queued messages
     */
    processMessageQueue() {
        while (this.messageQueue.length > 0) {
            const message = this.messageQueue.shift();
            this.sendMessage(message);
        }
    }

    /**
     * Start heartbeat to keep connection alive
     */
    startHeartbeat() {
        this.heartbeatTimer = setInterval(() => {
            this.sendMessage({ type: 'heartbeat' });
        }, this.config.heartbeatInterval);
    }

    /**
     * Handle heartbeat response
     */
    handleHeartbeat(data) {
        // Connection is alive
        this.log('Heartbeat received');
    }

    /**
     * Handle system broadcasts
     */
    handleSystemBroadcast(data) {
        this.emit('system-broadcast', data);
    }

    /**
     * Handle notifications
     */
    handleNotification(data) {
        this.emit('notification', data);
    }

    /**
     * Handle server errors
     */
    handleServerError(data) {
        this.log('Server error:', data);
        this.emit('server-error', data);
    }

    /**
     * Schedule reconnection attempt
     */
    scheduleReconnect() {
        this.reconnectAttempts++;
        const delay = Math.min(this.config.reconnectInterval * this.reconnectAttempts, 30000);

        this.log(`Scheduling reconnect attempt ${this.reconnectAttempts} in ${delay}ms`);

        setTimeout(() => {
            this.connect();
        }, delay);
    }

    /**
     * Cleanup resources
     */
    cleanup() {
        this.isConnected = false;
        this.sessionId = null;

        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
        }

        this.collaborators.clear();
        this.messageQueue = [];
    }

    /**
     * Generate unique conversation ID
     */
    generateConversationId() {
        return `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Event system
     */
    on(event, handler) {
        if (!this.eventHandlers.has(event)) {
            this.eventHandlers.set(event, []);
        }
        this.eventHandlers.get(event).push(handler);
    }

    off(event, handler) {
        if (this.eventHandlers.has(event)) {
            const handlers = this.eventHandlers.get(event);
            const index = handlers.indexOf(handler);
            if (index > -1) {
                handlers.splice(index, 1);
            }
        }
    }

    emit(event, data) {
        if (this.eventHandlers.has(event)) {
            this.eventHandlers.get(event).forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    this.log('Error in event handler:', error);
                }
            });
        }
    }

    /**
     * Debug logging
     */
    log(...args) {
        if (this.config.debug) {
            console.log('[BizOSaaS Collaboration]', ...args);
        }
    }

    // ========================================================================================
    // PUBLIC API METHODS
    // ========================================================================================

    /**
     * Get current collaboration state
     */
    getCollaborationState() {
        return {
            isConnected: this.isConnected,
            sessionId: this.sessionId,
            collaborators: Array.from(this.collaborators.values()),
            aiAssistantReady: this.aiAssistantReady,
            conversationHistory: this.conversationHistory
        };
    }

    /**
     * Get collaborator information
     */
    getCollaborators() {
        return Array.from(this.collaborators.values());
    }

    /**
     * Check if user is collaborating
     */
    isUserCollaborating(userId) {
        return this.collaborators.has(userId);
    }

    /**
     * Get conversation history
     */
    getConversationHistory() {
        return [...this.conversationHistory];
    }

    /**
     * Clear conversation history
     */
    clearConversationHistory() {
        this.conversationHistory = [];
    }

    /**
     * Check connection status
     */
    isConnectionActive() {
        return this.isConnected && this.ws && this.ws.readyState === WebSocket.OPEN;
    }
}

/**
 * Factory function for creating collaboration clients
 */
function createCollaborationClient(config) {
    return new BizOSaaSCollaborationClient(config);
}

/**
 * Create AI Assistant client specifically
 */
function createAIAssistantClient(config) {
    return new BizOSaaSCollaborationClient({
        ...config,
        connectionType: 'ai-assistant'
    });
}

/**
 * Create Document Collaboration client specifically
 */
function createDocumentCollaborationClient(config) {
    return new BizOSaaSCollaborationClient({
        ...config,
        connectionType: 'collaboration',
        scope: 'document-specific',
        scopeId: config.documentId
    });
}

// Export for use in different module systems
if (typeof module !== 'undefined' && module.exports) {
    // Node.js/CommonJS
    module.exports = {
        BizOSaaSCollaborationClient,
        createCollaborationClient,
        createAIAssistantClient,
        createDocumentCollaborationClient
    };
} else if (typeof define === 'function' && define.amd) {
    // AMD
    define([], function() {
        return {
            BizOSaaSCollaborationClient,
            createCollaborationClient,
            createAIAssistantClient,
            createDocumentCollaborationClient
        };
    });
} else {
    // Browser globals
    window.BizOSaaSCollaborationClient = BizOSaaSCollaborationClient;
    window.createCollaborationClient = createCollaborationClient;
    window.createAIAssistantClient = createAIAssistantClient;
    window.createDocumentCollaborationClient = createDocumentCollaborationClient;
}
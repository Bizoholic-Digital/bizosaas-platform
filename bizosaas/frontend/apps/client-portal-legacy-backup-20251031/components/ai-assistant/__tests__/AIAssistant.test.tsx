import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AIAssistant } from '../AIAssistant';
import { useAIAssistant } from '../hooks/useAIAssistant';

// Mock the hook
jest.mock('../hooks/useAIAssistant');

const mockUseAIAssistant = useAIAssistant as jest.MockedFunction<typeof useAIAssistant>;

describe('AIAssistant', () => {
  const mockProps = {
    initialContext: {
      userId: 'test-user',
      tenantId: 'test-tenant',
      currentPage: '/dashboard',
      userProfile: {
        id: 'test-user',
        name: 'Test User',
        email: 'test@example.com',
        role: 'admin',
        subscription: {
          plan: 'pro',
          status: 'active',
          features: ['advanced_analytics']
        },
        preferences: {
          language: 'en',
          timezone: 'UTC',
          notifications: true
        }
      }
    }
  };

  const mockHookReturn = {
    conversation: null,
    isOpen: false,
    isMinimized: false,
    isTyping: false,
    isConnected: true,
    openAssistant: jest.fn(),
    closeAssistant: jest.fn(),
    toggleMinimize: jest.fn(),
    startConversation: jest.fn(),
    endConversation: jest.fn(),
    clearHistory: jest.fn(),
    sendMessage: jest.fn(),
    handleQuickAction: jest.fn(),
    startVoiceInput: jest.fn(),
    provideFeedback: jest.fn(),
    isVoiceAvailable: true
  };

  beforeEach(() => {
    mockUseAIAssistant.mockReturnValue(mockHookReturn);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders trigger button when closed', () => {
    render(<AIAssistant {...mockProps} />);
    
    const triggerButton = screen.getByRole('button', { name: /open ai assistant/i });
    expect(triggerButton).toBeInTheDocument();
  });

  it('opens assistant when trigger is clicked', () => {
    render(<AIAssistant {...mockProps} />);
    
    const triggerButton = screen.getByRole('button', { name: /open ai assistant/i });
    fireEvent.click(triggerButton);
    
    expect(mockHookReturn.openAssistant).toHaveBeenCalled();
  });

  it('renders chat interface when open', () => {
    mockUseAIAssistant.mockReturnValue({
      ...mockHookReturn,
      isOpen: true,
      conversation: {
        id: 'test-conv',
        messages: [
          {
            id: 'msg-1',
            type: 'assistant',
            content: 'Hello! How can I help you today?',
            timestamp: new Date(),
            metadata: {}
          }
        ],
        context: mockProps.initialContext,
        isTyping: false,
        isConnected: true,
        lastActivity: new Date()
      }
    });

    render(<AIAssistant {...mockProps} />);
    
    expect(screen.getByText('AI Assistant')).toBeInTheDocument();
    expect(screen.getByText('Hello! How can I help you today?')).toBeInTheDocument();
  });

  it('shows connection status', () => {
    mockUseAIAssistant.mockReturnValue({
      ...mockHookReturn,
      isOpen: true,
      isConnected: false
    });

    render(<AIAssistant {...mockProps} />);
    
    expect(screen.getByText('Offline')).toBeInTheDocument();
  });

  it('handles minimize toggle', () => {
    mockUseAIAssistant.mockReturnValue({
      ...mockHookReturn,
      isOpen: true
    });

    render(<AIAssistant {...mockProps} />);
    
    const minimizeButton = screen.getByTitle(/minimize/i);
    fireEvent.click(minimizeButton);
    
    expect(mockHookReturn.toggleMinimize).toHaveBeenCalled();
  });

  it('handles close action', () => {
    mockUseAIAssistant.mockReturnValue({
      ...mockHookReturn,
      isOpen: true
    });

    render(<AIAssistant {...mockProps} />);
    
    const closeButton = screen.getByTitle(/close assistant/i);
    fireEvent.click(closeButton);
    
    expect(mockHookReturn.closeAssistant).toHaveBeenCalled();
  });

  it('displays typing indicator when AI is typing', () => {
    mockUseAIAssistant.mockReturnValue({
      ...mockHookReturn,
      isOpen: true,
      isTyping: true,
      conversation: {
        id: 'test-conv',
        messages: [],
        context: mockProps.initialContext,
        isTyping: true,
        isConnected: true,
        lastActivity: new Date()
      }
    });

    render(<AIAssistant {...mockProps} />);
    
    expect(screen.getByText(/ai is typing/i)).toBeInTheDocument();
  });

  it('starts conversation when opened with context', async () => {
    mockUseAIAssistant.mockReturnValue({
      ...mockHookReturn,
      isOpen: true,
      conversation: null
    });

    render(<AIAssistant {...mockProps} />);
    
    await waitFor(() => {
      expect(mockHookReturn.startConversation).toHaveBeenCalledWith(
        expect.objectContaining({
          userId: 'test-user',
          tenantId: 'test-tenant',
          currentPage: expect.any(String),
          userProfile: mockProps.initialContext.userProfile
        })
      );
    });
  });

  it('renders minimized state correctly', () => {
    mockUseAIAssistant.mockReturnValue({
      ...mockHookReturn,
      isOpen: true,
      isMinimized: true,
      conversation: {
        id: 'test-conv',
        messages: [
          { id: 'msg-1', type: 'user', content: 'Hello', timestamp: new Date() },
          { id: 'msg-2', type: 'assistant', content: 'Hi there!', timestamp: new Date() }
        ],
        context: mockProps.initialContext,
        isTyping: false,
        isConnected: true,
        lastActivity: new Date()
      }
    });

    render(<AIAssistant {...mockProps} />);
    
    expect(screen.getByText('2 messages')).toBeInTheDocument();
  });

  it('shows typing indicator in minimized state', () => {
    mockUseAIAssistant.mockReturnValue({
      ...mockHookReturn,
      isOpen: true,
      isMinimized: true,
      isTyping: true,
      conversation: {
        id: 'test-conv',
        messages: [],
        context: mockProps.initialContext,
        isTyping: true,
        isConnected: true,
        lastActivity: new Date()
      }
    });

    render(<AIAssistant {...mockProps} />);
    
    expect(screen.getByText(/ai typing/i)).toBeInTheDocument();
  });
});
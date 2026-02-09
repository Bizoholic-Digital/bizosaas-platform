export interface AIResponse {
    message: string;
    actions?: Array<{
        type: 'execute_workflow' | 'query_analytics' | 'control_agent' | 'system_command';
        payload: any;
    }>;
    suggestions?: string[];
    context_update?: any;
    intent?: string;
}

export class AICommandProcessor {
    private apiUrl: string;
    private userRole: string;
    private tenantId: string;
    private onTabNavigate?: (tabId: string) => void;

    constructor(
        apiUrl: string,
        userRole: string = 'user',
        tenantId: string = 'demo',
        onTabNavigate?: (tabId: string) => void
    ) {
        this.apiUrl = apiUrl;
        this.userRole = userRole;
        this.tenantId = tenantId;
        this.onTabNavigate = onTabNavigate;
    }

    async processCommand(command: string): Promise<AIResponse> {
        try {
            const response = await fetch(`${this.apiUrl}/api/ai/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: command,
                    tenant_id: this.tenantId,
                    role: this.userRole
                }),
            });

            if (!response.ok) {
                throw new Error(`AI API failed: ${response.statusText}`);
            }

            const data = await response.json();
            return {
                message: data.response || 'I processed your request, but have no response text.',
                actions: data.actions || [],
                suggestions: data.suggestions || [],
                context_update: data.metadata || {},
                intent: data.intent || 'general'
            };
        } catch (error) {
            console.error('Error in AICommandProcessor.processCommand:', error);
            throw error;
        }
    }

    async executeAction(action: any): Promise<any> {
        console.log('Executing AI Action:', action);

        // Handle tab navigation if provided in action
        if (action.type === 'navigate' && action.payload?.tab && this.onTabNavigate) {
            this.onTabNavigate(action.payload.tab);
            return { success: true, message: `Navigated to ${action.payload.tab}` };
        }

        try {
            const response = await fetch(`${this.apiUrl}/api/ai/execute`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: action.type,
                    payload: action.payload,
                    tenant_id: this.tenantId
                }),
            });

            if (!response.ok) {
                throw new Error(`Action execution failed: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error in AICommandProcessor.executeAction:', error);
            throw error;
        }
    }
}

# AI Agent System

A comprehensive multi-agent AI system with 93+ specialized agents, BYOK (Bring Your Own Key) support, and HashiCorp Vault integration for secure multi-tenant operations.

## 🎯 Overview

The AI Agent System provides:
- **93 Specialized Agents** across 13 categories
- **BYOK Support** for 20+ services (AI, Marketing, Payment, Analytics, etc.)
- **Multi-Agent Orchestration** (Single, Sequential, Parallel execution)
- **HashiCorp Vault Integration** for secure key management
- **Cost Tracking** and usage analytics
- **Multi-Tenant Security** with complete isolation

## 📁 Structure

```
lib/ai/
├── types.ts                 # TypeScript type definitions
├── agent-registry.ts        # 93 agent definitions
├── byok-manager.ts          # BYOK and Vault integration
├── agent-orchestrator.ts    # Multi-agent coordination
└── index.ts                 # Public API exports
```

## 🚀 Quick Start

### Basic Usage

```typescript
import { getOrchestrator, getAgentById } from '@/lib/ai';

// Create orchestrator for tenant and user
const orchestrator = getOrchestrator('tenant_123', 'user_456');

// Create a task from user message
const task = await orchestrator.createTaskFromMessage(
  'Analyze my marketing campaign performance',
  'conversation_789'
);

// Execute the task
const result = await orchestrator.executeTask(task);

console.log(result.finalResponse);
console.log(`Cost: $${result.totalCost}`);
console.log(`Tokens: ${result.totalTokens}`);
```

### Using BYOK

```typescript
import { getBYOKManager } from '@/lib/ai';

// Get BYOK manager for tenant
const byokManager = getBYOKManager('tenant_123');

// Set tenant's OpenAI API key
await byokManager.setAPIKey('openai', 'api_key', 'sk-...');

// Get API key (tenant-specific or platform fallback)
const apiKey = await byokManager.getAPIKey('openai', 'api_key', true);

// Test API key validity
const validation = await byokManager.testAPIKey('openai', 'api_key', 'sk-...');
console.log(validation.isValid);

// Get usage statistics
const stats = await byokManager.getUsageStats();
console.log(stats.totalCost);
```

### Working with Agents

```typescript
import { 
  getAgentById, 
  getAgentsByCategory, 
  getActiveAgents,
  searchAgents 
} from '@/lib/ai';

// Get specific agent
const agent = getAgentById('campaign_manager');

// Get all marketing agents
const marketingAgents = getAgentsByCategory('marketing');

// Get all active agents
const activeAgents = getActiveAgents();

// Search agents
const results = searchAgents('seo');
```

## 🤖 Available Agents

### Active Agents (7)
- **Personal Assistant** - Main coordinator
- **Campaign Manager** - Marketing campaign optimization
- **Blog Writer** - SEO-optimized content creation
- **SEO Strategist** - Comprehensive SEO strategies
- **Data Analyst** - Business metrics analysis
- **Lead Qualifier** - Lead scoring and qualification
- **Product Recommender** - Product recommendations

### Agent Categories (93 Total)

| Category | Count | Examples |
|----------|-------|----------|
| General & Personal | 1 | Personal Assistant |
| Marketing & Advertising | 15 | Google Ads, Meta Ads, LinkedIn Ads |
| Content Creation | 12 | Blog Writer, Email Copywriter, Video Script Writer |
| SEO | 10 | SEO Strategist, Keyword Researcher, Technical SEO |
| Social Media | 8 | Instagram, Twitter, LinkedIn Specialists |
| Analytics & Insights | 8 | Data Analyst, Google Analytics, Predictive Analytics |
| Email Marketing | 6 | Campaign Manager, Template Designer, Deliverability |
| CRM | 6 | Lead Qualifier, Sales Assistant, Churn Prediction |
| E-commerce | 8 | Product Recommender, Dynamic Pricing, Cart Recovery |
| Design & Creative | 5 | Graphic Designer, Logo Designer, Infographic Designer |
| Automation & Workflows | 4 | Workflow Automation, Task Scheduling |
| Research & Analysis | 3 | Market Research, Competitor Research, Trend Analysis |
| Customer Support | 4 | Support Chatbot, Ticket Classifier, Sentiment Analyzer |

## 🔐 BYOK (Bring Your Own Key)

### Supported Services

#### AI Services
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- OpenRouter (200+ models)
- Google AI (Gemini)

#### Marketing Platforms
- Google Ads
- Meta Ads (Facebook/Instagram)
- LinkedIn Ads
- TikTok Ads

#### Payment Gateways
- Stripe
- PayPal
- Razorpay

#### Analytics
- Google Analytics
- Mixpanel

#### Email Services
- SendGrid
- Mailchimp

#### SMS Services
- Twilio

#### Cloud Storage
- AWS S3
- Google Cloud Storage

#### CRM
- Salesforce
- HubSpot

### Key Management

```typescript
// Set API key
await byokManager.setAPIKey('stripe', 'secret_key', 'sk_live_...');

// Delete API key
await byokManager.deleteAPIKey('stripe', 'secret_key');

// List all keys
const keys = await byokManager.listAPIKeys();

// Rotate key
await byokManager.rotateAPIKey('openai', 'api_key', 'sk-new-key');

// Get LLM config with BYOK
const config = await byokManager.getLLMConfig('openai');
console.log(config.usingPlatformKey); // true if using fallback
```

## 🎭 Agent Orchestration

### Execution Modes

#### Single Agent
```typescript
const task = {
  id: 'task_1',
  type: 'single',
  agentIds: ['seo_strategist'],
  input: 'Analyze my website SEO',
  context: { /* ... */ }
};

const result = await orchestrator.executeTask(task);
```

#### Sequential (Pipeline)
```typescript
const task = {
  id: 'task_2',
  type: 'sequential',
  agentIds: ['keyword_researcher', 'seo_content_optimizer', 'blog_writer'],
  input: 'Create an SEO-optimized blog post about AI',
  context: { /* ... */ }
};

// Output of each agent feeds into the next
const result = await orchestrator.executeTask(task);
```

#### Parallel (Comprehensive Analysis)
```typescript
const task = {
  id: 'task_3',
  type: 'parallel',
  agentIds: ['seo_strategist', 'content_strategist', 'social_media_manager'],
  input: 'Analyze my content strategy',
  context: { /* ... */ }
};

// All agents run simultaneously
const result = await orchestrator.executeTask(task);
```

### Intent Analysis

The orchestrator automatically analyzes user intent and selects appropriate agents:

```typescript
const intent = await orchestrator.analyzeIntent('How can I improve my Google Ads performance?');

console.log(intent.primaryAgent); // google_ads_specialist
console.log(intent.confidence); // 0.85
```

## 💰 Cost Tracking

```typescript
// Get usage statistics
const stats = await byokManager.getUsageStats();

console.log(stats.totalRequests);
console.log(stats.totalCost);
console.log(stats.byService); // Cost breakdown by service
```

## 🔒 Security

### Multi-Tenant Isolation
- Each tenant's API keys are stored separately in Vault
- Complete isolation between tenants
- No cross-tenant data access

### Key Encryption
- All keys encrypted at rest in Vault
- Keys masked when displayed to users
- Secure key rotation supported

### Compliance
- PCI-DSS compliant key storage
- SOC2 ready
- GDPR compliant
- HIPAA ready

### Key Validation

```typescript
import { validateKeyFormat, calculateKeyStrength } from '@/lib/ai';

// Validate key format
const validation = validateKeyFormat('openai', 'api_key', 'sk-...');
console.log(validation.isValid);

// Calculate key strength (0-100)
const strength = calculateKeyStrength('sk-...');
console.log(strength); // 85
```

## 📊 Types

All types are fully documented with TypeScript:

```typescript
import type {
  AIAgent,
  AgentTask,
  AgentResult,
  AgentContext,
  OrchestratorResult,
  BYOKConfig,
  KeyValidationResult,
  LLMConfig,
  UsageMetrics,
} from '@/lib/ai';
```

## 🛠️ Development

### Adding a New Agent

1. Add agent definition to `agent-registry.ts`:

```typescript
my_new_agent: {
  id: 'my_new_agent',
  name: 'My New Agent',
  description: 'Does amazing things',
  category: 'marketing',
  capabilities: [
    {
      id: 'amazing_capability',
      name: 'Amazing Capability',
      description: 'Performs amazing tasks'
    }
  ],
  requiredTools: ['api_tool'],
  requiredServices: ['external_api'],
  requiredAPIs: [
    {
      service: 'external_api',
      keyType: 'api_key',
      required: true,
      fallbackToPlatform: true
    }
  ],
  costTier: 'premium',
  permissions: ['view_data', 'create_campaigns'],
  status: 'active',
  metadata: {
    version: '1.0.0',
    author: 'Your Name',
    lastUpdated: '2024-12-04',
    tags: ['marketing', 'automation'],
  },
  systemPrompt: 'You are an expert at...',
}
```

2. Update intent analysis in `agent-orchestrator.ts` if needed

3. Test the agent:

```typescript
const agent = getAgentById('my_new_agent');
const task = await orchestrator.createTaskFromMessage('Use my new agent', 'conv_1');
const result = await orchestrator.executeTask(task);
```

### Adding a New Service to BYOK

Add to `SERVICE_CATALOG` in `byok-manager.ts`:

```typescript
my_service: {
  name: 'My Service',
  category: 'analytics',
  keyTypes: ['api_key', 'secret'],
  requiredKeys: ['api_key'],
  documentation: 'https://docs.myservice.com',
}
```

## 📝 API Reference

### AgentOrchestrator

- `executeTask(task: AgentTask): Promise<OrchestratorResult>`
- `analyzeIntent(message: string): Promise<IntentResult>`
- `createTaskFromMessage(message: string, conversationId: string): Promise<AgentTask>`

### BYOKManager

- `getAPIKey(service: ServiceId, keyType: string, fallback?: boolean): Promise<string | null>`
- `setAPIKey(service: ServiceId, keyType: string, value: string): Promise<boolean>`
- `deleteAPIKey(service: ServiceId, keyType: string): Promise<boolean>`
- `listAPIKeys(): Promise<APIKey[]>`
- `testAPIKey(service: ServiceId, keyType: string, value: string): Promise<KeyValidationResult>`
- `getLLMConfig(provider: LLMProvider): Promise<LLMConfig>`
- `getUsageStats(): Promise<UsageMetrics>`
- `rotateAPIKey(service: ServiceId, keyType: string, newValue: string): Promise<boolean>`

### Agent Registry

- `getAgentById(agentId: string): AIAgent | undefined`
- `getAgentsByCategory(category: AgentCategory): AIAgent[]`
- `getActiveAgents(): AIAgent[]`
- `getAllAgents(): AIAgent[]`
- `searchAgents(query: string): AIAgent[]`

## 🐛 Troubleshooting

### Agent Not Responding

1. Check agent status: `getAgentById('agent_id').status`
2. Verify API key is configured: `byokManager.getAPIKey(...)`
3. Check usage limits and quotas
4. Review error logs

### BYOK Key Issues

1. Validate key format: `validateKeyFormat(...)`
2. Test key: `byokManager.testAPIKey(...)`
3. Check Vault connectivity
4. Verify tenant permissions

### Performance Issues

1. Check agent execution time in results
2. Review LLM token usage
3. Consider using parallel execution
4. Enable caching where appropriate

## 📈 Roadmap

### Phase 2 (Weeks 3-4)
- [ ] LLM integration (OpenAI, Anthropic, OpenRouter)
- [ ] Activate 20+ additional agents
- [ ] BYOK UI in Client Portal
- [ ] Usage analytics dashboard

### Phase 3 (Weeks 5-6)
- [ ] Activate all 93 agents
- [ ] Admin dashboard for agent management
- [ ] MCP (Model Context Protocol) integration
- [ ] Advanced analytics and A/B testing

### Phase 4 (Weeks 7-8)
- [ ] Streaming responses
- [ ] Custom agent creation
- [ ] Agent marketplace
- [ ] Fine-tuning capabilities

## 📄 License

Proprietary - BizOSaaS Platform

## 🤝 Support

For issues or questions:
- Check the troubleshooting guide above
- Review the implementation summary
- Contact the development team

---

**Last Updated:** December 4, 2024  
**Version:** 1.0.0 (Phase 1 Complete)

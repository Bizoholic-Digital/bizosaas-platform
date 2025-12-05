# BizOSaaS Platform - Comprehensive Workflow, Wizard & AI Assistant Analysis

## Executive Summary

This document provides a complete analysis of all required workflows, wizards, and AI assistant features across the entire BizOSaaS platform ecosystem, identifying implementation gaps and providing a prioritized development roadmap.

## Current Platform Architecture

### Existing Components Analysis

#### **1. Frontend Applications (Confirmed)**
- **Client Portal** (port 3006): Multi-tenant client dashboard with Stripe integration
- **BizOSaaS Admin** (port 3009): Platform administration interface
- **Bizoholic Frontend** (Legacy): Marketing agency website
- **CoreLDove Frontend** (Legacy): E-commerce storefront

#### **2. Backend Services (Docker Compose)**
- **AI Agents System** (port 8000): 28+ specialized marketing agents
- **Auth Service** (port 3001): JWT-based authentication
- **Tenant Service** (port 3003): Multi-tenant management
- **Campaign Service** (port 3006): Marketing campaign management
- **Analytics Service** (port 3007): Performance tracking
- **Integration Service** (port 3008): Third-party API management
- **Contact Service** (port 3009): CRM functionality
- **Site Builder Service** (port 3010): Website creation
- **Subscription Service** (port 3011): Billing management
- **Media Service** (port 3005): File management
- **LLM Gateway Service** (port 3004): AI model management
- **Health Monitor** (port 3012): System monitoring

#### **3. Infrastructure Services**
- **PostgreSQL**: Multi-tenant database with pgvector
- **Dragonfly**: High-performance cache (25x faster than Redis)
- **Traefik**: API gateway and load balancer
- **Strapi CMS**: Headless content management
- **N8N**: Workflow automation engine
- **Mautic**: Marketing automation platform

#### **4. Existing Wizard System**
Located at `/ai/services/bizosaas-brain/wizard_manager.py` with 12 wizard types:
- Tenant Onboarding (Comprehensive - 8 steps)
- User Onboarding (5 steps)
- Integration Setup (5 steps)
- AI Agent Configuration (2 steps)
- Analytics Setup (Draft)
- Workflow Creation (Draft)
- Billing Setup (Draft)
- Security Configuration (Draft)
- Branding Setup (Active)
- Notification Configuration (Draft)
- Team Setup (Active)
- Migration Wizard (Active)

## Complete Workflow Inventory

### **1. User Onboarding Workflows**

#### **1.1 Tenant Onboarding Workflow** ✅ IMPLEMENTED
- **Status**: Complete (8 steps)
- **Components**: Organization setup, admin account, business goals, branding, integrations, AI agents
- **Success Rate**: 87%
- **Average Time**: 22 minutes

#### **1.2 User Onboarding Workflow** ✅ IMPLEMENTED
- **Status**: Complete (5 steps)
- **Components**: Profile setup, role assignment, permissions, notifications
- **Success Rate**: 92%
- **Average Time**: 9 minutes

#### **1.3 Developer Onboarding Workflow** ❌ MISSING
- **Required For**: BizOSaaS Admin
- **Components**: API access setup, SDK configuration, webhook setup, testing environment
- **Estimated Implementation**: 2-3 days

#### **1.4 Partner Onboarding Workflow** ❌ MISSING
- **Required For**: Bizoholic Platform
- **Components**: Partner agreement, integration requirements, revenue sharing, support channels
- **Estimated Implementation**: 3-4 days

### **2. Business Process Workflows**

#### **2.1 Lead Management Workflow** ⚠️ PARTIAL
- **Current**: Basic contact service exists
- **Missing**: Lead scoring, qualification, assignment, follow-up automation
- **Required For**: All platforms
- **Estimated Implementation**: 5-7 days

#### **2.2 Order Processing Workflow** ❌ MISSING
- **Required For**: CoreLDove Platform
- **Components**: Cart management, payment processing, fulfillment, shipping, returns
- **Integration**: Saleor E-commerce, payment gateways
- **Estimated Implementation**: 7-10 days

#### **2.3 Content Publishing Workflow** ⚠️ PARTIAL
- **Current**: Strapi CMS exists
- **Missing**: Content approval, scheduling, multi-platform publishing, SEO optimization
- **Required For**: All platforms
- **Estimated Implementation**: 4-6 days

#### **2.4 Campaign Execution Workflow** ⚠️ PARTIAL
- **Current**: Campaign service and AI agents exist
- **Missing**: Campaign approval, budget management, performance monitoring, optimization
- **Required For**: Bizoholic Platform
- **Estimated Implementation**: 6-8 days

### **3. Integration Workflows**

#### **3.1 API Integration Workflow** ⚠️ PARTIAL
- **Current**: Basic integration setup wizard exists
- **Missing**: Rate limiting, error handling, monitoring, versioning
- **Required For**: All platforms
- **Estimated Implementation**: 4-5 days

#### **3.2 Data Sync Workflow** ❌ MISSING
- **Required For**: All platforms
- **Components**: Real-time sync, conflict resolution, audit logging, rollback
- **Estimated Implementation**: 8-10 days

#### **3.3 Webhook Configuration Workflow** ❌ MISSING
- **Required For**: All platforms
- **Components**: Webhook setup, testing, retry logic, security validation
- **Estimated Implementation**: 3-4 days

### **4. AI Agent Workflows**

#### **4.1 Agent Deployment Workflow** ⚠️ PARTIAL
- **Current**: Basic AI agent configuration wizard exists
- **Missing**: Agent training, testing, monitoring, performance optimization
- **Required For**: All platforms
- **Estimated Implementation**: 5-7 days

#### **4.2 Human-in-the-Loop (HITL) Workflow** ❌ MISSING
- **Required For**: All platforms
- **Components**: Task escalation, human review, approval, feedback loop
- **Estimated Implementation**: 6-8 days

#### **4.3 Multi-Agent Coordination Workflow** ❌ MISSING
- **Required For**: All platforms
- **Components**: Task delegation, agent collaboration, conflict resolution, result aggregation
- **Estimated Implementation**: 8-10 days

### **5. Administrative Workflows**

#### **5.1 User Management Workflow** ⚠️ PARTIAL
- **Current**: Basic auth service exists
- **Missing**: Role-based access control, permission matrix, audit logging
- **Required For**: All platforms
- **Estimated Implementation**: 4-6 days

#### **5.2 Security Compliance Workflow** ⚠️ PARTIAL
- **Current**: Security config wizard (draft)
- **Missing**: Compliance monitoring, audit reports, policy enforcement
- **Required For**: All platforms
- **Estimated Implementation**: 7-9 days

#### **5.3 Billing Management Workflow** ⚠️ PARTIAL
- **Current**: Subscription service and billing wizard (draft)
- **Missing**: Usage tracking, invoice generation, payment retry, collections
- **Required For**: All platforms
- **Estimated Implementation**: 6-8 days

## Missing Wizard Inventory

### **Critical Priority Wizards**

#### **1. E-commerce Store Setup Wizard** ❌ MISSING
- **Required For**: CoreLDove Platform
- **Steps**: Product catalog setup, payment methods, shipping configuration, tax setup, store design
- **Estimated Implementation**: 4-5 days
- **Business Impact**: HIGH

#### **2. Marketing Campaign Creation Wizard** ❌ MISSING
- **Required For**: Bizoholic Platform
- **Steps**: Campaign objectives, target audience, budget allocation, creative assets, timeline, tracking setup
- **Estimated Implementation**: 5-6 days
- **Business Impact**: HIGH

#### **3. API Key Management Wizard** ❌ MISSING
- **Required For**: All platforms
- **Steps**: API key generation, permissions setup, rate limiting, monitoring, revocation
- **Estimated Implementation**: 3-4 days
- **Business Impact**: HIGH

#### **4. Data Import/Export Wizard** ❌ MISSING
- **Required For**: All platforms
- **Steps**: Data source selection, mapping, validation, transformation, import/export execution
- **Estimated Implementation**: 6-7 days
- **Business Impact**: MEDIUM

### **High Priority Wizards**

#### **5. Multi-Platform Integration Wizard** ❌ MISSING
- **Required For**: All platforms
- **Steps**: Platform selection, authentication, data mapping, sync configuration, testing
- **Estimated Implementation**: 7-8 days
- **Business Impact**: HIGH

#### **6. Custom Workflow Builder Wizard** ❌ MISSING
- **Required For**: All platforms
- **Steps**: Trigger selection, action configuration, condition setup, testing, deployment
- **Estimated Implementation**: 8-10 days
- **Business Impact**: HIGH

#### **7. Performance Optimization Wizard** ❌ MISSING
- **Required For**: All platforms
- **Steps**: Performance analysis, bottleneck identification, optimization recommendations, implementation
- **Estimated Implementation**: 5-6 days
- **Business Impact**: MEDIUM

### **Medium Priority Wizards**

#### **8. Mobile App Configuration Wizard** ❌ MISSING
- **Required For**: Client Portal, CoreLDove
- **Steps**: App store setup, push notifications, mobile-specific features, testing
- **Estimated Implementation**: 6-7 days
- **Business Impact**: MEDIUM

#### **9. Compliance Setup Wizard** ❌ MISSING
- **Required For**: All platforms
- **Steps**: Regulation selection, policy configuration, audit setup, reporting
- **Estimated Implementation**: 7-8 days
- **Business Impact**: MEDIUM

#### **10. Disaster Recovery Wizard** ❌ MISSING
- **Required For**: All platforms
- **Steps**: Backup configuration, recovery procedures, testing, documentation
- **Estimated Implementation**: 5-6 days
- **Business Impact**: MEDIUM

## AI Personal Assistant Requirements

### **Platform-Specific Assistant Features**

#### **1. Client Portal Assistant**
- **Name**: "Portal Assistant"
- **Capabilities**:
  - Account management guidance
  - Service usage optimization
  - Billing inquiries and support
  - Feature discovery and onboarding
  - Integration troubleshooting
- **Integration**: Client Portal frontend, Subscription Service, Analytics Service
- **Implementation**: 4-5 days

#### **2. BizOSaaS Admin Assistant**
- **Name**: "Admin Command Center"
- **Capabilities**:
  - Platform monitoring and alerts
  - User management commands
  - System optimization recommendations
  - Performance analytics interpretation
  - Incident response coordination
- **Integration**: Health Monitor, Analytics Service, all backend services
- **Implementation**: 6-7 days

#### **3. Bizoholic Marketing Assistant**
- **Name**: "Marketing Strategist AI"
- **Capabilities**:
  - Campaign strategy recommendations
  - Performance analysis and optimization
  - Content creation guidance
  - Client communication assistance
  - ROI analysis and reporting
- **Integration**: Existing 28+ AI Agents, Campaign Service, Analytics Service
- **Implementation**: 5-6 days

#### **4. CoreLDove E-commerce Assistant**
- **Name**: "Commerce Advisor"
- **Capabilities**:
  - Product optimization recommendations
  - Inventory management guidance
  - Customer behavior analysis
  - Sales performance insights
  - Marketing automation setup
- **Integration**: Saleor E-commerce, Analytics Service, Campaign Service
- **Implementation**: 5-6 days

### **Cross-Platform Assistant Capabilities**

#### **1. Natural Language Command Processing**
- **Voice Commands**: Integration with Web Speech API
- **Text Commands**: Natural language interpretation
- **Contextual Understanding**: Platform-specific context awareness
- **Multi-language Support**: English, Spanish, French, German
- **Implementation**: 8-10 days

#### **2. Conversational Interface**
- **Chat Interface**: Real-time messaging with typing indicators
- **Voice Interface**: Speech-to-text and text-to-speech
- **Visual Interface**: Interactive elements and quick actions
- **Mobile Optimization**: Responsive design for mobile devices
- **Implementation**: 6-8 days

#### **3. Integration with AI Crew System**
- **Agent Coordination**: Seamless integration with existing 28+ agents
- **Task Delegation**: Intelligent routing to appropriate agents
- **Result Aggregation**: Combining outputs from multiple agents
- **Progress Tracking**: Real-time updates on agent tasks
- **Implementation**: 7-9 days

## End-to-End Flow Analysis

### **1. Bizoholic Platform: Marketing Agency Client Journey**

#### **Current State**: ⚠️ PARTIAL IMPLEMENTATION
- ✅ Lead capture through public website
- ✅ Basic AI agents for campaign management
- ❌ Client onboarding automation
- ❌ Project management workflow
- ❌ Delivery and reporting automation

#### **Required End-to-End Flow**:
1. **Lead Generation** → Lead form submission
2. **Lead Qualification** → AI-powered lead scoring and routing
3. **Initial Consultation** → Automated scheduling and preparation
4. **Proposal Creation** → AI-generated proposals based on client needs
5. **Contract Management** → Digital contract workflow
6. **Project Initiation** → Automated project setup and team assignment
7. **Campaign Execution** → Multi-agent campaign management
8. **Progress Reporting** → Automated client reporting
9. **Optimization** → Continuous improvement recommendations
10. **Renewal/Upsell** → Customer success workflow

#### **Missing Components**:
- Lead qualification automation
- Proposal generation system
- Contract management workflow
- Project management integration
- Client reporting automation
- **Estimated Implementation**: 15-20 days

### **2. CoreLDove Platform: E-commerce Customer Journey**

#### **Current State**: ❌ REQUIRES SIGNIFICANT IMPLEMENTATION
- ⚠️ Basic Saleor E-commerce backend exists
- ❌ Frontend e-commerce application
- ❌ Customer onboarding workflow
- ❌ Order management automation
- ❌ Customer support integration

#### **Required End-to-End Flow**:
1. **Product Discovery** → Personalized product recommendations
2. **Cart Management** → Intelligent cart abandonment recovery
3. **Checkout Process** → Streamlined checkout with multiple payment options
4. **Order Processing** → Automated order fulfillment workflow
5. **Shipping Management** → Real-time tracking and notifications
6. **Customer Support** → AI-powered support integration
7. **Review Management** → Automated review solicitation and management
8. **Loyalty Program** → Points and rewards automation
9. **Reorder Process** → Subscription and reorder workflows
10. **Returns Management** → Streamlined returns and refunds

#### **Missing Components**:
- Complete frontend e-commerce application
- Order management workflow
- Shipping integration
- Customer support system
- Loyalty program management
- Returns processing workflow
- **Estimated Implementation**: 25-30 days

### **3. Client Portal: Tenant Management Journey**

#### **Current State**: ✅ GOOD FOUNDATION
- ✅ Basic tenant onboarding wizard
- ✅ User management
- ✅ Stripe payment integration
- ⚠️ Limited self-service capabilities
- ❌ Advanced automation features

#### **Required End-to-End Flow**:
1. **Initial Signup** → Automated tenant provisioning
2. **Service Configuration** → Self-service feature activation
3. **Team Setup** → User invitation and role management
4. **Integration Setup** → Third-party service connections
5. **Usage Monitoring** → Real-time usage tracking and alerts
6. **Support Requests** → Automated ticket routing and resolution
7. **Billing Management** → Self-service billing and payments
8. **Feature Requests** → Product feedback and feature voting
9. **Account Growth** → Usage-based upgrade recommendations
10. **Renewal Process** → Automated renewal and contract management

#### **Missing Components**:
- Advanced self-service capabilities
- Usage-based recommendations
- Feature request management
- Advanced billing automation
- **Estimated Implementation**: 10-12 days

### **4. BizOSaaS Admin: Platform Administration Journey**

#### **Current State**: ⚠️ BASIC IMPLEMENTATION
- ✅ Basic admin interface
- ⚠️ Limited monitoring capabilities
- ❌ Advanced analytics and insights
- ❌ Automated platform management

#### **Required End-to-End Flow**:
1. **Platform Monitoring** → Real-time health and performance monitoring
2. **Incident Response** → Automated alerting and escalation
3. **User Management** → Advanced user lifecycle management
4. **Resource Optimization** → AI-powered resource allocation
5. **Security Management** → Continuous security monitoring and response
6. **Performance Analytics** → Advanced platform analytics and insights
7. **Capacity Planning** → Predictive scaling and resource planning
8. **Feature Rollouts** → Controlled feature deployment and monitoring
9. **Compliance Monitoring** → Automated compliance checking and reporting
10. **Platform Evolution** → Data-driven platform improvement recommendations

#### **Missing Components**:
- Advanced monitoring and alerting
- AI-powered optimization
- Security incident response automation
- Advanced analytics dashboard
- Capacity planning tools
- **Estimated Implementation**: 18-22 days

## Implementation Priority Matrix

### **Critical Priority (Complete within 2-4 weeks)**

#### **Workflow Gaps**
1. **Lead Management Workflow** - 5-7 days
2. **Order Processing Workflow** - 7-10 days
3. **Campaign Execution Workflow** - 6-8 days
4. **Multi-Agent Coordination Workflow** - 8-10 days

#### **Missing Wizards**
1. **E-commerce Store Setup Wizard** - 4-5 days
2. **Marketing Campaign Creation Wizard** - 5-6 days
3. **API Key Management Wizard** - 3-4 days

#### **AI Assistant Features**
1. **Client Portal Assistant** - 4-5 days
2. **Natural Language Command Processing** - 8-10 days

### **High Priority (Complete within 4-8 weeks)**

#### **Workflow Gaps**
1. **HITL Workflow** - 6-8 days
2. **Data Sync Workflow** - 8-10 days
3. **Security Compliance Workflow** - 7-9 days
4. **Billing Management Workflow** - 6-8 days

#### **Missing Wizards**
1. **Multi-Platform Integration Wizard** - 7-8 days
2. **Custom Workflow Builder Wizard** - 8-10 days
3. **Data Import/Export Wizard** - 6-7 days

#### **AI Assistant Features**
1. **BizOSaaS Admin Assistant** - 6-7 days
2. **Marketing Strategist AI** - 5-6 days
3. **Commerce Advisor** - 5-6 days

### **Medium Priority (Complete within 8-12 weeks)**

#### **Workflow Gaps**
1. **Content Publishing Workflow** - 4-6 days
2. **User Management Workflow** - 4-6 days
3. **API Integration Workflow** - 4-5 days

#### **Missing Wizards**
1. **Performance Optimization Wizard** - 5-6 days
2. **Mobile App Configuration Wizard** - 6-7 days
3. **Compliance Setup Wizard** - 7-8 days

#### **AI Assistant Features**
1. **Conversational Interface** - 6-8 days
2. **Integration with AI Crew System** - 7-9 days

### **Low Priority (Complete within 12+ weeks)**

#### **Workflow Gaps**
1. **Webhook Configuration Workflow** - 3-4 days
2. **Developer Onboarding Workflow** - 2-3 days
3. **Partner Onboarding Workflow** - 3-4 days

#### **Missing Wizards**
1. **Disaster Recovery Wizard** - 5-6 days

## Integration Flow Requirements

### **Cross-Platform Data Synchronization**
- **Real-time sync** between all platform databases
- **Conflict resolution** for concurrent updates
- **Audit logging** for all data changes
- **Rollback capabilities** for failed operations
- **Implementation**: 8-10 days

### **Multi-Tenant Data Isolation**
- **Row-level security** (already partially implemented)
- **Tenant-specific configurations**
- **Data export/import per tenant**
- **Compliance per tenant**
- **Implementation**: 5-6 days

### **Real-time Notification System**
- **Cross-platform notifications**
- **Multi-channel delivery** (email, SMS, push, in-app)
- **Preference management**
- **Delivery tracking and retry**
- **Implementation**: 6-7 days

### **Backup and Recovery Workflows**
- **Automated backup scheduling**
- **Cross-platform backup coordination**
- **Point-in-time recovery**
- **Disaster recovery procedures**
- **Implementation**: 7-8 days

### **Compliance and Audit Workflows**
- **GDPR compliance automation**
- **SOC 2 compliance monitoring**
- **Audit trail generation**
- **Compliance reporting**
- **Implementation**: 10-12 days

## Resource Requirements and Timeline

### **Development Team Structure**
- **Frontend Developers**: 3-4 developers
- **Backend Developers**: 4-5 developers
- **AI/ML Engineers**: 2-3 engineers
- **DevOps Engineers**: 1-2 engineers
- **QA Engineers**: 2-3 engineers
- **UX/UI Designers**: 2 designers
- **Project Manager**: 1 PM

### **Phase 1: Critical Foundation (4 weeks)**
- **Week 1-2**: Lead Management + Order Processing workflows
- **Week 3**: E-commerce Store Setup + Campaign Creation wizards
- **Week 4**: Client Portal Assistant + API Key Management

### **Phase 2: Core Platform Features (6 weeks)**
- **Week 5-6**: Multi-Agent Coordination + HITL workflows
- **Week 7-8**: Data Sync + Security Compliance workflows
- **Week 9-10**: Multi-Platform Integration + Custom Workflow Builder wizards

### **Phase 3: Advanced Features (8 weeks)**
- **Week 11-12**: All AI Assistants implementation
- **Week 13-14**: Natural Language Processing + Conversational Interface
- **Week 15-16**: Performance Optimization + Mobile Configuration wizards
- **Week 17-18**: Integration with AI Crew System + Cross-platform sync

### **Phase 4: Polish and Optimization (4 weeks)**
- **Week 19-20**: Compliance + Audit workflows
- **Week 21**: Testing and bug fixes
- **Week 22**: Performance optimization and monitoring

### **Total Estimated Timeline**: 22 weeks (5.5 months)
### **Total Estimated Effort**: 180-220 developer days

## Success Criteria and Metrics

### **Technical Success Criteria**
- **Workflow Completion Rate**: >95% for all critical workflows
- **Wizard Success Rate**: >90% completion rate for all wizards
- **AI Assistant Response Time**: <2 seconds for standard queries
- **Cross-Platform Sync Latency**: <5 seconds for real-time sync
- **System Uptime**: >99.9% availability

### **Business Success Criteria**
- **User Onboarding Time**: Reduced by 60%
- **Support Ticket Volume**: Reduced by 40%
- **Feature Adoption Rate**: >80% for new wizard-driven features
- **Customer Satisfaction**: >4.5/5 rating for onboarding experience
- **Revenue Per User**: Increased by 25% through better self-service

### **Platform-Specific KPIs**

#### **Client Portal**
- **Self-Service Resolution Rate**: >70%
- **Feature Discovery Rate**: >60%
- **Billing Issue Resolution**: <24 hours

#### **Bizoholic Platform**
- **Campaign Setup Time**: Reduced by 70%
- **Client Onboarding Time**: Reduced by 50%
- **Campaign Performance**: Improved by 30%

#### **CoreLDove Platform**
- **Store Setup Time**: <2 hours for basic store
- **Order Processing Time**: <5 minutes automated
- **Customer Support Resolution**: <4 hours

#### **BizOSaaS Admin**
- **Incident Response Time**: <15 minutes
- **Platform Optimization**: 20% resource efficiency gain
- **Monitoring Coverage**: 100% of critical services

## Risk Assessment and Mitigation

### **High-Risk Areas**
1. **Multi-Agent Coordination Complexity**
   - **Risk**: Agent conflicts and coordination failures
   - **Mitigation**: Extensive testing, fallback mechanisms, human oversight

2. **Cross-Platform Data Consistency**
   - **Risk**: Data synchronization failures and inconsistencies
   - **Mitigation**: Distributed transaction management, conflict resolution algorithms

3. **AI Assistant Performance**
   - **Risk**: Slow response times or incorrect responses
   - **Mitigation**: Response caching, model optimization, human fallback

### **Medium-Risk Areas**
1. **Integration Complexity**
   - **Risk**: Third-party API limitations and failures
   - **Mitigation**: Robust error handling, retry mechanisms, alternative providers

2. **User Adoption**
   - **Risk**: Low adoption of new workflow features
   - **Mitigation**: User training, progressive rollout, feedback incorporation

### **Mitigation Strategies**
- **Phased Rollout**: Deploy features incrementally with user feedback
- **A/B Testing**: Test different workflow approaches with user groups
- **Comprehensive Monitoring**: Real-time monitoring of all workflows and wizards
- **Fallback Mechanisms**: Manual alternatives for all automated processes
- **Regular Reviews**: Weekly review of implementation progress and user feedback

## Conclusion

The BizOSaaS platform has a solid foundation with comprehensive wizard management and AI agent systems already in place. However, significant gaps exist in end-to-end workflows, platform-specific wizards, and AI personal assistants.

**Key Recommendations**:

1. **Prioritize Critical Workflows**: Focus first on lead management, order processing, and campaign execution workflows that directly impact revenue
2. **Implement Platform-Specific Wizards**: Create targeted wizards for e-commerce setup and marketing campaign creation
3. **Deploy AI Assistants**: Start with the Client Portal Assistant to improve user experience and reduce support load
4. **Establish Cross-Platform Integration**: Ensure seamless data flow and synchronization across all platforms
5. **Maintain Quality Standards**: Implement comprehensive testing and monitoring throughout the development process

With proper resource allocation and execution of this roadmap, the BizOSaaS platform will provide a comprehensive, AI-powered experience across all user journeys, significantly improving user satisfaction, operational efficiency, and business outcomes.
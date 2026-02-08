export enum AutomationType {
    RULE_BASED = 'rule_based',
    WORKFLOW_LOGIC = 'workflow_logic',
    DATABASE_TRIGGERS = 'database_triggers',
    API_INTEGRATIONS = 'api_integrations',
    SCHEDULED_TASKS = 'scheduled_tasks',
    LOGIC_WITH_AI_VALIDATION = 'logic_with_ai_validation',
    AI_ENHANCED_WORKFLOWS = 'ai_enhanced_workflows',
    AI_AGENT = 'ai_agent',
    AI_DECISION_MAKING = 'ai_decision_making',
    AI_CONTENT_GENERATION = 'ai_content_generation'
}

export enum TaskComplexity {
    SIMPLE = 'simple',
    MODERATE = 'moderate',
    COMPLEX = 'complex',
    CREATIVE = 'creative'
}

export interface AutomationTask {
    id: string;
    name: string;
    description: string;
    complexity: TaskComplexity;
    requirements: string[];
}

export interface AutomationRecommendation {
    task_id: string;
    recommended_type: AutomationType;
    confidence: number;
    reasoning: string;
    implementation_options: {
        primary: {
            type: AutomationType;
            estimated_accuracy: number;
            estimated_speed: number;
            cost_efficiency: number;
        };
        fallback?: {
            type: AutomationType;
            estimated_accuracy: number;
            estimated_speed: number;
            cost_efficiency: number;
        };
    };
    logic_workflows: string[];
    ai_alternatives: string[];
}

export const COMMON_AUTOMATION_TASKS: Record<string, AutomationTask> = {
    data_entry: {
        id: 'data_entry',
        name: 'Data Entry',
        description: 'Copying data from one system to another',
        complexity: TaskComplexity.SIMPLE,
        requirements: ['accuracy', 'speed']
    },
    email_triage: {
        id: 'email_triage',
        name: 'Email Triage',
        description: 'Categorizing incoming support emails',
        complexity: TaskComplexity.MODERATE,
        requirements: ['understanding', 'classification']
    },
    lead_research: {
        id: 'lead_research',
        name: 'Lead Research',
        description: 'Finding information about potential customers',
        complexity: TaskComplexity.COMPLEX,
        requirements: ['search', 'analysis']
    },
    content_drafting: {
        id: 'content_drafting',
        name: 'Content Drafting',
        description: 'Creating initial drafts for blog posts',
        complexity: TaskComplexity.CREATIVE,
        requirements: ['creativity', 'tone']
    }
};

class AutomationDecisionEngine {
    analyzeTask(task: AutomationTask): AutomationRecommendation {
        let recommended_type: AutomationType;
        let confidence: number;
        let reasoning: string;

        switch (task.complexity) {
            case TaskComplexity.SIMPLE:
                recommended_type = AutomationType.RULE_BASED;
                confidence = 0.95;
                reasoning = 'Structured tasks with clear rules are best handled by deterministic logic.';
                break;
            case TaskComplexity.MODERATE:
                recommended_type = AutomationType.LOGIC_WITH_AI_VALIDATION;
                confidence = 0.88;
                reasoning = 'Moderate tasks benefit from logic-first processing with AI verification.';
                break;
            case TaskComplexity.COMPLEX:
                recommended_type = AutomationType.AI_AGENT;
                confidence = 0.82;
                reasoning = 'Complex tasks requiring multi-step reasoning are best handled by AI agents.';
                break;
            case TaskComplexity.CREATIVE:
                recommended_type = AutomationType.AI_CONTENT_GENERATION;
                confidence = 0.90;
                reasoning = 'Creative tasks leverage the generative capabilities of large language models.';
                break;
            default:
                recommended_type = AutomationType.WORKFLOW_LOGIC;
                confidence = 0.70;
                reasoning = 'Default fallback to structured workflow logic.';
        }

        return {
            task_id: task.id,
            recommended_type,
            confidence,
            reasoning,
            implementation_options: {
                primary: {
                    type: recommended_type,
                    estimated_accuracy: Math.round(confidence * 100),
                    estimated_speed: task.complexity === TaskComplexity.SIMPLE ? 99 : 75,
                    cost_efficiency: task.complexity === TaskComplexity.SIMPLE ? 98 : 60
                },
                fallback: {
                    type: AutomationType.WORKFLOW_LOGIC,
                    estimated_accuracy: 70,
                    estimated_speed: 90,
                    cost_efficiency: 95
                }
            },
            logic_workflows: ['standard_validation', 'system_sync'],
            ai_alternatives: ['agent_reflection', 'llm_classification']
        };
    }
}

export default new AutomationDecisionEngine();

/**
 * SuperDesign.dev Configuration for BizoSaaS Frontend
 * 
 * This configuration file provides ready-to-use prompts and settings
 * for generating components with SuperDesign in Claude Code
 */

// import { getDesignPromptContext } from '../../design-tokens';

// Base configuration for BizoSaaS frontend
export const superDesignConfig = {
  platform: 'bizoholic' as const,
  framework: 'Next.js 14',
  styling: 'TailwindCSS',
  uiLibrary: 'ShadCN/UI',
  typescript: true,
  responsive: true,
  accessibility: true,
};

// Get BizoSaaS design context
// const designContext = getDesignPromptContext('bizoholic');
const designContext = {
  platform: 'bizoholic',
  description: 'Modern AI Marketing Agency',
  primaryColor: '#2563eb',
  accentColor: '#10b981',
  framework: 'Next.js 14',
  characteristics: ['Clean', 'Professional', 'Modern', 'AI-powered']
};

// Ready-to-use component generation prompts
export const componentPrompts = {
  // Dashboard Components
  metricCard: `
Generate a MetricCard component for BizoSaaS marketing dashboard:

Platform: ${designContext.platform}
Style: ${designContext.description}
Primary Color: ${designContext.primaryColor}
Framework: ${designContext.framework}

Component Requirements:
- Display metric title, current value, and percentage change
- Trend indicator with up/down arrow and color coding
- Subtle hover effects and professional styling
- Mobile-responsive design
- TypeScript interface with proper props
- Accessibility attributes (ARIA labels)
- Clean, minimal design with subtle shadows

Design Characteristics:
${designContext.characteristics.map(c => `- ${c}`).join('\n')}

Please include:
1. TypeScript interface definition
2. Complete React component
3. TailwindCSS styling classes
4. Usage example
5. Responsive breakpoints
`,

  campaignCard: `
Generate a CampaignCard component for BizoSaaS campaign management:

Platform: ${designContext.platform}
Style: ${designContext.description}
Primary Color: ${designContext.primaryColor}
Framework: ${designContext.framework}

Component Requirements:
- Campaign name, status badge, and performance metrics
- Channel indicators (email, social, etc.)
- Action buttons (edit, duplicate, delete) 
- Progress bar for campaign completion
- Professional blue color scheme
- Card hover effects and clean typography
- Mobile-responsive layout

Design Elements:
- Status badges (draft, active, paused, completed)
- Channel icons in a horizontal list
- Metrics display (impressions, clicks, CTR)
- Action menu or button group
- Professional, data-driven aesthetic

Please provide complete implementation with TypeScript and TailwindCSS.
`,

  dashboardLayout: `
Generate a DashboardLayout component for BizoSaaS main dashboard:

Platform: ${designContext.platform}
Style: ${designContext.description}
Primary Color: ${designContext.primaryColor}
Framework: ${designContext.framework}

Layout Requirements:
- Collapsible sidebar navigation
- Top header with user menu and notifications
- Main content area with proper spacing
- Responsive design (mobile, tablet, desktop)
- Professional SaaS aesthetics
- Clean grid layout for dashboard widgets

Navigation Elements:
- Dashboard, Campaigns, Analytics, AI Studio, Team, Settings
- User avatar and dropdown menu
- Notification bell with badge
- Search functionality
- Professional blue branding

Please include complete layout structure with proper responsive behavior.
`,

  aiContentStudio: `
Generate an AIContentStudio interface for BizoSaaS AI content generation:

Platform: ${designContext.platform}
Style: ${designContext.description}
Primary Color: ${designContext.primaryColor}
Accent Color: ${designContext.accentColor} (for AI features)
Framework: ${designContext.framework}

Interface Requirements:
- Three-panel layout: controls, preview, history
- Input controls (content type, tone, keywords, length)
- Generated content preview with editing capability
- History panel with saved generations
- Purple accent colors for AI-related features
- Modern, tech-forward aesthetic
- Streaming text animation placeholder

Features:
- Content type selector (social post, email, ad copy, blog)
- Tone slider (professional to casual)
- Keyword tag input
- Generate button with loading states
- Save to library functionality
- Professional with AI innovation focus

Please provide complete component with proper state management structure.
`
};

// Component variants for different use cases
export const componentVariants = {
  button: {
    primary: 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-sky-600 hover:bg-sky-700 focus:ring-sky-500', 
    ai: 'bg-purple-600 hover:bg-purple-700 focus:ring-purple-500',
    success: 'bg-green-600 hover:bg-green-700 focus:ring-green-500',
    warning: 'bg-amber-600 hover:bg-amber-700 focus:ring-amber-500',
    danger: 'bg-red-600 hover:bg-red-700 focus:ring-red-500',
  },
  
  card: {
    default: 'bg-white border border-gray-200 rounded-lg shadow-md',
    hover: 'bg-white border border-gray-200 rounded-lg shadow-md hover:shadow-lg transition-shadow',
    selected: 'bg-blue-50 border border-blue-200 rounded-lg shadow-md',
  },
  
  badge: {
    draft: 'bg-gray-100 text-gray-800',
    active: 'bg-green-100 text-green-800',
    paused: 'bg-yellow-100 text-yellow-800', 
    completed: 'bg-blue-100 text-blue-800',
  }
};

// Integration helpers
export const integrationHelpers = {
  // Generate component with proper imports
  generateWithImports: (componentName: string) => `
Please generate a ${componentName} component and include these imports:

\`\`\`typescript
import React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
// Add other ShadCN/UI imports as needed
\`\`\`

Use the existing ShadCN/UI components as base and extend with custom styling.
`,

  // File structure guidance
  fileStructure: {
    components: '/components/bizoholic/',
    ui: '/components/ui/', // ShadCN/UI base components
    utils: '/lib/utils.ts',
    types: '/types/index.ts',
  },

  // Styling guidelines
  stylingGuidelines: `
Use these styling patterns:
- Consistent spacing with Tailwind spacing scale
- Professional blue color scheme (${designContext.primaryColor})
- Subtle shadows and rounded corners
- Hover effects with smooth transitions
- Proper focus states for accessibility
- Mobile-first responsive design
`,
};

// Quick start commands for Claude Code
export const quickStartCommands = {
  generateMetricCard: `Use SuperDesign to ${componentPrompts.metricCard}`,
  generateCampaignCard: `Use SuperDesign to ${componentPrompts.campaignCard}`,
  generateDashboardLayout: `Use SuperDesign to ${componentPrompts.dashboardLayout}`,
  generateAIStudio: `Use SuperDesign to ${componentPrompts.aiContentStudio}`,
};

export default {
  config: superDesignConfig,
  prompts: componentPrompts,
  variants: componentVariants,
  helpers: integrationHelpers,
  quickStart: quickStartCommands,
};
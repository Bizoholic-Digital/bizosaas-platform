/**
 * Gamification Portfolio API Route
 * Connects client portal to gamification service via FastAPI Central Hub
 */

import { NextRequest, NextResponse } from 'next/server';

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const response = await fetch(
      `${BRAIN_API_URL}/api/brain/gamification/portfolio/generate`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Host': 'localhost:3001',
          'Authorization': request.headers.get('Authorization') || 'Bearer mock-token',
        },
        body: JSON.stringify(body),
      }
    );

    if (!response.ok) {
      console.error('Failed to generate portfolio:', response.status);
      // Return fallback portfolio data
      return NextResponse.json({
        portfolio_id: 'portfolio_' + Math.random().toString(36).substr(2, 9),
        portfolio_url: 'https://showcase.bizosaas.com/acme-corporation',
        featured_metrics: [
          {
            metric: 'Total Leads Generated',
            value: '2,847',
            growth: '+23%',
            icon: '🎯',
            description: 'Leads captured across all campaigns'
          },
          {
            metric: 'Revenue Growth',
            value: '$145,230',
            growth: '+67%',
            icon: '💰',
            description: 'Revenue increase since platform adoption'
          },
          {
            metric: 'Campaign Success Rate',
            value: '89%',
            growth: '+34%',
            icon: '📈',
            description: 'Campaigns meeting or exceeding goals'
          },
          {
            metric: 'Client Satisfaction',
            value: '4.8/5',
            growth: '+12%',
            icon: '⭐',
            description: 'Average client rating and feedback'
          }
        ],
        case_studies: [
          {
            id: 'cs_001',
            title: 'AI-Powered Email Campaign Boosts Conversions by 150%',
            client: 'TechStart Inc.',
            industry: 'Technology',
            challenge: 'Low email engagement and conversion rates',
            solution: 'Implemented AI-driven email personalization and timing optimization',
            results: {
              metric: 'Email Conversions',
              before: '2.3%',
              after: '5.8%',
              improvement: '150%'
            },
            testimonial: 'BizOSaaS transformed our email marketing. The AI insights were game-changing.',
            image_url: '/case-studies/techstart-email-campaign.jpg'
          },
          {
            id: 'cs_002',
            title: 'Multi-Channel Strategy Increases Lead Quality by 200%',
            client: 'Growth Co.',
            industry: 'Professional Services',
            challenge: 'High volume but low-quality leads',
            solution: 'Integrated AI lead scoring with multi-channel attribution',
            results: {
              metric: 'Qualified Leads',
              before: '23%',
              after: '69%',
              improvement: '200%'
            },
            testimonial: 'Our sales team now focuses on high-quality prospects. ROI has tripled.',
            image_url: '/case-studies/growth-co-multichannel.jpg'
          }
        ],
        social_templates: [
          {
            platform: 'LinkedIn',
            template: '🎉 Proud to share our latest achievement! Our AI-powered marketing campaigns helped {client} increase {metric} by {improvement}%. Ready to transform your business? Let\'s connect! #MarketingSuccess #AI #BusinessGrowth',
            image_suggestion: 'Infographic showing before/after metrics'
          },
          {
            platform: 'Twitter',
            template: '🚀 Just delivered incredible results for {client}: {improvement}% improvement in {metric}! AI + human creativity = magic ✨ #MarketingWins #AIMarketing',
            image_suggestion: 'Achievement badge or celebration graphic'
          },
          {
            platform: 'Facebook',
            template: 'Celebrating another success story! 📊 We helped {client} transform their marketing strategy and achieve {improvement}% growth in {metric}. This is why I love what we do at BizOSaaS! Ready to write your success story?',
            image_suggestion: 'Professional photo with client or team celebration'
          }
        ],
        estimated_impact: {
          seo_score: 94,
          social_shares_potential: 250,
          lead_generation_boost: '35%',
          brand_authority_increase: 'High',
          competitive_advantage: 'Strong positioning in AI marketing space'
        },
        optimization_suggestions: [
          {
            category: 'Content',
            suggestion: 'Add video testimonials to increase engagement by 45%',
            priority: 'High',
            effort: 'Medium'
          },
          {
            category: 'SEO',
            suggestion: 'Optimize for "AI marketing agency" keywords',
            priority: 'High',
            effort: 'Low'
          },
          {
            category: 'Social Proof',
            suggestion: 'Display real-time metrics dashboard',
            priority: 'Medium',
            effort: 'High'
          },
          {
            category: 'Call-to-Action',
            suggestion: 'Add interactive ROI calculator',
            priority: 'Medium',
            effort: 'Medium'
          }
        ]
      }, { status: 200 });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error generating portfolio:', error);
    return NextResponse.json(
      { error: 'Failed to generate portfolio' },
      { status: 500 }
    );
  }
}
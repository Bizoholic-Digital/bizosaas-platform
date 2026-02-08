/**
 * Marketing Content API Route for Client Portal
 * Manages content templates and AI-generated content via FastAPI AI Central Hub
 */

import { NextRequest, NextResponse } from 'next/server'

const BRAIN_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001'

// GET /api/brain/marketing/content - Fetch content templates and suggestions
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const type = searchParams.get('type') // 'email', 'ad', 'social', 'landing_page'
    const campaign_type = searchParams.get('campaign_type')
    const industry = searchParams.get('industry')
    const audience = searchParams.get('audience')
    const tone = searchParams.get('tone')
    
    let url = `${BRAIN_API_URL}/api/brain/marketing/content`
    const params = new URLSearchParams()
    
    if (type) params.set('type', type)
    if (campaign_type) params.set('campaign_type', campaign_type)
    if (industry) params.set('industry', industry)
    if (audience) params.set('audience', audience)
    if (tone) params.set('tone', tone)
    
    url += `?${params.toString()}`

    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      cache: 'no-store',
    })

    if (!response.ok) {
      throw new Error(`FastAPI AI Central Hub responded with status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error fetching content from Marketing API via Brain API:', error)
    
    // Return fallback content data
    const fallbackData = {
      email_templates: [
        {
          id: 'email-1',
          name: 'Welcome Series - Tech Startup',
          subject: 'Welcome to the future of {{company_type}} automation',
          preview_text: 'Discover how AI can transform your business processes',
          content: {
            html: `
              <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h1 style="color: #2563eb;">Welcome to Bizoholic, {{first_name}}!</h1>
                <p>We're excited to help {{company_name}} achieve breakthrough results with AI-powered marketing automation.</p>
                <div style="background: #f8fafc; padding: 20px; margin: 20px 0; border-radius: 8px;">
                  <h3>What happens next?</h3>
                  <ul>
                    <li>✅ Your dedicated success manager will reach out within 24 hours</li>
                    <li>🚀 We'll set up your first automated campaign</li>
                    <li>📊 You'll see initial results within 7 days</li>
                  </ul>
                </div>
                <a href="{{dashboard_url}}" style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                  Access Your Dashboard
                </a>
                <p style="margin-top: 30px; color: #64748b; font-size: 14px;">
                  Questions? Reply to this email or schedule a call with our team.
                </p>
              </div>
            `,
            text: `Welcome to Bizoholic, {{first_name}}!\n\nWe're excited to help {{company_name}} achieve breakthrough results with AI-powered marketing automation.\n\nWhat happens next?\n- Your dedicated success manager will reach out within 24 hours\n- We'll set up your first automated campaign\n- You'll see initial results within 7 days\n\nAccess your dashboard: {{dashboard_url}}\n\nQuestions? Reply to this email or schedule a call with our team.`
          },
          variables: ['first_name', 'company_name', 'company_type', 'dashboard_url'],
          metrics: {
            open_rate: 42.5,
            click_rate: 8.3,
            conversion_rate: 3.2
          },
          ai_score: 88,
          tags: ['welcome', 'onboarding', 'b2b'],
          created_at: '2024-01-10T00:00:00Z'
        },
        {
          id: 'email-2',
          name: 'Follow-up - Demo Request',
          subject: 'Thanks for your interest in {{product_name}}',
          preview_text: "Let's schedule your personalized demo",
          content: {
            html: `
              <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #2563eb;">Hi {{first_name}},</h2>
                <p>Thank you for requesting a demo of {{product_name}}. We're excited to show you how our AI-powered platform can help {{company_name}} achieve {{specific_goal}}.</p>
                <div style="background: #f0f9ff; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #2563eb;">
                  <h3 style="margin-top: 0;">What you'll see in your demo:</h3>
                  <ul style="margin-bottom: 0;">
                    <li>Live campaign creation and optimization</li>
                    <li>Real-time analytics and insights</li>
                    <li>Custom automation workflows for your industry</li>
                    <li>ROI projections based on your current metrics</li>
                  </ul>
                </div>
                <a href="{{calendar_link}}" style="background: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin: 20px 0;">
                  Schedule Your Demo
                </a>
                <p>The demo takes just 30 minutes and can be customized to focus on your specific needs and challenges.</p>
                <p style="color: #64748b;">Best regards,<br>{{sender_name}}<br>{{sender_title}}</p>
              </div>
            `,
            text: `Hi {{first_name}},\n\nThank you for requesting a demo of {{product_name}}. We're excited to show you how our AI-powered platform can help {{company_name}} achieve {{specific_goal}}.\n\nWhat you'll see in your demo:\n- Live campaign creation and optimization\n- Real-time analytics and insights\n- Custom automation workflows for your industry\n- ROI projections based on your current metrics\n\nSchedule your demo: {{calendar_link}}\n\nThe demo takes just 30 minutes and can be customized to focus on your specific needs and challenges.\n\nBest regards,\n{{sender_name}}\n{{sender_title}}`
          },
          variables: ['first_name', 'product_name', 'company_name', 'specific_goal', 'calendar_link', 'sender_name', 'sender_title'],
          metrics: {
            open_rate: 38.7,
            click_rate: 12.4,
            conversion_rate: 5.8
          },
          ai_score: 91,
          tags: ['follow-up', 'demo', 'sales'],
          created_at: '2024-01-12T00:00:00Z'
        }
      ],
      ad_templates: [
        {
          id: 'ad-1',
          name: 'LinkedIn Lead Gen - B2B SaaS',
          platform: 'linkedin',
          format: 'single_image',
          content: {
            headline: 'Stop Losing Leads to Manual Processes',
            description: 'See how {{company_examples}} increased conversions by 340% with AI marketing automation. Get your free strategy session.',
            cta: 'Get Free Strategy Session',
            image_requirements: {
              dimensions: '1200x627',
              format: 'JPG/PNG',
              max_size: '5MB'
            }
          },
          targeting_suggestions: {
            job_titles: ['Marketing Manager', 'VP Marketing', 'CMO', 'Growth Manager'],
            industries: ['Technology', 'Software', 'SaaS'],
            company_sizes: ['51-200', '201-500', '501-1000', '1001-5000']
          },
          metrics: {
            avg_ctr: 2.8,
            avg_cpc: 4.25,
            avg_conversion_rate: 6.2
          },
          ai_score: 85,
          tags: ['b2b', 'saas', 'lead-generation'],
          created_at: '2024-01-08T00:00:00Z'
        },
        {
          id: 'ad-2',
          name: 'Facebook Retargeting - Service Business',
          platform: 'facebook',
          format: 'carousel',
          content: {
            headline: 'Still thinking about {{service_name}}?',
            description: 'Join {{customer_count}}+ businesses already growing with our proven system. Limited time: 50% off setup.',
            cta: 'Claim Your Discount',
            cards: [
              {
                image_text: 'Before: Manual processes, lost leads',
                description: 'Stop losing potential customers to inefficient workflows'
              },
              {
                image_text: 'After: Automated success, 340% growth',
                description: 'See real results from businesses just like yours'
              },
              {
                image_text: 'Your Turn: Get started today',
                description: '50% off setup - limited time offer'
              }
            ]
          },
          targeting_suggestions: {
            custom_audiences: ['Website visitors - Last 30 days', 'Pricing page visitors'],
            lookalike_audiences: ['Existing customers - 1%'],
            interests: ['Business software', 'Marketing automation']
          },
          metrics: {
            avg_ctr: 3.2,
            avg_cpc: 1.85,
            avg_conversion_rate: 8.7
          },
          ai_score: 92,
          tags: ['retargeting', 'service-business', 'discount'],
          created_at: '2024-01-14T00:00:00Z'
        }
      ],
      social_templates: [
        {
          id: 'social-1',
          name: 'LinkedIn Thought Leadership',
          platform: 'linkedin',
          content: {
            text: `🤔 The biggest mistake I see in B2B marketing?\n\nTreating every lead the same.\n\nHere's what changed everything for us:\n\n→ Segment by company size\n→ Personalize by industry\n→ Automate by behavior\n\nResult? 340% increase in qualified leads.\n\nWhat's your biggest marketing challenge? 👇`,
            hashtags: ['#B2BMarketing', '#LeadGeneration', '#MarketingAutomation', '#GrowthHacking'],
            image_suggestions: [
              'Infographic showing segmentation strategy',
              'Before/after metrics comparison',
              'Team celebrating success'
            ]
          },
          engagement_tactics: {
            best_times: ['Tuesday 9-10 AM', 'Wednesday 11-12 PM', 'Thursday 2-3 PM'],
            call_to_action: 'Ask question in comments',
            follow_up_strategy: 'Respond to all comments within 2 hours'
          },
          metrics: {
            avg_engagement_rate: 4.8,
            avg_reach: 2500,
            avg_comments: 18
          },
          ai_score: 89,
          tags: ['thought-leadership', 'b2b', 'engagement'],
          created_at: '2024-01-11T00:00:00Z'
        },
        {
          id: 'social-2',
          name: 'Instagram Success Story',
          platform: 'instagram',
          content: {
            text: `✨ Client Spotlight ✨\n\n@techstartupxyz went from 50 leads/month to 500+ leads/month in just 90 days! 📈\n\nHere's what we implemented:\n🎯 AI-powered audience targeting\n📧 Automated email sequences\n📊 Real-time optimization\n\nThe result? 10x growth and their best quarter ever! 🚀\n\nReady to write your success story? Link in bio! 👆`,
            hashtags: ['#SuccessStory', '#ClientResults', '#StartupGrowth', '#MarketingAutomation', '#TechStartup'],
            image_suggestions: [
              'Before/after metrics graphic',
              'Client testimonial quote',
              'Growth chart visualization'
            ]
          },
          engagement_tactics: {
            best_times: ['Monday 6-8 PM', 'Wednesday 11-1 PM', 'Friday 1-3 PM'],
            call_to_action: 'Link in bio',
            follow_up_strategy: 'Story polls about growth challenges'
          },
          metrics: {
            avg_engagement_rate: 3.2,
            avg_reach: 1800,
            avg_saves: 45
          },
          ai_score: 86,
          tags: ['success-story', 'social-proof', 'results'],
          created_at: '2024-01-13T00:00:00Z'
        }
      ],
      landing_page_templates: [
        {
          id: 'lp-1',
          name: 'Lead Magnet - Marketing Automation Guide',
          type: 'lead_magnet',
          sections: {
            hero: {
              headline: 'The Complete Guide to Marketing Automation for {{industry}} Companies',
              subheadline: 'Download the same strategy that helped 500+ companies increase leads by 340%',
              cta: 'Get Free Guide',
              image: 'Guide mockup with company logos'
            },
            benefits: [
              'Step-by-step automation setup',
              '50+ proven email templates',
              'ROI calculator spreadsheet',
              'Implementation timeline',
              'Common mistakes to avoid'
            ],
            social_proof: {
              testimonials: [
                {
                  quote: 'This guide completely transformed our lead generation process.',
                  author: 'Sarah Johnson, CMO at TechCorp'
                }
              ],
              logos: ['Company A', 'Company B', 'Company C'],
              stats: '500+ downloads in first month'
            },
            form_fields: ['First Name', 'Email', 'Company', 'Job Title']
          },
          metrics: {
            avg_conversion_rate: 24.5,
            avg_time_on_page: '2:45',
            avg_bounce_rate: 35.2
          },
          ai_score: 91,
          tags: ['lead-magnet', 'guide', 'automation'],
          created_at: '2024-01-09T00:00:00Z'
        }
      ],
      content_ideas: [
        {
          type: 'blog_post',
          title: '10 Marketing Automation Mistakes That Cost You Customers',
          description: 'Common pitfalls and how to avoid them',
          target_audience: 'Marketing managers',
          estimated_time: '8 min read',
          seo_keywords: ['marketing automation', 'lead generation', 'customer retention'],
          ai_score: 87
        },
        {
          type: 'webinar',
          title: 'Live Demo: Build Your First Automated Campaign in 30 Minutes',
          description: 'Interactive workshop with Q&A',
          target_audience: 'Business owners, marketing teams',
          estimated_time: '45 min',
          seo_keywords: ['automated campaigns', 'marketing workshop', 'lead generation'],
          ai_score: 92
        },
        {
          type: 'case_study',
          title: 'How TechStartup Increased Leads by 500% with AI Marketing',
          description: 'Detailed breakdown of strategy and results',
          target_audience: 'Tech startup founders',
          estimated_time: '12 min read',
          seo_keywords: ['startup marketing', 'ai marketing', 'lead generation case study'],
          ai_score: 94
        }
      ],
      ai_optimization_suggestions: [
        {
          type: 'subject_line',
          current: 'Welcome to Bizoholic',
          suggested: 'Your marketing automation setup is ready, {{first_name}}',
          reason: 'Personalization + urgency increases open rates by 23%',
          impact_score: 85
        },
        {
          type: 'cta_button',
          current: 'Learn More',
          suggested: 'Get My Free Strategy Session',
          reason: 'Specific value proposition improves click rates by 18%',
          impact_score: 78
        },
        {
          type: 'headline',
          current: 'Marketing Automation Software',
          suggested: 'Stop Losing 60% of Your Leads to Manual Processes',
          reason: 'Problem-focused headlines increase engagement by 31%',
          impact_score: 89
        }
      ],
      source: "fallback"
    }
    
    return NextResponse.json(fallbackData, { status: 200 })
  }
}

// POST /api/brain/marketing/content - Generate AI content
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Validate required fields
    const { content_type, prompt, target_audience } = body
    if (!content_type || !prompt || !target_audience) {
      return NextResponse.json(
        { error: 'Missing required fields: content_type, prompt, target_audience' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BRAIN_API_URL}/api/brain/marketing/content/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Host': 'localhost:3000',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify({
        generation_request: {
          content_type: content_type,
          prompt: prompt,
          target_audience: target_audience,
          tone: body.tone || 'professional',
          length: body.length || 'medium',
          industry: body.industry || 'technology',
          platform: body.platform || 'email',
          campaign_goal: body.campaign_goal || 'lead_generation'
        },
        options: {
          include_variations: body.include_variations || true,
          optimize_for_engagement: body.optimize_for_engagement || true,
          include_hashtags: body.include_hashtags || false,
          personalization_level: body.personalization_level || 'medium'
        }
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(`FastAPI AI Central Hub responded with status: ${response.status}, ${JSON.stringify(errorData)}`)
    }

    const data = await response.json()
    return NextResponse.json({
      success: true,
      message: 'Content generated successfully',
      content: data.content,
      variations: data.variations || [],
      ai_insights: data.ai_insights || []
    })
  } catch (error) {
    console.error('Error generating content via Marketing API:', error)
    
    // Return development fallback
    const body = await request.json()
    const fallbackContent = {
      success: true,
      content: {
        id: 'generated-' + Date.now(),
        type: body.content_type,
        content: generateFallbackContent(body.content_type, body.prompt, body.target_audience),
        metadata: {
          tone: body.tone || 'professional',
          length: body.length || 'medium',
          target_audience: body.target_audience,
          generated_at: new Date().toISOString()
        }
      },
      variations: [
        {
          id: 'variation-1',
          content: generateFallbackContent(body.content_type, body.prompt, body.target_audience, 'variation'),
          changes: ['Different opening', 'Stronger CTA', 'Added urgency']
        }
      ],
      message: 'Content generated successfully (Development mode)',
      ai_insights: [
        'Consider A/B testing different headlines',
        'Add social proof for better credibility',
        'Optimize for mobile viewing'
      ],
      source: "fallback"
    }
    
    return NextResponse.json(fallbackContent, { status: 201 })
  }
}

function generateFallbackContent(type: string, prompt: string, audience: string, variant: string = 'original') {
  const variations = {
    email: {
      original: `Subject: Transform Your ${audience} Strategy Today\n\nHi there,\n\n${prompt}\n\nOur AI-powered platform has helped hundreds of businesses like yours achieve breakthrough results.\n\nKey benefits:\n• 340% increase in lead generation\n• 50% reduction in manual work\n• Real-time optimization and insights\n\nReady to see what's possible for your business?\n\nBest regards,\nThe Bizoholic Team`,
      variation: `Subject: ${audience}: Stop Losing Leads to Manual Processes\n\nHello,\n\n${prompt}\n\nWhat if you could automate your entire marketing funnel and see results like these:\n\n✅ 340% more qualified leads\n✅ 50% less manual work\n✅ Real-time performance insights\n\nThousands of businesses have already made the switch.\n\nYour turn?\n\nCheers,\nThe Bizoholic Team`
    },
    ad: {
      original: `${prompt}\n\nSee how businesses in ${audience} are growing 340% faster with AI marketing automation.\n\nGet your free strategy session today.`,
      variation: `Stop losing leads to manual processes!\n\n${prompt}\n\nJoin 500+ ${audience} companies already scaling with AI automation.\n\nClaim your free consultation →`
    },
    social: {
      original: `🚀 ${prompt}\n\nFor ${audience} professionals, this changes everything:\n\n→ 340% more leads\n→ 50% less manual work\n→ Real-time insights\n\nWhat's your biggest marketing challenge? 👇`,
      variation: `💡 The secret ${audience} companies don't want you to know...\n\n${prompt}\n\nResult? 340% growth in just 90 days.\n\nComment 'GROWTH' for the full strategy 👇`
    }
  }

  return variations[type]?.[variant] || `Generated content for ${type}: ${prompt} targeting ${audience}`
}
#!/usr/bin/env node

const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();

// Service pages data with SEO-optimized content
const SERVICES_DATA = {
    'seo-optimization-local-seo': {
        title: 'SEO Optimization & Local SEO',
        icon: '🔍',
        badge: 'Most Popular',
        category: 'Search Marketing',
        description: 'Boost your search rankings with AI-powered SEO optimization. Our advanced algorithms analyze your website, competitors, and search trends to deliver 200% better organic traffic within 90 days.',
        price: '$299/month',
        features: [
            'AI-powered keyword research and optimization',
            'Local SEO setup and Google My Business optimization',
            'Technical SEO audits and fixes',
            'Content optimization for search engines',
            'Competitor analysis and strategy',
            'Monthly performance reporting'
        ],
        benefits: [
            '200% increase in organic traffic',
            'First page Google rankings',
            'Local search domination',
            'Higher conversion rates'
        ]
    },
    'paid-advertising-ppc-management': {
        title: 'Paid Advertising (PPC) Management',
        icon: '💰',
        badge: 'High ROI',
        category: 'Paid Media',
        description: 'Maximize your ad spend with AI-driven PPC campaigns. Our intelligent bidding algorithms reduce cost-per-click by 45% while increasing conversions by 180%.',
        price: '$599/month',
        features: [
            'Google Ads and Facebook Ads management',
            'AI-powered bid optimization',
            'Advanced audience targeting',
            'Landing page optimization',
            'A/B testing and optimization',
            'Real-time performance monitoring'
        ],
        benefits: [
            '45% reduction in cost-per-click',
            '180% increase in conversions',
            'Higher quality leads',
            'Better ROI on ad spend'
        ]
    },
    'social-media-marketing-management': {
        title: 'Social Media Marketing & Management',
        icon: '📱',
        badge: 'Trending',
        category: 'Social Media',
        description: 'Grow your social presence with AI-powered content creation and scheduling. Generate viral-worthy posts, optimize posting times, and engage with your audience automatically.',
        price: '$399/month',
        features: [
            'AI content generation for all platforms',
            'Automated posting and scheduling',
            'Community management and engagement',
            'Social media analytics and insights',
            'Influencer outreach and partnerships',
            'Brand reputation monitoring'
        ],
        benefits: [
            'Consistent social media presence',
            'Higher engagement rates',
            'Increased follower growth',
            'Better brand awareness'
        ]
    },
    'content-marketing-blog-writing': {
        title: 'Content Marketing & Blog Writing',
        icon: '✍️',
        badge: 'SEO Optimized',
        category: 'Content Marketing',
        description: 'Create engaging, SEO-optimized content that converts. Our AI writers produce high-quality blog posts, articles, and web copy that ranks on page 1 of Google.',
        price: '$249/month',
        features: [
            'SEO-optimized blog posts and articles',
            'Content strategy and planning',
            'Topic research and trending analysis',
            'Content distribution across platforms',
            'Performance tracking and optimization',
            'Editorial calendar management'
        ],
        benefits: [
            'Higher search engine rankings',
            'Increased website traffic',
            'Better lead generation',
            'Enhanced brand authority'
        ]
    },
    'email-marketing-automation': {
        title: 'Email Marketing Automation',
        icon: '📧',
        badge: 'High Conversion',
        category: 'Email Marketing',
        description: 'Build automated email sequences that nurture leads and drive sales. Our AI personalizes every email for maximum engagement and 60% higher conversion rates.',
        price: '$199/month',
        features: [
            'Automated email sequences and drip campaigns',
            'AI-powered personalization',
            'Advanced segmentation and targeting',
            'A/B testing for subject lines and content',
            'Performance analytics and optimization',
            'Integration with CRM and sales tools'
        ],
        benefits: [
            '60% higher conversion rates',
            'Increased customer lifetime value',
            'Better lead nurturing',
            'Automated revenue generation'
        ]
    },
    'lead-generation-conversion': {
        title: 'Lead Generation & Conversion',
        icon: '🎯',
        badge: 'Results Guaranteed',
        category: 'Lead Generation',
        description: 'Generate high-quality leads with AI-powered targeting and conversion optimization. Increase your lead volume by 300% while reducing cost-per-lead by 50%.',
        price: '$449/month',
        features: [
            'AI-powered lead scoring and qualification',
            'Landing page optimization and testing',
            'Conversion funnel optimization',
            'Lead magnet creation and distribution',
            'CRM integration and automation',
            'Lead nurturing campaigns'
        ],
        benefits: [
            '300% increase in lead volume',
            '50% reduction in cost-per-lead',
            'Higher quality prospects',
            'Better sales conversion rates'
        ]
    },
    'website-design-development': {
        title: 'Website Design & Development',
        icon: '🌐',
        badge: 'Mobile First',
        category: 'Web Development',
        description: 'Build high-converting websites with AI-optimized design and development. Our responsive, fast-loading sites increase conversion rates by 150% and improve user experience.',
        price: '$1299 one-time',
        features: [
            'Mobile-first responsive design',
            'AI-optimized user experience',
            'Fast loading speeds and performance',
            'SEO-friendly structure and code',
            'Conversion optimization elements',
            'Analytics and tracking setup'
        ],
        benefits: [
            '150% increase in conversion rates',
            'Better user experience',
            'Higher search rankings',
            'Mobile-optimized performance'
        ]
    },
    'analytics-performance-tracking': {
        title: 'Analytics & Performance Tracking',
        icon: '📊',
        badge: 'Data Driven',
        category: 'Analytics',
        description: 'Make data-driven decisions with advanced analytics and AI insights. Track every metric that matters and get actionable recommendations to improve your marketing ROI.',
        price: '$149/month',
        features: [
            'Advanced analytics setup and configuration',
            'Custom dashboard and reporting',
            'AI-powered insights and recommendations',
            'Conversion tracking and attribution',
            'Performance monitoring and alerts',
            'ROI analysis and optimization'
        ],
        benefits: [
            'Better decision making with data',
            'Improved marketing ROI',
            'Clear performance visibility',
            'Actionable insights and recommendations'
        ]
    },
    'brand-strategy-reputation-management': {
        title: 'Brand Strategy & Reputation Management',
        icon: '🏆',
        badge: 'Brand Building',
        category: 'Brand Management',
        description: 'Build and protect your brand with AI-powered reputation management. Monitor mentions, respond to reviews automatically, and strengthen your brand presence across all channels.',
        price: '$349/month',
        features: [
            'Brand strategy development and positioning',
            'Online reputation monitoring and management',
            'Review management and response automation',
            'Brand mention tracking across platforms',
            'Crisis management and response',
            'Brand asset creation and management'
        ],
        benefits: [
            'Stronger brand reputation',
            'Better customer trust',
            'Improved online presence',
            'Crisis prevention and management'
        ]
    }
};

// Generate service page HTML
function generateServicePage(serviceSlug) {
    const service = SERVICES_DATA[serviceSlug];
    if (!service) return null;

    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${service.title} - Bizoholic AI Marketing</title>
    <meta name="description" content="${service.description.substring(0, 160)}">
    <meta name="keywords" content="AI marketing, ${service.title.toLowerCase()}, digital marketing, automation, ${service.category.toLowerCase()}">
    <meta property="og:title" content="${service.title} - Bizoholic AI Marketing">
    <meta property="og:description" content="${service.description.substring(0, 160)}">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="${service.title}">
    <meta name="twitter:description" content="${service.description.substring(0, 160)}">
    
    <!-- Service-specific structured data -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "${service.title}",
        "description": "${service.description}",
        "provider": {
            "@type": "Organization",
            "name": "Bizoholic",
            "url": "http://localhost:3000"
        },
        "serviceType": "${service.category}",
        "areaServed": "Global",
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "${service.title} Plans",
            "itemListElement": {
                "@type": "Offer",
                "description": "${service.description}",
                "price": "${service.price}"
            }
        }
    }
    </script>
    
    <!-- Include the same CSS as the homepage -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        :root {
            /* Apple-inspired Color Palette */
            --color-primary: #007AFF;
            --color-primary-dark: #0056CC;
            --color-secondary: #5AC8FA;
            --color-success: #34C759;
            --color-warning: #FF9F0A;
            --color-danger: #FF3B30;
            
            /* Neutral Colors */
            --color-black: #1D1D1F;
            --color-gray-900: #1C1C1E;
            --color-gray-800: #2C2C2E;
            --color-gray-700: #3A3A3C;
            --color-gray-600: #636366;
            --color-gray-500: #8E8E93;
            --color-gray-400: #AEAEB2;
            --color-gray-300: #C7C7CC;
            --color-gray-200: #D1D1D6;
            --color-gray-100: #F2F2F7;
            --color-white: #FFFFFF;
            
            /* Typography */
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --font-size-xs: 0.75rem;
            --font-size-sm: 0.875rem;
            --font-size-base: 1rem;
            --font-size-lg: 1.125rem;
            --font-size-xl: 1.25rem;
            --font-size-2xl: 1.5rem;
            --font-size-3xl: 1.875rem;
            --font-size-4xl: 2.25rem;
            --font-size-5xl: 3rem;
            --font-size-6xl: 3.75rem;
            
            /* Spacing */
            --spacing-1: 0.25rem;
            --spacing-2: 0.5rem;
            --spacing-3: 0.75rem;
            --spacing-4: 1rem;
            --spacing-5: 1.25rem;
            --spacing-6: 1.5rem;
            --spacing-8: 2rem;
            --spacing-10: 2.5rem;
            --spacing-12: 3rem;
            --spacing-16: 4rem;
            --spacing-20: 5rem;
            --spacing-24: 6rem;
            --spacing-32: 8rem;
            
            /* Shadows */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            
            /* Border Radius */
            --border-radius-sm: 0.375rem;
            --border-radius-md: 0.5rem;
            --border-radius-lg: 0.75rem;
            --border-radius-xl: 1rem;
            --border-radius-2xl: 1.5rem;
            
            /* Transitions */
            --transition-fast: all 0.15s ease;
            --transition-base: all 0.2s ease;
            --transition-slow: all 0.3s ease;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html {
            scroll-behavior: smooth;
        }
        
        body {
            font-family: var(--font-family);
            font-size: var(--font-size-base);
            line-height: 1.6;
            color: var(--color-black);
            background-color: var(--color-white);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        /* Layout Components */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 var(--spacing-6);
        }
        
        .section {
            padding: var(--spacing-24) 0;
        }
        
        .section-sm {
            padding: var(--spacing-16) 0;
        }
        
        /* Header & Navigation */
        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--color-gray-200);
            z-index: 1000;
            transition: var(--transition-base);
        }
        
        .nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: var(--spacing-4) 0;
            min-height: 60px;
        }
        
        .logo {
            font-size: var(--font-size-xl);
            font-weight: 700;
            color: var(--color-black);
            text-decoration: none;
            letter-spacing: -0.02em;
        }
        
        .nav-links {
            display: flex;
            align-items: center;
            gap: var(--spacing-8);
            list-style: none;
        }
        
        .nav-links a {
            color: var(--color-gray-600);
            text-decoration: none;
            font-weight: 500;
            font-size: var(--font-size-sm);
            transition: var(--transition-base);
            padding: var(--spacing-2) var(--spacing-3);
            border-radius: var(--border-radius-md);
        }
        
        .nav-links a:hover {
            color: var(--color-primary);
            background-color: var(--color-gray-100);
        }
        
        .nav-cta {
            display: flex;
            align-items: center;
            gap: var(--spacing-3);
        }
        
        /* Buttons */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: var(--spacing-3) var(--spacing-6);
            font-size: var(--font-size-sm);
            font-weight: 600;
            text-decoration: none;
            border-radius: var(--border-radius-xl);
            transition: var(--transition-base);
            border: none;
            cursor: pointer;
            white-space: nowrap;
        }
        
        .btn-primary {
            background-color: var(--color-primary);
            color: var(--color-white);
        }
        
        .btn-primary:hover {
            background-color: var(--color-primary-dark);
            transform: translateY(-1px);
            box-shadow: var(--shadow-lg);
        }
        
        .btn-secondary {
            background-color: transparent;
            color: var(--color-primary);
            border: 1px solid var(--color-gray-300);
        }
        
        .btn-secondary:hover {
            background-color: var(--color-gray-100);
            border-color: var(--color-gray-400);
        }
        
        .btn-lg {
            padding: var(--spacing-4) var(--spacing-8);
            font-size: var(--font-size-base);
        }
        
        .btn-xl {
            padding: var(--spacing-5) var(--spacing-10);
            font-size: var(--font-size-lg);
        }
        
        /* Main Content Areas */
        .main {
            margin-top: 60px; /* Account for fixed header */
        }
        
        /* Hero Section - Apple.com Inspired */
        .hero {
            padding: var(--spacing-32) 0 var(--spacing-24);
            background: linear-gradient(180deg, var(--color-gray-100) 0%, var(--color-white) 50%);
            text-align: center;
        }
        
        .hero h1 {
            font-size: var(--font-size-6xl);
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -0.04em;
            margin-bottom: var(--spacing-6);
            color: var(--color-black);
        }
        
        .hero p {
            font-size: var(--font-size-2xl);
            font-weight: 400;
            line-height: 1.4;
            color: var(--color-gray-600);
            max-width: 800px;
            margin: 0 auto var(--spacing-10);
        }
        
        .badge {
            display: inline-flex;
            align-items: center;
            background: var(--color-primary);
            color: var(--color-white);
            padding: var(--spacing-2) var(--spacing-4);
            border-radius: var(--border-radius-xl);
            font-size: var(--font-size-sm);
            font-weight: 600;
            margin-bottom: var(--spacing-4);
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: var(--spacing-8);
        }
        
        .feature-card {
            background-color: var(--color-white);
            border-radius: var(--border-radius-2xl);
            padding: var(--spacing-8);
            text-align: center;
            border: 1px solid var(--color-gray-200);
            transition: var(--transition-base);
        }
        
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
            border-color: var(--color-gray-300);
        }
        
        .feature-card h3 {
            font-size: var(--font-size-xl);
            font-weight: 600;
            margin-bottom: var(--spacing-4);
            color: var(--color-black);
        }
        
        .feature-card ul {
            list-style: none;
            text-align: left;
        }
        
        .feature-card li {
            margin-bottom: var(--spacing-2);
            display: flex;
            align-items: center;
            color: var(--color-gray-600);
        }
        
        .feature-card li::before {
            content: '✓';
            color: var(--color-success);
            margin-right: var(--spacing-2);
            font-weight: bold;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
            
            .hero h1 {
                font-size: var(--font-size-4xl);
            }
            
            .hero p {
                font-size: var(--font-size-lg);
            }
            
            .features-grid {
                grid-template-columns: 1fr;
                gap: var(--spacing-4);
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav container">
            <a href="/" class="logo">
                <img src="/Bizoholic_Digital_-_Color-transparent.png" alt="Bizoholic Digital" style="height: 32px; width: auto;">
            </a>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/services">Services</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/pricing">Pricing</a></li>
                <li><a href="/contact">Contact</a></li>
            </ul>
            <div class="nav-cta">
                <a href="/contact" class="btn btn-secondary">Get Started</a>
                <a href="http://localhost:3005" class="btn btn-primary">Client Portal</a>
            </div>
        </nav>
    </header>

    <main class="main">
        <!-- Service Hero Section -->
        <section class="hero">
            <div class="container">
                <div class="badge">
                    ${service.badge}
                </div>
                
                <h1>
                    ${service.icon} ${service.title}
                </h1>
                
                <p>${service.description}</p>
                
                <div style="display: flex; gap: var(--spacing-4); justify-content: center; flex-wrap: wrap;">
                    <a href="/contact" class="btn btn-primary btn-xl">Start Free Trial - ${service.price}</a>
                    <a href="/" class="btn btn-secondary btn-xl">Learn More</a>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="section">
            <div class="container">
                <h2 style="text-align: center; font-size: var(--font-size-4xl); font-weight: 700; margin-bottom: var(--spacing-16); color: var(--color-black);">
                    What's Included in ${service.title}
                </h2>
                <div class="features-grid">
                    <div class="feature-card">
                        <h3>📋 Service Features</h3>
                        <ul>
                            ${service.features.map(feature => `<li>${feature}</li>`).join('')}
                        </ul>
                    </div>
                    <div class="feature-card">
                        <h3>🎯 Key Benefits</h3>
                        <ul>
                            ${service.benefits.map(benefit => `<li>${benefit}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- Call to Action -->
        <section class="section" style="background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%); color: var(--color-white);">
            <div class="container" style="text-align: center;">
                <h2 style="font-size: var(--font-size-4xl); font-weight: 700; margin-bottom: var(--spacing-6); color: var(--color-white);">
                    Ready to Get Started with ${service.title}?
                </h2>
                <p style="font-size: var(--font-size-xl); margin-bottom: var(--spacing-8); opacity: 0.9; max-width: 600px; margin-left: auto; margin-right: auto;">
                    Join hundreds of businesses already using our ${service.title.toLowerCase()} service to grow their revenue and reduce costs.
                </p>
                <div style="display: flex; gap: var(--spacing-4); justify-content: center; flex-wrap: wrap;">
                    <a href="/contact" class="btn" style="background: var(--color-white); color: var(--color-primary); font-size: var(--font-size-lg); padding: var(--spacing-5) var(--spacing-10);">
                        Start Free Trial
                    </a>
                    <a href="/" class="btn" style="background: transparent; color: var(--color-white); border: 1px solid var(--color-white); font-size: var(--font-size-lg); padding: var(--spacing-5) var(--spacing-10);">
                        All Services
                    </a>
                </div>
            </div>
        </section>

        <!-- Related Services -->
        <section class="section-sm">
            <div class="container">
                <h3 style="text-align: center; font-size: var(--font-size-2xl); font-weight: 600; margin-bottom: var(--spacing-8); color: var(--color-black);">
                    Explore Our Other Services
                </h3>
                <div style="display: flex; gap: var(--spacing-4); justify-content: center; flex-wrap: wrap;">
                    ${Object.keys(SERVICES_DATA).filter(slug => slug !== serviceSlug).slice(0, 3).map(slug => 
                        `<a href="/${slug}" class="btn btn-secondary">${SERVICES_DATA[slug].icon} ${SERVICES_DATA[slug].title.split(' ')[0]}</a>`
                    ).join('')}
                </div>
            </div>
        </section>
    </main>
</body>
</html>
    `;
}

// Generate homepage HTML
function generateHomepage() {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bizoholic - AI-Powered Marketing Automation</title>
    <meta name="description" content="Transform your marketing with AI automation. Get 75% cost savings, ROI within 7 days, and setup in 15 minutes. The smartest marketing platform for small businesses.">
    <meta name="keywords" content="AI marketing automation, digital marketing SaaS, marketing campaigns, lead generation, SEO optimization">
    <meta name="author" content="Bizoholic Digital">
    <meta property="og:title" content="Bizoholic - AI-Powered Marketing Automation">
    <meta property="og:description" content="Transform your marketing with AI automation. Get 75% cost savings, ROI within 7 days, and setup in 15 minutes.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="http://localhost:3000">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Bizoholic - AI-Powered Marketing Automation">
    <meta name="twitter:description" content="AI-powered marketing automation for modern businesses">
    
    <!-- Preload fonts for better performance -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        :root {
            /* Apple-inspired Color Palette */
            --color-primary: #007AFF;
            --color-primary-dark: #0056CC;
            --color-secondary: #5AC8FA;
            --color-success: #34C759;
            --color-warning: #FF9F0A;
            --color-danger: #FF3B30;
            
            /* Neutral Colors */
            --color-black: #1D1D1F;
            --color-gray-900: #1C1C1E;
            --color-gray-800: #2C2C2E;
            --color-gray-700: #3A3A3C;
            --color-gray-600: #636366;
            --color-gray-500: #8E8E93;
            --color-gray-400: #AEAEB2;
            --color-gray-300: #C7C7CC;
            --color-gray-200: #D1D1D6;
            --color-gray-100: #F2F2F7;
            --color-white: #FFFFFF;
            
            /* Typography */
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --font-size-xs: 0.75rem;
            --font-size-sm: 0.875rem;
            --font-size-base: 1rem;
            --font-size-lg: 1.125rem;
            --font-size-xl: 1.25rem;
            --font-size-2xl: 1.5rem;
            --font-size-3xl: 1.875rem;
            --font-size-4xl: 2.25rem;
            --font-size-5xl: 3rem;
            --font-size-6xl: 3.75rem;
            
            /* Spacing */
            --spacing-1: 0.25rem;
            --spacing-2: 0.5rem;
            --spacing-3: 0.75rem;
            --spacing-4: 1rem;
            --spacing-5: 1.25rem;
            --spacing-6: 1.5rem;
            --spacing-8: 2rem;
            --spacing-10: 2.5rem;
            --spacing-12: 3rem;
            --spacing-16: 4rem;
            --spacing-20: 5rem;
            --spacing-24: 6rem;
            --spacing-32: 8rem;
            
            /* Shadows */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            
            /* Border Radius */
            --border-radius-sm: 0.375rem;
            --border-radius-md: 0.5rem;
            --border-radius-lg: 0.75rem;
            --border-radius-xl: 1rem;
            --border-radius-2xl: 1.5rem;
            
            /* Transitions */
            --transition-fast: all 0.15s ease;
            --transition-base: all 0.2s ease;
            --transition-slow: all 0.3s ease;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html {
            scroll-behavior: smooth;
        }
        
        body {
            font-family: var(--font-family);
            font-size: var(--font-size-base);
            line-height: 1.6;
            color: var(--color-black);
            background-color: var(--color-white);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        /* Layout Components */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 var(--spacing-6);
        }
        
        .section {
            padding: var(--spacing-24) 0;
        }
        
        /* Header & Navigation */
        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--color-gray-200);
            z-index: 1000;
            transition: var(--transition-base);
        }
        
        .nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: var(--spacing-4) 0;
            min-height: 60px;
        }
        
        .logo {
            font-size: var(--font-size-xl);
            font-weight: 700;
            color: var(--color-black);
            text-decoration: none;
            letter-spacing: -0.02em;
        }
        
        .nav-links {
            display: flex;
            align-items: center;
            gap: var(--spacing-8);
            list-style: none;
        }
        
        .nav-links a {
            color: var(--color-gray-600);
            text-decoration: none;
            font-weight: 500;
            font-size: var(--font-size-sm);
            transition: var(--transition-base);
            padding: var(--spacing-2) var(--spacing-3);
            border-radius: var(--border-radius-md);
        }
        
        .nav-links a:hover {
            color: var(--color-primary);
            background-color: var(--color-gray-100);
        }
        
        .nav-cta {
            display: flex;
            align-items: center;
            gap: var(--spacing-3);
        }
        
        /* Buttons */
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: var(--spacing-3) var(--spacing-6);
            font-size: var(--font-size-sm);
            font-weight: 600;
            text-decoration: none;
            border-radius: var(--border-radius-xl);
            transition: var(--transition-base);
            border: none;
            cursor: pointer;
            white-space: nowrap;
        }
        
        .btn-primary {
            background-color: var(--color-primary);
            color: var(--color-white);
        }
        
        .btn-primary:hover {
            background-color: var(--color-primary-dark);
            transform: translateY(-1px);
            box-shadow: var(--shadow-lg);
        }
        
        .btn-secondary {
            background-color: transparent;
            color: var(--color-primary);
            border: 1px solid var(--color-gray-300);
        }
        
        .btn-secondary:hover {
            background-color: var(--color-gray-100);
            border-color: var(--color-gray-400);
        }
        
        .btn-lg {
            padding: var(--spacing-4) var(--spacing-8);
            font-size: var(--font-size-base);
        }
        
        .btn-xl {
            padding: var(--spacing-5) var(--spacing-10);
            font-size: var(--font-size-lg);
        }
        
        /* Main Content Areas */
        .main {
            margin-top: 60px; /* Account for fixed header */
        }
        
        /* Hero Section - Apple.com Inspired */
        .hero {
            padding: var(--spacing-32) 0 var(--spacing-24);
            background: linear-gradient(180deg, var(--color-gray-100) 0%, var(--color-white) 50%);
            text-align: center;
        }
        
        .hero h1 {
            font-size: var(--font-size-6xl);
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -0.04em;
            margin-bottom: var(--spacing-6);
            color: var(--color-black);
        }
        
        .hero p {
            font-size: var(--font-size-2xl);
            font-weight: 400;
            line-height: 1.4;
            color: var(--color-gray-600);
            max-width: 800px;
            margin: 0 auto var(--spacing-10);
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: var(--spacing-8);
        }
        
        .feature-card {
            background-color: var(--color-white);
            border-radius: var(--border-radius-2xl);
            padding: var(--spacing-8);
            text-align: center;
            border: 1px solid var(--color-gray-200);
            transition: var(--transition-base);
            position: relative;
        }
        
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
            border-color: var(--color-gray-300);
        }
        
        .feature-icon {
            font-size: var(--font-size-5xl);
            margin-bottom: var(--spacing-4);
            display: block;
        }
        
        .feature-card h3 {
            font-size: var(--font-size-2xl);
            font-weight: 600;
            margin-bottom: var(--spacing-4);
            color: var(--color-black);
            letter-spacing: -0.01em;
        }
        
        .feature-card p {
            font-size: var(--font-size-base);
            line-height: 1.6;
            color: var(--color-gray-600);
            margin-bottom: var(--spacing-4);
        }
        
        .badge {
            position: absolute;
            top: var(--spacing-4);
            right: var(--spacing-4);
            background: var(--color-primary);
            color: var(--color-white);
            padding: var(--spacing-1) var(--spacing-3);
            border-radius: var(--border-radius-sm);
            font-size: var(--font-size-xs);
            font-weight: 600;
        }
        
        /* Stats Section */
        .stats {
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
            color: var(--color-white);
            padding: var(--spacing-24) 0;
            text-align: center;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: var(--spacing-8);
        }
        
        .stat-item h3 {
            font-size: var(--font-size-5xl);
            font-weight: 800;
            margin-bottom: var(--spacing-2);
            letter-spacing: -0.02em;
        }
        
        .stat-item p {
            font-size: var(--font-size-lg);
            font-weight: 500;
            opacity: 0.9;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
            
            .hero h1 {
                font-size: var(--font-size-4xl);
            }
            
            .hero p {
                font-size: var(--font-size-lg);
            }
            
            .features-grid {
                grid-template-columns: 1fr;
                gap: var(--spacing-4);
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav container">
            <a href="/" class="logo">
                <img src="/Bizoholic_Digital_-_Color-transparent.png" alt="Bizoholic Digital" style="height: 32px; width: auto;">
            </a>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/services">Services</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/pricing">Pricing</a></li>
                <li><a href="/contact">Contact</a></li>
            </ul>
            <div class="nav-cta">
                <a href="/contact" class="btn btn-secondary">Get Started</a>
                <a href="http://localhost:3005" class="btn btn-primary">Client Portal</a>
            </div>
        </nav>
    </header>

    <main class="main">
        <!-- Hero Section -->
        <section class="hero">
            <div class="container">
                <h1>AI-Powered Marketing Automation</h1>
                <p>Transform your marketing with AI automation. Get 75% cost savings, ROI within 7 days, and setup in 15 minutes. The smartest marketing platform for small businesses.</p>
                <div style="display: flex; gap: var(--spacing-4); justify-content: center; flex-wrap: wrap;">
                    <a href="/contact" class="btn btn-primary btn-xl">Get Started Free</a>
                    <a href="/services" class="btn btn-secondary btn-xl">View Services</a>
                </div>
            </div>
        </section>

        <!-- Featured Services Section -->
        <section class="section" style="background-color: var(--color-gray-100);">
            <div class="container">
                <h2 style="text-align: center; font-size: var(--font-size-4xl); font-weight: 700; margin-bottom: var(--spacing-4); color: var(--color-black);">Our Marketing Services</h2>
                <p style="text-align: center; font-size: var(--font-size-xl); color: var(--color-gray-600); max-width: 800px; margin: 0 auto var(--spacing-16);">Comprehensive AI-powered marketing solutions designed to grow your business</p>
                
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="badge">Most Popular</div>
                        <div class="feature-icon">🔍</div>
                        <h3>SEO Optimization</h3>
                        <p>Boost your search rankings with AI-powered SEO optimization. Deliver 200% better organic traffic within 90 days.</p>
                        <a href="/seo-optimization-local-seo" class="btn btn-primary" style="width: 100%;">From $299/month →</a>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">💰</div>
                        <h3>Paid Advertising (PPC)</h3>
                        <p>Maximize your ad spend with AI-driven PPC campaigns. Reduce cost-per-click by 45% while increasing conversions by 180%.</p>
                        <a href="/paid-advertising-ppc-management" class="btn btn-secondary" style="width: 100%;">From $599/month →</a>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">📱</div>
                        <h3>Social Media Marketing</h3>
                        <p>Grow your social presence with AI-powered content creation and scheduling. Generate viral-worthy posts automatically.</p>
                        <a href="/social-media-marketing-management" class="btn btn-secondary" style="width: 100%;">From $399/month →</a>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">🎯</div>
                        <h3>Lead Generation</h3>
                        <p>Generate high-quality leads with AI-powered targeting. Increase lead volume by 300% while reducing cost-per-lead by 50%.</p>
                        <a href="/lead-generation-conversion" class="btn btn-secondary" style="width: 100%;">From $449/month →</a>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">✍️</div>
                        <h3>Content Marketing</h3>
                        <p>Create engaging, SEO-optimized content that converts. Our AI writers produce content that ranks on page 1 of Google.</p>
                        <a href="/content-marketing-blog-writing" class="btn btn-secondary" style="width: 100%;">From $249/month →</a>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">📧</div>
                        <h3>Email Marketing</h3>
                        <p>Build automated email sequences that nurture leads and drive sales. AI personalizes every email for 60% higher conversion rates.</p>
                        <a href="/email-marketing-automation" class="btn btn-secondary" style="width: 100%;">From $199/month →</a>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: var(--spacing-16);">
                    <a href="/services" class="btn btn-primary btn-xl">View All 9 Services</a>
                </div>
            </div>
        </section>
        
        <!-- Stats Section -->
        <section class="stats">
            <div class="container">
                <div class="stats-grid">
                    <div class="stat-item">
                        <h3>75%</h3>
                        <p>Cost Savings</p>
                    </div>
                    <div class="stat-item">
                        <h3>7</h3>
                        <p>Days to ROI</p>
                    </div>
                    <div class="stat-item">
                        <h3>15</h3>
                        <p>Minutes Setup</p>
                    </div>
                    <div class="stat-item">
                        <h3>35+</h3>
                        <p>AI Agents</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="section">
            <div class="container">
                <div style="text-align: center; padding: var(--spacing-16) 0;">
                    <h2 style="font-size: var(--font-size-4xl); font-weight: 700; margin-bottom: var(--spacing-6); color: var(--color-black);">Ready to Transform Your Marketing?</h2>
                    <p style="font-size: var(--font-size-xl); color: var(--color-gray-600); max-width: 600px; margin: 0 auto var(--spacing-8);">Join hundreds of businesses already using AI to scale their marketing and reduce costs.</p>
                    <div style="display: flex; gap: var(--spacing-4); justify-content: center; flex-wrap: wrap;">
                        <a href="/contact" class="btn btn-primary btn-xl">Start Free Trial</a>
                        <a href="/services" class="btn btn-secondary btn-xl">View Services</a>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <script>
        // Apple.com-inspired header scroll effect
        function initHeaderScrollEffect() {
            const header = document.querySelector('.header');
            
            function updateHeader() {
                const scrollY = window.scrollY;
                
                if (scrollY > 60) {
                    header.classList.add('scrolled');
                } else {
                    header.classList.remove('scrolled');
                }
            }
            
            // Throttled scroll event for better performance
            let ticking = false;
            function onScroll() {
                if (!ticking) {
                    requestAnimationFrame(() => {
                        updateHeader();
                        ticking = false;
                    });
                    ticking = true;
                }
            }
            
            window.addEventListener('scroll', onScroll, { passive: true });
            updateHeader(); // Initial call
        }
        
        // Enhanced animations on scroll (intersection observer)
        function initScrollAnimations() {
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }
                });
            }, observerOptions);
            
            // Observe feature cards and stats with staggered animation
            const elements = document.querySelectorAll('.feature-card, .stat-item');
            elements.forEach((el, index) => {
                el.style.opacity = '0';
                el.style.transform = 'translateY(30px)';
                el.style.transition = \`opacity 0.6s ease \${index * 0.1}s, transform 0.6s ease \${index * 0.1}s\`;
                observer.observe(el);
            });
        }
        
        // Initialize all interactions when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            initHeaderScrollEffect();
            initScrollAnimations();
        });
    </script>
</body>
</html>
    `;
}

// Routes
// Serve logo image
app.get('/Bizoholic_Digital_-_Color-transparent.png', (req, res) => {
    res.sendFile('/home/alagiri/projects/bizoholic/Bizoholic_Digital_-_Color-transparent.png');
});

app.get('/', (req, res) => {
    // Serve our Apple.com-inspired homepage directly
    const homepageHtml = generateHomepage();
    res.send(homepageHtml);
});

// Service page routes
Object.keys(SERVICES_DATA).forEach(serviceSlug => {
    app.get(`/${serviceSlug}`, (req, res) => {
        const html = generateServicePage(serviceSlug);
        if (html) {
            res.send(html);
        } else {
            res.status(404).send('Service not found');
        }
    });
});

// Services overview page
app.get('/services', (req, res) => {
    const servicesHtml = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All Services - Bizoholic AI Marketing</title>
    <meta name="description" content="Explore all our AI-powered marketing services. From SEO and PPC to social media and content marketing.">
</head>
<body>
    <h1>All Marketing Services</h1>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; padding: 2rem;">
        ${Object.entries(SERVICES_DATA).map(([slug, service]) => `
            <div style="border: 1px solid #ddd; border-radius: 12px; padding: 1.5rem; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">${service.icon}</div>
                <h3>${service.title}</h3>
                <p>${service.description.substring(0, 120)}...</p>
                <p><strong>${service.price}</strong></p>
                <a href="/${slug}" style="display: inline-block; background: #007AFF; color: white; padding: 0.75rem 1.5rem; text-decoration: none; border-radius: 8px; margin-top: 1rem;">Learn More</a>
            </div>
        `).join('')}
    </div>
</body>
</html>
    `;
    res.send(servicesHtml);
});

// 404 handler
app.use((req, res) => {
    res.status(404).send(`
<!DOCTYPE html>
<html>
<head>
    <title>Page Not Found - Bizoholic</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; text-align: center; padding: 4rem; }
        .container { max-width: 600px; margin: 0 auto; }
        h1 { font-size: 4rem; margin-bottom: 1rem; color: #1D1D1F; }
        p { font-size: 1.25rem; color: #636366; margin-bottom: 2rem; }
        .btn { display: inline-block; background: #007AFF; color: white; padding: 1rem 2rem; text-decoration: none; border-radius: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖</h1>
        <h2>Page Not Found</h2>
        <p>The page you're looking for doesn't exist. Let's get you back on track.</p>
        <a href="/" class="btn">Go to Homepage</a>
    </div>
</body>
</html>
    `);
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Static Website Server running at:`);
    console.log(`   Local:    http://localhost:${PORT}`);
    console.log(`   Network:  http://0.0.0.0:${PORT}`);
    console.log('');
    console.log('📄 Available service pages:');
    Object.keys(SERVICES_DATA).forEach(slug => {
        console.log(`   • http://localhost:${PORT}/${slug}`);
    });
    console.log(`   • http://localhost:${PORT}/services (all services)`);
    console.log('');
    console.log('🎯 Ready to serve AI-powered marketing services! 🎉');
});

module.exports = app;
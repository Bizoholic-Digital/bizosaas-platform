#!/usr/bin/env node

const express = require('express');
const app = express();

app.use(express.static('public'));

// Bizoholic homepage and service routes
const serveBizoholicPage = (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bizoholic - AI-Powered Marketing Automation</title>
    <meta name="description" content="Transform your marketing with AI automation that delivers 200% better results. Professional SEO, PPC, social media, and content marketing services.">
    <meta name="keywords" content="AI marketing, digital marketing automation, SEO services, PPC management, social media marketing">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="Bizoholic - AI-Powered Marketing Automation">
    <meta property="og:description" content="Transform your marketing with AI automation that delivers 200% better results.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="http://localhost:3000">
    
    <!-- Twitter Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Bizoholic - AI-Powered Marketing Automation">
    <meta name="twitter:description" content="Transform your marketing with AI automation that delivers 200% better results.">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Bizoholic",
        "description": "AI-Powered Marketing Automation Agency",
        "url": "http://localhost:3000",
        "logo": "http://localhost:3000/logo.png",
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+1-800-BIZOHOLIC",
            "contactType": "customer service"
        },
        "sameAs": [
            "https://twitter.com/bizoholic",
            "https://linkedin.com/company/bizoholic",
            "https://facebook.com/bizoholic"
        ]
    }
    </script>
    
    <style>
        :root {
            --color-primary: #007AFF;
            --color-primary-dark: #0056CC;
            --color-secondary: #5856D6;
            --color-success: #34C759;
            --color-warning: #FF9500;
            --color-error: #FF3B30;
            --color-white: #FFFFFF;
            --color-black: #000000;
            --color-gray-50: #F9FAFB;
            --color-gray-100: #F3F4F6;
            --color-gray-200: #E5E7EB;
            --color-gray-300: #D1D5DB;
            --color-gray-400: #9CA3AF;
            --color-gray-500: #6B7280;
            --color-gray-600: #4B5563;
            --color-gray-700: #374151;
            --color-gray-800: #1F2937;
            --color-gray-900: #111827;
            
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
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
            --font-size-7xl: 4.5rem;
            
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
            
            --border-radius-sm: 0.25rem;
            --border-radius-base: 0.375rem;
            --border-radius-lg: 0.5rem;
            --border-radius-xl: 0.75rem;
            --border-radius-2xl: 1rem;
            --border-radius-3xl: 1.5rem;
            
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-base: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            
            --transition-base: all 0.2s ease;
            --transition-slow: all 0.3s ease;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: var(--font-family);
            line-height: 1.6;
            color: var(--color-gray-800);
            background-color: var(--color-white);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
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
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 var(--spacing-6);
        }
        
        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--spacing-4) 0;
        }
        
        .logo {
            font-size: var(--font-size-2xl);
            font-weight: 700;
            color: var(--color-black);
            text-decoration: none;
        }
        
        .nav-links {
            display: flex;
            list-style: none;
            gap: var(--spacing-8);
        }
        
        .nav-links a {
            color: var(--color-gray-600);
            text-decoration: none;
            font-weight: 500;
            transition: var(--transition-base);
        }
        
        .nav-links a:hover {
            color: var(--color-primary);
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: var(--spacing-3) var(--spacing-6);
            font-size: var(--font-size-base);
            font-weight: 600;
            border-radius: var(--border-radius-lg);
            text-decoration: none;
            cursor: pointer;
            border: none;
            transition: var(--transition-base);
        }
        
        .btn-primary {
            background: var(--color-primary);
            color: var(--color-white);
        }
        
        .btn-primary:hover {
            background: var(--color-primary-dark);
            transform: translateY(-1px);
            box-shadow: var(--shadow-lg);
        }
        
        .btn-secondary {
            background: transparent;
            color: var(--color-primary);
            border: 2px solid var(--color-primary);
        }
        
        .btn-secondary:hover {
            background: var(--color-primary);
            color: var(--color-white);
        }
        
        .btn-lg {
            padding: var(--spacing-4) var(--spacing-8);
            font-size: var(--font-size-lg);
        }
        
        .btn-xl {
            padding: var(--spacing-5) var(--spacing-10);
            font-size: var(--font-size-xl);
        }
        
        .main {
            margin-top: 80px;
        }
        
        .hero {
            padding: var(--spacing-32) 0;
            text-align: center;
            background: linear-gradient(135deg, var(--color-gray-50) 0%, var(--color-white) 100%);
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
        
        .cta-buttons {
            display: flex;
            gap: var(--spacing-4);
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: var(--spacing-16);
        }
        
        .stats {
            display: flex;
            justify-content: center;
            gap: var(--spacing-12);
            flex-wrap: wrap;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-number {
            font-size: var(--font-size-4xl);
            font-weight: 800;
            color: var(--color-primary);
        }
        
        .stat-label {
            font-size: var(--font-size-base);
            color: var(--color-gray-600);
            margin-top: var(--spacing-2);
        }
        
        .section {
            padding: var(--spacing-24) 0;
        }
        
        .section-title {
            font-size: var(--font-size-4xl);
            font-weight: 700;
            text-align: center;
            margin-bottom: var(--spacing-16);
            color: var(--color-black);
            letter-spacing: -0.02em;
        }
        
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: var(--spacing-8);
            margin-top: var(--spacing-12);
        }
        
        .service-card {
            background: var(--color-white);
            padding: var(--spacing-8);
            border-radius: var(--border-radius-2xl);
            box-shadow: var(--shadow-base);
            transition: var(--transition-base);
            border: 1px solid var(--color-gray-200);
        }
        
        .service-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
        }
        
        .service-icon {
            font-size: var(--font-size-4xl);
            margin-bottom: var(--spacing-4);
        }
        
        .service-card h3 {
            font-size: var(--font-size-2xl);
            font-weight: 600;
            margin-bottom: var(--spacing-3);
            color: var(--color-black);
        }
        
        .service-card p {
            color: var(--color-gray-600);
            margin-bottom: var(--spacing-6);
            line-height: 1.6;
        }
        
        .service-price {
            font-size: var(--font-size-xl);
            font-weight: 700;
            color: var(--color-primary);
            margin-bottom: var(--spacing-4);
        }
        
        .footer {
            background: var(--color-gray-900);
            color: var(--color-gray-300);
            padding: var(--spacing-20) 0 var(--spacing-8);
            text-align: center;
        }
        
        .footer h2 {
            color: var(--color-white);
            font-size: var(--font-size-3xl);
            margin-bottom: var(--spacing-6);
        }
        
        .footer p {
            max-width: 600px;
            margin: 0 auto var(--spacing-8);
            line-height: 1.6;
        }
        
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
            
            .hero h1 {
                font-size: var(--font-size-4xl);
            }
            
            .hero p {
                font-size: var(--font-size-xl);
            }
            
            .cta-buttons {
                flex-direction: column;
                align-items: center;
            }
            
            .stats {
                flex-direction: column;
                gap: var(--spacing-6);
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <nav class="nav">
                <a href="/" class="logo">Bizoholic</a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/services">Services</a></li>
                    <li><a href="/pricing">Pricing</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
                <a href="/contact" class="btn btn-primary">Get Started</a>
            </nav>
        </div>
    </header>

    <main class="main">
        <section class="hero">
            <div class="container">
                <h1>AI-Powered Marketing Automation</h1>
                <p>Transform your marketing with AI automation that delivers 200% better results. Our intelligent agents optimize campaigns 24/7, increase conversions, and reduce costs.</p>
                
                <div class="cta-buttons">
                    <a href="/contact" class="btn btn-primary btn-xl">Start Free Trial</a>
                    <a href="/demo" class="btn btn-secondary btn-xl">Watch Demo</a>
                </div>
                
                <div class="stats">
                    <div class="stat">
                        <div class="stat-number">200%</div>
                        <div class="stat-label">Better Results</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">10K+</div>
                        <div class="stat-label">Happy Clients</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">24/7</div>
                        <div class="stat-label">AI Optimization</div>
                    </div>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <h2 class="section-title">Our AI Marketing Services</h2>
                
                <div class="services-grid">
                    <div class="service-card">
                        <div class="service-icon">🔍</div>
                        <h3>SEO Optimization & Local SEO</h3>
                        <p>Boost your search rankings with AI-powered SEO optimization. Our advanced algorithms analyze your website, competitors, and search trends to deliver 200% better organic traffic within 90 days.</p>
                        <div class="service-price">Starting at $299/month</div>
                        <a href="/seo-optimization-local-seo" class="btn btn-primary">Learn More</a>
                    </div>
                    
                    <div class="service-card">
                        <div class="service-icon">💰</div>
                        <h3>Paid Advertising (PPC) Management</h3>
                        <p>Maximize your ad spend with AI-driven PPC campaigns. Our intelligent bidding algorithms reduce cost-per-click by 45% while increasing conversions by 180%.</p>
                        <div class="service-price">Starting at $599/month</div>
                        <a href="/paid-advertising-ppc-management" class="btn btn-primary">Learn More</a>
                    </div>
                    
                    <div class="service-card">
                        <div class="service-icon">📱</div>
                        <h3>Social Media Marketing & Management</h3>
                        <p>Grow your social presence with AI-powered content creation and scheduling. Generate viral-worthy posts, optimize posting times, and engage with your audience automatically.</p>
                        <div class="service-price">Starting at $399/month</div>
                        <a href="/social-media-marketing-management" class="btn btn-primary">Learn More</a>
                    </div>
                    
                    <div class="service-card">
                        <div class="service-icon">✍️</div>
                        <h3>Content Marketing & Blog Writing</h3>
                        <p>Create engaging, SEO-optimized content that converts. Our AI writers produce high-quality blog posts, articles, and web copy that ranks on page 1 of Google.</p>
                        <div class="service-price">Starting at $249/month</div>
                        <a href="/content-marketing-blog-writing" class="btn btn-primary">Learn More</a>
                    </div>
                    
                    <div class="service-card">
                        <div class="service-icon">📧</div>
                        <h3>Email Marketing Automation</h3>
                        <p>Build automated email sequences that nurture leads and drive sales. Our AI personalizes every email for maximum engagement and 60% higher conversion rates.</p>
                        <div class="service-price">Starting at $199/month</div>
                        <a href="/email-marketing-automation" class="btn btn-primary">Learn More</a>
                    </div>
                    
                    <div class="service-card">
                        <div class="service-icon">🎯</div>
                        <h3>Lead Generation & Conversion</h3>
                        <p>Generate high-quality leads with AI-powered targeting and conversion optimization. Increase your lead volume by 300% while reducing cost-per-lead by 50%.</p>
                        <div class="service-price">Starting at $449/month</div>
                        <a href="/lead-generation-conversion" class="btn btn-primary">Learn More</a>
                    </div>
                    
                    <div class="service-card">
                        <div class="service-icon">🌐</div>
                        <h3>Website Design & Development</h3>
                        <p>Build high-converting websites with AI-optimized design and development. Our responsive, fast-loading sites increase conversion rates by 150% and improve user experience.</p>
                        <div class="service-price">Starting at $1,299 one-time</div>
                        <a href="/website-design-development" class="btn btn-primary">Learn More</a>
                    </div>
                    
                    <div class="service-card">
                        <div class="service-icon">📊</div>
                        <h3>Analytics & Performance Tracking</h3>
                        <p>Make data-driven decisions with advanced analytics and AI insights. Track every metric that matters and get actionable recommendations to improve your marketing ROI.</p>
                        <div class="service-price">Starting at $149/month</div>
                        <a href="/analytics-performance-tracking" class="btn btn-primary">Learn More</a>
                    </div>
                    
                    <div class="service-card">
                        <div class="service-icon">🏆</div>
                        <h3>Brand Strategy & Reputation Management</h3>
                        <p>Build and protect your brand with AI-powered reputation management. Monitor mentions, respond to reviews automatically, and strengthen your brand presence across all channels.</p>
                        <div class="service-price">Starting at $349/month</div>
                        <a href="/brand-strategy-reputation-management" class="btn btn-primary">Learn More</a>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="footer">
        <div class="container">
            <h2>Ready to Transform Your Marketing?</h2>
            <p>Join thousands of businesses already using our AI-powered marketing automation to grow their revenue and reduce costs.</p>
            <a href="/contact" class="btn btn-primary btn-xl">Start Your Free Trial Today</a>
        </div>
    </footer>
</body>
</html>
    `);
};

// Define routes
app.get('/', serveBizoholicPage);
app.get('/home', serveBizoholicPage);
app.get('/services', serveBizoholicPage);
app.get('/pricing', serveBizoholicPage);
app.get('/about', serveBizoholicPage);
app.get('/contact', serveBizoholicPage);
app.get('/demo', serveBizoholicPage);
app.get('/seo-optimization-local-seo', serveBizoholicPage);
app.get('/paid-advertising-ppc-management', serveBizoholicPage);
app.get('/social-media-marketing-management', serveBizoholicPage);
app.get('/content-marketing-blog-writing', serveBizoholicPage);
app.get('/email-marketing-automation', serveBizoholicPage);
app.get('/lead-generation-conversion', serveBizoholicPage);
app.get('/website-design-development', serveBizoholicPage);
app.get('/analytics-performance-tracking', serveBizoholicPage);
app.get('/brand-strategy-reputation-management', serveBizoholicPage);

const PORT = 3000;
const HOST = '0.0.0.0';

app.listen(PORT, HOST, () => {
    console.log(`🚀 Bizoholic Marketing Website running at:`);
    console.log(`   Local:    http://localhost:${PORT}`);
    console.log(`   Network:  http://${HOST}:${PORT}`);
    console.log(`🎯 AI-Powered Marketing Automation is LIVE! 🎉`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('\\nShutting down Bizoholic server...');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('\\nShutting down Bizoholic server...');
    process.exit(0);
});
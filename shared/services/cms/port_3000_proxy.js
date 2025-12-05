#!/usr/bin/env node

const http = require('http');
const httpProxy = require('http-proxy');

// Create proxy server
const proxy = httpProxy.createProxyServer({});

// Handle proxy errors gracefully
proxy.on('error', (err, req, res) => {
    console.error('Proxy error:', err.message);
    if (res && !res.headersSent) {
        res.writeHead(502, { 'Content-Type': 'text/html' });
        res.end(`
            <html>
                <head><title>Service Unavailable - Bizoholic</title></head>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1>🚧 Service Temporarily Unavailable</h1>
                    <p>Wagtail CMS is starting up. Please refresh in a moment.</p>
                    <p><a href="/" onclick="window.location.reload()" style="color: #0d9488;">🔄 Refresh Page</a></p>
                </body>
            </html>
        `);
    }
});

// Create HTTP server that routes intelligently
const server = http.createServer((req, res) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    
    // Check if this is a service page request
    const serviceRoutes = [
        '/seo-optimization-local-seo',
        '/paid-advertising-ppc-management', 
        '/social-media-marketing-management',
        '/content-marketing-blog-writing',
        '/email-marketing-automation',
        '/lead-generation-conversion',
        '/website-design-development',
        '/analytics-performance-tracking',
        '/brand-strategy-reputation-management',
        '/services'
    ];
    
    const isServicePage = serviceRoutes.some(route => req.url.startsWith(route));
    
    if (req.url === '/' || req.url === '/home') {
        // Route homepage to our static website server for now (until Wagtail is configured)
        proxy.web(req, res, {
            target: 'http://localhost:3001',
            changeOrigin: true,
            timeout: 10000,
            proxyTimeout: 10000,
        });
    } else if (isServicePage) {
        // Route service pages to our static website server
        proxy.web(req, res, {
            target: 'http://localhost:3001',
            changeOrigin: true,
            timeout: 10000,
            proxyTimeout: 10000,
        });
    } else {
        // Route everything else to Wagtail CMS 
        proxy.web(req, res, {
            target: 'http://localhost:8006',
            changeOrigin: true,
            timeout: 10000,
            proxyTimeout: 10000,
        });
    }
});

const PORT = process.env.PORT || 3000;
const HOST = '0.0.0.0';

server.listen(PORT, HOST, () => {
    console.log(`🚀 Bizoholic Website Proxy running at:`);
    console.log(`   Local:    http://localhost:${PORT}`);
    console.log(`   Network:  http://${HOST}:${PORT}`);
    console.log(``);
    console.log(`🔄 Proxying all requests to Wagtail CMS at http://localhost:8006`);
    console.log(`📊 This will serve the dynamic Wagtail-powered website on port 3000`);
    console.log(``);
    console.log(`Ready to serve the Bizoholic dynamic website! 🎉`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('\nShutting down Bizoholic proxy server...');
    server.close(() => {
        console.log('Proxy server closed.');
        process.exit(0);
    });
});

process.on('SIGINT', () => {
    console.log('\nShutting down Bizoholic proxy server...');
    server.close(() => {
        console.log('Proxy server closed.');
        process.exit(0);
    });
});
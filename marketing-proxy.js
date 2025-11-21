const http = require('http');
const httpProxy = require('http-proxy');

// Create a proxy server
const proxy = httpProxy.createProxyServer({});

// Create the marketing proxy server
const server = http.createServer((req, res) => {
  // Set CORS headers to avoid issues
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // Proxy all requests to localhost:3002 where the marketing website is working
  proxy.web(req, res, {
    target: 'http://localhost:3002',
    changeOrigin: true,
    headers: {
      host: 'localhost:3001'
    }
  }, (error) => {
    console.error('Proxy error:', error);
    res.writeHead(500, {'Content-Type': 'text/html'});
    res.end('<h1>Proxy Error</h1><p>Unable to connect to marketing website</p>');
  });
});

// Handle upgrade requests (WebSockets)
server.on('upgrade', (req, socket, head) => {
  proxy.ws(req, socket, head, {
    target: 'http://localhost:3002',
    changeOrigin: true
  });
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Marketing proxy server running on port ${PORT}`);
  console.log(`Proxying requests to http://localhost:3002`);
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
  console.log('Received SIGTERM, shutting down gracefully');
  server.close(() => {
    console.log('HTTP server closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('Received SIGINT, shutting down gracefully');
  server.close(() => {
    console.log('HTTP server closed');
    process.exit(0);
  });
});
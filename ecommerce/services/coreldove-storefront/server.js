const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3003;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Saleor GraphQL API endpoint (correct port is 8024)
const SALEOR_API_URL = process.env.SALEOR_API_URL || 'http://localhost:8024/graphql/';

// Login redirect to unified BizOSaaS dashboard
app.get('/login', (req, res) => {
    res.redirect('http://localhost:3000/auth/login?redirect=coreldove');
});

// Main CoreLDove Storefront Route
app.get('/', (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CoreLDove - AI-Powered Dropshipping Store</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .product-card:hover { transform: translateY(-4px); }
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .pulse { animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .urgent-offer { background: linear-gradient(45deg, #ff6b6b, #ee5a52); }
        .trust-badge { background: rgba(34, 197, 94, 0.1); border: 1px solid rgb(34, 197, 94); }
        .floating-chat { position: fixed; bottom: 20px; right: 20px; z-index: 1000; }
        .scarcity-indicator { background: linear-gradient(45deg, #f59e0b, #d97706); }
        .social-proof { background: rgba(59, 130, 246, 0.05); border-left: 4px solid rgb(59, 130, 246); }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center">
                    <h1 class="text-2xl font-bold text-gray-900">CoreLDove</h1>
                    <span class="ml-2 bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">AI-Powered</span>
                    <div class="ml-4 hidden md:flex items-center space-x-2 text-xs">
                        <span class="trust-badge text-green-700 px-2 py-1 rounded">✅ Trusted by 10K+ Customers</span>
                        <span class="scarcity-indicator text-white px-2 py-1 rounded pulse">🔥 Flash Sale: 40% OFF</span>
                    </div>
                </div>
                <nav class="hidden md:flex space-x-8">
                    <a href="#" class="text-gray-900 hover:text-blue-600">Home</a>
                    <a href="#products" class="text-gray-600 hover:text-blue-600">Products</a>
                    <a href="#categories" class="text-gray-600 hover:text-blue-600">Categories</a>
                    <a href="#about" class="text-gray-600 hover:text-blue-600">About</a>
                </nav>
                <div class="flex items-center space-x-4">
                    <button class="relative p-2">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1.5 5M7 13l-1.5-5M7 13h10m0 0v8a2 2 0 01-2 2H9a2 2 0 01-2-2v-8m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01"></path>
                        </svg>
                        <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">0</span>
                    </button>
                    <button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium">
                        Sign In
                    </button>
                </div>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="gradient-bg text-white py-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 class="text-5xl font-bold mb-6">Discover Amazing Products</h2>
            <p class="text-xl mb-8 max-w-2xl mx-auto">AI-curated selection of sports, fitness, and wellness products sourced from trusted suppliers worldwide</p>
            <button class="bg-white text-blue-600 hover:bg-gray-100 px-8 py-3 rounded-lg font-semibold text-lg transition duration-300">
                Shop Now
            </button>
        </div>
    </section>

    <!-- Featured Categories -->
    <section id="categories" class="py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h3 class="text-3xl font-bold text-gray-900 mb-12 text-center">Featured Categories</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition duration-300">
                    <div class="h-48 bg-gradient-to-r from-green-400 to-blue-500"></div>
                    <div class="p-6">
                        <h4 class="text-xl font-semibold mb-2">Sports Equipment</h4>
                        <p class="text-gray-600 mb-4">Professional sports gear for all activities</p>
                        <button class="text-blue-600 hover:text-blue-800 font-medium">Explore →</button>
                    </div>
                </div>
                <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition duration-300">
                    <div class="h-48 bg-gradient-to-r from-purple-400 to-pink-500"></div>
                    <div class="p-6">
                        <h4 class="text-xl font-semibold mb-2">Fitness & Exercise</h4>
                        <p class="text-gray-600 mb-4">Home and gym fitness equipment</p>
                        <button class="text-blue-600 hover:text-blue-800 font-medium">Explore →</button>
                    </div>
                </div>
                <div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition duration-300">
                    <div class="h-48 bg-gradient-to-r from-orange-400 to-red-500"></div>
                    <div class="p-6">
                        <h4 class="text-xl font-semibold mb-2">Health & Wellness</h4>
                        <p class="text-gray-600 mb-4">Nutrition and recovery products</p>
                        <button class="text-blue-600 hover:text-blue-800 font-medium">Explore →</button>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Products Section -->
    <section id="products" class="bg-white py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center mb-12">
                <h3 class="text-3xl font-bold text-gray-900">Featured Products</h3>
                <div class="text-sm text-gray-600">
                    <span id="product-status">Loading products from Saleor...</span>
                </div>
            </div>
            <div id="products-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                <!-- Products will be loaded here -->
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
                <div>
                    <h4 class="text-xl font-bold mb-4">CoreLDove</h4>
                    <p class="text-gray-400">AI-powered dropshipping platform connecting you with quality products worldwide.</p>
                </div>
                <div>
                    <h5 class="font-semibold mb-4">Shop</h5>
                    <ul class="space-y-2 text-gray-400">
                        <li><a href="#" class="hover:text-white">Sports Equipment</a></li>
                        <li><a href="#" class="hover:text-white">Fitness & Exercise</a></li>
                        <li><a href="#" class="hover:text-white">Health Products</a></li>
                    </ul>
                </div>
                <div>
                    <h5 class="font-semibold mb-4">Support</h5>
                    <ul class="space-y-2 text-gray-400">
                        <li><a href="#" class="hover:text-white">Help Center</a></li>
                        <li><a href="#" class="hover:text-white">Shipping Info</a></li>
                        <li><a href="#" class="hover:text-white">Returns</a></li>
                    </ul>
                </div>
                <div>
                    <h5 class="font-semibold mb-4">Connect</h5>
                    <ul class="space-y-2 text-gray-400">
                        <li><a href="#" class="hover:text-white">Newsletter</a></li>
                        <li><a href="#" class="hover:text-white">Social Media</a></li>
                        <li><a href="#" class="hover:text-white">Contact Us</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
                <p>&copy; 2025 CoreLDove. Powered by AI. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Load products from Saleor API
        async function loadProducts() {
            const statusElement = document.getElementById('product-status');
            const gridElement = document.getElementById('products-grid');
            
            try {
                statusElement.textContent = 'Connecting to Saleor API...';
                
                // GraphQL query to fetch products
                const query = \`
                    query GetProducts {
                        products(first: 8) {
                            edges {
                                node {
                                    id
                                    name
                                    description
                                    thumbnail {
                                        url
                                    }
                                    pricing {
                                        priceRange {
                                            start {
                                                gross {
                                                    amount
                                                    currency
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                \`;

                const response = await fetch('${SALEOR_API_URL}', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query })
                });

                const data = await response.json();
                
                if (data.errors) {
                    throw new Error(data.errors[0].message);
                }

                const products = data.data.products.edges;
                
                if (products.length === 0) {
                    statusElement.textContent = 'No products found. Add products in Saleor Dashboard.';
                    gridElement.innerHTML = createNoProductsMessage();
                } else {
                    statusElement.textContent = \`Showing \${products.length} products\`;
                    gridElement.innerHTML = products.map(createProductCard).join('');
                }
                
            } catch (error) {
                console.error('Error loading products:', error);
                statusElement.textContent = 'Showing sample products (Saleor API not available)';
                gridElement.innerHTML = createSampleProducts();
            }
        }

        function createProductCard({ node: product }) {
            const price = product.pricing?.priceRange?.start?.gross;
            const thumbnail = product.thumbnail?.url || '/api/placeholder/300/300';
            
            return \`
                <div class="bg-white rounded-lg shadow-md overflow-hidden product-card transition duration-300">
                    <img src="\${thumbnail}" alt="\${product.name}" class="w-full h-48 object-cover">
                    <div class="p-4">
                        <h4 class="text-lg font-semibold mb-2 truncate">\${product.name}</h4>
                        <p class="text-gray-600 text-sm mb-4 line-clamp-2">\${product.description || 'No description available'}</p>
                        <div class="flex justify-between items-center">
                            <span class="text-xl font-bold text-blue-600">
                                \${price ? \`\${price.currency} \${price.amount}\` : 'Price on request'}
                            </span>
                            <button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm font-medium">
                                Add to Cart
                            </button>
                        </div>
                    </div>
                </div>
            \`;
        }

        function createNoProductsMessage() {
            return \`
                <div class="col-span-full text-center py-12">
                    <div class="text-gray-400 mb-4">
                        <svg class="mx-auto h-24 w-24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold text-gray-600 mb-2">No Products Yet</h3>
                    <p class="text-gray-500 mb-6 max-w-md mx-auto">
                        Add products to your Saleor dashboard to see them here. 
                        You can also use the Amazon integration to import products automatically.
                    </p>
                    <a href="http://localhost:9000" target="_blank" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium inline-block">
                        Open Saleor Dashboard
                    </a>
                </div>
            \`;
        }

        function createErrorMessage() {
            return \`
                <div class="col-span-full text-center py-12">
                    <div class="text-red-400 mb-4">
                        <svg class="mx-auto h-24 w-24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                    </div>
                    <h3 class="text-xl font-semibold text-red-600 mb-2">Connection Error</h3>
                    <p class="text-gray-500 mb-6">
                        Unable to connect to Saleor API. Please check that Saleor is running on port 8100.
                    </p>
                    <button onclick="loadProducts()" class="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-medium">
                        Retry Connection
                    </button>
                </div>
            \`;
        }

        function createSampleProducts() {
            const sampleProducts = [
                {
                    id: 'sample-1',
                    name: 'Professional Basketball',
                    description: 'High-quality basketball for professional training and games',
                    price: { amount: '49.99', currency: 'USD' },
                    image: 'https://images.unsplash.com/photo-1546519638-68e109498ffc?ixlib=rb-4.0.3&w=400&h=300&fit=crop'
                },
                {
                    id: 'sample-2', 
                    name: 'Yoga Mat Premium',
                    description: 'Eco-friendly premium yoga mat with excellent grip',
                    price: { amount: '79.99', currency: 'USD' },
                    image: 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?ixlib=rb-4.0.3&w=400&h=300&fit=crop'
                },
                {
                    id: 'sample-3',
                    name: 'Protein Powder Vanilla',
                    description: 'Premium whey protein powder for muscle building',
                    price: { amount: '59.99', currency: 'USD' },
                    image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&w=400&h=300&fit=crop'
                },
                {
                    id: 'sample-4',
                    name: 'Resistance Band Set',
                    description: 'Complete set of resistance bands for home workouts',
                    price: { amount: '29.99', currency: 'USD' },
                    image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&w=400&h=300&fit=crop'
                },
                {
                    id: 'sample-5',
                    name: 'Running Shoes',
                    description: 'Lightweight running shoes for maximum comfort',
                    price: { amount: '129.99', currency: 'USD' },
                    image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&w=400&h=300&fit=crop'
                },
                {
                    id: 'sample-6',
                    name: 'Dumbbell Set',
                    description: 'Adjustable dumbbell set for strength training',
                    price: { amount: '199.99', currency: 'USD' },
                    image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&w=400&h=300&fit=crop'
                },
                {
                    id: 'sample-7',
                    name: 'Fitness Tracker',
                    description: 'Smart fitness tracker with heart rate monitoring',
                    price: { amount: '149.99', currency: 'USD' },
                    image: 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?ixlib=rb-4.0.3&w=400&h=300&fit=crop'
                },
                {
                    id: 'sample-8',
                    name: 'Water Bottle',
                    description: 'Insulated stainless steel water bottle',
                    price: { amount: '24.99', currency: 'USD' },
                    image: 'https://images.unsplash.com/photo-1523362628745-0c100150b504?ixlib=rb-4.0.3&w=400&h=300&fit=crop'
                }
            ];

            return sampleProducts.map(product => \`
                <div class="bg-white rounded-lg shadow-md overflow-hidden product-card transition duration-300">
                    <img src="\${product.image}" alt="\${product.name}" class="w-full h-48 object-cover">
                    <div class="p-4">
                        <h4 class="text-lg font-semibold mb-2 truncate">\${product.name}</h4>
                        <p class="text-gray-600 text-sm mb-4 line-clamp-2">\${product.description}</p>
                        <div class="flex justify-between items-center">
                            <span class="text-xl font-bold text-blue-600">
                                \${product.price.currency} \${product.price.amount}
                            </span>
                            <button class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm font-medium">
                                Add to Cart
                            </button>
                        </div>
                    </div>
                </div>
            \`).join('');
        }

        // Load products when page loads
        document.addEventListener('DOMContentLoaded', loadProducts);
    </script>
</body>
</html>
    `);
});

// Legacy redirect to unified BizOSaaS dashboard
app.get('/dashboard', (req, res) => {
    res.redirect('http://localhost:3000/dashboard/coreldove');
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ 
        status: 'healthy', 
        service: 'coreldove-storefront',
        timestamp: new Date().toISOString(),
        saleor_api: SALEOR_API_URL
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🛒 CoreLDove Storefront running on http://localhost:${PORT}`);
    console.log(`📡 Saleor API: ${SALEOR_API_URL}`);
});
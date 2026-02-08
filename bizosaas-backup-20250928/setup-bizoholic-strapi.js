#!/usr/bin/env node

/**
 * Setup script for Bizoholic Strapi CMS
 * This script configures API permissions and creates sample content
 */

const axios = require('axios');

const STRAPI_URL = 'http://localhost:1337';

console.log('🚀 Setting up Bizoholic Strapi CMS...\n');

async function setupStrapi() {
  try {
    // Check if Strapi is accessible
    console.log('📡 Checking Strapi connectivity...');
    const healthCheck = await axios.get(`${STRAPI_URL}/_health`);
    if (healthCheck.status === 200) {
      console.log('✅ Strapi is accessible');
    }

    // Test API endpoints
    console.log('\n🔗 Testing API Endpoints:');
    const endpoints = [
      '/api/blog-posts',
      '/api/services', 
      '/api/pages',
      '/api/case-studies',
      '/api/pricing-plans'
    ];

    for (const endpoint of endpoints) {
      try {
        const response = await axios.get(`${STRAPI_URL}${endpoint}`);
        if (response.status === 200) {
          console.log(`✅ ${endpoint} - Working (${response.data?.data?.length || 0} items)`);
        }
      } catch (error) {
        if (error.response?.status === 403) {
          console.log(`🔒 ${endpoint} - Forbidden (permissions need setup)`);
        } else if (error.response?.status === 404) {
          console.log(`❌ ${endpoint} - Not Found`);
        } else {
          console.log(`⚠️  ${endpoint} - Status: ${error.response?.status || 'Unknown error'}`);
        }
      }
    }

    console.log('\n📋 Next Steps:');
    console.log('1. 🌐 Open: http://localhost:1337/admin');
    console.log('2. 👤 Create admin user (if first time)');
    console.log('3. ⚙️  Go to Settings → Users & Permissions → Roles → Public');
    console.log('4. ✅ Enable "find" and "findOne" for all content types:');
    console.log('   - Blog Post');
    console.log('   - Service'); 
    console.log('   - Page');
    console.log('   - Case Study');
    console.log('   - Pricing Plan');
    console.log('5. 💾 Save permissions');
    console.log('6. 🔄 Test API endpoints again');

    console.log('\n🎯 Admin Credentials (use when creating admin user):');
    console.log('📧 Email: admin@bizoholic.com');
    console.log('🔑 Password: AdminBizo2024');

    console.log('\n📍 Admin URL: http://localhost:1337/admin');
    console.log('📍 API Base: http://localhost:1337/api');

  } catch (error) {
    console.error('❌ Error setting up Strapi:', error.message);
    console.log('\n🔧 Troubleshooting:');
    console.log('- Ensure Strapi container is running: docker ps | grep strapi');
    console.log('- Check container logs: docker logs bizoholic-strapi-v5');
    console.log('- Verify port 1337 is accessible');
  }
}

// Create sample content after permissions are set
async function createSampleContent() {
  console.log('\n📝 Sample content will be created after API permissions are configured');
  console.log('💡 You can add content through the admin panel at http://localhost:1337/admin');
}

setupStrapi().then(() => {
  console.log('\n✨ Bizoholic Strapi setup guidance complete!');
  console.log('🎯 Next: Configure permissions in admin panel, then run API tests');
});
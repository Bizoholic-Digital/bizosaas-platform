const fetch = require('node-fetch');

const STRAPI_URL = 'http://localhost:1337';

// This script sets up API permissions for Strapi v5
async function setupPermissions() {
  console.log('🔧 Setting up Strapi API permissions...\n');

  try {
    // Check if Strapi is accessible
    const healthCheck = await fetch(`${STRAPI_URL}/_health`);
    if (!healthCheck.ok) {
      throw new Error('Strapi is not accessible');
    }
    console.log('✅ Strapi is accessible');

    // Check if public role permissions exist
    const permissionsResponse = await fetch(`${STRAPI_URL}/admin/users-permissions/roles`);
    
    if (permissionsResponse.ok) {
      const roles = await permissionsResponse.json();
      console.log('✅ Can access roles endpoint');
      console.log('📋 Found roles:', roles.map(r => r.name).join(', '));
    } else {
      console.log('ℹ️  Admin setup required first');
      console.log('📋 Manual Steps:');
      console.log('1. Open: http://localhost:1337/admin');
      console.log('2. Create admin user (first time)');
      console.log('3. Go to Settings → Users & Permissions → Roles → Public');
      console.log('4. Enable find and findOne for:');
      console.log('   - Blog Post');
      console.log('   - Service');
      console.log('   - Page');
      console.log('   - Case Study');
    }

    // Test API endpoints
    console.log('\n🔗 Testing API Endpoints:');
    
    const endpoints = [
      '/api/blog-posts',
      '/api/services', 
      '/api/pages',
      '/api/case-studies'
    ];

    for (const endpoint of endpoints) {
      try {
        const response = await fetch(`${STRAPI_URL}${endpoint}`);
        if (response.status === 403) {
          console.log(`❌ ${endpoint} - Forbidden (permissions not set)`);
        } else if (response.status === 200) {
          console.log(`✅ ${endpoint} - Working`);
        } else {
          console.log(`⚠️  ${endpoint} - Status: ${response.status}`);
        }
      } catch (error) {
        console.log(`❌ ${endpoint} - Error: ${error.message}`);
      }
    }

    console.log('\n📋 If all endpoints show "Forbidden", you need to:');
    console.log('1. Create admin user at: http://localhost:1337/admin');
    console.log('2. Set public permissions in admin panel');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

setupPermissions();
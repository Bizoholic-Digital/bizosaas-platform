#!/usr/bin/env node

/**
 * Script to populate Strapi with all the digital marketing services
 * This fixes the service cards display issue on the homepage
 */

const STRAPI_URL = 'http://localhost:1337';

// Digital Marketing Services that should be displayed on homepage
const digitalMarketingServices = [
  {
    title: 'SEO (Search Engine Optimization)',
    description: 'AI-powered keyword research, content optimization, and technical SEO combined with expert strategy to dominate search rankings.',
    icon: 'TrendingUp',
    badge: 'AI + Expert Based Solution',
    category: 'Search Marketing',
    platform: 'bizoholic'
  },
  {
    title: 'SEM (Search Engine Marketing)',
    description: 'Intelligent Google Ads and Bing Ads management with AI bid optimization and expert campaign strategy for maximum ROI.',
    icon: 'Target',
    badge: 'AI + Expert Based Solution',
    category: 'Paid Advertising',
    platform: 'bizoholic'
  },
  {
    title: 'Social Media Marketing',
    description: 'Automated content creation, posting schedules, and engagement strategies powered by AI with expert social media guidance.',
    icon: 'Users',
    badge: 'AI + Expert Based Solution',
    category: 'Social Media',
    platform: 'bizoholic'
  },
  {
    title: 'Social Media Optimization',
    description: 'AI-driven profile optimization, hashtag research, and engagement analysis combined with expert brand positioning.',
    icon: 'Zap',
    badge: 'AI + Expert Based Solution',
    category: 'Social Media',
    platform: 'bizoholic'
  },
  {
    title: 'Email Marketing',
    description: 'Intelligent email automation, personalization, and A/B testing powered by AI with expert copywriting and strategy.',
    icon: 'Bot',
    badge: 'AI + Expert Based Solution',
    category: 'Email Marketing',
    platform: 'bizoholic'
  },
  {
    title: 'Content Marketing',
    description: 'AI-generated content ideas, automated blog writing, and content optimization guided by expert content strategists.',
    icon: 'Lightbulb',
    badge: 'AI + Expert Based Solution',
    category: 'Content Strategy',
    platform: 'bizoholic'
  },
  {
    title: 'App Store Optimization',
    description: 'AI-powered ASO keyword research, app description optimization, and performance tracking with expert mobile marketing insights.',
    icon: 'BarChart',
    badge: 'AI + Expert Based Solution',
    category: 'Mobile Marketing',
    platform: 'bizoholic'
  }
];

// Function to create or update services in Strapi
async function createOrUpdateServices() {
  console.log('🚀 Setting up Strapi services...');
  
  try {
    // First, get existing services
    const existingResponse = await fetch(`${STRAPI_URL}/api/services`);
    const existingData = await existingResponse.json();
    const existingServices = existingData.data || [];
    
    console.log(`📊 Found ${existingServices.length} existing services`);
    
    // Create new services
    for (const service of digitalMarketingServices) {
      // Check if service already exists
      const existingService = existingServices.find(s => 
        s.title === service.title && s.platform === service.platform
      );
      
      if (existingService) {
        console.log(`⚠️  Service "${service.title}" already exists, updating...`);
        
        // Update existing service
        const updateResponse = await fetch(`${STRAPI_URL}/api/services/${existingService.documentId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            data: service
          })
        });
        
        if (updateResponse.ok) {
          console.log(`✅ Updated service: ${service.title}`);
        } else {
          console.error(`❌ Failed to update service: ${service.title}`);
          console.error(await updateResponse.text());
        }
      } else {
        console.log(`➕ Creating new service: ${service.title}...`);
        
        // Create new service
        const createResponse = await fetch(`${STRAPI_URL}/api/services`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            data: service
          })
        });
        
        if (createResponse.ok) {
          console.log(`✅ Created service: ${service.title}`);
        } else {
          console.error(`❌ Failed to create service: ${service.title}`);
          console.error(await createResponse.text());
        }
      }
    }
    
    // Verify the services were created
    console.log('\n🔍 Verifying services...');
    const verifyResponse = await fetch(`${STRAPI_URL}/api/services?filters[platform][$eq]=bizoholic`);
    const verifyData = await verifyResponse.json();
    const bizoServices = verifyData.data || [];
    
    console.log(`📊 Total bizoholic services in database: ${bizoServices.length}`);
    console.log('Services:');
    bizoServices.forEach((service, index) => {
      console.log(`  ${index + 1}. ${service.title} (${service.badge})`);
    });
    
    if (bizoServices.length >= 7) {
      console.log('\n🎉 Success! All services are now available in Strapi');
      console.log('💡 The homepage should now display all service cards properly');
    } else {
      console.log('\n⚠️  Warning: Expected 7 services but found', bizoServices.length);
    }
    
  } catch (error) {
    console.error('❌ Error setting up services:', error);
    console.error('Make sure Strapi is running on http://localhost:1337');
  }
}

// Function to check Strapi availability
async function checkStrapi() {
  try {
    const response = await fetch(`${STRAPI_URL}/api/services`, { method: 'HEAD' });
    return response.ok;
  } catch (error) {
    return false;
  }
}

// Main execution
async function main() {
  console.log('🔧 Bizoholic Digital Marketing Services Setup');
  console.log('==========================================\n');
  
  // Check if Strapi is available
  console.log('🔍 Checking Strapi availability...');
  const strapiAvailable = await checkStrapi();
  
  if (!strapiAvailable) {
    console.error('❌ Strapi is not available at http://localhost:1337');
    console.error('Please make sure Strapi is running before running this script.');
    console.error('You can start Strapi with: npm run dev or docker-compose up strapi');
    process.exit(1);
  }
  
  console.log('✅ Strapi is available');
  console.log('');
  
  await createOrUpdateServices();
  
  console.log('\n🏁 Setup complete!');
  console.log('📱 Refresh your homepage at http://localhost:3001 to see the changes');
}

// Run the script
main().catch(error => {
  console.error('💥 Script failed:', error);
  process.exit(1);
});
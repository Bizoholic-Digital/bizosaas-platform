const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');

const STRAPI_URL = 'http://localhost:1337';

// Simple content type schemas for Strapi v5
const contentTypeSchemas = {
  'blog-post': {
    "kind": "collectionType",
    "collectionName": "blog_posts",
    "info": {
      "singularName": "blog-post",
      "pluralName": "blog-posts", 
      "displayName": "Blog Post"
    },
    "options": {
      "draftAndPublish": true
    },
    "attributes": {
      "title": {
        "type": "string",
        "required": true
      },
      "content": {
        "type": "richtext"
      },
      "excerpt": {
        "type": "text"
      },
      "author": {
        "type": "string"
      },
      "publishDate": {
        "type": "date"
      },
      "category": {
        "type": "string"
      },
      "platform": {
        "type": "enumeration",
        "enum": ["bizoholic", "coreldove", "both"],
        "default": "both"
      },
      "featured": {
        "type": "boolean",
        "default": false
      }
    }
  },
  
  'service': {
    "kind": "collectionType",
    "collectionName": "services",
    "info": {
      "singularName": "service",
      "pluralName": "services",
      "displayName": "Service"
    },
    "options": {
      "draftAndPublish": true
    },
    "attributes": {
      "title": {
        "type": "string",
        "required": true
      },
      "description": {
        "type": "text",
        "required": true
      },
      "icon": {
        "type": "string"
      },
      "badge": {
        "type": "string"
      },
      "category": {
        "type": "string"
      },
      "platform": {
        "type": "enumeration", 
        "enum": ["bizoholic", "coreldove", "both"],
        "default": "both"
      }
    }
  },
  
  'page': {
    "kind": "collectionType", 
    "collectionName": "pages",
    "info": {
      "singularName": "page",
      "pluralName": "pages",
      "displayName": "Page"
    },
    "options": {
      "draftAndPublish": true
    },
    "attributes": {
      "title": {
        "type": "string",
        "required": true
      },
      "content": {
        "type": "richtext"
      },
      "metaDescription": {
        "type": "text"
      },
      "platform": {
        "type": "enumeration",
        "enum": ["bizoholic", "coreldove", "both"],
        "default": "both"
      }
    }
  },
  
  'case-study': {
    "kind": "collectionType",
    "collectionName": "case_studies", 
    "info": {
      "singularName": "case-study",
      "pluralName": "case-studies",
      "displayName": "Case Study"
    },
    "options": {
      "draftAndPublish": true
    },
    "attributes": {
      "title": {
        "type": "string",
        "required": true
      },
      "client": {
        "type": "string"
      },
      "industry": {
        "type": "string"
      },
      "challenge": {
        "type": "text"
      },
      "solution": {
        "type": "richtext"
      },
      "results": {
        "type": "text"
      },
      "metrics": {
        "type": "json"
      },
      "platform": {
        "type": "enumeration",
        "enum": ["bizoholic", "coreldove", "both"],
        "default": "both"
      }
    }
  }
};

async function createContentTypeFiles() {
  console.log('📁 Creating Strapi v5 content type files...\n');

  const strapiApiPath = '/home/alagiri/projects/bizoholic/bizosaas/strapi-v5/src/api';

  for (const [contentType, schema] of Object.entries(contentTypeSchemas)) {
    const apiPath = path.join(strapiApiPath, contentType);
    const contentTypesPath = path.join(apiPath, 'content-types', contentType);
    const controllersPath = path.join(apiPath, 'controllers');
    const servicesPath = path.join(apiPath, 'services');
    const routesPath = path.join(apiPath, 'routes');

    try {
      // Create directories
      await fs.mkdir(contentTypesPath, { recursive: true });
      await fs.mkdir(controllersPath, { recursive: true });
      await fs.mkdir(servicesPath, { recursive: true });
      await fs.mkdir(routesPath, { recursive: true });

      // Create schema.json
      await fs.writeFile(
        path.join(contentTypesPath, 'schema.json'),
        JSON.stringify(schema, null, 2)
      );

      // Create controller
      await fs.writeFile(
        path.join(controllersPath, `${contentType}.ts`),
        `import { factories } from '@strapi/strapi';\n\nexport default factories.createCoreController('api::${contentType}.${contentType}');`
      );

      // Create service  
      await fs.writeFile(
        path.join(servicesPath, `${contentType}.ts`),
        `import { factories } from '@strapi/strapi';\n\nexport default factories.createCoreService('api::${contentType}.${contentType}');`
      );

      // Create routes
      await fs.writeFile(
        path.join(routesPath, `${contentType}.ts`),
        `import { factories } from '@strapi/strapi';\n\nexport default factories.createCoreRouter('api::${contentType}.${contentType}');`
      );

      console.log(`✅ Created ${contentType} content type`);
    } catch (error) {
      console.error(`❌ Error creating ${contentType}:`, error.message);
    }
  }

  console.log('\n🎉 Content type files created successfully!');
  console.log('\n📋 Next steps:');
  console.log('1. Restart your Strapi container');
  console.log('2. Access the admin panel at http://localhost:1337/admin');
  console.log('3. Set up API permissions for public access');
  console.log('4. Add sample content through the admin interface');
}

async function createSampleData() {
  console.log('📝 Creating sample data...\n');

  const sampleData = {
    'blog-posts': [
      {
        data: {
          title: "The Future of AI Marketing: Trends to Watch in 2025",
          content: "# The Future of AI Marketing\\n\\nArtificial Intelligence is revolutionizing the marketing landscape...",
          excerpt: "Discover the key AI marketing trends that will dominate 2025 and how your business can stay ahead of the curve.",
          author: "Marketing Team",
          publishDate: new Date().toISOString().split('T')[0],
          category: "AI & Technology",
          platform: "both",
          featured: true
        }
      }
    ],
    'services': [
      {
        data: {
          title: "AI-Powered Marketing Automation",
          description: "Transform your marketing campaigns with cutting-edge AI technology. Our automated systems optimize ad spend, personalize content, and increase conversion rates by up to 300%.",
          icon: "Bot",
          badge: "Most Popular",
          category: "Marketing Automation",
          platform: "bizoholic"
        }
      },
      {
        data: {
          title: "E-commerce Growth Optimization", 
          description: "Boost your online store's performance with our comprehensive e-commerce solutions. From product optimization to conversion funnel analysis.",
          icon: "TrendingUp",
          badge: "New",
          category: "E-commerce",
          platform: "coreldove"
        }
      }
    ],
    'pages': [
      {
        data: {
          title: "About Us",
          content: "# About Our Marketing Agency\\n\\nWe are a cutting-edge marketing agency specializing in AI-powered solutions for modern businesses...",
          metaDescription: "Learn about our AI-powered marketing agency and how we help businesses grow through innovative digital solutions.",
          platform: "both"
        }
      }
    ],
    'case-studies': [
      {
        data: {
          title: "E-commerce Revenue Boost: 450% ROI in 6 Months",
          client: "TechGear Solutions",
          industry: "E-commerce Technology", 
          challenge: "TechGear Solutions was struggling with low conversion rates and high customer acquisition costs despite having quality products.",
          solution: "# Our Comprehensive Solution\\n\\n## Strategy Implementation\\n- AI-powered product recommendation engine\\n- Personalized email marketing campaigns",
          results: "Achieved 450% ROI within 6 months, reduced customer acquisition cost by 60%, and increased average order value by 85%.",
          metrics: {
            roi: "450%",
            conversionIncrease: "240%",
            costReduction: "60%",
            revenueGrowth: "320%"
          },
          platform: "both"
        }
      }
    ]
  };

  for (const [endpoint, items] of Object.entries(sampleData)) {
    for (const item of items) {
      try {
        const response = await axios.post(`${STRAPI_URL}/api/${endpoint}`, item, {
          headers: { 'Content-Type': 'application/json' }
        });
        console.log(`✅ Created sample ${endpoint} entry`);
      } catch (error) {
        console.log(`❌ Error creating ${endpoint} sample: ${error.response?.data?.error?.message || error.message}`);
      }
    }
  }
}

async function waitForStrapi() {
  console.log('⏳ Waiting for Strapi to be ready...');
  
  for (let i = 0; i < 30; i++) {
    try {
      await axios.get(STRAPI_URL);
      console.log('✅ Strapi is ready!');
      return true;
    } catch (error) {
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }
  
  console.log('❌ Strapi is not responding');
  return false;
}

async function main() {
  console.log('🚀 Strapi v5 Content Types Setup\n');

  // Create content type files
  await createContentTypeFiles();
  
  console.log('\n⚠️  Please restart your Strapi container now and then run this script again with --sample-data flag to add sample content\n');
  
  if (process.argv.includes('--sample-data')) {
    if (await waitForStrapi()) {
      await createSampleData();
    }
  }
}

if (require.main === module) {
  main().catch(console.error);
}
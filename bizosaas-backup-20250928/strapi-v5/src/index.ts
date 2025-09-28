export default {
  /**
   * An asynchronous register function that runs before
   * your application is initialized.
   *
   * This gives you an opportunity to extend code.
   */
  register(/*{ strapi }*/) {},

  /**
   * An asynchronous bootstrap function that runs before
   * your application gets started.
   *
   * This gives you an opportunity to set up your data model,
   * run jobs, or perform some special logic.
   */
  async bootstrap({ strapi }) {
    console.log('🚀 Starting Strapi bootstrap process...');
    
    // Skip permission setup for now - will be done manually in admin
    console.log('ℹ️  Permissions will be set up manually in admin panel');

    // Add sample data if collections are empty
    try {
      // Sample blog post
      const blogPostCount = await strapi.entityService.count('api::blog-post.blog-post');
      if (blogPostCount === 0) {
        await strapi.entityService.create('api::blog-post.blog-post', {
          data: {
            title: "The Future of AI Marketing: Trends to Watch in 2025",
            slug: "future-ai-marketing-trends-2025",
            content: "# The Future of AI Marketing\n\nArtificial Intelligence is revolutionizing the marketing landscape. Here's what you need to know about the upcoming trends that will shape the industry in 2025.\n\n## Key Trends\n\n1. **Personalized Content at Scale**\n2. **Predictive Analytics for Customer Behavior**\n3. **AI-Powered Chatbots and Customer Service**\n4. **Automated Campaign Optimization**\n\nThese developments will fundamentally change how businesses connect with their customers.",
            excerpt: "Discover the key AI marketing trends that will dominate 2025 and how your business can stay ahead of the curve.",
            author: "Marketing Team",
            publishDate: new Date(),
            category: "AI & Technology",
            platform: "both",
            featured: true,
            publishedAt: new Date()
          }
        });
        console.log('✅ Sample blog post created');
      }

      // Sample service
      const serviceCount = await strapi.entityService.count('api::service.service');
      if (serviceCount === 0) {
        await strapi.entityService.create('api::service.service', {
          data: {
            title: "AI-Powered Marketing Automation",
            description: "Transform your marketing campaigns with cutting-edge AI technology. Our automated systems optimize ad spend, personalize content, and increase conversion rates by up to 300%.",
            icon: "Bot",
            badge: "Most Popular",
            category: "Marketing Automation",
            platform: "bizoholic",
            publishedAt: new Date()
          }
        });

        await strapi.entityService.create('api::service.service', {
          data: {
            title: "E-commerce Growth Optimization",
            description: "Boost your online store's performance with our comprehensive e-commerce solutions. From product optimization to conversion funnel analysis.",
            icon: "TrendingUp",
            badge: "New",
            category: "E-commerce",
            platform: "coreldove",
            publishedAt: new Date()
          }
        });
        console.log('✅ Sample services created');
      }

      // Sample page
      const pageCount = await strapi.entityService.count('api::page.page');
      if (pageCount === 0) {
        await strapi.entityService.create('api::page.page', {
          data: {
            title: "About Us",
            slug: "about-us",
            content: "# About Our Marketing Agency\n\nWe are a cutting-edge marketing agency specializing in AI-powered solutions for modern businesses. Our team combines creativity with data-driven insights to deliver exceptional results.\n\n## Our Mission\n\nTo revolutionize digital marketing through innovative AI solutions that drive real business growth.\n\n## Our Values\n\n- Innovation\n- Transparency\n- Results-driven approach\n- Client success",
            metaDescription: "Learn about our AI-powered marketing agency and how we help businesses grow through innovative digital solutions.",
            platform: "both",
            publishedAt: new Date()
          }
        });
        console.log('✅ Sample page created');
      }

      // Sample case study
      const caseStudyCount = await strapi.entityService.count('api::case-study.case-study');
      if (caseStudyCount === 0) {
        await strapi.entityService.create('api::case-study.case-study', {
          data: {
            title: "E-commerce Revenue Boost: 450% ROI in 6 Months",
            client: "TechGear Solutions",
            industry: "E-commerce Technology",
            challenge: "TechGear Solutions was struggling with low conversion rates and high customer acquisition costs despite having quality products.",
            solution: "# Our Comprehensive Solution\n\n## Strategy Implementation\n- AI-powered product recommendation engine\n- Personalized email marketing campaigns\n- Conversion funnel optimization\n- Retargeting campaigns\n\n## Technologies Used\n- Machine learning algorithms\n- Advanced analytics\n- A/B testing frameworks",
            results: "Achieved 450% ROI within 6 months, reduced customer acquisition cost by 60%, and increased average order value by 85%.",
            metrics: {
              roi: "450%",
              conversionIncrease: "240%",
              costReduction: "60%",
              revenueGrowth: "320%",
              customerSatisfaction: "95%"
            },
            platform: "both",
            publishedAt: new Date()
          }
        });
        console.log('✅ Sample case study created');
      }

    } catch (error) {
      console.error('Error creating sample data:', error);
    }

    console.log('🚀 Strapi bootstrap completed successfully!');
  },
};
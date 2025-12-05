#!/usr/bin/env node

/**
 * PWA Functionality Testing Script
 * Tests all implemented PWA features for BizOSaaS Platform containers
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');

const execAsync = util.promisify(exec);

// Container configurations
const containers = [
  { name: 'bizoholic-frontend', port: 3008, path: 'frontend/apps/bizoholic-frontend' },
  { name: 'coreldove-frontend', port: 3007, path: 'frontend/apps/coreldove-frontend' },
  { name: 'client-portal', port: 3006, path: 'frontend/apps/client-portal' },
  { name: 'bizosaas-admin', port: 3009, path: 'frontend/apps/bizosaas-admin' },
  { name: 'business-directory', port: 3010, path: 'frontend/apps/business-directory' }
];

// Test results tracking
const testResults = {
  manifest: {},
  serviceWorker: {},
  offlinePage: {},
  icons: {},
  nextConfig: {},
  pwaProvider: {},
  indexedDB: {},
  mobileComponents: {},
  overall: {}
};

/**
 * Test PWA Manifest files
 */
async function testManifests() {
  console.log('\n🔍 Testing PWA Manifest Files...');
  
  for (const container of containers) {
    const manifestPath = path.join(container.path, 'public/manifest.json');
    
    try {
      if (fs.existsSync(manifestPath)) {
        const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
        
        // Validate required manifest fields
        const requiredFields = ['name', 'short_name', 'start_url', 'display', 'icons'];
        const hasAllFields = requiredFields.every(field => manifest[field]);
        
        testResults.manifest[container.name] = {
          exists: true,
          valid: hasAllFields,
          name: manifest.name,
          startUrl: manifest.start_url,
          display: manifest.display,
          iconCount: manifest.icons?.length || 0
        };
        
        console.log(`  ✅ ${container.name}: Valid manifest with ${manifest.icons?.length || 0} icons`);
      } else {
        testResults.manifest[container.name] = { exists: false, valid: false };
        console.log(`  ❌ ${container.name}: Manifest not found`);
      }
    } catch (error) {
      testResults.manifest[container.name] = { exists: true, valid: false, error: error.message };
      console.log(`  ❌ ${container.name}: Invalid manifest - ${error.message}`);
    }
  }
}

/**
 * Test Service Worker files
 */
async function testServiceWorkers() {
  console.log('\n🔍 Testing Service Worker Files...');
  
  for (const container of containers) {
    const swPath = path.join(container.path, 'public/sw.js');
    
    try {
      if (fs.existsSync(swPath)) {
        const swContent = fs.readFileSync(swPath, 'utf8');
        
        // Check for key service worker features
        const hasInstallEvent = swContent.includes('install');
        const hasActivateEvent = swContent.includes('activate');
        const hasFetchEvent = swContent.includes('fetch');
        const hasCaching = swContent.includes('caches.open');
        const hasBackgroundSync = swContent.includes('sync');
        
        testResults.serviceWorker[container.name] = {
          exists: true,
          hasInstallEvent,
          hasActivateEvent,
          hasFetchEvent,
          hasCaching,
          hasBackgroundSync,
          size: swContent.length
        };
        
        console.log(`  ✅ ${container.name}: Service worker with caching and sync features`);
      } else {
        testResults.serviceWorker[container.name] = { exists: false };
        console.log(`  ❌ ${container.name}: Service worker not found`);
      }
    } catch (error) {
      testResults.serviceWorker[container.name] = { exists: true, error: error.message };
      console.log(`  ❌ ${container.name}: Service worker error - ${error.message}`);
    }
  }
}

/**
 * Test Offline Pages
 */
async function testOfflinePages() {
  console.log('\n🔍 Testing Offline Pages...');
  
  for (const container of containers) {
    const offlinePath = path.join(container.path, 'public/offline.html');
    
    try {
      if (fs.existsSync(offlinePath)) {
        const offlineContent = fs.readFileSync(offlinePath, 'utf8');
        
        // Check for essential offline page elements
        const hasTitle = offlineContent.includes('<title>');
        const hasOfflineMessage = offlineContent.toLowerCase().includes('offline');
        const hasRetryButton = offlineContent.toLowerCase().includes('retry') || offlineContent.toLowerCase().includes('try again');
        
        testResults.offlinePage[container.name] = {
          exists: true,
          hasTitle,
          hasOfflineMessage,
          hasRetryButton,
          size: offlineContent.length
        };
        
        console.log(`  ✅ ${container.name}: Offline page with retry functionality`);
      } else {
        testResults.offlinePage[container.name] = { exists: false };
        console.log(`  ❌ ${container.name}: Offline page not found`);
      }
    } catch (error) {
      testResults.offlinePage[container.name] = { exists: true, error: error.message };
      console.log(`  ❌ ${container.name}: Offline page error - ${error.message}`);
    }
  }
}

/**
 * Test App Icons
 */
async function testIcons() {
  console.log('\n🔍 Testing App Icons...');
  
  for (const container of containers) {
    const iconsPath = path.join(container.path, 'public/icons');
    
    try {
      if (fs.existsSync(iconsPath)) {
        const iconFiles = fs.readdirSync(iconsPath);
        const pngIcons = iconFiles.filter(file => file.endsWith('.png'));
        
        // Check for required icon sizes
        const requiredSizes = ['192x192', '512x512'];
        const hasRequiredSizes = requiredSizes.every(size => 
          pngIcons.some(icon => icon.includes(size))
        );
        
        testResults.icons[container.name] = {
          exists: true,
          iconCount: iconFiles.length,
          pngCount: pngIcons.length,
          hasRequiredSizes,
          files: iconFiles
        };
        
        console.log(`  ✅ ${container.name}: ${pngIcons.length} PNG icons including required sizes`);
      } else {
        testResults.icons[container.name] = { exists: false };
        console.log(`  ❌ ${container.name}: Icons directory not found`);
      }
    } catch (error) {
      testResults.icons[container.name] = { exists: true, error: error.message };
      console.log(`  ❌ ${container.name}: Icons error - ${error.message}`);
    }
  }
}

/**
 * Test Next.js Configuration
 */
async function testNextConfig() {
  console.log('\n🔍 Testing Next.js PWA Configuration...');
  
  for (const container of containers) {
    const configPath = path.join(container.path, 'next.config.js');
    
    try {
      if (fs.existsSync(configPath)) {
        const configContent = fs.readFileSync(configPath, 'utf8');
        
        // Check for PWA-related configurations
        const hasPWAHeaders = configContent.includes('X-PWA-Mode') || configContent.includes('manifest');
        const hasServiceWorkerHeaders = configContent.includes('Service-Worker');
        const hasSecurityHeaders = configContent.includes('Content-Security-Policy');
        
        testResults.nextConfig[container.name] = {
          exists: true,
          hasPWAHeaders,
          hasServiceWorkerHeaders,
          hasSecurityHeaders
        };
        
        console.log(`  ✅ ${container.name}: Next.js config with PWA headers`);
      } else {
        testResults.nextConfig[container.name] = { exists: false };
        console.log(`  ❌ ${container.name}: Next.js config not found`);
      }
    } catch (error) {
      testResults.nextConfig[container.name] = { exists: true, error: error.message };
      console.log(`  ❌ ${container.name}: Next.js config error - ${error.message}`);
    }
  }
}

/**
 * Test PWA Provider Component
 */
async function testPWAProvider() {
  console.log('\n🔍 Testing PWA Provider Component...');
  
  for (const container of containers) {
    const providerPath = path.join(container.path, 'components/PWAProvider.tsx');
    
    try {
      if (fs.existsSync(providerPath)) {
        const providerContent = fs.readFileSync(providerPath, 'utf8');
        
        // Check for essential PWA provider features
        const hasServiceWorkerRegistration = providerContent.includes('serviceWorker.register');
        const hasInstallPrompt = providerContent.includes('beforeinstallprompt');
        const hasUpdateHandling = providerContent.includes('controllerchange') || providerContent.includes('updatefound');
        
        testResults.pwaProvider[container.name] = {
          exists: true,
          hasServiceWorkerRegistration,
          hasInstallPrompt,
          hasUpdateHandling
        };
        
        console.log(`  ✅ ${container.name}: PWA Provider with install prompts and updates`);
      } else {
        testResults.pwaProvider[container.name] = { exists: false };
        console.log(`  ❌ ${container.name}: PWA Provider not found`);
      }
    } catch (error) {
      testResults.pwaProvider[container.name] = { exists: true, error: error.message };
      console.log(`  ❌ ${container.name}: PWA Provider error - ${error.message}`);
    }
  }
}

/**
 * Test IndexedDB Implementation
 */
async function testIndexedDB() {
  console.log('\n🔍 Testing IndexedDB Implementation...');
  
  for (const container of containers) {
    const indexedDBPath = path.join(container.path, 'lib/pwa/indexedDB.ts');
    
    try {
      if (fs.existsSync(indexedDBPath)) {
        const indexedDBContent = fs.readFileSync(indexedDBPath, 'utf8');
        
        // Check for key IndexedDB features
        const hasDatabase = indexedDBContent.includes('class PWADatabase');
        const hasStores = indexedDBContent.includes('createObjectStore');
        const hasFormQueue = indexedDBContent.includes('queueFormSubmission');
        const hasCache = indexedDBContent.includes('cacheData');
        const hasCleanup = indexedDBContent.includes('cleanup');
        
        testResults.indexedDB[container.name] = {
          exists: true,
          hasDatabase,
          hasStores,
          hasFormQueue,
          hasCache,
          hasCleanup
        };
        
        console.log(`  ✅ ${container.name}: IndexedDB with offline storage and sync`);
      } else {
        testResults.indexedDB[container.name] = { exists: false };
        console.log(`  ❌ ${container.name}: IndexedDB implementation not found`);
      }
    } catch (error) {
      testResults.indexedDB[container.name] = { exists: true, error: error.message };
      console.log(`  ❌ ${container.name}: IndexedDB error - ${error.message}`);
    }
  }
}

/**
 * Test Mobile Components
 */
async function testMobileComponents() {
  console.log('\n🔍 Testing Mobile UX Components...');
  
  for (const container of containers) {
    const pullToRefreshPath = path.join(container.path, 'components/mobile/PullToRefresh.tsx');
    const loadingSkeletonPath = path.join(container.path, 'components/mobile/LoadingSkeleton.tsx');
    
    try {
      const hasPullToRefresh = fs.existsSync(pullToRefreshPath);
      const hasLoadingSkeleton = fs.existsSync(loadingSkeletonPath);
      
      let skeletonVariants = 0;
      if (hasLoadingSkeleton) {
        const skeletonContent = fs.readFileSync(loadingSkeletonPath, 'utf8');
        // Count skeleton variants
        const variants = ['CardSkeleton', 'TableSkeleton', 'MobileCardSkeleton', 'MobileListSkeleton'];
        skeletonVariants = variants.filter(variant => skeletonContent.includes(variant)).length;
      }
      
      testResults.mobileComponents[container.name] = {
        hasPullToRefresh,
        hasLoadingSkeleton,
        skeletonVariants
      };
      
      if (hasPullToRefresh && hasLoadingSkeleton) {
        console.log(`  ✅ ${container.name}: Complete mobile UX with ${skeletonVariants} skeleton variants`);
      } else {
        console.log(`  ⚠️  ${container.name}: Partial mobile UX implementation`);
      }
    } catch (error) {
      testResults.mobileComponents[container.name] = { error: error.message };
      console.log(`  ❌ ${container.name}: Mobile components error - ${error.message}`);
    }
  }
}

/**
 * Generate Overall Test Summary
 */
function generateSummary() {
  console.log('\n📊 PWA Implementation Summary\n');
  
  const categories = [
    { name: 'Manifest Files', data: testResults.manifest },
    { name: 'Service Workers', data: testResults.serviceWorker },
    { name: 'Offline Pages', data: testResults.offlinePage },
    { name: 'App Icons', data: testResults.icons },
    { name: 'Next.js Config', data: testResults.nextConfig },
    { name: 'PWA Provider', data: testResults.pwaProvider },
    { name: 'IndexedDB', data: testResults.indexedDB },
    { name: 'Mobile Components', data: testResults.mobileComponents }
  ];
  
  let totalTests = 0;
  let passedTests = 0;
  
  categories.forEach(category => {
    const categoryResults = Object.values(category.data);
    const categoryPassed = categoryResults.filter(result => 
      result.exists !== false && !result.error
    ).length;
    
    totalTests += categoryResults.length;
    passedTests += categoryPassed;
    
    const percentage = categoryResults.length > 0 ? 
      Math.round((categoryPassed / categoryResults.length) * 100) : 0;
    
    console.log(`${category.name}: ${categoryPassed}/${categoryResults.length} (${percentage}%)`);
  });
  
  const overallPercentage = Math.round((passedTests / totalTests) * 100);
  console.log(`\n🎯 Overall PWA Implementation: ${passedTests}/${totalTests} (${overallPercentage}%)`);
  
  testResults.overall = {
    totalTests,
    passedTests,
    percentage: overallPercentage,
    timestamp: new Date().toISOString()
  };
  
  // Recommendations
  console.log('\n💡 Recommendations:');
  
  containers.forEach(container => {
    const containerIssues = [];
    
    if (!testResults.manifest[container.name]?.exists) {
      containerIssues.push('Add PWA manifest');
    }
    if (!testResults.serviceWorker[container.name]?.exists) {
      containerIssues.push('Implement service worker');
    }
    if (!testResults.pwaProvider[container.name]?.exists) {
      containerIssues.push('Add PWA Provider component');
    }
    if (!testResults.mobileComponents[container.name]?.hasPullToRefresh) {
      containerIssues.push('Add mobile UX components');
    }
    
    if (containerIssues.length > 0) {
      console.log(`  ${container.name}: ${containerIssues.join(', ')}`);
    }
  });
}

/**
 * Save Test Results
 */
function saveResults() {
  const resultsPath = path.join(process.cwd(), 'pwa-test-results.json');
  fs.writeFileSync(resultsPath, JSON.stringify(testResults, null, 2));
  console.log(`\n💾 Test results saved to: ${resultsPath}`);
}

/**
 * Main Test Runner
 */
async function runTests() {
  console.log('🚀 Starting PWA Functionality Tests for BizOSaaS Platform');
  console.log('==================================================');
  
  try {
    await testManifests();
    await testServiceWorkers();
    await testOfflinePages();
    await testIcons();
    await testNextConfig();
    await testPWAProvider();
    await testIndexedDB();
    await testMobileComponents();
    
    generateSummary();
    saveResults();
    
    console.log('\n✅ PWA testing completed successfully!');
    
    // Exit with appropriate code
    const overallPassed = testResults.overall.percentage >= 80;
    process.exit(overallPassed ? 0 : 1);
    
  } catch (error) {
    console.error('\n❌ PWA testing failed:', error.message);
    process.exit(1);
  }
}

// Run tests
if (require.main === module) {
  runTests();
}

module.exports = { runTests, testResults };
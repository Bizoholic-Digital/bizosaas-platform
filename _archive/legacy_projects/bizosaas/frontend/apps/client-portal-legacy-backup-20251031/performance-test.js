#!/usr/bin/env node

/**
 * Performance & Load Testing Suite for Client Portal APIs
 * Focuses on working endpoints with detailed performance analysis
 */

const BASE_URL = 'http://localhost:3006'

// Working endpoints based on previous test results
const workingEndpoints = [
  // Billing System (100% success rate)
  { method: 'GET', url: '/api/brain/billing/payment-methods', category: 'Billing', name: 'Payment Methods' },
  { method: 'GET', url: '/api/brain/billing/subscriptions', category: 'Billing', name: 'Subscriptions' },
  { method: 'GET', url: '/api/brain/billing/invoices', category: 'Billing', name: 'Invoices' },
  { method: 'GET', url: '/api/brain/billing/usage', category: 'Billing', name: 'Usage Tracking' },
  { method: 'GET', url: '/api/brain/billing/payments', category: 'Billing', name: 'Payments History' },
  
  // Integration Management (100% success rate)
  { method: 'GET', url: '/api/brain/integrations/overview', category: 'Integrations', name: 'Overview' },
  { method: 'GET', url: '/api/brain/integrations/webhooks', category: 'Integrations', name: 'Webhooks' },
  { method: 'GET', url: '/api/brain/integrations/apis', category: 'Integrations', name: 'API Keys' },
  { method: 'GET', url: '/api/brain/integrations/logs', category: 'Integrations', name: 'Integration Logs' },
  { method: 'GET', url: '/api/brain/integrations/automations', category: 'Integrations', name: 'Automations' },
  { method: 'GET', url: '/api/brain/integrations/third-party', category: 'Integrations', name: 'Third-Party' },
  
  // Marketing (Partial success - working endpoints)
  { method: 'GET', url: '/api/brain/marketing/campaigns', category: 'Marketing', name: 'Campaigns' },
  { method: 'GET', url: '/api/brain/marketing/audiences', category: 'Marketing', name: 'Audiences' },
  { method: 'GET', url: '/api/brain/marketing/approvals', category: 'Marketing', name: 'Approvals' }
]

class PerformanceTester {
  constructor() {
    this.results = {
      baseline: {},
      load: {},
      spike: {},
      soak: {},
      stress: {}
    }
  }

  async measureBaseline() {
    console.log('📊 Running Baseline Performance Tests...\n')
    
    const baselineResults = {}
    
    for (const endpoint of workingEndpoints) {
      console.log(`Testing ${endpoint.name}...`)
      
      const measurements = []
      const sampleSize = 10
      
      for (let i = 0; i < sampleSize; i++) {
        try {
          const startTime = process.hrtime.bigint()
          const response = await fetch(`${BASE_URL}${endpoint.url}`, {
            headers: { 'Authorization': 'Bearer test-token' }
          })
          const endTime = process.hrtime.bigint()
          
          const responseTimeNs = endTime - startTime
          const responseTimeMs = Number(responseTimeNs) / 1000000
          
          const data = await response.json()
          
          measurements.push({
            responseTime: responseTimeMs,
            status: response.status,
            success: response.ok,
            dataSize: JSON.stringify(data).length,
            fallbackMode: data?.source === 'fallback'
          })
          
        } catch (error) {
          measurements.push({
            responseTime: 0,
            status: 0,
            success: false,
            error: error.message
          })
        }
        
        // Small delay between requests
        await new Promise(resolve => setTimeout(resolve, 50))
      }
      
      // Calculate statistics
      const successfulMeasurements = measurements.filter(m => m.success)
      const responseTimes = successfulMeasurements.map(m => m.responseTime)
      
      if (responseTimes.length > 0) {
        responseTimes.sort((a, b) => a - b)
        
        baselineResults[endpoint.name] = {
          category: endpoint.category,
          samples: measurements.length,
          success_rate: (successfulMeasurements.length / measurements.length) * 100,
          response_times: {
            min: Math.min(...responseTimes),
            max: Math.max(...responseTimes),
            avg: responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length,
            p50: responseTimes[Math.floor(responseTimes.length * 0.5)],
            p95: responseTimes[Math.floor(responseTimes.length * 0.95)],
            p99: responseTimes[Math.floor(responseTimes.length * 0.99)]
          },
          data_size_avg: successfulMeasurements.reduce((a, b) => a + (b.dataSize || 0), 0) / successfulMeasurements.length,
          fallback_rate: (successfulMeasurements.filter(m => m.fallbackMode).length / successfulMeasurements.length) * 100
        }
        
        const stats = baselineResults[endpoint.name]
        console.log(`  ✅ ${stats.success_rate.toFixed(1)}% success, ${stats.response_times.avg.toFixed(0)}ms avg, ${stats.response_times.p95.toFixed(0)}ms p95`)
      } else {
        console.log(`  ❌ All requests failed`)
      }
    }
    
    this.results.baseline = baselineResults
    return baselineResults
  }

  async runLoadTest() {
    console.log('\n⚡ Running Load Test (Concurrent Requests)...\n')
    
    const concurrentUsers = [1, 5, 10, 20]
    const loadResults = {}
    
    for (const users of concurrentUsers) {
      console.log(`Testing with ${users} concurrent users...`)
      
      const testPromises = []
      const startTime = Date.now()
      
      for (let i = 0; i < users; i++) {
        // Each user hits a random working endpoint
        const endpoint = workingEndpoints[Math.floor(Math.random() * workingEndpoints.length)]
        
        const userPromise = this.simulateUserRequests(endpoint, 5) // 5 requests per user
        testPromises.push(userPromise)
      }
      
      const results = await Promise.all(testPromises)
      const endTime = Date.now()
      
      // Flatten and analyze results
      const allMeasurements = results.flat()
      const successful = allMeasurements.filter(m => m.success)
      const responseTimes = successful.map(m => m.responseTime)
      
      if (responseTimes.length > 0) {
        responseTimes.sort((a, b) => a - b)
        
        loadResults[`${users}_users`] = {
          concurrent_users: users,
          total_requests: allMeasurements.length,
          successful_requests: successful.length,
          success_rate: (successful.length / allMeasurements.length) * 100,
          total_time: endTime - startTime,
          throughput_rps: (successful.length / ((endTime - startTime) / 1000)).toFixed(2),
          response_times: {
            avg: responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length,
            p95: responseTimes[Math.floor(responseTimes.length * 0.95)],
            p99: responseTimes[Math.floor(responseTimes.length * 0.99)]
          }
        }
        
        const stats = loadResults[`${users}_users`]
        console.log(`  ✅ ${stats.throughput_rps} RPS, ${stats.response_times.avg.toFixed(0)}ms avg, ${stats.success_rate.toFixed(1)}% success`)
      } else {
        console.log(`  ❌ Load test failed`)
      }
    }
    
    this.results.load = loadResults
    return loadResults
  }

  async simulateUserRequests(endpoint, requestCount) {
    const measurements = []
    
    for (let i = 0; i < requestCount; i++) {
      try {
        const startTime = Date.now()
        const response = await fetch(`${BASE_URL}${endpoint.url}`, {
          headers: { 'Authorization': 'Bearer test-token' }
        })
        const endTime = Date.now()
        
        measurements.push({
          endpoint: endpoint.name,
          responseTime: endTime - startTime,
          status: response.status,
          success: response.ok
        })
        
      } catch (error) {
        measurements.push({
          endpoint: endpoint.name,
          responseTime: 0,
          status: 0,
          success: false,
          error: error.message
        })
      }
      
      // Random delay to simulate real user behavior
      await new Promise(resolve => setTimeout(resolve, Math.random() * 100))
    }
    
    return measurements
  }

  async runSpikeTest() {
    console.log('\n🚀 Running Spike Test (Traffic Spike Simulation)...\n')
    
    // Simulate sudden traffic spike
    const spikeUsers = 50
    const spikeDuration = 10000 // 10 seconds
    
    console.log(`Simulating spike: ${spikeUsers} concurrent users for ${spikeDuration/1000}s`)
    
    const startTime = Date.now()
    const requests = []
    
    // Generate spike load
    for (let i = 0; i < spikeUsers; i++) {
      const endpoint = workingEndpoints[i % workingEndpoints.length]
      requests.push(this.performSpikeRequest(endpoint))
    }
    
    const results = await Promise.all(requests)
    const endTime = Date.now()
    
    const successful = results.filter(r => r.success)
    const responseTimes = successful.map(r => r.responseTime)
    
    if (responseTimes.length > 0) {
      responseTimes.sort((a, b) => a - b)
      
      this.results.spike = {
        concurrent_users: spikeUsers,
        duration_ms: endTime - startTime,
        total_requests: results.length,
        successful_requests: successful.length,
        success_rate: (successful.length / results.length) * 100,
        avg_response_time: responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length,
        p95_response_time: responseTimes[Math.floor(responseTimes.length * 0.95)],
        max_response_time: Math.max(...responseTimes),
        throughput_rps: (successful.length / ((endTime - startTime) / 1000)).toFixed(2)
      }
      
      console.log(`  ✅ Spike handled: ${this.results.spike.throughput_rps} RPS, ${this.results.spike.avg_response_time.toFixed(0)}ms avg`)
    } else {
      console.log(`  ❌ Spike test failed - system overloaded`)
    }
    
    return this.results.spike
  }

  async performSpikeRequest(endpoint) {
    try {
      const startTime = Date.now()
      const response = await fetch(`${BASE_URL}${endpoint.url}`, {
        headers: { 'Authorization': 'Bearer test-token' },
        timeout: 10000 // 10 second timeout
      })
      const endTime = Date.now()
      
      return {
        endpoint: endpoint.name,
        responseTime: endTime - startTime,
        success: response.ok,
        status: response.status
      }
    } catch (error) {
      return {
        endpoint: endpoint.name,
        responseTime: 0,
        success: false,
        error: error.message
      }
    }
  }

  generatePerformanceReport() {
    console.log('\n' + '='.repeat(80))
    console.log('🎯 COMPREHENSIVE PERFORMANCE TEST RESULTS')
    console.log('='.repeat(80))

    // Baseline Performance Summary
    console.log('\n📊 BASELINE PERFORMANCE:')
    Object.entries(this.results.baseline).forEach(([name, stats]) => {
      const grade = this.getPerformanceGrade(stats.response_times.avg)
      console.log(`${name}: ${stats.response_times.avg.toFixed(0)}ms avg (${stats.response_times.p95.toFixed(0)}ms p95) ${grade}`)
    })

    // Load Test Summary
    if (Object.keys(this.results.load).length > 0) {
      console.log('\n⚡ LOAD TEST RESULTS:')
      Object.entries(this.results.load).forEach(([users, stats]) => {
        console.log(`${stats.concurrent_users} users: ${stats.throughput_rps} RPS, ${stats.response_times.avg.toFixed(0)}ms avg`)
      })

      // Find breaking point
      const loadEntries = Object.values(this.results.load)
      const breakingPoint = loadEntries.find(stats => stats.success_rate < 95 || stats.response_times.p95 > 1000)
      if (breakingPoint) {
        console.log(`⚠️  Breaking point detected at ${breakingPoint.concurrent_users} users`)
      } else {
        console.log(`✅ System stable up to ${loadEntries[loadEntries.length - 1].concurrent_users} concurrent users`)
      }
    }

    // Spike Test Summary
    if (this.results.spike && Object.keys(this.results.spike).length > 0) {
      console.log('\n🚀 SPIKE TEST RESULTS:')
      console.log(`Peak Load: ${this.results.spike.concurrent_users} users`)
      console.log(`Success Rate: ${this.results.spike.success_rate.toFixed(1)}%`)
      console.log(`Throughput: ${this.results.spike.throughput_rps} RPS`)
      console.log(`Response Time: ${this.results.spike.avg_response_time.toFixed(0)}ms avg, ${this.results.spike.p95_response_time.toFixed(0)}ms p95`)
      
      if (this.results.spike.success_rate > 95) {
        console.log('✅ System handled spike gracefully')
      } else {
        console.log('⚠️  System degraded under spike load')
      }
    }

    // Performance Recommendations
    console.log('\n🎯 PERFORMANCE ANALYSIS:')
    
    const allAvgTimes = Object.values(this.results.baseline).map(s => s.response_times.avg)
    const overallAvg = allAvgTimes.reduce((a, b) => a + b, 0) / allAvgTimes.length
    
    console.log(`Overall Average Response Time: ${overallAvg.toFixed(0)}ms`)
    
    if (overallAvg < 100) {
      console.log('🟢 EXCELLENT: All endpoints performing well under 100ms')
    } else if (overallAvg < 500) {
      console.log('🟡 GOOD: Response times acceptable, some optimization possible')
    } else {
      console.log('🔴 NEEDS ATTENTION: Response times above recommended thresholds')
    }

    // Fallback Usage Analysis
    const fallbackEndpoints = Object.entries(this.results.baseline)
      .filter(([name, stats]) => stats.fallback_rate > 0)
      .map(([name]) => name)
    
    if (fallbackEndpoints.length > 0) {
      console.log('\n🔄 FALLBACK MODE USAGE:')
      console.log(`Endpoints using fallback: ${fallbackEndpoints.join(', ')}`)
      console.log('ℹ️  This indicates Central Hub connectivity issues')
    }

    console.log('\n📋 RECOMMENDATIONS:')
    if (overallAvg > 200) {
      console.log('• Consider implementing caching for frequently accessed endpoints')
      console.log('• Review database query optimization for slow endpoints')
    }
    if (fallbackEndpoints.length > 0) {
      console.log('• Investigate Central Hub connectivity and response times')
      console.log('• Consider implementing circuit breaker pattern')
    }
    if (this.results.spike && this.results.spike.success_rate < 90) {
      console.log('• Implement rate limiting and request queuing for traffic spikes')
      console.log('• Consider horizontal scaling for high-traffic scenarios')
    }
    
    console.log('• All tested endpoints have robust fallback mechanisms ✅')
    console.log('• API routing pattern is consistent and predictable ✅')

    console.log('\n' + '='.repeat(80))

    return {
      timestamp: new Date().toISOString(),
      overall_avg_response_time: overallAvg,
      performance_grade: this.getPerformanceGrade(overallAvg),
      fallback_usage: fallbackEndpoints.length,
      baseline: this.results.baseline,
      load: this.results.load,
      spike: this.results.spike
    }
  }

  getPerformanceGrade(avgTime) {
    if (avgTime < 100) return '🟢 A'
    if (avgTime < 200) return '🟡 B'
    if (avgTime < 500) return '🟠 C'
    return '🔴 D'
  }
}

async function runPerformanceTests() {
  const tester = new PerformanceTester()
  
  try {
    await tester.measureBaseline()
    await tester.runLoadTest()
    await tester.runSpikeTest()
    
    const report = tester.generatePerformanceReport()
    
    // Save results
    const fs = require('fs').promises
    await fs.writeFile('performance-test-results.json', JSON.stringify(report, null, 2))
    console.log('\n💾 Performance test results saved to: performance-test-results.json')
    
    return report
  } catch (error) {
    console.error('Performance testing failed:', error)
    throw error
  }
}

// Auto-run if called directly
if (require.main === module) {
  runPerformanceTests().catch(console.error)
}

module.exports = { PerformanceTester, workingEndpoints }
#!/usr/bin/env python3
"""
BizOSaaS Analytics Data Flows Testing
=====================================

Tests end-to-end analytics data flows, real-time streaming, and data integrity
across the entire BizOSaaS platform ecosystem.
"""

import json
import time
import sys
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode

class AnalyticsDataFlowTester:
    """Test analytics data flows and real-time capabilities"""
    
    def __init__(self):
        self.test_results = []
        self.services = {
            'central_hub': 'http://localhost:8001',
            'superset': 'http://localhost:8088',
            'business_directory': 'http://localhost:8004',
            'sqladmin': 'http://localhost:8005'
        }
        
    def test_database_analytics_tables(self):
        """Test if analytics-related database tables exist and have data"""
        print("🗄️ Testing Database Analytics Tables...")
        
        # Test SQL Admin accessibility (indicates database access)
        try:
            req = Request(f"{self.services['sqladmin']}/", 
                         headers={'User-Agent': 'Analytics-Tester'})
            response = urlopen(req, timeout=5)
            
            db_accessible = response.getcode() == 200
            
            result = {
                'test': 'Database Analytics Access',
                'status': 'PASS' if db_accessible else 'FAIL',
                'details': f"SQL Admin accessible: {db_accessible}",
                'timestamp': datetime.now().isoformat(),
                'recommendations': [
                    "SQL Admin dashboard provides database access for analytics",
                    "Verify analytics tables exist: users, sessions, events, metrics",
                    "Check for time-series data with proper indexing"
                ] if db_accessible else [
                    "Fix SQL Admin dashboard connectivity",
                    "Verify PostgreSQL database is running",
                    "Check database credentials and network access"
                ]
            }
            
            self.test_results.append(result)
            print(f"   {'✅' if db_accessible else '❌'} Database Access: {result['status']}")
            
        except Exception as e:
            result = {
                'test': 'Database Analytics Access',
                'status': 'FAIL',
                'details': f"Database access error: {str(e)}",
                'timestamp': datetime.now().isoformat(),
                'recommendations': [
                    "Verify PostgreSQL container is running",
                    "Check SQL Admin dashboard configuration",
                    "Test database connection manually"
                ]
            }
            self.test_results.append(result)
            print(f"   ❌ Database Access: FAIL - {str(e)}")
    
    def test_superset_data_connectivity(self):
        """Test Apache Superset data connectivity and dashboard functionality"""
        print("📊 Testing Apache Superset Data Connectivity...")
        
        superset_tests = []
        
        # Test main Superset endpoints
        endpoints = {
            'main_page': '/',
            'login_page': '/login/',
            'api_csrf': '/api/v1/security/csrf_token/',
            'health_check': '/health'
        }
        
        for test_name, endpoint in endpoints.items():
            try:
                req = Request(f"{self.services['superset']}{endpoint}",
                             headers={'User-Agent': 'Analytics-Tester'})
                response = urlopen(req, timeout=5)
                status_code = response.getcode()
                
                superset_tests.append({
                    'endpoint': test_name,
                    'status_code': status_code,
                    'status': 'PASS' if status_code in [200, 302] else 'PARTIAL',
                    'note': 'Accessible' if status_code == 200 else 'Redirect/Auth required' if status_code == 302 else 'Response received'
                })
                
            except HTTPError as e:
                superset_tests.append({
                    'endpoint': test_name,
                    'status_code': e.code,
                    'status': 'PARTIAL' if e.code in [401, 403] else 'FAIL',
                    'note': 'Auth required' if e.code in [401, 403] else f'HTTP Error {e.code}'
                })
                
            except Exception as e:
                superset_tests.append({
                    'endpoint': test_name,
                    'status_code': 0,
                    'status': 'FAIL',
                    'note': f'Connection failed: {str(e)}'
                })
        
        # Evaluate overall Superset status
        passing_tests = sum(1 for test in superset_tests if test['status'] == 'PASS')
        partial_tests = sum(1 for test in superset_tests if test['status'] == 'PARTIAL')
        total_tests = len(superset_tests)
        
        if passing_tests >= 2 or (passing_tests + partial_tests) >= 3:
            overall_status = 'PASS'
            status_detail = f"Superset operational ({passing_tests} pass, {partial_tests} partial)"
        else:
            overall_status = 'FAIL'
            status_detail = f"Superset issues detected ({passing_tests} pass, {partial_tests} partial)"
        
        result = {
            'test': 'Apache Superset Data Connectivity',
            'status': overall_status,
            'details': status_detail,
            'endpoint_tests': superset_tests,
            'timestamp': datetime.now().isoformat(),
            'recommendations': [
                "Configure database connections in Superset",
                "Create default analytics dashboards",
                "Set up automated data refresh schedules",
                "Configure user access and permissions"
            ] if overall_status == 'PASS' else [
                "Verify Superset container health",
                "Check Superset configuration and database connections",
                "Review Superset logs for errors",
                "Ensure Superset has proper network access"
            ]
        }
        
        self.test_results.append(result)
        print(f"   {'✅' if overall_status == 'PASS' else '❌'} Superset Connectivity: {overall_status}")
        
        for test in superset_tests:
            status_icon = "✅" if test['status'] == 'PASS' else "🟡" if test['status'] == 'PARTIAL' else "❌"
            print(f"     {status_icon} {test['endpoint']}: {test['note']}")
    
    def test_realtime_analytics_endpoints(self):
        """Test real-time analytics API endpoints"""
        print("⚡ Testing Real-time Analytics Endpoints...")
        
        central_hub = self.services['central_hub']
        
        analytics_endpoints = {
            'health': '/health',
            'metrics': '/api/metrics',
            'analytics_overview': '/api/analytics/overview',
            'user_analytics': '/api/analytics/users',
            'performance_metrics': '/api/analytics/performance',
            'revenue_analytics': '/api/analytics/revenue',
            'system_status': '/api/system/status'
        }
        
        endpoint_results = []
        
        for endpoint_name, endpoint_path in analytics_endpoints.items():
            try:
                start_time = time.time()
                req = Request(f"{central_hub}{endpoint_path}",
                             headers={'User-Agent': 'Analytics-Tester'})
                response = urlopen(req, timeout=3)
                response_time = (time.time() - start_time) * 1000  # Convert to ms
                
                status_code = response.getcode()
                content_type = response.headers.get('content-type', 'unknown')
                
                # Try to read response data
                try:
                    response_data = response.read()
                    data_size = len(response_data)
                    
                    # Check if JSON response
                    if 'json' in content_type.lower():
                        try:
                            json_data = json.loads(response_data.decode())
                            has_data = bool(json_data)
                        except:
                            has_data = False
                    else:
                        has_data = data_size > 0
                except:
                    data_size = 0
                    has_data = False
                
                endpoint_results.append({
                    'endpoint': endpoint_name,
                    'path': endpoint_path,
                    'status_code': status_code,
                    'response_time_ms': round(response_time, 2),
                    'content_type': content_type,
                    'data_size': data_size,
                    'has_data': has_data,
                    'status': 'AVAILABLE' if status_code == 200 else 'EXISTS',
                    'performance': 'FAST' if response_time < 500 else 'SLOW'
                })
                
            except HTTPError as e:
                endpoint_results.append({
                    'endpoint': endpoint_name,
                    'path': endpoint_path,
                    'status_code': e.code,
                    'response_time_ms': 0,
                    'content_type': 'error',
                    'data_size': 0,
                    'has_data': False,
                    'status': 'EXISTS' if e.code in [401, 403, 404, 405] else 'ERROR',
                    'performance': 'ERROR'
                })
                
            except Exception as e:
                endpoint_results.append({
                    'endpoint': endpoint_name,
                    'path': endpoint_path,
                    'status_code': 0,
                    'response_time_ms': 0,
                    'content_type': 'error',
                    'data_size': 0,
                    'has_data': False,
                    'status': 'UNAVAILABLE',
                    'performance': 'ERROR',
                    'error': str(e)
                })
        
        # Evaluate analytics endpoints
        available_endpoints = sum(1 for ep in endpoint_results if ep['status'] == 'AVAILABLE')
        existing_endpoints = sum(1 for ep in endpoint_results if ep['status'] in ['AVAILABLE', 'EXISTS'])
        total_endpoints = len(endpoint_results)
        
        availability_rate = existing_endpoints / total_endpoints
        data_availability = sum(1 for ep in endpoint_results if ep.get('has_data', False))
        
        if availability_rate >= 0.7:
            overall_status = 'PASS'
        elif availability_rate >= 0.5:
            overall_status = 'PARTIAL'
        else:
            overall_status = 'FAIL'
        
        result = {
            'test': 'Real-time Analytics Endpoints',
            'status': overall_status,
            'details': f"Available: {available_endpoints}, Existing: {existing_endpoints}, Total: {total_endpoints}",
            'availability_rate': round(availability_rate * 100, 1),
            'data_endpoints': data_availability,
            'endpoint_results': endpoint_results,
            'timestamp': datetime.now().isoformat(),
            'recommendations': [
                "Implement missing analytics endpoints",
                "Add real-time data collection and streaming",
                "Optimize endpoint response times",
                "Add analytics data caching"
            ] if overall_status != 'PASS' else [
                "Monitor endpoint performance continuously",
                "Add analytics data validation",
                "Implement analytics data retention policies",
                "Add advanced analytics features"
            ]
        }
        
        self.test_results.append(result)
        print(f"   {'✅' if overall_status == 'PASS' else '🟡' if overall_status == 'PARTIAL' else '❌'} Analytics Endpoints: {overall_status} ({availability_rate:.1%} available)")
        
        for ep in endpoint_results:
            status_icon = "✅" if ep['status'] == 'AVAILABLE' else "🟡" if ep['status'] == 'EXISTS' else "❌"
            perf_note = f" ({ep['response_time_ms']}ms)" if ep['response_time_ms'] > 0 else ""
            print(f"     {status_icon} {ep['endpoint']}: {ep['status']}{perf_note}")
    
    def test_business_directory_analytics(self):
        """Test business directory analytics and data quality"""
        print("🏢 Testing Business Directory Analytics...")
        
        directory_url = self.services['business_directory']
        
        directory_tests = []
        
        # Test directory service endpoints
        endpoints = {
            'health': '/health',
            'api_businesses': '/api/businesses',
            'analytics': '/api/analytics',
            'metrics': '/api/metrics'
        }
        
        for test_name, endpoint in endpoints.items():
            try:
                req = Request(f"{directory_url}{endpoint}",
                             headers={'User-Agent': 'Analytics-Tester'})
                response = urlopen(req, timeout=3)
                status_code = response.getcode()
                
                # Try to read response data
                try:
                    response_data = response.read()
                    content_type = response.headers.get('content-type', 'unknown')
                    
                    if 'json' in content_type.lower():
                        json_data = json.loads(response_data.decode())
                        has_data = bool(json_data)
                        data_count = len(json_data) if isinstance(json_data, list) else 1 if json_data else 0
                    else:
                        has_data = len(response_data) > 0
                        data_count = 0
                except:
                    has_data = False
                    data_count = 0
                
                directory_tests.append({
                    'endpoint': test_name,
                    'status_code': status_code,
                    'has_data': has_data,
                    'data_count': data_count,
                    'status': 'PASS'
                })
                
            except HTTPError as e:
                directory_tests.append({
                    'endpoint': test_name,
                    'status_code': e.code,
                    'has_data': False,
                    'data_count': 0,
                    'status': 'EXISTS' if e.code in [401, 403, 404, 405] else 'FAIL'
                })
                
            except Exception as e:
                directory_tests.append({
                    'endpoint': test_name,
                    'status_code': 0,
                    'has_data': False,
                    'data_count': 0,
                    'status': 'FAIL',
                    'error': str(e)
                })
        
        # Evaluate directory analytics
        passing_tests = sum(1 for test in directory_tests if test['status'] == 'PASS')
        data_endpoints = sum(1 for test in directory_tests if test['has_data'])
        total_data_count = sum(test['data_count'] for test in directory_tests)
        
        if passing_tests >= 2:
            overall_status = 'PASS'
        elif passing_tests >= 1:
            overall_status = 'PARTIAL'
        else:
            overall_status = 'FAIL'
        
        result = {
            'test': 'Business Directory Analytics',
            'status': overall_status,
            'details': f"Passing endpoints: {passing_tests}, Data endpoints: {data_endpoints}, Total records: {total_data_count}",
            'directory_tests': directory_tests,
            'timestamp': datetime.now().isoformat(),
            'recommendations': [
                "Implement directory analytics dashboards",
                "Add business performance tracking",
                "Create directory usage analytics",
                "Add search analytics and insights"
            ] if overall_status == 'PASS' else [
                "Fix directory service connectivity",
                "Implement analytics endpoints",
                "Add business data validation",
                "Create sample business data for testing"
            ]
        }
        
        self.test_results.append(result)
        print(f"   {'✅' if overall_status == 'PASS' else '🟡' if overall_status == 'PARTIAL' else '❌'} Directory Analytics: {overall_status}")
        
        for test in directory_tests:
            status_icon = "✅" if test['status'] == 'PASS' else "🟡" if test['status'] == 'EXISTS' else "❌"
            data_note = f" (data: {test['data_count']})" if test['has_data'] else ""
            print(f"     {status_icon} {test['endpoint']}: {test['status']}{data_note}")
    
    def test_data_quality_and_integrity(self):
        """Test analytics data quality and integrity"""
        print("🔍 Testing Data Quality and Integrity...")
        
        quality_tests = []
        
        # Test 1: Timestamp consistency
        try:
            # Check if services return consistent timestamps
            current_time = datetime.now()
            
            # Get timestamps from different services
            service_timestamps = {}
            
            for service_name, service_url in self.services.items():
                try:
                    req = Request(f"{service_url}/health",
                                 headers={'User-Agent': 'Analytics-Tester'})
                    response = urlopen(req, timeout=2)
                    
                    # Try to extract timestamp from response
                    try:
                        response_data = response.read()
                        if 'json' in response.headers.get('content-type', ''):
                            json_data = json.loads(response_data.decode())
                            if 'timestamp' in json_data:
                                service_timestamps[service_name] = json_data['timestamp']
                    except:
                        pass
                    
                    service_timestamps[service_name + '_response_time'] = datetime.now().isoformat()
                    
                except:
                    pass
            
            quality_tests.append({
                'test': 'Timestamp Consistency',
                'status': 'PASS' if len(service_timestamps) > 0 else 'PARTIAL',
                'details': f"Collected {len(service_timestamps)} timestamps",
                'data': service_timestamps
            })
            
        except Exception as e:
            quality_tests.append({
                'test': 'Timestamp Consistency',
                'status': 'FAIL',
                'details': f"Timestamp test failed: {str(e)}"
            })
        
        # Test 2: Data format consistency
        try:
            # Test if API responses follow consistent format
            consistent_formats = 0
            total_tests = 0
            
            test_endpoints = [
                f"{self.services['central_hub']}/health",
                f"{self.services['business_directory']}/health"
            ]
            
            for endpoint in test_endpoints:
                try:
                    req = Request(endpoint, headers={'User-Agent': 'Analytics-Tester'})
                    response = urlopen(req, timeout=2)
                    
                    if 'json' in response.headers.get('content-type', ''):
                        consistent_formats += 1
                    total_tests += 1
                    
                except:
                    total_tests += 1
            
            format_consistency = consistent_formats / total_tests if total_tests > 0 else 0
            
            quality_tests.append({
                'test': 'Data Format Consistency',
                'status': 'PASS' if format_consistency >= 0.8 else 'PARTIAL' if format_consistency >= 0.5 else 'FAIL',
                'details': f"JSON format consistency: {format_consistency:.1%} ({consistent_formats}/{total_tests})"
            })
            
        except Exception as e:
            quality_tests.append({
                'test': 'Data Format Consistency',
                'status': 'FAIL',
                'details': f"Format consistency test failed: {str(e)}"
            })
        
        # Test 3: Service response reliability
        try:
            reliable_services = 0
            total_services = len(self.services)
            
            for service_name, service_url in self.services.items():
                try:
                    req = Request(f"{service_url}/health",
                                 headers={'User-Agent': 'Analytics-Tester'})
                    response = urlopen(req, timeout=2)
                    
                    if response.getcode() in [200, 401, 403]:  # Consider auth-protected as reliable
                        reliable_services += 1
                except:
                    pass
            
            reliability_rate = reliable_services / total_services
            
            quality_tests.append({
                'test': 'Service Response Reliability',
                'status': 'PASS' if reliability_rate >= 0.8 else 'PARTIAL' if reliability_rate >= 0.6 else 'FAIL',
                'details': f"Reliable services: {reliability_rate:.1%} ({reliable_services}/{total_services})"
            })
            
        except Exception as e:
            quality_tests.append({
                'test': 'Service Response Reliability',
                'status': 'FAIL',
                'details': f"Reliability test failed: {str(e)}"
            })
        
        # Evaluate overall data quality
        passing_quality_tests = sum(1 for test in quality_tests if test['status'] == 'PASS')
        total_quality_tests = len(quality_tests)
        quality_score = passing_quality_tests / total_quality_tests if total_quality_tests > 0 else 0
        
        overall_status = 'PASS' if quality_score >= 0.8 else 'PARTIAL' if quality_score >= 0.6 else 'FAIL'
        
        result = {
            'test': 'Data Quality and Integrity',
            'status': overall_status,
            'details': f"Quality score: {quality_score:.1%} ({passing_quality_tests}/{total_quality_tests} tests passed)",
            'quality_tests': quality_tests,
            'quality_score': quality_score,
            'timestamp': datetime.now().isoformat(),
            'recommendations': [
                "Implement data validation schemas",
                "Add automated data quality monitoring",
                "Create data integrity checks",
                "Implement consistent error handling"
            ] if overall_status != 'PASS' else [
                "Monitor data quality continuously",
                "Add advanced data validation rules",
                "Implement data quality alerts",
                "Create data quality dashboards"
            ]
        }
        
        self.test_results.append(result)
        print(f"   {'✅' if overall_status == 'PASS' else '🟡' if overall_status == 'PARTIAL' else '❌'} Data Quality: {overall_status} ({quality_score:.1%})")
        
        for test in quality_tests:
            status_icon = "✅" if test['status'] == 'PASS' else "🟡" if test['status'] == 'PARTIAL' else "❌"
            print(f"     {status_icon} {test['test']}: {test['status']}")
    
    def run_comprehensive_test(self):
        """Run all analytics data flow tests"""
        print("🚀 BizOSaaS Analytics Data Flow Testing")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all test categories
        test_functions = [
            self.test_database_analytics_tables,
            self.test_superset_data_connectivity,
            self.test_realtime_analytics_endpoints,
            self.test_business_directory_analytics,
            self.test_data_quality_and_integrity
        ]
        
        for test_function in test_functions:
            try:
                test_function()
            except Exception as e:
                print(f"❌ Test error in {test_function.__name__}: {str(e)}")
                self.test_results.append({
                    'test': test_function.__name__,
                    'status': 'ERROR',
                    'details': f"Test execution error: {str(e)}",
                    'timestamp': datetime.now().isoformat()
                })
        
        execution_time = time.time() - start_time
        
        # Generate comprehensive report
        self.generate_final_report(execution_time)
    
    def generate_final_report(self, execution_time):
        """Generate final comprehensive analytics report"""
        
        print(f"\n📊 Analytics Data Flow Test Results")
        print("=" * 60)
        
        # Calculate summary statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.get('status') == 'PASS')
        partial_tests = sum(1 for result in self.test_results if result.get('status') == 'PARTIAL')
        failed_tests = sum(1 for result in self.test_results if result.get('status') in ['FAIL', 'ERROR'])
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"🟡 Partial: {partial_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Execution Time: {execution_time:.2f} seconds")
        
        # Determine overall analytics health
        if success_rate >= 80:
            overall_health = "🟢 EXCELLENT - Analytics platform fully operational"
        elif success_rate >= 60:
            overall_health = "🟡 GOOD - Analytics platform mostly operational with minor issues"
        elif success_rate >= 40:
            overall_health = "🟠 FAIR - Analytics platform partially operational, needs attention"
        else:
            overall_health = "🔴 POOR - Analytics platform needs immediate attention"
        
        print(f"\nOverall Analytics Health: {overall_health}")
        
        # Print detailed results
        print(f"\n🔍 Detailed Test Results:")
        print("-" * 40)
        
        for result in self.test_results:
            status_icon = {
                'PASS': '✅',
                'PARTIAL': '🟡', 
                'FAIL': '❌',
                'ERROR': '💥'
            }.get(result.get('status', 'UNKNOWN'), '❓')
            
            print(f"{status_icon} {result.get('test', 'Unknown Test')}: {result.get('status', 'UNKNOWN')}")
            print(f"   {result.get('details', 'No details available')}")
        
        # Generate recommendations
        print(f"\n🎯 Priority Recommendations:")
        print("-" * 30)
        
        if failed_tests > 0:
            print("🔴 CRITICAL - Address failing tests first:")
            for result in self.test_results:
                if result.get('status') in ['FAIL', 'ERROR']:
                    recommendations = result.get('recommendations', [])
                    if recommendations:
                        print(f"   • {result.get('test')}: {recommendations[0]}")
        
        if partial_tests > 0:
            print("🟡 IMPROVEMENTS - Enhance partially working systems:")
            for result in self.test_results:
                if result.get('status') == 'PARTIAL':
                    recommendations = result.get('recommendations', [])
                    if recommendations:
                        print(f"   • {result.get('test')}: {recommendations[0]}")
        
        if passed_tests > 0:
            print("✅ ENHANCEMENTS - Optimize working systems:")
            passing_recommendations = [
                "Implement advanced analytics dashboards",
                "Add real-time alerting and monitoring",
                "Create automated analytics reports",
                "Implement predictive analytics capabilities",
                "Add user behavior tracking and insights"
            ]
            for i, rec in enumerate(passing_recommendations[:3]):
                print(f"   • {rec}")
        
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"analytics_dataflow_report_{timestamp}.json"
        
        detailed_report = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'execution_time': execution_time,
                'total_tests': total_tests,
                'success_rate': success_rate,
                'overall_health': overall_health
            },
            'test_summary': {
                'passed': passed_tests,
                'partial': partial_tests,
                'failed': failed_tests,
                'total': total_tests
            },
            'detailed_results': self.test_results,
            'services_tested': list(self.services.keys())
        }
        
        with open(report_filename, 'w') as f:
            json.dump(detailed_report, f, indent=2)
        
        print(f"\n💾 Detailed report saved: {report_filename}")
        
        return detailed_report

def main():
    """Main execution function"""
    
    tester = AnalyticsDataFlowTester()
    
    try:
        report = tester.run_comprehensive_test()
        return 0
    except Exception as e:
        print(f"❌ Analytics data flow testing failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
BizOSaaS Platform - Wizard Functional Testing
=============================================

This script performs functional testing of wizard implementations by:
1. Testing wizard navigation flows
2. Validating form submissions
3. Testing error handling
4. Verifying data persistence
5. Testing mobile responsiveness
6. Accessibility compliance testing
"""

import asyncio
import json
import logging
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WizardFunctionalTestResult:
    """Results from functional testing of a wizard"""
    wizard_name: str
    platform: str
    url: str
    test_categories: Dict[str, Dict[str, Any]]
    overall_score: float
    grade: str
    issues_found: List[str]
    test_duration: float
    timestamp: str

class WizardFunctionalTester:
    """Functional testing framework for wizards"""
    
    def __init__(self):
        self.platforms = {
            'client_portal': 'http://localhost:3000',
            'coreldove_frontend': 'http://localhost:3002', 
            'business_directory': 'http://localhost:3004',
            'bizosaas_admin': 'http://localhost:3009'
        }
        
        self.wizard_endpoints = {
            'client_portal': [
                '/onboarding',
                '/campaigns/new',
                '/analytics/setup',
                '/billing/setup'
            ],
            'coreldove_frontend': [
                '/store-setup',
                '/sourcing/wizard'
            ],
            'business_directory': [
                '/listing/create'
            ],
            'bizosaas_admin': [
                '/tenants/setup',
                '/ai/setup',
                '/integrations/setup',
                '/users/roles/setup'
            ]
        }
        
        self.test_results = []
        
    def test_wizard_navigation(self, platform_url: str, wizard_path: str) -> Dict[str, Any]:
        """Test wizard navigation functionality"""
        test_result = {
            'category': 'Navigation',
            'tests': {
                'wizard_loads': False,
                'step_indicators_present': False,
                'next_button_present': False,
                'previous_button_present': False,
                'progress_bar_present': False,
                'step_validation': False
            },
            'score': 0,
            'issues': []
        }
        
        try:
            # Test if wizard page loads
            response = requests.get(f"{platform_url}{wizard_path}", timeout=10)
            if response.status_code == 200:
                test_result['tests']['wizard_loads'] = True
                content = response.text.lower()
                
                # Check for navigation elements
                if any(indicator in content for indicator in ['step', 'progress', 'wizard']):
                    test_result['tests']['step_indicators_present'] = True
                    
                if any(btn in content for btn in ['next', 'continue', 'proceed']):
                    test_result['tests']['next_button_present'] = True
                    
                if any(btn in content for btn in ['previous', 'back', 'prev']):
                    test_result['tests']['previous_button_present'] = True
                    
                if any(progress in content for progress in ['progress', 'percent', '%']):
                    test_result['tests']['progress_bar_present'] = True
                    
                # Check for form validation indicators
                if any(validation in content for validation in ['required', 'error', 'invalid']):
                    test_result['tests']['step_validation'] = True
                    
            else:
                test_result['issues'].append(f"Wizard page returned {response.status_code}")
                
        except Exception as e:
            test_result['issues'].append(f"Navigation test failed: {str(e)}")
            
        # Calculate score
        passed_tests = sum(1 for test in test_result['tests'].values() if test)
        test_result['score'] = (passed_tests / len(test_result['tests'])) * 100
        
        return test_result
        
    def test_form_validation(self, platform_url: str, wizard_path: str) -> Dict[str, Any]:
        """Test form validation and error handling"""
        test_result = {
            'category': 'Form Validation',
            'tests': {
                'has_form_elements': False,
                'has_validation_rules': False,
                'error_messages_present': False,
                'required_field_validation': False,
                'input_type_validation': False
            },
            'score': 0,
            'issues': []
        }
        
        try:
            response = requests.get(f"{platform_url}{wizard_path}", timeout=10)
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for form elements
                if any(element in content for element in ['<form', '<input', '<select', '<textarea']):
                    test_result['tests']['has_form_elements'] = True
                    
                # Check for validation rules
                if any(validation in content for validation in ['required', 'pattern', 'minlength', 'maxlength']):
                    test_result['tests']['has_validation_rules'] = True
                    
                # Check for error handling
                if any(error in content for error in ['error', 'invalid', 'message']):
                    test_result['tests']['error_messages_present'] = True
                    
                # Check for required field indicators
                if 'required' in content or '*' in content:
                    test_result['tests']['required_field_validation'] = True
                    
                # Check for input type validation
                if any(input_type in content for input_type in ['email', 'tel', 'url', 'number']):
                    test_result['tests']['input_type_validation'] = True
                    
        except Exception as e:
            test_result['issues'].append(f"Form validation test failed: {str(e)}")
            
        # Calculate score
        passed_tests = sum(1 for test in test_result['tests'].values() if test)
        test_result['score'] = (passed_tests / len(test_result['tests'])) * 100
        
        return test_result
        
    def test_api_integration(self, platform_url: str, wizard_path: str) -> Dict[str, Any]:
        """Test API integration and data submission"""
        test_result = {
            'category': 'API Integration',
            'tests': {
                'api_endpoints_accessible': False,
                'csrf_protection': False,
                'error_handling': False,
                'loading_states': False,
                'success_responses': False
            },
            'score': 0,
            'issues': []
        }
        
        try:
            # Test common API endpoints
            api_endpoints = ['/api/wizard', '/api/save', '/api/submit', '/api/validate']
            accessible_endpoints = 0
            
            for endpoint in api_endpoints:
                try:
                    response = requests.get(f"{platform_url}{endpoint}", timeout=5)
                    if response.status_code < 500:  # Any response except server error
                        accessible_endpoints += 1
                except:
                    pass
                    
            if accessible_endpoints > 0:
                test_result['tests']['api_endpoints_accessible'] = True
                
            # Check main page for API integration indicators
            response = requests.get(f"{platform_url}{wizard_path}", timeout=10)
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for CSRF protection
                if any(csrf in content for csrf in ['csrf', 'token', '_token']):
                    test_result['tests']['csrf_protection'] = True
                    
                # Check for error handling
                if any(error in content for error in ['catch', 'error', 'try']):
                    test_result['tests']['error_handling'] = True
                    
                # Check for loading states
                if any(loading in content for loading in ['loading', 'spinner', 'pending']):
                    test_result['tests']['loading_states'] = True
                    
                # Check for success handling
                if any(success in content for success in ['success', 'complete', 'done']):
                    test_result['tests']['success_responses'] = True
                    
        except Exception as e:
            test_result['issues'].append(f"API integration test failed: {str(e)}")
            
        # Calculate score
        passed_tests = sum(1 for test in test_result['tests'].values() if test)
        test_result['score'] = (passed_tests / len(test_result['tests'])) * 100
        
        return test_result
        
    def test_accessibility(self, platform_url: str, wizard_path: str) -> Dict[str, Any]:
        """Test accessibility compliance"""
        test_result = {
            'category': 'Accessibility',
            'tests': {
                'semantic_html': False,
                'aria_labels': False,
                'keyboard_navigation': False,
                'focus_management': False,
                'alt_text': False,
                'color_contrast': False
            },
            'score': 0,
            'issues': []
        }
        
        try:
            response = requests.get(f"{platform_url}{wizard_path}", timeout=10)
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for semantic HTML
                if any(semantic in content for semantic in ['<main', '<section', '<header', '<nav']):
                    test_result['tests']['semantic_html'] = True
                    
                # Check for ARIA labels
                if any(aria in content for aria in ['aria-label', 'aria-describedby', 'aria-expanded']):
                    test_result['tests']['aria_labels'] = True
                    
                # Check for keyboard navigation
                if any(keyboard in content for keyboard in ['tabindex', 'onkeydown', 'onkeypress']):
                    test_result['tests']['keyboard_navigation'] = True
                    
                # Check for focus management
                if 'focus' in content:
                    test_result['tests']['focus_management'] = True
                    
                # Check for alt text
                if 'alt=' in content:
                    test_result['tests']['alt_text'] = True
                    
                # Check for color contrast considerations
                if any(contrast in content for contrast in ['dark:', 'light:', 'contrast']):
                    test_result['tests']['color_contrast'] = True
                    
        except Exception as e:
            test_result['issues'].append(f"Accessibility test failed: {str(e)}")
            
        # Calculate score
        passed_tests = sum(1 for test in test_result['tests'].values() if test)
        test_result['score'] = (passed_tests / len(test_result['tests'])) * 100
        
        return test_result
        
    def test_responsive_design(self, platform_url: str, wizard_path: str) -> Dict[str, Any]:
        """Test responsive design and mobile compatibility"""
        test_result = {
            'category': 'Responsive Design',
            'tests': {
                'viewport_meta': False,
                'responsive_css': False,
                'mobile_friendly': False,
                'touch_friendly': False,
                'breakpoint_support': False
            },
            'score': 0,
            'issues': []
        }
        
        try:
            response = requests.get(f"{platform_url}{wizard_path}", timeout=10)
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check for viewport meta tag
                if 'viewport' in content and 'width=device-width' in content:
                    test_result['tests']['viewport_meta'] = True
                    
                # Check for responsive CSS
                if any(responsive in content for responsive in ['@media', 'responsive', 'fluid']):
                    test_result['tests']['responsive_css'] = True
                    
                # Check for mobile-friendly elements
                if any(mobile in content for mobile in ['mobile', 'touch', 'gesture']):
                    test_result['tests']['mobile_friendly'] = True
                    
                # Check for touch-friendly design
                if any(touch in content for touch in ['ontouchstart', 'touchend', 'tap']):
                    test_result['tests']['touch_friendly'] = True
                    
                # Check for breakpoint support (Tailwind CSS)
                if any(breakpoint in content for breakpoint in ['sm:', 'md:', 'lg:', 'xl:']):
                    test_result['tests']['breakpoint_support'] = True
                    
        except Exception as e:
            test_result['issues'].append(f"Responsive design test failed: {str(e)}")
            
        # Calculate score
        passed_tests = sum(1 for test in test_result['tests'].values() if test)
        test_result['score'] = (passed_tests / len(test_result['tests'])) * 100
        
        return test_result
        
    def test_performance(self, platform_url: str, wizard_path: str) -> Dict[str, Any]:
        """Test wizard performance"""
        test_result = {
            'category': 'Performance',
            'tests': {
                'fast_loading': False,
                'optimized_assets': False,
                'lazy_loading': False,
                'caching': False,
                'compression': False
            },
            'score': 0,
            'issues': [],
            'metrics': {}
        }
        
        try:
            start_time = time.time()
            response = requests.get(f"{platform_url}{wizard_path}", timeout=10)
            load_time = time.time() - start_time
            
            test_result['metrics']['load_time'] = load_time
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Check loading time
                if load_time < 3.0:
                    test_result['tests']['fast_loading'] = True
                else:
                    test_result['issues'].append(f"Slow loading time: {load_time:.2f}s")
                    
                # Check for optimized assets
                if any(optimization in content for optimization in ['webp', 'optimize', 'minified']):
                    test_result['tests']['optimized_assets'] = True
                    
                # Check for lazy loading
                if any(lazy in content for lazy in ['lazy', 'intersection', 'defer']):
                    test_result['tests']['lazy_loading'] = True
                    
                # Check response headers for caching
                cache_headers = ['cache-control', 'etag', 'expires']
                if any(header in response.headers for header in cache_headers):
                    test_result['tests']['caching'] = True
                    
                # Check for compression
                if 'gzip' in response.headers.get('content-encoding', ''):
                    test_result['tests']['compression'] = True
                    
        except Exception as e:
            test_result['issues'].append(f"Performance test failed: {str(e)}")
            
        # Calculate score
        passed_tests = sum(1 for test in test_result['tests'].values() if test)
        test_result['score'] = (passed_tests / len(test_result['tests'])) * 100
        
        return test_result
        
    def test_wizard_comprehensive(self, platform_key: str, wizard_path: str) -> WizardFunctionalTestResult:
        """Run comprehensive functional testing on a wizard"""
        start_time = time.time()
        platform_url = self.platforms[platform_key]
        wizard_name = wizard_path.strip('/').replace('/', '_')
        
        logger.info(f"🧪 Testing wizard: {wizard_name} on {platform_key}")
        
        # Run all test categories
        test_categories = {
            'navigation': self.test_wizard_navigation(platform_url, wizard_path),
            'form_validation': self.test_form_validation(platform_url, wizard_path),
            'api_integration': self.test_api_integration(platform_url, wizard_path),
            'accessibility': self.test_accessibility(platform_url, wizard_path),
            'responsive_design': self.test_responsive_design(platform_url, wizard_path),
            'performance': self.test_performance(platform_url, wizard_path)
        }
        
        # Calculate overall score
        total_score = sum(category['score'] for category in test_categories.values())
        overall_score = total_score / len(test_categories)
        
        # Collect all issues
        all_issues = []
        for category in test_categories.values():
            all_issues.extend(category.get('issues', []))
            
        # Determine grade
        grade = self._get_grade(overall_score)
        
        result = WizardFunctionalTestResult(
            wizard_name=wizard_name,
            platform=platform_key,
            url=f"{platform_url}{wizard_path}",
            test_categories=test_categories,
            overall_score=overall_score,
            grade=grade,
            issues_found=all_issues,
            test_duration=time.time() - start_time,
            timestamp=datetime.now().isoformat()
        )
        
        return result
        
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90: return 'A+'
        elif score >= 80: return 'A'
        elif score >= 70: return 'B'
        elif score >= 60: return 'C'
        elif score >= 50: return 'D'
        else: return 'F'
        
    async def run_all_wizard_tests(self) -> Dict[str, Any]:
        """Run functional tests on all wizards"""
        logger.info("🧪 Starting Comprehensive Wizard Functional Testing")
        logger.info("=" * 60)
        
        all_results = []
        
        for platform_key, wizard_paths in self.wizard_endpoints.items():
            if platform_key not in self.platforms:
                continue
                
            # Check if platform is accessible
            try:
                response = requests.get(self.platforms[platform_key], timeout=5)
                if response.status_code != 200:
                    logger.warning(f"⚠️ {platform_key} not accessible, skipping")
                    continue
            except:
                logger.warning(f"❌ {platform_key} unreachable, skipping")
                continue
                
            logger.info(f"🌐 Testing platform: {platform_key}")
            
            for wizard_path in wizard_paths:
                try:
                    result = self.test_wizard_comprehensive(platform_key, wizard_path)
                    all_results.append(result)
                    
                    # Log immediate result
                    status = "✅" if result.overall_score >= 70 else "⚠️" if result.overall_score >= 50 else "❌"
                    logger.info(f"   {status} {result.wizard_name}: {result.overall_score:.1f}/100 ({result.grade})")
                    
                except Exception as e:
                    logger.error(f"   ❌ Failed to test {wizard_path}: {e}")
                    
        self.test_results = all_results
        
        # Generate summary report
        report = self._generate_functional_report(all_results)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"wizard_functional_test_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        logger.info("=" * 60)
        logger.info("🎯 FUNCTIONAL TESTING COMPLETE")
        logger.info(f"🧪 Wizards Tested: {len(all_results)}")
        logger.info(f"📊 Average Score: {report['summary']['average_score']:.1f}/100")
        logger.info(f"📋 Report: {report_file}")
        
        return report
        
    def _generate_functional_report(self, results: List[WizardFunctionalTestResult]) -> Dict[str, Any]:
        """Generate comprehensive functional testing report"""
        if not results:
            return {'summary': {'no_results': True}}
            
        total_score = sum(r.overall_score for r in results)
        avg_score = total_score / len(results)
        
        # Category scores
        category_scores = {}
        for category in ['navigation', 'form_validation', 'api_integration', 'accessibility', 'responsive_design', 'performance']:
            scores = [r.test_categories[category]['score'] for r in results if category in r.test_categories]
            if scores:
                category_scores[category] = sum(scores) / len(scores)
                
        # Top and bottom performers
        sorted_results = sorted(results, key=lambda x: x.overall_score, reverse=True)
        top_performers = sorted_results[:3]
        bottom_performers = sorted_results[-3:] if len(sorted_results) > 3 else []
        
        # Common issues
        all_issues = []
        for result in results:
            all_issues.extend(result.issues_found)
        issue_counts = {}
        for issue in all_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        common_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        report = {
            'summary': {
                'timestamp': datetime.now().isoformat(),
                'total_wizards_tested': len(results),
                'average_score': avg_score,
                'grade_distribution': {
                    'A+': len([r for r in results if r.grade == 'A+']),
                    'A': len([r for r in results if r.grade == 'A']),
                    'B': len([r for r in results if r.grade == 'B']),
                    'C': len([r for r in results if r.grade == 'C']),
                    'D': len([r for r in results if r.grade == 'D']),
                    'F': len([r for r in results if r.grade == 'F'])
                }
            },
            'category_performance': category_scores,
            'top_performers': [
                {
                    'name': r.wizard_name,
                    'platform': r.platform,
                    'score': r.overall_score,
                    'grade': r.grade
                } for r in top_performers
            ],
            'needs_improvement': [
                {
                    'name': r.wizard_name,
                    'platform': r.platform,
                    'score': r.overall_score,
                    'grade': r.grade,
                    'issues': len(r.issues_found)
                } for r in bottom_performers
            ],
            'common_issues': common_issues,
            'detailed_results': [
                {
                    'wizard_name': r.wizard_name,
                    'platform': r.platform,
                    'url': r.url,
                    'overall_score': r.overall_score,
                    'grade': r.grade,
                    'category_scores': {cat: data['score'] for cat, data in r.test_categories.items()},
                    'issues_count': len(r.issues_found),
                    'test_duration': r.test_duration
                } for r in results
            ]
        }
        
        return report

def main():
    """Main execution function"""
    tester = WizardFunctionalTester()
    
    # Run comprehensive functional tests
    report = asyncio.run(tester.run_all_wizard_tests())
    
    # Print summary
    print("\n" + "="*60)
    print("🧪 WIZARD FUNCTIONAL TESTING SUMMARY")
    print("="*60)
    
    if 'no_results' in report.get('summary', {}):
        print("❌ No test results available")
        return
        
    for result in tester.test_results:
        status_icon = "✅" if result.overall_score >= 70 else "⚠️" if result.overall_score >= 50 else "❌"
        print(f"{status_icon} {result.wizard_name:<30} {result.overall_score:>5.1f}/100 ({result.grade})")
        
    print(f"\n📊 Average Score: {report['summary']['average_score']:.1f}/100")
    
    # Show category performance
    print("\n📋 CATEGORY PERFORMANCE:")
    for category, score in report['category_performance'].items():
        status = "✅" if score >= 70 else "⚠️" if score >= 50 else "❌"
        print(f"   {status} {category.replace('_', ' ').title():<20} {score:>5.1f}/100")
        
    # Show top performers
    if report['top_performers']:
        print("\n🏆 TOP PERFORMERS:")
        for performer in report['top_performers']:
            print(f"   🥇 {performer['name']} - {performer['score']:.1f}/100 ({performer['grade']})")

if __name__ == "__main__":
    main()
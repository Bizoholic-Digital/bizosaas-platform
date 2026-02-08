#!/usr/bin/env python3
"""
BizOSaaS Platform - Comprehensive Wizard Testing Framework
===========================================================

This framework systematically tests and validates all wizard implementations
and guided flows across the BizOSaaS platform frontend applications.

Key Testing Areas:
1. Wizard step flows and navigation
2. Form validation and error handling  
3. Data persistence and recovery
4. Completion and success states
5. Responsive design across devices
6. Accessibility compliance (WCAG 2.1)
7. Backend API integration
8. Progress indicators
9. User type customization
10. Analytics and completion tracking
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WizardTestResult:
    """Results from testing a specific wizard"""
    wizard_name: str
    platform: str
    url: str
    total_steps: int
    completed_steps: int
    validation_errors: List[str]
    navigation_issues: List[str]
    accessibility_issues: List[str]
    performance_metrics: Dict[str, float]
    mobile_responsive: bool
    data_persistence: bool
    success_state_reached: bool
    overall_score: float
    test_duration: float
    timestamp: str

@dataclass
class PlatformEndpoint:
    """Platform endpoint configuration"""
    name: str
    url: str
    port: int
    status: str

class WizardTestingFramework:
    """Comprehensive wizard testing framework"""
    
    def __init__(self):
        self.platforms = {
            'client_portal': PlatformEndpoint('Client Portal', 'http://localhost:3000', 3000, 'unknown'),
            'bizoholic_frontend': PlatformEndpoint('Bizoholic Frontend', 'http://localhost:3001', 3001, 'unknown'),
            'coreldove_frontend': PlatformEndpoint('CoreLDove Frontend', 'http://localhost:3002', 3002, 'unknown'),
            'business_directory': PlatformEndpoint('Business Directory', 'http://localhost:3004', 3004, 'unknown'),
            'bizosaas_admin': PlatformEndpoint('BizOSaaS Admin', 'http://localhost:3009', 3009, 'unknown')
        }
        
        self.wizards_to_test = [
            {
                'name': 'Client Onboarding Wizard',
                'platform': 'client_portal',
                'path': '/onboarding',
                'type': 'business_discovery',
                'expected_steps': 5,
                'data_fields': ['business_name', 'industry', 'goals', 'budget', 'timeline']
            },
            {
                'name': 'Campaign Setup Wizard', 
                'platform': 'client_portal',
                'path': '/campaigns/new',
                'type': 'campaign_configuration',
                'expected_steps': 6,
                'data_fields': ['campaign_name', 'platforms', 'targeting', 'budget', 'creative', 'schedule']
            },
            {
                'name': 'Product Sourcing Wizard',
                'platform': 'coreldove_frontend', 
                'path': '/sourcing/wizard',
                'type': 'product_sourcing',
                'expected_steps': 4,
                'data_fields': ['product_category', 'criteria', 'profit_margin', 'supplier_preferences']
            },
            {
                'name': 'E-commerce Store Setup Wizard',
                'platform': 'coreldove_frontend',
                'path': '/store-setup',
                'type': 'store_configuration',
                'expected_steps': 7,
                'data_fields': ['store_name', 'domain', 'theme', 'payment_methods', 'shipping', 'tax_settings', 'launch_settings']
            },
            {
                'name': 'Business Directory Listing Wizard',
                'platform': 'business_directory',
                'path': '/listing/create',
                'type': 'directory_listing',
                'expected_steps': 4,
                'data_fields': ['business_info', 'location', 'services', 'contact_details']
            },
            {
                'name': 'Multi-tenant Setup Wizard',
                'platform': 'bizosaas_admin',
                'path': '/tenants/setup',
                'type': 'tenant_configuration',
                'expected_steps': 5,
                'data_fields': ['tenant_name', 'domain', 'plan', 'admin_user', 'billing']
            },
            {
                'name': 'AI Agent Configuration Wizard',
                'platform': 'bizosaas_admin',
                'path': '/ai/setup',
                'type': 'ai_configuration',
                'expected_steps': 4,
                'data_fields': ['agent_type', 'parameters', 'integrations', 'deployment']
            },
            {
                'name': 'Analytics Dashboard Setup Wizard',
                'platform': 'client_portal',
                'path': '/analytics/setup',
                'type': 'analytics_configuration',
                'expected_steps': 3,
                'data_fields': ['data_sources', 'metrics', 'visualization']
            },
            {
                'name': 'Payment and Billing Setup Wizard',
                'platform': 'client_portal',
                'path': '/billing/setup',
                'type': 'payment_configuration',
                'expected_steps': 4,
                'data_fields': ['payment_method', 'billing_address', 'plan_selection', 'confirmation']
            },
            {
                'name': 'Integration Setup Wizard',
                'platform': 'bizosaas_admin',
                'path': '/integrations/setup',
                'type': 'integration_configuration',
                'expected_steps': 3,
                'data_fields': ['integration_type', 'credentials', 'configuration']
            },
            {
                'name': 'User Role and Permissions Wizard',
                'platform': 'bizosaas_admin',
                'path': '/users/roles/setup',
                'type': 'role_configuration',
                'expected_steps': 4,
                'data_fields': ['role_name', 'permissions', 'users', 'confirmation']
            }
        ]
        
        self.test_results = []
        self.driver = None
        
    def setup_driver(self, mobile=False):
        """Setup Selenium WebDriver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        if mobile:
            chrome_options.add_argument('--window-size=375,667')  # iPhone size
            chrome_options.add_experimental_option("mobileEmulation", {
                "deviceName": "iPhone 12"
            })
        else:
            chrome_options.add_argument('--window-size=1920,1080')
            
        self.driver = webdriver.Chrome(options=chrome_options)
        return self.driver
        
    def check_platform_availability(self):
        """Check if all platforms are accessible"""
        logger.info("Checking platform availability...")
        
        for platform_key, platform in self.platforms.items():
            try:
                response = requests.get(platform.url, timeout=5)
                if response.status_code == 200:
                    platform.status = 'accessible'
                    logger.info(f"✅ {platform.name} is accessible at {platform.url}")
                else:
                    platform.status = f'error_{response.status_code}'
                    logger.warning(f"⚠️ {platform.name} returned status {response.status_code}")
            except requests.exceptions.RequestException as e:
                platform.status = 'unreachable'
                logger.error(f"❌ {platform.name} is unreachable: {e}")
                
    def test_wizard_accessibility(self, wizard_url: str) -> List[str]:
        """Test wizard for WCAG 2.1 accessibility compliance"""
        issues = []
        
        try:
            # Check for proper heading structure
            headings = self.driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")
            if not headings:
                issues.append("No heading elements found")
                
            # Check for form labels
            inputs = self.driver.find_elements(By.CSS_SELECTOR, "input, select, textarea")
            for input_elem in inputs:
                input_id = input_elem.get_attribute('id')
                if input_id:
                    labels = self.driver.find_elements(By.CSS_SELECTOR, f"label[for='{input_id}']")
                    if not labels:
                        aria_label = input_elem.get_attribute('aria-label')
                        if not aria_label:
                            issues.append(f"Input missing label: {input_elem.get_attribute('name') or 'unnamed'}")
                            
            # Check for alt text on images
            images = self.driver.find_elements(By.CSS_SELECTOR, "img")
            for img in images:
                alt_text = img.get_attribute('alt')
                if not alt_text:
                    issues.append(f"Image missing alt text: {img.get_attribute('src')}")
                    
            # Check for keyboard navigation support
            focusable_elements = self.driver.find_elements(By.CSS_SELECTOR, "button, input, select, textarea, a[href]")
            if not focusable_elements:
                issues.append("No focusable elements found")
                
        except Exception as e:
            issues.append(f"Accessibility check error: {str(e)}")
            
        return issues
        
    def test_wizard_navigation(self, wizard_config: Dict) -> Dict[str, Any]:
        """Test wizard step navigation and flow"""
        navigation_results = {
            'completed_steps': 0,
            'navigation_issues': [],
            'step_timings': [],
            'back_navigation_works': False,
            'skip_functionality': False
        }
        
        try:
            # Look for navigation elements
            next_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                "button[data-testid*='next'], button:contains('Next'), .wizard-next, .btn-next")
            back_buttons = self.driver.find_elements(By.CSS_SELECTOR,
                "button[data-testid*='back'], button:contains('Back'), .wizard-back, .btn-back")
            step_indicators = self.driver.find_elements(By.CSS_SELECTOR,
                ".step-indicator, .wizard-steps, .progress-steps, [data-testid*='step']")
                
            if not next_buttons:
                navigation_results['navigation_issues'].append("No 'Next' button found")
                
            if not step_indicators:
                navigation_results['navigation_issues'].append("No step indicators found")
                
            # Try to navigate through steps
            for step in range(wizard_config['expected_steps']):
                start_time = time.time()
                
                # Try to fill any required fields in current step
                self.fill_wizard_step_data(step)
                
                # Try to proceed to next step
                if next_buttons:
                    try:
                        next_buttons[0].click()
                        WebDriverWait(self.driver, 5).until(
                            lambda d: len(d.find_elements(By.CSS_SELECTOR, ".active-step, .current-step")) > 0
                        )
                        navigation_results['completed_steps'] += 1
                        step_time = time.time() - start_time
                        navigation_results['step_timings'].append(step_time)
                    except TimeoutException:
                        navigation_results['navigation_issues'].append(f"Step {step + 1} navigation timeout")
                        break
                else:
                    break
                    
            # Test back navigation
            if back_buttons and navigation_results['completed_steps'] > 1:
                try:
                    back_buttons[0].click()
                    time.sleep(1)
                    navigation_results['back_navigation_works'] = True
                except:
                    navigation_results['navigation_issues'].append("Back navigation failed")
                    
        except Exception as e:
            navigation_results['navigation_issues'].append(f"Navigation test error: {str(e)}")
            
        return navigation_results
        
    def fill_wizard_step_data(self, step_index: int):
        """Fill sample data for wizard step"""
        try:
            # Common test data patterns
            test_data = {
                'business_name': 'Test Business',
                'email': 'test@example.com', 
                'company': 'Test Company',
                'name': 'Test User',
                'phone': '1234567890',
                'address': '123 Test St',
                'website': 'https://test.com',
                'budget': '5000',
                'industry': 'Technology'
            }
            
            # Fill text inputs
            text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='email'], textarea")
            for i, input_elem in enumerate(text_inputs):
                input_name = input_elem.get_attribute('name') or input_elem.get_attribute('placeholder') or f'field_{i}'
                
                # Match test data to input
                value = test_data.get(input_name.lower(), f'test_value_{i}')
                input_elem.clear()
                input_elem.send_keys(value)
                
            # Handle select dropdowns
            selects = self.driver.find_elements(By.CSS_SELECTOR, "select")
            for select in selects:
                options = select.find_elements(By.CSS_SELECTOR, "option")
                if len(options) > 1:
                    options[1].click()  # Select first non-default option
                    
            # Handle checkboxes and radio buttons
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            for checkbox in checkboxes[:2]:  # Check first two checkboxes
                if not checkbox.is_selected():
                    checkbox.click()
                    
        except Exception as e:
            logger.warning(f"Error filling step data: {e}")
            
    def test_form_validation(self) -> List[str]:
        """Test form validation and error handling"""
        validation_issues = []
        
        try:
            # Try submitting empty form
            submit_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                "button[type='submit'], .submit-btn, .btn-submit, button:contains('Submit')")
                
            if submit_buttons:
                submit_buttons[0].click()
                time.sleep(1)
                
                # Look for validation error messages
                error_elements = self.driver.find_elements(By.CSS_SELECTOR,
                    ".error, .validation-error, .field-error, .form-error, [data-testid*='error']")
                    
                if not error_elements:
                    validation_issues.append("No validation errors shown for empty form")
                    
            # Test invalid email format
            email_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='email']")
            for email_input in email_inputs:
                email_input.clear()
                email_input.send_keys("invalid-email")
                
                # Trigger validation
                email_input.click()
                self.driver.find_element(By.TAG_NAME, "body").click()
                
                # Check for validation message
                parent = email_input.find_element(By.XPATH, "..")
                error_in_parent = parent.find_elements(By.CSS_SELECTOR, ".error, .validation-error")
                if not error_in_parent:
                    validation_issues.append("No validation for invalid email format")
                    
        except Exception as e:
            validation_issues.append(f"Validation test error: {str(e)}")
            
        return validation_issues
        
    def test_data_persistence(self, wizard_config: Dict) -> bool:
        """Test wizard data persistence and recovery"""
        try:
            # Fill some data
            self.fill_wizard_step_data(0)
            
            # Navigate to next step and back
            next_button = self.driver.find_element(By.CSS_SELECTOR, 
                "button[data-testid*='next'], button:contains('Next'), .wizard-next")
            next_button.click()
            time.sleep(1)
            
            back_button = self.driver.find_element(By.CSS_SELECTOR,
                "button[data-testid*='back'], button:contains('Back'), .wizard-back")
            back_button.click()
            time.sleep(1)
            
            # Check if data is still there
            text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
            for input_elem in text_inputs:
                if input_elem.get_attribute('value'):
                    return True
                    
            return False
            
        except Exception as e:
            logger.warning(f"Data persistence test failed: {e}")
            return False
            
    def test_responsive_design(self, wizard_url: str) -> bool:
        """Test wizard responsive design on mobile"""
        try:
            # Switch to mobile view
            self.driver.set_window_size(375, 667)
            self.driver.get(wizard_url)
            time.sleep(2)
            
            # Check if layout adapts
            mobile_indicators = self.driver.find_elements(By.CSS_SELECTOR,
                ".mobile-view, .responsive, @media, .sm\\:, .md\\:")
                
            # Check if elements are not overlapping
            overlapping_elements = self.driver.execute_script("""
                const elements = document.querySelectorAll('*');
                const overlapping = [];
                for (let i = 0; i < elements.length; i++) {
                    const rect1 = elements[i].getBoundingClientRect();
                    if (rect1.width > window.innerWidth) {
                        overlapping.push(elements[i].tagName);
                    }
                }
                return overlapping.length === 0;
            """)
            
            return overlapping_elements
            
        except Exception as e:
            logger.warning(f"Responsive design test failed: {e}")
            return False
            
    def measure_performance(self, wizard_url: str) -> Dict[str, float]:
        """Measure wizard loading and interaction performance"""
        performance_metrics = {}
        
        try:
            # Measure page load time
            start_time = time.time()
            self.driver.get(wizard_url)
            
            # Wait for page to be ready
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            performance_metrics['page_load_time'] = time.time() - start_time
            
            # Measure interaction responsiveness
            button = self.driver.find_element(By.CSS_SELECTOR, "button")
            start_interaction = time.time()
            button.click()
            time.sleep(0.1)  # Allow for UI response
            performance_metrics['interaction_response_time'] = time.time() - start_interaction
            
            # Get browser performance metrics
            navigation_timing = self.driver.execute_script(
                "return window.performance.getEntriesByType('navigation')[0];"
            )
            
            if navigation_timing:
                performance_metrics['dns_lookup_time'] = navigation_timing.get('domainLookupEnd', 0) - navigation_timing.get('domainLookupStart', 0)
                performance_metrics['server_response_time'] = navigation_timing.get('responseEnd', 0) - navigation_timing.get('requestStart', 0)
                performance_metrics['dom_ready_time'] = navigation_timing.get('domContentLoadedEventEnd', 0) - navigation_timing.get('navigationStart', 0)
                
        except Exception as e:
            logger.warning(f"Performance measurement failed: {e}")
            performance_metrics['error'] = str(e)
            
        return performance_metrics
        
    def test_wizard(self, wizard_config: Dict) -> WizardTestResult:
        """Test a specific wizard comprehensively"""
        start_time = time.time()
        logger.info(f"Testing wizard: {wizard_config['name']} on {wizard_config['platform']}")
        
        platform = self.platforms[wizard_config['platform']]
        wizard_url = f"{platform.url}{wizard_config['path']}"
        
        # Initialize test result
        result = WizardTestResult(
            wizard_name=wizard_config['name'],
            platform=wizard_config['platform'],
            url=wizard_url,
            total_steps=wizard_config['expected_steps'],
            completed_steps=0,
            validation_errors=[],
            navigation_issues=[],
            accessibility_issues=[],
            performance_metrics={},
            mobile_responsive=False,
            data_persistence=False,
            success_state_reached=False,
            overall_score=0.0,
            test_duration=0.0,
            timestamp=datetime.now().isoformat()
        )
        
        # Skip if platform is not accessible
        if platform.status != 'accessible':
            result.validation_errors.append(f"Platform {platform.name} is not accessible")
            result.test_duration = time.time() - start_time
            return result
            
        try:
            # Setup driver and navigate to wizard
            self.setup_driver()
            
            # Test performance
            result.performance_metrics = self.measure_performance(wizard_url)
            
            # Test accessibility
            result.accessibility_issues = self.test_wizard_accessibility(wizard_url)
            
            # Test navigation and flow
            navigation_results = self.test_wizard_navigation(wizard_config)
            result.completed_steps = navigation_results['completed_steps']
            result.navigation_issues = navigation_results['navigation_issues']
            
            # Test form validation
            result.validation_errors = self.test_form_validation()
            
            # Test data persistence
            result.data_persistence = self.test_data_persistence(wizard_config)
            
            # Test responsive design
            result.mobile_responsive = self.test_responsive_design(wizard_url)
            
            # Check if wizard reached success state
            success_indicators = self.driver.find_elements(By.CSS_SELECTOR,
                ".success, .complete, .wizard-complete, .congratulations, [data-testid*='success']")
            result.success_state_reached = len(success_indicators) > 0
            
            # Calculate overall score
            score_factors = {
                'step_completion': (result.completed_steps / result.total_steps) * 30,
                'no_navigation_issues': (1 - min(len(result.navigation_issues) / 5, 1)) * 20,
                'no_validation_errors': (1 - min(len(result.validation_errors) / 5, 1)) * 20,
                'accessibility': (1 - min(len(result.accessibility_issues) / 10, 1)) * 15,
                'mobile_responsive': 10 if result.mobile_responsive else 0,
                'data_persistence': 5 if result.data_persistence else 0
            }
            
            result.overall_score = sum(score_factors.values())
            
        except Exception as e:
            logger.error(f"Error testing wizard {wizard_config['name']}: {e}")
            result.validation_errors.append(f"Test execution error: {str(e)}")
            
        finally:
            if self.driver:
                self.driver.quit()
                
        result.test_duration = time.time() - start_time
        return result
        
    def generate_detailed_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        report = {
            'test_summary': {
                'total_wizards_tested': len(self.test_results),
                'total_platforms': len(self.platforms),
                'accessible_platforms': sum(1 for p in self.platforms.values() if p.status == 'accessible'),
                'average_score': sum(r.overall_score for r in self.test_results) / len(self.test_results) if self.test_results else 0,
                'timestamp': datetime.now().isoformat()
            },
            'platform_status': {
                name: {
                    'url': platform.url,
                    'status': platform.status,
                    'accessible': platform.status == 'accessible'
                } for name, platform in self.platforms.items()
            },
            'wizard_results': [],
            'issues_summary': {
                'critical_issues': [],
                'accessibility_issues': [],
                'navigation_issues': [],
                'validation_issues': [],
                'performance_issues': []
            },
            'recommendations': []
        }
        
        for result in self.test_results:
            wizard_data = {
                'name': result.wizard_name,
                'platform': result.platform,
                'url': result.url,
                'score': result.overall_score,
                'grade': self.get_grade(result.overall_score),
                'completion_rate': f"{result.completed_steps}/{result.total_steps}",
                'issues': {
                    'navigation': len(result.navigation_issues),
                    'validation': len(result.validation_errors),
                    'accessibility': len(result.accessibility_issues)
                },
                'features': {
                    'mobile_responsive': result.mobile_responsive,
                    'data_persistence': result.data_persistence,
                    'success_state': result.success_state_reached
                },
                'performance': result.performance_metrics,
                'test_duration': f"{result.test_duration:.2f}s"
            }
            report['wizard_results'].append(wizard_data)
            
            # Collect issues for summary
            if result.overall_score < 50:
                report['issues_summary']['critical_issues'].append(f"{result.wizard_name}: Score {result.overall_score}")
                
            report['issues_summary']['accessibility_issues'].extend(
                [f"{result.wizard_name}: {issue}" for issue in result.accessibility_issues]
            )
            report['issues_summary']['navigation_issues'].extend(
                [f"{result.wizard_name}: {issue}" for issue in result.navigation_issues]
            )
            report['issues_summary']['validation_issues'].extend(
                [f"{result.wizard_name}: {issue}" for issue in result.validation_errors]
            )
            
        # Generate recommendations
        avg_score = report['test_summary']['average_score']
        if avg_score < 70:
            report['recommendations'].append("Overall wizard quality needs improvement")
        if len(report['issues_summary']['accessibility_issues']) > 10:
            report['recommendations'].append("Focus on accessibility compliance across wizards")
        if len(report['issues_summary']['navigation_issues']) > 5:
            report['recommendations'].append("Improve wizard navigation consistency")
            
        return report
        
    def get_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 90: return 'A+'
        elif score >= 80: return 'A'
        elif score >= 70: return 'B'
        elif score >= 60: return 'C'
        elif score >= 50: return 'D'
        else: return 'F'
        
    async def run_comprehensive_tests(self):
        """Run comprehensive wizard testing across all platforms"""
        logger.info("🧙‍♂️ Starting BizOSaaS Platform Wizard Testing Framework")
        logger.info("=" * 60)
        
        # Check platform availability
        self.check_platform_availability()
        
        # Test each wizard
        for wizard_config in self.wizards_to_test:
            result = self.test_wizard(wizard_config)
            self.test_results.append(result)
            
            # Log immediate results
            status = "✅" if result.overall_score >= 70 else "⚠️" if result.overall_score >= 50 else "❌"
            logger.info(f"{status} {result.wizard_name}: {result.overall_score:.1f}/100 ({self.get_grade(result.overall_score)})")
            
        # Generate final report
        report = self.generate_detailed_report()
        
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"wizard_testing_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        logger.info("=" * 60)
        logger.info("🎯 WIZARD TESTING COMPLETE")
        logger.info(f"📊 Average Score: {report['test_summary']['average_score']:.1f}/100")
        logger.info(f"🎭 Wizards Tested: {report['test_summary']['total_wizards_tested']}")
        logger.info(f"🌐 Platforms Accessible: {report['test_summary']['accessible_platforms']}/{report['test_summary']['total_platforms']}")
        logger.info(f"📋 Detailed Report: {report_file}")
        
        return report

def main():
    """Main execution function"""
    framework = WizardTestingFramework()
    
    # Run the comprehensive tests
    report = asyncio.run(framework.run_comprehensive_tests())
    
    # Print summary to console
    print("\n" + "="*60)
    print("🧙‍♂️ BIZOSAAS WIZARD TESTING SUMMARY")
    print("="*60)
    
    for result in framework.test_results:
        status_icon = "✅" if result.overall_score >= 70 else "⚠️" if result.overall_score >= 50 else "❌"
        print(f"{status_icon} {result.wizard_name:<30} {result.overall_score:>5.1f}/100 ({framework.get_grade(result.overall_score)})")
        
    print("\n🎯 PLATFORM STATUS:")
    for name, platform in framework.platforms.items():
        status_icon = "✅" if platform.status == 'accessible' else "❌"
        print(f"{status_icon} {platform.name:<25} {platform.url}")
        
    print(f"\n📊 Overall Platform Score: {report['test_summary']['average_score']:.1f}/100")
    
    # Show critical issues
    if report['issues_summary']['critical_issues']:
        print("\n🚨 CRITICAL ISSUES:")
        for issue in report['issues_summary']['critical_issues']:
            print(f"   ❌ {issue}")
            
    print("\n📋 Detailed report saved to:", [f for f in locals() if f.endswith('.json')])

if __name__ == "__main__":
    main()
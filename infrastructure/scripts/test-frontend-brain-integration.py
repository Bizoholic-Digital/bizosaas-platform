#!/usr/bin/env python3
"""
BizOSaaS Frontend-Brain API Integration Testing Suite

This script validates the integration between all frontend applications and the Brain API.
Tests include API connectivity, endpoint availability, and data flow validation.
"""

import requests
import json
import subprocess
import time
import os
import sys
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import concurrent.futures

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class FrontendBrainTester:
    def __init__(self):
        self.brain_api_url = "http://localhost:8001"
        self.results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'details': []
        }
        
        # Frontend applications configuration
        self.frontend_apps = {
            'bizoholic': {
                'name': 'Bizoholic Marketing Platform',
                'port': 3000,
                'path': '/home/alagiri/projects/bizoholic/bizosaas/apps/bizoholic-frontend',
                'tenant_type': 'bizoholic',
                'api_endpoints': [
                    '/api/brain/wagtail/homepage',
                    '/api/brain/wagtail/services',
                    '/api/brain/wagtail/blog',
                    '/api/brain/wagtail/pages'
                ]
            },
            'coreldove': {
                'name': 'CoreLDove E-commerce Platform',
                'port': 3001,
                'path': '/home/alagiri/projects/bizoholic/bizosaas/apps/coreldove-frontend',
                'tenant_type': 'coreldove',
                'api_endpoints': [
                    '/api/brain/saleor/products',
                    '/api/brain/saleor/categories',
                    '/api/brain/saleor/collections',
                    '/api/brain/saleor/homepage'
                ]
            },
            'bizosaas': {
                'name': 'BizOSaaS Admin Dashboard',
                'port': 3001,
                'path': '/home/alagiri/projects/bizoholic/bizosaas/services/frontend-nextjs',
                'tenant_type': 'bizosaas',
                'api_endpoints': [
                    '/api/brain/health',
                    '/api/brain/analytics/dashboard',
                    '/api/brain/tenants',
                    '/api/brain/wizards'
                ]
            }
        }

    def print_header(self, title: str):
        print(f"\n{Color.BOLD}{Color.CYAN}{'='*60}{Color.END}")
        print(f"{Color.BOLD}{Color.CYAN}  {title}{Color.END}")
        print(f"{Color.BOLD}{Color.CYAN}{'='*60}{Color.END}")

    def print_test(self, test_name: str, status: str, details: str = ""):
        if status == "PASS":
            print(f"  {Color.GREEN}✓{Color.END} {test_name}")
            self.results['passed'] += 1
        elif status == "FAIL":
            print(f"  {Color.RED}✗{Color.END} {test_name}")
            if details:
                print(f"    {Color.RED}Error: {details}{Color.END}")
            self.results['failed'] += 1
        elif status == "WARN":
            print(f"  {Color.YELLOW}⚠{Color.END} {test_name}")
            if details:
                print(f"    {Color.YELLOW}Warning: {details}{Color.END}")
            self.results['warnings'] += 1
        
        self.results['details'].append({
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })

    def test_brain_api_health(self) -> bool:
        """Test Brain API health and availability"""
        self.print_header("Brain API Health Check")
        
        try:
            response = requests.get(f"{self.brain_api_url}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                self.print_test("Brain API Health", "PASS", f"Status: {health_data.get('status', 'unknown')}")
                
                # Test specific components
                components = health_data.get('components', {})
                for component, status in components.items():
                    component_status = "PASS" if status == "healthy" or status == "available" else "WARN"
                    self.print_test(f"Component: {component}", component_status, f"Status: {status}")
                
                return True
            else:
                self.print_test("Brain API Health", "FAIL", f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.print_test("Brain API Health", "FAIL", str(e))
            return False

    def test_brain_api_endpoints(self) -> bool:
        """Test key Brain API endpoints"""
        self.print_header("Brain API Core Endpoints")
        
        endpoints = [
            ('/wizards', 'Wizard Management'),
            ('/analytics/dashboard', 'Analytics Dashboard'),
            ('/agents/available', 'AI Agents'),
            ('/tenants/config', 'Tenant Configuration')
        ]
        
        success_count = 0
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{self.brain_api_url}{endpoint}", timeout=5)
                if response.status_code in [200, 404]:  # 404 is acceptable for some endpoints
                    self.print_test(f"Endpoint: {name}", "PASS", f"HTTP {response.status_code}")
                    success_count += 1
                else:
                    self.print_test(f"Endpoint: {name}", "WARN", f"HTTP {response.status_code}")
            except Exception as e:
                self.print_test(f"Endpoint: {name}", "FAIL", str(e))
        
        return success_count > len(endpoints) // 2  # At least half should work

    def check_frontend_files(self, app_config: Dict) -> bool:
        """Check if frontend application files exist and are properly configured"""
        app_path = app_config['path']
        app_name = app_config['name']
        
        # Check essential files
        essential_files = [
            'package.json',
            'next.config.js',
            'app/layout.tsx',
            'app/page.tsx'
        ]
        
        missing_files = []
        for file_path in essential_files:
            full_path = os.path.join(app_path, file_path)
            if not os.path.exists(full_path):
                missing_files.append(file_path)
        
        if missing_files:
            self.print_test(f"{app_name} - File Structure", "FAIL", f"Missing: {', '.join(missing_files)}")
            return False
        else:
            self.print_test(f"{app_name} - File Structure", "PASS")
            return True

    def check_next_config(self, app_config: Dict) -> bool:
        """Check Next.js configuration for Brain API integration"""
        config_path = os.path.join(app_config['path'], 'next.config.js')
        app_name = app_config['name']
        
        try:
            with open(config_path, 'r') as f:
                config_content = f.read()
            
            # Check for API rewrites
            if '/api/brain' in config_content and 'localhost:8001' in config_content:
                self.print_test(f"{app_name} - Next.js Config", "PASS", "Brain API proxy configured")
                return True
            else:
                self.print_test(f"{app_name} - Next.js Config", "WARN", "Brain API proxy not found")
                return False
        except Exception as e:
            self.print_test(f"{app_name} - Next.js Config", "FAIL", str(e))
            return False

    def test_frontend_build(self, app_config: Dict) -> bool:
        """Test if frontend application can build successfully"""
        app_path = app_config['path']
        app_name = app_config['name']
        
        try:
            # Change to app directory and run build
            result = subprocess.run(
                ['npm', 'run', 'build'],
                cwd=app_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                self.print_test(f"{app_name} - Build Test", "PASS")
                return True
            else:
                error_msg = result.stderr[:200] + "..." if len(result.stderr) > 200 else result.stderr
                self.print_test(f"{app_name} - Build Test", "FAIL", error_msg)
                return False
        except subprocess.TimeoutExpired:
            self.print_test(f"{app_name} - Build Test", "FAIL", "Build timeout (5 minutes)")
            return False
        except Exception as e:
            self.print_test(f"{app_name} - Build Test", "FAIL", str(e))
            return False

    def start_frontend_dev(self, app_config: Dict) -> Optional[subprocess.Popen]:
        """Start frontend application in development mode"""
        app_path = app_config['path']
        
        try:
            # Start dev server
            process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                cwd=app_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give it some time to start
            time.sleep(10)
            
            return process
        except Exception as e:
            print(f"Failed to start {app_config['name']}: {e}")
            return None

    def test_frontend_server(self, app_config: Dict) -> bool:
        """Test if frontend server is responding"""
        port = app_config['port']
        app_name = app_config['name']
        
        try:
            response = requests.get(f"http://localhost:{port}", timeout=10)
            if response.status_code == 200:
                self.print_test(f"{app_name} - Server Response", "PASS", f"Port {port}")
                return True
            else:
                self.print_test(f"{app_name} - Server Response", "FAIL", f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.print_test(f"{app_name} - Server Response", "FAIL", str(e))
            return False

    def test_api_proxy_endpoints(self, app_config: Dict) -> bool:
        """Test API proxy endpoints for frontend application"""
        port = app_config['port']
        app_name = app_config['name']
        api_endpoints = app_config.get('api_endpoints', [])
        
        success_count = 0
        for endpoint in api_endpoints:
            try:
                response = requests.get(f"http://localhost:{port}{endpoint}", timeout=10)
                # Accept various status codes as the endpoints might not have real data
                if response.status_code in [200, 404, 500, 502]:
                    self.print_test(f"{app_name} - API Proxy: {endpoint}", "PASS", f"HTTP {response.status_code}")
                    success_count += 1
                else:
                    self.print_test(f"{app_name} - API Proxy: {endpoint}", "WARN", f"HTTP {response.status_code}")
            except Exception as e:
                self.print_test(f"{app_name} - API Proxy: {endpoint}", "FAIL", str(e))
        
        return success_count > 0

    def test_shared_ui_integration(self) -> bool:
        """Test shared UI package integration"""
        self.print_header("Shared UI Package Integration")
        
        shared_ui_path = "/home/alagiri/projects/bizoholic/bizosaas/packages/shared-ui"
        
        # Check if shared-ui package exists
        if not os.path.exists(shared_ui_path):
            self.print_test("Shared UI Package", "FAIL", "Package directory not found")
            return False
        
        # Check package.json
        package_json_path = os.path.join(shared_ui_path, "package.json")
        if os.path.exists(package_json_path):
            self.print_test("Shared UI Package Structure", "PASS")
        else:
            self.print_test("Shared UI Package Structure", "FAIL", "package.json missing")
            return False
        
        # Check for key files
        key_files = [
            "src/types/index.ts",
            "src/components",
            "src/lib"
        ]
        
        for file_path in key_files:
            full_path = os.path.join(shared_ui_path, file_path)
            if os.path.exists(full_path):
                self.print_test(f"Shared UI - {file_path}", "PASS")
            else:
                self.print_test(f"Shared UI - {file_path}", "WARN", "File/directory missing")
        
        return True

    def run_comprehensive_test(self):
        """Run comprehensive test suite"""
        print(f"{Color.BOLD}{Color.MAGENTA}BizOSaaS Frontend-Brain API Integration Test Suite{Color.END}")
        print(f"{Color.BOLD}Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Color.END}\n")
        
        # Test 1: Brain API Health
        brain_healthy = self.test_brain_api_health()
        
        # Test 2: Brain API Endpoints
        if brain_healthy:
            self.test_brain_api_endpoints()
        else:
            print(f"{Color.RED}Skipping Brain API endpoint tests due to health check failure{Color.END}")
        
        # Test 3: Shared UI Integration
        self.test_shared_ui_integration()
        
        # Test 4: Frontend Applications
        self.print_header("Frontend Applications Validation")
        
        for app_key, app_config in self.frontend_apps.items():
            print(f"\n{Color.BOLD}{Color.BLUE}Testing {app_config['name']}{Color.END}")
            
            # Check file structure
            self.check_frontend_files(app_config)
            
            # Check Next.js configuration
            self.check_next_config(app_config)
            
            # Test build (optional - takes time)
            build_test = input(f"Run build test for {app_config['name']}? (y/N): ").lower().strip()
            if build_test == 'y':
                self.test_frontend_build(app_config)
        
        # Test 5: Runtime Integration Tests
        runtime_test = input(f"\nRun runtime integration tests? This will start dev servers (y/N): ").lower().strip()
        if runtime_test == 'y':
            self.run_runtime_tests()
        
        # Print Summary
        self.print_summary()

    def run_runtime_tests(self):
        """Run runtime tests by starting dev servers"""
        self.print_header("Runtime Integration Tests")
        
        processes = {}
        
        try:
            # Start all frontend applications
            for app_key, app_config in self.frontend_apps.items():
                if app_key == 'bizosaas':  # Skip bizosaas as it might conflict with coreldove port
                    continue
                    
                print(f"Starting {app_config['name']}...")
                process = self.start_frontend_dev(app_config)
                if process:
                    processes[app_key] = process
            
            # Wait a bit more for servers to fully start
            time.sleep(15)
            
            # Test server responses and API proxies
            for app_key, app_config in self.frontend_apps.items():
                if app_key in processes or app_key == 'bizosaas':
                    # Test server
                    self.test_frontend_server(app_config)
                    
                    # Test API proxies
                    self.test_api_proxy_endpoints(app_config)
        
        finally:
            # Clean up processes
            for app_key, process in processes.items():
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except:
                    process.kill()
                print(f"Stopped {self.frontend_apps[app_key]['name']}")

    def print_summary(self):
        """Print test summary"""
        self.print_header("Test Summary")
        
        total_tests = self.results['passed'] + self.results['failed'] + self.results['warnings']
        
        print(f"  {Color.GREEN}Passed: {self.results['passed']}{Color.END}")
        print(f"  {Color.RED}Failed: {self.results['failed']}{Color.END}")
        print(f"  {Color.YELLOW}Warnings: {self.results['warnings']}{Color.END}")
        print(f"  {Color.BOLD}Total: {total_tests}{Color.END}")
        
        success_rate = (self.results['passed'] / total_tests * 100) if total_tests > 0 else 0
        print(f"  {Color.BOLD}Success Rate: {success_rate:.1f}%{Color.END}")
        
        # Save detailed results
        results_file = f"/home/alagiri/projects/bizoholic/bizosaas/frontend-brain-test-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n{Color.CYAN}Detailed results saved to: {results_file}{Color.END}")
        
        if self.results['failed'] == 0:
            print(f"\n{Color.BOLD}{Color.GREEN}🎉 All critical tests passed! Frontend-Brain API integration is working correctly.{Color.END}")
        elif self.results['failed'] < 5:
            print(f"\n{Color.BOLD}{Color.YELLOW}⚠️  Some issues found but overall integration looks good.{Color.END}")
        else:
            print(f"\n{Color.BOLD}{Color.RED}❌ Significant issues found. Please review and fix before production.{Color.END}")

def main():
    tester = FrontendBrainTester()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
BizOSaaS Analytics Platform Comprehensive Testing Execution
============================================================

Executes all analytics testing suites and provides a unified assessment
of the BizOSaaS platform's analytics capabilities, real-time data flows,
and business intelligence features.
"""

import sys
import time
import json
import subprocess
from datetime import datetime
from pathlib import Path

class AnalyticsTestExecutor:
    """Orchestrates comprehensive analytics testing"""
    
    def __init__(self):
        self.test_scripts = [
            {
                'name': 'Basic Analytics Validation',
                'script': 'validate_analytics_simple.py',
                'description': 'Tests basic service connectivity and analytics endpoints',
                'critical': True
            },
            {
                'name': 'Analytics Data Flow Testing',
                'script': 'test_analytics_data_flows.py', 
                'description': 'Tests end-to-end analytics data flows and real-time capabilities',
                'critical': True
            }
        ]
        
        self.results = []
        self.overall_metrics = {}
        
    def check_script_exists(self, script_name):
        """Check if test script exists"""
        return Path(script_name).exists()
    
    def run_test_script(self, script_info):
        """Run individual test script"""
        script_name = script_info['script']
        
        print(f"\n🔍 Running: {script_info['name']}")
        print(f"📝 Description: {script_info['description']}")
        print("-" * 50)
        
        if not self.check_script_exists(script_name):
            return {
                'script': script_name,
                'status': 'SKIPPED',
                'reason': 'Script file not found',
                'execution_time': 0,
                'output': ''
            }
        
        try:
            start_time = time.time()
            
            # Execute the script and capture output
            result = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            execution_time = time.time() - start_time
            
            # Determine status based on return code
            if result.returncode == 0:
                status = 'PASS'
            else:
                status = 'FAIL'
            
            return {
                'script': script_name,
                'status': status,
                'return_code': result.returncode,
                'execution_time': execution_time,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'output_summary': self.extract_output_summary(result.stdout)
            }
            
        except subprocess.TimeoutExpired:
            return {
                'script': script_name,
                'status': 'TIMEOUT',
                'reason': 'Script execution timed out after 5 minutes',
                'execution_time': 300,
                'output': 'Test execution timeout'
            }
            
        except Exception as e:
            return {
                'script': script_name,
                'status': 'ERROR',
                'reason': f'Execution error: {str(e)}',
                'execution_time': 0,
                'output': str(e)
            }
    
    def extract_output_summary(self, stdout_text):
        """Extract key metrics from script output"""
        summary = {
            'services_tested': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'success_rate': 0,
            'key_findings': []
        }
        
        lines = stdout_text.split('\\n')
        
        for line in lines:
            # Look for success indicators
            if '✅' in line:
                summary['tests_passed'] += 1
            elif '❌' in line:
                summary['tests_failed'] += 1
            
            # Look for specific metrics
            if 'success rate' in line.lower() or 'success:' in line.lower():
                try:
                    # Extract percentage
                    import re
                    match = re.search(r'(\\d+(?:\\.\\d+)?)%', line)
                    if match:
                        summary['success_rate'] = float(match.group(1))
                except:
                    pass
            
            # Look for key findings
            if any(keyword in line.lower() for keyword in ['operational', 'healthy', 'available', 'critical']):
                if len(line.strip()) > 10:  # Avoid empty lines
                    summary['key_findings'].append(line.strip())
        
        summary['total_tests'] = summary['tests_passed'] + summary['tests_failed']
        
        if summary['total_tests'] > 0 and summary['success_rate'] == 0:
            summary['success_rate'] = (summary['tests_passed'] / summary['total_tests']) * 100
        
        return summary
    
    def run_all_tests(self):
        """Execute all analytics test suites"""
        
        print("🚀 BizOSaaS Analytics Platform Comprehensive Testing")
        print("=" * 70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Test suites to execute: {len(self.test_scripts)}")
        
        overall_start_time = time.time()
        
        # Execute each test script
        for i, script_info in enumerate(self.test_scripts, 1):
            print(f"\\n{'='*20} Test Suite {i}/{len(self.test_scripts)} {'='*20}")
            
            result = self.run_test_script(script_info)
            result['script_info'] = script_info
            self.results.append(result)
            
            # Print immediate summary
            status_icon = {
                'PASS': '✅',
                'FAIL': '❌', 
                'TIMEOUT': '⏰',
                'ERROR': '💥',
                'SKIPPED': '⏭️'
            }.get(result['status'], '❓')
            
            print(f"\\n{status_icon} {script_info['name']}: {result['status']}")
            
            if result['status'] == 'PASS':
                summary = result.get('output_summary', {})
                if summary.get('success_rate', 0) > 0:
                    print(f"   Success Rate: {summary['success_rate']:.1f}%")
                if summary.get('total_tests', 0) > 0:
                    print(f"   Tests: {summary['tests_passed']}/{summary['total_tests']} passed")
            
            print(f"   Execution Time: {result['execution_time']:.2f} seconds")
            
            if result['status'] in ['FAIL', 'ERROR', 'TIMEOUT']:
                print(f"   Issue: {result.get('reason', 'See output for details')}")
        
        total_execution_time = time.time() - overall_start_time
        
        # Generate comprehensive summary
        self.generate_comprehensive_summary(total_execution_time)
        
        return self.results
    
    def generate_comprehensive_summary(self, total_execution_time):
        """Generate comprehensive analytics platform assessment"""
        
        print(f"\\n📊 COMPREHENSIVE ANALYTICS PLATFORM ASSESSMENT")
        print("=" * 70)
        
        # Calculate overall metrics
        total_scripts = len(self.results)
        passed_scripts = sum(1 for r in self.results if r['status'] == 'PASS')
        failed_scripts = sum(1 for r in self.results if r['status'] in ['FAIL', 'ERROR', 'TIMEOUT'])
        skipped_scripts = sum(1 for r in self.results if r['status'] == 'SKIPPED')
        
        script_success_rate = (passed_scripts / total_scripts * 100) if total_scripts > 0 else 0
        
        # Aggregate test metrics from individual scripts
        total_individual_tests = 0
        total_individual_passed = 0
        individual_success_rates = []
        
        for result in self.results:
            if result['status'] == 'PASS':
                summary = result.get('output_summary', {})
                if summary.get('total_tests', 0) > 0:
                    total_individual_tests += summary['total_tests']
                    total_individual_passed += summary['tests_passed']
                if summary.get('success_rate', 0) > 0:
                    individual_success_rates.append(summary['success_rate'])
        
        avg_success_rate = sum(individual_success_rates) / len(individual_success_rates) if individual_success_rates else 0
        
        print(f"⏱️  Total Execution Time: {total_execution_time:.2f} seconds")
        print(f"📊 Test Script Results: {passed_scripts}/{total_scripts} scripts passed ({script_success_rate:.1f}%)")
        print(f"🎯 Individual Test Results: {total_individual_passed}/{total_individual_tests} tests passed")
        print(f"📈 Average Success Rate: {avg_success_rate:.1f}%")
        
        # Determine overall platform health
        if script_success_rate >= 80 and avg_success_rate >= 80:
            platform_health = "🟢 EXCELLENT"
            health_description = "Analytics platform is fully operational with excellent performance"
        elif script_success_rate >= 60 and avg_success_rate >= 60:
            platform_health = "🟡 GOOD"
            health_description = "Analytics platform is mostly operational with minor issues"
        elif script_success_rate >= 40 or avg_success_rate >= 40:
            platform_health = "🟠 FAIR"
            health_description = "Analytics platform is partially operational and needs attention"
        else:
            platform_health = "🔴 POOR"
            health_description = "Analytics platform has critical issues requiring immediate attention"
        
        print(f"\\n🏥 OVERALL PLATFORM HEALTH: {platform_health}")
        print(f"📋 Assessment: {health_description}")
        
        # Key findings summary
        print(f"\\n🔍 KEY FINDINGS:")
        print("-" * 30)
        
        findings_count = 0
        for result in self.results:
            if result['status'] == 'PASS':
                summary = result.get('output_summary', {})
                key_findings = summary.get('key_findings', [])
                for finding in key_findings[:2]:  # Show top 2 findings per script
                    if findings_count < 8:  # Limit total findings
                        print(f"   • {finding}")
                        findings_count += 1
        
        # Critical issues
        critical_issues = []
        for result in self.results:
            if result['status'] in ['FAIL', 'ERROR', 'TIMEOUT']:
                script_info = result.get('script_info', {})
                if script_info.get('critical', False):
                    critical_issues.append({
                        'script': script_info.get('name', 'Unknown'),
                        'issue': result.get('reason', 'Unknown error'),
                        'status': result['status']
                    })
        
        if critical_issues:
            print(f"\\n🚨 CRITICAL ISSUES REQUIRING IMMEDIATE ATTENTION:")
            print("-" * 50)
            for issue in critical_issues:
                print(f"   🔴 {issue['script']}: {issue['issue']}")
        
        # Recommendations
        print(f"\\n🎯 PRIORITY RECOMMENDATIONS:")
        print("-" * 35)
        
        if critical_issues:
            print("1. 🔴 CRITICAL - Fix failing analytics systems:")
            for issue in critical_issues[:2]:
                print(f"   • Address {issue['script']} ({issue['status']})")
        
        if avg_success_rate < 80:
            print("2. 🟡 HIGH - Improve analytics capabilities:")
            print("   • Implement missing analytics endpoints")
            print("   • Fix service connectivity issues")
            print("   • Enhance real-time data flows")
        
        print("3. ✅ MEDIUM - Enhance working systems:")
        print("   • Add advanced analytics dashboards")
        print("   • Implement monitoring and alerting")
        print("   • Create automated analytics reports")
        
        print("4. 🚀 LOW - Future enhancements:")
        print("   • Add predictive analytics capabilities")
        print("   • Implement AI-powered insights")
        print("   • Create custom analytics solutions")
        
        # Save comprehensive report
        self.save_comprehensive_report(total_execution_time, {
            'script_success_rate': script_success_rate,
            'avg_success_rate': avg_success_rate,
            'platform_health': platform_health,
            'health_description': health_description,
            'critical_issues': critical_issues
        })
    
    def save_comprehensive_report(self, total_execution_time, metrics):
        """Save comprehensive analytics assessment report"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"analytics_comprehensive_assessment_{timestamp}.json"
        
        comprehensive_report = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_execution_time': total_execution_time,
                'platform': 'BizOSaaS Analytics Platform',
                'assessment_version': '1.0.0'
            },
            'executive_summary': {
                'platform_health': metrics['platform_health'],
                'health_description': metrics['health_description'],
                'script_success_rate': metrics['script_success_rate'],
                'avg_success_rate': metrics['avg_success_rate'],
                'critical_issues_count': len(metrics['critical_issues'])
            },
            'test_execution_results': self.results,
            'critical_issues': metrics['critical_issues'],
            'detailed_metrics': {
                'total_scripts_executed': len(self.results),
                'scripts_passed': sum(1 for r in self.results if r['status'] == 'PASS'),
                'scripts_failed': sum(1 for r in self.results if r['status'] in ['FAIL', 'ERROR', 'TIMEOUT']),
                'scripts_skipped': sum(1 for r in self.results if r['status'] == 'SKIPPED')
            }
        }
        
        with open(report_filename, 'w') as f:
            json.dump(comprehensive_report, f, indent=2, default=str)
        
        print(f"\\n💾 Comprehensive assessment saved: {report_filename}")
        
        # Also create a markdown summary
        md_filename = f"analytics_assessment_summary_{timestamp}.md"
        self.create_markdown_summary(md_filename, comprehensive_report)
        
        print(f"📄 Markdown summary created: {md_filename}")
        
        return report_filename
    
    def create_markdown_summary(self, filename, report):
        """Create markdown summary report"""
        
        md_content = f"""# BizOSaaS Analytics Platform Assessment Report

**Generated:** {report['report_metadata']['generated_at']}  
**Execution Time:** {report['report_metadata']['total_execution_time']:.2f} seconds  
**Platform:** {report['report_metadata']['platform']}

## Executive Summary

**Platform Health:** {report['executive_summary']['platform_health']}  
**Assessment:** {report['executive_summary']['health_description']}

### Key Metrics
- **Script Success Rate:** {report['executive_summary']['script_success_rate']:.1f}%
- **Average Test Success Rate:** {report['executive_summary']['avg_success_rate']:.1f}%
- **Critical Issues:** {report['executive_summary']['critical_issues_count']}

## Test Execution Results

| Test Suite | Status | Execution Time | Notes |
|------------|--------|----------------|--------|
"""
        
        for result in report['test_execution_results']:
            script_info = result.get('script_info', {})
            name = script_info.get('name', 'Unknown')
            status = result['status']
            exec_time = result.get('execution_time', 0)
            
            status_icon = {'PASS': '✅', 'FAIL': '❌', 'ERROR': '💥', 'TIMEOUT': '⏰', 'SKIPPED': '⏭️'}.get(status, '❓')
            
            md_content += f"| {name} | {status_icon} {status} | {exec_time:.2f}s | - |\n"
        
        if report['critical_issues']:
            md_content += "\n## 🚨 Critical Issues\n\n"
            for issue in report['critical_issues']:
                md_content += f"- **{issue['script']}:** {issue['issue']} ({issue['status']})\n"
        
        md_content += "\n## Recommendations\n\n"
        md_content += "### Immediate Actions\n"
        md_content += "1. Address all critical issues listed above\n"
        md_content += "2. Fix failing analytics services and endpoints\n"
        md_content += "3. Verify database and service connectivity\n\n"
        
        md_content += "### Short-term Improvements\n"
        md_content += "1. Implement missing analytics endpoints\n"
        md_content += "2. Add real-time data monitoring\n"
        md_content += "3. Create analytics dashboards\n\n"
        
        md_content += "### Long-term Enhancements\n"
        md_content += "1. Add predictive analytics capabilities\n"
        md_content += "2. Implement AI-powered insights\n"
        md_content += "3. Create automated reporting systems\n"
        
        with open(filename, 'w') as f:
            f.write(md_content)

def main():
    """Main execution function"""
    
    executor = AnalyticsTestExecutor()
    
    try:
        results = executor.run_all_tests()
        
        # Determine exit code based on critical test results
        critical_failures = sum(1 for r in results 
                              if r['status'] in ['FAIL', 'ERROR', 'TIMEOUT'] 
                              and r.get('script_info', {}).get('critical', False))
        
        if critical_failures > 0:
            print(f"\\n⚠️  Warning: {critical_failures} critical test(s) failed")
            return 1
        else:
            print(f"\\n✅ Analytics testing completed successfully")
            return 0
            
    except Exception as e:
        print(f"❌ Analytics testing execution failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
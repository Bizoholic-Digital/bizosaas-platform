#!/usr/bin/env python3
"""
Analytics Test Runner for BizOSaaS Platform
Executes comprehensive analytics validation with proper error handling and logging
"""

import sys
import os
import subprocess
import asyncio
from datetime import datetime

def check_dependencies():
    """Check if required dependencies are available"""
    required_modules = ['aiohttp', 'psycopg2', 'redis', 'pandas', 'numpy']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            if module == 'psycopg2':
                try:
                    __import__('psycopg2-binary')
                except ImportError:
                    missing.append(module)
            else:
                missing.append(module)
    
    return missing

def install_dependencies(missing_modules):
    """Install missing dependencies"""
    if not missing_modules:
        return True
    
    print(f"Installing missing dependencies: {', '.join(missing_modules)}")
    
    try:
        for module in missing_modules:
            if module == 'psycopg2':
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'])
            else:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False

async def main():
    """Main execution with dependency management"""
    
    print("🔍 BizOSaaS Analytics Test Suite Runner")
    print("=" * 50)
    
    # Check and install dependencies
    missing = check_dependencies()
    if missing:
        print(f"⚠️  Missing dependencies: {', '.join(missing)}")
        if not install_dependencies(missing):
            print("❌ Failed to install dependencies. Please install manually:")
            print("pip install aiohttp psycopg2-binary redis pandas numpy")
            return 1
    
    print("✅ All dependencies available")
    
    # Import and run the test suite
    try:
        from analytics_comprehensive_test_suite import BizOSaaSAnalyticsTestSuite
        
        test_suite = BizOSaaSAnalyticsTestSuite()
        
        print("\n🚀 Starting comprehensive analytics validation...")
        start_time = datetime.now()
        
        report = await test_suite.run_all_tests()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n✅ Analytics test suite completed!")
        print(f"⏱️  Total execution time: {duration:.2f} seconds")
        print(f"📊 Success rate: {report['executive_summary']['success_rate']:.1f}%")
        print(f"🎯 Overall status: {report['executive_summary']['overall_status']}")
        
        # Print key findings
        print(f"\n🔍 Key Findings:")
        for finding in report['executive_summary']['key_findings']:
            print(f"   {finding}")
        
        # Print platform health
        print(f"\n🏥 Platform Health:")
        for component, status in report['platform_health'].items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {component.replace('_', ' ').title()}: {'Operational' if status else 'Needs Attention'}")
        
        # Print high priority recommendations
        high_priority_recs = [r for r in report['recommendations'] if r['priority'] == 'HIGH']
        if high_priority_recs:
            print(f"\n🚨 High Priority Recommendations:")
            for rec in high_priority_recs[:3]:
                print(f"   • {rec['category']}: {rec['action']}")
        
        print(f"\n📄 Detailed reports saved with timestamp: {datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        return 0
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed correctly.")
        return 1
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
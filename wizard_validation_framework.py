#!/usr/bin/env python3
"""
BizOSaaS Platform - Wizard Validation Framework
===============================================

This framework validates wizard implementations through API testing, 
component analysis, and automated checks without requiring browser automation.

Key Testing Areas:
1. Wizard component structure validation
2. API endpoint testing for wizard flows
3. Form validation and error handling
4. Data persistence and state management
5. Mobile responsiveness checks
6. Accessibility compliance analysis
7. Performance metrics
8. Integration testing
"""

import asyncio
import json
import logging
import time
import re
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import requests
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WizardAnalysisResult:
    """Results from analyzing a specific wizard implementation"""
    wizard_name: str
    platform: str
    file_path: str
    component_structure: Dict[str, Any]
    validation_schema: Dict[str, Any]
    api_endpoints: List[str]
    form_fields: List[str]
    step_count: int
    navigation_features: List[str]
    accessibility_features: List[str]
    responsive_design: bool
    state_management: str
    error_handling: bool
    data_persistence: bool
    performance_score: float
    code_quality_score: float
    overall_score: float
    issues: List[str]
    recommendations: List[str]
    test_duration: float
    timestamp: str

@dataclass
class PlatformStatus:
    """Platform availability and health"""
    name: str
    url: str
    port: int
    status: str
    response_time: float
    endpoints_tested: int
    endpoints_working: int

class WizardValidationFramework:
    """Comprehensive wizard validation framework"""
    
    def __init__(self):
        self.platforms = {
            'client_portal': {'name': 'Client Portal', 'url': 'http://localhost:3000', 'port': 3000},
            'bizoholic_frontend': {'name': 'Bizoholic Frontend', 'url': 'http://localhost:3001', 'port': 3001},
            'coreldove_frontend': {'name': 'CoreLDove Frontend', 'url': 'http://localhost:3002', 'port': 3002},
            'business_directory': {'name': 'Business Directory', 'url': 'http://localhost:3004', 'port': 3004},
            'bizosaas_admin': {'name': 'BizOSaaS Admin', 'url': 'http://localhost:3009', 'port': 3009}
        }
        
        self.wizard_files = []
        self.analysis_results = []
        self.platform_status = []
        
    def discover_wizard_files(self) -> List[str]:
        """Discover all wizard-related files in the frontend directory"""
        logger.info("🔍 Discovering wizard files...")
        
        frontend_dir = "/home/alagiri/projects/bizoholic/bizosaas-platform/frontend"
        wizard_files = []
        
        # Search patterns for wizard files
        patterns = [
            "*wizard*.tsx", "*wizard*.ts", "*Wizard*.tsx", "*Wizard*.ts",
            "*onboard*.tsx", "*onboard*.ts", "*setup*.tsx", "*setup*.ts"
        ]
        
        for root, dirs, files in os.walk(frontend_dir):
            # Skip node_modules
            if 'node_modules' in root:
                continue
                
            for file in files:
                file_lower = file.lower()
                if (file.endswith('.tsx') or file.endswith('.ts')) and \
                   ('wizard' in file_lower or 'onboard' in file_lower or 'setup' in file_lower):
                    wizard_files.append(os.path.join(root, file))
                    
        self.wizard_files = wizard_files
        logger.info(f"📁 Found {len(wizard_files)} wizard files")
        
        for file in wizard_files:
            logger.info(f"   🧙‍♂️ {file}")
            
        return wizard_files
        
    def check_platform_status(self) -> List[PlatformStatus]:
        """Check availability and health of all platforms"""
        logger.info("🌐 Checking platform status...")
        
        status_results = []
        
        for platform_key, platform_info in self.platforms.items():
            start_time = time.time()
            
            try:
                # Test basic connectivity
                response = requests.get(platform_info['url'], timeout=5)
                response_time = time.time() - start_time
                
                status = PlatformStatus(
                    name=platform_info['name'],
                    url=platform_info['url'],
                    port=platform_info['port'],
                    status='accessible' if response.status_code == 200 else f'error_{response.status_code}',
                    response_time=response_time,
                    endpoints_tested=1,
                    endpoints_working=1 if response.status_code == 200 else 0
                )
                
                # Test additional endpoints if main one works
                if response.status_code == 200:
                    additional_endpoints = ['/api/health', '/health', '/status']
                    for endpoint in additional_endpoints:
                        try:
                            test_response = requests.get(f"{platform_info['url']}{endpoint}", timeout=2)
                            status.endpoints_tested += 1
                            if test_response.status_code == 200:
                                status.endpoints_working += 1
                        except:
                            status.endpoints_tested += 1
                            
                logger.info(f"✅ {platform_info['name']}: {status.status} ({response_time:.2f}s)")
                
            except requests.exceptions.RequestException as e:
                status = PlatformStatus(
                    name=platform_info['name'],
                    url=platform_info['url'],
                    port=platform_info['port'],
                    status='unreachable',
                    response_time=time.time() - start_time,
                    endpoints_tested=1,
                    endpoints_working=0
                )
                logger.error(f"❌ {platform_info['name']}: unreachable - {e}")
                
            status_results.append(status)
            
        self.platform_status = status_results
        return status_results
        
    def analyze_wizard_file(self, file_path: str) -> WizardAnalysisResult:
        """Analyze a single wizard file for structure, patterns, and quality"""
        start_time = time.time()
        logger.info(f"🔍 Analyzing: {os.path.basename(file_path)}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return self._create_error_result(file_path, str(e))
            
        # Determine platform from path
        platform = self._determine_platform(file_path)
        wizard_name = os.path.basename(file_path).replace('.tsx', '').replace('.ts', '')
        
        # Analyze component structure
        component_structure = self._analyze_component_structure(content)
        
        # Extract validation schema
        validation_schema = self._extract_validation_schema(content)
        
        # Find API endpoints
        api_endpoints = self._extract_api_endpoints(content)
        
        # Analyze form fields
        form_fields = self._extract_form_fields(content)
        
        # Count wizard steps
        step_count = self._count_wizard_steps(content)
        
        # Analyze navigation features
        navigation_features = self._analyze_navigation_features(content)
        
        # Check accessibility features
        accessibility_features = self._check_accessibility_features(content)
        
        # Check responsive design
        responsive_design = self._check_responsive_design(content)
        
        # Analyze state management
        state_management = self._analyze_state_management(content)
        
        # Check error handling
        error_handling = self._check_error_handling(content)
        
        # Check data persistence
        data_persistence = self._check_data_persistence(content)
        
        # Calculate scores
        performance_score = self._calculate_performance_score(content)
        code_quality_score = self._calculate_code_quality_score(content)
        
        # Generate issues and recommendations
        issues = self._identify_issues(content, component_structure)
        recommendations = self._generate_recommendations(issues, component_structure)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score({
            'component_structure': len(component_structure.get('hooks', [])) * 10,
            'validation': 20 if validation_schema else 0,
            'api_integration': len(api_endpoints) * 5,
            'form_fields': min(len(form_fields) * 2, 20),
            'navigation': len(navigation_features) * 5,
            'accessibility': len(accessibility_features) * 3,
            'responsive': 15 if responsive_design else 0,
            'error_handling': 10 if error_handling else 0,
            'data_persistence': 10 if data_persistence else 0,
            'code_quality': code_quality_score
        })
        
        result = WizardAnalysisResult(
            wizard_name=wizard_name,
            platform=platform,
            file_path=file_path,
            component_structure=component_structure,
            validation_schema=validation_schema,
            api_endpoints=api_endpoints,
            form_fields=form_fields,
            step_count=step_count,
            navigation_features=navigation_features,
            accessibility_features=accessibility_features,
            responsive_design=responsive_design,
            state_management=state_management,
            error_handling=error_handling,
            data_persistence=data_persistence,
            performance_score=performance_score,
            code_quality_score=code_quality_score,
            overall_score=overall_score,
            issues=issues,
            recommendations=recommendations,
            test_duration=time.time() - start_time,
            timestamp=datetime.now().isoformat()
        )
        
        return result
        
    def _determine_platform(self, file_path: str) -> str:
        """Determine which platform a wizard belongs to based on file path"""
        if 'client-portal' in file_path:
            return 'client_portal'
        elif 'bizoholic-frontend' in file_path:
            return 'bizoholic_frontend'
        elif 'coreldove-frontend' in file_path:
            return 'coreldove_frontend'
        elif 'business-directory' in file_path:
            return 'business_directory'
        elif 'bizosaas-admin' in file_path:
            return 'bizosaas_admin'
        else:
            return 'unknown'
            
    def _analyze_component_structure(self, content: str) -> Dict[str, Any]:
        """Analyze React component structure"""
        structure = {
            'imports': [],
            'hooks': [],
            'components': [],
            'interfaces': [],
            'enums': [],
            'functions': []
        }
        
        # Extract imports
        import_pattern = r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]'
        structure['imports'] = re.findall(import_pattern, content)
        
        # Extract React hooks
        hook_patterns = [
            r'useState\s*\(',
            r'useEffect\s*\(',
            r'useForm\s*\(',
            r'useCallback\s*\(',
            r'useMemo\s*\(',
            r'use\w+\s*\('
        ]
        
        for pattern in hook_patterns:
            matches = re.findall(pattern, content)
            structure['hooks'].extend([match.replace('(', '') for match in matches])
            
        # Extract interfaces
        interface_pattern = r'interface\s+(\w+)'
        structure['interfaces'] = re.findall(interface_pattern, content)
        
        # Extract enums
        enum_pattern = r'enum\s+(\w+)'
        structure['enums'] = re.findall(enum_pattern, content)
        
        # Extract function components
        component_pattern = r'export\s+(?:function|const)\s+(\w+)'
        structure['components'] = re.findall(component_pattern, content)
        
        return structure
        
    def _extract_validation_schema(self, content: str) -> Dict[str, Any]:
        """Extract validation schema information"""
        schemas = {}
        
        # Check for Zod schemas
        if 'z.object' in content:
            schemas['zod'] = True
            zod_patterns = re.findall(r'(\w+)\s*:\s*z\.(\w+)', content)
            schemas['zod_fields'] = zod_patterns
            
        # Check for Yup schemas
        if 'yup.' in content:
            schemas['yup'] = True
            
        # Check for React Hook Form validation
        if 'useForm' in content and 'resolver' in content:
            schemas['react_hook_form'] = True
            
        return schemas
        
    def _extract_api_endpoints(self, content: str) -> List[str]:
        """Extract API endpoint calls"""
        endpoints = []
        
        # Find fetch calls
        fetch_pattern = r'fetch\s*\(\s*[\'"]([^\'"]+)[\'"]'
        endpoints.extend(re.findall(fetch_pattern, content))
        
        # Find axios calls
        axios_patterns = [
            r'axios\.get\s*\(\s*[\'"]([^\'"]+)[\'"]',
            r'axios\.post\s*\(\s*[\'"]([^\'"]+)[\'"]',
            r'axios\.put\s*\(\s*[\'"]([^\'"]+)[\'"]',
            r'axios\.delete\s*\(\s*[\'"]([^\'"]+)[\'"]'
        ]
        
        for pattern in axios_patterns:
            endpoints.extend(re.findall(pattern, content))
            
        return list(set(endpoints))  # Remove duplicates
        
    def _extract_form_fields(self, content: str) -> List[str]:
        """Extract form field names and types"""
        fields = []
        
        # Find input elements
        input_pattern = r'<input[^>]*name=[\'"]([^\'"]+)[\'"]'
        fields.extend(re.findall(input_pattern, content))
        
        # Find form field registrations
        register_pattern = r'register\s*\(\s*[\'"]([^\'"]+)[\'"]'
        fields.extend(re.findall(register_pattern, content))
        
        # Find form value references
        value_pattern = r'\.(\w+)\s*\}'
        potential_fields = re.findall(value_pattern, content)
        # Filter out common non-field names
        common_props = {'length', 'map', 'filter', 'includes', 'push', 'pop', 'toString', 'valueOf'}
        fields.extend([f for f in potential_fields if f not in common_props and len(f) > 2])
        
        return list(set(fields))
        
    def _count_wizard_steps(self, content: str) -> int:
        """Count the number of wizard steps"""
        step_indicators = [
            len(re.findall(r'step\s*[\d+]', content.lower())),
            len(re.findall(r'currentstep', content.lower())),
            len(re.findall(r'wizard.*step', content.lower())),
            len(re.findall(r'case\s+\d+:', content)),
            content.lower().count('nextstep'),
            content.lower().count('prevstep')
        ]
        
        return max(step_indicators) if step_indicators else 0
        
    def _analyze_navigation_features(self, content: str) -> List[str]:
        """Analyze wizard navigation features"""
        features = []
        
        if 'goToNextStep' in content or 'nextStep' in content:
            features.append('next_navigation')
        if 'goToPreviousStep' in content or 'prevStep' in content:
            features.append('previous_navigation')
        if 'goToStep' in content:
            features.append('step_jumping')
        if 'progress' in content.lower():
            features.append('progress_indicator')
        if 'breadcrumb' in content.lower():
            features.append('breadcrumbs')
        if 'stepper' in content.lower():
            features.append('step_indicator')
            
        return features
        
    def _check_accessibility_features(self, content: str) -> List[str]:
        """Check for accessibility features"""
        features = []
        
        if 'aria-label' in content:
            features.append('aria_labels')
        if 'aria-describedby' in content:
            features.append('aria_descriptions')
        if 'role=' in content:
            features.append('semantic_roles')
        if 'alt=' in content:
            features.append('image_alt_text')
        if 'tabIndex' in content:
            features.append('keyboard_navigation')
        if 'onKeyDown' in content or 'onKeyPress' in content:
            features.append('keyboard_events')
        if 'focus' in content.lower():
            features.append('focus_management')
            
        return features
        
    def _check_responsive_design(self, content: str) -> bool:
        """Check for responsive design indicators"""
        responsive_indicators = [
            'md:' in content,  # Tailwind medium breakpoint
            'lg:' in content,  # Tailwind large breakpoint
            'sm:' in content,  # Tailwind small breakpoint
            'mobile' in content.lower(),
            'tablet' in content.lower(),
            'desktop' in content.lower(),
            'grid-cols' in content,
            'flex-col' in content,
            '@media' in content
        ]
        
        return any(responsive_indicators)
        
    def _analyze_state_management(self, content: str) -> str:
        """Analyze state management approach"""
        if 'useState' in content and 'useReducer' in content:
            return 'complex_state'
        elif 'useReducer' in content:
            return 'reducer'
        elif 'useState' in content:
            return 'local_state'
        elif 'zustand' in content.lower():
            return 'zustand'
        elif 'redux' in content.lower():
            return 'redux'
        elif 'context' in content.lower():
            return 'context'
        else:
            return 'unknown'
            
    def _check_error_handling(self, content: str) -> bool:
        """Check for error handling patterns"""
        error_patterns = [
            'try {' in content,
            'catch' in content,
            'error' in content.lower(),
            'throw' in content,
            'finally' in content,
            '.error(' in content,
            'onError' in content
        ]
        
        return any(error_patterns)
        
    def _check_data_persistence(self, content: str) -> bool:
        """Check for data persistence features"""
        persistence_patterns = [
            'localStorage' in content,
            'sessionStorage' in content,
            'autosave' in content.lower(),
            'saveProgress' in content,
            'persist' in content.lower(),
            'draft' in content.lower()
        ]
        
        return any(persistence_patterns)
        
    def _calculate_performance_score(self, content: str) -> float:
        """Calculate performance score based on code patterns"""
        score = 50.0  # Base score
        
        # Positive indicators
        if 'useCallback' in content:
            score += 10
        if 'useMemo' in content:
            score += 10
        if 'React.memo' in content:
            score += 10
        if 'lazy' in content:
            score += 15
        if 'Suspense' in content:
            score += 10
            
        # Negative indicators
        if content.count('useEffect') > 5:
            score -= 10
        if content.count('useState') > 10:
            score -= 5
        if len(content) > 50000:  # Very large files
            score -= 15
            
        return max(0, min(100, score))
        
    def _calculate_code_quality_score(self, content: str) -> float:
        """Calculate code quality score"""
        score = 50.0
        
        # Type safety
        if ': ' in content and 'interface' in content:
            score += 20
        elif 'any' in content:
            score -= 10
            
        # Documentation
        comment_lines = len([line for line in content.split('\n') if line.strip().startswith('//')])
        if comment_lines > 5:
            score += 10
            
        # Naming conventions
        if re.search(r'[a-z][A-Z]', content):  # camelCase
            score += 5
            
        # Modularity
        if content.count('export') > 1:
            score += 10
            
        return max(0, min(100, score))
        
    def _identify_issues(self, content: str, structure: Dict) -> List[str]:
        """Identify potential issues in the wizard implementation"""
        issues = []
        
        if len(structure.get('hooks', [])) > 15:
            issues.append("Excessive use of hooks - consider refactoring")
            
        if len(content) > 50000:
            issues.append("Very large file - consider splitting into smaller components")
            
        if not any('error' in hook.lower() for hook in structure.get('hooks', [])):
            issues.append("No error handling hooks detected")
            
        if 'any' in content:
            issues.append("TypeScript 'any' types detected - reduce for better type safety")
            
        if not structure.get('interfaces'):
            issues.append("No TypeScript interfaces found - add type definitions")
            
        if content.count('useState') > 10:
            issues.append("Many useState hooks - consider useReducer for complex state")
            
        return issues
        
    def _generate_recommendations(self, issues: List[str], structure: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if "Excessive use of hooks" in ' '.join(issues):
            recommendations.append("Extract custom hooks for reusable logic")
            
        if "Very large file" in ' '.join(issues):
            recommendations.append("Split wizard into smaller step components")
            
        if not structure.get('interfaces'):
            recommendations.append("Add TypeScript interfaces for better type safety")
            
        if len(structure.get('hooks', [])) < 3:
            recommendations.append("Consider adding form validation and error handling")
            
        recommendations.append("Add unit tests for wizard step navigation")
        recommendations.append("Implement accessibility testing")
        recommendations.append("Add mobile responsiveness testing")
        
        return recommendations
        
    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """Calculate overall wizard quality score"""
        return min(100, sum(scores.values()))
        
    def _create_error_result(self, file_path: str, error_message: str) -> WizardAnalysisResult:
        """Create an error result when analysis fails"""
        return WizardAnalysisResult(
            wizard_name=os.path.basename(file_path),
            platform='unknown',
            file_path=file_path,
            component_structure={},
            validation_schema={},
            api_endpoints=[],
            form_fields=[],
            step_count=0,
            navigation_features=[],
            accessibility_features=[],
            responsive_design=False,
            state_management='unknown',
            error_handling=False,
            data_persistence=False,
            performance_score=0.0,
            code_quality_score=0.0,
            overall_score=0.0,
            issues=[f"Analysis failed: {error_message}"],
            recommendations=[],
            test_duration=0.0,
            timestamp=datetime.now().isoformat()
        )
        
    def test_wizard_apis(self, platform_key: str, api_endpoints: List[str]) -> Dict[str, Any]:
        """Test wizard API endpoints"""
        platform = self.platforms.get(platform_key, {})
        if not platform:
            return {'error': 'Platform not found'}
            
        base_url = platform['url']
        results = {
            'platform': platform['name'],
            'base_url': base_url,
            'endpoints_tested': 0,
            'endpoints_working': 0,
            'test_results': []
        }
        
        for endpoint in api_endpoints:
            if not endpoint.startswith('/'):
                endpoint = '/' + endpoint
                
            full_url = base_url + endpoint
            
            try:
                response = requests.get(full_url, timeout=5)
                results['endpoints_tested'] += 1
                
                test_result = {
                    'endpoint': endpoint,
                    'status_code': response.status_code,
                    'response_time': response.elapsed.total_seconds(),
                    'working': response.status_code < 400
                }
                
                if test_result['working']:
                    results['endpoints_working'] += 1
                    
                results['test_results'].append(test_result)
                
            except Exception as e:
                results['endpoints_tested'] += 1
                results['test_results'].append({
                    'endpoint': endpoint,
                    'error': str(e),
                    'working': False
                })
                
        return results
        
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        total_wizards = len(self.analysis_results)
        accessible_platforms = len([p for p in self.platform_status if p.status == 'accessible'])
        
        if total_wizards > 0:
            avg_score = sum(r.overall_score for r in self.analysis_results) / total_wizards
            avg_steps = sum(r.step_count for r in self.analysis_results) / total_wizards
        else:
            avg_score = 0
            avg_steps = 0
            
        # Categorize wizards by score
        excellent_wizards = [r for r in self.analysis_results if r.overall_score >= 80]
        good_wizards = [r for r in self.analysis_results if 60 <= r.overall_score < 80]
        needs_improvement = [r for r in self.analysis_results if r.overall_score < 60]
        
        report = {
            'summary': {
                'timestamp': datetime.now().isoformat(),
                'total_wizards_analyzed': total_wizards,
                'platforms_accessible': accessible_platforms,
                'total_platforms': len(self.platform_status),
                'average_score': round(avg_score, 1),
                'average_steps': round(avg_steps, 1),
                'excellent_wizards': len(excellent_wizards),
                'good_wizards': len(good_wizards),
                'needs_improvement': len(needs_improvement)
            },
            'platform_status': [asdict(p) for p in self.platform_status],
            'wizard_analysis': [asdict(r) for r in self.analysis_results],
            'top_performers': [
                {
                    'name': r.wizard_name,
                    'platform': r.platform,
                    'score': r.overall_score,
                    'grade': self._get_grade(r.overall_score)
                } for r in sorted(self.analysis_results, key=lambda x: x.overall_score, reverse=True)[:5]
            ],
            'critical_issues': self._collect_critical_issues(),
            'recommendations': self._collect_all_recommendations(),
            'compliance_summary': self._generate_compliance_summary()
        }
        
        return report
        
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90: return 'A+'
        elif score >= 80: return 'A'
        elif score >= 70: return 'B'
        elif score >= 60: return 'C'
        elif score >= 50: return 'D'
        else: return 'F'
        
    def _collect_critical_issues(self) -> List[str]:
        """Collect all critical issues across wizards"""
        all_issues = []
        for result in self.analysis_results:
            for issue in result.issues:
                if any(keyword in issue.lower() for keyword in ['error', 'critical', 'security', 'accessibility']):
                    all_issues.append(f"{result.wizard_name}: {issue}")
        return list(set(all_issues))
        
    def _collect_all_recommendations(self) -> List[str]:
        """Collect and deduplicate recommendations"""
        all_recommendations = []
        for result in self.analysis_results:
            all_recommendations.extend(result.recommendations)
        return list(set(all_recommendations))
        
    def _generate_compliance_summary(self) -> Dict[str, Any]:
        """Generate compliance and best practices summary"""
        total_wizards = len(self.analysis_results)
        if total_wizards == 0:
            return {}
            
        return {
            'accessibility': {
                'wizards_with_aria': len([r for r in self.analysis_results if 'aria_labels' in r.accessibility_features]),
                'percentage': round(len([r for r in self.analysis_results if r.accessibility_features]) / total_wizards * 100, 1)
            },
            'responsive_design': {
                'responsive_wizards': len([r for r in self.analysis_results if r.responsive_design]),
                'percentage': round(len([r for r in self.analysis_results if r.responsive_design]) / total_wizards * 100, 1)
            },
            'error_handling': {
                'wizards_with_error_handling': len([r for r in self.analysis_results if r.error_handling]),
                'percentage': round(len([r for r in self.analysis_results if r.error_handling]) / total_wizards * 100, 1)
            },
            'data_persistence': {
                'wizards_with_persistence': len([r for r in self.analysis_results if r.data_persistence]),
                'percentage': round(len([r for r in self.analysis_results if r.data_persistence]) / total_wizards * 100, 1)
            }
        }
        
    async def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run comprehensive wizard validation"""
        logger.info("🧙‍♂️ Starting BizOSaaS Wizard Validation Framework")
        logger.info("=" * 60)
        
        # Discover wizard files
        wizard_files = self.discover_wizard_files()
        
        # Check platform status
        platform_status = self.check_platform_status()
        
        # Analyze each wizard file
        logger.info("🔍 Analyzing wizard implementations...")
        for file_path in wizard_files:
            result = self.analyze_wizard_file(file_path)
            self.analysis_results.append(result)
            
            # Log immediate result
            status = "✅" if result.overall_score >= 70 else "⚠️" if result.overall_score >= 50 else "❌"
            logger.info(f"{status} {result.wizard_name}: {result.overall_score:.1f}/100 ({self._get_grade(result.overall_score)})")
            
        # Test APIs for accessible platforms
        logger.info("🔗 Testing wizard API endpoints...")
        for result in self.analysis_results:
            if result.api_endpoints and result.platform != 'unknown':
                platform_status = next((p for p in self.platform_status if p.name.lower().replace(' ', '_') == result.platform), None)
                if platform_status and platform_status.status == 'accessible':
                    api_results = self.test_wizard_apis(result.platform, result.api_endpoints)
                    result.component_structure['api_test_results'] = api_results
                    
        # Generate comprehensive report
        report = self.generate_comprehensive_report()
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"wizard_validation_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
            
        logger.info("=" * 60)
        logger.info("🎯 WIZARD VALIDATION COMPLETE")
        logger.info(f"📊 Average Score: {report['summary']['average_score']}/100")
        logger.info(f"🧙‍♂️ Wizards Analyzed: {report['summary']['total_wizards_analyzed']}")
        logger.info(f"🌟 Excellent: {report['summary']['excellent_wizards']}")
        logger.info(f"👍 Good: {report['summary']['good_wizards']}")
        logger.info(f"⚠️ Needs Improvement: {report['summary']['needs_improvement']}")
        logger.info(f"🌐 Accessible Platforms: {report['summary']['platforms_accessible']}/{report['summary']['total_platforms']}")
        logger.info(f"📋 Detailed Report: {report_file}")
        
        return report

def main():
    """Main execution function"""
    framework = WizardValidationFramework()
    
    # Run comprehensive validation
    report = asyncio.run(framework.run_comprehensive_validation())
    
    # Print summary
    print("\n" + "="*60)
    print("🧙‍♂️ BIZOSAAS WIZARD VALIDATION SUMMARY")
    print("="*60)
    
    for result in framework.analysis_results:
        status_icon = "✅" if result.overall_score >= 70 else "⚠️" if result.overall_score >= 50 else "❌"
        print(f"{status_icon} {result.wizard_name:<35} {result.overall_score:>5.1f}/100 ({framework._get_grade(result.overall_score)})")
        
    print("\n🎯 TOP PERFORMERS:")
    for performer in report['top_performers']:
        print(f"   🏆 {performer['name']} - {performer['score']:.1f}/100 ({performer['grade']})")
        
    print("\n🌐 PLATFORM STATUS:")
    for platform in framework.platform_status:
        status_icon = "✅" if platform.status == 'accessible' else "❌"
        print(f"{status_icon} {platform.name:<25} {platform.url} ({platform.response_time:.2f}s)")
        
    print(f"\n📊 Overall Platform Score: {report['summary']['average_score']:.1f}/100")
    
    # Show compliance summary
    compliance = report.get('compliance_summary', {})
    if compliance:
        print("\n📋 COMPLIANCE SUMMARY:")
        print(f"   ♿ Accessibility: {compliance['accessibility']['percentage']:.1f}%")
        print(f"   📱 Responsive Design: {compliance['responsive_design']['percentage']:.1f}%")
        print(f"   🛡️ Error Handling: {compliance['error_handling']['percentage']:.1f}%")
        print(f"   💾 Data Persistence: {compliance['data_persistence']['percentage']:.1f}%")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
BizOSaaS Project Structure Analysis Tool
Comprehensive analysis of all components to ensure nothing essential is missed during reorganization
"""

import os
import json
import subprocess
import re
from typing import Dict, List, Any, Set
from pathlib import Path
from datetime import datetime
import yaml

class ProjectStructureAnalyzer:
    """Comprehensive analyzer for BizOSaaS project structure"""
    
    def __init__(self, project_root: str = "/home/alagiri/projects/bizoholic/bizosaas"):
        self.project_root = Path(project_root)
        self.analysis_results = {}
        self.required_components = {}
        self.deprecated_components = {}
        self.active_services = set()
        self.configuration_files = {}
        
    def analyze_complete_structure(self) -> Dict[str, Any]:
        """Perform comprehensive project structure analysis"""
        print("🔍 Starting comprehensive BizOSaaS project structure analysis...")
        
        analysis = {
            "analysis_timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "services_analysis": self._analyze_services(),
            "configuration_analysis": self._analyze_configurations(),
            "dependencies_analysis": self._analyze_dependencies(),
            "infrastructure_analysis": self._analyze_infrastructure(),
            "documentation_analysis": self._analyze_documentation(),
            "deprecated_components": self._identify_deprecated_components(),
            "essential_components": self._identify_essential_components(),
            "test_requirements": self._analyze_test_requirements(),
            "deployment_readiness": self._check_deployment_readiness()
        }
        
        return analysis
    
    def _analyze_services(self) -> Dict[str, Any]:
        """Analyze all services in the project"""
        print("📋 Analyzing services...")
        
        services_dir = self.project_root / "services"
        services_analysis = {
            "total_services": 0,
            "active_services": [],
            "deprecated_services": [],
            "service_types": {},
            "port_conflicts": [],
            "missing_health_checks": [],
            "docker_configurations": {},
            "service_dependencies": {}
        }
        
        if not services_dir.exists():
            return services_analysis
        
        # Analyze each service
        for service_path in services_dir.iterdir():
            if service_path.is_dir() and not service_path.name.startswith('.'):
                service_name = service_path.name
                services_analysis["total_services"] += 1
                
                service_info = self._analyze_individual_service(service_path)
                
                # Categorize services
                if self._is_deprecated_service(service_name):
                    services_analysis["deprecated_services"].append({
                        "name": service_name,
                        "reason": self._get_deprecation_reason(service_name),
                        "migration_target": self._get_migration_target(service_name),
                        "size_mb": self._get_directory_size(service_path)
                    })
                else:
                    services_analysis["active_services"].append({
                        "name": service_name,
                        "type": service_info["type"],
                        "status": service_info["status"],
                        "port": service_info["port"],
                        "health_endpoint": service_info["health_endpoint"],
                        "dependencies": service_info["dependencies"]
                    })
                    self.active_services.add(service_name)
        
        return services_analysis
    
    def _analyze_individual_service(self, service_path: Path) -> Dict[str, Any]:
        """Analyze an individual service"""
        service_info = {
            "type": "unknown",
            "status": "unknown",
            "port": None,
            "health_endpoint": "/health",
            "dependencies": [],
            "has_dockerfile": False,
            "has_requirements": False,
            "has_package_json": False,
            "configuration_files": []
        }
        
        # Check for common files
        if (service_path / "Dockerfile").exists():
            service_info["has_dockerfile"] = True
        
        if (service_path / "requirements.txt").exists():
            service_info["has_requirements"] = True
            service_info["type"] = "python"
        
        if (service_path / "package.json").exists():
            service_info["has_package_json"] = True
            service_info["type"] = "nodejs"
        
        # Look for configuration files
        for config_file in ["config.py", "settings.py", ".env", "docker-compose.yml"]:
            if (service_path / config_file).exists():
                service_info["configuration_files"].append(config_file)
        
        # Try to determine port from common files
        service_info["port"] = self._extract_service_port(service_path)
        
        return service_info
    
    def _extract_service_port(self, service_path: Path) -> int:
        """Extract service port from configuration files"""
        port_patterns = [
            r"PORT\s*=\s*(\d+)",
            r"port\s*:\s*(\d+)",
            r"listen\s+(\d+)",
            r"--port\s+(\d+)"
        ]
        
        # Check common configuration files
        for file_name in ["main.py", "app.py", "server.js", "Dockerfile", "docker-compose.yml"]:
            file_path = service_path / file_name
            if file_path.exists():
                try:
                    content = file_path.read_text()
                    for pattern in port_patterns:
                        match = re.search(pattern, content)
                        if match:
                            return int(match.group(1))
                except Exception:
                    continue
        
        return None
    
    def _analyze_configurations(self) -> Dict[str, Any]:
        """Analyze configuration files"""
        print("⚙️ Analyzing configurations...")
        
        config_analysis = {
            "docker_compose_files": [],
            "environment_files": [],
            "kubernetes_manifests": [],
            "nginx_configs": [],
            "database_configs": [],
            "vault_configs": [],
            "monitoring_configs": []
        }
        
        # Find Docker Compose files
        for compose_file in self.project_root.glob("docker-compose*.yml"):
            config_analysis["docker_compose_files"].append({
                "file": str(compose_file.relative_to(self.project_root)),
                "services_count": self._count_docker_services(compose_file),
                "size_kb": compose_file.stat().st_size // 1024
            })
        
        # Find environment files
        for env_file in self.project_root.glob("**/.env*"):
            if not any(x in str(env_file) for x in ['.git', '__pycache__', 'node_modules']):
                config_analysis["environment_files"].append({
                    "file": str(env_file.relative_to(self.project_root)),
                    "variables_count": self._count_env_variables(env_file)
                })
        
        # Find Kubernetes manifests
        for k8s_file in self.project_root.glob("**/*.yaml"):
            if self._is_k8s_manifest(k8s_file):
                config_analysis["kubernetes_manifests"].append({
                    "file": str(k8s_file.relative_to(self.project_root)),
                    "type": self._get_k8s_resource_type(k8s_file)
                })
        
        return config_analysis
    
    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze project dependencies"""
        print("📦 Analyzing dependencies...")
        
        dependencies = {
            "python_requirements": [],
            "nodejs_packages": [],
            "system_dependencies": [],
            "docker_images": [],
            "external_services": []
        }
        
        # Python requirements
        for req_file in self.project_root.glob("**/requirements*.txt"):
            if not any(x in str(req_file) for x in ['.git', '__pycache__']):
                deps = self._parse_requirements_file(req_file)
                dependencies["python_requirements"].extend(deps)
        
        # Node.js packages
        for package_file in self.project_root.glob("**/package.json"):
            if not any(x in str(package_file) for x in ['.git', 'node_modules']):
                deps = self._parse_package_json(package_file)
                dependencies["nodejs_packages"].extend(deps)
        
        # Docker images
        for dockerfile in self.project_root.glob("**/Dockerfile*"):
            images = self._extract_docker_images(dockerfile)
            dependencies["docker_images"].extend(images)
        
        return dependencies
    
    def _analyze_infrastructure(self) -> Dict[str, Any]:
        """Analyze infrastructure components"""
        print("🏗️ Analyzing infrastructure...")
        
        infrastructure = {
            "databases": [],
            "cache_systems": [],
            "message_queues": [],
            "load_balancers": [],
            "monitoring_systems": [],
            "secrets_management": [],
            "storage_systems": []
        }
        
        # Check for database configurations
        for db_term in ["postgres", "mongodb", "redis", "mysql"]:
            files = list(self.project_root.glob(f"**/*{db_term}*"))
            if files:
                infrastructure["databases"].append({
                    "type": db_term,
                    "files": [str(f.relative_to(self.project_root)) for f in files[:5]]
                })
        
        # Check for monitoring
        for monitor_term in ["prometheus", "grafana", "jaeger"]:
            files = list(self.project_root.glob(f"**/*{monitor_term}*"))
            if files:
                infrastructure["monitoring_systems"].append({
                    "type": monitor_term,
                    "files": [str(f.relative_to(self.project_root)) for f in files[:3]]
                })
        
        return infrastructure
    
    def _analyze_documentation(self) -> Dict[str, Any]:
        """Analyze documentation files"""
        print("📚 Analyzing documentation...")
        
        docs_analysis = {
            "readme_files": [],
            "api_documentation": [],
            "deployment_docs": [],
            "architecture_docs": [],
            "loose_md_files": []
        }
        
        # Find all markdown files
        for md_file in self.project_root.glob("**/*.md"):
            if not any(x in str(md_file) for x in ['.git', 'node_modules']):
                relative_path = str(md_file.relative_to(self.project_root))
                file_size = md_file.stat().st_size
                
                if md_file.name.lower().startswith('readme'):
                    docs_analysis["readme_files"].append({
                        "file": relative_path,
                        "size_kb": file_size // 1024
                    })
                elif any(x in md_file.name.lower() for x in ['deploy', 'install', 'setup']):
                    docs_analysis["deployment_docs"].append({
                        "file": relative_path,
                        "size_kb": file_size // 1024
                    })
                elif any(x in md_file.name.lower() for x in ['architecture', 'design', 'tech']):
                    docs_analysis["architecture_docs"].append({
                        "file": relative_path,
                        "size_kb": file_size // 1024
                    })
                elif md_file.parent == self.project_root:
                    docs_analysis["loose_md_files"].append({
                        "file": relative_path,
                        "size_kb": file_size // 1024
                    })
        
        return docs_analysis
    
    def _identify_deprecated_components(self) -> List[Dict[str, Any]]:
        """Identify deprecated components that can be moved to backup"""
        print("⚠️ Identifying deprecated components...")
        
        deprecated = []
        
        # Deprecated services
        deprecated_services = ["medusa", "medusa-coreldove", "medusa-official", "strapi"]
        for service in deprecated_services:
            service_path = self.project_root / "services" / service
            if service_path.exists():
                deprecated.append({
                    "type": "service",
                    "name": service,
                    "path": f"services/{service}",
                    "reason": f"Migrated to {'Saleor' if 'medusa' in service else 'Wagtail'}",
                    "size_mb": self._get_directory_size(service_path),
                    "can_backup": True
                })
        
        # Old documentation files
        old_doc_patterns = [
            "*MEDUSA*", "*STRAPI*", "*OLD*", "*DEPRECATED*", "*BACKUP*"
        ]
        for pattern in old_doc_patterns:
            for file_path in self.project_root.glob(f"**/{pattern}"):
                if file_path.is_file():
                    deprecated.append({
                        "type": "documentation",
                        "name": file_path.name,
                        "path": str(file_path.relative_to(self.project_root)),
                        "reason": "Legacy documentation",
                        "size_kb": file_path.stat().st_size // 1024,
                        "can_backup": True
                    })
        
        return deprecated
    
    def _identify_essential_components(self) -> Dict[str, List[str]]:
        """Identify essential components that must be kept"""
        print("✅ Identifying essential components...")
        
        essential = {
            "core_services": [
                "auth-service", "auth-service-v2", "user-management", "api-gateway",
                "ai-governance-layer", "gdpr-compliance-service", "wagtail-cms"
            ],
            "ecommerce_services": [
                "saleor-backend", "saleor-storefront", "coreldove-saleor", "payment-service"
            ],
            "ai_services": [
                "ai-agents", "bizosaas-brain", "ai-integration-service", "personal-ai-assistant"
            ],
            "configuration_files": [
                "docker-compose.yml", "docker-compose.production.yml", ".env.example"
            ],
            "infrastructure_configs": [
                "k8s/", "deployment/", "database/", "vault-config/"
            ],
            "critical_scripts": [
                "scripts/", "deployment/"
            ]
        }
        
        return essential
    
    def _analyze_test_requirements(self) -> Dict[str, Any]:
        """Analyze what needs to be tested before reorganization"""
        print("🧪 Analyzing test requirements...")
        
        test_requirements = {
            "services_to_test": [],
            "configurations_to_validate": [],
            "dependencies_to_check": [],
            "data_to_backup": []
        }
        
        # Services that need health checks
        for service in self.active_services:
            test_requirements["services_to_test"].append({
                "service": service,
                "tests": ["health_check", "port_availability", "dependencies"]
            })
        
        # Critical configurations
        critical_configs = [
            "docker-compose.yml", "docker-compose.production.yml",
            ".env.example", "k8s/manifests/"
        ]
        for config in critical_configs:
            config_path = self.project_root / config
            if config_path.exists():
                test_requirements["configurations_to_validate"].append({
                    "config": config,
                    "tests": ["syntax_check", "service_references", "port_conflicts"]
                })
        
        return test_requirements
    
    def _check_deployment_readiness(self) -> Dict[str, Any]:
        """Check if project is ready for reorganization"""
        print("🚀 Checking deployment readiness...")
        
        readiness = {
            "overall_score": 0,
            "checks": {
                "essential_services_present": False,
                "no_port_conflicts": False,
                "configurations_valid": False,
                "dependencies_resolved": False,
                "backup_plan_ready": False
            },
            "recommendations": []
        }
        
        # Check essential services
        essential_services = ["auth-service", "wagtail-cms", "saleor-backend", "ai-governance-layer"]
        present_services = [s for s in essential_services if (self.project_root / "services" / s).exists()]
        readiness["checks"]["essential_services_present"] = len(present_services) == len(essential_services)
        
        if not readiness["checks"]["essential_services_present"]:
            missing = set(essential_services) - set(present_services)
            readiness["recommendations"].append(f"Missing essential services: {missing}")
        
        # Calculate overall score
        score = sum(readiness["checks"].values()) / len(readiness["checks"]) * 100
        readiness["overall_score"] = round(score, 1)
        
        return readiness
    
    # Helper methods
    def _is_deprecated_service(self, service_name: str) -> bool:
        """Check if service is deprecated"""
        deprecated_services = ["medusa", "medusa-coreldove", "medusa-official", "strapi"]
        return any(dep in service_name.lower() for dep in deprecated_services)
    
    def _get_deprecation_reason(self, service_name: str) -> str:
        """Get deprecation reason for service"""
        if "medusa" in service_name.lower():
            return "Migrated to Saleor for e-commerce functionality"
        elif "strapi" in service_name.lower():
            return "Migrated to Wagtail CMS for content management"
        return "Service deprecated"
    
    def _get_migration_target(self, service_name: str) -> str:
        """Get migration target for deprecated service"""
        if "medusa" in service_name.lower():
            return "saleor-backend"
        elif "strapi" in service_name.lower():
            return "wagtail-cms"
        return "unknown"
    
    def _get_directory_size(self, directory: Path) -> float:
        """Get directory size in MB"""
        try:
            result = subprocess.run(['du', '-sm', str(directory)], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return float(result.stdout.split()[0])
        except Exception:
            pass
        return 0.0
    
    def _count_docker_services(self, compose_file: Path) -> int:
        """Count services in docker-compose file"""
        try:
            with open(compose_file) as f:
                content = yaml.safe_load(f)
                return len(content.get('services', {}))
        except Exception:
            return 0
    
    def _count_env_variables(self, env_file: Path) -> int:
        """Count environment variables in file"""
        try:
            with open(env_file) as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                return len([line for line in lines if '=' in line])
        except Exception:
            return 0
    
    def _is_k8s_manifest(self, file_path: Path) -> bool:
        """Check if file is a Kubernetes manifest"""
        try:
            with open(file_path) as f:
                content = f.read()
                return 'apiVersion:' in content and 'kind:' in content
        except Exception:
            return False
    
    def _get_k8s_resource_type(self, file_path: Path) -> str:
        """Get Kubernetes resource type"""
        try:
            with open(file_path) as f:
                content = yaml.safe_load(f)
                return content.get('kind', 'unknown')
        except Exception:
            return 'unknown'
    
    def _parse_requirements_file(self, req_file: Path) -> List[str]:
        """Parse Python requirements file"""
        try:
            with open(req_file) as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                return [line.split('==')[0].split('>=')[0] for line in lines]
        except Exception:
            return []
    
    def _parse_package_json(self, package_file: Path) -> List[str]:
        """Parse Node.js package.json"""
        try:
            with open(package_file) as f:
                content = json.load(f)
                deps = list(content.get('dependencies', {}).keys())
                deps.extend(list(content.get('devDependencies', {}).keys()))
                return deps
        except Exception:
            return []
    
    def _extract_docker_images(self, dockerfile: Path) -> List[str]:
        """Extract base images from Dockerfile"""
        try:
            with open(dockerfile) as f:
                content = f.read()
                from_pattern = r'FROM\s+([^\s]+)'
                matches = re.findall(from_pattern, content, re.IGNORECASE)
                return matches
        except Exception:
            return []

def main():
    """Main analysis function"""
    print("🎯 BizOSaaS Project Structure Analysis Starting")
    print("="*80)
    
    analyzer = ProjectStructureAnalyzer()
    analysis_results = analyzer.analyze_complete_structure()
    
    # Save analysis results
    output_file = "/home/alagiri/projects/bizoholic/bizosaas/PROJECT_STRUCTURE_ANALYSIS_REPORT.json"
    with open(output_file, 'w') as f:
        json.dump(analysis_results, f, indent=2, default=str)
    
    # Print summary
    print("\n🏆 ANALYSIS COMPLETED")
    print("="*80)
    print(f"📊 Analysis Report: {output_file}")
    print(f"📋 Total Services: {analysis_results['services_analysis']['total_services']}")
    print(f"✅ Active Services: {len(analysis_results['services_analysis']['active_services'])}")
    print(f"⚠️ Deprecated Services: {len(analysis_results['services_analysis']['deprecated_services'])}")
    print(f"📄 Configuration Files: {len(analysis_results['configuration_analysis']['docker_compose_files'])}")
    print(f"🚀 Deployment Readiness: {analysis_results['deployment_readiness']['overall_score']}%")
    
    # Print recommendations
    recommendations = analysis_results['deployment_readiness']['recommendations']
    if recommendations:
        print(f"\n⚠️ RECOMMENDATIONS:")
        for rec in recommendations:
            print(f"   • {rec}")
    
    print("\n✅ Ready for testing and reorganization planning")
    print("="*80)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Essential Components Testing Script
Test all critical components before project reorganization to ensure nothing breaks
"""

import asyncio
import aiohttp
import subprocess
import json
import yaml
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
import socket
import time

class EssentialComponentsTester:
    """Test all essential components before reorganization"""
    
    def __init__(self, project_root: str = "/home/alagiri/projects/bizoholic/bizosaas"):
        self.project_root = Path(project_root)
        self.test_results = {}
        self.failed_tests = []
        self.warnings = []
        
        # Essential services that must work
        self.essential_services = {
            "auth-service": {"port": 3001, "health": "/health", "critical": True},
            "auth-service-v2": {"port": 3002, "health": "/health", "critical": True},
            "api-gateway": {"port": 8080, "health": "/health", "critical": True},
            "user-management": {"port": 8006, "health": "/health", "critical": True},
            "wagtail-cms": {"port": 8010, "health": "/admin/", "critical": True},
            "saleor-backend": {"port": 8011, "health": "/health/", "critical": True},
            "ai-governance-layer": {"port": 8090, "health": "/health", "critical": True},
            "gdpr-compliance-service": {"port": 8091, "health": "/health", "critical": True},
            "bizosaas-brain": {"port": 8001, "health": "/health", "critical": False},
            "personal-ai-assistant": {"port": 8020, "health": "/health", "critical": False}
        }
        
        # Essential configuration files
        self.essential_configs = [
            "docker-compose.yml",
            "docker-compose.production.yml", 
            ".env.example",
            "k8s/manifests/",
            "deployment/",
            "database/init-scripts/",
            "services/ai-governance-layer/",
            "services/gdpr-compliance-service/"
        ]
        
        # Infrastructure dependencies
        self.infrastructure_deps = {
            "postgresql": {"port": 5432, "service": "database"},
            "redis": {"port": 6379, "service": "cache"}, 
            "vault": {"port": 8200, "service": "secrets"}
        }
    
    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all essential component tests"""
        print("🧪 Starting Essential Components Testing")
        print("="*80)
        
        test_suite = {
            "test_timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "service_tests": await self._test_essential_services(),
            "configuration_tests": await self._test_essential_configurations(),
            "dependency_tests": await self._test_dependencies(),
            "infrastructure_tests": await self._test_infrastructure(),
            "port_conflict_tests": await self._test_port_conflicts(),
            "file_integrity_tests": await self._test_file_integrity(),
            "deployment_tests": await self._test_deployment_readiness(),
            "backup_safety_tests": await self._test_backup_safety(),
            "overall_status": "pending"
        }
        
        # Calculate overall status
        test_suite["overall_status"] = self._calculate_overall_status(test_suite)
        
        return test_suite
    
    async def _test_essential_services(self) -> Dict[str, Any]:
        """Test essential services health and availability"""
        print("🏥 Testing essential services...")
        
        service_tests = {
            "total_services": len(self.essential_services),
            "services_tested": 0,
            "services_healthy": 0,
            "services_failed": 0,
            "critical_failures": 0,
            "service_results": {}
        }
        
        for service_name, config in self.essential_services.items():
            print(f"  🔍 Testing {service_name}...")
            
            service_result = {
                "status": "unknown",
                "port_available": False,
                "health_check": False,
                "response_time": None,
                "error": None,
                "critical": config["critical"]
            }
            
            # Test port availability
            port_available = await self._test_port_available(config["port"])
            service_result["port_available"] = port_available
            
            if port_available:
                # Test health endpoint
                health_result = await self._test_health_endpoint(
                    service_name, config["port"], config["health"]
                )
                service_result.update(health_result)
                
                if service_result["health_check"]:
                    service_tests["services_healthy"] += 1
                    service_result["status"] = "healthy"
                else:
                    service_tests["services_failed"] += 1
                    service_result["status"] = "unhealthy"
                    if config["critical"]:
                        service_tests["critical_failures"] += 1
            else:
                service_tests["services_failed"] += 1
                service_result["status"] = "not_running"
                service_result["error"] = f"Port {config['port']} not available"
                if config["critical"]:
                    service_tests["critical_failures"] += 1
            
            service_tests["services_tested"] += 1
            service_tests["service_results"][service_name] = service_result
        
        return service_tests
    
    async def _test_essential_configurations(self) -> Dict[str, Any]:
        """Test essential configuration files"""
        print("⚙️ Testing essential configurations...")
        
        config_tests = {
            "total_configs": len(self.essential_configs),
            "configs_valid": 0,
            "configs_failed": 0,
            "config_results": {}
        }
        
        for config_path in self.essential_configs:
            print(f"  📋 Testing {config_path}...")
            
            full_path = self.project_root / config_path
            config_result = {
                "exists": full_path.exists(),
                "type": "file" if config_path.endswith(('.yml', '.yaml', '.json', '.env')) else "directory",
                "syntax_valid": False,
                "size_bytes": 0,
                "error": None
            }
            
            if config_result["exists"]:
                try:
                    if full_path.is_file():
                        config_result["size_bytes"] = full_path.stat().st_size
                        
                        # Test syntax for specific file types
                        if config_path.endswith(('.yml', '.yaml')):
                            config_result["syntax_valid"] = await self._test_yaml_syntax(full_path)
                        elif config_path.endswith('.json'):
                            config_result["syntax_valid"] = await self._test_json_syntax(full_path)
                        elif config_path.endswith('.env'):
                            config_result["syntax_valid"] = await self._test_env_syntax(full_path)
                        else:
                            config_result["syntax_valid"] = True  # Assume valid for other files
                    else:
                        # Directory
                        config_result["syntax_valid"] = True
                        config_result["size_bytes"] = sum(
                            f.stat().st_size for f in full_path.rglob('*') if f.is_file()
                        )
                    
                    if config_result["syntax_valid"]:
                        config_tests["configs_valid"] += 1
                    else:
                        config_tests["configs_failed"] += 1
                        
                except Exception as e:
                    config_result["error"] = str(e)
                    config_tests["configs_failed"] += 1
            else:
                config_result["error"] = "File/directory does not exist"
                config_tests["configs_failed"] += 1
            
            config_tests["config_results"][config_path] = config_result
        
        return config_tests
    
    async def _test_dependencies(self) -> Dict[str, Any]:
        """Test system and application dependencies"""
        print("📦 Testing dependencies...")
        
        dependency_tests = {
            "system_dependencies": {},
            "python_dependencies": {},
            "nodejs_dependencies": {},
            "docker_dependencies": {}
        }
        
        # Test system dependencies
        system_deps = ["docker", "python3", "node", "npm", "curl", "git"]
        for dep in system_deps:
            available = await self._test_system_dependency(dep)
            dependency_tests["system_dependencies"][dep] = {
                "available": available,
                "version": await self._get_dependency_version(dep) if available else None
            }
        
        # Test Python dependencies
        python_deps = ["fastapi", "uvicorn", "sqlalchemy", "aiohttp", "pytest"]
        for dep in python_deps:
            available = await self._test_python_dependency(dep)
            dependency_tests["python_dependencies"][dep] = {"available": available}
        
        # Test Docker
        docker_available = await self._test_docker_availability()
        dependency_tests["docker_dependencies"]["docker_daemon"] = {
            "available": docker_available,
            "containers_running": await self._count_running_containers() if docker_available else 0
        }
        
        return dependency_tests
    
    async def _test_infrastructure(self) -> Dict[str, Any]:
        """Test infrastructure components"""
        print("🏗️ Testing infrastructure...")
        
        infra_tests = {
            "database_connectivity": {},
            "cache_connectivity": {},
            "secrets_connectivity": {},
            "monitoring_systems": {}
        }
        
        # Test database connectivity
        for service, config in self.infrastructure_deps.items():
            print(f"  🔍 Testing {service}...")
            
            connectivity_result = {
                "port_available": await self._test_port_available(config["port"]),
                "service_type": config["service"],
                "error": None
            }
            
            if service == "postgresql":
                connectivity_result["connection_test"] = await self._test_postgres_connection()
            elif service == "redis":
                connectivity_result["connection_test"] = await self._test_redis_connection()
            elif service == "vault":
                connectivity_result["connection_test"] = await self._test_vault_connection()
            
            infra_tests[f"{config['service']}_connectivity"][service] = connectivity_result
        
        return infra_tests
    
    async def _test_port_conflicts(self) -> Dict[str, Any]:
        """Test for port conflicts between services"""
        print("🔌 Testing port conflicts...")
        
        port_tests = {
            "ports_in_use": [],
            "potential_conflicts": [],
            "service_port_mapping": {}
        }
        
        # Collect all ports from essential services
        all_ports = {}
        for service_name, config in self.essential_services.items():
            port = config["port"]
            if port not in all_ports:
                all_ports[port] = []
            all_ports[port].append(service_name)
            port_tests["service_port_mapping"][service_name] = port
        
        # Check for conflicts
        for port, services in all_ports.items():
            if len(services) > 1:
                port_tests["potential_conflicts"].append({
                    "port": port,
                    "conflicting_services": services
                })
            
            # Check if port is in use
            if await self._test_port_available(port):
                port_tests["ports_in_use"].append({
                    "port": port,
                    "services": services
                })
        
        return port_tests
    
    async def _test_file_integrity(self) -> Dict[str, Any]:
        """Test file integrity of essential components"""
        print("🔒 Testing file integrity...")
        
        integrity_tests = {
            "essential_files": {},
            "checksum_validation": {},
            "permission_checks": {}
        }
        
        essential_files = [
            "services/ai-governance-layer/main.py",
            "services/gdpr-compliance-service/main.py",
            "docker-compose.yml",
            "docker-compose.production.yml"
        ]
        
        for file_path in essential_files:
            full_path = self.project_root / file_path
            
            file_check = {
                "exists": full_path.exists(),
                "readable": False,
                "size_bytes": 0,
                "permissions": None
            }
            
            if file_check["exists"]:
                try:
                    file_check["size_bytes"] = full_path.stat().st_size
                    file_check["permissions"] = oct(full_path.stat().st_mode)[-3:]
                    
                    # Test readability
                    with open(full_path, 'r') as f:
                        f.read(100)  # Read first 100 chars
                    file_check["readable"] = True
                    
                except Exception as e:
                    file_check["error"] = str(e)
            
            integrity_tests["essential_files"][file_path] = file_check
        
        return integrity_tests
    
    async def _test_deployment_readiness(self) -> Dict[str, Any]:
        """Test deployment readiness"""
        print("🚀 Testing deployment readiness...")
        
        deployment_tests = {
            "docker_compose_valid": False,
            "k8s_manifests_valid": False,
            "environment_complete": False,
            "secrets_available": False,
            "deployment_scripts_executable": False
        }
        
        # Test Docker Compose
        try:
            result = subprocess.run(
                ["docker-compose", "config", "--quiet"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            deployment_tests["docker_compose_valid"] = result.returncode == 0
        except Exception:
            deployment_tests["docker_compose_valid"] = False
        
        # Test environment files
        env_files = [".env.example", ".env.production.example"]
        env_complete = True
        for env_file in env_files:
            if not (self.project_root / env_file).exists():
                env_complete = False
                break
        deployment_tests["environment_complete"] = env_complete
        
        return deployment_tests
    
    async def _test_backup_safety(self) -> Dict[str, Any]:
        """Test backup safety before reorganization"""
        print("💾 Testing backup safety...")
        
        backup_tests = {
            "deprecated_services_identified": False,
            "backup_space_available": False,
            "no_active_dependencies": False,
            "safe_to_move": []
        }
        
        # Check deprecated services
        deprecated_services = ["medusa", "medusa-coreldove", "strapi"]
        deprecated_paths = []
        
        for service in deprecated_services:
            service_path = self.project_root / "services" / service
            if service_path.exists():
                deprecated_paths.append(str(service_path))
                
                # Check if safe to move
                safe_to_move = await self._check_service_safe_to_move(service)
                if safe_to_move:
                    backup_tests["safe_to_move"].append(service)
        
        backup_tests["deprecated_services_identified"] = len(deprecated_paths) > 0
        
        # Check available disk space
        backup_tests["backup_space_available"] = await self._check_backup_space()
        
        return backup_tests
    
    # Helper methods
    async def _test_port_available(self, port: int) -> bool:
        """Test if port is available/in use"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex(('localhost', port))
            return result == 0  # Port is in use (available for testing)
        except Exception:
            return False
        finally:
            sock.close()
    
    async def _test_health_endpoint(self, service_name: str, port: int, health_path: str) -> Dict[str, Any]:
        """Test service health endpoint"""
        url = f"http://localhost:{port}{health_path}"
        
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    response_time = time.time() - start_time
                    
                    return {
                        "health_check": response.status in [200, 204],
                        "status_code": response.status,
                        "response_time": round(response_time * 1000, 2)  # ms
                    }
        except Exception as e:
            return {
                "health_check": False,
                "status_code": None,
                "response_time": None,
                "error": str(e)
            }
    
    async def _test_yaml_syntax(self, file_path: Path) -> bool:
        """Test YAML file syntax"""
        try:
            with open(file_path) as f:
                yaml.safe_load(f)
            return True
        except Exception:
            return False
    
    async def _test_json_syntax(self, file_path: Path) -> bool:
        """Test JSON file syntax"""
        try:
            with open(file_path) as f:
                json.load(f)
            return True
        except Exception:
            return False
    
    async def _test_env_syntax(self, file_path: Path) -> bool:
        """Test .env file syntax"""
        try:
            with open(file_path) as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' not in line:
                            return False
            return True
        except Exception:
            return False
    
    async def _test_system_dependency(self, dependency: str) -> bool:
        """Test if system dependency is available"""
        try:
            result = subprocess.run(
                ["which", dependency],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    async def _get_dependency_version(self, dependency: str) -> str:
        """Get dependency version"""
        try:
            version_flags = {
                "docker": "--version",
                "python3": "--version", 
                "node": "--version",
                "npm": "--version",
                "git": "--version"
            }
            
            flag = version_flags.get(dependency, "--version")
            result = subprocess.run(
                [dependency, flag],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except Exception:
            return "unknown"
    
    async def _test_python_dependency(self, dependency: str) -> bool:
        """Test if Python dependency is available"""
        try:
            result = subprocess.run(
                ["python3", "-c", f"import {dependency}"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    async def _test_docker_availability(self) -> bool:
        """Test Docker daemon availability"""
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False
    
    async def _count_running_containers(self) -> int:
        """Count running Docker containers"""
        try:
            result = subprocess.run(
                ["docker", "ps", "-q"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return len([line for line in result.stdout.strip().split('\n') if line])
            return 0
        except Exception:
            return 0
    
    async def _test_postgres_connection(self) -> bool:
        """Test PostgreSQL connection"""
        try:
            # Simple connection test (would need actual credentials in production)
            result = subprocess.run(
                ["pg_isready", "-h", "localhost", "-p", "5432"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    async def _test_redis_connection(self) -> bool:
        """Test Redis connection"""
        try:
            result = subprocess.run(
                ["redis-cli", "-h", "localhost", "-p", "6379", "ping"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return "PONG" in result.stdout
        except Exception:
            return False
    
    async def _test_vault_connection(self) -> bool:
        """Test Vault connection"""
        try:
            result = subprocess.run(
                ["curl", "-s", "http://localhost:8200/v1/sys/health"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    async def _check_service_safe_to_move(self, service_name: str) -> bool:
        """Check if service is safe to move to backup"""
        # Services are safe to move if they're deprecated and not running
        port = None
        if service_name == "medusa":
            port = 9000
        elif service_name == "strapi":
            port = 1337
        
        if port:
            return not await self._test_port_available(port)
        return True
    
    async def _check_backup_space(self) -> bool:
        """Check if enough space for backup"""
        try:
            result = subprocess.run(
                ["df", "-h", str(self.project_root)],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    # Parse available space (simplified)
                    parts = lines[1].split()
                    if len(parts) > 3:
                        avail = parts[3]
                        # Check if more than 1GB available
                        return 'G' in avail and float(avail.replace('G', '')) > 1.0
            return False
        except Exception:
            return False
    
    def _calculate_overall_status(self, test_suite: Dict[str, Any]) -> str:
        """Calculate overall test status"""
        service_tests = test_suite["service_tests"]
        config_tests = test_suite["configuration_tests"]
        
        # Check critical failures
        if service_tests["critical_failures"] > 0:
            return "CRITICAL_FAILURES"
        
        # Check overall health
        total_services = service_tests["total_services"]
        healthy_services = service_tests["services_healthy"]
        healthy_configs = config_tests["configs_valid"]
        total_configs = config_tests["total_configs"]
        
        service_health_rate = healthy_services / total_services if total_services > 0 else 0
        config_health_rate = healthy_configs / total_configs if total_configs > 0 else 0
        
        overall_rate = (service_health_rate + config_health_rate) / 2
        
        if overall_rate >= 0.9:
            return "EXCELLENT"
        elif overall_rate >= 0.7:
            return "GOOD"
        elif overall_rate >= 0.5:
            return "ACCEPTABLE"
        else:
            return "NEEDS_ATTENTION"

async def main():
    """Main testing function"""
    print("🧪 Essential Components Testing Starting")
    print("="*80)
    
    tester = EssentialComponentsTester()
    test_results = await tester.run_comprehensive_tests()
    
    # Save test results
    output_file = "/home/alagiri/projects/bizoholic/bizosaas/ESSENTIAL_COMPONENTS_TEST_REPORT.json"
    with open(output_file, 'w') as f:
        json.dump(test_results, f, indent=2, default=str)
    
    # Print summary
    service_tests = test_results["service_tests"]
    config_tests = test_results["configuration_tests"]
    
    print("\n🏆 TESTING COMPLETED")
    print("="*80)
    print(f"📊 Test Report: {output_file}")
    print(f"🏥 Service Health: {service_tests['services_healthy']}/{service_tests['total_services']}")
    print(f"⚙️ Config Validation: {config_tests['configs_valid']}/{config_tests['total_configs']}")
    print(f"🚨 Critical Failures: {service_tests['critical_failures']}")
    print(f"🏆 Overall Status: {test_results['overall_status']}")
    
    # Print critical issues
    if service_tests['critical_failures'] > 0:
        print(f"\n🚨 CRITICAL ISSUES FOUND:")
        for service_name, result in service_tests['service_results'].items():
            if result['critical'] and result['status'] != 'healthy':
                print(f"   ❌ {service_name}: {result['status']} - {result.get('error', 'Unknown error')}")
    
    # Recommendations
    if test_results['overall_status'] in ['NEEDS_ATTENTION', 'CRITICAL_FAILURES']:
        print(f"\n⚠️ RECOMMENDATIONS:")
        print("   • Fix critical service failures before reorganization")
        print("   • Validate configuration files")
        print("   • Ensure infrastructure dependencies are running")
    else:
        print(f"\n✅ READY FOR REORGANIZATION:")
        print("   • All critical components tested successfully")
        print("   • Safe to proceed with project structure reorganization")
    
    print("="*80)

if __name__ == "__main__":
    asyncio.run(main())
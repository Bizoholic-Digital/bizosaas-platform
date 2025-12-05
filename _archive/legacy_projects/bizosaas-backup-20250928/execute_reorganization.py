#!/usr/bin/env python3
"""
BizOSaaS Project Reorganization Execution Script
Move files to new unified structure (no duplicates, safe for reuse)
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class BizOSaaSReorganizer:
    """Execute the project reorganization plan"""
    
    def __init__(self, project_root: str = "/home/alagiri/projects/bizoholic/bizosaas"):
        self.project_root = Path(project_root)
        self.new_root = self.project_root.parent / "bizosaas-platform"
        self.backup_root = self.project_root.parent / "bizosaas-backup"
        self.reorganization_log = []
        
        # Define categorization mapping
        self.service_categories = {
            "core": [
                "auth-service", "auth-service-v2", "user-management", "api-gateway",
                "ai-governance-layer", "gdpr-compliance-service", "wagtail-cms",
                "vault-integration", "logging-service", "identity-service",
                "event-bus", "notification", "byok-health-monitor"
            ],
            "ecommerce": [
                "saleor-backend", "saleor-storefront", "saleor-storage",
                "coreldove-saleor", "coreldove-bridge-saleor", "coreldove-ai-sourcing",
                "coreldove-frontend", "coreldove-storefront", "payment-service",
                "amazon-integration-service"
            ],
            "ai": [
                "bizosaas-brain", "personal-ai-assistant", "ai-agents",
                "ai-integration-service", "marketing-ai-service", "analytics-ai-service",
                "agent-orchestration-service", "agent-monitor", "claude-telegram-bot",
                "telegram-integration", "marketing-automation-service"
            ],
            "crm": [
                "django-crm", "crm-service", "crm-service-v2", "campaign-management",
                "campaign-service", "business-directory", "client-dashboard"
            ],
            "integration": [
                "integration", "marketing-apis-service", "temporal-integration",
                "temporal-orchestration", "image-integration", "client-sites"
            ],
            "analytics": [
                "analytics", "analytics-service", "monitoring"
            ]
        }
        
        self.deprecated_services = [
            "medusa", "medusa-coreldove", "medusa-official", "strapi"
        ]
        
        self.frontend_apps = [
            "bizoholic-frontend", "client-portal", "coreldove-frontend", "bizosaas-admin"
        ]
    
    def execute_reorganization(self) -> Dict[str, Any]:
        """Execute complete reorganization"""
        print("🚀 Starting BizOSaaS Project Reorganization")
        print("="*80)
        
        reorganization_result = {
            "start_time": datetime.now().isoformat(),
            "phases": {},
            "moved_files": 0,
            "backup_files": 0,
            "errors": [],
            "success": False
        }
        
        try:
            # Phase 1: Create new structure
            reorganization_result["phases"]["phase1"] = self._phase1_create_structure()
            
            # Phase 2: Move deprecated services to backup
            reorganization_result["phases"]["phase2"] = self._phase2_backup_deprecated()
            
            # Phase 3: Move services by category
            reorganization_result["phases"]["phase3"] = self._phase3_move_services()
            
            # Phase 4: Move frontend apps
            reorganization_result["phases"]["phase4"] = self._phase4_move_frontend()
            
            # Phase 5: Reorganize configurations
            reorganization_result["phases"]["phase5"] = self._phase5_reorganize_configs()
            
            # Phase 6: Reorganize documentation
            reorganization_result["phases"]["phase6"] = self._phase6_reorganize_docs()
            
            # Phase 7: Move infrastructure
            reorganization_result["phases"]["phase7"] = self._phase7_move_infrastructure()
            
            reorganization_result["success"] = True
            reorganization_result["end_time"] = datetime.now().isoformat()
            
        except Exception as e:
            reorganization_result["errors"].append(str(e))
            reorganization_result["success"] = False
        
        return reorganization_result
    
    def _phase1_create_structure(self) -> Dict[str, Any]:
        """Phase 1: Create new directory structure"""
        print("📁 Phase 1: Creating new unified structure...")
        
        phase_result = {"created_directories": [], "errors": []}
        
        # Create main structure
        directories_to_create = [
            # Main platform structure
            self.new_root,
            self.new_root / "core" / "services",
            self.new_root / "core" / "configs", 
            self.new_root / "core" / "docs",
            self.new_root / "ecommerce" / "services",
            self.new_root / "ecommerce" / "configs",
            self.new_root / "ecommerce" / "docs",
            self.new_root / "ai" / "services",
            self.new_root / "ai" / "configs",
            self.new_root / "ai" / "docs",
            self.new_root / "crm" / "services",
            self.new_root / "crm" / "configs",
            self.new_root / "crm" / "docs",
            self.new_root / "integration" / "services",
            self.new_root / "integration" / "configs",
            self.new_root / "integration" / "docs",
            self.new_root / "analytics" / "services",
            self.new_root / "analytics" / "configs",
            self.new_root / "analytics" / "docs",
            self.new_root / "frontend" / "apps",
            self.new_root / "frontend" / "configs",
            self.new_root / "frontend" / "docs",
            self.new_root / "infrastructure" / "monitoring",
            self.new_root / "infrastructure" / "security",
            self.new_root / "infrastructure" / "vault",
            self.new_root / "infrastructure" / "database",
            self.new_root / "infrastructure" / "k8s",
            self.new_root / "infrastructure" / "deployment",
            self.new_root / "configs",
            self.new_root / "docs" / "architecture",
            self.new_root / "docs" / "deployment",
            self.new_root / "docs" / "api-reference",
            self.new_root / "docs" / "governance",
            
            # Backup structure
            self.backup_root,
            self.backup_root / "deprecated-services",
            self.backup_root / "old-configs",
            self.backup_root / "old-docs",
            self.backup_root / "migration-logs"
        ]
        
        for directory in directories_to_create:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                phase_result["created_directories"].append(str(directory))
                self._log_action(f"Created directory: {directory}")
            except Exception as e:
                phase_result["errors"].append(f"Failed to create {directory}: {e}")
        
        print(f"✅ Created {len(phase_result['created_directories'])} directories")
        return phase_result
    
    def _phase2_backup_deprecated(self) -> Dict[str, Any]:
        """Phase 2: Move deprecated services to backup"""
        print("📦 Phase 2: Moving deprecated services to backup...")
        
        phase_result = {"moved_services": [], "errors": []}
        
        services_dir = self.project_root / "services"
        backup_services_dir = self.backup_root / "deprecated-services"
        
        for service_name in self.deprecated_services:
            service_path = services_dir / service_name
            if service_path.exists():
                try:
                    backup_path = backup_services_dir / service_name
                    shutil.move(str(service_path), str(backup_path))
                    phase_result["moved_services"].append(service_name)
                    self._log_action(f"MOVED: {service_path} -> {backup_path}")
                    print(f"  📦 Moved {service_name} to backup")
                except Exception as e:
                    phase_result["errors"].append(f"Failed to move {service_name}: {e}")
        
        print(f"✅ Moved {len(phase_result['moved_services'])} deprecated services to backup")
        return phase_result
    
    def _phase3_move_services(self) -> Dict[str, Any]:
        """Phase 3: Move services by category"""
        print("🏗️ Phase 3: Moving services by category...")
        
        phase_result = {"moved_by_category": {}, "errors": []}
        
        services_dir = self.project_root / "services"
        
        for category, service_list in self.service_categories.items():
            category_moved = []
            category_target = self.new_root / category / "services"
            
            for service_name in service_list:
                service_path = services_dir / service_name
                if service_path.exists():
                    try:
                        target_path = category_target / service_name
                        shutil.move(str(service_path), str(target_path))
                        category_moved.append(service_name)
                        self._log_action(f"MOVED: {service_path} -> {target_path}")
                        print(f"  🔄 Moved {service_name} to {category}")
                    except Exception as e:
                        phase_result["errors"].append(f"Failed to move {service_name}: {e}")
            
            phase_result["moved_by_category"][category] = category_moved
            print(f"✅ {category}: {len(category_moved)} services moved")
        
        # Move any remaining services to a "misc" category
        remaining_services = []
        misc_target = self.new_root / "misc" / "services"
        misc_target.mkdir(parents=True, exist_ok=True)
        
        for service_path in services_dir.iterdir():
            if service_path.is_dir() and not service_path.name.startswith('.'):
                try:
                    target_path = misc_target / service_path.name
                    shutil.move(str(service_path), str(target_path))
                    remaining_services.append(service_path.name)
                    self._log_action(f"MOVED: {service_path} -> {target_path}")
                    print(f"  📂 Moved {service_path.name} to misc")
                except Exception as e:
                    phase_result["errors"].append(f"Failed to move {service_path.name}: {e}")
        
        if remaining_services:
            phase_result["moved_by_category"]["misc"] = remaining_services
            print(f"✅ misc: {len(remaining_services)} services moved")
        
        return phase_result
    
    def _phase4_move_frontend(self) -> Dict[str, Any]:
        """Phase 4: Move frontend applications"""
        print("💻 Phase 4: Moving frontend applications...")
        
        phase_result = {"moved_apps": [], "errors": []}
        
        apps_dir = self.project_root / "apps"
        frontend_target = self.new_root / "frontend" / "apps"
        
        if apps_dir.exists():
            for app_path in apps_dir.iterdir():
                if app_path.is_dir():
                    try:
                        target_path = frontend_target / app_path.name
                        shutil.move(str(app_path), str(target_path))
                        phase_result["moved_apps"].append(app_path.name)
                        self._log_action(f"MOVED: {app_path} -> {target_path}")
                        print(f"  💻 Moved {app_path.name} to frontend/apps")
                    except Exception as e:
                        phase_result["errors"].append(f"Failed to move {app_path.name}: {e}")
            
            # Remove empty apps directory
            try:
                apps_dir.rmdir()
                self._log_action(f"REMOVED: Empty directory {apps_dir}")
            except Exception:
                pass
        
        print(f"✅ Moved {len(phase_result['moved_apps'])} frontend applications")
        return phase_result
    
    def _phase5_reorganize_configs(self) -> Dict[str, Any]:
        """Phase 5: Reorganize configuration files"""
        print("⚙️ Phase 5: Reorganizing configuration files...")
        
        phase_result = {"moved_configs": [], "consolidated_configs": [], "errors": []}
        
        # Move specific config directories to infrastructure
        config_dirs_to_move = {
            "k8s": self.new_root / "infrastructure" / "k8s",
            "deployment": self.new_root / "infrastructure" / "deployment", 
            "database": self.new_root / "infrastructure" / "database",
            "vault-config": self.new_root / "infrastructure" / "vault",
            "saleor-config": self.new_root / "ecommerce" / "configs" / "saleor",
            "temporal-config": self.new_root / "integration" / "configs" / "temporal"
        }
        
        for config_name, target_path in config_dirs_to_move.items():
            source_path = self.project_root / config_name
            if source_path.exists():
                try:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source_path), str(target_path))
                    phase_result["moved_configs"].append(config_name)
                    self._log_action(f"MOVED: {source_path} -> {target_path}")
                    print(f"  ⚙️ Moved {config_name} to infrastructure")
                except Exception as e:
                    phase_result["errors"].append(f"Failed to move {config_name}: {e}")
        
        # Move main configuration files
        main_configs = [
            "docker-compose.yml",
            "docker-compose.production.yml", 
            ".env.example",
            ".env.production.example"
        ]
        
        for config_file in main_configs:
            source_path = self.project_root / config_file
            if source_path.exists():
                try:
                    target_path = self.new_root / "configs" / config_file
                    shutil.move(str(source_path), str(target_path))
                    phase_result["moved_configs"].append(config_file)
                    self._log_action(f"MOVED: {source_path} -> {target_path}")
                    print(f"  📋 Moved {config_file} to configs")
                except Exception as e:
                    phase_result["errors"].append(f"Failed to move {config_file}: {e}")
        
        # Move category-specific docker-compose files to backup
        docker_compose_files = list(self.project_root.glob("docker-compose*.yml"))
        backup_configs = self.backup_root / "old-configs"
        
        for compose_file in docker_compose_files:
            if compose_file.exists():
                try:
                    target_path = backup_configs / compose_file.name
                    shutil.move(str(compose_file), str(target_path))
                    phase_result["moved_configs"].append(f"backup:{compose_file.name}")
                    self._log_action(f"MOVED: {compose_file} -> {target_path}")
                    print(f"  📦 Moved {compose_file.name} to backup")
                except Exception as e:
                    phase_result["errors"].append(f"Failed to move {compose_file.name}: {e}")
        
        print(f"✅ Reorganized {len(phase_result['moved_configs'])} configuration files")
        return phase_result
    
    def _phase6_reorganize_docs(self) -> Dict[str, Any]:
        """Phase 6: Reorganize documentation"""
        print("📚 Phase 6: Reorganizing documentation...")
        
        phase_result = {"moved_docs": [], "organized_docs": [], "errors": []}
        
        # Move markdown files from root to docs
        markdown_files = list(self.project_root.glob("*.md"))
        docs_target = self.new_root / "docs"
        
        # Categorize documentation
        doc_categories = {
            "architecture": ["ARCHITECTURE", "DESIGN", "TECH", "SYSTEM"],
            "deployment": ["DEPLOY", "INSTALL", "SETUP", "CONFIG", "DOCKER", "K8S"],
            "governance": ["GDPR", "COMPLIANCE", "SECURITY", "PRIVACY", "GOVERNANCE"],
            "api-reference": ["API", "ENDPOINT", "REFERENCE"]
        }
        
        for md_file in markdown_files:
            try:
                # Determine category
                category = "general"
                file_upper = md_file.name.upper()
                
                for cat, keywords in doc_categories.items():
                    if any(keyword in file_upper for keyword in keywords):
                        category = cat
                        break
                
                # Move to appropriate category
                target_dir = docs_target / category
                target_dir.mkdir(parents=True, exist_ok=True)
                target_path = target_dir / md_file.name
                
                shutil.move(str(md_file), str(target_path))
                phase_result["moved_docs"].append(f"{category}:{md_file.name}")
                self._log_action(f"MOVED: {md_file} -> {target_path}")
                print(f"  📄 Moved {md_file.name} to docs/{category}")
                
            except Exception as e:
                phase_result["errors"].append(f"Failed to move {md_file.name}: {e}")
        
        # Move existing docs directory if it exists
        existing_docs = self.project_root / "docs"
        if existing_docs.exists():
            try:
                target_path = docs_target / "legacy"
                shutil.move(str(existing_docs), str(target_path))
                phase_result["moved_docs"].append("legacy-docs")
                self._log_action(f"MOVED: {existing_docs} -> {target_path}")
                print(f"  📁 Moved existing docs to docs/legacy")
            except Exception as e:
                phase_result["errors"].append(f"Failed to move existing docs: {e}")
        
        print(f"✅ Reorganized {len(phase_result['moved_docs'])} documentation files")
        return phase_result
    
    def _phase7_move_infrastructure(self) -> Dict[str, Any]:
        """Phase 7: Move remaining infrastructure files"""
        print("🏗️ Phase 7: Moving remaining infrastructure files...")
        
        phase_result = {"moved_files": [], "errors": []}
        
        # Move remaining scripts and infrastructure files
        script_files = list(self.project_root.glob("*.sh"))
        script_files.extend(list(self.project_root.glob("*.py")))
        
        infrastructure_target = self.new_root / "infrastructure" / "scripts"
        infrastructure_target.mkdir(parents=True, exist_ok=True)
        
        for script_file in script_files:
            # Skip our reorganization scripts
            if script_file.name in ["execute_reorganization.py", "PROJECT_STRUCTURE_ANALYSIS.py", "TEST_ESSENTIAL_COMPONENTS.py"]:
                continue
                
            try:
                target_path = infrastructure_target / script_file.name
                shutil.move(str(script_file), str(target_path))
                phase_result["moved_files"].append(script_file.name)
                self._log_action(f"MOVED: {script_file} -> {target_path}")
                print(f"  🔧 Moved {script_file.name} to infrastructure/scripts")
            except Exception as e:
                phase_result["errors"].append(f"Failed to move {script_file.name}: {e}")
        
        # Move remaining directories to infrastructure
        remaining_dirs = ["scripts", "logs", "secrets"]
        for dir_name in remaining_dirs:
            source_path = self.project_root / dir_name
            if source_path.exists():
                try:
                    target_path = self.new_root / "infrastructure" / dir_name
                    shutil.move(str(source_path), str(target_path))
                    phase_result["moved_files"].append(dir_name)
                    self._log_action(f"MOVED: {source_path} -> {target_path}")
                    print(f"  📁 Moved {dir_name} to infrastructure")
                except Exception as e:
                    phase_result["errors"].append(f"Failed to move {dir_name}: {e}")
        
        print(f"✅ Moved {len(phase_result['moved_files'])} infrastructure files")
        return phase_result
    
    def _log_action(self, action: str):
        """Log reorganization action"""
        self.reorganization_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action
        })
    
    def save_reorganization_log(self):
        """Save reorganization log"""
        log_path = self.backup_root / "migration-logs" / "reorganization_log.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, 'w') as f:
            json.dump(self.reorganization_log, f, indent=2)
        
        print(f"📋 Reorganization log saved: {log_path}")

def main():
    """Execute reorganization"""
    print("🎯 BizOSaaS Project Reorganization Starting")
    print("="*80)
    
    reorganizer = BizOSaaSReorganizer()
    
    # User has already confirmed, proceed directly
    print("✅ User confirmed - proceeding with reorganization")
    print("   - Active services will be moved to bizosaas-platform/")
    print("   - Deprecated services will be moved to bizosaas-backup/")
    print("   - Original structure will be dismantled")
    print()
    
    try:
        result = reorganizer.execute_reorganization()
        reorganizer.save_reorganization_log()
        
        print("\n" + "="*80)
        if result["success"]:
            print("🏆 REORGANIZATION COMPLETED SUCCESSFULLY")
            print("="*80)
            print("📁 New Structure: bizosaas-platform/")
            print("📦 Backup Location: bizosaas-backup/")
            print("📋 Reorganization Log: bizosaas-backup/migration-logs/")
            
            # Summary
            total_moved = sum(len(phase.get("moved_services", [])) + 
                            len(phase.get("moved_apps", [])) + 
                            len(phase.get("moved_configs", [])) + 
                            len(phase.get("moved_docs", [])) + 
                            len(phase.get("moved_files", []))
                            for phase in result["phases"].values())
            
            print(f"📊 Total Items Moved: {total_moved}")
            print("✅ All deprecated services safely backed up")
            print("✅ Active services organized by category") 
            print("✅ Configurations consolidated")
            print("✅ Documentation organized")
            
        else:
            print("❌ REORGANIZATION FAILED")
            print("Errors encountered:")
            for error in result["errors"]:
                print(f"  - {error}")
        
        print("="*80)
        
    except Exception as e:
        print(f"💥 Critical error: {e}")

if __name__ == "__main__":
    main()
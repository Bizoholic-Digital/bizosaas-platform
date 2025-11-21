"""
N8N Workflow Templates Integration for CoreLDove
Integrates with awesome-n8n-templates repository and provides automation workflows
"""

import aiohttp
import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)

@dataclass
class N8NTemplate:
    """Represents an N8N workflow template"""
    id: str
    name: str
    description: str
    category: str
    use_case: str
    complexity: str
    template_url: str
    github_url: Optional[str] = None
    workflow_json: Optional[Dict[str, Any]] = None
    tags: List[str] = None
    requirements: Dict[str, Any] = None
    installations_count: int = 0
    success_rate: float = 0.0

class N8NTemplateManager:
    """Manages N8N workflow templates from awesome-n8n-templates repository"""
    
    def __init__(self):
        self.base_url = "https://api.github.com/repos/enescingoz/awesome-n8n-templates"
        self.templates_cache = {}
        self.last_updated = None
        
    async def fetch_awesome_templates(self) -> List[N8NTemplate]:
        """Fetch templates from the awesome-n8n-templates repository"""
        
        templates = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # Get repository contents
                async with session.get(f"{self.base_url}/contents") as response:
                    if response.status != 200:
                        logger.error(f"Failed to fetch repository contents: {response.status}")
                        return self._get_fallback_templates()
                    
                    contents = await response.json()
                    
                # Look for template files and directories
                for item in contents:
                    if item['type'] == 'dir' and 'template' in item['name'].lower():
                        # Fetch templates from subdirectory
                        subdir_templates = await self._fetch_templates_from_dir(session, item['path'])
                        templates.extend(subdir_templates)
                    elif item['name'].endswith('.json'):
                        # Individual template file
                        template = await self._process_template_file(session, item)
                        if template:
                            templates.append(template)
                            
        except Exception as e:
            logger.error(f"Error fetching awesome-n8n-templates: {e}")
            return self._get_fallback_templates()
            
        return templates
    
    async def _fetch_templates_from_dir(self, session: aiohttp.ClientSession, dir_path: str) -> List[N8NTemplate]:
        """Fetch templates from a specific directory"""
        
        templates = []
        
        try:
            async with session.get(f"{self.base_url}/contents/{dir_path}") as response:
                if response.status != 200:
                    return templates
                    
                contents = await response.json()
                
                for item in contents:
                    if item['name'].endswith('.json'):
                        template = await self._process_template_file(session, item)
                        if template:
                            templates.append(template)
                            
        except Exception as e:
            logger.error(f"Error fetching templates from directory {dir_path}: {e}")
            
        return templates
    
    async def _process_template_file(self, session: aiohttp.ClientSession, file_item: Dict[str, Any]) -> Optional[N8NTemplate]:
        """Process a single template file"""
        
        try:
            # Download the template file
            async with session.get(file_item['download_url']) as response:
                if response.status != 200:
                    return None
                    
                content = await response.text()
                workflow_json = json.loads(content)
                
                # Extract metadata from workflow
                template = self._extract_template_metadata(workflow_json, file_item)
                return template
                
        except Exception as e:
            logger.error(f"Error processing template file {file_item['name']}: {e}")
            return None
    
    def _extract_template_metadata(self, workflow_json: Dict[str, Any], file_item: Dict[str, Any]) -> N8NTemplate:
        """Extract metadata from workflow JSON"""
        
        # Extract basic info
        name = workflow_json.get('name', file_item['name'].replace('.json', ''))
        description = workflow_json.get('meta', {}).get('description', 'N8N workflow template')
        
        # Determine category and use case from workflow content
        category = self._determine_category(workflow_json)
        use_case = self._determine_use_case(workflow_json)
        complexity = self._determine_complexity(workflow_json)
        
        # Extract tags
        tags = self._extract_tags(workflow_json)
        
        # Extract requirements
        requirements = self._extract_requirements(workflow_json)
        
        return N8NTemplate(
            id=file_item['sha'][:8],
            name=name,
            description=description,
            category=category,
            use_case=use_case,
            complexity=complexity,
            template_url=file_item['html_url'],
            github_url=file_item['download_url'],
            workflow_json=workflow_json,
            tags=tags,
            requirements=requirements
        )
    
    def _determine_category(self, workflow_json: Dict[str, Any]) -> str:
        """Determine workflow category based on nodes and structure"""
        
        nodes = workflow_json.get('nodes', [])
        node_types = [node.get('type', '').lower() for node in nodes]
        
        # E-commerce related categories
        if any('shopify' in node_type for node_type in node_types):
            return 'e-commerce'
        elif any('amazon' in node_type for node_type in node_types):
            return 'marketplace'
        elif any('webhook' in node_type for node_type in node_types):
            return 'automation'
        elif any('schedule' in node_type for node_type in node_types):
            return 'monitoring'
        elif any('http' in node_type for node_type in node_types):
            return 'integration'
        else:
            return 'general'
    
    def _determine_use_case(self, workflow_json: Dict[str, Any]) -> str:
        """Determine specific use case"""
        
        name = workflow_json.get('name', '').lower()
        description = workflow_json.get('meta', {}).get('description', '').lower()
        
        content = f"{name} {description}"
        
        if 'price' in content and 'monitor' in content:
            return 'price_tracking'
        elif 'inventory' in content:
            return 'inventory_management'
        elif 'listing' in content:
            return 'marketplace_listing'
        elif 'keyword' in content:
            return 'seo_optimization'
        elif 'image' in content:
            return 'image_processing'
        elif 'review' in content:
            return 'review_monitoring'
        elif 'social' in content:
            return 'social_media'
        else:
            return 'general_automation'
    
    def _determine_complexity(self, workflow_json: Dict[str, Any]) -> str:
        """Determine workflow complexity"""
        
        nodes = workflow_json.get('nodes', [])
        connections = workflow_json.get('connections', {})
        
        node_count = len(nodes)
        connection_count = sum(len(conns) for conns in connections.values())
        
        # Calculate complexity based on structure
        if node_count <= 5 and connection_count <= 5:
            return 'beginner'
        elif node_count <= 15 and connection_count <= 20:
            return 'intermediate'
        else:
            return 'advanced'
    
    def _extract_tags(self, workflow_json: Dict[str, Any]) -> List[str]:
        """Extract relevant tags from workflow"""
        
        tags = set()
        
        # Extract from metadata
        meta_tags = workflow_json.get('meta', {}).get('tags', [])
        if isinstance(meta_tags, list):
            tags.update(meta_tags)
        
        # Extract from node types
        nodes = workflow_json.get('nodes', [])
        for node in nodes:
            node_type = node.get('type', '').lower()
            if node_type:
                tags.add(node_type)
        
        # Common e-commerce tags
        name_desc = f"{workflow_json.get('name', '')} {workflow_json.get('meta', {}).get('description', '')}".lower()
        
        ecommerce_keywords = {
            'amazon': 'amazon',
            'shopify': 'shopify', 
            'ebay': 'ebay',
            'product': 'products',
            'price': 'pricing',
            'inventory': 'inventory',
            'order': 'orders',
            'customer': 'customers',
            'review': 'reviews',
            'image': 'images',
            'keyword': 'keywords',
            'seo': 'seo'
        }
        
        for keyword, tag in ecommerce_keywords.items():
            if keyword in name_desc:
                tags.add(tag)
        
        return list(tags)[:10]  # Limit to 10 tags
    
    def _extract_requirements(self, workflow_json: Dict[str, Any]) -> Dict[str, Any]:
        """Extract workflow requirements"""
        
        requirements = {
            'credentials': [],
            'external_services': [],
            'prerequisites': []
        }
        
        nodes = workflow_json.get('nodes', [])
        
        for node in nodes:
            node_type = node.get('type', '').lower()
            
            # Check for credential requirements
            if 'credentials' in node:
                cred_type = node['credentials'].get('api', {}).get('type')
                if cred_type and cred_type not in requirements['credentials']:
                    requirements['credentials'].append(cred_type)
            
            # Check for external service requirements
            if any(service in node_type for service in ['shopify', 'amazon', 'ebay', 'google']):
                service_name = node_type.capitalize()
                if service_name not in requirements['external_services']:
                    requirements['external_services'].append(service_name)
        
        return requirements
    
    def _get_fallback_templates(self) -> List[N8NTemplate]:
        """Return fallback templates when GitHub API is unavailable"""
        
        fallback_templates = [
            N8NTemplate(
                id="fallback_001",
                name="Amazon Product Monitor",
                description="Monitor Amazon product prices and trigger alerts on changes",
                category="monitoring",
                use_case="price_tracking",
                complexity="intermediate",
                template_url="https://github.com/enescingoz/awesome-n8n-templates",
                tags=["amazon", "monitoring", "price-tracking"],
                requirements={"credentials": ["amazon-api"], "external_services": ["Amazon"]}
            ),
            N8NTemplate(
                id="fallback_002",
                name="eBay Listing Automation",
                description="Automatically create eBay listings from product data",
                category="automation",
                use_case="marketplace_listing",
                complexity="advanced",
                template_url="https://github.com/enescingoz/awesome-n8n-templates",
                tags=["ebay", "automation", "listing"],
                requirements={"credentials": ["ebay-api"], "external_services": ["eBay"]}
            ),
            N8NTemplate(
                id="fallback_003",
                name="Shopify Inventory Sync",
                description="Sync inventory levels across multiple platforms",
                category="synchronization",
                use_case="inventory_management", 
                complexity="intermediate",
                template_url="https://github.com/enescingoz/awesome-n8n-templates",
                tags=["shopify", "inventory", "sync"],
                requirements={"credentials": ["shopify-api"], "external_services": ["Shopify"]}
            ),
            N8NTemplate(
                id="fallback_004",
                name="Keyword Research Automation",
                description="Automatically research and analyze keywords for products",
                category="research",
                use_case="seo_optimization",
                complexity="advanced",
                template_url="https://github.com/enescingoz/awesome-n8n-templates",
                tags=["keywords", "seo", "research"],
                requirements={"credentials": ["google-ads-api"], "external_services": ["Google Ads"]}
            ),
            N8NTemplate(
                id="fallback_005",
                name="Competitor Price Tracking",
                description="Track competitor pricing and adjust accordingly",
                category="monitoring",
                use_case="competitive_analysis",
                complexity="intermediate",
                template_url="https://github.com/enescingoz/awesome-n8n-templates",
                tags=["competitors", "pricing", "monitoring"],
                requirements={"credentials": [], "external_services": []}
            ),
            N8NTemplate(
                id="fallback_006", 
                name="Product Image Processor",
                description="Batch process and optimize product images",
                category="processing",
                use_case="image_optimization",
                complexity="advanced",
                template_url="https://github.com/enescingoz/awesome-n8n-templates",
                tags=["images", "processing", "optimization"],
                requirements={"credentials": [], "external_services": ["Image Processing API"]}
            )
        ]
        
        return fallback_templates
    
    async def get_templates_by_category(self, category: str) -> List[N8NTemplate]:
        """Get templates filtered by category"""
        
        templates = await self.fetch_awesome_templates()
        return [t for t in templates if t.category.lower() == category.lower()]
    
    async def get_templates_by_use_case(self, use_case: str) -> List[N8NTemplate]:
        """Get templates filtered by use case"""
        
        templates = await self.fetch_awesome_templates()
        return [t for t in templates if t.use_case.lower() == use_case.lower()]
    
    async def get_templates_by_complexity(self, complexity: str) -> List[N8NTemplate]:
        """Get templates filtered by complexity level"""
        
        templates = await self.fetch_awesome_templates()
        return [t for t in templates if t.complexity.lower() == complexity.lower()]
    
    async def search_templates(self, query: str) -> List[N8NTemplate]:
        """Search templates by name, description, or tags"""
        
        templates = await self.fetch_awesome_templates()
        query = query.lower()
        
        results = []
        for template in templates:
            if (query in template.name.lower() or 
                query in template.description.lower() or
                any(query in tag.lower() for tag in (template.tags or []))):
                results.append(template)
        
        return results
    
    async def get_recommended_templates(self, product_data: Dict[str, Any]) -> List[N8NTemplate]:
        """Get recommended templates based on product data"""
        
        templates = await self.fetch_awesome_templates()
        recommendations = []
        
        # Analyze product data to determine relevant templates
        category = product_data.get('category', '').lower()
        source_type = product_data.get('source_type', '').lower()
        
        # Score templates based on relevance
        scored_templates = []
        for template in templates:
            score = 0
            
            # Category match
            if category and category in template.name.lower():
                score += 3
            if category and category in template.description.lower():
                score += 2
            
            # Source type match (amazon, ebay, etc.)
            if source_type and source_type in template.name.lower():
                score += 4
            if source_type and source_type in (template.tags or []):
                score += 3
            
            # Use case relevance
            relevant_use_cases = [
                'price_tracking', 'inventory_management', 'marketplace_listing',
                'seo_optimization', 'image_processing', 'competitive_analysis'
            ]
            if template.use_case in relevant_use_cases:
                score += 2
            
            # Success rate bonus
            if template.success_rate > 80:
                score += 1
            
            if score > 0:
                scored_templates.append((template, score))
        
        # Sort by score and return top recommendations
        scored_templates.sort(key=lambda x: x[1], reverse=True)
        return [template for template, score in scored_templates[:6]]

class WorkflowTemplateService:
    """Service for managing and deploying workflow templates"""
    
    def __init__(self, n8n_api_url: str, n8n_api_key: str):
        self.n8n_api_url = n8n_api_url
        self.n8n_api_key = n8n_api_key
        self.template_manager = N8NTemplateManager()
        
    async def deploy_template(self, template: N8NTemplate, tenant_id: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Deploy a template to N8N instance"""
        
        try:
            if not template.workflow_json:
                raise ValueError("Template workflow JSON not available")
            
            # Customize workflow for tenant
            customized_workflow = self._customize_workflow(template.workflow_json, tenant_id, config or {})
            
            # Deploy to N8N
            headers = {
                'X-N8N-API-KEY': self.n8n_api_key,
                'Content-Type': 'application/json'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.n8n_api_url}/workflows",
                    headers=headers,
                    json=customized_workflow
                ) as response:
                    if response.status == 201:
                        result = await response.json()
                        logger.info(f"Template {template.name} deployed successfully for tenant {tenant_id}")
                        return {
                            "success": True,
                            "workflow_id": result.get('id'),
                            "message": "Template deployed successfully"
                        }
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to deploy template: {response.status} - {error_text}")
                        return {
                            "success": False,
                            "error": f"Deployment failed: {response.status}"
                        }
        
        except Exception as e:
            logger.error(f"Error deploying template {template.name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _customize_workflow(self, workflow_json: Dict[str, Any], tenant_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Customize workflow JSON for specific tenant and configuration"""
        
        customized = workflow_json.copy()
        
        # Update workflow name to include tenant
        original_name = customized.get('name', 'Unnamed Workflow')
        customized['name'] = f"{original_name} - {tenant_id}"
        
        # Update node configurations based on config
        nodes = customized.get('nodes', [])
        for node in nodes:
            # Update webhook URLs
            if node.get('type') == 'webhook':
                if 'parameters' not in node:
                    node['parameters'] = {}
                node['parameters']['path'] = f"/{tenant_id}/{node['parameters'].get('path', 'webhook')}"
            
            # Update database connections
            elif 'database' in node.get('type', '').lower():
                if 'parameters' not in node:
                    node['parameters'] = {}
                # Use tenant-specific database settings
                if 'database' in config:
                    node['parameters'].update(config['database'])
            
            # Update API credentials
            elif 'credentials' in node:
                # Prefix credential names with tenant ID for isolation
                for cred_key, cred_value in node['credentials'].items():
                    if isinstance(cred_value, dict) and 'id' in cred_value:
                        cred_value['id'] = f"{tenant_id}_{cred_value['id']}"
        
        return customized
    
    async def get_template_requirements(self, template: N8NTemplate) -> Dict[str, Any]:
        """Get detailed requirements for deploying a template"""
        
        requirements = template.requirements or {}
        
        # Add deployment-specific requirements
        deployment_requirements = {
            "credentials_needed": requirements.get('credentials', []),
            "external_services": requirements.get('external_services', []),
            "prerequisites": requirements.get('prerequisites', []),
            "estimated_setup_time": self._estimate_setup_time(template),
            "complexity_level": template.complexity,
            "recommended_for": self._get_recommendations(template)
        }
        
        return deployment_requirements
    
    def _estimate_setup_time(self, template: N8NTemplate) -> str:
        """Estimate setup time based on complexity"""
        
        complexity_times = {
            'beginner': '10-20 minutes',
            'intermediate': '30-60 minutes', 
            'advanced': '1-3 hours'
        }
        
        return complexity_times.get(template.complexity, '30-60 minutes')
    
    def _get_recommendations(self, template: N8NTemplate) -> List[str]:
        """Get recommendations for when to use this template"""
        
        recommendations = []
        
        if template.use_case == 'price_tracking':
            recommendations.extend([
                "Products with frequent price changes",
                "Competitive markets with multiple sellers",
                "High-value products where price monitoring is critical"
            ])
        elif template.use_case == 'inventory_management':
            recommendations.extend([
                "Multi-channel selling operations",
                "Products with limited stock",
                "Businesses with complex supply chains"
            ])
        elif template.use_case == 'marketplace_listing':
            recommendations.extend([
                "Large product catalogs",
                "Regular new product launches", 
                "Cross-platform selling strategies"
            ])
        
        return recommendations

# Usage example
async def main():
    """Example usage of N8N Template Integration"""
    
    # Initialize template manager
    template_manager = N8NTemplateManager()
    
    # Fetch available templates
    templates = await template_manager.fetch_awesome_templates()
    print(f"Found {len(templates)} templates")
    
    # Search for specific templates
    amazon_templates = await template_manager.search_templates("amazon")
    print(f"Found {len(amazon_templates)} Amazon-related templates")
    
    # Get recommendations for a product
    product_data = {
        "category": "electronics",
        "source_type": "amazon",
        "profit_potential": "high"
    }
    
    recommended = await template_manager.get_recommended_templates(product_data)
    print(f"Recommended templates: {[t.name for t in recommended]}")
    
    # Initialize workflow service (would use actual N8N credentials)
    # workflow_service = WorkflowTemplateService("https://n8n.example.com/api/v1", "your-api-key")
    
    # Deploy a template
    # result = await workflow_service.deploy_template(recommended[0], "tenant123")
    # print(f"Deployment result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
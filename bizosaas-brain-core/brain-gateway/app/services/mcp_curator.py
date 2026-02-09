from datetime import datetime, timezone
from typing import Dict, Any, List
import json
from ..models.mcp import McpRegistry

class McpCuratorService:
    """
    Service responsible for calculating quality scores for MCP servers
    and curating the registry based on various metrics.
    """

    @staticmethod
    def calculate_quality_score(mcp_data: Dict[str, Any]) -> int:
        """
        Calculates a quality score (0-100) based on source, popularity, 
        and maintenance metrics.
        
        Scoring logic:
        - Source Type: Official (30), Community w/ Org (20), Individual (5)
        - Popularity (Stars): 1000+ (30), 100+ (20), 10+ (10)
        - Maintenance: Commit < 30d (20), < 90d (15), < 180d (10)
        - Security: Passed Audit (20), No Audit but clean (10)
        """
        score = 0
        
        # 1. Source Type (Max 30)
        source_type = mcp_data.get('source_type', 'community')
        creator_org = mcp_data.get('creator_org')
        
        if source_type == 'official':
            score += 30
        elif source_type == 'community' and creator_org:
            score += 20
        else:
            score += 5
            
        # 2. Popularity / GitHub Stars (Max 30)
        stars = mcp_data.get('github_stars', 0)
        if stars >= 1000:
            score += 30
        elif stars >= 100:
            score += 20
        elif stars >= 10:
            score += 10
            
        # 3. Maintenance (Max 20)
        is_maintained = mcp_data.get('is_maintained', True)
        last_commit = mcp_data.get('last_commit_date')
        
        if is_maintained and last_commit:
            if isinstance(last_commit, str):
                try:
                    last_commit = datetime.fromisoformat(last_commit.replace('Z', '+00:00'))
                except ValueError:
                    last_commit = None
            
            if last_commit:
                delta = datetime.now(timezone.utc) - last_commit
                days_since = delta.days
                if days_since < 30:
                    score += 20
                elif days_since < 90:
                    score += 15
                elif days_since < 180:
                    score += 10
                    
        # 4. Security Status (Max 20)
        security_status = mcp_data.get('security_audit_status', 'not_required')
        if security_status == 'passed':
            score += 20
        elif security_status == 'not_required':
            score += 10
            
        return min(score, 100)

    @staticmethod
    def classify_and_tag(mcp_registry_item: McpRegistry):
        """
        Processes an MCP registry item, updates its quality score,
        sets recommended flag, and applies tags based on its data.
        """
        # Prepare data for scoring
        data = {
            'source_type': mcp_registry_item.source_type,
            'creator_org': mcp_registry_item.creator_org,
            'github_stars': mcp_registry_item.github_stars,
            'is_maintained': mcp_registry_item.is_maintained,
            'last_commit_date': mcp_registry_item.last_commit_date,
            'security_audit_status': mcp_registry_item.security_audit_status
        }
        
        score = McpCuratorService.calculate_quality_score(data)
        mcp_registry_item.quality_score = score
        mcp_registry_item.is_recommended = score >= 80
        
        # Auto-tagging logic
        tags = set(mcp_registry_item.tags or [])
        
        if mcp_registry_item.source_type == 'official':
            tags.add('official')
        
        if mcp_registry_item.is_recommended:
            tags.add('recommended')
            
        if 'graphql' in (mcp_registry_item.description or '').lower():
            tags.add('graphql')
            
        if 'rest' in (mcp_registry_item.description or '').lower():
            tags.add('rest')
            
        if mcp_registry_item.github_stars > 500:
            tags.add('popular')
            
        mcp_registry_item.tags = list(tags)
        
        return mcp_registry_item

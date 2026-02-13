#!/usr/bin/env python3
"""
Fix remaining DOKPLOY_API_KEY context access warnings in deployment workflows.
This script ensures all deploy-*.yml files use the env block pattern for secret access.
"""

import os
import re
from pathlib import Path

def fix_dokploy_secret(filepath):
    """Fix DOKPLOY_API_KEY usage in a workflow file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern 1: Direct secret access in curl command without env block
    # Match the "Trigger Dokploy Deployment" step
    pattern1 = r'(- name: Trigger Dokploy Deployment.*?\n)(        run: \|.*?curl.*?-H "X-API-Key: \$\{\{ secrets\.DOKPLOY_API_KEY \}\}")'
    
    def replacement1(match):
        step_name = match.group(1)
        run_block = match.group(2)
        # Add env block and update the run command
        new_run = run_block.replace(
            '-H "X-API-Key: ${{ secrets.DOKPLOY_API_KEY }}"',
            '-H "X-API-Key: $DOKPLOY_API_KEY"'
        )
        return f'{step_name}        env:\n          DOKPLOY_API_KEY: ${{{{ secrets.DOKPLOY_API_KEY }}}}\n{new_run}'
    
    content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)
    
    # Pattern 2: Already has env block but still uses ${{ secrets.DOKPLOY_API_KEY }} in curl
    pattern2 = r'(-H "X-API-Key: )\$\{\{ secrets\.DOKPLOY_API_KEY \}\}(")'
    content = re.sub(pattern2, r'\1$DOKPLOY_API_KEY\2', content)
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✓ Fixed {filepath}")
        return True
    else:
        print(f"  No changes needed for {filepath}")
        return False

def main():
    workflows_dir = Path('.github/workflows')
    
    # Find all deploy-*.yml files
    deploy_files = list(workflows_dir.glob('deploy-*.yml'))
    
    fixed_count = 0
    for filepath in deploy_files:
        if fix_dokploy_secret(filepath):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} out of {len(deploy_files)} deployment workflows")

if __name__ == "__main__":
    main()

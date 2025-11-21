#!/usr/bin/env python3
"""
Secret Migration Script
Migrates secrets from .env files to HashiCorp Vault
"""
import os
import sys
import logging
from typing import Dict, Any
from dotenv import dotenv_values

# Add the directory containing vault_client to path
sys.path.append(os.path.join(os.getcwd(), 'bizosaas/ai/services/bizosaas-brain'))

from vault_client import get_vault_client

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def migrate_secrets():
    """Migrate secrets from .env files to Vault"""
    vault = get_vault_client()
    
    # Check Vault connection
    health = vault.health_check()
    if not health.get('vault_connected'):
        logger.error(f"Cannot connect to Vault: {health.get('error')}")
        return

    logger.info("Connected to Vault. Starting migration...")

    # Define mappings from .env files to Vault paths
    # Format: (env_file_path, vault_path_prefix, secret_mapping)
    # secret_mapping: { 'ENV_VAR_NAME': 'vault_key' } or None for all
    
    migrations = [
        (
            'bizosaas/ai/services/bizosaas-brain/.env.saleor',
            'bizosaas/saleor',
            None # Import all
        ),
        (
            'bizosaas/ai/services/bizosaas-brain/.env.analytics',
            'bizosaas/analytics',
            None
        ),
         (
            'bizosaas/ai/services/bizosaas-brain/.env',
             'bizosaas/ai-agents',
             None
         )
    ]
    
    # Add more specific mappings for core services if their .env files are found
    # For example, database credentials often in a root .env or specific service .env
    
    # Database Config (Example mapping if found in a common .env)
    # We might need to construct this manually if it's scattered
    
    for env_path, vault_path, mapping in migrations:
        if not os.path.exists(env_path):
            logger.warning(f"Environment file not found: {env_path}")
            continue
            
        logger.info(f"Processing {env_path} -> {vault_path}")
        
        env_vars = dotenv_values(env_path)
        secrets_to_store = {}
        
        if mapping:
            for env_key, vault_key in mapping.items():
                if env_key in env_vars:
                    secrets_to_store[vault_key] = env_vars[env_key]
        else:
            # Store all, converting keys to lowercase for consistency if needed
            # or keeping as is. Let's keep as is for now, or lowercase?
            # Vault keys are usually lowercase.
            for key, value in env_vars.items():
                secrets_to_store[key.lower()] = value
                
        if secrets_to_store:
            if vault.put_secret(vault_path, secrets_to_store):
                logger.info(f"Successfully migrated {len(secrets_to_store)} secrets to {vault_path}")
            else:
                logger.error(f"Failed to migrate secrets to {vault_path}")
        else:
            logger.info(f"No secrets found to migrate in {env_path}")

    logger.info("Migration completed.")

if __name__ == "__main__":
    migrate_secrets()

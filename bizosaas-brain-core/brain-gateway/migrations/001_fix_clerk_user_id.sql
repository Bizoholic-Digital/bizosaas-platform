-- Migration: Fix user_id type mismatch in user_mcp_installations
-- Issue: Clerk provides string user IDs, but column was defined as UUID
-- Date: 2026-01-10

BEGIN;

-- Step 1: Drop the foreign key constraint
ALTER TABLE user_mcp_installations 
DROP CONSTRAINT IF EXISTS user_mcp_installations_user_id_fkey;

-- Step 2: Change column type from UUID to VARCHAR
ALTER TABLE user_mcp_installations 
ALTER COLUMN user_id TYPE VARCHAR(255);

-- Step 3: Add index for performance
CREATE INDEX IF NOT EXISTS ix_user_mcp_installations_user_id 
ON user_mcp_installations(user_id);

COMMIT;

-- Verification query
SELECT 
    column_name, 
    data_type, 
    character_maximum_length 
FROM information_schema.columns 
WHERE table_name = 'user_mcp_installations' 
AND column_name = 'user_id';

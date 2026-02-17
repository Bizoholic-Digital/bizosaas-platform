# Database Migration Guide - Fix Clerk User ID Type

## Issue
The `user_mcp_installations` table had `user_id` defined as UUID, but Clerk provides string-based user IDs like `user_37SpjCv6JUvLxu5cl8IHzQ2DzCG`, causing this error:

```
sqlalchemy.exc.DataError: invalid input syntax for type uuid: "user_37SpjCv6JUvLxu5cl8IHzQ2DzCG"
```

## Solution
Changed `user_id` column from UUID to VARCHAR(255) to support Clerk's string-based user IDs.

## Running the Migration

### Option 1: Using Raw SQL (Recommended for Production)

```bash
# Connect to your database
psql -h <host> -U <user> -d <database>

# Or if using Docker
docker exec -it brain-postgres psql -U postgres -d bizosaas

# Run the migration
\i /path/to/bizosaas-brain-core/brain-gateway/migrations/001_fix_clerk_user_id.sql
```

### Option 2: Using Alembic (If configured)

```bash
cd bizosaas-brain-core/brain-gateway
alembic upgrade head
```

### Option 3: Direct SQL Command

```bash
# For Docker Postgres
docker exec -i brain-postgres psql -U postgres -d bizosaas <<EOF
BEGIN;
ALTER TABLE user_mcp_installations DROP CONSTRAINT IF EXISTS user_mcp_installations_user_id_fkey;
ALTER TABLE user_mcp_installations ALTER COLUMN user_id TYPE VARCHAR(255);
CREATE INDEX IF NOT EXISTS ix_user_mcp_installations_user_id ON user_mcp_installations(user_id);
COMMIT;
EOF
```

## Verification

After running the migration, verify the change:

```sql
SELECT 
    column_name, 
    data_type, 
    character_maximum_length 
FROM information_schema.columns 
WHERE table_name = 'user_mcp_installations' 
AND column_name = 'user_id';
```

Expected output:
```
 column_name | data_type      | character_maximum_length
-------------+----------------+-------------------------
 user_id     | character varying | 255
```

## What Changed

### Model Changes
- **File**: `app/models/mcp.py`
- **Change**: `user_id` column type from `GUID` to `String(255)`
- **Impact**: Removed foreign key relationship to `users` table since Clerk IDs don't map to local user records

### Database Schema
```sql
-- Before
user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE

-- After  
user_id VARCHAR(255) NOT NULL
CREATE INDEX ix_user_mcp_installations_user_id ON user_mcp_installations(user_id)
```

## Rollback (If Needed)

If you need to rollback this change:

```sql
BEGIN;
DROP INDEX IF EXISTS ix_user_mcp_installations_user_id;
ALTER TABLE user_mcp_installations ALTER COLUMN user_id TYPE UUID USING user_id::uuid;
ALTER TABLE user_mcp_installations 
    ADD CONSTRAINT user_mcp_installations_user_id_fkey 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
COMMIT;
```

⚠️ **Warning**: Rollback will fail if you have any Clerk user IDs stored in the table.

## Testing

After migration, test the MCP installations endpoint:

```bash
# Should no longer throw UUID error
curl -H "Authorization: Bearer <clerk-token>" \
     https://api.bizoholic.net/api/mcp/installed
```

## Notes

- This migration is **safe to run** on existing data
- The change is **backward compatible** if the table is empty
- No data loss occurs during migration
- The index improves query performance for user-specific MCP lookups

## Migration 006: Support Ticket Messages

### Run
```bash
docker exec -it brain-postgres psql -U postgres -d bizosaas -f /path/to/bizosaas-brain-core/brain-gateway/migrations/006_support_ticket_messages.sql
# OR
docker exec -i brain-postgres psql -U postgres -d bizosaas < migrations/006_support_ticket_messages.sql
```

#!/bin/bash
# Quick setup script for Phase 0.5C: Vector DB Migration
# Run this script to execute the HNSW index migration on NeonDB

set -e  # Exit on error

echo "🚀 Phase 0.5C: Running HNSW Index Migration on NeonDB"
echo "=================================================="

# NeonDB connection string (from your credentials.md)
export DATABASE_URL="postgresql://neondb_owner:npg_puEbTnkSO9F8@ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

# Redis Cloud connection string
export REDIS_CLOUD_URL="redis://bizosaas-admin:rwL1HrSHn01$^w@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690"

echo ""
echo "📊 Database: ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/neondb"
echo "🔴 Redis: redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690"
echo ""

# Check if we're in the right directory
if [ ! -f "bizosaas-brain-core/brain-gateway/migrations/add_hnsw_indexes.py" ]; then
    echo "❌ Error: Migration script not found!"
    echo "Please run this script from the project root: /home/alagiri/projects/bizosaas-platform"
    exit 1
fi

echo "✅ Migration script found"
echo ""
echo "🔧 Running migration..."
echo ""

# Run the migration
python bizosaas-brain-core/brain-gateway/migrations/add_hnsw_indexes.py

echo ""
echo "✅ Migration completed!"
echo ""
echo "📝 Next steps:"
echo "1. Verify RediSearch is enabled on Redis Cloud (see phase_0.5c_setup_guide.md)"
echo "2. Store DATABASE_URL and REDIS_CLOUD_URL in Vault"
echo "3. Deploy Brain Gateway to staging"
echo "4. Monitor cache hit rates in logs"

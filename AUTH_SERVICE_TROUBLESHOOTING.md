# Auth Service Not Responding - Troubleshooting Guide

## 🔴 Issue
Auth Service started (PID: 1682391) but is not responding to health checks.

## 🔍 Diagnostic Steps

### Step 1: Check if the process is still running
```bash
ps aux | grep 1682391
```

**Expected**: Should show the uvicorn process  
**If not found**: Process crashed, check logs

### Step 2: Check the Auth Service logs
```bash
tail -100 /tmp/auth-service.log
```

**Look for**:
- Import errors (missing dependencies)
- Database connection errors
- Port binding errors
- Python syntax errors

### Step 3: Check if port 8008 is listening
```bash
lsof -i :8008
```

**Expected**: Should show python/uvicorn listening  
**If empty**: Service failed to start

### Step 4: Check database connectivity
```bash
PGPASSWORD=postgres psql -h localhost -U postgres -d bizosaas -c "SELECT 1;"
```

**Expected**: Should return `1`  
**If error**: Database is not accessible

### Step 5: Try starting Auth Service manually
```bash
cd shared/services/auth
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas"
export REDIS_URL="redis://localhost:6379/0"
uvicorn main:app --host 0.0.0.0 --port 8008
```

**Watch for**:
- Import errors
- Database connection errors
- Missing environment variables

## 🐛 Common Issues & Fixes

### Issue 1: Database Connection Error
**Symptom**: Logs show "could not connect to server" or "connection refused"

**Fix**:
```bash
# Check if Postgres is running
docker ps | grep postgres

# If not running, start it
docker-compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres

# Wait 5 seconds
sleep 5

# Restart Auth Service
cd shared/services/auth
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas"
uvicorn main:app --host 0.0.0.0 --port 8008 --reload
```

### Issue 2: Import Error (Missing Dependencies)
**Symptom**: Logs show "ModuleNotFoundError" or "ImportError"

**Fix**:
```bash
cd shared/services/auth
pip install -r requirements.txt
```

### Issue 3: Port Already in Use
**Symptom**: Logs show "Address already in use"

**Fix**:
```bash
# Find and kill the process using port 8008
lsof -t -i :8008 | xargs kill -9

# Wait a moment
sleep 2

# Restart Auth Service
cd shared/services/auth
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas"
uvicorn main:app --host 0.0.0.0 --port 8008 --reload
```

### Issue 4: Redis Connection Error
**Symptom**: Logs show "Error connecting to Redis"

**Fix**:
```bash
# Check if Redis is running
docker ps | grep redis

# If not running, start it
docker-compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d redis

# Restart Auth Service
cd shared/services/auth
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas"
export REDIS_URL="redis://localhost:6379/0"
uvicorn main:app --host 0.0.0.0 --port 8008 --reload
```

### Issue 5: Python/Uvicorn Not Found
**Symptom**: Command not found errors

**Fix**:
```bash
# Install uvicorn
pip install uvicorn

# Or use python -m uvicorn
cd shared/services/auth
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8008 --reload
```

## ✅ Quick Fix (Most Common)

The most common issue is database connectivity. Try this:

```bash
# 1. Ensure Postgres is running
docker-compose -f shared/infrastructure/docker-compose.infrastructure.yml up -d postgres redis

# 2. Wait for it to be ready
sleep 5

# 3. Start Auth Service manually
cd shared/services/auth
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas"
export REDIS_URL="redis://localhost:6379/0"
uvicorn main:app --host 0.0.0.0 --port 8008 --reload
```

## 🧪 Verify It's Working

Once started, test in another terminal:

```bash
# Health check
curl http://localhost:8008/health

# Should return: {"status":"healthy","service":"auth-service"}
```

## 📝 Next Steps After Fix

1. **If Auth Service works manually**:
   - Update the startup script to wait longer for database
   - Or add retry logic

2. **If still not working**:
   - Check the actual error in `/tmp/auth-service.log`
   - Share the error message for further debugging

3. **Once working**:
   - Test login at `http://localhost:3003/login`
   - Verify dashboard loads

## 🎯 Most Likely Cause

Based on the symptoms (service starts but doesn't respond), the most likely causes are:

1. **Database not ready** - Auth Service tries to connect before Postgres is fully initialized
2. **Import error** - Missing Python dependency
3. **Configuration error** - Wrong DATABASE_URL or missing environment variable

**Recommended Action**: Run the "Quick Fix" above and check the logs.

# Bizoholic Startup Issues - Resolution Guide

## Problem Summary

After laptop restart, the startup script `./scripts/start-bizoholic-full.sh` encounters two main issues:

1. **Frontend Port Conflict (EADDRINUSE on port 3001)**
   - Caused by orphaned processes or insufficient wait time for Next.js compilation
   - Health check fails because Next.js takes 60-90 seconds to compile

2. **Auth Service Fails to Start**
   - Database connection error: "the database system is starting up"
   - Auth service tries to connect before Postgres is fully ready

## Root Causes

### 1. Frontend Issues
- **Insufficient wait time**: Script waits only 15 seconds, but Next.js needs 60-90 seconds
- **Orphaned processes**: PID files may reference dead processes
- **Multiple processes**: Sometimes multiple processes bind to port 3001

### 2. Backend Service Timing
- **Race condition**: Services start before infrastructure is ready
- **Postgres startup time**: Takes 5-10 seconds to accept connections
- **No retry logic**: Services fail immediately if DB isn't ready

## Solutions Implemented

### 1. Enhanced Start Script (`start-bizoholic-full.sh`)

**Changes made:**
- ✅ Improved process cleanup (handles multiple PIDs on port 3001)
- ✅ Increased wait time from 15s to 90s for Next.js compilation
- ✅ Better PID file management
- ✅ More informative status messages

**Key improvements:**
```bash
# Kill ALL processes on port 3001, not just one
EXISTING_PIDS=$(lsof -Pi :3001 -sTCP:LISTEN -t)
for PID in $EXISTING_PIDS; do
    kill -9 $PID 2>/dev/null || true
done

# Wait 90 seconds for Next.js to compile
sleep 90  # Next.js needs significant time to compile on first start
```

### 2. Enhanced Stop Script (`stop-bizoholic-full.sh`)

**Changes made:**
- ✅ Stops all processes on port 3001 (not just PID file)
- ✅ Cleans up log files
- ✅ Includes Wagtail CMS in services to stop
- ✅ Better error handling

### 3. New Status Script (`status-bizoholic.sh`)

**Features:**
- ✅ Check all services (frontend, backend, infrastructure)
- ✅ HTTP health checks
- ✅ Show recent frontend logs
- ✅ Color-coded status output

## Usage Instructions

### Starting Services

```bash
cd ~/projects/bizosaas-platform
./scripts/start-bizoholic-full.sh
```

**Expected timeline:**
- Infrastructure: 5 seconds
- Backend services: 35 seconds
- Frontend compilation: 60-90 seconds
- **Total: ~2-3 minutes**

### Stopping Services

```bash
./scripts/stop-bizoholic-full.sh
```

This will:
- Stop frontend (all processes on port 3001)
- Stop backend services (Brain, Auth, CRM, Wagtail)
- Keep infrastructure running (Postgres, Redis, Vault)

### Checking Status

```bash
./scripts/status-bizoholic.sh
```

This shows:
- Frontend status and recent logs
- Backend service health
- Infrastructure status
- Quick access URLs

## Troubleshooting

### Issue: "Port 3001 already in use"

**Solution 1: Use the stop script**
```bash
./scripts/stop-bizoholic-full.sh
```

**Solution 2: Manual cleanup**
```bash
# Find and kill processes on port 3001
lsof -i :3001 -sTCP:LISTEN -t | xargs kill -9

# Clean up PID file
rm /tmp/bizoholic-frontend.pid
```

### Issue: "Auth service not running"

**Cause**: Postgres not ready when Auth starts

**Solution**: Restart just the auth service
```bash
docker-compose -f shared/services/docker-compose.services.yml restart auth
```

Or restart all backend services:
```bash
docker-compose -f shared/services/docker-compose.services.yml restart brain-gateway auth crm cms
```

### Issue: "Frontend shows 'Not responding'"

**Cause**: Next.js still compiling

**Solution**: Wait longer or check logs
```bash
# Check if it's still compiling
tail -f /tmp/bizoholic-frontend.log

# Look for "Ready in XX.Xs" message
```

### Issue: After laptop restart, services won't start

**Solution**: Full cleanup and restart
```bash
# 1. Stop everything
./scripts/stop-bizoholic-full.sh

# 2. Stop infrastructure too
docker-compose -f shared/infrastructure/docker-compose.infrastructure.yml stop

# 3. Clean up any orphaned processes
lsof -i :3001 -sTCP:LISTEN -t | xargs kill -9 2>/dev/null || true

# 4. Start fresh
./scripts/start-bizoholic-full.sh
```

## Service URLs

Once all services are running:

- **Frontend**: http://localhost:3001
- **Brain API**: http://localhost:8000
- **Auth Service**: http://localhost:8007
- **CRM**: http://localhost:8005
- **Wagtail CMS**: http://localhost:8002

### Embedded Admin Panels (via Frontend)

- **Wagtail**: http://localhost:3001/portal/dashboard/content
- **CRM**: http://localhost:3001/portal/dashboard/crm

## Best Practices

### 1. Always use the scripts
- ✅ Use `start-bizoholic-full.sh` to start
- ✅ Use `stop-bizoholic-full.sh` to stop
- ✅ Use `status-bizoholic.sh` to check

### 2. Be patient with startup
- Infrastructure: ~5 seconds
- Backend: ~35 seconds
- Frontend: ~90 seconds
- **Don't interrupt during startup**

### 3. Check status before restarting
```bash
./scripts/status-bizoholic.sh
```

### 4. Clean shutdown before laptop sleep/restart
```bash
./scripts/stop-bizoholic-full.sh
```

## Known Limitations

1. **Frontend compilation time**: Next.js dev server takes 60-90 seconds on first start
2. **Auth service timing**: May need manual restart if Postgres takes longer than expected
3. **Wagtail health**: Sometimes shows unhealthy even when working
4. **Temporal service**: May restart a few times before stabilizing

## Future Improvements

1. **Add retry logic to Auth service** - Automatically retry DB connection
2. **Implement health check dependencies** - Services wait for dependencies
3. **Add frontend pre-compilation** - Build .next folder in advance
4. **Create systemd services** - Auto-start on boot
5. **Add Docker health checks** - Better container orchestration

## Files Modified

1. `/scripts/start-bizoholic-full.sh` - Enhanced startup logic
2. `/scripts/stop-bizoholic-full.sh` - Enhanced cleanup logic
3. `/scripts/status-bizoholic.sh` - New status checking script (created)

## Testing Checklist

After implementing these changes:

- [ ] Stop all services: `./scripts/stop-bizoholic-full.sh`
- [ ] Verify port 3001 is free: `lsof -i :3001`
- [ ] Start services: `./scripts/start-bizoholic-full.sh`
- [ ] Wait full 2-3 minutes
- [ ] Check status: `./scripts/status-bizoholic.sh`
- [ ] Access frontend: http://localhost:3001
- [ ] Test auth login
- [ ] Verify all services healthy

---

**Last Updated**: 2025-12-02
**Status**: ✅ Implemented and ready for testing

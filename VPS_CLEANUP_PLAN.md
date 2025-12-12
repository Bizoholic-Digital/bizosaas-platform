# VPS Storage Cleanup Plan - CRITICAL UPDATE
## URGENT: 80GB/100GB Used (80% - Critical Threshold)

**Date**: 2025-12-11  
**Status**: 🔴 **CRITICAL** - Immediate action required  
**Current Usage**: 80GB / 100GB (80%)  
**Available**: 20GB  
**Threshold**: 80% (EXCEEDED)

---

## ⚠️ CRITICAL SITUATION

**VPS Storage**: 80GB/100GB (80% used)  
**Risk Level**: HIGH - System may become unstable  
**Action Required**: IMMEDIATE cleanup needed

---

## IMMEDIATE CLEANUP PLAN (Target: Free 30-40GB)

### Phase 1: Docker Cleanup (IMMEDIATE - ~15-20GB)

**Priority**: 🔴 **CRITICAL** - Execute NOW

```bash
# SSH to VPS first
# ssh user@vps-ip

# 1. Remove all stopped containers
docker container prune -f

# 2. Remove unused images
docker image prune -a -f

# 3. Remove unused volumes
docker volume prune -f

# 4. Remove build cache
docker builder prune -a -f

# 5. Complete system cleanup
docker system prune -a --volumes -f

# Expected savings: 15-20GB
```

**Verification**:
```bash
docker system df
df -h
```

---

### Phase 2: Log Files Cleanup (IMMEDIATE - ~2-5GB)

**Priority**: 🔴 **CRITICAL**

```bash
# Clean Docker container logs
docker ps -aq | xargs -I {} sh -c 'truncate -s 0 $(docker inspect --format="{{.LogPath}}" {} 2>/dev/null)' 2>/dev/null

# Clean application logs
find /var/log -name "*.log" -type f -mtime +7 -delete
find /var/log -name "*.gz" -type f -delete

# Clean journal logs
journalctl --vacuum-time=7d
journalctl --vacuum-size=500M

# Expected savings: 2-5GB
```

---

### Phase 3: Package Manager Cleanup (IMMEDIATE - ~1-2GB)

**Priority**: 🔴 **CRITICAL**

```bash
# Clean apt cache
apt-get clean
apt-get autoclean
apt-get autoremove -y

# Clean npm cache
npm cache clean --force

# Clean pip cache
pip cache purge

# Expected savings: 1-2GB
```

---

### Phase 4: Temporary Files (IMMEDIATE - ~1-2GB)

**Priority**: 🔴 **CRITICAL**

```bash
# Clean /tmp
rm -rf /tmp/*

# Clean /var/tmp
rm -rf /var/tmp/*

# Clean user cache
rm -rf ~/.cache/*

# Expected savings: 1-2GB
```

---

### Phase 5: Old Kernels (IMMEDIATE - ~1-2GB)

**Priority**: 🟡 **HIGH**

```bash
# List installed kernels
dpkg --list | grep linux-image

# Remove old kernels (keep current + 1)
apt-get autoremove --purge -y

# Expected savings: 1-2GB
```

---

## EMERGENCY CLEANUP SCRIPT

**Create and run immediately**:

```bash
#!/bin/bash
# EMERGENCY VPS Cleanup Script
# Target: Free 30-40GB immediately

set -e

echo "========================================="
echo "EMERGENCY VPS CLEANUP - CRITICAL"
echo "Current usage: 80GB/100GB (80%)"
echo "========================================="
echo ""

# Show current usage
echo "Before cleanup:"
df -h / | grep -E 'Filesystem|/'
echo ""

# Phase 1: Docker cleanup
echo "=== Phase 1: Docker Cleanup ==="
docker system prune -a --volumes -f
echo "✅ Docker cleanup complete"
echo ""

# Phase 2: Log files
echo "=== Phase 2: Log Files Cleanup ==="
docker ps -aq | xargs -I {} sh -c 'truncate -s 0 $(docker inspect --format="{{.LogPath}}" {} 2>/dev/null)' 2>/dev/null || true
find /var/log -name "*.log" -type f -mtime +7 -delete 2>/dev/null || true
find /var/log -name "*.gz" -type f -delete 2>/dev/null || true
journalctl --vacuum-time=7d 2>/dev/null || true
journalctl --vacuum-size=500M 2>/dev/null || true
echo "✅ Log cleanup complete"
echo ""

# Phase 3: Package managers
echo "=== Phase 3: Package Manager Cleanup ==="
apt-get clean 2>/dev/null || true
apt-get autoclean 2>/dev/null || true
apt-get autoremove -y 2>/dev/null || true
npm cache clean --force 2>/dev/null || true
pip cache purge 2>/dev/null || true
echo "✅ Package cleanup complete"
echo ""

# Phase 4: Temporary files
echo "=== Phase 4: Temporary Files ==="
rm -rf /tmp/* 2>/dev/null || true
rm -rf /var/tmp/* 2>/dev/null || true
rm -rf ~/.cache/* 2>/dev/null || true
echo "✅ Temp files cleanup complete"
echo ""

# Show final usage
echo "========================================="
echo "After cleanup:"
df -h / | grep -E 'Filesystem|/'
echo ""
docker system df
echo ""
echo "========================================="
```

**Save as**: `/root/emergency-cleanup.sh`

**Execute**:
```bash
chmod +x /root/emergency-cleanup.sh
/root/emergency-cleanup.sh
```

**Expected Result**: 50-60GB used (50-60%)

---

## SECONDARY CLEANUP (If still >70%)

### Phase 6: Application Data Review

**Check large directories**:
```bash
du -sh /var/lib/docker/* | sort -hr | head -20
du -sh /home/* | sort -hr | head -20
du -sh /opt/* | sort -hr | head -20
```

**Identify and remove**:
- Old application backups
- Unused application data
- Old deployment artifacts

---

### Phase 7: Database Cleanup

**PostgreSQL**:
```bash
# Clean old WAL files
sudo -u postgres psql -c "SELECT pg_switch_wal();"
sudo -u postgres psql -c "CHECKPOINT;"

# Vacuum databases
sudo -u postgres vacuumdb --all --full
```

**Expected savings**: 2-5GB

---

### Phase 8: Nginx/Apache Logs

```bash
# Clean web server logs
find /var/log/nginx -name "*.log" -type f -mtime +7 -delete
find /var/log/nginx -name "*.gz" -type f -delete
find /var/log/apache2 -name "*.log" -type f -mtime +7 -delete
find /var/log/apache2 -name "*.gz" -type f -delete
```

**Expected savings**: 1-2GB

---

## MONITORING & PREVENTION

### Set Up Disk Usage Alerts

**Create monitoring script** (`/root/monitor-disk.sh`):
```bash
#!/bin/bash
# Alert if disk usage > 75%

THRESHOLD=75
USAGE=$(df / | grep / | awk '{ print $5}' | sed 's/%//g')

if [ $USAGE -gt $THRESHOLD ]; then
    echo "CRITICAL: Disk usage is ${USAGE}%"
    echo "Running emergency cleanup..."
    /root/emergency-cleanup.sh
    
    # Send alert (configure email/webhook)
    # curl -X POST webhook-url -d "Disk usage: ${USAGE}%"
fi
```

**Add to crontab**:
```bash
# Run every hour
0 * * * * /root/monitor-disk.sh
```

---

### Docker Log Rotation

**Create** `/etc/docker/daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

**Restart Docker**:
```bash
systemctl restart docker
```

---

### Automatic Cleanup Cron

**Add to crontab**:
```bash
# Daily cleanup at 2 AM
0 2 * * * docker system prune -f
0 2 * * * journalctl --vacuum-time=7d
0 2 * * * find /var/log -name "*.log" -type f -mtime +7 -delete
```

---

## EXECUTION PRIORITY

### 🔴 IMMEDIATE (Execute NOW)
1. ✅ SSH to VPS
2. ✅ Run emergency cleanup script
3. ✅ Verify disk usage < 70%
4. ✅ Set up monitoring

**Timeline**: 30 minutes  
**Expected Result**: 50-60GB used (50-60%)

### 🟡 HIGH (Within 24 hours)
1. ⏳ Set up Docker log rotation
2. ⏳ Set up automatic cleanup cron
3. ⏳ Review large directories
4. ⏳ Clean database if needed

**Timeline**: 2 hours  
**Expected Result**: 45-55GB used (45-55%)

### 🟢 MEDIUM (Within 1 week)
1. ⏳ Implement disk usage alerts
2. ⏳ Review application data retention
3. ⏳ Set up log aggregation
4. ⏳ Plan for storage expansion if needed

---

## SUCCESS CRITERIA

- [ ] Disk usage < 70% (CRITICAL)
- [ ] Disk usage < 60% (TARGET)
- [ ] Monitoring alerts configured
- [ ] Automatic cleanup scheduled
- [ ] Log rotation enabled
- [ ] No service disruption

---

## RISK ASSESSMENT

| Current Status | Risk Level | Action Required |
|----------------|------------|-----------------|
| 80GB/100GB (80%) | 🔴 CRITICAL | IMMEDIATE cleanup |
| 70-79GB (70-79%) | 🟡 HIGH | Cleanup within 24h |
| 60-69GB (60-69%) | 🟢 MEDIUM | Monitor closely |
| <60GB (<60%) | ✅ HEALTHY | Normal monitoring |

---

## BACKUP PLAN

**If cleanup doesn't free enough space**:

1. **Identify largest consumers**:
   ```bash
   du -sh /* | sort -hr | head -20
   ```

2. **Consider**:
   - Moving logs to external storage
   - Archiving old data
   - Upgrading VPS storage
   - Migrating services to separate servers

3. **Emergency measures**:
   - Stop non-critical services
   - Remove old Docker images completely
   - Clear all caches aggressively

---

## NEXT STEPS

1. 🔴 **IMMEDIATE**: Run emergency cleanup script on VPS
2. 🟡 **HIGH**: Set up monitoring and automation
3. 🟢 **MEDIUM**: Review and optimize long-term storage strategy

**After cleanup, return to**: Admin Dashboard & Authentik Integration

---

## STATUS TRACKING

- [ ] Emergency cleanup executed
- [ ] Disk usage verified < 70%
- [ ] Monitoring configured
- [ ] Automation set up
- [ ] Documentation updated
- [ ] Ready to proceed with admin dashboard

**Current Priority**: 🔴 **VPS CLEANUP FIRST**, then admin dashboard

# WSL Quick Reference Guide

## Common Docker Commands

### View System Status
```bash
# Check Docker disk usage
docker system df

# List all containers (running and stopped)
docker ps -a

# List all images
docker images

# List all volumes
docker volume ls

# Check system resources
df -h /
free -h
```

### Cleanup Commands

#### Quick Cleanup (Safe)
```bash
# Remove stopped containers
docker container prune -f

# Remove unused images
docker image prune -f

# Remove unused volumes
docker volume prune -f

# Remove build cache
docker builder prune -f
```

#### Deep Cleanup (Removes Everything Unused)
```bash
# Remove all unused containers, images, volumes, and networks
docker system prune -a --volumes -f
```

#### Use the Automated Script
```bash
# Run the interactive cleanup script
~/.agent/scripts/wsl_cleanup.sh
```

---

## Port Management

### Check Listening Ports
```bash
# List all listening ports
ss -tulpn | grep LISTEN

# Count listening ports
ss -tulpn | grep LISTEN | wc -l

# Check specific port
ss -tulpn | grep :8080
```

### Find Process Using a Port
```bash
# Find what's using port 8080
sudo lsof -i :8080

# Or using ss
ss -tulpn | grep :8080
```

---

## Process Management

### Check for Zombie Processes
```bash
# List zombie processes
ps aux | awk '$8 ~ /Z/ {print}'

# Count zombie processes
ps aux | awk '$8 ~ /Z/ {print}' | wc -l
```

### View Resource Usage
```bash
# Real-time process monitoring
top

# One-time snapshot
top -bn1 | head -20

# Docker container stats
docker stats
```

---

## WSL-Specific Commands

### Restart WSL (from Windows PowerShell)
```powershell
wsl --shutdown
wsl
```

### Optimize WSL Disk (from Windows PowerShell as Admin)
```powershell
wsl --shutdown
Optimize-VHD -Path "$env:LOCALAPPDATA\Packages\CanonicalGroupLimited.Ubuntu*\LocalState\ext4.vhdx" -Mode Full
```

### WSL Configuration (~/.wslconfig)
```ini
[wsl2]
memory=6GB
processors=4
swap=2GB
localhostForwarding=true
```

---

## Docker Compose Commands

### Start Services
```bash
# Start all services in background
docker-compose up -d

# Start specific service
docker-compose up -d service_name

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f service_name
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop but keep containers
docker-compose stop
```

### Rebuild Services
```bash
# Rebuild and restart
docker-compose up -d --build

# Force recreate containers
docker-compose up -d --force-recreate
```

---

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker logs container_name

# Check last 100 lines
docker logs --tail 100 container_name

# Follow logs in real-time
docker logs -f container_name
```

### High Disk Usage
```bash
# Check what's using space
docker system df -v

# Clean everything
docker system prune -a --volumes -f
```

### High Memory Usage
```bash
# Check memory usage
free -h

# Check Docker container memory
docker stats --no-stream

# Restart Docker daemon
sudo systemctl restart docker
```

### Network Issues
```bash
# List networks
docker network ls

# Remove unused networks
docker network prune -f

# Inspect network
docker network inspect network_name
```

---

## Maintenance Schedule

### Daily
- Check running containers: `docker ps`
- Monitor disk space: `df -h /`

### Weekly
- Review logs: `docker-compose logs --tail 100`
- Check resource usage: `docker stats --no-stream`

### Monthly
- Run cleanup script: `~/.agent/scripts/wsl_cleanup.sh`
- Review and remove unused images: `docker images`
- Check for updates: `docker-compose pull`

### Quarterly
- Optimize WSL disk (Windows PowerShell)
- Review and update .wslconfig
- Backup important volumes

---

## Useful Aliases

Add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# Docker aliases
alias dps='docker ps'
alias dpsa='docker ps -a'
alias di='docker images'
alias ddf='docker system df'
alias dclean='docker system prune -a -f'
alias dstop='docker stop $(docker ps -q)'

# Docker Compose aliases
alias dc='docker-compose'
alias dcup='docker-compose up -d'
alias dcdown='docker-compose down'
alias dclogs='docker-compose logs -f'
alias dcrestart='docker-compose restart'

# System aliases
alias ports='ss -tulpn | grep LISTEN'
alias meminfo='free -h'
alias diskinfo='df -h /'
```

---

## Emergency Commands

### Kill All Containers
```bash
docker kill $(docker ps -q)
```

### Remove All Containers
```bash
docker rm -f $(docker ps -aq)
```

### Remove All Images
```bash
docker rmi -f $(docker images -q)
```

### Complete Docker Reset
```bash
docker system prune -a --volumes -f
docker network prune -f
```

### Restart Docker Service
```bash
sudo systemctl restart docker
```

---

## Important Notes

⚠️ **Before Running Cleanup Commands:**
- Ensure no important containers are running
- Backup any important data
- Check which volumes will be removed

✅ **Safe to Remove:**
- Stopped containers
- Unused images
- Dangling volumes
- Build cache

❌ **Do NOT Remove:**
- Running containers
- Named volumes with data
- Images currently in use

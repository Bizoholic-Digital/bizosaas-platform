# BizOSaaS Virtual Environment Guide

## Overview

This guide covers the new virtual environment setup for BizOSaaS services, which provides isolated Python environments for each service to prevent dependency conflicts and improve development workflow.

## Architecture

### Before (Global Dependencies)
- All Python packages installed globally
- Dependency conflicts between services
- Difficult to manage different package versions
- No isolation between development and production

### After (Virtual Environments)
- Each service has its own isolated Python environment
- Service-specific dependencies in `services/.venvs/`
- Clean dependency management with service-specific `requirements.txt`
- Professional development workflow

## Directory Structure

```
bizosaas/
├── services/
│   ├── .venvs/                    # Virtual environments directory
│   │   ├── ai-agents/             # AI Agents service virtual env
│   │   ├── api-gateway/           # API Gateway service virtual env
│   │   ├── business-directory/    # Business Directory virtual env
│   │   ├── wagtail-cms/          # Wagtail CMS virtual env
│   │   └── ...                   # Other service virtual envs
│   ├── ai-agents/
│   │   ├── requirements.txt      # Service-specific dependencies
│   │   ├── requirements-frozen.txt # Frozen dependencies for reproducibility
│   │   └── main.py
│   └── ...
├── scripts/
│   ├── setup-virtual-environments.sh
│   ├── start-services-with-venv.sh
│   ├── activate-venv.sh
│   ├── manage-dependencies.sh
│   └── ...
└── logs/                         # Service logs and PID files
    ├── ai-agents.log
    ├── ai-agents.pid
    └── ...
```

## Management Scripts

### 1. Initial Setup
```bash
# Create virtual environments for all services
bash scripts/setup-virtual-environments.sh

# Or run complete migration (includes stopping services)
bash scripts/venv-migration.sh
```

### 2. Service Management
```bash
# Start all services with virtual environments
bash scripts/start-services-with-venv.sh

# Start individual service
bash scripts/start-service.sh ai-agents
bash scripts/start-service.sh api-gateway 8080

# Stop all services
bash scripts/stop-all-services.sh

# Check service status
bash scripts/check-service-status.sh
```

### 3. Development Workflow
```bash
# Activate virtual environment for development
source scripts/activate-venv.sh ai-agents

# Now you can work with the service
cd services/ai-agents
python main.py

# When done, deactivate
deactivate
```

### 4. Dependency Management
```bash
# Update all service dependencies
bash scripts/manage-dependencies.sh update

# Update specific service
bash scripts/manage-dependencies.sh update ai-agents

# Check for outdated packages
bash scripts/manage-dependencies.sh check

# Install package to specific service
bash scripts/manage-dependencies.sh install ai-agents numpy

# Generate dependency report
bash scripts/manage-dependencies.sh report
```

## Service Configuration

### Supported Services

| Service | Port | Virtual Env | Main File |
|---------|------|-------------|-----------|
| AI Agents | 8001 | ✅ | main.py |
| API Gateway | 8080 | ✅ | main.py |
| Business Directory | 8003 | ✅ | main.py |
| Auth Service V2 | 8004 | ✅ | main.py |
| CRM Service V2 | 8005 | ✅ | main.py |
| Wagtail CMS | 8006 | ✅ | manage.py |
| Marketing Automation | 8007 | ✅ | main.py |

### Service Types

**FastAPI Services**: Most services use FastAPI and are started with uvicorn
```bash
# Automatically detected and started with:
uvicorn main:app --host 0.0.0.0 --port <port>
```

**Django Services** (Wagtail CMS):
```bash
# Started with Django management command:
python manage.py runserver 0.0.0.0:<port>
```

**Custom Services**: Services with specific startup requirements
```bash
# Started with direct python execution:
python main.py
```

## Development Best Practices

### 1. Working on a Service
```bash
# Always activate the service's virtual environment
source scripts/activate-venv.sh ai-agents

# Install new dependencies
pip install new-package
echo "new-package>=1.0.0" >> requirements.txt

# Or use the management script
bash scripts/manage-dependencies.sh install ai-agents new-package

# Test your changes
python main.py

# When done
deactivate
```

### 2. Adding New Dependencies
```bash
# Method 1: Using management script (recommended)
bash scripts/manage-dependencies.sh install service-name package-name

# Method 2: Manual installation
source scripts/activate-venv.sh service-name
pip install package-name
echo "package-name>=version" >> requirements.txt
deactivate
```

### 3. Debugging Services
```bash
# Check if service is running
bash scripts/check-service-status.sh

# View service logs
tail -f logs/ai-agents.log

# Start service in debug mode
source scripts/activate-venv.sh ai-agents
cd services/ai-agents
python main.py  # Direct execution for debugging
```

### 4. Production Deployment
```bash
# Generate frozen requirements for reproducibility
bash scripts/manage-dependencies.sh update
# This creates requirements-frozen.txt for each service

# Use frozen requirements in production
pip install -r requirements-frozen.txt
```

## Troubleshooting

### Common Issues

**Service won't start**:
1. Check virtual environment exists: `ls services/.venvs/`
2. Check dependencies installed: `source scripts/activate-venv.sh service-name && pip list`
3. Check logs: `tail logs/service-name.log`

**Port already in use**:
```bash
# Find process using port
lsof -i :8001

# Kill process if needed
kill -9 <PID>
```

**Virtual environment missing**:
```bash
# Recreate virtual environments
bash scripts/setup-virtual-environments.sh
```

**Dependencies missing**:
```bash
# Reinstall dependencies
bash scripts/manage-dependencies.sh update service-name
```

### Log Files

All service logs are stored in `/home/alagiri/projects/bizoholic/bizosaas/logs/`:
- `service-name.log` - Service output and errors
- `service-name.pid` - Process ID for management

### Environment Variables

Each service can use environment-specific variables. Create `.env` files in service directories:
```bash
# services/ai-agents/.env
OPENAI_API_KEY=your-key
DEBUG=true
```

## Migration from Global Packages

If you're migrating from the old system:

1. **Backup current state** - Services will be stopped during migration
2. **Run migration**: `bash scripts/venv-migration.sh`
3. **Verify services**: `bash scripts/check-service-status.sh`
4. **Test endpoints**: Check service health endpoints

## Performance Benefits

- **Faster startup**: Services only load required dependencies
- **Smaller memory footprint**: No unused packages loaded
- **Cleaner development**: No conflicts between service dependencies
- **Better debugging**: Clear separation of service environments
- **Production parity**: Same environment structure in development and production

## Next Steps

After setting up virtual environments:

1. **Test all services**: Ensure endpoints respond correctly
2. **Update CI/CD**: Modify deployment scripts to use virtual environments
3. **Document custom packages**: Add any project-specific packages to requirements.txt
4. **Monitor performance**: Compare startup times and memory usage

## Support

For issues with the virtual environment setup:

1. Check service status: `bash scripts/check-service-status.sh`
2. Review logs in `logs/` directory
3. Recreate environments: `bash scripts/setup-virtual-environments.sh`
4. Contact development team with specific error messages
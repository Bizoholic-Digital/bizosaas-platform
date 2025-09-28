# Wagtail CMS Port Standardization

## Current Issue
Wagtail is currently running on TWO ports:
- Port 8006: Docker/Gunicorn (production)
- Port 8007: Development server (local)

## Recommended Solution

### Production Environment
- **Port 3010**: Wagtail CMS Admin (accessible via unified dashboard authentication)
- **Access**: `http://localhost:3010/admin/` or `https://admin.bizosaas.com/`
- **Security**: Requires authentication, localhost binding for admin access

### Development Environment  
- **Port 8007**: Local development server (localhost only)
- **Access**: `http://localhost:8007/admin/`
- **Security**: Localhost only, development purposes

## Implementation Steps

### Step 1: Update Docker Configuration
```yaml
# docker-compose.yml
wagtail-cms:
  build: ./services/wagtail-cms
  ports:
    - "127.0.0.1:3010:8000"  # Bind to localhost only
  environment:
    - WAGTAIL_ADMIN_PORT=3010
```

### Step 2: Update Wagtail Settings
```python
# wagtail_cms/settings/base.py
WAGTAILADMIN_BASE_URL = 'http://localhost:3010'

# For production with domain
WAGTAILADMIN_BASE_URL = 'https://admin.bizosaas.com'
```

### Step 3: Update Static Website Links
Replace references to port 8006/8007 with the unified dashboard:
```html
<!-- Old -->
<a href="http://localhost:8006/admin/">Admin</a>

<!-- New -->  
<a href="http://localhost:3005/admin/cms/">CMS Admin</a>
```

### Step 4: Unified Dashboard Integration
The Wagtail admin should be accessible through the unified dashboard at:
- `http://localhost:3005/admin/cms/` (proxied to port 3010)

## Security Benefits

1. **Single entry point** through unified dashboard
2. **Authentication required** before accessing Wagtail admin
3. **No direct external access** to Wagtail admin interface
4. **Consistent with port allocation strategy**

## Configuration Changes

### Environment Variables
```bash
# .env
WAGTAIL_ADMIN_PORT=3010
WAGTAIL_ADMIN_HOST=127.0.0.1  # localhost only
```

### Traefik Labels (if using Traefik)
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.wagtail.rule=Host(`admin.bizosaas.com`)"
  - "traefik.http.routers.wagtail.tls=true"
  - "traefik.http.routers.wagtail.middlewares=auth@file"
```
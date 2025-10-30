# GitHub Packages Setup for BizOSaaS Shared Libraries

**Purpose:** Publish and consume @bizosaas shared packages via GitHub Packages (npm registry)
**Date:** October 30, 2025

---

## Overview

GitHub Packages provides a free npm registry for private packages. We'll publish our 6 shared packages here and consume them in all microservices.

---

## Step 1: Configure Package Metadata

Each package needs proper npm configuration for publishing.

### Required Fields in package.json

```json
{
  "name": "@bizosaas/package-name",
  "version": "1.0.0",
  "publishConfig": {
    "registry": "https://npm.pkg.github.com",
    "@bizosaas:registry": "https://npm.pkg.github.com"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/bizoholic-digital/bizosaas-platform.git"
  }
}
```

---

## Step 2: Create .npmrc for Publishing

Create `.npmrc` in each package directory:

```
@bizosaas:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

---

## Step 3: GitHub Token Setup

### Create Personal Access Token (PAT)

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Required scopes:
   - `write:packages` - Publish packages
   - `read:packages` - Download packages
   - `repo` - Access private repository

### Set Environment Variable

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

Or add to `~/.bashrc` / `~/.zshrc`:

```bash
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

---

## Step 4: Publish Packages

### Manual Publishing

```bash
# Build and publish each package
cd packages/auth
npm run build
npm publish

cd ../ui-components
npm run build
npm publish

# ... repeat for all 6 packages
```

### Automated Publishing Script

Create `scripts/publish-packages.sh`:

```bash
#!/bin/bash

PACKAGES=(
  "auth"
  "ui-components"
  "api-client"
  "hooks"
  "utils"
  "animated-components"
)

for package in "${PACKAGES[@]}"; do
  echo "Publishing @bizosaas/$package..."
  cd "packages/$package"
  npm run build
  npm publish
  cd ../..
  echo "✅ Published @bizosaas/$package"
done

echo "🎉 All packages published successfully!"
```

---

## Step 5: Configure Services to Use Published Packages

### Update package.json in Each Service

**Before (local workspaces):**
```json
{
  "dependencies": {
    "@bizosaas/auth": "file:../../../../../packages/auth"
  }
}
```

**After (GitHub Packages):**
```json
{
  "dependencies": {
    "@bizosaas/auth": "^1.0.0"
  }
}
```

### Create .npmrc in Service Directory

Create `bizosaas/misc/services/bizoholic-frontend/.npmrc`:

```
@bizosaas:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

---

## Step 6: Docker Build Configuration

### Add .npmrc to Docker Build

**Option 1: Build Args (Recommended)**

```dockerfile
FROM node:18-alpine AS deps
WORKDIR /app

# Accept GitHub token as build arg
ARG GITHUB_TOKEN

# Create .npmrc with token
RUN echo "@bizosaas:registry=https://npm.pkg.github.com" > .npmrc && \
    echo "//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}" >> .npmrc

COPY package*.json ./
RUN npm ci --only=production

# Remove .npmrc to avoid leaking token
RUN rm -f .npmrc
```

**Build Command:**
```bash
docker build --build-arg GITHUB_TOKEN=$GITHUB_TOKEN -t service:latest .
```

**Option 2: Docker Secret (More Secure)**

```dockerfile
FROM node:18-alpine AS deps
WORKDIR /app

# Mount secret containing GitHub token
RUN --mount=type=secret,id=github_token \
    echo "@bizosaas:registry=https://npm.pkg.github.com" > .npmrc && \
    echo "//npm.pkg.github.com/:_authToken=$(cat /run/secrets/github_token)" >> .npmrc && \
    npm ci --only=production && \
    rm -f .npmrc
```

**Build Command:**
```bash
echo $GITHUB_TOKEN | docker build --secret id=github_token,src=- -t service:latest .
```

---

## Step 7: GitHub Actions CI/CD

### Workflow for Publishing Packages

Create `.github/workflows/publish-packages.yml`:

```yaml
name: Publish Shared Packages

on:
  push:
    branches: [main]
    paths:
      - 'packages/**'

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          registry-url: 'https://npm.pkg.github.com'
          scope: '@bizosaas'

      - name: Install dependencies
        run: npm ci
        working-directory: packages

      - name: Build and publish packages
        run: |
          for dir in packages/*; do
            if [ -d "$dir" ]; then
              echo "Publishing $dir..."
              cd "$dir"
              npm run build
              npm publish
              cd ../..
            fi
          done
        env:
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Workflow for Building Services

Create `.github/workflows/build-bizoholic.yml`:

```yaml
name: Build Bizoholic Frontend

on:
  push:
    branches: [main]
    paths:
      - 'bizosaas/misc/services/bizoholic-frontend/**'

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v3

      - name: Login to GHCR
        uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: bizosaas/misc/services/bizoholic-frontend
          push: true
          tags: ghcr.io/bizoholic-digital/bizosaas-bizoholic-frontend:latest
          build-args: |
            GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}
```

---

## Step 8: Local Development Workflow

### Development with npm Workspaces

When developing locally, use npm workspaces for instant feedback:

```bash
# Install all workspace packages
cd /home/alagiri/projects/bizosaas-platform
npm install

# Make changes to shared package
cd packages/auth
# ... edit files ...
npm run build

# Test in service immediately
cd ../../bizosaas/misc/services/bizoholic-frontend
npm run dev
```

### Production Testing with Published Packages

To test the production workflow locally:

```bash
# Publish to GitHub Packages
cd packages/auth
npm version patch
npm run build
npm publish

# Update service to use published version
cd ../../bizosaas/misc/services/bizoholic-frontend
npm update @bizosaas/auth

# Build Docker image
docker build --build-arg GITHUB_TOKEN=$GITHUB_TOKEN -t test:latest .
```

---

## Step 9: Version Management

### Semantic Versioning Strategy

- **Major (1.0.0 → 2.0.0):** Breaking changes
  - Changed function signatures
  - Removed exports
  - Changed behavior

- **Minor (1.0.0 → 1.1.0):** New features
  - New components
  - New hooks
  - New utilities
  - Backward compatible

- **Patch (1.0.0 → 1.0.1):** Bug fixes
  - Bug fixes
  - Documentation updates
  - Performance improvements

### Updating Versions

```bash
# Patch version (bug fix)
npm version patch

# Minor version (new feature)
npm version minor

# Major version (breaking change)
npm version major

# Then publish
npm run build
npm publish
```

---

## Step 10: Troubleshooting

### Error: Authentication Required

```
npm ERR! 401 Unauthorized
```

**Solution:** Check GitHub token has correct permissions:
- `write:packages` for publishing
- `read:packages` for installing
- Token not expired

### Error: Package Not Found

```
npm ERR! 404 Not Found - GET https://npm.pkg.github.com/@bizosaas/auth
```

**Solution:**
1. Verify package is published: Check GitHub → Packages
2. Verify .npmrc is configured correctly
3. Verify token has `read:packages` permission

### Error: Version Already Exists

```
npm ERR! 403 Forbidden - PUT https://npm.pkg.github.com/@bizosaas/auth
```

**Solution:** Bump version before publishing:
```bash
npm version patch
npm publish
```

---

## Summary

### Configuration Checklist

- [ ] Each package has `publishConfig` in package.json
- [ ] Each package has `.npmrc` file
- [ ] GitHub PAT created with correct permissions
- [ ] `GITHUB_TOKEN` environment variable set
- [ ] All 6 packages built and published
- [ ] Service package.json updated to use published versions
- [ ] Service `.npmrc` configured
- [ ] Dockerfile updated with token authentication
- [ ] GitHub Actions workflows created
- [ ] Local development workflow documented

### Published Packages

1. `@bizosaas/auth@1.0.0` - Authentication
2. `@bizosaas/ui-components@1.0.0` - UI components
3. `@bizosaas/api-client@1.0.0` - API client
4. `@bizosaas/hooks@1.0.0` - React hooks
5. `@bizosaas/utils@1.0.0` - Utilities
6. `@bizosaas/animated-components@1.0.0` - Animations

### Next Steps

1. Run `scripts/publish-packages.sh` to publish all packages
2. Update Bizoholic frontend to use published packages
3. Create proper microservice Dockerfile
4. Test Docker build with GitHub Packages
5. Deploy to Dokploy
6. Repeat for remaining 6 frontends

---

**Previous:** [MICROSERVICES_DDD_ARCHITECTURE.md](./MICROSERVICES_DDD_ARCHITECTURE.md)
**Next:** Implementation and deployment

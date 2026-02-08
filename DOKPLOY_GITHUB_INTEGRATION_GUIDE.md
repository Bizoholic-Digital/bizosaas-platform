# Dokploy GitHub Integration Guide

## Current Status
- **Dokploy Version**: Running on KVM2 (194.238.16.237)
- **Dokploy URL**: https://dk.bizoholic.com
- **Issue**: GitHub Provider not configured, causing all deployments to fail with "Github Provider not found"

## Problem Analysis

### Root Cause
Dokploy requires a GitHub provider to be configured before it can clone repositories and deploy compose files. The API endpoints for creating GitHub providers are not exposed in the current Dokploy version, requiring manual UI configuration.

### Current Deployment Failures
All three compose deployments are failing:
- **Infrastructure** (Compose ID: `UFbl0OAttxVLthzQ3fSn2`)
- **Backend** (Compose ID: `dg2AbBEXS2BMRcUofPSdo`)
- **Frontend** (Compose ID: `E9LNOMr4-d5PBk5eh0-Ef`)

Error: `❌ Github Provider not found`

## Solution: Manual GitHub Provider Configuration

### Step 1: Access Dokploy UI
1. Navigate to: https://dk.bizoholic.com
2. Login with your Dokploy credentials

### Step 2: Configure GitHub Provider
1. Go to **Settings** → **Git Providers**
2. Click **Add GitHub Provider**
3. Choose one of the following methods:

#### Option A: Personal Access Token (Recommended for Testing)
```
Provider Name: bizosaas-github
GitHub Token: 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
GitHub Username: Bizoholic-Digital
```

**Note**: This token needs the following scopes:
- `repo` (Full control of private repositories)
- `read:packages`
- `write:packages`

#### Option B: GitHub App (Recommended for Production)
1. Create a GitHub App at: https://github.com/organizations/Bizoholic-Digital/settings/apps
2. Configure the app with:
   - **Repository permissions**:
     - Contents: Read & write
     - Metadata: Read-only
     - Pull requests: Read & write
   - **Subscribe to events**: Push, Pull request
3. Install the app to the `bizosaas-platform` repository
4. In Dokploy, enter:
   - App ID
   - Installation ID
   - Private Key (PEM format)

### Step 3: Verify GitHub Connection
After adding the provider:
1. Go to any compose deployment (Infrastructure, Backend, or Frontend)
2. Check if the GitHub repository is now accessible
3. Trigger a manual deployment

### Step 4: Re-trigger Deployments
Once GitHub provider is configured, re-run the deployment script:

```bash
cd /home/alagiri/projects/bizosaas-platform
./scripts/deploy-to-dokploy-api.sh
```

Or manually trigger each deployment in Dokploy UI:
1. Infrastructure: Project `bizosaas-infrastructure-staging` → Compose `infrastructure-staging`
2. Backend: Project `bizosaas-backend-staging` → Compose `backend-services-staging`
3. Frontend: Project `bizosaas-frontend-staging` → Compose `frontend-apps-staging`

## Alternative: Use Dokploy CLI (If Available)

If Dokploy CLI is installed on the VPS:

```bash
ssh root@194.238.16.237
dokploy github create \
  --name "bizosaas-github" \
  --token "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" \
  --username "Bizoholic-Digital"
```

**Note**: The `dokploy` CLI is not currently installed on the VPS.

## GitHub Actions CI/CD Integration

### Current Workflows
The repository has the following GitHub Actions workflows:
- `deploy-admin-dashboard.yml`
- `deploy-ai-agents.yml`
- `deploy-brain-gateway.yml`
- `deploy-business-directory.yml`
- `deploy-client-portal.yml`
- `production-readiness-testing.yml`
- `security-scan.yml`

### Issue with Current Workflows
The workflows reference an old Dokploy instance (`dk8.bizoholic.com`) and old compose IDs. They need to be updated.

### Required GitHub Secrets
Ensure these secrets are set in the GitHub repository:
- `GHCR_TOKEN`: GitHub Container Registry token
- `DOKPLOY_API_KEY`: `mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug`
- `NEXTAUTH_SECRET`: NextAuth secret key
- `CLERK_SECRET_KEY`: Clerk secret key

### Update Workflow Files
The workflows need to be updated to use the new Dokploy instance and compose IDs:

**Old Configuration:**
```yaml
curl -X POST "https://dk8.bizoholic.com/api/compose.deploy" \
  -H "x-api-key: ${{ secrets.DOKPLOY_API_KEY }}" \
  -d '{"composeId": "hU2yhYOqv3_ftKGGvcAiv"}'
```

**New Configuration:**
```yaml
curl -X POST "https://dk.bizoholic.com/api/compose.deploy" \
  -H "X-API-Key: ${{ secrets.DOKPLOY_API_KEY }}" \
  -d '{"composeId": "E9LNOMr4-d5PBk5eh0-Ef"}'
```

## Compose IDs Reference

### Current Deployments (2026-01-29)
- **Infrastructure**: `UFbl0OAttxVLthzQ3fSn2`
- **Backend Services**: `dg2AbBEXS2BMRcUofPSdo`
- **Frontend Applications**: `E9LNOMr4-d5PBk5eh0-Ef`

### Project IDs
- **Infrastructure**: `imS9ILN82vjqBzSpAs5A_` (Environment: `fh4wZ4r_Hce4cHsl6H-6W`)
- **Backend**: `-aElopMBZMcyOjMU4X2TA` (Environment: `rmEK7-cphJvH3fIjQgQp0`)
- **Frontend**: `PG7s5YVGUMsJKSZvmDore` (Environment: `4DGXVhGjcs8_REfP0Oomc`)

## Troubleshooting

### Check Deployment Logs
```bash
# Get deployment status
curl -s -H "X-API-Key: mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug" \
  "https://dk.bizoholic.com/api/compose.one?composeId=UFbl0OAttxVLthzQ3fSn2" | jq '.deployments[0]'

# View logs on VPS
ssh root@194.238.16.237
cat /etc/dokploy/logs/compose-*/compose-*-2026-01-29*.log
```

### Verify GitHub Token
Test if the GitHub token is valid:
```bash
curl -H "Authorization: token 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" \
  https://api.github.com/user
```

### Check Dokploy API Connectivity
```bash
curl -s -H "X-API-Key: mKgAkCySnrCaAupZYGLiHNNugPRzbsGQZHbcJFMoQSSfdhKUGUPksUuGrWQGWBug" \
  "https://dk.bizoholic.com/api/project.all" | jq '.[].name'
```

## Next Steps

1. **Immediate**: Configure GitHub provider in Dokploy UI
2. **Short-term**: Update GitHub Actions workflows with new compose IDs
3. **Medium-term**: Set up GitHub App for better security
4. **Long-term**: Implement automated deployment verification script

## Support

If issues persist:
1. Check Dokploy logs: `docker logs dokploy.1.i9nojxbwynu0tfpfv6ni98u1z`
2. Verify network connectivity between Dokploy and GitHub
3. Ensure the GitHub token has not expired
4. Contact Dokploy support or check documentation at https://docs.dokploy.com

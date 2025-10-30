# GitHub Token Setup for Package Publishing

**Date:** October 30, 2025
**Required for:** Publishing @bizosaas packages to GitHub Packages

---

## Step 1: Create Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a descriptive name: "BizOSaaS Package Publishing"
4. Set expiration: 90 days (or longer based on your security policy)
5. Select required scopes:
   - ✅ `repo` - Full control of private repositories
   - ✅ `write:packages` - Upload packages to GitHub Package Registry
   - ✅ `read:packages` - Download packages from GitHub Package Registry
   - ✅ `delete:packages` - Delete packages from GitHub Package Registry (optional)

6. Click "Generate token"
7. **COPY THE TOKEN IMMEDIATELY** - You won't be able to see it again!

---

## Step 2: Set Environment Variable

### For Current Session (Temporary)

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### For Permanent Setup (Recommended)

Add to your shell profile:

```bash
# For bash
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.bashrc
source ~/.bashrc

# For zsh
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

---

## Step 3: Verify Token is Set

```bash
echo "Token starts with: ${GITHUB_TOKEN:0:10}..."
```

You should see: `Token starts with: ghp_XXXXXX...`

---

## Step 4: Test Token Permissions

```bash
# Test read access to GitHub Packages
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://npm.pkg.github.com/@bizosaas%2fauth

# Should return 404 (package doesn't exist yet) or package info
```

---

## Security Best Practices

### DO:
- ✅ Store token in environment variable
- ✅ Use token with minimum required scopes
- ✅ Set expiration dates on tokens
- ✅ Rotate tokens regularly
- ✅ Use different tokens for different purposes

### DON'T:
- ❌ Commit token to Git
- ❌ Share token in plain text
- ❌ Use same token for everything
- ❌ Set token without expiration
- ❌ Include token in Docker images

---

## Using Token in Scripts

### Shell Scripts

```bash
#!/bin/bash

if [ -z "$GITHUB_TOKEN" ]; then
  echo "❌ Error: GITHUB_TOKEN not set"
  echo "Please run: export GITHUB_TOKEN='your_token_here'"
  exit 1
fi

# Use token
npm publish
```

### Docker Builds

```dockerfile
# Pass as build arg
ARG GITHUB_TOKEN

# Use in RUN commands
RUN echo "//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}" > .npmrc && \
    npm ci && \
    rm -f .npmrc
```

### GitHub Actions

GitHub Actions automatically provides `GITHUB_TOKEN` secret:

```yaml
- name: Publish packages
  run: npm publish
  env:
    NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Troubleshooting

### Token Not Working

1. Check token hasn't expired
2. Verify correct scopes are selected
3. Ensure token belongs to account with repo access
4. Try regenerating token

### Permission Denied

```
npm ERR! 403 Forbidden
```

- Ensure `write:packages` scope is enabled
- Verify you have admin access to repository
- Check organization package settings

### Token Leaked

If token is accidentally committed or shared:

1. Immediately revoke token at https://github.com/settings/tokens
2. Generate new token
3. Update environment variable
4. Review recent activity for unauthorized access

---

## Next Steps

After setting up the token:

1. Run `/home/alagiri/projects/bizosaas-platform/scripts/publish-all-packages.sh`
2. Packages will be published to GitHub Packages
3. Update services to use published versions
4. Test Docker builds with published packages

---

**Related Docs:**
- [GITHUB_PACKAGES_SETUP.md](./GITHUB_PACKAGES_SETUP.md)
- [MICROSERVICES_DDD_ARCHITECTURE.md](./MICROSERVICES_DDD_ARCHITECTURE.md)

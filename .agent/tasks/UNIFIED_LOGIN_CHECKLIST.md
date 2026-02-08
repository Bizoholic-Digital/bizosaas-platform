# Unified Login Migration - Quick Start Checklist

## ✅ Pre-Migration Checklist

- [ ] Review full plan in `UNIFIED_LOGIN_MIGRATION.md`
- [ ] Backup current login pages
- [ ] Verify both portals are working correctly
- [ ] Create feature branch: `git checkout -b feat/unified-login`

## 🚀 Phase 1: Setup (30 min)

### 1.1 Configure Root TypeScript
```bash
# Edit tsconfig.json at root
```
- [ ] Add path mapping for `@bizosaas/shared-ui`
- [ ] Verify TypeScript resolves imports

### 1.2 Update Portal Configs
```bash
# Edit portals/admin-dashboard/tsconfig.json
# Edit portals/client-portal/tsconfig.json
```
- [ ] Extend root tsconfig
- [ ] Add shared-ui path
- [ ] Test: `npm run type-check` (both portals)

### 1.3 Update Next.js Configs
```bash
# Edit portals/admin-dashboard/next.config.js
# Edit portals/client-portal/next.config.js
```
- [ ] Add `transpilePackages: ['@bizosaas/shared-ui']`
- [ ] Test: `npm run build` (both portals)

## 🎨 Phase 2: Admin Dashboard (1 hour)

### 2.1 Backup Current Login
```bash
cp portals/admin-dashboard/app/login/page.tsx \
   portals/admin-dashboard/app/login/page.tsx.backup
```
- [ ] Backup created

### 2.2 Replace Login Page
- [ ] Update `portals/admin-dashboard/app/login/page.tsx`
- [ ] Import UnifiedLoginForm
- [ ] Configure for SSO mode
- [ ] Test: `npm run dev` - no errors

### 2.3 Test Admin Login
- [ ] Visit `http://localhost:3004/login`
- [ ] SSO button visible
- [ ] Click SSO → redirects to Authentik
- [ ] After auth → redirects to dashboard
- [ ] Protected routes require auth
- [ ] `/api/health` works without auth

## 👥 Phase 3: Client Portal (1 hour)

### 3.1 Create Wrapper Component
```bash
# Create portals/client-portal/app/login/ClientLoginForm.tsx
```
- [ ] Client component created
- [ ] UnifiedLoginForm configured for credentials
- [ ] Test: No TypeScript errors

### 3.2 Update Login Page
- [ ] Backup original: `page.tsx.backup`
- [ ] Update to use ClientLoginForm
- [ ] Test: `npm run dev` - no errors

### 3.3 Test Client Login
- [ ] Visit `http://localhost:3003/login`
- [ ] Email/password form visible
- [ ] Demo credentials shown (dev mode)
- [ ] Login with valid credentials works
- [ ] Login with invalid credentials shows error
- [ ] Protected routes require auth

## 🧹 Phase 4: Cleanup (30 min)

### 4.1 Archive Old Components
```bash
mkdir -p portals/client-portal/components/auth/_archive
mv portals/client-portal/components/auth/LoginForm.tsx \
   portals/client-portal/components/auth/_archive/
mv portals/client-portal/components/auth/login-form.tsx \
   portals/client-portal/components/auth/_archive/
```
- [ ] Old components archived
- [ ] No broken imports
- [ ] Test: `npm run build` (both portals)

### 4.2 Update Documentation
- [ ] Update root README.md
- [ ] Update admin dashboard README
- [ ] Update client portal README
- [ ] Document shared component usage

## 🚀 Phase 5: Deployment (1 hour)

### 5.1 Commit and Push
```bash
git add .
git commit -m "feat: migrate to unified login component

- Configure monorepo for shared-ui package
- Migrate admin dashboard to UnifiedLoginForm (SSO)
- Migrate client portal to UnifiedLoginForm (credentials)
- Archive old login components
- Update documentation"

git push origin feat/unified-login
```
- [ ] Changes committed
- [ ] Pushed to GitHub

### 5.2 Deploy to Staging
- [ ] Merge to `staging` branch
- [ ] Dokploy auto-deploys
- [ ] Wait for build completion
- [ ] Test on staging URLs

### 5.3 Staging Verification
- [ ] Admin: `https://admin.bizoholic.net/login`
- [ ] Client: `https://portal.bizoholic.net/login` (or your URL)
- [ ] Both login flows work
- [ ] No console errors
- [ ] No broken styles

### 5.4 Production Deployment
- [ ] All staging tests passed
- [ ] Code review completed
- [ ] Merge to `main`
- [ ] Tag release: `git tag v1.1.0-unified-login`
- [ ] Monitor production

## 🎯 Success Criteria

- [ ] Admin SSO login works
- [ ] Client credentials login works
- [ ] All tests pass
- [ ] No TypeScript errors
- [ ] No ESLint warnings
- [ ] Documentation updated
- [ ] Code deployed to production

## 🐛 Quick Troubleshooting

**Import errors?**
```bash
rm -rf .next node_modules/.cache
npm run build
```

**Styles not loading?**
- Check `transpilePackages` in next.config.js
- Clear browser cache

**SSO redirect loop?**
- Verify `NEXTAUTH_URL` environment variable
- Check Authentik callback URL

**Credentials login fails?**
- Check credentials provider in NextAuth config
- Verify API endpoint

## 📞 Need Help?

- Review full plan: `.agent/tasks/UNIFIED_LOGIN_MIGRATION.md`
- Check shared-ui README: `packages/shared-ui/README.md`
- Test locally before deploying

---

**Estimated Total Time**: 4 hours  
**Difficulty**: Medium  
**Risk**: Low (easy rollback)

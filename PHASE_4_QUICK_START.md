# Phase 4 - Quick Start Guide

**Status:** 🚀 READY TO BEGIN
**Estimated Time:** 2-3 days (9-12 hours)

---

## TL;DR - Start Testing in 3 Steps

### Step 1: Verify Auth Service (5 minutes)

```bash
# Check if auth service is accessible
curl -s https://api.bizoholic.com/auth/health

# If not accessible, verify on server
ssh root@72.60.219.244 'docker service ls | grep auth'
```

### Step 2: Start All Frontend Applications (10 minutes)

Open 7 terminal windows and run:

```bash
# Terminal 1 - Client Portal
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/client-portal && npm run dev

# Terminal 2 - Bizoholic Frontend
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/bizoholic-frontend && npm run dev

# Terminal 3 - CoreLDove Storefront
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/coreldove-storefront && pnpm dev

# Terminal 4 - BizOSaaS Admin
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/bizosaas-admin && npm run dev

# Terminal 5 - Business Directory
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/business-directory && npm run dev

# Terminal 6 - ThrillRing Gaming
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/thrillring-gaming && npm run dev

# Terminal 7 - Analytics Dashboard
cd /home/alagiri/projects/bizosaas-platform/bizosaas/frontend/apps/analytics-dashboard && npm run dev
```

### Step 3: Begin Testing (Start now!)

1. **Open browser** to `http://localhost:3000`
2. **Login** with `admin@bizosaas.com` / `AdminDemo2024!`
3. **Verify** dashboard loads
4. **Navigate** to other platforms and verify SSO works
5. **Document** results in [PHASE_4_TESTING_EXECUTION.md](PHASE_4_TESTING_EXECUTION.md)

---

## Test Credentials Quick Reference

```bash
# Super Admin (all platforms)
admin@bizosaas.com / AdminDemo2024!

# Standard User
user@bizosaas.com / UserDemo2024!

# Tenant Admins
admin@bizoholic.com / AdminDemo2024!
admin@coreldove.com / AdminDemo2024!
admin@thrillring.com / AdminDemo2024!
```

---

## Platform URLs

| Platform | URL | Port |
|----------|-----|------|
| Client Portal | http://localhost:3000 | 3000 |
| Bizoholic Frontend | http://localhost:3001 | 3001 |
| CoreLDove Storefront | http://localhost:3002 | 3002 |
| BizOSaaS Admin | http://localhost:3003 | 3003 |
| Business Directory | http://localhost:3004 | 3004 |
| ThrillRing Gaming | http://localhost:3006 | 3006 |
| Analytics Dashboard | http://localhost:3009 | 3009 |

---

## Testing Checklist

### Priority 1: Basic Auth (30 minutes)
- [ ] Login works on all 7 platforms
- [ ] Logout works on all 7 platforms
- [ ] User info displays correctly
- [ ] No console errors

### Priority 2: SSO (45 minutes)
- [ ] Login on one platform = logged in on all
- [ ] Logout on one platform = logged out on all
- [ ] Session shared via cookies
- [ ] No duplicate logins required

### Priority 3: Security (30 minutes)
- [ ] No tokens in localStorage
- [ ] No tokens in sessionStorage
- [ ] Refresh tokens are HttpOnly
- [ ] Cookies have Secure flag

### Priority 4: RBAC (60 minutes)
- [ ] Super admin sees all features
- [ ] Standard users see limited features
- [ ] Admin features hidden from non-admins
- [ ] No privilege escalation possible

---

## Quick Commands

```bash
# Check all running frontends
lsof -i :3000,3001,3002,3003,3004,3006,3009

# Clear browser cache (Chrome)
# Press: Ctrl+Shift+Del → Clear browsing data

# View auth service logs
ssh root@72.60.219.244 'docker service logs backendservices-authservice-ux07ss --tail 50'

# Restart auth service (if needed)
ssh root@72.60.219.244 'docker service update --force backendservices-authservice-ux07ss'
```

---

## Documentation Files

- **Testing Plan:** [PHASE_4_SSO_TESTING_PLAN.md](PHASE_4_SSO_TESTING_PLAN.md) - Detailed 7 test suites
- **Execution Log:** [PHASE_4_TESTING_EXECUTION.md](PHASE_4_TESTING_EXECUTION.md) - Track progress
- **Ready Status:** [PHASE_4_READY_TO_BEGIN.md](PHASE_4_READY_TO_BEGIN.md) - Pre-testing checklist
- **Phase 3 Summary:** [PHASE_3_COMPLETE_SUMMARY.md](PHASE_3_COMPLETE_SUMMARY.md) - What was completed

---

## Expected Results

✅ **After successful Phase 4:**
- Login works seamlessly across all 7 platforms
- SSO propagates login/logout across platforms
- Users see appropriate features based on roles
- Session persists after page refresh
- Security features verified (XSS/CSRF protection)
- All findings documented

❌ **If issues found:**
- Document in [PHASE_4_TESTING_EXECUTION.md](PHASE_4_TESTING_EXECUTION.md)
- Create GitHub issues for critical bugs
- Update troubleshooting guide

---

## Support

**Documentation:** All test plans and execution logs are in `/home/alagiri/projects/bizosaas-platform/`

**GitHub:** https://github.com/Bizoholic-Digital/bizosaas-platform

**Latest Commits:**
- [ac4451d](https://github.com/Bizoholic-Digital/bizosaas-platform/commit/ac4451d) - Phase 4 ready status
- [a1d0d8d](https://github.com/Bizoholic-Digital/bizosaas-platform/commit/a1d0d8d) - Phase 4 testing execution log
- [43840f5](https://github.com/Bizoholic-Digital/bizosaas-platform/commit/43840f5) - Phase 4 testing plan

---

**Ready to begin?** Start with Step 1 above! 🚀

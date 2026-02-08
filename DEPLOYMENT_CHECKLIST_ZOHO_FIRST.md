# Deployment Checklist: Zoho-First Strategy Implementation

**Date:** January 15, 2026  
**Status:** Ready for Deployment

---

## 🎯 Deployment Decision Summary

### Lago Status: **KEEP IN STANDBY MODE** ✅

**Rationale:**
- Already deployed and running
- Minimal resource consumption
- Provides future migration path
- No immediate need to delete
- Can be stopped (not deleted) if resources are tight

**Action:** Leave Lago deployed but inactive. Focus on Zoho integration.

---

## 📦 Changes Ready for Deployment

### 1. Brain Gateway Service
**Files Changed:**
- `bizosaas-brain-core/brain-gateway/seed_mcp.py` (31 new MCPs)
- Database schema (already updated via seed script)

**Deployment Method:** Dokploy UI Redeploy

### 2. Admin Dashboard Service
**Files Changed:**
- `portals/admin-dashboard/app/(dashboard)/mcp-management/page.tsx` (NEW)

**Deployment Method:** Dokploy UI Redeploy

### 3. Documentation
**Files Updated:**
- `ZOHO_FIRST_STRATEGY_IMPLEMENTATION.md` (NEW)
- `bizosaas-details-11012026.md` (TO BE UPDATED)

---

## ✅ Pre-Deployment Checklist

### Step 1: Commit Changes to Git
```bash
cd /home/alagiri/projects/bizosaas-platform

# Stage all changes
git add bizosaas-brain-core/brain-gateway/seed_mcp.py
git add portals/admin-dashboard/app/\(dashboard\)/mcp-management/
git add ZOHO_FIRST_STRATEGY_IMPLEMENTATION.md
git add bizosaas-details-11012026.md

# Commit with descriptive message
git commit -m "feat: Implement Zoho-First strategy with 76 MCPs and admin management

- Add 31 new MCPs (Zoho suite, Microsoft, Google, hosting providers)
- Create MCP Management page for admin dashboard
- Enable affiliate link management from UI
- Expand hosting options (AWS, Azure, DigitalOcean, Vultr, Utho, Hostinger)
- Document Zoho-First billing strategy
- Total MCPs: 76 across 12 categories"

# Push to GitHub
git push origin main
```

### Step 2: Verify GitHub Push
- [ ] Check GitHub repository shows latest commit
- [ ] Verify all files are present in the commit

### Step 3: Redeploy Brain Gateway via Dokploy
1. [ ] Open Dokploy UI: `https://dk8.bizoholic.com`
2. [ ] Navigate to "Brain Gateway" service
3. [ ] Click "Redeploy" or "Rebuild"
4. [ ] Wait for build to complete (monitor logs)
5. [ ] Verify deployment success

### Step 4: Verify Brain Gateway Deployment
```bash
# Check if service is running
docker ps | grep brain-gateway

# Verify MCP count
docker exec bizosaas-brain-staging python3 -c "from app.dependencies import SessionLocal; from app.models.mcp import McpRegistry; db = SessionLocal(); print(f'Total MCPs: {db.query(McpRegistry).count()}')"

# Expected output: Total MCPs: 76
```

### Step 5: Redeploy Admin Dashboard via Dokploy
1. [ ] Navigate to "Admin Dashboard" service in Dokploy
2. [ ] Click "Redeploy" or "Rebuild"
3. [ ] Wait for build to complete
4. [ ] Verify deployment success

### Step 6: Verify Admin Dashboard Deployment
1. [ ] Open Admin Dashboard: `https://admin.bizoholic.net`
2. [ ] Navigate to `/mcp-management`
3. [ ] Verify page loads correctly
4. [ ] Check that all 76 MCPs are displayed
5. [ ] Test editing an affiliate link
6. [ ] Verify changes save successfully

### Step 7: Test Client Portal Onboarding
1. [ ] Open Client Portal: `https://portal.bizoholic.net`
2. [ ] Start onboarding flow
3. [ ] Navigate to "Select Tools" step (Step 3)
4. [ ] Verify all 76 MCPs are displayed
5. [ ] Check category filtering works
6. [ ] Verify Zoho services are visible

---

## 🔧 Post-Deployment Tasks

### Immediate (Day 1)
- [ ] Configure Zoho Billing API credentials
- [ ] Set up payment gateway integrations (Stripe, PayPal, Razorpay)
- [ ] Add affiliate links for top 10 MCPs
- [ ] Test end-to-end subscription flow

### Short-term (Week 1)
- [ ] Create sub-admin roles and permissions
- [ ] Implement MCP marketplace (add/remove MCPs from UI)
- [ ] Add MCP installation workflow
- [ ] Create affiliate tracking dashboard

### Medium-term (Month 1)
- [ ] Integrate PartnerStack or FirstPromoter for affiliate tracking
- [ ] Build commission reporting
- [ ] Add MCP usage analytics
- [ ] Create recommendation engine

---

## 🚨 Rollback Plan (If Needed)

### If Brain Gateway Deployment Fails:
```bash
# Rollback to previous version via Dokploy UI
# Or manually:
docker exec bizosaas-brain-staging git checkout HEAD~1
docker restart bizosaas-brain-staging
```

### If Admin Dashboard Deployment Fails:
```bash
# Rollback via Dokploy UI
# Or remove the new page temporarily:
rm portals/admin-dashboard/app/\(dashboard\)/mcp-management/page.tsx
git commit -m "temp: Remove MCP management page"
git push origin main
# Redeploy via Dokploy
```

---

## 📊 Success Metrics

After deployment, verify:
- [ ] **76 MCPs** visible in database
- [ ] **Admin MCP Management** page accessible
- [ ] **Client Onboarding** displays all tools
- [ ] **Affiliate links** editable from admin UI
- [ ] **No errors** in application logs
- [ ] **All services** running smoothly

---

## 🎉 Next Steps After Successful Deployment

1. **Update Documentation** - Mark all tasks as complete
2. **Notify Team** - Share deployment success
3. **Begin Zoho Integration** - Set up API credentials
4. **Test Workflows** - Verify end-to-end user journeys
5. **Monitor Performance** - Watch logs for any issues

---

## 📞 Support Contacts

**If Issues Arise:**
- Check Dokploy logs for build errors
- Review Docker container logs
- Verify database connectivity
- Check GitHub Actions (if CI/CD enabled)

---

**Deployment Owner:** Platform Admin  
**Estimated Time:** 30-45 minutes  
**Risk Level:** Low (incremental changes, no breaking changes)

---

## ✅ Final Checklist

Before marking as complete:
- [ ] All code committed and pushed
- [ ] Brain Gateway redeployed successfully
- [ ] Admin Dashboard redeployed successfully
- [ ] 76 MCPs verified in database
- [ ] MCP Management page accessible
- [ ] Client onboarding shows new tools
- [ ] No critical errors in logs
- [ ] Documentation updated
- [ ] Team notified

**Status:** ⏳ Ready to Deploy

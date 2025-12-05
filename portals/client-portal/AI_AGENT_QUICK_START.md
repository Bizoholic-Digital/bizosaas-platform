# AI Agent System - Quick Start Guide

**Date:** December 4, 2024, 9:55 PM IST

---

## 🚀 **Quick Start (5 Minutes)**

### **Step 1: Seed Test Accounts** (1 min)
```bash
cd /home/alagiri/projects/bizosaas-platform/shared/services/auth
python3 seed_test_users.py
```

### **Step 2: Start Platform** (2 min)
```bash
cd /home/alagiri/projects/bizosaas-platform
./scripts/start-bizosaas-full.sh
```

### **Step 3: Login** (1 min)
1. Navigate to: `http://localhost:3003/login`
2. Email: `admin@bizoholic.com`
3. Password: `AdminDemo2024!`

### **Step 4: Access AI Agents** (1 min)
1. Look for "AI Agents (93)" in sidebar
2. Click to view all agents
3. Click any agent to configure
4. Explore 7 configuration tabs

---

## ✅ **Verification Checklist**

- [ ] Build completes successfully
- [ ] Login works with admin@bizoholic.com
- [ ] "AI Agents" menu visible in sidebar
- [ ] Can navigate to /ai-agents
- [ ] All 93 agents are listed
- [ ] Can click agent to configure
- [ ] 7 tabs visible (Super Admin)
- [ ] BYOK page loads

---

## 🎯 **What You Can Do Now**

### **1. Browse All 93 Agents**
- Filter by category (13 categories)
- Search by name
- Toggle grid/list view
- See agent status (Active/Inactive)

### **2. Configure Any Agent**
- **Basic Settings** - Name, description, cost tier
- **System Prompt** - Custom behavior (Super Admin only)
- **Fine-Tuning** - Instructions and examples (Super Admin only)
- **LLM Config** - Provider, model, temperature
- **Tools** - Select available tools
- **APIs** - Configure required keys
- **Permissions** - Access control

### **3. Manage API Keys (BYOK)**
- Add keys for 20+ services
- Test key validity
- View usage statistics
- Rotate keys
- Delete keys

---

## 📋 **Test Accounts**

| Role | Email | Password |
|------|-------|----------|
| Super Admin | admin@bizoholic.com | AdminDemo2024! |
| Admin | admin@test.com | Admin2024!Test |
| User | user@test.com | User2024!Test |
| Client | client@test.com | Client2024!Test |

**See TEST_ACCOUNTS.md for complete list**

---

## 🐛 **Troubleshooting**

### **Issue: AI Agents menu not showing**
**Solution:** Login with admin@bizoholic.com (super_admin role)

### **Issue: Build fails**
**Solution:** 
```bash
cd /home/alagiri/projects/bizosaas-platform/portals/client-portal
npm install @radix-ui/react-slider --legacy-peer-deps
npm run build
```

### **Issue: Cannot login**
**Solution:** Re-seed accounts:
```bash
cd /home/alagiri/projects/bizosaas-platform/shared/services/auth
python3 seed_test_users.py
```

---

## 📚 **Documentation**

- **AI_AGENT_COMPLETE_SUMMARY.md** - Complete implementation summary
- **TEST_ACCOUNTS.md** - All test account credentials
- **AI_AGENT_TROUBLESHOOTING.md** - Troubleshooting guide
- **AI_AGENT_SETTINGS_RECOMMENDATION.md** - UI/UX design rationale

---

## 🎉 **You're Ready!**

The AI Agent System is fully implemented and ready to use!

**Next:** Start configuring agents and adding your API keys via BYOK.

---

**Last Updated:** December 4, 2024, 9:55 PM IST

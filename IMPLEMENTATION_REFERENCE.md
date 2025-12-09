# BizOSaaS Implementation Reference Guide

**Date**: 2025-12-08  
**Status**: Pre-Deployment (Local Testing Phase)

---

## 📚 Documents to Keep Open

### Core Architecture
| Document | Path | Purpose |
|----------|------|---------|
| **DDD + Hexagonal Guide** | `bizosaas-brain-core/DDD-Hexogonal-Architecture.md` | Architecture principles, bounded contexts |
| **Architecture V3** | `bizosaas-brain-core/ARCHITECTURE_RECOMMENDATION_V3.md` | Detailed system design |

### Authentication
| Document | Path | Purpose |
|----------|------|---------|
| **Auth Strategy** | `AUTH_VS_AUTHENTIK.md` | Decision: Why Authentik wins |
| **Authentik Implementation** | `AUTHENTIK_IMPLEMENTATION.md` | Step-by-step integration guide |

### Deployment
| Document | Path | Purpose |
|----------|------|---------|
| **Oracle Cloud Setup** | `ORACLE_CLOUD_SETUP.md` | VM provisioning guide |
| **Deployment Tools** | `DEPLOYMENT_TOOLS_ANALYSIS.md` | Coolify recommendation |
| **Terraform Config** | `infrastructure/terraform/` | Infrastructure as Code |

### Gap Analysis
| Document | Path | Purpose |
|----------|------|---------|
| **Client Portal Gaps** | `CLIENT_PORTAL_GAP_ANALYSIS.md` | Frontend/Backend status |

### Scripts
| File | Path | Purpose |
|------|------|---------|
| **Oracle Setup Script** | `scripts/setup_oracle.sh` | Installs Docker + Coolify |

---

## 🔄 Current Implementation Priority

### Phase 1: Authentik Integration (LOCAL)
1. ⬜ Start Authentik locally via Docker Compose
2. ⬜ Create `domain/ports/identity_port.py`
3. ⬜ Create `adapters/identity/authentik_adapter.py`
4. ⬜ Update Brain Gateway middleware
5. ⬜ Update NextAuth to use Authentik provider
6. ⬜ Test login flow end-to-end

### Phase 2: Oracle Deployment
1. ⬜ Install Terraform locally
2. ⬜ Run `terraform apply` → Get 2 Oracle VMs
3. ⬜ Run `setup_oracle.sh` on VM 1
4. ⬜ Access Coolify, deploy services

---

## 📁 Project Structure Reference

```
bizosaas-platform/
├── bizosaas-brain-core/
│   ├── auth/                    # ❌ TO BE REPLACED by Authentik
│   ├── brain-gateway/           # ✅ Core API (Update for Authentik)
│   │   ├── domain/
│   │   │   └── ports/           # 🆕 CREATE: identity_port.py
│   │   ├── adapters/
│   │   │   └── identity/        # 🆕 CREATE: authentik_adapter.py
│   │   └── main.py              # UPDATE: Remove auth proxy
│   ├── docker-compose.yml       # UPDATE: Add Authentik
│   └── DDD-Hexogonal-Architecture.md
│
├── portals/
│   └── client-portal/
│       ├── app/
│       │   ├── api/auth/        # UPDATE: NextAuth → Authentik
│       │   └── dashboard/       # ✅ Ready
│       └── components/auth/     # UPDATE: Remove credential login
│
├── infrastructure/
│   └── terraform/               # ✅ Ready (2 Oracle VMs)
│
├── scripts/
│   └── setup_oracle.sh          # ✅ Ready
│
└── [Documentation Files]        # ✅ All created
```

---

## 🔑 Key Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Identity Provider** | Authentik (not custom, not FastAPI Users) | SSO across Portal + WordPress + Gateway |
| **Deployment Tool** | Coolify (not Dokploy, not K8s) | ARM64 native, one-click services |
| **Secrets Management** | Vault | Enterprise-grade, tenant isolation |
| **Infrastructure** | Oracle Cloud Free Tier | 4 OCPU, 24GB RAM, $0/month |
| **Architecture** | Hexagonal + DDD | Swappable adapters, testable core |

---

## 🚀 Quick Start Commands

### Start Authentik Locally
```bash
cd bizosaas-brain-core
docker-compose -f docker-compose.authentik.yml up -d
# Access: http://localhost:9000/if/flow/initial-setup/
```

### Start Brain Stack Locally
```bash
cd bizosaas-brain-core
./start-bizosaas-core-full.sh
# Or: docker-compose up -d
```

### Provision Oracle Cloud
```bash
cd infrastructure/terraform
terraform init
terraform apply
```

---

## ⚠️ Next Immediate Action

**Before Oracle deployment, complete Authentik integration locally:**

1. Create the Identity Port interface (Phase 1, Step 2)
2. Create the Authentik Adapter (Phase 1, Step 3)
3. Test locally with `docker-compose.authentik.yml`

Once local testing passes → Deploy to Oracle.

---

## 📞 Support Files Index

| Need | Document |
|------|----------|
| How to verify DDD compliance | `DDD-Hexogonal-Architecture.md` (lines 320-384) |
| What tabs are implemented | `CLIENT_PORTAL_GAP_ANALYSIS.md` (Tab Matrix) |
| How to connect WordPress | `Connector` dialog (already implemented) |
| Oracle firewall rules | `ORACLE_CLOUD_SETUP.md` (Phase 2) |

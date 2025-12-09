# Authentication Strategy: Final Recommendation

**Date**: 2025-12-08  
**Platform**: BizOSaaS (Multi-tenant, Multi-brand SaaS)  
**Constraint**: Must integrate with HashiCorp Vault for secrets.

---

## ✅ FINAL RECOMMENDATION: **Authentik**

For a **Platform** (not a single app), Authentik is the correct choice.

---

## Why NOT FastAPI Users + Authlib?

| Factor | FastAPI Users | Why It Falls Short for BizOSaaS |
|--------|---------------|--------------------------------|
| **SSO Across Apps** | ❌ Not built-in | BizOSaaS has Portal, Gateway, WordPress, CMS. Each needs SSO. FastAPI Users only protects one app. |
| **OAuth Provider** | ❌ Must build from scratch | You want WordPress (Hostinger) to "Login with BizOSaaS". This requires an **OAuth Server**. FastAPI Users is a **Client**, not a Server. |
| **MFA/Security** | ⚠️ DIY | You must implement TOTP, WebAuthn, brute-force protection yourself. |
| **Admin UI** | ❌ None | No user management dashboard. You build it. |

**Verdict**: FastAPI Users is excellent for **single-app** backends. BizOSaaS is a **multi-app ecosystem** requiring a centralized Identity Provider.

---

## Why Authentik Wins

| Requirement | Authentik Capability |
|-------------|---------------------|
| **SSO for Portal + Gateway + WordPress** | ✅ Native OIDC/OAuth2 Provider |
| **MFA for Clients** | ✅ Built-in (TOTP, WebAuthn) |
| **Tenant Isolation (Brands)** | ✅ Via "Tenants" feature |
| **Enterprise SAML** | ✅ Ready for corporate clients |
| **Coolify One-Click Deploy** | ✅ Available as service |
| **Scalability** | ✅ Runs separately from Brain |

---

## Vault Integration Strategy

**Vault** and **Authentik** serve **different purposes**:

| System | Role | Stores |
|--------|------|--------|
| **Authentik** | Identity Provider | User accounts, passwords (hashed), MFA tokens |
| **Vault** | Secrets Manager | API Keys, DB Credentials, Client Secrets, Connector Tokens |

### Integration Points:

1. **Brain Gateway → Vault**: Retrieves `AUTHENTIK_CLIENT_SECRET` at startup.
2. **Brain Gateway → Vault**: Retrieves Connector credentials (WordPress API keys, etc.).
3. **Authentik → Vault** (Optional Advanced): Authentik can use Vault as a "Signing Key Provider" for JWT signatures.

### Secrets That Go Into Vault:
- `authentik/client_secret` (For Gateway OIDC)
- `postgres/password`
- `redis/password`
- `connectors/wordpress/api_key`
- `connectors/shopify/api_secret`

### Secrets That Stay in Authentik:
- User password hashes (bcrypt/argon2).
- TOTP seeds.
- Session tokens.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Oracle Cloud (Free Tier)                 │
├────────────────────────┬────────────────────────────────────┤
│     Node 1 (Primary)   │         Node 2 (Worker)            │
│  ┌──────────────────┐  │  ┌──────────────────────────────┐  │
│  │     Coolify      │  │  │  Brain Gateway (FastAPI)     │  │
│  ├──────────────────┤  │  ├──────────────────────────────┤  │
│  │    Authentik     │◄─┼──│  Client Portal (Next.js)     │  │
│  ├──────────────────┤  │  ├──────────────────────────────┤  │
│  │   Vault (HA?)    │◄─┼──│  Temporal Workers            │  │
│  ├──────────────────┤  │  └──────────────────────────────┘  │
│  │   PostgreSQL     │  │                                    │
│  │   Redis          │  │                                    │
│  └──────────────────┘  │                                    │
└────────────────────────┴────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   Hostinger VPS (WordPress)   │
              │   bizoholic.com / coreldove   │
              │   Uses "Login with BizOSaaS"  │
              │   via Authentik OIDC          │
              └───────────────────────────────┘
```

---

## Implementation Order

1. ✅ **Terraform** → Provision Oracle Nodes (Done - Ready to Apply)
2. ⬜ **Coolify** → Install on Node 1
3. ⬜ **Authentik** → Deploy via Coolify
4. ⬜ **Vault** → Deploy via Coolify (or Docker Compose)
5. ⬜ **Brain Gateway** → Deploy, configure OIDC to Authentik
6. ⬜ **Client Portal** → Deploy, configure NextAuth to Authentik
7. ⬜ **Test** → Login flow end-to-end

---

## Conclusion

**Use Authentik** as the central Identity Provider.  
**Use Vault** for API secrets and connector credentials.  
**Do NOT use FastAPI Users** for a multi-app platform.

# Dokploy Environment Variable Configuration Guide

Based on the 3 Neon DB accounts and other cloud services, please configure the following environment variables in the Dokploy UI for each stack.

## 1. Core Stack (`core-stack`)
**Usage**: Brain Gateway + AI Agents + MCP
**Database**: Neon Account 2 (Dedicated Core DB)

| Variable | Recommended Value |
|---|---|
| `DATABASE_URL` | `postgresql://<user>:<pass>@<account2-host>.neon.tech/bizosaas?sslmode=require` |
| `REDIS_URL` | `redis://bizosaas-admin:rwL1HrSHn01$^w@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0` |
| `TEMPORAL_ADDRESS` | `ap-south-2.aws.api.temporal.io:7233` |
| `TEMPORAL_NAMESPACE` | `bizosaas-platform.mdqxv` |
| `TEMPORAL_API_KEY` | `eyJhbGciOiJFUzI1NiIsICJraWQiOiJXdnR3YUEifQ...` (see credentials.md) |
| `OPENAI_API_KEY` | (OpenRouter Key) |
| `OPENROUTER_API_KEY` | (OpenRouter Key) |
| `VAULT_URL` | `http://brain-vault:8200` |
| `GITHUB_TOKEN` | (GitHub PAT) |

---

## 2. Postiz Stack
**Usage**: Social Media Scheduling
**Database**: Neon Account 3 (Social DB)

| Variable | Recommended Value |
|---|---|
| `POSTIZ_DATABASE_URL` | `postgresql://<user>:<pass>@<account3-host>.neon.tech/postiz?sslmode=require` |
| `REDIS_URL` | `redis://bizosaas-admin:rwL1HrSHn01$^w@redis-10690.c264.ap-south-1-1.ec2.cloud.redislabs.com:10690/0` |
| `TEMPORAL_ADDRESS` | `ap-south-2.aws.api.temporal.io:7233` |
| `TEMPORAL_NAMESPACE` | `bizosaas-platform.mdqxv` |
| `TEMPORAL_API_KEY` | (same as core-stack) |
| `OPENAI_API_KEY` | (OpenRouter Key) |
| `POSTIZ_AUTHENTIK_CLIENT_ID` | (from Authentik Admin) |
| `POSTIZ_AUTHENTIK_CLIENT_SECRET` | (from Authentik Admin) |

---

## 3. Lago Billing & Wagtail CMS
**Usage**: Billing & Content
**Database**: Neon Account 1 (Existing: `ep-gentle-flower`)

**Lago Environment**:
- `DATABASE_URL=postgresql://neondb_owner:npg_puEbTnkSO9F8@ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require`

**Wagtail Environment**:
- `DATABASE_URL=postgresql://neondb_owner:npg_puEbTnkSO9F8@ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/wagtail_db?sslmode=require`

---

## Next Steps for Verification
1. **Apply these variables** in Dokploy.
2. **Redeploy** the stacks.
3. Run `curl https://api.bizoholic.net/health` to verify core connectivity.
4. Run `docker ps` on the VPS to ensure zero local database containers (except Authentik/Vault/SEO Panel MySQL).

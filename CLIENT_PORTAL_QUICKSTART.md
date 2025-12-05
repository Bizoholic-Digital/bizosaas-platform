# 🚀 Client Portal - Quick Start (Subdomain Architecture)

## Local Development URLs

| Service | URL | Port |
|---------|-----|------|
| **Client Portal** | `http://localhost:3003` | 3003 |
| **Bizoholic Frontend** | `http://localhost:3001` | 3001 |
| **Brain API** | `http://localhost:8000` | 8000 |
| **Auth Service** | `http://localhost:8008` | 8008 |

## Production URLs (Future)

| Service | URL |
|---------|-----|
| **Client Portal** | `https://client.bizoholic.com` |
| **Main Website** | `https://www.bizoholic.com` |
| **API Gateway** | `https://api.bizoholic.com` |

## Quick Commands

### Start Client Portal
```bash
cd portals/client-portal
npm run dev -- --port 3003
```

### Start Bizoholic Frontend
```bash
cd brands/bizoholic/frontend
npm run dev
```

### Demo Login Credentials
- **Email:** `demo@bizosaas.com`
- **Password:** `demo123`

## Testing Checklist

- [ ] Access `http://localhost:3003`
- [ ] Redirected to `http://localhost:3003/login`
- [ ] Login successful
- [ ] Dashboard loads at `http://localhost:3003/`
- [ ] Click CRM → URL is `http://localhost:3003/?tab=crm`
- [ ] Click AI Assistant → URL is `http://localhost:3003/chat`
- [ ] From AI Assistant, click CRM → Back to `http://localhost:3003/?tab=crm`
- [ ] No unexpected login redirects
- [ ] Browser back/forward works correctly

## Troubleshooting

### Issue: "Cannot GET /portal"
**Solution:** You're using the old URL. Use `http://localhost:3003` instead of `http://localhost:3001/portal`.

### Issue: Redirect loop to login
**Solution:** 
1. Open browser console (F12)
2. Look for `[AUTH]` logs
3. Clear localStorage: `localStorage.clear()`
4. Refresh and login again

### Issue: Changes not reflecting
**Solution:** Restart the server (Ctrl+C, then `npm run dev -- --port 3003`)

## Architecture Change Summary

✅ **Removed:** `basePath: '/portal'` from Client Portal  
✅ **Removed:** Proxy rewrites from Bizoholic Frontend  
✅ **Result:** Clean, independent services on separate ports/domains

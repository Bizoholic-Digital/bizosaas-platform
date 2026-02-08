# Client Portal Login Credentials

## Current Setup (Demo Mode)

The Client Portal currently uses a **demo/fallback login** system while the SSO Auth Service integration is being finalized.

### Demo Login Credentials ✅ WORKING NOW

```
Email: demo@bizosaas.com
Password: demo123
```

This is handled by the internal API route at `/api/auth/login` in the Client Portal.

---

## Future SSO Integration (Planned)

Once the Auth Service endpoints are configured, you'll be able to use these SSO credentials:

### SuperAdmin Account
```
Email: superadmin@bizosaas.com
Password: BizoSaaS2025!Admin
Role: superadmin
```

### Administrator Account
```
Email: administrator@bizosaas.com
Password: Bizoholic2025!Admin
Role: admin
```

### Regular User Account
```
Email: bizoholic_user@bizosaas.com
Password: Bizoholic2025!User
Role: user
```

---

## How to Login

1. **Access the Client Portal:**
   ```
   http://localhost:3003
   ```

2. **You will be redirected to:**
   ```
   http://localhost:3003/login
   ```

3. **Enter credentials** (use any of the accounts above)

4. **After successful login:**
   - You'll be redirected to `http://localhost:3003/` (Dashboard)
   - Your session will be stored in `localStorage`
   - Tokens: `access_token`, `refresh_token`, `user_data`

---

## Troubleshooting

### If Auth Service is not running:
```bash
# Check if auth service is running
curl http://localhost:8008/health

# If not running, start it
cd /home/alagiri/projects/bizosaas-platform
# Use your start script or docker-compose
```

### If login fails:
1. **Check browser console** for error messages
2. **Check Auth Service logs**
3. **Verify the Auth Service is accessible:**
   ```bash
   curl -X POST http://localhost:8008/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"superadmin@bizosaas.com","password":"BizoSaaS2025!Admin"}'
   ```

### Clear session if stuck:
```javascript
// In browser console (F12)
localStorage.clear();
location.reload();
```

---

## Auth Flow

```
User → Login Form (localhost:3003/login)
  ↓
  POST to Auth Service (localhost:8008/auth/login)
  ↓
  Auth Service validates credentials
  ↓
  Returns: { access_token, refresh_token, user: {...} }
  ↓
  AuthProvider stores tokens in localStorage
  ↓
  Redirect to Dashboard (localhost:3003/)
```

---

## Notes

- The Auth Service uses **JWT tokens** for authentication
- Tokens are stored in browser `localStorage`
- Session persists across page refreshes
- Logout clears all tokens and redirects to `/login`

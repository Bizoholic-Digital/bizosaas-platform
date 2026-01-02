# 🚨 Urgent Fixes Required

## 1. Fix Database Connection (Brain Gateway)
The logs show the `brain-gateway` is still trying to connect to the OLD `bizosaas-postgres-staging` container.
This means **Dokploy has stale Environment Variables** configured in its UI.

**Action Required:**
1.  Go to **Dokploy UI** -> **BizOSaaS Core** Project -> **brain-gateway** service.
2.  Go to the **Environment** tab.
3.  **Update `DATABASE_URL`** to the Neon Cloud URL:
    ```
    postgresql://neondb_owner:npg_puEbTnkSO9F8@ep-gentle-flower-a15rdh2r-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
    ```
4.  Remove any references to `bizosaas-postgres-staging` or `localhost`.
5.  Click **Save**.

## 2. Fix Admin Dashboard Not Updating
The UI changes (sidebar user profile) are not showing up because the build didn't pick up the latest code. This happens if Dokploy reuses a cached build.

**Action Required:**
1.  Go to **Dokploy UI** -> **BizOSaaS Frontend** Project -> **admin-dashboard** service.
2.  Go to **Deployment** tab (or Settings).
3.  Look for **"Clear Cache"** or **"Rebuild without Cache"** option if available.
4.  If not, simply clicking "Redeploy" *should* work now that I've pushed a fresh commit (see below).

## 3. Client Portal Update
I have moved the **Live API** indicator from the header to the sidebar footer, next to "System Online".
*   **Action**: Redeploy **Client Portal** service in Dokploy.

---

## 🛠️ Summary of Changes Pushed
*   **Client Portal**: UI updated ("Live API" moved to sidebar).
*   **Admin Dashboard**: (No code changes needed, just rebuild required).
*   **Brain Gateway**: (No code changes needed, environment variable fix required in Dokploy UI).

Please proceed with these steps now.

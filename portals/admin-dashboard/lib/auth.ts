import NextAuth from "next-auth";
import type { NextAuthConfig } from "next-auth";
import Credentials from "next-auth/providers/credentials";

// Use same Authentik URL pattern as client portal
const AUTHENTIK_URL = process.env.AUTHENTIK_URL || process.env.NEXT_PUBLIC_SSO_URL || 'https://sso.bizoholic.net';

// Ensure NEXTAUTH_URL is set for production
if (process.env.NODE_ENV === 'production' && !process.env.NEXTAUTH_URL) {
  console.warn('⚠️  NEXTAUTH_URL is not set in production!');
}

export const authConfig: NextAuthConfig = {
  providers: [
    ...(process.env.AUTHENTIK_CLIENT_ID && process.env.AUTHENTIK_CLIENT_SECRET ? [
      {
        id: "authentik",
        name: "BizOSaaS SSO",
        type: "oidc" as const,
        // Use same base URL, different application slug
        issuer: process.env.AUTHENTIK_ISSUER || `${AUTHENTIK_URL}/application/o/bizosaas/`,
        clientId: process.env.AUTHENTIK_CLIENT_ID || "bizosaas-admin-dashboard",
        clientSecret: process.env.AUTHENTIK_CLIENT_SECRET || "",
        authorization: {
          params: {
            scope: "openid profile email groups",
          },
          url: `${AUTHENTIK_URL}/application/o/authorize/`,
        },
        token: `${AUTHENTIK_URL}/application/o/token/`,
        userinfo: `${AUTHENTIK_URL}/application/o/userinfo/`,
        profile(profile: any) {
          // Map Authentik groups to roles
          const groups = profile.groups || [];
          const roles = groups.filter((g: string) =>
            g === 'super_admin' || g === 'platform_admin'
          );

          return {
            id: profile.sub,
            name: profile.name,
            email: profile.email,
            image: profile.picture,
            roles: roles,
            tenant_id: (profile as any).tenant_id,
          };
        },
      }
    ] : []),
    Credentials({
      name: "BizOSaaS Credentials",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;

        try {
          // Method 1: Direct Resource Owner Password Credentials (ROPC) flow against Authentik
          // This allows background login without redirecting to the Authentik UI
          const clientId = process.env.AUTHENTIK_CLIENT_ID;
          const clientSecret = process.env.AUTHENTIK_CLIENT_SECRET;

          if (clientId && clientSecret) {
            try {
              const tokenEndpoint = `${AUTHENTIK_URL}/application/o/token/`;
              const params = new URLSearchParams();
              params.append('grant_type', 'password');
              params.append('username', credentials.email as string);
              params.append('password', credentials.password as string);
              params.append('client_id', clientId);
              params.append('client_secret', clientSecret);
              // Admin might need specific scopes or just standard ones
              params.append('scope', 'openid profile email groups');

              const tokenResponse = await fetch(tokenEndpoint, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: params
              });

              if (tokenResponse.ok) {
                const tokens = await tokenResponse.json();

                if (tokens.access_token) {
                  // Now fetch user profile with the access token
                  const userinfoResponse = await fetch(`${AUTHENTIK_URL}/application/o/userinfo/`, {
                    headers: {
                      'Authorization': `Bearer ${tokens.access_token}`
                    }
                  });

                  if (userinfoResponse.ok) {
                    const profile = await userinfoResponse.json();
                    const groups = profile.groups || [];
                    const roles = groups.filter((g: string) =>
                      g === 'super_admin' || g === 'platform_admin'
                    );

                    console.log("✅ Admin Authentik Background Login Successful for:", profile.email);

                    return {
                      id: profile.sub,
                      name: profile.name,
                      email: profile.email,
                      image: profile.picture,
                      roles: roles,
                      tenant_id: (profile as any).tenant_id,
                    };
                  }
                }
              } else {
                const errorText = await tokenResponse.text();
                console.warn("⚠️ Admin Authentik ROPC Login failed (falling back):", tokenResponse.status, errorText);
              }
            } catch (ropcError) {
              console.error("⚠️ Admin Authentik ROPC Error (falling back):", ropcError);
            }
          }

          // Validate against Auth Service
          const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL || 'http://brain-auth:8007';
          const authServiceResponse = await fetch(`${AUTH_SERVICE_URL}/auth/sso/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              email: credentials.email,
              password: credentials.password,
              platform: 'bizosaas-admin', // Use admin platform identifier
              remember_me: true
            })
          });

          if (authServiceResponse.ok) {
            const data = await authServiceResponse.json();

            // Allow all users to login, role based routing handled in authorized callback
            return {
              id: data.user.id,
              name: `${data.user.first_name || ''} ${data.user.last_name || ''}`.trim(),
              email: data.user.email,
              roles: [data.user?.role],
              tenant_id: data.tenant.id,
            };
          }
          return null;
        } catch (e) {
          console.error('Admin login error:', e);
          return null;
        }
      }
    }),
  ],
  callbacks: {
    async jwt({ token, user, account, profile }) {
      if (account && user) {
        token.accessToken = account.access_token;
        token.roles = user.roles;
        token.tenant_id = user.tenant_id;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.accessToken = token.accessToken as string;
        session.user.roles = token.roles as string[];
        session.user.tenant_id = token.tenant_id as string;
      }
      return session;
    },
    async authorized({ auth, request }) {
      const { pathname } = request.nextUrl;

      // Public routes
      if (pathname === "/login" || pathname === "/unauthorized" || pathname.startsWith("/api/auth") || pathname.startsWith("/api/health")) {
        return true;
      }

      // Check if user is authenticated
      if (!auth?.user) {
        return false;
      }

      // Check if user has admin role
      const roles = (auth.user as any).roles || [];
      // Accept 'admin' as well, as some backends might return generic 'admin' role
      const hasAdminRole = roles.includes("platform_admin") || roles.includes("super_admin") || roles.includes("admin");

      if (!hasAdminRole) {
        console.warn("⚠️ User authenticated but lacks admin role:", auth.user?.email, roles);
        // Redirect non-admins to Client Portal
        const clientPortalUrl = process.env.NEXT_PUBLIC_CLIENT_PORTAL_URL || 'http://localhost:3003';
        return Response.redirect(`${clientPortalUrl}/dashboard`);
      }

      return true;
    },
  },
  pages: {
    signIn: "/login",
    error: "/login",
  },
  debug: process.env.NODE_ENV === 'development',
  session: {
    strategy: "jwt" as const,
    maxAge: 8 * 60 * 60, // 8 hours total session duration
    updateAge: 30 * 60, // Update session every 30 minutes (inactivity timeout)
  },
  cookies: {
    sessionToken: {
      name: `next-auth.session-token`,
      options: {
        httpOnly: true,
        sameSite: 'lax' as const,
        path: '/',
        domain: process.env.NODE_ENV === 'production' ? '.bizoholic.net' : undefined,
        secure: process.env.NODE_ENV === 'production',
      },
    },
  },
  secret: process.env.NEXTAUTH_SECRET || 'development-secret-change-in-production',
  trustHost: true,
};

export const { handlers, auth, signIn, signOut } = NextAuth(authConfig);

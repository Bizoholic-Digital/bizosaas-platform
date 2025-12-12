import NextAuth from "next-auth";
import type { NextAuthConfig } from "next-auth";

// Use same Authentik URL pattern as client portal
const AUTHENTIK_URL = process.env.AUTHENTIK_URL || process.env.NEXT_PUBLIC_SSO_URL || 'https://sso.bizoholic.net';

export const authConfig: NextAuthConfig = {
  providers: [
    {
      id: "authentik",
      name: "BizOSaaS SSO",
      type: "oidc",
      // Use same base URL, different application slug
      issuer: process.env.AUTHENTIK_ISSUER || `${AUTHENTIK_URL}/application/o/bizosaas-admin/`,
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
      profile(profile) {
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
    },
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
      const hasAdminRole = roles.includes("platform_admin") || roles.includes("super_admin");

      if (!hasAdminRole) {
        return Response.redirect(new URL("/unauthorized", request.url));
      }

      return true;
    },
  },
  pages: {
    signIn: "/login",
    error: "/login",
  },
  session: {
    strategy: "jwt",
  },
  trustHost: true,
};

export const { handlers, auth, signIn, signOut } = NextAuth(authConfig);

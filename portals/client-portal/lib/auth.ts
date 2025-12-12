import NextAuth from "next-auth";
// import type { NextAuthConfig } from "next-auth"; // Removed to avoid resolution error
import Authentik from "next-auth/providers/authentik";
import Credentials from "next-auth/providers/credentials";

const BRAIN_GATEWAY_URL = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8001';
const AUTHENTIK_URL = process.env.AUTHENTIK_URL || process.env.NEXT_PUBLIC_SSO_URL || 'https://sso.bizoholic.net';

export const authConfig = {
    providers: [
        Authentik({
            name: 'BizOSaaS SSO',
            clientId: process.env.AUTHENTIK_CLIENT_ID,
            clientSecret: process.env.AUTHENTIK_CLIENT_SECRET,
            issuer: process.env.AUTHENTIK_ISSUER || `${AUTHENTIK_URL}/application/o/bizosaas/`,
            authorization: {
                params: {
                    scope: "openid profile email",
                },
                url: `${AUTHENTIK_URL}/application/o/authorize/`,
            },
            token: `${AUTHENTIK_URL}/application/o/token/`,
            userinfo: `${AUTHENTIK_URL}/application/o/userinfo/`,
        }),
        Credentials({
            name: 'Email & Password',
            credentials: {
                email: { label: "Email", type: "email" },
                password: { label: "Password", type: "password" },
                brand: { label: "Brand", type: "text" }
            },
            async authorize(credentials) {
                if (!credentials?.email || !credentials?.password) {
                    return null;
                }

                try {
                    // Method 1: Validate against Authentik using API
                    const AUTHENTIK_API_TOKEN = process.env.AUTHENTIK_API_TOKEN;

                    if (AUTHENTIK_API_TOKEN) {
                        const userResponse = await fetch(
                            `${AUTHENTIK_URL}/api/v3/core/users/?email=${encodeURIComponent(credentials.email as string)}`,
                            {
                                headers: {
                                    'Authorization': `Bearer ${AUTHENTIK_API_TOKEN}`,
                                },
                            }
                        );

                        if (userResponse.ok) {
                            const userData = await userResponse.json();
                            const user = userData.results?.[0];

                            if (user && user.is_active) {
                                console.log('User found in Authentik, but password validation requires SSO');
                                return null;
                            }
                        }
                    }

                    // Method 2: Fallback to Auth Service
                    const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL || 'http://brain-auth:8007';
                    const authServiceResponse = await fetch(`${AUTH_SERVICE_URL}/auth/sso/login`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            email: credentials.email,
                            password: credentials.password,
                            platform: credentials.brand || 'bizoholic',
                            remember_me: true
                        })
                    });

                    if (authServiceResponse.ok) {
                        const data = await authServiceResponse.json();
                        return {
                            id: data.user.id,
                            name: `${data.user.first_name || ''} ${data.user.last_name || ''}`.trim(),
                            email: data.user.email,
                            role: data.user.role,
                            tenant_id: data.tenant.id,
                            brand: (credentials.brand as string) || 'bizoholic',
                            access_token: data.access_token,
                            refresh_token: data.refresh_token
                        };
                    }
                    return null;
                } catch (e) {
                    console.error('Login error:', e);
                    return null;
                }
            }
        })
    ],
    callbacks: {
        async jwt({ token, user, account, profile }) {
            if (user) {
                token.id = user.id;
                token.role = (user as any).role;
                token.tenant_id = (user as any).tenant_id;
                token.brand = (user as any).brand;
                token.access_token = (user as any).access_token;
                token.refresh_token = (user as any).refresh_token;
            }

            if (account?.provider === 'authentik' && profile) {
                const groups = (profile as any).groups || [];
                const role = groups.includes('authentik Admins') ? 'admin' : 'user';
                token.id = profile.sub || token.id;
                token.role = role;
                token.tenant_id = (profile as any).tenant_id || 'default-tenant';
                token.brand = 'bizoholic';
            }
            return token;
        },
        async session({ session, token }) {
            if (token && session.user) {
                session.user.id = token.id as string;
                (session.user as any).role = token.role as string;
                (session.user as any).tenant_id = token.tenant_id as string;
                (session.user as any).brand = token.brand as string;
                (session as any).access_token = token.access_token as string;
                (session as any).refresh_token = token.refresh_token as string;
            }
            return session;
        },
        async authorized({ auth, request: { nextUrl } }) {
            const isLoggedIn = !!auth?.user;
            const isOnDashboard = nextUrl.pathname.startsWith('/dashboard');
            if (isOnDashboard) {
                if (isLoggedIn) return true;
                return false; // Redirect unauthenticated users to login page
            } else if (isLoggedIn) {
                // return Response.redirect(new URL('/dashboard', nextUrl));
            }
            return true;
        },
    },
    pages: {
        signIn: '/login',
        error: '/login',
    },
    session: {
        strategy: 'jwt',
        maxAge: 8 * 60 * 60, // 8 hours total session duration
        updateAge: 30 * 60, // Update session every 30 minutes (inactivity timeout)
    },
    secret: process.env.NEXTAUTH_SECRET || 'development-secret-change-in-production',
    trustHost: true,
};

export const { handlers, auth, signIn, signOut } = NextAuth(authConfig);

import NextAuth from "next-auth";
// import type { NextAuthConfig } from "next-auth"; // Removed to avoid resolution error
import Authentik from "next-auth/providers/authentik";
import Google from "next-auth/providers/google";
import AzureAD from "next-auth/providers/azure-ad";
import LinkedIn from "next-auth/providers/linkedin";
import Credentials from "next-auth/providers/credentials";

const BRAIN_GATEWAY_URL = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8001';
const AUTHENTIK_URL = process.env.AUTHENTIK_URL || process.env.NEXT_PUBLIC_SSO_URL || 'https://sso.bizoholic.net';

// Ensure NEXTAUTH_URL is set for production
if (process.env.NODE_ENV === 'production' && !process.env.NEXTAUTH_URL) {
    console.warn('⚠️  NEXTAUTH_URL is not set in production!');
}

export const authConfig = {
    providers: [
        // Google OAuth
        ...(process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET ? [
            Google({
                clientId: process.env.GOOGLE_CLIENT_ID,
                clientSecret: process.env.GOOGLE_CLIENT_SECRET,
                authorization: {
                    params: {
                        prompt: "consent",
                        access_type: "offline",
                        response_type: "code"
                    }
                }
            })
        ] : []),
        // Microsoft OAuth
        ...(process.env.MICROSOFT_CLIENT_ID && process.env.MICROSOFT_CLIENT_SECRET ? [
            AzureAD({
                clientId: process.env.MICROSOFT_CLIENT_ID,
                clientSecret: process.env.MICROSOFT_CLIENT_SECRET,
                tenantId: process.env.MICROSOFT_TENANT_ID || "common",
            })
        ] : []),
        // LinkedIn OAuth
        ...(process.env.LINKEDIN_CLIENT_ID && process.env.LINKEDIN_CLIENT_SECRET ? [
            LinkedIn({
                clientId: process.env.LINKEDIN_CLIENT_ID,
                clientSecret: process.env.LINKEDIN_CLIENT_SECRET,
                authorization: {
                    params: { scope: "r_liteprofile r_emailaddress" }
                }
            })
        ] : []),
        // Authentik SSO (disabled for Client Portal - uses background ROPC instead)
        // Users login via email/password which authenticates against Authentik in the background
        // To re-enable SSO redirect: uncomment lines below
        /*
        ...(process.env.AUTHENTIK_CLIENT_ID && process.env.AUTHENTIK_CLIENT_SECRET ? [
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
            })
        ] : []),
        */
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

                // TEST USER: For staging verification (remove in production)
                // This bypasses external services to prove NextAuth flow works
                console.log('🔐 Authorize called with:', credentials.email);
                console.log('🔐 ENV check - NEXTAUTH_URL:', process.env.NEXTAUTH_URL);
                console.log('🔐 ENV check - NEXTAUTH_SECRET exists:', !!process.env.NEXTAUTH_SECRET);

                if (credentials.email === 'demo@bizoholic.net' && credentials.password === 'demo123') {
                    console.log("✅ Demo user login successful - returning user object");
                    return {
                        id: 'demo-user-001',
                        name: 'Demo User',
                        email: 'demo@bizoholic.net',
                        role: 'admin',
                        tenant_id: 'demo-tenant',
                        brand: 'bizoholic',
                        access_token: 'demo-token',
                        refresh_token: 'demo-refresh'
                    };
                }

                try {
                    // Method 1: Direct Resource Owner Password Credentials (ROPC) flow against Authentik
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
                            params.append('scope', 'openid profile email');

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
                                        const role = groups.includes('authentik Admins') ? 'admin' : 'user';

                                        console.log("✅ Authentik Background Login Successful for:", profile.email);

                                        return {
                                            id: profile.sub,
                                            name: profile.name,
                                            email: profile.email,
                                            role: role,
                                            tenant_id: 'default-tenant',
                                            brand: 'bizoholic',
                                            access_token: tokens.access_token,
                                            refresh_token: tokens.refresh_token
                                        };
                                    }
                                }
                            } else {
                                const errorText = await tokenResponse.text();
                                console.warn("⚠️ Authentik ROPC Login failed (falling back):", tokenResponse.status, errorText);
                            }
                        } catch (ropcError) {
                            console.error("⚠️ Authentik ROPC Error (falling back):", ropcError);
                        }
                    }

                    // Method 2: Fallback to Auth Service
                    // Only used if Direct Authentik login failed or wasn't configured
                    console.log("🔄 Falling back to Brain Auth Service...");
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
                console.log("DEBUG: JWT Callback - User:", { id: user.id, hasToken: !!(user as any).access_token });
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
            console.log("DEBUG: Session Callback - Token:", { hasToken: !!token.access_token });
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
    debug: true, // Temporarily enabled for troubleshooting
    session: {
        strategy: 'jwt' as const,
        maxAge: 8 * 60 * 60, // 8 hours total session duration
        updateAge: 30 * 60, // Update session every 30 minutes (inactivity timeout)
    },
    cookies: {
        sessionToken: {
            name: process.env.NODE_ENV === 'production'
                ? '__Secure-next-auth.session-token'
                : 'next-auth.session-token',
            options: {
                httpOnly: true,
                sameSite: 'lax',
                path: '/',
                secure: process.env.NODE_ENV === 'production',
            },
        },
    },

    secret: process.env.NEXTAUTH_SECRET || 'development-secret-change-in-production',
    trustHost: true,
};

export const { handlers, auth, signIn, signOut } = NextAuth(authConfig);

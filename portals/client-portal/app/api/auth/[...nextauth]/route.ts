import NextAuth, { NextAuthOptions } from 'next-auth';
import AuthentikProvider from 'next-auth/providers/authentik';
import CredentialsProvider from 'next-auth/providers/credentials';

const BRAIN_GATEWAY_URL = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8001';

// Use Authentik URL from environment (same for both internal and public in Dokploy)
const AUTHENTIK_URL = process.env.AUTHENTIK_URL || process.env.NEXT_PUBLIC_SSO_URL || 'https://sso.bizoholic.net';

export const authOptions: NextAuthOptions = {
    providers: [
        // Authentik Provider (SSO)
        AuthentikProvider({
            name: 'BizOSaaS SSO',
            clientId: process.env.AUTHENTIK_CLIENT_ID || '',
            clientSecret: process.env.AUTHENTIK_CLIENT_SECRET || '',
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

        // Hybrid Credentials Provider (Email/Password via Authentik)
        CredentialsProvider({
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
                    // Note: We can't directly validate password via API, so we check if user exists
                    // and rely on SSO button for actual Authentik authentication
                    const AUTHENTIK_API_TOKEN = process.env.AUTHENTIK_API_TOKEN;

                    if (AUTHENTIK_API_TOKEN) {
                        const userResponse = await fetch(
                            `${AUTHENTIK_URL}/api/v3/core/users/?email=${encodeURIComponent(credentials.email)}`,
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
                                // User exists in Authentik
                                // For security, we should use SSO button for Authentik users
                                // But for convenience, we'll create a session if user exists
                                // Note: This doesn't validate password! Use SSO for secure auth

                                console.log('User found in Authentik, but password validation requires SSO');
                                // Don't authenticate here - redirect to SSO
                                return null; // Force user to use SSO button
                            }
                        }
                    }

                    // Method 2: Fallback to Auth Service (for legacy users)
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
                            email: data.user.email,
                            name: `${data.user.first_name || ''} ${data.user.last_name || ''}`.trim(),
                            role: data.user.role,
                            tenant_id: data.tenant.id,
                            brand: credentials.brand || 'bizoholic',
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
        }),
        // Social Providers removed (Handled by Authentik)
    ],

    callbacks: {
        // JWT Callback - Add custom fields to token
        async jwt({ token, user, account, profile }) {
            // Initial sign in
            if (user) {
                token.id = user.id;
                token.role = user.role;
                token.tenant_id = user.tenant_id;
                token.brand = user.brand;
                token.access_token = user.access_token;
                token.refresh_token = user.refresh_token;
            }

            // Handle Authentik login - Map OIDC profile directly
            if (account?.provider === 'authentik' && profile) {
                // Determine role from groups or default
                const groups = (profile as any).groups || [];
                const role = groups.includes('authentik Admins') ? 'admin' : 'user';

                token.id = profile.sub || token.id;
                token.role = role;
                token.tenant_id = (profile as any).tenant_id || 'default-tenant';
                token.brand = 'bizoholic';
                // Don't call backend yet - rely on OIDC profile
                return token;
            }

            // Handle legacy social login (Github/Google)
            if (account?.provider === 'github' || account?.provider === 'google') {
                try {
                    // Register/login user via Brain Gateway
                    const response = await fetch(`${BRAIN_GATEWAY_URL}/api/auth/social-login`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            email: profile?.email,
                            provider: account.provider,
                            secret: process.env.NEXTAUTH_SECRET, // Required for verification
                            platform: 'bizoholic', // Default platform for social login
                            name: profile?.name,
                            avatar_url: (profile as any)?.image || (profile as any)?.picture || (profile as any)?.avatar_url
                        })
                    });

                    if (response.ok) {
                        const data = await response.json();
                        token.id = data.user.id;
                        token.role = data.user.role;
                        token.tenant_id = data.tenant.id;
                        token.brand = 'bizoholic';
                        token.access_token = data.access_token;
                        token.refresh_token = data.refresh_token;
                    } else {
                        console.error('Social login failed:', await response.text());
                    }
                } catch (error) {
                    console.error('Social login error:', error);
                }
            }

            return token;
        },

        // Session Callback - Add custom fields to session
        async session({ session, token }) {
            if (token && session.user) {
                session.user.id = token.id as string;
                session.user.role = token.role as string;
                session.user.tenant_id = token.tenant_id as string;
                session.user.brand = token.brand as string;
                session.access_token = token.access_token as string;
                session.refresh_token = token.refresh_token as string;
            }
            return session;
        },

        // Redirect Callback - Handle post-login redirects
        async redirect({ url, baseUrl }) {
            // If redirecting after login, go to dashboard
            if (url === baseUrl || url === `${baseUrl}/`) {
                return `${baseUrl}/dashboard`;
            }
            // Allow relative URLs
            if (url.startsWith('/')) return `${baseUrl}${url}`;
            // Allow same origin URLs
            else if (url.startsWith(baseUrl)) return url;
            // Default to dashboard
            return `${baseUrl}/dashboard`;
        }
    },

    pages: {
        signIn: '/login',
        error: '/login',
    },

    session: {
        strategy: 'jwt',
        maxAge: 30 * 24 * 60 * 60, // 30 days
    },

    secret: process.env.NEXTAUTH_SECRET || 'development-secret-change-in-production',
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };

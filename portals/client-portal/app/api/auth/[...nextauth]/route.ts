import NextAuth, { NextAuthOptions } from 'next-auth';
import AuthentikProvider from 'next-auth/providers/authentik';
import CredentialsProvider from 'next-auth/providers/credentials';

const BRAIN_GATEWAY_URL = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8001';

// Use Authentik service name for internal Docker communication
const AUTHENTIK_INTERNAL_URL = process.env.AUTHENTIK_INTERNAL_URL || 'http://authentik-server:9000';
// Use localhost for browser-redirects
const AUTHENTIK_PUBLIC_URL = process.env.AUTHENTIK_URL || 'http://localhost:9000';

export const authOptions: NextAuthOptions = {
    providers: [
        // Authentik Provider (SSO)
        AuthentikProvider({
            name: 'BizOSaaS SSO',
            clientId: process.env.AUTHENTIK_CLIENT_ID || 'bizosaas-brain',
            clientSecret: process.env.AUTHENTIK_CLIENT_SECRET || '',
            issuer: process.env.AUTHENTIK_ISSUER || `${AUTHENTIK_INTERNAL_URL}/application/o/bizosaas-brain/`,
            authorization: {
                params: {
                    scope: "openid profile email",
                },
                url: `${AUTHENTIK_PUBLIC_URL}/application/o/authorize/`,
            },
            token: `${AUTHENTIK_INTERNAL_URL}/application/o/token/`,
            userinfo: `${AUTHENTIK_INTERNAL_URL}/application/o/userinfo/`,
            wellKnown: `${AUTHENTIK_INTERNAL_URL}/application/o/bizosaas-brain/.well-known/openid-configuration`,
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
                    // Try Authentik first (Resource Owner Password Credentials flow)
                    const authentikTokenUrl = `${AUTHENTIK_INTERNAL_URL}/application/o/token/`;

                    const authentikResponse = await fetch(authentikTokenUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: new URLSearchParams({
                            grant_type: 'password',
                            username: credentials.email,
                            password: credentials.password,
                            client_id: process.env.AUTHENTIK_CLIENT_ID || '',
                            client_secret: process.env.AUTHENTIK_CLIENT_SECRET || '',
                            scope: 'openid profile email',
                        }),
                    });

                    if (authentikResponse.ok) {
                        const tokenData = await authentikResponse.json();

                        // Get user info from Authentik
                        const userinfoResponse = await fetch(`${AUTHENTIK_INTERNAL_URL}/application/o/userinfo/`, {
                            headers: {
                                'Authorization': `Bearer ${tokenData.access_token}`,
                            },
                        });

                        if (userinfoResponse.ok) {
                            const userInfo = await userinfoResponse.json();

                            return {
                                id: userInfo.sub,
                                email: userInfo.email,
                                name: userInfo.name || userInfo.preferred_username,
                                role: userInfo.groups?.includes('authentik Admins') ? 'admin' : 'user',
                                tenant_id: userInfo.tenant_id || 'default-tenant',
                                brand: credentials.brand || 'bizoholic',
                                access_token: tokenData.access_token,
                                refresh_token: tokenData.refresh_token,
                            };
                        }
                    }

                    // Fallback to Auth Service (for legacy users not in Authentik)
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

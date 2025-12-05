import NextAuth, { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import GithubProvider from 'next-auth/providers/github';
import GoogleProvider from 'next-auth/providers/google';

const BRAIN_GATEWAY_URL = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8001';

export const authOptions: NextAuthOptions = {
    providers: [
        // Credentials Provider - Email/Password via Brain Gateway
        CredentialsProvider({
            name: 'Credentials',
            credentials: {
                email: { label: "Email", type: "email" },
                password: { label: "Password", type: "password" },
                brand: { label: "Brand", type: "text" }
            },
            async authorize(credentials) {
                if (!credentials?.email || !credentials?.password) {
                    throw new Error('Email and password required');
                }

                try {
                    // Call Auth Service DIRECTLY (bypassing Brain Gateway for now)
                    const AUTH_SERVICE_URL = 'http://localhost:8009';
                    const response = await fetch(`${AUTH_SERVICE_URL}/auth/sso/login`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            email: credentials.email,
                            password: credentials.password,
                            platform: credentials.brand || 'bizoholic',
                            remember_me: true
                        })
                    });

                    if (!response.ok) {
                        const errorText = await response.text();
                        console.error('Login failed:', response.status, errorText);
                        return null;
                    }

                    const data = await response.json();
                    console.log('Login successful:', data);

                    // Return user object with tokens
                    return {
                        id: data.user.id,
                        email: data.user.email,
                        name: `${data.user.first_name || ''} ${data.user.last_name || ''}`.trim() || data.user.email,
                        role: data.user.role,
                        tenant_id: data.tenant.id,
                        brand: credentials.brand || 'bizoholic',
                        access_token: data.access_token,
                        refresh_token: data.refresh_token
                    };
                } catch (error) {
                    console.error('Auth error:', error);
                    return null;
                }
            }
        }),

        // GitHub Provider
        GithubProvider({
            clientId: process.env.GITHUB_CLIENT_ID || 'dummy',
            clientSecret: process.env.GITHUB_CLIENT_SECRET || 'dummy',
            authorization: {
                params: {
                    scope: 'read:user user:email'
                }
            }
        }),

        // Google Provider
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID || 'dummy',
            clientSecret: process.env.GOOGLE_CLIENT_SECRET || 'dummy',
            authorization: {
                params: {
                    prompt: "consent",
                    access_type: "offline",
                    response_type: "code"
                }
            }
        })
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

            // Handle social login
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

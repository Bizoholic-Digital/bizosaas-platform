import NextAuth, { NextAuthOptions, DefaultSession, DefaultUser } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import GoogleProvider from "next-auth/providers/google";

declare const process: {
    env: {
        [key: string]: string | undefined;
    };
};

declare module "next-auth" {
    interface Session extends DefaultSession {
        user: {
            id: string;
            roles: string[];
            tenant_id: string;
        } & DefaultSession["user"];
        accessToken?: string;
    }

    interface User extends DefaultUser {
        id: string;
        roles?: string[];
        tenant_id?: string;
    }
}

const AUTHENTIK_URL = process.env.AUTHENTIK_URL || process.env.NEXT_PUBLIC_SSO_URL || 'https://sso.bizoholic.net';
const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL || 'http://brain-auth:8007';

export const authOptions: NextAuthOptions = {
    providers: [
        CredentialsProvider({
            name: "BizOSaaS Credentials",
            credentials: {
                email: { label: "Email", type: "text" },
                password: { label: "Password", type: "password" }
            },
            async authorize(credentials) {
                if (!credentials?.email || !credentials?.password) return null;

                // TEST USER: For staging verification (remove in production)
                if (credentials.email === 'admin@bizoholic.net' && credentials.password === 'admin123') {
                    console.log("✅ Admin demo user login successful");
                    return {
                        id: 'admin-demo-001',
                        name: 'Admin Demo',
                        email: 'admin@bizoholic.net',
                        roles: ['super_admin'],
                        tenant_id: 'demo-tenant',
                    } as any;
                }

                const AUTHENTIK_CLIENT_ID = process.env.AUTHENTIK_CLIENT_ID;
                const AUTHENTIK_CLIENT_SECRET = process.env.AUTHENTIK_CLIENT_SECRET;

                // Method 1: ROPC flow against Authentik
                if (AUTHENTIK_CLIENT_ID && AUTHENTIK_CLIENT_SECRET) {
                    try {
                        const tokenEndpoint = `${AUTHENTIK_URL}/application/o/token/`;
                        const params = new URLSearchParams();
                        params.append('grant_type', 'password');
                        params.append('username', credentials.email);
                        params.append('password', credentials.password);
                        params.append('client_id', AUTHENTIK_CLIENT_ID);
                        params.append('client_secret', AUTHENTIK_CLIENT_SECRET);
                        params.append('scope', 'openid profile email groups');

                        const tokenResponse = await fetch(tokenEndpoint, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: params
                        });

                        if (tokenResponse.ok) {
                            const tokens = await tokenResponse.json();
                            if (tokens.access_token) {
                                const userinfoResponse = await fetch(`${AUTHENTIK_URL}/application/o/userinfo/`, {
                                    headers: { 'Authorization': `Bearer ${tokens.access_token}` }
                                });

                                if (userinfoResponse.ok) {
                                    const profile = await userinfoResponse.json();
                                    const groups = profile.groups || [];
                                    const roles = groups.flatMap((g: string) => {
                                        if (g === 'authentik Admins') return ['super_admin'];
                                        if (g === 'admin' || g === 'super_admin' || g === 'platform_admin') return [g];
                                        return [];
                                    });

                                    // Check if user has admin role
                                    if (roles.length === 0) {
                                        console.warn(`User ${profile.email} lacks admin roles for Admin Dashboard`);
                                        return null;
                                    }

                                    return {
                                        id: profile.sub,
                                        name: profile.name,
                                        email: profile.email,
                                        roles: roles,
                                        tenant_id: profile.tenant_id || "default",
                                        accessToken: tokens.access_token
                                    } as any;
                                }
                            }
                        }
                    } catch (e) {
                        console.error('ROPC flow error:', e);
                    }
                }

                // Method 2: Fallback to Auth Service
                try {
                    console.log(`Admin Login: Falling back to Auth Service at ${AUTH_SERVICE_URL}`);
                    const response = await fetch(`${AUTH_SERVICE_URL}/auth/sso/login`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            email: credentials.email,
                            password: credentials.password,
                            platform: 'bizosaas-admin',
                            remember_me: true
                        })
                    });

                    if (response.ok) {
                        const data = await response.json();
                        console.log("Admin Login: Fallback success for", data.user.email);
                        return {
                            id: data.user.id,
                            name: `${data.user.first_name || ''} ${data.user.last_name || ''}`.trim(),
                            email: data.user.email,
                            roles: [data.user?.role || 'admin'],
                            tenant_id: data.tenant?.id || "default",
                        };
                    } else {
                        const errText = await response.text();
                        console.error("Admin Login: Fallback failed with status", response.status, errText);
                    }
                } catch (e) {
                    console.error('Admin fallback login error:', e);
                }
                return null;
            }
        }),
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID || "",
            clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
            profile(profile: any) {
                return {
                    id: profile.sub,
                    name: profile.name,
                    email: profile.email,
                    image: profile.picture,
                    roles: ["user"], // Default role for social login
                    tenant_id: "default", // Default tenant or look up
                };
            },
        }),
        // Authentik SSO (disabled - uses background ROPC instead)
        /*
        {
            id: "authentik",
            name: "BizOSaaS SSO",
            type: "oauth",
            wellKnown: `${AUTHENTIK_URL}/application/o/bizosaas-admin/.well-known/openid-configuration`,
            authorization: { params: { scope: "openid profile email groups" } },
            idToken: true,
            clientId: process.env.AUTHENTIK_CLIENT_ID || "",
            clientSecret: process.env.AUTHENTIK_CLIENT_SECRET || "",
            checks: ["pkce", "state"],
            profile(profile: any) {
                console.log("Admin SSO Profile Received:", profile.email, "Groups:", profile.groups);
                const groups = profile.groups || [];
                const roles = groups.flatMap((g: string) => {
                    if (g === 'authentik Admins') return ['super_admin'];
                    if (g === 'admin' || g === 'super_admin' || g === 'platform_admin') return [g];
                    return [];
                });

                return {
                    id: profile.sub,
                    name: profile.name,
                    email: profile.email,
                    image: profile.picture,
                    roles: roles,
                    tenant_id: profile.tenant_id || "default",
                };
            },
        } as any,
        */
    ],
    callbacks: {
        async jwt({ token, user, account, profile }: any) {
            if (user) {
                console.log("Admin JWT: Initial sign-in for user:", user.email);
                token.id = user.id;
                token.roles = (user as any).roles;
                token.tenant_id = (user as any).tenant_id;
            }
            if (account) {
                console.log("Admin JWT: Account provider:", account.provider);
                token.accessToken = account.access_token;
            }
            if (profile) {
                console.log("Admin JWT: Profile recognized");
            }
            return token;
        },
        async session({ session, token }: any) {
            if (token && session.user) {
                console.log("Admin Session: Mapping token to session for:", session.user.email);
                (session.user as any).id = token.id as string;
                (session.user as any).roles = token.roles as string[];
                (session.user as any).tenant_id = token.tenant_id as string;
                (session as any).accessToken = token.accessToken as string;
            }
            return session;
        },
    },
    pages: {
        signIn: "/login",
        error: "/login",
    },
    session: {
        strategy: "jwt",
    },
    debug: true,
    secret: process.env.NEXTAUTH_SECRET || 'development-secret-change-in-production',
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };

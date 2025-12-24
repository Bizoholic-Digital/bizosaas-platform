import NextAuth, { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

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

                try {
                    // Direct login via Auth Service (standard pattern)
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
        {
            id: "authentik",
            name: "BizOSaaS SSO",
            type: "oauth",
            wellKnown: `${AUTHENTIK_URL}/application/o/bizosaas/.well-known/openid-configuration`,
            authorization: { params: { scope: "openid profile email groups" } },
            idToken: true,
            clientId: process.env.AUTHENTIK_CLIENT_ID,
            clientSecret: process.env.AUTHENTIK_CLIENT_SECRET,
            checks: ["pkce", "state"],
            profile(profile: any) {
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
                    tenant_id: profile.tenant_id,
                };
            },
        } as any,
    ],
    callbacks: {
        async jwt({ token, user, account }) {
            if (user) {
                token.id = user.id;
                token.roles = (user as any).roles;
                token.tenant_id = (user as any).tenant_id;
            }
            if (account) {
                token.accessToken = account.access_token;
            }
            return token;
        },
        async session({ session, token }) {
            if (session.user) {
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
    secret: process.env.NEXTAUTH_SECRET || 'development-secret-change-in-production',
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };

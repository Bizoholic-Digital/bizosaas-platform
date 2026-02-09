import NextAuth from "next-auth"
import type { NextAuthConfig } from "next-auth"
import Authentik from "next-auth/providers/authentik"

export const config = {
    providers: [
        Authentik({
            clientId: process.env.AUTH_AUTHENTIK_ID,
            clientSecret: process.env.AUTH_AUTHENTIK_SECRET,
            issuer: process.env.AUTH_AUTHENTIK_ISSUER,
        })
    ],
    callbacks: {
        async session({ session, token }: any) {
            if (token) {
                session.access_token = token.accessToken
                session.user.id = token.sub
                session.user.role = token.role as string
                session.user.tenant_id = token.tenant_id as string
                session.user.onboarded = token.onboarded as boolean
                session.user.plan_features = token.plan_features as string[] || []

                // Optionally fetch latest data from backend if needed
                // To keep it fast, we rely on the token but the token should be refreshed 
                // or the backend should update the user profile in the SSO.
            }
            return session
        },
        async jwt({ token, user, account }: any) {
            if (account && user) {
                token.accessToken = account.access_token

                // Fetch latest data from backend to get role and plan features
                try {
                    const baseUrl = process.env.NEXT_PUBLIC_BRAIN_API_URL || 'http://localhost:8000';
                    const res = await fetch(`${baseUrl}/api/users/me`, {
                        headers: { 'Authorization': `Bearer ${account.access_token}` }
                    });
                    if (res.ok) {
                        const profile = await res.json();
                        token.role = profile.role;
                        token.plan_features = profile.plan_features;
                        token.tenant_id = profile.tenant_id;
                        token.onboarded = profile.onboarded;
                    } else {
                        // Fallback to provider data
                        token.role = user.role
                        token.tenant_id = user.tenant_id
                        token.onboarded = user.onboarded
                    }
                } catch (e) {
                    console.error('Failed to fetch profile in JWT callback', e);
                    token.role = user.role
                    token.tenant_id = user.tenant_id
                    token.onboarded = user.onboarded
                }
            }
            return token
        }
    },
    session: { strategy: "jwt" },
    secret: process.env.NEXTAUTH_SECRET,
} satisfies NextAuthConfig

export const { handlers, auth, signIn, signOut } = NextAuth(config)

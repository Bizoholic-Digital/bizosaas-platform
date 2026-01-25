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

                // Optionally fetch latest data from backend if needed
                // To keep it fast, we rely on the token but the token should be refreshed 
                // or the backend should update the user profile in the SSO.
            }
            return session
        },
        async jwt({ token, user, account }: any) {
            if (account && user) {
                token.accessToken = account.access_token
                token.role = user.role
                token.tenant_id = user.tenant_id
                token.onboarded = user.onboarded
            }
            return token
        }
    },
    session: { strategy: "jwt" },
    secret: process.env.NEXTAUTH_SECRET,
} satisfies NextAuthConfig

export const { handlers, auth, signIn, signOut } = NextAuth(config)

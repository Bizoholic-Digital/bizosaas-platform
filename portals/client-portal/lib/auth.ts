import NextAuth from "next-auth"
import type { NextAuthConfig } from "next-auth"

export const config = {
    providers: [], // Configured in auth.config.ts or at runtime
    callbacks: {
        async session({ session, token }: any) {
            if (token) {
                session.access_token = token.accessToken
                session.user.id = token.sub
                session.user.role = token.role as string
                session.user.tenant_id = token.tenant_id as string
            }
            return session
        },
        async jwt({ token, user, account }: any) {
            if (account && user) {
                token.accessToken = account.access_token
                token.role = user.role
                token.tenant_id = user.tenant_id
            }
            return token
        }
    },
    session: { strategy: "jwt" },
    secret: process.env.NEXTAUTH_SECRET,
} satisfies NextAuthConfig

export const { handlers, auth, signIn, signOut } = NextAuth(config)

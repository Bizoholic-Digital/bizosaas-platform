import NextAuth, { DefaultSession, DefaultUser } from "next-auth"
import { JWT } from "next-auth/jwt"

declare module "next-auth" {
    /**
     * Returned by `useSession`, `getSession` and received as a prop on the `SessionProvider` React Context
     */
    interface Session {
        user: {
            id: string
            role: string
            tenant_id: string
            brand: string
        } & DefaultSession["user"]
        access_token: string
        refresh_token: string
    }

    interface User extends DefaultUser {
        id: string
        role: string
        tenant_id: string
        brand: string
        access_token: string
        refresh_token: string
    }

    interface NextAuthOptions {
        trustHost?: boolean
    }
}

declare module "next-auth/jwt" {
    /** Returned by the `jwt` callback and `getToken`, when using JWT sessions */
    interface JWT {
        id: string
        role: string
        tenant_id: string
        brand: string
        access_token: string
        refresh_token: string
    }
}

import NextAuth, { DefaultSession } from "next-auth";

declare module "next-auth" {
    interface Session {
        accessToken?: string;
        user: {
            roles?: string[];
            tenant_id?: string;
        } & DefaultSession["user"];
    }

    interface User {
        roles?: string[];
        tenant_id?: string;
    }
}

declare module "next-auth/jwt" {
    interface JWT {
        accessToken?: string;
        roles?: string[];
        tenant_id?: string;
    }
}

import NextAuth from 'next-auth';
import AuthentikProvider from 'next-auth/providers/authentik';

const handler = NextAuth({
    providers: [
        AuthentikProvider({
            clientId: process.env.AUTHENTIK_CLIENT_ID || '',
            clientSecret: process.env.AUTHENTIK_CLIENT_SECRET || '',
            issuer: process.env.AUTHENTIK_ISSUER,
        }),
    ],
    pages: {
        signIn: '/auth/login',
        error: '/auth/error',
    },
    callbacks: {
        async jwt({ token, account }) {
            // Pass the access token through to the token object
            if (account) {
                token.accessToken = account.access_token;
            }
            return token;
        },
        async session({ session, token }) {
            // Pass the access token through to the session object
            (session as any).accessToken = token.accessToken;
            return session;
        },
    },
});

export { handler as GET, handler as POST };

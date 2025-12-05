import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';
import GitHubProvider from 'next-auth/providers/github';

const handler = NextAuth({
    providers: [
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID || '',
            clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
        }),
        GitHubProvider({
            clientId: process.env.GITHUB_CLIENT_ID || '',
            clientSecret: process.env.GITHUB_CLIENT_SECRET || '',
        }),
    ],
    pages: {
        signIn: '/portal/login',
        error: '/portal/login', // Error code passed in query string as ?error=
    },
    callbacks: {
        async signIn({ user, account, profile }) {
            if (!user.email) return false;

            try {
                // Exchange OAuth profile for Platform JWT
                const response = await fetch(`${process.env.AUTH_SERVICE_URL || 'http://localhost:8007'}/auth/token/exchange`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: user.email,
                        provider: account?.provider,
                        secret: process.env.NEXTAUTH_SECRET,
                        name: user.name,
                        avatar_url: user.image,
                        platform: 'bizoholic'
                    }),
                });

                if (!response.ok) {
                    console.error('Token exchange failed:', await response.text());
                    return false;
                }

                const data = await response.json();
                // Attach platform token to user object for passing to jwt callback
                (user as any).accessToken = data.access_token;
                (user as any).refreshToken = data.refresh_token;
                (user as any).tenant = data.tenant;
                (user as any).role = data.user?.role;

                return true;
            } catch (error) {
                console.error('SignIn error:', error);
                return false;
            }
        },
        async jwt({ token, user }) {
            // Initial sign in
            if (user) {
                token.accessToken = (user as any).accessToken;
                token.refreshToken = (user as any).refreshToken;
                token.tenant = (user as any).tenant;
                token.role = (user as any).role;
            }
            return token;
        },
        async session({ session, token }) {
            (session as any).accessToken = token.accessToken;
            (session as any).tenant = token.tenant;
            (session as any).role = token.role;
            return session;
        },
    },
});

export { handler as GET, handler as POST };

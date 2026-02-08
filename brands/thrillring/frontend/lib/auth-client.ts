export const authClient = {
    async signIn(credentials: any) {
        console.warn("auth-client stub called");
        return { success: false, message: "Not implemented" };
    },
    async signOut() {
        return true;
    },
    async getSession() {
        return null;
    }
};

export default authClient;

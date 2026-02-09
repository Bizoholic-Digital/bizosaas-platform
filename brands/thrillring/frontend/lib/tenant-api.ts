export const DEFAULT_TENANT = { id: "default", name: "Default" };

export const tenantAPI = {
    async getTenant() {
        console.warn("tenant-api stub called");
        return { id: "1", name: "Default Tenant" };
    },
    async updateTenant(data: any) {
        return { success: true };
    }
};

export const tenantApi = tenantAPI;

export interface SyncJob {
    id: string;
    type: 'inventory' | 'price' | 'full';
    status: 'pending' | 'running' | 'completed' | 'failed';
    progress: number;
    startedAt: string;
    completedAt?: string;
    results?: {
        updated: number;
        failed: number;
        total: number;
    };
}

export interface InventoryAlert {
    id: string;
    type: string;
    priority: 'low' | 'medium' | 'high' | 'critical';
    title: string;
    message: string;
    createdAt: string;
}

class InventorySyncService {
    async startSync(type: 'inventory' | 'price' | 'full'): Promise<SyncJob> {
        return {
            id: `sync_${Date.now()}`,
            type,
            status: 'running',
            progress: 0,
            startedAt: new Date().toISOString()
        };
    }

    async getSyncStatus(jobId: string): Promise<SyncJob> {
        return {
            id: jobId,
            type: 'full',
            status: 'completed',
            progress: 100,
            startedAt: new Date().toISOString(),
            completedAt: new Date().toISOString(),
            results: { updated: 10, failed: 0, total: 10 }
        };
    }

    async getRecentAlerts(): Promise<InventoryAlert[]> {
        return [];
    }
}

export const inventorySync = new InventorySyncService();

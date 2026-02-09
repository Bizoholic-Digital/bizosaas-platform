export class ConversationalMemoryManager {
    async saveMessage(message: any) {
        console.warn("ConversationalMemoryManager stub called");
        return true;
    }

    async getHistory(limit: number = 10) {
        return [];
    }
}

export const conversationalMemoryManager = new ConversationalMemoryManager();

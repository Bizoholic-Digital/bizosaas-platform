export class AICommandProcessor {
    async processCommand(command: string) {
        console.warn("AICommandProcessor stub called");
        return { success: false, message: "Not implemented" };
    }
}

export const aiCommandProcessor = new AICommandProcessor();

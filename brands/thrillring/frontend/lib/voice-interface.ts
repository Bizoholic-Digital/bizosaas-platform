export class VoiceInterface {
    async startListening() {
        console.warn("VoiceInterface stub called");
        return false;
    }

    async stopListening() {
        return true;
    }
}

export const voiceInterface = new VoiceInterface();
export const VoiceInterfaceManager = voiceInterface;

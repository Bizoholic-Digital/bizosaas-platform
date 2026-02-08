export interface VoiceSettings {
    enabled: boolean;
    speechToText: {
        enabled: boolean;
        language: string;
        continuous: boolean;
        interimResults: boolean;
    };
    textToSpeech: {
        enabled: boolean;
        voice: string;
        rate: number;
        pitch: number;
        volume: number;
    };
    autoPlayResponses: boolean;
    voiceActivation: boolean;
    noiseReduction: boolean;
}

export interface VoiceState {
    isListening: boolean;
    isRecognizing: boolean;
    isSpeaking: boolean;
    hasPermission: boolean;
    error: string | null;
}

export interface VoiceRecognitionResult {
    transcript: string;
    confidence: number;
    isFinal: boolean;
}

export interface VoiceCallbacks {
    onStateChange?: (state: VoiceState) => void;
    onResult?: (result: VoiceRecognitionResult) => void;
    onError?: (error: string) => void;
}

export class VoiceInterfaceManager {
    private settings: VoiceSettings;
    private state: VoiceState = {
        isListening: false,
        isRecognizing: false,
        isSpeaking: false,
        hasPermission: false,
        error: null
    };
    private callbacks: VoiceCallbacks = {};
    private recognition: any = null;
    private synthesis: SpeechSynthesis | null = null;
    private currentUtterance: SpeechSynthesisUtterance | null = null;

    constructor(settings: VoiceSettings) {
        this.settings = settings;
        if (typeof window !== 'undefined') {
            this.synthesis = window.speechSynthesis;
            this.initializeRecognition();
        }
    }

    private initializeRecognition() {
        if (typeof window === 'undefined') return;

        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        if (SpeechRecognition) {
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = this.settings.speechToText.continuous;
            this.recognition.interimResults = this.settings.speechToText.interimResults;
            this.recognition.lang = this.settings.speechToText.language;

            this.recognition.onstart = () => {
                this.updateState({ isListening: true, isRecognizing: true });
            };

            this.recognition.onresult = (event: any) => {
                const result = event.results[event.results.length - 1];
                const transcript = result[0].transcript;
                const confidence = result[0].confidence;
                const isFinal = result.isFinal;

                if (this.callbacks.onResult) {
                    this.callbacks.onResult({ transcript, confidence, isFinal });
                }
            };

            this.recognition.onerror = (event: any) => {
                const error = `Recognition error: ${event.error}`;
                this.updateState({ error, isListening: false, isRecognizing: false });
                if (this.callbacks.onError) this.callbacks.onError(error);
            };

            this.recognition.onend = () => {
                this.updateState({ isListening: false, isRecognizing: false });
            };
        }
    }

    setCallbacks(callbacks: VoiceCallbacks) {
        this.callbacks = callbacks;
    }

    updateSettings(settings: VoiceSettings) {
        this.settings = settings;
        if (this.recognition) {
            this.recognition.continuous = settings.speechToText.continuous;
            this.recognition.interimResults = settings.speechToText.interimResults;
            this.recognition.lang = settings.speechToText.language;
        }
    }

    async requestPermission(): Promise<boolean> {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            stream.getTracks().forEach(track => track.stop());
            this.updateState({ hasPermission: true });
            return true;
        } catch (error) {
            this.updateState({ hasPermission: false, error: 'Microphone permission denied' });
            return false;
        }
    }

    async startListening() {
        if (!this.recognition) return;
        try {
            this.recognition.start();
        } catch (error) {
            console.warn('Recognition already started or failed to start', error);
        }
    }

    stopListening() {
        if (this.recognition) {
            this.recognition.stop();
        }
    }

    async speakText(text: string): Promise<void> {
        if (!this.synthesis || !this.settings.textToSpeech.enabled) return;

        this.stopSpeaking();

        return new Promise((resolve) => {
            this.currentUtterance = new SpeechSynthesisUtterance(text);

            const voices = this.synthesis!.getVoices();
            const selectedVoice = voices.find(v => v.name === this.settings.textToSpeech.voice);
            if (selectedVoice) this.currentUtterance.voice = selectedVoice;

            this.currentUtterance.rate = this.settings.textToSpeech.rate;
            this.currentUtterance.pitch = this.settings.textToSpeech.pitch;
            this.currentUtterance.volume = this.settings.textToSpeech.volume;

            this.currentUtterance.onstart = () => {
                this.updateState({ isSpeaking: true });
            };

            this.currentUtterance.onend = () => {
                this.updateState({ isSpeaking: false });
                this.currentUtterance = null;
                resolve();
            };

            this.currentUtterance.onerror = (event) => {
                console.error('Speech synthesis error', event);
                this.updateState({ isSpeaking: false, error: 'Speech synthesis failed' });
                this.currentUtterance = null;
                resolve();
            };

            this.synthesis!.speak(this.currentUtterance);
        });
    }

    stopSpeaking() {
        if (this.synthesis) {
            this.synthesis.cancel();
            this.updateState({ isSpeaking: false });
        }
    }

    getAvailableVoices(): SpeechSynthesisVoice[] {
        if (!this.synthesis) return [];
        return this.synthesis.getVoices();
    }

    isSupported() {
        return {
            speechToText: !!((window as any).SpeechRecognition || (window as any).webkitSpeechRecognition),
            textToSpeech: !!(typeof window !== 'undefined' && window.speechSynthesis)
        };
    }

    destroy() {
        this.stopListening();
        this.stopSpeaking();
    }

    private updateState(newState: Partial<VoiceState>) {
        this.state = { ...this.state, ...newState };
        if (this.callbacks.onStateChange) {
            this.callbacks.onStateChange(this.state);
        }
    }
}

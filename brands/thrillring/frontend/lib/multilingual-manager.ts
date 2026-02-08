export class MultilingualManager {
    async translate(text: string, targetLang: string) {
        console.warn("MultilingualManager stub called");
        return text;
    }

    async detectLanguage(text: string) {
        return "en";
    }
}

export const multilingualManager = new MultilingualManager();

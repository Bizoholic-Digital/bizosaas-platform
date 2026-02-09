export interface Language {
    code: string;
    name: string;
    nativeName: string;
    direction: 'ltr' | 'rtl';
    flag: string;
    enabled: boolean;
    translationProgress: number;
    lastUpdated: string;
}

export interface MultilingualSettings {
    enabled: boolean;
    defaultLanguage: string;
    availableLanguages: Language[];
    autoDetect: boolean;
}

export class MultilingualManager {
    private apiUrl: string;
    private tenantId: string;
    private userId: string | null = null;
    private currentLanguage: string = 'en';
    private settings: MultilingualSettings = {
        enabled: true,
        defaultLanguage: 'en',
        availableLanguages: [
            { code: 'en', name: 'English', nativeName: 'English', direction: 'ltr', flag: '🇺🇸', enabled: true, translationProgress: 100, lastUpdated: new Date().toISOString() },
            { code: 'es', name: 'Spanish', nativeName: 'Español', direction: 'ltr', flag: '🇪🇸', enabled: true, translationProgress: 85, lastUpdated: new Date().toISOString() },
            { code: 'fr', name: 'French', nativeName: 'Français', direction: 'ltr', flag: '🇫🇷', enabled: true, translationProgress: 70, lastUpdated: new Date().toISOString() },
            { code: 'ar', name: 'Arabic', nativeName: 'العربية', direction: 'rtl', flag: '🇸🇦', enabled: true, translationProgress: 50, lastUpdated: new Date().toISOString() }
        ],
        autoDetect: true
    };

    constructor(apiUrl: string, tenantId: string) {
        this.apiUrl = apiUrl;
        this.tenantId = tenantId;
    }

    async initialize(tenantId: string, userId: string, role: string) {
        this.tenantId = tenantId;
        this.userId = userId;

        try {
            const response = await fetch(`${this.apiUrl}/api/multilingual/settings?tenant_id=${tenantId}`);
            if (response.ok) {
                const data = await response.json();
                this.settings = { ...this.settings, ...data };
                this.currentLanguage = this.settings.defaultLanguage;
            }
        } catch (error) {
            console.warn('Failed to fetch multilingual settings, using defaults');
        }
    }

    getCurrentLanguage(): string {
        return this.currentLanguage;
    }

    getAvailableLanguages(): Language[] {
        return this.settings.availableLanguages;
    }

    getSettings(): MultilingualSettings {
        return this.settings;
    }

    async changeLanguage(code: string): Promise<boolean> {
        this.currentLanguage = code;
        // Logic to update UI language, possibly via storage or API
        return true;
    }
}

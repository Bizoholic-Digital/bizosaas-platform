/**
 * i18n Configuration for BizOSaaS Client Portal
 * 
 * Supported locales:
 * - en: English (default)
 * - es: Spanish (LATAM expansion)
 * - pt-BR: Portuguese Brazil (LGPD market)
 * 
 * More locales can be added by:
 * 1. Creating a new messages/[locale].json file
 * 2. Adding the locale to the 'locales' array below
 */

export const locales = ['en', 'es', 'pt-BR'] as const;
export type Locale = (typeof locales)[number];

export const defaultLocale: Locale = 'en';

export const localeNames: Record<Locale, string> = {
    'en': 'English',
    'es': 'Español',
    'pt-BR': 'Português (BR)',
};

export const localeFlags: Record<Locale, string> = {
    'en': '🇺🇸',
    'es': '🇲🇽',
    'pt-BR': '🇧🇷',
};

/**
 * Get messages for a locale
 * Using static imports for TypeScript compatibility
 */
export async function getMessages(locale: Locale): Promise<Record<string, unknown>> {
    switch (locale) {
        case 'es':
            return (await import('@/messages/es.json')).default;
        case 'pt-BR':
            return (await import('@/messages/pt-BR.json')).default;
        case 'en':
        default:
            return (await import('@/messages/en.json')).default;
    }
}


/**
 * Detect user's preferred locale from browser or cookie
 */
export function detectLocale(acceptLanguage?: string): Locale {
    if (!acceptLanguage) return defaultLocale;

    // Parse Accept-Language header
    const languages = acceptLanguage
        .split(',')
        .map(lang => lang.split(';')[0].trim().toLowerCase());

    // Find first matching locale
    for (const lang of languages) {
        // Exact match
        if (locales.includes(lang as Locale)) {
            return lang as Locale;
        }
        // Partial match (e.g., 'pt' matches 'pt-BR')
        const partial = locales.find(l => l.toLowerCase().startsWith(lang));
        if (partial) {
            return partial;
        }
    }

    return defaultLocale;
}

/**
 * Currency formatting by locale
 */
export const localeCurrencies: Record<Locale, string> = {
    'en': 'USD',
    'es': 'USD', // Most LATAM uses USD for SaaS
    'pt-BR': 'BRL',
};

/**
 * Date formatting options by locale
 */
export const localeDateFormats: Record<Locale, Intl.DateTimeFormatOptions> = {
    'en': { month: 'short', day: 'numeric', year: 'numeric' },
    'es': { day: 'numeric', month: 'short', year: 'numeric' },
    'pt-BR': { day: 'numeric', month: 'short', year: 'numeric' },
};

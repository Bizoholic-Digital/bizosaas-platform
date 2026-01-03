'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Locale, defaultLocale, locales, getMessages } from './config';

type Messages = Record<string, any>;

interface I18nContextType {
    locale: Locale;
    messages: Messages;
    setLocale: (locale: Locale) => void;
    t: (key: string, params?: Record<string, string | number>) => string;
    isLoading: boolean;
}

const I18nContext = createContext<I18nContextType | undefined>(undefined);

const LOCALE_STORAGE_KEY = 'bizosaas-locale';

/**
 * Get nested value from object using dot notation
 */
function getNestedValue(obj: Record<string, any>, path: string): string | undefined {
    return path.split('.').reduce((acc, part) => acc?.[part], obj);
}

/**
 * Replace template variables in string
 */
function interpolate(str: string, params?: Record<string, string | number>): string {
    if (!params) return str;
    return str.replace(/{(\w+)}/g, (_, key) => String(params[key] ?? `{${key}}`));
}

interface I18nProviderProps {
    children: ReactNode;
    initialLocale?: Locale;
    initialMessages?: Messages;
}

export function I18nProvider({
    children,
    initialLocale = defaultLocale,
    initialMessages = {}
}: I18nProviderProps) {
    const [locale, setLocaleState] = useState<Locale>(initialLocale);
    const [messages, setMessages] = useState<Messages>(initialMessages);
    const [isLoading, setIsLoading] = useState(!initialMessages || Object.keys(initialMessages).length === 0);

    // Load messages when locale changes
    useEffect(() => {
        async function loadMessages() {
            setIsLoading(true);
            try {
                const msgs = await getMessages(locale);
                setMessages(msgs);
            } catch (error) {
                console.error('Failed to load messages:', error);
            } finally {
                setIsLoading(false);
            }
        }

        // Only load if we don't have initial messages or locale changed
        if (!initialMessages || locale !== initialLocale) {
            loadMessages();
        }
    }, [locale, initialLocale, initialMessages]);

    // Persist locale preference
    useEffect(() => {
        if (typeof window !== 'undefined') {
            localStorage.setItem(LOCALE_STORAGE_KEY, locale);
        }
    }, [locale]);

    // Load saved locale on mount
    useEffect(() => {
        if (typeof window !== 'undefined') {
            const saved = localStorage.getItem(LOCALE_STORAGE_KEY) as Locale | null;
            if (saved && locales.includes(saved)) {
                setLocaleState(saved);
            }
        }
    }, []);

    const setLocale = (newLocale: Locale) => {
        if (locales.includes(newLocale)) {
            setLocaleState(newLocale);
        }
    };

    /**
     * Translation function
     * Usage: t('nav.dashboard') or t('onboarding.step', { current: 1, total: 10 })
     */
    const t = (key: string, params?: Record<string, string | number>): string => {
        const value = getNestedValue(messages, key);
        if (value === undefined) {
            console.warn(`Missing translation: ${key}`);
            return key;
        }
        return interpolate(value, params);
    };

    return (
        <I18nContext.Provider value={{ locale, messages, setLocale, t, isLoading }}>
            {children}
        </I18nContext.Provider>
    );
}

/**
 * Hook to access i18n context
 */
export function useI18n() {
    const context = useContext(I18nContext);
    if (!context) {
        throw new Error('useI18n must be used within an I18nProvider');
    }
    return context;
}

/**
 * Hook for translation function only
 */
export function useTranslation() {
    const { t, locale, isLoading } = useI18n();
    return { t, locale, isLoading };
}

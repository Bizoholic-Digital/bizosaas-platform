'use client';

import React from 'react';
import { Globe } from 'lucide-react';
import { useI18n } from '@/lib/i18n/provider';
import { locales, localeNames, localeFlags, Locale } from '@/lib/i18n/config';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';

interface LanguageSwitcherProps {
    variant?: 'default' | 'minimal' | 'full';
    className?: string;
}

export function LanguageSwitcher({ variant = 'default', className = '' }: LanguageSwitcherProps) {
    const { locale, setLocale, isLoading } = useI18n();

    const handleLocaleChange = (newLocale: Locale) => {
        setLocale(newLocale);
    };

    if (variant === 'minimal') {
        return (
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon" className={className} disabled={isLoading}>
                        <Globe className="h-4 w-4" />
                        <span className="sr-only">Change language</span>
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                    {locales.map((loc) => (
                        <DropdownMenuItem
                            key={loc}
                            onClick={() => handleLocaleChange(loc)}
                            className={locale === loc ? 'bg-accent' : ''}
                        >
                            <span className="mr-2">{localeFlags[loc]}</span>
                            {localeNames[loc]}
                        </DropdownMenuItem>
                    ))}
                </DropdownMenuContent>
            </DropdownMenu>
        );
    }

    if (variant === 'full') {
        return (
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <Button variant="outline" className={className} disabled={isLoading}>
                        <Globe className="mr-2 h-4 w-4" />
                        <span className="mr-2">{localeFlags[locale]}</span>
                        {localeNames[locale]}
                    </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                    {locales.map((loc) => (
                        <DropdownMenuItem
                            key={loc}
                            onClick={() => handleLocaleChange(loc)}
                            className={locale === loc ? 'bg-accent' : ''}
                        >
                            <span className="mr-2">{localeFlags[loc]}</span>
                            {localeNames[loc]}
                        </DropdownMenuItem>
                    ))}
                </DropdownMenuContent>
            </DropdownMenu>
        );
    }

    // Default variant
    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="sm" className={className} disabled={isLoading}>
                    <Globe className="mr-1 h-4 w-4" />
                    <span>{localeFlags[locale]}</span>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                {locales.map((loc) => (
                    <DropdownMenuItem
                        key={loc}
                        onClick={() => handleLocaleChange(loc)}
                        className={locale === loc ? 'bg-accent' : ''}
                    >
                        <span className="mr-2">{localeFlags[loc]}</span>
                        {localeNames[loc]}
                    </DropdownMenuItem>
                ))}
            </DropdownMenuContent>
        </DropdownMenu>
    );
}

export default LanguageSwitcher;

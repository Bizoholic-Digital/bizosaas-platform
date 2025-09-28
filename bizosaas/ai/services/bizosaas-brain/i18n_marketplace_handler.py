#!/usr/bin/env python3
"""
Internationalization and Marketplace Handler for BizOSaaS Brain API
Provides comprehensive i18n support with marketplace detection, currency conversion,
and locale-specific formatting for global e-commerce operations.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import babel
from babel import dates, numbers, core
from babel.numbers import format_currency
from babel.dates import format_datetime
import requests
from functools import lru_cache

logger = logging.getLogger(__name__)

class MarketplaceRegion(str, Enum):
    """Marketplace regions with their primary locales"""
    INDIA = "IN"
    US = "US" 
    UK = "UK"
    GERMANY = "DE"
    FRANCE = "FR"
    JAPAN = "JP"
    AUSTRALIA = "AU"
    CANADA = "CA"

class CurrencyCode(str, Enum):
    """ISO 4217 Currency codes for supported marketplaces"""
    INR = "INR"  # Indian Rupee
    USD = "USD"  # US Dollar
    GBP = "GBP"  # British Pound
    EUR = "EUR"  # Euro
    JPY = "JPY"  # Japanese Yen
    AUD = "AUD"  # Australian Dollar
    CAD = "CAD"  # Canadian Dollar

@dataclass
class MarketplaceConfig:
    """Configuration for each marketplace"""
    region: str
    currency: str
    locale: str
    language: str
    timezone: str
    tax_rate: float
    shipping_regions: List[str]
    payment_methods: List[str]
    amazon_marketplace_id: str

@dataclass
class LocalizedProduct:
    """Localized product data structure"""
    id: str
    name: str
    description: str
    price: Dict[str, Any]
    currency: str
    locale: str
    formatted_price: str
    tax_inclusive: bool
    shipping_info: Dict[str, Any]
    availability: Dict[str, Any]

class I18nMarketplaceHandler:
    """
    Comprehensive internationalization handler for multi-marketplace operations
    Handles currency conversion, locale detection, and marketplace-specific formatting
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.I18nMarketplaceHandler")
        
        # Load marketplace configurations
        self.marketplace_configs = self._load_marketplace_configs()
        
        # Exchange rate cache (in production, use Redis/external service)
        self.exchange_rates = {}
        self.rate_cache_time = None
        
        # Locale mappings
        self.locale_mappings = self._load_locale_mappings()
        
        # Load translations
        self.translations = self._load_translations()
        
    def _load_marketplace_configs(self) -> Dict[str, MarketplaceConfig]:
        """Load marketplace-specific configurations"""
        return {
            MarketplaceRegion.INDIA: MarketplaceConfig(
                region="IN",
                currency="INR",
                locale="hi_IN",  # Hindi (India)
                language="hi",
                timezone="Asia/Kolkata",
                tax_rate=18.0,  # GST
                shipping_regions=["North India", "South India", "West India", "East India"],
                payment_methods=["UPI", "Credit Card", "Debit Card", "Net Banking", "COD"],
                amazon_marketplace_id="A21TJRUUN4KGV"
            ),
            MarketplaceRegion.US: MarketplaceConfig(
                region="US",
                currency="USD",
                locale="en_US",
                language="en",
                timezone="America/New_York",
                tax_rate=8.5,
                shipping_regions=["Northeast", "Southeast", "Midwest", "Southwest", "West Coast"],
                payment_methods=["Credit Card", "Debit Card", "PayPal", "Apple Pay", "Google Pay"],
                amazon_marketplace_id="ATVPDKIKX0DER"
            ),
            MarketplaceRegion.UK: MarketplaceConfig(
                region="UK",
                currency="GBP",
                locale="en_GB",
                language="en",
                timezone="Europe/London",
                tax_rate=20.0,  # VAT
                shipping_regions=["England", "Scotland", "Wales", "Northern Ireland"],
                payment_methods=["Credit Card", "Debit Card", "PayPal", "Apple Pay"],
                amazon_marketplace_id="A1F83G8C2ARO7P"
            ),
            MarketplaceRegion.GERMANY: MarketplaceConfig(
                region="DE",
                currency="EUR",
                locale="de_DE",
                language="de",
                timezone="Europe/Berlin",
                tax_rate=19.0,  # VAT
                shipping_regions=["North Germany", "South Germany", "East Germany", "West Germany"],
                payment_methods=["Credit Card", "Debit Card", "SEPA", "PayPal"],
                amazon_marketplace_id="A1PA6795UKMFR9"
            ),
            MarketplaceRegion.JAPAN: MarketplaceConfig(
                region="JP",
                currency="JPY",
                locale="ja_JP",
                language="ja",
                timezone="Asia/Tokyo",
                tax_rate=10.0,  # Consumption Tax
                shipping_regions=["Kanto", "Kansai", "Kyushu", "Tohoku"],
                payment_methods=["Credit Card", "Convenience Store", "Bank Transfer"],
                amazon_marketplace_id="A1VC38T7YXB528"
            )
        }
    
    def _load_locale_mappings(self) -> Dict[str, Dict[str, str]]:
        """Load locale-specific mappings for formatting"""
        return {
            "hi_IN": {
                "date_format": "dd/MM/yyyy",
                "time_format": "HH:mm",
                "number_format": "##,##,###.##",  # Indian numbering system
                "currency_symbol": "₹"
            },
            "en_US": {
                "date_format": "MM/dd/yyyy",
                "time_format": "h:mm a",
                "number_format": "###,###.##",
                "currency_symbol": "$"
            },
            "en_GB": {
                "date_format": "dd/MM/yyyy",
                "time_format": "HH:mm",
                "number_format": "###,###.##",
                "currency_symbol": "£"
            },
            "de_DE": {
                "date_format": "dd.MM.yyyy",
                "time_format": "HH:mm",
                "number_format": "###.###,##",
                "currency_symbol": "€"
            },
            "ja_JP": {
                "date_format": "yyyy年MM月dd日",
                "time_format": "HH:mm",
                "number_format": "###,###",
                "currency_symbol": "¥"
            }
        }
    
    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load translation strings for supported languages"""
        return {
            "en": {
                "add_to_cart": "Add to Cart",
                "buy_now": "Buy Now",
                "out_of_stock": "Out of Stock",
                "free_shipping": "Free Shipping",
                "tax_inclusive": "Tax Inclusive",
                "tax_exclusive": "Tax Exclusive"
            },
            "hi": {
                "add_to_cart": "कार्ट में जोड़ें",
                "buy_now": "अभी खरीदें",
                "out_of_stock": "स्टॉक में नहीं",
                "free_shipping": "मुफ्त शिपिंग",
                "tax_inclusive": "कर सहित",
                "tax_exclusive": "कर रहित"
            },
            "de": {
                "add_to_cart": "In den Warenkorb",
                "buy_now": "Jetzt kaufen",
                "out_of_stock": "Nicht auf Lager",
                "free_shipping": "Kostenloser Versand",
                "tax_inclusive": "Inkl. Steuern",
                "tax_exclusive": "Exkl. Steuern"
            },
            "ja": {
                "add_to_cart": "カートに追加",
                "buy_now": "今すぐ購入",
                "out_of_stock": "在庫切れ",
                "free_shipping": "送料無料",
                "tax_inclusive": "税込み",
                "tax_exclusive": "税抜き"
            }
        }
    
    def detect_marketplace_from_request(self, accept_language: str = None, 
                                      user_country: str = None,
                                      currency_preference: str = None) -> MarketplaceConfig:
        """
        Detect the appropriate marketplace based on request headers and preferences
        """
        # Priority: explicit currency preference > country detection > language header
        
        if currency_preference:
            for config in self.marketplace_configs.values():
                if config.currency == currency_preference:
                    return config
        
        if user_country:
            if user_country in self.marketplace_configs:
                return self.marketplace_configs[user_country]
        
        if accept_language:
            # Parse Accept-Language header
            languages = self._parse_accept_language(accept_language)
            for lang, _ in languages:
                if lang.startswith('hi'):
                    return self.marketplace_configs[MarketplaceRegion.INDIA]
                elif lang.startswith('en'):
                    if 'GB' in lang:
                        return self.marketplace_configs[MarketplaceRegion.UK]
                    else:
                        return self.marketplace_configs[MarketplaceRegion.US]
                elif lang.startswith('de'):
                    return self.marketplace_configs[MarketplaceRegion.GERMANY]
                elif lang.startswith('ja'):
                    return self.marketplace_configs[MarketplaceRegion.JAPAN]
        
        # Default to India (our primary focus)
        return self.marketplace_configs[MarketplaceRegion.INDIA]
    
    def _parse_accept_language(self, accept_language: str) -> List[Tuple[str, float]]:
        """Parse Accept-Language header and return sorted list by preference"""
        languages = []
        for item in accept_language.split(','):
            parts = item.strip().split(';')
            lang = parts[0].strip()
            quality = 1.0
            if len(parts) > 1 and parts[1].strip().startswith('q='):
                try:
                    quality = float(parts[1].strip()[2:])
                except ValueError:
                    pass
            languages.append((lang, quality))
        
        return sorted(languages, key=lambda x: x[1], reverse=True)
    
    @lru_cache(maxsize=100)
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Get exchange rate between currencies
        In production, integrate with a real exchange rate API
        """
        if from_currency == to_currency:
            return 1.0
        
        # Mock exchange rates (replace with real API in production)
        mock_rates = {
            ("USD", "INR"): 83.25,
            ("USD", "GBP"): 0.79,
            ("USD", "EUR"): 0.92,
            ("USD", "JPY"): 149.50,
            ("INR", "USD"): 0.012,
            ("GBP", "USD"): 1.27,
            ("EUR", "USD"): 1.09,
            ("JPY", "USD"): 0.0067
        }
        
        return mock_rates.get((from_currency, to_currency), 1.0)
    
    def convert_price(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert price between currencies"""
        if from_currency == to_currency:
            return amount
        
        rate = self.get_exchange_rate(from_currency, to_currency)
        return round(amount * rate, 2)
    
    def format_price(self, amount: float, currency: str, locale: str) -> str:
        """Format price according to locale conventions"""
        try:
            # Handle special cases for Indian numbering system
            if locale == "hi_IN" and currency == "INR":
                # Indian numbering system (lakhs, crores)
                if amount >= 10000000:  # 1 crore
                    crores = amount / 10000000
                    return f"₹{crores:.2f} Cr"
                elif amount >= 100000:  # 1 lakh
                    lakhs = amount / 100000
                    return f"₹{lakhs:.2f} L"
                else:
                    return f"₹{amount:,.2f}"
            
            # Use Babel for standard formatting
            babel_locale = babel.core.Locale.parse(locale) if '_' in locale else babel.core.Locale.parse(locale + '_' + locale.upper())
            return format_currency(amount, currency, locale=babel_locale)
        
        except Exception as e:
            self.logger.warning(f"Error formatting price: {e}, falling back to basic format")
            symbol = self.locale_mappings.get(locale, {}).get("currency_symbol", currency)
            return f"{symbol}{amount:,.2f}"
    
    def localize_product(self, product_data: Dict[str, Any], 
                        marketplace_config: MarketplaceConfig) -> LocalizedProduct:
        """
        Localize product data for specific marketplace
        """
        # Convert price if needed
        original_price = product_data.get("price", {}).get("amount", 0)
        original_currency = product_data.get("price", {}).get("currency", "USD")
        
        localized_price = self.convert_price(
            original_price, 
            original_currency, 
            marketplace_config.currency
        )
        
        # Format price
        formatted_price = self.format_price(
            localized_price,
            marketplace_config.currency,
            marketplace_config.locale
        )
        
        # Calculate tax-inclusive price
        tax_inclusive_price = localized_price * (1 + marketplace_config.tax_rate / 100)
        formatted_tax_inclusive = self.format_price(
            tax_inclusive_price,
            marketplace_config.currency,
            marketplace_config.locale
        )
        
        # Localize shipping information
        shipping_info = {
            "regions": marketplace_config.shipping_regions,
            "free_shipping_threshold": self.convert_price(500, "USD", marketplace_config.currency),
            "estimated_delivery": "2-5 business days"
        }
        
        return LocalizedProduct(
            id=product_data.get("id"),
            name=product_data.get("name"),
            description=product_data.get("description"),
            price={
                "amount": localized_price,
                "tax_inclusive_amount": tax_inclusive_price,
                "currency": marketplace_config.currency,
                "original_amount": original_price,
                "original_currency": original_currency
            },
            currency=marketplace_config.currency,
            locale=marketplace_config.locale,
            formatted_price=formatted_price,
            tax_inclusive=True,
            shipping_info=shipping_info,
            availability={
                "in_stock": product_data.get("inventory", {}).get("available", True),
                "quantity": product_data.get("inventory", {}).get("quantity", 0),
                "marketplace": marketplace_config.region
            }
        )
    
    def get_localized_strings(self, language: str) -> Dict[str, str]:
        """Get translated strings for a specific language"""
        return self.translations.get(language, self.translations["en"])
    
    def format_date(self, date_obj: datetime, locale: str) -> str:
        """Format date according to locale conventions"""
        try:
            babel_locale = babel.core.Locale.parse(locale) if '_' in locale else babel.core.Locale.parse(locale + '_' + locale.upper())
            return format_datetime(date_obj, locale=babel_locale)
        except Exception as e:
            self.logger.warning(f"Error formatting date: {e}, falling back to ISO format")
            return date_obj.isoformat()

# Global instance
i18n_handler = I18nMarketplaceHandler()
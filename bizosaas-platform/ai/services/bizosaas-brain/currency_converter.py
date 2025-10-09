#!/usr/bin/env python3
"""
Real-time Currency Conversion Service for BizOSaaS Brain API
Provides accurate currency conversion with live exchange rates and fallback support.
"""

import logging
import requests
from typing import Dict, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class CurrencyConverter:
    """
    Advanced currency converter with multiple data sources and caching
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.CurrencyConverter")
        
        # Exchange rate cache with timestamp
        self.exchange_rates = {}
        self.cache_timestamp = None
        self.cache_duration = timedelta(hours=1)  # Cache for 1 hour
        
        # Fallback exchange rates (updated as of 2024)
        self.fallback_rates = {
            # Base: USD = 1.00
            "USD": 1.00,
            "INR": 83.25,   # 1 USD = 83.25 INR
            "GBP": 0.79,    # 1 USD = 0.79 GBP  
            "EUR": 0.92,    # 1 USD = 0.92 EUR
            "JPY": 149.50,  # 1 USD = 149.50 JPY
            "AUD": 1.52,    # 1 USD = 1.52 AUD
            "CAD": 1.36,    # 1 USD = 1.36 CAD
        }
        
        # API endpoints for live rates (in order of preference)
        self.rate_apis = [
            "https://api.exchangerate-api.com/v4/latest/USD",
            "https://api.fixer.io/latest?base=USD",
            "https://api.currencylayer.com/live?access_key=YOUR_KEY&source=USD"
        ]
    
    def _fetch_live_rates(self) -> Optional[Dict[str, float]]:
        """
        Fetch live exchange rates from external APIs
        """
        for api_url in self.rate_apis:
            try:
                response = requests.get(api_url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Handle different API response formats
                    if 'rates' in data:
                        rates = data['rates']
                        rates['USD'] = 1.0  # Ensure USD base is always 1.0
                        self.logger.info(f"✅ Live exchange rates fetched from {api_url}")
                        return rates
                        
            except Exception as e:
                self.logger.warning(f"Failed to fetch from {api_url}: {str(e)}")
                continue
        
        return None
    
    def _update_rates_if_needed(self) -> None:
        """
        Update exchange rates if cache is stale
        """
        now = datetime.now()
        
        # Check if cache needs updating
        if (self.cache_timestamp is None or 
            now - self.cache_timestamp > self.cache_duration or
            not self.exchange_rates):
            
            self.logger.info("Updating currency exchange rates...")
            
            # Try to fetch live rates
            live_rates = self._fetch_live_rates()
            
            if live_rates:
                self.exchange_rates = live_rates
                self.cache_timestamp = now
                self.logger.info(f"✅ Exchange rates updated with live data")
            else:
                # Fall back to static rates
                self.exchange_rates = self.fallback_rates.copy()
                self.cache_timestamp = now
                self.logger.warning("⚠️ Using fallback exchange rates (live rates unavailable)")
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert amount from one currency to another
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code (e.g., 'INR')
            to_currency: Target currency code (e.g., 'USD')
            
        Returns:
            Converted amount rounded to 2 decimal places
        """
        if from_currency == to_currency:
            return round(amount, 2)
        
        # Update rates if needed
        self._update_rates_if_needed()
        
        # Get exchange rates
        from_rate = self.exchange_rates.get(from_currency, 1.0)
        to_rate = self.exchange_rates.get(to_currency, 1.0)
        
        if from_currency not in self.exchange_rates:
            self.logger.warning(f"Currency {from_currency} not supported, using 1.0")
            from_rate = 1.0
            
        if to_currency not in self.exchange_rates:
            self.logger.warning(f"Currency {to_currency} not supported, using 1.0")
            to_rate = 1.0
        
        # Convert: amount_in_from_currency -> USD -> amount_in_to_currency
        amount_in_usd = amount / from_rate
        converted_amount = amount_in_usd * to_rate
        
        self.logger.debug(f"Converted {amount} {from_currency} -> {converted_amount:.2f} {to_currency}")
        
        return round(converted_amount, 2)
    
    def get_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Get the exchange rate between two currencies
        
        Returns:
            Exchange rate (how many units of to_currency = 1 unit of from_currency)
        """
        if from_currency == to_currency:
            return 1.0
            
        # Update rates if needed  
        self._update_rates_if_needed()
        
        from_rate = self.exchange_rates.get(from_currency, 1.0)
        to_rate = self.exchange_rates.get(to_currency, 1.0)
        
        # Calculate rate: 1 from_currency = ? to_currency
        rate = to_rate / from_rate
        return round(rate, 4)
    
    def get_all_rates(self) -> Dict[str, float]:
        """
        Get all current exchange rates
        """
        self._update_rates_if_needed()
        return self.exchange_rates.copy()
    
    def format_price(self, amount: float, currency: str) -> str:
        """
        Format price with appropriate currency symbol and locale formatting
        """
        currency_symbols = {
            "USD": "$",
            "INR": "₹", 
            "GBP": "£",
            "EUR": "€",
            "JPY": "¥",
            "AUD": "A$",
            "CAD": "C$"
        }
        
        symbol = currency_symbols.get(currency, currency)
        
        # Special formatting for different currencies
        if currency == "JPY":
            # Japanese Yen doesn't use decimal places
            return f"{symbol}{amount:,.0f}"
        elif currency == "INR":
            # Indian numbering system formatting
            if amount >= 10000000:  # 1 crore
                crores = amount / 10000000
                return f"{symbol}{crores:.2f} Cr"
            elif amount >= 100000:  # 1 lakh  
                lakhs = amount / 100000
                return f"{symbol}{lakhs:.2f} L"
            else:
                return f"{symbol}{amount:,.2f}"
        else:
            # Standard formatting for most currencies
            return f"{symbol}{amount:,.2f}"

# Global currency converter instance
currency_converter = CurrencyConverter()

# Convenience functions
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert currency amount"""
    return currency_converter.convert(amount, from_currency, to_currency)

def format_currency(amount: float, currency: str) -> str:
    """Format currency with proper symbols"""
    return currency_converter.format_price(amount, currency)

def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """Get exchange rate between currencies"""
    return currency_converter.get_rate(from_currency, to_currency)
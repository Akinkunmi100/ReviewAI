"""
Currency formatting and conversion utilities.
"""

import re
import requests
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, Tuple

from core.config import Constants


class CurrencyFormatter:
    """Handles Nigerian Naira formatting and currency conversion"""
    
    def __init__(self, cache_manager=None):
        self.cache = cache_manager
        self._rates: Dict[str, float] = {}
        self._rates_timestamp: Optional[datetime] = None
    
    @staticmethod
    def format_naira(amount: float, show_symbol: bool = True) -> str:
        """Format amount as Nigerian Naira"""
        if amount is None:
            return "Price unavailable"
        
        formatted = f"{amount:,.0f}"
        
        if show_symbol:
            return f"₦{formatted}"
        return formatted
    
    @staticmethod
    def parse_naira(price_string: str) -> Optional[float]:
        """Parse Naira price string to float"""
        if not price_string:
            return None
        
        try:
            cleaned = price_string.replace('₦', '').replace('NGN', '')
            cleaned = cleaned.replace(',', '').replace(' ', '').strip()
            
            if '-' in cleaned:
                cleaned = cleaned.split('-')[0]
            
            match = re.search(r'[\d.]+', cleaned)
            if match:
                return float(match.group())
            return None
        except:
            return None
    
    def _get_usd_rates(self) -> Dict[str, float]:
        """Fetch and cache FX rates with USD as base."""
        if self._rates and self._rates_timestamp:
            if datetime.now(timezone.utc) - self._rates_timestamp < timedelta(hours=1):
                return self._rates

        try:
            response = requests.get(
                "https://api.exchangerate-api.com/v4/latest/USD",
                timeout=5
            )
            if response.ok:
                data = response.json()
                rates = data.get('rates', {}) or {}
                if 'NGN' not in rates:
                    rates['NGN'] = Constants.USD_TO_NGN_FALLBACK
                self._rates = rates
                self._rates_timestamp = datetime.now(timezone.utc)
                return self._rates
        except Exception:
            pass

        self._rates = {'NGN': Constants.USD_TO_NGN_FALLBACK}
        self._rates_timestamp = datetime.now(timezone.utc)
        return self._rates

    def convert_to_naira(self, amount: float, currency_code: str) -> Optional[float]:
        """Convert an amount in the given currency to Nigerian Naira."""
        if amount is None:
            return None

        code = (currency_code or 'NGN').upper()
        if code in ('NGN', '₦'):
            return amount

        rates = self._get_usd_rates()
        if code not in rates and 'NGN' in rates:
            return amount * rates['NGN']

        try:
            ngn_per_usd = rates.get('NGN', Constants.USD_TO_NGN_FALLBACK)
            code_per_usd = rates.get(code)
            if not code_per_usd:
                return amount * ngn_per_usd
            return amount * (ngn_per_usd / code_per_usd)
        except Exception:
            return amount * Constants.USD_TO_NGN_FALLBACK

    @staticmethod
    def detect_currency(price_string: str) -> str:
        """Best-effort detection of currency code from a raw price string."""
        s = (price_string or "").upper()
        if "₦" in s or "NGN" in s:
            return "NGN"
        if "$" in s or "USD" in s:
            return "USD"
        if "€" in s or "EUR" in s:
            return "EUR"
        if "£" in s or "GBP" in s:
            return "GBP"
        if "CAD" in s or "C$" in s:
            return "CAD"
        if "AUD" in s or "A$" in s:
            return "AUD"
        return "NGN"

    @staticmethod
    def parse_price_with_currency(price_string: str) -> Tuple[Optional[float], str]:
        """Parse a generic price string into (amount, currency_code)."""
        if not price_string:
            return None, "NGN"

        currency = CurrencyFormatter.detect_currency(price_string)
        try:
            cleaned = price_string
            for ch in ['₦', '$', '€', '£']:
                cleaned = cleaned.replace(ch, '')
            for code in ['NGN', 'USD', 'EUR', 'GBP', 'CAD', 'AUD']:
                cleaned = cleaned.replace(code, '')
            cleaned = cleaned.replace(',', '').strip()

            if '-' in cleaned:
                cleaned = cleaned.split('-')[0].strip()

            match = re.search(r'[\d.]+', cleaned)
            if match:
                return float(match.group()), currency
            return None, currency
        except Exception:
            return None, currency
    
    def format_price_range(self, min_price: float, max_price: float) -> str:
        """Format a price range in Naira"""
        if min_price == max_price:
            return self.format_naira(min_price)
        return f"{self.format_naira(min_price)} - {self.format_naira(max_price)}"

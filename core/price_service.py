"""
Price fetching and comparison services.
"""

import os
import time
import logging
import requests
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

from core.config import AppConfig, Constants
from core.models import RetailerPrice, PriceComparison, RecommendedRetailer
from core.cache import CacheManager
from core.currency import CurrencyFormatter
from core.utils import model_to_jsonable

logger = logging.getLogger(__name__)


class RapidAPIPriceService:
    """Fetches prices from global retailers via RapidAPI"""
    
    def __init__(self, cache_manager: CacheManager, config: AppConfig, api_key: str = None):
        self.cache = cache_manager
        self.config = config
        self.api_key = api_key or os.environ.get('RAPIDAPI_KEY', '')
        self.currency = CurrencyFormatter(cache_manager)
        self.session = requests.Session()
    
    def get_amazon_price(self, product_name: str) -> Optional[RetailerPrice]:
        """Get price from Amazon via RapidAPI Real-Time Amazon Data"""
        if not self.api_key:
            logger.warning("RapidAPI key not configured")
            return None
        
        cache_key = self.cache._get_cache_key(f"amazon_{product_name}")
        cached = self.cache.get(cache_key)
        if cached:
            return RetailerPrice(**cached)
        
        try:
            url = "https://real-time-amazon-data.p.rapidapi.com/search"
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": Constants.RAPIDAPI_HOST_AMAZON
            }
            params = {
                "query": product_name,
                "page": "1",
                "country": "US",
                "category_id": "aps"
            }
            
            response = self.session.get(url, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            products = data.get('data', {}).get('products', [])
            if not products:
                return None
            
            first_product = products[0]
            price_str = first_product.get('product_price', '')
            price_usd, _ = CurrencyFormatter.parse_price_with_currency(price_str)
            
            if price_usd is None:
                return None
            
            # Convert to Naira
            price_naira = self.currency.convert_to_naira(price_usd, 'USD')
            
            result = RetailerPrice(
                retailer_id='amazon',
                retailer_name='Amazon (US)',
                price_naira=price_naira,
                original_price=price_usd,  # Store USD for reference
                product_url=first_product.get('product_url', ''),
                in_stock=first_product.get('is_prime', True),
                last_checked=datetime.now(timezone.utc)
            )
            
            self.cache.set(cache_key, model_to_jsonable(result))
            return result
            
        except Exception as e:
            logger.warning(f"Amazon RapidAPI error: {e}")
            return None
    
    def get_multi_platform_prices(self, product_name: str) -> List[RetailerPrice]:
        """Get prices from multiple platforms via Product Item Search API"""
        if not self.api_key:
            logger.warning("RapidAPI key not configured")
            return []
        
        cache_key = self.cache._get_cache_key(f"multiplatform_{product_name}")
        cached = self.cache.get(cache_key)
        if cached:
            return [RetailerPrice(**p) for p in cached]
        
        try:
            url = "https://product-item-search-price-comparison.p.rapidapi.com/search"
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": Constants.RAPIDAPI_HOST_PRICE
            }
            params = {"query": product_name}
            
            response = self.session.get(url, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            results = []
            items = data.get('results', []) or data.get('items', []) or []
            
            for item in items[:5]:  # Limit to 5 results
                price_str = item.get('price', '') or item.get('current_price', '')
                price, currency = CurrencyFormatter.parse_price_with_currency(price_str)
                
                if price is None:
                    continue
                
                price_naira = self.currency.convert_to_naira(price, currency)
                
                results.append(RetailerPrice(
                    retailer_id=item.get('store', 'unknown').lower().replace(' ', '_'),
                    retailer_name=item.get('store', 'Unknown Store'),
                    price_naira=price_naira,
                    product_url=item.get('url', ''),
                    in_stock=True,
                    last_checked=datetime.now(timezone.utc)
                ))
            
            if results:
                self.cache.set(cache_key, [model_to_jsonable(r) for r in results])
            
            return results
            
        except Exception as e:
            logger.warning(f"Multi-platform RapidAPI error: {e}")
            return []


class NigerianPriceService:
    """Fetches and compares prices from Nigerian online retailers and global sources via RapidAPI"""
    
    def __init__(self, cache_manager: CacheManager, config: AppConfig, rapidapi_key: str = None):
        self.cache = cache_manager
        self.config = config
        self.currency = CurrencyFormatter(cache_manager)
        self.rapidapi_key = rapidapi_key or os.environ.get('RAPIDAPI_KEY', '')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': Constants.USER_AGENT,
            'Accept-Language': 'en-NG,en;q=0.9'
        })
    
    def get_price_comparison(self, product_name: str, include_global: bool = True) -> PriceComparison:
        """Get prices from multiple Nigerian retailers and optionally global sources via RapidAPI"""
        cache_key = self.cache._get_cache_key(f"all_prices_{product_name}_{include_global}")
        cached_prices = self.cache.get(cache_key)
        
        if cached_prices:
            logger.info(f"Using cached prices for: {product_name}")
            return PriceComparison(**cached_prices)
        
        prices = []
        
        # Fetch from each Nigerian retailer
        logger.info(f"Fetching prices from {len(Constants.NIGERIAN_RETAILERS)} Nigerian retailers...")
        for retailer_id, retailer_info in Constants.NIGERIAN_RETAILERS.items():
            try:
                price = self._fetch_retailer_price(product_name, retailer_id, retailer_info)
                if price:
                    prices.append(price)
                    logger.info(f"Got price from {retailer_info['name']}: ₦{price.price_naira:,.0f}" if price.price_naira else f"Got price from {retailer_info['name']}: N/A")
                time.sleep(self.config.request_delay)  # Be polite
            except Exception as e:
                logger.warning(f"Failed to fetch price from {retailer_info['name']}: {e}")
                continue
        
        # Fetch from RapidAPI (global sources) if enabled and key is available
        if include_global and self.rapidapi_key:
            try:
                rapidapi_service = RapidAPIPriceService(self.cache, self.config, self.rapidapi_key)
                
                # Try Amazon
                amazon_price = rapidapi_service.get_amazon_price(product_name)
                if amazon_price:
                    prices.append(amazon_price)
                    logger.info(f"Got Amazon price: ₦{amazon_price.price_naira:,.0f}" if amazon_price.price_naira else "Got Amazon price: N/A")
                
                # Try multi-platform API
                multi_prices = rapidapi_service.get_multi_platform_prices(product_name)
                if multi_prices:
                    prices.extend(multi_prices)
                    logger.info(f"Got {len(multi_prices)} prices from multi-platform API")
            except Exception as e:
                logger.warning(f"RapidAPI fetch failed: {e}")
        
        # Calculate statistics
        valid_prices = [p.price_naira for p in prices if p.price_naira is not None]
        
        comparison = PriceComparison(
            product_name=product_name,
            prices=prices,
            lowest_price=min(valid_prices) if valid_prices else None,
            highest_price=max(valid_prices) if valid_prices else None,
            average_price=sum(valid_prices) / len(valid_prices) if valid_prices else None,
            best_deal_retailer=min(prices, key=lambda x: x.price_naira or float('inf')).retailer_name if prices else None,
            price_last_updated=datetime.now(timezone.utc)
        )

        # Derive deal quality based on price spread
        if valid_prices and len(valid_prices) >= 2:
            lowest = comparison.lowest_price
            avg = comparison.average_price
            spread_pct = ((avg - lowest) / avg) * 100 if avg else 0
            
            if spread_pct >= 20:
                comparison.deal_quality = "excellent"
                comparison.deal_explanation = f"Best price is {spread_pct:.0f}% below average - great savings potential!"
            elif spread_pct >= 10:
                comparison.deal_quality = "good"
                comparison.deal_explanation = f"Best price is {spread_pct:.0f}% below average"
            else:
                comparison.deal_quality = "normal"
                comparison.deal_explanation = "Prices are fairly consistent across retailers"
        
        # Cache the comparison (JSON-safe)
        if prices:
            self.cache.set(cache_key, model_to_jsonable(comparison))
        
        return comparison
    
    def get_recommended_retailer(self, price_comparison: 'PriceComparison') -> Optional['RecommendedRetailer']:
        """Select the best retailer balancing price and trust score."""
        if not price_comparison or not price_comparison.prices:
            return None
        
        valid_prices = [p for p in price_comparison.prices if p.price_naira is not None]
        if not valid_prices:
            return None
        
        min_price = min(p.price_naira for p in valid_prices)
        max_price = max(p.price_naira for p in valid_prices)
        price_range = max_price - min_price if max_price > min_price else 1
        
        best_retailer = None
        best_score = -1
        best_reason = ""
        
        for price_entry in valid_prices:
            retailer_id = price_entry.retailer_id
            retailer_info = Constants.NIGERIAN_RETAILERS.get(retailer_id, {})
            trust_score = retailer_info.get('trust_score', 3)  # Default to 3 if unknown
            trust_note = retailer_info.get('trust_note', '')
            
            if price_range > 0:
                normalized_price = 1 - ((price_entry.price_naira - min_price) / price_range)
            else:
                normalized_price = 1.0
            
            combined_score = (trust_score / 5.0) * 0.4 + normalized_price * 0.6
            
            if combined_score > best_score:
                best_score = combined_score
                best_retailer = price_entry
                
                is_cheapest = price_entry.price_naira == min_price
                is_highly_trusted = trust_score >= 4
                
                if is_cheapest and is_highly_trusted:
                    best_reason = f"Best price among trusted retailers with official warranty support"
                elif is_cheapest:
                    best_reason = f"Lowest price available - verify seller reputation before purchase"
                elif is_highly_trusted:
                    best_reason = f"Highly trusted authorized retailer with reliable warranty and support"
                else:
                    best_reason = f"Good balance of competitive pricing and retailer reliability"
        
        if best_retailer:
            retailer_info = Constants.NIGERIAN_RETAILERS.get(best_retailer.retailer_id, {})
            return RecommendedRetailer(
                retailer_name=best_retailer.retailer_name,
                retailer_id=best_retailer.retailer_id,
                price_naira=best_retailer.price_naira,
                product_url=best_retailer.product_url,
                trust_score=retailer_info.get('trust_score', 3),
                trust_note=retailer_info.get('trust_note', ''),
                recommendation_reason=best_reason
            )
        
        return None

    def _fetch_retailer_price(self, product_name: str, retailer_id: str, 
                             retailer_info: Dict) -> Optional[RetailerPrice]:
        """Fetch price from a single retailer"""
        try:
            if retailer_id == 'jumia':
                return self._scrape_jumia(product_name, retailer_id, retailer_info)
            elif retailer_id == 'konga':
                return self._scrape_konga(product_name, retailer_id, retailer_info)
            elif retailer_id == 'slot':
                return self._scrape_slot(product_name, retailer_id, retailer_info)
            elif retailer_id == 'pointek':
                return self._scrape_pointek(product_name, retailer_id, retailer_info)
            elif retailer_id == 'jiji':
                return self._scrape_jiji(product_name, retailer_id, retailer_info)
            elif retailer_id == 'kilimall':
                return self._scrape_kilimall(product_name, retailer_id, retailer_info)
            elif retailer_id == 'kara':
                return self._scrape_kara(product_name, retailer_id, retailer_info)
            elif retailer_id == '3chub':
                return self._scrape_3chub(product_name, retailer_id, retailer_info)
            elif retailer_id == 'fouani':
                return self._scrape_fouani(product_name, retailer_id, retailer_info)
            elif retailer_id in ('computervillage', 'computervillage_ng', 'komputervillage'):
                return self._scrape_woocommerce_generic(product_name, retailer_id, retailer_info)
            return None
        except Exception as e:
            logger.warning(f"Scraping {retailer_id} failed: {e}")
            return None

    def _scrape_jumia(self, product_name: str, retailer_id: str, retailer_info: Dict) -> Optional[RetailerPrice]:
        try:
            search_url = f"{retailer_info['search_url']}{quote_plus(product_name)}"
            response = self.session.get(search_url, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            product = soup.find('article', class_='prd')
            if not product:
                return None
            
            price_elem = product.find('div', class_='prc')
            if not price_elem:
                return None
            
            price = CurrencyFormatter.parse_naira(price_elem.text)
            
            original_price = None
            old_price_elem = product.find('div', class_='old')
            if old_price_elem:
                original_price = CurrencyFormatter.parse_naira(old_price_elem.text)
            
            discount = None
            if original_price and price and original_price > price:
                discount = ((original_price - price) / original_price) * 100
            
            link = product.find('a', class_='core')
            product_url = retailer_info['base_url'] + link.get('href', '') if link else ''
            
            return RetailerPrice(
                retailer_id=retailer_id,
                retailer_name=retailer_info['name'],
                price_naira=price,
                original_price=original_price,
                discount_percent=discount,
                product_url=product_url,
                in_stock=True,
                last_checked=datetime.now(timezone.utc)
            )
        except Exception as e:
            logger.warning(f"Jumia scraping error: {e}")
            return None
    
    def _scrape_konga(self, product_name: str, retailer_id: str, retailer_info: Dict) -> Optional[RetailerPrice]:
        try:
            search_url = f"{retailer_info['search_url']}{quote_plus(product_name)}"
            response = self.session.get(search_url, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            product = soup.find('div', class_='product-item') or soup.find('section', class_='product-card')
            if not product:
                product = soup.find('div', {'data-testid': 'product-card'})
            if not product:
                return None
            
            price = None
            price_selectors = ['.product-price', '.price', '[class*="price"]', 'span[class*="amount"]']
            for selector in price_selectors:
                price_elem = product.select_one(selector)
                if price_elem:
                    price = CurrencyFormatter.parse_naira(price_elem.text)
                    if price:
                        break
            if not price:
                return None
            
            link = product.find('a', href=True)
            product_url = link.get('href', '') if link else ''
            if product_url and not product_url.startswith('http'):
                product_url = retailer_info['base_url'] + product_url
            
            return RetailerPrice(
                retailer_id=retailer_id,
                retailer_name=retailer_info['name'],
                price_naira=price,
                product_url=product_url,
                in_stock=True,
                last_checked=datetime.now(timezone.utc)
            )
        except Exception as e:
            logger.warning(f"Konga scraping error: {e}")
            return None
    
    def _scrape_slot(self, product_name: str, retailer_id: str, retailer_info: Dict) -> Optional[RetailerPrice]:
        try:
            search_url = f"{retailer_info['search_url']}{quote_plus(product_name)}&post_type=product"
            response = self.session.get(search_url, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            product = soup.find('li', class_='product') or soup.find('div', class_='product')
            if not product:
                return None
            
            price = None
            price_elem = product.find('span', class_='woocommerce-Price-amount') or product.find('bdi')
            if price_elem:
                price = CurrencyFormatter.parse_naira(price_elem.text)
            if not price:
                return None
            
            link = product.find('a', href=True)
            product_url = link.get('href', '') if link else ''
            
            return RetailerPrice(
                retailer_id=retailer_id,
                retailer_name=retailer_info['name'],
                price_naira=price,
                product_url=product_url,
                in_stock=True,
                last_checked=datetime.now(timezone.utc)
            )
        except Exception as e:
            logger.warning(f"Slot scraping error: {e}")
            return None
    
    def _scrape_pointek(self, product_name: str, retailer_id: str, retailer_info: Dict) -> Optional[RetailerPrice]:
        try:
            search_url = f"{retailer_info['search_url']}{quote_plus(product_name)}&post_type=product"
            response = self.session.get(search_url, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            product = soup.find('li', class_='product') or soup.find('div', class_='product-small')
            if not product:
                return None
            
            price = None
            price_elem = product.find('span', class_='woocommerce-Price-amount')
            if not price_elem:
                price_elem = product.find('bdi')
            if price_elem:
                price = CurrencyFormatter.parse_naira(price_elem.text)
            if not price:
                return None
            
            link = product.find('a', href=True)
            product_url = link.get('href', '') if link else ''
            
            return RetailerPrice(
                retailer_id=retailer_id,
                retailer_name=retailer_info['name'],
                price_naira=price,
                product_url=product_url,
                in_stock=True,
                last_checked=datetime.now(timezone.utc)
            )
        except Exception as e:
            logger.warning(f"Pointek scraping error: {e}")
            return None
    
    def _scrape_jiji(self, product_name: str, retailer_id: str, retailer_info: Dict) -> Optional[RetailerPrice]:
        try:
            search_url = f"{retailer_info['search_url']}{quote_plus(product_name)}"
            response = self.session.get(search_url, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            product = soup.find('div', class_='b-list-advert__item-wrapper') or \
                      soup.find('article', class_='b-advert') or \
                      soup.find('div', {'data-testid': 'listing-card'})
            if not product:
                return None
            
            price = None
            price_elem = product.find('div', class_='qa-advert-price') or \
                         product.find('span', class_='price') or \
                         product.select_one('[class*="price"]')
            if price_elem:
                price = CurrencyFormatter.parse_naira(price_elem.text)
            if not price:
                return None
            
            link = product.find('a', href=True)
            product_url = link.get('href', '') if link else ''
            if product_url and not product_url.startswith('http'):
                product_url = retailer_info['base_url'] + product_url
            
            return RetailerPrice(
                retailer_id=retailer_id,
                retailer_name=retailer_info['name'],
                price_naira=price,
                product_url=product_url,
                in_stock=True,
                last_checked=datetime.now(timezone.utc)
            )
        except Exception as e:
            logger.warning(f"Jiji scraping error: {e}")
            return None
    
    def _scrape_kilimall(self, product_name: str, retailer_id: str, retailer_info: Dict) -> Optional[RetailerPrice]:
        try:
            search_url = f"{retailer_info['search_url']}{quote_plus(product_name)}"
            response = self.session.get(search_url, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            product = soup.find('div', class_='product-item') or \
                      soup.find('li', class_='product-list-item')
            if not product:
                return None
            
            price = None
            price_elem = product.find('span', class_='price') or \
                         product.select_one('[class*="price"]')
            if price_elem:
                price = CurrencyFormatter.parse_naira(price_elem.text)
            if not price:
                return None
            
            link = product.find('a', href=True)
            product_url = link.get('href', '') if link else ''
            if product_url and not product_url.startswith('http'):
                product_url = retailer_info['base_url'] + product_url
            
            return RetailerPrice(
                retailer_id=retailer_id,
                retailer_name=retailer_info['name'],
                price_naira=price,
                product_url=product_url,
                in_stock=True,
                last_checked=datetime.now(timezone.utc)
            )
        except Exception as e:
            logger.warning(f"Kilimall scraping error: {e}")
            return None
    
    def _scrape_kara(self, product_name: str, retailer_id: str, retailer_info: Dict) -> Optional[RetailerPrice]:
        try:
            search_url = f"{retailer_info['search_url']}{quote_plus(product_name)}&post_type=product"
            response = self.session.get(search_url, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            product = soup.find('li', class_='product') or soup.find('div', class_='product')
            if not product:
                return None
            
            price = None
            price_elem = product.find('span', class_='woocommerce-Price-amount') or product.find('bdi')
            if price_elem:
                price = CurrencyFormatter.parse_naira(price_elem.text)
            if not price:
                return None
            
            link = product.find('a', href=True)
            product_url = link.get('href', '') if link else ''
            
            return RetailerPrice(
                retailer_id=retailer_id,
                retailer_name=retailer_info['name'],
                price_naira=price,
                product_url=product_url,
                in_stock=True,
                last_checked=datetime.now(timezone.utc)
            )
        except Exception as e:
            logger.warning(f"Kara scraping error: {e}")
            return None
    
    def _scrape_3chub(self, product_name: str, retailer_id: str, retailer_info: Dict) -> Optional[RetailerPrice]:
        try:
            search_url = f"{retailer_info['search_url']}{quote_plus(product_name)}&post_type=product"
            response = self.session.get(search_url, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            product = soup.find('li', class_='product') or soup.find('div', class_='product')
            if not product:
                return None
            
            price = None
            price_elem = product.find('span', class_='woocommerce-Price-amount') or product.find('bdi')
            if price_elem:
                price = CurrencyFormatter.parse_naira(price_elem.text)
            if not price:
                return None
            
            link = product.find('a', href=True)
            product_url = link.get('href', '') if link else ''
            
            return RetailerPrice(
                retailer_id=retailer_id,
                retailer_name=retailer_info['name'],
                price_naira=price,
                product_url=product_url,
                in_stock=True,
                last_checked=datetime.now(timezone.utc)
            )
        except Exception as e:
            logger.warning(f"3C Hub scraping error: {e}")
            return None
    
    def _scrape_fouani(self, product_name: str, retailer_id: str, retailer_info: Dict) -> Optional[RetailerPrice]:
        try:
            search_url = f"{retailer_info['search_url']}{quote_plus(product_name)}&post_type=product"
            response = self.session.get(search_url, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            product = soup.find('li', class_='product') or soup.find('div', class_='product-small')
            if not product:
                return None
            
            price = None
            price_elem = product.find('span', class_='woocommerce-Price-amount') or product.find('bdi')
            if price_elem:
                price = CurrencyFormatter.parse_naira(price_elem.text)
            if not price:
                return None
            
            link = product.find('a', href=True)
            product_url = link.get('href', '') if link else ''
            
            return RetailerPrice(
                retailer_id=retailer_id,
                retailer_name=retailer_info['name'],
                price_naira=price,
                product_url=product_url,
                in_stock=True,
                last_checked=datetime.now(timezone.utc)
            )
        except Exception as e:
            logger.warning(f"Fouani scraping error: {e}")
            return None
    
    def _scrape_woocommerce_generic(self, product_name: str, retailer_id: str, retailer_info: Dict) -> Optional[RetailerPrice]:
        try:
            search_url = f"{retailer_info['search_url']}{quote_plus(product_name)}&post_type=product"
            response = self.session.get(search_url, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            product = soup.find('li', class_='product') or \
                      soup.find('div', class_='product') or \
                      soup.find('div', class_='product-small') or \
                      soup.find('article', class_='product')
            if not product:
                return None
            
            price = None
            price_selectors = [
                ('span', 'woocommerce-Price-amount'),
                ('bdi', None),
                ('span', 'price'),
                ('ins', None),
            ]
            for tag, cls in price_selectors:
                if cls:
                    price_elem = product.find(tag, class_=cls)
                else:
                    price_elem = product.find(tag)
                if price_elem:
                    price = CurrencyFormatter.parse_naira(price_elem.text)
                    if price:
                        break
            if not price:
                return None
            
            link = product.find('a', href=True)
            product_url = link.get('href', '') if link else ''
            if product_url and not product_url.startswith('http'):
                product_url = retailer_info['base_url'] + product_url
            
            return RetailerPrice(
                retailer_id=retailer_id,
                retailer_name=retailer_info['name'],
                price_naira=price,
                product_url=product_url,
                in_stock=True,
                last_checked=datetime.now(timezone.utc)
            )
        except Exception as e:
            logger.warning(f"{retailer_info['name']} scraping error: {e}")
            return None

"""
Web scraping and search utilities.
"""

import time
import re
import logging
import json
import base64
import requests
from io import BytesIO
from urllib.parse import quote_plus, urlparse
from bs4 import BeautifulSoup
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, timezone
from PIL import Image

from core.config import AppConfig, Constants
from core.models import SearchResult, ScrapedContent, ProductImage
from core.cache import CacheManager
from core.utils import model_to_jsonable

logger = logging.getLogger(__name__)


class SearchError(Exception):
    """Search-related errors"""
    pass


class WebSearchClient:
    """Handles web search operations"""
    
    def __init__(self, cache_manager: CacheManager, config: AppConfig):
        self.cache = cache_manager
        self.config = config
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create configured HTTP session"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': Constants.USER_AGENT,
            'Accept': Constants.ACCEPT_HEADER,
            'Accept-Language': Constants.ACCEPT_LANGUAGE,
        })
        return session
    
    def search_products(self, product_name: str) -> List[SearchResult]:
        """Search for product information"""
        cache_key = self.cache._get_cache_key(f"search_{product_name}")
        cached_results = self.cache.get(cache_key)
        
        if cached_results:
            logger.info(f"Using cached search results for: {product_name}")
            return [SearchResult(**result) for result in cached_results]
        
        try:
            search_query = f"{product_name} specifications review price features"
            results = self._duckduckgo_search(search_query)
            
            if results:
                # Cache the raw dict data (JSON-safe via model_to_jsonable)
                self.cache.set(cache_key, [model_to_jsonable(result) for result in results])
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed for {product_name}: {e}")
            raise SearchError(f"Search failed: {str(e)}")
    
    def _duckduckgo_search(self, query: str) -> List[SearchResult]:
        """Perform DuckDuckGo search"""
        try:
            url = "https://html.duckduckgo.com/html/"
            data = {'q': query}
            
            response = self.session.post(url, data=data, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for result in soup.find_all('div', class_='result')[:self.config.max_search_results]:
                link = result.find('a', class_='result__a')
                snippet = result.find('a', class_='result__snippet')
                
                if link and snippet:
                    url = self._clean_url(link.get('href', ''))
                    domain = self._extract_domain(url)
                    
                    results.append(SearchResult(
                        title=link.text.strip(),
                        url=url,
                        snippet=snippet.text.strip(),
                        domain=domain
                    ))
            
            return results
            
        except requests.RequestException as e:
            raise SearchError(f"Search request failed: {str(e)}")
        except Exception as e:
            raise SearchError(f"Search parsing failed: {str(e)}")
    
    def _clean_url(self, url: str) -> str:
        """Clean and format URL"""
        if url.startswith('//'):
            return 'https:' + url
        return url
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return ""


class ContentScraper:
    """Handles web content scraping"""
    
    def __init__(self, cache_manager: CacheManager, config: AppConfig):
        self.cache = cache_manager
        self.config = config
        # Use a session with browser-like headers to reduce 403/anti-bot blocks
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': Constants.USER_AGENT,
            'Accept': Constants.ACCEPT_HEADER,
            'Accept-Language': Constants.ACCEPT_LANGUAGE,
        })
    
    def scrape_content(self, search_results: List[SearchResult]) -> List[ScrapedContent]:
        """Scrape content from search results"""
        scraped_data = []
        
        for i, result in enumerate(search_results[:self.config.max_scrape_results]):
            try:
                content = self._scrape_single_page(result.url, result.title)
                if content:
                    scraped_data.append(content)
                    
                # Be polite to servers
                if i < len(search_results) - 1:
                    time.sleep(self.config.request_delay)
                    
            except Exception as e:
                logger.warning(f"Failed to scrape {result.url}: {e}")
                continue
                
        return scraped_data
    
    def _scrape_single_page(self, url: str, title: str) -> Optional[ScrapedContent]:
        """Scrape a single web page"""
        cache_key = self.cache._get_cache_key(f"content_{url}")
        cached_content = self.cache.get(cache_key)
        
        if cached_content:
            return ScrapedContent(**cached_content)
        
        try:
            response = self.session.get(url, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'ads', 'iframe']):
                element.decompose()
            
            # Extract main content
            content = self._extract_main_content(soup)
            if not content:
                return None
            
            # Clean and truncate content
            cleaned_content = self._clean_content(content)
            truncated_content = cleaned_content[:self.config.max_content_length]
            
            scraped_content = ScrapedContent(
                url=url,
                title=title,
                content=truncated_content,
                content_length=len(truncated_content),
                scrape_timestamp=datetime.now(timezone.utc)
            )
            
            # Cache the content (JSON-safe)
            self.cache.set(cache_key, model_to_jsonable(scraped_content))
            
            return scraped_content
            
        except Exception as e:
            logger.warning(f"Scraping failed for {url}: {e}")
            return None
    
    def _extract_main_content(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract main content from page"""
        content_selectors = [
            'main', 'article', 
            'div.content', 'div#content',
            'div.main-content', 'div.article-content',
            'div.post-content', 'div.entry-content'
        ]
        
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(separator=' ', strip=True)
        
        # Fallback to body
        body = soup.find('body')
        if body:
            return body.get_text(separator=' ', strip=True)
            
        return None
    
    def _clean_content(self, content: str) -> str:
        """Clean extracted content"""
        # Remove extra whitespace
        content = ' '.join(content.split())
        # Remove excessive line breaks
        content = re.sub(r'\n\s*\n', '\n\n', content)
        return content


class ProductImageFetcher:
    """Fetches product images from multiple sources"""

    def __init__(self, cache_manager: CacheManager, config: AppConfig):
        self.cache = cache_manager
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': Constants.USER_AGENT})

    def fetch_product_images(self, product_name: str, max_images: int = 5) -> List[ProductImage]:
        """Fetch exact product images from brand site, retailers, then web search (strictly filtered)."""
        cache_key = self.cache._get_cache_key(f"images_{product_name}")
        cached_images = self.cache.get(cache_key)
        if cached_images:
            logger.info(f"Using cached images for: {product_name}")
            return [ProductImage(**img) for img in cached_images]
        
        images: List[ProductImage] = []
        try:
            # 1) Brand official site (highest priority - most accurate)
            logger.info(f"Fetching brand images for: {product_name}")
            brand_imgs = self._fetch_brand_images(product_name, max_images=3)
            images.extend(brand_imgs)
            
            # 2) Nigerian retailers (accurate, locally relevant)
            if len(images) < max_images:
                logger.info(f"Fetching retailer images for: {product_name}")
                retail_imgs = self._fetch_retailer_images(product_name, max_images=3)
                images.extend(retail_imgs)
            
            # 3) DuckDuckGo (strict query + filtering)
            if len(images) < max_images:
                logger.info(f"Fetching DuckDuckGo images for: {product_name}")
                ddg_imgs = self._fetch_duckduckgo_images(product_name, max_images * 3)
                images.extend(ddg_imgs)
            
            # 4) Bing (strict query + filtering)
            if len(images) < max_images:
                logger.info(f"Fetching Bing images for: {product_name}")
                bing_imgs = self._fetch_bing_images(product_name, max_images * 3)
                images.extend(bing_imgs)
            
        except Exception as e:
            logger.error(f"Image fetching failed: {e}")
        
        # De-dup images
        def _dedup(imgs: List[ProductImage]) -> List[ProductImage]:
            seen = set()
            out: List[ProductImage] = []
            for im in imgs:
                key = (im.url or "", im.thumbnail_url or "")
                if key not in seen and im.url:
                    seen.add(key)
                    out.append(im)
            return out
        
        images = _dedup(images)
        
        # Rank images by relevance
        images = self._rank_images(images, product_name)
        
        if not images:
            logger.warning(f"No matching images found for '{product_name}' after strict filtering.")
        else:
            logger.info(f"Found {len(images)} matching images for '{product_name}'")
            self.cache.set(cache_key, [model_to_jsonable(img) for img in images[:max_images]])
        
        return images[:max_images]

    def _enhance_image_query(self, product_name: str) -> str:
        """Clean up and enhance the product name to form an image search query."""
        clean_name = ' '.join(product_name.split())
        return f'"{clean_name}" official product image'

    def _fetch_duckduckgo_images(self, product_name: str, max_images: int) -> List[ProductImage]:
        """Fetch images from DuckDuckGo with strict filtering."""
        try:
            query = self._enhance_image_query(product_name)
            url = "https://duckduckgo.com/"
            params = {'q': query, 'iax': 'images', 'ia': 'images'}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            vqd_match = re.search(r'vqd=([\d-]+)', response.text)
            if not vqd_match:
                return []
            vqd = vqd_match.group(1)
            image_url = "https://duckduckgo.com/i.js"
            params = {'q': query, 'vqd': vqd, 'l': 'us-en', 'p': '1', 'v7exp': 'a'}
            response = self.session.get(image_url, params=params, timeout=10)
            data = response.json()
            results = data.get('results', [])
            if not results:
                return []
            images: List[ProductImage] = []
            for res in results[:max_images * 3]:
                img_url = res.get('image')
                alt = res.get('title', product_name)
                if img_url and self._is_valid_image_url(img_url) and self._is_product_image(img_url, alt, product_name):
                    images.append(ProductImage(
                        url=img_url,
                        thumbnail_url=res.get('thumbnail'),
                        source='DuckDuckGo',
                        width=res.get('width'),
                        height=res.get('height'),
                        alt_text=alt,
                    ))
            return images[:max_images]
        except Exception as e:
            logger.warning(f"DuckDuckGo image fetch failed: {e}")
            return []
    
    def _fetch_wikimedia_images(self, product_name: str, max_images: int) -> List[ProductImage]:
        """Use Wikimedia Commons API to fetch generic images."""
        try:
            api = "https://commons.wikimedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "generator": "search",
                "gsrnamespace": 6,
                "gsrlimit": max(10, max_images * 2),
                "gsrsearch": product_name,
                "prop": "imageinfo",
                "iiprop": "url",
                "iiurlwidth": 800,
            }
            resp = self.session.get(api, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            pages = (data.get("query", {}).get("pages", {}) or {}).values()
            images: List[ProductImage] = []
            for p in pages:
                infos = p.get("imageinfo") or []
                if not infos:
                    continue
                info = infos[0]
                url = info.get("thumburl") or info.get("url")
                if not url:
                    continue
                images.append(ProductImage(url=url, thumbnail_url=info.get("thumburl"), source="Wikimedia"))
                if len(images) >= max_images:
                    break
            return images
        except Exception:
            return []
    
    def _is_valid_image_url(self, url: str) -> bool:
        if not url:
            return False
        u = url.lower()
        invalid = ['placeholder', 'no-image', 'default', 'icon', 'logo', 'loading.gif', 'spinner', '1x1', 'pixel.png', 'blank', 'avatar', 'thumb-', 'favicon', 'banner', 'hero-bg', 'lockscreen', 'wallpaper', 'screenshot', 'lifestyle', 'holding', 'hand-', 'user-', 'background', 'pattern', 'texture']
        if any(x in u for x in invalid):
            return False
        if not any(ext in u for ext in ['.jpg', '.jpeg', '.png', '.webp']):
            if not any(x in u for x in ['image', 'img', 'photo', 'product', 'media']):
                return False
        return True
    
    def _is_product_image(self, img_url: str, alt_text: str, product_name: str) -> bool:
        """Strict check: is this actually a product image for the EXACT product searched?"""
        if not img_url:
            return False
        
        combined = (img_url + ' ' + (alt_text or '')).lower()
        
        lifestyle_keywords = [
            'person', 'people', 'man', 'woman', 'model', 'hand', 'holding', 
            'using', 'portrait', 'face', 'wallpaper', 'lockscreen', 'screenshot',
            'girl', 'boy', 'kid', 'child', 'user', 'customer', 'lifestyle',
            'stock-photo', 'stock_photo', 'shutterstock', 'getty', 'istock',
            'case', 'cover', 'accessory', 'accessories', 'charger', 'cable',
            'screen-protector', 'comparison', 'vs-', '-vs-', 'versus',
            'unboxing', 'box-', 'packaging', 'review-thumbnail', 'concept',
            'render', 'leaked', 'rumor', 'mockup', 'mock-up'
        ]
        
        if any(k in combined for k in lifestyle_keywords):
            return False
        
        product_lower = product_name.lower()
        all_tokens = [t for t in re.split(r"[^a-z0-9]+", product_lower) if len(t) >= 1]
        
        numeric_tokens = []
        for token in all_tokens:
            if token.isdigit() and len(token) >= 1:
                numeric_tokens.append(token)
            elif any(c.isdigit() for c in token) and len(token) >= 2:
                numeric_tokens.append(token)
        
        if numeric_tokens:
            for num_token in numeric_tokens:
                if num_token not in combined:
                    found = False
                    for word in re.split(r'[\s/_\-]+', combined):
                        if num_token in word:
                            found = True
                            break
                    if not found:
                        return False
        
        known_brands = {
            'iphone', 'samsung', 'galaxy', 'pixel', 'macbook', 'ipad', 'airpods',
            'sony', 'lg', 'dell', 'hp', 'lenovo', 'asus', 'xiaomi', 'redmi',
            'oppo', 'vivo', 'realme', 'infinix', 'tecno', 'itel', 'huawei',
            'oneplus', 'nokia', 'motorola', 'nintendo', 'switch', 'playstation',
            'xbox', 'bose', 'jbl', 'canon', 'nikon', 'gopro', 'dyson', 'apple'
        }
        
        brand_tokens = [t for t in all_tokens if t in known_brands]
        if brand_tokens:
            brand_found = any(bt in combined for bt in brand_tokens)
            if not brand_found:
                if 'iphone' in product_lower or 'ipad' in product_lower or 'macbook' in product_lower:
                    brand_found = 'apple' in combined
                if not brand_found:
                    return False
        
        variant_keywords = ['pro', 'max', 'plus', 'ultra', 'lite', 'mini', 'se', 'air']
        product_variants = [t for t in all_tokens if t in variant_keywords]
        
        if product_variants:
            variant_found = any(v in combined for v in product_variants)
            if not variant_found:
                logger.debug(f"Warning: variant mismatch for {product_name}, image may be generic")
        
        return True
    
    def _fetch_brand_images(self, product_name: str, max_images: int = 2) -> List[ProductImage]:
        brand = self._detect_brand(product_name)
        if not brand:
            return []
        images: List[ProductImage] = []
        try:
            search_url = f"https://{brand['domain']}{brand['search_path']}{quote_plus(product_name)}"
            resp = self.session.get(search_url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            selectors = [
                'meta[property="og:image"]',
                'picture img',
                'img[class*="product"]',
                'img[class*="hero"]',
                'div.product-image img',
                'div.product-gallery img'
            ]
            for sel in selectors:
                if sel.startswith('meta'):
                    tag = soup.select_one(sel)
                    if tag:
                        img_url = tag.get('content')
                        if img_url and self._is_valid_image_url(img_url) and self._is_product_image(img_url, product_name, product_name):
                            images.append(ProductImage(url=img_url, thumbnail_url=img_url, source=f"{brand['name']} Official", alt_text=product_name))
                            if len(images) >= max_images:
                                break
                else:
                    for img in soup.select(sel)[:max_images]:
                        img_url = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                        if not img_url:
                            continue
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        elif img_url.startswith('/'):
                            img_url = f"https://{brand['domain']}{img_url}"
                        alt = img.get('alt', product_name)
                        if self._is_valid_image_url(img_url) and self._is_product_image(img_url, alt, product_name):
                            images.append(ProductImage(url=img_url, thumbnail_url=img_url, source=f"{brand['name']} Official", alt_text=alt))
                            if len(images) >= max_images:
                                break
            return images[:max_images]
        except Exception:
            return []
    
    def _detect_brand(self, product_name: str) -> Optional[Dict[str,str]]:
        name = product_name.lower()
        brands = {
            'apple': {'name': 'Apple', 'domain': 'apple.com', 'search_path': '/search/'},
            'samsung': {'name': 'Samsung', 'domain': 'samsung.com', 'search_path': '/search/?searchvalue='},
            'sony': {'name': 'Sony', 'domain': 'sony.com', 'search_path': '/en-us/search/?q='},
            'lg': {'name': 'LG', 'domain': 'lg.com', 'search_path': '/search?q='},
            'dell': {'name': 'Dell', 'domain': 'dell.com', 'search_path': '/search?q='},
            'hp': {'name': 'HP', 'domain': 'hp.com', 'search_path': '/search?q='},
            'lenovo': {'name': 'Lenovo', 'domain': 'lenovo.com', 'search_path': '/search?q='},
            'asus': {'name': 'ASUS', 'domain': 'asus.com', 'search_path': '/search?q='},
            'google': {'name': 'Google', 'domain': 'store.google.com', 'search_path': '/search?q='},
            'xiaomi': {'name': 'Xiaomi', 'domain': 'mi.com', 'search_path': '/global/search?keyword='},
            'oppo': {'name': 'OPPO', 'domain': 'oppo.com', 'search_path': '/en/search/?q='},
            'vivo': {'name': 'Vivo', 'domain': 'vivo.com', 'search_path': '/en/search?q='},
            'realme': {'name': 'Realme', 'domain': 'realme.com', 'search_path': '/search?q='},
            'infinix': {'name': 'Infinix', 'domain': 'infinixmobility.com', 'search_path': '/search?q='},
            'tecno': {'name': 'Tecno', 'domain': 'tecno-mobile.com', 'search_path': '/search?q='},
            'itel': {'name': 'Itel', 'domain': 'itel-mobile.com', 'search_path': '/search?q='},
            'nintendo': {'name': 'Nintendo', 'domain': 'nintendo.com', 'search_path': '/search/?q='},
            'playstation': {'name': 'PlayStation', 'domain': 'playstation.com', 'search_path': '/search/?q='},
            'xbox': {'name': 'Xbox', 'domain': 'xbox.com', 'search_path': '/search?q='},
            'bose': {'name': 'Bose', 'domain': 'bose.com', 'search_path': '/search?q='},
            'jbl': {'name': 'JBL', 'domain': 'jbl.com', 'search_path': '/search?q='},
            'canon': {'name': 'Canon', 'domain': 'canon.com', 'search_path': '/search?q='},
            'nikon': {'name': 'Nikon', 'domain': 'nikon.com', 'search_path': '/search?q='},
        }
        for k, v in brands.items():
            if k in name or v['name'].lower() in name:
                return v
        return None
    
    def _fetch_retailer_images(self, product_name: str, max_images: int = 3) -> List[ProductImage]:
        images: List[ProductImage] = []
        for retailer_id, retailer_info in Constants.NIGERIAN_RETAILERS.items():
            if len(images) >= max_images:
                break
            try:
                search_url = retailer_info['search_url'] + quote_plus(product_name)
                resp = self.session.get(search_url, timeout=10)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, 'html.parser')
                selectors = ['img.img-fluid', 'img[data-src]', 'img.product-image', 'div.image-wrapper img', 'div.product img']
                for sel in selectors:
                    for img in soup.select(sel)[:2]:
                        img_url = img.get('src') or img.get('data-src')
                        if not img_url:
                            continue
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        elif img_url.startswith('/'):
                            img_url = retailer_info['base_url'] + img_url
                        alt = img.get('alt', product_name)
                        if self._is_valid_image_url(img_url) and self._is_product_image(img_url, alt, product_name):
                            images.append(ProductImage(url=img_url, thumbnail_url=img_url, source=retailer_info['name'], alt_text=alt))
                            if len(images) >= max_images:
                                break
                    if len(images) >= max_images:
                        break
            except Exception:
                continue
        return images
    
    def _get_brand_domains(self, product_name: str) -> List[str]:
        name = product_name.lower()
        domains: List[str] = []
        tokens = [t for t in re.split(r"[^a-z0-9]+", name) if t]
        if tokens:
            brand_guess = tokens[0]
            if len(brand_guess) >= 3:
                domains.append(f"{brand_guess}.com")
                domains.append(f"{brand_guess}.com.ng")

        # Apple ecosystem
        if any(k in name for k in ["iphone", "macbook", "ipad", "apple watch", "airpods", "apple"]):
            domains.append("apple.com")

        # Samsung
        if "samsung" in name:
            domains.append("samsung.com")

        # Google
        if any(k in name for k in ["pixel", "chromebook"]):
            domains.append("google.com")

        # Tecno / Infinix (common in Nigerian market)
        if "tecno" in name:
            domains.append("tecno-mobile.com")
        if "infinix" in name:
            domains.append("infinixmobility.com")

        # Xiaomi / Redmi
        if any(k in name for k in ["xiaomi", "redmi", "mi "]):
            domains.append("mi.com")

        # Sony
        if "sony" in name:
            domains.append("sony.com")
        
        return domains
    
    def _rank_images(self, images: List[ProductImage], product_name: str) -> List[ProductImage]:
        from urllib.parse import urlparse
        brand_domains = set(self._get_brand_domains(product_name))
        name_tokens = [t for t in re.split(r"[^a-z0-9]+", product_name.lower()) if t]

        preferred_hosts = [
            "amazon.", "bestbuy.", "walmart.", "target.", "ikea.",
            "jumia.com.ng", "konga.com", "slot.ng", "pointekonline.com",
            "ebayimg.com", "ebaystatic.com", "ebay.com", "aliexpress.",
            "bhphotovideo.", "microcenter.", "newegg.", "argos.", "currys.",
            "gsmarena.com", "apple.com", "samsung.com", "mi.com", "sony.com",
        ]
        positive_path_terms = ["product", "pdp", "sku", "item", "buy", "shop"]
        negative_terms = ["wallpaper", "background", "logo", "icon", "mockup", "render", "vector", "clipart"]

        def score(pi: ProductImage) -> int:
            s = 0
            u = (pi.url or "").lower()
            try:
                d = urlparse(u).netloc.lower()
            except:
                d = ""

            if d in brand_domains:
                s += 100
            if any(h in d for h in preferred_hosts):
                s += 40

            for tok in name_tokens:
                if tok and tok in u:
                    s += 5

            if any(term in u for term in positive_path_terms):
                s += 8
            if any(term in u for term in negative_terms):
                s -= 20

            try:
                w = int(pi.width or 0)
                h = int(pi.height or 0)
                if w * h > 0:
                    mp = (w * h) / 1_000_000
                    if mp > 0.5:
                        s += 5
            except Exception:
                pass

            return s

        return sorted(images, key=score, reverse=True)
    
    def _fetch_bing_images(self, product_name: str, max_images: int) -> List[ProductImage]:
        """Fetch images from Bing (strict filtering)."""
        try:
            query = self._enhance_image_query(product_name)
            url = f"https://www.bing.com/images/search?q={quote_plus(query)}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            images: List[ProductImage] = []
            for img_tag in soup.find_all('a', class_='iusc')[:max_images * 3]:
                try:
                    m = img_tag.get('m')
                    if m:
                        img_data = json.loads(m)
                        img_url = img_data.get('murl', '')
                        alt = img_data.get('t', product_name)
                        if img_url and self._is_valid_image_url(img_url) and self._is_product_image(img_url, alt, product_name):
                            images.append(ProductImage(
                                url=img_url,
                                thumbnail_url=img_data.get('turl', ''),
                                source='Bing',
                                alt_text=alt
                            ))
                except:
                    continue
            
            return images[:max_images]
            
        except Exception as e:
            logger.warning(f"Bing image fetch failed: {e}")
            return []
    
    def download_and_cache_image(self, image_url: str) -> Optional[str]:
        """Download image and return base64 encoded string"""
        try:
            response = self.session.get(image_url, timeout=10, stream=True)
            response.raise_for_status()
            
            # Open and resize image
            img = Image.open(BytesIO(response.content))
            
            # Resize for optimization (max 800px width)
            if img.width > 800:
                ratio = 800 / img.width
                new_size = (800, int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert to base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            logger.warning(f"Image download failed for {image_url}: {e}")
            return None

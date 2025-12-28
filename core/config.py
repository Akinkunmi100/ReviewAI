"""
Configuration and constants for the Product Review Engine.
"""

import logging
from dataclasses import dataclass
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AppConfig:
    """Centralized configuration management"""
    # API Settings
    model_name: str = "llama-3.3-70b-versatile"
    max_tokens_review: int = 2500
    max_tokens_chat: int = 1000
    temperature_review: float = 0.3
    temperature_chat: float = 0.5
    
    # Web Settings
    max_search_results: int = 10
    max_scrape_results: int = 6
    request_timeout: int = 10
    request_delay: float = 0.5
    max_content_length: int = 5000
    
    # Cache Settings
    cache_ttl_hours: int = 168  # Aggressive: catch for 7 days
    cache_max_size: int = 500   # Aggressive: store more items
    
    # UI Settings
    max_pros_cons_display: int = 10
    
    # Ranking weights
    sentiment_weight: float = 0.6
    mention_weight: float = 0.25
    aspect_weight: float = 0.15

    # LLM-based consolidation
    enable_llm_consolidation: bool = False
    consolidation_temperature: float = 0.2
    consolidation_max_tokens: int = 400


class Constants:
    """Application constants"""
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    ACCEPT_HEADER = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    ACCEPT_LANGUAGE = "en-US,en;q=0.5"
    
    # Currency settings
    DEFAULT_CURRENCY = 'NGN'
    NAIRA_SYMBOL = '₦'
    USD_TO_NGN_FALLBACK = 1600.0
    
    # RapidAPI settings
    RAPIDAPI_HOST_AMAZON = "real-time-amazon-data.p.rapidapi.com"
    RAPIDAPI_HOST_PRICE = "price-comparison.p.rapidapi.com"
    
    # Nigerian Retailers
    NIGERIAN_RETAILERS: Dict[str, Dict[str, Any]] = {
        'jumia': {
            'name': 'Jumia Nigeria',
            'base_url': 'https://www.jumia.com.ng',
            'search_url': 'https://www.jumia.com.ng/catalog/?q=',
            'logo': '🟠',
            'trust_score': 4,
            'trust_note': 'Established e-commerce platform with buyer protection and return policy'
        },
        'konga': {
            'name': 'Konga',
            'base_url': 'https://www.konga.com',
            'search_url': 'https://www.konga.com/search?search=',
            'logo': '🔵',
            'trust_score': 4,
            'trust_note': 'Major Nigerian retailer with warranty support and physical stores'
        },
        'slot': {
            'name': 'Slot Nigeria',
            'base_url': 'https://slot.ng',
            'search_url': 'https://slot.ng/?s=',
            'logo': '🟢',
            'trust_score': 5,
            'trust_note': 'Authorized dealer with nationwide physical stores and official warranty'
        },
        'pointek': {
            'name': 'PointekOnline',
            'base_url': 'https://pointekonline.com',
            'search_url': 'https://pointekonline.com/?s=',
            'logo': '🟣',
            'trust_score': 4,
            'trust_note': 'Established electronics retailer with good customer service'
        },
        'jiji': {
            'name': 'Jiji Nigeria',
            'base_url': 'https://jiji.ng',
            'search_url': 'https://jiji.ng/search?query=',
            'logo': '🟡',
            'trust_score': 2,
            'trust_note': 'Classifieds marketplace - verify seller reputation before purchase'
        },
        'kilimall': {
            'name': 'Kilimall Nigeria',
            'base_url': 'https://www.kilimall.com.ng',
            'search_url': 'https://www.kilimall.com.ng/search?q=',
            'logo': '🔴',
            'trust_score': 3,
            'trust_note': 'Online marketplace - check seller ratings before purchase'
        },
        'kara': {
            'name': 'Kara Nigeria',
            'base_url': 'https://kara.com.ng',
            'search_url': 'https://kara.com.ng/?s=',
            'logo': '⚫',
            'trust_score': 4,
            'trust_note': 'Established appliance and electronics retailer'
        },
        '3chub': {
            'name': '3C Hub',
            'base_url': 'https://3chub.com',
            'search_url': 'https://3chub.com/?s=',
            'logo': '🟤',
            'trust_score': 4,
            'trust_note': 'Authorized technology retailer with product warranty'
        },
        'fouani': {
            'name': 'Fouani Nigeria',
            'base_url': 'https://fouanistore.com',
            'search_url': 'https://fouanistore.com/?s=',
            'logo': '⚪',
            'trust_score': 5,
            'trust_note': 'Official LG distributor in Nigeria with manufacturer warranty'
        },
        'computervillage': {
            'name': 'Computer Village Online',
            'base_url': 'https://computervillageonline.com',
            'search_url': 'https://computervillageonline.com/?s=',
            'logo': '💻',
            'trust_score': 3,
            'trust_note': 'Online platform - verify specific vendor reputation'
        },
        'computervillage_ng': {
            'name': 'ComputerVillage.ng',
            'base_url': 'https://computervillage.ng',
            'search_url': 'https://computervillage.ng/?s=',
            'logo': '🖥️',
            'trust_score': 3,
            'trust_note': 'Online platform - verify specific vendor reputation'
        },
        'komputervillage': {
            'name': 'Komputer Village',
            'base_url': 'https://komputervillage.com',
            'search_url': 'https://komputervillage.com/?s=',
            'logo': '🔌',
            'trust_score': 3,
            'trust_note': 'Online platform - verify specific vendor reputation'
        },
        'spar': {
            'name': 'Spar Nigeria',
            'base_url': 'https://spar.com.ng',
            'search_url': 'https://spar.com.ng/?s=',
            'logo': '🛒',
            'trust_score': 4,
            'trust_note': 'Major retail chain with nationwide presence'
        },
        'shoprite': {
            'name': 'ShopRite Nigeria',
            'base_url': 'https://shoprite.ng',
            'search_url': 'https://shoprite.ng/?s=',
            'logo': '🏪',
            'trust_score': 4,
            'trust_note': 'Major retail chain with warranty support'
        },
        'payporte': {
            'name': 'Payporte',
            'base_url': 'https://www.payporte.com',
            'search_url': 'https://www.payporte.com/search?q=',
            'logo': '💳',
            'trust_score': 3,
            'trust_note': 'Nigerian online retailer with buyer protection'
        },
        'buyright': {
            'name': 'BuyRight Electronics',
            'base_url': 'https://buyrightelectronics.com.ng',
            'search_url': 'https://buyrightelectronics.com.ng/?s=',
            'logo': '🔋',
            'trust_score': 4,
            'trust_note': 'Electronics specialist with product warranty'
        },
        'megaplaza': {
            'name': 'MegaPlaza Store',
            'base_url': 'https://megaplazaonline.com',
            'search_url': 'https://megaplazaonline.com/?s=',
            'logo': '🏬',
            'trust_score': 4,
            'trust_note': 'Major shopping center with multiple brands'
        },
        'hubmart': {
            'name': 'Hubmart Stores',
            'base_url': 'https://hubmart.com.ng',
            'search_url': 'https://hubmart.com.ng/?s=',
            'logo': '🛍️',
            'trust_score': 4,
            'trust_note': 'Nigerian supermarket chain with quality products'
        },
        'parknshop': {
            'name': 'Park n Shop',
            'base_url': 'https://parknshop.ng',
            'search_url': 'https://parknshop.ng/?s=',
            'logo': '🅿️',
            'trust_score': 4,
            'trust_note': 'Retail chain with physical stores'
        },
        'supermart': {
            'name': 'Supermart.ng',
            'base_url': 'https://supermart.ng',
            'search_url': 'https://supermart.ng/catalogsearch/result/?q=',
            'logo': '🛒',
            'trust_score': 4,
            'trust_note': 'Online supermarket with delivery services'
        },
        'olist': {
            'name': 'Olist.ng',
            'base_url': 'https://olist.ng',
            'search_url': 'https://olist.ng/search?q=',
            'logo': '📱',
            'trust_score': 3,
            'trust_note': 'Online marketplace - check seller ratings'
        },
        'superonline': {
            'name': 'Superonline.ng',
            'base_url': 'https://superonline.ng',
            'search_url': 'https://superonline.ng/?s=',
            'logo': '⚡',
            'trust_score': 3,
            'trust_note': 'Online electronics store'
        },
        'game': {
            'name': 'Game Nigeria',
            'base_url': 'https://game.co.za/ng',
            'search_url': 'https://game.co.za/ng/search?q=',
            'logo': '🎮',
            'trust_score': 4,
            'trust_note': 'Major South African retail chain operating in Nigeria'
        },
        'dealdey': {
            'name': 'DealDey',
            'base_url': 'https://dealdey.com',
            'search_url': 'https://dealdey.com/search?q=',
            'logo': '💰',
            'trust_score': 3,
            'trust_note': 'Nigerian deals and discount platform'
        }
    }

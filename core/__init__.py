"""
Core package for Product Review Engine.

This package contains the modularized components extracted from app_update.py.
"""

from core.config import AppConfig, Constants
from core.currency import CurrencyFormatter
from core.models import (
    SearchResult,
    ScrapedContent,
    ProductReview,
    SentimentScore,
    ProductImage,
    RetailerPrice,
    PriceComparison,
    RedFlag,
    RedFlagReport,
    PurchaseTimingAdvice,
    BestForTag,
    UserProfile,
    ProductComparisonItem,
    ProductComparison,
    AlternativeProduct,
    RecommendedRetailer,
    ResaleAnalysis,
    EnhancedProductReview,
)

__all__ = [
    'AppConfig',
    'Constants',
    'CurrencyFormatter',
    'SearchResult',
    'ScrapedContent',
    'ProductReview',
    'SentimentScore',
    'ProductImage',
    'RetailerPrice',
    'PriceComparison',
    'RedFlag',
    'RedFlagReport',
    'PurchaseTimingAdvice',
    'BestForTag',
    'UserProfile',
    'ProductComparisonItem',
    'ProductComparison',
    'AlternativeProduct',
    'RecommendedRetailer',
    'ResaleAnalysis',
    'EnhancedProductReview',
]

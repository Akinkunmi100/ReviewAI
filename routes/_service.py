"""Shared service utilities for routes."""

import os
from core.config import AppConfig
from core.product_service import EnhancedProductReviewService, ProductReviewError

__all__ = ['get_review_service', 'ProductReviewError']


def get_review_service() -> EnhancedProductReviewService:
    """Create (or in future reuse) the enhanced review service."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY environment variable is not set")
    config = AppConfig()
    return EnhancedProductReviewService(api_key, config)

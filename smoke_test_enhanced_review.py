"""
Smoke test for EnhancedReviewGenerator using a stub Groq client.
Run with: python smoke_test_enhanced_review.py
"""
import json
import types
from datetime import datetime, timezone
from pathlib import Path

from app_update import (
    AppConfig, CacheManager, SentimentAnalyzer, ProductImageFetcher,
    EnhancedReviewGenerator, SearchResult, ScrapedContent
)

# --- Stub Groq client ------------------------------------------------------
class StubGroq:
    def __init__(self):
        self.chat = types.SimpleNamespace()
        def create(**kwargs):
            # Return a minimal, valid ProductReview JSON for the generator
            review = {
                "product_name": "iPhone 15 Pro",
                "specifications_inferred": "A premium smartphone with A17 chip, 6.1-inch OLED display, 8GB RAM, 256GB storage.",
                "predicted_rating": "4.6 / 5.0",
                "pros": [
                    "Excellent performance with A17 chip",
                    "Outstanding camera system",
                    "Premium build quality and materials",
                    "Long battery life compared to prior models"
                ],
                "cons": [
                    "Very expensive compared to alternatives",
                    "Limited port options (no USB-C on some regions)",
                    "Battery may degrade under heavy use over long term"
                ],
                "verdict": "A top-tier device for power users who value camera and performance, but pricey for budget-conscious buyers.",
                "price_info": "$999",
                "sources": ["https://example.com/review1", "https://example.com/review2"],
                "last_updated": datetime.now(timezone.utc).strftime('%Y-%m-%d'),
                "data_source_type": "free_web_search"
            }
            # Build a simple completion-like object
            response = types.SimpleNamespace()
            response.choices = [types.SimpleNamespace(message=types.SimpleNamespace(content=json.dumps(review)))]
            return response
        self.chat.completions = types.SimpleNamespace(create=create)


def main():
    config = AppConfig()
    cache = CacheManager(cache_dir=Path(".cache_test"))
    sentiment = SentimentAnalyzer()
    # Use a minimal image fetcher stub to avoid external fetch methods in the full class
    class MinimalImageFetcher:
        def fetch_product_images(self, product_name, max_images=5):
            return []

    image_fetcher = MinimalImageFetcher()

    # Stub Groq client that returns a deterministic review
    groq = StubGroq()

    gen = EnhancedReviewGenerator(groq, config, sentiment, image_fetcher)

    # Monkeypatch any missing helper methods used by EnhancedReviewGenerator for the smoke test
    def _compute_purchase_recommendation(self, timing_advice=None, red_flag_report=None, price_comparison=None, data_quality=None):
        return ("consider_alternatives", ["Default recommendation due to smoke-test mode"]) 

    import types
    gen._compute_purchase_recommendation = types.MethodType(_compute_purchase_recommendation, gen)
    def _build_authenticity_note(self, data_source_type=None, data_quality=None, price_confidence=None, num_sources=0, num_retailers=0):
        return f"Data quality: {data_quality or 'unknown'}, price confidence: {price_confidence or 'unknown'}"

    gen._build_authenticity_note = types.MethodType(_build_authenticity_note, gen)

    # Minimal search results and scraped content (the review is produced by stub)
    search_results = [
        SearchResult(title="iPhone 15 Pro Review - Example", url="https://example.com/review1", snippet="Great performance and camera.", domain="example.com")
    ]
    scraped = [
        ScrapedContent(url="https://example.com/review1", title="Example Review 1", content="Excellent performance. Camera is outstanding.", content_length=80, scrape_timestamp=datetime.now(timezone.utc)),
    ]

    print("Running smoke test: generate_enhanced_review('iPhone 15 Pro')")
    try:
        review = gen.generate_enhanced_review("iPhone 15 Pro", search_results, scraped)
        # Print a concise summary
        print("--- Enhanced Review Summary ---")
        print(f"Product: {review.product_name}")
        print(f"Rating: {review.predicted_rating}")
        print(f"Top Strengths: {review.top_strengths}")
        print(f"Main Weaknesses: {review.main_weaknesses}")
        print(f"Primary Image: {review.primary_image_url}")
        print(f"Price (Naira): {review.price_naira}")
        print(f"Purchase Recommendation: {review.purchase_recommendation}")
    except Exception as e:
        print("Smoke test failed:", repr(e))


if __name__ == '__main__':
    main()

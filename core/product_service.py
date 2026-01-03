"""
Main product review service orchestration.
"""

import logging
from typing import List, Optional, cast
from groq import Groq

from core.config import AppConfig
from core.models import (
    ProductReview, EnhancedProductReview, ProductComparison, UserProfile
)
from core.cache import CacheManager
from core.scraping import (
    WebSearchClient, ContentScraper, ProductImageFetcher, SearchError
)
from core.sentiment import SentimentAnalyzer
from core.price_service import NigerianPriceService
from core.chat_service import ChatService
from core.review_generator import (
    ReviewGenerator, EnhancedReviewGenerator, ComparisonGenerator, AIGenerationError
)
from core.analyzers import (
    RedFlagDetector, PurchaseTimingAdvisor, ResaleAnalyzer,
    VideoProofFinder, FakeSpotter, VoxPopuliAnalyzer,
    SmartSwapAnalyzer, NetPriceAnalyzer, DisasterAnalyzer
)

logger = logging.getLogger(__name__)


class ProductReviewError(Exception):
    """Base error for product review service"""
    pass


class ProductReviewService:
    """Orchestrates product review generation"""
    
    def __init__(self, groq_api_key: str, config: AppConfig = None):
        self.config = config or AppConfig()
        self.groq_client = Groq(api_key=groq_api_key)
        self.cache_manager = CacheManager(self.config)
        
        # Initialize components
        self.search_client = WebSearchClient(self.cache_manager, self.config)
        self.scraper = ContentScraper(self.cache_manager, self.config)
        self.review_generator = ReviewGenerator(self.groq_client, self.config)
        self.chat_service = ChatService(
            self.groq_client, 
            self.config,
            web_search_client=self.search_client,
            content_scraper=self.scraper
        )
    
    def generate_review(self, product_name: str, use_web_search: bool = True) -> ProductReview:
        """Generate product review"""
        try:
            if use_web_search:
                return self._generate_web_review(product_name)
            else:
                return self._generate_ai_knowledge_review(product_name)
                
        except ProductReviewError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error generating review: {e}")
            raise ProductReviewError(f"Failed to generate review: {str(e)}")
    
    def _generate_web_review(self, product_name: str) -> ProductReview:
        """Generate review using web search"""
        # Step 1: Search
        search_results = self.search_client.search_products(product_name)
        if not search_results:
            raise SearchError("No search results found")
        
        # Step 2: Scrape content
        scraped_content = self.scraper.scrape_content(search_results)
        
        # Step 3: Generate review
        return self.review_generator.generate_web_review(
            product_name, search_results, scraped_content
        )
    
    def _generate_ai_knowledge_review(self, product_name: str) -> ProductReview:
        """Generate review using AI knowledge"""
        return self.review_generator.generate_ai_knowledge_review(product_name)


class EnhancedProductReviewService(ProductReviewService):
    """Enhanced service with Nigerian pricing, sentiment, red flags, and timing intelligence"""
    
    def __init__(self, groq_api_key: str, config: AppConfig = None):
        super().__init__(groq_api_key, config)
        
        # Initialize analysis components
        self.sentiment_analyzer = SentimentAnalyzer()
        self.image_fetcher = ProductImageFetcher(self.cache_manager, self.config)
        
        # Initialize Nigerian pricing service
        self.price_service = NigerianPriceService(self.cache_manager, self.config)
        
        # Initialize intelligence services
        self.red_flag_detector = RedFlagDetector(self.groq_client, self.config)
        self.timing_advisor = PurchaseTimingAdvisor(self.groq_client, self.config)
        self.resale_analyzer = ResaleAnalyzer(self.groq_client, self.config)
        self.video_proof_finder = VideoProofFinder(self.groq_client, self.config)
        self.fake_spotter = FakeSpotter(self.groq_client, self.config)
        self.vox_populi = VoxPopuliAnalyzer(self.groq_client, self.config)
        self.smart_swap_analyzer = SmartSwapAnalyzer(self.groq_client, self.config)
        self.net_price_analyzer = NetPriceAnalyzer(self.groq_client, self.config)
        self.disaster_analyzer = DisasterAnalyzer(self.groq_client, self.config)
        
        # Initialize comparison generator
        self.comparison_generator = ComparisonGenerator(self.groq_client, self.config)
        
        # Replace review generator with enhanced version
        self.review_generator = EnhancedReviewGenerator(
            self.groq_client,
            self.config,
            self.sentiment_analyzer,
            self.image_fetcher,
            self.price_service,
            self.red_flag_detector,
            self.timing_advisor,
            self.resale_analyzer,
            self.video_proof_finder,
            self.fake_spotter,
            self.vox_populi,
            self.smart_swap_analyzer,
            self.net_price_analyzer,
            self.disaster_analyzer
        )
    
    def generate_review(self, product_name: str, use_web_search: bool = True, mode: str = None) -> EnhancedProductReview:
        """Generate enhanced product review.

        Args:
            product_name: Name of the product to review
            use_web_search: If True, use web search; if False, use AI knowledge only
            mode: Optional explicit mode ("web", "ai", "hybrid"). If provided, overrides use_web_search.
        
        mode options:
          - "web": use only live web data
          - "ai": use only AI knowledge  
          - "hybrid": combine web + AI knowledge (prefer web when they conflict)
        """
        try:
            # Determine effective mode
            if mode is None:
                effective_mode = "web" if use_web_search else "ai"
            else:
                effective_mode = mode
            
            if effective_mode == "web":
                return self._generate_enhanced_web_review(product_name)
            elif effective_mode == "ai":
                return self._generate_enhanced_ai_review(product_name)
            elif effective_mode == "hybrid":
                return self._generate_enhanced_hybrid_review(product_name)
            else:
                # Fallback to web
                return self._generate_enhanced_web_review(product_name)
        except ProductReviewError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error generating enhanced review: {e}")
            raise ProductReviewError(f"Failed to generate review: {str(e)}")
    
    def generate_comparison(self, product_names: List[str]) -> ProductComparison:
        """Generate comparison between multiple products"""
        reviews = []
        for name in product_names[:3]:  # Max 3 products
            try:
                # Always use web mode for comparisons to get specs
                review = self.generate_review(name, use_web_search=True, mode="web")
                reviews.append(review)
            except Exception as e:
                logger.warning(f"Failed to generate review for {name}: {e}")
                continue
        
        if len(reviews) < 2:
            raise ProductReviewError("Need at least 2 successful reviews for comparison")
        
        return self.comparison_generator.generate_comparison(reviews)
    
    def _generate_enhanced_web_review(self, product_name: str) -> EnhancedProductReview:
        """Generate review with web search, Nigerian prices, and intelligence"""
        # Search and scrape
        
        # Casting parent classes might be needed if type checker complains, 
        # but here we know self.review_generator is EnhancedReviewGenerator
        
        search_results = self.search_client.search_products(product_name)
        if not search_results:
            raise SearchError("No search results found")
        
        scraped_content = self.scraper.scrape_content(search_results)
        
        # Generate enhanced review with all intelligence
        # self.review_generator IS an EnhancedReviewGenerator instance here
        return cast(EnhancedReviewGenerator, self.review_generator).generate_enhanced_review(
            product_name, search_results, scraped_content
        )
    
    def _generate_enhanced_ai_review(self, product_name: str) -> EnhancedProductReview:
        """Generate AI knowledge review with Nigerian pricing and intelligence"""
        # This calls the base's generate_ai_knowledge_review but then we need to enhance it
        # Actually EnhancedReviewGenerator doesn't override generate_ai_knowledge_review to return EnhancedProductReview
        # It inherits it. So we get a ProductReview.
        # We need a way to upgrade it.
        
        # Wait, I missed the _postprocess_enhanced_review logic in my extraction plan or logic?
        # In app_update.py, _generate_enhanced_ai_review calls self._postprocess_enhanced_review.
        # I need to implement that here or ensure it's in ReviewGenerator.
        # EnhancedProductReviewService should handle this logic as it owns the components.
        
        base_review = self.review_generator.generate_ai_knowledge_review(product_name)
        return self._postprocess_enhanced_review(product_name, base_review)
    
    def _generate_enhanced_hybrid_review(self, product_name: str) -> EnhancedProductReview:
        """Generate hybrid review combining web search data with AI knowledge."""
        try:
            # First attempt: Get web-based review
            search_results = self.search_client.search_products(product_name)
            scraped_content = []
            
            if search_results:
                scraped_content = self.scraper.scrape_content(search_results)
            
            if search_results and scraped_content:
                logger.info(f"Hybrid mode: Using web data for {product_name}")
                return cast(EnhancedReviewGenerator, self.review_generator).generate_enhanced_review(
                    product_name, search_results, scraped_content
                )
            
            # Fallback
            logger.info(f"Hybrid mode: Web data sparse, falling back to AI knowledge for {product_name}")
            base_review = self.review_generator.generate_ai_knowledge_review(product_name)
            return self._postprocess_enhanced_review(product_name, base_review)
            
        except SearchError:
            logger.warning(f"Hybrid mode: Web search failed, using AI knowledge for {product_name}")
            base_review = self.review_generator.generate_ai_knowledge_review(product_name)
            return self._postprocess_enhanced_review(product_name, base_review)

    def _postprocess_enhanced_review(self, product_name: str, base_review: ProductReview) -> EnhancedProductReview:
        """Post-process a base review to add enhanced features (images, sentiment, pricing, etc.)"""
        # This logic effectively duplicates what generate_enhanced_review does but starting from a base review
        # instead of search results.
        
        # Since I moved the logic into EnhancedReviewGenerator.generate_enhanced_review, 
        # I might need to expose a method there to enrich an existing review?
        # Or I can just reproduce the orchestration here since I have access to all components.
        
        # Ideally, I should avoid code duplication.
        # But `generate_enhanced_review` takes search results.
        # Here we have a base review.
        
        # I will reconstruct the enrichment logic here using the components.
        
        # Fetch product images
        logger.info(f"Enriching review with images for: {product_name}")
        product_images = self.image_fetcher.fetch_product_images(product_name, max_images=5)
        
        # Perform sentiment analysis
        logger.info("Analyzing sentiment...")
        sentiment = self.sentiment_analyzer.analyze_review(base_review)
        component_sentiments = self.sentiment_analyzer.analyze_text_components(base_review)
        aspect_breakdown = self.sentiment_analyzer.summarize_aspect_sentiment(base_review, product_name)
        
        # Pricing
        price_comparison = None
        price_naira = None
        original_price_display = None
        
        # Try to parse global price
        global_amount = None
        global_currency = "NGN"
        if base_review.price_info:
            try:
                from core.currency import CurrencyFormatter
                global_amount, global_currency = CurrencyFormatter.parse_price_with_currency(base_review.price_info)
                if global_amount is not None:
                    cf = self.price_service.currency if self.price_service else CurrencyFormatter()
                    price_naira = cf.convert_to_naira(global_amount, global_currency)
                    original_price_display = f"{base_review.price_info.strip()}"
            except Exception:
                pass

        if self.price_service:
            try:
                price_comparison = self.price_service.get_price_comparison(product_name)
                if price_naira is None and price_comparison.lowest_price is not None:
                    price_naira = price_comparison.lowest_price
                    from core.currency import CurrencyFormatter
                    if price_comparison.best_deal_retailer:
                        original_price_display = (
                            f"{CurrencyFormatter.format_naira(price_comparison.lowest_price)} "
                            f"from {price_comparison.best_deal_retailer}"
                        )
            except Exception:
                pass
        
        # Red Flags
        red_flag_report = None
        if self.red_flag_detector:
            try:
                # For AI review which has no scraped content, we use review content?
                # Original code used " ".join([c.content...]) which would be empty for AI review.
                # So we pass empty string or maybe the pros/cons text?
                # Use base_review fields
                review_text = f"{base_review.expert_assessment} {' '.join(base_review.pros)} {' '.join(base_review.cons)}"
                red_flag_report = self.red_flag_detector.analyze_red_flags(
                    product_name, review_text, base_review.pros, base_review.cons
                )
            except Exception:
                pass
        
        # Timing
        timing_advice = None
        if self.timing_advisor:
            try:
                # Build context
                context = f"""
                Product: {product_name}
                Specs: {base_review.specifications_inferred}
                Assessment: {base_review.expert_assessment}
                """
                timing_advice = self.timing_advisor.get_timing_advice(product_name, price_naira, context)
            except Exception:
                pass
        
        # We need to access private methods of review_generator or duplicate their logic.
        # Since they are private (_generate_best_for_tags), I should probably have made them public
        # or static utilities.
        # However, Python doesn't enforce private. I can call them.
        
        rg = cast(EnhancedReviewGenerator, self.review_generator)
        best_for_tags = rg._generate_best_for_tags(base_review)
        budget_tier = rg._determine_budget_tier(price_naira)
        
        # Determine price confidence
        price_confidence = rg._compute_price_confidence(global_amount, price_comparison, price_naira)
        
        # Authentic recommendation
        purchase_recommendation, reasons = rg._compute_purchase_recommendation(
            timing_advice=timing_advice,
            red_flag_report=red_flag_report,
            price_comparison=price_comparison,
            data_quality="limited" # AI knowledge is limited
        )
        
        # Other intelligence
        resale_analysis = None
        video_proof = None
        fake_spotter_report = None
        vox_populi_report = None
        
        # For AI review, we don't have scraped text often, so some analyzers might be skipped or limited
        # But we try anyway
        
        try:
            if self.resale_analyzer:
                resale_analysis = self.resale_analyzer.analyze_resale_value(product_name, price_naira)
        except Exception:
            pass
            
        try:
            if self.video_proof_finder:
                video_proof = self.video_proof_finder.find_video_proofs(
                    product_name, base_review.pros, base_review.cons
                )
        except Exception:
            pass
            
        # Others typically need scraped content text (fake spotter, vox populi)
        # We can skip them or pass empty text
        
        enhanced_review = EnhancedProductReview(
            **base_review.model_dump(),
            sentiment_analysis=sentiment,
            product_images=product_images,
            primary_image_url=product_images[0].url if product_images else None,
            pros_sentiment=component_sentiments['pros_sentiment'],
            cons_sentiment=component_sentiments['cons_sentiment'],
            verdict_sentiment=component_sentiments['verdict_sentiment'],
            aspect_breakdown=aspect_breakdown,
            price_comparison=price_comparison,
            price_naira=price_naira,
            original_price_display=original_price_display,
            price_confidence=price_confidence,
            red_flag_report=red_flag_report,
            timing_advice=timing_advice,
            best_for_tags=best_for_tags,
            budget_tier=budget_tier,
            data_quality="limited",
            alternatives=[],
            resale_analysis=resale_analysis,
            video_proof=video_proof,
            fake_spotter_report=fake_spotter_report, # Likely None
            vox_populi_report=vox_populi_report, # Likely None
            purchase_recommendation=purchase_recommendation,
            purchase_recommendation_reasons=reasons,
            authenticity_note="Source: AI Knowledge (Limited data quality)"
        )
        
        return enhanced_review

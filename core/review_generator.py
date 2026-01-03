"""
AI-powered review and comparison generation services.
"""

import json
import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timezone
from collections import Counter
from pydantic import ValidationError as PydanticValidationError
from groq import Groq

from core.config import AppConfig
from core.models import (
    ProductReview, EnhancedProductReview, ProductComparison, 
    ProductComparisonItem, SearchResult, ScrapedContent, 
    PriceComparison, AlternativeProduct, BestForTag
)
from core.currency import CurrencyFormatter
from core.sentiment import SentimentAnalyzer
from core.scraping import ProductImageFetcher
from core.price_service import NigerianPriceService
from core.analyzers import (
    RedFlagDetector, PurchaseTimingAdvisor, ResaleAnalyzer,
    VideoProofFinder, FakeSpotter, VoxPopuliAnalyzer,
    SmartSwapAnalyzer, NetPriceAnalyzer, DisasterAnalyzer,
    PurchaseTimingAdvice, RedFlagReport
)

logger = logging.getLogger(__name__)


class AIGenerationError(Exception):
    """AI generation related errors"""
    pass


class ValidationError(Exception):
    """Validation related errors"""
    pass


class ComparisonGenerator:
    """Generates side-by-side product comparisons"""
    
    def __init__(self, groq_client: Groq, config: AppConfig):
        self.client = groq_client
        self.config = config
    
    def generate_comparison(self, products: List[EnhancedProductReview]) -> ProductComparison:
        """Generate comparison from multiple product reviews"""
        if len(products) < 2:
            raise ValueError("Need at least 2 products to compare")
        
        comparison_items = []
        
        for product in products:
            item = ProductComparisonItem(
                product_name=product.product_name,
                price_naira=product.price_naira,
                rating=product.predicted_rating,
                pros=product.pros[:5],
                cons=product.cons[:5],
                image_url=product.primary_image_url,
                best_for=[tag.use_case for tag in product.best_for_tags[:3]] if product.best_for_tags else []
            )
            comparison_items.append(item)
        
        # Determine winners by category
        winner_by_category = self._determine_winners(comparison_items)
        
        # Determine best value, budget, premium
        sorted_by_price = sorted(
            [p for p in comparison_items if p.price_naira], 
            key=lambda x: x.price_naira
        )
        
        best_budget = sorted_by_price[0].product_name if sorted_by_price else None
        best_premium = sorted_by_price[-1].product_name if len(sorted_by_price) > 1 else None
        
        # Calculate value scores and determine best value
        best_value = self._determine_best_value(comparison_items)
        
        # Generate AI recommendation
        ai_recommendation = self._generate_ai_recommendation(comparison_items, winner_by_category)
        
        return ProductComparison(
            products=comparison_items,
            comparison_categories=list(winner_by_category.keys()),
            winner_by_category=winner_by_category,
            overall_winner=self._determine_overall_winner(winner_by_category),
            best_value=best_value,
            best_budget=best_budget,
            best_premium=best_premium,
            ai_recommendation=ai_recommendation,
            comparison_date=datetime.now(timezone.utc)
        )
    
    def _determine_winners(self, items: List[ProductComparisonItem]) -> Dict[str, str]:
        """Determine winner for each comparison category (universal + gadget-specific)"""
        import re
        from core.gadget_detector import detect_gadget_category
        
        winners = {}
        
        if not items:
            return winners
        
        # Detect category from first product
        category = detect_gadget_category(items[0].product_name) if items else None
        
        # Price winner (lowest) - UNIVERSAL
        priced_items = [i for i in items if i.price_naira]
        if priced_items:
            winners['Price'] = min(priced_items, key=lambda x: x.price_naira).product_name
        
        # Rating winner - UNIVERSAL
        rated_items = [i for i in items if i.rating and '/' in i.rating]
        if rated_items:
            def extract_rating(item):
                try:
                    return float(item.rating.split('/')[0].strip())
                except:
                    return 0
            winners['Rating'] = max(rated_items, key=extract_rating).product_name
        
        # Features winner (most pros) - UNIVERSAL
        if items:
            winners['Features'] = max(items, key=lambda x: len(x.pros)).product_name
        
        # Reliability winner (fewest cons) - UNIVERSAL
        if items:
            winners['Reliability'] = min(items, key=lambda x: len(x.cons)).product_name
        
        # GADGET-SPECIFIC CATEGORIES
        if category in ['phone', 'laptop', 'tablet']:
            # Battery extraction (mAh)
            def extract_battery(item):
                text = ' '.join(item.pros).lower()
                match = re.search(r'(\d{4,5})\s*mah', text)
                return int(match.group(1)) if match else 0
            
            battery_items = [(i, extract_battery(i)) for i in items]
            battery_items = [(i, b) for i, b in battery_items if b > 0]
            if battery_items:
                winners['Battery'] = max(battery_items, key=lambda x: x[1])[0].product_name
        
        if category == 'phone':
            # Camera extraction (MP)
            def extract_camera(item):
                text = ' '.join(item.pros).lower()
                match = re.search(r'(\d{2,3})\s*mp', text)
                return int(match.group(1)) if match else 0
            
            camera_items = [(i, extract_camera(i)) for i in items]
            camera_items = [(i, c) for i, c in camera_items if c > 0]
            if camera_items:
                winners['Camera'] = max(camera_items, key=lambda x: x[1])[0].product_name
            
            # RAM extraction (GB)
            def extract_ram(item):
                text = ' '.join(item.pros).lower()
                match = re.search(r'(\d{1,2})\s*gb\s*ram', text)
                return int(match.group(1)) if match else 0
            
            ram_items = [(i, extract_ram(i)) for i in items]
            ram_items = [(i, r) for i, r in ram_items if r > 0]
            if ram_items:
                winners['RAM'] = max(ram_items, key=lambda x: x[1])[0].product_name
        
        if category == 'laptop':
            # Processor core extraction
            def extract_cores(item):
                text = ' '.join(item.pros).lower()
                match = re.search(r'(\d{1,2})\s*core', text)
                if not match:
                    match = re.search(r'i(\d)\s', text)  # i5, i7, i9
                return int(match.group(1)) if match else 0
            
            core_items = [(i, extract_cores(i)) for i in items]
            core_items = [(i, c) for i, c in core_items if c > 0]
            if core_items:
                winners['Processor'] = max(core_items, key=lambda x: x[1])[0].product_name
            
            # RAM extraction (GB)
            def extract_ram(item):
                text = ' '.join(item.pros).lower()
                match = re.search(r'(\d{1,2})\s*gb\s*(?:ram|ddr)', text)
                return int(match.group(1)) if match else 0
            
            ram_items = [(i, extract_ram(i)) for i in items]
            ram_items = [(i, r) for i, r in ram_items if r > 0]
            if ram_items:
                winners['RAM'] = max(ram_items, key=lambda x: x[1])[0].product_name
            
            # Storage extraction (GB/TB)
            def extract_storage(item):
                text = ' '.join(item.pros).lower()
                match = re.search(r'(\d+)\s*(?:gb|tb)\s*(?:ssd|nvme|storage)', text)
                if match:
                    val = int(match.group(1))
                    if 'tb' in text:
                        val *= 1000
                    return val
                return 0
            
            storage_items = [(i, extract_storage(i)) for i in items]
            storage_items = [(i, s) for i, s in storage_items if s > 0]
            if storage_items:
                winners['Storage'] = max(storage_items, key=lambda x: x[1])[0].product_name
        
        # Versatility winner (most use cases in best_for) - UNIVERSAL
        items_with_usecases = [i for i in items if i.best_for and len(i.best_for) > 0]
        if items_with_usecases:
            winners['Versatility'] = max(items_with_usecases, key=lambda x: len(x.best_for)).product_name
        
        return winners
    
    def _determine_best_value(self, items: List[ProductComparisonItem]) -> Optional[str]:
        """Determine best value for money with proper 0-10 scoring"""
        if not items:
            return None
        
        # Get price range for normalization
        priced_items = [i for i in items if i.price_naira and i.price_naira > 0]
        if not priced_items:
            return None
        
        max_price = max(i.price_naira for i in priced_items)
        min_price = min(i.price_naira for i in priced_items)
        price_range = max_price - min_price if max_price > min_price else max_price
        
        scored_items = []
        for item in items:
            if item.price_naira and item.rating:
                try:
                    # Extract rating (e.g., "4.2 / 5.0" -> 4.2)
                    rating = float(item.rating.split('/')[0].strip())
                    
                    # Normalize rating to 0-1 (rating out of 5)
                    rating_norm = min(rating / 5.0, 1.0)
                    
                    # Normalize price to 0-1 (lower price = higher score)
                    # Use inverse: (1 - (price - min) / range) gives 1 for cheapest, 0 for most expensive
                    if price_range > 0:
                        price_norm = 1.0 - ((item.price_naira - min_price) / price_range)
                    else:
                        price_norm = 0.5  # All same price
                    
                    # Value Score = weighted combination, scaled to 0-10
                    # 60% rating importance, 40% price importance
                    value_score = (0.6 * rating_norm + 0.4 * price_norm) * 10
                    
                    # Clamp to 0-10 range
                    item.value_score = round(max(0, min(10, value_score)), 1)
                    scored_items.append(item)
                except:
                    continue
        
        if scored_items:
            return max(scored_items, key=lambda x: x.value_score or 0).product_name
        return None
    
    def _determine_overall_winner(self, winners: Dict[str, str]) -> Optional[str]:
        """Determine overall winner based on category wins"""
        if not winners:
            return None
        
        win_counts = Counter(winners.values())
        return win_counts.most_common(1)[0][0]
    
    def _generate_ai_recommendation(self, items: List[ProductComparisonItem], 
                                   winners: Dict[str, str]) -> str:
        """Generate AI-powered detailed recommendation using LLM"""
        if not items:
            return "Unable to generate recommendation."
        
        overall_winner = self._determine_overall_winner(winners)
        
        # Build context for LLM
        products_summary = []
        for item in items:
            price_str = f"₦{item.price_naira:,.0f}" if item.price_naira else "N/A"
            products_summary.append(f"""
**{item.product_name}**:
- Price: {price_str}
- Rating: {item.rating or 'N/A'}
- Value Score: {item.value_score}/10
- Pros: {', '.join(item.pros[:3])}
- Cons: {', '.join(item.cons[:2])}""")
        
        winners_str = ', '.join([f"{cat}: {winner}" for cat, winner in winners.items()])
        
        try:
            prompt = f"""Based on this product comparison, write a brief 2-3 sentence recommendation:

{chr(10).join(products_summary)}

Category winners: {winners_str}
Overall winner by category count: {overall_winner or 'Tie'}

Guidelines:
- Be specific about WHO should buy which product
- Mention value for money
- Highlight the key differentiator
- Keep it under 50 words"""

            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful product comparison advisor. Be concise and actionable."},
                    {"role": "user", "content": prompt}
                ],
                model=self.config.model_name,
                temperature=0.5,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Fallback to simple recommendation
            if overall_winner:
                return f"Based on our analysis, **{overall_winner}** offers the best overall package, " \
                       f"winning in {sum(1 for w in winners.values() if w == overall_winner)} out of " \
                       f"{len(winners)} categories."
            return "Both products have their strengths. Choose based on your priorities."


class ReviewGenerator:
    """Handles AI review generation"""
    
    def __init__(self, groq_client: Groq, config: AppConfig):
        self.client = groq_client
        self.config = config
    
    def generate_web_review(self, product_name: str, search_results: List[SearchResult], 
                          scraped_content: List[ScrapedContent]) -> ProductReview:
        """Generate review from web data"""
        context = self._build_web_context(product_name, search_results, scraped_content)
        
        system_prompt = self._get_web_review_system_prompt()
        user_prompt = self._get_web_review_user_prompt(product_name, context, scraped_content)
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.config.model_name,
                response_format={"type": "json_object"},
                temperature=self.config.temperature_review,
                max_tokens=self.config.max_tokens_review
            )
            
            review_data = json.loads(response.choices[0].message.content)
            validated_review = self._validate_review_data(review_data, scraped_content)
            
            return validated_review
            
        except PydanticValidationError:
            raise
        except Exception as e:
            logger.error(f"AI review generation failed: {e}")
            raise AIGenerationError(f"Failed to generate review: {str(e)}")
    
    def generate_ai_knowledge_review(self, product_name: str) -> ProductReview:
        """Generate review from AI knowledge"""
        return ProductReview.from_ai_knowledge(product_name)
    
    def _build_web_context(self, product_name: str, search_results: List[SearchResult],
                          scraped_content: List[ScrapedContent]) -> str:
        """Build context from web data"""
        context_parts = [f"# Product Review Request: {product_name}\n"]
        
        # Add search results
        context_parts.append("## Search Results:\n")
        for i, result in enumerate(search_results, 1):
            context_parts.append(f"{i}. **{result.title}**")
            context_parts.append(f"   Summary: {result.snippet}")
            context_parts.append(f"   URL: {result.url}\n")
        
        # Add detailed content
        if scraped_content:
            context_parts.append("\n## Detailed Content:\n")
            for i, content in enumerate(scraped_content, 1):
                context_parts.append(f"### Source {i}: {content.title}")
                context_parts.append(f"Content: {content.content[:2000]}...\n")
        
        return "\n".join(context_parts)
    
    def _get_web_review_system_prompt(self) -> str:
        return """You are an expert product reviewer for the NIGERIAN market. Create a comprehensive review STRICTLY from provided sources.

Critical Rules:
1. Use ONLY information from provided sources
2. Be specific - reference actual features/specs found
3. PRICING IS CRITICAL: 
   - Always use Nigerian Naira (₦) prices
   - Prioritize prices from Nigerian retailers (Jumia, Konga, Slot)
   - For older products, use CURRENT resale/market value, NOT original launch price
   - Account for depreciation based on product age
4. Be balanced - mention both strengths and weaknesses
5. Note conflicting information if present
6. NEVER fabricate information
7. Rate fairly based on available information

Output must be valid JSON matching the exact schema."""
    
    def _get_web_review_user_prompt(self, product_name: str, context: str, 
                                   scraped_content: List[ScrapedContent]) -> str:
        sources = [content.url for content in scraped_content]
        
        # Get category-specific instructions
        from core.gadget_detector import get_category_prompt_instructions
        category_instructions = get_category_prompt_instructions(product_name)
        
        return f"""Based on this current web information (gathered on {datetime.now(timezone.utc).strftime('%B %d, %Y')}), create a product review:

{context}

{category_instructions}

Generate JSON with this exact structure:
{{
"product_name": "Full product name from sources",
"specifications_inferred": "Concise summary of key specs found - INCLUDE critical specs for this product category",
"predicted_rating": "CALCULATED SCORE / 5.0. Logic: Start at 5.0. Deduct 0.5 for each MAJOR flaw (red flag). Deduct 0.2 for each minor complaint. Example: 4.3 / 5.0",
"pros": [
    "SPECIFIC strength with measurable claim (e.g., '4500mAh battery lasts 2 days', '12th Gen i7 handles multitasking')",
    "Focus on CRITICAL FEATURES for this product type as specified above",
    "Real advantage mentioned in reviews - cite specific features, numbers, or comparisons",
    "Maximum 5 pros - only include genuinely notable strengths"
],
"cons": [
    "SPECIFIC weakness with detail (e.g., 'Battery only lasts 4 hours', 'Heating issues during gaming')",
    "Focus on CRITICAL FEATURES for this product type as specified above",
    "Include durability concerns if mentioned (repairs, breakage, lifespan)",
    "Maximum 5 cons - only include genuine problems users report"
],
"verdict": "Comprehensive concluding paragraph",
"price_info": "CRITICAL: Use CURRENT Nigerian market price in Naira (₦). For older products, use depreciated resale value, NOT launch price. Prioritize prices from Jumia, Konga, or Slot Nigeria. Format: ₦XXX,XXX - ₦XXX,XXX",
"sources": {json.dumps(sources)},
"last_updated": "{datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
"data_source_type": "free_web_search"
}}

PRICE RULES:
- For 1-2 year old products: Use 60-80% of launch price
- For 2-4 year old products: Use 30-50% of launch price  
- For 4+ year old products: Use 20-35% of launch price
- Always prefer Nigerian retailer prices (Jumia, Konga, Slot) over USD conversions

Be critical and honest. Include issues mentioned in sources."""
    
    def _validate_review_data(self, review_data: Dict, scraped_content: List[ScrapedContent]) -> ProductReview:
        """Validate and clean review data"""
        try:
            # Ensure sources are properly set
            if not review_data.get('sources') and scraped_content:
                review_data['sources'] = [content.url for content in scraped_content]
            
            # Ensure data source type is set
            review_data['data_source_type'] = 'free_web_search'
            review_data['last_updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%d')
            # Backfill expert_assessment from older keys if present
            if 'expert_assessment' not in review_data:
                # older prompts returned a 'verdict' field; accept that as the expert assessment
                if 'verdict' in review_data:
                    review_data['expert_assessment'] = review_data.pop('verdict')
                elif 'summary' in review_data:
                    review_data['expert_assessment'] = review_data.pop('summary')
                else:
                    # Provide a sensible default to satisfy model validation
                    review_data['expert_assessment'] = ""
            
            return ProductReview(**review_data)
            
        except PydanticValidationError as e:
            logger.error(f"Review validation failed: {e}")
            raise ValidationError(f"Invalid review data: {e}")

    def _generate_best_for_tags(self, review: ProductReview) -> List[BestForTag]:
        """Generate 'best for' recommendation tags based on review content"""
        tags = []
        review_text = f"{review.specifications_inferred} {' '.join(review.pros)} {review.verdict}".lower()
        
        # Use case mappings
        use_cases = {
            'gaming': ['gaming', 'game', 'fps', 'graphics', 'refresh rate', 'latency'],
            'work': ['productivity', 'business', 'professional', 'office', 'multitasking'],
            'photography': ['camera', 'photo', 'megapixel', 'lens', 'portrait', 'night mode'],
            'travel': ['portable', 'lightweight', 'battery life', 'compact', 'travel'],
            'students': ['affordable', 'budget', 'student', 'school', 'education'],
            'content creation': ['video', 'editing', 'creator', 'streaming', 'youtube'],
            'fitness': ['health', 'fitness', 'workout', 'exercise', 'heart rate', 'tracking'],
            'music': ['audio', 'sound', 'music', 'bass', 'noise cancellation', 'headphone'],
            'home': ['home', 'kitchen', 'family', 'household', 'living room', 'bedroom', 'appliance', 'cleaning'],
            'outdoor': ['outdoor', 'garden', 'camping', 'patio', 'solar', 'weather', 'waterproof', 'rugged'],
            'energy efficiency': ['power', 'energy', 'saving', 'efficient', 'bill', 'electric', 'inverter', 'eco'],
            'durability': ['durable', 'sturdy', 'tough', 'long-lasting', 'reliable', 'quality']
        }
        
        for use_case, keywords in use_cases.items():
            matches = sum(1 for kw in keywords if kw in review_text)
            if matches >= 2:
                score = min(matches * 0.2, 1.0)
                tags.append(BestForTag(
                    use_case=use_case.title(),
                    score=score,
                    reasoning=f"Strong match based on {matches} relevant features"
                ))
        
        # Sort by score and return top 5
        return sorted(tags, key=lambda x: x.score, reverse=True)[:5]
    
    def _determine_budget_tier(self, price_naira: Optional[float]) -> str:
        """Determine budget tier based on Nigerian Naira price"""
        if price_naira is None:
            return "mid-range"
        
        # Nigerian market price tiers (in Naira)
        if price_naira < 100000:  # Under ₦100k
            return "budget"
        elif price_naira < 300000:  # ₦100k - ₦300k
            return "mid-range"
        elif price_naira < 800000:  # ₦300k - ₦800k
            return "premium"
        else:  # Over ₦800k
            return "flagship"


class EnhancedReviewGenerator(ReviewGenerator):
    """Review generator with sentiment analysis, images, Nigerian pricing, and intelligence features"""
    
    def __init__(self, groq_client: Groq, config: AppConfig, 
                 sentiment_analyzer: SentimentAnalyzer,
                 image_fetcher: ProductImageFetcher,
                 price_service: Optional[NigerianPriceService] = None,
                 red_flag_detector: Optional[RedFlagDetector] = None,
                 timing_advisor: Optional[PurchaseTimingAdvisor] = None,
                 resale_analyzer: Optional[ResaleAnalyzer] = None,
                 video_finder: Optional[VideoProofFinder] = None,
                 fake_spotter: Optional[FakeSpotter] = None,
                 vox_analyzer: Optional[VoxPopuliAnalyzer] = None,
                 smart_swap_analyzer: Optional[SmartSwapAnalyzer] = None,
                 net_price_analyzer: Optional[NetPriceAnalyzer] = None,
                 disaster_analyzer: Optional[DisasterAnalyzer] = None):
        super().__init__(groq_client, config)
        self.sentiment_analyzer = sentiment_analyzer
        self.image_fetcher = image_fetcher
        self.price_service = price_service
        self.red_flag_detector = red_flag_detector
        self.timing_advisor = timing_advisor
        self.resale_analyzer = resale_analyzer
        self.video_finder = video_finder
        self.fake_spotter = fake_spotter
        self.vox_analyzer = vox_analyzer
        self.smart_swap_analyzer = smart_swap_analyzer
        self.net_price_analyzer = net_price_analyzer
        self.disaster_analyzer = disaster_analyzer
    
    def generate_enhanced_review(self, product_name: str, search_results: List[SearchResult],
                                scraped_content: List[ScrapedContent]) -> EnhancedProductReview:
        """Generate review with sentiment analysis, images, Nigerian prices, and intelligence"""
        
        # Generate base review
        base_review = super().generate_web_review(product_name, search_results, scraped_content)
        
        # Fetch product images
        logger.info("Fetching product images...")
        product_images = self.image_fetcher.fetch_product_images(product_name, max_images=5)
        
        # Perform sentiment analysis
        logger.info("Analyzing sentiment...")
        sentiment = self.sentiment_analyzer.analyze_review(base_review)
        component_sentiments = self.sentiment_analyzer.analyze_text_components(base_review)
        aspect_breakdown = self.sentiment_analyzer.summarize_aspect_sentiment(base_review, product_name)
        
        # Derive primary price from the review's price_info (any currency), then convert to Naira
        price_comparison: Optional[PriceComparison] = None
        price_naira: Optional[float] = None
        original_price_display: Optional[str] = None

        # 1) Try to parse and convert whatever price the model surfaced
        global_amount: Optional[float] = None
        global_currency: str = "NGN"
        if base_review.price_info:
            try:
                global_amount, global_currency = CurrencyFormatter.parse_price_with_currency(base_review.price_info)
                if global_amount is not None:
                    cf = self.price_service.currency if self.price_service else CurrencyFormatter()
                    price_naira = cf.convert_to_naira(global_amount, global_currency)
                    original_price_display = f"{base_review.price_info.strip()}"
            except Exception as e:
                logger.warning(f"Global price parse/convert failed: {e}")

        # 2) Optionally enrich with Nigerian retailer-specific prices (if available)
        if self.price_service:
            logger.info("Fetching Nigerian retailer prices...")
            try:
                price_comparison = self.price_service.get_price_comparison(product_name)
                # If we didn't already set price_naira from global price, fall back to best local price
                if price_naira is None and price_comparison.lowest_price is not None:
                    price_naira = price_comparison.lowest_price
                    # For local-only data, show best retailer in "original" display
                    if price_comparison.best_deal_retailer and price_comparison.lowest_price is not None:
                        original_price_display = (
                            f"{CurrencyFormatter.format_naira(price_comparison.lowest_price)} "
                            f"from {price_comparison.best_deal_retailer}"
                        )
            except Exception as e:
                logger.warning(f"Price fetching failed: {e}")
        
        # Analyze red flags
        red_flag_report = None
        if self.red_flag_detector:
            logger.info("Analyzing red flags...")
            try:
                scraped_text = " ".join([c.content for c in scraped_content])
                red_flag_report = self.red_flag_detector.analyze_red_flags(
                    product_name, scraped_text, base_review.pros, base_review.cons
                )
            except Exception as e:
                logger.warning(f"Red flag analysis failed: {e}")
        
        # Get timing advice
        timing_advice = None
        if self.timing_advisor:
            logger.info("Generating purchase timing advice...")
            try:
                timing_advice = self.timing_advisor.get_timing_advice(product_name, price_naira)
            except Exception as e:
                logger.warning(f"Timing advice failed: {e}")
        
        # Generate best-for tags
        best_for_tags = self._generate_best_for_tags(base_review)
        
        # Determine budget tier
        budget_tier = self._determine_budget_tier(price_naira)

        # Data quality assessment
        data_quality = self._assess_data_quality(search_results, scraped_content)

        # Price confidence label
        price_confidence = self._compute_price_confidence(
            global_amount=global_amount,
            price_comparison=price_comparison,
            price_naira=price_naira,
        )

        # Alternative products (lightweight suggestions based on search results)
        alternatives = self._select_alternatives(product_name, search_results)
        
        # === NEW: Compute authentic recommendation fields ===
        
        # Get recommended retailer (balancing price and trust)
        recommended_retailer = None
        if self.price_service and price_comparison:
            recommended_retailer = self.price_service.get_recommended_retailer(price_comparison)
        
        # Compute ranked strengths and weaknesses (use scraped content + aspect breakdown for accuracy)
        top_strengths = self._rank_strengths(base_review.pros, scraped_content, aspect_breakdown)
        main_weaknesses = self._rank_weaknesses(base_review.cons, scraped_content, aspect_breakdown)

        # Optionally consolidate / dedupe using the LLM (best-effort)
        try:
            if getattr(self.config, 'enable_llm_consolidation', False):
                top_strengths = self._consolidate_with_llm(top_strengths, role='pros', product_name=product_name)
                main_weaknesses = self._consolidate_with_llm(main_weaknesses, role='cons', product_name=product_name)
        except Exception as e:
            logger.warning(f"LLM consolidation step failed: {e}")
        
        # Compute purchase recommendation
        purchase_recommendation, recommendation_reasons = self._compute_purchase_recommendation(
            timing_advice=timing_advice,
            red_flag_report=red_flag_report,
            price_comparison=price_comparison,
            data_quality=data_quality
        )
        
        # Build data authenticity note
        data_authenticity_note = self._build_authenticity_note(
            data_source_type=base_review.data_source_type,
            data_quality=data_quality,
            price_confidence=price_confidence,
            num_sources=len(base_review.sources),
            num_retailers=len(price_comparison.prices) if price_comparison else 0
        )
        
        # === Compose additional intelligence outputs ===
        all_content_text = " ".join([c.content for c in scraped_content if c and c.content])

        resale_analysis = None
        video_proof = None
        fake_spotter_report = None
        vox_populi_report = None
        smart_swap_report = None
        net_price_report = None
        what_if_report = None

        try:
            if self.resale_analyzer:
                resale_analysis = self.resale_analyzer.analyze_resale_value(product_name, price_naira)
        except Exception as e:
            logger.warning(f"Resale analyzer failed: {e}")

        try:
            if self.video_finder:
                video_proof = self.video_finder.find_video_proofs(product_name, base_review.pros, base_review.cons)
        except Exception as e:
            logger.warning(f"Video proof finder failed: {e}")

        try:
            if self.fake_spotter:
                fake_spotter_report = self.fake_spotter.analyze_authenticity(product_name, all_content_text)
        except Exception as e:
            logger.warning(f"Fake spotter failed: {e}")

        try:
            if self.vox_analyzer:
                vox_populi_report = self.vox_analyzer.analyze_owner_sentiment(product_name, all_content_text)
        except Exception as e:
            logger.warning(f"Vox Populi analyzer failed: {e}")

        try:
            if self.smart_swap_analyzer:
                smart_swap_report = self.smart_swap_analyzer.analyze_swap_options(product_name, price_naira or 0)
        except Exception as e:
            logger.warning(f"Smart swap analyzer failed: {e}")

        try:
            if self.net_price_analyzer:
                net_price_report = self.net_price_analyzer.calculate_net_price(product_name, price_naira or 0)
        except Exception as e:
            logger.warning(f"Net price analyzer failed: {e}")

        try:
            if self.disaster_analyzer:
                what_if_report = self.disaster_analyzer.simulate_disasters(product_name, base_review.specifications_inferred)
        except Exception as e:
            logger.warning(f"Disaster analyzer failed: {e}")

        # Create enhanced review
        enhanced_review = EnhancedProductReview(
            **base_review.model_dump(),
            sentiment_analysis=sentiment,
            product_images=product_images,
            primary_image_url=product_images[0].url if product_images else None,
            pros_sentiment=component_sentiments['pros_sentiment'],
            cons_sentiment=component_sentiments['cons_sentiment'],
            verdict_sentiment=component_sentiments['verdict_sentiment'],
            aspect_breakdown=aspect_breakdown,
            # Pricing story
            price_comparison=price_comparison,
            price_naira=price_naira,
            original_price_display=original_price_display,
            price_confidence=price_confidence,
            # Red flags and timing
            red_flag_report=red_flag_report,
            timing_advice=timing_advice,
            # Best for tags
            best_for_tags=best_for_tags,
            budget_tier=budget_tier,
            # Data quality and alternatives
            data_quality=data_quality,
            alternatives=alternatives,
            # Intelligence outputs
            resale_analysis=resale_analysis,
            video_proof=video_proof,
            fake_spotter_report=fake_spotter_report,
            vox_populi_report=vox_populi_report,
            smart_swap_report=smart_swap_report,
            net_price_report=net_price_report,
            what_if_report=what_if_report,
            # === NEW: Authentic recommendation fields ===
            purchase_recommendation=purchase_recommendation,
            purchase_recommendation_reasons=recommendation_reasons,
            top_strengths=top_strengths,
            main_weaknesses=main_weaknesses,
            recommended_retailer=recommended_retailer,
            data_authenticity_note=data_authenticity_note,
        )
        
        return enhanced_review
    
    def _assess_data_quality(
        self,
        search_results: List[SearchResult],
        scraped_content: List[ScrapedContent],
    ) -> str:
        """Very simple heuristic data-quality assessment."""
        if not search_results or not scraped_content:
            return "poor"

        total_chars = sum(len(c.content) for c in scraped_content)
        if len(search_results) >= 3 and total_chars > 4000:
            return "good"
        if total_chars > 1000:
            return "limited"
        return "poor"

    def _compute_price_confidence(
        self,
        global_amount: Optional[float],
        price_comparison: Optional[PriceComparison],
        price_naira: Optional[float],
    ) -> str:
        """Determine high/medium/low confidence in the price story."""
        has_global = global_amount is not None
        has_local = bool(price_comparison and price_comparison.prices)
        local_count = len(price_comparison.prices) if price_comparison and price_comparison.prices else 0

        if has_global and local_count >= 2 and price_naira is not None:
            return "high"
        if has_global or has_local:
            return "medium"
        return "low"

    def _compute_purchase_recommendation(
        self,
        timing_advice: Optional[PurchaseTimingAdvice] = None,
        red_flag_report: Optional[RedFlagReport] = None,
        price_comparison: Optional[PriceComparison] = None,
        data_quality: Optional[str] = None,
    ) -> Tuple[str, List[str]]:
        """Heuristic purchase recommendation generator."""
        reasons: List[str] = []

        # If there are critical red flags, avoid buying
        if red_flag_report and red_flag_report.has_critical_issues:
            reasons.append("Critical issues reported in user data or recalls")
            return "avoid", reasons

        # Use timing advice if present
        if timing_advice:
            if timing_advice.recommendation == 'buy_now':
                reasons.append(f"Timing advice: {timing_advice.reasoning}")
                return 'buy_now', reasons
            if timing_advice.recommendation == 'wait':
                reasons.append(f"Timing advice: {timing_advice.reasoning}")
                return 'wait', reasons

        # Price signal: if a clear low local price exists, encourage buying
        try:
            if price_comparison and price_comparison.lowest_price is not None:
                if price_comparison.deal_quality in (None, 'excellent'):
                    reasons.append('Good local deal available')
                    return 'buy_now', reasons
        except Exception:
            pass

        # Data quality fallback
        if data_quality == 'good':
            reasons.append('Sufficient high-quality sources available')
            return 'buy_now', reasons
        if data_quality == 'limited':
            reasons.append('Some coverage found; consider waiting for better deals')
            return 'consider_alternatives', reasons

        # Default conservative recommendation
        reasons.append('Insufficient up-to-date data; consider alternatives or wait for more information')
        return 'consider_alternatives', reasons

    def _select_alternatives(
        self,
        product_name: str,
        search_results: List[SearchResult],
    ) -> List[AlternativeProduct]:
        """Pick 2-3 plausible alternative products from search results."""
        base = product_name.lower()
        alts: List[AlternativeProduct] = []
        for result in search_results[:6]:
            title_lower = result.title.lower()
            # Skip exact-match titles
            if base in title_lower or title_lower in base:
                continue
            reason = "Similar product from same category or brand"
            alts.append(
                AlternativeProduct(
                    product_name=result.title.strip(),
                    url=result.url,
                    snippet=result.snippet,
                    reason=reason,
                )
            )
            if len(alts) >= 3:
                break
        return alts

    def _build_authenticity_note(self, data_source_type: str = 'web_search', data_quality: str = None,
                                 price_confidence: str = None, num_sources: int = 0, num_retailers: int = 0) -> str:
        """Create a short authenticity / provenance note for the enhanced review."""
        parts = []
        parts.append(f"Data source: {data_source_type}")
        if data_quality:
            parts.append(f"Data quality: {data_quality}")
        if price_confidence:
            parts.append(f"Price confidence: {price_confidence}")
        if num_sources:
            parts.append(f"Sources used: {num_sources}")
        if num_retailers:
            parts.append(f"Retailers checked: {num_retailers}")

        return "; ".join(parts)

    def _rank_strengths(self, pros: List[str], scraped_content: List[ScrapedContent], aspect_breakdown: List[Dict[str, Any]] = None) -> List[str]:
        """Rank and return the top strengths (pros) with improved accuracy."""
        if not pros:
            return []

        # Precompute mention counts across scraped content
        mention_counts = {}
        all_text = "\n".join([c.content for c in (scraped_content or [])]).lower()
        for p in pros:
            if not p:
                mention_counts[p] = 0
                continue
            mention_counts[p] = all_text.count(p.lower())

        # Build aspect relevance map for quick lookup
        aspect_map = {}
        if aspect_breakdown:
            for a in aspect_breakdown:
                name = a.get('aspect', '').lower()
                aspect_map[name] = a.get('mentions', 0)

        # Compute raw scores
        scored: List[Tuple[float, str]] = []
        max_mentions = max(mention_counts.values()) if mention_counts else 1
        for p in pros:
            text = (p or "").strip()
            if not text:
                continue

            # Sentiment score
            try:
                if self.sentiment_analyzer:
                    sentiment = float(self.sentiment_analyzer._analyze_text(text))
                else:
                    sentiment = 1.0 if any(t in text.lower() for t in getattr(self.sentiment_analyzer, 'positive_terms', [])) else 0.0
            except Exception:
                sentiment = 0.0

            # Normalize mention score
            mentions = mention_counts.get(p, 0)
            mention_score = mentions / max_mentions if max_mentions > 0 else 0.0

            # Aspect relevance
            aspect_score = 0.0
            try:
                for aspect_name, mentions_count in aspect_map.items():
                    if aspect_name and aspect_name in text.lower():
                        aspect_score += min(1.0, mentions_count / 5.0)
            except Exception:
                aspect_score = 0.0

            sw = getattr(self.config, 'sentiment_weight', 0.6)
            mw = getattr(self.config, 'mention_weight', 0.25)
            aw = getattr(self.config, 'aspect_weight', 0.15)

            score = (sw * sentiment) + (mw * mention_score) + (aw * aspect_score)
            score += min(len(text) / 500.0, 0.1)

            scored.append((score, text))

        scored.sort(key=lambda x: x[0], reverse=True)
        out: List[str] = []
        seen = set()
        for _, s in scored:
            if s not in seen:
                seen.add(s)
                out.append(s)
            if len(out) >= 5:
                break

        return out

    def _rank_weaknesses(self, cons: List[str], scraped_content: List[ScrapedContent], aspect_breakdown: List[Dict[str, Any]] = None) -> List[str]:
        """Rank and return the main weaknesses (cons) with improved accuracy."""
        if not cons:
            return []

        # Precompute mention counts
        mention_counts = {}
        all_text = "\n".join([c.content for c in (scraped_content or [])]).lower()
        for c in cons:
            mention_counts[c] = all_text.count((c or "").lower())

        aspect_map = {}
        if aspect_breakdown:
            for a in aspect_breakdown:
                name = a.get('aspect', '').lower()
                aspect_map[name] = a.get('mentions', 0)

        max_mentions = max(mention_counts.values()) if mention_counts else 1
        scored: List[Tuple[float, str]] = []
        for c in cons:
            text = (c or "").strip()
            if not text:
                continue

            # Severity: invert compound sentiment
            try:
                if self.sentiment_analyzer:
                    sentiment = float(self.sentiment_analyzer._analyze_text(text))
                else:
                    sentiment = 0.0
            except Exception:
                sentiment = 0.0
            severity = max(0.0, -sentiment)

            mentions = mention_counts.get(c, 0)
            mention_score = mentions / max_mentions if max_mentions > 0 else 0.0

            aspect_score = 0.0
            try:
                for aspect_name, mentions_count in aspect_map.items():
                    if aspect_name and aspect_name in text.lower():
                        aspect_score += min(1.0, mentions_count / 5.0)
            except Exception:
                aspect_score = 0.0

            sw = getattr(self.config, 'sentiment_weight', 0.6)
            mw = getattr(self.config, 'mention_weight', 0.25)
            aw = getattr(self.config, 'aspect_weight', 0.15)

            score = (sw * severity) + (mw * mention_score) + (aw * aspect_score)
            score += min(len(text) / 500.0, 0.1)

            scored.append((score, text))

        scored.sort(key=lambda x: x[0], reverse=True)
        out: List[str] = []
        seen = set()
        for _, s in scored:
            if s not in seen:
                seen.add(s)
                out.append(s)
            if len(out) >= 5:
                break
        return out

    def _consolidate_with_llm(self, items: List[str], role: str = 'pros', product_name: str = None) -> List[str]:
        """Optionally consolidate semantically similar items using the LLM."""
        try:
            if not getattr(self.config, 'enable_llm_consolidation', False):
                return items
            if not items:
                return items

            prompt = f"""
            You are an assistant that consolidates and ranks {role} statements about a product.
            Product: {product_name or 'Unknown'}
            Input: A JSON array of short statements (may contain duplicates or near-duplicates).

            Task:
            1) Merge semantically similar statements into a single concise statement.
            2) Remove duplicates and trivial items.
            3) Rank the resulting statements by importance/relevance (most important first).
            4) Return a JSON array of at most 5 strings, in order of importance.

            Input items:
            {json.dumps(items, ensure_ascii=False)}

            Output exactly a JSON array of strings, e.g. ["Strong battery life", "Excellent camera"]
            """

            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a concise summarizer and ranker."},
                    {"role": "user", "content": prompt}
                ],
                model=self.config.model_name,
                temperature=getattr(self.config, 'consolidation_temperature', 0.2),
                max_tokens=getattr(self.config, 'consolidation_max_tokens', 400),
                response_format={"type": "json_object"}
            )

            content = completion.choices[0].message.content
            if not content:
                return items
            data = json.loads(content)
            if isinstance(data, list):
                # ensure results are strings and non-empty
                results = [str(x).strip() for x in data if x and str(x).strip()]
                return results[:5]
        except Exception as e:
            logger.warning(f"LLM consolidation failed: {e}")
        return items

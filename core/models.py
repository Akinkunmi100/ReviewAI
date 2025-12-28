"""
Data models for the Product Review Engine.

Contains all Pydantic models used throughout the application.
"""

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Tuple, Union
from pydantic import BaseModel, Field

from core.currency import CurrencyFormatter


# =============================================================================
# BASE DATA MODELS
# =============================================================================

class SearchResult(BaseModel):
    """Model for search results"""
    title: str
    url: str
    snippet: str
    domain: str = Field(default="", description="Domain of the URL")


class ScrapedContent(BaseModel):
    """Model for scraped web content"""
    url: str
    title: str
    content: str
    content_length: int
    scrape_timestamp: datetime


class ProductReview(BaseModel):
    """A comprehensive product review based on real web data."""
    product_name: str = Field(description="The full name of the product being reviewed.")
    specifications_inferred: str = Field(description="A concise summary of key technical specs.")
    predicted_rating: str = Field(description="A critical rating out of 5.0 (e.g., '4.6 / 5.0').")
    pros: List[str] = Field(description="A list of strengths and advantages.")
    cons: List[str] = Field(description="A list of weaknesses, trade-offs, or user pain points.")
    expert_assessment: str = Field(description="Professional assessment of the product's overall value proposition.")
    price_info: str = Field(default="Price not available", description="Current pricing information if found.")
    sources: List[str] = Field(default=[], description="List of source URLs used.")
    last_updated: str = Field(default="", description="Date when information was gathered.")
    data_source_type: str = Field(default="web_search", description="Type of data source used.")
    
    @property
    def verdict(self) -> str:
        """Alias for expert_assessment (backward compatibility)"""
        return self.expert_assessment
    
    @property
    def summary(self) -> str:
        """Alias for expert_assessment"""
        return self.expert_assessment
    
    @classmethod
    def from_ai_knowledge(cls, product_name: str) -> 'ProductReview':
        """Create a placeholder for AI knowledge-based reviews"""
        return cls(
            product_name=product_name,
            specifications_inferred="Based on AI training data (updated January 2025)",
            predicted_rating="N/A (AI Knowledge)",
            pros=["Information from AI training data"],
            cons=["May not reflect current specifications or pricing"],
            expert_assessment="This review is based on AI training data. Please verify current information.",
            price_info="Price varies - check current retailers",
            sources=["AI Training Data (Updated January 2025)"],
            last_updated=datetime.now(timezone.utc).strftime('%Y-%m-%d'),
            data_source_type="ai_knowledge"
        )


# =============================================================================
# SENTIMENT & IMAGE MODELS
# =============================================================================

class SentimentScore(BaseModel):
    """Detailed sentiment analysis scores"""
    overall_sentiment: str = Field(description="Overall sentiment: Positive, Negative, or Mixed")
    polarity_score: float = Field(ge=-1.0, le=1.0, description="Polarity: -1 (negative) to 1 (positive)")
    subjectivity_score: float = Field(ge=0.0, le=1.0, description="Subjectivity: 0 (objective) to 1 (subjective)")
    compound_score: float = Field(ge=-1.0, le=1.0, description="VADER compound score")
    positive_ratio: float = Field(ge=0.0, le=1.0, description="Positive sentiment ratio")
    negative_ratio: float = Field(ge=0.0, le=1.0, description="Negative sentiment ratio")
    neutral_ratio: float = Field(ge=0.0, le=1.0, description="Neutral sentiment ratio")
    sentiment_confidence: float = Field(ge=0.0, le=1.0, description="Confidence in sentiment assessment")
    emotional_tone: str = Field(description="Dominant emotional tone")
    key_positive_aspects: List[str] = Field(default=[], description="Most positive aspects")
    key_negative_aspects: List[str] = Field(default=[], description="Most negative aspects")
    
    @property
    def sentiment_emoji(self) -> str:
        """Get emoji representation of sentiment"""
        if self.compound_score >= 0.5:
            return "😊"
        elif self.compound_score >= 0.1:
            return "🙂"
        elif self.compound_score >= -0.1:
            return "😐"
        elif self.compound_score >= -0.5:
            return "😕"
        else:
            return "😞"
    
    @property
    def sentiment_color(self) -> str:
        """Get color code for sentiment"""
        if self.compound_score >= 0.5:
            return "#4CAF50"
        elif self.compound_score >= 0.1:
            return "#8BC34A"
        elif self.compound_score >= -0.1:
            return "#FFC107"
        elif self.compound_score >= -0.5:
            return "#FF9800"
        else:
            return "#F44336"


class ProductImage(BaseModel):
    """Product image information"""
    url: str
    thumbnail_url: Optional[str] = None
    source: str
    width: Optional[int] = None
    height: Optional[int] = None
    alt_text: Optional[str] = None


# =============================================================================
# PRICE & COMPARISON MODELS
# =============================================================================

class RetailerPrice(BaseModel):
    """Price from a single Nigerian retailer"""
    retailer_id: str = Field(description="Retailer identifier")
    retailer_name: str = Field(description="Display name of retailer")
    price_naira: Optional[float] = Field(default=None, description="Price in Naira")
    original_price: Optional[float] = Field(default=None, description="Original price before discount")
    discount_percent: Optional[float] = Field(default=None, description="Discount percentage")
    product_url: str = Field(default="", description="Direct link to product page")
    in_stock: bool = Field(default=True, description="Whether product is in stock")
    last_checked: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    seller_rating: Optional[float] = Field(default=None, description="Seller rating if available")
    
    @property
    def formatted_price(self) -> str:
        """Get formatted Naira price"""
        if self.price_naira is None:
            return "Price unavailable"
        return CurrencyFormatter.format_naira(self.price_naira)
    
    @property
    def has_discount(self) -> bool:
        return self.discount_percent is not None and self.discount_percent > 0


class PriceComparison(BaseModel):
    """Multi-retailer price comparison for a product"""
    product_name: str
    prices: List[RetailerPrice] = Field(default=[], description="Prices from different retailers")
    lowest_price: Optional[float] = Field(default=None, description="Lowest price found")
    highest_price: Optional[float] = Field(default=None, description="Highest price found")
    average_price: Optional[float] = Field(default=None, description="Average price across retailers")
    best_deal_retailer: Optional[str] = Field(default=None, description="Retailer with best price")
    price_last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    currency: str = Field(default="NGN")
    deal_quality: Optional[str] = Field(default=None, description="excellent, good, normal, poor")
    deal_explanation: Optional[str] = Field(default=None)
    
    @property
    def price_range_display(self) -> str:
        """Display price range in Naira"""
        if self.lowest_price is None:
            return "Prices unavailable"
        if self.lowest_price == self.highest_price:
            return CurrencyFormatter.format_naira(self.lowest_price)
        return f"{CurrencyFormatter.format_naira(self.lowest_price)} - {CurrencyFormatter.format_naira(self.highest_price)}"
    
    @property
    def savings_potential(self) -> Optional[float]:
        """Potential savings between highest and lowest price"""
        if self.lowest_price and self.highest_price:
            return self.highest_price - self.lowest_price
        return None
    
    def get_sorted_prices(self, ascending: bool = True) -> List[RetailerPrice]:
        """Get prices sorted by amount"""
        valid_prices = [p for p in self.prices if p.price_naira is not None]
        return sorted(valid_prices, key=lambda x: x.price_naira, reverse=not ascending)


# =============================================================================
# RED FLAG & RISK MODELS
# =============================================================================

class RedFlag(BaseModel):
    """Individual red flag/warning about a product"""
    severity: str = Field(description="Severity level: high, medium, low")
    category: str = Field(description="Category: defect, fake_reviews, warranty, recall, reliability")
    title: str = Field(description="Short title of the issue")
    description: str = Field(description="Detailed description")
    source: Optional[str] = Field(default=None, description="Source of information")
    affected_percentage: Optional[float] = Field(default=None, description="% of users affected")
    
    @property
    def severity_emoji(self) -> str:
        if self.severity == "high":
            return "🚨"
        elif self.severity == "medium":
            return "⚠️"
        return "ℹ️"
    
    @property
    def severity_color(self) -> str:
        if self.severity == "high":
            return "#F44336"
        elif self.severity == "medium":
            return "#FF9800"
        return "#2196F3"


class RedFlagReport(BaseModel):
    """Complete red flag analysis for a product"""
    product_name: str
    red_flags: List[RedFlag] = Field(default=[])
    overall_risk_level: str = Field(default="low", description="Overall risk: high, medium, low")
    risk_score: float = Field(default=0.0, ge=0.0, le=10.0, description="Risk score 0-10")
    fake_review_score: Optional[float] = Field(default=None, description="Fake review likelihood 0-1")
    common_complaints: List[str] = Field(default=[], description="Most common user complaints")
    recommendation: str = Field(default="", description="Purchase recommendation based on risks")
    
    @property
    def has_critical_issues(self) -> bool:
        return any(flag.severity == "high" for flag in self.red_flags)
    
    @property
    def risk_emoji(self) -> str:
        if self.overall_risk_level == "high":
            return "🚨"
        elif self.overall_risk_level == "medium":
            return "⚠️"
        return "✅"


# =============================================================================
# TIMING & RECOMMENDATION MODELS
# =============================================================================

class PurchaseTimingAdvice(BaseModel):
    """Purchase timing intelligence"""
    product_name: str
    lifecycle_stage: str = Field(description="Stage: new, mature, end_of_life, successor_announced")
    recommendation: str = Field(description="buy_now, wait, consider_alternatives")
    reasoning: str = Field(description="Explanation for the recommendation")
    new_model_expected: bool = Field(default=False)
    expected_release_window: Optional[str] = Field(default=None, description="e.g., 'Q2 2025'")
    best_sale_periods: List[str] = Field(default=[], description="Best times to buy")
    current_deal_quality: str = Field(default="normal", description="excellent, good, normal, poor")
    price_trend: str = Field(default="stable", description="rising, stable, falling")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    
    @property
    def recommendation_emoji(self) -> str:
        if self.recommendation == "buy_now":
            return "✅"
        elif self.recommendation == "wait":
            return "⏳"
        return "🤔"
    
    @property
    def lifecycle_emoji(self) -> str:
        stages = {
            "new": "🆕",
            "mature": "✅",
            "end_of_life": "⚠️",
            "successor_announced": "📢"
        }
        return stages.get(self.lifecycle_stage, "❓")


class BestForTag(BaseModel):
    """'Best for' recommendation tag"""
    use_case: str = Field(description="e.g., gaming, travel, work, photography")
    score: float = Field(ge=0.0, le=1.0, description="Suitability score 0-1")
    reasoning: str = Field(default="", description="Why it's good for this use case")
    
    @property
    def score_display(self) -> str:
        if self.score >= 0.8:
            return "⭐⭐⭐"
        elif self.score >= 0.6:
            return "⭐⭐"
        elif self.score >= 0.4:
            return "⭐"
        return ""


class UserProfile(BaseModel):
    """Simple personalization profile for the current user/session"""
    min_budget: Optional[float] = Field(default=None, description="Minimum budget in Naira")
    max_budget: Optional[float] = Field(default=None, description="Maximum budget in Naira")
    use_cases: List[str] = Field(default_factory=list, description="Preferred use cases")
    preferred_brands: List[str] = Field(default_factory=list, description="Brands user prefers")
    avoided_brands: List[str] = Field(default_factory=list, description="Brands to avoid")


# =============================================================================
# COMPARISON & ALTERNATIVE MODELS
# =============================================================================

class ProductComparisonItem(BaseModel):
    """Single product in a comparison"""
    product_name: str
    price_naira: Optional[float] = None
    rating: Optional[str] = None
    specs: Dict[str, str] = Field(default={})
    pros: List[str] = Field(default=[])
    cons: List[str] = Field(default=[])
    image_url: Optional[str] = None
    best_for: List[str] = Field(default=[])
    value_score: Optional[float] = Field(default=None, ge=0.0, le=10.0)


class ProductComparison(BaseModel):
    """Side-by-side product comparison"""
    products: List[ProductComparisonItem] = Field(default=[], max_length=4)
    comparison_categories: List[str] = Field(default=[], description="Categories compared")
    winner_by_category: Dict[str, str] = Field(default={}, description="Winner for each category")
    overall_winner: Optional[str] = Field(default=None)
    best_value: Optional[str] = Field(default=None, description="Best value for money")
    best_budget: Optional[str] = Field(default=None, description="Best budget option")
    best_premium: Optional[str] = Field(default=None, description="Best premium option")
    ai_recommendation: str = Field(default="", description="AI's recommendation")
    comparison_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AlternativeProduct(BaseModel):
    """Lightweight suggestion for alternative products"""
    product_name: str
    url: str
    snippet: str = ""
    reason: str = ""


class RecommendedRetailer(BaseModel):
    """Recommended retailer balancing price and trust/quality"""
    retailer_name: str = Field(description="Name of the recommended retailer")
    retailer_id: str = Field(description="Retailer identifier")
    price_naira: Optional[float] = Field(default=None, description="Price at this retailer")
    product_url: str = Field(default="", description="Direct link to product page")
    trust_score: int = Field(default=3, ge=1, le=5, description="Trust score 1-5")
    trust_note: str = Field(default="", description="Why this retailer is trustworthy")
    recommendation_reason: str = Field(default="", description="Why we recommend this retailer")
    
    @property
    def formatted_price(self) -> str:
        if self.price_naira is None:
            return "Price unavailable"
        return CurrencyFormatter.format_naira(self.price_naira)


class ResaleAnalysis(BaseModel):
    """Resale value analysis for a product"""
    product_name: str
    estimated_resale_value: Optional[float] = Field(default=None, description="Estimated resale in Naira")
    resale_percentage: Optional[float] = Field(default=None, description="Percentage of original price")
    depreciation_rate: Optional[str] = Field(default=None, description="slow, moderate, fast")
    resale_confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    best_resale_platforms: List[str] = Field(default=[], description="Best platforms to resell")
    resale_tips: List[str] = Field(default=[], description="Tips for maximizing resale value")
    
    # Allow loose mapping
    class Config:
        extra = "ignore"


# =============================================================================
# NEW INTELLIGENCE MODELS (VIDEO, FAKE SPOTTER, ETC.)
# =============================================================================

class VideoMoment(BaseModel):
    label: str
    search_query: str
    youtube_url: str
    description: str

class VideoProof(BaseModel):
    moments: List[VideoMoment] = Field(default=[])

class AuthenticityCheck(BaseModel):
    check_type: str
    instruction: str
    expected_result: str
    warning_sign: str = ""

class FakeSpotterReport(BaseModel):
    risk_level: str
    common_scams: List[str] = Field(default=[])
    verification_steps: List[AuthenticityCheck] = Field(default=[])

class ForumOpinion(BaseModel):
    platform: str
    sentiment: str
    key_takeaway: str

class VoxPopuliReport(BaseModel):
    owner_verdict: str
    love_it_for: List[str] = Field(default=[])
    hate_it_for: List[str] = Field(default=[])
    forum_consensus: List[ForumOpinion] = Field(default=[])

class SmartSwapOption(BaseModel):
    product_name: str
    price: Any  # Could be float or string/range
    condition: str
    performance_diff: str = ""
    camera_diff: str = ""
    reason_to_buy: str = ""
    reason_to_avoid: str = ""

class SmartSwapReport(BaseModel):
    base_price: float
    recommendation: str
    swaps: List[SmartSwapOption] = Field(default=[])

class TradeInOption(BaseModel):
    device_name: str
    estimated_value: float
    net_price: float

class NetPriceReport(BaseModel):
    upgrade_from: List[TradeInOption] = Field(default=[])

class DisasterScenario(BaseModel):
    name: str
    scenario: str
    outcome: str
    repair_cost_estimate: str
    survivability_score: int

class WhatIfReport(BaseModel):
    disaster_score: int
    scenarios: List[DisasterScenario] = Field(default=[])


# =============================================================================
# ENHANCED REVIEW MODEL
# =============================================================================

class EnhancedProductReview(BaseModel):
    """Complete enhanced product review with all features"""
    # Base review (inherited fields duplicated for clarity or composition)
    product_name: str
    specifications_inferred: str = ""
    predicted_rating: str = ""
    pros: List[str] = Field(default=[])
    cons: List[str] = Field(default=[])
    expert_assessment: str = ""
    price_info: str = "Price not available"
    sources: List[str] = Field(default=[])
    last_updated: str = ""
    data_source_type: str = "web_search"
    
    # Enhanced features
    sentiment_analysis: Optional[SentimentScore] = None
    product_images: List[ProductImage] = Field(default=[])
    primary_image_url: Optional[str] = None
    
    # Sentiment breakdowns
    pros_sentiment: List[Tuple[str, float]] = Field(default=[])
    cons_sentiment: List[Tuple[str, float]] = Field(default=[])
    verdict_sentiment: float = 0.0
    aspect_breakdown: List[Dict[str, Any]] = Field(default=[])
    
    # Pricing
    price_naira: Optional[float] = None
    price_comparison: Optional[PriceComparison] = None
    original_price_display: Optional[str] = None
    price_confidence: Optional[str] = None
    
    # Intelligence
    red_flag_report: Optional[RedFlagReport] = None
    timing_advice: Optional[PurchaseTimingAdvice] = None
    
    best_for_tags: List[BestForTag] = Field(default=[])
    budget_tier: Optional[str] = None
    alternatives: List[AlternativeProduct] = Field(default=[])
    recommended_retailer: Optional[RecommendedRetailer] = None
    
    # Advanced Intelligence Reports
    resale_analysis: Optional[ResaleAnalysis] = None
    video_proof: Optional[VideoProof] = None
    fake_spotter_report: Optional[FakeSpotterReport] = None
    vox_populi_report: Optional[VoxPopuliReport] = None
    smart_swap_report: Optional[SmartSwapReport] = None
    net_price_report: Optional[NetPriceReport] = None
    what_if_report: Optional[WhatIfReport] = None
    
    # Metadata & Authentic Recommendation
    data_quality: Optional[str] = None
    purchase_recommendation: Optional[str] = None
    purchase_recommendation_reasons: List[str] = Field(default=[], alias="purchase_reasons")
    top_strengths: List[str] = Field(default=[])
    main_weaknesses: List[str] = Field(default=[])
    data_authenticity_note: Optional[str] = Field(default=None, alias="authenticity_note")

    # Allow population by alias (for fields like purchase_reasons/authenticity_note)
    class Config:
        populate_by_name = True
        extra = "ignore" # Ignore extra fields if any

    @property
    def verdict(self) -> str:
        return self.expert_assessment
    
    @property
    def summary(self) -> str:
        return self.expert_assessment

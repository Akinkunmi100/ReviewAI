"""
Sentiment analysis and NLU services.
"""

import re
import logging
from typing import List, Dict, Any, Optional
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from core.models import ProductReview, SentimentScore

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    """Sophisticated sentiment analysis for product reviews"""
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        
        # Product-specific sentiment lexicon enhancements
        self.positive_terms = {
            'excellent', 'amazing', 'outstanding', 'superb', 'fantastic',
            'premium', 'durable', 'reliable', 'innovative', 'impressive',
            'worth', 'recommend', 'love', 'perfect', 'flawless'
        }
        
        self.negative_terms = {
            'disappointing', 'terrible', 'awful', 'poor', 'defective',
            'broken', 'overpriced', 'waste', 'regret', 'avoid',
            'frustrating', 'unreliable', 'cheaply', 'horrible'
        }
        
        # Aspect keywords
        self.aspect_keywords = {
            'quality': ['quality', 'build', 'durability', 'material', 'construction'],
            'performance': ['performance', 'speed', 'fast', 'slow', 'responsive'],
            'value': ['price', 'value', 'worth', 'expensive', 'cheap', 'cost'],
            'design': ['design', 'look', 'aesthetic', 'style', 'appearance'],
            'features': ['features', 'functionality', 'capability', 'options'],
            'usability': ['easy', 'difficult', 'intuitive', 'complicated', 'user-friendly']
        }
    
    def analyze_review(self, review: ProductReview) -> SentimentScore:
        """Perform comprehensive sentiment analysis on product review"""
        
        # Combine all text for overall analysis
        full_text = self._build_full_text(review)
        
        # TextBlob analysis
        blob = TextBlob(full_text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # VADER analysis
        vader_scores = self.vader.polarity_scores(full_text)
        
        # Determine overall sentiment
        compound = vader_scores['compound']
        if compound >= 0.05:
            overall = "Positive"
        elif compound <= -0.05:
            overall = "Negative"
        else:
            overall = "Mixed"
        
        # Calculate confidence
        confidence = self._calculate_confidence(polarity, compound, subjectivity)
        
        # Emotional tone analysis
        emotional_tone = self._determine_emotional_tone(full_text, compound)
        
        # Extract key aspects
        positive_aspects = self._extract_positive_aspects(review.pros, full_text)
        negative_aspects = self._extract_negative_aspects(review.cons, full_text)
        
        return SentimentScore(
            overall_sentiment=overall,
            polarity_score=polarity,
            subjectivity_score=subjectivity,
            compound_score=compound,
            positive_ratio=vader_scores['pos'],
            negative_ratio=vader_scores['neg'],
            neutral_ratio=vader_scores['neu'],
            sentiment_confidence=confidence,
            emotional_tone=emotional_tone,
            key_positive_aspects=positive_aspects,
            key_negative_aspects=negative_aspects
        )
    
    def analyze_text_components(self, review: ProductReview) -> Dict[str, Any]:
        """Analyze sentiment of individual review components"""
        # Return lists of (text, score) tuples for pros and cons
        pros_sentiment = [(p, self._analyze_text(p)) for p in review.pros]
        cons_sentiment = [(c, self._analyze_text(c)) for c in review.cons]
        
        return {
            'pros_sentiment': pros_sentiment,
            'cons_sentiment': cons_sentiment,
            'verdict_sentiment': self._analyze_text(review.verdict),
            'specs_sentiment': self._analyze_text(review.specifications_inferred)
        }

    def _build_full_text(self, review: ProductReview) -> str:
        """Build a single text blob from all key review fields for analysis."""
        full_text = f"{review.specifications_inferred}. "
        full_text += " ".join(review.pros) + ". "
        full_text += " ".join(review.cons) + ". "
        full_text += review.verdict
        return full_text

    def summarize_aspect_sentiment(self, review: ProductReview) -> List[Dict[str, Any]]:
        """Summarize sentiment per aspect (quality, performance, value, etc.)."""
        text = self._build_full_text(review)
        sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]
        aspect_summaries: List[Dict[str, Any]] = []

        for aspect, keywords in self.aspect_keywords.items():
            aspect_sentiments = []
            mentions = 0
            for sent in sentences:
                lower = sent.lower()
                if any(kw in lower for kw in keywords):
                    scores = self.vader.polarity_scores(sent)
                    aspect_sentiments.append(scores["compound"])
                    mentions += 1
            if mentions > 0 and aspect_sentiments:
                avg_sent = float(sum(aspect_sentiments) / len(aspect_sentiments))
                aspect_summaries.append(
                    {
                        "aspect": aspect.title(),
                        "mentions": mentions,
                        "avg_sentiment": avg_sent,
                    }
                )
        aspect_summaries.sort(key=lambda x: x["mentions"], reverse=True)
        return aspect_summaries
    
    def _analyze_text(self, text: str) -> float:
        """Analyze sentiment of a text snippet"""
        if not text:
            return 0.0
        scores = self.vader.polarity_scores(text)
        return scores['compound']
    
    def _calculate_confidence(self, polarity: float, compound: float, subjectivity: float) -> float:
        """Calculate confidence in sentiment assessment"""
        agreement = 1.0 - abs(polarity - compound) / 2.0
        magnitude = (abs(polarity) + abs(compound)) / 2.0
        objectivity_factor = 1.0 - (subjectivity * 0.3)
        
        confidence = (agreement * 0.4 + magnitude * 0.4 + objectivity_factor * 0.2)
        return round(confidence, 3)
    
    def _determine_emotional_tone(self, text: str, compound: float) -> str:
        """Determine the dominant emotional tone"""
        text_lower = text.lower()
        
        excitement_words = ['amazing', 'awesome', 'love', 'excellent', 'fantastic']
        satisfaction_words = ['good', 'satisfied', 'happy', 'pleased', 'solid']
        disappointment_words = ['disappointing', 'expected', 'unfortunately', 'hoped']
        frustration_words = ['frustrating', 'annoying', 'terrible', 'horrible', 'awful']
        
        excitement = sum(1 for word in excitement_words if word in text_lower)
        satisfaction = sum(1 for word in satisfaction_words if word in text_lower)
        disappointment = sum(1 for word in disappointment_words if word in text_lower)
        frustration = sum(1 for word in frustration_words if word in text_lower)
        
        if compound >= 0.5:
            return "Enthusiastic" if excitement > satisfaction else "Satisfied"
        elif compound >= 0.1:
            return "Cautiously Optimistic"
        elif compound >= -0.1:
            return "Neutral/Balanced"
        elif compound >= -0.5:
            return "Disappointed" if disappointment > frustration else "Concerned"
        else:
            return "Frustrated" if frustration > disappointment else "Very Disappointed"
    
    def _extract_positive_aspects(self, pros: List[str], full_text: str) -> List[str]:
        """Extract key positive aspects mentioned"""
        aspects = []
        text_lower = full_text.lower()
        
        for aspect, keywords in self.aspect_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    for pro in pros:
                        if keyword in pro.lower():
                            aspects.append(aspect.title())
                            break
        
        return list(set(aspects))[:5]
    
    def _extract_negative_aspects(self, cons: List[str], full_text: str) -> List[str]:
        """Extract key negative aspects mentioned"""
        aspects = []
        text_lower = full_text.lower()
        
        for aspect, keywords in self.aspect_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    for con in cons:
                        if keyword in con.lower():
                            aspects.append(aspect.title())
                            break
        
        return list(set(aspects))[:5]
    
    def generate_sentiment_summary(self, sentiment: SentimentScore) -> str:
        """Generate human-readable sentiment summary"""
        summary_parts = []
        
        summary_parts.append(f"**Overall Sentiment:** {sentiment.overall_sentiment} {sentiment.sentiment_emoji}")
        
        confidence_level = "High" if sentiment.sentiment_confidence > 0.7 else "Medium" if sentiment.sentiment_confidence > 0.4 else "Low"
        summary_parts.append(f"**Confidence:** {confidence_level} ({sentiment.sentiment_confidence:.1%})")
        
        summary_parts.append(f"**Tone:** {sentiment.emotional_tone}")
        
        summary_parts.append(f"**Score Breakdown:** {sentiment.positive_ratio:.0%} Positive, {sentiment.neutral_ratio:.0%} Neutral, {sentiment.negative_ratio:.0%} Negative")
        
        return "\n\n".join(summary_parts)

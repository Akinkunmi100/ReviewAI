"""
Interactive chat services for product queries with real-time web search integration.
"""

import re
import logging
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any, TYPE_CHECKING

from groq import Groq

from core.config import AppConfig
from core.models import ProductReview, UserProfile, EnhancedProductReview

if TYPE_CHECKING:
    from core.scraping import WebSearchClient, ContentScraper

logger = logging.getLogger(__name__)


class AIGenerationError(Exception):
    """AI generation related errors"""
    pass


# Common filler phrases to remove from LLM responses
FILLER_PHRASES = [
    r"^As an AI( language model)?[,.]?\s*",
    r"^I'd be happy to help[.!]?\s*",
    r"^Great question[.!]?\s*",
    r"^That's a great question[.!]?\s*",
    r"^Sure[,!]?\s*",
    r"^Of course[,!]?\s*",
    r"^Absolutely[,!]?\s*",
    r"\s*I hope this helps[.!]?\s*$",
    r"\s*Let me know if you have any other questions[.!]?\s*$",
    r"\s*Feel free to ask if you need more information[.!]?\s*$",
    r"\s*Is there anything else you'd like to know\??\s*$",
]

# Keywords suggesting need for fresh/current data
FRESH_DATA_KEYWORDS = [
    'current price', 'latest price', 'price now', 'today',
    'available', 'in stock', 'out of stock', 'where to buy',
    'discount', 'sale', 'deal', 'offer', 'cheapest',
    'latest', 'newest', 'recent', 'updated', 'new model',
    '2024', '2025', 'this month', 'this week',
    'buy now', 'should i buy', 'worth buying',
]


class ChatService:
    """Handles product chat conversations with real-time data capabilities"""
    
    def __init__(
        self, 
        groq_client: Groq, 
        config: AppConfig,
        web_search_client: Optional['WebSearchClient'] = None,
        content_scraper: Optional['ContentScraper'] = None
    ):
        self.client = groq_client
        self.config = config
        self.web_search_client = web_search_client
        self.content_scraper = content_scraper
    
    def get_chat_response(
        self,
        user_message: str,
        conversation_history: List[Dict], 
        product_review: ProductReview,
        user_profile: Optional[UserProfile] = None,
    ) -> str:
        """Get chat response about the product, aware of user profile and price/timing context"""
        
        # Check if we need fresh data from the web
        fresh_context = ""
        if self._needs_fresh_data(user_message, product_review):
            fresh_context = self._fetch_fresh_context(
                product_review.product_name, 
                user_message
            )
        
        # Build system prompt with freshness info and optional real-time data
        system_prompt = self._get_chat_system_prompt(
            product_review, 
            user_profile,
            fresh_context
        )
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.config.model_name,
                temperature=self.config.temperature_chat,
                max_tokens=self.config.max_tokens_chat
            )
            
            raw_response = response.choices[0].message.content
            
            # Post-process to clean up response
            cleaned_response = self._post_process_response(raw_response)
            
            return cleaned_response
            
        except Exception as e:
            logger.error(f"Chat response failed: {e}")
            raise AIGenerationError(f"Chat failed: {str(e)}")
    
    def _needs_fresh_data(self, user_message: str, product_review: ProductReview) -> bool:
        """Detect if the user's question requires fresh web data."""
        if not self.web_search_client or not self.content_scraper:
            return False
        
        message_lower = user_message.lower()
        
        # Check if message contains fresh data keywords
        if any(kw in message_lower for kw in FRESH_DATA_KEYWORDS):
            return True
        
        # Check if data is stale (older than 7 days)
        if self._is_data_stale(product_review, days_threshold=7):
            return True
        
        return False
    
    def _is_data_stale(self, product_review: ProductReview, days_threshold: int = 7) -> bool:
        """Check if product review data is older than threshold."""
        try:
            last_updated = getattr(product_review, 'last_updated', None)
            if not last_updated:
                return True  # Unknown = assume stale
            
            # Parse if string
            if isinstance(last_updated, str):
                # Try multiple formats
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%B %d, %Y"]:
                    try:
                        last_updated = datetime.strptime(last_updated, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return True  # Couldn't parse = assume stale
            
            # Make timezone-aware if needed
            if last_updated.tzinfo is None:
                last_updated = last_updated.replace(tzinfo=timezone.utc)
            
            days_old = (datetime.now(timezone.utc) - last_updated).days
            return days_old > days_threshold
            
        except Exception:
            return True  # On error, assume stale
    
    def _get_data_freshness_context(self, product_review: ProductReview) -> str:
        """Generate freshness context for the LLM."""
        try:
            last_updated = getattr(product_review, 'last_updated', None)
            if not last_updated:
                return "📊 DATA FRESHNESS: ⚠️ UNKNOWN (no timestamp available)"
            
            # Parse if string
            if isinstance(last_updated, str):
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%B %d, %Y"]:
                    try:
                        last_updated = datetime.strptime(last_updated, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return "📊 DATA FRESHNESS: ⚠️ UNKNOWN (couldn't parse date)"
            
            # Make timezone-aware if needed
            if last_updated.tzinfo is None:
                last_updated = last_updated.replace(tzinfo=timezone.utc)
            
            days_old = (datetime.now(timezone.utc) - last_updated).days
            
            if days_old <= 1:
                return f"📊 DATA FRESHNESS: ✅ FRESH (updated today)"
            elif days_old <= 7:
                return f"📊 DATA FRESHNESS: ✅ FRESH (updated {days_old} days ago)"
            elif days_old <= 30:
                return f"📊 DATA FRESHNESS: ⚡ RECENT (updated {days_old} days ago)"
            else:
                return f"📊 DATA FRESHNESS: ⚠️ POTENTIALLY OUTDATED (updated {days_old} days ago)"
                
        except Exception:
            return "📊 DATA FRESHNESS: ⚠️ UNKNOWN"
    
    def _fetch_fresh_context(self, product_name: str, user_message: str) -> str:
        """Fetch fresh web data relevant to the user's question."""
        if not self.web_search_client or not self.content_scraper:
            return ""
        
        try:
            # Build targeted search query
            search_terms = self._extract_search_terms(user_message)
            current_year = datetime.now().year
            search_query = f"{product_name} {search_terms} {current_year}"
            
            logger.info(f"Fetching fresh data for: {search_query}")
            
            # Use existing infrastructure
            search_results = self.web_search_client.search_products(search_query)
            if not search_results:
                return ""
            
            scraped_content = self.content_scraper.scrape_content(search_results[:3])
            if not scraped_content:
                return ""
            
            # Format for LLM context
            fresh_context = "\n\n🔄 REAL-TIME WEB DATA (just fetched - USE THIS FOR CURRENT INFO):\n"
            for i, content in enumerate(scraped_content, 1):
                # Truncate content to avoid token overflow
                snippet = content.content[:400].strip()
                if len(content.content) > 400:
                    snippet += "..."
                fresh_context += f"\n[Source {i}]: {content.title}\n{snippet}\n"
            
            fresh_context += "\n⚠️ IMPORTANT: Use the REAL-TIME WEB DATA above for current prices, availability, and recent information.\n"
            
            return fresh_context
            
        except Exception as e:
            logger.warning(f"Failed to fetch fresh context: {e}")
            return ""
    
    def _extract_search_terms(self, user_message: str) -> str:
        """Extract relevant search terms from user message."""
        # Keywords to preserve
        important_terms = ['price', 'cost', 'buy', 'available', 'stock', 'discount', 'sale', 'deal', 'specs', 'review']
        
        message_lower = user_message.lower()
        terms = []
        
        for term in important_terms:
            if term in message_lower:
                terms.append(term)
        
        return ' '.join(terms) if terms else 'price review'
    
    def _post_process_response(self, response: str) -> str:
        """Clean up LLM response for consistency and quality."""
        if not response:
            return response
        
        cleaned = response.strip()
        
        # Remove common filler phrases
        for pattern in FILLER_PHRASES:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.MULTILINE)
        
        # Remove excessive newlines (more than 2 in a row)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in cleaned.split('\n')]
        cleaned = '\n'.join(lines)
        
        # Final trim
        cleaned = cleaned.strip()
        
        return cleaned
    
    def _get_chat_system_prompt(
        self, 
        product_review: ProductReview, 
        user_profile: Optional[UserProfile] = None,
        fresh_context: str = ""
    ) -> str:
        current_date = datetime.now().strftime("%B %d, %Y")
        freshness_info = self._get_data_freshness_context(product_review)
        
        base_prompt = f"""You are a friendly, knowledgeable shopping assistant helping users make smart buying decisions.

📅 TODAY: {current_date}
{freshness_info}

=== YOUR PERSONALITY ===
- Be warm, conversational, and genuinely helpful—like a tech-savvy friend
- Sound natural—avoid robotic or overly formal language
- Get straight to the point—no fluff, no filler
- Share honest opinions and practical advice
- Use casual language but stay professional

=== HOW TO RESPOND ===
- Answer the question directly in the FIRST sentence
- Keep responses SHORT (50-150 words for simple questions)
- Use **bold** for important specs, prices, and key points
- Use bullet points only when listing 3+ items
- Be specific—use actual numbers, not vague descriptions

=== CONVERSATION STYLE ===
- Simple questions → Brief, helpful answers (1-3 sentences)
- Complex questions → Structured with key points
- Opinion questions → Share your recommendation with reasoning
- Comparison questions → Quick verdict + key differences

=== DON'T ===
- Say "Confirmation:" or "Based on the data..." - just answer naturally
- List system status or capabilities
- Give meta-commentary about the product data
- Be vague when you have specific information"""

        # Add product context
        if product_review.data_source_type == 'free_web_search':
            base_prompt += f"""

=== PRODUCT CONTEXT ===
- **Product**: {product_review.product_name}
- **Key Specs**: {product_review.specifications_inferred}
- **Rating**: {product_review.predicted_rating}
- **Price**: {product_review.price_info}
- **Data Source**: Real-time web search
- **Last Updated**: {product_review.last_updated or "Unknown"}"""
        else:
            base_prompt += f"""

=== PRODUCT CONTEXT ===
- **Product**: {product_review.product_name}
- **Data Source**: AI Knowledge Base
- ⚠️ Note: This is from AI training data, not live web data. Verify current specs and pricing."""

        # Add fresh web data if available
        if fresh_context:
            base_prompt += fresh_context
        
        # Personalization context
        if user_profile:
            try:
                profile = user_profile if isinstance(user_profile, UserProfile) else UserProfile(**user_profile)
                
                budget_text = "unknown"
                if profile.min_budget and profile.max_budget:
                    budget_text = f"₦{profile.min_budget:,.0f}–₦{profile.max_budget:,.0f}"
                elif profile.max_budget:
                    budget_text = f"up to ₦{profile.max_budget:,.0f}"
                elif profile.min_budget:
                    budget_text = f"from ₦{profile.min_budget:,.0f}"

                base_prompt += f"""

=== USER PROFILE (personalize answers to this) ===
- **Budget**: {budget_text}
- **Use Cases**: {', '.join(profile.use_cases) if profile.use_cases else 'not specified'}
- **Preferred Brands**: {', '.join(profile.preferred_brands) if profile.preferred_brands else 'none'}

When answering "is it worth it?" or "should I buy?", ALWAYS reference this profile."""
            except Exception:
                pass

        # Enhanced product signals
        if hasattr(product_review, "timing_advice") or hasattr(product_review, "red_flag_report"):
            timing_note = ""
            risk_note = ""
            
            timing = getattr(product_review, "timing_advice", None)
            if timing:
                timing_note = f"Buy Recommendation: {timing.recommendation.replace('_', ' ').title()}"
            
            risk = getattr(product_review, "red_flag_report", None)
            if risk:
                risk_note = f"Risk Level: {risk.overall_risk_level.title()}"
            
            if timing_note or risk_note:
                base_prompt += f"""

=== BUYING SIGNALS ===
- {timing_note or 'No timing data'}
- {risk_note or 'No risk assessment'}

Reference these signals when answering "Should I wait?" or "Is it risky?" questions."""

        return base_prompt

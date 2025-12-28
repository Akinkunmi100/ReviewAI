"""
Streamlit UI components for the Product Review Engine.
"""

import streamlit as st
import json
import time
import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Tuple

from core.config import Constants
from core.currency import CurrencyFormatter
from core.models import (
    ProductReview, EnhancedProductReview, UserProfile, PriceComparison,
    RedFlagReport, PurchaseTimingAdvice, BestForTag, SentimentScore,
    AlternativeProduct, RecommendedRetailer
)
from core.product_service import ProductReviewService, EnhancedProductReviewService, AIGenerationError

logger = logging.getLogger(__name__)


class StreamlitUI:
    """Handles Streamlit user interface"""
    
    def __init__(self, review_service: ProductReviewService):
        self.service = review_service
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize session state"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "current_product" not in st.session_state:
            st.session_state.current_product = None
        if "review_data" not in st.session_state:
            st.session_state.review_data = None
        if "chat_mode" not in st.session_state:
            st.session_state.chat_mode = False
        if "user_profile" not in st.session_state:
            st.session_state.user_profile = {}
        if "history" not in st.session_state:
            st.session_state.history = []
        if "shortlist" not in st.session_state:
            st.session_state.shortlist = []
    
    def render_sidebar(self):
        """Render sidebar content with Nigerian market focus"""
        with st.sidebar:
            st.title("🌍 Global Product Review Engine")
            st.caption("Global reviews • Prices in Nigerian Naira (₦)")
            st.markdown("---")
            
            # Mode toggle buttons
            st.markdown("**Mode:**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📱 Review", use_container_width=True, key="sidebar_review"):
                    st.session_state.comparison_mode = False
                    st.session_state.chat_mode = False
                    st.rerun()
            with col2:
                if st.button("⚖️ Compare", use_container_width=True, key="sidebar_compare"):
                    st.session_state.comparison_mode = True
                    st.session_state.chat_mode = False
                    st.rerun()
            
            st.markdown("---")
            
            if st.session_state.current_product:
                self._render_current_product_sidebar()
            else:
                st.info("👈 Enter a product name to start")
            
            self._render_profile_section()
            self._render_history_and_shortlist()
            self._render_help_section()
            self._render_footer()
    
    def _render_current_product_sidebar(self):
        """Render current product info in sidebar"""
        st.success(f"**Current Product:**\n{st.session_state.current_product}")
        st.markdown("---")
        
        if st.session_state.review_data:
            review = st.session_state.review_data
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Rating", review.predicted_rating)
            with col2:
                source_type = review.data_source_type
                if source_type == 'free_web_search':
                    st.metric("Sources", len(review.sources))
                else:
                    st.metric("Source", "AI KB")
            
            st.metric("Pros", len(review.pros))
            st.metric("Cons", len(review.cons))
        
        st.markdown("---")
        
        if st.button("🔄 Review Different Product", use_container_width=True):
            self._reset_conversation()
            st.rerun()
    
    def _render_history_and_shortlist(self):
        """Render recent history and shortlist panels in the sidebar."""
        with st.expander("🕒 Recent products this session"):
            history = st.session_state.get("history", [])
            if not history:
                st.caption("No products analyzed yet.")
            else:
                for item in history[-10:][::-1]:
                    line = f"**{item.get('name','?')}** — {item.get('rating','?')} | {item.get('price','N/A')}"
                    st.markdown(line)
                    meta_bits = []
                    if item.get("deal_quality"):
                        meta_bits.append(f"Deal: {item['deal_quality'].upper()}")
                    if item.get("timing"):
                        meta_bits.append(f"Timing: {item['timing']}")
                    if item.get("risk"):
                        meta_bits.append(f"Risk: {item['risk'].title()}")
                    if meta_bits:
                        st.caption(" • ".join(meta_bits))
        
        with st.expander("⭐ Shortlist"):
            shortlist = st.session_state.get("shortlist", [])
            if not shortlist:
                st.caption("You haven't shortlisted any products yet.")
            else:
                for idx, item in enumerate(shortlist):
                    line = f"**{item.get('name','?')}** — {item.get('rating','?')} | {item.get('price','N/A')}"
                    st.markdown(line)
                    meta_bits = []
                    if item.get("deal_quality"):
                        meta_bits.append(f"Deal: {item['deal_quality'].upper()}")
                    if item.get("timing"):
                        meta_bits.append(f"Timing: {item['timing']}")
                    if item.get("risk"):
                        meta_bits.append(f"Risk: {item['risk'].title()}")
                    if meta_bits:
                        st.caption(" • ".join(meta_bits))
                    cols = st.columns(2)
                    with cols[0]:
                        if st.button("Remove", key=f"shortlist_remove_{idx}"):
                            st.session_state.shortlist.pop(idx)
                            st.rerun()
                    with cols[1]:
                        if st.button("Compare", key=f"shortlist_compare_{idx}"):
                            names = [i.get("name") for i in shortlist]
                            clicked_name = item.get("name")
                            ordered = [clicked_name] + [n for n in names if n != clicked_name]
                            st.session_state.comparison_products = ordered[:3]
                            st.session_state.comparison_mode = True
                            st.rerun()

                if len(shortlist) >= 2 and st.button("⚖️ Compare all shortlisted", key="shortlist_compare_all", use_container_width=True):
                    names = [i.get("name") for i in shortlist][:3]
                    st.session_state.comparison_products = names
                    st.session_state.comparison_mode = True
                    st.rerun()

    def _render_profile_section(self):
        """Render user personalization profile editor"""
        with st.expander("👤 Your Profile & Preferences"):
            raw_profile = st.session_state.get("user_profile", {}) or {}
            profile = UserProfile(**raw_profile) if isinstance(raw_profile, dict) else UserProfile()

            col_budget_min, col_budget_max = st.columns(2)
            with col_budget_min:
                min_budget = st.number_input(
                    "Min Budget (₦)",
                    min_value=0.0,
                    value=float(profile.min_budget) if profile.min_budget is not None else 0.0,
                    step=10000.0,
                    format="%.0f",
                )
            with col_budget_max:
                max_budget = st.number_input(
                    "Max Budget (₦)",
                    min_value=0.0,
                    value=float(profile.max_budget) if profile.max_budget is not None else 0.0,
                    step=10000.0,
                    format="%.0f",
                )

            all_use_cases = [
                "Gaming", "Work", "Photography", "Travel", "Students",
                "Content Creation", "Fitness", "Music"
            ]
            selected_use_cases = st.multiselect(
                "Main use cases you care about",
                options=all_use_cases,
                default=[u for u in profile.use_cases if u in all_use_cases],
            )

            preferred_brands_str = ", ".join(profile.preferred_brands)
            avoided_brands_str = ", ".join(profile.avoided_brands)

            preferred_brands_input = st.text_input(
                "Preferred brands (comma-separated)",
                value=preferred_brands_str,
                placeholder="e.g., Apple, Samsung, Tecno",
            )
            avoided_brands_input = st.text_input(
                "Brands to avoid (comma-separated)",
                value=avoided_brands_str,
                placeholder="e.g., Infinix, Itel",
            )

            if st.button("💾 Save Profile", use_container_width=True):
                new_profile = UserProfile(
                    min_budget=min_budget or None,
                    max_budget=max_budget or None,
                    use_cases=selected_use_cases,
                    preferred_brands=[b.strip() for b in preferred_brands_input.split(",") if b.strip()],
                    avoided_brands=[b.strip() for b in avoided_brands_input.split(",") if b.strip()],
                )
                st.session_state.user_profile = json.loads(new_profile.model_dump_json())
                st.success("Profile saved! Future recommendations will use these preferences.")

    def _render_help_section(self):
        """Render help and tips section with Nigerian market info"""
        with st.expander("💡 How to Use"):
            st.markdown("""
            **Getting Started:**  
            1. Enter a product name  
            2. Choose data source (Web or AI)  
            3. Get instant review with 🇳🇬 Nigerian prices  
            4. Ask follow-up questions  
              
            **Features:**  
            - 🇳🇬 **Nigerian Prices**: Compare prices from Jumia, Konga, Slot, Pointek  
            - ⚠️ **Red Flags**: Detect potential issues  
            - ⏰ **Buy Timing**: Know when to buy  
            - ⚖️ **Compare**: Side-by-side product comparison  
              
            **Example Questions:**  
            - "How does it compare to [competitor]?"  
            - "Where can I buy this in Nigeria?"  
            - "Is it good for Nigerian weather?"  
            - "Should I wait for Black Friday?"  
            """)
        
        with st.expander("📝 Suggested Questions"):
            suggestions = [
                "Compare with alternatives", "Best use cases", "Value for money",
                "Long-term reliability", "Setup and learning curve", "Compatibility issues"
            ]
            for suggestion in suggestions:
                st.markdown(f"• {suggestion}")
    
    def _render_footer(self):
        """Render sidebar footer with Nigerian market info"""
        st.markdown("---")
        st.caption("🇳🇬 **Nigerian Retailers (when available):**")
        st.caption("🟠 Jumia Nigeria")
        st.caption("🟥 Konga")
        st.caption("🟢 Slot Nigeria")
        st.caption("🟪 PointekOnline")
        st.markdown("---")
        st.caption("🆓 100% Free • No API costs")
        st.caption("🌐 Web Search: DuckDuckGo")
        st.caption("🤖 AI: Groq Llama 3.3 70B")
        st.caption("💱 Currency: Nigerian Naira (₦)")
    
    def render_search_interface(self):
        """Render initial search interface with global review + Nigerian pricing"""
        st.title("🌍 Global Product Review Engine")
        st.markdown("### Get expert product reviews worldwide, with prices in Nigerian Naira from Jumia, Konga, Slot & Pointek")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            product_input = st.text_input(
                "Enter Product Name",
                placeholder="e.g., Sony WH-1000XM5, MacBook Pro M3, Nintendo Switch OLED",
                label_visibility="collapsed"
            )
        
        data_choice = st.radio(
            "Choose Data Source:",
            [
                "🌐 Web Search (Real-time, most accurate)",
                "🤖 AI Knowledge Only (Fast, may be outdated)",
                "🌐+🤖 Hybrid (Combine Web + AI Knowledge)"
            ],
            horizontal=True,
            help="Web: scrape current info. AI: use training data. Hybrid: combine both."
        )

        if data_choice.startswith("🌐+🤖"):
            data_mode = "hybrid"
        elif data_choice.startswith("🤖"):
            data_mode = "ai"
        else:
            data_mode = "web"
        
        with col2:
            search_button = st.button("🔍 Analyze", use_container_width=True, type="primary")
        
        self._render_example_products()
        
        st.info("""
        **🌐 Web Mode**: Searches global product information from the web, then checks Nigerian retailer prices.
        **🤖 AI Mode**: Fast responses using only AI training data.
        **🌐+🤖 Hybrid Mode**: Combines live web data with AI knowledge.
        """)
        
        return product_input, search_button, data_mode
    
    def _render_example_products(self):
        """Render example product buttons - Nigerian market focused"""
        st.markdown("**Popular Products in Nigeria:**")
        example_cols = st.columns(4)
        examples = [
            "iPhone 16 Pro Max", "Samsung Galaxy S24 Ultra", 
            "Tecno Camon 30 Pro", "Infinix Note 40 Pro"
        ]
        
        for idx, example in enumerate(examples):
            with example_cols[idx]:
                if st.button(example, use_container_width=True, key=f"example_{idx}"):
                    st.session_state.example_product = example
                    st.rerun()
    
    def render_review_display(self, review: ProductReview):
        """Display the structured review"""
        st.markdown("---")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.header(f"📱 {review.product_name}")
        with col2:
            st.markdown(f"### ⭐ {review.predicted_rating}")
        with col3:
            if review.data_source_type == 'free_web_search':
                st.success("🌐 Live Web Data")
            else:
                st.info("🤖 AI Knowledge")
        
        if review.data_source_type == 'free_web_search':
            st.success(f"✅ Verified from {len(review.sources)} web sources on {review.last_updated}")
        else:
            st.warning("⚠️ Based on AI training data (updated January 2025). Verify current specs.")
        
        col_price, col_specs = st.columns([1, 2])
        with col_price:
            st.markdown("### 💰 Pricing")
            st.info(review.price_info)
        with col_specs:
            st.markdown("### 🔧 Key Specifications")
            st.info(review.specifications_inferred)
        
        st.markdown("---")
        
        col_pros, col_cons = st.columns(2)
        with col_pros:
            st.markdown("### 🟢 Strengths")
            for i, pro in enumerate(review.pros[:10], 1):
                st.markdown(f"**{i}.** {pro}")
        with col_cons:
            st.markdown("### 🔴 Weaknesses")
            for i, con in enumerate(review.cons[:10], 1):
                st.markdown(f"**{i}.** {con}")
        
        st.markdown("---")
        st.markdown("### ✅ Final Verdict")
        st.write(review.verdict)
        
        if review.sources and review.data_source_type == 'free_web_search':
            with st.expander("📚 Sources Used"):
                for i, source in enumerate(review.sources, 1):
                    st.markdown(f"{i}. [{source}]({source})")
    
    def render_chat_interface(self):
        """Render chat interface"""
        st.title(f"💬 Chat about: {st.session_state.current_product}")
        
        with st.expander("📊 View Full Review", expanded=False):
            if st.session_state.review_data:
                self.render_review_display(st.session_state.review_data)
        
        st.markdown("---")
        self._render_chat_messages()
        
        if len(st.session_state.messages) <= 1:
            self._render_quick_questions()
        
        self._handle_chat_input()
    
    def _render_chat_messages(self):
        """Render chat message history"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                st.caption(message.get("timestamp", ""))
    
    def _render_quick_questions(self):
        """Render quick question suggestions"""
        st.markdown("**💡 Try asking:**")
        suggestion_cols = st.columns(3)
        quick_questions = [
            f"How does {st.session_state.current_product} compare to competitors?",
            f"What are the best use cases for this product?", 
            f"Is {st.session_state.current_product} worth the price?"
        ]
        
        for idx, question in enumerate(quick_questions):
            with suggestion_cols[idx]:
                if st.button(question, key=f"quick_{idx}"):
                    self._process_user_message(question)
    
    def _handle_chat_input(self):
        """Handle chat input from user"""
        user_input = st.chat_input("Ask anything about this product...")
        if user_input:
            self._process_user_message(user_input)
    
    def _process_user_message(self, user_input: str):
        """Process user message and get AI response"""
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%I:%M %p")
        })
        
        with st.spinner("🤔 Thinking..."):
            try:
                conversation_history = [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.messages[:-1]
                ]
                
                raw_profile = st.session_state.get("user_profile")
                profile_obj: Optional[UserProfile] = None
                if isinstance(raw_profile, dict) and raw_profile:
                    try:
                        profile_obj = UserProfile(**raw_profile)
                    except Exception:
                        profile_obj = None

                response = self.service.chat_service.get_chat_response(
                    user_input, 
                    conversation_history,
                    st.session_state.review_data,
                    user_profile=profile_obj,
                )
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "timestamp": datetime.now().strftime("%I:%M %p")
                })
                st.rerun()
                
            except AIGenerationError as e:
                st.error(f"Chat error: {e}")
                st.session_state.messages.pop()
    
    def _reset_conversation(self):
        """Reset conversation state"""
        st.session_state.messages = []
        st.session_state.current_product = None
        st.session_state.review_data = None
        st.session_state.chat_mode = False



class EnhancedStreamlitUI(StreamlitUI):
    """Enhanced UI with Nigerian pricing, images, sentiment, red flags, and timing intelligence"""
    
    def __init__(self, review_service: EnhancedProductReviewService):
        super().__init__(review_service)
        if "comparison_mode" not in st.session_state:
            st.session_state.comparison_mode = False
        if "comparison_products" not in st.session_state:
            st.session_state.comparison_products = []

    def render_deal_checker(self):
        """Simple tool: user enters a price and we tell them if it's a good deal vs Nigerian prices."""
        with st.expander("💰 Is this a good deal? (Nigeria)"):
            product_name = st.text_input("Product name for deal check", key="deal_product_name", placeholder="e.g., iPhone 16 Pro Max")
            user_price = st.number_input("Current deal price (₦)", min_value=0.0, step=10000.0, format="%.0f", key="deal_price")
            if st.button("Check Deal Quality", key="deal_check_btn", use_container_width=True):
                if not product_name or user_price <= 0:
                    st.error("Please enter both a product name and a valid price.")
                else:
                    with st.spinner("Comparing with Nigerian retailers..."):
                        try:
                            # Cast to EnhancedProductReviewService to access price_service
                            svc = self.service
                            if hasattr(svc, 'price_service'):
                                price_comparison = svc.price_service.get_price_comparison(product_name)
                                if not price_comparison or not price_comparison.lowest_price:
                                    st.warning("Could not find reliable Nigerian prices for this product.")
                                else:
                                    lowest = price_comparison.lowest_price
                                    avg = price_comparison.average_price or lowest
                                    price = user_price

                                    if price <= 0.9 * lowest:
                                        quality = "excellent"; msg = "Well below the best Nigerian price I could find."
                                    elif price <= lowest:
                                        quality = "good"; msg = "At or slightly below the best Nigerian price."
                                    elif price <= 1.1 * avg:
                                        quality = "normal"; msg = "Roughly in line with normal pricing."
                                    else:
                                        quality = "poor"; msg = "Above typical Nigerian prices; you can likely find cheaper."

                                    st.markdown(f"**Deal Quality:** {quality.upper()}\n\n{msg}\n\nBenchmark range: {price_comparison.price_range_display} (from Nigerian retailers).")
                            else:
                                st.error("Price service not available.")
                        except Exception as e:
                            st.error(f"Deal check failed: {e}")

    def render_review_display(self, review: EnhancedProductReview):
        """Display enhanced review with images, sentiment, and a compact decision card"""
        st.markdown("---")

        # Sticky mini-header
        price_line, _ = self._format_price_story(review)
        timing_label = ""
        if getattr(review, "timing_advice", None):
            timing_label = review.timing_advice.recommendation.replace("_", " ").title()
        
        timing_span = f"<span class='badge-buy'>{timing_label}</span>" if timing_label else ""
        sticky_html = f'<div class="sticky-header"><span><strong>{review.product_name}</strong></span><span>⭐ {review.predicted_rating}</span><span>{price_line}</span>{timing_span}</div>'
        st.markdown(sticky_html, unsafe_allow_html=True)
        
        self._render_decision_card(review)
        
        # Header with image
        if hasattr(review, 'primary_image_url') and review.primary_image_url:
            col_img, col_info = st.columns([1, 2])
            with col_img:
                try: st.image(review.primary_image_url, use_container_width=True, caption=review.product_name)
                except: st.info("📷 Image unavailable")
                if hasattr(review, 'product_images') and len(review.product_images) > 1:
                    with st.expander("🖼️ View More Images"):
                        img_cols = st.columns(3)
                        for idx, img in enumerate(review.product_images[1:4]):
                            with img_cols[idx % 3]:
                                try: st.image(img.thumbnail_url or img.url, use_container_width=True)
                                except: pass
            with col_info:
                st.header(f"📱 {review.product_name}")
                col_rating, col_sentiment = st.columns(2)
                with col_rating: st.markdown(f"### ⭐ {review.predicted_rating}")
                with col_sentiment:
                    if hasattr(review, 'sentiment_analysis') and review.sentiment_analysis:
                        st.markdown(f"### {review.sentiment_analysis.sentiment_emoji} {review.sentiment_analysis.overall_sentiment}")
                if review.data_source_type == 'free_web_search':
                    st.success(f"🌐 Live data from {len(review.sources)} sources")
                else:
                    st.info("🤖 AI Knowledge Base")
        else:
            st.header(f"📱 {review.product_name}")
            col_rating, col_sentiment = st.columns(2)
            with col_rating: st.markdown(f"### ⭐ {review.predicted_rating}")
            with col_sentiment:
                if hasattr(review, 'sentiment_analysis') and review.sentiment_analysis:
                    st.markdown(f"### {review.sentiment_analysis.sentiment_emoji} {review.sentiment_analysis.overall_sentiment}")
        
        st.markdown("---")
        
        if hasattr(review, 'sentiment_analysis') and review.sentiment_analysis:
            self._render_sentiment_analysis(review.sentiment_analysis)
            st.markdown("---")
        
        fit_text = self._compute_fit_for_current_user(review)
        if fit_text:
            st.markdown(f"**🎯 Fit for You:** {fit_text}")
            st.markdown("---")

        if getattr(review, "data_quality", "good") == "limited":
            st.warning("Limited web data found for this product. Rating & specs may be less reliable.")
        elif getattr(review, "data_quality", "good") == "poor":
            st.error("Very limited web data found for this product. Treat this review as approximate.")

        raw_profile = st.session_state.get("user_profile")
        profile = UserProfile(**raw_profile) if isinstance(raw_profile, dict) and raw_profile else None

        if profile and review.price_naira:
            price_val = float(review.price_naira)
            if profile.max_budget and price_val > profile.max_budget:
                st.warning(f"💰 This is above your max budget of ₦{profile.max_budget:,.0f}.")

        if profile and getattr(review, "best_for_tags", None) and profile.use_cases:
            profile_cases_lower = {u.lower() for u in profile.use_cases}
            best_for_lower = {t.use_case.lower() for t in review.best_for_tags}
            if not (profile_cases_lower & best_for_lower):
                st.info(f"🎯 This product is not strongly aligned with your selected use cases ({', '.join(profile.use_cases)}).")

        col_price, col_specs = st.columns([1, 2])
        with col_price:
            st.markdown("### 💰 Pricing")
            price_line, confidence_label = self._format_price_story(review)
            st.markdown(price_line, unsafe_allow_html=True)
            if confidence_label: st.caption(confidence_label)
        with col_specs:
            st.markdown("### 🔧 Key Specifications")
            st.info(review.specifications_inferred)
        
        st.markdown("---")
        
        col_pros, col_cons = st.columns(2)
        with col_pros:
            st.markdown("### 🟢 Strengths")
            if hasattr(review, 'pros_sentiment') and review.pros_sentiment:
                # Logic to display sentiment score if available
                pass
            for i, pro in enumerate(review.pros[:10], 1):
                st.markdown(f"**{i}.** {pro}")
        
        with col_cons:
            st.markdown("### 🔴 Weaknesses")
            for i, con in enumerate(review.cons[:10], 1):
                st.markdown(f"**{i}.** {con}")
        
        st.markdown("---")
        st.markdown("### ✅ Final Verdict")
        st.write(review.verdict)

        self._render_next_steps(review)
        
        if hasattr(review, 'price_comparison') and review.price_comparison:
            self._render_nigerian_prices(review.price_comparison)
            st.markdown("---")
        
        if hasattr(review, 'red_flag_report') and review.red_flag_report:
            self._render_red_flags(review.red_flag_report)
            st.markdown("---")
        
        if hasattr(review, 'timing_advice') and review.timing_advice:
            self._render_timing_advice(review.timing_advice)
            st.markdown("---")
        
        if hasattr(review, 'best_for_tags') and review.best_for_tags:
            self._render_best_for_tags(review.best_for_tags, getattr(review, 'budget_tier', None))
            st.markdown("---")
        
        if getattr(review, "alternatives", None):
            self._render_alternatives(review.alternatives)
            st.markdown("---")

        self._render_copy_share_summary(review)
        st.markdown("---")

        if review.sources and review.data_source_type == 'free_web_search':
            with st.expander("📚 Sources Used"):
                for i, source in enumerate(review.sources, 1):
                    st.markdown(f"{i}. [{source}]({source})")

    def _render_nigerian_prices(self, price_comparison: PriceComparison):
        """Render Nigerian retailer price comparison"""
        st.markdown("### 💰 Price Comparison (Converted to ₦)")
        col_range, col_best = st.columns([2, 1])
        with col_range:
            st.markdown(f"**Price Range:** {price_comparison.price_range_display}")
            if price_comparison.savings_potential:
                st.markdown(f"💰 **Potential Savings:** {CurrencyFormatter.format_naira(price_comparison.savings_potential)}")
        with col_best:
            if price_comparison.best_deal_retailer:
                st.success(f"🏆 Best Price: **{price_comparison.best_deal_retailer}**")
        
        if price_comparison.prices:
            sorted_prices = price_comparison.get_sorted_prices(ascending=True)
            num_cols = min(len(sorted_prices), 4)
            cols = st.columns(num_cols)
            for idx, price in enumerate(sorted_prices[:4]):
                retailer_info = Constants.NIGERIAN_RETAILERS.get(price.retailer_id, {})
                logo = retailer_info.get('logo', '🛒')
                with cols[idx % num_cols]:
                    is_best = idx == 0
                    border_color = "#4CAF50" if is_best else "#ddd"
                    st.markdown(f"""
                    <div style="border: 2px solid {border_color}; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 10px;">
                        <h4>{logo} {price.retailer_name}</h4>
                        <h3 style="color: {'#4CAF50' if is_best else '#333'};">{price.formatted_price}</h3>
                        {'<span style="background-color: #4CAF50; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;">BEST PRICE</span>' if is_best else ''}
                        {f'<p style="color: #888; text-decoration: line-through;">{CurrencyFormatter.format_naira(price.original_price)}</p>' if price.has_discount else ''}
                        <p style="color: {'green' if price.in_stock else 'red'};">{'✅ In Stock' if price.in_stock else '❌ Out of Stock'}</p>
                    </div>""", unsafe_allow_html=True)
                    if price.product_url:
                        st.markdown(f"[🛒 Buy from {price.retailer_name}]({price.product_url})")

        st.caption(f"Prices last updated: {price_comparison.price_last_updated.strftime('%Y-%m-%d %H:%M')}")

    def _render_red_flags(self, report: RedFlagReport):
        st.markdown("### ⚠️ Product Risk Assessment")
        col_risk, col_score, col_rec = st.columns(3)
        with col_risk:
            risk_colors = {"high": "#F44336", "medium": "#FF9800", "low": "#4CAF50"}
            risk_color = risk_colors.get(report.overall_risk_level, "#888")
            st.markdown(f'<div style="background-color: {risk_color}; color: white; padding: 15px; border-radius: 10px; text-align: center;"><h3>{report.risk_emoji} Risk Level: {report.overall_risk_level.upper()}</h3></div>', unsafe_allow_html=True)
        with col_score: st.metric("Risk Score", f"{report.risk_score:.1f}/10")
        with col_rec:
            if report.fake_review_score:
                st.metric("Fake Review Risk", f"{report.fake_review_score * 100:.0f}%")
        
        if report.red_flags:
            st.markdown("#### 🚨 Identified Issues")
            for flag in report.red_flags:
                severity_colors = {"high": "#FFEBEE", "medium": "#FFF3E0", "low": "#E3F2FD"}
                bg_color = severity_colors.get(flag.severity, "#f5f5f5")
                st.markdown(f'<div style="background-color: {bg_color}; padding: 10px; border-radius: 8px; margin: 5px 0; border-left: 4px solid {flag.severity_color};"><strong>{flag.severity_emoji} {flag.title}</strong><span style="background-color: #888; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; margin-left: 10px;">{flag.category.upper()}</span><p>{flag.description}</p></div>', unsafe_allow_html=True)
        else:
            st.success("✅ No major red flags detected!")
        
        if report.common_complaints:
            with st.expander("📋 Common User Complaints"):
                for i, c in enumerate(report.common_complaints, 1): st.markdown(f"{i}. {c}")
        st.info(report.recommendation)

    def _render_timing_advice(self, advice: PurchaseTimingAdvice):
        st.markdown("### ⏰ Purchase Timing Intelligence")
        rec_colors = {"buy_now": "#4CAF50", "wait": "#FF9800", "consider_alternatives": "#2196F3"}
        rec_color = rec_colors.get(advice.recommendation, "#888")
        st.markdown(f'<div style="background-color: {rec_color}; color: white; padding: 20px; border-radius: 10px; text-align: center;"><h2>{advice.recommendation_emoji}</h2><h3>{advice.recommendation.replace("_", " ").title()}</h3></div>', unsafe_allow_html=True)
        st.markdown(f"**📝 Analysis:** {advice.reasoning}")
        
        col_details1, col_details2 = st.columns(2)
        with col_details1:
            if advice.new_model_expected: st.warning(f"📢 **New Model Expected:** {advice.expected_release_window or 'Soon'}")
            st.markdown(f"**Price Trend:** {advice.price_trend.title()}")
        with col_details2:
            st.markdown(f"**Current Deal Quality:** {advice.current_deal_quality.upper()}")
            st.markdown(f"**Confidence:** {advice.confidence:.0%}")
        
        if advice.best_sale_periods:
            st.markdown("**🛍️ Best Times to Buy in Nigeria:**")
            for period in advice.best_sale_periods: st.markdown(f"• {period}")

    def _render_best_for_tags(self, tags: List[BestForTag], budget_tier: str = None):
        st.markdown("### 🎯 Best For...")
        col_tags, col_tier = st.columns([3, 1])
        with col_tags:
            if tags:
                tag_cols = st.columns(min(len(tags), 4))
                for idx, tag in enumerate(tags[:4]):
                    with tag_cols[idx]:
                        bg_color = "#E8F5E9" if tag.score >= 0.8 else "#FFF8E1" if tag.score >= 0.6 else "#ECEFF1"
                        st.markdown(f'<div style="background-color: {bg_color}; border-radius: 10px; padding: 15px; text-align: center;"><h4>{tag.use_case}</h4><p>{tag.score_display}</p><small>{tag.reasoning}</small></div>', unsafe_allow_html=True)
        with col_tier:
            if budget_tier:
                st.markdown(f'<div style="background-color: #2196F3; color: white; padding: 15px; border-radius: 10px; text-align: center;"><small>Budget Tier</small><h3>{budget_tier.upper()}</h3></div>', unsafe_allow_html=True)

    def _compute_fit_for_current_user(self, review: EnhancedProductReview) -> Optional[str]:
        raw_profile = st.session_state.get("user_profile")
        if not raw_profile: return None
        try: profile = UserProfile(**raw_profile)
        except: return None
        score = 50; reasons = []
        if review.price_naira and (profile.min_budget or profile.max_budget):
            p = float(review.price_naira)
            if (not profile.min_budget or p >= profile.min_budget) and (not profile.max_budget or p <= profile.max_budget):
                score += 20; reasons.append("within budget")
            else: score -= 10
        if profile.use_cases and getattr(review, "best_for_tags", None):
            u_lower = {u.lower() for u in profile.use_cases}
            matches = [t.use_case for t in review.best_for_tags if t.use_case.lower() in u_lower]
            if matches: score += 15; reasons.append(f"good for {', '.join(matches)}")
        if any(b.lower() in review.product_name.lower() for b in profile.preferred_brands):
            score += 10; reasons.append("preferred brand")
        return f"{min(100, max(0, score))}/100 ({'; '.join(reasons)})" if reasons else f"{score}/100"

    def _format_price_story(self, review: EnhancedProductReview) -> Tuple[str, str]:
        price_naira = getattr(review, "price_naira", None)
        naira_str = CurrencyFormatter.format_naira(price_naira) if price_naira else "Price unavailable"
        confidence = getattr(review, "price_confidence", "medium")
        line = f"<span class='naira-price'>Price: {naira_str}</span>"
        conf_label = f"Price confidence: {confidence.title()}"
        return line, conf_label

    def _render_decision_card(self, review: EnhancedProductReview):
        fit_text = self._compute_fit_for_current_user(review)
        price_line, _ = self._format_price_story(review)
        col_left, col_right = st.columns([1, 2])
        with col_left:
            if getattr(review, "primary_image_url", None):
                try: st.image(review.primary_image_url, use_container_width=True)
                except: pass
            st.markdown(f"### ⭐ {review.predicted_rating}")
        with col_right:
            st.markdown(f"## {review.product_name}")
            st.markdown(price_line, unsafe_allow_html=True)
            if fit_text: st.markdown(f"**🎯 Fit for You:** {fit_text}")
            if st.button("⭐ Add to shortlist", key="shortlist_add_main"):
                self._add_current_to_shortlist(review)

    def _render_alternatives(self, alternatives: List[AlternativeProduct]):
        st.markdown("### 🔁 You might also consider")
        for alt in alternatives:
            st.markdown(f"**{alt.product_name}** - {alt.snippet}")
            if st.button(f"Compare with {alt.product_name}", key=f"alt_{alt.product_name}"):
                st.session_state.comparison_mode = True
                st.session_state.comparison_products = [st.session_state.current_product, alt.product_name]
                st.rerun()

    def _add_current_to_shortlist(self, review: EnhancedProductReview):
        entry = {
            "name": review.product_name, "rating": review.predicted_rating,
            "price": CurrencyFormatter.format_naira(review.price_naira) if review.price_naira else review.price_info,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        shortlist = st.session_state.get("shortlist", [])
        if entry["name"] not in {i.get("name") for i in shortlist}:
            shortlist.append(entry)
            st.session_state.shortlist = shortlist
            st.success("Added to shortlist.")

    def _render_copy_share_summary(self, review: EnhancedProductReview):
        with st.expander("📋 Copy short summary"):
            text = f"Product: {review.product_name}\nRating: {review.predicted_rating}\nVerdict: {review.verdict[:100]}..."
            st.text_area("Summary", value=text)

    def _render_next_steps(self, review: EnhancedProductReview):
        timing = getattr(review, "timing_advice", None)
        if timing:
            st.markdown("### ▶️ What to do next")
            if timing.recommendation == "buy_now": st.markdown("- Good time to buy.")
            elif timing.recommendation == "wait": st.markdown("- Consider waiting.")
            else: st.markdown("- Consider alternatives.")

    def _render_sentiment_analysis(self, sentiment: SentimentScore):
        st.markdown("### 🎭 Sentiment Analysis")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Overall", sentiment.overall_sentiment)
        with col2: st.metric("Score", f"{sentiment.compound_score:+.2f}")
        with col3: st.metric("Tone", sentiment.emotional_tone)
        
        if sentiment.key_positive_aspects:
            st.markdown("**✅ Positives:** " + ", ".join(sentiment.key_positive_aspects))
        if sentiment.key_negative_aspects:
            st.markdown("**❌ Negatives:** " + ", ".join(sentiment.key_negative_aspects))

    def _render_current_product_sidebar(self):
        super()._render_current_product_sidebar()
        if st.session_state.review_data and hasattr(st.session_state.review_data, 'sentiment_analysis'):
            sentiment = st.session_state.review_data.sentiment_analysis
            if sentiment:
                st.markdown(f"**Sentiment:** {sentiment.overall_sentiment} {sentiment.sentiment_emoji}")

    def render_comparison_interface(self):
        st.title("⚖️ Product Comparison Mode")
        col1, col2, col3 = st.columns(3)
        with col1: p1 = st.text_input("Product 1", key="comp_prod1")
        with col2: p2 = st.text_input("Product 2", key="comp_prod2")
        with col3: p3 = st.text_input("Product 3", key="comp_prod3")
        
        if st.button("⚖️ Compare Products", type="primary"):
            prods = [p for p in [p1, p2, p3] if p.strip()]
            if len(prods) < 2: st.error("Enter at least 2 products")
            else:
                with st.spinner("Analyzing..."):
                    try:
                        comparison = self.service.generate_comparison(prods)
                        self._render_comparison_results(comparison)
                    except Exception as e: st.error(f"Comparison failed: {e}")

        if st.session_state.comparison_products:
            # Auto-run if products pre-filled
            prods = st.session_state.comparison_products
            st.session_state.comparison_products = [] # Clear to avoid loops
            with st.spinner("Analyzing..."):
                try:
                    comparison = self.service.generate_comparison(prods)
                    self._render_comparison_results(comparison)
                except Exception as e: st.error(f"Comparison failed: {e}")

        if st.button("⬅️ Back"):
            st.session_state.comparison_mode = False
            st.rerun()

    def _render_comparison_results(self, comparison: PriceComparison):
        st.markdown("---")
        st.markdown("## 📊 Comparison Results")
        if comparison.overall_winner: st.success(f"🏆 Winner: {comparison.overall_winner}")
        
        cols = st.columns(len(comparison.products))
        for idx, prod in enumerate(comparison.products):
            with cols[idx]:
                st.markdown(f"### {prod.product_name}")
                if prod.price_naira: st.markdown(f"**{CurrencyFormatter.format_naira(prod.price_naira)}**")
                st.markdown(f"Rating: {prod.rating}")
                st.markdown("**Pros:**")
                for p in prod.pros[:3]: st.markdown(f"- {p}")

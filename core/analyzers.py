"""
AI-powered analysis modules for product reviews.
"""

import json
import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timezone
from urllib.parse import quote_plus
from groq import Groq

from core.config import AppConfig
from core.models import (
    RedFlagReport, RedFlag, PurchaseTimingAdvice, ResaleAnalysis, 
    VideoProof, VideoMoment, FakeSpotterReport, AuthenticityCheck,
    VoxPopuliReport, ForumOpinion, SmartSwapReport, SmartSwapOption,
    DisasterScenario, WhatIfReport, NetPriceReport, TradeInOption
)

logger = logging.getLogger(__name__)


class RedFlagDetector:
    """Detects potential issues and red flags in product reviews"""
    
    def __init__(self, groq_client: Groq, config: AppConfig):
        self.client = groq_client
        self.config = config
        
        # Common red flag patterns
        self.defect_keywords = [
            'defective', 'broken', 'stopped working', 'died', 'malfunction',
            'not working', 'faulty', 'dead on arrival', 'DOA', 'repair',
            'replacement', 'warranty claim', 'returned'
        ]
        
        self.reliability_keywords = [
            'unreliable', 'inconsistent', 'random', 'crashes', 'freezes',
            'overheating', 'battery drain', 'slow', 'lag', 'buggy'
        ]
        
        self.fake_review_indicators = [
            'received free', 'in exchange for', 'honest review', 'disclaimer',
            'provided by', 'gifted', 'sponsored'
        ]
    
    def analyze_red_flags(self, product_name: str, review_content: str, 
                         pros: List[str], cons: List[str]) -> RedFlagReport:
        """Analyze content for potential red flags"""
        red_flags = []
        risk_score = 0.0
        
        full_text = f"{review_content} {' '.join(cons)}".lower()
        
        # Check for defect patterns
        defect_count = sum(1 for keyword in self.defect_keywords if keyword in full_text)
        if defect_count >= 3:
            red_flags.append(RedFlag(
                severity="high",
                category="defect",
                title="Multiple Defect Reports",
                description=f"Found {defect_count} references to defects or malfunctions in reviews.",
                affected_percentage=min(defect_count * 10, 50)
            ))
            risk_score += 3.0
        elif defect_count >= 1:
            red_flags.append(RedFlag(
                severity="medium",
                category="defect",
                title="Some Defect Reports",
                description="Some users reported defects or issues.",
                affected_percentage=defect_count * 5
            ))
            risk_score += 1.5
        
        # Check for reliability issues
        reliability_count = sum(1 for keyword in self.reliability_keywords if keyword in full_text)
        if reliability_count >= 2:
            red_flags.append(RedFlag(
                severity="medium",
                category="reliability",
                title="Reliability Concerns",
                description="Multiple mentions of reliability or performance issues."
            ))
            risk_score += 2.0
        
        # Analyze cons severity
        severe_cons = [con for con in cons if any(word in con.lower() for word in 
                      ['major', 'serious', 'critical', 'deal-breaker', 'avoid'])]
        if severe_cons:
            red_flags.append(RedFlag(
                severity="medium",
                category="reliability",
                title="Serious Drawbacks Noted",
                description=f"Reviewers identified {len(severe_cons)} significant concerns."
            ))
            risk_score += 1.5
        
        # Check for fake review indicators
        fake_count = sum(1 for indicator in self.fake_review_indicators if indicator in full_text)
        fake_review_score = min(fake_count * 0.15, 0.5)
        if fake_count >= 2:
            red_flags.append(RedFlag(
                severity="low",
                category="fake_reviews",
                title="Potential Incentivized Reviews",
                description="Some reviews may have been incentivized or sponsored."
            ))
        
        # Extract common complaints from cons
        common_complaints = cons[:5] if cons else []
        
        # Determine overall risk level
        if risk_score >= 5:
            overall_risk = "high"
        elif risk_score >= 2:
            overall_risk = "medium"
        else:
            overall_risk = "low"
        
        # Generate recommendation
        if overall_risk == "high":
            recommendation = "⚠️ Proceed with caution. Consider alternatives or ensure good return policy."
        elif overall_risk == "medium":
            recommendation = "✅ Generally safe to purchase, but be aware of reported issues."
        else:
            recommendation = "✅ No major red flags detected. Product appears reliable."
        
        return RedFlagReport(
            product_name=product_name,
            red_flags=red_flags,
            overall_risk_level=overall_risk,
            risk_score=min(risk_score, 10.0),
            fake_review_score=fake_review_score,
            common_complaints=common_complaints,
            recommendation=recommendation
        )
    
    @property
    def has_critical_issues(self) -> bool:
        """Helper to unify 'critical' check if needed (not part of model, but logic)"""
        # This logic is usually outside, but good to know: high risk = critical
        return False # Placeholder if needed


class PurchaseTimingAdvisor:
    """Provides purchase timing recommendations"""
    
    def __init__(self, groq_client: Groq, config: AppConfig):
        self.client = groq_client
        self.config = config
        
        # Nigerian sale periods
        self.sale_periods = {
            'black_friday': {'months': [11], 'name': 'Black Friday (November)'},
            'boxing_day': {'months': [12], 'name': 'Boxing Day Sales (December)'},
            'new_year': {'months': [1], 'name': 'New Year Sales (January)'},
            'independence': {'months': [10], 'name': 'Independence Day Sales (October)'},
            'easter': {'months': [3, 4], 'name': 'Easter Sales (March/April)'},
            'back_to_school': {'months': [8, 9], 'name': 'Back to School (August/September)'}
        }
        
        # Product release patterns (approximate)
        self.release_patterns = {
            'iphone': {'typical_month': 9, 'cycle_years': 1},
            'samsung galaxy': {'typical_month': 2, 'cycle_years': 1},
            'pixel': {'typical_month': 10, 'cycle_years': 1},
            'macbook': {'typical_month': 6, 'cycle_years': 1.5},
            'ipad': {'typical_month': 3, 'cycle_years': 1.5},
            'playstation': {'typical_month': 11, 'cycle_years': 7},
            'xbox': {'typical_month': 11, 'cycle_years': 7},
        }
    
    def get_timing_advice(self, product_name: str, current_price: Optional[float] = None, 
                         context: str = "") -> PurchaseTimingAdvice:
        """Generate purchase timing recommendation"""
        product_lower = product_name.lower()
        current_month = datetime.now(timezone.utc).month
        
        # Determine lifecycle stage
        lifecycle_stage = self._determine_lifecycle(product_lower)
        
        # Find upcoming sales
        best_sale_periods = self._get_upcoming_sales(current_month)
        
        # Check for new model timing
        new_model_expected, release_window = self._check_new_model(product_lower)
        
        # Determine price trend (simplified)
        price_trend = "stable"
        
        # Generate recommendation
        recommendation, reasoning = self._generate_recommendation(
            lifecycle_stage, new_model_expected, current_month, best_sale_periods
        )
        
        # Determine deal quality
        deal_quality = self._assess_deal_quality(current_month)
        
        return PurchaseTimingAdvice(
            product_name=product_name,
            lifecycle_stage=lifecycle_stage,
            recommendation=recommendation,
            reasoning=reasoning,
            new_model_expected=new_model_expected,
            expected_release_window=release_window,
            best_sale_periods=best_sale_periods,
            current_deal_quality=deal_quality,
            price_trend=price_trend,
            confidence=0.7 if new_model_expected else 0.5
        )
    
    def _determine_lifecycle(self, product_lower: str) -> str:
        """Determine product lifecycle stage"""
        current_year = datetime.now(timezone.utc).year
        
        for year in range(current_year, current_year - 5, -1):
            if str(year) in product_lower:
                age = current_year - year
                if age == 0:
                    return "new"
                elif age == 1:
                    return "mature"
                elif age >= 2:
                    return "end_of_life"
        
        if any(word in product_lower for word in ['latest', 'new', '2024', '2025']):
            return "new"
        elif any(word in product_lower for word in ['previous', 'last gen', 'older']):
            return "end_of_life"
        
        return "mature"
    
    def _get_upcoming_sales(self, current_month: int) -> List[str]:
        """Get upcoming sale periods"""
        upcoming = []
        months_to_check = [(current_month + i - 1) % 12 + 1 for i in range(6)]
        
        for period_name, period_info in self.sale_periods.items():
            if any(month in period_info['months'] for month in months_to_check[:4]):
                upcoming.append(period_info['name'])
        
        return upcoming[:3]
    
    def _check_new_model(self, product_lower: str) -> Tuple[bool, Optional[str]]:
        """Check if new model might be coming"""
        current_month = datetime.now(timezone.utc).month
        
        for product_type, pattern in self.release_patterns.items():
            if product_type in product_lower:
                months_until_release = (pattern['typical_month'] - current_month) % 12
                if months_until_release <= 3:
                    quarter = (pattern['typical_month'] - 1) // 3 + 1
                    return True, f"Q{quarter} {datetime.now(timezone.utc).year}"
        
        return False, None
    
    def _generate_recommendation(self, lifecycle: str, new_model: bool, 
                                current_month: int, upcoming_sales: List[str]) -> Tuple[str, str]:
        """Generate purchase recommendation"""
        in_sale_period = current_month in [11, 12, 1]  # Black Friday to New Year
        
        if new_model and lifecycle == "mature":
            return "wait", f"New model expected soon. Wait for release or price drop on current model."
        elif in_sale_period:
            return "buy_now", f"Good time to buy! Current sale season offers best prices."
        elif upcoming_sales and lifecycle != "new":
            return "wait", f"Consider waiting for {upcoming_sales[0]} for better deals."
        elif lifecycle == "new":
            return "buy_now", "New product at peak value. Buy now if you need the latest features."
        elif lifecycle == "end_of_life":
            return "consider_alternatives", "Product is aging. Consider newer alternatives unless price is very attractive."
        else:
            return "buy_now", "Product is at a stable point in its lifecycle. Safe to purchase."
    
    def _assess_deal_quality(self, current_month: int) -> str:
        """Assess current deal quality based on timing"""
        excellent_months = [11, 12]  # Black Friday, Christmas
        good_months = [1, 6, 7]  # New Year, Mid-year sales
        
        if current_month in excellent_months:
            return "excellent"
        elif current_month in good_months:
            return "good"
        else:
            return "normal"


class ResaleAnalyzer:
    """Analyzes product resale value and depreciation trends"""

    def __init__(self, groq_client: Groq, config: AppConfig):
        self.client = groq_client
        self.config = config

    def analyze_resale_value(self, product_name: str, price_naira: Optional[float]) -> ResaleAnalysis:
        """Generate resale value forecast"""
        try:
            current_price_desc = f"Current Price: ₦{price_naira:,.2f}" if price_naira else "Current Price: Unknown (Estimate based on market)"
        
            prompt = f"""
            Analyze the potential resale value and depreciation for '{product_name}'.
            {current_price_desc}
        
            Focus on:
            1. Brand value retention (e.g. Apple vs Android vs Generic).
            2. Typical depreciation curves for this product category.
            3. Demand in the Nigerian used market.
        
            Return JSON matching this schema:
            {{
                "predicted_value_1yr": "e.g. 75% (approx ₦XXX,XXX)",
                "predicted_value_3yr": "e.g. 45% (approx ₦XXX,XXX)",
                "depreciation_rate": "Fast/Moderate/Slow",
                "investment_score": 0-10 (integer, 10=excellent retention),
                "verdict": "e.g. Buy New / Buy Used / Good Short-term"
            }}
            """
        
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a valuation expert for consumer products in Nigeria, covering electronics, appliances, vehicles, fashion, and more."},
                    {"role": "user", "content": prompt}
                ],
                model=self.config.model_name,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
        
            data = json.loads(completion.choices[0].message.content)
        
            return ResaleAnalysis(
                predicted_value_1yr=data.get("predicted_value_1yr", "Unknown"),
                predicted_value_3yr=data.get("predicted_value_3yr", "Unknown"),
                depreciation_rate=data.get("depreciation_rate", "Moderate"),
                investment_score=int(data.get("investment_score", 5)),
                verdict=data.get("verdict", "Neutral")
            )
        
        except Exception as e:
            logger.warning(f"Resale analysis failed: {e}")
            return ResaleAnalysis(
                predicted_value_1yr="Unknown",
                predicted_value_3yr="Unknown",
                depreciation_rate="Unknown",
                investment_score=0,
                verdict="Unknown"
            )


class VideoProofFinder:
    """Generates targeted YouTube search queries for verification"""

    def __init__(self, groq_client: Groq, config: AppConfig):
        self.client = groq_client
        self.config = config

    def find_video_proofs(self, product_name: str, pros: List[str], cons: List[str]) -> VideoProof:
        """Identify key moments to verify and generate search links"""
        try:
            prompt = f"""
            Identify 3-5 specific "Video Proof" moments for '{product_name}' that a user should watch to verify claims.
            Focus on visual/audible tests (e.g., Camera Zoom, Mic Quality, hinge durability, screen brightness).
        
            Pros: {json.dumps(pros)}
            Cons: {json.dumps(cons)}
        
            Return JSON matching this schema:
            {{
                "moments": [
                    {{
                        "label": "e.g. 50x Zoom Test",
                        "search_query": "e.g. {product_name} 50x zoom camera test",
                        "description": "Watch for stabilization issues at max zoom"
                    }}
                ]
            }}
            """
        
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a product reviewer creating verification guides for any product category."},
                    {"role": "user", "content": prompt}
                ],
                model=self.config.model_name,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
        
            data = json.loads(completion.choices[0].message.content)
        
            moments = []
            for m in data.get("moments", []):
                # Construct YouTube URL
                query = quote_plus(m.get("search_query", ""))
                url = f"https://www.youtube.com/results?search_query={query}"
                moments.append(VideoMoment(
                    label=m.get("label", ""),
                    search_query=m.get("search_query", ""),
                    youtube_url=url,
                    description=m.get("description", "")
                ))
        
            return VideoProof(moments=moments)
        
        except Exception as e:
            logger.warning(f"Video proof finding failed: {e}")
            return VideoProof(moments=[])


class FakeSpotter:
    """Analyzes products for counterfeit risks and generates verification guides"""

    def __init__(self, groq_client: Groq, config: AppConfig):
        self.client = groq_client
        self.config = config

    def analyze_authenticity(self, product_name: str, scraped_text: str) -> FakeSpotterReport:
        """Generate counterfeit detection guide"""
        try:
            prompt = f"""
            Create a "Fake Spotter" guide for '{product_name}'.
            The Nigerian market has many counterfeit and refurbished products.
        
            IMPORTANT: Generate scams and checks SPECIFIC to this exact product type.
            - For PHONES: Focus on fake IMEI, cloned devices, refurbished batteries
            - For LAPTOPS: Focus on fake specs, replaced GPUs, dead pixels
            - For APPLIANCES: Focus on fake watts, non-genuine parts, missing warranty
            - For FASHION: Focus on stitching, labels, materials
            - For ELECTRONICS: Focus on serial verification, genuine accessories
            
            DO NOT use generic examples. Every scam must be relevant to '{product_name}'.
        
            Focus on:
            1. Risk Level: How common are fakes for THIS SPECIFIC item?
            2. Common Scams: List 2-3 scams SPECIFIC to this product (not generic examples)
            3. Verification Steps: Specific checks for THIS product type
        
            Context:
            {scraped_text[:2000]}
        
            Return JSON matching this schema:
            {{
                "risk_level": "High/Medium/Low",
                "common_scams": ["Specific scam for this product", "Another specific scam"],
                "verification_steps": [
                    {{
                        "check_type": "Physical/Software/Serial/Packaging",
                        "instruction": "Specific check for this product",
                        "expected_result": "What authentic product should show",
                        "warning_sign": "What indicates counterfeit"
                    }}
                ]
            }}
            """
        
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a counterfeit detection expert specialized in the Nigerian market, covering electronics, appliances, fashion, and other product categories."},
                    {"role": "user", "content": prompt}
                ],
                model=self.config.model_name,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
        
            data = json.loads(completion.choices[0].message.content)
        
            steps = [AuthenticityCheck(**s) for s in data.get("verification_steps", [])]
        
            return FakeSpotterReport(
                risk_level=data.get("risk_level", "Low"),
                common_scams=data.get("common_scams", []),
                verification_steps=steps
            )
        
        except Exception as e:
            logger.warning(f"Fake spotter analysis failed: {e}")
            return FakeSpotterReport(
                risk_level="Unknown",
                common_scams=[],
                verification_steps=[]
            )


class VoxPopuliAnalyzer:
    """Analyzes owner sentiment from forums like Nairaland, Reddit, and Twitter"""

    def __init__(self, groq_client: Groq, config: AppConfig):
        self.client = groq_client
        self.config = config

    def analyze_owner_sentiment(self, product_name: str, scraped_text: str) -> VoxPopuliReport:
        """Generate forum sentiment digest"""
        try:
            prompt = f"""
            Act as a forum lurker on Nairaland, Reddit (r/gadgets), and Twitter/X.
            What are REAL owners saying about '{product_name}' after using it for months?
            Ignore the spec sheet. Focus on the "hidden truths" - bugs, overheating, battery drain, or surprisingly good features.
        
            Context:
            {scraped_text[:3000]}
        
            Return JSON matching this schema:
            {{
                "owner_verdict": "e.g. Great camera, but the battery will betray you at 6pm.",
                "love_it_for": ["Feature 1", "Feature 2"],
                "hate_it_for": ["Complaint 1", "Complaint 2"],
                "forum_consensus": [
                    {{
                        "platform": "Nairaland",
                        "sentiment": "Positive/Mixed/Negative",
                        "key_takeaway": "e.g. Many users complaining about price vs value"
                    }},
                    {{
                        "platform": "Reddit",
                        "sentiment": "Positive/Mixed/Negative",
                        "key_takeaway": "e.g. Praised for longevity but hated for slow charging"
                    }}
                ]
            }}
            """
        
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a forum analyst who cuts through marketing hype for any product category."},
                    {"role": "user", "content": prompt}
                ],
                model=self.config.model_name,
                temperature=0.4,
                response_format={"type": "json_object"}
            )
        
            data = json.loads(completion.choices[0].message.content)
        
            opinions = [ForumOpinion(**o) for o in data.get("forum_consensus", [])]
        
            return VoxPopuliReport(
                owner_verdict=data.get("owner_verdict", "No widespread consensus yet."),
                love_it_for=data.get("love_it_for", []),
                hate_it_for=data.get("hate_it_for", []),
                forum_consensus=opinions
            )
        
        except Exception as e:
            logger.warning(f"Vox Populi analysis failed: {e}")
            return VoxPopuliReport(
                owner_verdict="Data unavailable",
                love_it_for=[],
                hate_it_for=[],
                forum_consensus=[]
            )


class SmartSwapAnalyzer:
    """Identifies used/refurbished flagship alternatives that offer better value"""

    def __init__(self, groq_client: Groq, config: AppConfig):
        self.client = groq_client
        self.config = config

    def analyze_swap_options(self, product_name: str, price_naira: float) -> SmartSwapReport:
        """Generate Smart Swap alternatives"""
        if not price_naira or price_naira == 0:
            return SmartSwapReport(base_price=0, recommendation="Keep Original", swaps=[])

        try:
            price_str = f"{price_naira:,.0f}"
            prompt = f"""
The user is considering buying a NEW '{product_name}' for ₦{price_str}.

Find 2-3 USED, REFURBISHED, or OLDER PREMIUM alternatives in the SAME PRODUCT CATEGORY 
available in Nigeria for roughly the SAME PRICE.

Requirements:
- Alternatives must be objectively BETTER (higher specs, professional grade, premium build)
- Match the exact product category (phones→phones, TVs→TVs, blenders→blenders)
- ALL PRICES MUST BE IN NIGERIAN NAIRA (₦) - no USD or other currencies
- Use realistic Nigerian market prices from Jumia, Konga, or Jiji

Return JSON:
{{
    "recommendation": "Swap Recommended" or "Keep Original",
    "swaps": [
        {{
            "product_name": "Full product name",
            "price": "₦XXX,XXX (REQUIRED - actual Nigerian market price)",
            "condition": "Used/Refurbished/Like New",
            "performance_diff": "+XX% better in key metric",
            "reason_to_buy": "Why this is a smart swap",
            "reason_to_avoid": "Potential downside"
        }}
    ]
}}
"""
        
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a financial advisor for all product categories. You find value in used premium goods across electronics, appliances, vehicles, fashion, and more."},
                    {"role": "user", "content": prompt}
                ],
                model=self.config.model_name,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
        
            data = json.loads(completion.choices[0].message.content)
        
            swaps = [SmartSwapOption(**s) for s in data.get("swaps", [])]
        
            return SmartSwapReport(
                base_price=price_naira,
                recommendation=data.get("recommendation", "Keep Original"),
                swaps=swaps
            )
        
        except Exception as e:
            logger.warning(f"Smart Swap analysis failed: {e}")
            return SmartSwapReport(
                base_price=price_naira,
                recommendation="Keep Original",
                swaps=[]
            )


class DisasterAnalyzer:
    """Simulates random Nigerian disaster scenarios to test durability"""

    def __init__(self, groq_client: Groq, config: AppConfig):
        self.client = groq_client
        self.config = config

    def simulate_disasters(self, product_name: str, category: str) -> WhatIfReport:
        """Run disaster simulation"""
        try:
            prompt = f"""
            Simulate 3 realistic, culturally relevant Nigerian disaster scenarios for '{product_name}' (Category: {category}).
            Focus on Environmental Hazards (Dust/Heat), Infrastructure Failures (Power Surge), or Daily Chaos (Danfo Bus/Market Crowds).
        
            Determine if the product survives based on its known durability (IP rating, build materials, cooling).
        
            Return JSON matching this schema:
            {{
                "disaster_score": 7, (Overall resilience 1-10)
                "scenarios": [
                    {{
                        "name": "The Danfo Drop",
                        "scenario": "You are jostled in a packed Danfo and the device falls face-down on metal flooring.",
                        "outcome": "Cracked Screen",
                        "repair_cost_estimate": "NGN 120,000",
                        "survivability_score": 4
                    }}
                ]
            }}
            """
        
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a stress-test engineer specializing in African operating conditions."},
                    {"role": "user", "content": prompt}
                ],
                model=self.config.model_name,
                temperature=0.5,
                response_format={"type": "json_object"}
            )
        
            data = json.loads(completion.choices[0].message.content)
            scenarios = [DisasterScenario(**s) for s in data.get("scenarios", [])]
        
            return WhatIfReport(
                disaster_score=data.get("disaster_score", 5),
                scenarios=scenarios
            )
        except Exception as e:
            logger.warning(f"Disaster simulation failed: {e}")
            return WhatIfReport(disaster_score=0, scenarios=[])


class NetPriceAnalyzer:
    """Calculates upgrade cost by estimating trade-in values of predecessors"""

    def __init__(self, groq_client: Groq, config: AppConfig):
        self.client = groq_client
        self.config = config

    def calculate_net_price(self, product_name: str, current_price: float) -> NetPriceReport:
        """Identify predecessors and calculate net upgrade cost"""
        if not current_price:
            return NetPriceReport(upgrade_from=[])
        
        try:
            price_str = f"{current_price:,.0f}"
            prompt = (
                f"The user wants to buy '{product_name}' (Price: NGN {price_str}). "
                f"We need to identify potential trade-in options, but ONLY if valid for this product category. "
                f"\n\nStep 1: Identify the exact product category of '{product_name}' (e.g., Smartphone, Blender, Generator, Laptop, Shoe). "
                f"\n\nStep 2: Check if this category typically has an active 'trade-in' market in Nigeria. "
                f"   - Valid Categories: Smartphones, Laptops, Tablets, Gaming Consoles, Smartwatches, High-End Cameras. "
                f"   - Invalid Categories: Home Appliances (Blenders, Irons), Fashion, Generators, Furniture, Food, Accessories. "
                f"\n\nStep 3: "
                f"   - IF INVALID: Return an empty 'upgrade_from' list immediately. "
                f"   - IF VALID: Identify 3 common OLDER models or PREDECESSORS that users usually upgrade FROM to get '{product_name}'. "
                f"     * CRITICAL: The predecessors MUST match the exact product category. (e.g. if Laptop, list Laptops). "
                f"     * DO NOT list phones if the product is not a phone. "
                f"     * Estimate their current Used/Trade-In value in Nigeria. "
                f"\n\nReturn JSON with key 'upgrade_from' containing array of objects with device_name, estimated_value (number), and net_price (number = {current_price} minus estimated_value)"
            )
        
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a trade-in expert. You are extremely strict about product categories. You NEVER suggest phone trade-ins for non-phone products."},
                    {"role": "user", "content": prompt}
                ],
                model=self.config.model_name,
                temperature=0.1,  # Lower temperature for strictness
                response_format={"type": "json_object"}
            )
        
            data = json.loads(completion.choices[0].message.content)
        
            # Recalculate net_price ensuring no negatives
            opts = []
            for o in data.get("upgrade_from", []):
                try:
                    est_val = float(o.get("estimated_value", 0))
                except Exception:
                    est_val = 0
                net = max(0, current_price - est_val)
                opts.append(TradeInOption(device_name=o.get("device_name", ""), estimated_value=est_val, net_price=net))
        
            return NetPriceReport(upgrade_from=opts)
        except Exception as e:
            logger.warning(f"Net price calculation failed: {e}")
            return NetPriceReport(upgrade_from=[])

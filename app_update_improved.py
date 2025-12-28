# This file contains the improved review summary formatting
# Replace the review_summary section in app_update.py (around line 5940) with this:

review_summary = f"""## 📱 {review_data.product_name}

---

### ⭐ Rating & Score
**Rating:** {review_data.predicted_rating} ⭐

{f'''### 💰 Pricing
{price_text}
**Price:** {review_data.price_info}
''' if hasattr(review_data, 'price_comparison') or review_data.price_info else ''}

---

### 🔧 Specifications
{review_data.specifications_inferred}

---

### ✅ Top Strengths
{chr(10).join([f"• {pro}" for pro in review_data.pros[:3]])}

### ⚠️ Main Weaknesses
{chr(10).join([f"• {con}" for con in review_data.cons[:3]])}

---

### 📝 Verdict
{review_data.verdict[:300]}...

{sentiment_text if sentiment else ''}

{timing_text if hasattr(review_data, 'timing_advice') and review_data.timing_advice else ''}

{risk_text if hasattr(review_data, 'red_flag_report') and review_data.red_flag_report else ''}

---

**📊 Data Source:** {review_data.data_source_type.replace('_', ' ').title()}
{f"**🖼️ Images Found:** {len(review_data.product_images)}" if hasattr(review_data, 'product_images') else ''}

💬 **Ask me anything about this product!**
"""

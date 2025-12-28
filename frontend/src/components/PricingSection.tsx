import React from "react";
import type { EnhancedProductReview } from "../api/types";
import { DollarSign, TrendingDown, TrendingUp, Store, Award, Tag, BarChart3, ShieldCheck } from "lucide-react";

interface Props {
  review: EnhancedProductReview;
}

const getDealBadgeStyle = (quality: string) => {
  const lower = quality.toLowerCase();
  if (lower === "excellent" || lower === "great") {
    return { className: "deal-badge excellent", icon: "🔥" };
  }
  if (lower === "good") {
    return { className: "deal-badge good", icon: "👍" };
  }
  if (lower === "fair" || lower === "average") {
    return { className: "deal-badge fair", icon: "➡️" };
  }
  if (lower === "poor" || lower === "overpriced") {
    return { className: "deal-badge poor", icon: "⚠️" };
  }
  return { className: "deal-badge", icon: "💰" };
};

const PricingSection: React.FC<Props> = ({ review }) => {
  const naira = review?.price_naira ?? null;
  const priceDisplay = naira ?? review.price_info;
  const pc = review.price_comparison;

  const dealStyle = pc?.deal_quality ? getDealBadgeStyle(pc.deal_quality) : null;

  return (
    <section className="section pricing-section">
      <div className="pricing-header">
        <DollarSign className="section-icon" size={20} />
        <h3>Pricing & Value</h3>
      </div>

      {/* Main Price Card */}
      <div className="main-price-card">
        <div className="price-label">Current Price</div>
        <div className="price-value">
          {typeof priceDisplay === "number"
            ? `₦${priceDisplay.toLocaleString()}`
            : priceDisplay || "Price unavailable"}
        </div>
        {review.original_price_display && (
          <div className="original-price">
            <Tag size={14} />
            <span>{review.original_price_display}</span>
          </div>
        )}
      </div>

      {/* Price Comparison Details */}
      {pc && (
        <div className="price-comparison-grid">
          {/* Price Range */}
          {(Number.isFinite(pc?.lowest_price ?? NaN) && Number.isFinite(pc?.highest_price ?? NaN)) && (
            <div className="price-stat-card">
              <div className="stat-icon range">
                <BarChart3 size={18} />
              </div>
              <div className="stat-content">
                <span className="stat-label">Nigerian Price Range</span>
                <span className="stat-value">
                  ₦{(pc!.lowest_price ?? 0).toLocaleString()} - ₦{(pc!.highest_price ?? 0).toLocaleString()}
                </span>
              </div>
            </div>
          )}

          {/* Best Retailer */}
          {pc.best_deal_retailer && (
            <div className="price-stat-card best-deal">
              <div className="stat-icon store">
                <Store size={18} />
              </div>
              <div className="stat-content">
                <span className="stat-label">Best Deal At</span>
                <span className="stat-value highlight">{pc.best_deal_retailer}</span>
              </div>
              <Award className="best-badge" size={16} />
            </div>
          )}

          {/* Deal Quality */}
          {dealStyle && pc.deal_quality && (
            <div className="price-stat-card deal-quality">
              <div className={dealStyle.className}>
                <span className="deal-icon">{dealStyle.icon}</span>
                <span className="deal-text">{pc.deal_quality.toUpperCase()}</span>
              </div>
              {pc.deal_explanation && (
                <p className="deal-explanation">{pc.deal_explanation}</p>
              )}
            </div>
          )}
        </div>
      )}

      {/* Confidence Indicator */}
      {review.price_confidence && (
        <div className="price-confidence">
          <ShieldCheck size={14} />
          <span>Confidence: {review.price_confidence}</span>
        </div>
      )}
    </section>
  );
};

export default PricingSection;

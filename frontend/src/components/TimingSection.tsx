import React from "react";
import { safeArray, safeNum, safeFixed } from "../utils/safeHelpers";
import { Clock, TrendingUp, TrendingDown, Minus, Calendar, Tag, Zap } from "lucide-react";
import type { EnhancedProductReview } from "../api/types";

interface Props {
  review: EnhancedProductReview;
}

const TimingSection: React.FC<Props> = ({ review }) => {
  const t = review.timing_advice;
  if (!t) return null;

  const getRecommendationConfig = (rec: string) => {
    switch (rec) {
      case "buy_now":
        return { color: "#10b981", bg: "#10b98120", icon: <Zap size={18} />, label: "Buy Now" };
      case "wait":
        return { color: "#f59e0b", bg: "#f59e0b20", icon: <Clock size={18} />, label: "Wait" };
      case "consider_alternatives":
        return { color: "#6366f1", bg: "#6366f120", icon: <Tag size={18} />, label: "Consider Alternatives" };
      default:
        return { color: "#6b7280", bg: "#6b728020", icon: <Clock size={18} />, label: rec.replace("_", " ") };
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend?.toLowerCase()) {
      case "rising": return <TrendingUp size={16} style={{ color: "#ef4444" }} />;
      case "falling": return <TrendingDown size={16} style={{ color: "#10b981" }} />;
      default: return <Minus size={16} style={{ color: "#6b7280" }} />;
    }
  };

  const config = getRecommendationConfig(t.recommendation ?? '');

  return (
    <section className="timing-section">
      <div className="timing-header">
        <div className="timing-icon">
          <Clock size={24} />
        </div>
        <div>
          <h3>When to Buy</h3>
          <p className="timing-subtitle">Purchase timing intelligence</p>
        </div>
      </div>

      <div className="timing-recommendation">
        <div className="recommendation-badge" style={{ background: config.bg, color: config.color }}>
          {config.icon}
          <span>{config.label}</span>
        </div>
        {t.lifecycle_stage && (
          <span className="lifecycle-badge">
            {t.lifecycle_stage.replace("_", " ")}
          </span>
        )}
      </div>

      <div className="timing-reasoning">
        <p>{t.reasoning}</p>
      </div>

      <div className="timing-details">
        {t.price_trend && (
          <div className="timing-detail-item">
            {getTrendIcon(t.price_trend)}
            <span>Price trend: <strong>{t.price_trend}</strong></span>
          </div>
        )}
        {t.current_deal_quality && (
          <div className="timing-detail-item">
            <Tag size={16} style={{ color: "#6366f1" }} />
            <span>Deal quality: <strong>{t.current_deal_quality}</strong></span>
          </div>
        )}
        {t.expected_release_window && (
          <div className="timing-detail-item">
            <Calendar size={16} style={{ color: "#8b5cf6" }} />
            <span>Next model: <strong>{t.expected_release_window}</strong></span>
          </div>
        )}
      </div>

        {safeArray(t.best_sale_periods).length > 0 && (
        <div className="sale-periods">
          <span className="sale-periods-label">Best times to buy:</span>
          <div className="sale-chips">
            {safeArray(t.best_sale_periods).map((period, idx) => (
              <span key={idx} className="sale-chip">
                <Calendar size={12} />
                {period}
              </span>
            ))}
          </div>
        </div>
      )}

      {t.confidence !== undefined && (
        <div className="timing-confidence">
          <span>Confidence: {(t.confidence * 100).toFixed(0)}%</span>
          <div className="confidence-bar-bg">
            <div className="confidence-bar" style={{ width: `${t.confidence * 100}%` }} />
          </div>
        </div>
      )}
    </section>
  );
};

export default TimingSection;

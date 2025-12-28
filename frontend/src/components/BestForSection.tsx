import React from "react";
import type { EnhancedProductReview } from "../api/types";
import { Target, Users, Briefcase, Gamepad2, Camera, Music, Palette, GraduationCap, Heart, Zap, Award } from "lucide-react";

// Icon mapping for use cases
const getUseCaseIcon = (useCase: string) => {
  const lowered = useCase.toLowerCase();
  if (lowered.includes("gaming") || lowered.includes("game")) return Gamepad2;
  if (lowered.includes("photo") || lowered.includes("camera")) return Camera;
  if (lowered.includes("music") || lowered.includes("audio")) return Music;
  if (lowered.includes("creative") || lowered.includes("design") || lowered.includes("art")) return Palette;
  if (lowered.includes("student") || lowered.includes("education") || lowered.includes("learning")) return GraduationCap;
  if (lowered.includes("business") || lowered.includes("professional") || lowered.includes("work")) return Briefcase;
  if (lowered.includes("family") || lowered.includes("home")) return Heart;
  if (lowered.includes("power") || lowered.includes("performance")) return Zap;
  if (lowered.includes("team") || lowered.includes("collaboration")) return Users;
  return Target;
};

// Budget tier styling
const getBudgetTierStyle = (tier: string) => {
  const lowered = tier.toLowerCase();
  if (lowered.includes("budget") || lowered.includes("entry")) {
    return { className: "budget-tier-badge budget", label: "💰 Budget-Friendly" };
  }
  if (lowered.includes("mid") || lowered.includes("value")) {
    return { className: "budget-tier-badge mid-range", label: "⚖️ Mid-Range Value" };
  }
  if (lowered.includes("premium") || lowered.includes("high") || lowered.includes("flagship")) {
    return { className: "budget-tier-badge premium", label: "✨ Premium Segment" };
  }
  return { className: "budget-tier-badge", label: tier };
};

const BestForSection: React.FC<{ review: EnhancedProductReview }> = ({ review }) => {
  const tags = review.best_for_tags ?? [];
  if (tags.length === 0 && !review.budget_tier) return null;

  const tierStyle = review.budget_tier ? getBudgetTierStyle(review.budget_tier) : null;

  return (
    <section className="section best-for-section">
      <div className="best-for-header">
        <Award className="section-icon" size={20} />
        <h3>Ideal For</h3>
      </div>

      {tierStyle && (
        <div className={tierStyle.className}>
          {tierStyle.label}
        </div>
      )}

      {tags.length > 0 && (
        <div className="best-for-tags">
          {tags.map((t) => {
            const Icon = getUseCaseIcon(t.use_case);
            const score = t.score ?? 0;
            return (
              <div key={t.use_case} className="best-for-tag">
                <div className="tag-icon-wrapper">
                  <Icon size={18} />
                </div>
                <div className="tag-content">
                  <span className="tag-label">{t.use_case}</span>
                  {score > 0 && (
                    <div className="tag-score">
                      <div className="score-bar">
                        <div
                          className="score-fill"
                          style={{ width: `${Math.min(score * 10, 100)}%` }}
                        />
                      </div>
                      <span className="score-value">{score}/10</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
};

export default BestForSection;

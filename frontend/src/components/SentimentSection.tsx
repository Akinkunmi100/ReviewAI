import React from "react";
import type { EnhancedProductReview, AspectBreakdownItem } from "../api/types";

const SentimentSection: React.FC<{ review: EnhancedProductReview }> = ({ review }) => {
  const s = review?.sentiment_analysis;
  const aspects: AspectBreakdownItem[] = review?.aspect_breakdown ?? [];

  if (!s && aspects.length === 0) return null;

  function sentimentColor(score: number): string {
    if (score >= 0.5) return "#4CAF50";
    if (score >= 0.1) return "#8BC34A";
    if (score >= -0.1) return "#FFC107";
    if (score >= -0.5) return "#FF9800";
    return "#F44336";
  }

  return (
    <section className="section">
      <h3>Sentiment</h3>
      {s && (
        <div className="sentiment-summary-cards">
          {/* Overall Verdict */}
          <div className={`sentiment-card ${s.overall_sentiment?.toLowerCase() || 'neutral'}`}>
            <div className="sentiment-card-icon">
              {s.overall_sentiment === 'Positive' ? '😊' : s.overall_sentiment === 'Negative' ? '😟' : '😐'}
            </div>
            <div className="sentiment-card-content">
              <span className="sentiment-card-label">Overall Verdict</span>
              <span className="sentiment-card-value">{s.overall_sentiment || 'Mixed'}</span>
              <span className="sentiment-card-desc">
                {s.overall_sentiment === 'Positive'
                  ? 'Reviewers are generally happy with this product'
                  : s.overall_sentiment === 'Negative'
                    ? 'Reviewers have significant concerns about this product'
                    : 'Reviews show a mix of positive and negative opinions'}
              </span>
            </div>
          </div>

          {/* Emotional Tone */}
          <div className="sentiment-card tone">
            <div className="sentiment-card-icon">🎭</div>
            <div className="sentiment-card-content">
              <span className="sentiment-card-label">Reviewer Mood</span>
              <span className="sentiment-card-value">{s.emotional_tone || 'Balanced'}</span>
              <span className="sentiment-card-desc">
                {s.emotional_tone?.includes('Enthusiastic') || s.emotional_tone?.includes('Satisfied')
                  ? 'People who bought this are happy with their purchase'
                  : s.emotional_tone?.includes('Disappointed') || s.emotional_tone?.includes('Frustrated')
                    ? 'Many buyers express regret or frustration'
                    : 'Buyers have balanced expectations'}
              </span>
            </div>
          </div>

          {/* Confidence */}
          <div className="sentiment-card confidence">
            <div className="sentiment-card-icon">📊</div>
            <div className="sentiment-card-content">
              <span className="sentiment-card-label">Analysis Confidence</span>
              <div className="confidence-bar">
                <div
                  className="confidence-fill"
                  style={{ width: `${Math.round((s.sentiment_confidence || 0.5) * 100)}%` }}
                />
              </div>
              <span className="sentiment-card-desc">
                Based on {s.sentiment_confidence && s.sentiment_confidence > 0.7
                  ? 'many consistent reviews'
                  : s.sentiment_confidence && s.sentiment_confidence > 0.4
                    ? 'a moderate number of reviews'
                    : 'limited review data'}
              </span>
            </div>
          </div>
        </div>
      )}

      {aspects.length > 0 && (
        <div className="aspect-chart">
          <h4>Aspect sentiment (most talked-about)</h4>
          {aspects.map((row) => {
            const width = Math.round(((row.avg_sentiment + 1) / 2) * 100);
            const color = sentimentColor(row.avg_sentiment);
            const pct = Math.round(row.avg_sentiment * 100);

            // Human-friendly descriptions with styled badges
            let emoji: string;
            let description: string;
            let badgeClass: string;
            if (pct >= 50) {
              emoji = "👍";
              description = "Highly praised";
              badgeClass = "badge-excellent";
            } else if (pct >= 10) {
              emoji = "👍";
              description = "Generally liked";
              badgeClass = "badge-good";
            } else if (pct >= -10) {
              emoji = "🤔";
              description = "Mixed reviews";
              badgeClass = "badge-neutral";
            } else if (pct >= -50) {
              emoji = "⚠️";
              description = "Some concerns";
              badgeClass = "badge-warning";
            } else {
              emoji = "⛔";
              description = "Often criticized";
              badgeClass = "badge-critical";
            }

            return (
              <div key={row.aspect} className="aspect-row">
                <div className="aspect-label">
                  <strong>{row.aspect}</strong>
                </div>
                <div className="aspect-bar-bg">
                  <div
                    className="aspect-bar"
                    style={{ width: `${width}%`, backgroundColor: color }}
                  />
                </div>
                <div className="aspect-indicator">
                  <span className={`sentiment-badge ${badgeClass}`}>
                    <span className="badge-emoji">{emoji}</span>
                    <span className="badge-text">{description}</span>
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
};

export default SentimentSection;

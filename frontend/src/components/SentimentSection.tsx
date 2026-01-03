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
        <div className="sentiment-summary">
          <p>
            <strong>Overall:</strong> {s.overall_sentiment}
          </p>
          <p>
            <strong>Compound score:</strong> {(typeof s.compound_score === 'number' ? s.compound_score.toFixed(2) : 'N/A')}
          </p>
          <p>
            <strong>Confidence:</strong> {(typeof s.sentiment_confidence === 'number' ? (s.sentiment_confidence * 100).toFixed(0) + '%' : 'N/A')}
          </p>
          <p>
            <strong>Tone:</strong> {s.emotional_tone}
          </p>
        </div>
      )}

      {aspects.length > 0 && (
        <div className="aspect-chart">
          <h4>Aspect sentiment (most talked-about)</h4>
          {aspects.map((row) => {
            const width = Math.round(((row.avg_sentiment + 1) / 2) * 100);
            const color = sentimentColor(row.avg_sentiment);
            const pct = Math.round(row.avg_sentiment * 100);

            // Human-friendly descriptions
            let description: string;
            let cssClass: string;
            if (pct >= 50) {
              description = "👍 Highly praised by users";
              cssClass = "positive";
            } else if (pct >= 10) {
              description = "👍 Generally liked";
              cssClass = "positive";
            } else if (pct >= -10) {
              description = "🤔 Mixed opinions";
              cssClass = "neutral";
            } else if (pct >= -50) {
              description = "⚠️ Some concerns raised";
              cssClass = "negative";
            } else {
              description = "⛔ Frequently criticized";
              cssClass = "negative";
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
                <div className={`aspect-score ${cssClass}`}>
                  {description}
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

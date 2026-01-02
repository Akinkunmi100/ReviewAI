import React, { useState } from "react";
import { apiCompare } from "../api/client";
import type { ProductComparison } from "../api/types";
import { Scale, Plus, AlertCircle, ThumbsUp, ThumbsDown, Sparkles, ArrowRight } from "lucide-react";

interface Props {
  shortlist: { name: string }[];
}

const ComparisonView: React.FC<Props> = ({ shortlist }) => {
  const [namesInput, setNamesInput] = useState("");
  const [comparison, setComparison] = useState<ProductComparison | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleCompare(source: "shortlist" | "manual") {
    const names: string[] =
      source === "shortlist"
        ? shortlist.map((s) => s.name).slice(0, 3)
        : namesInput
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean)
          .slice(0, 3);

    if (names.length < 2) {
      setError("Need at least 2 products to compare");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const data = await apiCompare(names);
      setComparison(data);
    } catch (e: any) {
      setError(e.message ?? "Comparison failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="comparison-section">
      <div className="comparison-header">
        <div className="comparison-icon">
          <Scale size={24} />
        </div>
        <div>
          <h3>Compare Products</h3>
          <p>Compare up to 3 products side by side</p>
        </div>
      </div>

      <div className="compare-inputs">
        <div className="compare-input-group">
          <label className="compare-input-label">
            <Plus size={16} />
            Enter product names to compare
          </label>
          <div className="compare-input-row">
            <input
              type="text"
              value={namesInput}
              onChange={(e) => setNamesInput(e.target.value)}
              placeholder="e.g., iPhone 15, Samsung Galaxy S24, Google Pixel 8"
              className="compare-input"
            />
            <button
              onClick={() => handleCompare("manual")}
              className="compare-btn"
              disabled={loading}
            >
              Compare <ArrowRight size={16} />
            </button>
          </div>
        </div>

        {shortlist.length >= 2 && (
          <div className="compare-shortlist">
            <span className="shortlist-info">
              Or compare from your shortlist ({shortlist.length} items)
            </span>
            <button
              onClick={() => handleCompare("shortlist")}
              disabled={shortlist.length < 2 || loading}
              className="compare-btn-secondary"
            >
              Compare Shortlisted
            </button>
          </div>
        )}
      </div>

      {loading && (
        <div className="compare-loading">
          <div className="loading-spinner"></div>
          <span>Analyzing products...</span>
        </div>
      )}

      {error && (
        <div className="compare-error">
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {comparison && (
        <div className="comparison-results">
          {/* Winner Summary Banner */}
          {comparison.overall_winner && (
            <div className="winner-banner">
              <span className="winner-crown">🏆</span>
              <span className="winner-text">
                <strong>{comparison.overall_winner}</strong> is the overall winner
              </span>
            </div>
          )}

          {/* Category Winners as Tags */}
          {comparison.winner_by_category && Object.keys(comparison.winner_by_category).length > 0 && (
            <div className="category-winners">
              <span className="category-label">Winners by category:</span>
              <div className="category-tags">
                {Object.entries(comparison.winner_by_category).map(([cat, winner]) => (
                  <span key={cat} className="category-tag">
                    <span className="cat-name">{cat}</span>
                    <span className="cat-winner">{winner as string}</span>
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Quick Awards */}
          <div className="quick-awards">
            {comparison.best_value && (
              <span className="award-badge value">💎 Best Value: {comparison.best_value}</span>
            )}
            {comparison.best_budget && (
              <span className="award-badge budget">💰 Budget Pick: {comparison.best_budget}</span>
            )}
            {comparison.best_premium && (
              <span className="award-badge premium">✨ Premium Choice: {comparison.best_premium}</span>
            )}
          </div>

          <div className="comparison-grid">
            {Array.isArray(comparison.products) ? comparison.products.map((p) => {
              const isWinner = p.product_name === comparison.overall_winner;
              const valueScore = p.value_score ?? 0;
              const scoreClass = valueScore >= 7 ? 'high' : valueScore >= 5 ? 'medium' : 'low';

              return (
                <div key={p.product_name} className={`product-compare-card ${isWinner ? 'winner' : ''}`}>
                  {isWinner && <div className="winner-ribbon">👑 Winner</div>}

                  <div className="product-compare-header">
                    <h4>{p.product_name}</h4>
                    {p.rating && (
                      <span className="product-rating">⭐ {p.rating}</span>
                    )}
                  </div>

                  <div className="product-compare-stats">
                    <div className="stat-item">
                      <span className="stat-label">Price</span>
                      <span className="stat-value price">
                        {typeof p.price_naira === 'number' && Number.isFinite(p.price_naira) ? `₦${p.price_naira.toLocaleString()}` : "N/A"}
                      </span>
                    </div>
                    {p.value_score !== undefined && (
                      <div className="stat-item">
                        <span className="stat-label">Value Score</span>
                        <span className={`stat-value score ${scoreClass}`}>{p.value_score.toFixed(1)}/10</span>
                      </div>
                    )}
                  </div>

                  <div className="product-pros-cons">
                    <div className="pros-section">
                      <div className="section-title">
                        <ThumbsUp size={14} />
                        <span>Pros</span>
                      </div>
                      <ul>
                        {p.pros.slice(0, 3).map((pro, idx) => (
                          <li key={idx}>{pro}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="cons-section">
                      <div className="section-title">
                        <ThumbsDown size={14} />
                        <span>Cons</span>
                      </div>
                      <ul>
                        {p.cons.slice(0, 3).map((con, idx) => (
                          <li key={idx}>{con}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              );
            }) : null}
          </div>

          {comparison.ai_recommendation && (
            <div className="ai-recommendation">
              <div className="recommendation-header">
                <Sparkles size={20} />
                <span>AI Recommendation</span>
              </div>
              <p>{comparison.ai_recommendation}</p>
            </div>
          )}
        </div>
      )}
    </section>
  );
};

export default ComparisonView;

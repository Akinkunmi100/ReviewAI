import React from "react";
import { ThumbsUp, ThumbsDown, CheckCircle, AlertCircle } from "lucide-react";
import type { EnhancedProductReview } from "../api/types";

interface Props {
  review: EnhancedProductReview;
}

const ProsConsSection: React.FC<Props> = ({ review }) => {
  const pros = Array.isArray(review.pros) ? review.pros : [];
  const cons = Array.isArray(review.cons) ? review.cons : [];

  return (
    <section className="pros-cons-section">
      <div className="pros-cons-grid">
        {/* Top Strengths */}
        <div className="pros-card">
          <div className="pros-header">
            <div className="pros-icon">
              <ThumbsUp size={24} />
            </div>
            <h3>Top Strengths</h3>
          </div>
          <ul className="pros-list">
            {pros.slice(0, 8).map((pro, idx) => (
              <li key={idx} className="pro-item">
                <CheckCircle size={16} className="item-icon success" />
                <span>{pro}</span>
              </li>
            ))}
          </ul>
          {pros.length > 8 && (
            <p className="more-items">+{pros.length - 8} more strengths</p>
          )}
        </div>

        {/* Main Weaknesses */}
        <div className="cons-card">
          <div className="cons-header">
            <div className="cons-icon">
              <ThumbsDown size={24} />
            </div>
            <h3>Main Weaknesses</h3>
          </div>
          <ul className="cons-list">
            {cons.slice(0, 8).map((con, idx) => (
              <li key={idx} className="con-item">
                <AlertCircle size={16} className="item-icon warning" />
                <span>{con}</span>
              </li>
            ))}
          </ul>
          {cons.length > 8 && (
            <p className="more-items">+{cons.length - 8} more weaknesses</p>
          )}
        </div>
      </div>
    </section>
  );
};

export default ProsConsSection;

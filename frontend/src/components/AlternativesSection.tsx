import React from "react";
import type { EnhancedProductReview } from "../api/types";
import { Layers, ExternalLink, ArrowRight, Package } from "lucide-react";

interface Props {
  review: EnhancedProductReview;
}

const AlternativesSection: React.FC<Props> = ({ review }) => {
  const alts = review.alternatives ?? [];
  if (alts.length === 0) return null;

  return (
    <section className="section alternatives-section">
      <div className="alternatives-header">
        <Layers className="section-icon" size={20} />
        <h3>Alternatives to Consider</h3>
        <span className="alternatives-count">{alts.length} options</span>
      </div>

      <div className="alternatives-grid">
        {alts.map((alt, index) => (
          <div key={alt.product_name} className="alternative-card">
            <div className="alt-number">{index + 1}</div>
            <div className="alt-icon">
              <Package size={24} />
            </div>
            <div className="alt-content">
              <h4 className="alt-name">{alt.product_name}</h4>
              {alt.snippet && (
                <p className="alt-snippet">{alt.snippet}</p>
              )}
            </div>
            <a
              href={alt.url}
              target="_blank"
              rel="noreferrer"
              className="alt-link"
            >
              <span>View Details</span>
              <ExternalLink size={14} />
            </a>
          </div>
        ))}
      </div>
    </section>
  );
};

export default AlternativesSection;

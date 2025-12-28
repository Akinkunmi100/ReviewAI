import React from "react";
import type { EnhancedProductReview } from "../api/types";
import { FileText, ExternalLink, Globe, Link2 } from "lucide-react";

// Extract domain from URL
const getDomain = (url: string): string => {
  try {
    const domain = new URL(url).hostname.replace("www.", "");
    return domain;
  } catch {
    return url;
  }
};

// Get favicon URL
const getFaviconUrl = (url: string): string => {
  try {
    const domain = new URL(url).hostname;
    return `https://www.google.com/s2/favicons?domain=${domain}&sz=32`;
  } catch {
    return "";
  }
};

import { safeArray } from "../utils/safeHelpers";

const SourcesSection: React.FC<{ review: EnhancedProductReview }> = ({ review }) => {
  const sources = safeArray(review?.sources);
  if (sources.length === 0) return null;

  return (
    <section className="section sources-section">
      <div className="sources-header">
        <FileText className="section-icon" size={20} />
        <h3>Research Sources</h3>
        <span className="sources-count">{review.sources.length} sources</span>
      </div>

      <div className="sources-list">
        {sources.map((src, idx) => {
          const domain = getDomain(src);
          const faviconUrl = getFaviconUrl(src);

          return (
            <a
              key={idx}
              href={src}
              target="_blank"
              rel="noreferrer"
              className="source-item"
            >
              <div className="source-icon">
                {faviconUrl ? (
                  <img
                    src={faviconUrl}
                    alt=""
                    onError={(e) => {
                      e.currentTarget.style.display = 'none';
                      e.currentTarget.nextElementSibling?.classList.remove('hidden');
                    }}
                  />
                ) : null}
                <Globe size={16} className={faviconUrl ? "hidden" : ""} />
              </div>
              <div className="source-content">
                <span className="source-domain">{domain}</span>
                <span className="source-url">{src}</span>
              </div>
              <ExternalLink size={14} className="source-external" />
            </a>
          );
        })}
      </div>

      <div className="sources-footer">
        <Link2 size={12} />
        <span>All sources verified and retrieved in real-time</span>
      </div>
    </section>
  );
};

export default SourcesSection;

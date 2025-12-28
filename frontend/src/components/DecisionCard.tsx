import React from "react";
import { formatNaira } from "../utils/safeHelpers";
import { Star, Tag, Heart, Check } from "lucide-react";
import type { EnhancedProductReview } from "../api/types";

interface Props {
  review: EnhancedProductReview;
  onShortlistAdd: (entry: { name: string; rating?: string; price?: string | number }) => void | Promise<void>;
  isShortlisted: boolean;
}

const DecisionCard: React.FC<Props> = ({ review, onShortlistAdd, isShortlisted }) => {
  const handleShortlist = () => {
    if (isShortlisted) return;

    const entry = {
      name: review.product_name,
      rating: review.predicted_rating,
      price: review.price_naira ?? review.price_info,
    };
    onShortlistAdd(entry);
  };

  // Render rating stars
  const renderStars = (rating: string) => {
    const numRating = parseFloat(rating) || 0;
    const fullStars = Math.floor(numRating);
    const hasHalfStar = numRating % 1 >= 0.5;

    return (
      <div style={{ display: 'flex', gap: '4px', alignItems: 'center' }}>
        {[...Array(5)].map((_, i) => (
          <Star
            key={i}
            size={20}
            className={i < fullStars || (i === fullStars && hasHalfStar) ? 'star-filled' : 'star-empty'}
            strokeWidth={2}
          />
        ))}
        <span className="rating-number">
          {rating}
        </span>
      </div>
    );
  };

  return (
    <section className="decision-card">
      <div className="decision-main">
        <div className="decision-meta">
          <div className="decision-title-row">
            <h2>{review.product_name}</h2>
            {isShortlisted && (
              <span className="shortlist-indicator" title="This product is in your shortlist">
                <Check size={14} /> In shortlist
              </span>
            )}
          </div>
          <div className="rating-row">
            {renderStars(review.predicted_rating)}
          </div>
          <p className="price-row">
            <Tag size={20} className="price-icon" />
            <span className="price-text">
              {typeof review.price_naira === 'number'
                ? formatNaira(review.price_naira)
                : review.price_info || 'Price unavailable'}
            </span>
          </p>
          <button
            onClick={handleShortlist}
            className={`shortlist-btn ${isShortlisted ? 'active' : ''}`}
            disabled={isShortlisted}
            aria-disabled={isShortlisted}
          >
            {isShortlisted ? <Check size={18} /> : <Heart size={18} />}
            {isShortlisted ? "In Shortlist" : "Add to Shortlist"}
          </button>
        </div>
        {review.primary_image_url && (
          <img
            src={review.primary_image_url}
            alt={review.product_name}
            className="decision-image"
          />
        )}
      </div>
    </section>
  );
};

export default DecisionCard;

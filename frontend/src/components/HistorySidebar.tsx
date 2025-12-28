import React from "react";
import { Clock, Star, Heart, Package } from "lucide-react";

export interface HistoryEntry {
  name: string;
  rating?: string;
  price?: string | number;
  timestamp?: string;
}

interface Props {
  history: HistoryEntry[];
  shortlist: HistoryEntry[];
  onSelectHistory?: (entry: HistoryEntry) => void;
  onRemoveShortlist?: (entry: HistoryEntry) => void;
}

const HistorySidebar: React.FC<Props> = ({
  history,
  shortlist,
  onSelectHistory,
  onRemoveShortlist,
}) => {
  const hist = Array.isArray(history) ? history : [];
  const list = Array.isArray(shortlist) ? shortlist : [];

  return (
    <div className="history-sidebar">
      {/* Recent Section */}
      <div className="sidebar-section">
        <div className="sidebar-section-header">
          <Clock size={18} />
          <h3>Recent Searches</h3>
        </div>
        {hist.length === 0 ? (
          <div className="sidebar-empty">
            <Package size={24} />
            <span>No recent searches</span>
          </div>
        ) : (
          <div className="sidebar-items">
            {hist
              .slice(-10)
              .reverse()
              .map((item, idx) => (
                <div
                  key={idx}
                  className="sidebar-item"
                  onClick={() => onSelectHistory?.(item)}
                  style={{ cursor: onSelectHistory ? "pointer" : "default" }}
                >
                  <div className="item-content">
                    <strong className="item-name">{item.name}</strong>
                    <div className="item-meta">
                      {item.rating && (
                        <span className="item-rating">
                          <Star size={12} />
                          {item.rating}
                        </span>
                      )}
                      {item.price && (
                        <span className="item-price">₦{item.price}</span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
          </div>
        )}
      </div>

      {/* Shortlist Section */}
      <div className="sidebar-section shortlist-section">
        <div className="sidebar-section-header">
          <Heart size={18} />
          <h3>Shortlist</h3>
          {list.length > 0 && (
            <span className="section-count">{list.length}</span>
          )}
        </div>
        {list.length === 0 ? (
          <div className="sidebar-empty">
            <Heart size={24} />
            <span>No saved items</span>
          </div>
        ) : (
          <div className="sidebar-items">
            {list.map((item, idx) => (
              <div key={idx} className="sidebar-item shortlist-item">
                <div className="item-content">
                  <strong className="item-name">{item.name}</strong>
                  <div className="item-meta">
                    {item.rating && (
                      <span className="item-rating">
                        <Star size={12} />
                        {item.rating}
                      </span>
                    )}
                    {item.price && (
                      <span className="item-price">₦{item.price}</span>
                    )}
                  </div>
                </div>
                {onRemoveShortlist && (
                  <button
                    className="shortlist-remove"
                    onClick={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                      onRemoveShortlist(item);
                    }}
                    type="button"
                  >
                    Remove
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default HistorySidebar;

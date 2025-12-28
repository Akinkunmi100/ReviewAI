import React from "react";
import { Shield, AlertTriangle, AlertCircle, CheckCircle, Info } from "lucide-react";
import type { EnhancedProductReview } from "../api/types";
import { safeArray, safeNum, safeString } from "../utils/safeHelpers";

interface Props {
  review: EnhancedProductReview;
}

const RiskSection: React.FC<Props> = ({ review }) => {
  const r = review?.red_flag_report;
  if (!r) return null;

  const getRiskColor = (level: string) => {
    switch (level.toLowerCase()) {
      case "high": return "#ef4444";
      case "medium": return "#f59e0b";
      case "low": return "#10b981";
      default: return "#6b7280";
    }
  };

  const getRiskIcon = (level: string) => {
    switch (level.toLowerCase()) {
      case "high": return <AlertTriangle size={20} />;
      case "medium": return <AlertCircle size={20} />;
      case "low": return <CheckCircle size={20} />;
      default: return <Info size={20} />;
    }
  };

  const getSeverityBadge = (severity: string) => {
    const colors: Record<string, string> = {
      high: "#ef4444",
      medium: "#f59e0b",
      low: "#10b981"
    };
    return colors[severity.toLowerCase()] || "#6b7280";
  };

  const riskPercent = Math.min(100, (safeNum(r.risk_score) ?? 0) / 10 * 100);

  return (
    <section className="risk-section">
      <div className="risk-header">
        <div className="risk-icon" style={{ background: `${getRiskColor(r.overall_risk_level)}20`, color: getRiskColor(r.overall_risk_level) }}>
          <Shield size={24} />
        </div>
        <div>
          <h3>Risk & Red Flags</h3>
          <p className="risk-subtitle">Safety and reliability assessment</p>
        </div>
      </div>

      <div className="risk-overview">
        <div className="risk-meter">
          <div className="risk-meter-header">
            <span>Overall Risk Level</span>
            <span className="risk-badge" style={{ background: `${getRiskColor(safeString(r.overall_risk_level))}20`, color: getRiskColor(safeString(r.overall_risk_level)) }}>
              {getRiskIcon(safeString(r.overall_risk_level))}
              {safeString(r.overall_risk_level).toUpperCase()}
            </span>
          </div>
          <div className="risk-bar-container">
            <div
              className="risk-bar"
              style={{
                width: `${riskPercent}%`,
                background: getRiskColor(r.overall_risk_level)
              }}
            />
          </div>
          <div className="risk-score">
            <span>{safeNum(r.risk_score) !== null ? (r.risk_score).toFixed(1) : 'N/A'}</span>
            <span className="risk-max">/ 10</span>
          </div>
        </div>

        {r.fake_review_score !== undefined && (
          <div className="fake-review-indicator">
            <AlertCircle size={16} />
            <span>Fake review risk: </span>
            <strong style={{ color: r.fake_review_score > 0.5 ? "#ef4444" : r.fake_review_score > 0.3 ? "#f59e0b" : "#10b981" }}>
              {(r.fake_review_score * 100).toFixed(0)}%
            </strong>
          </div>
        )}
      </div>

        {safeArray(r.red_flags).length > 0 && (
        <div className="red-flags-list">
          <h4>Identified Issues</h4>
          {safeArray(r.red_flags).map((flag, idx) => (
            <div key={idx} className="red-flag-item" style={{ borderLeftColor: getSeverityBadge(flag.severity) }}>
              <div className="red-flag-header">
                <span className="severity-badge" style={{ background: `${getSeverityBadge(flag.severity)}20`, color: getSeverityBadge(flag.severity) }}>
                  {flag.severity.toUpperCase()}
                </span>
                <strong>{flag.title}</strong>
              </div>
              <p>{flag.description}</p>
              {flag.affected_percentage && (
                <span className="affected-users">{flag.affected_percentage}% of users affected</span>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="risk-recommendation">
        <CheckCircle size={18} style={{ color: "#10b981" }} />
        <span>{r.recommendation}</span>
      </div>
    </section>
  );
};

export default RiskSection;

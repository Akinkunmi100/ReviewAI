import React from "react";
import { TrendingDown, TrendingUp, DollarSign, BarChart3, Clock, AlertCircle } from "lucide-react";
import type { EnhancedProductReview } from "../api/types";

interface Props {
    review: EnhancedProductReview;
}

const ResalePanel: React.FC<Props> = ({ review }) => {
    const analysis = review?.resale_analysis;
    if (!analysis) return null;

    const getDepreciationClass = (rate: string) => {
        const r = rate.toLowerCase();
        if (r.includes("slow") || r.includes("stable") || r.includes("good")) return "depreciation-good";
        if (r.includes("fast") || r.includes("high")) return "depreciation-bad";
        return "depreciation-medium";
    };

    const depRate = (analysis.depreciation_rate ?? "").toString();
    const depClass = getDepreciationClass(depRate);
    const RateIcon = depRate.toLowerCase().includes("slow") || depRate.toLowerCase().includes("stable") ? TrendingUp
        : depRate.toLowerCase().includes("fast") || depRate.toLowerCase().includes("high") ? TrendingDown
            : BarChart3;

    return (
        <section className="resale-section section-card">
            <div className="section-header">
                <div className="section-icon resale-icon">
                    <DollarSign size={24} />
                </div>
                <div>
                    <h3>Resale Value Forecaster</h3>
                    <p className="section-subtitle">Investment potential and depreciation analysis</p>
                </div>
            </div>

            <div className="resale-grid">
                {/* Investment Score */}
                <div className="resale-card score-card">
                    <div className={`big-score ${(analysis.investment_score ?? 0) >= 8 ? 'score-good' : (analysis.investment_score ?? 0) >= 5 ? 'score-medium' : 'score-poor'}`}>
                        {(Number.isFinite(analysis.investment_score) ? analysis.investment_score : 'N/A')}/10
                    </div>
                    <div className="card-label">Investment Score</div>
                </div>

                {/* Verdict */}
                <div className="resale-card">
                    <div className="verdict-stats">
                        <div className={`verdict-badge ${depClass}`}>
                            <RateIcon size={16} />
                            <span>{depRate || 'Unknown'}</span>
                        </div>
                        <div className="verdict-text">{analysis.verdict ?? 'No verdict'}</div>
                    </div>
                </div>
            </div>

            {/* Forecast Line */}
            <div className="forecast-container">
                <h4 className="subsection-title">
                    <Clock size={18} />
                    Value Projection
                </h4>

                <div className="timeline-values">
                    {/* Connecting line */}
                    <div className="timeline-line"></div>

                    <div className="timeline-item">
                        <div className="timeline-dot"></div>
                        <div className="timeline-content">
                            <span className="timeline-label">Today</span>
                            <span className="timeline-value">100% (New)</span>
                        </div>
                    </div>

                    <div className="timeline-item">
                        <div className="timeline-dot"></div>
                        <div className="timeline-content">
                            <span className="timeline-label">1 Year</span>
                            <span className="timeline-value highlight">{analysis.predicted_value_1yr ?? 'N/A'}</span>
                        </div>
                    </div>

                    <div className="timeline-item">
                        <div className="timeline-dot"></div>
                        <div className="timeline-content">
                            <span className="timeline-label">3 Years</span>
                            <span className="timeline-value">{analysis.predicted_value_3yr ?? 'N/A'}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="disclaimer">
                <AlertCircle size={14} />
                <p>Projections based on historical brand performance in the Nigerian market. Actual resale value depends on condition and market demand.</p>
            </div>
        </section>
    );
};

export default ResalePanel;

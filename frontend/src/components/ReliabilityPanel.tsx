import React from "react";
import { Wrench, Clock, ShieldCheck, AlertTriangle, Hammer, CheckCircle, Info } from "lucide-react";
import type { EnhancedProductReview } from "../api/types";

interface Props {
    review: EnhancedProductReview;
}

const ReliabilityPanel: React.FC<Props> = ({ review }) => {
    const report = review?.reliability_report;

    // If no reliability report is available, don't render this panel
    if (!report) return null;

    const getAvailabilityClass = (avail?: string) => {
        const lower = (avail ?? "").toLowerCase();
        if (lower.includes("common") || lower.includes("easy")) return "badge-success";
        if (lower.includes("scarce") || lower.includes("difficult")) return "badge-danger";
        return "badge-warning";
    };

    return (
        <section className="reliability-section section-card">
            <div className="section-header">
                <div className="section-icon reliability-icon">
                    <Wrench size={24} />
                </div>
                <div>
                    <h3>Reliability & Repair Engine</h3>
                    <p className="section-subtitle">Durability analysis and local repair estimates</p>
                </div>
            </div>

            <div className="reliability-grid">
                {/* Reliability Score */}
                <div className="reliability-card score-card">
                    <div className={`big-score ${(report.overall_reliability_score ?? 0) >= 80 ? 'score-good' : (report.overall_reliability_score ?? 0) >= 60 ? 'score-medium' : 'score-poor'}`}>
                        {(Number.isFinite(report.overall_reliability_score) ? report.overall_reliability_score : 'N/A')}/100
                    </div>
                    <div className="card-label">Reliability Score</div>
                </div>

                {/* Predicted Lifespan */}
                <div className="reliability-card">
                    <Clock className="card-icon" size={24} color="#60a5fa" />
                    <div className="card-value">{report.predicted_lifespan ?? 'Unknown'}</div>
                    <div className="card-label">Predicted Lifespan</div>
                </div>

                {/* Warranty Difficulty */}
                <div className="reliability-card">
                    <ShieldCheck className="card-icon" size={24} color="#a78bfa" />
                    <div className="card-value">{report.warranty_difficulty ?? 'Unknown'}</div>
                    <div className="card-label">Warranty in Nigeria</div>
                </div>
            </div>

            {/* Common Risks */}
            {report.common_risks && report.common_risks.length > 0 && (
                <div className="risks-container">
                    <h4 className="subsection-title">
                        <AlertTriangle size={18} className="text-warning" />
                        Common Fault Lines
                    </h4>
                    <div className="risks-list">
                        {report.common_risks.map((risk, idx) => (
                            <div key={idx} className="risk-item">
                                <div className="risk-header">
                                    <span className="risk-type">{risk.risk_type}</span>
                                    <span className={`risk-badge badge-${(risk.likelihood ?? '').toLowerCase()}`}>{risk.likelihood ?? 'Unknown'} Likelihood</span>
                                </div>
                                <p className="risk-desc">{risk.description}</p>
                                <div className="risk-tip">
                                    <CheckCircle size={14} />
                                    <span>Tip: {risk.prevention_tip ?? ''}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Repair Costs Table */}
            {report.repair_costs && report.repair_costs.length > 0 && (
                <div className="costs-container">
                    <h4 className="subsection-title">
                        <Hammer size={18} className="text-muted" />
                        Repair Cost Estimates (Nigeria)
                    </h4>
                    <div className="table-responsive">
                        <table className="repair-table">
                            <thead>
                                <tr>
                                    <th>Part / Repair</th>
                                    <th>Est. Cost (₦)</th>
                                    <th>Availability</th>
                                </tr>
                            </thead>
                            <tbody>
                                {report.repair_costs.map((cost, idx) => (
                                    <tr key={idx}>
                                        <td>{cost.part_name}</td>
                                        <td className="cost-value">{cost.estimated_cost_naira}</td>
                                        <td>
                                            <span className={`status-badge ${getAvailabilityClass(cost.availability_in_nigeria)}`}>
                                                {cost.availability_in_nigeria}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    <p className="disclaimer">
                        * Estimates based on typical market rates. Actual repair costs may vary by technician and location.
                    </p>
                </div>
            )}
        </section>
    );
};

export default ReliabilityPanel;

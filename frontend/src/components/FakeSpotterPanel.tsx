import React, { useState } from "react";
import { ShieldAlert, CheckSquare, AlertTriangle, Fingerprint } from "lucide-react";
import type { EnhancedProductReview } from "../api/types";

interface Props {
    review: EnhancedProductReview;
}

const FakeSpotterPanel: React.FC<Props> = ({ review }) => {
    const report = review?.fake_spotter_report;
    // If report is missing or empty, don't render
    if (!report || !Array.isArray(report.verification_steps) || report.verification_steps.length === 0) return null;

    const [checkedItems, setCheckedItems] = useState<Record<number, boolean>>({});

    const toggleCheck = (idx: number) => {
        setCheckedItems(prev => ({ ...prev, [idx]: !prev[idx] }));
    };

    // Normalize risk level to lowercase for CSS class
    const riskLevel = (report.risk_level ?? "unknown").toLowerCase();

    return (
        <section className={`fake-spotter-section section-card risk-${riskLevel}`} data-risk-level={riskLevel}>
            <div className="section-header">
                <div className={`section-icon fake-icon risk-icon-${riskLevel}`}>
                    <Fingerprint size={24} />
                </div>
                <div>
                    <h3>Fake Spotter</h3>
                    <p className="section-subtitle">
                        Counterfeit Risk: <strong className={`risk-text-${riskLevel}`}>{report.risk_level}</strong>
                    </p>
                </div>
            </div>

            {(Array.isArray(report.common_scams) && report.common_scams.length > 0) && (
                <div className="scam-alert-box">
                    <div className="scam-header">
                        <ShieldAlert size={18} />
                        <span>Common Scams for this Product</span>
                    </div>
                    <ul className="scam-list">
                        {(report.common_scams ?? []).map((scam, i) => (
                            <li key={i}>{scam}</li>
                        ))}
                    </ul>
                </div>
            )}

            <div className="verification-checklist">
                <h4 className="subsection-title">
                    <CheckSquare size={18} />
                    <span>Interactive Inspection Checklist</span>
                </h4>

                <div className="checklist-grid">
                    {report.verification_steps.map((step, idx) => (
                        <div
                            key={idx}
                            className={`check-item ${checkedItems[idx] ? 'checked' : ''}`}
                            onClick={() => toggleCheck(idx)}
                        >
                            <div className="check-item-content">
                                <div className="checkbox-custom">
                                    {checkedItems[idx] && <CheckSquare size={14} />}
                                </div>

                                <div className="check-content flex-1">
                                    <div className="check-header">
                                        <span className="badge-type">
                                            {step.check_type}
                                        </span>
                                    </div>

                                    <p className="check-instruction">{step.instruction}</p>

                                    <div className="check-details-grid">
                                        <div className="detail-box detail-expected">
                                            <span className="detail-label">Expected:</span>
                                            {step.expected_result}
                                        </div>
                                        <div className="detail-box detail-warning">
                                            <span className="detail-label">Warning Sign:</span>
                                            <div className="warning-content">
                                                <AlertTriangle size={12} />
                                                {step.warning_sign}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default FakeSpotterPanel;

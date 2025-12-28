import React from "react";
import { Skull, Activity } from "lucide-react";
import type { EnhancedProductReview } from "../api/types";
import { safeArray, safeNum } from "../utils/safeHelpers";

interface Props {
    review: EnhancedProductReview;
}

const WhatIfPanel: React.FC<Props> = ({ review }) => {
    const report = review?.what_if_report;
    const scenarios = safeArray(report?.scenarios);
    if (!report || scenarios.length === 0) return null;

    return (
        <section className="what-if-section section-card">
            <div className="section-header">
                <div className="section-icon what-if-icon">
                    <Skull size={24} />
                </div>
                <div>
                    <h3>"What-If" Disaster Simulator</h3>
                    <p className="section-subtitle">Stressing testing against Nigerian realities</p>
                </div>
            </div>

            <div className="what-if-score-container">
                <div className="score-ring">
                    <span className={`score-value ${report.disaster_score >= 7 ? "text-success" : report.disaster_score >= 4 ? "text-warning" : "text-danger"}`}>
                        {report.disaster_score}/10
                    </span>
                    <span className="score-label">Survival Score</span>
                </div>
                <p className="score-desc">
                    {report.disaster_score >= 8 ? "Built like a Tank." :
                        report.disaster_score >= 5 ? "Handles daily abuse, but not disasters." :
                            "Treat like an egg."}
                </p>
            </div>

            <div className="scenarios-grid">
                {report.scenarios.map((scene, idx) => (
                    <div key={idx} className="scenario-card">
                        <h4 className="scenario-header">
                            <Activity size={16} />
                            {scene?.name ?? 'Scenario'}
                        </h4>
                        <p className="scenario-desc">{scene?.scenario ?? ''}</p>

                        <div className={`outcome-badge ${safeNum(scene.survivability_score) !== null && scene.survivability_score >= 7 ? "good" : safeNum(scene.survivability_score) !== null && scene.survivability_score <= 3 ? "critical" : "bad"}`}>
                            {scene?.outcome ?? ''}
                        </div>

                        {scene.repair_cost_estimate !== "N/A" && (
                            <div className="repair-estimate">
                                <span>Est. Repair:</span>
                                <strong>{scene.repair_cost_estimate}</strong>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </section>
    );
};

export default WhatIfPanel;

import React from "react";
import { ArrowLeftRight, TrendingUp, AlertCircle, CheckCircle, ExternalLink } from "lucide-react";
import type { EnhancedProductReview } from "../api/types";

interface Props {
    review: EnhancedProductReview;
}

const SmartSwapPanel: React.FC<Props> = ({ review }) => {

    const report = review?.smart_swap_report;
    if (!report || !Array.isArray(report.swaps) || report.swaps.length === 0) return null;

    // Don't show if the recommendation is "Keep Original" and no strong swaps found
    if ((report.recommendation ?? "") === "Keep Original" && report.swaps.length === 0) return null;

    return (
        <section className="smart-swap-section section-card">
            <div className="section-header">
                <div className="section-icon swap-icon">
                    <ArrowLeftRight size={24} />
                </div>
                <div>
                    <h3>The "Smart Swap" Engine</h3>
                    <p className="section-subtitle">
                        Buying New? Consider these <strong>Used Flagships</strong> for the same price.
                    </p>
                </div>
            </div>

            <div className="swap-recommendation">
                <strong>Advice:</strong>
                {
                    (() => {
                        const rec = report.recommendation ?? "No recommendation";
                        const isSwap = (rec ?? "").includes("Swap");
                        return <span className={isSwap ? "text-green-400" : "text-gray-300"}>{rec}</span>;
                    })()
                }
            </div>

            <div className="swaps-grid">
                {report.swaps.map((swap, idx) => {
                    const name = swap?.product_name ?? "Unknown product";
                    const condition = swap?.condition ?? "Used";
                    const price = Number.isFinite(swap?.price) ? swap!.price : null;
                    const priceStr = price !== null ? `~₦${price.toLocaleString()}` : "Price N/A";
                    const perf = swap?.performance_diff ?? "—";
                    const reasonBuy = swap?.reason_to_buy ?? "";
                    const reasonAvoid = swap?.reason_to_avoid ?? "";

                    return (
                        <div key={idx} className="swap-card">
                            <div className="swap-header">
                                <h4>{name}</h4>
                                <span className="condition-badge">{condition}</span>
                            </div>

                            <div className="price-tag">
                                {priceStr}
                                <a
                                    href={`https://www.google.com/search?q=${encodeURIComponent(name + " " + condition + " price Nigeria")}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="verify-price-link"
                                    title="Check current market price"
                                >
                                    <ExternalLink size={14} />
                                </a>
                            </div>

                            <div className="performance-boost">
                                <TrendingUp size={16} />
                                <span>{perf}</span>
                            </div>

                            <div className="swap-details">
                                <div className="detail-row good">
                                    <CheckCircle size={14} />
                                    <span>{reasonBuy}</span>
                                </div>
                                <div className="detail-row bad">
                                    <AlertCircle size={14} />
                                    <span>{reasonAvoid}</span>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </section>
    );
};

export default SmartSwapPanel;

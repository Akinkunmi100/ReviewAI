import React from "react";
import { Banknote } from "lucide-react";
import type { EnhancedProductReview } from "../api/types";

interface Props {
    review: EnhancedProductReview;
}

const NetPricePanel: React.FC<Props> = ({ review }) => {
    const report = review?.net_price_report;
    if (!report || !Array.isArray(report.upgrade_from) || report.upgrade_from.length === 0) return null;

    return (
        <section className="net-price-section section-card">
            <div className="section-header">
                <div className="section-icon net-price-icon">
                    <Banknote size={24} />
                </div>
                <div>
                    <h3>Net Price Engine</h3>
                    <p className="section-subtitle">Your Real Cost to Upgrade (Trade-in Estimates)</p>
                </div>
            </div>

            <div className="trade-in-grid">
                {report.upgrade_from.map((option, idx) => {
                    const deviceName = option?.device_name ?? "Unknown device";
                    const estVal = Number.isFinite(option?.estimated_value) ? option!.estimated_value : null;
                    const netVal = Number.isFinite(option?.net_price) ? option!.net_price : null;
                    const newPriceStr = (estVal !== null && netVal !== null)
                        ? `₦${(estVal + netVal).toLocaleString()}`
                        : "—";
                    const estStr = estVal !== null ? `₦${estVal.toLocaleString()}` : "—";
                    const netStr = netVal !== null ? `₦${netVal.toLocaleString()}` : "—";

                    return (
                        <div key={idx} className="trade-in-card">
                            <div className="trade-header">
                                <span className="trade-label">Trading In:</span>
                                <span className="trade-device">{deviceName}</span>
                            </div>

                            <div className="price-math">
                                <div className="math-row">
                                    <span>New Price:</span>
                                    <span className="price-value">{newPriceStr}</span>
                                </div>
                                <div className="math-row math-row-deduction">
                                    <span>- Your Device:</span>
                                    <span>({estStr})</span>
                                </div>
                            </div>

                            <div className="final-net-price">
                                <div className="net-label">YOU PAY</div>
                                <div className="net-amount">{netStr}</div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </section>
    );
};

export default NetPricePanel;
